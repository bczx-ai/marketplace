# Getting started

## Prerequisites

- Node.js `^22.0.0 || ^24.0.0`
- pnpm
- Access to the private `@brain` npm scope

Configure the project-level registry without committing credentials:

```ini
@brain:registry=https://codebase.zhonganinfo.com/api/v4/projects/<project_id>/packages/npm/
//codebase.zhonganinfo.com/api/v4/projects/<project_id>/packages/npm/:_authToken=${NPM_TOKEN}
```

## Scaffold

```bash
pnpm dlx @brain/create-extension my-extension \
  --publisher devcube \
  --template command
```

Templates are `command`, `native-panel`, `webview`, and `trusted-node`. The generated project must depend on normal SemVer releases of `@brain/*`; do not use `workspace:*`, `file:`, or Brain repository paths.

## Initial workflow

```bash
pnpm install
pnpm typecheck
pnpm test
pnpm build
pnpm exec brain-extension check
pnpm exec brain-extension package
```

Both commands default to the current directory. Packaging writes `<extensionId>-<version>.brain-ext` to the caller's current directory; use `--output` only when another destination is required. Drag the resulting file into the local Extension settings page to import, install, and enable it in one step.

For iterative work on an unpacked directory, turn on “开发模式” in the Extension settings page and add the project directory there. Turning it off prevents new directory imports without changing already installed development extensions.

Choose the least powerful runtime:

- `declarative`: contributions without executable backend code.
- `sandboxed`: executable backend through a conformance-approved sandbox.
- `trusted-node`: full service-user Node/process/network authority, restricted by publisher, signature, source, and policy checks for production packages.

Return to `SKILL.md` and load the Manifest/runtime or security/data reference only when the task requires it.
