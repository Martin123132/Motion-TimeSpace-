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

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4959"
VALIDATION = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4959_VALIDATION.csv"

RESEARCH = POST / "scripts" / "Y5_R2FR_4959_curvature_sixpoint_projectors.py"
CHECKPOINT = POST / "4959-Y5-R2FR-O2-O3-O4-external-scalar-sixpoint-projectors-and-full-invariant-amplitude-or-curvature-route-rejection.md"
PROVENANCE = SOURCE / "PROVENANCE.md"
FORMAL = ROOT / "formalization-workbench" / "975-PPC4161-curvature-sixpoint-projectors-and-O2-independent-rate-bound.md"
CLAIMS = ROOT / "formalization-workbench" / "02-claims-register.csv"
VARIABLES = ROOT / "formalization-workbench" / "04-variable-audit.csv"
EQUATIONS = ROOT / "formalization-workbench" / "05-equation-register.md"
RED_TEAM = ROOT / "formalization-workbench" / "06-consistency-red-team.md"
SPINE = ROOT / "formalization-workbench" / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
LOCAL_SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

RESULT = SOURCE / "curvature_sixpoint_projector_results.json"
IDENTITY = SOURCE / "sixpoint_projector_identity_checks.csv"
REPLICATES = SOURCE / "sixpoint_projector_QMC_replicates.csv"
GRAM = SOURCE / "sixpoint_projector_gram_matrix.csv"
TRAJECTORY = SOURCE / "trajectory_full_amplitude_bounds.csv"
SCALING = SOURCE / "sixpoint_IR_power_counting.csv"
DECISION = SOURCE / "sixpoint_projector_decision.csv"

OUTPUTS = [RESULT, IDENTITY, REPLICATES, GRAM, TRAJECTORY, SCALING, DECISION]
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
    LOCAL_SPINE,
]

MARKER = "MTS_4959_CURVATURE_SIXPOINT_PROJECTORS"
VALIDATION_MARKER = "MTS_4959_INDEPENDENT_VALIDATION"
PROJECTORS = ("X2_exchange", "X3_contact", "O2_covariant", "O3_C3", "O4_C2X")


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


