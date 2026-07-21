from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4956"
VALIDATION = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4956_VALIDATION.csv"

RESEARCH = POST / "scripts" / "Y5_R2FR_4956_functional_PX_fixed_function_gate.py"
CHECKPOINT = POST / "4956-Y5-R2FR-functional-PX-motion-flow-gravity-source-and-convergence-or-derivative-hierarchy-rejection.md"
PROVENANCE = SOURCE / "PROVENANCE.md"
FORMAL = ROOT / "formalization-workbench" / "972-PPC4161-functional-PX-fixed-function-and-convergence-decision.md"
CLAIMS = ROOT / "formalization-workbench" / "02-claims-register.csv"
VARIABLES = ROOT / "formalization-workbench" / "04-variable-audit.csv"
EQUATIONS = ROOT / "formalization-workbench" / "05-equation-register.md"
RED_TEAM = ROOT / "formalization-workbench" / "06-consistency-red-team.md"
SPINE = ROOT / "formalization-workbench" / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

RESULT = SOURCE / "functional_PX_fixed_function_results.json"
HESSIAN = SOURCE / "functional_PX_Hessian_contract.csv"
CALIBRATION = SOURCE / "functional_PX_calibration.csv"
HOMOTOPY = SOURCE / "polynomial_GR_homotopy_trace.csv"
FIXED_POINT = SOURCE / "polynomial_fixed_point_convergence.csv"
COEFFICIENTS = SOURCE / "functional_coefficient_convergence.csv"
REGULARITY = SOURCE / "functional_regular_convexity_gate.csv"
DECISION = SOURCE / "functional_PX_route_decision.csv"

OUTPUTS = [
    RESULT,
    HESSIAN,
    CALIBRATION,
    HOMOTOPY,
    FIXED_POINT,
    COEFFICIENTS,
    REGULARITY,
    DECISION,
]
DOCUMENTS = [
    RESEARCH,
    CHECKPOINT,
    PROVENANCE,
    FORMAL,
    CLAIMS,
    VARIABLES,
    EQUATIONS,
    RED_TEAM,
    SPINE,
    RESUME,
]

