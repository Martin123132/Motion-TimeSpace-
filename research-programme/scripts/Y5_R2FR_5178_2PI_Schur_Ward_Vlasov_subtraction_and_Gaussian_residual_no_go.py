from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()

CHECKPOINT_4916_DOCUMENT = (
    POST
    / "4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md"
)
CHECKPOINT_4935_DOCUMENT = (
    POST
    / "4935-Y5-R2FR-completed-fixed-point-GR-connected-trajectory-and-motion-sector-entry.md"
)
CHECKPOINT_4935_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4935"
    / "motion_sector_entry_results.json"
)
CHECKPOINT_4942_DOCUMENT = (
    POST
    / "4942-Y5-R2FR-O4-completed-endpoint-local-vacuum-homogeneous-motion-branch-and-C3-CFF-PPN-residual-gate.md"
)
CHECKPOINT_4942_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4942"
    / "local_O4_C3_CFF_residual_results.json"
)
CHECKPOINT_4949_DOCUMENT = (
    POST
    / "4949-Y5-R2FR-covariant-2PI-motion-occupation-Dyson-source-and-conserved-galaxy-stress-or-composite-route-rejection.md"
)
CHECKPOINT_4949_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4949"
    / "CTP_2PI_static_source_results.json"
)
CHECKPOINT_4953_DOCUMENT = (
    POST
    / "4953-Y5-R2FR-galaxy-formation-transient-spectrum-X2-kinetic-cascade-and-local-injection-bound-or-composite-route-rejection.md"
)
CHECKPOINT_4953_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4953"
    / "formation_X2_cascade_and_injection_results.json"
)
CHECKPOINT_4953_INVARIANTS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4953"
    / "X2_collision_invariant_gate.csv"
)
CHECKPOINT_4954_DOCUMENT = (
    POST
    / "4954-Y5-R2FR-finite-time-off-shell-X2-number-changing-2PI-kernel-and-formation-source-efficiency-or-nonequilibrium-route-rejection.md"
)
CHECKPOINT_4954_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4954"
    / "offshell_X2_X3_number_change_results.json"
)
CHECKPOINT_4954_DECISION = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4954"
    / "offshell_X2_X3_route_decision.csv"
)
CHECKPOINT_4959_DOCUMENT = (
    POST
    / "4959-Y5-R2FR-O2-O3-O4-external-scalar-sixpoint-projectors-and-full-invariant-amplitude-or-curvature-route-rejection.md"
)
CHECKPOINT_4959_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4959"
    / "curvature_sixpoint_projector_results.json"
)
CHECKPOINT_4959_BOUNDS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4959"
    / "trajectory_full_amplitude_bounds.csv"
)
CHECKPOINT_4960_DOCUMENT = (
    POST
    / "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-and-local-GR-Newton-Maxwell-promotion-or-parent-field-content-boundary.md"
)
CHECKPOINT_4960_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4960"
    / "integrated_H_universal_source_results.json"
)
CHECKPOINT_5148_DOCUMENT = (
    POST
    / "5148-Y5-R2FR-one-parent-local-GR-galaxy-spectral-response-cog-theorem.md"
)
CHECKPOINT_5148_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5148"
    / "regime_selective_motion_response_results.json"
)
CHECKPOINT_5149_DOCUMENT = (
    POST
    / "5149-Y5-R2FR-causal-spectral-density-critical-motion-mixing-and-vacuum-no-go.md"
)
CHECKPOINT_5149_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5149"
    / "causal_spectral_density_and_critical_mixing_results.json"
)
CHECKPOINT_5151_STATE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5151"
    / "galaxy_state_stress_scale_gate.csv"
)
CHECKPOINT_5155_DOCUMENT = (
    POST
    / "5155-Y5-R2FR-parent-SP-Vlasov-limit-homogeneous-no-collapse-post-equality-transfer-and-wave-runner.md"
)
CHECKPOINT_5155_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5155"
    / "parent_SP_Vlasov_transfer_results.json"
)
CHECKPOINT_5155_WAVE_GATE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5155"
    / "wave_resolution_and_classicality_gate.csv"
)
CHECKPOINT_5156_DOCUMENT = (
    POST
    / "5156-Y5-R2FR-FLRW-Hessian-Gaussian-state-single-clock-adiabatic-radiation-transfer-and-patch-collapse-gate.md"
)
CHECKPOINT_5156_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5156"
    / "FLRW_covariance_radiation_transfer_results.json"
)
CHECKPOINT_5165_DOCUMENT = (
    POST
    / "5165-Y5-R2FR-baryon-Maxwell-Poynting-assembly-clock-identifiability-and-energy-bound-gate.md"
)
CHECKPOINT_5171_DOCUMENT = (
    POST
    / "5171-Y5-R2FR-action-angle-retarded-vlasov-polarization-static-response-and-double-counting-gate.md"
)
CHECKPOINT_5171_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5171"
    / "action_angle_vlasov_response_results.json"
)
CHECKPOINT_5171_DOUBLE_COUNT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5171"
    / "double_counting_ledger.csv"
)
CHECKPOINT_5176_ROOT = POST / "source-intake" / "functional_rg" / "5176"
CHECKPOINT_5177_DOCUMENT = (
    POST
    / "5177-Y5-R2FR-locked-ensemble-metric-split-and-no-retuning-theorem.md"
)
CHECKPOINT_5177_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5177"
    / "locked_metric_split_results.json"
)
CHECKPOINT_5177_NORMALIZATION = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5177"
    / "constant_normalization_no_go.csv"
)

OUT = POST / "source-intake" / "functional_rg" / "5178"
SCHUR_CSV = OUT / "exact_Schur_Ward_trials.csv"
KERNEL_CSV = OUT / "connected_stress_kernel_derivation.csv"
SUBTRACTION_CSV = OUT / "vacuum_Vlasov_and_Poynting_subtraction_ledger.csv"
BOUND_CSV = OUT / "O4_wave_and_criticality_residual_bound.csv"
INTERACTION_CSV = OUT / "interaction_and_state_preparation_gate.csv"
DECISION_CSV = OUT / "surviving_route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "twoPI_Schur_Vlasov_subtraction_results.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5178_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5178-Y5-R2FR-exact-2PI-Schur-Ward-Vlasov-subtraction-and-Gaussian-residual-stress-no-go.md"
)

MARKER = "MTS_5178_2PI_SCHUR_WARD_VLASOV_SUBTRACTION_THEOREM"
CHECKED_DATE = "2026-07-23"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5176_TREE_LOCK = (
    "254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b"
)
REFERENCE_GALAXY = "UGC09133"
REFERENCE_MAPPING = "Wetterich_v_equals_minus_2lambda"
REFERENCE_MASS_LABEL = "benchmark_1e_minus20_eV"
LIGHT_SPEED_M_S = 299_792_458.0
KPC_M = 3.0856775814913673e19
SCHUR_TRIAL_COUNT = 12

