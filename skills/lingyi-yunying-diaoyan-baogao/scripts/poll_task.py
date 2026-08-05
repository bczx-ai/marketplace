#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""社媒运营调研报告 v0.6.0 —— 轮询：阻塞模式 + 单次查询模式

GET /social-research-report/{task_id}，按 data.next_action 决定出路：
  poll   → 继续轮询（stderr 打印阶段进度 + 心跳）
  resume → awaiting_prompt，本轮停止：等待对齐调研诉求后跑 resume_task 推 user_prompt
  retry  → 任务失败，本轮停止（退出码 12），提示可调 retry
  done   → 任务完成，本轮停止：吐出报告正文(markdown)/url(html)

两种模式：
  --once          单次查询：只 GET 一次，把状态以机器可读 KV 吐到 stdout 后立即退出（不阻塞）。
                  供 skill 周期性主动查状态、在等待间隙向用户同步进度，避免长时间静默像"卡死"。
  （默认）阻塞模式 反复轮询直到分叉点/终态/超时，期间 stderr 打印阶段变化与心跳。

输出协议（stdout，供 skill 解析）：
  --once 模式（每行一个 KV，便于非阻塞解析）：
    TASK_ID=<id>
    STAGE=<capturing|analyzing|awaiting_prompt|completed|failed|...>
    NEXT_ACTION=<poll|resume|retry|done|...>
    STATUS=<底层状态>
    WARNING=<非阻断警告，可能为空>
    ERROR=<失败原因，可能为空>
    CONTENT_EMPTY=<true|false>          # 仅 stage=completed 时有意义
    POINTS_USED=<本次扣点，可能为空>      # 服务端若返回
    REPORT_URL=<url，仅 html_url 形态>
    === RESEARCH_REPORT_START === <报告正文> === RESEARCH_REPORT_END ===  # 仅 completed 且非空时出现
    <最后一行 task_id>
  阻塞模式：进度走 stderr；完成后吐 POINTS_USED= / RESEARCH_REPORT 块 / 最后一行 task_id。
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

DEFAULT_BASE_URL = "https://claw.lingyishuke.com/services"
API_PATH = "/api/v1/social-analytics/social-research-report"
DEFAULT_POLL_INTERVAL = 10
DEFAULT_POLL_TIMEOUT = 2400
DEFAULT_HEARTBEAT = 30  # 同一 stage 停留超过此秒数时，定期打心跳到 stderr，避免静默

E_OK = 0
E_NO_KEY = 2
E_PARAM = 3
E_BALANCE = 4
E_AUTH = 8
E_4XX = 10
E_5XX = 11
E_FAILED = 12
E_TIMEOUT = 13

REPORT_START = "=== RESEARCH_REPORT_START ==="
REPORT_END = "=== RESEARCH_REPORT_END ==="


def log(msg):
    print("[poll] %s" % msg, file=sys.stderr, flush=True)


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


# 本次实际扣点的高置信字段（命中才报数；否则由调用方按规模估算并标"约"）
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


def request_json(url, api_key):
    req = urllib.request.Request(url)
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


def extract_report(data):
    """从 completed 响应里取最终报告：markdown_text 读 content，html_url 读 result_url。"""
    if not isinstance(data, dict):
        return "", "", ""
    out_format = data.get("output_format") or "markdown_text"
    content = data.get("content")
    result_url = data.get("result_url")
    if out_format == "html_url":
        return "url", to_text(result_url) if result_url else "", out_format
    return "markdown", to_text(content) if content else "", out_format


def emit_block(start, end, body):
    print(start)
    print(body if body else "")
    print(end)


