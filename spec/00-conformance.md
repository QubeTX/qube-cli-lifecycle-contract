# Conformance

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, and MAY are
normative. `spec/obligations.json` is the complete obligation index for contract 2.0.0.

A product conforms only when:

1. Its local adapter and ADR pin this exact contract release (`GOV-001`).
2. Product-local tests cover every mandatory fixture applicable to its advertised channels.
3. Every advertised managed/native channel passes target-installed qualification (`TST-001`).
4. Its completion receipt has no failing, missing, or indeterminate mandatory row (`TST-002`).
5. The product remains fully independent from this repository (`GOV-002`).

A schema-valid file is not behavioral proof. A unit fixture is not package-manager, elevation,
PATH, signature, GUI, process-lifecycle, or public-byte proof. The terminal result is no stronger
than the weakest mandatory receipt row.

Fixtures are abstract inputs and expected observations. Each adopter maps abstract resources to
its own registries, receipts, paths, package tools, processes, and data roots without weakening
the expectation. Product-specific integrations add test rows; they do not remove shared rows.

