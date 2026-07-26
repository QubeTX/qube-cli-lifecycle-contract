#!/usr/bin/env python3
"""Self-contained structural validator for the reference contract."""

from __future__ import annotations

import json
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBLIGATION_ID = re.compile(r"^[A-Z]+-[0-9]{3}$")
FIXTURE_ID = re.compile(r"^[A-Z]+-[A-Z0-9-]+-[0-9]{3}$")
STATUS_EXIT = {
    "succeeded": 0,
    "no_change": 0,
    "cancelled": 1,
    "confirmation_required": 1,
    "failed": 2,
    "rolled_back": 2,
    "requires_user_action": 3,
    "pending_restart": 3,
    "pending_handoff": 3,
    "rollback_failed": 4,
}
RESULT_KEYS = {
    "schema", "product", "action", "status", "result", "success", "changed",
    "current_version", "target_version", "installed_version", "install_channel",
    "ownership_before", "ownership_after", "data_policy", "phase",
    "requires_user_action", "restart_required", "message", "recovery_url", "error",
    "residuals", "warnings", "exit_code",
}


def raw_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def corpus_sha256(paths: list[Path]) -> str:
    ledger = "".join(
        f"{raw_sha256(path)}  {path.relative_to(ROOT).as_posix()}\n"
        for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix())
    )
    return hashlib.sha256(ledger.encode("utf-8")).hexdigest()


def provenance_hashes() -> dict[str, str]:
    snapshots = list((ROOT / "snapshots" / "json").glob("*.json"))
    snapshots.extend((ROOT / "snapshots" / "terminal").glob("*.txt"))
    return {
        "obligations_sha256": raw_sha256(ROOT / "spec" / "obligations.json"),
        "schemas_sha256": corpus_sha256(list((ROOT / "schemas").glob("*.json"))),
        "fixtures_sha256": corpus_sha256(list((ROOT / "fixtures").glob("*/required-cases.json"))),
        "snapshots_sha256": corpus_sha256(snapshots),
    }
IGNORED_TREE_PARTS = {".git", "target", "__pycache__"}


def is_source_file(path: Path) -> bool:
    return not IGNORED_TREE_PARTS.intersection(path.relative_to(ROOT).parts)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise AssertionError(f"{path.relative_to(ROOT)}: invalid JSON: {exc}") from exc


def validate_json_files() -> int:
    paths = sorted(path for path in ROOT.rglob("*.json") if is_source_file(path))
    for path in paths:
        load_json(path)
    return len(paths)


def validate_obligations_and_fixtures() -> tuple[int, int]:
    index = load_json(ROOT / "spec" / "obligations.json")
    assert index["contract_version"] == (ROOT / "CONTRACT_VERSION").read_text(encoding="utf-8").strip()
    obligations = index["obligations"]
    ids = [item["id"] for item in obligations]
    assert len(ids) == len(set(ids)), "duplicate obligation ID"
    for item in obligations:
        assert OBLIGATION_ID.fullmatch(item["id"]), f"invalid obligation ID: {item['id']}"
        assert item["level"] == "MUST", f"unexpected obligation level: {item['id']}"
        assert item["summary"] and item["oracle"], f"missing obligation text: {item['id']}"

    covered: set[str] = set()
    case_ids: set[str] = set()
    case_count = 0
    fixture_paths = sorted((ROOT / "fixtures").glob("*/required-cases.json"))
    assert fixture_paths, "no fixture files found"
    for path in fixture_paths:
        fixture = load_json(path)
        assert fixture["schema"] == "qubetx.cli-lifecycle.fixtures.v2"
        assert fixture["category"] == path.parent.name
        for case in fixture["cases"]:
            case_count += 1
            case_id = case["id"]
            assert FIXTURE_ID.fullmatch(case_id), f"invalid fixture ID: {case_id}"
            assert case_id not in case_ids, f"duplicate fixture ID: {case_id}"
            case_ids.add(case_id)
            assert case["covers"], f"fixture has no obligations: {case_id}"
            assert "given" in case and "when" in case and "expect" in case, f"incomplete fixture: {case_id}"
            for obligation in case["covers"]:
                assert obligation in ids, f"{case_id} references unknown obligation {obligation}"
                covered.add(obligation)

    missing = sorted(item["id"] for item in obligations if item["fixture_required"] and item["id"] not in covered)
    assert not missing, f"obligations missing fixture coverage: {', '.join(missing)}"

    markdown = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(ROOT.rglob("*.md"))
        if is_source_file(path)
    )
    absent_from_docs = sorted(obligation for obligation in ids if obligation not in markdown)
    assert not absent_from_docs, f"obligations absent from documentation: {', '.join(absent_from_docs)}"
    return len(obligations), case_count


