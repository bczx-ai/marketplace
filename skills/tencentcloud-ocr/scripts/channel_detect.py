#!/usr/bin/env python3
"""
Skill 调用渠道自动探测模块

在各 AI 平台中运行 Skill 时，自动探测当前平台并返回标准化标识：
- skill-workbuddy
- skill-codebuddy
- skill-adp
- skill-openclaw
- skill-qclaw
- skillother（未识别）

供腾讯云 SDK 的 ClientProfile.request_client 使用，最终落到
ES 日志的 requestClient 字段和计费上报的 Source 字段。

用法：
    from channel_detect import resolve_user_agent
    client_profile.request_client = resolve_user_agent()

或带显式覆盖：
    client_profile.request_client = resolve_user_agent(cli_value)

设计原则：
- 零依赖：不引入任何第三方库（psutil 可选，有则用，无则降级 ps）
- 异常安全：任何失败一律回退 "skillother"，绝不影响主业务
- 向前兼容：显式传参仍原样使用
"""

import os

# 默认调用来源标识（未识别到具体平台时使用）
DEFAULT_USER_AGENT = "skillother"


def _proc_tree_cmdline() -> str:
    """
    回溯进程树，返回各级进程 cmdline 拼接的小写字符串（用于平台探测兜底）。

    skill 脚本永远是调用方客户端拉起的子进程，父进程命令行必含客户端标识。
    本函数异常安全：任何失败一律返回空串，绝不影响主流程。
    """
    try:
        import psutil  # type: ignore

        parts, proc = [], psutil.Process(os.getpid())
        for _ in range(15):
            if proc is None:
                break
            try:
                parts.append(" ".join(proc.cmdline()) or proc.name())
            except Exception:
                pass
            try:
                proc = proc.parent()
            except Exception:
                break
        return " ".join(parts).lower()
    except Exception:
        pass

    # 兜底：POSIX 环境用 ps 逐级回溯（带超时，避免阻塞主流程）
    if os.name == "posix":
        try:
            import subprocess

            parts, pid = [], os.getpid()
            for _ in range(15):
                # Python 3.6 兼容：不使用 capture_output/text（3.7+ 才支持）
                out = subprocess.run(
                    ["ps", "-o", "ppid=,args=", "-p", str(pid)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    timeout=2,
                ).stdout.strip()
                if not out:
                    break
                seg = out.split(None, 1)
                parts.append(seg[1] if len(seg) > 1 else "")
                ppid = seg[0]
                if ppid in ("0", "1", str(pid)):
                    break
                pid = int(ppid)
            return " ".join(parts).lower()
        except Exception:
            return ""
    return ""


def detect_channel() -> str:
    """
    探测当前 skill 被哪个平台调用，返回平台标识；无法识别时返回空串。

    返回值（与 resolve_user_agent 配合使用）：
    - "workbuddy"  → skill-workbuddy
    - "qclaw"      → skill-qclaw
    - "openclaw"   → skill-openclaw
    - "adp"        → skill-adp
    - "codebuddy"  → skill-codebuddy
    - ""           → skillother（兜底）

    判定顺序按"特异性从高到低"，绝不可调换：
    - WorkBuddy 内嵌 CodeBuddy 内核，也会注入 CODEBUDDY_* 变量，必须最先判定。
    - QClaw 内嵌 OpenClaw 运行时，也会注入 OPENCLAW_* 变量，必须在 OpenClaw 前判定。
    - 主判据用环境变量；环境变量未命中时用进程树 cmdline 回溯兜底。

    本函数异常安全：任何失败一律返回空串，绝不影响主业务。
    """
    try:
        env = os.environ
        bundle = env.get("__CFBundleIdentifier", "")

        # 1) WorkBuddy —— 特异性最高（内嵌 CodeBuddy 内核，同样带 CODEBUDDY_* 变量）
        if (
            "WORKBUDDY_APP_NAME" in env
            or "WORKBUDDY_CONFIG_DIR" in env
            or bundle == "com.workbuddy.workbuddy"
            or env.get("CODEBUDDY_HOST") == "workbuddy-desktop"
        ):
            return "workbuddy"

        # 2) QClaw —— 内嵌 OpenClaw 运行时，同样带 OPENCLAW_* 变量，必须在 OpenClaw 前判定
        #    实测指纹：QCLAW_* 环境变量、__CFBundleIdentifier=com.tencent.qclaw
        if (
            any(k.startswith("QCLAW_") for k in env)
            or bundle == "com.tencent.qclaw"
        ):
            return "qclaw"

        # 3) OpenClaw（此时已排除 QClaw）
        if any(k.startswith("OPENCLAW_") for k in env):
            return "openclaw"

        # 4) ADP —— 云端容器执行，使用多特征联合指纹，避免单一 HOSTNAME 误判
        #    实测指纹：HOSTNAME=kernel-*、KERNEL_SERVICE_HOST、CODE_SQUID_PROXY_SERVICE_HOST、
        #    进程树含 codeinterpreter.kernel.launcher / kernel_gunicorn_conf / /data/taurus/
        if _is_adp_environment(env, ""):
            return "adp"

        # 5) CodeBuddy（此时已排除 WorkBuddy）
        if any(k.startswith("CODEBUDDY_") for k in env) or bundle == "com.tencent.codebuddycn":
            return "codebuddy"

        # 6) 环境变量未命中 → 进程树 cmdline 兜底（同样按特异性排序）
        blob = _proc_tree_cmdline()
        if "workbuddy.app" in blob or "com.workbuddy" in blob:
            return "workbuddy"
        if "qclaw.app" in blob or "com.tencent.qclaw" in blob:
            return "qclaw"
        if "openclaw" in blob:
            return "openclaw"
        if _is_adp_environment(env, blob):
            return "adp"
        if "codebuddy cn.app" in blob or "@tencent-ai/codebuddy-code" in blob:
            return "codebuddy"
    except Exception:
        pass
    return ""


def _is_adp_environment(env, proc_blob: str) -> bool:
    """
    ADP 云端代码解释器环境的多特征联合指纹。

    不使用单一 HOSTNAME=kernel-* 直接判定，避免普通 K8s / Notebook 容器误判。
    实测 ADP 指纹至少会同时命中多个特征：
    - 环境变量：HOSTNAME=kernel-*、KERNEL_SERVICE_HOST、CODE_SQUID_PROXY_SERVICE_HOST、COS_UTIL_SERVICE_HOST
    - 进程树：codeinterpreter.kernel.launcher、kernel_gunicorn_conf、server_main:flask_app、/data/taurus/
    """
    score = 0
    hostname = env.get("HOSTNAME", "")
    if hostname.startswith("kernel-"):
        score += 1
    if "KERNEL_SERVICE_HOST" in env:
        score += 1
    if "CODE_SQUID_PROXY_SERVICE_HOST" in env:
        score += 1
    if "COS_UTIL_SERVICE_HOST" in env:
        score += 1

    blob = proc_blob.lower() if proc_blob else ""
    if "codeinterpreter.kernel" in blob:
        score += 2
    if "kernel_gunicorn_conf" in blob:
        score += 2
    if "server_main:flask_app" in blob:
        score += 1
    if "/data/taurus/" in blob:
        score += 1

    return score >= 3


def resolve_user_agent(cli_value: str = None) -> str:
    """
    解析最终的调用来源标识（request_client），优先级：
    1. 显式参数 cli_value（人工可覆盖，原样使用，保证向后兼容）
    2. 自动探测到的平台 → "skill-<platform>"
    3. 默认 "skillother"（未识别平台时）
    """
    if cli_value:
        return cli_value
    channel = detect_channel()
    return f"skill-{channel}" if channel else DEFAULT_USER_AGENT
