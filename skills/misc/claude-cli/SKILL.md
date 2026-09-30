---
name: use-claude-cli
description: Invoke the Claude Code CLI (`claude`) from Codex exclusively as a "host-mode bridge" — a duplex stream-json coprocess where Codex acts as the SDK host, approves tool calls in real time over the control protocol, streams events live, and can steer mid-run. Use whenever you need to invoke claude, spawn claude as a subprocess, or ask claude to do work Codex is not doing itself.
---

# Use Claude CLI from Codex — host-mode bridge only

Invoke `claude` **only** as a **host-mode bridge**: a long-running duplex NDJSON coprocess
(`--input-format stream-json --output-format stream-json --permission-prompt-tool stdio`),
started as a persistent session that Codex drives. "Host mode" is claude's own word for this:
the SDK host (Codex) answers `can_use_tool` control requests in real time.

## The hard rule

- Always start claude as a host-mode bridge (recipe below). No exceptions for "simple" tasks.
- **Banned:** blocking one-shot `claude -p "..."` (no host ⇒ every ask is a silent terminal
  denial), PTY/keystroke-driving the interactive TUI, and `--dangerously-skip-permissions` used
  as a convenience — the approval step is the point of the bridge.
- Pre-approval flags (`--allowedTools`, `permissions.allow`, `--permission-mode acceptEdits`)
  are allowed *inside* the bridge to cut prompt traffic; the bridge and its host stay in the
  loop for everything else.

Why forced: approvals must reach Codex (otherwise privileged calls silently fail); one channel
carries streaming, steering, and approvals; and this exact shape is verified end-to-end on
Claude Code 2.1.285 (2026-09).

## When to use

- Get a **second opinion** on your diff or plan from a different model/provider.
- Delegate a self-contained task (write tests, refactor one module), approving each privileged
  call as it comes in.
- **Parallel work**: one bridge per task (separate bridge dirs), staggered starts.
- **Steer mid-run**: interject corrections without killing and restarting claude.
- Watch a long task stream live instead of waiting blind on a blocking call.

Do NOT use claude for trivial lookups you can answer yourself — each call costs tokens and time.

## First, verify the environment

```bash
command -v claude && claude --version
claude auth status            # exits non-zero if not authenticated
```

If auth is missing, tell the user to run `claude auth login` (interactive — you cannot do it
for them). For CI/unattended use, `claude setup-token` produces a long-lived OAuth token.

## The bridge — canonical recipe

```bash
# 1. one bridge = one dir (use distinct dirs for concurrent bridges)
BRIDGE=/tmp/claude-bridge-1
mkdir -p "$BRIDGE" && : > "$BRIDGE/in.ndjson"

# 2. start claude as a PERSISTENT session (long timeout; sandboxed Codex needs network escalation)
tail -f "$BRIDGE/in.ndjson" | claude -p \
  --input-format stream-json --output-format stream-json --verbose \
  --permission-prompt-tool stdio --permission-mode default
#  ^ tail holds stdin open; a plain non-tty exec without it sees EOF and claude exits immediately

# 3. send a task (append a line while the session runs)
printf '%s\n' '{"type":"user","message":{"role":"user","content":[{"type":"text","text":"<task>"}]}}' >> "$BRIDGE/in.ndjson"
```

Events arrive as NDJSON on stdout. What matters:

| Event | Meaning |
|---|---|
| `system`/`init` | `session_id`, model, tool inventory |
| `assistant` | model text and `tool_use` as they happen |
| `control_request` | **an approval ask — answer it now** (below) |
| `user` | `tool_result` for executed calls (proof of what ran) |
| `result` | end of turn: `result` text, `permission_denials`, `total_cost_usd`, `session_id` |

Every event includes `session_id`; the turn's final `result` event closes the turn but the
process stays alive for more messages. Read selectively: `system`/`thinking_tokens` events
dominate the stream (a small task can emit tens of thousands of tokens of them), so watch
`assistant`, `control_request`, `user` (tool_result) and `result` — and never relay the raw
stream to the user.

### Answering an approval ask

