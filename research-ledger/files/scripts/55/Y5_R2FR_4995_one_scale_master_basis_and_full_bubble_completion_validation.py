from __future__ import annotations

import csv
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4995"
VALIDATION = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4995_VALIDATION.csv"
VALIDATION_PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"
RESULT = SOURCE / "one_scale_master_basis_and_full_bubble_results.json"
IDENTITY = SOURCE / "one_scale_master_identity.csv"
SAMPLES = SOURCE / "mixed_dimension_samples.csv"
RECONSTRUCTION = SOURCE / "mixed_dimension_basis_reconstruction.csv"
BUBBLES = SOURCE / "finite_bubble_convention.csv"
GATES = SOURCE / "one_scale_master_basis_and_bubble_gate.csv"
DOCUMENT = POST / "4995-Y5-R2FR-one-scale-master-basis-cancellation-and-full-bubble-completion.md"
GENERATOR = POST / "scripts" / "Y5_R2FR_4995_one_scale_master_basis_and_full_bubble_completion.py"

MARKER = "MTS_4995_ONE_SCALE_MASTER_BASIS_AND_FULL_BUBBLE_COMPLETION"
D = sp.Symbol("D")
t = sp.Symbol("t", nonzero=True)
u = sp.Symbol("u", nonzero=True)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def expression(value: str) -> sp.Expr:
    return sp.sympify(value, locals={"D": D, "t": t, "u": u})


def add(checks: list[dict[str, Any]], check: str, passed: bool, detail: str) -> None:
    checks.append({
        "check": check,
        "passed": bool(passed),
        "detail": detail,
        "checkpoint_marker": MARKER,
        "valid_for_full_MTS_claim": False,
    })


def write_csv(path: Path, checks: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)


