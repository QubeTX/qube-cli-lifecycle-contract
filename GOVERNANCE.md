# Governance

## Versioning

The contract uses semantic versioning:

- Major: changes an existing required state transition, status, exit code, field meaning,
  destructive safety invariant, or mandatory fixture expectation.
- Minor: adds an optional profile, optional extension, or new obligation that does not change an
  existing adopter's conforming observable behavior.
- Patch: corrects spelling or clarifies wording without changing schemas, fixtures, or behavior.

If a clarification changes how a fixture passes, it is not a patch.

## Adoption

A product adopts a contract version only when its ADR pins the immutable contract tag and commit,
its product-local tests cover the required fixture IDs, and its advertised managed channels pass
the applicable installed-system gates. Reference examples or this repository's validator cannot
certify a product installation.

The central adopter registry is updated first. As later products adopt, their ADRs must link every
existing sibling lifecycle ADR, and already-adopted ADRs must be back-patched with the new direct
link before the family advances to another product.

## Exceptions

An exception must identify the product, contract version, affected obligation IDs, observable
difference, reason, retained safety invariants, conformance fixtures, approval source, and
revalidation trigger. Missing unadvertised channels and product-specific integrations are adapter
facts, not exceptions.

This is the mandatory exception rule (`GOV-003`).

No exception may waive:

- destructive ambiguity stopping before mutation;
- channel preservation during automatic update;
- external-output and host-data preservation;
- exact-tag candidate use after release resolution;
- truthful success and rollback reporting; or
- immutable published release bytes.

## Independence

Product builds and releases must succeed offline from their own checkout. They may contain
product-authored local equivalents of schemas and fixtures with provenance hashes, but must not
fetch this repository. Automated synchronization is optional developer tooling only and may not
run in product CI, build, packaging, installation, update, uninstall, or runtime paths.