def validate_result_snapshots() -> int:
    paths = sorted((ROOT / "snapshots" / "json").glob("*.json"))
    assert paths, "no JSON snapshots found"
    for path in paths:
        result = load_json(path)
        assert set(result) == RESULT_KEYS, f"{path.name}: result keys drifted"
        assert result["schema"] == "qubetx.cli-lifecycle.result.v2"
        status = result["status"]
        assert status in STATUS_EXIT, f"{path.name}: unknown status {status}"
        assert result["exit_code"] == STATUS_EXIT[status], f"{path.name}: status/exit mismatch"
        assert result["success"] == (result["exit_code"] == 0), f"{path.name}: success/exit mismatch"
        if result["exit_code"] == 0:
            assert result["error"] is None, f"{path.name}: successful result carries error"
        if status == "pending_handoff":
            assert not result["success"] and result["result"] is None
    return len(paths)


def validate_terminal_snapshots() -> int:
    paths = sorted((ROOT / "snapshots" / "terminal").glob("*.txt"))
    assert paths, "no terminal snapshots found"
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert text.startswith("Qube CLI Lifecycle"), f"{path.name}: missing common heading"
        assert "\x1b" not in text, f"{path.name}: canonical snapshot contains ANSI"
    return len(paths)


def validate_adopters() -> int:
    registry = load_json(ROOT / "adopters" / "registry.json")
    assert registry["contract_version"] == "2.0.0"
    products: set[str] = set()
    for entry in registry["adopters"]:
        product = entry["product_id"]
        assert product not in products, f"duplicate adopter: {product}"
        products.add(product)
        profile_path = ROOT / entry["profile"]
        assert profile_path.is_file(), f"missing adopter profile: {entry['profile']}"
        profile = load_json(profile_path)
        for key in ("product_id", "status", "target_version", "repository"):
            assert profile[key] == entry[key], f"{product}: registry/profile mismatch for {key}"
        if entry["status"] == "adopted":
            assert entry["adr_url"], f"{product}: adopted without ADR URL"
            assert profile["contract_pin"], f"{product}: adopted without contract pin"
        else:
            assert profile["contract_pin"] is None, f"{product}: pending profile has a pin"
    assert products == {"wb300", "sd300", "nd300", "tr300", "honk300"}
    return len(products)


def validate_reference_independence() -> None:
    cargo = (ROOT / "reference" / "rust" / "Cargo.toml").read_text(encoding="utf-8")
    assert "publish = false" in cargo, "Rust reference must remain publish=false"
    assert "[dependencies]" not in cargo, "Rust reference must remain dependency-free"
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "not a product dependency" in readme


def main() -> int:
    try:
        json_count = validate_json_files()
        obligation_count, fixture_count = validate_obligations_and_fixtures()
        result_count = validate_result_snapshots()
        terminal_count = validate_terminal_snapshots()
        adopter_count = validate_adopters()
        validate_reference_independence()
        hashes = provenance_hashes()
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(
        "PASS: "
        f"{json_count} JSON files; {obligation_count} obligations; "
        f"{fixture_count} fixtures; {result_count} JSON snapshots; "
        f"{terminal_count} terminal snapshots; {adopter_count} adopter profiles"
    )
    for name, digest in hashes.items():
        print(f"{name}: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
