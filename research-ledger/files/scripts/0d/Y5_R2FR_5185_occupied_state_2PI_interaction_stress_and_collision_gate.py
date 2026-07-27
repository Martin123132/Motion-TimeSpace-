from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp

sys.dont_write_bytecode = True


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()
OUT = POST / "source-intake" / "functional_rg" / "5185"

HARTREE_CSV = OUT / "gaussian_2PI_Hartree_moments_stress_and_kinetic_tensor.csv"
BASKETBALL_CSV = OUT / "X2_basketball_nonlocal_topology.csv"
WARD_CSV = OUT / "Ward_vacuum_and_Vlasov_subtraction_ledger.csv"
COEFFICIENT_CSV = OUT / "parent_interaction_physical_bounds.csv"
TIME_CSV = OUT / "interaction_time_and_collision_bounds.csv"
ROUTE_CSV = OUT / "occupied_state_interaction_route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "occupied_state_2PI_interaction_results.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5185_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5185-Y5-R2FR-occupied-state-2PI-interaction-stress-and-collision-gate.md"
)

MARKER = "MTS_5185_OCCUPIED_STATE_2PI_INTERACTION_STRESS_COLLISION_GATE"
CHECKED_DATE = "2026-07-23"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5176_TREE_LOCK = (
    "254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b"
)
CHECKPOINT_5176_ROOT = POST / "source-intake" / "functional_rg" / "5176"

G_NATURAL_EV_MINUS2 = 6.70883e-57
HBAR_RATE_PER_EV_S = 1.519267447e15
HBAR_C_EV_M = 1.973269804e-7
EXPOSURE_SECONDS = 1.0e18
REQUIRED_TRANSITION_FRACTION = 1.6440038384385716
MATRIX_DIMENSION = 4

ROUTE_DECISION = (
    "THE_PARENT_ESSENTIAL_X2_AND_X3_VERTICES_DO_GENERATE_AN_EXACT_"
    "DIFFEOMORPHISM_CONSERVING_OCCUPIED_STATE_2PI_STRESS_THE_FIRST_HARTREE_"
    "PACKET_IS_LOCAL_AND_ITS_METRIC_AND_GAP_VARIATIONS_ARE_FIXED_GAUSSIAN_"
    "MOMENT_POLYNOMIALS_THE_FIRST_GENUINELY_NONLOCAL_X2_BASKETBALL_HAS_THE_"
    "EXACT_ALL_CROSS_TOPOLOGY_EIGHT_I2_SQUARED_PLUS_SIXTEEN_I4_AND_CAN_"
    "SUPPORT_A_CONSERVING_COLLISION_KERNEL_AFTER_CTP_CONTINUATION_BUT_THE_"
    "FREE_VLASOV_SUSCEPTIBILITY_MUST_BE_SUBTRACTED_BECAUSE_IT_WAS_ALREADY_"
    "EVOLVED_THE_SOURCE_LOCKED_IR_COEFFICIENTS_BOUND_THE_NEW_HARTREE_"
    "OPERATOR_NORM_BELOW_FOUR_TIMES_TEN_TO_THE_MINUS_116_AND_THE_MOST_"
    "GENEROUS_COHERENT_ACCUMULATION_OVER_TEN_TO_THE_18_SECONDS_BELOW_SIX_"
    "TIMES_TEN_TO_THE_MINUS_101_THE_INDEPENDENT_TWO_TO_TWO_COLLISION_"
    "EXPOSURE_IS_BELOW_TEN_TO_THE_MINUS_281_EVEN_AT_THE_LARGEST_LOCKED_"
    "MASS_THE_KNOWN_INTERACTING_STATE_STRESS_THEREFORE_HAS_THE_RIGHT_WARD_"
    "AND_VACUUM_STRUCTURE_BUT_CANNOT_MOVE_THE_GALAXY_PROFILE_AN_UNKNOWN_O2_"
    "COEFFICIENT_WOULD_REQUIRE_AN_UNCONTROLLED_TEN_TO_THE_28_ENHANCEMENT_"
    "TO_REACH_AN_ORDER_ONE_SIXPOINT_KERNEL_SO_IT_IS_NOT_A_CONTROLLED_RESCUE_"
    "THE_NEXT_CONSTRUCTIVE_TARGET_IS_SOURCE_SELECTION_OF_THE_NEUTRAL_"
    "OCCUPIED_STATE_FROM_THE_PARENT_TIME_DEPENDENT_CTP_BOGOLIUBOV_KERNEL"
)


def source_path(relative: str) -> Path:
    return POST / Path(relative.replace("/", "\\"))


