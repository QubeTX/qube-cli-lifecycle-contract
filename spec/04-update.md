# Update

The canonical surface is:

```text
<command> update [--json] [--verbose] [--no-color]
```

Update begins from one proven supported owner. It preserves that channel and scope exactly and
MUST NOT cross-fallback after any preflight or runtime failure (`UPD-001`). Unknown, unmanaged, or
conflicting ownership stops before release download or mutation.

The transaction resolves the release once and pins the exact tag (`REL-001`). Public versionless
URLs are entrypoints only. After resolution, payloads, manifests, and sidecars come from the exact
tag. The candidate is checked for product, version, target, size, digest, and every signature the
channel advertises (`REL-002`). A same-origin hash sidecar is integrity evidence, not an
independent publisher signature.

A healthy equal-version installation returns `no_change`/`already_current`. A proven degraded
owner may repair only through the same channel and exact release (`UPD-002`). A newer release runs
the install transaction and verifies both installed version and durable owner (`UPD-003`).

Integrity failure, installer failure, locked process, elevation denial, endpoint policy,
ownership conflict, restart requirement, verification failure, rollback, and rollback failure
use the shared status/error/exit vocabulary (`UPD-004`). Mutation failures verify rollback and
remain non-success (`UPD-005`).

