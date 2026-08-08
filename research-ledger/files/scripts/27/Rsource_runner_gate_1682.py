from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
VALIDATION = OUT / "P8_Y5_BRR545_1681_VALIDATION.csv"
RESULT_MATRIX = OUT / "P8_Y5_PARENT_QLOC_1681_VALIDATOR_RESULT_MATRIX.csv"
ARENA_MATRIX = OUT / "P8_Y5_PARENT_QLOC_1681_ARENA_USE_REFUSAL_MATRIX.csv"
ALLOWED_ARENAS = {"WEP", "R10", "NEWTON_GM", "R11"}


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _truth(value: object) -> bool:
    return str(value).strip().lower() == "true"


def evaluate_source_branch_gate(arena: str | None = None, root: str | Path | None = None) -> dict[str, object]:
    base = Path(root) if root is not None else ROOT
    out = base / "source-intake" / "mts_residuals"
    validation_path = out / VALIDATION.name
    result_path = out / RESULT_MATRIX.name
    arena_path = out / ARENA_MATRIX.name
    missing_files = [str(path) for path in [validation_path, result_path, arena_path] if not path.exists()]
    if missing_files:
        return {
            "gate_pass": False,
            "arena": arena,
            "reason": "MISSING_GATE_FILES",
            "missing_files": missing_files,
            "valid_for_claim": False,
            "claim_allowed": False,
        }

    validation_rows = _read_csv(validation_path)
    result_rows = _read_csv(result_path)
    arena_rows = _read_csv(arena_path)
    overall_pass = any(row.get("check_id") == "VAL1681_OVERALL" and row.get("result") == "PASS" for row in validation_rows)
    component_pass = all(_truth(row.get("validator_pass", "False")) for row in result_rows)
    arena_rejections = {row.get("arena"): row for row in arena_rows if row.get("validator_result", "").startswith("REJECT")}
    arena_key = arena.upper() if isinstance(arena, str) else None
    if arena_key and arena_key not in ALLOWED_ARENAS:
        return {
            "gate_pass": False,
            "arena": arena,
            "reason": "UNKNOWN_SOURCE_ARENA",
            "known_arenas": sorted(ALLOWED_ARENAS),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    arena_pass = arena_key is None and not arena_rejections
    if arena_key is not None:
        arena_pass = arena_key not in arena_rejections
    gate_pass = overall_pass and component_pass and arena_pass
    return {
        "gate_pass": gate_pass,
        "arena": arena_key,
        "reason": "PASS" if gate_pass else "SOURCE_BRANCH_GATE_REJECTED",
        "overall_1681_validation_pass": overall_pass,
        "component_rows_pass": component_pass,
        "arena_pass": arena_pass,
        "rejected_arenas": sorted(arena_rejections),
        "component_failures": [row.get("basis_component") for row in result_rows if not _truth(row.get("validator_pass", "False"))],
        "valid_for_claim": gate_pass,
        "claim_allowed": gate_pass,
    }


def require_source_branch_gate(arena: str | None = None, root: str | Path | None = None) -> dict[str, object]:
    result = evaluate_source_branch_gate(arena=arena, root=root)
    if not result["gate_pass"]:
        raise RuntimeError(f"source branch gate rejected: {result}")
    return result
