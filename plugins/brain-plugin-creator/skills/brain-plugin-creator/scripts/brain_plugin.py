#!/usr/bin/env python3
"""Create and validate Brain-native marketplace plugins with the Python stdlib."""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


SLUG = re.compile(r"^[a-z0-9]+(?:[._-][a-z0-9]+)*$")
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
SHA256 = re.compile(r"^[a-f0-9]{64}$")
CLI_ENV = re.compile(r"^[A-Z][A-Z0-9_]{1,63}$")
CLI_COMMAND = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
MAX_CLI_SIZE = 128 * 1024 * 1024
CLI_TARGETS = {"darwin-arm64", "darwin-x64", "linux-arm64", "linux-x64", "win32-x64"}
ARCHIVE_ENTRY = re.compile(r"^[A-Za-z0-9._+-]+(?:/[A-Za-z0-9._+-]+)*$")
AUTH_KINDS = {"oauth2", "oauth2_pkce", "mcp_oauth", "cli_oauth", "api_key", "none"}
OAUTH_PARAMETERS = re.compile(r"^[A-Za-z][A-Za-z0-9._~-]{0,127}$")
RESERVED_OAUTH_PARAMETERS = {"client_id", "redirect_uri", "response_type", "state", "code_challenge", "code_challenge_method"}
FORBIDDEN_CLI_ENVS = {
    "COLORTERM", "COMSPEC", "HOME", "LANG", "LC_ALL", "LC_CTYPE", "PATH",
    "PATHEXT", "SHELL", "TERM", "TMP", "TEMP", "TMPDIR", "USER",
}
FORBIDDEN_CLI_ENV_PREFIXES = (
    "BRAIN_", "CLAUDE_", "CODEX_", "DYLD_", "ELECTRON_", "GIT_", "LD_",
    "NODE_", "NPM_", "PYTHON", "SSH_",
)
ALLOWED_COMPONENTS = {
    "agents",
    "skills",
    "commands",
    "apps",
    "appTemplates",
    "assets",
    "hooks",
    "rules",
    "mcp",
    "cli",
}
ALLOWED_ROOTS = {
    ".codex-plugin",
    ".claude-plugin",
    "brain.json",
    "agents",
    "skills",
    "commands",
    "apps",
    "app-templates",
    "assets",
    "hooks",
    "rules",
    "mcp",
    "LICENSE",
    "CHANGELOG.md",
}


