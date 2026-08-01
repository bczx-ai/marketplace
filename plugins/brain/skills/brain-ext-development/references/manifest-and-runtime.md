# Manifest and runtime

The manifest filename is exactly `brain.extension.json`; unknown fields and compatibility names are rejected. IDs use `<publisher>.<name>`, and every contribution ID stays in that namespace.

Required identity and compatibility fields:

```json
{
  "schemaVersion": "1.0",
  "id": "devcube.example",
  "publisher": "devcube",
  "name": "example",
  "displayName": "Example",
  "description": "Example extension",
  "version": "1.0.0",
  "license": "MIT",
  "engines": {
    "brain": "^1.0.20",
    "extensionApi": "^1.0.0",
    "node": "^22.0.0 || ^24.0.0"
  },
  "runtime": {
    "kind": "trusted-node",
    "entry": "dist/extension.js"
  },
  "activationEvents": [],
  "permissions": [],
  "contributes": {}
}
```

`node` is required for Trusted Node. `sandboxed` and `trusted-node` require a package-relative entry. `declarative` has no entry. Package paths cannot be absolute, use `..`, URI schemes, backslashes, or undeclared top-level files.

Every Command and tool panel needs a matching `onCommand:<id>` or `onToolPanel:<id>` activation event. Runtime lifecycle exports are `activate`, optional `deactivate`, and migration handlers declared by stable migration IDs.

Dependencies use:

```json
{
  "dependencies": {
    "extensions": { "devcube.other": "^1.0.0" },
    "skills": [{ "name": "example-skill", "optional": false }]
  }
}
```

Migrations declare `id`, `from`, `to`, SHA-256 `checksum`, and `reversible`. Never mutate an already released migration. Upgrade and rollback must checkpoint data and fail closed when migration state is unknown.

Custom icons are ordinary package resources. Declare only a package-relative image accepted by the contribution schema, keep it inside the package, and include it in the integrity set. Do not use external URLs or files outside the extension root.

Validate with `brain-extension check`; schema failures use `EXTENSION_SCHEMA_INVALID`, while archive/layout failures use `EXTENSION_PACKAGE_INVALID`.
