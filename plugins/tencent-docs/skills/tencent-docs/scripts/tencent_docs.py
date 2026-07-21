#!/usr/bin/env python3
"""Minimal Tencent Docs OpenAPI client using Brain-projected credentials."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def load_config() -> dict:
    path = os.environ.get("TENCENT_DOCS_CONFIG")
    if not path:
        raise SystemExit("TENCENT_DOCS_CONFIG is not set; configure the Tencent Docs app in Brain")
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not data.get("client_id") or not data.get("access_token") or not data.get("open_id"):
        raise SystemExit("Tencent Docs connection is missing client_id, access_token, or open_id")
    return data


def json_object(value: str, label: str) -> dict:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{label} is not valid JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise SystemExit(f"{label} must be a JSON object")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(description="Call Tencent Docs OpenAPI")
    parser.add_argument("method", choices=["GET", "POST", "PUT", "PATCH", "DELETE"])
    parser.add_argument("path", help="API path beginning with /openapi/")
    parser.add_argument("--query", default="{}", help="JSON object encoded as query parameters")
    body = parser.add_mutually_exclusive_group()
    body.add_argument("--data", help="JSON request body")
    body.add_argument("--data-file", help="Path to a JSON request body")
    args = parser.parse_args()

    if not args.path.startswith("/openapi/") or "://" in args.path:
        raise SystemExit("path must begin with /openapi/ and must not be an absolute URL")

    config = load_config()
    query = urllib.parse.urlencode(json_object(args.query, "--query"), doseq=True)
    url = "https://docs.qq.com" + args.path + (f"?{query}" if query else "")
    payload = None
    if args.data is not None:
        payload = json.dumps(json_object(args.data, "--data"), ensure_ascii=False).encode()
    elif args.data_file is not None:
        raw = Path(args.data_file).read_text(encoding="utf-8")
        payload = json.dumps(json_object(raw, "--data-file"), ensure_ascii=False).encode()

    request = urllib.request.Request(
        url,
        data=payload,
        method=args.method,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Access-Token": config["access_token"],
            "Client-Id": config["client_id"],
            "Open-Id": config["open_id"],
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            content = response.read().decode("utf-8")
            if content:
                try:
                    print(json.dumps(json.loads(content), ensure_ascii=False, indent=2))
                except json.JSONDecodeError:
                    print(content)
            return 0
    except urllib.error.HTTPError as exc:
        message = exc.read().decode("utf-8", errors="replace")
        print(f"Tencent Docs API returned HTTP {exc.code}: {message}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"Tencent Docs API request failed: {exc.reason}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
