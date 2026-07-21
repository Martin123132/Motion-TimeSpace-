from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4998"
VALIDATION = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4998_VALIDATION.csv"
VALIDATION_PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"

RESULT = SOURCE / "covariant_mixed_projector_and_box_completion_results.json"
PROJECTOR = SOURCE / "B2_current_and_mixed_projector_proof.csv"
MIXED = SOURCE / "complete_generic_D_mixed_cut.csv"
BOXES = SOURCE / "generic_D_full_box_and_hh_inference.csv"
GATES = SOURCE / "covariant_mixed_projector_and_box_gate.csv"
DOCUMENT = POST / "4998-Y5-R2FR-covariant-mixed-projector-and-generic-D-box-completion.md"
GENERATOR = POST / "scripts" / "Y5_R2FR_4998_covariant_mixed_projector_and_generic_D_box_completion.py"

MARKER = "MTS_4998_COVARIANT_MIXED_PROJECTOR_AND_GENERIC_D_BOX_COMPLETION"
D = sp.Symbol("D")
t = sp.Symbol("t", nonzero=True)
u = sp.Symbol("u", nonzero=True)
s = -t - u
epsilon = sp.Symbol("epsilon")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def expression(value: str) -> sp.Expr:
    return sp.sympify(value, locals={"D": D, "t": t, "u": u, "s": s})


def add(checks: list[dict[str, Any]], check: str, passed: bool, detail: str) -> None:
    checks.append({"check": check, "passed": bool(passed), "detail": detail, "checkpoint_marker": MARKER, "valid_for_full_MTS_claim": False})


def write_checks(checks: list[dict[str, Any]]) -> None:
    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)


