#!/usr/bin/env python3
"""
channel_detect 自测脚本

验证渠道探测逻辑在各种模拟环境下的输出是否正确。
不需要真实安装任何客户端，通过模拟环境变量即可验证。

用法：
    python3 test_channel_detect.py

预期输出：全部 PASS
"""

import os
import sys
import importlib.util


def load_channel_detect():
    """从同目录加载 channel_detect 模块"""
    spec = importlib.util.spec_from_file_location(
        "channel_detect",
        os.path.join(os.path.dirname(__file__), "channel_detect.py"),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def set_env(updates: dict):
    """设置环境变量，返回原始值的备份"""
    backup = {}
    for k, v in updates.items():
        backup[k] = os.environ.get(k)
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    return backup


def restore_env(backup: dict):
    """恢复环境变量"""
    for k, v in backup.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v


def run_case(name: str, env_updates: dict, expected: str, mod) -> bool:
    """运行单个测试用例"""
    backup = set_env(env_updates)
    try:
        result = mod.resolve_user_agent()
        status = "PASS" if result == expected else "FAIL"
        if status == "FAIL":
            print(f"  [{status}] {name}")
            print(f"         期望: {expected}")
            print(f"         实际: {result}")
        else:
            print(f"  [{status}] {name} → {result}")
        return status == "PASS"
    finally:
        restore_env(backup)


def main():
    mod = load_channel_detect()

    # 保存原始环境，测试结束后恢复
    # 注意：我们无法完美隔离当前进程的真实环境变量，
    # 所以策略是：先清除所有相关变量，再按用例设置

    # 动态收集所有需要清除的变量（包括真实环境中已存在的）
    prefixes = ("WORKBUDDY_", "OPENCLAW_", "QCLAW_", "ADP_", "CODEBUDDY_", "__CFBundleIdentifier", "HOSTNAME")
    channels_to_clear = []
    for k in list(os.environ.keys()):
        if any(k.startswith(p) or k == p for p in prefixes):
            channels_to_clear.append(k)

    # 备份并清除
    backup = {}
    for k in channels_to_clear:
        backup[k] = os.environ.get(k)
        os.environ.pop(k, None)

    passed = 0
    failed = 0

    print("=" * 60)
    print("channel_detect 自测")
    print("=" * 60)

    # --- 测试用例 ---

    cases = [
        # 1. WorkBuddy（通过 WORKBUDDY_APP_NAME）
        ("WorkBuddy via WORKBUDDY_APP_NAME",
         {"WORKBUDDY_APP_NAME": "WorkBuddy"},
         "skill-workbuddy"),

        # 2. WorkBuddy（通过 __CFBundleIdentifier）
        ("WorkBuddy via CFBundleIdentifier",
         {"__CFBundleIdentifier": "com.workbuddy.workbuddy"},
         "skill-workbuddy"),

        # 3. WorkBuddy 优先于 CodeBuddy（关键！内嵌内核场景）
        ("WorkBuddy 优先于 CodeBuddy（内嵌内核）",
         {"WORKBUDDY_APP_NAME": "WorkBuddy",
          "CODEBUDDY_COPILOT_INTERNET_ENVIRONMENT": "iOA"},
         "skill-workbuddy"),

        # 4. CodeBuddy
        ("CodeBuddy via CODEBUDDY_",
         {"CODEBUDDY_COPILOT_INTERNET_ENVIRONMENT": "iOA"},
         "skill-codebuddy"),

        # 5. CodeBuddy via bundle
        ("CodeBuddy via CFBundleIdentifier",
         {"__CFBundleIdentifier": "com.tencent.codebuddycn"},
         "skill-codebuddy"),

        # 6. OpenClaw
        ("OpenClaw via OPENCLAW_",
         {"OPENCLAW_CLI": "1", "OPENCLAW_STATE_DIR": "/tmp/.openclaw"},
         "skill-openclaw"),

        # 7. QClaw
        ("QClaw via QCLAW_",
         {"QCLAW_DEVICE_ID": "test", "QCLAW_USER_DATA_DIR": "/tmp/qclaw"},
         "skill-qclaw"),

        # 7b. QClaw 优先于 OpenClaw（关键！QClaw 内嵌 OpenClaw 运行时）
        ("QClaw 优先于 OpenClaw（内嵌运行时）",
         {"QCLAW_DEVICE_ID": "test",
          "OPENCLAW_CLI": "1", "OPENCLAW_STATE_DIR": "/tmp/.qclaw"},
         "skill-qclaw"),

        # 7c. QClaw via CFBundleIdentifier
        ("QClaw via CFBundleIdentifier",
         {"__CFBundleIdentifier": "com.tencent.qclaw"},
         "skill-qclaw"),

        # 8. ADP —— 云端容器，多特征联合指纹（HOSTNAME + KERNEL_SERVICE + CODE_SQUID）
        ("ADP via 多环境变量指纹",
         {"HOSTNAME": "kernel-d4d45b685-zvppg",
          "KERNEL_SERVICE_HOST": "9.165.67.141",
          "CODE_SQUID_PROXY_SERVICE_HOST": "9.165.64.196"},
         "skill-adp"),

        # 8b. ADP —— 只有 HOSTNAME=kernel-* 不应误判
        ("ADP 单一 HOSTNAME 不误判",
         {"HOSTNAME": "kernel-d4d45b685-zvppg"},
         "skillother"),

        # 8c. ADP —— 进程树强特征命中
        ("ADP via 进程树指纹",
         {},
         "skill-adp"),

        # 9. 未识别 → skillother
        #     注意：在真实客户端环境里运行时，进程树兜底会命中，
        #     所以这里临时 mock _proc_tree_cmdline 返回空串
        ("未识别平台 → skillother",
         {},
         "skillother"),

        # 10. 显式传参覆盖（人工指定任意值）
        ("人工传参覆盖",
         {"CODEBUDDY_COPILOT_INTERNET_ENVIRONMENT": "iOA"},
         "my-custom-value"),  # 传了 cli_value="my-custom-value"
    ]

    for name, env_updates, expected in cases:
        if "人工传参" in name:
            backup2 = set_env(env_updates)
            result = mod.resolve_user_agent("my-custom-value")
            status = "PASS" if result == expected else "FAIL"
            if status == "FAIL":
                print(f"  [{status}] {name}")
                print(f"         期望: {expected}")
                print(f"         实际: {result}")
            else:
                print(f"  [{status}] {name} → {result}")
            restore_env(backup2)
            if status == "PASS":
                passed += 1
            else:
                failed += 1
        elif "ADP 单一 HOSTNAME" in name:
            # mock 进程树为空，验证单一 HOSTNAME=kernel-* 不会误判 ADP
            backup2 = set_env(env_updates)
            orig_proc = mod._proc_tree_cmdline
            mod._proc_tree_cmdline = lambda: ""
            result = mod.resolve_user_agent()
            mod._proc_tree_cmdline = orig_proc
            status = "PASS" if result == expected else "FAIL"
            if status == "FAIL":
                print(f"  [{status}] {name}")
                print(f"         期望: {expected}")
                print(f"         实际: {result}")
            else:
                print(f"  [{status}] {name} → {result}")
            restore_env(backup2)
            if status == "PASS":
                passed += 1
            else:
                failed += 1
        elif "ADP via 进程树" in name:
            # mock ADP 实测进程树：codeinterpreter.kernel.launcher + kernel_gunicorn_conf + /data/taurus/
            backup2 = set_env(env_updates)
            orig_proc = mod._proc_tree_cmdline
            mod._proc_tree_cmdline = lambda: "python3 -m codeinterpreter.kernel.launcher gunicorn -c python:kernel_gunicorn_conf server_main:flask_app /data/taurus/venv"
            result = mod.resolve_user_agent()
            mod._proc_tree_cmdline = orig_proc
            status = "PASS" if result == expected else "FAIL"
            if status == "FAIL":
                print(f"  [{status}] {name}")
                print(f"         期望: {expected}")
                print(f"         实际: {result}")
            else:
                print(f"  [{status}] {name} → {result}")
            restore_env(backup2)
            if status == "PASS":
                passed += 1
            else:
                failed += 1
        elif "未识别" in name:
            # mock 进程树返回空串，避免真实环境干扰
            backup2 = set_env(env_updates)
            orig_proc = mod._proc_tree_cmdline
            mod._proc_tree_cmdline = lambda: ""
            result = mod.resolve_user_agent()
            mod._proc_tree_cmdline = orig_proc
            status = "PASS" if result == expected else "FAIL"
            if status == "FAIL":
                print(f"  [{status}] {name}")
                print(f"         期望: {expected}")
                print(f"         实际: {result}")
            else:
                print(f"  [{status}] {name} → {result}")
            restore_env(backup2)
            if status == "PASS":
                passed += 1
            else:
                failed += 1
        else:
            if run_case(name, env_updates, expected, mod):
                passed += 1
            else:
                failed += 1

    # 恢复原始环境
    restore_env(backup)

    print("-" * 60)
    print(f"结果: {passed} PASS, {failed} FAIL / 共 {passed + failed} 用例")
    print("=" * 60)

    if failed > 0:
        print("\n❌ 有失败的用例，请检查 channel_detect.py 的探测逻辑")
        sys.exit(1)
    else:
        print("\n✅ 全部通过")
        sys.exit(0)


if __name__ == "__main__":
    main()