def main() -> int:
    checks: list[dict[str, Any]] = []
    required = [RESULT, IDENTITY, SAMPLES, RECONSTRUCTION, BUBBLES, GATES, DOCUMENT, GENERATOR]
    for path in required:
        add(checks, f"exists:{path.name}", path.exists(), str(path))
    if not all(path.exists() for path in required):
        write_csv(VALIDATION, checks)
        return 1

    result = json.loads(RESULT.read_text(encoding="utf-8"))
    add(checks, "result_marker", result.get("checkpoint_marker") == MARKER, str(result.get("checkpoint_marker")))
    add(checks, "basis_pole_cancelled", result.get("mixed_dimension_basis_pole_cancelled") is True, "must be true")
    add(checks, "finite_bubble_convention", result.get("finite_4d_Dunbar_bubble_convention_complete") is True, "must be true")
    add(checks, "rational_remainder_open", result.get("nonlocal_rational_J2_remainder_complete") is False, "must remain false")
    add(checks, "complete_amplitude_blocked", result.get("complete_one_loop_phi2h2") is False, "must remain false")
    add(checks, "full_claim_blocked", result.get("valid_for_full_MTS_claim") is False, "must remain false")
    for relative_path, expected_hash in result.get("source_hashes_sha256", {}).items():
        path = ROOT / Path(relative_path)
        add(checks, f"source_hash:{Path(relative_path).name}", path.exists() and digest(path) == expected_hash, relative_path)

    identity_rows = rows(IDENTITY)
    reconstruction_rows = rows(RECONSTRUCTION)
    sample_rows = rows(SAMPLES)
    bubble_rows = rows(BUBBLES)
    gate_rows = rows(GATES)
    for name, table in (("identity", identity_rows), ("reconstruction", reconstruction_rows), ("samples", sample_rows), ("bubbles", bubble_rows), ("gates", gate_rows)):
        add(checks, f"{name}_nonempty", bool(table), str(len(table)))
        add(checks, f"{name}_marker", all(row.get("checkpoint_marker") == MARKER for row in table), "all rows")
        add(checks, f"{name}_nonclaim", all(row.get("valid_for_full_MTS_claim") == "False" for row in table), "all rows")

    epsilon, channel = sp.symbols("epsilon channel", nonzero=True)
    ratio = (D - 4) * channel / (2 * (D - 3))
    add(checks, "epsilon_form_of_master_ratio", sp.cancel(ratio.subs(D, 4 - 2 * epsilon) + epsilon * channel / (1 - 2 * epsilon)) == 0, "ratio=-epsilon*x/(1-2epsilon)")
    add(checks, "identity_rows_closed", all(row.get("status") == "closed" and row.get("residual") == "0" for row in identity_rows), "all exact identities")

    formula_map: dict[tuple[str, str], sp.Expr] = {}
    for row in reconstruction_rows:
        reconstructed = expression(row["reconstructed_formula"])
        expected = expression(row["expected_formula"])
        passed = sp.cancel(reconstructed - expected) == 0 and row["formula_residual"] == "0" and row["heldout_squared_residual"] == "0" and row["status"] == "closed"
        add(checks, f"reconstruction:{row['anchor']}:{row['quantity']}", passed, row["reconstructed_formula"])
        formula_map[(row["anchor"], row["quantity"])] = reconstructed
    for row in sample_rows:
        formula = formula_map[(row["anchor"], "B_su")]
        passed = sp.cancel(formula.subs(D, expression(row["D"])) - expression(row["B_su"])) == 0
        add(checks, f"sample_Bsu:{row['anchor']}:{row['D']}", passed, row["B_su"])

    transformed = {row["identity"]: row for row in identity_rows if row["identity"].endswith("finite_coordinate_transform")}
    add(checks, "anchor_A_transform_limit", transformed.get("anchor_A_finite_coordinate_transform", {}).get("limit_residual") == "0", str(transformed.get("anchor_A_finite_coordinate_transform")))
    add(checks, "anchor_B_transform_limit", transformed.get("anchor_B_finite_coordinate_transform", {}).get("limit_residual") == "0", str(transformed.get("anchor_B_finite_coordinate_transform")))

    bubble_map = {row["component"]: expression(row["coefficient"]) for row in bubble_rows}
    bubble_sum = sp.cancel(bubble_map["C_s_full"] + bubble_map["C_t_full"] + bubble_map["C_u_full"])
    add(checks, "bubble_sum_symbolic_zero", bubble_sum == 0, str(bubble_sum))
    add(checks, "scalar_split_symbolic", sp.cancel(bubble_map["C_s_hh"] + bubble_map["C_s_scalar"] - bubble_map["C_s_full"]) == 0, "C_s_hh+C_s_scalar=C_s")
    expected_cs = t**2 * u**2 * (t**2 + u**2) / 4
    add(checks, "C_s_expected", sp.cancel(bubble_map["C_s_full"] - expected_cs) == 0, str(bubble_map["C_s_full"]))
    add(checks, "bubble_rows_closed", all(row.get("status") == "closed" for row in bubble_rows), "all rows")

    gates = {row["gate"]: row for row in gate_rows}
    for gate in ("primary_source_lock", "exact_one_scale_master_identity", "exceptional_anchor_reconstruction", "generic_anchor_reconstruction", "mixed_coefficient_pole_cancelled", "finite_bubble_convention_complete", "local_R2_counterterm_ambiguity"):
        add(checks, f"gate_closed:{gate}", gates.get(gate, {}).get("passed") == "True" and gates.get(gate, {}).get("status") == "closed", str(gates.get(gate)))
    for gate in ("nonlocal_rational_J2_remainder", "complete_one_loop_phi2h2", "full_MTS_or_local_GR_claim"):
        add(checks, f"gate_open:{gate}", gates.get(gate, {}).get("passed") == "False" and gates.get(gate, {}).get("status") == "open", str(gates.get(gate)))

    document = DOCUMENT.read_text(encoding="utf-8")
    add(checks, "document_states_basis_nonobservability", "not observables" in document, "required caveat")
    add(checks, "document_keeps_J2_open", "d J2" in document and "not fixed" in document, "required blocker")
    add(checks, "document_no_full_claim", "not a full MTS" in document, "required nonclaim")

    passed = all(check["passed"] for check in checks)
    add(checks, "all_validation_checks", passed, f"pre-summary checks={len(checks)}")
    write_csv(VALIDATION, checks)
    VALIDATION_PROVENANCE.write_text(
        "# 4995 validation provenance\n\n"
        f"Validator: `{GENERATOR.parent.name}/{Path(__file__).name}`\n\n"
        f"Generator SHA-256: `{digest(GENERATOR)}`\n\n"
        f"Result SHA-256: `{digest(RESULT)}`\n\n"
        "Validation independently reparses every formula, checks every stored B_su sample, verifies the exact epsilon-form master relation, checks the bubble identities, locks source hashes, and enforces all nonclaim gates.\n",
        encoding="utf-8",
    )
    print(json.dumps({"checkpoint_marker": MARKER, "checks": len(checks), "passed": all(check["passed"] for check in checks), "validation": str(VALIDATION)}, indent=2))
    return 0 if all(check["passed"] for check in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
