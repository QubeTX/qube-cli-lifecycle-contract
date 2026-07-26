# Vocabulary

## Product and delivery terms

- **Install owner:** the one durable authority responsible for an installed product.
- **Install channel:** the lifecycle-preserving origin used by update and uninstall, such as
  `msi-global`, `managed-shell`, or `cargo`.
- **Delivery method:** how an installer was invoked. It does not determine ownership.
- **Package format:** MSI, Inno EXE, PKG, DMG app, DEB, managed script, Cargo, or archive.
- **Scope:** `user`, `system`, or `unmanaged`.
- **Target:** operating system, architecture, and ABI.
- **Data policy:** `preserve` for install/update, `purge` for default uninstall, or `keep-data`.

A channel is not a URL, shell executable, architecture, package extension, or PATH. Windows
PowerShell and `pwsh` may invoke the same `managed-powershell` channel. A versionless URL may
bootstrap an exact tagged release without becoming the installed owner.

## Ownership states

Every discovery result MUST be exactly one of (`OWN-003`):

- `absent`: no recognized owner and no competing product command at the intended target.
- `owned`: exactly one complete, supported, durable owner.
- `degraded`: exactly one durable owner but an owned payload or integration is missing, stale, or
  corrupt, with no competing owner.
- `conflict`: multiple recognized owners, or one recognized owner plus a competing product binary,
  registration, receipt, or command resolution.
- `unmanaged`: a genuine portable/source installation with no supported owner.
- `unknown`: evidence cannot safely prove whether or how the installation is owned.

Classification priority is conflict, unknown/unmanaged, degraded/owned, then absent. An exact
recognized legacy owner remains `owned` with `legacy: true`.

## Evidence authority

A destructive owner proof MUST combine a durable package registration or validated receipt with
the expected product identity, path, scope, and payload (`OWN-002`). A mutable hint, display name,
or path substring alone cannot authorize deletion. Contradictory lower-authority hints make a
single proven owner `degraded`; evidence of another owner makes it `conflict`.

