#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""运营调研报告 v0.3.0 —— 创建采集任务 + 内联轮询

POST /social-research-report，支持两种模式（由是否传 --user-prompt 决定）：
  - deferred（默认，不传 analysis）：先采集，停在 stage=awaiting_prompt，等 resume
    脚本补分析 Prompt 后再生成报告。契合「采集→确认结构→生成」主流程。
    ⚠️ deferred 靠「不传 analysis」实现；不要显式传 analysis:{prompt_mode:"deferred"}，
    服务端会 422 拒（已实测）。
  - custom（传 --user-prompt）：创建时带 analysis.user_prompt，服务端 capturing→
    analyzing→completed 一把梭，content 直返 Markdown。

本脚本建任务成功后立即开始内联轮询：deferred 期望停在 awaiting_prompt；custom 期望
跑到 completed 并直接吐报告正文。成功最后一行打印 task_id。退出码见 SKILL.md。
纯标准库。
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# --------------------------------------------------------------------------- 常量
DEFAULT_BASE_URL = "https://claw.lingyishuke.com/services"
API_PATH = "/api/v1/social-analytics/social-research-report"
REAL_PLATFORMS = ("douyin", "wx_video")  # 实采平台；xhs 仅兼容保留会被后端忽略
DEFAULT_CONTENT_LIMIT = 5
MIN_CONTENT_LIMIT = 1
MAX_CONTENT_LIMIT = 20
MAX_ACCOUNTS_TOTAL = 200   # douyin+wx_video 账号总数上限
MAX_KEYWORDS_TOTAL = 200   # douyin+wx_video 关键词总数上限

DEFAULT_POLL_INTERVAL = 10
DEFAULT_POLL_TIMEOUT = 2400

E_OK = 0
E_NO_KEY = 2
E_PARAM = 3
E_BALANCE = 4
E_AUTH = 8
E_4XX = 10
E_5XX = 11
E_FAILED = 12   # 任务失败终态
E_TIMEOUT = 13   # 轮询超时（非终态，可再调 poll）


# --------------------------------------------------------------------------- 工具
def log(msg):
    print("[create] %s" % msg, file=sys.stderr, flush=True)


def fail(code, msg):
    log("❌ " + msg)
    sys.exit(code)


def to_text(value):
    if isinstance(value, bytes):
        try:
            return value.decode("utf-8")
        except Exception:
            return value.decode("utf-8", "ignore")
    return value


def get_api_key():
    skill_dir = Path(__file__).resolve().parent.parent
    cfg = skill_dir / "config.json"
    if cfg.is_file():
        try:
            data = json.loads(cfg.read_text("utf-8"))
            if isinstance(data, dict) and data.get("LY_API_KEY"):
                return to_text(data["LY_API_KEY"]).strip()
        except Exception:
            pass
    return (
        os.environ.get("OPENCLAW_RELAY_API_KEY")
        or os.environ.get("LY_API_KEY")
        or ""
    )


def get_base_url():
    return os.environ.get("OPENCLAW_API_BASE", DEFAULT_BASE_URL).rstrip("/")


def normalize_text_list(value, field_name):
    """trim + 去空串 + 去重，保持顺序。"""
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("%s 必须是 JSON 数组" % field_name)
    result, seen = [], set()
    for item in value:
        text = to_text(item).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    return result


def normalize_limit(value, field_name):
    if value is None:
        return DEFAULT_CONTENT_LIMIT
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("%s 必须是整数" % field_name)
    if value < MIN_CONTENT_LIMIT or value > MAX_CONTENT_LIMIT:
        raise ValueError("%s 取值范围 %d-%d" % (field_name, MIN_CONTENT_LIMIT, MAX_CONTENT_LIMIT))
    return value


