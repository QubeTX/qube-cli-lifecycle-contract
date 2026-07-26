# Output, statuses, and exit codes

Family-owned terminal headings, ordered phases, symbols, warnings, failures, and summaries match
the parameterized snapshots under `snapshots/terminal/` (`OUT-001`). Product names, commands,
versions, channels, and exact paths are variables; wording and layout are not.

JSON mode emits exactly one object conforming to `lifecycle-result-v2.schema.json` on stdout.
Progress, child processes, package managers, warnings, and verbose diagnostics go to stderr or are
captured (`OUT-002`). All keys remain present with null/empty values; products cannot add top-level
fields.

Status and exit mapping (`OUT-003`):

| Exit | Statuses | Meaning |
|---:|---|---|
| 0 | `succeeded`, `no_change` | Every mandatory postcondition is verified |
| 1 | `cancelled`, `confirmation_required` | No mutation; cancellation or missing confirmation |
| 2 | `failed`, `rolled_back` | No mutation, or prior working state verified restored |
| 3 | `requires_user_action`, `pending_restart`, `pending_handoff` | Operation is not complete |
| 4 | `rollback_failed` | Unsafe or indeterminate partial state |

`success` is true only for exit 0. `result` is `installed`, `repaired`, `taken_over`, `updated`,
`already_current`, `removed`, `not_installed`, or null. Merely starting another process, receiving
a package-manager zero before post-verification, or retaining a mandatory residual cannot be
success (`OUT-005`).

`--no-color` removes ANSI styling without changing text or symbols. Automatic ASCII fallback may
replace only the snapshot-defined symbols. `--verbose` adds stderr evidence without changing the
semantic result, JSON shape, or exit code (`OUT-004`).

