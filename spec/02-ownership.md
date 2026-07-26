# Ownership discovery

Discovery MUST enumerate all product-defined package registrations, receipts, legacy identities,
managed records, Cargo metadata, intended payload paths, relevant PATH/profile entries, shortcuts,
startup/service hooks, update backups, and fresh-terminal command resolutions before choosing an
owner (`OWN-001`). It MUST NOT stop at the first plausible record.

The adapter defines exact proof conjunctions for each channel. Discovery is deterministic: no
confidence score, fuzzy name match, newest timestamp, or preferred-channel ordering may turn
ambiguous evidence into destructive authority.

Unknown, unmanaged, conflicting, malformed, symlinked/reparse-point, or unsupported evidence MUST
stop before mutation and report the exact relevant paths and records (`OWN-004`). Incidental
portable files outside the target and command-resolution set are never guessed at, scanned for
globally, or deleted.

The operation acquires a product/scope lifecycle lock and records a discovery fingerprint. After
elevation and immediately before the first destructive action, it MUST repeat the deciding probes
and compare the fingerprint (`OWN-005`). A changed owner, registration, path identity, or command
resolution invalidates the plan.