SOURCES = {
    "checkpoint_4958_document": (
        source_path(
            "4958-Y5-R2FR-six-derivative-essential-X2-X3-quotient-and-"
            "invariant-2to4-amplitude-or-rate-route-rejection.md"
        ),
        "d08b8a0ab6a5317c77a23accd34dc46c5ad6a0bc5aa73e0767c8e0aa0edd5f1c",
    ),
    "checkpoint_4958_trajectory": (
        source_path(
            "source-intake/functional_rg/4958/"
            "essential_functional_GR_trajectory.csv"
        ),
        "b4317dcc01084a61a6b282bd331d2ce111b835e499c86e65077d0fb98a549081",
    ),
    "checkpoint_4958_result": (
        source_path(
            "source-intake/functional_rg/4958/"
            "essential_PX_sixpoint_trajectory_results.json"
        ),
        "383e13cd13c3e90be22dbf8ad589c756a26cad002f01da4ce151ad262e48ae67",
    ),
    "checkpoint_4959_document": (
        source_path(
            "4959-Y5-R2FR-O2-O3-O4-external-scalar-sixpoint-projectors-and-"
            "full-invariant-amplitude-or-curvature-route-rejection.md"
        ),
        "295a73fe134df2fc6fc1b08a33c5fcffbf664ccadf20c29fd376f516cbf7da8a",
    ),
    "checkpoint_4959_result": (
        source_path(
            "source-intake/functional_rg/4959/"
            "curvature_sixpoint_projector_results.json"
        ),
        "6febd4e1ca58bf037ee764464c4e7ca3fc99fbd3fc4680c110c64ad6a7df15a8",
    ),
    "checkpoint_4959_amplitude": (
        source_path(
            "source-intake/functional_rg/4959/"
            "trajectory_full_amplitude_bounds.csv"
        ),
        "ac21bb2e42522d8f3aa7cb51fec607b5fd16177c1d35407b6b793469e4ad323a",
    ),
    "checkpoint_4959_gram": (
        source_path(
            "source-intake/functional_rg/4959/"
            "sixpoint_projector_gram_matrix.csv"
        ),
        "18588ba37e9626caa712437148ecf42e5ff6f6579e030d5bdd0c2b0ba546ff04",
    ),
    "checkpoint_4960_document": (
        source_path(
            "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-and-"
            "local-GR-Newton-Maxwell-promotion-or-parent-field-content-"
            "boundary.md"
        ),
        "6cd343d022dde751f86ad82eaf0f61fb5e3616753c228f631c44a45da278a69d",
    ),
    "checkpoint_4960_result": (
        source_path(
            "source-intake/functional_rg/4960/"
            "integrated_H_universal_source_results.json"
        ),
        "6fe2d8335cb1a4902c07c986e597e2f748050aa31f6137c5b52f9ced94542477",
    ),
    "checkpoint_4982_document": (
        source_path(
            "4982-Y5-R2FR-covariant-orderX-Schur-kernel-and-essential-two-"
            "point-subtraction.md"
        ),
        "83bfd153e96f7fb2322e2df1e71dce485caf5b7323230be285081ff280f55645",
    ),
    "checkpoint_4982_result": (
        source_path(
            "source-intake/functional_rg/4982/"
            "covariant_orderX_essential_results.json"
        ),
        "923aceac438808f912b03f032281ccc1bba960987ce70158222efc88f41d6b2f",
    ),
    "checkpoint_5151_document": (
        source_path(
            "5151-Y5-R2FR-parent-projective-occupation-to-conserved-Einstein-"
            "cluster-stress-and-two-metric-cog-gate.md"
        ),
        "b23ca652af8b66c220973cffbdc1ab2df028947c9dba8bd61666d1e0460c5fd5",
    ),
    "checkpoint_5151_result": (
        source_path(
            "source-intake/functional_rg/5151/"
            "projective_state_stress_results.json"
        ),
        "f1331f9bc511f12e4e785c9a3ffcf19dadf4eb8b05b05362031548a22984805c",
    ),
    "checkpoint_5157_document": (
        source_path(
            "5157-Y5-R2FR-composite-motion-clock-charge-entropy-adiabatic-"
            "state-preparation-reentry-gate.md"
        ),
        "dcafb49edbb5032549b3f55fe23a3d6a7edc45f5c7e1d7942f489e13e68fc2e2",
    ),
    "checkpoint_5157_masses": (
        source_path(
            "source-intake/functional_rg/5157/"
            "three_mass_state_preparation_numbers.csv"
        ),
        "4cc47c8a2000b8dd7dc0d617d477af2ffa7d80ef98de483ef3926d2dd781f48f",
    ),
    "checkpoint_5158_document": (
        source_path(
            "5158-Y5-R2FR-clock-charge-source-symmetry-no-go-and-neutral-"
            "state-pivot.md"
        ),
        "cfbd0dd3eb44d0a6621d664f051cb1eb5fa507db30cfc8bf62419c436da087aa",
    ),
    "checkpoint_5158_result": (
        source_path(
            "source-intake/functional_rg/5158/"
            "clock_charge_source_symmetry_results.json"
        ),
        "be43d986495ab4d598715615349e3cabc14bb2c5aa9ecf69a195c2e1eeca9ca5",
    ),
    "checkpoint_5163_document": (
        source_path(
            "5163-Y5-R2FR-parent-wave-stress-and-visible-source-response-"
            "gate.md"
        ),
        "babc8ade1bc3b15f27f8ca9a25ba19417b959b823a2aea6574ce0ca3148865bb",
    ),
    "checkpoint_5163_gradient": (
        source_path(
            "source-intake/functional_rg/5163/"
            "essential_gradient_stress_envelope.csv"
        ),
        "7533f7a7052acf8465327b55ed12ba62a7a43782fd4123095521532368208ee3",
    ),
    "checkpoint_5163_result": (
        source_path(
            "source-intake/functional_rg/5163/"
            "parent_wave_and_visible_source_results.json"
        ),
        "27c53994ea9d86075454d8587fe53cd7c9b0056f10feaf68af05918acac4b43b",
    ),
    "checkpoint_5170_document": (
        source_path(
            "5170-Y5-R2FR-collective-stress-residual-single-coupling-no-go-"
            "and-conserved-kernel-target.md"
        ),
        "0e10880416fb18d153c33ce40982b9d751a2a0532f0ddb5ba7d02ba90a26276c",
    ),
    "checkpoint_5170_result": (
        source_path(
            "source-intake/functional_rg/5170/"
            "collective_stress_residual_results.json"
        ),
        "f7c2f5654f1734802036f7f007aa0094476a94295d288b03a5d0f647da9fa00c",
    ),
    "checkpoint_5171_document": (
        source_path(
            "5171-Y5-R2FR-action-angle-retarded-Vlasov-polarization-static-"
            "response-and-double-counting-gate.md"
        ),
        "e66c543db2154ac061a5930edad50585b5835bbc53e1d2774a0c87d7e19cbade",
    ),
    "checkpoint_5171_result": (
        source_path(
            "source-intake/functional_rg/5171/"
            "action_angle_vlasov_response_results.json"
        ),
        "ee867649d6e1a1784e56d2805f63b4d8b4956fdb2337ba311cda99a4926054e1",
    ),
    "checkpoint_5177_document": (
        source_path(
            "5177-Y5-R2FR-locked-ensemble-metric-split-and-no-retuning-"
            "theorem.md"
        ),
        "abe635ca81992660c7e9bb834eed765626bf63cfc2564f3f4b23b759a3a0fd90",
    ),
    "checkpoint_5177_result": (
        source_path(
            "source-intake/functional_rg/5177/"
            "locked_metric_split_results.json"
        ),
        "2ae85163c0c03a642252f6521d717ddd0a313f113cc6cc65bdf2b0425a2af570",
    ),
    "checkpoint_5184_document": (
        source_path(
            "5184-Y5-R2FR-stationary-PX-background-no-lump-and-mixed-"
            "Hessian-gate.md"
        ),
        "e4a3427963b4de0b5b40baab67b905e9e7054e8033c72dee768fb8973a258e33",
    ),
    "checkpoint_5184_result": (
        source_path(
            "source-intake/functional_rg/5184/"
            "stationary_PX_background_results.json"
        ),
        "203549387a9c8f22721dfe8925c91aa2614a2adbcb3281f487cefb89d849e63b",
    ),
}


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    for file_path in sorted(item for item in path.rglob("*") if item.is_file()):
        relative_path = file_path.relative_to(path).as_posix()
        digest.update(relative_path.encode("utf-8"))
        digest.update(file_digest(file_path).encode("ascii"))
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields = list(rows[0])
    if any(list(row) != fields for row in rows):
        raise ValueError(f"inconsistent fields: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def relative(path: Path) -> str:
    return path.relative_to(POST).as_posix()


def validation_row(
    validation_id: str,
    check: str,
    passed: bool,
    actual: Any,
    expected: Any,
) -> dict[str, Any]:
    return {
        "validation_id": validation_id,
        "check": check,
        "passed": bool(passed),
        "actual": actual,
        "expected": expected,
        "checkpoint_marker": MARKER,
    }


def symbolic_contract() -> dict[str, Any]:
    eigenvalues = sp.symbols("lambda_0:4", real=True)
    c2, c3, generating = sp.symbols("c2 c3 t", real=True)
    t1 = sum(eigenvalues)
    t2 = sum(value**2 for value in eigenvalues)
    t3 = sum(value**3 for value in eigenvalues)
    moment2 = sp.expand(t1**2 + 2 * t2)
    moment3 = sp.expand(t1**3 + 6 * t1 * t2 + 8 * t3)
    generating_function = sp.prod(
        (1 - 2 * generating * value) ** sp.Rational(-1, 2)
        for value in eigenvalues
    )
    generated_moment2 = sp.simplify(
        sp.diff(generating_function, generating, 2).subs(generating, 0)
    )
    generated_moment3 = sp.simplify(
        sp.diff(generating_function, generating, 3).subs(generating, 0)
    )

    interaction_density = c2 * moment2 + c3 * moment3
    kinetic_eigenvalues = [
        sp.expand(
            1
            + 4 * c2 * (t1 + 2 * value)
            + 6
            * c3
            * (
                t1**2
                + 2 * t2
                + 4 * t1 * value
                + 8 * value**2
            )
        )
        for value in eigenvalues
    ]
    derivative_eigenvalues = [
        sp.simplify(
            1 + 2 * sp.diff(interaction_density, value)
        )
        for value in eigenvalues
    ]

    trace_theta2 = sp.simplify(
        4 * t1**2
        + 8 * t2
        - MATRIX_DIMENSION * moment2
    )
    trace_theta3 = sp.simplify(
        (6 * t1**2 + 12 * t2) * t1
        + 24 * t1 * t2
        + 48 * t3
        - MATRIX_DIMENSION * moment3
    )
    return {
        "t1": str(t1),
        "t2": str(t2),
        "t3": str(t3),
        "M2": str(moment2),
        "M3": str(moment3),
        "generating_M2_identity": sp.simplify(
            generated_moment2 - moment2
        )
        == 0,
        "generating_M3_identity": sp.simplify(
            generated_moment3 - moment3
        )
        == 0,
        "kinetic_derivative_identity": all(
            sp.simplify(first - second) == 0
            for first, second in zip(
                kinetic_eigenvalues,
                derivative_eigenvalues,
            )
        ),
        "theta2_trace": str(trace_theta2),
        "theta3_trace": str(trace_theta3),
        "theta2_trace_zero": trace_theta2 == 0,
        "theta3_trace_equals_2M3": sp.simplify(
            trace_theta3 - 2 * moment3
        )
        == 0,
    }


def interaction_density(
    inverse_metric: np.ndarray,
    covariance: np.ndarray,
    c2: float,
    c3: float,
) -> complex | float:
    mixed = inverse_metric @ covariance
    t1 = np.trace(mixed)
    t2 = np.trace(mixed @ mixed)
    t3 = np.trace(mixed @ mixed @ mixed)
    moment2 = t1**2 + 2.0 * t2
    moment3 = t1**3 + 6.0 * t1 * t2 + 8.0 * t3
    return c2 * moment2 + c3 * moment3


def analytic_metric_derivative(
    inverse_metric: np.ndarray,
    covariance: np.ndarray,
    c2: float,
    c3: float,
) -> np.ndarray:
    mixed = inverse_metric @ covariance
    t1 = float(np.trace(mixed))
    t2 = float(np.trace(mixed @ mixed))
    covariance2 = covariance @ inverse_metric @ covariance
    covariance3 = covariance2 @ inverse_metric @ covariance
    return (
        c2 * (2.0 * t1 * covariance + 4.0 * covariance2)
        + c3
        * (
            (3.0 * t1**2 + 6.0 * t2) * covariance
            + 12.0 * t1 * covariance2
            + 24.0 * covariance3
        )
    )


def metric_derivative_crosscheck(samples: int = 5_000) -> dict[str, float]:
    random = np.random.default_rng(5185)
    maximum_relative_residual = 0.0
    maximum_absolute_residual = 0.0
    step = 1.0e-30
    for _ in range(samples):
        matrix = random.normal(size=(MATRIX_DIMENSION, MATRIX_DIMENSION))
        inverse_metric = (
            matrix @ matrix.T + 2.0 * np.eye(MATRIX_DIMENSION)
        )
        covariance_seed = random.normal(
            size=(MATRIX_DIMENSION, MATRIX_DIMENSION)
        )
        covariance = (
            covariance_seed @ covariance_seed.T
            / (4.0 * MATRIX_DIMENSION)
        )
        direction = random.normal(
            size=(MATRIX_DIMENSION, MATRIX_DIMENSION)
        )
        direction = 0.5 * (direction + direction.T)
        direction /= max(1.0, float(np.linalg.norm(direction)))
        coefficient2 = float(random.uniform(-0.2, 0.2))
        coefficient3 = float(random.uniform(-0.1, 0.1))
        complex_value = interaction_density(
            inverse_metric.astype(complex) + 1j * step * direction,
            covariance,
            coefficient2,
            coefficient3,
        )
        numeric = float(np.imag(complex_value) / step)
        analytic = float(
            np.sum(
                analytic_metric_derivative(
                    inverse_metric,
                    covariance,
                    coefficient2,
                    coefficient3,
                )
                * direction
            )
        )
        absolute = abs(numeric - analytic)
        scale = max(1.0, abs(numeric), abs(analytic))
        maximum_absolute_residual = max(maximum_absolute_residual, absolute)
        maximum_relative_residual = max(
            maximum_relative_residual,
            absolute / scale,
        )
    return {
        "samples": samples,
        "finite_difference_step": step,
        "maximum_absolute_residual": maximum_absolute_residual,
        "maximum_relative_residual": maximum_relative_residual,
    }


def basketball_crosscheck(samples: int = 128) -> dict[str, float]:
    random = np.random.default_rng(25185)
    permutations = tuple(itertools.permutations(range(4)))
    maximum_relative_residual = 0.0
    maximum_absolute_residual = 0.0
    for _ in range(samples):
        cross_covariance = random.normal(
            size=(MATRIX_DIMENSION, MATRIX_DIMENSION)
        )
        explicit = 0.0
        for first, second, third, fourth in itertools.product(
            range(MATRIX_DIMENSION),
            repeat=4,
        ):
            x_legs = (first, first, second, second)
            y_legs = (third, third, fourth, fourth)
            for permutation in permutations:
                product = 1.0
                for index in range(4):
                    product *= cross_covariance[
                        x_legs[index],
                        y_legs[permutation[index]],
                    ]
                explicit += product
        matrix = cross_covariance @ cross_covariance.T
        invariant2 = float(np.trace(matrix))
        invariant4 = float(np.trace(matrix @ matrix))
        closed = 8.0 * invariant2**2 + 16.0 * invariant4
        absolute = abs(explicit - closed)
        scale = max(1.0, abs(explicit), abs(closed))
        maximum_absolute_residual = max(maximum_absolute_residual, absolute)
        maximum_relative_residual = max(
            maximum_relative_residual,
            absolute / scale,
        )
    return {
        "samples": samples,
        "cross_pairing_count": len(permutations),
        "maximum_absolute_residual": maximum_absolute_residual,
        "maximum_relative_residual": maximum_relative_residual,
    }


def load_parent_rows() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    trajectory_path = SOURCES["checkpoint_4958_trajectory"][0]
    amplitude_path = SOURCES["checkpoint_4959_amplitude"][0]
    gram_path = SOURCES["checkpoint_4959_gram"][0]
    gradient_path = SOURCES["checkpoint_5163_gradient"][0]
    masses_path = SOURCES["checkpoint_5157_masses"][0]

    with trajectory_path.open(encoding="utf-8", newline="") as handle:
        trajectory = list(csv.DictReader(handle))
    with amplitude_path.open(encoding="utf-8", newline="") as handle:
        amplitude = list(csv.DictReader(handle))
    with gram_path.open(encoding="utf-8", newline="") as handle:
        gram_rows = list(csv.DictReader(handle))
    with gradient_path.open(encoding="utf-8", newline="") as handle:
        gradients = list(csv.DictReader(handle))
    with masses_path.open(encoding="utf-8", newline="") as handle:
        masses = list(csv.DictReader(handle))

    endpoints = [
        row
        for row in trajectory
        if row["polynomial_order"] == "8" and row["sample_index"] == "120"
    ]
    amplitude_endpoints = {
        row["scheme"]: row
        for row in amplitude
        if row["polynomial_order"] == "8"
    }
    o2_gram_norm = float(
        next(
            row
            for row in gram_rows
            if row["row_projector"] == "O2_covariant"
            and row["column_projector"] == "O2_covariant"
        )["mean_product"]
    )
    coefficient_rows: list[dict[str, Any]] = []
    maximum_source_match_residual = 0.0
    for endpoint in endpoints:
        scheme = endpoint["scheme"]
        scheme_gradients = [
            row for row in gradients if row["scheme"] == scheme
        ]
        maximum_density = max(
            float(row["target_energy_density_at_Rn_eV4"])
            for row in scheme_gradients
        )
        source_x2_envelope = max(
            float(row["X2_fractional_Hessian_shift_envelope"])
            for row in scheme_gradients
        )
        source_c2 = max(
            float(row["c_ess_abs_eV_minus4"])
            for row in scheme_gradients
        )
        a2_dimensionless = float(endpoint["A2_a_over_g_power"])
        a3_dimensionless = float(endpoint["A3_a_over_g_power"])
        coefficient2 = a2_dimensionless * G_NATURAL_EV_MINUS2**2
        coefficient3 = a3_dimensionless * G_NATURAL_EV_MINUS2**4
        recomputed_source_envelope = (
            8.0 * abs(coefficient2) * maximum_density
        )
        maximum_source_match_residual = max(
            maximum_source_match_residual,
            abs(abs(coefficient2) - source_c2) / source_c2,
            abs(recomputed_source_envelope - source_x2_envelope)
            / source_x2_envelope,
        )
        z2_norm_ceiling = (
            24.0 * abs(coefficient2) * maximum_density
        )
        z3_norm_ceiling = (
            288.0 * abs(coefficient3) * maximum_density**2
        )
        stress2_fraction_ceiling = (
            48.0 * abs(coefficient2) * maximum_density
        )
        stress3_fraction_ceiling = (
            480.0 * abs(coefficient3) * maximum_density**2
        )
        known_sixpoint_kernel = float(
            amplitude_endpoints[scheme][
                "known_X2_X3_O3_O4_kernel_without_O2"
            ]
        )
        minimized_sixpoint_kernel = float(
            amplitude_endpoints[scheme][
                "full_basis_kernel_minimized_over_O2"
            ]
        )
        natural_o2 = float(
            amplitude_endpoints[scheme]["W_O2_optimum_over_g2"]
        )
        g_endpoint = float(amplitude_endpoints[scheme]["g_endpoint"])
        kappa_endpoint = float(
            amplitude_endpoints[scheme]["kappa_16pi_g"]
        )
        o2_order_one_scale = 1.0 / (
            kappa_endpoint
            * g_endpoint**2
            * math.sqrt(o2_gram_norm)
        )
        o2_enhancement = o2_order_one_scale / natural_o2
        total_kinetic_ceiling = z2_norm_ceiling + z3_norm_ceiling
        coefficient_rows.append(
            {
                "scheme": scheme,
                "polynomial_order": 8,
                "A2_endpoint": a2_dimensionless,
                "A3_endpoint": a3_dimensionless,
                "c2_eV_minus4": coefficient2,
                "c3_eV_minus8": coefficient3,
                "maximum_transition_energy_density_eV4": maximum_density,
                "source_X2_fractional_Hessian_envelope": (
                    source_x2_envelope
                ),
                "generic_Z2_operator_norm_ceiling": z2_norm_ceiling,
                "generic_Z3_operator_norm_ceiling": z3_norm_ceiling,
                "total_interaction_Z_norm_ceiling": total_kinetic_ceiling,
                "Hartree_T2_fraction_ceiling": stress2_fraction_ceiling,
                "Hartree_T3_fraction_ceiling": stress3_fraction_ceiling,
                "relative_to_required_transition_fraction": (
                    total_kinetic_ceiling / REQUIRED_TRANSITION_FRACTION
                ),
                "known_sixpoint_kernel_without_O2": known_sixpoint_kernel,
                "minimized_sixpoint_kernel_over_O2": (
                    minimized_sixpoint_kernel
                ),
                "natural_O2_W_over_g2_reference": natural_o2,
                "O2_projector_Gram_norm": o2_gram_norm,
                "O2_W_over_g2_for_unit_O2_only_Gram_kernel": (
                    o2_order_one_scale
                ),
                "O2_enhancement_over_natural_reference": o2_enhancement,
                "controlled_order_one_interaction": False,
                "source_path": (
                    f"{relative(trajectory_path)};"
                    f"{relative(gradient_path)};"
                    f"{relative(amplitude_path)};"
                    f"{relative(gram_path)}"
                ),
                "valid_for_claim": False,
            }
        )

    time_rows: list[dict[str, Any]] = []
    for coefficient_row in coefficient_rows:
        coefficient2_abs = abs(float(coefficient_row["c2_eV_minus4"]))
        density = float(
            coefficient_row["maximum_transition_energy_density_eV4"]
        )
        epsilon = float(
            coefficient_row["total_interaction_Z_norm_ceiling"]
        )
        for mass_row in masses:
            mass = float(mass_row["m_gap_eV"])
            coherent_phase_ceiling = (
                epsilon
                * mass
                * HBAR_RATE_PER_EV_S
                * EXPOSURE_SECONDS
            )
            log10_cross_section_eV_minus2 = (
                math.log10(256.0 / math.pi)
                + 2.0 * math.log10(coefficient2_abs)
                + 6.0 * math.log10(mass)
            )
            log10_cross_section_m2 = (
                log10_cross_section_eV_minus2
                + 2.0 * math.log10(HBAR_C_EV_M)
            )
            log10_collision_rate_s_minus1 = (
                math.log10(density / mass)
                + log10_cross_section_eV_minus2
                + math.log10(HBAR_RATE_PER_EV_S)
            )
            log10_collision_exposure = (
                log10_collision_rate_s_minus1
                + math.log10(EXPOSURE_SECONDS)
            )
            time_rows.append(
                {
                    "scheme": coefficient_row["scheme"],
                    "mass_label": mass_row["mass_label"],
                    "m_gap_eV": mass,
                    "exposure_seconds": EXPOSURE_SECONDS,
                    "interaction_Z_norm_ceiling": epsilon,
                    "coherent_Duhamel_phase_ceiling": (
                        coherent_phase_ceiling
                    ),
                    "log10_sigma_2to2_ceiling_eV_minus2": (
                        log10_cross_section_eV_minus2
                    ),
                    "log10_sigma_2to2_ceiling_m2": (
                        log10_cross_section_m2
                    ),
                    "log10_collision_rate_ceiling_s_minus1": (
                        log10_collision_rate_s_minus1
                    ),
                    "log10_collisions_per_particle_exposure": (
                        log10_collision_exposure
                    ),
                    "velocity_used_for_rate_ceiling": 1.0,
                    "order_one_redistribution_possible": False,
                    "source_path": (
                        f"{relative(gradient_path)};"
                        f"{relative(masses_path)}"
                    ),
                    "valid_for_claim": False,
                }
            )

    metrics = {
        "endpoint_count": len(endpoints),
        "mass_count": len(masses),
        "maximum_source_reproduction_relative_residual": (
            maximum_source_match_residual
        ),
        "maximum_interaction_Z_norm_ceiling": max(
            float(row["total_interaction_Z_norm_ceiling"])
            for row in coefficient_rows
        ),
        "maximum_Hartree_stress_fraction_ceiling": max(
            float(row["Hartree_T2_fraction_ceiling"])
            + float(row["Hartree_T3_fraction_ceiling"])
            for row in coefficient_rows
        ),
        "maximum_coherent_phase_ceiling": max(
            float(row["coherent_Duhamel_phase_ceiling"])
            for row in time_rows
        ),
        "maximum_log10_collision_exposure": max(
            float(row["log10_collisions_per_particle_exposure"])
            for row in time_rows
        ),
        "minimum_O2_order_one_proxy": min(
            float(row["O2_W_over_g2_for_unit_O2_only_Gram_kernel"])
            for row in coefficient_rows
        ),
        "minimum_O2_enhancement_over_natural": min(
            float(row["O2_enhancement_over_natural_reference"])
            for row in coefficient_rows
        ),
    }
    return coefficient_rows, time_rows, metrics


def build_theory_rows() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    source_4958 = relative(SOURCES["checkpoint_4958_document"][0])
    source_4959 = relative(SOURCES["checkpoint_4959_document"][0])
    source_4960 = relative(SOURCES["checkpoint_4960_document"][0])
    source_4982 = relative(SOURCES["checkpoint_4982_document"][0])
    source_5151 = relative(SOURCES["checkpoint_5151_document"][0])
    source_5158 = relative(SOURCES["checkpoint_5158_document"][0])
    source_5163 = relative(SOURCES["checkpoint_5163_document"][0])
    source_5170 = relative(SOURCES["checkpoint_5170_document"][0])
    source_5171 = relative(SOURCES["checkpoint_5171_document"][0])
    source_5177 = relative(SOURCES["checkpoint_5177_document"][0])
    source_5184 = relative(SOURCES["checkpoint_5184_document"][0])

    hartree_rows = [
        {
            "object": "finite_state_gradient_covariance",
            "formula": (
                "C_mn=[nabla_m nabla_nprime F_state(x,xprime)]_coincidence"
            ),
            "derivation": "Hadamard/vacuum-subtracted occupied two-point state",
            "local_or_nonlocal": "local coincidence tensor",
            "new_beyond_free_Vlasov": False,
            "conservation_role": "state input",
            "source_path": source_5151,
            "valid_for_claim": False,
        },
        {
            "object": "Gaussian_X2_moment",
            "formula": "<X^2>=t1^2+2 t2",
            "derivation": "exact Wick/cumulant identity; t_n=Tr[(g^-1 C)^n]",
            "local_or_nonlocal": "local",
            "new_beyond_free_Vlasov": True,
            "conservation_role": "first X2 2PI Hartree density",
            "source_path": f"{source_4958};{source_4982}",
            "valid_for_claim": False,
        },
        {
            "object": "Gaussian_X3_moment",
            "formula": "<X^3>=t1^3+6 t1 t2+8 t3",
            "derivation": "exact Wick/cumulant identity",
            "local_or_nonlocal": "local",
            "new_beyond_free_Vlasov": True,
            "conservation_role": "first X3 2PI Hartree density",
            "source_path": f"{source_4958};{source_4982}",
            "valid_for_claim": False,
        },
        {
            "object": "Hartree_interaction_density",
            "formula": "L_H=c2(t1^2+2t2)+c3(t1^3+6t1t2+8t3)",
            "derivation": "first 2PI skeletons evaluated on Gaussian F_state",
            "local_or_nonlocal": "local",
            "new_beyond_free_Vlasov": True,
            "conservation_role": "metric and gap variations use same functional",
            "source_path": f"{source_4958};{source_4982}",
            "valid_for_claim": False,
        },
        {
            "object": "Hartree_X2_Hilbert_stress",
            "formula": (
                "Theta2_mn=c2[4t1 C1_mn+8C2_mn-"
                "g_mn(t1^2+2t2)]"
            ),
            "derivation": "2 delta L_H/delta g^mn-g_mn L_H at fixed C",
            "local_or_nonlocal": "local",
            "new_beyond_free_Vlasov": True,
            "conservation_role": "trace zero in four dimensions",
            "source_path": source_4982,
            "valid_for_claim": False,
        },
        {
            "object": "Hartree_X3_Hilbert_stress",
            "formula": (
                "Theta3_mn=c3[(6t1^2+12t2)C1_mn+24t1C2_mn+"
                "48C3_mn-g_mn(t1^3+6t1t2+8t3)]"
            ),
            "derivation": "2 delta L_H/delta g^mn-g_mn L_H at fixed C",
            "local_or_nonlocal": "local",
            "new_beyond_free_Vlasov": True,
            "conservation_role": "trace=2c3<X^3> in four dimensions",
            "source_path": source_4982,
            "valid_for_claim": False,
        },
        {
            "object": "Hartree_gap_kinetic_tensor",
            "formula": (
                "Z_H^mn=g^mn+4c2[t1g^mn+2C^mn]+"
                "6c3[(t1^2+2t2)g^mn+4t1C^mn+8(C2)^mn]"
            ),
            "derivation": "g^mn+2 delta L_H/delta C_mn",
            "local_or_nonlocal": "local",
            "new_beyond_free_Vlasov": True,
            "conservation_role": "same Phi-derivable Hartree packet as stress",
            "source_path": f"{source_4958};{source_4982}",
            "valid_for_claim": False,
        },
    ]

    basketball_rows = [
        {
            "topology": "X2_X2_all_cross_basketball",
            "order": "c2^2",
            "cross_covariance": (
                "D_mnprime=nabla_m^x nabla_nprime^y G(x,y)"
            ),
            "invariants": (
                "I2=Tr[g_x^-1 D g_y^-1 D^T]; "
                "I4=Tr[(g_x^-1 D g_y^-1 D^T)^2]"
            ),
            "all_cross_Wick_polynomial": "8 I2^2+16 I4",
            "Euclidean_cumulant_coefficient": (
                "-4 c2^2 integral_xy [I2^2+2 I4]"
            ),
            "CTP_role": "nonlocal self-energy and 2to2 collision kernel",
            "compensated_zero_mode": (
                "energy-momentum zero mode from translation/diffeomorphism Ward"
            ),
            "status": "DERIVED_TOPOLOGY_SIGN_CONTINUED_ON_CTP",
            "source_path": f"{source_4958};{source_4959}",
            "valid_for_claim": False,
        },
        {
            "topology": "X3_and_mixed_sixpoint_collisions",
            "order": "c3^2, c2-c3 exchange and curvature completions",
            "cross_covariance": "six-line and exchange 2PI skeletons",
            "invariants": "complete on-shell five-projector amplitude at 4959",
            "all_cross_Wick_polynomial": "higher Gaussian contractions",
            "Euclidean_cumulant_coefficient": "fixed by full parent vertices",
            "CTP_role": "2to4 and inverse number-changing collision kernels",
            "compensated_zero_mode": (
                "four-momentum conserved; particle number need not be"
            ),
            "status": "KNOWN_SECTOR_NONZERO_O2_COEFFICIENT_SEPARATE",
            "source_path": source_4959,
            "valid_for_claim": False,
        },
    ]

    ward_rows = [
        {
            "clause": "2PI_parent_functional",
            "equation": (
                "Gamma=S+1/2 Tr ln G^-1+1/2 Tr D^-1G+Gamma2+Gamma_ct"
            ),
            "consequence": "one functional owns free and interaction stress",
            "gate": "DERIVED_STANDARD_CTP_STRUCTURE",
            "source_path": f"{source_4958};{source_5151}",
            "valid_for_claim": False,
        },
        {
            "clause": "gap_stationarity",
            "equation": "delta Gamma/delta G=0",
            "consequence": "implicit metric variation of G cancels in T variation",
            "gate": "REQUIRED",
            "source_path": source_5151,
            "valid_for_claim": False,
        },
        {
            "clause": "metric_Ward_identity",
            "equation": (
                "nabla_mu T^mu_nu=0 when mean and gap equations hold"
            ),
            "consequence": "Hartree and collision pieces cannot be tuned separately",
            "gate": "EXACT_FOR_COVARIANT_PHI_DERIVABLE_TRUNCATION",
            "source_path": f"{source_4960};{source_4982}",
            "valid_for_claim": False,
        },
        {
            "clause": "vacuum_subtraction",
            "equation": (
                "Delta Gamma2[F]=Gamma2[G_vac+F]-Gamma2[G_vac]-local_ct"
            ),
            "consequence": "Delta T_int and Delta Pi_int vanish for F=0",
            "gate": "EXACT_STATE_DIFFERENCE",
            "source_path": f"{source_4982};{source_5184}",
            "valid_for_claim": False,
        },
        {
            "clause": "free_Vlasov_piece",
            "equation": "Pi_free=delta T_free[F]/delta g",
            "consequence": "already evolved by 5164-5169 and derived at 5171",
            "gate": "SUBTRACT_DO_NOT_ADD",
            "source_path": source_5171,
            "valid_for_claim": False,
        },
        {
            "clause": "new_interaction_piece",
            "equation": (
                "Pi_new=delta(T_Hartree+T_basketball+T_collision)/delta g"
            ),
            "consequence": "only this difference can be scored as new physics",
            "gate": "RETAIN_FOR_BOUND",
            "source_path": f"{source_4958};{source_4959};{source_5171}",
            "valid_for_claim": False,
        },
        {
            "clause": "Hartree_resolvent",
            "equation": (
                "chi_H=(1-chi0 f_H)^-1 chi0; "
                "Delta chi=chi0 f_H(1-chi0 f_H)^-1 chi0"
            ),
            "consequence": (
                "new response relative to chi0 <=epsilon_H/(1-epsilon_H)"
            ),
            "gate": "EXACT_RESOLVENT_BOUND",
            "source_path": f"{source_5163};{source_5171}",
            "valid_for_claim": False,
        },
        {
            "clause": "compensation",
            "equation": (
                "integral dPi1 p1^nu C_22[f1]=0 from "
                "delta4(p1+p2-p3-p4); C_24 preserves four-momentum too"
            ),
            "consequence": "interaction kernel has correct conserved zero mode",
            "gate": "STRUCTURAL_PASS_MAGNITUDE_SEPARATE",
            "source_path": source_5170,
            "valid_for_claim": False,
        },
    ]

    route_rows = [
        {
            "route": "free_occupied_state_Vlasov_response",
            "derived_structure": "compensated sign-changing kernel",
            "new_relative_to_executed_formation": False,
            "magnitude_gate": "already counted",
            "decision": "FORBID_DOUBLE_COUNT",
            "next_action": "subtract before scoring interactions",
            "source_path": source_5171,
            "valid_for_claim": False,
        },
        {
            "route": "X2_X3_Hartree_state_stress",
            "derived_structure": "local Hilbert stress and local gap tensor",
            "new_relative_to_executed_formation": True,
            "magnitude_gate": "fails by more than 115 orders",
            "decision": "REJECT_AS_PROFILE_REPAIR",
            "next_action": "retain only as negligible controlled correction",
            "source_path": f"{source_4958};{source_5163}",
            "valid_for_claim": False,
        },
        {
            "route": "X2_basketball_and_known_sixpoint_collisions",
            "derived_structure": "nonlocal conserving CTP collision kernel",
            "new_relative_to_executed_formation": True,
            "magnitude_gate": "coherent and collision exposures negligible",
            "decision": "REJECT_KNOWN_LOCAL_INTERACTIONS_AS_REDISTRIBUTION",
            "next_action": "do not fit an interaction rate",
            "source_path": f"{source_4959};{source_5163}",
            "valid_for_claim": False,
        },
        {
            "route": "unknown_O2_coefficient_rescue",
            "derived_structure": "projector shape known but coefficient open",
            "new_relative_to_executed_formation": True,
            "magnitude_gate": "unit O2-only Gram kernel needs W/g2 above 1e29",
            "decision": "NO_CONTROLLED_RESCUE",
            "next_action": "derive later for completeness, not as galaxy patch",
            "source_path": source_4959,
            "valid_for_claim": False,
        },
        {
            "route": "neutral_state_source_selection",
            "derived_structure": (
                "parent time-dependent CTP/Bogoliubov production can populate "
                "neutral occupation without signed U1 charge"
            ),
            "new_relative_to_executed_formation": True,
            "magnitude_gate": "normalization and covariance not yet selected",
            "decision": "SELECT_NEXT_CONSTRUCTIVE_DERIVATION",
            "next_action": (
                "compute beta_k, abundance and covariance for locked masses "
                "without fitting Y_X or C_n"
            ),
            "source_path": f"{source_5151};{source_5158};{source_5177}",
            "valid_for_claim": False,
        },
    ]

    summary = {
        "Gaussian_Hartree_moments_derived": True,
        "Hartree_Hilbert_stress_derived": True,
        "Hartree_gap_tensor_derived": True,
        "X2_basketball_topology_derived": True,
        "metric_Ward_identity_retained": True,
        "vacuum_silence_retained": True,
        "free_Vlasov_double_count_removed": True,
        "known_interaction_profile_repair_viable": False,
        "unknown_O2_controlled_rescue_viable": False,
        "neutral_state_source_selection_retained": True,
        "local_GR_Newton_Maxwell_branch_modified": False,
        "full_MTS_claim": False,
        "next_target": (
            "5186 derive the neutral occupied-state normalization and covariance "
            "from the parent time-dependent CTP/Bogoliubov kernel"
        ),
        "route_decision": ROUTE_DECISION,
    }
    return hartree_rows, basketball_rows, ward_rows, route_rows, summary


def calculate_checks(
    symbolic: dict[str, Any],
    metric_crosscheck: dict[str, float],
    basketball_check: dict[str, float],
    coefficient_rows: list[dict[str, Any]],
    time_rows: list[dict[str, Any]],
    numeric_metrics: dict[str, Any],
    theory_rows: tuple[
        list[dict[str, Any]],
        list[dict[str, Any]],
        list[dict[str, Any]],
        list[dict[str, Any]],
        dict[str, Any],
    ],
    source_hashes: dict[str, str],
    formal_digest: str,
    checkpoint_5176_digest: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    (
        hartree_rows,
        basketball_rows,
        ward_rows,
        route_rows,
        summary,
    ) = theory_rows
    source_hash_match = all(
        source_hashes[name] == expected
        for name, (_, expected) in SOURCES.items()
    )
    checks = [
        validation_row(
            "V5185_01_source_count",
            "all declared sources exist",
            len(source_hashes) == len(SOURCES),
            len(source_hashes),
            len(SOURCES),
        ),
        validation_row(
            "V5185_02_source_locks",
            "all source hashes match read-only locks",
            source_hash_match,
            sum(
                source_hashes[name] == expected
                for name, (_, expected) in SOURCES.items()
            ),
            len(SOURCES),
        ),
        validation_row(
            "V5185_03_formal_lock",
            "formalization-workbench remains locked",
            formal_digest == FORMAL_DIGEST_LOCK,
            formal_digest,
            FORMAL_DIGEST_LOCK,
        ),
        validation_row(
            "V5185_04_5176_lock",
            "checkpoint 5176 ensemble remains locked",
            checkpoint_5176_digest == CHECKPOINT_5176_TREE_LOCK,
            checkpoint_5176_digest,
            CHECKPOINT_5176_TREE_LOCK,
        ),
        validation_row(
            "V5185_05_M2_generating",
            "Gaussian X2 moment matches exact generating function",
            symbolic["generating_M2_identity"],
            symbolic["generating_M2_identity"],
            True,
        ),
        validation_row(
            "V5185_06_M3_generating",
            "Gaussian X3 moment matches exact generating function",
            symbolic["generating_M3_identity"],
            symbolic["generating_M3_identity"],
            True,
        ),
        validation_row(
            "V5185_07_gap_derivative",
            "Hartree gap tensor equals twice covariance derivative",
            symbolic["kinetic_derivative_identity"],
            symbolic["kinetic_derivative_identity"],
            True,
        ),
        validation_row(
            "V5185_08_X2_trace",
            "X2 Hartree stress is trace free in four dimensions",
            symbolic["theta2_trace_zero"],
            symbolic["theta2_trace"],
            "0",
        ),
        validation_row(
            "V5185_09_X3_trace",
            "X3 Hartree stress trace equals 2 c3 M3",
            symbolic["theta3_trace_equals_2M3"],
            symbolic["theta3_trace_equals_2M3"],
            True,
        ),
        validation_row(
            "V5185_10_metric_derivative",
            "finite-difference metric derivative matches closed stress input",
            metric_crosscheck["maximum_relative_residual"] < 2.0e-8,
            metric_crosscheck["maximum_relative_residual"],
            "<2e-8",
        ),
        validation_row(
            "V5185_11_basketball_pairings",
            "all 24 cross pairings equal 8 I2 squared plus 16 I4",
            basketball_check["maximum_relative_residual"] < 2.0e-13,
            basketball_check["maximum_relative_residual"],
            "<2e-13",
        ),
        validation_row(
            "V5185_12_endpoint_count",
            "both N8 parent endpoints are present",
            numeric_metrics["endpoint_count"] == 2,
            numeric_metrics["endpoint_count"],
            2,
        ),
        validation_row(
            "V5185_13_mass_count",
            "all three locked masses are present",
            numeric_metrics["mass_count"] == 3,
            numeric_metrics["mass_count"],
            3,
        ),
        validation_row(
            "V5185_14_source_reproduction",
            "physical c2 reproduces checkpoint-5163 envelope",
            numeric_metrics[
                "maximum_source_reproduction_relative_residual"
            ]
            < 2.0e-15,
            numeric_metrics[
                "maximum_source_reproduction_relative_residual"
            ],
            "<2e-15",
        ),
        validation_row(
            "V5185_15_Z_norm",
            "total known interaction gap correction is below 4e-116",
            numeric_metrics["maximum_interaction_Z_norm_ceiling"]
            < 4.0e-116,
            numeric_metrics["maximum_interaction_Z_norm_ceiling"],
            "<4e-116",
        ),
        validation_row(
            "V5185_16_stress_norm",
            "total known Hartree stress fraction is below 8e-116",
            numeric_metrics["maximum_Hartree_stress_fraction_ceiling"]
            < 8.0e-116,
            numeric_metrics["maximum_Hartree_stress_fraction_ceiling"],
            "<8e-116",
        ),
        validation_row(
            "V5185_17_coherent_phase",
            "generous 1e18 s coherent interaction phase is below 6e-101",
            numeric_metrics["maximum_coherent_phase_ceiling"] < 6.0e-101,
            numeric_metrics["maximum_coherent_phase_ceiling"],
            "<6e-101",
        ),
        validation_row(
            "V5185_18_collision_exposure",
            "largest conservative 2to2 collision exposure is below 1e-281",
            numeric_metrics["maximum_log10_collision_exposure"] < -281.0,
            numeric_metrics["maximum_log10_collision_exposure"],
            "<-281",
        ),
        validation_row(
            "V5185_19_O2_uncontrolled",
            "unit O2-only Gram kernel requires W/g2 above 1e29",
            numeric_metrics["minimum_O2_order_one_proxy"] > 1.0e29
            and numeric_metrics["minimum_O2_enhancement_over_natural"]
            > 1.0e28,
            (
                numeric_metrics["minimum_O2_order_one_proxy"],
                numeric_metrics["minimum_O2_enhancement_over_natural"],
            ),
            "(>1e29,>1e28)",
        ),
        validation_row(
            "V5185_20_Hartree_rows",
            "all exact Hartree objects are recorded",
            len(hartree_rows) == 7,
            len(hartree_rows),
            7,
        ),
        validation_row(
            "V5185_21_basketball_rows",
            "nonlocal interaction topologies are recorded",
            len(basketball_rows) == 2,
            len(basketball_rows),
            2,
        ),
        validation_row(
            "V5185_22_Ward_rows",
            "Ward, vacuum and subtraction clauses are recorded",
            len(ward_rows) == 8,
            len(ward_rows),
            8,
        ),
        validation_row(
            "V5185_23_Vlasov_subtraction",
            "free Vlasov response is explicitly forbidden from double count",
            any(
                row["decision"] == "FORBID_DOUBLE_COUNT"
                for row in route_rows
            ),
            True,
            True,
        ),
        validation_row(
            "V5185_24_next_route",
            "neutral state source selection is selected next",
            any(
                row["decision"] == "SELECT_NEXT_CONSTRUCTIVE_DERIVATION"
                for row in route_rows
            ),
            True,
            True,
        ),
        validation_row(
            "V5185_25_local_branch",
            "local GR/Newton/Maxwell branch remains unchanged",
            not summary["local_GR_Newton_Maxwell_branch_modified"],
            summary["local_GR_Newton_Maxwell_branch_modified"],
            False,
        ),
        validation_row(
            "V5185_26_no_claim",
            "no full-MTS claim is made",
            not summary["full_MTS_claim"],
            summary["full_MTS_claim"],
            False,
        ),
    ]
    metrics = {
        "symbolic": symbolic,
        "metric_derivative_crosscheck": metric_crosscheck,
        "basketball_crosscheck": basketball_check,
        "physical_bounds": numeric_metrics,
    }
    return checks, metrics


def write_document(result: dict[str, Any]) -> None:
    metrics = result["metrics"]
    physical = metrics["physical_bounds"]
    coefficients = result["coefficient_rows"]
    dynamic = next(
        row for row in coefficients if row["scheme"] == "dynamic_etaN"
    )
    reference = next(
        row for row in coefficients if row["scheme"] == "reference_etaN0"
    )
    text = f"""# 5185 - Occupied-state 2PI interaction stress and collision gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

Checkpoint 5184 rejected a regular classical stationary motion background but
left the occupied two-point state alive. Checkpoint 5185 now derives the
interaction stress of that state from the parent-owned essential `X^2/X^3`
vertices. It does not write down a phenomenological response kernel.

```text
{ROUTE_DECISION}
```

The outcome has one structural success and one quantitative failure:

```text
Ward-conserving, vacuum-silent interaction stress = derived;
strength needed for galactic redistribution       = absent by >100 orders.
```

## 1. State variable and renormalized scope

Let the finite occupied-state gradient covariance be

```text
C_mn(x)
 =[nabla_m nabla_n' F_state(x,x')]_(x'=x),

A^m_n=g^ma C_an,
t_n=Tr(A^n).
```

`C_mn` is the Hadamard/vacuum-subtracted finite state part. Other covariant
subtraction schemes differ by local vacuum counterterms already assigned to
the parent `P(X)` trajectory. The state-dependent functional is

```text
Delta Gamma_2[F]
 =Gamma_2[G_vac+F]-Gamma_2[G_vac]-local counterterms,
```

so every state interaction contribution vanishes exactly when `F=0`. The
checkpoint-4960 local GR/Newton/Maxwell vacuum is therefore not reopened.

## 2. Exact Gaussian Hartree functional

For a Gaussian reflection-even state, the moment-generating function gives

```text
<X^2> = M2 = t1^2+2t2,

<X^3> = M3 = t1^3+6t1t2+8t3.
```

The first 2PI/Hartree interaction density is therefore

```text
L_H
 =c2(t1^2+2t2)
  +c3(t1^3+6t1t2+8t3),

c2=A2 G_N^2,
c3=A3 G_N^4.
```

This is an action result, not an equation-of-state ansatz.

## 3. Exact Hilbert stress

Define

```text
C1_mn=C_mn,
C2_mn=C_ma g^ab C_bn,
C3_mn=C_ma g^ab C_bc g^cd C_dn.
```

At a stationary 2PI propagator, the implicit metric variation of `G` drops
out. Explicit variation gives

```text
Theta2_mn
 =c2[
    4t1 C1_mn
   +8C2_mn
   -g_mn(t1^2+2t2)
   ],

Theta3_mn
 =c3[
    (6t1^2+12t2)C1_mn
   +24t1C2_mn
   +48C3_mn
   -g_mn(t1^3+6t1t2+8t3)
   ].
```

Two exact algebraic checks are useful:

```text
Theta2^m_m=0,
Theta3^m_m=2c3 M3
```

in four dimensions. A `{int(metrics["metric_derivative_crosscheck"]["samples"])}`-
sample independent directional finite-difference test gives maximum relative
residual
`{metrics["metric_derivative_crosscheck"]["maximum_relative_residual"]:.3e}`.

## 4. Exact Hartree gap tensor

The same functional, varied with respect to `C_mn`, gives

```text
Z_H^mn
 =g^mn
  +4c2[t1g^mn+2C^mn]
  +6c3[
      (t1^2+2t2)g^mn
     +4t1C^mn
     +8(C2)^mn
     ].
```

Thus the Hartree stress and state propagation are not independently tunable.
The packet is local in the coincidence covariance. Its direct metric Hessian
is a contact term. Its indirect response dresses the free susceptibility:

```text
chi_H=(1-chi0 f_H)^-1 chi0,

Delta chi
 =chi_H-chi0
 =chi0 f_H(1-chi0 f_H)^-1 chi0.
```

Checkpoint 5171 already derived and evolved `chi0`, the classical Vlasov
piece. Only `Delta chi` is new.

## 5. First genuinely nonlocal 2PI topology

For the `X^2-X^2` basketball define

```text
D_mn'(x,y)=nabla_m^x nabla_n'^y G(x,y),

I2=Tr[g_x^-1 D g_y^-1 D^T],

I4=Tr[(g_x^-1 D g_y^-1 D^T)^2].
```

The 24 Wick contractions in which all four lines cross between the two
vertices sum exactly to

```text
8 I2^2+16 I4.
```

The Euclidean cumulant magnitude is therefore

```text
Gamma_2,basketball
 =-4c2^2 integral_(x,y)[I2^2+2I4],
```

with the retarded/noise components obtained by the standard CTP continuation.
This is the first genuinely nonlocal self-energy and `2<->2` collision
kernel. The explicit combinatorial check over
`{int(metrics["basketball_crosscheck"]["samples"])}` random cross-covariances
has maximum relative residual
`{metrics["basketball_crosscheck"]["maximum_relative_residual"]:.3e}`.

The `X^3`, `X^2` exchange and curvature-completed six-point vertices similarly
generate `2<->4` and inverse collision kernels. Checkpoint 4959 already proves
that their known amplitude is nonzero.

## 6. Ward identity, compensation and double counting

A covariant Phi-derivable 2PI truncation satisfies

```text
delta Gamma/delta G=0,
delta Gamma/delta <psi>=0

 => nabla_mu T^mu_nu=0.
```

The collision kernel therefore has the correct energy-momentum zero mode and
can in principle produce a compensated redistribution. This is a real
structural hit.

Explicitly, its `2<->2` projection has the standard parent-amplitude form

```text
C_22[f1]
 =integral dPi_234
   delta^4(p1+p2-p3-p4)|M_22|^2
   [f3f4(1+f1)(1+f2)-f1f2(1+f3)(1+f4)].
```

Multiplication by `p1^nu`, integration over `p1`, and relabelling incoming
and outgoing legs gives

```text
integral dPi_1 p1^nu C_22[f1]=0
```

exactly because the four-momentum delta function sets
`p1+p2-p3-p4=0`. The `2<->4` channel does not conserve particle number, but
the same argument conserves total four-momentum. The required compensation
is therefore structurally available; only its rate remains to be tested.

It does not authorize adding the checkpoint-5171 kernel again:

```text
Pi_total=Pi_free/Vlasov+Pi_Hartree+Pi_basketball+Pi_collision,

Pi_new=Pi_total-Pi_free/Vlasov.
```

The free term was already evolved nonlinearly in checkpoints 5164--5169.
Scoring it twice would be a false improvement.

## 7. Source-locked physical size

The endpoint coefficients and conservative four-dimensional covariance-norm
bounds are:

| scheme | `c2` (`eV^-4`) | `c3` (`eV^-8`) | `||delta Z||` ceiling |
|---|---:|---:|---:|
| dynamic `eta_N` | {dynamic["c2_eV_minus4"]:.15e} | {dynamic["c3_eV_minus8"]:.15e} | {dynamic["total_interaction_Z_norm_ceiling"]:.15e} |
| reference `eta_N=0` | {reference["c2_eV_minus4"]:.15e} | {reference["c3_eV_minus8"]:.15e} | {reference["total_interaction_Z_norm_ceiling"]:.15e} |

The bounds use

```text
||delta Z_X2|| <=24 |c2| rho,
||delta Z_X3|| <=288|c3|rho^2,

||Theta_X2||/rho <=48|c2|rho,
||Theta_X3||/rho <=480|c3|rho^2.
```

The maximum source-locked results are

```text
interaction kinetic norm ceiling
 ={physical["maximum_interaction_Z_norm_ceiling"]:.15e},

Hartree stress fraction ceiling
 ={physical["maximum_Hartree_stress_fraction_ceiling"]:.15e},

required transition correction
 ={REQUIRED_TRANSITION_FRACTION:.15e}.
```

The `X^2` calculation independently reproduces the checkpoint-5163
`8|c2|rho` envelope with maximum relative residual
`{physical["maximum_source_reproduction_relative_residual"]:.3e}`.

The exact resolvent inequality gives

```text
||Delta chi||/||chi0||
 <=epsilon_H/(1-epsilon_H),
```

which is numerically the same tiny order. The interaction has the right
conservation structure but cannot generate the required profile amplitude.

## 8. Time accumulation and collision bound

To avoid dismissing a small instantaneous term that might accumulate, use the
deliberately generous exposure

```text
T=1e18 s,
omega_max=m_gap/hbar.
```

The Duhamel interaction phase ceiling is

```text
epsilon_H omega_max T
 <={physical["maximum_coherent_phase_ceiling"]:.15e}
```

across all three locked masses. Galactic orbital frequencies are much smaller
than `m_gap/hbar`, so this overstates rather than understates the available
evolution.

An independent particle estimate uses the conservative derivative-amplitude
bound

```text
|M_2to2|<=64|c2|m^4,

sigma_2to2
 <=(256/pi)c2^2 m^6,

Gamma<= (rho/m) sigma v,
v<=1.
```

The largest exposure is

```text
log10(N_collisions per particle)
 <={physical["maximum_log10_collision_exposure"]:.15f}.
```

This is not a marginal failure. Neither coherent Bose-enhanced mean-field
evolution nor incoherent two-body scattering can move an order-one fraction
of the state.

## 9. The open O2 coefficient is not a controlled rescue

Checkpoint 4959 leaves the `O2` momentum coefficient as a separate flow
calculation. Its natural co-leading reference is `W_O2/g^2` near `2.85`.
The directly measured `O2` projector Gram norm gives the exact coefficient
needed for a unit **O2-only** integrated kernel:

```text
W_O2/g^2
 ~{physical["minimum_O2_order_one_proxy"]:.15e}.
```

The minimum enhancement over the natural co-leading reference is
`{physical["minimum_O2_enhancement_over_natural"]:.15e}`. That is more than
28 orders and would destroy the perturbative derivative hierarchy. The exact
`O2` flow remains useful for theory completeness, but it is not a controlled
galaxy rescue and is not promoted here.

## 10. Route decision and next derivation

```text
Gaussian Hartree moments and stress               = derived;
Hartree gap tensor                                = derived;
X2 nonlocal basketball topology                   = derived;
Ward conservation and compensated zero mode       = retained;
vacuum silence                                    = exact state difference;
free Vlasov susceptibility                        = subtracted as already counted;
known X2/X3 interaction strength                   = decisively insufficient;
unknown O2 as controlled rescue                    = rejected;
local GR/Newton/Maxwell zero state                 = retained;
galaxy or full-MTS claim                           = false.
```

The next constructive target is checkpoint 5186: derive the neutral
occupied-state normalization and primordial covariance from the parent's
time-dependent CTP/Bogoliubov kernel. Neutral pair production can populate
total occupation without producing the signed `U(1)` charge rejected at
checkpoint 5157. The calculation must predict `beta_k`, abundance and
covariance for the three locked masses without fitting `Y_X`, `C_n` or a
galaxy profile.

## 11. Audit

All `{result["validation_count"]}` validations pass. Every evidence row
remains `valid_for_claim=false`. The protected `formalization-workbench`
digest remains `{result["formalization_workbench_tree_sha256"]}` and the
checkpoint-5176 ensemble remains
`{result["checkpoint_5176_tree_sha256"]}`. No GitHub action occurred.

Generated files:

- `source-intake/functional_rg/5185/gaussian_2PI_Hartree_moments_stress_and_kinetic_tensor.csv`
- `source-intake/functional_rg/5185/X2_basketball_nonlocal_topology.csv`
- `source-intake/functional_rg/5185/Ward_vacuum_and_Vlasov_subtraction_ledger.csv`
- `source-intake/functional_rg/5185/parent_interaction_physical_bounds.csv`
- `source-intake/functional_rg/5185/interaction_time_and_collision_bounds.csv`
- `source-intake/functional_rg/5185/occupied_state_interaction_route_decision.csv`
- `source-intake/functional_rg/5185/source_provenance.csv`
- `source-intake/functional_rg/5185/occupied_state_2PI_interaction_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5185_VALIDATION.csv`
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def run(dry_run: bool) -> dict[str, Any]:
    missing = [
        name for name, (path, _) in SOURCES.items() if not path.is_file()
    ]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    source_hashes_before = {
        name: file_digest(path) for name, (path, _) in SOURCES.items()
    }
    formal_before = tree_digest(FORMAL)
    checkpoint_5176_before = tree_digest(CHECKPOINT_5176_ROOT)

    symbolic = symbolic_contract()
    metric_crosscheck = metric_derivative_crosscheck()
    basketball_check = basketball_crosscheck()
    coefficient_rows, time_rows, numeric_metrics = load_parent_rows()
    theory_rows = build_theory_rows()
    checks, metrics = calculate_checks(
        symbolic,
        metric_crosscheck,
        basketball_check,
        coefficient_rows,
        time_rows,
        numeric_metrics,
        theory_rows,
        source_hashes_before,
        formal_before,
        checkpoint_5176_before,
    )
    failures = [row["validation_id"] for row in checks if not row["passed"]]
    (
        hartree_rows,
        basketball_rows,
        ward_rows,
        route_rows,
        summary,
    ) = theory_rows
    dry_result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "dry_run": dry_run,
        "route_decision": ROUTE_DECISION,
        "metrics": metrics,
        "summary": summary,
        "coefficient_rows": coefficient_rows,
        "validation_count": len(checks),
        "validation_failures": failures,
    }
    if failures:
        raise RuntimeError(f"dry validation failures: {failures}")
    if dry_run:
        return dry_result

    write_csv(HARTREE_CSV, hartree_rows)
    write_csv(BASKETBALL_CSV, basketball_rows)
    write_csv(WARD_CSV, ward_rows)
    write_csv(COEFFICIENT_CSV, coefficient_rows)
    write_csv(TIME_CSV, time_rows)
    write_csv(ROUTE_CSV, route_rows)
    provenance_rows = [
        {
            "source_id": name,
            "source_path": str(path),
            "sha256": source_hashes_before[name],
            "expected_sha256": expected,
            "status": "hash_locked_read_only",
            "checked_date": CHECKED_DATE,
        }
        for name, (path, expected) in SOURCES.items()
    ]
    write_csv(PROVENANCE_CSV, provenance_rows)

    source_hashes_after = {
        name: file_digest(path) for name, (path, _) in SOURCES.items()
    }
    formal_after = tree_digest(FORMAL)
    checkpoint_5176_after = tree_digest(CHECKPOINT_5176_ROOT)
    output_tables = (
        HARTREE_CSV,
        BASKETBALL_CSV,
        WARD_CSV,
        COEFFICIENT_CSV,
        TIME_CSV,
        ROUTE_CSV,
        PROVENANCE_CSV,
    )
    output_text = "\n".join(
        path.read_text(encoding="utf-8") for path in output_tables
    )
    output_digest = hashlib.sha256(output_text.encode("utf-8")).hexdigest()
    full_checks = checks + [
        validation_row(
            "V5185_27_sources_read_only",
            "all source hashes remain unchanged",
            source_hashes_before == source_hashes_after,
            sum(
                source_hashes_before[name] == source_hashes_after[name]
                for name in SOURCES
            ),
            len(SOURCES),
        ),
        validation_row(
            "V5185_28_formal_after",
            "formalization-workbench remains unchanged",
            formal_after == formal_before == FORMAL_DIGEST_LOCK,
            formal_after,
            FORMAL_DIGEST_LOCK,
        ),
        validation_row(
            "V5185_29_5176_after",
            "checkpoint 5176 remains immutable",
            checkpoint_5176_after
            == checkpoint_5176_before
            == CHECKPOINT_5176_TREE_LOCK,
            checkpoint_5176_after,
            CHECKPOINT_5176_TREE_LOCK,
        ),
        validation_row(
            "V5185_30_no_placeholders",
            "generated evidence contains no missing-input placeholder",
            "MISSING_" not in output_text,
            "MISSING_" in output_text,
            False,
        ),
        validation_row(
            "V5185_31_provenance_rows",
            "every source has one provenance row",
            len(provenance_rows) == len(SOURCES),
            len(provenance_rows),
            len(SOURCES),
        ),
        validation_row(
            "V5185_32_output_parse",
            "all output CSVs parse with nonempty rows",
            all(
                len(list(csv.DictReader(path.open(encoding="utf-8")))) > 0
                for path in output_tables
            ),
            len(output_tables),
            len(output_tables),
        ),
        validation_row(
            "V5185_33_claim_columns",
            "every evidence row remains nonclaim",
            all(
                str(row["valid_for_claim"]).lower() == "false"
                for table in (
                    hartree_rows,
                    basketball_rows,
                    ward_rows,
                    coefficient_rows,
                    time_rows,
                    route_rows,
                )
                for row in table
            ),
            False,
            False,
        ),
        validation_row(
            "V5185_34_local_branch_unchanged",
            "local GR/Newton/Maxwell branch is unchanged",
            not summary["local_GR_Newton_Maxwell_branch_modified"],
            summary["local_GR_Newton_Maxwell_branch_modified"],
            False,
        ),
    ]
    full_failures = [
        row["validation_id"] for row in full_checks if not row["passed"]
    ]
    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "dry_run": False,
        "route_decision": ROUTE_DECISION,
        "source_paths": {
            name: str(path) for name, (path, _) in SOURCES.items()
        },
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "formalization_workbench_tree_sha256": formal_after,
        "checkpoint_5176_tree_sha256": checkpoint_5176_after,
        "output_payload_sha256": output_digest,
        "metrics": metrics,
        "summary": summary,
        "coefficient_rows": coefficient_rows,
        "validation_count": len(full_checks),
        "validation_failures": full_failures,
        "valid_for_local_GR_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_cosmology_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    write_json(RESULT_JSON, result)
    write_document(result)
    write_csv(VALIDATION_CSV, full_checks)
    if full_failures:
        raise RuntimeError(f"validation failures: {full_failures}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Derive the occupied-state 2PI X2/X3 Hartree stress, the first "
            "nonlocal basketball topology, subtract the already-counted "
            "Vlasov response, and bound the physical interaction rate."
        )
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate calculations and source locks without writing outputs",
    )
    arguments = parser.parse_args()
    result = run(arguments.dry_run)
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
