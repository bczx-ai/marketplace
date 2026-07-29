#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""运营调研报告 v0.3.0 —— 重试失败任务

POST /social-research-report/{task_id}/retry（无 body），仅当 next_action=retry 时调用。
awaiting_prompt 状态不能 retry，应改走 resume。脚本据返回 stage 提示下一步。
成功最后一行打印 task_id。纯标准库。
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

DEFAULT_BASE_URL = "https://claw.lingyishuke.com/services"
API_PATH = "/api/v1/social-analytics/social-research-report"

E_OK = 0
E_NO_KEY = 2
E_PARAM = 3
E_BALANCE = 4
E_AUTH = 8
E_4XX = 10
E_5XX = 11


def log(msg):
    print("[retry] %s" % msg, file=sys.stderr, flush=True)


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


def request_json(url, api_key):
    req = urllib.request.Request(url, data=b"", method="POST")
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
    parser = argparse.ArgumentParser(description="重试 Social Research Report 失败任务")
    parser.add_argument("--task-id", required=True, help="任务 ID")
    parser.add_argument("--once", action="store_true",
                        help="重试后以 KV 形式吐出任务新状态（STAGE/NEXT_ACTION 等），便于非阻塞衔接 poll；默认仅 stderr 打状态、stdout 出 task_id")
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

    retry_url = get_base_url() + API_PATH + "/" + urllib.parse.quote(task_id, safe="") + "/retry"
    try:
        http_code, resp_json = request_json(retry_url, api_key)
    except RuntimeError as e:
        log("❌ %s" % to_text(str(e)))
        print(task_id)
        sys.exit(E_5XX)

    if http_code == 401:
        log("鉴权失败（401），key 失效或过期，请更新 config.json 后重试。")
        print(task_id); sys.exit(E_AUTH)
    if http_code == 402:
        log("余额不足（402）。响应: %s" % compact_json(resp_json))
        print(task_id); sys.exit(E_BALANCE)
    if http_code == 409:
        fail_msg = resp_json.get("message") if isinstance(resp_json, dict) else ""
        log("❌ 重试未被接受（409）：%s" % to_text(fail_msg))
        log("任务可能非 failed（awaiting_prompt 应改走 resume；其他状态请先 poll 确认）。")
        print(task_id); sys.exit(E_4XX)
    if http_code == 400 or http_code == 422:
        log("❌ 参数错误（HTTP %s）：%s" % (http_code, compact_json(resp_json)))
        print(task_id); sys.exit(E_PARAM)
    if http_code >= 500:
        log("❌ 服务端错误（HTTP %s）：%s" % (http_code, compact_json(resp_json)))
        print(task_id); sys.exit(E_5XX)
    if http_code != 200:
        log("❌ 重试失败（HTTP %s）：%s" % (http_code, compact_json(resp_json)))
        print(task_id); sys.exit(E_4XX)

    code = resp_json.get("code") if isinstance(resp_json, dict) else None
    if code not in (200, 201):
        log("❌ 重试失败，业务码 code=%s：%s" % (to_text(str(code)), compact_json(resp_json)))
        print(task_id); sys.exit(E_4XX)

    data = resp_json.get("data") or {}
    if not isinstance(data, dict):
        data = {}
    stage = data.get("stage") or ""
    next_action = data.get("next_action") or ""
    log("✅ 已发起重试 stage=%s next_action=%s" % (stage, next_action))
    if next_action == "resume" or stage == "awaiting_prompt":
        log("任务推进到 awaiting_prompt（采集已完成，需 resume 推分析 Prompt 继续生成报告）。")
    elif next_action == "poll":
        log("任务重新进入采集中，请运行 poll_task.py 继续等待。")
    elif next_action == "done":
        log("任务已完成，请运行 poll_task.py 读取 content。")

    if args.once:
        # KV 形式吐出重试后状态，便于非阻塞衔接后续 poll
        print("TASK_ID=%s" % task_id)
        print("STAGE=%s" % stage)
        print("NEXT_ACTION=%s" % next_action)
        print("STATUS=%s" % (data.get("status") or ""))
        warning = to_text(data.get("warning_message")) if data.get("warning_message") else ""
        print("WARNING=%s" % warning)
    print(task_id)
    return E_OK


if __name__ == "__main__":
    main()
