#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""运营调研报告 v0.3.0 —— 推送分析 Prompt 继续生成报告

POST /social-research-report/{task_id}/resume，把「用户确认后的分析 Prompt」作为
user_prompt 提交（接口API.md §6 契约 body 为 {"user_prompt": "..."}），触发服务端
基于「采集到的素材 + 分析 Prompt」生成最终调研报告。

门②兜底：user_prompt 非空才发请求，否则退出码 3 不发请求。成功后再次轮询直至
completed（content 直返 Markdown）。最后一行打印 task_id。纯标准库。
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

DEFAULT_BASE_URL = "https://claw.lingyishuke.com/services"
API_PATH = "/api/v1/social-analytics/social-research-report"
DEFAULT_POLL_INTERVAL = 10
DEFAULT_POLL_TIMEOUT = 2400

E_OK = 0
E_NO_KEY = 2
E_PARAM = 3
E_BALANCE = 4
E_AUTH = 8
E_4XX = 10
E_5XX = 11
E_FAILED = 12
E_TIMEOUT = 13


def log(msg):
    print("[resume] %s" % msg, file=sys.stderr, flush=True)


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
    return os.environ.get("OPENCLAW_RELAY_API_KEY") or os.environ.get("LY_API_KEY") or ""


def get_base_url():
    return os.environ.get("OPENCLAW_API_BASE", DEFAULT_BASE_URL).rstrip("/")


