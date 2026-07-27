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
SOURCE = POST / "source-intake" / "functional_rg" / "4957"
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_4957_VALIDATION.csv"
)

RESEARCH = POST / "scripts" / "Y5_R2FR_4957_functional_PX_O4_GR_trajectory.py"
CHECKPOINT = POST / "4957-Y5-R2FR-functional-PX-GR-connected-trajectory-and-O2-O4-O5-residual-bound-or-motion-sector-rejection.md"
PROVENANCE = SOURCE / "PROVENANCE.md"
FORMAL = ROOT / "formalization-workbench" / "973-PPC4161-functional-PX-O4-GR-trajectory-and-local-residual-decision.md"
CLAIMS = ROOT / "formalization-workbench" / "02-claims-register.csv"
VARIABLES = ROOT / "formalization-workbench" / "04-variable-audit.csv"
EQUATIONS = ROOT / "formalization-workbench" / "05-equation-register.md"
RED_TEAM = ROOT / "formalization-workbench" / "06-consistency-red-team.md"
SPINE = ROOT / "formalization-workbench" / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

RESULT = SOURCE / "functional_PX_O4_GR_trajectory_results.json"
FIXED = SOURCE / "combined_functional_fixed_point_convergence.csv"
SPECTRUM = SOURCE / "combined_functional_stability_spectrum.csv"
TRAJECTORY = SOURCE / "functional_PX_O4_GR_trajectory.csv"
ENDPOINT = SOURCE / "infrared_motion_coordinate_convergence.csv"
REGULARITY = SOURCE / "trajectory_functional_regularity_gate.csv"
RESIDUAL = SOURCE / "local_operator_residual_gate.csv"
DECISION = SOURCE / "functional_trajectory_decision.csv"

