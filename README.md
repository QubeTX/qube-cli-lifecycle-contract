# Qube CLI Lifecycle Contract

The Qube CLI Lifecycle Contract defines the observable installation, repair, takeover, update,
rollback, output, and uninstall behavior shared by the Qube product family. Products keep the
package formats, deployment targets, and application integrations that make sense for them.
They share one behavioral contract.

Current contract: **2.0.0**.

## Reference only

This repository is deliberately not a product dependency. A product must not download, import,
link, vendor as a submodule, or execute code from this repository during build, release, install,
update, uninstall, or runtime. Each product implements the contract locally, pins the contract
tag and commit in its ADR, and keeps its own executable conformance tests.

The Rust code under `reference/rust/` is a small, `publish = false` model that demonstrates the
status and ownership vocabulary. It is an example for agents, not a shared library.

## What is normative

- `spec/` defines the requirements and assigns stable obligation IDs.
- `spec/obligations.json` is the obligation index and fixture-coverage ledger.
- `schemas/` defines stable machine-readable results, adapters, release manifests, and receipts.
- `fixtures/` defines required abstract lifecycle cases.
- `snapshots/` fixes the family-owned terminal and JSON presentation.
- `adr/TEMPLATE.md` defines each adopter's decision record.
- `adopters/` records adoption status and stable ADR destinations.

Native package-manager windows and operating-system elevation UI are platform-owned and are not
required to be visually identical. The terminal envelope, state transitions, statuses, JSON,
error classifications, exit codes, safety properties, and completion claims are shared.

## Applying the contract

1. Read the complete tagged contract.
2. Create a product-local adapter manifest conforming to
   `schemas/lifecycle-adapter-v2.schema.json`.
3. Create a product ADR from `adr/TEMPLATE.md`, pinning the tag, commit, and relevant hashes.
4. Implement product-local fixtures corresponding to every mandatory fixture ID.
5. Run source conformance and real installed-package qualification on every advertised managed
   channel and target.
6. Record the completion receipt without treating simulated fixtures as installed-system proof.

## Validate this repository

```text
python scripts/validate.py
cargo test --manifest-path reference/rust/Cargo.toml
```

The Python validator uses only the standard library. It parses every JSON artifact, verifies that
every required obligation has fixture coverage, checks status/exit invariants, and confirms the
adopter registry agrees with the product profiles. It also prints the provenance hashes adopters
pin in their local adapter and ADR.

The obligation hash is SHA-256 over the raw `spec/obligations.json` bytes. Schema, fixture, and
snapshot corpus hashes are SHA-256 over a UTF-8/LF ledger sorted by POSIX relative path. Each
ledger line is `<raw-file-sha256>  <relative-path>\n`; schema files are `schemas/*.json`, fixture
files are `fixtures/*/required-cases.json`, and snapshots are `snapshots/json/*.json` plus
`snapshots/terminal/*.txt`. `scripts/validate.py` is the canonical implementation.

## License

PolyForm Noncommercial 1.0.0. See `LICENSE`.
