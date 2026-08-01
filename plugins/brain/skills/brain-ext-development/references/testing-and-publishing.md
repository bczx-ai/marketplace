# Testing and publishing

## Required checks

```bash
pnpm typecheck
pnpm test
pnpm build
pnpm exec brain-extension check
pnpm exec brain-extension test
pnpm exec brain-extension package
```

Test Manifest rejection, activation/deactivation, cancellation, capability denial, Host crash/restart, stale generation, panel isolation, upgrade/rollback, and migration failure. Trusted Node provider integrations should use fake executables or isolated service accounts in automation.

The archive suffix is `.brain-ext` and MIME is `application/vnd.brain.extension+zip`. Without `--output`, `brain-extension package` writes `<extensionId>-<version>.brain-ext` in the caller's current directory. The archive contains `brain.extension.json`, declared build/assets/localization files, integrity metadata, and signature files only.

Create a final signed package from the extension directory with an approved key outside the repository:

```bash
pnpm exec brain-extension sign . \
  --key /secure/path/publisher.pem \
  --key-id publisher-key-id \
  --output devcube.example-1.0.0.brain-ext
```

`package` also accepts `--key` and `--key-id` together. Signing does not append to an existing archive; it always packages the source directory into the final `.brain-ext` output.

Publish only an already signed package to an approved Catalog:

```bash
pnpm exec brain-extension publish devcube.example-1.0.0.brain-ext \
  --catalog https://catalog.example.com/extensions
```

Publishing is idempotent by immutable version; never overwrite different content under the same version. Do not commit tokens or private keys.

## Public Plugin distribution

A public Marketplace Plugin can install an extension by declaring the same entry in both Plugin manifests:

```json
{
  "brainExtensions": [
    { "name": "issues", "version": "^1.2.0" }
  ]
}
```

Map each declaration to `brainextensions/<name>/extension.json`:

```json
{
  "schemaVersion": 1,
  "extensionId": "devcube.issues",
  "version": "1.2.3",
  "publisher": "devcube",
  "runtimeKind": "trusted-node",
  "downloadUrl": "https://downloads.example.com/devcube.issues-1.2.3.brain-ext",
  "size": 123456,
  "sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
}
```

The URL must be stable HTTPS without credentials, query, fragment, or redirects. The Controller downloads and caches the exact immutable artifact, then Workspace validates its identity, size, digest, signature, and policy before the Plugin transaction commits.

The Marketplace Git repository contains only the Plugin declarations and download descriptors. Keep extension source, build output, signing material, and `.brain-ext` artifacts in their dedicated build and artifact systems.

## SDK publication

Brain SDK maintainers publish the five `@brain` packages with:

```bash
pnpm pack:extension-sdk
BRAIN_NPM_PROJECT_ID=<id> NPM_TOKEN=<token> pnpm publish:extension-sdk
pnpm publish:extension-sdk -- --dry-run
```

The publisher validates all five packages before the first upload, uses a temporary npmrc, skips an existing identical immutable version, and stops if existing content differs.
