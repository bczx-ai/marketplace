# Security and data

Use the least powerful runtime and smallest declared capability set. Brain APIs do not sandbox Trusted Node operating-system authority.

## Trusted Node

Trusted Node code runs with the Brain service user's file, process, environment, and network access. Production packages are admitted only when publisher, signature, source, runtime, path, owner, and enterprise policy checks pass. Unpacked code can run only after the user turns on the settings-page “开发模式” and imports its directory.

Never execute user input through a shell. Use fixed executables, validated argv, stdin for sensitive bodies, timeouts, output limits, cancellation, and child-process cleanup.

## Capabilities

Declare only capabilities actually used. Path and origin constraints must be narrow. Installation and lifecycle operations write workspace-scoped allow entries for the exact Manifest declarations automatically; there is no separate user action for this state.

The server still validates that each operation is declared, satisfies its constraints, belongs to the current owner/workspace/project, and is permitted by source, signature, runtime, and enterprise policy. Automatic state never broadens a Manifest declaration, bypasses path security, or delegates owner checks to a panel.

## Data

- Configuration keys must be declared in the Manifest.
- Ordinary configuration and storage are extension-namespaced.
- Secret plaintext is available only to Trusted Node and never enters RPC snapshots, panel messages, logs, diagnostics, or analytics.
- `undefined` deletes a configuration/storage value; JSON `null` is a normal value.
- Use Extension API configuration, storage, and secret methods. Do not open Brain databases or construct paths to Brain-managed state.
- Brain's internal Extension state lives under `$BRAIN_HOME/extensions/state/`; it is private implementation data, not an extension persistence API.

Migrations use stable IDs and checksums. Take a checkpoint before update or rollback, validate size and integrity, and restore atomically on failure. Do not read package-manager directories, internal JSON/NDJSON files, SQLite tables, UI state, or other extensions' data.

Logs must be bounded and redacted. Avoid tokens, full provider responses, file contents, private URLs, and user-authored descriptions. Diagnostics should expose stable codes and safe metadata only.
