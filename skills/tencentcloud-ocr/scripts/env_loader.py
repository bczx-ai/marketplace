#!/usr/bin/env python3
"""
腾讯云 API 密钥统一加载模块。

环境变量读取优先级（从高到低）：
1. 系统环境变量（os.environ）—— 显式 export 的优先级最高，不被覆盖
2. .env 文件 —— 从脚本所在目录逐级向上查找，找到的第一个生效

支持的 .env 格式：
    TENCENTCLOUD_SECRET_ID=AKIDxxxxxxxxxxxx
    TENCENTCLOUD_SECRET_KEY=xxxxxxxxxxxx
    TENCENTCLOUD_ENDPOINT=ocr.tencentcloudapi.com

若以上两处均未提供 TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY，
则打印明确提示引导用户设置，并退出。

用法：
    from env_loader import validate_env, get_endpoint
    secret_id, secret_key = validate_env()
    endpoint = get_endpoint()
"""

import os
import sys

# 必填环境变量
REQUIRED_SECRET_ID = "TENCENTCLOUD_SECRET_ID"
REQUIRED_SECRET_KEY = "TENCENTCLOUD_SECRET_KEY"

# OCR 服务默认端点（线上环境）
DEFAULT_ENDPOINT = "ocr.tencentcloudapi.com"


def _find_env_file() -> str:
    """
    从脚本所在目录逐级向上查找 .env 文件，最多向上 5 级。

    查找范围：
    - scripts/             （脚本所在目录）
    - tencentcloud-ocr-xx/ （skill 根目录）
    - workspace_root/      （工作区根目录，.env 通常放在这里）

    返回找到的第一个 .env 的绝对路径，找不到返回空串。
    本函数异常安全：任何失败一律返回空串，绝不影响主流程。
    """
    try:
        current = os.path.dirname(os.path.abspath(__file__))
        for _ in range(5):
            env_path = os.path.join(current, ".env")
            if os.path.isfile(env_path):
                return env_path
            parent = os.path.dirname(current)
            if parent == current:
                break
            current = parent
    except Exception:
        pass
    return ""


def _parse_env_file(path: str) -> dict:
    """
    解析 .env 文件，返回键值对字典。

    支持：
    - KEY=VALUE 格式
    - 值两端的引号（单引号/双引号）自动去除
    - # 开头的注释行跳过
    - 空行跳过
    - 值中可包含 = 号（以第一个 = 为分隔符）

    本函数异常安全：任何失败一律返回空字典。
    """
    result = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip()
                # 去除值两端的引号（单引号或双引号）
                if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                    value = value[1:-1]
                if key:
                    result[key] = value
    except Exception:
        pass
    return result


def _ensure_env_loaded() -> None:
    """
    将 .env 文件中的变量加载到 os.environ。

    优先级：系统环境变量 > .env 文件。
    仅当 os.environ 中不存在该 key 或值为空时，才从 .env 设置。
    这样既不覆盖用户显式设置的有效值，也能兜底平台注入空字符串的情况。
    幂等：多次调用安全，不会重复加载。
    """
    env_path = _find_env_file()
    if not env_path:
        return
    for key, value in _parse_env_file(env_path).items():
        if not os.environ.get(key):
            os.environ[key] = value


def validate_env() -> tuple:
    """
    校验并返回腾讯云 API 密钥。

    先加载 .env 文件（不覆盖已有系统环境变量），再从 os.environ 读取。
    若密钥缺失，打印明确提示并 sys.exit(1)。

    返回: (secret_id, secret_key)
    """
    _ensure_env_loaded()

    secret_id = os.environ.get(REQUIRED_SECRET_ID)
    secret_key = os.environ.get(REQUIRED_SECRET_KEY)

    if not secret_id or not secret_key:
        env_path = _find_env_file()
        if env_path:
            hint = f"已找到 .env 文件({env_path})，但缺少必需的密钥配置"
        else:
            hint = "未找到 .env 文件"

        missing = []
        if not secret_id:
            missing.append(REQUIRED_SECRET_ID)
        if not secret_key:
            missing.append(REQUIRED_SECRET_KEY)

        print(
            f"错误: {hint}\n"
            f"缺失变量: {', '.join(missing)}\n"
            f"\n"
            f"请通过以下任一方式提供腾讯云 API 密钥：\n"
            f"  方式1 - 在项目根目录创建 .env 文件：\n"
            f"    TENCENTCLOUD_SECRET_ID=你的SecretId\n"
            f"    TENCENTCLOUD_SECRET_KEY=你的SecretKey\n"
            f"  方式2 - 在终端设置环境变量：\n"
            f"    export TENCENTCLOUD_SECRET_ID='你的SecretId'\n"
            f"    export TENCENTCLOUD_SECRET_KEY='你的SecretKey'\n"
            f"  方式3 - 直接提供密钥，由调用方写入 .env 或环境变量\n",
            file=sys.stderr,
        )
        sys.exit(1)

    return secret_id, secret_key


def get_endpoint() -> str:
    """
    获取 OCR 服务端点地址。

    优先级：系统环境变量 > .env 文件 > 默认值(ocr.tencentcloudapi.com)
    """
    _ensure_env_loaded()
    return os.environ.get("TENCENTCLOUD_ENDPOINT", DEFAULT_ENDPOINT)