def close(left: float, right: float, relative: float = 2.0e-9, absolute: float = 1.0e-13) -> bool:
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
    before_hashes = {str(path): digest(path) for path in OUTPUTS if path.is_file()}
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
        "VAL4959_00_research",
        "full 4x32768-event research runner completes",
        0,
        execution.returncode,
        execution.returncode == 0 and f"{MARKER}_DONE" in execution.stdout,
    )

    missing = [str(path) for path in OUTPUTS + DOCUMENTS if not path.is_file()]
    add(checks, "VAL4959_01_paths", "all outputs and synchronized documents exist", [], missing, not missing)
    if missing or execution.returncode != 0:
        write_validation(checks)
        return 1

    compile_failures: list[str] = []
    for path in (RESEARCH, Path(__file__)):
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as error:
            compile_failures.append(f"{path}:{error}")
    add(checks, "VAL4959_02_compile", "research and validator compile", [], compile_failures, not compile_failures)

    after_hashes = {str(path): digest(path) for path in OUTPUTS}
    deterministic = bool(before_hashes) and before_hashes == after_hashes
    add(
        checks,
        "VAL4959_03_deterministic",
        "full rerun reproduces every generated output byte for byte",
        True,
        deterministic,
        deterministic,
    )

    result = json.loads(RESULT.read_text(encoding="utf-8"))
    identity_rows = read_csv(IDENTITY)
    replicate_rows = read_csv(REPLICATES)
    gram_rows = read_csv(GRAM)
    trajectory_rows = read_csv(TRAJECTORY)
    scaling_rows = read_csv(SCALING)
    decision_rows = read_csv(DECISION)
    all_rows = identity_rows + replicate_rows + gram_rows + trajectory_rows + scaling_rows + decision_rows
    marker_ok = all(row.get("checkpoint_marker") == MARKER for row in all_rows)
    nonclaim_ok = all(not as_bool(row.get("valid_for_full_MTS_claim")) for row in all_rows)
    add(checks, "VAL4959_04_csv", "all CSV files parse with marker and nonclaim flags", True, marker_ok and nonclaim_ok, marker_ok and nonclaim_ok)

    identity_failures = [row["check"] for row in identity_rows if not as_bool(row["passed"])]
    add(checks, "VAL4959_05_identities", "all analytic projector identities pass", [], identity_failures, not identity_failures)
    identity_map = {row["check"]: row for row in identity_rows}
    witness = float(identity_map["X3_O2_exact_nonproportionality_witness"]["value"])
    witness_ok = close(witness, 175.0 / 41472.0, relative=1.0e-12)
    add(checks, "VAL4959_06_witness", "two-event X3/O2 determinant is 175/41472", 175.0 / 41472.0, witness, witness_ok)
    ward = abs(float(identity_map["O2_contact_plus_legs_Ward_identity"]["value"]))
    add(checks, "VAL4959_07_ward", "gauge-complete O2 Ward residual is below 1e-13", "<1e-13", ward, ward < 1.0e-13)

    replicate_ok = (
        len(replicate_rows) == 4
        and {int(row["sobol_power"]) for row in replicate_rows} == {15}
        and {int(row["event_count"]) for row in replicate_rows} == {32768}
        and all(as_bool(row["all_finite"]) for row in replicate_rows)
        and all(float(row["gram_minimum_eigenvalue"]) > 0.0 for row in replicate_rows)
        and all(float(row["X3_O2_schur_complement"]) > 0.0 for row in replicate_rows)
    )
    add(checks, "VAL4959_08_replicas", "four finite positive-definite full-statistics replicas pass", True, replicate_ok, replicate_ok)

    gram = np.zeros((5, 5))
    for row in gram_rows:
        left = PROJECTORS.index(row["row_projector"])
        right = PROJECTORS.index(row["column_projector"])
        gram[left, right] = float(row["mean_product"])
    symmetry_residual = float(np.max(np.abs(gram - gram.T)))
    eigenvalues = np.linalg.eigvalsh(gram)
    gram_ok = symmetry_residual < 1.0e-14 and float(np.min(eigenvalues)) > 0.0
    add(checks, "VAL4959_09_gram", "five-projector Gram matrix is symmetric positive definite", "symmetric and min eigenvalue >0", f"sym={symmetry_residual};eigmin={np.min(eigenvalues)}", gram_ok)

    schur = gram[1, 1] - gram[1, 2] ** 2 / gram[2, 2]
    residual_fraction = schur / gram[1, 1]
    stored_bound = result["x3_o2_no_cancellation"]
    bound_ok = (
        schur > 0.0
        and close(schur, float(stored_bound["schur_complement"]))
        and close(residual_fraction, float(stored_bound["residual_fraction_after_best_O2_cancellation"]))
        and 0.84 < residual_fraction < 0.88
    )
    add(checks, "VAL4959_10_schur", "arbitrary O2 leaves a positive X3 rate floor", "0.84<fraction<0.88", residual_fraction, bound_ok)

    calibration = result["qmc"]["scalar_calibration"]
    calibration_ok = float(calibration["maximum_relative_difference"]) < 1.0e-3
    add(checks, "VAL4959_11_scalar_calibration", "new scalar Gram block reproduces 4954 below 1e-3", "<1e-3", calibration["maximum_relative_difference"], calibration_ok)

    correction_ok = all(
        close(float(row["corrected_scalar_kernel_factor_256"]), 256.0 * float(row["old_4958_scalar_kernel"]), relative=1.0e-12, absolute=0.0)
        for row in trajectory_rows
    )
    add(checks, "VAL4959_12_normalization", "all trajectory rows apply the exact factor-256 correction", True, correction_ok, correction_ok)

    trajectory_ok = (
        len(trajectory_rows) == 4
        and {(row["scheme"], int(row["polynomial_order"])) for row in trajectory_rows}
        == {("dynamic_etaN", 6), ("dynamic_etaN", 8), ("reference_etaN0", 6), ("reference_etaN0", 8)}
        and all(float(row["full_basis_kernel_minimized_over_O2"]) > 0.0 for row in trajectory_rows)
        and all(float(row["full_basis_kernel_minimized_over_O2"]) <= float(row["known_X2_X3_O3_O4_kernel_without_O2"]) for row in trajectory_rows)
        and all(0.84 < float(row["optimized_fraction_of_known_without_O2"]) < 0.88 for row in trajectory_rows)
    )
    add(checks, "VAL4959_13_trajectory", "all four trajectory endpoints retain the bounded positive rate", True, trajectory_ok, trajectory_ok)

    scaling_operators = {row["operator"] for row in scaling_rows}
    scaling_ok = len(scaling_rows) == 5 and {
        "O1=X_source^3",
        "O2=X_source(nabla_nabla_phi)^2",
        "two O(X_source^2) insertions",
        "O3=C^3",
        "O4=C^2 X_source",
    } == scaling_operators
    add(checks, "VAL4959_14_scaling", "all five p6 amplitude sources have scoped IR power counting", True, scaling_ok, scaling_ok)

    gates = result["gates"]
    gate_ok = (
        result["source_hashes_match"]
        and result["identity_checks_pass"]
        and gates["O2_projector"] == "DERIVED_GAUGE_COMPLETE"
        and gates["O3_projector"] == "DERIVED_WEYL_GAUGE_INVARIANT"
        and gates["O4_projector"] == "DERIVED_WEYL_GAUGE_INVARIANT"
        and gates["arbitrary_O2_cannot_cancel_X3_rate"]
        and gates["O2_parent_coefficient"] == "OPEN_MOMENTUM_DEPENDENT_FLOW"
        and gates["local_GR_Newton_Maxwell_4947"] == "RETAINED"
        and not gates["full_MTS"]
    )
    add(checks, "VAL4959_15_gates", "claim boundary and retained local branch are explicit", True, gate_ok, gate_ok)

    document_text = "\n".join(path.read_text(encoding="utf-8-sig") for path in DOCUMENTS[1:])
    document_markers = (
        "MTS_CURVATURE_SIXPOINT_PROJECTOR_DECISION_4959",
        "PPC4161_CURVATURE_SIXPOINT_PROJECTORS_4959",
        '"L-801"',
        "FullSixPointAmplitude4959_MTS",
        "## 1.252 Gauge-complete curvature six-point amplitude",
        "## 203. A bounded complete projector form",
    )
    missing_markers = [marker for marker in document_markers if marker not in document_text]
    add(checks, "VAL4959_16_documents", "formal registers contain all 4959 markers", [], missing_markers, not missing_markers)

    claim_rows = read_csv(CLAIMS)
    variable_rows = read_csv(VARIABLES)
    register_ok = (
        sum(row["claim_id"] == "L-801" for row in claim_rows) == 1
        and len({row["symbol"] for row in variable_rows}) == len(variable_rows)
        and all(len(row) == 13 for row in claim_rows)
        and all(len(row) == 11 for row in variable_rows)
    )
    add(checks, "VAL4959_17_registers", "L-801 is unique and both CSV registers are well formed", True, register_ok, register_ok)

    pycache = [str(path) for path in (POST / "scripts").rglob("__pycache__")]
    add(checks, "VAL4959_18_pycache", "project scripts contain no Python cache directories", [], pycache, not pycache)

    all_pass = all(bool(row["passed"]) for row in checks)
    add(checks, "VAL4959_19_final", "all independent 4959 checks pass", True, all_pass, all_pass)
    write_validation(checks)
    print(f"{VALIDATION_MARKER}_DONE checks={len(checks)} pass={all(row['passed'] for row in checks)}")
    if execution.stdout:
        print(execution.stdout.strip())
    if execution.stderr:
        print(execution.stderr.strip(), file=sys.stderr)
    return 0 if all(row["passed"] for row in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