def normalize_platforms(raw_platforms):
    """归一化平台采集配置；返回可直接作为 payload 的 dict（对象形态，支持分平台差异化配额）。"""
    if not raw_platforms:
        raise ValueError("缺少采集平台：至少需要指定一个平台（douyin/wx_video）")

    result = {}
    accounts_total, keywords_total = 0, 0
    for raw_key, raw_config in raw_platforms.items():
        platform = to_text(raw_key).strip()
        if platform not in REAL_PLATFORMS:
            raise ValueError("不支持的平台 key: %s，目前仅支持 douyin、wx_video" % to_text(raw_key))
        if not isinstance(raw_config, dict):
            raise ValueError("%s 的配置必须是 JSON 对象" % to_text(raw_key))

        accounts = normalize_text_list(raw_config.get("accounts"), "%s.accounts" % raw_key)
        keywords = normalize_text_list(raw_config.get("keywords"), "%s.keywords" % raw_key)
        accounts_limit = normalize_limit(raw_config.get("accounts_content_limit"), "%s.accounts_content_limit" % raw_key)
        keywords_limit = normalize_limit(raw_config.get("keywords_content_limit"), "%s.keywords_content_limit" % raw_key)

        accounts_total += len(accounts)
        keywords_total += len(keywords)

        if accounts or keywords:
            result[platform] = {
                "accounts": accounts,
                "keywords": keywords,
                "accounts_content_limit": accounts_limit,
                "keywords_content_limit": keywords_limit,
            }

    if not result:
        raise ValueError("至少要给一个平台的有效账号或关键词（抖音/视频号）——采集源是必填项，缺了无法发起任务")
    if accounts_total > MAX_ACCOUNTS_TOTAL:
        raise ValueError("账号总数超过上限 %d" % MAX_ACCOUNTS_TOTAL)
    if keywords_total > MAX_KEYWORDS_TOTAL:
        raise ValueError("关键词总数超过上限 %d" % MAX_KEYWORDS_TOTAL)
    return result


def request_json(url, api_key, payload=None):
    if payload is None:
        req = urllib.request.Request(url)
    else:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(url, data=body)
        req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", api_key)
    req.add_header("X-Appbuilder-From", "openclaw")
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        status = getattr(resp, "code", None) or resp.getcode()
        raw = resp.read()
    except urllib.error.HTTPError as e:
        status = e.code
        raw = e.read() if hasattr(e, "read") else b""
    except urllib.error.URLError as e:
        raise RuntimeError("网络请求失败: %s" % to_text(str(e)))
    text = to_text(raw)
    try:
        data = json.loads(text) if text else {}
    except Exception:
        data = {"raw": text}
    return status, data