def poll_once(task_id, api_key, resp_json=None, http_code=None, err=None):
    """单次查询模式：把任务状态以机器可读 KV 吐到 stdout 后返回（不阻塞、不循环）。
    resp_json/http_code 可由调用方传入；若为 None 则自行 GET 一次。
    返回退出码：0 正常拿到状态（含 failed，只要查到了）/ 对应错误码。
    """
    print("TASK_ID=%s" % task_id)
    if err:
        print("STAGE=unknown")
        print("NEXT_ACTION=poll")
        print("ERROR=%s" % to_text(err)[:500])
        print(task_id)
        return E_5XX

    # HTTP 错误码以 KV 形式透出，便于 skill 决策（如 401→换key、404→任务不存在）
    if http_code == 401:
        print("STAGE=unknown"); print("NEXT_ACTION=poll"); print("ERROR=鉴权失败（401），key 失效或过期")
        print(task_id); return E_AUTH
    if http_code == 404:
        print("STAGE=unknown"); print("NEXT_ACTION="); print("ERROR=任务不存在或不属于当前账号（404）")
        print(task_id); return E_4XX
    if http_code == 402:
        print("STAGE=unknown"); print("NEXT_ACTION="); print("ERROR=余额不足（402）")
        print(task_id); return E_BALANCE
    if http_code >= 500:
        print("STAGE=unknown"); print("NEXT_ACTION=poll")
        print("ERROR=服务端错误（HTTP %s），任务可能仍存活，建议稍后重试查询" % http_code)
        print(task_id); return E_5XX
    if http_code != 200:
        print("STAGE=unknown"); print("NEXT_ACTION=poll")
        print("ERROR=查询失败（HTTP %s）" % http_code)
        print(task_id); return E_4XX

    data = resp_json.get("data") if isinstance(resp_json, dict) else None
    if not isinstance(data, dict):
        data = {}
    stage = data.get("stage") or ""
    next_action = data.get("next_action") or ""
    status = data.get("status") or ""
    warning = to_text(data.get("warning_message")) if data.get("warning_message") else ""
    error = to_text(data.get("error_message")) if data.get("error_message") else ""

    print("STAGE=%s" % stage)
    print("NEXT_ACTION=%s" % next_action)
    print("STATUS=%s" % status)
    print("WARNING=%s" % warning)
    print("ERROR=%s" % error)

    pts = extract_points(resp_json)
    pts_str = ""
    if pts is not None:
        try:
            f = float(pts)
            pts_str = str(int(f)) if f.is_integer() else str(f)
        except (TypeError, ValueError):
            pts_str = str(pts)
    print("POINTS_USED=%s" % pts_str)

    # completed 时附带 content（可能为空，skill 据此判断报告落库是否完成）
    if stage == "completed" or next_action == "done":
        kind, body, out_format = extract_report(data)
        print("CONTENT_EMPTY=%s" % ("true" if not body else "false"))
        if kind == "url" and body:
            print("REPORT_URL=%s" % body)
        elif body:
            print(REPORT_START)
            print(body)
            print(REPORT_END)
        else:
            # content 为空：报告可能仍在落库，skill 可稍后再 --once 取一次
            pass
    print(task_id)
    if stage == "failed" or next_action == "retry":
        return E_FAILED
    return E_OK