MARKER = "MTS_4956_FUNCTIONAL_PX_FIXED_FUNCTION_GATE"
VALIDATION_MARKER = "MTS_4956_INDEPENDENT_VALIDATION"
SCENARIOS = {"reference_etaN0", "fixed_point_etaNminus2"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def close(left: float, right: float, relative: float = 2.0e-10, absolute: float = 1.0e-14) -> bool:
    return math.isclose(left, right, rel_tol=relative, abs_tol=absolute)


def add(
    checks: list[dict[str, Any]],
    check_id: str,
    requirement: str,
    expected: Any,
    actual: Any,
    passed: bool,
) -> None:
    checks.append(
        {
            "check_id": check_id,
            "requirement": requirement,
            "expected": expected,
            "actual": actual,
            "passed": passed,
            "validation_marker": VALIDATION_MARKER,
        }
    )


def main() -> int:
    checks: list[dict[str, Any]] = []
    before_hashes = {
        str(path): digest(path) for path in OUTPUTS if path.is_file()
    }
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    execution = subprocess.run(
        [sys.executable, str(RESEARCH)],
        cwd=POST,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    add(
        checks,
        "VAL4956_00_research",
        "research runner completes",
        0,
        execution.returncode,
        execution.returncode == 0 and f"{MARKER}_DONE" in execution.stdout,
    )

    missing = [str(path) for path in OUTPUTS + DOCUMENTS if not path.is_file()]
    add(
        checks,
        "VAL4956_01_paths",
        "all output and synchronized document paths exist",
        [],
        missing,
        not missing,
    )
    if missing or execution.returncode != 0:
        VALIDATION.parent.mkdir(parents=True, exist_ok=True)
        with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
            writer.writeheader()
            writer.writerows(checks)
        return 1

    compile_failures: list[str] = []
    for path in (RESEARCH, Path(__file__)):
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as error:
            compile_failures.append(f"{path}:{error}")
    add(
        checks,
        "VAL4956_02_compile",
        "research and validator compile without bytecode output",
        [],
        compile_failures,
        not compile_failures,
    )

    result = json.loads(RESULT.read_text(encoding="utf-8"))
    hessian = read_csv(HESSIAN)
    calibration = read_csv(CALIBRATION)
    homotopy = read_csv(HOMOTOPY)
    fixed = read_csv(FIXED_POINT)
    coefficients = read_csv(COEFFICIENTS)
    regularity = read_csv(REGULARITY)
    decisions = read_csv(DECISION)
    tables = (hessian, calibration, homotopy, fixed, coefficients, regularity, decisions)

    marker_ok = result["checkpoint_marker"] == MARKER and all(
        row["checkpoint_marker"] == MARKER for table in tables for row in table
    )
    add(checks, "VAL4956_03_marker", "all evidence uses one checkpoint marker", MARKER, result["checkpoint_marker"], marker_ok)
    nonclaim_ok = all(
        not as_bool(row["valid_for_full_MTS_claim"])
        for table in tables
        for row in table
    )
    add(checks, "VAL4956_04_nonclaim", "all generated rows remain private nonclaim", True, nonclaim_ok, nonclaim_ok)

    hash_failures = [
        path
        for path, expected in result["source_hashes"].items()
        if not Path(path).is_file() or digest(Path(path)) != expected
    ]
    add(checks, "VAL4956_05_source_hashes", "all source hashes independently recompute", [], hash_failures, result["source_hashes_match"] and not hash_failures)
    clauses_ok = len(result["source_clause_checks"]) == 9 and all(result["source_clause_checks"].values())
    add(checks, "VAL4956_06_source_clauses", "all nine source clauses pass", "9 true", result["source_clause_checks"], clauses_ok)

    hessian_ids = {row["contract_id"] for row in hessian}
    required_hessian = {f"H4956_{index:02d}_{suffix}" for index, suffix in enumerate(("metric_block", "mixed_block", "scalar_block", "regulator_insertion", "functional_flow", "normalization"), start=1)}
    hessian_ok = len(hessian) == 6 and hessian_ids == required_hessian and all(as_bool(row["passed"]) for row in hessian)
    add(checks, "VAL4956_07_hessian", "all six functional Hessian and flow clauses exist", sorted(required_hessian), sorted(hessian_ids), hessian_ok)

    scalar_q2 = 5.0 * 0.2**2 / (8.0 * math.pi**2) + 0.1 / (4.0 * math.pi**2)
    scalar_q3 = -37.0 * 0.2**3 / (10.0 * math.pi**2) + 21.0 * 0.2 * (-0.1) / (8.0 * math.pi**2) - 5.0 * 0.03 / (12.0 * math.pi**2)
    calibration_failures: list[str] = []
    for row in calibration:
        actual = float(row["actual"])
        if row["calibration_id"] == "CAL4956_scalar_Q2":
            expected = scalar_q2
        elif row["calibration_id"] == "CAL4956_scalar_Q3":
            expected = scalar_q3
        elif row["calibration_id"] == "CAL4956_gravity_Q2":
            expected = 20.0
        elif row["calibration_id"] == "CAL4956_gravity_Q3":
            expected = -208.0 * math.pi / 5.0
        else:
            calibration_failures.append(row["calibration_id"])
            continue
        if not close(actual, expected, relative=2.0e-13) or not as_bool(row["passed"]):
            calibration_failures.append(row["calibration_id"])
    calibration_ok = len(calibration) == 10 and not calibration_failures
    add(checks, "VAL4956_08_calibration", "two scalar and eight gravity calibration rows independently match", "10 exact targets", calibration_failures, calibration_ok)
    add(checks, "VAL4956_09_calibration_error", "maximum calibration relative error is below 1e-12", "<1e-12", result["calibration"]["maximum_relative_error"], result["calibration"]["all_rows_pass"] and float(result["calibration"]["maximum_relative_error"]) < 1.0e-12)

    homotopy_shapes = {
        scenario: sum(row["scenario"] == scenario for row in homotopy)
        for scenario in SCENARIOS
    }
    homotopy_ok = len(homotopy) == 68 and homotopy_shapes == {scenario: 34 for scenario in SCENARIOS} and all(as_bool(row["step_passed"]) for row in homotopy)
    add(checks, "VAL4956_10_homotopy_shape", "both three-stage homotopies contain 34 passing rows", {scenario: 34 for scenario in SCENARIOS}, homotopy_shapes, homotopy_ok)
    endpoint_failures: list[str] = []
    for scenario in SCENARIOS:
        endpoint_rows = [
            row
            for row in homotopy
            if row["scenario"] == scenario
            and row["homotopy_type"] == "N12_GRAVITY_FIXED_POINT_TO_GAUSSIAN"
        ]
        endpoint = endpoint_rows[-1]
        values = json.loads(endpoint["coefficients_a2_up_json"])
        if float(endpoint["g"]) != 0.0 or max(abs(float(value)) for value in values) > 1.0e-12:
            endpoint_failures.append(scenario)
    add(checks, "VAL4956_11_gaussian_endpoint", "both N12 trajectories return to the Gaussian coefficient origin", [], endpoint_failures, not endpoint_failures)

    fixed_shape = len(fixed) == 22 and {row["scenario"] for row in fixed} == SCENARIOS
    order_shape = all(
        {int(row["polynomial_order"]) for row in fixed if row["scenario"] == scenario}
        == set(range(2, 13))
        for scenario in SCENARIOS
    )
    add(checks, "VAL4956_12_fixed_shape", "orders N=2 through N=12 exist in both schemes", "22 rows", len(fixed), fixed_shape and order_shape)
    n12 = {row["scenario"]: row for row in fixed if int(row["polynomial_order"]) == 12}
    endpoint_norms_ok = all(float(row["gaussian_endpoint_norm"]) < 1.0e-12 for row in n12.values())
    add(checks, "VAL4956_13_endpoint_norm", "N12 output records zero Gaussian endpoint norm", "<1e-12", {key: row["gaussian_endpoint_norm"] for key, row in n12.items()}, endpoint_norms_ok)

    targets = {
        "reference_etaN0": (-0.057903408163605945, -0.08980815464115473, 0.07018018016583172, 4.350637889249325),
        "fixed_point_etaNminus2": (-0.06569466057802394, -0.12252807013362962, 0.11542500443652522, 3.8441357677763572),
    }
    coordinate_failures: list[str] = []
    for scenario, expected in targets.items():
        row = n12[scenario]
        actual = tuple(float(row[key]) for key in ("eta_psi", "a2", "a3", "r3_fixed_point"))
        if not all(close(left, right) for left, right in zip(actual, expected)):
            coordinate_failures.append(scenario)
    add(checks, "VAL4956_14_N12_coordinates", "both N12 low-coordinate solutions reproduce", [], coordinate_failures, not coordinate_failures)

    convergence_ok = len(coefficients) == 8 and all(as_bool(row["converged"]) for row in coefficients)
    maximum_spread = max(float(row["relative_spread"]) for row in coefficients)
    add(checks, "VAL4956_15_low_convergence", "a2 a3 eta_psi and r3 converge in both schemes", "8 rows below 1e-4", maximum_spread, convergence_ok and maximum_spread < 1.0e-4)
    bracket = sorted(float(row["r3_fixed_point"]) for row in n12.values())
    add(checks, "VAL4956_16_r3_bracket", "UV fixed-germ r3 bracket is finite and ordered", "[3.8441,4.3507]", bracket, 3.8441 < bracket[0] < bracket[1] < 4.3507)

    local_rows = [row for row in regularity if close(float(row["x_domain_max"]), 0.1)]
    global_rows = [row for row in regularity if close(float(row["x_domain_max"]), 0.25)]
    local_ok = len(local_rows) == 2 and all(row["status"] == "LOCAL_GERM_REGULAR" and as_bool(row["scalar_convex"]) and float(row["minimum_singular_value"]) > 0.3 for row in local_rows)
    global_ok = len(global_rows) == 2 and all(row["status"] == "GLOBAL_REGULARITY_NOT_ESTABLISHED" and not as_bool(row["scalar_convex"]) for row in global_rows)
    add(checks, "VAL4956_17_local_regularity", "both schemes are convex and Hessian-regular on x<=0.1", True, local_ok, local_ok)
    add(checks, "VAL4956_18_global_block", "neither N12 scheme establishes regularity on x<=0.25", True, global_ok, global_ok)
    zeros_ok = all(0.1 < float(row["first_longitudinal_zero"]) < 0.25 for row in n12.values())
    add(checks, "VAL4956_19_longitudinal_zero", "both first longitudinal zeros lie outside local and inside global domain", "0.1<zero<0.25", {key: row["first_longitudinal_zero"] for key, row in n12.items()}, zeros_ok)
    growth_ok = all(abs(float(row["a12"])) > 1.0e6 and 0.09 < float(row["last_coefficient_ratio_radius"]) < 0.12 for row in n12.values())
    add(checks, "VAL4956_20_high_order_warning", "large alternating tail and finite-radius warning remain explicit", True, growth_ok, growth_ok)

    required_statuses = {
        "FUNCTIONAL_PX_HESSIAN_DERIVED",
        "FUNCTIONAL_PROJECTOR_EXACTLY_CALIBRATED",
        "GAUSSIAN_CONNECTED_POLYNOMIAL_ROOTS_THROUGH_N12",
        "LOW_FUNCTIONAL_COORDINATES_CONVERGED",
        "LOCAL_FIXED_FUNCTION_GERM_RETAINED",
        "GLOBAL_FIXED_FUNCTION_NOT_ESTABLISHED",
        "UV_R3_GERM_DERIVED_IR_R3_OPEN",
        "FULL_MOTION_HESSIAN_NOT_COMPLETE",
        "4947_LOCAL_GR_NEWTON_MAXWELL_RETAINED",
        "FULL_MTS_PROMOTION_BLOCKED",
    }
    decision_statuses = {row["status"] for row in decisions}
    decisions_ok = len(decisions) == 10 and decision_statuses == required_statuses
    add(checks, "VAL4956_21_decisions", "all ten route decisions are present", sorted(required_statuses), sorted(decision_statuses), decisions_ok)

    gates = result["gates"]
    gates_ok = gates["all_N12_homotopies_pass"] and gates["low_coordinates_converged"] and gates["local_x_le_0p1_fixed_function_germ"] and not gates["global_x_le_0p25_fixed_function"] and gates["UV_r3_germ"] == "DERIVED_SCHEME_BRACKETED" and gates["IR_r3_trajectory"] == "OPEN" and not gates["full_motion_Hessian"] and gates["local_GR_Newton_Maxwell_4947"] == "RETAINED" and not gates["full_MTS"]
    add(checks, "VAL4956_22_result_gates", "result preserves local success and global/full-theory blocks", True, gates, gates_ok)
    orders_ok = result["projection"]["polynomial_orders"] == list(range(2, 13))
    add(checks, "VAL4956_23_projection_orders", "result records every executed polynomial order", list(range(2, 13)), result["projection"]["polynomial_orders"], orders_ok)

    checkpoint_text = CHECKPOINT.read_text(encoding="utf-8")
    formal_text = FORMAL.read_text(encoding="utf-8")
    claims_text = CLAIMS.read_text(encoding="utf-8")
    variables_text = VARIABLES.read_text(encoding="utf-8")
    equations_text = EQUATIONS.read_text(encoding="utf-8")
    red_text = RED_TEAM.read_text(encoding="utf-8")
    spine_text = SPINE.read_text(encoding="utf-8")
    resume_text = RESUME.read_text(encoding="utf-8")
    documentation_ok = all(
        token in text
        for token, text in (
            ("MTS_FUNCTIONAL_PX_FIXED_FUNCTION_DECISION_4956", checkpoint_text),
            ("PPC4161_FUNCTIONAL_PX_FIXED_FUNCTION_4956", formal_text),
            ('"L-798"', claims_text),
            ("PredictivityStatus4956_MTS", variables_text),
            ("## 1.249", equations_text),
            ("## 200.", red_text),
            ("checkpoint 4956", spine_text),
            ("Current checkpoint 4956 handoff", resume_text),
        )
    )
    add(checks, "VAL4956_24_documents", "checkpoint 4956 is synchronized across every register", True, documentation_ok, documentation_ok)
    claim_rows = read_csv(CLAIMS)
    variable_rows = read_csv(VARIABLES)
    registry_ok = sum(row["claim_id"] == "L-798" for row in claim_rows) == 1 and sum(row["symbol"] == "PredictivityStatus4956_MTS" for row in variable_rows) == 1 and len(claim_rows[-1]) == 13 and len(variable_rows[-1]) == 11
    add(checks, "VAL4956_25_registry_csv", "claim and variable registers parse with unique 4956 rows", True, registry_ok, registry_ok)
    prohibited = ["FULL_MTS_TRUE", "GLOBAL_FIXED_FUNCTION_DERIVED", "IR_R3_DERIVED", "O2_O4_O5_COMPLETE"]
    synchronized = "\n".join((checkpoint_text, formal_text, equations_text, red_text, spine_text, resume_text))
    present = [token for token in prohibited if token in synchronized]
    add(checks, "VAL4956_26_prohibitions", "synchronized prose contains no false promotion marker", [], present, not present)

    provenance_text = PROVENANCE.read_text(encoding="utf-8")
    provenance_ok = all(value in provenance_text for value in result["source_hashes"].values())
    add(checks, "VAL4956_27_provenance", "provenance records every locked source hash", True, provenance_ok, provenance_ok)
    after_hashes = {str(path): digest(path) for path in OUTPUTS}
    deterministic = len(before_hashes) == len(OUTPUTS) and before_hashes == after_hashes
    add(checks, "VAL4956_28_determinism", "one full rerun reproduces every evidence-file hash", True, deterministic, deterministic)
    pycache = list((POST / "scripts").glob("__pycache__"))
    add(checks, "VAL4956_29_pycache", "no script bytecode cache remains", [], [str(path) for path in pycache], not pycache)
    hash_report = {
        "research_sha256": digest(RESEARCH),
        "result_sha256": digest(RESULT),
        "checkpoint_sha256": digest(CHECKPOINT),
    }
    add(checks, "VAL4956_30_hash_report", "reproducibility hashes are valid SHA-256 values", "three 64-character hashes", hash_report, all(len(value) == 64 for value in hash_report.values()))

    all_previous = all(as_bool(row["passed"]) for row in checks)
    add(checks, "VAL4956_31_complete", "all preceding independent checks pass", True, all_previous, all_previous)
    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)
    return 0 if all(as_bool(row["passed"]) for row in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())

