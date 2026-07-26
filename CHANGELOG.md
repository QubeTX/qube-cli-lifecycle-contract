# Changelog

All notable contract changes are documented here. Published contract tags are immutable.

## [2.0.1] - 2026-07-26

### Fixed

- Published the unchanged v2 behavioral contract through an immutable GitHub release after the
  repository setting was enabled. The earlier `v2.0.0` tag and release remain untouched; adopters
  pin `v2.0.1`.

## [2.0.0] - 2026-07-26

### Added

- Initial reference-only lifecycle contract for Qube CLI products.
- Normative ownership, installation, update, rollback, uninstall, presentation, and publication
  obligations with stable IDs.
- Closed JSON schemas, conformance fixtures, terminal/JSON snapshots, ADR governance, adoption
  profiles, a self-contained validator, and a non-publishable Rust reference model.