def compact_json(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def read_user_prompt(arg_value, path_value):
    if path_value:
        try:
            text = Path(path_value).read_text("utf-8")
        except Exception as e:
            raise ValueError("读取分析 Prompt 文件失败：%s" % to_text(str(e)))
        return text.strip()
    return to_text(arg_value or "").strip()


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


def main():
    parser = argparse.ArgumentParser(description="推送分析 Prompt 继续生成报告（resume）")
    parser.add_argument("--task-id", required=True, help="任务 ID")
    parser.add_argument("--user-prompt", default="", help="用户确认后的分析 Prompt（与 --user-prompt-file 二选一）")
    parser.add_argument("--user-prompt-file", default="", help="从文件读取分析 Prompt（推荐，多行更稳）")
    parser.add_argument("--no-poll", action="store_true", help="只推 resume 不内联轮询（默认会轮询到 completed）")
    parser.add_argument("--interval", type=int, default=DEFAULT_POLL_INTERVAL)
    parser.add_argument("--timeout", type=int, default=DEFAULT_POLL_TIMEOUT)
    args = parser.parse_args()

    api_key = get_api_key()
    if not api_key:
        log("未读取到 API Key")
        log("请前往 https://claw.lingyishuke.com/webapps/01claw-auth/index.html?source=workbuddy 取 key，写入 config.json 后重试。")
        sys.exit(E_NO_KEY)

    task_id = (args.task_id or "").strip()
    if not task_id:
        log("task_id 不能为空")
        sys.exit(E_PARAM)

    # ---- 门②兜底：user_prompt 非空才发请求 ----
    try:
        user_prompt = read_user_prompt(args.user_prompt, args.user_prompt_file)
    except ValueError as e:
        log("❌ %s" % to_text(str(e)))
        sys.exit(E_PARAM)
    if not user_prompt:
        log("❌ user_prompt 为空（报告生成所需字段缺失，不调用 resume）")
        log("请先与用户对齐调研诉求，写成文件后用 --user-prompt-file 提交。详见 SKILL.md「采集后对齐」。")
        sys.exit(E_PARAM)

    resume_url = get_base_url() + API_PATH + "/" + urllib.parse.quote(task_id, safe="") + "/resume"
    try:
        http_code, resp_json = request_json(resume_url, api_key, {"user_prompt": user_prompt})
    except RuntimeError as e:
        log("❌ %s" % to_text(str(e)))
        print(task_id)
        sys.exit(E_5XX)

    if http_code == 401:
        log("鉴权失败（401），key 失效或过期，请更新 config.json 后重试。")
        print(task_id); sys.exit(E_AUTH)
    if http_code == 402:
        log("余额不足（402），任务未提交。响应: %s" % compact_json(resp_json))
        print(task_id); sys.exit(E_BALANCE)
    if http_code == 409:
        fail_msg = resp_json.get("message") if isinstance(resp_json, dict) else ""
        log("❌ 继续请求未被接受（409）：%s" % to_text(fail_msg))
        log("任务可能不处于 awaiting_prompt（已采集未确认结构 / 已 resume / 已完成）。请先 poll 确认状态。")
        print(task_id); sys.exit(E_4XX)
    if http_code == 400 or http_code == 422:
        log("❌ 参数错误（HTTP %s）：%s" % (http_code, compact_json(resp_json)))
        print(task_id); sys.exit(E_PARAM)
    if http_code >= 500:
        log("❌ 服务端错误（HTTP %s）：%s" % (http_code, compact_json(resp_json)))
        print(task_id); sys.exit(E_5XX)
    if http_code != 200:
        log("❌ 继续失败（HTTP %s）：%s" % (http_code, compact_json(resp_json)))
        print(task_id); sys.exit(E_4XX)

    code = resp_json.get("code") if isinstance(resp_json, dict) else None
    if code not in (200, 201):
        log("❌ 继续失败，业务码 code=%s：%s" % (to_text(str(code)), compact_json(resp_json)))
        print(task_id); sys.exit(E_4XX)

    data = resp_json.get("data") or {}
    stage = data.get("stage") or ""
    next_action = data.get("next_action") or ""
    log("✅ 已提交分析 Prompt，stage=%s next_action=%s" % (stage, next_action))

    if args.no_poll:
        log("（--no-poll 已指定，请运行 poll_task.py 轮询至完成）")
        print(task_id)
        return E_OK

    # ---- 内联轮询直到 completed ----
    poll_loop(task_id, args.interval, args.timeout)


def poll_loop(task_id, poll_interval, poll_timeout, heartbeat=30):
    poll_url = get_base_url() + API_PATH + "/" + urllib.parse.quote(task_id, safe="")
    start_ts = int(time.time())
    last_stage = None
    last_heartbeat_ts = start_ts
    while True:
        try:
            http_code, resp_json = request_json(poll_url, get_api_key())
        except RuntimeError as e:
            log("❌ %s" % to_text(str(e)))
            print(task_id); sys.exit(E_5XX)

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
            log("⏳ 仍在 stage=%s 已运行 %ss，报告生成中，请稍候（可用 poll_task.py --once 实时查）"
                % (stage, now - start_ts))
            last_heartbeat_ts = now

        if next_action == "done" or stage == "completed":
            content = to_text(data.get("content")) if data.get("content") else ""
            out_format = data.get("output_format") or "markdown_text"
            log("✅ 报告生成完成 output_format=%s" % out_format)
            # 透出本次实际扣点（服务端若返回）；为空时由调用方按采集规模估算并标"约"
            pts = extract_points(resp_json)
            pts_str = ""
            if pts is not None:
                try:
                    f = float(pts)
                    pts_str = str(int(f)) if f.is_integer() else str(f)
                except (TypeError, ValueError):
                    pts_str = str(pts)
            print("POINTS_USED=%s" % pts_str)
            if out_format == "html_url" and data.get("result_url"):
                print("REPORT_URL=%s" % to_text(data.get("result_url")))
            else:
                if not content:
                    log("⚠️ 任务标记完成但 content 为空（报告可能仍在落库，稍后再 poll 一次）。")
                print("=== RESEARCH_REPORT_START ===")
                print(content or "")
                print("=== RESEARCH_REPORT_END ===")
            print(task_id)
            return E_OK

        if next_action == "retry" or stage == "failed":
            err = data.get("error_message") or ""
            log("❌ 报告生成失败 stage=%s error=%s" % (stage, to_text(err)))
            log("失败响应: %s" % compact_json(resp_json))
            print(task_id); sys.exit(E_FAILED)

        if next_action == "resume" or stage == "awaiting_prompt":
            log("⚠️ 任务仍停留在 awaiting_prompt（resume 未生效？）。请检查后重试。")
            print(task_id); sys.exit(E_4XX)

        elapsed = int(time.time()) - start_ts
        if elapsed >= poll_timeout:
            log("⏰ 报告生成轮询超时（%ss），任务可能仍在运行，可运行 poll_task.py 继续等待。" % poll_timeout)
            print(task_id); sys.exit(E_TIMEOUT)

        time.sleep(poll_interval)


if __name__ == "__main__":
    main()
