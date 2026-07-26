# Release and publication

A release candidate is bound to one source commit and one immutable tag. Its lifecycle manifest
lists every advertised asset's channel, target, size, SHA-256, and signature requirement. All
candidate assets, manifests, signatures, and provenance are verified before publication.

Versionless public installer names remain stable, but execution pins one exact release before
payload download (`REL-001`). A product need—not family symmetry—justifies a package format or
target.

Published tags and asset bytes MUST NOT be replaced, clobbered, force-pushed, or retagged
(`REL-003`). A torn or defective release is repaired through a new version. Publication tooling
must fail if an asset name already exists with different bytes.

After publication, qualification downloads public assets again, validates them against the public
manifest, and repeats versionless installer, core-functionality, update, and uninstall smoke tests.
A locally built artifact cannot substitute for that public-byte oracle.

