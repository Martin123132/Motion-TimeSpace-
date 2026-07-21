from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4996"
VALIDATION = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4996_VALIDATION.csv"
VALIDATION_PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"

RESULT = SOURCE / "generic_D_scalar_box_and_mixed_correction_results.json"
COEFFICIENTS = SOURCE / "generic_D_scalar_box_coefficients.csv"
SLICES = SOURCE / "rank_four_descendant_reconstruction.csv"
ANCHORS = SOURCE / "exact_IBP_anchor_checks.csv"
CROSS = SOURCE / "mixed_massive_cross_channel_correction.csv"
CONTRACT = SOURCE / "massive_cut_completion_contract.csv"
GATES = SOURCE / "generic_D_scalar_box_and_mixed_correction_gate.csv"
DOCUMENT = POST / "4996-Y5-R2FR-generic-D-scalar-box-and-mixed-massive-correction.md"
GENERATOR = POST / "scripts" / "Y5_R2FR_4996_generic_D_scalar_box_and_mixed_massive_correction.py"
REDUCER_SOURCE = POST / "scripts" / "Y5_R2FR_4994_strict_4d_mixed_bubble_and_evanescent_pole.py"

MARKER = "MTS_4996_GENERIC_D_SCALAR_BOX_AND_MIXED_MASSIVE_CORRECTION"
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