OUTPUTS = [
    RESULT,
    FIXED,
    SPECTRUM,
    TRAJECTORY,
    ENDPOINT,
    REGULARITY,
    RESIDUAL,
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

MARKER = "MTS_4957_FUNCTIONAL_PX_O4_GR_TRAJECTORY"
VALIDATION_MARKER = "MTS_4957_INDEPENDENT_VALIDATION"
SCHEMES = {"dynamic_etaN", "reference_etaN0"}
ORDERS = {6, 8}


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


def close(
    left: float,
    right: float,
    relative: float = 2.0e-9,
    absolute: float = 1.0e-13,
) -> bool:
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


def write_validation(checks: list[dict[str, Any]]) -> None:
    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)


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
        "VAL4957_00_research",
        "research runner completes",
        0,
        execution.returncode,
        execution.returncode == 0 and f"{MARKER}_DONE" in execution.stdout,
    )

    missing = [str(path) for path in OUTPUTS + DOCUMENTS if not path.is_file()]
    add(
        checks,
        "VAL4957_01_paths",
        "all output and synchronized document paths exist",
        [],
        missing,
        not missing,
    )
    if missing or execution.returncode != 0:
        write_validation(checks)
        return 1

    compile_failures: list[str] = []
    for path in (RESEARCH, Path(__file__)):
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as error:
            compile_failures.append(f"{path}:{error}")
    add(
        checks,
        "VAL4957_02_compile",
        "research and validator compile without bytecode output",
        [],
        compile_failures,
        not compile_failures,
    )

    result = json.loads(RESULT.read_text(encoding="utf-8"))
    fixed = read_csv(FIXED)
    spectrum = read_csv(SPECTRUM)
    trajectory = read_csv(TRAJECTORY)
    endpoint = read_csv(ENDPOINT)
    regularity = read_csv(REGULARITY)
    residual = read_csv(RESIDUAL)
    decisions = read_csv(DECISION)
    tables = (fixed, spectrum, trajectory, endpoint, regularity, residual, decisions)

    marker_ok = result["checkpoint_marker"] == MARKER and all(
        row["checkpoint_marker"] == MARKER for table in tables for row in table
    )
    add(
        checks,
        "VAL4957_03_marker",
        "all evidence uses one checkpoint marker",
        MARKER,
        result["checkpoint_marker"],
        marker_ok,
    )
    nonclaim_ok = all(
        not as_bool(row["valid_for_full_MTS_claim"])
        for table in tables
        for row in table
    )
    add(
        checks,
        "VAL4957_04_nonclaim",
        "all generated rows remain private nonclaim",
        True,
        nonclaim_ok,
        nonclaim_ok,
    )

    hash_failures = [
        path
        for path, expected in result["source_hashes"].items()
        if not Path(path).is_file() or digest(Path(path)) != expected
    ]
    add(
        checks,
        "VAL4957_05_source_hashes",
        "all locked parent hashes independently recompute",
        [],
        hash_failures,
        result["source_hashes_match"] and not hash_failures,
    )
    clauses_ok = (
        len(result["source_clause_checks"]) == 7
        and all(result["source_clause_checks"].values())
    )
    add(
        checks,
        "VAL4957_06_source_clauses",
        "all seven parent interpretation clauses pass",
        "7 true",
        result["source_clause_checks"],
        clauses_ok,
    )

    fixed_shape = (
        len(fixed) == 14
        and {row["scheme"] for row in fixed} == SCHEMES
        and all(
            {
                int(row["polynomial_order"])
                for row in fixed
                if row["scheme"] == scheme
            }
            == set(range(2, 9))
            for scheme in SCHEMES
        )
        and all(
            row["status"] == "SELF_CONSISTENT_COMBINED_FIXED_POINT"
            for row in fixed
        )
    )
    add(
        checks,
        "VAL4957_07_fixed_shape",
        "combined roots exist at N=2 through N=8 in both schemes",
        "14 roots",
        len(fixed),
        fixed_shape,
    )

    n8 = {
        row["scheme"]: row
        for row in fixed
        if int(row["polynomial_order"]) == 8
    }
    targets = {
        "dynamic_etaN": (
            0.13088296933325305,
            -0.001835563680440286,
            -0.06586596415174378,
            -0.12315660009442461,
            0.11646517125639921,
        ),
        "reference_etaN0": (
            0.13088239715622346,
            -0.0018318937400760304,
            -0.058052759171999244,
            -0.09026375417780831,
            0.07079262121935832,
        ),
    }
    coordinate_failures: list[str] = []
    for scheme, expected in targets.items():
        actual = tuple(
            float(n8[scheme][key])
            for key in ("g", "u_O4", "eta_psi", "a2", "a3")
        )
        if not all(close(left, right) for left, right in zip(actual, expected)):
            coordinate_failures.append(scheme)
    add(
        checks,
        "VAL4957_08_fixed_coordinates",
        "both N8 combined fixed points reproduce",
        [],
        coordinate_failures,
        not coordinate_failures,
    )
    fixed_residual = max(float(row["scaled_beta_residual"]) for row in fixed)
    add(
        checks,
        "VAL4957_09_fixed_residual",
        "every combined fixed-point scaled residual is below 1e-8",
        "<1e-8",
        fixed_residual,
        fixed_residual < 1.0e-8,
    )

    spectrum_shape = (
        len(spectrum) == 48
        and {row["scheme"] for row in spectrum} == SCHEMES
        and {int(row["polynomial_order"]) for row in spectrum} == ORDERS
    )
    relevant_failures: list[str] = []
    eigenvalues: dict[str, float] = {}
    for scheme in SCHEMES:
        for order in ORDERS:
            rows = [
                row
                for row in spectrum
                if row["scheme"] == scheme
                and int(row["polynomial_order"]) == order
            ]
            relevant = [row for row in rows if as_bool(row["relevant"])]
            connected = [
                row for row in rows if as_bool(row["gravity_connected_mode"])
            ]
            key = f"{scheme}_N{order}"
            if len(relevant) != 1 or len(connected) != 1 or relevant[0] != connected[0]:
                relevant_failures.append(key)
            else:
                eigenvalues[key] = float(relevant[0]["beta_eigenvalue_real"])
                if not (-1.90 < eigenvalues[key] < -1.88):
                    relevant_failures.append(key)
    add(
        checks,
        "VAL4957_10_stability",
        "N6 and N8 in both schemes have exactly one GR-connected relevant mode",
        "4 unique modes",
        relevant_failures,
        spectrum_shape and not relevant_failures,
    )

    trajectory_shape = (
        len(trajectory) == 484
        and all(
            len(
                [
                    row
                    for row in trajectory
                    if row["scheme"] == scheme
                    and int(row["polynomial_order"]) == order
                ]
            )
            == 121
            for scheme in SCHEMES
            for order in ORDERS
        )
    )
    add(
        checks,
        "VAL4957_11_trajectory_shape",
        "four functional trajectories each contain 121 samples",
        484,
        len(trajectory),
        trajectory_shape,
    )

    trajectory_failures: list[str] = []
    endpoint_rows: dict[str, dict[str, str]] = {}
    for scheme in SCHEMES:
        for order in ORDERS:
            rows = sorted(
                (
                    row
                    for row in trajectory
                    if row["scheme"] == scheme
                    and int(row["polynomial_order"]) == order
                ),
                key=lambda row: int(row["sample_index"]),
            )
            key = f"{scheme}_N{order}"
            endpoint_rows[key] = rows[-1]
            gravity_values = [float(row["g"]) for row in rows]
            if (
                not close(gravity_values[-1], 1.0e-10, relative=1.0e-8, absolute=1.0e-18)
                or not all(
                    gravity_values[index + 1] <= gravity_values[index] * (1.0 + 1.0e-10)
                    for index in range(len(gravity_values) - 1)
                )
                or not all(as_bool(row["convex_x_le_0p1"]) for row in rows)
                or max(float(row["eta_self_consistency_residual"]) for row in rows)
                > 1.0e-10
            ):
                trajectory_failures.append(key)
    add(
        checks,
        "VAL4957_12_trajectory_endpoint",
        "all trajectories monotonically reach g=1e-10 and remain locally convex",
        [],
        trajectory_failures,
        not trajectory_failures,
    )

    convergence_ok = (
        len(endpoint) == 10
        and all(as_bool(row["converged_below_1e_minus_3"]) for row in endpoint)
    )
    maximum_order_difference = max(
        float(row["relative_difference"]) for row in endpoint
    )
    add(
        checks,
        "VAL4957_13_order_convergence",
        "all five infrared coordinates converge from N6 to N8 in both schemes",
        "10 rows below 1e-3",
        maximum_order_difference,
        convergence_ok and maximum_order_difference < 1.0e-3,
    )

    regularity_ok = (
        len(regularity) == 10
        and all(
            row["status"] == "TRAJECTORY_LOCAL_HESSIAN_REGULAR"
            and as_bool(row["scalar_convex"])
            and int(row["polynomial_order"]) == 8
            for row in regularity
        )
    )
    minimum_singular = min(
        float(row["minimum_singular_value"]) for row in regularity
    )
    add(
        checks,
        "VAL4957_14_regularity",
        "both N8 trajectories pass five direct full-Hessian local scans",
        "10 regular rows and min>0.3",
        minimum_singular,
        regularity_ok and minimum_singular > 0.3,
    )

    residual_status = {row["operator"]: row for row in residual}
    residual_ok = (
        len(residual) == 5
        and residual_status["O2=X(nabla_nabla_psi)^2"]["local_GR_status"]
        == "EXACTLY_SILENT_ON_PSI_ZERO"
        and residual_status["O4=C2 X"]["nonzero_state_status"]
        == "SELF_CONSISTENT_TRAJECTORY_INCLUDED"
        and residual_status["O5=C(nabla_psi)^2(nabla_nabla_psi)"]["local_GR_status"]
        == "EXACTLY_FORBIDDEN"
        and residual_status["raw_to_essential_X2_X3_map"]["nonzero_state_status"]
        == "PHYSICAL_RATE_PROMOTION_BLOCKED"
    )
    add(
        checks,
        "VAL4957_15_operator_residuals",
        "O2 O4 O5 and essential-map statuses preserve the local/full-theory firewall",
        True,
        residual_ok,
        residual_ok,
    )

    required_decisions = {
        "SELF_CONSISTENT_COMBINED_FIXED_POINTS_RETAINED",
        "ONE_GR_CONNECTED_RELEVANT_DIRECTION_RETAINED",
        "FUNCTIONAL_GR_CONNECTED_TRAJECTORY_RETAINED",
        "TRAJECTORY_LOCAL_REGULARITY_RETAINED",
        "O2_LOCAL_LINEAR_RESIDUAL_EXACT_ZERO",
        "O4_ETA_WEIGHTED_TRAJECTORY_INCLUDED",
        "O5_REFLECTION_FORBIDDEN",
        "RAW_IR_RATIO_DERIVED_ESSENTIAL_RATE_MAP_OPEN",
        "4947_LOCAL_GR_NEWTON_MAXWELL_RETAINED",
        "FULL_MTS_PROMOTION_BLOCKED",
    }
    decision_status = {row["status"] for row in decisions}
    decisions_ok = len(decisions) == 10 and decision_status == required_decisions
    add(
        checks,
        "VAL4957_16_decisions",
        "all ten trajectory decisions are present",
        sorted(required_decisions),
        sorted(decision_status),
        decisions_ok,
    )

    json_endpoints = result["endpoint_summary"]
    endpoint_targets = {
        "dynamic_etaN_N8": (-202.0413471653601, 65.34514250637913, -3.3225249561681114),
        "reference_etaN0_N8": (-200.18681200874363, 65.34514178569091, -3.3224177636400554),
    }
    endpoint_failures: list[str] = []
    for key, expected in endpoint_targets.items():
        actual = tuple(
            float(json_endpoints[key][coordinate])
            for coordinate in ("A2_endpoint", "A3_endpoint", "W_O4_endpoint")
        )
        if not all(close(left, right) for left, right in zip(actual, expected)):
            endpoint_failures.append(key)
    add(
        checks,
        "VAL4957_17_endpoint_coordinates",
        "both N8 infrared low-coordinate endpoints reproduce",
        [],
        endpoint_failures,
        not endpoint_failures,
    )

    gr3 = {
        key: float(value["g_endpoint"]) * float(value["r3_raw_endpoint"])
        for key, value in json_endpoints.items()
    }
    gr3_ok = (
        close(gr3["dynamic_etaN_N6"], gr3["dynamic_etaN_N8"])
        and close(gr3["reference_etaN0_N6"], gr3["reference_etaN0_N8"])
        and 8.0e-4 < min(gr3.values()) < max(gr3.values()) < 8.2e-4
    )
    add(
        checks,
        "VAL4957_18_raw_ratio_scaling",
        "g times raw r3 is finite and order converged while raw r3 scales as 1/g",
        "8.0e-4 to 8.2e-4",
        gr3,
        gr3_ok,
    )

    dynamic_kernel = float(
        json_endpoints["dynamic_etaN_N8"][
            "dimensionless_sigma24_raw_kernel_endpoint"
        ]
    )
    reference_kernel = float(
        json_endpoints["reference_etaN0_N8"][
            "dimensionless_sigma24_raw_kernel_endpoint"
        ]
    )
    kernel_spread = abs(dynamic_kernel - reference_kernel) / max(
        abs(dynamic_kernel), abs(reference_kernel)
    )
    kernel_ok = (
        5.8e-64 < dynamic_kernel < 5.9e-64
        and 5.8e-64 < reference_kernel < 5.9e-64
        and kernel_spread < 1.0e-6
    )
    add(
        checks,
        "VAL4957_19_raw_kernel",
        "raw infrared six-point kernel is finite, decaying and scheme stable",
        "5.8e-64 to 5.9e-64; spread<1e-6",
        {"dynamic": dynamic_kernel, "reference": reference_kernel, "spread": kernel_spread},
        kernel_ok,
    )

    gates = result["gates"]
    gates_ok = (
        gates["combined_fixed_points_through_N8"]
        and gates["one_GR_connected_relevant_direction"]
        and gates["all_functional_trajectories_reach_IR"]
        and gates["low_IR_coordinates_order_converged"]
        and gates["trajectory_local_x_le_0p1_regular"]
        and float(gates["minimum_trajectory_Hessian_singular_value"]) > 0.3
        and gates["O2_local_linear_residual"] == "EXACT_ZERO_BY_FIELD_DEGREE"
        and gates["O4_functional_eta_trajectory"] == "INCLUDED"
        and gates["O5"] == "FORBIDDEN_BY_REFLECTION"
        and gates["raw_IR_r3"] == "DERIVED"
        and gates["physical_essential_IR_r3"] == "OPEN"
        and gates["local_GR_Newton_Maxwell_4947"] == "RETAINED"
        and not gates["full_MTS"]
    )
    add(
        checks,
        "VAL4957_20_result_gates",
        "result retains local success and blocks essential/full-theory promotion",
        True,
        gates,
        gates_ok,
    )

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
            ("MTS_FUNCTIONAL_PX_O4_GR_TRAJECTORY_DECISION_4957", checkpoint_text),
            ("PPC4161_FUNCTIONAL_PX_O4_GR_TRAJECTORY_4957", formal_text),
            ('"L-799"', claims_text),
            ("PredictivityStatus4957_MTS", variables_text),
            ("## 1.250", equations_text),
            ("## 201.", red_text),
            ("checkpoint 4957", spine_text),
            ("Current checkpoint 4957 handoff", resume_text),
        )
    )
    add(
        checks,
        "VAL4957_21_documents",
        "checkpoint 4957 is synchronized across every register",
        True,
        documentation_ok,
        documentation_ok,
    )

    claim_rows = read_csv(CLAIMS)
    variable_rows = read_csv(VARIABLES)
    registry_ok = (
        sum(row["claim_id"] == "L-799" for row in claim_rows) == 1
        and sum(
            row["symbol"] == "PredictivityStatus4957_MTS"
            for row in variable_rows
        )
        == 1
        and len(claim_rows[-1]) == 13
        and len(variable_rows[-1]) == 11
    )
    add(
        checks,
        "VAL4957_22_registry_csv",
        "claim and variable registers parse with unique 4957 rows",
        True,
        registry_ok,
        registry_ok,
    )

    synchronized = "\n".join(
        (checkpoint_text, formal_text, equations_text, red_text, spine_text, resume_text)
    )
    prohibited = [
        "FULL_MTS_TRUE",
        "ESSENTIAL_R3_DERIVED",
        "GLOBAL_FIXED_FUNCTION_DERIVED",
        "O2_NONZERO_BACKGROUND_COMPLETE",
    ]
    present = [token for token in prohibited if token in synchronized]
    add(
        checks,
        "VAL4957_23_prohibitions",
        "synchronized prose contains no false promotion marker",
        [],
        present,
        not present,
    )

    provenance_text = PROVENANCE.read_text(encoding="utf-8")
    provenance_ok = all(
        value in provenance_text for value in result["source_hashes"].values()
    )
    add(
        checks,
        "VAL4957_24_provenance",
        "provenance records every locked source hash",
        True,
        provenance_ok,
        provenance_ok,
    )

    after_hashes = {str(path): digest(path) for path in OUTPUTS}
    deterministic = len(before_hashes) == len(OUTPUTS) and before_hashes == after_hashes
    add(
        checks,
        "VAL4957_25_determinism",
        "one full rerun reproduces every evidence-file hash",
        True,
        deterministic,
        deterministic,
    )

    pycache = list((POST / "scripts").glob("__pycache__"))
    add(
        checks,
        "VAL4957_26_pycache",
        "no script bytecode cache remains",
        [],
        [str(path) for path in pycache],
        not pycache,
    )
    hash_report = {
        "research_sha256": digest(RESEARCH),
        "result_sha256": digest(RESULT),
        "checkpoint_sha256": digest(CHECKPOINT),
    }
    add(
        checks,
        "VAL4957_27_hash_report",
        "reproducibility hashes are valid SHA-256 values",
        "three 64-character hashes",
        hash_report,
        all(len(value) == 64 for value in hash_report.values()),
    )

    all_previous = all(as_bool(row["passed"]) for row in checks)
    add(
        checks,
        "VAL4957_28_complete",
        "all preceding independent checks pass",
        True,
        all_previous,
        all_previous,
    )
    write_validation(checks)
    return 0 if all(as_bool(row["passed"]) for row in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