def main():
    parser = argparse.ArgumentParser(description="轮询 Social Research Report 任务")
    parser.add_argument("--task-id", required=True, help="任务 ID")
    parser.add_argument("--interval", type=int, default=None, help="轮询间隔(秒)")
    parser.add_argument("--timeout", type=int, default=None, help="轮询总超时(秒)")
    parser.add_argument("--heartbeat", type=int, default=None, help="同一阶段心跳间隔(秒)")
    parser.add_argument("--once", action="store_true", help="单次查询模式：只查一次并以 KV 吐状态，不阻塞轮询")
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

    poll_interval = args.interval if args.interval is not None else int(os.environ.get("POLL_INTERVAL_SECONDS", str(DEFAULT_POLL_INTERVAL)))
    poll_timeout = args.timeout if args.timeout is not None else int(os.environ.get("POLL_TIMEOUT_SECONDS", str(DEFAULT_POLL_TIMEOUT)))
    heartbeat = args.heartbeat if args.heartbeat is not None else DEFAULT_HEARTBEAT

    poll_url = get_base_url() + API_PATH + "/" + urllib.parse.quote(task_id, safe="")

    # ---- 单次查询模式 ----
    if args.once:
        try:
            http_code, resp_json = request_json(poll_url, api_key)
        except RuntimeError as e:
            sys.exit(poll_once(task_id, api_key, err=to_text(str(e))))
        sys.exit(poll_once(task_id, api_key, resp_json=resp_json, http_code=http_code))

    # ---- 阻塞轮询模式 ----
    start_ts = int(time.time())
    last_stage = None
    last_stage_ts = start_ts
    last_heartbeat_ts = start_ts

    while True:
        try:
            http_code, resp_json = request_json(poll_url, api_key)
        except RuntimeError as e:
            # 网络瞬时抖动：不立即判死，提示 skill 可用 poll --once 复查任务是否仍存活
            log("⚠️ 网络异常：%s（任务可能仍在服务端运行，可用 poll --once 复查）" % to_text(str(e)))
            print(task_id)
            sys.exit(E_5XX)

        if http_code == 401:
            log("鉴权失败（401），key 失效或过期，请更新 config.json 后重试。")
            print(task_id); sys.exit(E_AUTH)
        if http_code == 404:
            log("任务不存在或不属于当前账号（404）。")
            print(task_id); sys.exit(E_4XX)
        if http_code >= 500:
            log("服务端错误（HTTP %s）：%s（任务可能仍存活，稍后可用 poll --once 复查）" % (http_code, compact_json(resp_json)))
            print(task_id); sys.exit(E_5XX)
        if http_code != 200:
            log("轮询失败（HTTP %s）：%s" % (http_code, compact_json(resp_json)))
            print(task_id); sys.exit(E_4XX)

        if isinstance(resp_json, dict) and "code" in resp_json:
            code = resp_json.get("code")
            if code not in (200, 201):
                log("轮询失败，业务码 code=%s：%s" % (to_text(str(code)), compact_json(resp_json)))
                print(task_id); sys.exit(E_4XX)

        data = resp_json.get("data") if isinstance(resp_json, dict) else None
        if not isinstance(data, dict):
            data = {}
        stage = data.get("stage") or ""
        next_action = data.get("next_action") or ""
        status = data.get("status") or ""
        warning = data.get("warning_message")
        if warning:
            log("⚠️ warning: %s" % to_text(warning))

        now = int(time.time())
        # stage 变化：打一行
        if stage != last_stage:
            log("阶段 stage=%s status=%s next_action=%s" % (stage, status, next_action))
            last_stage = stage
            last_stage_ts = now
            last_heartbeat_ts = now
        # 同一 stage 停留超过心跳间隔：打心跳，避免长时间静默像卡死
        elif now - last_heartbeat_ts >= heartbeat:
            elapsed = now - start_ts
            log("⏳ 仍在 stage=%s 已运行 %ss，任务进行中，请稍候（可用 --once 实时查）" % (stage, elapsed))
            last_heartbeat_ts = now

        if next_action == "resume" or stage == "awaiting_prompt":
            log("✅ 采集完成，任务暂停在 awaiting_prompt，等待确认报告结构。")
            print(task_id)
            sys.exit(E_OK)

        if next_action == "done" or stage == "completed":
            kind, body, out_format = extract_report(data)
            log("✅ 报告生成完成 output_format=%s" % out_format)
            pts = extract_points(resp_json)
            pts_str = ""
            if pts is not None:
                try:
                    f = float(pts)
                    pts_str = str(int(f)) if f.is_integer() else str(f)
                except (TypeError, ValueError):
                    pts_str = str(pts)
            print("POINTS_USED=%s" % pts_str)
            if kind == "url":
                print("REPORT_URL=%s" % body)
            else:
                if not body:
                    log("⚠️ 任务标记完成但 content 为空（报告可能仍在落库，稍后再 poll 一次）。")
                emit_block(REPORT_START, REPORT_END, body)
            print(task_id)
            sys.exit(E_OK)

        if next_action == "retry" or stage == "failed":
            err = data.get("error_message") or ""
            log("❌ 任务失败 stage=%s error=%s（可调 retry_task 重试，复用已采集数据）" % (stage, to_text(err)))
            log("失败响应: %s" % compact_json(resp_json))
            print(task_id)
            sys.exit(E_FAILED)

        # next_action == "poll" 或未知 → 继续轮询
        elapsed = int(time.time()) - start_ts
        if elapsed >= poll_timeout:
            log("⏰ 轮询超时（%ss），任务可能仍在运行（非失败），可用 poll --once 复查或带 task_id 再阻塞轮询一次。" % poll_timeout)
            print(task_id)
            sys.exit(E_TIMEOUT)

        time.sleep(poll_interval)


if __name__ == "__main__":
    main()
