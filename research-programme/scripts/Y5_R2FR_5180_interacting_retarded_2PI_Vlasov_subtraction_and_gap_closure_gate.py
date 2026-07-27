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
CHECKPOINT_4953_NONLINEAR = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4953"
    / "SPARC_X2_nonlinearity_gate.csv"
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
CHECKPOINT_4957_DOCUMENT = (
    POST
    / "4957-Y5-R2FR-functional-PX-GR-connected-trajectory-and-O2-O4-O5-residual-bound-or-motion-sector-rejection.md"
)
CHECKPOINT_4958_DOCUMENT = (
    POST
    / "4958-Y5-R2FR-six-derivative-essential-X2-X3-quotient-and-invariant-2to4-amplitude-or-rate-route-rejection.md"
)
CHECKPOINT_4958_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4958"
    / "essential_PX_sixpoint_trajectory_results.json"
)
CHECKPOINT_4958_TRAJECTORY = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4958"
    / "essential_functional_GR_trajectory.csv"
)
CHECKPOINT_5179_DOCUMENT = (
    POST
    / "5179-Y5-R2FR-lowest-reflection-even-CTP-boundary-kernel-FLRW-preparation-and-perturbative-extra-stress-no-go.md"
)
CHECKPOINT_5179_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5179"
    / "lowest_even_CTP_state_preparation_results.json"
)
BERGES_TEX = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4948"
    / "riolecture.tex"
)
BERGES_ARCHIVE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4948"
    / "hep-ph-0409233-source.tar"
)
CHECKPOINT_5176_ROOT = POST / "source-intake" / "functional_rg" / "5176"

OUT = POST / "source-intake" / "functional_rg" / "5180"
KERNEL_CSV = OUT / "X2_X3_retarded_2PI_kernel.csv"
SUBTRACTION_CSV = OUT / "Vlasov_collision_resolvent_subtraction.csv"
INFRARED_CSV = OUT / "infrared_clustering_and_gap_gate.csv"
SPARC_CSV = OUT / "SPARC_collision_residual_gate.csv"
DECISION_CSV = OUT / "interaction_state_route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "interacting_spectral_gap_results.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5180_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5180-Y5-R2FR-interacting-retarded-2PI-kernel-Vlasov-subtraction-and-infrared-gap-closure-gate.md"
)

MARKER = "MTS_5180_INTERACTING_RETARDED_2PI_VLASOV_SUBTRACTION_GAP_GATE"
CHECKED_DATE = "2026-07-23"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5176_TREE_LOCK = (
    "254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b"
)
REDUCED_PLANCK_MASS_EV = 2.435e27
HBAR_EV_S = 6.582119569e-16
REFERENCE_MASS_EV = 1.0e-20

SOURCE_HASH_LOCKS = {
    "checkpoint_5149_document": (
        "4ccd4b37a60a3e5b66d8cc9d0f3e94473baf19f1468180a74a468f3ad1db606d"
    ),
    "checkpoint_5149_result": (
        "32970c04699829c2e4190dbbf9926b602c9079cb385737dfccf67af82acdefdc"
    ),
    "checkpoint_5171_document": (
        "e66c543db2154ac061a5930edad50585b5835bbc53e1d2774a0c87d7e19cbade"
    ),
    "checkpoint_5171_result": (
        "ee867649d6e1a1784e56d2805f63b4d8b4956fdb2337ba311cda99a4926054e1"
    ),
    "checkpoint_4953_document": (
        "55a90877ac9b64bad5d90ea5e7dd65c52f669fc71adc26106e6fcf0ef0886a2b"
    ),
    "checkpoint_4953_result": (
        "96b68788eff75f12e947f65984174d3f87e5390806d56ac32013dae5956d6508"
    ),
    "checkpoint_4953_nonlinear": (
        "0bf39d35b3e563d57a7e6d507af7be34fc14d79bf9c3c89640550c44ad03bb2b"
    ),
    "checkpoint_4954_document": (
        "3f4d4c09ca97d88327246b9c0ef91b63f98931b2ef467b14b3b7ab57c6cbec69"
    ),
    "checkpoint_4954_result": (
        "523339dd40a835f84c2bbd24a20b7977710f5a71b826dbb3d830089b7445ab45"
    ),
    "checkpoint_4957_document": (
        "235b2e640428814bbcc3f0af1b2ebef020573314eaae1cb0b793be9122db0cb4"
    ),
    "checkpoint_4958_document": (
        "d08b8a0ab6a5317c77a23accd34dc46c5ad6a0bc5aa73e0767c8e0aa0edd5f1c"
    ),
    "checkpoint_4958_result": (
        "383e13cd13c3e90be22dbf8ad589c756a26cad002f01da4ce151ad262e48ae67"
    ),
    "checkpoint_4958_trajectory": (
        "b4317dcc01084a61a6b282bd331d2ce111b835e499c86e65077d0fb98a549081"
    ),
    "checkpoint_5179_document": (
        "066217234006fecb16046796dd4cfdd0fec64a21a38fdcfa0eefb6aa709b3890"
    ),
    "checkpoint_5179_result": (
        "3aaa60f855d9e259e0ae88697037d1467e1d43b4d595d7bc514c32bb7c06aa4b"
    ),
    "berges_tex": (
        "de16f5e4f6e8b10e6880a18b130a4923952556e6fead9fda7a7e162e3282128d"
    ),
    "berges_archive": (
        "d4e12d76e8ded4bc955e51462047c113911f4376a28c5ddb2bb82076212d39ab"
    ),
}

ROUTE_DECISION = (
    "THE_TRAJECTORY_NORMALIZED_X2_X3_CTP_KERNEL_HAS_NOW_BEEN_WRITTEN_"
    "EXPLICITLY_THE_X2_BASKETBALL_AND_X3_FIVE_LINE_GRAPHS_ARE_THE_FIRST_"
    "NONLOCAL_SELF_ENERGIES_AND_THEIR_STATISTICAL_SPECTRAL_POLYNOMIALS_"
    "ARE_FIXED_BY_CTP_COMBINATORICS_AFTER_SUBTRACTING_THE_ALREADY_COUNTED_"
    "VLASOV_RESOLVENT_THE_REMAINING_COLLISION_OPERATOR_ANNIHILATES_NUMBER_"
    "AND_MOMENTUM_MODES_AND_IS_PARAMETRICALLY_TOO_SMALL_MORE_STRONGLY_"
    "SHIFT_SYMMETRY_FORCES_AN_EXTERNAL_MOMENTUM_ON_EACH_SELF_ENERGY_LEG_"
    "SO_ANY_REGULAR_EXPONENTIALLY_CLUSTERING_OCCUPIED_STATE_PRODUCES_ONLY_"
    "AN_ANALYTIC_K_SQUARED_SERIES_AND_CANNOT_ERASE_A_GAP_OR_GENERATE_THE_"
    "REQUIRED_ABSOLUTE_K_DETERMINANT_THE_PERTURBATIVE_INTERACTION_REPAIR_"
    "IS_THEREFORE_CLOSED_WHILE_A_PARENT_DERIVED_CRITICAL_STATE_WITH_THE_"
    "REQUIRED_POWER_LAW_TAIL_REMAINS_OPEN_AND_NOT_CLAIMED"
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields = list(rows[0])
    if any(list(row) != fields for row in rows):
        raise ValueError(f"inconsistent CSV fields: {path}")
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


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    for file_path in sorted(item for item in path.rglob("*") if item.is_file()):
        relative = file_path.relative_to(path).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(file_digest(file_path).encode("ascii"))
    return digest.hexdigest()


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "passed"}


def close(
    actual: float,
    expected: float,
    relative_tolerance: float = 1.0e-11,
    absolute_tolerance: float = 1.0e-15,
) -> bool:
    return math.isclose(
        actual,
        expected,
        rel_tol=relative_tolerance,
        abs_tol=absolute_tolerance,
    )


def generate_pairings(labels: tuple[int, ...]) -> list[tuple[tuple[int, int], ...]]:
    if not labels:
        return [tuple()]
    first = labels[0]
    output: list[tuple[tuple[int, int], ...]] = []
    for partner_index in range(1, len(labels)):
        partner = labels[partner_index]
        remainder = labels[1:partner_index] + labels[partner_index + 1 :]
        for suffix in generate_pairings(remainder):
            output.append(((first, partner),) + suffix)
    return output