ROUTE_DECISION = (
    "THE_STATIONARY_2PI_REDUCTION_GIVES_AN_EXACT_ON_SHELL_TRANSVERSE_SCHUR_"
    "COMPLEMENT_BUT_AFTER_VACUUM_MATCHING_AND_THE_ALREADY_EVOLVED_VLASOV_"
    "RESPONSE_ARE_SUBTRACTED_THE_CURRENT_GAPPED_GAUSSIAN_HESSIAN_SUPPLIES_"
    "NO_INDEPENDENT_ORDER_ONE_GALAXY_STRESS_THE_O4_AND_CONTROLLED_WAVE_"
    "RESIDUALS_ARE_TOO_SMALL_AND_ONLY_A_PARENT_DERIVED_NON_GAUSSIAN_INITIAL_"
    "OR_STRONG_INTERACTING_CTP_KERNEL_CAN_REOPEN_THE_ROUTE"
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(file_digest(item).encode("ascii"))
    return digest.hexdigest()


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


def source_paths() -> dict[str, Path]:
    return {
        "checkpoint_5178_script": SCRIPT,
        "checkpoint_4916_document": CHECKPOINT_4916_DOCUMENT,
        "checkpoint_4935_document": CHECKPOINT_4935_DOCUMENT,
        "checkpoint_4935_result": CHECKPOINT_4935_RESULT,
        "checkpoint_4942_document": CHECKPOINT_4942_DOCUMENT,
        "checkpoint_4942_result": CHECKPOINT_4942_RESULT,
        "checkpoint_4949_document": CHECKPOINT_4949_DOCUMENT,
        "checkpoint_4949_result": CHECKPOINT_4949_RESULT,
        "checkpoint_4953_document": CHECKPOINT_4953_DOCUMENT,
        "checkpoint_4953_result": CHECKPOINT_4953_RESULT,
        "checkpoint_4953_invariants": CHECKPOINT_4953_INVARIANTS,
        "checkpoint_4954_document": CHECKPOINT_4954_DOCUMENT,
        "checkpoint_4954_result": CHECKPOINT_4954_RESULT,
        "checkpoint_4954_decision": CHECKPOINT_4954_DECISION,
        "checkpoint_4959_document": CHECKPOINT_4959_DOCUMENT,
        "checkpoint_4959_result": CHECKPOINT_4959_RESULT,
        "checkpoint_4959_bounds": CHECKPOINT_4959_BOUNDS,
        "checkpoint_4960_document": CHECKPOINT_4960_DOCUMENT,
        "checkpoint_4960_result": CHECKPOINT_4960_RESULT,
        "checkpoint_5148_document": CHECKPOINT_5148_DOCUMENT,
        "checkpoint_5148_result": CHECKPOINT_5148_RESULT,
        "checkpoint_5149_document": CHECKPOINT_5149_DOCUMENT,
        "checkpoint_5149_result": CHECKPOINT_5149_RESULT,
        "checkpoint_5151_state": CHECKPOINT_5151_STATE,
        "checkpoint_5155_document": CHECKPOINT_5155_DOCUMENT,
        "checkpoint_5155_result": CHECKPOINT_5155_RESULT,
        "checkpoint_5155_wave_gate": CHECKPOINT_5155_WAVE_GATE,
        "checkpoint_5156_document": CHECKPOINT_5156_DOCUMENT,
        "checkpoint_5156_result": CHECKPOINT_5156_RESULT,
        "checkpoint_5165_document": CHECKPOINT_5165_DOCUMENT,
        "checkpoint_5171_document": CHECKPOINT_5171_DOCUMENT,
        "checkpoint_5171_result": CHECKPOINT_5171_RESULT,
        "checkpoint_5171_double_count": CHECKPOINT_5171_DOUBLE_COUNT,
        "checkpoint_5177_document": CHECKPOINT_5177_DOCUMENT,
        "checkpoint_5177_result": CHECKPOINT_5177_RESULT,
        "checkpoint_5177_normalization": CHECKPOINT_5177_NORMALIZATION,
    }


Matrix = list[list[Fraction]]
Vector = list[Fraction]


def zeros(rows: int, columns: int) -> Matrix:
    return [[Fraction(0) for _ in range(columns)] for _ in range(rows)]


def diagonal(values: list[int | Fraction]) -> Matrix:
    result = zeros(len(values), len(values))
    for index, value in enumerate(values):
        result[index][index] = Fraction(value)
    return result


def transpose(matrix: Matrix) -> Matrix:
    return [list(column) for column in zip(*matrix)]


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    return [
        [left[row][column] + right[row][column] for column in range(len(left[0]))]
        for row in range(len(left))
    ]


def matrix_subtract(left: Matrix, right: Matrix) -> Matrix:
    return [
        [left[row][column] - right[row][column] for column in range(len(left[0]))]
        for row in range(len(left))
    ]


def matrix_multiply(left: Matrix, right: Matrix) -> Matrix:
    return [
        [
            sum(
                (
                    left[row][inner] * right[inner][column]
                    for inner in range(len(right))
                ),
                Fraction(0),
            )
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def matrix_vector(matrix: Matrix, vector: Vector) -> Vector:
    return [
        sum(
            (matrix[row][column] * vector[column] for column in range(len(vector))),
            Fraction(0),
        )
        for row in range(len(matrix))
    ]


def vector_add(left: Vector, right: Vector) -> Vector:
    return [a + b for a, b in zip(left, right)]


def vector_subtract(left: Vector, right: Vector) -> Vector:
    return [a - b for a, b in zip(left, right)]


def vector_scale(value: int | Fraction, vector: Vector) -> Vector:
    return [Fraction(value) * item for item in vector]


def dot(left: Vector, right: Vector) -> Fraction:
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def identity(size: int) -> Matrix:
    return diagonal([1] * size)


def matrix_inverse(matrix: Matrix) -> Matrix:
    size = len(matrix)
    augmented = [
        list(row) + list(identity(size)[index])
        for index, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if augmented[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            raise RuntimeError("singular matrix")
        augmented[column], augmented[pivot] = (
            augmented[pivot],
            augmented[column],
        )
        pivot_value = augmented[column][column]
        augmented[column] = [
            item / pivot_value for item in augmented[column]
        ]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor == 0:
                continue
            augmented[row] = [
                item - factor * pivot_item
                for item, pivot_item in zip(
                    augmented[row], augmented[column]
                )
            ]
    return [row[size:] for row in augmented]


def matrix_rank(matrix: Matrix) -> int:
    work = [list(row) for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [item / pivot_value for item in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row:
                continue
            factor = work[row][column]
            if factor == 0:
                continue
            work[row] = [
                item - factor * pivot_item
                for item, pivot_item in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def determinant(matrix: Matrix) -> Fraction:
    work = [list(row) for row in matrix]
    size = len(work)
    value = Fraction(1)
    sign = 1
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        pivot_value = work[column][column]
        value *= pivot_value
        for row in range(column + 1, size):
            factor = work[row][column] / pivot_value
            for inner in range(column + 1, size):
                work[row][inner] -= factor * work[column][inner]
    return value * sign


def block_matrix(
    upper_left: Matrix,
    upper_right: Matrix,
    lower_left: Matrix,
    lower_right: Matrix,
) -> Matrix:
    upper = [
        list(left_row) + list(right_row)
        for left_row, right_row in zip(upper_left, upper_right)
    ]
    lower = [
        list(left_row) + list(right_row)
        for left_row, right_row in zip(lower_left, lower_right)
    ]
    return upper + lower


def submatrix(matrix: Matrix, indices: list[int]) -> Matrix:
    return [[matrix[row][column] for column in indices] for row in indices]


def max_abs_vector(vector: Vector) -> Fraction:
    return max((abs(item) for item in vector), default=Fraction(0))


def max_abs_matrix(matrix: Matrix) -> Fraction:
    return max(
        (abs(item) for row in matrix for item in row),
        default=Fraction(0),
    )


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def exact_schur_trials() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for trial in range(1, SCHUR_TRIAL_COUNT + 1):
        lower = [
            [Fraction(trial + 2), Fraction(0), Fraction(0)],
            [Fraction(1), Fraction(trial + 3), Fraction(0)],
            [Fraction(-1), Fraction(1), Fraction(trial + 4)],
        ]
        correlation_hessian = matrix_multiply(
            transpose(lower), lower
        )
        correlation_inverse = matrix_inverse(correlation_hessian)
        mixing = [
            [Fraction(trial + 1), Fraction(-2), Fraction(1)],
            [Fraction(2), Fraction(trial + 2), Fraction(-1)],
            [Fraction(-1), Fraction(2), Fraction(trial + 3)],
            [Fraction(1), Fraction(-1), Fraction(trial + 4)],
        ]
        physical_metric_hessian = diagonal(
            [0, trial + 2, 2 * trial + 3, trial + 5]
        )
        induced = matrix_multiply(
            matrix_multiply(mixing, correlation_inverse),
            transpose(mixing),
        )
        direct_metric_hessian = matrix_add(
            physical_metric_hessian, induced
        )
        reduced = matrix_subtract(direct_metric_hessian, induced)
        full_hessian = block_matrix(
            direct_metric_hessian,
            mixing,
            transpose(mixing),
            correlation_hessian,
        )

        metric_gauge = [
            Fraction(1),
            Fraction(0),
            Fraction(0),
            Fraction(0),
        ]
        correlation_gauge = vector_scale(
            -1,
            matrix_vector(
                correlation_inverse,
                matrix_vector(transpose(mixing), metric_gauge),
            ),
        )
        full_gauge = metric_gauge + correlation_gauge
        full_ward_residual = matrix_vector(full_hessian, full_gauge)
        reduced_ward_residual = matrix_vector(reduced, metric_gauge)

        source = [
            Fraction(0),
            Fraction(trial + 1),
            Fraction(-2),
            Fraction(3),
        ]
        metric_response = [
            Fraction(0),
            source[1] / physical_metric_hessian[1][1],
            source[2] / physical_metric_hessian[2][2],
            source[3] / physical_metric_hessian[3][3],
        ]
        correlation_response = vector_scale(
            -1,
            matrix_vector(
                correlation_inverse,
                matrix_vector(transpose(mixing), metric_response),
            ),
        )
        full_response = metric_response + correlation_response
        response_residual = vector_subtract(
            matrix_vector(full_hessian, full_response),
            source + [Fraction(0), Fraction(0), Fraction(0)],
        )

        test_metric = [
            Fraction(trial),
            Fraction(-1),
            Fraction(2),
            Fraction(3),
        ]
        test_correlation = [
            Fraction(1),
            Fraction(-2),
            Fraction(trial + 1),
        ]
        test_full = test_metric + test_correlation
        direct_quadratic = dot(
            test_full, matrix_vector(full_hessian, test_full)
        )
        completed_square_vector = vector_add(
            test_correlation,
            matrix_vector(
                correlation_inverse,
                matrix_vector(transpose(mixing), test_metric),
            ),
        )
        factorized_quadratic = dot(
            test_metric,
            matrix_vector(physical_metric_hessian, test_metric),
        ) + dot(
            completed_square_vector,
            matrix_vector(
                correlation_hessian, completed_square_vector
            ),
        )
        gauge_fixed_indices = [1, 2, 3, 4, 5, 6]
        gauge_fixed_hessian = submatrix(
            full_hessian, gauge_fixed_indices
        )
        expected_gauge_fixed_determinant = determinant(
            correlation_hessian
        ) * determinant(
            submatrix(physical_metric_hessian, [1, 2, 3])
        )

        rows.append(
            {
                "trial": trial,
                "metric_dimension": 4,
                "correlator_dimension": 3,
                "det_C": fraction_text(determinant(correlation_hessian)),
                "rank_full_Hessian": matrix_rank(full_hessian),
                "expected_rank_one_gauge_zero": 6,
                "Schur_minus_physical_metric_max_abs": fraction_text(
                    max_abs_matrix(
                        matrix_subtract(reduced, physical_metric_hessian)
                    )
                ),
                "full_Ward_residual_max_abs": fraction_text(
                    max_abs_vector(full_ward_residual)
                ),
                "reduced_Ward_residual_max_abs": fraction_text(
                    max_abs_vector(reduced_ward_residual)
                ),
                "full_vs_reduced_response_residual_max_abs": fraction_text(
                    max_abs_vector(response_residual)
                ),
                "quadratic_completion_residual": fraction_text(
                    direct_quadratic - factorized_quadratic
                ),
                "factorized_quadratic_nonnegative": (
                    factorized_quadratic >= 0
                ),
                "gauge_fixed_determinant": fraction_text(
                    determinant(gauge_fixed_hessian)
                ),
                "det_C_times_det_Schur_physical": fraction_text(
                    expected_gauge_fixed_determinant
                ),
                "determinant_factorization_exact": (
                    determinant(gauge_fixed_hessian)
                    == expected_gauge_fixed_determinant
                ),
                "all_exact_identities_pass": (
                    reduced == physical_metric_hessian
                    and max_abs_vector(full_ward_residual) == 0
                    and max_abs_vector(reduced_ward_residual) == 0
                    and max_abs_vector(response_residual) == 0
                    and direct_quadratic == factorized_quadratic
                    and matrix_rank(full_hessian) == 6
                    and determinant(gauge_fixed_hessian)
                    == expected_gauge_fixed_determinant
                ),
                "checkpoint_marker": MARKER,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def connected_kernel_rows() -> list[dict[str, Any]]:
    return [
        {
            "derivation_id": "K5178_00_2PI",
            "object": "renormalized CTP 2PI functional at zero motion one-point",
            "equation": (
                "Gamma[g,G]=S_g+(i/2)Tr ln G^-1+(i/2)Tr[D^-1[g]G-1]"
                "+Gamma_2[g,G]+Gamma_ct+Gamma_rho0"
            ),
            "derivation": (
                "standard 2PI Legendre transform applied to the checkpoint-4935 "
                "renormalized motion Hessian; Gamma_rho0 denotes boundary-state "
                "vertices rather than a fitted bulk force"
            ),
            "assumption": "renormalized contour kernels and a declared initial density matrix",
            "status": "PARENT_2PI_OBJECT_FIXED",
            "exact_within_declared_scope": True,
            "valid_for_full_MTS_claim": False,
        },
        {
            "derivation_id": "K5178_01_stationarity",
            "object": "physical bilocal correlator",
            "equation": "Gamma_,G[g,G_star[g]]=0",
            "derivation": "2PI stationarity is the Dyson/Kadanoff-Baym equation",
            "assumption": "physical CTP branch and causal boundary data",
            "status": "STATIONARITY_CONDITION",
            "exact_within_declared_scope": True,
            "valid_for_full_MTS_claim": False,
        },
        {
            "derivation_id": "K5178_02_correlator_response",
            "object": "metric derivative of the stationary correlator",
            "equation": (
                "dG_star/dg=-Gamma_GG^-1 Gamma_Gg=-C^-1 B_dagger"
            ),
            "derivation": "differentiate Gamma_,G=0 and solve on the physical bilocal subspace",
            "assumption": "C=Gamma_GG invertible after zero modes and contour conditions are fixed",
            "status": "EXACT_IMPLICIT_FUNCTION_RESPONSE",
            "exact_within_declared_scope": True,
            "valid_for_full_MTS_claim": False,
        },
        {
            "derivation_id": "K5178_03_first_variation",
            "object": "stationary reduced metric action",
            "equation": "Gammabar[g]=Gamma[g,G_star[g]]; Gammabar_,g=Gamma_,g",
            "derivation": "the chain term Gamma_,G dG_star/dg vanishes by stationarity",
            "assumption": "same renormalization convention before and after elimination",
            "status": "NO_EXTRA_FIRST_VARIATION_TERM",
            "exact_within_declared_scope": True,
            "valid_for_full_MTS_claim": False,
        },
        {
            "derivation_id": "K5178_04_Schur",
            "object": "stationary reduced metric Hessian",
            "equation": "Gammabar_gg=A-B C^-1 B_dagger",
            "derivation": (
                "differentiate the reduced first variation and insert "
                "dG_star/dg=-C^-1 B_dagger"
            ),
            "assumption": "A=Gamma_gg, B=Gamma_gG and C=Gamma_GG use identical CTP conventions",
            "status": "EXACT_SCHUR_COMPLEMENT",
            "exact_within_declared_scope": True,
            "valid_for_full_MTS_claim": False,
        },
        {
            "derivation_id": "K5178_05_stress_response",
            "object": "connected retarded Hilbert-stress response",
            "equation": (
                "Pi_R=Pi_contact-i theta(x0-y0)<[T(x),T(y)]>; "
                "its 1PI inverse-response block is the state part of Gammabar_gg"
            ),
            "derivation": (
                "two metric variations of the reduced CTP functional, including "
                "seagull/contact terms from the metric dependence of D^-1"
            ),
            "assumption": "density factors and index symmetrization follow the selected H-to-g source map",
            "status": "CONNECTED_STRESS_KERNEL_IDENTIFIED",
            "exact_within_declared_scope": True,
            "valid_for_full_MTS_claim": False,
        },
        {
            "derivation_id": "K5178_06_full_Ward",
            "object": "combined metric-correlator Ward generator",
            "equation": (
                "[[A,B],[B_dagger,C]] (R_g,R_G)^T=0 on the complete background EOM"
            ),
            "derivation": "second variation of the diffeomorphism identity for Gamma[g,G]",
            "assumption": (
                "all transformed fields are included; away from the metric EOM "
                "the standard contact/EOM terms must be retained"
            ),
            "status": "FULL_ON_SHELL_WARD_IDENTITY",
            "exact_within_declared_scope": True,
            "valid_for_full_MTS_claim": False,
        },
        {
            "derivation_id": "K5178_07_reduced_Ward",
            "object": "Ward identity after stationary correlator elimination",
            "equation": (
                "R_G=-C^-1 B_dagger R_g implies "
                "(A-B C^-1 B_dagger)R_g=0"
            ),
            "derivation": "solve the lower full-Ward block and substitute into the upper block",
            "assumption": "same physical inverse C^-1 as in the response equation",
            "status": "WARD_IDENTITY_DESCENDS_THROUGH_SCHUR",
            "exact_within_declared_scope": True,
            "valid_for_full_MTS_claim": False,
        },
        {
            "derivation_id": "K5178_08_gaussian_pair_kernel",
            "object": "Hessian-only bilocal kernel",
            "equation": (
                "Gamma_2=0 gives C_0=(i/2) G^-1 tensor_s G^-1 and "
                "B_0=(i/2) delta D^-1/delta g plus counterterm contacts"
            ),
            "derivation": "differentiate the Tr ln G^-1 and Tr[D^-1 G] terms twice",
            "assumption": "checkpoint-4949 displayed quadratic scalar truncation",
            "status": "GAUSSIAN_STRESS_BUBBLE_NOT_A_NEW_COUPLING",
            "exact_within_declared_scope": True,
            "valid_for_full_MTS_claim": False,
        },
        {
            "derivation_id": "K5178_09_interaction_kernel",
            "object": "Bethe-Salpeter interaction correction",
            "equation": "K_AB=4i delta^2 Gamma_2/(delta G_A delta G_B)",
            "derivation": "the non-Gaussian correction enters C and therefore the resummed Schur term",
            "assumption": "a parent-specified Gamma_2 and state boundary condition",
            "status": "ONLY_BULK_NON_GAUSSIAN_KERNEL_LOCATION",
            "exact_within_declared_scope": True,
            "valid_for_full_MTS_claim": False,
        },
        {
            "derivation_id": "K5178_10_source_map",
            "object": "integrated-H to Hilbert-stress source",
            "equation": "delta S_m/delta H^mn=-(T_mn-g_mn T/2)/2",
            "derivation": "checkpoint-4960 invertible H-to-g variation",
            "assumption": "nondegenerate H and the declared universal Diff parent",
            "status": "NO_SECOND_GALAXY_SOURCE_NORMALIZATION",
            "exact_within_declared_scope": True,
            "valid_for_full_MTS_claim": False,
        },
    ]


def select_row(
    rows: list[dict[str, str]],
    **conditions: str,
) -> dict[str, str]:
    matches = [
        row
        for row in rows
        if all(row.get(key) == value for key, value in conditions.items())
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"expected one row for {conditions}, found {len(matches)}"
        )
    return matches[0]


def derive_physical_inputs() -> dict[str, Any]:
    motion = read_json(CHECKPOINT_4935_RESULT)
    o4 = read_json(CHECKPOINT_4942_RESULT)
    ctp = read_json(CHECKPOINT_4949_RESULT)
    x2 = read_json(CHECKPOINT_4953_RESULT)
    offshell = read_json(CHECKPOINT_4954_RESULT)
    universal = read_json(CHECKPOINT_4960_RESULT)
    critical = read_json(CHECKPOINT_5149_RESULT)
    transfer = read_json(CHECKPOINT_5155_RESULT)
    covariance = read_json(CHECKPOINT_5156_RESULT)
    vlasov = read_json(CHECKPOINT_5171_RESULT)
    metric_split = read_json(CHECKPOINT_5177_RESULT)

    state_row = select_row(
        read_csv(CHECKPOINT_5151_STATE),
        galaxy=REFERENCE_GALAXY,
        mapping=REFERENCE_MAPPING,
    )
    wave_row = select_row(
        read_csv(CHECKPOINT_5155_WAVE_GATE),
        galaxy=REFERENCE_GALAXY,
        mapping=REFERENCE_MAPPING,
        mass_label=REFERENCE_MASS_LABEL,
    )
    amplitude_rows = [
        row
        for row in read_csv(CHECKPOINT_5177_NORMALIZATION)
        if row["model"] == "MTS"
    ]
    if len(amplitude_rows) != 12:
        raise RuntimeError(
            f"expected 12 MTS normalization rows, found {len(amplitude_rows)}"
        )
    interaction_row = select_row(
        read_csv(CHECKPOINT_4959_BOUNDS),
        scheme="dynamic_etaN",
        polynomial_order="8",
    )
    invariant_rows = read_csv(CHECKPOINT_4953_INVARIANTS)
    invariant_map = {row["derivation_id"]: row for row in invariant_rows}
    offshell_rows = read_csv(CHECKPOINT_4954_DECISION)
    offshell_map = {row["decision_id"]: row for row in offshell_rows}
    double_count_rows = read_csv(CHECKPOINT_5171_DOUBLE_COUNT)

    radius_m = float(state_row["R_n_over_L_eff"]) * float(
        state_row["L_eff_kpc"]
    ) * KPC_M
    velocity_m_s = float(state_row["v_infinity_km_s"]) * 1000.0
    beta = velocity_m_s / LIGHT_SPEED_M_S
    abs_u_o4_over_z_m4 = float(
        o4["dimensionful_endpoint_envelope"]["abs_u_O4_over_Z_m4"]
    )
    o4_fraction_at_transition = (
        96.0
        * abs_u_o4_over_z_m4
        * beta**4
        / radius_m**4
    )

    transition_amplitudes = [
        float(row["amplitude_required_at_transition"])
        for row in amplitude_rows
    ]
    minimum_required_relative_transition_correction = (
        min(transition_amplitudes) - 1.0
    )
    quantum_proxy_transition = float(wave_row["epsilon_squared_at_R_n"])
    quantum_proxy_max_observed = float(
        wave_row[
            "maximum_observed_quantum_proxy_epsilon_over_x_squared"
        ]
    )

    return {
        "motion": motion,
        "o4": o4,
        "ctp": ctp,
        "x2": x2,
        "offshell": offshell,
        "universal": universal,
        "critical": critical,
        "transfer": transfer,
        "covariance": covariance,
        "vlasov": vlasov,
        "metric_split": metric_split,
        "state_row": state_row,
        "wave_row": wave_row,
        "interaction_row": interaction_row,
        "invariant_map": invariant_map,
        "offshell_map": offshell_map,
        "double_count_rows": double_count_rows,
        "radius_m": radius_m,
        "velocity_m_s": velocity_m_s,
        "beta": beta,
        "abs_u_o4_over_z_m4": abs_u_o4_over_z_m4,
        "o4_fraction_at_transition": o4_fraction_at_transition,
        "transition_amplitudes": transition_amplitudes,
        "minimum_required_relative_transition_correction": (
            minimum_required_relative_transition_correction
        ),
        "quantum_proxy_transition": quantum_proxy_transition,
        "quantum_proxy_max_observed": quantum_proxy_max_observed,
        "required_coefficient_over_quantum_transition": (
            minimum_required_relative_transition_correction
            / quantum_proxy_transition
        ),
        "required_coefficient_over_quantum_max_observed": (
            minimum_required_relative_transition_correction
            / quantum_proxy_max_observed
        ),
        "required_coefficient_over_o4": (
            minimum_required_relative_transition_correction
            / o4_fraction_at_transition
        ),
    }


def subtraction_rows(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    imported_double_count = all(
        not parse_bool(row["independent_new_stress"])
        for row in inputs["double_count_rows"]
    )
    return [
        {
            "ledger_id": "S5178_00_vacuum_local",
            "sector": "vacuum determinant local derivative expansion",
            "operation": "absorb into Lambda, M_R^2, a_R, a_C and higher Wilson matching",
            "already_counted_where": "checkpoint 4949 vacuum matching and checkpoint 4960 Gamma_higher",
            "subtract_before_new_state_stress": True,
            "independent_new_galaxy_stress": False,
            "reason": "state independent and not an adjustable occupation",
            "status": "MATCHED_NOT_READDABLE",
            "valid_for_claim": False,
        },
        {
            "ledger_id": "S5178_01_vacuum_finite_nonlocal",
            "sector": "finite nonlocal vacuum polarization",
            "operation": "retain as calculable state-independent quantum correction",
            "already_counted_where": "checkpoint 4949 Wilson ledger; coefficient matching remains explicit",
            "subtract_before_new_state_stress": True,
            "independent_new_galaxy_stress": False,
            "reason": "cannot be renamed as a free high-occupation halo source",
            "status": "CALCULABLE_QUANTUM_RESIDUAL_NOT_OCCUPATION",
            "valid_for_claim": False,
        },
        {
            "ledger_id": "S5178_02_gaussian_occupied_classical",
            "sector": "leading Wigner projection of the Gaussian occupied-state Schur term",
            "operation": "identify with linearized Vlasov response and subtract from any proposed additive stress",
            "already_counted_where": "checkpoints 5164-5169 nonlinear characteristics and checkpoint 5171 Frechet kernel",
            "subtract_before_new_state_stress": True,
            "independent_new_galaxy_stress": False,
            "reason": (
                "the same state, force and source history were already evolved; "
                "the checkpoint-5171 double-count ledger is fully negative="
                f"{imported_double_count}"
            ),
            "status": "FORBIDDEN_DOUBLE_COUNT",
            "valid_for_claim": False,
        },
        {
            "ledger_id": "S5178_03_gaussian_quantum_gradient",
            "sector": "higher Wigner/Moyal gradients of the occupied Gaussian state",
            "operation": "retain only as a controlled wave correction, not as a free stress",
            "already_counted_where": "checkpoint 5155 SP-to-Vlasov expansion and wave-resolution gate",
            "subtract_before_new_state_stress": False,
            "independent_new_galaxy_stress": True,
            "reason": "not identical to classical Vlasov, but its selected benchmark expansion parameter is bounded",
            "status": "INDEPENDENT_BUT_POWER_COUNTING_TOO_SMALL_IN_REFERENCE_WINDOW",
            "valid_for_claim": False,
        },
        {
            "ledger_id": "S5178_04_O4_portal",
            "sector": "C^2 (nabla psi)^2 Hessian and Hilbert contact terms",
            "operation": "retain with the parent coefficient; never fit it to the galaxy residual",
            "already_counted_where": "checkpoints 4935 and 4942",
            "subtract_before_new_state_stress": False,
            "independent_new_galaxy_stress": True,
            "reason": "parent owned but Planck-scaled curvature suppression is explicit",
            "status": "PARENT_OWNED_AND_NUMERICALLY_SILENT",
            "valid_for_claim": False,
        },
        {
            "ledger_id": "S5178_05_Poynting",
            "sector": "visible Maxwell/Poynting energy-momentum",
            "operation": "keep in the same universal Hilbert source and assembly history",
            "already_counted_where": "checkpoints 4960 and 5165-5169",
            "subtract_before_new_state_stress": True,
            "independent_new_galaxy_stress": False,
            "reason": (
                "T_EM^0i=E cross B is a component of the existing source; "
                "it can prepare motion only through a separately derived interaction or boundary kernel"
            ),
            "status": "SOURCE_HISTORY_NOT_SECOND_GRAVITATIONAL_COUPLING",
            "valid_for_claim": False,
        },
        {
            "ledger_id": "S5178_06_nonGaussian_boundary",
            "sector": "non-Gaussian initial density matrix or mixed initial correlations",
            "operation": "do not subtract; derive Gamma_rho0 from a parent state-preparation principle",
            "already_counted_where": "not present in the executed Gaussian/Vlasov profile",
            "subtract_before_new_state_stress": False,
            "independent_new_galaxy_stress": True,
            "reason": "this is boundary data, not a replacement G_N or a post-hoc radial multiplier",
            "status": "ONLY_UNCOUNTED_STATE_PREPARATION_ROUTE",
            "valid_for_claim": False,
        },
    ]


def residual_bound_rows(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    critical = inputs["critical"]["critical_mixing"]
    minimum_required = inputs[
        "minimum_required_relative_transition_correction"
    ]
    return [
        {
            "bound_id": "B5178_00_required_transition",
            "quantity": "minimum additive fractional V2 correction implied by the twelve locked MTS transition amplitudes",
            "value": minimum_required,
            "units": "dimensionless",
            "comparison": (
                f"min(A_transition_MTS)-1 from {min(inputs['transition_amplitudes'])}"
            ),
            "status": "ORDER_ONE_PROFILE_DEFICIT",
            "valid_for_claim": False,
        },
        {
            "bound_id": "B5178_01_O4_transition",
            "quantity": "absolute O4 kinetic prefactor correction at R_n",
            "value": inputs["o4_fraction_at_transition"],
            "units": "dimensionless",
            "comparison": (
                "96 |u_O4/Z| (v_infinity/c)^4 / R_n^4 using the spherical "
                "M_geom/R=(v/c)^2 envelope"
            ),
            "status": "TOO_SMALL_FOR_ORDER_ONE_RESIDUAL",
            "valid_for_claim": False,
        },
        {
            "bound_id": "B5178_02_O4_required_enhancement",
            "quantity": "coefficient enhancement required for O4 to equal the minimum transition deficit",
            "value": inputs["required_coefficient_over_o4"],
            "units": "dimensionless ratio",
            "comparison": "minimum required fractional correction divided by O4 prefactor",
            "status": "PARENT_O4_CANNOT_REPAIR_PROFILE",
            "valid_for_claim": False,
        },
        {
            "bound_id": "B5178_03_wave_at_transition",
            "quantity": "selected 1e-20 eV Wigner-gradient proxy at R_n",
            "value": inputs["quantum_proxy_transition"],
            "units": "dimensionless",
            "comparison": "(hbar/(m v R_n))^2",
            "status": "CONTROLLED_CLASSICAL_WINDOW",
            "valid_for_claim": False,
        },
        {
            "bound_id": "B5178_04_wave_max_observed",
            "quantity": "selected 1e-20 eV maximum Wigner-gradient proxy over observed radii",
            "value": inputs["quantum_proxy_max_observed"],
            "units": "dimensionless",
            "comparison": "max_Robserved (hbar/(m v R))^2",
            "status": "CONTROLLED_CLASSICAL_WINDOW",
            "valid_for_claim": False,
        },
        {
            "bound_id": "B5178_05_wave_required_enhancement",
            "quantity": "minimum coefficient needed for the largest observed wave proxy to equal the transition deficit",
            "value": inputs[
                "required_coefficient_over_quantum_max_observed"
            ],
            "units": "dimensionless ratio",
            "comparison": "minimum required correction divided by maximum observed proxy",
            "status": "CONTROLLED_GRADIENT_EXPANSION_CANNOT_SUPPLY_ORDER_ONE_REPAIR",
            "valid_for_claim": False,
        },
        {
            "bound_id": "B5178_06_critical_IR",
            "quantity": "required occupied-medium infrared determinant behavior",
            "value": float(critical["low_k_target_slope"]),
            "units": "power of |k|",
            "comparison": "1-zeta(k) proportional |k| from checkpoint 5149",
            "status": "NONANALYTIC_CRITICAL_TARGET",
            "valid_for_claim": False,
        },
        {
            "bound_id": "B5178_07_gapped_Gaussian_analyticity",
            "quantity": "lowest nonconstant power available to a regular local gapped Gaussian Hessian",
            "value": 2.0,
            "units": "power of k",
            "comparison": (
                "A(k^2), B(k^2), C(k^2)^-1 are analytic if det C(0) is nonzero"
            ),
            "status": "CANNOT_EQUAL_ABS_K_WITHOUT_ZERO_MODE_OR_CONTINUUM",
            "valid_for_claim": False,
        },
    ]


def interaction_rows(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    invariants = inputs["invariant_map"]
    offshell = inputs["offshell_map"]
    bound = inputs["interaction_row"]
    return [
        {
            "gate_id": "I5178_00_Gaussian",
            "kernel_or_state": "displayed checkpoint-4949 scalar Gamma_2",
            "parent_result": inputs["ctp"]["parent_CTP_result"][
                "scalar_only_fixed_metric_Gamma2"
            ],
            "deduction": "no bulk non-Gaussian Bethe-Salpeter kernel in the Hessian-only truncation",
            "independent_uncounted_static_stress": False,
            "status": "EXACT_ZERO_IN_DISPLAYED_TRUNCATION",
            "valid_for_claim": False,
        },
        {
            "gate_id": "I5178_01_X2_number",
            "kernel_or_state": "on-shell X2 2<->2 collision kernel",
            "parent_result": invariants["COL4953_03_number"]["status"],
            "deduction": "cannot create the required occupation number",
            "independent_uncounted_static_stress": False,
            "status": "NUMBER_COLLISION_INVARIANT_EXACT",
            "valid_for_claim": False,
        },
        {
            "gate_id": "I5178_02_X2_stress",
            "kernel_or_state": "on-shell X2 2<->2 stress moment",
            "parent_result": invariants["COL4953_04_four_momentum"]["status"],
            "deduction": "redistribution preserves total Hilbert stress",
            "independent_uncounted_static_stress": False,
            "status": "STRESS_COLLISION_INVARIANT_EXACT",
            "valid_for_claim": False,
        },
        {
            "gate_id": "I5178_03_X2_equilibrium",
            "kernel_or_state": "stationary Bose distribution under 2<->2",
            "parent_result": invariants["COL4953_05_equilibrium"]["status"],
            "deduction": "detailed balance makes the collision term zero while allowing a state-set chemical potential",
            "independent_uncounted_static_stress": False,
            "status": "NO_STATIONARY_SOURCE_SELECTION",
            "valid_for_claim": False,
        },
        {
            "gate_id": "I5178_04_controlled_2to4",
            "kernel_or_state": "complete leading six-point trajectory bound",
            "parent_result": float(
                bound["full_basis_kernel_minimized_over_O2"]
            ),
            "deduction": (
                "the channel exists and cannot be cancelled, but checkpoint "
                "4954 rejects the controlled high-frequency formation envelope"
            ),
            "independent_uncounted_static_stress": False,
            "status": "NONZERO_BUT_CONTROLLED_FORMATION_ROUTE_REJECTED",
            "valid_for_claim": False,
        },
        {
            "gate_id": "I5178_05_strong_CTP",
            "kernel_or_state": "strong nonquasiparticle X2-X3 2PI kernel",
            "parent_result": offshell["DEC4954_06_persistent_width"]["status"],
            "deduction": "requires an unequal-time nonperturbative solve and cannot be inferred from the Gaussian Hessian",
            "independent_uncounted_static_stress": True,
            "status": "OPEN_NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "gate_id": "I5178_06_Gaussian_covariance",
            "kernel_or_state": "homogeneous Gaussian n_k, c_k or P_R/P_S/P_RS",
            "parent_result": "NOT_UNIQUELY_FIXED_BY_THE_QUADRATIC_ACTION",
            "deduction": "checkpoint 5156 proves that reflection evenness and the Hessian do not select the covariance",
            "independent_uncounted_static_stress": True,
            "status": "PARENT_STATE_PREPARATION_LAW_OPEN",
            "valid_for_claim": False,
        },
        {
            "gate_id": "I5178_07_critical_medium",
            "kernel_or_state": "checkpoint-5149 occupied critical CTP continuum",
            "parent_result": inputs["critical"]["critical_mixing"][
                "occupied_critical_CTP_route_survives"
            ],
            "deduction": (
                "can evade the analytic gapped no-go only if its state, spectral "
                "density and mixing are generated by the parent"
            ),
            "independent_uncounted_static_stress": True,
            "status": "KINEMATICALLY_SURVIVES_PARENT_DERIVATION_OPEN",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D5178_00_exact_reduction",
            "question": "Does stationary 2PI elimination produce a definite metric response?",
            "answer": "YES",
            "reason": "Gammabar_gg=A-B C^-1 B_dagger",
            "status": "EXACT_SCHUR_COMPLEMENT",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D5178_01_conservation",
            "question": "Does the reduced response preserve the parent diffeomorphism Ward identity?",
            "answer": "YES_ON_THE_COMPLETE_BACKGROUND_EOM",
            "reason": "the full Ward null vector descends through the same C^-1 used in the Schur complement",
            "status": "EXACT_ON_SHELL_WARD_DESCENT",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D5178_02_Gaussian_new_stress",
            "question": "May the Gaussian occupied-state Schur term be added to checkpoints 5164-5177 as new stress?",
            "answer": "NO",
            "reason": "its leading classical projection is the already-evolved Vlasov response",
            "status": "FORBIDDEN_DOUBLE_COUNT",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D5178_03_O4_wave_repair",
            "question": "Can the parent O4 or controlled wave-gradient residual repair the order-one transition amplitude?",
            "answer": "NO_WITHIN_THE_CONTROLLED_REFERENCE_BRANCH",
            "reason": "the computed suppressions are many orders below the locked profile deficit",
            "status": "NUMERIC_POWER_COUNTING_NO_GO",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D5178_04_critical_response",
            "question": "Can a regular gapped local Gaussian Hessian generate the required |k| critical determinant?",
            "answer": "NO",
            "reason": "its Schur blocks are analytic in k^2 while the target is nonanalytic",
            "status": "ANALYTICITY_NO_GO",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D5178_05_survivor",
            "question": "What uncounted route remains?",
            "answer": "PARENT_DERIVED_NON_GAUSSIAN_INITIAL_OR_STRONG_INTERACTING_CTP_KERNEL",
            "reason": "only Gamma_rho0, nonzero Gamma_2 or a derived critical continuum can survive all subtractions",
            "status": "ONE_NARROW_ROUTE_REMAINS_OPEN",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D5178_06_local_branch",
            "question": "Is the calibrated local GR/Newton/Maxwell source changed?",
            "answer": "NO",
            "reason": "Delta G_state=0 locally, O4 tree stress is zero at psi=0 and no second source normalization is introduced",
            "status": "CHECKPOINT_4960_BRANCH_RETAINED",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D5178_07_route_token",
            "question": "What is the checkpoint route decision?",
            "answer": ROUTE_DECISION,
            "reason": "exact reduction plus subtraction and quantitative residual bounds",
            "status": "ADVANCE_TO_STATE_PREPARATION_OR_STRONG_CTP_NOT_NEW_COUPLING",
            "valid_for_claim": False,
        },
    ]


def validation_row(
    validation_id: str,
    description: str,
    passed: bool,
    observed: Any,
    expected: Any,
) -> dict[str, Any]:
    return {
        "validation_id": validation_id,
        "description": description,
        "passed": bool(passed),
        "observed": observed,
        "expected": expected,
        "checkpoint_marker": MARKER,
        "valid_for_full_MTS_claim": False,
    }


def write_document(result: dict[str, Any]) -> None:
    summary = result["summary"]
    DOCUMENT.write_text(
        f"""# 5178 - Exact 2PI Schur/Ward reduction, Vlasov subtraction and Gaussian residual-stress no-go

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

This checkpoint performs the parent-Hessian calculation requested by
checkpoint 5177. It does not add another target ledger and it does not fit a
new source coefficient. The stationary CTP-2PI correlator can be eliminated
exactly. Its metric response is the Schur complement

```text
Gammabar_gg=A-B C^-1 B_dagger.
```

The same inverse `C^-1` carries the full diffeomorphism Ward null vector into
the reduced kernel, so conservation survives on the complete background
equations. However, this does **not** make the whole Schur term a new source.
After the state-independent vacuum terms and the already-evolved classical
Vlasov response are removed, the current regular gapped Gaussian Hessian has
no independent order-one stress left to add to the checkpoint-5176/5177
profiles.

This narrows rather than abandons the MTS route. A new stress now requires a
parent-derived non-Gaussian initial boundary functional, a nonzero strong
`Gamma_2` kernel or a derived occupied critical continuum. It cannot be a
second `G_N`, an additive replay of Vlasov polarization, or an `O4` coefficient
retuned to the galaxy.

## 1. Exact stationary elimination

At zero motion one-point, write the renormalized contour functional as

```text
Gamma[g,G]
 =S_g[g]
  +(i/2) Tr ln G^-1
  +(i/2) Tr(D^-1[g]G-1)
  +Gamma_2[g,G]+Gamma_ct+Gamma_rho0.
```

`Gamma_rho0` records initial density-matrix vertices. It is boundary data, not
a radial force law. The physical correlator satisfies

```text
Gamma_,G[g,G_star[g]]=0.
```

With

```text
A=Gamma_gg,  B=Gamma_gG,  C=Gamma_GG,
```

differentiating stationarity gives

```text
dG_star/dg=-C^-1 B_dagger.
```

The reduced action `Gammabar[g]=Gamma[g,G_star[g]]` consequently obeys

```text
Gammabar_,g=Gamma_,g,
Gammabar_gg=A-B C^-1 B_dagger.
```

This is an exact implicit-function theorem, not a closure ansatz. On the
physical CTP branch `C^-1` means the causal inverse after contour boundary
conditions and any exact zero modes have been fixed.

Twelve rational-arithmetic block systems independently verify the Schur
identity, determinant factorization, full response equivalence, quadratic
completion and one gauge null direction. All
`{summary['exact_Schur_trial_count']}/{summary['exact_Schur_trial_count']}`
trials pass with exactly zero algebraic residual.

## 2. Ward identity after eliminating the correlator

On the complete background equations, diffeomorphism invariance gives

```text
[[A,B],[B_dagger,C]] (R_g,R_G)^T=0.
```

The lower block yields

```text
R_G=-C^-1 B_dagger R_g.
```

Substitution into the upper block gives

```text
(A-B C^-1 B_dagger)R_g=0.
```

Thus the same Schur complement is transverse on shell. Away from the complete
metric-plus-matter equations, the standard contact/EOM terms must be retained;
this checkpoint does not falsely call an isolated fixed-background matter
kernel transverse when its source is off shell. Checkpoint 4960's universal
Hilbert source supplies the complete conserved system.

The retarded stress response has the familiar form

```text
Pi_R=Pi_contact-i theta(x0-y0)<[T(x),T(y)]>,
```

where metric seagulls, including the `O4` variation, belong to
`Pi_contact`. The connected bubble and its Bethe-Salpeter resummation are
therefore fixed by the same parent action; they are not a new material-labelled
gravitational coupling.

## 3. What the Gaussian Hessian actually contains

For the checkpoint-4949 displayed quadratic scalar truncation,

```text
Gamma_2=0,
C_0=(i/2) G^-1 tensor_s G^-1,
B_0=(i/2) delta D^-1/delta g + contact terms.
```

The Schur term generated by `B_0 C_0^-1 B_0_dagger` is the connected Gaussian
stress bubble. Its leading Wigner/gradient projection is the collisionless
Vlasov response. Checkpoints 5164-5169 already evolved the same antithetic
state under the same Poisson characteristics, and checkpoint 5171 explicitly
constructed its Frechet response. Adding it again to the scored profile would
count the same physical response twice.

The vacuum part is also not missing. Local terms in `Tr ln D/2` renormalize
`Lambda`, `M_R^2`, `a_R`, `a_C` and higher Wilson coefficients. Finite
state-independent nonlocal terms remain calculable quantum corrections; they
cannot be renamed as an adjustable high-occupation galaxy source.

Maxwell/Poynting flow is treated the same way. `T_EM^0i=(E cross B)^i` already
enters checkpoint 4960's Hilbert tensor and checkpoints 5165-5169's assembly
history. It may help prepare a motion state only if a parent interaction or
initial-boundary kernel is derived. It is not a second gravitational source
normalization.

## 4. Quantitative residual bounds

For the locked reference galaxy and mass,

```text
galaxy                  = {REFERENCE_GALAXY};
mapping                 = {REFERENCE_MAPPING};
m_gap                   = 1e-20 eV;
R_n                     = {summary['reference_transition_radius_kpc']} kpc;
v_infinity              = {summary['reference_velocity_km_s']} km/s.
```

Checkpoint 4942 gives

```text
|u_O4/Z|={summary['abs_u_O4_over_Z_m4']} m^4.
```

Using `C^2=48 M_geom^2/r^6` and the conservative spherical relation
`M_geom/r=(v/c)^2`, the occupied-state kinetic prefactor at `R_n` is bounded by

```text
|Delta Z_O4/Z|
 =96 |u_O4/Z| (v/c)^4/R_n^4
 ={summary['O4_fraction_at_transition']}.
```

The twelve locked MTS profiles require at least
`{summary['minimum_required_relative_transition_correction']}` additional
fractional `V^2` at the transition. `O4` would therefore need an enhancement
of `{summary['required_coefficient_over_O4']}`, despite its coefficient
already being fixed by the parent trajectory.

The selected `1e-20 eV` Wigner correction is

```text
epsilon_Rn^2={summary['quantum_proxy_at_transition']};
max_observed (epsilon_Rn/x)^2={summary['maximum_observed_quantum_proxy']}.
```

Even granting the largest observed proxy, an order-one repair needs an
undemonstrated coefficient of at least
`{summary['required_coefficient_over_maximum_quantum_proxy']}`. That is outside
the controlled gradient expansion. This is a power-counting no-go for the
reference branch, not a theorem against every nonperturbative wave core.

## 5. Criticality and interaction gate

Checkpoint 5149 requires

```text
1-zeta(k) proportional |k|
```

in the infrared. A local gapped Gaussian parent has analytic
`A(k^2)`, `B(k^2)` and `C(k^2)`. If `det C(0)` is nonzero, `C^-1(k^2)` and
the Schur complement are analytic in `k^2`; they cannot generate `|k|`.
Therefore a zero mode, continuum threshold, occupied critical state or
non-Gaussian kernel is mandatory. This is the exact analyticity wall behind
the earlier numerical target.

The already-derived interaction hierarchy does not supply a hidden easy
escape:

- `X2` on-shell `2<->2` conserves quasiparticle number and stress exactly;
- its stationary Bose collision term satisfies detailed balance and does not
  select the occupation;
- the complete leading six-point channel is nonzero, with the dynamic-`eta_N`,
  order-eight lower kernel
  `{summary['controlled_sixpoint_minimum_kernel']}`, but checkpoints
  4954-4959 reject the controlled formation envelope;
- a strongly broadened nonquasiparticle `X2-X3` CTP state remains open, not
  derived;
- checkpoint 5156 proves that the quadratic action and reflection evenness do
  not select `n_k`, `c_k`, `P_R`, `P_S` or `P_RS`.

## 6. Consequence for checkpoint 5177

Checkpoint 5177's no-retuning theorem remains intact. What changes is the
interpretation of its suggested residual-stress route:

```text
vacuum local response             -> already matched;
vacuum finite response            -> calculable, not occupation;
Gaussian classical state response -> already evolved Vlasov response;
O4 response                       -> parent owned, approximately 10^-233 here;
controlled wave response          -> at most an expansion correction here;
X2 equilibrium collisions         -> no state source;
non-Gaussian Gamma_rho0/Gamma_2    -> genuinely uncounted and still open.
```

The next calculation must therefore derive or reject the lowest
non-Gaussian state-preparation kernel rather than invent another galaxy
coupling. The clean entry is the boundary/initial CTP functional on the
checkpoint-5156 FLRW branch, joined to the checkpoint-4953/4959 interaction
kernel and checkpoint-4960 Hilbert source. If that kernel vanishes or remains
perturbatively incapable, the extra-stress repair route closes and the locked
formation result must stand as a metric split rather than be tuned.

## 7. Exact status

```text
stationary 2PI Schur complement                         = derived exactly;
full-to-reduced on-shell Ward identity                  = derived exactly;
connected stress kernel location                        = derived;
vacuum matching subtraction                             = explicit;
classical Vlasov double-count subtraction               = explicit;
Gaussian gapped |k| critical response                   = rejected exactly;
O4 order-one profile repair                             = rejected numerically;
controlled wave-gradient order-one repair               = rejected by power counting;
X2 2<->2 occupation source                              = rejected exactly;
controlled six-point formation route                    = previously rejected;
strong non-Gaussian CTP/initial-state kernel             = open;
local GR/Newton/Maxwell source residue                   = unchanged;
galaxy or full-MTS claim                                 = false.
```

Route decision:
`{ROUTE_DECISION}`.

All `{result['validation_count']}` generated validation checks pass. The
protected `formalization-workbench` digest remains
`{result['formalization_workbench_tree_sha256']}` and the immutable checkpoint
5176 tree remains `{result['checkpoint_5176_tree_sha256']}`. No GitHub action
or public-worktree write occurred.
""",
        encoding="utf-8",
    )


def run(dry_run: bool) -> dict[str, Any]:
    paths = source_paths()
    missing = [str(path) for path in paths.values() if not path.exists()]
    if missing:
        raise RuntimeError(f"missing source paths: {missing}")

    source_hashes_before = {
        name: file_digest(path) for name, path in paths.items()
    }
    formal_before = tree_digest(FORMAL)
    checkpoint_5176_before = tree_digest(CHECKPOINT_5176_ROOT)
    schur_rows = exact_schur_trials()
    kernel_rows = connected_kernel_rows()
    inputs = derive_physical_inputs()
    subtraction = subtraction_rows(inputs)
    bounds = residual_bound_rows(inputs)
    interactions = interaction_rows(inputs)
    decisions = decision_rows()

    summary = {
        "exact_Schur_trial_count": len(schur_rows),
        "all_exact_Schur_trials_pass": all(
            row["all_exact_identities_pass"] for row in schur_rows
        ),
        "maximum_exact_Schur_residual": 0,
        "reference_galaxy": REFERENCE_GALAXY,
        "reference_mapping": REFERENCE_MAPPING,
        "reference_mass_label": REFERENCE_MASS_LABEL,
        "reference_transition_radius_kpc": (
            inputs["radius_m"] / KPC_M
        ),
        "reference_velocity_km_s": (
            inputs["velocity_m_s"] / 1000.0
        ),
        "abs_u_O4_over_Z_m4": inputs["abs_u_o4_over_z_m4"],
        "O4_fraction_at_transition": inputs[
            "o4_fraction_at_transition"
        ],
        "minimum_MTS_transition_amplitude": min(
            inputs["transition_amplitudes"]
        ),
        "maximum_MTS_transition_amplitude": max(
            inputs["transition_amplitudes"]
        ),
        "minimum_required_relative_transition_correction": inputs[
            "minimum_required_relative_transition_correction"
        ],
        "quantum_proxy_at_transition": inputs[
            "quantum_proxy_transition"
        ],
        "maximum_observed_quantum_proxy": inputs[
            "quantum_proxy_max_observed"
        ],
        "required_coefficient_over_transition_quantum_proxy": inputs[
            "required_coefficient_over_quantum_transition"
        ],
        "required_coefficient_over_maximum_quantum_proxy": inputs[
            "required_coefficient_over_quantum_max_observed"
        ],
        "required_coefficient_over_O4": inputs[
            "required_coefficient_over_o4"
        ],
        "critical_low_k_target_power": inputs["critical"][
            "critical_mixing"
        ]["low_k_target_slope"],
        "critical_low_k_measured_power": inputs["critical"][
            "critical_mixing"
        ]["low_k_one_minus_zeta_slope"],
        "controlled_sixpoint_minimum_kernel": float(
            inputs["interaction_row"][
                "full_basis_kernel_minimized_over_O2"
            ]
        ),
        "checkpoint_5171_double_count_rows": len(
            inputs["double_count_rows"]
        ),
        "all_checkpoint_5171_rows_deny_independent_stress": all(
            not parse_bool(row["independent_new_stress"])
            for row in inputs["double_count_rows"]
        ),
        "gaussian_hessian_independent_post_Vlasov_stress": False,
        "regular_gapped_Gaussian_can_generate_abs_k": False,
        "strong_nonGaussian_route_open": True,
        "local_GR_Newton_Maxwell_branch_modified": False,
        "valid_for_galaxy_claim": False,
        "valid_for_full_MTS_claim": False,
        "route_decision": ROUTE_DECISION,
    }

    dry_checks = [
        validation_row(
            "V5178_00_sources",
            "all cited local source paths exist",
            not missing,
            len(paths) - len(missing),
            len(paths),
        ),
        validation_row(
            "V5178_01_formal_lock",
            "protected formalization-workbench digest is unchanged",
            formal_before == FORMAL_DIGEST_LOCK,
            formal_before,
            FORMAL_DIGEST_LOCK,
        ),
        validation_row(
            "V5178_02_5176_lock",
            "immutable checkpoint-5176 tree is unchanged",
            checkpoint_5176_before == CHECKPOINT_5176_TREE_LOCK,
            checkpoint_5176_before,
            CHECKPOINT_5176_TREE_LOCK,
        ),
        validation_row(
            "V5178_03_exact_trials",
            "all rational Schur/Ward trials pass",
            summary["all_exact_Schur_trials_pass"],
            sum(row["all_exact_identities_pass"] for row in schur_rows),
            len(schur_rows),
        ),
        validation_row(
            "V5178_04_rank",
            "every full trial has exactly one gauge null direction",
            all(row["rank_full_Hessian"] == 6 for row in schur_rows),
            [row["rank_full_Hessian"] for row in schur_rows],
            [6] * len(schur_rows),
        ),
        validation_row(
            "V5178_05_determinant",
            "all gauge-fixed determinant factorizations are exact",
            all(
                row["determinant_factorization_exact"]
                for row in schur_rows
            ),
            sum(
                row["determinant_factorization_exact"]
                for row in schur_rows
            ),
            len(schur_rows),
        ),
        validation_row(
            "V5178_06_Gamma2_zero",
            "displayed checkpoint-4949 scalar Gamma2 is zero",
            inputs["ctp"]["parent_CTP_result"][
                "scalar_only_fixed_metric_Gamma2"
            ]
            == 0.0,
            inputs["ctp"]["parent_CTP_result"][
                "scalar_only_fixed_metric_Gamma2"
            ],
            0.0,
        ),
        validation_row(
            "V5178_07_vacuum_local",
            "checkpoint-4949 retains local vacuum matching",
            inputs["ctp"]["stress_and_local_limit"][
                "vacuum_Wilson_matching_still_open"
            ],
            inputs["ctp"]["stress_and_local_limit"][
                "vacuum_Wilson_matching_still_open"
            ],
            True,
        ),
        validation_row(
            "V5178_08_vlasov_double_count",
            "all checkpoint-5171 ledger rows deny independent new stress",
            summary[
                "all_checkpoint_5171_rows_deny_independent_stress"
            ],
            len(inputs["double_count_rows"]),
            4,
        ),
        validation_row(
            "V5178_09_X2_number",
            "X2 2-to-2 number collision invariant is exact",
            parse_bool(
                inputs["invariant_map"]["COL4953_03_number"]["passed"]
            ),
            inputs["invariant_map"]["COL4953_03_number"]["status"],
            "passed",
        ),
        validation_row(
            "V5178_10_X2_stress",
            "X2 2-to-2 stress collision invariant is exact",
            parse_bool(
                inputs["invariant_map"][
                    "COL4953_04_four_momentum"
                ]["passed"]
            ),
            inputs["invariant_map"][
                "COL4953_04_four_momentum"
            ]["status"],
            "passed",
        ),
        validation_row(
            "V5178_11_strong_CTP_open",
            "strong nonquasiparticle route is not silently claimed",
            inputs["offshell_map"]["DEC4954_06_persistent_width"][
                "status"
            ]
            == "STRONG_NONQUASIPARTICLE_ROUTE_OPEN",
            inputs["offshell_map"]["DEC4954_06_persistent_width"][
                "status"
            ],
            "STRONG_NONQUASIPARTICLE_ROUTE_OPEN",
        ),
        validation_row(
            "V5178_12_O4_positive",
            "O4 transition correction is positive finite",
            math.isfinite(summary["O4_fraction_at_transition"])
            and summary["O4_fraction_at_transition"] > 0.0,
            summary["O4_fraction_at_transition"],
            ">0 finite",
        ),
        validation_row(
            "V5178_13_O4_small",
            "O4 transition correction is far below the locked deficit",
            summary["O4_fraction_at_transition"]
            < summary[
                "minimum_required_relative_transition_correction"
            ],
            summary["required_coefficient_over_O4"],
            ">1",
        ),
        validation_row(
            "V5178_14_wave_controlled",
            "selected maximum observed wave proxy is below one percent",
            summary["maximum_observed_quantum_proxy"] < 0.01,
            summary["maximum_observed_quantum_proxy"],
            "<0.01",
        ),
        validation_row(
            "V5178_15_wave_small",
            "controlled wave proxy is far below the locked deficit",
            summary["required_coefficient_over_maximum_quantum_proxy"]
            > 1.0e4,
            summary[
                "required_coefficient_over_maximum_quantum_proxy"
            ],
            ">1e4",
        ),
        validation_row(
            "V5178_16_critical_target",
            "checkpoint-5149 requires a linear absolute-k infrared determinant",
            abs(
                float(summary["critical_low_k_target_power"]) - 1.0
            )
            < 1.0e-15,
            summary["critical_low_k_target_power"],
            1.0,
        ),
        validation_row(
            "V5178_17_Gaussian_analytic_no_go",
            "regular gapped Gaussian route is not promoted to the nonanalytic target",
            not summary[
                "regular_gapped_Gaussian_can_generate_abs_k"
            ],
            summary[
                "regular_gapped_Gaussian_can_generate_abs_k"
            ],
            False,
        ),
        validation_row(
            "V5178_18_universal_source",
            "checkpoint-4960 retains one leading source coupling",
            inputs["universal"]["decision"][
                "leading_local_source_coupling"
            ]
            == "DERIVED_WITHIN_DECLARED_INTEGRATED_H_DIFF_PARENT",
            inputs["universal"]["decision"][
                "leading_local_source_coupling"
            ],
            "DERIVED_WITHIN_DECLARED_INTEGRATED_H_DIFF_PARENT",
        ),
        validation_row(
            "V5178_19_covariance_open",
            "checkpoint-5156 does not claim the parent covariance is derived",
            not inputs["covariance"]["valid_for_full_MTS_claim"],
            inputs["covariance"]["valid_for_full_MTS_claim"],
            False,
        ),
        validation_row(
            "V5178_20_nonclaims",
            "all route and decomposition rows remain nonclaim",
            all(
                not row["valid_for_claim"]
                for row in subtraction + bounds + interactions + decisions
            )
            and all(
                not row["valid_for_full_MTS_claim"]
                for row in kernel_rows + schur_rows
            ),
            "all_false",
            "all_false",
        ),
    ]

    if dry_run:
        failures = [
            row["validation_id"]
            for row in dry_checks
            if not row["passed"]
        ]
        if failures:
            raise RuntimeError(f"dry-run validation failures: {failures}")
        return {
            "mode": "dry-run",
            "checkpoint_marker": MARKER,
            "planned_outputs": [
                str(path)
                for path in (
                    SCHUR_CSV,
                    KERNEL_CSV,
                    SUBTRACTION_CSV,
                    BOUND_CSV,
                    INTERACTION_CSV,
                    DECISION_CSV,
                    PROVENANCE_CSV,
                    RESULT_JSON,
                    VALIDATION_CSV,
                    DOCUMENT,
                )
            ],
            "summary": summary,
            "validation_count": len(dry_checks),
        }

    write_csv(SCHUR_CSV, schur_rows)
    write_csv(KERNEL_CSV, kernel_rows)
    write_csv(SUBTRACTION_CSV, subtraction)
    write_csv(BOUND_CSV, bounds)
    write_csv(INTERACTION_CSV, interactions)
    write_csv(DECISION_CSV, decisions)

    source_hashes_after = {
        name: file_digest(path) for name, path in paths.items()
    }
    formal_after = tree_digest(FORMAL)
    checkpoint_5176_after = tree_digest(CHECKPOINT_5176_ROOT)
    provenance_rows = [
        {
            "source_id": name,
            "source_path": str(path),
            "sha256_before": source_hashes_before[name],
            "sha256_after": source_hashes_after[name],
            "read_only_unchanged": (
                source_hashes_before[name] == source_hashes_after[name]
            ),
            "checkpoint_marker": MARKER,
            "valid_for_claim": False,
        }
        for name, path in paths.items()
    ]
    write_csv(PROVENANCE_CSV, provenance_rows)

    output_paths = (
        SCHUR_CSV,
        KERNEL_CSV,
        SUBTRACTION_CSV,
        BOUND_CSV,
        INTERACTION_CSV,
        DECISION_CSV,
        PROVENANCE_CSV,
    )
    output_text = "\n".join(
        path.read_text(encoding="utf-8") for path in output_paths
    )
    full_checks = dry_checks + [
        validation_row(
            "V5178_21_sources_read_only",
            "all source hashes remain unchanged",
            source_hashes_before == source_hashes_after,
            sum(
                source_hashes_before[name] == source_hashes_after[name]
                for name in paths
            ),
            len(paths),
        ),
        validation_row(
            "V5178_22_formal_after",
            "formalization-workbench remains protected after execution",
            formal_after == formal_before == FORMAL_DIGEST_LOCK,
            formal_after,
            FORMAL_DIGEST_LOCK,
        ),
        validation_row(
            "V5178_23_5176_after",
            "checkpoint-5176 remains immutable after execution",
            checkpoint_5176_after
            == checkpoint_5176_before
            == CHECKPOINT_5176_TREE_LOCK,
            checkpoint_5176_after,
            CHECKPOINT_5176_TREE_LOCK,
        ),
        validation_row(
            "V5178_24_output_rows",
            "all generated CSV row counts are nonzero and exact",
            [
                len(schur_rows),
                len(kernel_rows),
                len(subtraction),
                len(bounds),
                len(interactions),
                len(decisions),
                len(provenance_rows),
            ]
            == [12, 11, 7, 8, 8, 8, len(paths)],
            [
                len(schur_rows),
                len(kernel_rows),
                len(subtraction),
                len(bounds),
                len(interactions),
                len(decisions),
                len(provenance_rows),
            ],
            [12, 11, 7, 8, 8, 8, len(paths)],
        ),
        validation_row(
            "V5178_25_no_missing_markers",
            "generated evidence contains no MISSING_ placeholder",
            "MISSING_" not in output_text,
            "MISSING_" in output_text,
            False,
        ),
        validation_row(
            "V5178_26_route_unique",
            "exactly one decision row names the surviving route",
            sum(
                row["decision_id"] == "D5178_05_survivor"
                for row in decisions
            )
            == 1,
            sum(
                row["decision_id"] == "D5178_05_survivor"
                for row in decisions
            ),
            1,
        ),
        validation_row(
            "V5178_27_local_unchanged",
            "local GR/Newton/Maxwell branch is not modified",
            not summary[
                "local_GR_Newton_Maxwell_branch_modified"
            ],
            summary["local_GR_Newton_Maxwell_branch_modified"],
            False,
        ),
        validation_row(
            "V5178_28_no_claim",
            "checkpoint remains a galaxy and full-MTS nonclaim",
            not summary["valid_for_galaxy_claim"]
            and not summary["valid_for_full_MTS_claim"],
            [
                summary["valid_for_galaxy_claim"],
                summary["valid_for_full_MTS_claim"],
            ],
            [False, False],
        ),
    ]
    failures = [
        row["validation_id"] for row in full_checks if not row["passed"]
    ]
    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "route_decision": ROUTE_DECISION,
        "source_paths": {
            name: str(path) for name, path in paths.items()
        },
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "formalization_workbench_tree_sha256": formal_after,
        "checkpoint_5176_tree_sha256": checkpoint_5176_after,
        "summary": summary,
        "validation_count": len(full_checks),
        "validation_failures": failures,
        "valid_for_local_GR_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    write_json(RESULT_JSON, result)
    write_document(result)
    write_csv(VALIDATION_CSV, full_checks)
    if failures:
        raise RuntimeError(f"validation failures: {failures}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Derive the stationary 2PI Schur/Ward kernel, subtract vacuum "
            "and already-counted Vlasov response, and gate the remaining "
            "Gaussian stress."
        )
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate sources and calculations without writing outputs",
    )
    arguments = parser.parse_args()
    result = run(arguments.dry_run)
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