```jsonc
// out: claude asks before a gated call
{"type":"control_request","request_id":"<id>","request":{
  "subtype":"can_use_tool","tool_name":"Bash",
  "input":{"command":"mkdir -p /tmp/x && echo ok"},
  "permission_suggestions":[...]}}

// in: approve exactly as asked — omit updatedInput and the CLI uses the original tool input
{"type":"control_response","response":{"subtype":"success","request_id":"<id>",
  "response":{"behavior":"allow"}}}

// in: approve with a modification — include updatedInput to replace the tool input
{"type":"control_response","response":{"subtype":"success","request_id":"<id>",
  "response":{"behavior":"allow","updatedInput":{"command":"mkdir -p /tmp/x && echo ok"}}}}

// in: deny — same envelope per wire schema (not yet field-exercised)
{"type":"control_response","response":{"subtype":"success","request_id":"<id>",
  "response":{"behavior":"deny","message":"reason"}}}
```

- **Review before you allow**: Write/Edit asks carry the full `file_path` + `content`, so the
  host can inspect the actual change inside the request — the strongest reason to prefer the
  bridge over pre-approval.
- **Approve exactly what was asked** with a bare `{"behavior":"allow"}` — `updatedInput` is
  optional and the CLI falls back to the original tool input (verified: a 2 KB Write ask was
  approved this way). Include `updatedInput` only when you want to change the call.
- Decide per call; that is the entire point of the bridge. Never leave an ask unanswered — an
  unresolved `control_request` stalls the turn (observed waiting ~50 s with no timeout hit, so
  approval latency equals your polling interval: use 10–15 s polls while an ask is pending).
- `permission_suggestions` are claude's "don't ask again" options (`addRules` →
  `localSettings`, i.e. `.claude/settings.local.json`; also `addDirectories`, `setMode`), and
  their shape varies by tool. Plain allow does **not** adopt them; use `permission_updates`
  only when the user actually wants standing rules (wire shape not yet field-verified).
- Verified on 2.1.285: a gated `mkdir` surfaced as `can_use_tool`, an allow executed it, and
  the final result carried `permission_denials: []`. The identical setup without
  `--permission-prompt-tool stdio` auto-denied it.

### Steering and ending

- To steer or follow up, append another user message to `$BRIDGE/in.ndjson` — streaming input
  mode keeps the process alive across turns (design behavior; not yet field-exercised).
- End a bridge: `pkill -f 'claude-bridge-1[/]in.ndjson'` and `pkill -f 'permission-prompt-tool[ ]stdio'`
  (the bracket trick keeps the pattern from matching your own shell). Idling costs nothing.
- Resume later: relaunch a bridge with `--resume <session_id>` from a previous `result` event
  (not yet field-exercised).

## Operating checklist (Codex: persistent exec session + write_stdin)

1. `exec_command` (sandboxed): `BRIDGE=/tmp/claude-bridge-N; mkdir -p "$BRIDGE"; : > "$BRIDGE/in.ndjson"`.
2. `exec_command` the pipeline with a long yield (and escalation — claude needs API network).
3. Append the task line (sandboxed write to the bridge dir).
4. Poll with `write_stdin`: 30–60 s while idle, 10–15 s once a gated action is pending
   (approval latency == your polling interval); parse events as they stream.
5. On each `control_request`: append the `control_response` promptly.
6. On `result`: surface `result`, check `permission_denials`, then continue or end the bridge.
7. Verify out-of-band — `result` is claude's self-report. For code: rebuild clean + differential
   test; for "files untouched" claims: check them. Then end the bridge.

## Variants (all still host-mode bridges)

- **Read-only Q&A**: same shape; simply zero approval traffic.
- **Write/edit tasks**: keep the git-worktree discipline for isolation; each Edit/Write arrives
  as its own approval ask.
- **Fan-out**: one bridge per task in its own dir; stagger starts (rate limits).
- **Budget caps**: `--max-turns N --max-budget-usd X` are claude args in the bridge command.
- **Structured output**: `--json-schema '<schema>'` still applies; the validated payload rides
  the final `result` event (field-verify on first use).
