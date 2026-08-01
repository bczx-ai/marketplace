---
name: brain-ext-development
description: Develop, test, package, publish, or troubleshoot third-party Brain extensions. Use when creating brain.extension.json, choosing a runtime, implementing commands or panels, using Brain Extension APIs, defining capabilities or data, running brain-extension CLI, distributing extensions through a public Plugin, or diagnosing schema, activation, restart, signature, policy, and panel failures.
license: ""
metadata:
  version: "1.1.0"
  icon: Blocks
---

# Brain Extension Development

Use the smallest reference set that covers the request. Do not load all references by default.

## Workflow

1. Inspect the extension repository and identify whether the task is creation, contract/API work, security/data review, release, or troubleshooting.
2. For a new extension, read [Getting started](references/getting-started.md), then read only the references required by its runtime and contributions.
3. Treat `brain.extension.json`, `@brain/extension-api`, `@brain/extension-sdk`, `@brain/extension-ui`, `@brain/create-extension`, and `@brain/brain-extension` as the public contract. Do not import Brain source files.
4. Use the least powerful runtime and smallest declared capability set. Keep trusted backend work outside panel code.
5. Run typecheck, tests, build, `brain-extension check`, and package validation before handing off.
6. When diagnosing, preserve the stable `EXTENSION_*` error code and use [Troubleshooting](references/troubleshooting.md) before changing the contract.

## Reference routing

- Create or scaffold an extension: [Getting started](references/getting-started.md)
- Define Manifest, runtime, activation, dependencies, migrations, or icons: [Manifest and runtime](references/manifest-and-runtime.md)
- Implement Commands, native panels, Webviews, bridge, or APIs: [API and panels](references/api-and-panels.md)
- Review capabilities, Trusted Node, secrets, storage, or migration safety: [Security and data](references/security-and-data.md)
- Test, package, sign, or distribute SDK and extension artifacts: [Testing and publishing](references/testing-and-publishing.md)
- Diagnose invalid Manifest, activation, restart, Host, signature, policy, storage, or panel errors: [Troubleshooting](references/troubleshooting.md)

## Hard rules

- Use `extension`/“扩展” terminology and current filenames only; do not add compatibility aliases or migration reads.
- Brain carries no built-in extensions. Local development directories require the settings-page “开发模式”; production packages require an accepted signature and source policy.
- Installing a valid package enables it automatically. Do not design an additional user approval step for declared capabilities or runtime choice.
- Extensions access configuration, storage, secrets, workspace resources, and other privileged operations only through the public Extension API.
- Never commit registry credentials, signing private keys, GitLab tokens, extension source/build output, or packaged artifacts to a Marketplace Git repository.
