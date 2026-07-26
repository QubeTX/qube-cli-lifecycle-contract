# Install, repair, and takeover

The family-owned installer envelope follows this observable sequence:

1. Discover platform, target, existing version, all owners, and command resolution.
2. Resolve the candidate once.
3. Present existing installation, exact target, chosen channel/scope, and preserved data policy
   (`INS-001`).
4. Download into private randomized staging, verify it, and acquire the lifecycle lock.
5. Acquire required elevation before destructive operations and revalidate ownership (`INS-002`).
6. Establish and test the channel-specific rollback plan (`INS-006`).
7. Apply the clean install, repair, or approved takeover.
8. Remove recognized obsolete ownership, registrations, receipts, integrations, and backups.
9. Verify the target executable and durable owner, one fresh-terminal resolution, and preserved
   application state.
10. Clean staging and emit the shared result.

A clean install commits exactly one owner (`INS-003`). The same version and channel is an
idempotent repair (`INS-004`). An older recognized owner is either transactionally taken over or
rejected before mutation by an approved transition-matrix cell; leaving both installed is never
valid (`INS-005`).

Install/update failures after mutation restore and verify the prior working owner, payload,
registration, integrations, and version. A failed clean install restores the absent state. If
rollback cannot be verified, status is `rollback_failed`, never success (`INS-006`).

Commit requires the expected version, one durable owner, one intended fresh-terminal command,
correct integrations, no obsolete owner, and no owned backup or staging residue (`INS-007`).