def load_base_reducer() -> type:
    spec = importlib.util.spec_from_file_location("mts_reducer_4994_validation", REDUCER_SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {REDUCER_SOURCE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.OneLoopNullNumeratorReducer


BaseReducer = load_base_reducer()


class ScalarSCutReducer(BaseReducer):
    def _kinematics(self) -> tuple[list[list[Fraction]], list[Fraction]]:
        tv, uv = self.t_value, self.u_value
        lambdas = {1: sp.Matrix([1, 0]), 2: sp.Matrix([0, 1]), 3: sp.Matrix([1, -uv]), 4: sp.Matrix([1, tv])}
        tildes = {1: sp.Matrix([-1, -1]), 2: sp.Matrix([uv, -tv]), 3: sp.Matrix([1, 0]), 4: sp.Matrix([0, 1])}
        momenta = {index: lambdas[index] * tildes[index].T for index in range(1, 5)}
        shifts = {"A": momenta[1], "B": momenta[2], "C": -momenta[4], "D": -momenta[3]}
        loop = [sp.zeros(2), momenta[1] + momenta[2], shifts[self.topology[0]], shifts[self.topology[1]]]
        return (
            [[self._fraction(self._mass_squared(loop[left] - loop[right])) for right in range(4)] for left in range(4)],
            [self._fraction(shift[0, 0] - shift[0, 1]) for shift in loop],
        )


def main() -> int:
    checks: list[dict[str, Any]] = []
    required = [RESULT, COEFFICIENTS, SLICES, ANCHORS, CROSS, CONTRACT, GATES, DOCUMENT, GENERATOR, REDUCER_SOURCE]
    for path in required:
        add(checks, f"exists:{path.name}", path.exists(), str(path))
    if not all(path.exists() for path in required):
        write_checks(checks)
        return 1

    result = json.loads(RESULT.read_text(encoding="utf-8"))
    add(checks, "result_marker", result.get("checkpoint_marker") == MARKER, str(result.get("checkpoint_marker")))
    add(checks, "scalar_boxes_complete", result.get("generic_D_scalar_shared_box_sector_complete") is True, "must be true")
    add(checks, "mixed_epsilon_correction_complete", result.get("mixed_linear_epsilon_box_correction_complete") is True, "must be true")
    add(checks, "old_mixed_rejected", result.get("old_generic_D_mixed_continuation_rejected_as_physical") is True, "must be true")
    for key in ("generic_D_full_scalar_triangle_complete", "generic_D_internal_graviton_state_sum_complete", "cut_free_dJ2_remainder_complete", "complete_one_loop_phi2h2", "outer_cut_complete", "valid_for_full_MTS_claim"):
        add(checks, f"blocked:{key}", result.get(key) is False, "must remain false")
    for relative_path, expected in result.get("source_hashes_sha256", {}).items():
        path = ROOT / Path(relative_path)
        add(checks, f"source_hash:{Path(relative_path).name}", path.exists() and digest(path) == expected, relative_path)
    add(checks, "formalization_tree_unchanged", tree_digest(ROOT / "formalization-workbench") == result.get("formalization_workbench_tree_sha256"), result.get("formalization_workbench_tree_sha256", "missing"))

    tables = {"coefficients": rows(COEFFICIENTS), "slices": rows(SLICES), "anchors": rows(ANCHORS), "cross": rows(CROSS), "contract": rows(CONTRACT), "gates": rows(GATES)}
    for name, table in tables.items():
        add(checks, f"{name}_nonempty", bool(table), str(len(table)))
        add(checks, f"{name}_marker", all(row.get("checkpoint_marker") == MARKER for row in table), "all rows")
        add(checks, f"{name}_nonclaim", all(row.get("valid_for_full_MTS_claim") == "False" for row in table), "all rows")

    by_name = {row["coefficient"]: row for row in tables["coefficients"] if row.get("coefficient")}
    bst = expression(by_name["B_st_scalar(D)"]["formula"])
    bsu = expression(by_name["B_su_scalar(D)"]["formula"])
    tdesc = expression(by_name["T_s_rank4_descendant(D)"]["formula"])
    contact = expression(by_name["Delta_T_s_contact(D=4)"]["formula"])
    epsilon_correction = expression(by_name["delta_B_su_mixed^(epsilon)"]["formula"])
    add(checks, "box_crossing", sp.factor(bst.xreplace({t: u, u: t}) - bsu) == 0, "t<->u")
    add(checks, "Bst_D4", sp.factor(bst.subs(D, 4) - s**4 * t**4 / 32) == 0, str(bst.subs(D, 4)))
    add(checks, "Bsu_D4", sp.factor(bsu.subs(D, 4) - s**4 * u**4 / 32) == 0, str(bsu.subs(D, 4)))
    add(checks, "triangle_descendant_symmetry", sp.factor(tdesc.xreplace({t: u, u: t}) - tdesc) == 0, "t<->u")
    add(checks, "contact_symmetry", sp.factor(contact.xreplace({t: u, u: t}) - contact) == 0, "t<->u")
    add(checks, "epsilon_correction_exact", sp.factor(epsilon_correction + u**4 * (t + u)**2 * (11 * t**2 - 14 * t * u + 11 * u**2) / 192) == 0, str(epsilon_correction))

    cross_map = {row["audit"]: row for row in tables["cross"]}
    add(checks, "D4_cross_channel_zero", cross_map["D4_shared_box_closure"]["required_missing_correction"] == "0", str(cross_map["D4_shared_box_closure"]))
    add(checks, "D5_failure_witness", cross_map["D5_failure_witness"]["required_missing_correction"] == "621/128", str(cross_map["D5_failure_witness"]))
    add(checks, "cross_residuals_zero", all(row["residual"] == "0" for row in tables["cross"]), "all cross rows")
    add(checks, "slice_residuals_zero", all(row.get("held_out_residuals", "0") in ("0", "0;0") for row in tables["slices"] if row["reconstruction"].startswith("raw_triangle")), "all held-out dimensions")
    add(checks, "anchor_residuals_zero", all((row.get("formula_residual") or "0") == "0" for row in tables["anchors"]), "all exact anchors")

    # Independent exact reducer check at a point not used as a fit dimension for the box formula.
    dimension = Fraction(9, 2)
    scalar_values: dict[str, sp.Rational] = {}
    for topology, label in (("AC", "B_st_scalar"), ("AD", "B_su_scalar")):
        reducer = ScalarSCutReducer(1, 3, topology, dimension)
        value = reducer.coefficient_to((0, 1, 1, 1, 1))
        scalar_values[label] = sp.Rational(value.numerator, value.denominator) * (1 * 3) ** 4 / 16
    substitutions = {t: 1, u: 3, D: sp.Rational(9, 2)}
    add(checks, "independent_IBP_Bst", sp.factor(scalar_values["B_st_scalar"] - bst.subs(substitutions)) == 0, str(scalar_values["B_st_scalar"]))
    add(checks, "independent_IBP_Bsu", sp.factor(scalar_values["B_su_scalar"] - bsu.subs(substitutions)) == 0, str(scalar_values["B_su_scalar"]))

    gates = {row["gate"]: row for row in tables["gates"]}
    for gate in ("primary_source_lock", "D_scalar_tree_trace_cancellation", "generic_D_scalar_shared_boxes", "mixed_linear_epsilon_box_correction"):
        add(checks, f"gate_closed:{gate}", gates[gate]["passed"] == "True" and gates[gate]["status"] == "closed", str(gates[gate]))
    for gate in ("generic_D_full_scalar_triangle", "generic_D_internal_graviton_states", "cut_free_dJ2_remainder", "complete_outer_cut_or_full_MTS"):
        add(checks, f"gate_open:{gate}", gates[gate]["passed"] == "False" and gates[gate]["status"] == "open", str(gates[gate]))

    document = DOCUMENT.read_text(encoding="utf-8")
    add(checks, "document_rejects_old_continuation", "retracts any physical interpretation" in document, "required correction")
    add(checks, "document_separates_triangle", "not the full scalar triangle" in document.replace("**", ""), "required caveat")
    add(checks, "document_no_full_claim", "not a complete one-loop" in document, "required nonclaim")

    passed_before_summary = all(check["passed"] for check in checks)
    add(checks, "all_validation_checks", passed_before_summary, f"pre-summary checks={len(checks)}")
    write_checks(checks)
    VALIDATION_PROVENANCE.write_text(
        "# 4996 validation provenance\n\n"
        f"Validator: `{Path(__file__).name}`\n\n"
        f"Generator SHA-256: `{digest(GENERATOR)}`\n\n"
        f"Result SHA-256: `{digest(RESULT)}`\n\n"
        "The validator independently re-runs two generic-D scalar box reductions at (t,u,D)=(1,3,9/2), checks all symbolic limits and crossing identities, verifies the 621/128 failure witness and linear-epsilon correction, locks source hashes, and enforces every nonclaim gate.\n",
        encoding="utf-8",
    )
    print(json.dumps({"checkpoint_marker": MARKER, "checks": len(checks), "passed": all(check["passed"] for check in checks), "validation": str(VALIDATION)}, indent=2))
    return 0 if all(check["passed"] for check in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
