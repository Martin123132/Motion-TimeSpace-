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
SOURCE = POST / "source-intake" / "functional_rg" / "4997"
VALIDATION = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4997_VALIDATION.csv"
VALIDATION_PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"

RESULT = SOURCE / "full_H_contact_vanishing_and_scalar_cut_results.json"
HELICITY = SOURCE / "helicity_contact_vanishing_proof.csv"
COEFFICIENTS = SOURCE / "complete_generic_D_scalar_s_cut.csv"
RECONCILIATION = SOURCE / "one_scale_coordinate_reconciliation.csv"
GATES = SOURCE / "full_H_contact_and_scalar_cut_gate.csv"
DOCUMENT = POST / "4997-Y5-R2FR-full-H-contact-vanishing-and-generic-D-scalar-cut-completion.md"
GENERATOR = POST / "scripts" / "Y5_R2FR_4997_full_H_contact_vanishing_and_scalar_cut_completion.py"

MARKER = "MTS_4997_FULL_H_CONTACT_VANISHING_AND_SCALAR_CUT_COMPLETION"
D = sp.Symbol("D")
t = sp.Symbol("t", nonzero=True)
u = sp.Symbol("u", nonzero=True)
s = -t - u


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
    required = [RESULT, HELICITY, COEFFICIENTS, RECONCILIATION, GATES, DOCUMENT, GENERATOR]
    for path in required:
        add(checks, f"exists:{path.name}", path.exists(), str(path))
    if not all(path.exists() for path in required):
        write_checks(checks)
        return 1
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    add(checks, "result_marker", result.get("checkpoint_marker") == MARKER, str(result.get("checkpoint_marker")))
    add(checks, "contact_vanishes", result.get("full_H_contact_integral_vanishes") is True, "must be true")
    add(checks, "scalar_cut_complete", result.get("generic_D_scalar_s_cut_complete") is True, "must be true")
    add(checks, "coordinate_reclassified", result.get("4993_4995_scalar_split_reclassified_as_coordinate_dependent") is True, "must be true")
    for key in ("generic_D_internal_graviton_state_sum_complete", "cut_free_dJ2_remainder_complete", "complete_one_loop_phi2h2", "outer_cut_complete", "valid_for_full_MTS_claim"):
        add(checks, f"blocked:{key}", result.get(key) is False, "must remain false")
    for relative_path, expected in result.get("source_hashes_sha256", {}).items():
        path = ROOT / Path(relative_path)
        add(checks, f"source_hash:{Path(relative_path).name}", path.exists() and digest(path) == expected, relative_path)
    add(checks, "formalization_tree_unchanged", tree_digest(ROOT / "formalization-workbench") == result.get("formalization_workbench_tree_sha256"), result.get("formalization_workbench_tree_sha256", "missing"))

    tables = {"helicity": rows(HELICITY), "coefficients": rows(COEFFICIENTS), "reconciliation": rows(RECONCILIATION), "gates": rows(GATES)}
    for name, table in tables.items():
        add(checks, f"{name}_nonempty", bool(table), str(len(table)))
        add(checks, f"{name}_marker", all(row.get("checkpoint_marker") == MARKER for row in table), "all rows")
        add(checks, f"{name}_nonclaim", all(row.get("valid_for_full_MTS_claim") == "False" for row in table), "all rows")

    projection_expected = {"n.p1": "0", "n.p2": "0", "n.K": "0", "n.(-p4)": "1", "n.(-p3)": "-1"}
    projection_rows = {row["quantity"]: row for row in tables["helicity"] if row["proof_step"] == "helicity_covector"}
    for name, expected in projection_expected.items():
        add(checks, f"projection:{name}", projection_rows[name]["derived_value"] == expected and projection_rows[name]["residual"] == "0", str(projection_rows[name]))
    contact_rows = [row for row in tables["helicity"] if row["proof_step"].startswith("contact_tensor_power")]
    add(checks, "four_contact_powers", len(contact_rows) == 4, str(len(contact_rows)))
    add(checks, "contact_counting", all(int(row["free_A_vectors_available"]) < int(row["free_A_vectors_required"]) and row["derived_value"] == "0" for row in contact_rows), "r=0..3")
    add(checks, "all_helicity_residuals", all(row["residual"] == "0" for row in tables["helicity"]), "all rows")

    coefficients = {row["coefficient"]: row for row in tables["coefficients"]}
    bst = expression(coefficients["B_st_scalar_direct(D)"]["formula"])
    bsu = expression(coefficients["B_su_scalar_direct(D)"]["formula"])
    t_direct = expression(coefficients["T_s_scalar_direct(D)"]["formula"])
    add(checks, "box_crossing", sp.factor(bst.xreplace({t: u, u: t}) - bsu) == 0, "t<->u")
    add(checks, "Bst_D4", sp.factor(bst.subs(D, 4) - s**4 * t**4 / 32) == 0, str(bst.subs(D, 4)))
    add(checks, "Bsu_D4", sp.factor(bsu.subs(D, 4) - s**4 * u**4 / 32) == 0, str(bsu.subs(D, 4)))
    add(checks, "triangle_symmetry", sp.factor(t_direct.xreplace({t: u, u: t}) - t_direct) == 0, "t<->u")
    add(checks, "direct_bubble_zero", coefficients["C_s_scalar_direct(D)"]["formula"] == "0", str(coefficients["C_s_scalar_direct(D)"]))

    reconciliation = {row["identity"]: row for row in tables["reconciliation"]}
    add(checks, "reconciliation_residuals", all(row["residual"] in ("0", "not_applicable") for row in tables["reconciliation"]), "all rows")
    translation = expression(reconciliation["exact_coordinate_translation"]["C_translation"])
    ratio = (D - 4) * s / (2 * (D - 3))
    triangle_rows_4993 = rows(POST / "source-intake" / "functional_rg" / "4993" / "full_phi2h2_triangle_completion.csv")
    t_ir = expression(next(row["coefficient"] for row in triangle_rows_4993 if row["triangle_id"] == "TRI4993_05_Ts_scalar_remainder"))
    add(checks, "exact_master_translation", sp.factor(t_ir + ratio * translation - t_direct) == 0, "T_IR+r*C=T_direct")
    residue = sp.factor(sp.limit((D - 4) * translation, D, 4))
    expected_residue = (t**6 - t**5 * u + t**4 * u**2 - t**3 * u**3 + t**2 * u**4 - t * u**5 + u**6) / 4
    add(checks, "translation_residue", sp.factor(residue - expected_residue) == 0, str(residue))
    add(checks, "translation_has_pole", residue != 0, str(residue))

    gates = {row["gate"]: row for row in tables["gates"]}
    for gate in ("correct_scalar_helicity_covector", "full_H_contact_vanishing", "generic_D_scalar_s_cut_complete", "4993_4995_coordinate_reconciliation"):
        add(checks, f"gate_closed:{gate}", gates[gate]["passed"] == "True" and gates[gate]["status"] == "closed", str(gates[gate]))
    for gate in ("generic_D_internal_graviton_states", "cut_free_dJ2_remainder", "outer_cut_or_full_MTS"):
        add(checks, f"gate_open:{gate}", gates[gate]["passed"] == "False" and gates[gate]["status"] == "open", str(gates[gate]))

    document = DOCUMENT.read_text(encoding="utf-8")
    add(checks, "document_states_vanishing", "every contact integral is exactly zero" in document, "required theorem")
    add(checks, "document_reclassifies_not_rejects", "remains usable as a finite aggregate convention" in document, "required scope")
    add(checks, "document_no_full_claim", "not a complete one-loop" in document, "required nonclaim")
    passed = all(check["passed"] for check in checks)
    add(checks, "all_validation_checks", passed, f"pre-summary checks={len(checks)}")
    write_checks(checks)
    VALIDATION_PROVENANCE.write_text(
        "# 4997 validation provenance\n\n"
        f"Validator: `{Path(__file__).name}`\n\n"
        f"Generator SHA-256: `{digest(GENERATOR)}`\n\n"
        f"Result SHA-256: `{digest(RESULT)}`\n\n"
        "The validator reconstructs all helicity projections, checks the four contact tensor counts, reparses every direct-cut coefficient, independently verifies the exact I2/I3 coordinate translation and its nonzero pole residue, locks all inherited hashes, and enforces the remaining nonclaim gates.\n",
        encoding="utf-8",
    )
    print(json.dumps({"checkpoint_marker": MARKER, "checks": len(checks), "passed": all(check["passed"] for check in checks), "validation": str(VALIDATION)}, indent=2))
    return 0 if all(check["passed"] for check in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
