# ADR: Adopt Qube CLI Lifecycle Contract

- **Status:** Proposed | Accepted | Superseded
- **Date:** YYYY-MM-DD
- **Product:** <product>
- **Contract:** `v2.0.0`
- **Contract commit:** `<40-character SHA>`
- **Obligation index SHA-256:** `<hash>`
- **Schema corpus SHA-256:** `<hash>`
- **Fixture corpus SHA-256:** `<hash>`
- **Snapshot corpus SHA-256:** `<hash>`
- **Local adapter:** `<path>`
- **Local conformance tests:** `<paths>`

## Context

Describe the product's prior install/update/uninstall behavior, observed drift, public baseline,
and why adoption is needed.

## Decision

State that the product implements the pinned contract locally and does not import, download, or
depend on the reference repository during build, release, install, update, uninstall, or runtime.

## Advertised channels and targets

| Channel | Package format | Scope | Targets | Stable identities/assets | Managed? |
|---|---|---|---|---|---|
| | | | | | |

Unadvertised formats and targets are not added for symmetry.

## Ownership evidence

| Channel | Required durable record | Payload/path proof | Integration proof | Legacy proof |
|---|---|---|---|---|
| | | | | |

Document evidence precedence. Markers and paths alone cannot authorize deletion.

## Transition matrix

Each cell is `repair`, `takeover`, `reject-safe`, or `not-applicable`.

| Existing owner → Candidate channel | <channel A> | <channel B> |
|---|---|---|
| <channel A> | | |
| <channel B> | | |

Every `reject-safe` cell includes the canonical recovery command. No cell may permit coexistence.

## Data and integrations

| Resource | Classification | Purge | Keep Data | Owner proof / safety boundary |
|---|---|---:|---:|---|
| | app-owned / settings-state / external-output / host-shared / repository-local | | | |

List PATH/profile changes, shortcuts, startup/tray/service hooks, registrations, receipts, caches,
logs, update backups, and staging resources.

## Product-specific process lifecycle

Record safe process-stop, live-image handoff, GUI/tray/service restart, and restart-required
behavior.

## Approved exceptions

For each exception record ID, affected obligation IDs, observable difference, reason, retained
safety invariants, fixture IDs, operator approval, and revalidation trigger. If none, say none.

## Conformance mapping and evidence

Link the product-local fixture mapping, source-test receipt, installed-channel receipts, immutable
candidate evidence, public-redownload receipt, and explicit unrun physical gates.

## Family cross-links

Link the central adopter registry and every existing sibling lifecycle ADR. Pending sibling ADRs
link their valid central adopter profile; once adopted, back-patch this ADR with the direct link.

## Consequences and revalidation triggers

Revalidate on a contract change, new/removed channel or target, installer identity/path change,
ownership-record change, package-manager change, new application data root or integration,
updater/uninstaller refactor, or lifecycle defect found by a later adopter.
