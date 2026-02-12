# Parallel Worker Protocol (Separated)

This file is intentionally separate from `instructions.md`.

It should define only multi-worker orchestration concerns, such as:
- branch synchronization
- heartbeat/liveness
- page claiming and conflict resolution
- retry/recovery behavior

It should **not** redefine translation style rules or JSON schema.

For translation content requirements and output contract, use:
- `instructions.md`
