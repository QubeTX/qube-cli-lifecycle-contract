# Uninstall and data policy

The canonical surface is:

```text
<command> uninstall [--keep-data] [--yes] [--json] [--verbose] [--no-color]
```

Bare interactive uninstall offers Remove All, Keep Data, and Cancel, with Remove All selected by
default. `--keep-data` selects that policy but still requires confirmation unless `--yes` is
present. JSON and non-TTY invocation without `--yes` MUST NOT read stdin or mutate; it returns
`confirmation_required`, exit 1 (`UNI-001`).

After one owner is proven, uninstall freezes the exact removal set, stops product processes,
acquires authority, revalidates, removes the package/payload owner, removes integrations and
registrations, then applies the data policy. Default purge removes every declared app-owned
configuration, setting, cache, log, and state resource (`UNI-002`). `--keep-data` retains only the
adapter's declared settings/state while still removing the complete program and integrations
(`UNI-003`).

External exports, downloaded reports, host/shared resources, and declared repository-local
history are outside the delete set under every policy (`UNI-004`). Ambiguous resources are never
deleted.

The exact proven owner selects the package-aware uninstaller. A first similarly named registration
or path heuristic is insufficient (`UNI-005`). Success requires verified absence of every owner,
payload, registration, receipt, integration, backup, staging resource, and fresh-terminal command
resolution (`UNI-006`).

If a running image requires post-exit deletion, the parent may launch a constrained helper with a
pinned removal plan. The parent reports `pending_handoff`, exit 3, and `success: false`; spawning
the helper is not completion. The installed-system harness waits for the helper and checks its
completion receipt and final state (`UNI-007`). If automatic completion is impossible, return
`requires_user_action` with exact recovery steps.

Against an absent installation, an exact staged candidate returns `no_change`/`not_installed`,
exit 0 (`UNI-008`). This is the repeated-uninstall oracle because the installed command itself no
longer resolves after a successful uninstall.