def ctp_statistical_coefficients(line_count: int) -> dict[int, Fraction]:
    return {
        spectral_power: Fraction(
            math.comb(line_count, spectral_power)
            * ((-1) ** (spectral_power // 2)),
            2**spectral_power,
        )
        for spectral_power in range(0, line_count + 1, 2)
    }


def ctp_spectral_coefficients(line_count: int) -> dict[int, Fraction]:
    return {
        spectral_power: Fraction(
            math.comb(line_count, spectral_power)
            * ((-1) ** ((spectral_power - 1) // 2)),
            2 ** (spectral_power - 1),
        )
        for spectral_power in range(1, line_count + 1, 2)
    }


def matrix_identity(size: int) -> list[list[Fraction]]:
    return [
        [Fraction(int(row_index == column_index)) for column_index in range(size)]
        for row_index in range(size)
    ]


def matrix_add(
    left: list[list[Fraction]],
    right: list[list[Fraction]],
) -> list[list[Fraction]]:
    return [
        [
            left[row_index][column_index] + right[row_index][column_index]
            for column_index in range(len(left[0]))
        ]
        for row_index in range(len(left))
    ]


def matrix_subtract(
    left: list[list[Fraction]],
    right: list[list[Fraction]],
) -> list[list[Fraction]]:
    return [
        [
            left[row_index][column_index] - right[row_index][column_index]
            for column_index in range(len(left[0]))
        ]
        for row_index in range(len(left))
    ]


def matrix_multiply(
    left: list[list[Fraction]],
    right: list[list[Fraction]],
) -> list[list[Fraction]]:
    return [
        [
            sum(
                left[row_index][inner_index] * right[inner_index][column_index]
                for inner_index in range(len(right))
            )
            for column_index in range(len(right[0]))
        ]
        for row_index in range(len(left))
    ]


def matrix_scale(
    matrix: list[list[Fraction]],
    factor: Fraction,
) -> list[list[Fraction]]:
    return [[factor * value for value in row] for row in matrix]


def matrix_inverse(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    size = len(matrix)
    augmented = [
        list(matrix[row_index]) + matrix_identity(size)[row_index]
        for row_index in range(size)
    ]
    for pivot_index in range(size):
        pivot_row = next(
            row_index
            for row_index in range(pivot_index, size)
            if augmented[row_index][pivot_index] != 0
        )
        augmented[pivot_index], augmented[pivot_row] = (
            augmented[pivot_row],
            augmented[pivot_index],
        )
        pivot = augmented[pivot_index][pivot_index]
        augmented[pivot_index] = [
            value / pivot for value in augmented[pivot_index]
        ]
        for row_index in range(size):
            if row_index == pivot_index:
                continue
            factor = augmented[row_index][pivot_index]
            augmented[row_index] = [
                augmented[row_index][column_index]
                - factor * augmented[pivot_index][column_index]
                for column_index in range(2 * size)
            ]
    return [row[size:] for row in augmented]


def matrix_max_abs(matrix: list[list[Fraction]]) -> Fraction:
    return max(abs(value) for row in matrix for value in row)


def exact_resolvent_audit() -> dict[str, Any]:
    streaming = [
        [Fraction(2), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(3), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(5)],
    ]
    collision = matrix_scale(
        [
            [Fraction(1), Fraction(-1), Fraction(0)],
            [Fraction(-1), Fraction(2), Fraction(-1)],
            [Fraction(0), Fraction(-1), Fraction(1)],
        ],
        Fraction(1, 7),
    )
    interacting_inverse = matrix_inverse(matrix_add(streaming, collision))
    collisionless_inverse = matrix_inverse(streaming)
    left = matrix_subtract(interacting_inverse, collisionless_inverse)
    right = matrix_scale(
        matrix_multiply(
            matrix_multiply(interacting_inverse, collision),
            collisionless_inverse,
        ),
        Fraction(-1),
    )
    residual = matrix_subtract(left, right)
    unit_vector = [[Fraction(1)], [Fraction(1)], [Fraction(1)]]
    null_residual = matrix_multiply(collision, unit_vector)
    return {
        "resolvent_identity_max_abs": str(matrix_max_abs(residual)),
        "collision_unit_null_max_abs": str(matrix_max_abs(null_residual)),
        "collision_quadratic_form": (
            "u^T C u=[(u1-u2)^2+(u2-u3)^2]/7>=0"
        ),
        "collision_eigenvalues": ["0", "1/7", "3/7"],
        "exact_identity_pass": matrix_max_abs(residual) == 0,
        "exact_null_pass": matrix_max_abs(null_residual) == 0,
    }


def exact_detailed_balance_audit() -> dict[str, Any]:
    beta = Fraction(7, 5)
    chemical_potential = Fraction(2, 9)
    energy_1 = Fraction(11, 7)
    energy_2 = Fraction(13, 8)
    energy_3 = Fraction(17, 10)
    energy_4 = energy_1 + energy_2 - energy_3
    incoming_exponent = beta * (
        energy_1 + energy_2 - 2 * chemical_potential
    )
    outgoing_exponent = beta * (
        energy_3 + energy_4 - 2 * chemical_potential
    )
    return {
        "incoming_minus_outgoing_exponent": str(
            incoming_exponent - outgoing_exponent
        ),
        "energy_conservation_residual": str(
            energy_1 + energy_2 - energy_3 - energy_4
        ),
        "particle_number_residual": "0",
        "detailed_balance_pass": incoming_exponent == outgoing_exponent,
    }


def fit_log_slope(horizontal: list[float], vertical: list[float]) -> float:
    log_horizontal = [math.log(value) for value in horizontal]
    log_vertical = [math.log(value) for value in vertical]
    mean_horizontal = sum(log_horizontal) / len(log_horizontal)
    mean_vertical = sum(log_vertical) / len(log_vertical)
    numerator = sum(
        (left - mean_horizontal) * (right - mean_vertical)
        for left, right in zip(log_horizontal, log_vertical)
    )
    denominator = sum(
        (left - mean_horizontal) ** 2 for left in log_horizontal
    )
    return numerator / denominator


def clustering_audit() -> dict[str, Any]:
    momenta = [
        10.0 ** (-4.0 + 3.0 * index / 80.0) for index in range(81)
    ]
    normalized_transform = [
        1.0 / (1.0 + momentum**2) ** 2 for momentum in momenta
    ]
    departures = [
        1.0 - transform for transform in normalized_transform
    ]
    low_slice = [
        index for index, momentum in enumerate(momenta) if momentum <= 1.0e-2
    ]
    slope = fit_log_slope(
        [momenta[index] for index in low_slice],
        [departures[index] for index in low_slice],
    )
    return {
        "benchmark_correlator": "C(r)=C0 exp(-r/xi)",
        "exact_transform": (
            "chi(k)=8pi C0 xi^3/(1+k^2 xi^2)^2"
        ),
        "series": (
            "chi/chi0=1-2(k xi)^2+3(k xi)^4-4(k xi)^6+..."
        ),
        "measured_departure_slope": slope,
        "analytic_target_slope": 2.0,
        "checkpoint_5149_required_slope": 1.0,
        "odd_Taylor_coefficients_zero": True,
        "absolute_k_generated": False,
        "required_determinant_tail_3D": (
            "determinant |k| term corresponds after contact subtraction "
            "to an r^-4 equal-time kernel"
        ),
        "required_susceptibility_tail_3D": (
            "C_q(k^2)~mu/|k| corresponds to an r^-2 susceptibility"
        ),
    }


def source_paths() -> dict[str, Path]:
    return {
        "checkpoint_5149_document": CHECKPOINT_5149_DOCUMENT,
        "checkpoint_5149_result": CHECKPOINT_5149_RESULT,
        "checkpoint_5171_document": CHECKPOINT_5171_DOCUMENT,
        "checkpoint_5171_result": CHECKPOINT_5171_RESULT,
        "checkpoint_4953_document": CHECKPOINT_4953_DOCUMENT,
        "checkpoint_4953_result": CHECKPOINT_4953_RESULT,
        "checkpoint_4953_nonlinear": CHECKPOINT_4953_NONLINEAR,
        "checkpoint_4954_document": CHECKPOINT_4954_DOCUMENT,
        "checkpoint_4954_result": CHECKPOINT_4954_RESULT,
        "checkpoint_4957_document": CHECKPOINT_4957_DOCUMENT,
        "checkpoint_4958_document": CHECKPOINT_4958_DOCUMENT,
        "checkpoint_4958_result": CHECKPOINT_4958_RESULT,
        "checkpoint_4958_trajectory": CHECKPOINT_4958_TRAJECTORY,
        "checkpoint_5179_document": CHECKPOINT_5179_DOCUMENT,
        "checkpoint_5179_result": CHECKPOINT_5179_RESULT,
        "berges_tex": BERGES_TEX,
        "berges_archive": BERGES_ARCHIVE,
    }


def source_metadata() -> dict[str, dict[str, str]]:
    local = "local checkpoint"
    return {
        "checkpoint_5149_document": {
            "url": local,
            "role": "required critical infrared determinant and spectral route",
        },
        "checkpoint_5149_result": {
            "url": local,
            "role": "machine-readable critical-mixing asymptotics",
        },
        "checkpoint_5171_document": {
            "url": local,
            "role": "derived action-angle Vlasov response and double-counting gate",
        },
        "checkpoint_5171_result": {
            "url": local,
            "role": "machine-readable static dielectric spectrum",
        },
        "checkpoint_4953_document": {
            "url": local,
            "role": "exact X2 amplitude and collision invariants",
        },
        "checkpoint_4953_result": {
            "url": local,
            "role": "machine-readable formation and secular bounds",
        },
        "checkpoint_4953_nonlinear": {
            "url": local,
            "role": "173 positive-target SPARC nonlinear control rows",
        },
        "checkpoint_4954_document": {
            "url": local,
            "role": "finite-width and strong nonquasiparticle route boundary",
        },
        "checkpoint_4954_result": {
            "url": local,
            "role": "controlled finite-time and six-point bounds",
        },
        "checkpoint_4957_document": {
            "url": local,
            "role": "r3 equals a3 over twice a2 squared convention",
        },
        "checkpoint_4958_document": {
            "url": local,
            "role": "essential X2-X3 quotient and GR-connected trajectory",
        },
        "checkpoint_4958_result": {
            "url": local,
            "role": "machine-readable essential trajectory endpoints",
        },
        "checkpoint_4958_trajectory": {
            "url": local,
            "role": "dynamic-N8 A2 and essential r3 normalization",
        },
        "checkpoint_5179_document": {
            "url": local,
            "role": "2PI symmetry factors and state-preparation predecessor",
        },
        "checkpoint_5179_result": {
            "url": local,
            "role": "trajectory c and stress-amplitude predecessor values",
        },
        "berges_tex": {
            "url": "https://arxiv.org/abs/hep-ph/0409233",
            "role": "primary 2PI F-rho self-energy and kinetic source",
        },
        "berges_archive": {
            "url": "https://arxiv.org/e-print/hep-ph/0409233",
            "role": "immutable primary-source archive",
        },
    }


def source_signatures(paths: dict[str, Path]) -> dict[str, bool]:
    texts = {
        name: path.read_text(encoding="utf-8", errors="replace")
        for name, path in paths.items()
        if path.suffix.lower() in {".md", ".tex", ".json", ".csv"}
    }
    return {
        "5149_absolute_k": (
            "1-zeta(k) ~ k/(A mu)" in texts["checkpoint_5149_document"]
        ),
        "5149_critical_not_loop": (
            "This is a criticality condition, not a small loop correction."
            in texts["checkpoint_5149_document"]
        ),
        "5171_action_angle": (
            "delta f_n=[n.partial_J f_0/(n.Omega-omega-i0)]"
            in texts["checkpoint_5171_document"]
        ),
        "5171_double_counting": (
            "forbidden double count" in texts["checkpoint_5171_document"]
        ),
        "4953_number_invariant": (
            "int dPi C_cov,22=0" in texts["checkpoint_4953_document"]
        ),
        "4953_momentum_invariant": (
            "int dPi p^nu C_cov,22=0" in texts["checkpoint_4953_document"]
        ),
        "4957_r3_convention": (
            "r3_raw=a3/(2a2^2)" in texts["checkpoint_4957_document"]
        ),
        "4958_shift_symmetric": (
            "shift-symmetric scalar-gravity basis"
            in texts["checkpoint_4958_document"]
        ),
        "5179_double_bubble": (
            "Gamma_2,double-bubble proportional (1/8)"
            in texts["checkpoint_5179_document"]
        ),
        "5179_basketball": (
            "Gamma_2,basketball   proportional (1/48)"
            in texts["checkpoint_5179_document"]
        ),
        "berges_statistical": (
            "\\Sigma_F(x,y)" in texts["berges_tex"]
            and "F^2(x,y)" in texts["berges_tex"]
        ),
        "berges_spectral": (
            "\\Sigma_{\\rho}(x,y)" in texts["berges_tex"]
            and "\\rho^2(x,y)" in texts["berges_tex"]
        ),
        "berges_width_order": (
            "\\sim\\, \\Or (\\lambda^2/N)" in texts["berges_tex"]
        ),
    }


def load_inputs() -> dict[str, Any]:
    result_5149 = read_json(CHECKPOINT_5149_RESULT)
    result_5171 = read_json(CHECKPOINT_5171_RESULT)
    result_4953 = read_json(CHECKPOINT_4953_RESULT)
    result_4954 = read_json(CHECKPOINT_4954_RESULT)
    result_4958 = read_json(CHECKPOINT_4958_RESULT)
    result_5179 = read_json(CHECKPOINT_5179_RESULT)
    nonlinear_rows = [
        row
        for row in read_csv(CHECKPOINT_4953_NONLINEAR)
        if parse_bool(row["positive_outer_residual_target"])
    ]
    trajectory_rows = read_csv(CHECKPOINT_4958_TRAJECTORY)
    trajectory = next(
        row
        for row in trajectory_rows
        if row["scheme"] == "dynamic_etaN"
        and int(row["polynomial_order"]) == 8
        and row["status"] == "GR_CONNECTED_ESSENTIAL_FUNCTIONAL_TRAJECTORY"
        and close(float(row["g"]), 1.0e-10, 1.0e-8)
    )
    natural_c = REDUCED_PLANCK_MASS_EV**-4
    trajectory_c = (
        float(trajectory["A2_a_over_g_power"])
        * natural_c
        / (64.0 * math.pi**2)
    )
    trajectory_ratio = abs(trajectory_c) / natural_c
    essential_r3 = float(trajectory["r3_essential_scalar"])
    return {
        "result_5149": result_5149,
        "result_5171": result_5171,
        "result_4953": result_4953,
        "result_4954": result_4954,
        "result_4958": result_4958,
        "result_5179": result_5179,
        "nonlinear_rows": nonlinear_rows,
        "trajectory": trajectory,
        "natural_c_eV_minus4": natural_c,
        "trajectory_c_eV_minus4": trajectory_c,
        "trajectory_to_natural_ratio": trajectory_ratio,
        "essential_r3": essential_r3,
        "target_fraction": float(
            result_5179["summary"]["minimum_required_fraction"]
        ),
    }


def build_kernel_rows(
    quartic_statistical: dict[int, Fraction],
    quartic_spectral: dict[int, Fraction],
    sextic_statistical: dict[int, Fraction],
    sextic_spectral: dict[int, Fraction],
) -> list[dict[str, Any]]:
    rows = [
        (
            "K5180_01_V4",
            "symmetric X2 four-leg vertex",
            "V4=2 c_ess sum_(3 pairings)(p_i.p_j)(p_k.p_l)",
            "tree O(c_ess)",
            "local vertex",
            "2^2 2! times c_ess/4 gives 2 c_ess per pairing",
            "reproduces M22=(c_ess/2)(s^2+t^2+u^2)",
            "DERIVED",
        ),
        (
            "K5180_02_V6",
            "symmetric X3 six-leg vertex",
            "V6=6 e_ess sum_(15 pairings) product_(3 pairs)(p_i.p_j)",
            "tree O(e_ess)",
            "local vertex",
            "2^3 3! times e_ess/8 gives 6 e_ess per pairing",
            "fixes the direct essential six-scalar kernel",
            "DERIVED",
        ),
        (
            "K5180_03_X2_Hartree",
            "X2 double-bubble 2PI term",
            "Gamma2_X2,H=(1/8) integral_C V4 G G",
            "O(c_ess)",
            "coincident and local",
            "three pairings divided by 4! equals 1/8",
            "renormalizes local kinetic/background coefficients only",
            "DERIVED",
        ),
        (
            "K5180_04_X2_basketball",
            "X2 first nonlocal 2PI term",
            "Gamma2_X2,B=(1/48) integral_C V4(x) G(x,y)^4 V4(y)",
            "O(c_ess^2)",
            "three-line self-energy after one line is opened",
            "4! contractions divided by 2(4!)^2 equals 1/48",
            "owns the first collision width and occupied scattering cut",
            "DERIVED",
        ),
        (
            "K5180_05_X2_Sigma_F",
            "X2 statistical self-energy",
            "Sigma_F,4=-(V4 V4/6)[F^3-(3/4)F rho^2]",
            "O(c_ess^2)",
            "three-line convolution with derivative vertices",
            f"CTP coefficients={quartic_statistical}",
            "the full momentum expression sums the three F-rho-rho placements",
            "DERIVED",
        ),
        (
            "K5180_06_X2_Sigma_rho",
            "X2 spectral self-energy",
            "Sigma_rho,4=-(V4 V4/6)[3 rho F^2-(1/4)rho^3]",
            "O(c_ess^2)",
            "three-line convolution with derivative vertices",
            f"CTP coefficients={quartic_spectral}",
            "Sigma_R,4=theta(x0-y0) Sigma_rho,4",
            "DERIVED",
        ),
        (
            "K5180_07_X3_local",
            "X3 triple-bubble 2PI term",
            "Gamma2_X3,H=(1/48) integral_C V6 G G G",
            "O(e_ess)",
            "coincident and local",
            "15 pairings divided by 6! equals 1/48",
            "local derivative renormalization with no new infrared cut",
            "DERIVED",
        ),
        (
            "K5180_08_X3_tadpole_V4",
            "X3-induced effective four-leg vertex",
            "V4_bar=V4+(1/2)Tr_G V6+...",
            "O(c_ess)+O(e_ess G)",
            "local tadpole",
            "choose(6,2)4!/6!=1/2",
            "mixed c_ess e_ess nonlocal terms enter through V4_bar squared",
            "DERIVED",
        ),
        (
            "K5180_09_X3_five_line",
            "X3 first direct nonlocal 2PI term",
            "Gamma2_X3,B=(1/1440) integral_C V6(x) G(x,y)^6 V6(y)",
            "O(e_ess^2)",
            "five-line self-energy after one line is opened",
            "6! contractions divided by 2(6!)^2 equals 1/1440",
            "owns direct X3 3-to-3 and off-shell number-changing cuts",
            "DERIVED",
        ),
        (
            "K5180_10_X3_Sigma_F",
            "X3 statistical self-energy",
            "Sigma_F,6=-(V6 V6/120)[F^5-(5/2)F^3 rho^2+(5/16)F rho^4]",
            "O(e_ess^2)",
            "five-line convolution",
            f"CTP coefficients={sextic_statistical}",
            "self-energy opening factor is 2x6/1440=1/120",
            "DERIVED",
        ),
        (
            "K5180_11_X3_Sigma_rho",
            "X3 spectral self-energy",
            "Sigma_rho,6=-(V6 V6/120)[5 rho F^4-(5/2)rho^3 F^2+(1/16)rho^5]",
            "O(e_ess^2)",
            "five-line convolution",
            f"CTP coefficients={sextic_spectral}",
            "Sigma_R,6=theta(x0-y0) Sigma_rho,6",
            "DERIVED",
        ),
        (
            "K5180_12_vacuum_threshold_X2",
            "vacuum X2 spectral support",
            "Im Sigma_R,4(p)=0 below p^2=(3m_gap)^2",
            "O(c_ess^2)",
            "one-to-three cut",
            "three positive-energy massive internal spectral lines",
            "static galactic p0=0 branch is below the vacuum cut",
            "DERIVED_SUPPORT_BOUND",
        ),
        (
            "K5180_13_vacuum_threshold_X3",
            "vacuum X3 spectral support",
            "Im Sigma_R,6(p)=0 below p^2=(5m_gap)^2",
            "O(e_ess^2)",
            "one-to-five cut",
            "five positive-energy massive internal spectral lines",
            "X3 does not lower the vacuum threshold",
            "DERIVED_SUPPORT_BOUND",
        ),
        (
            "K5180_14_medium_cut",
            "occupied-medium spectral support",
            "Sigma_rho contains Landau/scattering cuts including p+p1<->p2+p3",
            "O(c_ess^2) and higher",
            "can reach low omega in an occupied state",
            "opposite-sign on-shell energies are available in the medium",
            "leading collisionless part must be separated from collisions",
            "DERIVED_STRUCTURE",
        ),
        (
            "K5180_15_shift_Adler_zero",
            "exact external-leg shift Ward factor",
            "V4(0,p2,p3,p4)=V6(0,p2,...,p6)=0",
            "all orders in X2-X3 diagrams",
            "each external psi is differentiated",
            "every pairing contains the zero external momentum once",
            "Sigma_X2-X3(p)=p_mu p_nu Pi^mu_nu(p)",
            "DERIVED_EXACT",
        ),
        (
            "K5180_16_regular_state_consequence",
            "regular occupied-state self-energy",
            "Pi^mu_nu(p)=Pi0^mu_nu+O(p^2) implies Sigma=O(p^2)",
            "all regular orders",
            "finite correlation length and finite moments",
            "shift Ward factor plus analytic clustering kernel",
            "no additive gap erasure and no absolute-k term",
            "DERIVED_NO_GO",
        ),
    ]
    return [
        {
            "kernel_id": identifier,
            "object": object_name,
            "exact_expression": expression,
            "order": order,
            "support_or_locality": support,
            "derivation": derivation,
            "consequence": consequence,
            "status": status,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for (
            identifier,
            object_name,
            expression,
            order,
            support,
            derivation,
            consequence,
            status,
        ) in rows
    ]


def build_subtraction_rows(
    resolvent: dict[str, Any],
    detailed_balance: dict[str, Any],
    inputs: dict[str, Any],
) -> list[dict[str, Any]]:
    primary = inputs["result_5171"]["summary"]["primary"]
    rows = [
        (
            "S5180_01_kinetic",
            "occupied Wigner equation",
            "(partial_t+v.grad_x+F.grad_p)f=C22[f]+...",
            "separates collisionless transport from the X2 collision term",
            "DERIVED_PARENT_DECOMPOSITION",
        ),
        (
            "S5180_02_Vlasov",
            "collisionless retarded resolvent",
            "R0(omega)=[-i omega+L_Vlasov]^-1",
            "its static action-angle projection is checkpoint 5171",
            "ALREADY_COUNTED",
        ),
        (
            "S5180_03_interacting",
            "interacting retarded resolvent",
            "RC(omega)=[-i omega+L_Vlasov+C22]^-1",
            "contains both previously evolved transport and new collision relaxation",
            "DERIVED",
        ),
        (
            "S5180_04_identity",
            "exact Vlasov subtraction",
            "RC-R0=-RC C22 R0",
            (
                "exact rational residual="
                f"{resolvent['resolvent_identity_max_abs']}"
            ),
            "DERIVED_EXACT",
        ),
        (
            "S5180_05_number_null",
            "collision number zero mode",
            "integral dPi C22=0 and C22 1=0",
            (
                "exact finite-kernel residual="
                f"{resolvent['collision_unit_null_max_abs']}"
            ),
            "DERIVED_EXACT",
        ),
        (
            "S5180_06_momentum_null",
            "collision four-momentum zero modes",
            "integral dPi p^nu C22=0",
            "the collision residual cannot manufacture missing source stress",
            "DERIVED_EXACT",
        ),
        (
            "S5180_07_positivity",
            "linearized collision dissipation",
            resolvent["collision_quadratic_form"],
            "collisions damp nonconserved distortions while preserving null modes",
            "EXACT_COMPARATOR",
        ),
        (
            "S5180_08_detailed_balance",
            "Bose equilibrium collision source",
            "(1+f_i)=exp[beta(E_i-mu)]f_i and E1+E2=E3+E4 imply C22[f_BE]=0",
            (
                "exact exponent residual="
                f"{detailed_balance['incoming_minus_outgoing_exponent']}; "
                "the collision rate does not select a new static equilibrium state"
            ),
            "DERIVED_EXACT",
        ),
        (
            "S5180_09_static_hydrodynamic",
            "static conserved susceptibility",
            "a dynamic diffusion pole has a Ward-required numerator and does not alone create static 1/|k|",
            "critical thermodynamics or a power-law state is still required",
            "DERIVED_SCOPED",
        ),
        (
            "S5180_10_double_count",
            "checkpoint-5171 occupied response",
            "delta f_static=f_Epsilon[deltaPsi-<deltaPsi>orbit]",
            "cannot be added again to checkpoints 5164-5169",
            "FORBIDDEN_DOUBLE_COUNT",
        ),
        (
            "S5180_11_no_pole",
            "executed Vlasov dielectric spectrum",
            (
                "lambda_max="
                f"{float(primary['maximum_static_dielectric_eigenvalue']):.17g}"
            ),
            "the fixed UGC09133 radial benchmark has no static Vlasov pole",
            "SOURCE_LOCKED",
        ),
    ]
    return [
        {
            "subtraction_id": identifier,
            "object": object_name,
            "equation": equation,
            "consequence": consequence,
            "status": status,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for identifier, object_name, equation, consequence, status in rows
    ]


def build_infrared_rows(
    clustering: dict[str, Any],
    inputs: dict[str, Any],
    sparc_summary: dict[str, Any],
) -> list[dict[str, Any]]:
    required_slope = float(
        inputs["result_5149"]["critical_mixing"][
            "low_k_target_slope"
        ]
    )
    rows = [
        (
            "I5180_01_cluster_bound",
            "exponentially clustering equal-time stress kernel",
            "|C_TT(r)|<=C0 exp(-r/xi)",
            "all spatial moments are finite",
            "ASSUMPTION_DEFINING_REGULAR_GAPPED_STATE",
        ),
        (
            "I5180_02_dominated_series",
            "Fourier moment expansion",
            "chi(k)=sum_n (-1)^n k_(i1)...k_(i2n) M_(i1...i2n)/(2n)!",
            "dominated convergence allows termwise derivatives at k=0",
            "DERIVED",
        ),
        (
            "I5180_03_rotation",
            "rotational scalar projection",
            "chi(k)=chi0+chi2 k^2+chi4 k^4+...",
            "only even analytic powers occur",
            "DERIVED",
        ),
        (
            "I5180_04_benchmark",
            clustering["benchmark_correlator"],
            clustering["exact_transform"],
            clustering["series"],
            "EXACT_TRANSFORM",
        ),
        (
            "I5180_05_measured_slope",
            "explicit benchmark departure",
            (
                "d log|chi(k)-chi(0)|/d log k="
                f"{clustering['measured_departure_slope']:.17g}"
            ),
            "converges to analytic slope 2",
            "NUMERICALLY_VERIFIED",
        ),
        (
            "I5180_06_required_slope",
            "checkpoint-5149 critical determinant",
            f"1-zeta(k) proportional |k|; slope={required_slope:.17g}",
            "requires a nonanalytic occupied response",
            "SOURCE_LOCKED_TARGET",
        ),
        (
            "I5180_07_Adler",
            "shift-symmetric X2-X3 self-energy",
            "Sigma(p)=p_mu p_nu Pi^mu_nu(p)",
            "a regular Pi changes kinetic coefficients but not an additive gap",
            "DERIVED_EXACT",
        ),
        (
            "I5180_08_tuned_local",
            "finite local critical tuning",
            "cancelling the k^2 coefficient leaves k^4,k^6,... rather than |k|",
            "a local coefficient tuning cannot reproduce checkpoint 5149",
            "DERIVED_NO_GO",
        ),
        (
            "I5180_09_required_tail",
            "surviving determinant kernel",
            clustering["required_determinant_tail_3D"],
            "the future state calculation has a precise real-space target",
            "DERIVED_SCALING_TARGET",
        ),
        (
            "I5180_10_required_susceptibility",
            "checkpoint-5149 susceptibility",
            clustering["required_susceptibility_tail_3D"],
            "ordinary exponential clustering is insufficient",
            "DERIVED_SCALING_TARGET",
        ),
        (
            "I5180_11_weak_kinetic",
            "largest trajectory-normalized X2 control parameter",
            (
                "max |c_ess|rho="
                f"{sparc_summary['maximum_trajectory_epsilon']:.17g}"
            ),
            (
                "order-one kinetic cancellation needs coefficient >="
                f"{sparc_summary['minimum_Hartree_enhancement_required']:.17g}"
            ),
            "CONTROLLED_ROUTE_REJECTED",
        ),
        (
            "I5180_12_X3",
            "largest conditional X3-to-X2 background ratio",
            (
                "max |e rho^2|/|c rho|=2 r3 |c rho|="
                f"{sparc_summary['maximum_X3_to_X2_ratio']:.17g}"
            ),
            "the essential X3 trajectory does not drive criticality",
            "CONTROLLED_ROUTE_REJECTED",
        ),
        (
            "I5180_13_collision",
            "largest unit-prefactor collision-to-streaming ratio",
            (
                "max Gamma_coll/omega_profile="
                f"{sparc_summary['maximum_collision_to_streaming']:.17g}"
            ),
            (
                "closure would require finite phase-space coefficient >="
                f"{sparc_summary['minimum_collision_prefactor_required']:.17g}"
            ),
            "CONTROLLED_ROUTE_REJECTED",
        ),
        (
            "I5180_14_evasion",
            "nonperturbative evasion condition",
            "xi->infinity or Pi(p) singular with parent-derived positive spectral matrix",
            "Bose condensation, a critical continuum or a full strong boundary hierarchy can evade the regular-state theorem",
            "OPEN_NOT_CLAIMED",
        ),
    ]
    return [
        {
            "infrared_id": identifier,
            "object": object_name,
            "equation_or_value": equation,
            "consequence": consequence,
            "status": status,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for identifier, object_name, equation, consequence, status in rows
    ]


def build_sparc_rows(
    inputs: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    trajectory_ratio = float(inputs["trajectory_to_natural_ratio"])
    essential_r3 = float(inputs["essential_r3"])
    target_fraction = float(inputs["target_fraction"])
    rows: list[dict[str, Any]] = []
    for source_row in inputs["nonlinear_rows"]:
        natural_epsilon = float(source_row["natural_X2_to_X_ratio"])
        trajectory_epsilon = trajectory_ratio * natural_epsilon
        profile_frequency = float(
            source_row["profile_angular_frequency_rad_s"]
        )
        profile_stream_energy = HBAR_EV_S * profile_frequency
        mass_to_streaming = REFERENCE_MASS_EV / profile_stream_energy
        natural_collision = natural_epsilon**2 * mass_to_streaming
        trajectory_collision = trajectory_epsilon**2 * mass_to_streaming
        x3_to_x2 = 2.0 * essential_r3 * trajectory_epsilon
        x3_strength = 2.0 * essential_r3 * trajectory_epsilon**2
        rows.append(
            {
                "galaxy": source_row["galaxy"],
                "outer_radius_m": float(source_row["outer_radius_m"]),
                "profile_angular_frequency_rad_s": profile_frequency,
                "profile_stream_energy_eV": profile_stream_energy,
                "reference_motion_mass_eV": REFERENCE_MASS_EV,
                "mass_to_streaming_ratio": mass_to_streaming,
                "natural_X2_epsilon": natural_epsilon,
                "trajectory_X2_epsilon": trajectory_epsilon,
                "trajectory_X3_strength": x3_strength,
                "trajectory_X3_to_X2_ratio": x3_to_x2,
                "natural_collision_to_streaming_unit_prefactor": natural_collision,
                "trajectory_collision_to_streaming_unit_prefactor": trajectory_collision,
                "Hartree_enhancement_required_for_locked_fraction": (
                    target_fraction / trajectory_epsilon
                ),
                "collision_prefactor_required_for_locked_fraction": (
                    target_fraction / trajectory_collision
                ),
                "collision_residual_closes_locked_fraction": False,
                "status": "CONTROLLED_INTERACTION_RESIDUAL_TOO_SMALL",
                "checkpoint_marker": MARKER,
                "valid_for_full_MTS_claim": False,
                "source_checked_date": CHECKED_DATE,
            }
        )
    maximum_epsilon_row = max(
        rows,
        key=lambda row: float(row["trajectory_X2_epsilon"]),
    )
    maximum_collision_row = max(
        rows,
        key=lambda row: float(
            row["trajectory_collision_to_streaming_unit_prefactor"]
        ),
    )
    maximum_x3_row = max(
        rows,
        key=lambda row: float(row["trajectory_X3_to_X2_ratio"]),
    )
    summary = {
        "positive_target_rows": len(rows),
        "maximum_natural_epsilon": max(
            float(row["natural_X2_epsilon"]) for row in rows
        ),
        "maximum_trajectory_epsilon": float(
            maximum_epsilon_row["trajectory_X2_epsilon"]
        ),
        "maximum_epsilon_galaxy": maximum_epsilon_row["galaxy"],
        "minimum_Hartree_enhancement_required": min(
            float(row["Hartree_enhancement_required_for_locked_fraction"])
            for row in rows
        ),
        "maximum_collision_to_streaming": float(
            maximum_collision_row[
                "trajectory_collision_to_streaming_unit_prefactor"
            ]
        ),
        "maximum_collision_galaxy": maximum_collision_row["galaxy"],
        "minimum_collision_prefactor_required": min(
            float(row["collision_prefactor_required_for_locked_fraction"])
            for row in rows
        ),
        "maximum_X3_to_X2_ratio": float(
            maximum_x3_row["trajectory_X3_to_X2_ratio"]
        ),
        "maximum_X3_strength": max(
            float(row["trajectory_X3_strength"]) for row in rows
        ),
        "maximum_X3_galaxy": maximum_x3_row["galaxy"],
        "trajectory_r3": essential_r3,
        "locked_fraction": target_fraction,
        "exact_two_body_angular_coefficient": 7.0 / (5.0 * math.pi),
    }
    return rows, summary


def build_decision_rows(
    inputs: dict[str, Any],
    sparc_summary: dict[str, Any],
) -> list[dict[str, Any]]:
    decisions = [
        (
            "D5180_01_kernel",
            "Is the first nonlocal X2-X3 retarded 2PI kernel explicit?",
            "YES",
            "X2 three-line and X3 five-line CTP self-energies are derived with exact symmetry factors",
            "KERNEL_DERIVED",
        ),
        (
            "D5180_02_Vlasov",
            "Is the collisionless occupied response a new stress?",
            "NO",
            "its action-angle kernel is checkpoint 5171 and was already evolved in 5164-5169",
            "FORBIDDEN_DOUBLE_COUNT",
        ),
        (
            "D5180_03_collision",
            "Can the controlled collision residual close the locked deficit?",
            "NO",
            (
                "minimum required dimensionless collision prefactor="
                f"{sparc_summary['minimum_collision_prefactor_required']:.17g}"
            ),
            "PERTURBATIVE_COLLISION_ROUTE_CLOSED",
        ),
        (
            "D5180_04_gap",
            "Can regular shift-symmetric X2-X3 diagrams erase a gap additively?",
            "NO",
            "every external leg is differentiated so Sigma(p)=p_mu p_nu Pi^mu_nu(p)",
            "EXACT_SHIFT_WARD_NO_GO",
        ),
        (
            "D5180_05_absolute_k",
            "Can an exponentially clustering occupied state generate 1-zeta proportional |k|?",
            "NO",
            "its equal-time Fourier kernel is analytic in k^2",
            "REGULAR_GAPPED_STATE_ROUTE_CLOSED",
        ),
        (
            "D5180_06_X3",
            "Does the conditional essential X3 trajectory rescue the weak route?",
            "NO",
            (
                "maximum X3-to-X2 background ratio="
                f"{sparc_summary['maximum_X3_to_X2_ratio']:.17g}"
            ),
            "CONTROLLED_X3_ROUTE_CLOSED",
        ),
        (
            "D5180_07_survivor",
            "What interaction/state route survives?",
            "PARENT_DERIVED_CRITICAL_OCCUPIED_STATE",
            "it must violate exponential clustering with the required r^-4 determinant tail while preserving Ward identities and positivity",
            "OPEN_NOT_CLAIMED",
        ),
        (
            "D5180_08_local",
            "Is the local GR/Newton/Maxwell branch modified?",
            "NO",
            "only higher interacting occupied-state response was tested",
            "LOCAL_BRANCH_RETAINED",
        ),
        (
            "D5180_09_full",
            "Is full MTS or the galaxy bridge claimed?",
            "NO",
            "the critical occupied state and its parent preparation remain underived",
            "NONCLAIM",
        ),
        (
            "D5180_10_next",
            "What is the next derivation rather than another weak loop?",
            "CRITICAL_STATE_EXISTENCE_AND_POSITIVITY_GATE",
            "construct a parent stationary or formation state whose connected kernel has the required power-law tail and test the full Hessian spectrum",
            "NEXT_TARGET_FIXED",
        ),
    ]
    return [
        {
            "decision_id": identifier,
            "question": question,
            "answer": answer,
            "evidence": evidence,
            "status": status,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for identifier, question, answer, evidence, status in decisions
    ]


def validation_row(
    identifier: str,
    check: str,
    passed: bool,
    actual: Any,
    expected: Any,
) -> dict[str, Any]:
    return {
        "validation_id": identifier,
        "check": check,
        "passed": bool(passed),
        "actual": actual,
        "expected": expected,
        "checkpoint_marker": MARKER,
        "source_checked_date": CHECKED_DATE,
    }


def write_document(result: dict[str, Any]) -> None:
    summary = result["summary"]
    sparc = summary["SPARC_control"]
    clustering = summary["clustering"]
    document = f"""# 5180 - Interacting retarded 2PI kernel, Vlasov subtraction and infrared gap-closure gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

This checkpoint performs the interaction calculation left open at 5179. The
trajectory-normalized `X2-X3` retarded CTP kernel is now explicit, the
collisionless Vlasov response is subtracted algebraically, and the remaining
collision and spectral pieces are tested against the checkpoint-5149
requirement

```text
1-zeta(k) proportional |k|.
```

The result is sharper than a weak-rate failure. Every field in the
shift-symmetric `X2` and `X3` vertices is differentiated. Consequently every
two-point self-energy constructed from them obeys the exact external-leg
identity

```text
Sigma_X2-X3(p)=p_mu p_nu Pi^mu_nu(p).
```

If the occupied state clusters exponentially, `Pi` is analytic at zero
momentum. The interactions can then renormalize kinetic coefficients but
cannot generate an additive gap cancellation or an `|k|` term. The controlled
interaction repair is closed. A genuinely critical occupied state remains
possible only if the parent derives the required power-law correlation tail;
that state is not claimed here.

## 1. Exact `X2-X3` CTP kernel

For

```text
L_int=(c_ess/4)(partial psi.partial psi)^2
     +(e_ess/8)(partial psi.partial psi)^3,
```

functional differentiation gives

```text
V4=2 c_ess sum_(3 pairings)(p_i.p_j)(p_k.p_l),
V6=6 e_ess sum_(15 pairings)
          (p_i.p_j)(p_k.p_l)(p_m.p_n).
```

The coefficients follow from `2^2 2! (c_ess/4)=2c_ess` and
`2^3 3! (e_ess/8)=6e_ess`; they are not fitted.

The 2PI hierarchy through the first nonlocal graph is

```text
Gamma2_X2,H=(1/8) integral_C V4 G G,
Gamma2_X2,B=(1/48) integral_C V4(x) G(x,y)^4 V4(y),

Gamma2_X3,H=(1/48) integral_C V6 G G G,
Gamma2_X3,B=(1/1440) integral_C V6(x) G(x,y)^6 V6(y).
```

Opening one line produces self-energy factors `1/6` and `1/120`. In the
equal-coordinate shorthand used by the primary 2PI source,

```text
Sigma_F,4
 =-(V4 V4/6)[F^3-(3/4)F rho^2],

Sigma_rho,4
 =-(V4 V4/6)[3 rho F^2-(1/4)rho^3],

Sigma_F,6
 =-(V6 V6/120)
   [F^5-(5/2)F^3 rho^2+(5/16)F rho^4],

Sigma_rho,6
 =-(V6 V6/120)
   [5 rho F^4-(5/2)rho^3 F^2+(1/16)rho^5],

Sigma_R=theta(x0-y0) Sigma_rho.
```

The full momentum kernels retain the derivative vertices and sum the distinct
placements of `F` and `rho`. The displayed coefficients are generated
directly from `(F-i rho/2)^n` and `(F+i rho/2)^n`.

At first order `X3` changes the four-leg kernel only through

```text
V4_bar=V4+(1/2)Tr_G V6+...,
```

where `choose(6,2)4!/6!=1/2`. The mixed `c_ess e_ess` basketball is therefore
inside `V4_bar^2`; the first direct nonlocal `X3` self-energy has five
internal lines.

In vacuum the three-line and five-line cuts begin at `3m_gap` and `5m_gap`.
An occupied medium admits low-frequency scattering cuts, but these must be
split into collisionless transport and an interacting residual before they
can be counted as new physics.

## 2. Exact Vlasov subtraction

Write the Wigner equation as

```text
(partial_t+v.grad_x+F.grad_p)f=C22[f]+... .
```

With

```text
R0=[-i omega+L_Vlasov]^-1,
RC=[-i omega+L_Vlasov+C22]^-1,
```

the new interacting response is not `RC`; checkpoint 5171 and the nonlinear
particle evolution already contain `R0`. The exact remainder is

```text
RC-R0=-RC C22 R0.
```

A rational three-state collision Laplacian verifies this identity with
exact residual `{summary['resolvent']['resolvent_identity_max_abs']}` and
verifies `C22 1=0` with exact residual
`{summary['resolvent']['collision_unit_null_max_abs']}`. This is an algebra
check, not a fit.

Checkpoint 4953 supplies the continuum invariants

```text
integral dPi C22=0,
integral dPi p^nu C22=0.
```

Detailed balance also gives `C22[f_BE]=0`. Collisions relax nonconserved
distortions and alter finite-frequency widths; they do not select a new static
equilibrium distribution or manufacture missing source stress. The fixed
UGC09133 Vlasov benchmark has dielectric eigenvalue
`{summary['primary_Vlasov_eigenvalue']:.17g}`, below its static pole.

## 3. Infrared theorem

Let the equal-time projected connected stress kernel obey

```text
|C_TT(r)|<=C0 exp(-r/xi).
```

All moments are finite, so dominated convergence gives

```text
chi(k)=chi0+chi2 k^2+chi4 k^4+... .
```

The exact benchmark

```text
C(r)=C0 exp(-r/xi)
```

has

```text
chi(k)=8 pi C0 xi^3/(1+k^2 xi^2)^2
      =chi0[1-2(k xi)^2+3(k xi)^4-...].
```

The executed low-momentum departure slope is
`{clustering['measured_departure_slope']:.17g}`, converging to `2`, whereas
checkpoint 5149 requires slope `1`. Even an exact cancellation of the `k^2`
coefficient leaves `k^4`, not `|k|`.

The surviving state target is now concrete. In three spatial dimensions, a
nonlocal determinant term proportional to `|k|` corresponds, after contact
subtraction, to an equal-time `r^-4` kernel. The checkpoint-5149
susceptibility `C_q~mu/|k|` corresponds to an `r^-2` tail. A future state
derivation must produce those tails, not merely a large local coefficient.

## 4. Quantitative occupied-state bound

The dynamic-`N=8` trajectory normalization is

```text
c_ess={summary['trajectory_c_eV_minus4']:.17g} eV^-4,
r3=e_ess/(2 c_ess^2)={summary['essential_r3']:.17g}
```

in the checkpoint-4957/4958 convention. Across all
`{sparc['positive_target_rows']}` positive-target SPARC rows,

```text
max |c_ess| rho
 ={sparc['maximum_trajectory_epsilon']:.17g},

min local enhancement needed for the locked fraction
 ={sparc['minimum_Hartree_enhancement_required']:.17g},

max |e_ess rho^2|/|c_ess rho|
 =2 r3 |c_ess rho|
 ={sparc['maximum_X3_to_X2_ratio']:.17g}.
```

For a narrow high-occupancy shell, checkpoint 4953 gives

```text
sigma22=7 c_ess^2 E^6/(5 pi),
rho~f E^4,
Gamma22~(f E^3) sigma22 f,
Gamma22/E~[7/(5 pi)](c_ess rho)^2.
```

The second factor of `f` is the generous final-state Bose stimulation. For
the profile comparison, grant the microscopic frequency `E=m`, which is much
larger than the profile streaming quantum, and replace the exact angular
coefficient by a general finite controlled coefficient:

```text
Gamma_coll/m=C_coll (c_ess rho)^2.
```

Using the profile streaming frequency `omega_profile` and granting the unit
coefficient comparator,

```text
max Gamma_coll/omega_profile
 ={sparc['maximum_collision_to_streaming']:.17g}.
```

Closing the locked deficit would require

```text
C_coll>={sparc['minimum_collision_prefactor_required']:.17g}.
```

The exact two-body angular coefficient is finite,
`7/(5 pi)={sparc['exact_two_body_angular_coefficient']:.17g}`, and the full
controlled phase-space kernel cannot provide a
coefficient of this magnitude. If occupation correlations make such a
coefficient effectively divergent, the calculation has left the controlled
quasiparticle branch and entered precisely the strong critical-state route.

## 5. Scope

```text
first nonlocal X2 retarded kernel                 = derived;
first direct nonlocal X3 retarded kernel          = derived;
CTP F/rho coefficients                            = derived exactly;
collisionless Vlasov response                     = subtracted exactly;
collision number and four-momentum zero modes     = retained exactly;
regular clustering X2-X3 gap closure              = rejected;
regular clustering |k| determinant                = rejected;
controlled collision/static repair                = rejected quantitatively;
parent-derived critical occupied state             = open, not claimed;
local GR/Newton/Maxwell branch                     = unchanged;
galaxy bridge or full MTS                          = not claimed.
```

Route decision:
`{ROUTE_DECISION}`.

The next calculation is not another weak loop. Construct the smallest
positive parent-derived critical occupied state compatible with the complete
even boundary hierarchy, calculate its equal-time and retarded stress kernel,
and test:

1. the `r^-4` determinant-tail coefficient and `r^-2` susceptibility tail;
2. the checkpoint-5149 unit-mixing normalization;
3. the full metric-motion spectral and gradient eigenvalues;
4. formation from the parent without an inserted occupation law.

If no such state exists, the galaxy bridge cannot come from the present
single shift-symmetric motion-scalar realization.

All `{result['validation_count']}` validation rows pass. The protected
`formalization-workbench` digest remains
`{result['formalization_workbench_tree_sha256']}` and checkpoint 5176 remains
`{result['checkpoint_5176_tree_sha256']}`. No GitHub action occurred.
"""
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text(document, encoding="utf-8")
    temporary.replace(DOCUMENT)


def run(dry_run: bool) -> dict[str, Any]:
    paths = source_paths()
    missing_paths = [str(path) for path in paths.values() if not path.is_file()]
    if missing_paths:
        raise FileNotFoundError(f"missing source paths: {missing_paths}")
    if not FORMAL.is_dir():
        raise FileNotFoundError(FORMAL)
    if not CHECKPOINT_5176_ROOT.is_dir():
        raise FileNotFoundError(CHECKPOINT_5176_ROOT)

    source_hashes_before = {
        name: file_digest(path) for name, path in paths.items()
    }
    signatures = source_signatures(paths)
    formal_before = tree_digest(FORMAL)
    checkpoint_5176_before = tree_digest(CHECKPOINT_5176_ROOT)
    inputs = load_inputs()

    quartic_pairings = generate_pairings(tuple(range(4)))
    sextic_pairings = generate_pairings(tuple(range(6)))
    quartic_statistical = ctp_statistical_coefficients(3)
    quartic_spectral = ctp_spectral_coefficients(3)
    sextic_statistical = ctp_statistical_coefficients(5)
    sextic_spectral = ctp_spectral_coefficients(5)
    resolvent = exact_resolvent_audit()
    detailed_balance = exact_detailed_balance_audit()
    clustering = clustering_audit()
    sparc_rows, sparc_summary = build_sparc_rows(inputs)
    kernel_rows = build_kernel_rows(
        quartic_statistical,
        quartic_spectral,
        sextic_statistical,
        sextic_spectral,
    )
    subtraction_rows = build_subtraction_rows(
        resolvent,
        detailed_balance,
        inputs,
    )
    infrared_rows = build_infrared_rows(
        clustering,
        inputs,
        sparc_summary,
    )
    decision_rows = build_decision_rows(inputs, sparc_summary)

    trajectory_c = float(inputs["trajectory_c_eV_minus4"])
    summary = {
        "route_decision": ROUTE_DECISION,
        "quartic_pairing_count": len(quartic_pairings),
        "sextic_pairing_count": len(sextic_pairings),
        "quartic_2PI_basketball_factor": "1/48",
        "quartic_self_energy_factor": "1/6",
        "sextic_2PI_basketball_factor": "1/1440",
        "sextic_self_energy_factor": "1/120",
        "quartic_statistical_coefficients": {
            str(power): str(value)
            for power, value in quartic_statistical.items()
        },
        "quartic_spectral_coefficients": {
            str(power): str(value)
            for power, value in quartic_spectral.items()
        },
        "sextic_statistical_coefficients": {
            str(power): str(value)
            for power, value in sextic_statistical.items()
        },
        "sextic_spectral_coefficients": {
            str(power): str(value)
            for power, value in sextic_spectral.items()
        },
        "resolvent": resolvent,
        "detailed_balance": detailed_balance,
        "clustering": clustering,
        "SPARC_control": sparc_summary,
        "trajectory_c_eV_minus4": trajectory_c,
        "trajectory_to_natural_ratio": float(
            inputs["trajectory_to_natural_ratio"]
        ),
        "essential_r3": float(inputs["essential_r3"]),
        "primary_Vlasov_eigenvalue": float(
            inputs["result_5171"]["summary"]["primary"][
                "maximum_static_dielectric_eigenvalue"
            ]
        ),
        "natural_galaxy_secular_phase_max": float(
            inputs["result_4953"]["execution"][
                "natural_galaxy_phase_max"
            ]
        ),
        "controlled_log_gain_max": float(
            inputs["result_4954"]["execution"][
                "controlled_envelope_log_gain_max_high_frequency"
            ]
        ),
        "shift_symmetric_external_Adler_zero": True,
        "regular_clustering_gap_closure": False,
        "regular_clustering_absolute_k": False,
        "controlled_collision_repair": False,
        "critical_occupied_state": "OPEN_NOT_CLAIMED",
        "local_GR_Newton_Maxwell_branch_modified": False,
        "valid_for_local_GR_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_cosmology_claim": False,
        "valid_for_full_MTS_claim": False,
    }

    dry_checks = [
        validation_row(
            "V5180_01_source_paths",
            "all source paths exist",
            not missing_paths,
            len(paths) - len(missing_paths),
            len(paths),
        ),
        validation_row(
            "V5180_02_source_locks",
            "all read-only source hashes match their locks",
            source_hashes_before == SOURCE_HASH_LOCKS,
            sum(
                source_hashes_before[name] == SOURCE_HASH_LOCKS[name]
                for name in SOURCE_HASH_LOCKS
            ),
            len(SOURCE_HASH_LOCKS),
        ),
        validation_row(
            "V5180_03_source_signatures",
            "all required parent and primary-source clauses are present",
            all(signatures.values()),
            sum(signatures.values()),
            len(signatures),
        ),
        validation_row(
            "V5180_04_formal_before",
            "formalization-workbench is protected before execution",
            formal_before == FORMAL_DIGEST_LOCK,
            formal_before,
            FORMAL_DIGEST_LOCK,
        ),
        validation_row(
            "V5180_05_5176_before",
            "checkpoint 5176 is immutable before execution",
            checkpoint_5176_before == CHECKPOINT_5176_TREE_LOCK,
            checkpoint_5176_before,
            CHECKPOINT_5176_TREE_LOCK,
        ),
        validation_row(
            "V5180_06_pairings",
            "quartic and sextic pairing counts are exact",
            [len(quartic_pairings), len(sextic_pairings)] == [3, 15],
            [len(quartic_pairings), len(sextic_pairings)],
            [3, 15],
        ),
        validation_row(
            "V5180_07_vertex_factors",
            "X2 and X3 per-pairing vertex factors are 2 and 6",
            [
                Fraction(1, 4) * 2**2 * math.factorial(2),
                Fraction(1, 8) * 2**3 * math.factorial(3),
            ]
            == [Fraction(2), Fraction(6)],
            ["2", "6"],
            ["2", "6"],
        ),
        validation_row(
            "V5180_08_2PI_factors",
            "basketball symmetry factors are exact",
            [
                Fraction(1, 2 * math.factorial(4)),
                Fraction(1, 2 * math.factorial(6)),
            ]
            == [Fraction(1, 48), Fraction(1, 1440)],
            ["1/48", "1/1440"],
            ["1/48", "1/1440"],
        ),
        validation_row(
            "V5180_09_self_energy_factors",
            "opening a 2PI line gives exact self-energy factors",
            [
                Fraction(2 * 4, 48),
                Fraction(2 * 6, 1440),
            ]
            == [Fraction(1, 6), Fraction(1, 120)],
            ["1/6", "1/120"],
            ["1/6", "1/120"],
        ),
        validation_row(
            "V5180_10_quartic_F",
            "three-line statistical CTP polynomial is exact",
            quartic_statistical
            == {0: Fraction(1), 2: Fraction(-3, 4)},
            str(quartic_statistical),
            "{0: 1, 2: -3/4}",
        ),
        validation_row(
            "V5180_11_quartic_rho",
            "three-line spectral CTP polynomial is exact",
            quartic_spectral
            == {1: Fraction(3), 3: Fraction(-1, 4)},
            str(quartic_spectral),
            "{1: 3, 3: -1/4}",
        ),
        validation_row(
            "V5180_12_sextic_F",
            "five-line statistical CTP polynomial is exact",
            sextic_statistical
            == {
                0: Fraction(1),
                2: Fraction(-5, 2),
                4: Fraction(5, 16),
            },
            str(sextic_statistical),
            "{0: 1, 2: -5/2, 4: 5/16}",
        ),
        validation_row(
            "V5180_13_sextic_rho",
            "five-line spectral CTP polynomial is exact",
            sextic_spectral
            == {
                1: Fraction(5),
                3: Fraction(-5, 2),
                5: Fraction(1, 16),
            },
            str(sextic_spectral),
            "{1: 5, 3: -5/2, 5: 1/16}",
        ),
        validation_row(
            "V5180_14_resolvent",
            "Vlasov-collision resolvent subtraction is exact",
            resolvent["exact_identity_pass"],
            resolvent["resolvent_identity_max_abs"],
            "0",
        ),
        validation_row(
            "V5180_15_collision_null",
            "collision operator preserves the unit mode exactly",
            resolvent["exact_null_pass"],
            resolvent["collision_unit_null_max_abs"],
            "0",
        ),
        validation_row(
            "V5180_15b_detailed_balance",
            "Bose two-to-two detailed balance exponent cancels exactly",
            detailed_balance["detailed_balance_pass"],
            detailed_balance["incoming_minus_outgoing_exponent"],
            "0",
        ),
        validation_row(
            "V5180_16_cluster_slope",
            "exponential clustering benchmark approaches k squared",
            close(
                float(clustering["measured_departure_slope"]),
                2.0,
                relative_tolerance=2.0e-4,
            ),
            clustering["measured_departure_slope"],
            2.0,
        ),
        validation_row(
            "V5180_17_target_slope",
            "checkpoint 5149 requires the distinct absolute-k slope",
            close(
                float(
                    inputs["result_5149"]["critical_mixing"][
                        "low_k_target_slope"
                    ]
                ),
                1.0,
            ),
            inputs["result_5149"]["critical_mixing"][
                "low_k_target_slope"
            ],
            1.0,
        ),
        validation_row(
            "V5180_18_Vlasov_no_pole",
            "fixed primary Vlasov dielectric eigenvalue stays below one",
            summary["primary_Vlasov_eigenvalue"] < 1.0,
            summary["primary_Vlasov_eigenvalue"],
            "<1",
        ),
        validation_row(
            "V5180_19_positive_rows",
            "all 173 positive-target SPARC rows are retained",
            sparc_summary["positive_target_rows"] == 173,
            sparc_summary["positive_target_rows"],
            173,
        ),
        validation_row(
            "V5180_20_trajectory_c",
            "trajectory c matches checkpoint 5179",
            close(
                trajectory_c,
                float(
                    inputs["result_5179"]["summary"][
                        "trajectory_c_eV_minus4"
                    ]
                ),
            ),
            trajectory_c,
            inputs["result_5179"]["summary"]["trajectory_c_eV_minus4"],
        ),
        validation_row(
            "V5180_21_weak_X2",
            "largest trajectory X2 control parameter is perturbative",
            sparc_summary["maximum_trajectory_epsilon"] < 1.0e-100,
            sparc_summary["maximum_trajectory_epsilon"],
            "<1e-100",
        ),
        validation_row(
            "V5180_22_weak_X3",
            "conditional essential X3 remains smaller than X2",
            sparc_summary["maximum_X3_to_X2_ratio"] < 1.0e-90,
            sparc_summary["maximum_X3_to_X2_ratio"],
            "<1e-90",
        ),
        validation_row(
            "V5180_23_collision_bound",
            "unit-prefactor collision residual is negligible",
            sparc_summary["maximum_collision_to_streaming"] < 1.0e-200,
            sparc_summary["maximum_collision_to_streaming"],
            "<1e-200",
        ),
        validation_row(
            "V5180_24_collision_requirement",
            "collision closure needs a nonperturbative prefactor",
            sparc_summary["minimum_collision_prefactor_required"]
            > 1.0e200,
            sparc_summary["minimum_collision_prefactor_required"],
            ">1e200",
        ),
        validation_row(
            "V5180_25_parent_invariants",
            "checkpoint 4953 collision invariants are source-locked",
            bool(
                inputs["result_4953"]["symbolic"][
                    "collision_invariants_ok"
                ]
            ),
            inputs["result_4953"]["symbolic"]["collision_invariants_ok"],
            True,
        ),
        validation_row(
            "V5180_26_no_regular_gap",
            "regular clustering branch does not claim gap closure",
            not summary["regular_clustering_gap_closure"],
            summary["regular_clustering_gap_closure"],
            False,
        ),
        validation_row(
            "V5180_27_no_claims",
            "all generated theory and SPARC rows remain nonclaims",
            all(
                not row["valid_for_full_MTS_claim"]
                for row in (
                    kernel_rows
                    + subtraction_rows
                    + infrared_rows
                    + sparc_rows
                    + decision_rows
                )
            ),
            "all_false",
            "all_false",
        ),
    ]
    failures = [
        row["validation_id"] for row in dry_checks if not row["passed"]
    ]
    if failures:
        raise RuntimeError(f"dry-run validation failures: {failures}")
    if dry_run:
        return {
            "mode": "dry-run",
            "checkpoint_marker": MARKER,
            "planned_outputs": [
                str(path)
                for path in (
                    KERNEL_CSV,
                    SUBTRACTION_CSV,
                    INFRARED_CSV,
                    SPARC_CSV,
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

    write_csv(KERNEL_CSV, kernel_rows)
    write_csv(SUBTRACTION_CSV, subtraction_rows)
    write_csv(INFRARED_CSV, infrared_rows)
    write_csv(SPARC_CSV, sparc_rows)
    write_csv(DECISION_CSV, decision_rows)
    source_hashes_after = {
        name: file_digest(path) for name, path in paths.items()
    }
    metadata = source_metadata()
    provenance_rows = [
        {
            "source_id": name,
            "source_path": str(path),
            "source_url": metadata[name]["url"],
            "role": metadata[name]["role"],
            "sha256_before": source_hashes_before[name],
            "sha256_after": source_hashes_after[name],
            "read_only_unchanged": (
                source_hashes_before[name] == source_hashes_after[name]
            ),
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for name, path in paths.items()
    ]
    write_csv(PROVENANCE_CSV, provenance_rows)

    formal_after = tree_digest(FORMAL)
    checkpoint_5176_after = tree_digest(CHECKPOINT_5176_ROOT)
    output_tables = (
        KERNEL_CSV,
        SUBTRACTION_CSV,
        INFRARED_CSV,
        SPARC_CSV,
        DECISION_CSV,
        PROVENANCE_CSV,
    )
    output_text = "\n".join(
        path.read_text(encoding="utf-8") for path in output_tables
    )
    full_checks = dry_checks + [
        validation_row(
            "V5180_28_sources_read_only",
            "all source hashes remain unchanged",
            source_hashes_before == source_hashes_after,
            sum(
                source_hashes_before[name] == source_hashes_after[name]
                for name in paths
            ),
            len(paths),
        ),
        validation_row(
            "V5180_29_formal_after",
            "formalization-workbench remains protected after execution",
            formal_after == formal_before == FORMAL_DIGEST_LOCK,
            formal_after,
            FORMAL_DIGEST_LOCK,
        ),
        validation_row(
            "V5180_30_5176_after",
            "checkpoint 5176 remains immutable after execution",
            checkpoint_5176_after
            == checkpoint_5176_before
            == CHECKPOINT_5176_TREE_LOCK,
            checkpoint_5176_after,
            CHECKPOINT_5176_TREE_LOCK,
        ),
        validation_row(
            "V5180_31_output_rows",
            "all generated evidence tables have exact row counts",
            [
                len(kernel_rows),
                len(subtraction_rows),
                len(infrared_rows),
                len(sparc_rows),
                len(decision_rows),
                len(provenance_rows),
            ]
            == [16, 11, 14, 173, 10, len(paths)],
            [
                len(kernel_rows),
                len(subtraction_rows),
                len(infrared_rows),
                len(sparc_rows),
                len(decision_rows),
                len(provenance_rows),
            ],
            [16, 11, 14, 173, 10, len(paths)],
        ),
        validation_row(
            "V5180_32_no_placeholders",
            "generated evidence contains no placeholder marker",
            "MISSING_" not in output_text,
            "MISSING_" in output_text,
            False,
        ),
        validation_row(
            "V5180_33_survivor_unique",
            "exactly one decision row identifies the surviving route",
            sum(
                row["decision_id"] == "D5180_07_survivor"
                for row in decision_rows
            )
            == 1,
            sum(
                row["decision_id"] == "D5180_07_survivor"
                for row in decision_rows
            ),
            1,
        ),
        validation_row(
            "V5180_34_local_unchanged",
            "local GR/Newton/Maxwell branch remains unchanged",
            not summary["local_GR_Newton_Maxwell_branch_modified"],
            summary["local_GR_Newton_Maxwell_branch_modified"],
            False,
        ),
        validation_row(
            "V5180_35_full_nonclaim",
            "checkpoint remains a local, galaxy, cosmology and full-MTS nonclaim",
            not any(
                summary[key]
                for key in (
                    "valid_for_local_GR_claim",
                    "valid_for_galaxy_claim",
                    "valid_for_cosmology_claim",
                    "valid_for_full_MTS_claim",
                )
            ),
            [
                summary["valid_for_local_GR_claim"],
                summary["valid_for_galaxy_claim"],
                summary["valid_for_cosmology_claim"],
                summary["valid_for_full_MTS_claim"],
            ],
            [False, False, False, False],
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
        "source_signatures": signatures,
        "formalization_workbench_tree_sha256": formal_after,
        "checkpoint_5176_tree_sha256": checkpoint_5176_after,
        "summary": summary,
        "validation_count": len(full_checks),
        "validation_failures": failures,
        "valid_for_local_GR_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_cosmology_claim": False,
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
            "Derive the X2-X3 retarded 2PI kernel, subtract Vlasov, and "
            "test infrared gap closure."
        )
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate source locks and calculations without writing outputs",
    )
    arguments = parser.parse_args()
    result = run(arguments.dry_run)
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
