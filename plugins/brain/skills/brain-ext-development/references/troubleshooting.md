# Troubleshooting

Start from the stable `EXTENSION_*` code and the server-side diagnostic entry. Preserve the first deterministic failure and do not add retry loops around unknown mutation outcomes.

## Manifest and package

- `EXTENSION_SCHEMA_INVALID`: inspect `brain.extension.json` for unknown fields, invalid IDs/SemVer, missing activation events, invalid dependency keys, runtime entry errors, or contribution/capability mismatch.
- `EXTENSION_PACKAGE_INVALID`: verify `.brain-ext` ZIP layout, referenced files, relative paths, size limits, integrity, and Catalog or Plugin descriptor identity.
- `EXTENSION_SIGNATURE_INVALID`: verify publisher, key status, validity window, SHA-256, signature document, accepted source, runtime, and enterprise policy.
- `EXTENSION_INCOMPATIBLE`: check Brain/API/Node ranges and SandboxAdapter availability.

## Install, activation, and restart

- A packaged install imports one `.brain-ext` from Extension settings and enables it automatically. If it is absent afterward, inspect the failed operation and its stable code rather than looking for another enable or capability step.
- A directory import requires “开发模式” to be on when the server starts the package operation. Confirm the setting and re-import the directory.
- `EXTENSION_ACTIVATION_FAILED`: run the built entry through `brain-extension dev`, confirm exports and package dependencies, then inspect redacted Host logs.
- `EXTENSION_HOST_CRASHED`: identify process exit, uncaught rejection, timeout, memory/output limit, or child-process leak. Fix the backend before retrying.
- Restart failure: confirm the extension is installed and enabled, the active version and runtime entry exist, policy still permits it, Host generation is current, and no migration/checkpoint remains unresolved.

## Capabilities, data, and panels

- `EXTENSION_PERMISSION_DENIED`: compare the requested API operation with the Manifest declaration, scope, workspace role, owner, project ID, and path/origin constraints. Lifecycle state is automatic; fix the declaration, constraints, or caller context.
- File Store startup or persistence failure: inspect `$BRAIN_HOME/extensions/state/` ownership, `0700` directories, `0600` files, realpaths, disk capacity, and the first schema/scope/integrity error. Do not edit internal JSON/NDJSON state or any SQLite database to repair it.
- Empty or disconnected panel: verify Manifest entry, build output, CSP-safe assets, `brainExtensionPanel`, MessagePort handshake, panel instance/generation, and bounded protocol validation.
- Missing custom icon: verify the declared package-relative resource exists, is included in package integrity, uses a supported image format, and is not a symlink, hardlink, empty file, or mismatched MIME.
- Stale responses: cancel work on generation change and never reuse a panel instance across the wrong project/session scope.

Reproduce with `brain-extension check`, `brain-extension test`, and `brain-extension dev`. Server enforcement is authoritative; do not work around signature, source, path, owner, policy, or capability failures in the client.
