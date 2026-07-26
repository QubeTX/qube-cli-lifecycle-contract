# Agent guide

This repository is the normative, reference-only Qube CLI Lifecycle Contract. It is not a
runtime crate, build dependency, Git dependency, submodule, or release-time download for any
product.

## Source precedence

1. The operator-approved product-family requirements.
2. `spec/` and `spec/obligations.json` in the same tagged contract release.
3. Machine-readable schemas, fixtures, and terminal snapshots.
4. Reference Rust code, which is illustrative and never normative by itself.

When prose and a fixture disagree, treat the contract candidate as invalid and repair both before
tagging. Do not silently choose one.

## Change rules

- Give every normative MUST a stable obligation ID and an observable oracle.
- Keep `spec/obligations.json`, fixtures, schemas, and snapshots in lockstep.
- Run `python scripts/validate.py` and
  `cargo test --manifest-path reference/rust/Cargo.toml` before review.
- Never weaken a fixture to accept a product implementation.
- Never add this repository to a product manifest, lockfile, submodule, build workflow, installer,
  updater, or runtime fetch path.
- Published tags and bytes are immutable. Fix forward.

