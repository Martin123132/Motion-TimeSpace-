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
SOURCE = POST / "source-intake" / "functional_rg" / "4958"
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_4958_VALIDATION.csv"
)

RESEARCH = POST / "scripts" / "Y5_R2FR_4958_essential_PX_sixpoint_trajectory.py"
CHECKPOINT = POST / "4958-Y5-R2FR-six-derivative-essential-X2-X3-quotient-and-invariant-2to4-amplitude-or-rate-route-rejection.md"
PROVENANCE = SOURCE / "PROVENANCE.md"
FORMAL = ROOT / "formalization-workbench" / "974-PPC4161-essential-PX-sixpoint-trajectory-and-curvature-projector-decision.md"
CLAIMS = ROOT / "formalization-workbench" / "02-claims-register.csv"
VARIABLES = ROOT / "formalization-workbench" / "04-variable-audit.csv"
EQUATIONS = ROOT / "formalization-workbench" / "05-equation-register.md"
RED_TEAM = ROOT / "formalization-workbench" / "06-consistency-red-team.md"
SPINE = ROOT / "formalization-workbench" / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

RESULT = SOURCE / "essential_PX_sixpoint_trajectory_results.json"
QUOTIENT = SOURCE / "six_derivative_essential_quotient.csv"
CALIBRATION = SOURCE / "essential_source_calibration.csv"
FIXED = SOURCE / "essential_functional_fixed_point_convergence.csv"
SPECTRUM = SOURCE / "essential_functional_stability_spectrum.csv"
TRAJECTORY = SOURCE / "essential_functional_GR_trajectory.csv"
CONVERGENCE = SOURCE / "essential_IR_coordinate_convergence.csv"
AMPLITUDE = SOURCE / "essential_scalar_24_amplitude.csv"
RESIDUAL = SOURCE / "curvature_sixpoint_residual_gate.csv"
DECISION = SOURCE / "essential_sixpoint_decision.csv"