- **Unattended CI**: prefer a CI wrapper that answers `control_request`s by policy; the only
  fallback when no host exists at all is `--bare` with complete pre-approval, where asks are
  terminal denials by design.

## Permission gotchas (verified 2.1.285)

- Builtin-safe commands never prompt: `pwd`, `whoami`, `alias`, `* --version`. Don't use them
  as negative controls when testing approvals.
- Project `.claude/settings.json` `permissions.allow` is **ignored in an untrusted workspace**
  ("this workspace has not been trusted"); inline `--settings '{"permissions":{"allow":[...]}}'`
  still applies. Trust a directory via one interactive run, or set
  `projects["<path>"].hasTrustDialogAccepted: true` in `~/.claude.json`.
- Interactive "Yes, don't ask again" persists a rule to `.claude/settings.local.json`.
- `--permission-prompts host|none` decides who answers; in a bridge you are the host, so keep
  the default.
- `--permission-prompt-tool` normally names an MCP approval tool, but in a stdio-host session
  prompts go to the stdio host and an MCP tool cannot answer them; the special value `stdio`
  selects the host path used here.
- Workspace-trust / authorization prompts require a real user; they are outside the protocol.
- `--permission-mode` choices: `acceptEdits` (edits auto-approved, shell gated), `auto`
  (classifier decides), `dontAsk` (deny unless pre-approved), `plan`, `bypassPermissions`,
  `manual` (alias of the default ask mode).

## Codex integration notes

- **Working directory matters**: claude reads `./CLAUDE.md` and `./.claude/` from where you
  launch it. Start the bridge with the project as cwd.
- **Long waits, not busy polling**: claude turns take seconds to minutes; poll `write_stdin`
  with long timeouts, dropping to 10–15 s polls while an approval ask is pending.
- **Network**: claude needs outbound API access; in a sandboxed Codex run this requires
  escalation.
- **Idle bridges are cheap** but not free to manage — end one you are done with.
- Prefer the final `result` text for the user; the NDJSON stream is working state.

## Quick reference — bridge edition

| Goal | How |
|---|---|
| Start a bridge | `tail -f $BRIDGE/in.ndjson \| claude -p --input-format stream-json --output-format stream-json --verbose --permission-prompt-tool stdio --permission-mode default` |
| Send a task | append `{"type":"user","message":{"role":"user","content":[...]}}` to `$BRIDGE/in.ndjson` |
| Allow a call | append `{"type":"control_response","response":{"subtype":"success","request_id":"<id>","response":{"behavior":"allow"}}}` (add `updatedInput` only to modify the call) |
| Deny a call | same envelope with `{"behavior":"deny","message":"..."}` |
| See what was denied | `permission_denials` on the `result` event |
| Steer mid-run | append another user message |
| Cap cost/length | `--max-turns N --max-budget-usd X` in the bridge command |
| Resume | relaunch bridge with `--resume <session_id>` |
| End | `pkill -f 'claude-bridge-1[/]in.ndjson'`; `pkill -f 'permission-prompt-tool[ ]stdio'` |

## Changelog

- 2026-09-30 (3): from a live bridge run — `updatedInput` optional (bare allow ⇒ original
  input; verified with a 2 KB Write), review-before-allow for Write/Edit asks, poll-cadence
  guidance, stream-noise filtering, rule-persistence hygiene, mandatory out-of-band
  verification; steering/resume marked not-yet-exercised. Verified against 2.1.285.
- 2026-09-30 (2): host-mode bridge is now the **only** sanctioned invocation style; the
  one-shot/PTY/"bypass as convenience" patterns are removed and explicitly banned; added the
  operating checklist, steering/ending, and bridge variants. Vocabulary: "host-mode bridge"
  (duplex stream-json coprocess; Codex = the SDK host). Verified against Claude Code 2.1.285.
- 2026-09-30 (1): added live permission approval via the stdio control protocol and permission
  gotchas; corrected `-p` denial semantics and `--permission-mode` choices.