def compact_json(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


# 本次实际扣点的高置信字段（命中才直接报数；否则由调用方按规模估算并标"约"）
F_POINTS_USED = ("points_used", "credits_used", "used_points", "deducted_points",
                 "charged_points", "points_cost", "point_used", "consumed_points",
                 "billing_points", "spent_points", "cost_points")


def extract_points(payload):
    """从响应里提取本次实际扣点。只认明确表示「已用点数」的字段，找到返回数值，否则 None。"""
    if not isinstance(payload, dict):
        return None
    levels = [payload]
    inner = payload.get("data")
    if isinstance(inner, dict):
        levels.append(inner)
        for sub in ("billing", "result", "payment", "cost", "usage"):
            sub_obj = inner.get(sub)
            if isinstance(sub_obj, dict):
                levels.append(sub_obj)
    for sub in ("billing", "payment", "cost", "usage"):
        sub_obj = payload.get(sub)
        if isinstance(sub_obj, dict):
            levels.append(sub_obj)
    for level in levels:
        for key in F_POINTS_USED:
            if key in level:
                val = level[key]
                if isinstance(val, (int, float)) and not isinstance(val, bool):
                    return val
    return None


# --------------------------------------------------------------------------- 主流程
def read_user_prompt(arg_value, path_value):
    """user_prompt 可由命令行直接给，或由 --user-prompt-file 读文件（多行更稳）。"""
    if path_value:
        try:
            return Path(path_value).read_text("utf-8").strip()
        except Exception as e:
            raise ValueError("读取 user_prompt 文件失败：%s" % to_text(str(e)))
    return to_text(arg_value or "").strip()


def main():
    parser = argparse.ArgumentParser(description="创建 Social Research Report 采集任务")
    parser.add_argument("--brand", required=True, help="品牌名（必填）")
    parser.add_argument("--selling-points", default="", help="产品/品牌卖点（选填）")
    parser.add_argument("--background-context", default="", help="项目/公司背景、目标人群等上下文（选填，可多行）")
    parser.add_argument("--platforms-json", required=True, help='平台采集配置 JSON 对象，key ∈ {douyin, wx_video}')
    parser.add_argument("--output-format", default="markdown_text", choices=["markdown_text", "html_url"], help="输出格式，默认 markdown_text")
    parser.add_argument("--no-poll", action="store_true", help="只创建不内联轮询（默认会轮询到分叉点）")
    parser.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL, help="轮询间隔(秒)")
    parser.add_argument("--poll-timeout", type=int, default=DEFAULT_POLL_TIMEOUT, help="轮询总超时(秒)")
    # custom 一次性模式：传了 user_prompt 即 custom（创建时带分析Prompt，一把梭到 completed）
    parser.add_argument("--user-prompt", default="", help="分析 Prompt（传了即走 custom 一次性模式，创建后直接生成报告）")
    parser.add_argument("--user-prompt-file", default="", help="从文件读取分析 Prompt（与 --user-prompt 二选一，custom 模式）")
    args = parser.parse_args()

    api_key = get_api_key()
    if not api_key:
        log("未读取到 API Key")
        log("请前往 https://claw.lingyishuke.com/webapps/01claw-auth/index.html?source=workbuddy 取 key，写入技能目录 config.json 的 LY_API_KEY 字段后重试。")
        sys.exit(E_NO_KEY)

    brand = (args.brand or "").strip()
    if not brand:
        fail(E_PARAM, "brand 不能为空（采集必填字段缺失，不调用 API）")

    try:
        platforms_raw = json.loads(args.platforms_json) if args.platforms_json else {}
        if not isinstance(platforms_raw, dict):
            raise ValueError("platforms-json 必须是 JSON 对象")
        platforms = normalize_platforms(platforms_raw)
    except ValueError as e:
        fail(E_PARAM, "%s（采集必填字段缺失或非法，不调用 API）" % to_text(str(e)))
    except Exception as e:
        fail(E_PARAM, "platforms-json 解析失败：%s（不调用 API）" % to_text(str(e)))

    # ---- 组装 payload ----
    # deferred（默认）：不传 analysis；服务端采集完成后停在 stage=awaiting_prompt，等 resume 补分析 Prompt。
    #   ⚠️ 不要显式传 analysis:{prompt_mode:"deferred"}，服务端会 422 拒（已实测）。
    # custom：传 analysis:{user_prompt:...}；服务端 capturing→analyzing→completed 一次性出报告。
    user_prompt = ""
    try:
        user_prompt = read_user_prompt(args.user_prompt, args.user_prompt_file)
    except ValueError as e:
        fail(E_PARAM, to_text(str(e)))

    payload = {
        "brand": brand,
        "platforms": platforms,
        "output_format": args.output_format,
    }
    selling_points = to_text(args.selling_points).strip()
    background_context = to_text(args.background_context).strip()
    if selling_points:
        payload["selling_points"] = selling_points
    if background_context:
        payload["background_context"] = background_context
    if user_prompt:
        payload["analysis"] = {"user_prompt": user_prompt}
    # 无 user_prompt → 不传 analysis，即 deferred

    mode = "custom" if user_prompt else "deferred"
    log("创建任务（模式=%s）..." % mode)

    create_url = get_base_url() + API_PATH
    try:
        http_code, resp_json = request_json(create_url, api_key, payload)
    except RuntimeError as e:
        fail(E_5XX, to_text(str(e)))

    if http_code == 401:
        log("鉴权失败（401），key 失效或过期，请更新 config.json 后重试。")
        sys.exit(E_AUTH)
    if http_code == 402:
        log("余额不足（402），任务未提交。响应: %s" % compact_json(resp_json))
        sys.exit(E_BALANCE)
    if http_code == 400 or http_code == 422:
        fail(E_PARAM, "参数错误（HTTP %s，多为缺嵌套 platforms 或误带 prompt_mode）：%s" % (http_code, compact_json(resp_json)))
    if http_code >= 500:
        fail(E_5XX, "服务端错误（HTTP %s）：%s" % (http_code, compact_json(resp_json)))
    if http_code != 200:
        fail(E_4XX, "创建失败（HTTP %s）：%s" % (http_code, compact_json(resp_json)))

    code = resp_json.get("code") if isinstance(resp_json, dict) else None
    if code not in (200, 201):
        fail(E_4XX, "创建失败，业务码 code=%s：%s" % (to_text(str(code)), compact_json(resp_json)))

    data = resp_json.get("data") or {}
    task_id = data.get("task_id")
    if not task_id:
        fail(E_4XX, "响应中未获取到 task_id：%s" % compact_json(resp_json))

    log("✅ 任务已创建 task_id=%s stage=%s next_action=%s（模式=%s）"
        % (task_id, data.get("stage"), data.get("next_action"), mode))
    warning = data.get("warning_message")
    if warning:
        log("⚠️ warning: %s" % to_text(warning))

    if args.no_poll:
        log("（--no-poll 已指定，请用 poll_task.py 轮询）")
        print(task_id)
        return

    # ---- 内联轮询 ----
    # deferred 期望停在 awaiting_prompt；custom 期望跑到 completed/done。
    poll_loop(task_id, args.poll_interval, args.poll_timeout, mode)