OUTPUTS = [
    RESULT,
    QUOTIENT,
    CALIBRATION,
    FIXED,
    SPECTRUM,
    TRAJECTORY,
    CONVERGENCE,
    AMPLITUDE,
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

MARKER = "MTS_4958_ESSENTIAL_PX_SIXPOINT_TRAJECTORY"
VALIDATION_MARKER = "MTS_4958_INDEPENDENT_VALIDATION"
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
        "VAL4958_00_research",
        "research runner completes",
        0,
        execution.returncode,
        execution.returncode == 0 and f"{MARKER}_DONE" in execution.stdout,
    )

    missing = [str(path) for path in OUTPUTS + DOCUMENTS if not path.is_file()]
    add(
        checks,
        "VAL4958_01_paths",
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
        "VAL4958_02_compile",
        "research and validator compile without bytecode output",
        [],
        compile_failures,
        not compile_failures,
    )

    result = json.loads(RESULT.read_text(encoding="utf-8"))
    quotient = read_csv(QUOTIENT)
    calibration = read_csv(CALIBRATION)
    fixed = read_csv(FIXED)
    spectrum = read_csv(SPECTRUM)
    trajectory = read_csv(TRAJECTORY)
    convergence = read_csv(CONVERGENCE)
    amplitude = read_csv(AMPLITUDE)
    residual = read_csv(RESIDUAL)
    decisions = read_csv(DECISION)
    tables = (
        quotient,
        calibration,
        fixed,
        spectrum,
        trajectory,
        convergence,
        amplitude,
        residual,
        decisions,
    )

    marker_ok = result["checkpoint_marker"] == MARKER and all(
        row["checkpoint_marker"] == MARKER for table in tables for row in table
    )
    add(
        checks,
        "VAL4958_03_marker",
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
        "VAL4958_04_nonclaim",
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
        "VAL4958_05_source_hashes",
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
        "VAL4958_06_source_clauses",
        "all seven source interpretation clauses pass",
        "7 true",
        result["source_clause_checks"],
        clauses_ok,
    )

    quotient_ok = (
        len(quotient) == 6
        and all(as_bool(row["passed"]) for row in quotient)
        and {row["proof_id"] for row in quotient}
        == {f"Q4958_{index:02d}_{name}" for index, name in enumerate(
            ("basis", "metric_map", "cessential", "eessential", "flow_kernel", "field_degree"),
            start=1,
        )}
    )
    add(
        checks,
        "VAL4958_07_quotient_rows",
        "all six quotient derivation rows pass",
        "6 passing rows",
        len(quotient),
        quotient_ok,
    )
    symbolic_ok = all(
        value == "True" for value in result["symbolic_quotient_checks"].values()
    ) and result["essential_frame_contract"] == {
        "beta_ctilde_zero_frame": "-g qN2/(3pi)+c qS2/(12pi^2)",
        "beta_d_zero_frame": "g(4qN2-18qN3+qS2-9qS3)/(6pi)-c qS2/(12pi^2)",
        "c_essential": "c+8pi*g*(ctilde+d)",
        "e_essential": "e+24pi*g*c*ctilde+128pi^2*g^2*ctilde^2+64pi^2*g^2*ctilde*d",
        "functional_kernel": "Delta beta_a_m=16pi*g*a_(m-1)[(3-m)beta_d+(m/2)beta_ctilde]",
        "renormalization_conditions": ["ctilde=0", "d=0"],
    }
    add(
        checks,
        "VAL4958_08_symbolic_contract",
        "symbolic quotient and minimal-essential contract are exact",
        True,
        symbolic_ok,
        symbolic_ok,
    )

    calibration_shape = (
        len(calibration) == 8
        and {row["calibration_id"] for row in calibration}
        == {"CAL4958_cessential", "CAL4958_eessential_at_origin"}
        and all(as_bool(row["passed"]) for row in calibration)
    )
    add(
        checks,
        "VAL4958_09_calibration_shape",
        "four gravity values calibrate c and e essential sources",
        "8 passing rows",
        len(calibration),
        calibration_shape,
    )
    calibration_error = max(float(row["relative_error"]) for row in calibration)
    lower_source_ok = (
        result["calibration"]["all_rows_pass"]
        and result["calibration"]["raw_beta_c_origin"] == "20g^2"
        and result["calibration"]["essential_beta_c_origin"] == "16g^2"
        and result["calibration"]["essential_beta_e_origin"] == "-(208pi/5)g^3"
        and calibration_error < 3.0e-15
    )
    add(
        checks,
        "VAL4958_10_lower_source",
        "minimal-essential flow reproduces 16g^2 and the X3 origin source",
        "relative error <3e-15",
        calibration_error,
        lower_source_ok,
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
            row["status"] == "SELF_CONSISTENT_ESSENTIAL_COMBINED_FIXED_POINT"
            and row["frame"] == "minimal_essential_ctilde_eq_d_eq_0"
            for row in fixed
        )
    )
    add(
        checks,
        "VAL4958_11_fixed_shape",
        "essential combined roots exist at N=2 through N=8 in both schemes",
        "14 roots",
        len(fixed),
        fixed_shape,
    )
    fixed_residual = max(float(row["scaled_beta_residual"]) for row in fixed)
    add(
        checks,
        "VAL4958_12_fixed_residual",
        "every essential fixed-point scaled residual is below 1e-8",
        "<1e-8",
        fixed_residual,
        fixed_residual < 1.0e-8,
    )
    n8 = {
        row["scheme"]: row
        for row in fixed
        if int(row["polynomial_order"]) == 8
    }
    targets = {
        "dynamic_etaN": (
            0.13088292973497262,
            -0.10205973548118645,
            0.1037133216701763,
            4.978467442910135,
        ),
        "reference_etaN0": (
            0.13088236305736775,
            -0.07208730673649272,
            0.0629219967635062,
            6.054174021734666,
        ),
    }
    fixed_failures: list[str] = []
    for scheme, expected in targets.items():
        actual = tuple(
            float(n8[scheme][key])
            for key in ("g", "a2", "a3", "r3_essential_scalar")
        )
        if not all(close(left, right) for left, right in zip(actual, expected)):
            fixed_failures.append(scheme)
    add(
        checks,
        "VAL4958_13_fixed_coordinates",
        "both N8 essential fixed points reproduce",
        [],
        fixed_failures,
        not fixed_failures,
    )

    spectrum_shape = (
        len(spectrum) == 48
        and {row["scheme"] for row in spectrum} == SCHEMES
        and {int(row["polynomial_order"]) for row in spectrum} == ORDERS
    )
    relevant_failures: list[str] = []
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
            if (
                len(relevant) != 1
                or len(connected) != 1
                or relevant[0] != connected[0]
                or not (-1.90 < float(relevant[0]["beta_eigenvalue_real"]) < -1.88)
            ):
                relevant_failures.append(f"{scheme}_N{order}")
    add(
        checks,
        "VAL4958_14_stability",
        "N6 and N8 in both schemes have one GR-connected relevant mode",
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
        "VAL4958_15_trajectory_shape",
        "four essential trajectories each contain 121 samples",
        484,
        len(trajectory),
        trajectory_shape,
    )
    trajectory_failures: list[str] = []
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
            gravity = [float(row["g"]) for row in rows]
            if (
                not close(gravity[-1], 1.0e-10, relative=1.0e-8, absolute=1.0e-18)
                or not all(
                    gravity[index + 1] <= gravity[index] * (1.0 + 1.0e-10)
                    for index in range(len(gravity) - 1)
                )
                or not all(as_bool(row["convex_x_le_0p1"]) for row in rows)
                or not all(
                    row["frame"] == "minimal_essential_ctilde_eq_d_eq_0"
                    for row in rows
                )
                or any(as_bool(row["full_gravity_sixpoint_complete"]) for row in rows)
            ):
                trajectory_failures.append(f"{scheme}_N{order}")
    add(
        checks,
        "VAL4958_16_trajectory_endpoint",
        "all essential trajectories monotonically reach g=1e-10 in the local chart",
        [],
        trajectory_failures,
        not trajectory_failures,
    )

    maximum_order_difference = max(
        float(row["relative_difference"]) for row in convergence
    )
    convergence_ok = (
        len(convergence) == 10
        and all(as_bool(row["converged_below_1e_minus_3"]) for row in convergence)
        and maximum_order_difference < 1.0e-3
    )
    add(
        checks,
        "VAL4958_17_order_convergence",
        "all five essential infrared coordinates converge in both schemes",
        "10 rows below 1e-3",
        maximum_order_difference,
        convergence_ok,
    )

    amplitude_ok = (
        len(amplitude) == 4
        and {row["scheme"] for row in amplitude} == SCHEMES
        and {int(row["polynomial_order"]) for row in amplitude} == ORDERS
        and all(
            row["scalar_flat_subamplitude_status"]
            == "INVARIANT_TREE_SUBAMPLITUDE_DERIVED"
            and row["full_gravity_amplitude_status"]
            == "BLOCKED_BY_O2_O3_O4_PROJECTORS"
            for row in amplitude
        )
    )
    add(
        checks,
        "VAL4958_18_amplitude_shape",
        "four invariant scalar subamplitudes retain the full-gravity block",
        "4 scoped rows",
        len(amplitude),
        amplitude_ok,
    )
    kernels = [
        float(row["dimensionless_sigma24_essential_scalar_kernel"])
        for row in amplitude
    ]
    scalar_kernel_ok = (
        5.8e-64 < min(kernels) <= max(kernels) < 5.9e-64
        and max(kernels) / min(kernels) - 1.0 < 1.0e-6
    )
    add(
        checks,
        "VAL4958_19_scalar_kernel",
        "essential scalar six-point kernel is finite and scheme/order stable",
        "5.8e-64 to 5.9e-64; spread<1e-6",
        {"minimum": min(kernels), "maximum": max(kernels)},
        scalar_kernel_ok,
    )

    residual_by_operator = {row["operator"]: row for row in residual}
    blockers = [
        row["operator"]
        for row in residual
        if row["full_amplitude_gate"] == "BLOCKS_FULL_GRAVITY_SIXPOINT"
    ]
    residual_ok = (
        len(residual) == 5
        and set(blockers)
        == {
            "O2=X(nabla_nabla_psi)^2",
            "O3=C^3",
            "O4=C^2 X",
        }
        and residual_by_operator[
            "O1=X^3"
        ]["full_amplitude_gate"] == "PASS_FOR_SCALAR_FLAT_SUBAMPLITUDE"
        and residual_by_operator[
            "O5=C(nabla_psi)^2(nabla_nabla_psi)"
        ]["trajectory_status"] == "EXACT_ZERO_BY_REFLECTION"
    )
    add(
        checks,
        "VAL4958_20_residual_gate",
        "O2 O3 O4 remain explicit blockers while O1 and O5 are scoped",
        ["O2", "O3", "O4"],
        blockers,
        residual_ok,
    )

    required_decisions = {
        "SIX_DERIVATIVE_ESSENTIAL_QUOTIENT_DERIVED",
        "FUNCTIONAL_MINIMAL_ESSENTIAL_KERNEL_DERIVED",
        "LOWER_ESSENTIAL_SOURCE_REPRODUCED",
        "ESSENTIAL_COMBINED_FIXED_POINTS_RETAINED",
        "ESSENTIAL_GR_CONNECTED_TRAJECTORY_RETAINED",
        "ESSENTIAL_SCALAR_SIXPOINT_SUBAMPLITUDE_DERIVED",
        "FULL_GRAVITY_SIXPOINT_PROJECTOR_OPEN",
        "4947_LOCAL_GR_NEWTON_MAXWELL_RETAINED",
        "FULL_MTS_AND_GALAXY_RATE_BLOCKED",
    }
    decision_status = {row["status"] for row in decisions}
    decisions_ok = len(decisions) == 9 and decision_status == required_decisions
    add(
        checks,
        "VAL4958_21_decisions",
        "all nine essential-amplitude decisions are present",
        sorted(required_decisions),
        sorted(decision_status),
        decisions_ok,
    )

    gates = result["gates"]
    gates_ok = (
        gates["six_derivative_essential_quotient"] == "DERIVED"
        and gates["minimal_essential_functional_kernel"] == "DERIVED"
        and gates["lower_essential_source_16g2"] == "REPRODUCED"
        and gates["essential_combined_fixed_points"]
        and gates["one_GR_connected_relevant_direction"]
        and gates["all_essential_trajectories_reach_IR"]
        and gates["essential_IR_order_convergence"]
        and gates["essential_scalar_24_subamplitude"] == "DERIVED"
        and gates["full_gravity_sixpoint"] == "OPEN_O2_O3_O4_PROJECTORS"
        and gates["local_GR_Newton_Maxwell_4947"] == "RETAINED"
        and not gates["galaxy_rate"]
        and not gates["full_MTS"]
    )
    add(
        checks,
        "VAL4958_22_result_gates",
        "result retains local success and blocks complete-amplitude promotion",
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
            ("MTS_ESSENTIAL_PX_SIXPOINT_TRAJECTORY_DECISION_4958", checkpoint_text),
            ("PPC4161_ESSENTIAL_PX_SIXPOINT_TRAJECTORY_4958", formal_text),
            ('"L-800"', claims_text),
            ("PredictivityStatus4958_MTS", variables_text),
            ("## 1.251", equations_text),
            ("## 202.", red_text),
            ("checkpoint 4958", spine_text),
            ("Current checkpoint 4958 handoff", resume_text),
        )
    )
    add(
        checks,
        "VAL4958_23_documents",
        "checkpoint 4958 is synchronized across every register",
        True,
        documentation_ok,
        documentation_ok,
    )

    claim_rows = read_csv(CLAIMS)
    variable_rows = read_csv(VARIABLES)
    registry_ok = (
        sum(row["claim_id"] == "L-800" for row in claim_rows) == 1
        and sum(
            row["symbol"] == "PredictivityStatus4958_MTS"
            for row in variable_rows
        )
        == 1
        and len(claim_rows[-1]) == 13
        and len(variable_rows[-1]) == 11
    )
    add(
        checks,
        "VAL4958_24_registry_csv",
        "claim and variable registers parse with unique 4958 rows",
        True,
        registry_ok,
        registry_ok,
    )

    synchronized = "\n".join(
        (checkpoint_text, formal_text, equations_text, red_text, spine_text, resume_text)
    )
    prohibited = [
        "FULL_MTS_TRUE",
        "FULL_GRAVITY_SIXPOINT_DERIVED",
        "GALAXY_RATE_DERIVED",
        "GLOBAL_FIXED_FUNCTION_DERIVED",
    ]
    present = [token for token in prohibited if token in synchronized]
    add(
        checks,
        "VAL4958_25_prohibitions",
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
        "VAL4958_26_provenance",
        "provenance records every locked source hash",
        True,
        provenance_ok,
        provenance_ok,
    )

    after_hashes = {str(path): digest(path) for path in OUTPUTS}
    deterministic = len(before_hashes) == len(OUTPUTS) and before_hashes == after_hashes
    add(
        checks,
        "VAL4958_27_determinism",
        "one full rerun reproduces every evidence-file hash",
        True,
        deterministic,
        deterministic,
    )

    pycache = list((POST / "scripts").glob("__pycache__"))
    add(
        checks,
        "VAL4958_28_pycache",
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
        "VAL4958_29_hash_report",
        "reproducibility hashes are valid SHA-256 values",
        "three 64-character hashes",
        hash_report,
        all(len(value) == 64 for value in hash_report.values()),
    )

    all_previous = all(as_bool(row["passed"]) for row in checks)
    add(
        checks,
        "VAL4958_30_complete",
        "all preceding independent checks pass",
        True,
        all_previous,
        all_previous,
    )
    write_validation(checks)
    return 0 if all(as_bool(row["passed"]) for row in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
