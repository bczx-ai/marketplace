# Diagnostics evidence schema

`brain-workspace-server diagnostics` prints exactly one JSON object on success.

```ts
interface DiagnosticEvidence {
  schemaVersion: 1;
  generatedAt: string;
  window: { since: string; sinceHours: number };
  environment: {
    runtimeKind: "desktop" | "workspace" | "standalone" | "local";
    runtimeVersion?: string;
    shellVersion?: string;
    platform: string;
    arch: string;
    osRelease: string;
    nodeVersion: string;
    memoryMiB: { free: number; total: number };
    storage: {
      brainHome: "missing" | "read-only" | "read-write" | "unavailable";
      data: "missing" | "read-only" | "read-write" | "unavailable";
      logs: "missing" | "read-only" | "read-write" | "unavailable";
      freeMiB?: number;
    };
  };
  sessionTranscripts: {
    rootAvailable: boolean;
    directoriesScanned: number;
    filesScanned: number;
    totalBytes: number;
    thresholds: {
      searchExcludedBytes: number;
      highRiskBytes: number;
    };
    searchExcludedCount: number;
    highRiskCount: number;
    scanTruncated: boolean;
    current?: {
      sizeBytes: number;
      modifiedAt: string;
      risk: "normal" | "search-excluded" | "high-risk";
    };
    largest: Array<{
      ref: string;
      sizeBytes: number;
      modifiedAt: string;
      risk: "normal" | "search-excluded" | "high-risk";
      currentSession: boolean;
    }>;
    warnings: string[];
  };
  collection: {
    directories: Array<{ source: string; available: boolean; matchingFiles: number }>;
    filesScanned: number;
    bytesRead: number;
    matchedEvents: number;
    omittedEvents: number;
    truncated: boolean;
  };
  events: Array<{
    id: string;
    timestamp: string;
    severity: "error" | "warning" | "info";
    source: string;
    file: string;
    label: string;
    excerpt: string;
  }>;
  warnings: string[];
}
```

Interpretation:

- `events` contains errors, warnings, and a small set of runtime lifecycle events. It intentionally excludes normal RPC payloads, audit records, complete Agent events, and ordinary local-server stdout.
- `matchedEvents` is the number of relevant deduplicated events before the `max-events` cap. `omittedEvents` reports events removed by that cap.
- `truncated` covers file-count, byte, tail, excerpt, or event limits. A truncated result is usable but cannot prove that an event was absent.
- An unavailable directory is not itself a root cause. Desktop, Workspace, Standalone, and development runtimes do not all produce every log source.
- Event ids are report-local citations, not persisted Brain identifiers.
- Paths use `$HOME` and `$PROJECT` placeholders; common correlation ids are replaced with stable report-local pseudonyms.
- `sessionTranscripts` is built only from directory entries plus file `size` and `mtime`; transcript JSON content is never opened. Sidecars and corrupt backups are excluded, and main transcript names and project directories are not returned.
- `search-excluded` reflects the existing 5 MiB message-search cutoff. `high-risk` is the 25 MiB diagnostic threshold for whole-file load/save pressure, not a hard storage limit or proof of causation.
- `current` is present only when a complete readable directory scan lets `BRAIN_SESSION_ID` uniquely match one main transcript. `largest` uses report-local `transcript-*` refs and never exposes the Session id.
- `scanTruncated` means the metadata scan reached its 10,000-file bound. Counts and totals then cover only the scanned prefix.