def poll_loop(task_id, poll_interval, poll_timeout, mode="deferred", heartbeat=30):
    poll_url = get_base_url() + API_PATH + "/" + urllib.parse.quote(task_id, safe="")
    start_ts = int(time.time())
    last_stage = None
    last_heartbeat_ts = start_ts
    while True:
        try:
            http_code, resp_json = request_json(poll_url, get_api_key())
        except RuntimeError as e:
            log("❌ %s" % to_text(str(e)))
            print(task_id)
            sys.exit(E_5XX)

        if http_code == 401:
            log("鉴权失败（401）。")
            print(task_id); sys.exit(E_AUTH)
        if http_code == 404:
            log("任务不存在或不属于当前账号（404）。")
            print(task_id); sys.exit(E_4XX)
        if http_code >= 500:
            log("服务端错误（HTTP %s）：%s" % (http_code, compact_json(resp_json)))
            print(task_id); sys.exit(E_5XX)
        if http_code != 200:
            log("轮询失败（HTTP %s）：%s" % (http_code, compact_json(resp_json)))
            print(task_id); sys.exit(E_4XX)

        data = resp_json.get("data") if isinstance(resp_json, dict) else {}
        if not isinstance(data, dict):
            data = {}
        stage = data.get("stage") or ""
        next_action = data.get("next_action") or ""
        warning = data.get("warning_message")
        if warning:
            log("⚠️ warning: %s" % to_text(warning))

        now = int(time.time())
        if stage != last_stage:
            log("阶段 stage=%s next_action=%s" % (stage, next_action))
            last_stage = stage
            last_heartbeat_ts = now
        elif now - last_heartbeat_ts >= heartbeat:
            # 同一阶段持续期间打心跳，避免长时间静默像卡死
            log("⏳ 仍在 stage=%s 已运行 %ss，采集进行中，请稍候（可用 poll_task.py --once 实时查）"
                % (stage, now - start_ts))
            last_heartbeat_ts = now

        if next_action == "resume" or stage == "awaiting_prompt":
            # deferred 路径的正常分叉点：采集完成，等 resume 补分析 Prompt
            log("✅ 采集完成，任务暂停在 awaiting_prompt")
            log("（与用户对齐调研诉求写为 user_prompt → resume_task 推送 → 轮询到 completed）。详见 SKILL.md「采集后对齐」。")
            print(task_id)
            sys.exit(E_OK)

        if next_action == "done" or stage == "completed":
            content = to_text(data.get("content")) if data.get("content") else ""
            if mode == "custom":
                # custom 一把梭：直接吐报告正文，无需再单独 poll/resume
                log("✅ 报告生成完成（custom 模式）。")
                pts = extract_points(resp_json)
                pts_str = ""
                if pts is not None:
                    try:
                        f = float(pts)
                        pts_str = str(int(f)) if f.is_integer() else str(f)
                    except (TypeError, ValueError):
                        pts_str = str(pts)
                print("POINTS_USED=%s" % pts_str)
                out_format = data.get("output_format") or "markdown_text"
                if out_format == "html_url" and data.get("result_url"):
                    print("REPORT_URL=%s" % to_text(data.get("result_url")))
                else:
                    if not content:
                        log("⚠️ 任务标记完成但 content 为空（报告可能仍在落库，稍后用 poll_task.py 再轮询一次）。")
                    print("=== RESEARCH_REPORT_START ===")
                    print(content or "")
                    print("=== RESEARCH_REPORT_END ===")
            else:
                # deferred 路径罕见地未经 resume 直接完成
                log("⚠️ 任务已 completed（deferred 未经 resume 即完成）。请用 poll_task.py 读取 content。")
            print(task_id)
            sys.exit(E_OK)

        if next_action == "retry" or stage == "failed":
            err = data.get("error_message") or ""
            log("❌ 任务失败 stage=%s error=%s" % (stage, to_text(err)))
            print(task_id)
            sys.exit(E_FAILED)

        elapsed = int(time.time()) - start_ts
        if elapsed >= poll_timeout:
            log("⏰ 轮询超时（%ss），任务可能仍在运行，可运行 poll_task.py 继续等待。" % poll_timeout)
            print(task_id)
            sys.exit(E_TIMEOUT)

        time.sleep(poll_interval)


if __name__ == "__main__":
    main()
