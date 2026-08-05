#!/usr/bin/env python3
"""检查运行环境，并按用户授权保存可选的本地写作偏好。"""

import argparse
import json
import platform
import shutil
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
PROFILE_PATH = SKILL_ROOT / "config" / "user_profile.json"
ENV_STATE_PATH = SKILL_ROOT / "config" / "environment_state.json"
SCRIPTS_DIR = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def load_environment_state():
    if not ENV_STATE_PATH.exists():
        return {}
    try:
        with ENV_STATE_PATH.open("r", encoding="utf-8") as state_file:
            state = json.load(state_file)
        return state if isinstance(state, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def save_environment_state(state):
    ENV_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with ENV_STATE_PATH.open("w", encoding="utf-8") as state_file:
        json.dump(state, state_file, ensure_ascii=False, indent=2)


def check_environment():
    state = load_environment_state()
    python3_available = shutil.which("python3") is not None
    python_docx_available = _module_available("docx")
    requests_available = _module_available("requests")
    blocking_issues = []
    if not python3_available:
        blocking_issues.append("python3_missing")
    if not python_docx_available:
        blocking_issues.append("python_docx_missing")
    if not requests_available:
        blocking_issues.append("requests_missing")
    return {
        "python": platform.python_version(),
        "python3_available": python3_available,
        "python_docx": python_docx_available,
        "requests": requests_available,
        "config_ini": (SKILL_ROOT / "config.ini").exists(),
        "font_note": "Word 文档会写入公文常用字体名称；打开端如缺少对应字体，Word/WPS 可能自动替换，需以本机打开后的显示为准。",
        "blocking_issues": blocking_issues,
        "ready": not blocking_issues,
        "dependency_install_prompt_needed": bool(blocking_issues) and not state.get("dependency_install_declined"),
        "install_hint": "经用户同意后，可执行 python3 -m pip install python-docx requests" if blocking_issues else None,
        "environment_state": {
            "dependency_install_declined": bool(state.get("dependency_install_declined")),
        },
    }


def _module_available(module_name):
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


def main():
    parser = argparse.ArgumentParser(description="深知写作助手初始化与环境检查")
    parser.add_argument("--organization", help="常用发文机关；不填写则使用 XX单位")
    parser.add_argument("--doc-prefix", help="常用发文字号前缀；不填写则使用 XX")
    parser.add_argument("--region", help="常用搜索地域；不填写则按任务询问")
    parser.add_argument("--print-unit", help="常用印发单位")
    parser.add_argument("--save", action="store_true", help="经用户授权后，将所填设置仅保存到本机")
    parser.add_argument("--decline-dependency-install", action="store_true", help="记录用户已拒绝依赖安装提示，后续不再反复询问")
    parser.add_argument("--reset-environment-prompts", action="store_true", help="清除依赖安装提示的拒绝记录")
    args = parser.parse_args()

    state = load_environment_state()
    if args.reset_environment_prompts:
        state.pop("dependency_install_declined", None)
    if args.decline_dependency_install:
        state["dependency_install_declined"] = True
    if args.reset_environment_prompts or args.decline_dependency_install:
        save_environment_state(state)

    if args.save:
        profile = {
            "organization": args.organization or "",
            "doc_prefix": args.doc_prefix or "",
            "region": args.region or "",
            "print_unit": args.print_unit or "",
        }
        PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with PROFILE_PATH.open("w", encoding="utf-8") as profile_file:
            json.dump(profile, profile_file, ensure_ascii=False, indent=2)

    result = check_environment()
    result["profile_saved"] = args.save
    result["profile_path"] = "config/user_profile.json" if args.save else None
    result["environment_state_path"] = "config/environment_state.json"
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