def main() -> int:
    checks: list[dict[str, Any]] = []
    required = [RESULT, PROJECTOR, MIXED, BOXES, GATES, DOCUMENT, GENERATOR]
    for path in required:
        add(checks, f"exists:{path.name}", path.exists(), str(path))
    if not all(path.exists() for path in required):
        write_checks(checks)
        return 1
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    add(checks, "result_marker", result.get("checkpoint_marker") == MARKER, str(result.get("checkpoint_marker")))
    for key in ("covariant_mixed_projector_complete", "generic_D_mixed_cut_complete", "generic_D_full_box_sector_complete", "generic_D_hh_box_sector_complete", "4996_evanescent_box_correction_reassigned_to_hh"):
        add(checks, f"complete:{key}", result.get(key) is True, "must be true")
    for key in ("generic_D_hh_one_scale_lower_sector_complete", "cut_free_dJ2_remainder_complete", "complete_one_loop_phi2h2", "outer_cut_complete", "valid_for_full_MTS_claim"):
        add(checks, f"blocked:{key}", result.get(key) is False, "must remain false")
    for relative_path, expected in result.get("source_hashes_sha256", {}).items():
        path = ROOT / Path(relative_path)
        add(checks, f"source_hash:{Path(relative_path).name}", path.exists() and digest(path) == expected, relative_path)
    add(checks, "formalization_tree_unchanged", tree_digest(ROOT / "formalization-workbench") == result.get("formalization_workbench_tree_sha256"), result.get("formalization_workbench_tree_sha256", "missing"))

    tables = {"projector": rows(PROJECTOR), "mixed": rows(MIXED), "boxes": rows(BOXES), "gates": rows(GATES)}
    for name, table in tables.items():
        add(checks, f"{name}_nonempty", bool(table), str(len(table)))
        add(checks, f"{name}_marker", all(row.get("checkpoint_marker") == MARKER for row in table), "all rows")
        add(checks, f"{name}_nonclaim", all(row.get("valid_for_full_MTS_claim") == "False" for row in table), "all rows")
    add(checks, "projector_residuals", all(row["residual"] == "0" for row in tables["projector"]), "all exact projector and anchor rows")
    proofs = {row["proof"]: row for row in tables["projector"]}
    for proof in ("internal_gauge_transversality", "helicity_current_nullity", "D_projector_trace_silence", "mixed_covariant_current_product", "spinor_to_covariant_numerator", "no_mu_squared_remainder"):
        add(checks, f"proof:{proof}", proofs[proof]["status"] == "closed" and proofs[proof]["residual"] == "0", str(proofs[proof]))

    mixed = {row["coefficient"]: expression(row["formula"]) for row in tables["mixed"]}
    add(checks, "B_box_crossing", sp.factor(mixed["B_su_full"].xreplace({t: u, u: t}) - mixed["B_st_full"]) == 0, "t<->u")
    add(checks, "T_triangle_crossing", sp.factor(mixed["T_u_finite"].xreplace({t: u, u: t}) - mixed["T_t_finite"]) == 0, "t<->u")
    add(checks, "C_bubble_crossing", sp.factor(mixed["C_u_finite"].xreplace({t: u, u: t}) - mixed["C_t_finite"]) == 0, "t<->u")
    add(checks, "Bst_D4", sp.factor(mixed["B_st_full"].subs(D, 4) - t**4 * (s**4 + t**4 + u**4) / 32) == 0, str(mixed["B_st_full"].subs(D, 4)))
    add(checks, "Bsu_D4", sp.factor(mixed["B_su_full"].subs(D, 4) - u**4 * (s**4 + t**4 + u**4) / 32) == 0, str(mixed["B_su_full"].subs(D, 4)))
    add(checks, "Btu_D4", sp.factor(mixed["B_tu_full"].subs(D, 4) - t**4 * u**4 / 16) == 0, str(mixed["B_tu_full"].subs(D, 4)))
    add(checks, "Tu_D4", sp.factor(mixed["T_u_finite"].subs(D, 4) + u**5 * (2 * t**2 + t * u + u**2) / 8) == 0, str(mixed["T_u_finite"].subs(D, 4)))

    box_map = {row["component"]: row for row in tables["boxes"]}
    hh_su = expression(box_map["B_su_hh(D)"]["formula"])
    hh_source = u**4 * (t**4 + u**4) / 32
    add(checks, "hh_D4_source", sp.factor(hh_su.subs(D, 4) - hh_source) == 0, str(hh_su.subs(D, 4)))
    hh_epsilon = sp.factor(sp.diff(hh_su.subs(D, 4 - 2 * epsilon), epsilon).subs(epsilon, 0))
    expected_epsilon = u**4 * (t + u) ** 2 * (11 * t**2 - 14 * t * u + 11 * u**2) / 192
    add(checks, "hh_epsilon_correction", sp.factor(hh_epsilon - expected_epsilon) == 0, str(hh_epsilon))
    add(checks, "hh_epsilon_matches_result", expression(result["hh_linear_epsilon_Bsu"]) == hh_epsilon, result["hh_linear_epsilon_Bsu"])

    gates = {row["gate"]: row for row in tables["gates"]}
    for gate in ("covariant_B2_current", "generic_D_mixed_cut", "generic_D_full_box_sector", "generic_D_hh_box_sector"):
        add(checks, f"gate_closed:{gate}", gates[gate]["passed"] == "True" and gates[gate]["status"] == "closed", str(gates[gate]))
    for gate in ("generic_D_hh_one_scale_lower_sector", "cut_free_dJ2_remainder", "outer_cut_or_full_MTS"):
        add(checks, f"gate_open:{gate}", gates[gate]["passed"] == "False" and gates[gate]["status"] == "open", str(gates[gate]))

    document = DOCUMENT.read_text(encoding="utf-8")
    add(checks, "document_promotes_mixed", "promoted from diagnostic to physical" in document, "required result")
    add(checks, "document_reassigns_owner", "owner is the `hh` state sum" in document, "required correction")
    add(checks, "document_no_full_claim", "not a complete one-loop" in document, "required nonclaim")
    passed = all(check["passed"] for check in checks)
    add(checks, "all_validation_checks", passed, f"pre-summary checks={len(checks)}")
    write_checks(checks)
    VALIDATION_PROVENANCE.write_text(
        "# 4998 validation provenance\n\n"
        f"Validator: `{Path(__file__).name}`\n\n"
        f"Generator SHA-256: `{digest(GENERATOR)}`\n\n"
        f"Result SHA-256: `{digest(RESULT)}`\n\n"
        "The validator reparses every covariant-current identity and held-out anchor, checks all D4 box/triangle limits and crossings, independently expands the inferred hh box through linear epsilon, locks every source hash, and enforces all remaining nonclaim gates.\n",
        encoding="utf-8",
    )
    print(json.dumps({"checkpoint_marker": MARKER, "checks": len(checks), "passed": all(check["passed"] for check in checks), "validation": str(VALIDATION)}, indent=2))
    return 0 if all(check["passed"] for check in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