class PluginError(Exception):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise PluginError(f"缺少文件: {path}") from error
    except json.JSONDecodeError as error:
        raise PluginError(f"JSON 格式错误: {path}: {error}") from error
    if not isinstance(value, dict):
        raise PluginError(f"JSON 顶层必须是对象: {path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(content)
        os.chmod(temporary, path.stat().st_mode & 0o777 if path.exists() else 0o644)
        os.replace(temporary, path)
    except Exception:
        Path(temporary).unlink(missing_ok=True)
        raise


def require_slug(value: str, label: str) -> None:
    if len(value) > 128 or not SLUG.fullmatch(value):
        raise PluginError(f"{label} 必须是小写稳定 slug: {value}")


def require_text(value: str, label: str, maximum: int) -> None:
    if not value.strip() or len(value) > maximum:
        raise PluginError(f"{label} 必须是 1-{maximum} 个字符")


def safe_relative(value: str, label: str) -> Path:
    normalized = value.replace("\\", "/")
    if normalized.startswith("/") or ".." in normalized.split("/"):
        raise PluginError(f"{label} 必须是包内相对路径: {value}")
    return Path(normalized.removeprefix("./"))


def catalog_entry(name: str, category: str, claude: bool = False) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "name": name,
        "source": {"source": "local", "path": f"./plugins/{name}"},
    }
    if not claude:
        entry.update(
            category=category,
            policy={"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        )
    return entry


def append_catalog(catalog: dict[str, Any], entry: dict[str, Any], path: Path) -> None:
    plugins = catalog.get("plugins")
    if not isinstance(catalog.get("name"), str) or not isinstance(plugins, list):
        raise PluginError(f"Marketplace catalog 顶层格式不合法: {path}")
    name = entry["name"]
    if any(isinstance(item, dict) and item.get("name") == name for item in plugins):
        raise PluginError(f"Marketplace catalog 已存在 {name}: {path}")
    plugins.append(entry)


def starter_skill(name: str, display_name: str, description: str) -> str:
    quoted = json.dumps(description, ensure_ascii=False)
    return (
        f"---\nname: {name}\ndescription: {quoted}\n---\n\n"
        f"# {display_name}\n\n"
        f"根据用户请求完成与 {display_name} 有关的工作。先读取项目约束和现有实现，"
        "复用项目工具，并在交付前运行最小相关校验。\n"
    )


def create_plugin(args: argparse.Namespace) -> Path:
    root = args.marketplace_root.expanduser().resolve()
    name = args.name
    require_slug(name, "Plugin name")
    require_slug(args.publisher_id, "publisherId")
    if not SEMVER.fullmatch(args.version):
        raise PluginError(f"version 必须是 SemVer: {args.version}")
    require_text(args.display_name, "displayName", 128)
    require_text(args.description, "description", 512)
    require_text(args.author, "author", 256)
    require_text(args.category, "category", 128)
    require_text(args.brain_compatibility, "brain compatibility", 128)

    catalogs: list[tuple[Path, dict[str, Any], dict[str, Any]]] = []
    for path, claude in [
        (root / ".agents/plugins/marketplace.json", False),
        (root / ".claude-plugin/marketplace.json", True),
    ]:
        if not path.is_file():
            continue
        original = load_json(path)
        updated = copy.deepcopy(original)
        append_catalog(updated, catalog_entry(name, args.category, claude=claude), path)
        catalogs.append((path, original, updated))
    if not catalogs:
        raise PluginError("Marketplace 未找到 Codex 或 Claude catalog")

    plugin_root = root / "plugins" / name
    if plugin_root.exists():
        raise PluginError(f"Plugin 目录已存在: {plugin_root}")

    manifest = {
        "name": name,
        "version": args.version,
        "description": args.description,
        "author": {"name": args.author},
        "skills": "./skills" if not args.without_skill else None,
        "interface": {
            "displayName": args.display_name,
            "shortDescription": args.description,
            "longDescription": args.description,
            "developerName": args.author,
            "category": args.category,
            "capabilities": ["Skills"] if not args.without_skill else [],
        },
    }
    manifest = {key: value for key, value in manifest.items() if value is not None}
    brain = {
        "$schema": "https://brain.zhonganinfo.com/schemas/plugin-extension/v1.json",
        "schemaVersion": 1,
        "publisherId": args.publisher_id,
        "compatibility": {"brain": args.brain_compatibility},
        "components": {
            "skills": [{"key": name}]
        } if not args.without_skill else {},
    }

    written_catalogs: list[tuple[Path, dict[str, Any]]] = []
    try:
        write_json(plugin_root / ".codex-plugin/plugin.json", manifest)
        write_json(plugin_root / ".claude-plugin/plugin.json", manifest)
        write_json(plugin_root / "brain.json", brain)
        if not args.without_skill:
            skill_path = plugin_root / "skills" / name / "SKILL.md"
            skill_path.parent.mkdir(parents=True, exist_ok=True)
            skill_path.write_text(
                starter_skill(name, args.display_name, args.description),
                encoding="utf-8",
            )
        for path, original, updated in catalogs:
            write_json(path, updated)
            written_catalogs.append((path, original))
    except Exception as error:
        shutil.rmtree(plugin_root, ignore_errors=True)
        try:
            for path, original in reversed(written_catalogs):
                write_json(path, original)
        except OSError as rollback_error:
            raise PluginError(f"创建失败且 catalog 回滚失败: {rollback_error}") from error
        raise

    print(f"已创建 {plugin_root}")
    return plugin_root


def expect_file(root: Path, candidates: list[str], label: str, errors: list[str]) -> None:
    if not any((root / candidate).is_file() for candidate in candidates):
        errors.append(f"{label} 缺少实现文件: {' 或 '.join(candidates)}")


def named_components(
    root: Path,
    components: dict[str, Any],
    key: str,
    candidates: Any,
    errors: list[str],
) -> None:
    values = components.get(key, [])
    if not isinstance(values, list):
        errors.append(f"components.{key} 必须是数组")
        return
    for item in values:
        if not isinstance(item, dict) or not isinstance(item.get("key"), str):
            errors.append(f"components.{key} 条目必须包含 key")
            continue
        name = item["key"]
        if not SLUG.fullmatch(name):
            errors.append(f"components.{key} key 不是 slug: {name}")
            continue
        requires = item.get("requires", [])
        if not isinstance(requires, list) or not all(isinstance(value, str) for value in requires):
            errors.append(f"components.{key}.{name}.requires 必须是字符串数组")
        expect_file(root, candidates(name), f"components.{key}.{name}", errors)


def validate_cli(components: dict[str, Any], source_scope: str, errors: list[str]) -> None:
    values = components.get("cli", [])
    if not isinstance(values, list):
        errors.append("components.cli 必须是数组")
        return
    for item in values:
        if not isinstance(item, dict):
            errors.append("components.cli 条目必须是对象")
            continue
        key, command, targets = item.get("key"), item.get("command"), item.get("targets")
        if not isinstance(key, str) or not SLUG.fullmatch(key):
            errors.append("components.cli.key 必须是 slug")
        if not isinstance(command, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", command):
            errors.append(f"components.cli.{key}.command 不合法")
        if not isinstance(targets, dict) or not targets:
            errors.append(f"components.cli.{key}.targets 不能为空")
            continue
        for target, artifact in targets.items():
            if target not in CLI_TARGETS:
                errors.append(f"components.cli.{key} target 不支持: {target}")
                continue
            if not isinstance(artifact, dict):
                errors.append(f"components.cli.{key}.{target} 必须是对象")
                continue
            if set(artifact) - {"file", "url", "size", "sha256", "archive"}:
                errors.append(f"components.cli.{key}.{target} 包含未知字段")
            file_name = artifact.get("file")
            url = artifact.get("url", "")
            parsed = urlparse(url if isinstance(url, str) else "")
            if not isinstance(file_name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", file_name):
                errors.append(f"components.cli.{key}.{target}.file 不合法")
            if target == "win32-x64" and isinstance(file_name, str) and not file_name.lower().endswith((".exe", ".cmd", ".bat")):
                errors.append(f"components.cli.{key}.{target}.file 扩展名不支持")
            allowed_schemes = {"https"} if source_scope == "public" else {"http", "https"}
            if parsed.scheme not in allowed_schemes or not parsed.hostname or parsed.username or parsed.password or parsed.fragment:
                schemes = "HTTPS" if source_scope == "public" else "HTTP 或 HTTPS"
                errors.append(f"components.cli.{key}.{target}.url 必须是无凭据、无 fragment 的 {schemes} URL")
            size = artifact.get("size")
            if type(size) is not int or not 0 < size <= MAX_CLI_SIZE:
                errors.append(f"components.cli.{key}.{target}.size 必须是 1-{MAX_CLI_SIZE} 的整数")
            if not isinstance(artifact.get("sha256"), str) or not SHA256.fullmatch(artifact["sha256"]):
                errors.append(f"components.cli.{key}.{target}.sha256 不合法")
            archive = artifact.get("archive")
            if archive is not None:
                if not isinstance(archive, dict) or set(archive) != {"format", "entry"}:
                    errors.append(f"components.cli.{key}.{target}.archive 不合法")
                elif (archive.get("format") not in {"tar.gz", "zip"}
                      or not isinstance(archive.get("entry"), str)
                      or not ARCHIVE_ENTRY.fullmatch(archive["entry"])
                      or any(segment in {".", ".."} for segment in archive["entry"].split("/"))):
                    errors.append(f"components.cli.{key}.{target}.archive 格式或入口不合法")


def validate_app_template(path: Path, errors: list[str]) -> None:
    try:
        template = load_json(path)
    except PluginError as error:
        errors.append(str(error))
        return
    auth = template.get("auth")
    if not isinstance(auth, dict) or auth.get("kind") not in AUTH_KINDS:
        errors.append(f"{path} auth.kind 不支持")
        return
    fields = template.get("fields")
    if not isinstance(fields, list):
        errors.append(f"{path} fields 必须是数组")
        return
    field_types: dict[str, str] = {}
    for field in fields:
        if not isinstance(field, dict) or not isinstance(field.get("key"), str) or not isinstance(field.get("type"), str):
            errors.append(f"{path} field 必须包含 key 和 type")
            continue
        field_types[field["key"]] = field["type"]
    oauth = auth["kind"] in {"oauth2", "oauth2_pkce", "mcp_oauth"}
    if oauth:
        if not (isinstance(auth.get("authorizationEndpoint"), str) or field_types.get(auth.get("authorizationEndpointField")) == "url"):
            errors.append(f"{path} OAuth 授权地址未声明")
        if not (isinstance(auth.get("tokenEndpoint"), str) or field_types.get(auth.get("tokenEndpointField")) == "url"):
            errors.append(f"{path} OAuth Token 地址未声明")
        if field_types.get(auth.get("clientIdField")) != "text":
            errors.append(f"{path} OAuth clientIdField 必须引用 text 字段")
        client_secret_field = auth.get("clientSecretField")
        if client_secret_field is not None and field_types.get(client_secret_field) != "secret":
            errors.append(f"{path} OAuth clientSecretField 必须引用 secret 字段")
        if auth.get("tokenMethod", "POST") not in {"GET", "POST"}:
            errors.append(f"{path} OAuth tokenMethod 只支持 GET 或 POST")
        parameters = auth.get("authorizationParams", {})
        if not isinstance(parameters, dict) or len(parameters) > 32:
            errors.append(f"{path} OAuth authorizationParams 不合法")
        else:
            for key, value in parameters.items():
                if not isinstance(key, str) or not OAUTH_PARAMETERS.fullmatch(key) or key in RESERVED_OAUTH_PARAMETERS:
                    errors.append(f"{path} OAuth 授权参数 {key} 不合法")
                if not isinstance(value, str) or not value.strip() or len(value) > 1024:
                    errors.append(f"{path} OAuth 授权参数 {key} 的值不合法")
    elif "authorizationParams" in auth or auth.get("tokenMethod", "POST") != "POST":
        errors.append(f"{path} OAuth 参数只适用于 OAuth App")
    if auth["kind"] != "cli_oauth":
        if "configDirEnv" in auth or "commands" in auth:
            errors.append(f"{path} CLI 登录配置只适用于 cli_oauth")
        return
    env = auth.get("configDirEnv")
    if not isinstance(env, str) or not CLI_ENV.fullmatch(env):
        errors.append(f"{path} cli_oauth.configDirEnv 不合法")
    elif env in FORBIDDEN_CLI_ENVS or env.startswith(FORBIDDEN_CLI_ENV_PREFIXES):
        errors.append(f"{path} cli_oauth.configDirEnv 不安全")
    commands = auth.get("commands")
    if not isinstance(commands, list) or not 1 <= len(commands) <= 4:
        errors.append(f"{path} cli_oauth.commands 必须包含 1-4 条命令")
        return
    for index, command in enumerate(commands):
        label = f"{path} cli_oauth.commands[{index}]"
        if not isinstance(command, dict) or not isinstance(command.get("command"), str) or not CLI_COMMAND.fullmatch(command["command"]):
            errors.append(f"{label}.command 不合法")
            continue
        arguments = command.get("args", [])
        if not isinstance(arguments, list) or len(arguments) > 64:
            errors.append(f"{label}.args 不合法")
        else:
            for argument in arguments:
                if isinstance(argument, str):
                    if not argument or len(argument) > 2048 or "\0" in argument:
                        errors.append(f"{label}.args 包含不合法固定参数")
                    continue
                if not isinstance(argument, dict) or set(argument) != {"valueFrom"} or not isinstance(argument["valueFrom"], str):
                    errors.append(f"{label}.args 动态参数格式不合法")
                    continue
                source = argument["valueFrom"]
                key = source.removeprefix("config.")
                if not source.startswith("config.") or field_types.get(key) in {None, "secret", "string_list"}:
                    errors.append(f"{label}.args 引用了不允许的来源 {source}")
        stdin_from = command.get("stdinFrom")
        if stdin_from is not None:
            key = stdin_from.removeprefix("secret.") if isinstance(stdin_from, str) else ""
            if not isinstance(stdin_from, str) or not stdin_from.startswith("secret.") or field_types.get(key) != "secret":
                errors.append(f"{label}.stdinFrom 必须引用 secret 字段")
        timeout = command.get("timeoutSeconds", 600)
        if type(timeout) is not int or not 10 <= timeout <= 600:
            errors.append(f"{label}.timeoutSeconds 必须是 10-600 的整数")


def validate_catalog(root: Path, name: str, errors: list[str]) -> None:
    expected = f"./plugins/{name}"
    found = 0
    for relative, is_codex in [
        (".agents/plugins/marketplace.json", True),
        (".claude-plugin/marketplace.json", False),
    ]:
        path = root / relative
        if not path.is_file():
            continue
        found += 1
        try:
            catalog = load_json(path)
        except PluginError as error:
            errors.append(str(error))
            continue
        plugins = catalog.get("plugins")
        if not isinstance(catalog.get("name"), str) or not isinstance(plugins, list):
            errors.append(f"catalog 顶层格式不合法: {relative}")
            continue
        matches = [item for item in plugins if isinstance(item, dict) and item.get("name") == name]
        if len(matches) != 1:
            errors.append(f"{relative} 必须且只能包含一个 {name} 条目")
            continue
        entry = matches[0]
        source = entry.get("source")
        if source != {"source": "local", "path": expected}:
            errors.append(f"{relative} 的 {name} source 必须指向 {expected}")
        if is_codex:
            policy = entry.get("policy")
            if not isinstance(entry.get("category"), str) or not entry["category"]:
                errors.append(f"{relative} 的 {name} 缺少 category")
            if policy != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
                errors.append(f"{relative} 的 {name} policy 不完整")
    if not found:
        errors.append("Marketplace 未找到 Codex 或 Claude catalog")


def validate_plugin(
    plugin_root: Path,
    marketplace_root: Path | None = None,
    source_scope: str = "public",
) -> None:
    source_root = plugin_root.expanduser()
    if source_root.is_symlink():
        raise PluginError(f"Plugin 根目录不能是 symlink: {source_root}")
    root = source_root.resolve()
    errors: list[str] = []
    name = root.name
    if not SLUG.fullmatch(name):
        errors.append(f"Plugin 目录名必须是 slug: {name}")

    for path in root.rglob("*"):
        if path.is_symlink():
            errors.append(f"Plugin 包不能包含 symlink: {path.relative_to(root)}")
    for path in root.iterdir() if root.is_dir() else []:
        if path.name not in ALLOWED_ROOTS:
            errors.append(f"Plugin 根目录包含不支持的内容: {path.name}")

    codex_path = root / ".codex-plugin/plugin.json"
    claude_path = root / ".claude-plugin/plugin.json"
    codex = load_json(codex_path) if codex_path.is_file() else None
    claude = load_json(claude_path) if claude_path.is_file() else None
    if codex is None and claude is None:
        raise PluginError("Plugin 缺少 .codex-plugin/plugin.json 或 .claude-plugin/plugin.json")
    manifest = codex if codex is not None else claude
    assert manifest is not None
    brain = load_json(root / "brain.json")

    if codex is not None and claude is not None and codex.get("name") != claude.get("name"):
        errors.append("Codex 与 Claude Plugin manifest name 不一致")
    if manifest.get("name") != name:
        errors.append("Plugin 目录名与 manifest name 不一致")
    if not isinstance(manifest.get("version"), str) or not SEMVER.fullmatch(manifest["version"]):
        errors.append("Brain 原生 Plugin version 必须是 SemVer")
    if not isinstance(manifest.get("description"), str) or not manifest["description"].strip():
        errors.append("Plugin manifest 缺少 description")

    if set(brain) - {"$schema", "schemaVersion", "publisherId", "releaseNotes", "compatibility", "components"}:
        errors.append("brain.json 包含未知顶层字段")
    if brain.get("schemaVersion") != 1:
        errors.append("brain.json schemaVersion 必须为 1")
    if not isinstance(brain.get("publisherId"), str) or not SLUG.fullmatch(brain["publisherId"]):
        errors.append("brain.json publisherId 必须是 slug")
    components = brain.get("components")
    if not isinstance(components, dict):
        errors.append("brain.json components 必须是对象")
        components = {}
    unknown = set(components) - ALLOWED_COMPONENTS
    if unknown:
        errors.append(f"brain.json 包含未知组件: {', '.join(sorted(unknown))}")

    named_components(root, components, "agents", lambda key: [f"agents/{key}.md", f"agents/{key}/AGENT.md"], errors)
    named_components(root, components, "skills", lambda key: [f"skills/{key}/SKILL.md"], errors)
    named_components(root, components, "commands", lambda key: [f"commands/{key}.md", f"commands/{key}.toml"], errors)
    named_components(root, components, "apps", lambda key: [f"apps/{key}/app.json"], errors)
    named_components(root, components, "hooks", lambda key: [f"hooks/{key}.json"], errors)
    named_components(root, components, "rules", lambda key: [f"rules/{key}.mdc", f"rules/{key}.md"], errors)

    for key, directory, file_name in [
        ("appTemplates", "app-templates", "template.json"),
    ]:
        values = components.get(key, [])
        if not isinstance(values, list):
            errors.append(f"components.{key} 必须是数组")
            continue
        for value in values:
            if not isinstance(value, str) or not SLUG.fullmatch(value):
                errors.append(f"components.{key} 条目必须是 slug")
            else:
                template_path = root / directory / value / file_name
                expect_file(root, [f"{directory}/{value}/{file_name}"], f"components.{key}.{value}", errors)
                if template_path.is_file():
                    validate_app_template(template_path, errors)

    assets = components.get("assets", [])
    if not isinstance(assets, list):
        errors.append("components.assets 必须是数组")
    else:
        for asset in assets:
            if not isinstance(asset, str):
                errors.append("components.assets 条目必须是字符串")
                continue
            try:
                relative = safe_relative(asset, "asset")
            except PluginError as error:
                errors.append(str(error))
                continue
            expect_file(root, [str(Path("assets") / relative)], f"components.assets.{asset}", errors)

    mcp = components.get("mcp", [])
    if not isinstance(mcp, list) or not all(isinstance(value, str) and SLUG.fullmatch(value) for value in mcp):
        errors.append("components.mcp 必须是 slug 数组")
    manifests = [item for item in [codex, claude] if item is not None]
    if mcp and not any("mcpServers" in item for item in manifests):
        errors.append("brain.json 声明 MCP 时 plugin.json 必须声明 mcpServers")
    if components.get("hooks") and not any("hooks" in item for item in manifests):
        errors.append("brain.json 声明 Hook 时 plugin.json 必须声明 hooks")
    validate_cli(components, source_scope, errors)

    for skill in components.get("skills", []) if isinstance(components.get("skills", []), list) else []:
        if not isinstance(skill, dict) or not isinstance(skill.get("key"), str):
            continue
        skill_path = root / "skills" / skill["key"] / "SKILL.md"
        if skill_path.is_file():
            text = skill_path.read_text(encoding="utf-8")
            if not re.match(r"^---\n(?s:.*?)\n---\n", text):
                errors.append(f"Skill {skill['key']} 缺少 YAML frontmatter")
            if "TODO" in text:
                errors.append(f"Skill {skill['key']} 仍包含 TODO")

    if marketplace_root is not None:
        validate_catalog(marketplace_root.expanduser().resolve(), name, errors)

    if errors:
        raise PluginError("校验失败:\n- " + "\n- ".join(errors))
    print(f"校验通过: {root}")


def self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="brain-plugin-creator-") as directory:
        root = Path(directory)
        write_json(root / ".agents/plugins/marketplace.json", {
            "name": "test", "interface": {"displayName": "Test"}, "plugins": []
        })
        write_json(root / ".claude-plugin/marketplace.json", {"name": "test", "plugins": []})
        args = argparse.Namespace(
            marketplace_root=root,
            name="sample-plugin",
            display_name="Sample Plugin",
            description="创建并校验示例插件。",
            publisher_id="sample",
            author="示例团队",
            category="开发工具",
            version="0.1.0",
            brain_compatibility=">=1.0.16",
            without_skill=False,
        )
        plugin_root = create_plugin(args)
        validate_plugin(plugin_root, root)
        app_template = plugin_root / "app-templates/sample-login/template.json"
        write_json(app_template, {
            "schemaVersion": 1,
            "key": "sample-login",
            "name": "Sample Login",
            "auth": {
                "kind": "cli_oauth",
                "configDirEnv": "SAMPLE_CONFIG_DIR",
                "commands": [{
                    "command": "sample",
                    "args": ["auth", {"valueFrom": "config.hostname"}],
                    "stdinFrom": "secret.token",
                    "timeoutSeconds": 600,
                }],
            },
            "networkScope": "public",
            "fields": [
                {"key": "hostname", "type": "text", "label": "Hostname", "required": True},
                {"key": "token", "type": "secret", "label": "Token", "required": True},
            ],
        })
        brain_path = plugin_root / "brain.json"
        brain = load_json(brain_path)
        brain["components"]["appTemplates"] = ["sample-login"]
        write_json(brain_path, brain)
        validate_plugin(plugin_root, root)
        template = load_json(app_template)
        template["auth"]["commands"][0]["args"] = [{"valueFrom": "config.token"}]
        write_json(app_template, template)
        try:
            validate_plugin(plugin_root, root)
        except PluginError:
            pass
        else:
            raise PluginError("cli_oauth secret argv 必须校验失败")
        template["auth"]["commands"][0]["args"] = ["auth", {"valueFrom": "config.hostname"}]
        write_json(app_template, template)
        write_json(app_template, {
            "schemaVersion": 1,
            "key": "sample-login",
            "name": "Sample Login",
            "auth": {
                "kind": "oauth2",
                "authorizationEndpoint": "https://identity.example/authorize",
                "authorizationParams": {"scope": "all"},
                "tokenEndpoint": "https://identity.example/token",
                "tokenMethod": "GET",
                "clientIdField": "client_id",
                "clientSecretField": "client_secret",
            },
            "networkScope": "public",
            "endpoint": "https://api.example/openapi/",
            "fields": [
                {"key": "client_id", "type": "text", "label": "Client ID", "required": True},
                {"key": "client_secret", "type": "secret", "label": "Client Secret", "required": True},
            ],
        })
        validate_plugin(plugin_root, root)
        oauth_template = load_json(app_template)
        oauth_template["auth"]["authorizationParams"] = {"state": "fixed"}
        write_json(app_template, oauth_template)
        try:
            validate_plugin(plugin_root, root)
        except PluginError:
            pass
        else:
            raise PluginError("OAuth 保留授权参数必须校验失败")
        oauth_template["auth"]["authorizationParams"] = {"scope": "all"}
        write_json(app_template, oauth_template)
        claude_path = plugin_root / ".claude-plugin/plugin.json"
        claude = load_json(claude_path)
        claude["description"] = "Claude 宿主专用描述。"
        write_json(claude_path, claude)
        validate_plugin(plugin_root, root)
        claude["name"] = "different-plugin"
        write_json(claude_path, claude)
        try:
            validate_plugin(plugin_root, root)
        except PluginError:
            pass
        else:
            raise PluginError("双 manifest name 不一致必须校验失败")
        claude_path.unlink()
        (root / ".claude-plugin/marketplace.json").unlink()
        validate_plugin(plugin_root, root)
        brain = load_json(brain_path)
        brain["components"]["cli"] = [{
            "key": "sample",
            "command": "sample",
            "targets": {"linux-x64": {
                "file": "sample",
                "url": "http://objects.example/sample",
                "size": 1,
                "sha256": "0" * 64,
                "archive": {"format": "tar.gz", "entry": "package/bin/sample"},
            }},
        }]
        write_json(brain_path, brain)
        validate_plugin(plugin_root, root, "private")
        brain["components"]["cli"][0]["targets"]["linux-x64"]["archive"]["entry"] = "../sample"
        write_json(brain_path, brain)
        try:
            validate_plugin(plugin_root, root, "private")
        except PluginError:
            pass
        else:
            raise PluginError("CLI 归档越界入口必须校验失败")
        brain["components"]["cli"][0]["targets"]["linux-x64"]["archive"]["entry"] = "package/bin/sample"
        write_json(brain_path, brain)
        for scope in ["public", "private"]:
            if scope == "private":
                brain["components"]["cli"][0]["targets"]["linux-x64"]["size"] = MAX_CLI_SIZE + 1
                write_json(brain_path, brain)
            try:
                validate_plugin(plugin_root, root, scope)
            except PluginError:
                pass
            else:
                raise PluginError(f"{scope} CLI 边界必须校验失败")
        single_args = copy.copy(args)
        single_args.name = "single-catalog-plugin"
        single_args.display_name = "Single Catalog Plugin"
        single_root = create_plugin(single_args)
        validate_plugin(single_root, root)
        try:
            create_plugin(args)
        except PluginError:
            pass
        else:
            raise PluginError("重复创建必须失败")
    print("self-test 通过")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)

    create = commands.add_parser("create", help="在现有 Marketplace 中创建 Brain Plugin")
    create.add_argument("marketplace_root", type=Path)
    create.add_argument("name")
    create.add_argument("--display-name", required=True)
    create.add_argument("--description", required=True)
    create.add_argument("--publisher-id", required=True)
    create.add_argument("--author", required=True)
    create.add_argument("--category", default="开发工具")
    create.add_argument("--version", default="0.1.0")
    create.add_argument("--brain-compatibility", default=">=1.0.16")
    create.add_argument("--without-skill", action="store_true")

    validate = commands.add_parser("validate", help="校验 Brain Plugin 包")
    validate.add_argument("plugin_root", type=Path)
    validate.add_argument("--marketplace-root", type=Path)
    validate.add_argument("--source-scope", choices=["public", "private", "personal"], default="public")

    commands.add_parser("self-test", help="运行脚手架与校验器自测")
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "create":
            create_plugin(args)
        elif args.command == "validate":
            validate_plugin(args.plugin_root, args.marketplace_root, args.source_scope)
        else:
            self_test()
    except (PluginError, OSError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
