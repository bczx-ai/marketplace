# API and panels

Import public types from `@brain/extension-api`. Runtime schemas, packaging, and test helpers come from `@brain/extension-sdk`. Webview bridge and theme helpers come from `@brain/extension-ui`.

## Commands

Register only Manifest-declared command IDs during activation:

```ts
export async function activate(context: ExtensionContext) {
  context.brain.commands.registerCommand(
    "devcube.example.refresh",
    async (args, invocation) => ({ args, projectId: invocation.projectId }),
  );
}
```

Commands may be exposed through composer, command palette, or menus. Their capability requirements must be a subset of Manifest declarations. Respect cancellation, deadlines, concurrency policy, and generation changes.

## Panels

- Native renderers (`tree`, `list`, `table`, `form`) send serializable models through the Host.
- `webview` panels load a package-relative entry in an isolated frame.
- The panel global bridge is `brainExtensionPanel`.
- Use `@brain/extension-ui` for MessagePort transport and theme synchronization.

Panel messages must be bounded JSON and scoped by trusted `panelInstanceId` plus generation. Validate private panel protocols on both sides. Dispose subscriptions, requests, and timers when a panel or Host closes.

Keep filesystem, process, network, credentials, and provider SDK operations in the backend. The Webview only renders and sends narrow intent messages. External URLs must be allowlisted and opened through the Host API.

Available API groups include commands, panels, workspace context, window, git, sessions, chat, artifacts, configuration, storage, secrets, network, and logging. Every privileged API remains subject to Manifest declaration, constraints, owner/workspace scope, policy, and server validation.
