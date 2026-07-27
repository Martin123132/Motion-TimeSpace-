from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import quad

sys.dont_write_bytecode = True


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()

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
CHECKPOINT_4935_OPERATORS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4935"
    / "motion_sector_entry_operator_table.csv"
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
CHECKPOINT_4958_SPECTRUM = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4958"
    / "essential_functional_stability_spectrum.csv"
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
CHECKPOINT_5178_DOCUMENT = (
    POST
    / "5178-Y5-R2FR-exact-2PI-Schur-Ward-Vlasov-subtraction-and-Gaussian-residual-stress-no-go.md"
)
CHECKPOINT_5178_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5178"
    / "twoPI_Schur_Vlasov_subtraction_results.json"
)
CHECKPOINT_5180_DOCUMENT = (
    POST
    / "5180-Y5-R2FR-interacting-retarded-2PI-kernel-Vlasov-subtraction-and-infrared-gap-closure-gate.md"
)
CHECKPOINT_5180_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5180"
    / "interacting_spectral_gap_results.json"
)
CHECKPOINT_5176_ROOT = POST / "source-intake" / "functional_rg" / "5176"

OUT = POST / "source-intake" / "functional_rg" / "5181"
PAIR_CSV = OUT / "critical_pair_bubble_derivation.csv"
HESSIAN_CSV = OUT / "positive_critical_Hessian_completion.csv"
OBSTRUCTION_CSV = OUT / "finite_gap_and_locality_obstruction.csv"
SCALING_CSV = OUT / "critical_scaling_and_parent_match.csv"
OWNERSHIP_CSV = OUT / "critical_pair_vertex_ownership_gate.csv"
DECISION_CSV = OUT / "critical_continuum_route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "critical_pair_completion_results.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5181_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5181-Y5-R2FR-critical-pair-bubble-positive-Hessian-and-parent-ownership-gate.md"
)

MARKER = "MTS_5181_CRITICAL_PAIR_BUBBLE_POSITIVE_HESSIAN_PARENT_OWNERSHIP_GATE"
CHECKED_DATE = "2026-07-23"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5176_TREE_LOCK = (
    "254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b"
)
REDUCED_PLANCK_MASS_EV = 2.435e27
HBAR_C_EV_M = 1.973269804e-7
KPC_M = 3.085677581491367e19
REFERENCE_GAP_EV = 1.0e-20

SOURCE_HASH_LOCKS = {
    "checkpoint_4935_document": (
        "649da892ba5c256b7670206e837604dbbe04358fcd3705b5871906805e00c1df"
    ),
    "checkpoint_4935_result": (
        "ba3dfdaacfb1e3d00282d82c4b4656a937e033cb9145e94c71b81e9c42a54240"
    ),
    "checkpoint_4935_operators": (
        "50f6a5481e3e1a94df12469ce13fa0a88450770a5930226eec928f8e9bafc3d6"
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
    "checkpoint_4958_spectrum": (
        "a58def91b022f9890831d564d3268c5f8ab034433815e836156dc138048f2f7b"
    ),
    "checkpoint_5148_document": (
        "b2d5bddd8ce3cee2299b2cdadd66a0688bbd07c945bc329ac2ade4c20c113352"
    ),
    "checkpoint_5148_result": (
        "a9f48dd11d6c7f3bdd79436ade9d467c8b870b50c5fb2c5c760abae8dc3f05aa"
    ),
    "checkpoint_5149_document": (
        "4ccd4b37a60a3e5b66d8cc9d0f3e94473baf19f1468180a74a468f3ad1db606d"
    ),
    "checkpoint_5149_result": (
        "32970c04699829c2e4190dbbf9926b602c9079cb385737dfccf67af82acdefdc"
    ),
    "checkpoint_5178_document": (
        "7bce528f8654373353304bf904316ddc15e2923dda3064bc7e9684e92a468ac9"
    ),
    "checkpoint_5178_result": (
        "f007ab8d2f157e0fbda7465806e2902cca9e8f98d94db2d5d2fe4f1c54a0b007"
    ),
    "checkpoint_5180_document": (
        "1df0b686a815496b143f5397aebf4b55d16058cd8bbca3910fb7993e980c0c10"
    ),
    "checkpoint_5180_result": (
        "699ac52dc60d07f6893b321aeb7a7701834870bb5fd1b09499f42a3486475512"
    ),
}

ROUTE_DECISION = (
    "THE_REQUIRED_INFRARED_ONE_OVER_ABSOLUTE_K_RESPONSE_IS_NO_LONGER_AN_"
    "UNSPECIFIED_KERNEL_IT_IS_EXACTLY_THE_MASSLESS_THREE_DIMENSIONAL_"
    "TWO_PARTICLE_BUBBLE_AND_CQ_EQUALS_EIGHT_MU_TIMES_THE_EXISTING_PHASE_"
    "OCCUPATION_TIMES_THAT_BUBBLE_A_POSITIVE_STATIC_AND_CAUSAL_GENERALIZED_"
    "CONTINUUM_HESSIAN_COMPLETION_EXISTS_AND_ITS_SCHUR_COMPLEMENT_GIVES_"
    "THE_REQUIRED_UNIT_MIXING_AND_K_CUBED_RESIDUAL_WITHOUT_A_GHOST_"
    "HOWEVER_THE_FULL_Q_CROSSOVER_IS_PROVABLY_NOT_A_POSITIVE_MIXTURE_OF_"
    "ORDINARY_MASSIVE_PAIR_THRESHOLDS_AND_THE_CURRENT_PARENT_DOES_NOT_YET_"
    "DERIVE_THE_LOGISTIC_COMPOSITE_FORM_FACTOR_THE_ENVIRONMENTAL_GAP_"
    "COLLAPSE_OR_THE_PLANCK_NORMALIZED_HILBERT_PAIR_VERTEX_THEREFORE_THE_"
    "CRITICAL_PAIR_CARRIER_IS_DERIVED_BUT_PARENT_OWNERSHIP_AND_ALL_"
    "PHENOMENOLOGICAL_CLAIMS_REMAIN_OPEN"
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


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "passed"}


def response_coefficient(s_value: float, q_value: float, mu_value: float) -> float:
    return mu_value ** (1.0 + q_value) / (
        math.sqrt(s_value)
        * (s_value ** (q_value / 2.0) + mu_value**q_value)
    )


def response_density(t_value: float, q_value: float, mu_value: float) -> float:
    angle = math.pi * q_value / 2.0
    t_power = t_value ** (q_value / 2.0)
    numerator = mu_value**q_value + t_power * math.cos(angle)
    denominator = (
        mu_value ** (2.0 * q_value)
        + 2.0
        * mu_value**q_value
        * t_power
        * math.cos(angle)
        + t_value**q_value
    )
    return (
        mu_value ** (1.0 + q_value)
        * numerator
        / (math.pi * math.sqrt(t_value) * denominator)
    )


def reconstruct_response(
    s_value: float,
    q_value: float,
    mu_value: float,
) -> float:
    def logarithmic_integrand(log_t: float) -> float:
        t_value = math.exp(log_t)
        return (
            response_density(t_value, q_value, mu_value)
            * t_value
            / (s_value + t_value)
        )

    return quad(
        logarithmic_integrand,
        -70.0,
        70.0,
        epsabs=1.0e-11,
        epsrel=1.0e-10,
        limit=1000,
    )[0]


def phase_occupation(k_value: float, q_value: float, mu_value: float) -> float:
    return mu_value**q_value / (k_value**q_value + mu_value**q_value)


def pair_bubble(k_value: float, mass_value: float) -> float:
    if mass_value == 0.0:
        return 1.0 / (8.0 * k_value)
    return math.atan(k_value / (2.0 * mass_value)) / (
        4.0 * math.pi * k_value
    )


def pair_bubble_feynman_parameter(k_value: float, mass_value: float) -> float:
    return quad(
        lambda x_value: 1.0
        / (
            8.0
            * math.pi
            * math.sqrt(
                mass_value**2
                + x_value * (1.0 - x_value) * k_value**2
            )
        ),
        0.0,
        1.0,
        epsabs=1.0e-13,
        epsrel=1.0e-12,
        limit=200,
    )[0]


def pair_mass_cumulative(
    mass_value: float,
    q_value: float,
    mu_value: float,
) -> float:
    angle_cosine = math.cos(math.pi * q_value / 2.0)
    x_value = (2.0 * mass_value / mu_value) ** q_value
    return (
        8.0
        * mu_value
        * (1.0 + angle_cosine * x_value)
        / (1.0 + 2.0 * angle_cosine * x_value + x_value**2)
    )


def pair_mass_weight_derivative(
    mass_value: float,
    q_value: float,
    mu_value: float,
) -> float:
    angle_cosine = math.cos(math.pi * q_value / 2.0)
    x_value = (2.0 * mass_value / mu_value) ** q_value
    denominator = 1.0 + 2.0 * angle_cosine * x_value + x_value**2
    return (
        -8.0
        * mu_value
        * q_value
        * x_value
        * (
            angle_cosine
            + 2.0 * x_value
            + angle_cosine * x_value**2
        )
        / (mass_value * denominator**2)
    )


def logarithmic_slope(horizontal: np.ndarray, vertical: np.ndarray) -> float:
    log_horizontal = np.log(horizontal)
    log_vertical = np.log(vertical)
    centered_horizontal = log_horizontal - np.mean(log_horizontal)
    centered_vertical = log_vertical - np.mean(log_vertical)
    return float(
        np.dot(centered_horizontal, centered_vertical)
        / np.dot(centered_horizontal, centered_horizontal)
    )


def fourier_power_coefficient(power: float, dimensions: float = 3.0) -> float:
    alpha_value = -power / 2.0
    return math.gamma(dimensions / 2.0 - alpha_value) / (
        4.0**alpha_value
        * math.pi ** (dimensions / 2.0)
        * math.gamma(alpha_value)
    )


def source_paths() -> dict[str, Path]:
    return {
        "checkpoint_4935_document": CHECKPOINT_4935_DOCUMENT,
        "checkpoint_4935_result": CHECKPOINT_4935_RESULT,
        "checkpoint_4935_operators": CHECKPOINT_4935_OPERATORS,
        "checkpoint_4958_document": CHECKPOINT_4958_DOCUMENT,
        "checkpoint_4958_result": CHECKPOINT_4958_RESULT,
        "checkpoint_4958_trajectory": CHECKPOINT_4958_TRAJECTORY,
        "checkpoint_4958_spectrum": CHECKPOINT_4958_SPECTRUM,
        "checkpoint_5148_document": CHECKPOINT_5148_DOCUMENT,
        "checkpoint_5148_result": CHECKPOINT_5148_RESULT,
        "checkpoint_5149_document": CHECKPOINT_5149_DOCUMENT,
        "checkpoint_5149_result": CHECKPOINT_5149_RESULT,
        "checkpoint_5178_document": CHECKPOINT_5178_DOCUMENT,
        "checkpoint_5178_result": CHECKPOINT_5178_RESULT,
        "checkpoint_5180_document": CHECKPOINT_5180_DOCUMENT,
        "checkpoint_5180_result": CHECKPOINT_5180_RESULT,
    }


def source_metadata() -> dict[str, dict[str, str]]:
    local = "local checkpoint"
    return {
        "checkpoint_4935_document": {
            "url": local,
            "role": "parent motion kinetic term, fractional potential, and gap entry",
        },
        "checkpoint_4935_result": {
            "url": local,
            "role": "machine-readable parent motion Hessian and mass-gap contract",
        },
        "checkpoint_4935_operators": {
            "url": local,
            "role": "parent motion operator and O4 Hessian table",
        },
        "checkpoint_4958_document": {
            "url": local,
            "role": "essential trajectory, scalar anomalous dimension, and O4 portal",
        },
        "checkpoint_4958_result": {
            "url": local,
            "role": "machine-readable fixed-point and infrared trajectory data",
        },
        "checkpoint_4958_trajectory": {
            "url": local,
            "role": "dynamic N8 GR-connected trajectory",
        },
        "checkpoint_4958_spectrum": {
            "url": local,
            "role": "current local-operator stability spectrum",
        },
        "checkpoint_5148_document": {
            "url": local,
            "role": "phase occupation and required static Schur response",
        },
        "checkpoint_5148_result": {
            "url": local,
            "role": "q, amplitude, mu-times-L, and galaxy corridor",
        },
        "checkpoint_5149_document": {
            "url": local,
            "role": "positive Stieltjes density and critical unit-mixing target",
        },
        "checkpoint_5149_result": {
            "url": local,
            "role": "machine-readable spectral and asymptotic tests",
        },
        "checkpoint_5178_document": {
            "url": local,
            "role": "exact 2PI Schur identity and connected stress kernel",
        },
        "checkpoint_5178_result": {
            "url": local,
            "role": "gapped Gaussian and O4 no-go benchmarks",
        },
        "checkpoint_5180_document": {
            "url": local,
            "role": "explicit interacting retarded 2PI and clustering no-go",
        },
        "checkpoint_5180_result": {
            "url": local,
            "role": "machine-readable weak-interaction and gap-closure bounds",
        },
    }


def source_signatures(paths: dict[str, Path]) -> dict[str, bool]:
    texts = {
        name: path.read_text(encoding="utf-8", errors="replace")
        for name, path in paths.items()
        if path.suffix.lower() in {".md", ".json", ".csv"}
    }
    return {
        "4935_parent_kinetic": (
            "-1/2 integral H^{mu nu} partial_mu psi partial_nu psi"
            in texts["checkpoint_4935_result"]
        ),
        "4935_mass_gap": (
            "m_gap=c_m g_psi^(3/8)" in texts["checkpoint_4935_result"]
        ),
        "4935_O4_unique": (
            "UNIQUE_SIX_DERIVATIVE_MOTION_HESSIAN_PORTAL"
            in texts["checkpoint_4935_operators"]
        ),
        "4958_eta": (
            '"eta_psi": -0.06532510306084385'
            in texts["checkpoint_4958_result"]
        ),
        "5148_phase_occupation": (
            "n_q(y) = y^q/(1+y^q)" in texts["checkpoint_5148_document"]
        ),
        "5148_response": (
            "C_q(y) = y n_q(y)" in texts["checkpoint_5148_document"]
        ),
        "5149_density": (
            "rho_C(t)=mu^(1+q)" in texts["checkpoint_5149_document"]
        ),
        "5149_unit_mixing": (
            "1-zeta(k) ~ k/(A mu)" in texts["checkpoint_5149_document"]
        ),
        "5178_stress_kernel": (
            "Pi_R=Pi_contact-i theta(x0-y0)<[T(x),T(y)]>"
            in texts["checkpoint_5178_document"]
        ),
        "5178_gaussian_no_go": (
            "Gaussian gapped |k| critical response"
            in texts["checkpoint_5178_document"]
        ),
        "5180_regular_clustering": (
            "chi(k)=chi0+chi2 k^2+chi4 k^4+..."
            in texts["checkpoint_5180_document"]
        ),
    }


def load_inputs() -> dict[str, Any]:
    result_4935 = read_json(CHECKPOINT_4935_RESULT)
    result_4958 = read_json(CHECKPOINT_4958_RESULT)
    result_5148 = read_json(CHECKPOINT_5148_RESULT)
    result_5149 = read_json(CHECKPOINT_5149_RESULT)
    result_5178 = read_json(CHECKPOINT_5178_RESULT)
    result_5180 = read_json(CHECKPOINT_5180_RESULT)
    operator_rows = read_csv(CHECKPOINT_4935_OPERATORS)
    spectrum_rows = [
        row
        for row in read_csv(CHECKPOINT_4958_SPECTRUM)
        if row["scheme"] == "dynamic_etaN"
        and int(row["polynomial_order"]) == 8
    ]
    trajectory_rows = [
        row
        for row in read_csv(CHECKPOINT_4958_TRAJECTORY)
        if row["scheme"] == "dynamic_etaN"
        and int(row["polynomial_order"]) == 8
    ]
    relevant_rows = [
        row for row in spectrum_rows if parse_bool(row["relevant"])
    ]
    return {
        "result_4935": result_4935,
        "result_4958": result_4958,
        "result_5148": result_5148,
        "result_5149": result_5149,
        "result_5178": result_5178,
        "result_5180": result_5180,
        "operator_rows": operator_rows,
        "spectrum_rows": spectrum_rows,
        "trajectory_rows": trajectory_rows,
        "relevant_rows": relevant_rows,
    }


def calculate(inputs: dict[str, Any]) -> dict[str, Any]:
    q_value = float(inputs["result_5148"]["kernel"]["q"])
    amplitude = float(
        inputs["result_5148"]["galaxy_smoke"]["amplitude_geometric_mean"]
    )
    mu_times_L = float(
        inputs["result_5148"]["kernel"]["best_mu_times_L_eff"]
    )
    minimum_L_kpc = float(
        inputs["result_5148"]["galaxy_smoke"]["minimum_L_eff_kpc"]
    )
    maximum_L_kpc = float(
        inputs["result_5148"]["galaxy_smoke"]["maximum_L_eff_kpc"]
    )
    bubble_trials = []
    bubble_spectral_errors = []
    for k_value, mass_value in (
        (0.1, 1.0),
        (1.0, 1.0),
        (10.0, 1.0),
        (1.0, 0.01),
        (1.0, 100.0),
        (0.001, 1.0),
        (1000.0, 1.0),
    ):
        analytic = pair_bubble(k_value, mass_value)
        numerical = pair_bubble_feynman_parameter(k_value, mass_value)
        bubble_trials.append(
            {
                "k": k_value,
                "mass": mass_value,
                "analytic": analytic,
                "feynman_parameter": numerical,
                "relative_error": abs(analytic - numerical) / analytic,
            }
        )
        spectral_value = quad(
            lambda mass_spectral: 1.0
            / (
                4.0
                * math.pi
                * (k_value**2 + mass_spectral**2)
            ),
            2.0 * mass_value,
            np.inf,
            epsabs=1.0e-13,
            epsrel=1.0e-12,
            limit=200,
        )[0]
        bubble_spectral_errors.append(
            abs(analytic - spectral_value) / analytic
        )
    factorization_errors = []
    for k_value in np.logspace(-12.0, 12.0, 97):
        coefficient = response_coefficient(k_value**2, q_value, 1.0)
        factorized = (
            8.0
            * phase_occupation(k_value, q_value, 1.0)
            * pair_bubble(k_value, 0.0)
        )
        factorization_errors.append(
            abs(coefficient - factorized) / coefficient
        )
    reconstruction_errors = []
    density_values = []
    for s_value in np.logspace(-8.0, 8.0, 9):
        exact = response_coefficient(s_value, q_value, 1.0)
        reconstructed = reconstruct_response(s_value, q_value, 1.0)
        reconstruction_errors.append(abs(exact - reconstructed) / exact)
        density_values.append(response_density(s_value, q_value, 1.0))
    hessian_minimum_eigenvalue = math.inf
    hessian_maximum_determinant_error = 0.0
    hessian_maximum_schur_error = 0.0
    for k_value in np.logspace(-6.0, 6.0, 49):
        coefficient = response_coefficient(k_value**2, q_value, 1.0)
        normalized_hessian = np.array(
            [
                [1.0, math.sqrt(amplitude)],
                [
                    math.sqrt(amplitude),
                    1.0 / coefficient + amplitude,
                ],
            ]
        )
        hessian_minimum_eigenvalue = min(
            hessian_minimum_eigenvalue,
            float(np.linalg.eigvalsh(normalized_hessian)[0]),
        )
        determinant = float(np.linalg.det(normalized_hessian))
        hessian_maximum_determinant_error = max(
            hessian_maximum_determinant_error,
            abs(determinant - 1.0 / coefficient)
            / max(1.0 / coefficient, 1.0e-300),
        )
        schur_direct = 1.0 - amplitude / (
            1.0 / coefficient + amplitude
        )
        schur_expected = 1.0 / (1.0 + amplitude * coefficient)
        hessian_maximum_schur_error = max(
            hessian_maximum_schur_error,
            abs(schur_direct - schur_expected) / schur_expected,
        )
    low_momenta = np.logspace(-9.0, -4.0, 60)
    one_minus_zeta = np.array(
        [
            1.0
            / (
                1.0
                + amplitude
                * response_coefficient(k_value**2, q_value, 1.0)
            )
            for k_value in low_momenta
        ]
    )
    effective_kernel = low_momenta**2 * one_minus_zeta
    mixing_slope = logarithmic_slope(low_momenta, one_minus_zeta)
    kernel_slope = logarithmic_slope(low_momenta, effective_kernel)
    passivity_residuals = []
    dressed_imaginary_parts = []
    for real_part in (-10.0, -1.0, 0.0, 1.0, 10.0):
        for imaginary_part in (1.0e-6, 0.01, 1.0, 10.0):
            response = complex(real_part, imaginary_part)
            dressed = response / (1.0 + amplitude * response)
            expected_imaginary = imaginary_part / abs(
                1.0 + amplitude * response
            ) ** 2
            dressed_imaginary_parts.append(dressed.imag)
            passivity_residuals.append(
                abs(dressed.imag - expected_imaginary)
            )
    mass_samples = np.logspace(-8.0, 8.0, 65)
    cumulative_values = [
        pair_mass_cumulative(value, q_value, 1.0)
        for value in mass_samples
    ]
    weight_derivatives = [
        pair_mass_weight_derivative(value, q_value, 1.0)
        for value in mass_samples
    ]
    cumulative_identity_errors = []
    derivative_identity_errors = []
    for mass_value in np.logspace(-6.0, 6.0, 25):
        cumulative = pair_mass_cumulative(mass_value, q_value, 1.0)
        density_cumulative = (
            16.0
            * math.pi
            * mass_value
            * response_density(4.0 * mass_value**2, q_value, 1.0)
        )
        cumulative_identity_errors.append(
            abs(cumulative - density_cumulative) / cumulative
        )
        step = mass_value * 1.0e-5
        finite_difference = (
            pair_mass_cumulative(
                mass_value + step,
                q_value,
                1.0,
            )
            - pair_mass_cumulative(
                mass_value - step,
                q_value,
                1.0,
            )
        ) / (2.0 * step)
        exact_derivative = pair_mass_weight_derivative(
            mass_value,
            q_value,
            1.0,
        )
        derivative_identity_errors.append(
            abs(finite_difference - exact_derivative)
            / abs(exact_derivative)
        )
    threshold_90 = 1.0 / (2.0 * math.tan(0.45 * math.pi))
    threshold_99 = 1.0 / (2.0 * math.tan(0.495 * math.pi))
    k_minimum_ev = HBAR_C_EV_M / (maximum_L_kpc * KPC_M)
    k_maximum_ev = HBAR_C_EV_M / (minimum_L_kpc * KPC_M)
    mass_maximum_90_ev = threshold_90 * k_minimum_ev
    mass_maximum_99_ev = threshold_99 * k_minimum_ev
    current_bubble_ratio_min = (
        2.0
        / math.pi
        * math.atan(k_minimum_ev / (2.0 * REFERENCE_GAP_EV))
    )
    current_bubble_ratio_max = (
        2.0
        / math.pi
        * math.atan(k_maximum_ev / (2.0 * REFERENCE_GAP_EV))
    )
    mu_minimum_ev = mu_times_L * k_minimum_ev
    mu_maximum_ev = mu_times_L * k_maximum_ev
    required_coefficient_minimum_ev = (
        32.0
        * REDUCED_PLANCK_MASS_EV**2
        / (amplitude * mu_maximum_ev)
    )
    required_coefficient_maximum_ev = (
        32.0
        * REDUCED_PLANCK_MASS_EV**2
        / (amplitude * mu_minimum_ev)
    )
    unit_pair_enhancement_minimum = (
        required_coefficient_minimum_ev / mu_maximum_ev
    )
    unit_pair_enhancement_maximum = (
        required_coefficient_maximum_ev / mu_minimum_ev
    )
    fixed_point_dynamic = inputs["result_4958"]["combined_fixed_points"][
        "dynamic_etaN"
    ]
    fixed_point_reference = inputs["result_4958"]["combined_fixed_points"][
        "reference_etaN0"
    ]
    infrared_dynamic = inputs["result_4958"]["endpoint_summary"][
        "dynamic_etaN_N8"
    ]
    relevant_exponent = float(
        inputs["relevant_rows"][0]["critical_exponent_real"]
    )
    tail_one_over_k = fourier_power_coefficient(-1.0)
    tail_k = fourier_power_coefficient(1.0)
    tail_k_cubed = fourier_power_coefficient(3.0)
    return {
        "q": q_value,
        "amplitude": amplitude,
        "mu_times_L": mu_times_L,
        "minimum_L_kpc": minimum_L_kpc,
        "maximum_L_kpc": maximum_L_kpc,
        "bubble_trials": bubble_trials,
        "maximum_bubble_relative_error": max(
            row["relative_error"] for row in bubble_trials
        ),
        "maximum_bubble_spectral_relative_error": max(
            bubble_spectral_errors
        ),
        "maximum_factorization_relative_error": max(factorization_errors),
        "maximum_spectral_reconstruction_relative_error": max(
            reconstruction_errors
        ),
        "minimum_sampled_spectral_density": min(density_values),
        "pair_mass_cumulative_smallest_sample": cumulative_values[0],
        "pair_mass_cumulative_largest_sample": cumulative_values[-1],
        "maximum_pair_mass_weight_derivative": max(weight_derivatives),
        "minimum_pair_mass_weight_derivative": min(weight_derivatives),
        "maximum_pair_cumulative_identity_relative_error": max(
            cumulative_identity_errors
        ),
        "maximum_pair_weight_derivative_relative_error": max(
            derivative_identity_errors
        ),
        "positive_massive_pair_mixture_possible": all(
            value >= 0.0 for value in weight_derivatives
        ),
        "minimum_normalized_Hessian_eigenvalue": hessian_minimum_eigenvalue,
        "maximum_Hessian_determinant_relative_error": (
            hessian_maximum_determinant_error
        ),
        "maximum_Schur_relative_error": hessian_maximum_schur_error,
        "one_minus_zeta_low_k_slope": mixing_slope,
        "effective_kernel_low_k_slope": kernel_slope,
        "minimum_dressed_imaginary_part": min(dressed_imaginary_parts),
        "maximum_passivity_identity_residual": max(passivity_residuals),
        "finite_gap_ratio_90_threshold": threshold_90,
        "finite_gap_ratio_99_threshold": threshold_99,
        "k_minimum_eV": k_minimum_ev,
        "k_maximum_eV": k_maximum_ev,
        "mass_maximum_90_eV": mass_maximum_90_ev,
        "mass_maximum_99_eV": mass_maximum_99_ev,
        "reference_gap_to_99_percent_bound": (
            REFERENCE_GAP_EV / mass_maximum_99_ev
        ),
        "reference_gap_bubble_ratio_minimum": current_bubble_ratio_min,
        "reference_gap_bubble_ratio_maximum": current_bubble_ratio_max,
        "mu_minimum_eV": mu_minimum_ev,
        "mu_maximum_eV": mu_maximum_ev,
        "required_projected_coefficient_minimum_eV": (
            required_coefficient_minimum_ev
        ),
        "required_projected_coefficient_maximum_eV": (
            required_coefficient_maximum_ev
        ),
        "unit_pair_enhancement_minimum": unit_pair_enhancement_minimum,
        "unit_pair_enhancement_maximum": unit_pair_enhancement_maximum,
        "ordered_derivative_bubble_coefficient": 1.0 / 32.0,
        "normalized_required_derivative_coefficient": 32.0 / amplitude,
        "tail_one_over_k_coefficient": tail_one_over_k,
        "tail_k_coefficient": tail_k,
        "tail_k_cubed_coefficient": tail_k_cubed,
        "Cq_tail_coefficient_mu_factored": tail_one_over_k,
        "one_minus_zeta_tail_coefficient_A_mu_factored": tail_k,
        "derivative_bubble_tail_coefficient": tail_k_cubed / 32.0,
        "required_IR_eta": 1.0,
        "required_IR_dimension_4D_continuation": 1.5,
        "required_UV_eta": 1.0 - q_value,
        "required_UV_dimension_4D_continuation": (
            1.0 + (1.0 - q_value) / 2.0
        ),
        "parent_fixed_point_eta_dynamic": float(
            fixed_point_dynamic["eta_psi"]
        ),
        "parent_fixed_point_eta_reference": float(
            fixed_point_reference["eta_psi"]
        ),
        "parent_IR_eta_dynamic": float(
            infrared_dynamic["eta_psi_endpoint"]
        ),
        "parent_relevant_exponent": relevant_exponent,
        "phase_exponent_matches_current_relevant_exponent": close(
            q_value,
            relevant_exponent,
            relative_tolerance=1.0e-3,
        ),
    }


def pair_rows(calculation: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        (
            "P5181_01_definition",
            "equal-mass static pair bubble in three spatial dimensions",
            "B_m(k)=integral d^3q/(2pi)^3/[((q^2+m^2)((q+k)^2+m^2))]",
            "definition",
            "positive Euclidean propagators",
            "DERIVED",
        ),
        (
            "P5181_02_parameterization",
            "Feynman parameter reduction",
            "B_m=(1/8pi) integral_0^1 dx [m^2+x(1-x)k^2]^-1/2",
            "1/(AB)=integral_0^1 dx/[xA+(1-x)B]^2",
            "k>0 and m>=0",
            "DERIVED",
        ),
        (
            "P5181_03_closed_form",
            "exact massive bubble",
            "B_m(k)=atan(k/(2m))/(4pi k)",
            "perform the shifted three-momentum integral and x integral",
            "m>0",
            "DERIVED",
        ),
        (
            "P5181_04_massless",
            "critical threshold",
            "B_0(k)=1/(8|k|)",
            "m->0 in the exact closed form",
            "gapless pair",
            "DERIVED",
        ),
        (
            "P5181_05_gapped_expansion",
            "regular finite-gap infrared limit",
            "B_m=1/(8pi m)-k^2/(96pi m^3)+O(k^4)",
            "Taylor-expand atan(k/(2m))",
            "|k|<<m",
            "DERIVED",
        ),
        (
            "P5181_06_factorization",
            "checkpoint-5148 response",
            "C_q(k^2)=8mu n_q(mu/k) B_0(k)",
            "n_q=mu^q/(k^q+mu^q) gives C_q=mu^(1+q)/[k(k^q+mu^q)]",
            "k>0 and 0<q<=1",
            "DERIVED",
        ),
        (
            "P5181_07_filter",
            "minimal external composite filter",
            "F_q(k)=sqrt(n_q(mu/k)); C_q=8mu F_q^2 B_0",
            "algebraic operator contract",
            "microscopic occupied loop still must derive F_q",
            "EXACT_CONTRACT_NOT_PARENT_OWNED",
        ),
        (
            "P5181_08_filter_flow",
            "logistic composite filter law",
            "d n_q/d ln k=-q n_q(1-n_q)",
            "differentiate n_q(mu/k)",
            "q is the crossover exponent",
            "DERIVED_TARGET",
        ),
        (
            "P5181_09_derivative_bubble",
            "ordered O=(grad psi)^2 pair contraction",
            "D_0_nonlocal=(k^4/4)B_0=|k|^3/32",
            "q.(q+k)=[q^2+(q+k)^2-k^2]/2; local and scaleless pieces subtract",
            "dimensional regularization and contact subtraction",
            "DERIVED_POWER_AND_ORDERED_COEFFICIENT",
        ),
        (
            "P5181_10_Wick_scope",
            "connected composite normalization",
            "full Wick and tensor factors multiply the ordered 1/32 coefficient",
            "operator normalization and metric projection dependent",
            "not licensed to set the parent Hilbert coefficient",
            "PARENT_VERTEX_GATE",
        ),
        (
            "P5181_11_pair_threshold_density",
            "spectral density of one massive pair bubble",
            "rho_Bm(t)=theta(t-4m^2)/(8pi sqrt(t))",
            "integrating from 4m^2 reproduces atan(sqrt(s)/(2m))/(4pi sqrt(s))",
            "positive ordinary pair threshold",
            "DERIVED",
        ),
        (
            "P5181_12_pair_mixture_no_go",
            "full C_q as a positive mixture of ordinary pair bubbles",
            "W(m)=16pi m rho_C(4m^2)=8mu(1+c x)/(1+2c x+x^2), x=(2m/mu)^q",
            "W decreases from 8mu to 0 and dW/dm<0",
            "0<q<=1; c=cos(pi q/2)>=0",
            "POSITIVE_PAIR_MASS_MIXTURE_REJECTED",
        ),
    ]
    return [
        {
            "derivation_id": row[0],
            "object": row[1],
            "exact_expression": row[2],
            "derivation": row[3],
            "domain_or_assumption": row[4],
            "status": row[5],
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
        }
        for row in rows
    ]


def hessian_rows(calculation: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        (
            "H5181_01_normalization",
            "canonical scalar-channel metric variable",
            "u=sqrt(K_h) h",
            "K_h>0",
            "metric quadratic form becomes u^2",
            "DERIVED_NORMALIZATION",
        ),
        (
            "H5181_02_block",
            "positive critical generalized-field Hessian",
            "H=[[1,sqrt(A)],[sqrt(A),C_q^-1+A]] in (u,chi)",
            "A>0 and C_q>0",
            "one exact scalar-channel completion",
            "CONSTRUCTED",
        ),
        (
            "H5181_03_square",
            "complete-square proof",
            "u^2+2sqrt(A)u chi+(C_q^-1+A)chi^2=(u+sqrt(A)chi)^2+C_q^-1 chi^2",
            "A>0 and C_q>0",
            "strict Euclidean positivity for finite k",
            "PROVED",
        ),
        (
            "H5181_04_determinant",
            "principal determinant",
            "det(H)=C_q^-1>0",
            "same conditions",
            "no static scalar ghost in the completed block",
            "PROVED",
        ),
        (
            "H5181_05_Schur",
            "reduced metric inverse kernel",
            "K_eff=K_h-A K_h/(C_q^-1+A)=K_h/(1+A C_q)",
            "integrate chi after solving its linear equation",
            "exact checkpoint-5148 target",
            "PROVED",
        ),
        (
            "H5181_06_mixing",
            "critical mixing fraction",
            "zeta=A C_q/(1+A C_q)",
            "definition zeta=1-K_eff/K_h",
            "zeta->1 in the infrared",
            "PROVED",
        ),
        (
            "H5181_07_IR_residual",
            "critical inverse-kernel residual",
            "for K_h=M_R^2 k^2, K_eff~M_R^2 |k|^3/(A mu)",
            "C_q~mu/|k|",
            "positive k-cubed residual",
            "DERIVED_TARGET",
        ),
        (
            "H5181_08_continuum",
            "causal generalized-field realization",
            "C_R(omega,k)=integral_0^infinity dt rho_C(t)/[k^2+t-(omega+i0)^2]",
            "rho_C(t)>0",
            "positive oscillator continuum",
            "EXISTS",
        ),
        (
            "H5181_09_passivity",
            "dressed retarded response",
            "Im[C_R/(1+A C_R)]=Im(C_R)/|1+A C_R|^2",
            "positive-frequency Im(C_R)>=0",
            "passivity sign is preserved",
            "PROVED",
        ),
        (
            "H5181_10_poles",
            "principal-sheet stability",
            "1+A C_q(z) has no zero off the Stieltjes cut for A>0",
            "Stieltjes C has nonzero signed imaginary part off the real axis and C(s)>0 for s>0",
            "no upper-half-frequency zero in this scalar completion",
            "PROVED_FOR_COMPLETED_SCALAR_CHANNEL",
        ),
        (
            "H5181_11_scope",
            "claim boundary",
            "positive scalar completion does not determine the constrained tensor projector or parent vertex",
            "Jeans, vector, tensor, and gauge blocks remain separate",
            "no full-Hessian or phenomenology claim",
            "OPEN_PARENT_PROJECTION",
        ),
    ]
    return [
        {
            "Hessian_id": row[0],
            "object": row[1],
            "exact_expression": row[2],
            "condition_or_derivation": row[3],
            "consequence": row[4],
            "status": row[5],
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
        }
        for row in rows
    ]


def obstruction_rows(calculation: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        (
            "O5181_01_finite_local",
            "finite local Hessian",
            "every block is analytic in s=k^2 near s=0",
            "finite derivative order and regular coefficients",
            "premise",
        ),
        (
            "O5181_02_gapped_inverse",
            "gapped eliminated block",
            "K_chi(s)^-1 is analytic by the matrix inverse theorem",
            "det K_chi(0) is nonzero",
            "proved",
        ),
        (
            "O5181_03_Schur",
            "finite gapped Schur complement",
            "K_h-B K_chi^-1 B_dagger is an integer-power Taylor series in s",
            "products and sums preserve analyticity",
            "proved",
        ),
        (
            "O5181_04_finite_massless",
            "finite number of local massless fields",
            "the reduced kernel is rational or Laurent in s with integer powers",
            "finite polynomial matrix and adjugate over determinant",
            "proved",
        ),
        (
            "O5181_05_branch_point",
            "required response",
            "|k|=s^(1/2) is a branch point and cannot arise from either finite class",
            "noninteger power",
            "finite-local route rejected",
        ),
        (
            "O5181_06_continuum",
            "necessary mechanism",
            "a gapless continuum, infinite tower accumulation, critical state, or explicit nonlocal parent is required",
            "contrapositive of the preceding theorem",
            "critical continuum selected",
        ),
        (
            "O5181_07_gap_ratio",
            "massive-to-massless pair ratio",
            "B_m/B_0=(2/pi)atan(k/(2m))",
            "exact bubble quotient",
            "derived",
        ),
        (
            "O5181_08_90",
            "90 percent massless corridor",
            "m/k<=1/[2tan(0.45pi)]",
            calculation["finite_gap_ratio_90_threshold"],
            "derived",
        ),
        (
            "O5181_09_99",
            "99 percent massless corridor",
            "m/k<=1/[2tan(0.495pi)]",
            calculation["finite_gap_ratio_99_threshold"],
            "derived",
        ),
        (
            "O5181_10_current_gap",
            "checkpoint-5178 benchmark gap",
            "m_gap=1e-20 eV gives only the recorded bubble-ratio interval across the 5148 corridor",
            (
                f"{calculation['reference_gap_bubble_ratio_minimum']}:"
                f"{calculation['reference_gap_bubble_ratio_maximum']}"
            ),
            "fails critical corridor",
        ),
        (
            "O5181_11_gap_collapse",
            "required environmental transition",
            "m_eff must be below the 99 percent bound at the largest L_eff",
            calculation["mass_maximum_99_eV"],
            "parent law open",
        ),
        (
            "O5181_12_boundary_state",
            "Gaussian boundary covariance alone",
            "equal-time F can change while the free retarded commutator remains fixed",
            "state covariance does not by itself derive C_R",
            "closure unless dynamics derives it",
        ),
    ]
    return [
        {
            "obstruction_id": row[0],
            "object": row[1],
            "statement": row[2],
            "value_or_reason": row[3],
            "status": row[4],
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
        }
        for row in rows
    ]


def scaling_rows(
    calculation: dict[str, Any],
    inputs: dict[str, Any],
) -> list[dict[str, Any]]:
    rows = [
        (
            "S5181_01_IR_dimension",
            "conditional Lorentz-invariant generalized-field continuation",
            "C(s)~s^-1/2",
            "Delta_IR=3/2 and eta_IR=1",
            "exact required continuum scaling",
            "MATCHES_CQ",
        ),
        (
            "S5181_02_UV_dimension",
            "same continuation",
            "C(s)~s^[-(1+q)/2]",
            (
                f"Delta_UV={calculation['required_UV_dimension_4D_continuation']}; "
                f"eta_UV={calculation['required_UV_eta']}"
            ),
            "q-dependent crossover scaling",
            "MATCHES_CQ",
        ),
        (
            "S5181_03_parent_UV_eta",
            "elementary parent psi at dynamic N8 fixed point",
            calculation["parent_fixed_point_eta_dynamic"],
            calculation["required_UV_eta"],
            "does not equal the required generalized-field eta",
            "ELEMENTARY_MATCH_FAILS",
        ),
        (
            "S5181_04_parent_IR_eta",
            "elementary parent psi at GR trajectory endpoint",
            calculation["parent_IR_eta_dynamic"],
            calculation["required_IR_eta"],
            "regular Gaussian infrared scalar",
            "ELEMENTARY_MATCH_FAILS",
        ),
        (
            "S5181_05_composite_scope",
            "reflection-even bilocal G or stress-pair operator",
            "composite anomalous dimension not present in the current stability block",
            "requires Bethe-Salpeter or composite FRG eigenproblem",
            "elementary eta mismatch does not reject the pair channel",
            "OPEN_COMPOSITE_BLOCK",
        ),
        (
            "S5181_06_phase_exponent",
            "logistic occupation exponent",
            calculation["q"],
            calculation["parent_relevant_exponent"],
            "q does not equal the sole current GR-connected relevant exponent",
            "NO_DIRECT_CURRENT_EIGENVALUE_MATCH",
        ),
        (
            "S5181_07_parent_kinetic",
            "minimal motion kinetic term",
            inputs["result_4935"]["parent_motion_action"]["kinetic"],
            "supplies two gapless propagator lines if m_eff reaches zero",
            "pair carrier already exists in the parent field content",
            "PARENT_OWNED_CARRIER",
        ),
        (
            "S5181_08_parent_gap",
            "renormalized motion two-point entry",
            inputs["result_4935"]["renormalized_entry"]["mass_gap"],
            calculation["mass_maximum_99_eV"],
            "formula identifies a gap but no environment-driven collapse law",
            "PARENT_TRANSITION_OPEN",
        ),
        (
            "S5181_09_O4",
            "unique six-derivative motion portal",
            inputs["result_4935"]["six_derivative_entry"]["unique_portal"],
            "not required to obtain the basic massless pair power",
            "checkpoint 5178 already bounds its benchmark contribution",
            "RETAINED_BUT_NOT_THE_CARRIER",
        ),
        (
            "S5181_10_normalization",
            "projected ordered derivative bubble coefficient",
            "g_proj=32 M_R^2/(A mu)",
            (
                f"{calculation['required_projected_coefficient_minimum_eV']}:"
                f"{calculation['required_projected_coefficient_maximum_eV']} eV"
            ),
            "exact in the displayed K_h=M_R^2 k^2 and D_0=k^3/32 convention",
            "PARENT_HILBERT_NORMALIZATION_OPEN",
        ),
        (
            "S5181_11_unit_pair_benchmark",
            "coefficient relative to one mu-normalized ordered pair",
            (
                f"{calculation['unit_pair_enhancement_minimum']}:"
                f"{calculation['unit_pair_enhancement_maximum']}"
            ),
            "large occupation or geometric normalization is necessary",
            "not a strict exclusion until parent field normalization is projected",
            "HARD_NORMALIZATION_GATE",
        ),
    ]
    return [
        {
            "scaling_id": row[0],
            "sector_or_operator": row[1],
            "parent_or_required_value": row[2],
            "comparison_value": row[3],
            "interpretation": row[4],
            "status": row[5],
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
        }
        for row in rows
    ]


def ownership_rows(calculation: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        (
            "G5181_01_kinetic_pair",
            "two motion propagator carrier",
            "PARENT_SIGNED",
            "4935 minimal kinetic term",
            "yes",
        ),
        (
            "G5181_02_Hilbert_entry",
            "metric-to-connected-stress pair entry",
            "PARENT_SIGNED_FORM_ONLY",
            "5178 Pi_R contact plus connected commutator",
            "yes",
        ),
        (
            "G5181_03_IR_power",
            "massless pair gives 1/|k| and derivative pair gives |k|^3",
            "DERIVED",
            "5181 exact loop integral",
            "yes",
        ),
        (
            "G5181_04_full_crossover",
            "F_q(k)^2=n_q(mu/k)",
            "OPEN_PARENT_DYNAMICS",
            "positive massive-pair averaging is rejected",
            "no",
        ),
        (
            "G5181_05_q",
            "q=0.77 composite crossover exponent",
            "EMPIRICAL_INPUT",
            "5148 phase-flow lock",
            "no",
        ),
        (
            "G5181_06_mu",
            "environmental critical scale mu",
            "EMPIRICAL_INPUT",
            "5148 mu-times-L fit",
            "no",
        ),
        (
            "G5181_07_gap",
            "m_eff sufficiently below galactic k",
            "CURRENT_BENCHMARK_FAILS",
            calculation["mass_maximum_99_eV"],
            "no",
        ),
        (
            "G5181_08_gap_law",
            "environmental gap collapse or critical formation",
            "OPEN_PARENT_DYNAMICS",
            "5180 controlled X2-X3 interactions cannot provide it",
            "no",
        ),
        (
            "G5181_09_cross_block",
            "B^2=A K_h in the normalized scalar Hessian",
            "CONSTRUCTED_NOT_PARENT_DERIVED",
            "needed for exact Schur response",
            "no",
        ),
        (
            "G5181_10_amplitude",
            "A from Hilbert pair projection",
            "EMPIRICAL_INPUT",
            calculation["amplitude"],
            "no",
        ),
        (
            "G5181_11_stiffness",
            "local k^2 term reaches unit cancellation while |k|^3 remains positive",
            "OPEN_PARENT_RENORMALIZATION",
            "criticality condition",
            "no",
        ),
        (
            "G5181_12_tensor_sign",
            "constraint-dressed scalar metric projection and seagull sign",
            "OPEN_PARENT_PROJECTION",
            "ordered scalar bubble alone cannot sign it",
            "no",
        ),
        (
            "G5181_13_static_positivity",
            "positive scalar full-Hessian completion",
            "PROVED_COMPATIBLE",
            "complete-square and determinant theorem",
            "yes",
        ),
        (
            "G5181_14_causality",
            "positive retarded generalized continuum",
            "PROVED_COMPATIBLE",
            "Stieltjes density and dressed passivity",
            "yes",
        ),
        (
            "G5181_15_local_cog",
            "local GR/Newton/Maxwell branch",
            "UNCHANGED",
            "no local equations or public files modified",
            "yes",
        ),
    ]
    return [
        {
            "gate_id": row[0],
            "required_clause": row[1],
            "status": row[2],
            "evidence_or_value": row[3],
            "closed_at_5181": row[4],
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
        }
        for row in rows
    ]


def decision_rows(calculation: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        (
            "D5181_01_kernel",
            "required infrared susceptibility",
            "DERIVED_AS_MASSLESS_PAIR_BUBBLE",
            "C_q=8mu n_q B_0 and B_0=1/(8|k|)",
        ),
        (
            "D5181_02_residual",
            "required inverse-kernel power",
            "DERIVED_AS_DERIVATIVE_PAIR_POWER",
            "D_0_nonlocal=|k|^3/32 after local/contact subtraction",
        ),
        (
            "D5181_03_positive_completion",
            "static and causal scalar completion",
            "EXISTS_WITHOUT_GHOST",
            "positive complete square, determinant, and retarded passivity",
        ),
        (
            "D5181_04_finite_local",
            "finite local gapped or finite massless completion",
            "REJECTED",
            "cannot generate the square-root branch point",
        ),
        (
            "D5181_05_pair_mixture",
            "full q crossover from positive ordinary massive pair weights",
            "REJECTED",
            "required cumulative threshold weight decreases from 8mu to zero",
        ),
        (
            "D5181_06_parent_carrier",
            "minimal MTS field content",
            "KINEMATIC_CARRIER_PRESENT",
            "kinetic motion field and connected Hilbert stress pair already exist",
        ),
        (
            "D5181_07_parent_ownership",
            "critical state, logistic filter, cross normalization and tensor sign",
            "OPEN_NOT_CLAIMED",
            "must be calculated from the actual parent CTP/constraint Hessian",
        ),
        (
            "D5181_08_next",
            "next derivation",
            "CALCULATE_CONSTRAINT_DRESSED_HILBERT_STRESS_PAIR_VERTEX",
            "test sign and coefficient, then derive or reject environmental gap collapse",
        ),
        (
            "D5181_09_claim",
            "galaxy, local GR, cosmology and full MTS",
            "NO_NEW_CLAIM",
            ROUTE_DECISION,
        ),
    ]
    return [
        {
            "decision_id": row[0],
            "question": row[1],
            "decision": row[2],
            "reason_or_next_action": row[3],
            "checkpoint_marker": MARKER,
            "valid_for_local_GR_claim": False,
            "valid_for_galaxy_claim": False,
            "valid_for_cosmology_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for row in rows
    ]


def validation_row(
    validation_id: str,
    description: str,
    passed: bool,
    actual: Any,
    expected: Any,
) -> dict[str, Any]:
    return {
        "validation_id": validation_id,
        "description": description,
        "passed": bool(passed),
        "actual": actual,
        "expected": expected,
        "checkpoint_marker": MARKER,
    }


def write_document(result: dict[str, Any]) -> None:
    summary = result["summary"]
    DOCUMENT.write_text(
        f"""# 5181 - Critical pair bubble, positive Hessian completion and parent ownership gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

This checkpoint closes a real mathematical gap rather than adding another
target ledger. The infrared kernel required at checkpoints 5148-5149 is an
exact, familiar critical object:

```text
B_0(k)=integral d^3q/(2pi)^3 [q^2(q+k)^2]^-1=1/(8|k|),

C_q(k^2)=8 mu n_q(mu/k) B_0(k).
```

Thus the required `1/|k|` is the massless two-particle motion bubble and not
an arbitrary fitted nonlocal power. A positive complete scalar Hessian exists
whose exact Schur complement yields `K_eff=K_h/(1+A C_q)`, and the positive
Stieltjes density supplies a causal passive continuum. No ghost is required
by this scalar mechanism.

The result is not yet a parent derivation. The whole `q={summary['q']}`
crossover cannot be a positive average of ordinary massive pair bubbles, the
current parent benchmark is far too gapped, and the required Hilbert-pair
normalization and constrained tensor sign have not been calculated.
Consequently no galaxy, local-GR, cosmology or full-MTS claim is promoted.

## 1. Exact critical pair bubble

For two equal Euclidean static propagators in three spatial dimensions,

```text
B_m(k)=integral d^3q/(2pi)^3
       1/[(q^2+m^2)((q+k)^2+m^2)].
```

Feynman parameterization and the shifted momentum integral give

```text
B_m(k)
 =1/(8pi) integral_0^1 dx [m^2+x(1-x)k^2]^-1/2
 =atan(|k|/(2m))/(4pi |k|).
```

Therefore

```text
B_0(k)=1/(8|k|),

B_m(k)=1/(8pi m)-k^2/(96pi m^3)+O(k^4),  |k|<<m.
```

The independent numerical Feynman-parameter check has maximum relative error
`{summary['maximum_bubble_relative_error']}`.

Checkpoint 5148's occupation is

```text
n_q(mu/k)=mu^q/(k^q+mu^q),
```

so the full target factorizes identically:

```text
C_q(k^2)
 =mu^(1+q)/[|k|(|k|^q+mu^q)]
 =8mu n_q(mu/k) B_0(k).
```

The maximum factorization residual over 24 momentum decades is
`{summary['maximum_factorization_relative_error']}`. Equivalently, the
required filtered pair operator has external form factor

```text
F_q(k)=sqrt(n_q(mu/k)),
d n_q/d ln k=-q n_q(1-n_q).
```

This is now an exact operator contract. It is not yet proof that the MTS
nonequilibrium state generates that filter inside the loop.

## 2. A new pair-mixture no-go

One massive pair bubble has the positive threshold density

```text
rho_Bm(t)=theta(t-4m^2)/(8pi sqrt(t)).
```

If `C_q` were a positive superposition `integral dm w(m)B_m`, positivity
would require the cumulative weight

```text
W(m)=integral_0^m dm' w(m')
    =16pi m rho_C(4m^2)
```

to be nonnegative and nondecreasing. Instead, with
`x=(2m/mu)^q` and `c=cos(pi q/2)`,

```text
W(m)=8mu(1+c x)/(1+2c x+x^2),

dW/dm
 =-8mu q x[c+2x+c x^2]/
   {{m(1+2c x+x^2)^2}} <0.
```

It decreases from `8mu` to zero. The full crossover is therefore **not** a
positive mass average of ordinary free pair thresholds. The infrared carrier
is a massless pair, but the factor `n_q` must be generated by a running
composite vertex, an occupied-state kernel, or equivalent parent dynamics.

This distinction prevents the exact infrared observation from being
overstated as a microscopic derivation of the entire response.

## 3. Derivative pair and the required residual

For the ordered derivative composite `O=(grad psi)^2`,

```text
q.(q+k)=[q^2+(q+k)^2-k^2]/2.
```

After the local/scaleless contact terms are subtracted, its massless pair
bubble is

```text
D_0,nonlocal=(k^4/4)B_0=|k|^3/32.
```

Wick multiplicity, tensor projectors, seagulls and the action normalization
must still be supplied by the actual Hilbert-stress vertex. In the displayed
convention

```text
K_h=M_R^2 k^2,
K_eff~M_R^2 |k|^3/(A mu),
```

the required ordered projected multiplier is

```text
g_proj=32 M_R^2/(A mu).
```

Across the checkpoint-5148 scale corridor and using the reduced-Planck
benchmark, this is
`{summary['required_projected_coefficient_minimum_eV']}` to
`{summary['required_projected_coefficient_maximum_eV']} eV`. Relative to a
single `mu`-normalized ordered pair, the benchmark enhancement is
`{summary['unit_pair_enhancement_minimum']}` to
`{summary['unit_pair_enhancement_maximum']}`. This is a hard normalization
gate, not a strict rejection, because the constrained geometric-motion field
normalization has not yet been projected.

## 4. Positive full scalar Hessian

Write the canonically normalized metric-channel variable as
`u=sqrt(K_h)h`. For `A>0` and `C_q>0`, consider

```text
H(u,chi) =
  [[1,       sqrt(A)],
   [sqrt(A), C_q^-1+A]].
```

Its quadratic form is exactly

```text
(u+sqrt(A)chi)^2+C_q^-1 chi^2,
```

and

```text
det H=C_q^-1>0.
```

Eliminating `chi` gives

```text
K_eff
 =K_h-A K_h/(C_q^-1+A)
 =K_h/(1+A C_q),

zeta=A C_q/(1+A C_q).
```

The minimum sampled normalized eigenvalue is
`{summary['minimum_normalized_Hessian_eigenvalue']}`. The measured infrared
slopes are

```text
1-zeta : {summary['one_minus_zeta_low_k_slope']}
K_eff  : {summary['effective_kernel_low_k_slope']}.
```

The positive density from checkpoint 5149 realizes `C_q` as a generalized
oscillator continuum. On the positive-frequency cut,

```text
Im[C_R/(1+A C_R)]
 =Im(C_R)/|1+A C_R|^2 >=0.
```

The maximum numerical identity residual is
`{summary['maximum_passivity_identity_residual']}`. This proves compatibility
with scalar static positivity and retarded passivity. It does not replace the
constraint-dressed scalar/vector/tensor Hessian calculation.

## 5. Finite-local obstruction and gap corridor

A finite local Hessian is polynomial or analytic in `s=k^2`. If an eliminated
block is gapped, its inverse and Schur complement are analytic at `s=0`. If a
finite number of local fields is massless, the inverse is rational or Laurent
in `s`, still with integer powers. Neither class can create the branch point
`s^(1/2)=|k|`.

The continuum is therefore necessary: it cannot be replaced by a finite set
of regular local auxiliary fields.

The exact finite-gap suppression is

```text
B_m/B_0=(2/pi)atan(k/(2m)).
```

To retain 90 or 99 percent of the massless bubble requires

```text
m/k <= {summary['finite_gap_ratio_90_threshold']}   (90 percent),
m/k <= {summary['finite_gap_ratio_99_threshold']}   (99 percent).
```

At the largest fitted `L_eff={summary['maximum_L_kpc']} kpc`, the 99-percent
bound is

```text
m_eff <= {summary['mass_maximum_99_eV']} eV.
```

The checkpoint-5178 benchmark `m_gap=1e-20 eV` is larger by
`{summary['reference_gap_to_99_percent_bound']}` and retains only
`{summary['reference_gap_bubble_ratio_minimum']}` to
`{summary['reference_gap_bubble_ratio_maximum']}` of the massless bubble over
the fitted corridor. Checkpoint 5180 already proves that the controlled
`X2-X3` interaction branch cannot generate this collapse.

## 6. What the current parent does and does not own

The parent already owns two indispensable kinematic ingredients:

1. the minimal motion kinetic term supplies the two propagator lines;
2. the Hilbert variation supplies the metric-to-connected-stress pair entry.

The massless pair power therefore does not require a new field or the tiny
`O4=C^2(nabla psi)^2` repair. But the selected parent branch currently has a
regular gap and elementary anomalous dimensions

```text
eta_psi,UV={summary['parent_fixed_point_eta_dynamic']},
eta_psi,IR={summary['parent_IR_eta_dynamic']}.
```

Conditional on a Lorentz-invariant generalized-field continuation, `C_q`
would require

```text
eta_IR=1,
eta_UV=1-q={summary['required_UV_eta']}.
```

That does not match the elementary scalar. It does **not** reject the
reflection-even pair route because the current truncation has never solved
the bilocal/composite Bethe-Salpeter eigenproblem. Likewise, the fitted
`q={summary['q']}` does not equal the current sole GR-connected relevant
exponent `{summary['parent_relevant_exponent']}`; the composite stability
block is the precise missing calculation.

## 7. Real-space tails

Away from contact terms in three dimensions,

```text
FT^-1[1/|k|]=1/(2pi^2 r^2),
FT^-1[|k|]=-1/(pi^2 r^4),
FT^-1[|k|^3]=12/(pi^2 r^6).
```

Hence

```text
C_q(r)~mu/(2pi^2 r^2),
1-zeta(r)~-1/(A mu pi^2 r^4),
D_0(r)~3/(8pi^2 r^6).
```

These are distributional, contact-subtracted equal-time statements. They
make the needed long-range state structure explicit.

## Claim boundary and next derivation

Checkpoint 5181 establishes:

- the exact critical pair carrier of the required infrared power;
- the exact phase-filter factorization;
- a no-go for positive ordinary massive-pair averaging of the full crossover;
- a positive and passive scalar Hessian completion;
- the exact finite-gap corridor and normalization target.

It does **not** establish:

- an environment-derived motion gap collapse;
- the composite logistic flow and values of `q`, `mu` and `A`;
- the constrained Hilbert-stress pair coefficient, seagull cancellation or
  tensor sign;
- a galaxy, local-GR, cosmology or full-MTS pass.

The next calculation is therefore no longer vague. It must evaluate the
constraint-dressed Hilbert stress-to-bilocal pair vertex from the existing
parent 2PI Hessian, including contact terms, and test whether it returns the
stabilizing `|k|^3` sign and the exact coefficient
`32M_R^2/(A mu)`. In parallel, the parent flow must derive or reject a
galaxy-environment critical-gap transition and the logistic composite
eigenmode. If those fail, this route is rejected rather than renamed as
closure.

## Machine-readable outputs

- `source-intake/functional_rg/5181/critical_pair_bubble_derivation.csv`
- `source-intake/functional_rg/5181/positive_critical_Hessian_completion.csv`
- `source-intake/functional_rg/5181/finite_gap_and_locality_obstruction.csv`
- `source-intake/functional_rg/5181/critical_scaling_and_parent_match.csv`
- `source-intake/functional_rg/5181/critical_pair_vertex_ownership_gate.csv`
- `source-intake/functional_rg/5181/critical_continuum_route_decision.csv`
- `source-intake/functional_rg/5181/source_provenance.csv`
- `source-intake/functional_rg/5181/critical_pair_completion_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5181_VALIDATION.csv`

Route decision:

```text
{ROUTE_DECISION}
```
""",
        encoding="utf-8",
    )


def run(dry_run: bool) -> dict[str, Any]:
    paths = source_paths()
    missing_paths = [
        str(path) for path in paths.values() if not path.is_file()
    ]
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
    calculation = calculate(inputs)
    generated_pair_rows = pair_rows(calculation)
    generated_hessian_rows = hessian_rows(calculation)
    generated_obstruction_rows = obstruction_rows(calculation)
    generated_scaling_rows = scaling_rows(calculation, inputs)
    generated_ownership_rows = ownership_rows(calculation)
    generated_decision_rows = decision_rows(calculation)
    all_theory_rows = (
        generated_pair_rows
        + generated_hessian_rows
        + generated_obstruction_rows
        + generated_scaling_rows
        + generated_ownership_rows
        + generated_decision_rows
    )
    summary = {
        **calculation,
        "critical_IR_pair_power_derived": True,
        "full_Cq_positive_Stieltjes_continuum": True,
        "full_Cq_positive_massive_pair_mixture": False,
        "positive_static_scalar_Hessian_completion": True,
        "retarded_passivity_completion": True,
        "finite_local_completion_can_generate_abs_k": False,
        "parent_kinetic_pair_carrier": True,
        "parent_composite_logistic_flow_derived": False,
        "parent_environmental_gap_collapse_derived": False,
        "parent_Hilbert_pair_normalization_derived": False,
        "parent_constraint_dressed_tensor_sign_derived": False,
        "local_GR_Newton_Maxwell_branch_modified": False,
        "valid_for_local_GR_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_cosmology_claim": False,
        "valid_for_full_MTS_claim": False,
        "route_decision": ROUTE_DECISION,
    }
    dry_checks = [
        validation_row(
            "V5181_01_sources_exist",
            "all cited source paths exist",
            not missing_paths,
            len(paths) - len(missing_paths),
            len(paths),
        ),
        validation_row(
            "V5181_02_source_locks",
            "all source hashes match their immutable locks",
            source_hashes_before == SOURCE_HASH_LOCKS,
            sum(
                source_hashes_before.get(name) == digest
                for name, digest in SOURCE_HASH_LOCKS.items()
            ),
            len(SOURCE_HASH_LOCKS),
        ),
        validation_row(
            "V5181_03_source_signatures",
            "all source clauses needed by the derivation are present",
            all(signatures.values()),
            sum(signatures.values()),
            len(signatures),
        ),
        validation_row(
            "V5181_04_formal_lock",
            "formalization-workbench matches its protected digest",
            formal_before == FORMAL_DIGEST_LOCK,
            formal_before,
            FORMAL_DIGEST_LOCK,
        ),
        validation_row(
            "V5181_05_5176_lock",
            "checkpoint 5176 matches its immutable tree digest",
            checkpoint_5176_before == CHECKPOINT_5176_TREE_LOCK,
            checkpoint_5176_before,
            CHECKPOINT_5176_TREE_LOCK,
        ),
        validation_row(
            "V5181_06_q_lock",
            "the phase exponent is inherited exactly from checkpoint 5148",
            close(calculation["q"], 0.77),
            calculation["q"],
            0.77,
        ),
        validation_row(
            "V5181_07_amplitude_lock",
            "the geometric-mean amplitude is inherited from checkpoint 5148",
            close(
                calculation["amplitude"],
                1.0691523388681814,
            ),
            calculation["amplitude"],
            1.0691523388681814,
        ),
        validation_row(
            "V5181_08_bubble_integral",
            "the closed massive bubble matches independent Feynman integration",
            calculation["maximum_bubble_relative_error"] < 2.0e-12,
            calculation["maximum_bubble_relative_error"],
            "<2e-12",
        ),
        validation_row(
            "V5181_08b_bubble_spectral",
            "the positive massive-pair threshold density reconstructs Bm",
            calculation["maximum_bubble_spectral_relative_error"]
            < 2.0e-12,
            calculation["maximum_bubble_spectral_relative_error"],
            "<2e-12",
        ),
        validation_row(
            "V5181_09_massless_limit",
            "the closed bubble has B0=1/(8k)",
            close(pair_bubble(3.0, 0.0), 1.0 / 24.0),
            pair_bubble(3.0, 0.0),
            1.0 / 24.0,
        ),
        validation_row(
            "V5181_10_gapped_expansion",
            "the finite-gap bubble agrees with its analytic low-k expansion",
            close(
                pair_bubble(1.0e-4, 1.0),
                1.0 / (8.0 * math.pi)
                - 1.0e-8 / (96.0 * math.pi),
                relative_tolerance=1.0e-12,
            ),
            pair_bubble(1.0e-4, 1.0),
            1.0 / (8.0 * math.pi)
            - 1.0e-8 / (96.0 * math.pi),
        ),
        validation_row(
            "V5181_11_Cq_factorization",
            "Cq equals eight mu times occupation times the massless pair bubble",
            calculation["maximum_factorization_relative_error"] < 1.0e-14,
            calculation["maximum_factorization_relative_error"],
            "<1e-14",
        ),
        validation_row(
            "V5181_12_spectral_reconstruction",
            "the positive density reconstructs Cq over sixteen s decades",
            calculation["maximum_spectral_reconstruction_relative_error"]
            < 1.0e-9,
            calculation["maximum_spectral_reconstruction_relative_error"],
            "<1e-9",
        ),
        validation_row(
            "V5181_13_density_positive",
            "the sampled Cq Stieltjes density is positive",
            calculation["minimum_sampled_spectral_density"] > 0.0,
            calculation["minimum_sampled_spectral_density"],
            ">0",
        ),
        validation_row(
            "V5181_14_pair_cumulative_limits",
            "ordinary-pair cumulative weight falls from near 8mu toward zero",
            (
                calculation["pair_mass_cumulative_smallest_sample"] > 7.99
                and calculation["pair_mass_cumulative_largest_sample"]
                < 1.0e-5
            ),
            [
                calculation["pair_mass_cumulative_smallest_sample"],
                calculation["pair_mass_cumulative_largest_sample"],
            ],
            "[>7.99,<1e-5]",
        ),
        validation_row(
            "V5181_15_pair_weight_negative",
            "the inferred ordinary-pair mass weight is strictly negative",
            calculation["maximum_pair_mass_weight_derivative"] < 0.0,
            calculation["maximum_pair_mass_weight_derivative"],
            "<0",
        ),
        validation_row(
            "V5181_15b_pair_weight_inversion",
            "the cumulative pair-weight inversion and derivative are independently checked",
            (
                calculation[
                    "maximum_pair_cumulative_identity_relative_error"
                ]
                < 1.0e-12
                and calculation[
                    "maximum_pair_weight_derivative_relative_error"
                ]
                < 1.0e-5
            ),
            [
                calculation[
                    "maximum_pair_cumulative_identity_relative_error"
                ],
                calculation[
                    "maximum_pair_weight_derivative_relative_error"
                ],
            ],
            "[<1e-12,<1e-5]",
        ),
        validation_row(
            "V5181_16_positive_pair_mixture_no_go",
            "the full q crossover is not a positive massive-pair mixture",
            not calculation["positive_massive_pair_mixture_possible"],
            calculation["positive_massive_pair_mixture_possible"],
            False,
        ),
        validation_row(
            "V5181_17_derivative_bubble",
            "the ordered derivative bubble has exact coefficient 1/32",
            close(
                calculation["ordered_derivative_bubble_coefficient"],
                0.03125,
            ),
            calculation["ordered_derivative_bubble_coefficient"],
            0.03125,
        ),
        validation_row(
            "V5181_18_Hessian_eigenvalues",
            "the sampled normalized completed Hessian is positive definite",
            calculation["minimum_normalized_Hessian_eigenvalue"] > 0.0,
            calculation["minimum_normalized_Hessian_eigenvalue"],
            ">0",
        ),
        validation_row(
            "V5181_19_Hessian_determinant",
            "the completed determinant equals Cq inverse",
            calculation["maximum_Hessian_determinant_relative_error"]
            < 1.0e-9,
            calculation["maximum_Hessian_determinant_relative_error"],
            "<1e-9",
        ),
        validation_row(
            "V5181_20_Schur_identity",
            "the direct Schur complement equals 1/(1+A Cq)",
            calculation["maximum_Schur_relative_error"] < 1.0e-9,
            calculation["maximum_Schur_relative_error"],
            "<1e-9",
        ),
        validation_row(
            "V5181_21_mixing_slope",
            "one minus zeta has the required infrared unit slope",
            close(
                calculation["one_minus_zeta_low_k_slope"],
                1.0,
                relative_tolerance=1.0e-3,
            ),
            calculation["one_minus_zeta_low_k_slope"],
            1.0,
        ),
        validation_row(
            "V5181_22_kernel_slope",
            "Keff has the required infrared cubic slope",
            close(
                calculation["effective_kernel_low_k_slope"],
                3.0,
                relative_tolerance=1.0e-3,
            ),
            calculation["effective_kernel_low_k_slope"],
            3.0,
        ),
        validation_row(
            "V5181_23_passivity",
            "dressing preserves the positive imaginary response sign",
            (
                calculation["minimum_dressed_imaginary_part"] > 0.0
                and calculation["maximum_passivity_identity_residual"]
                < 1.0e-12
            ),
            [
                calculation["minimum_dressed_imaginary_part"],
                calculation["maximum_passivity_identity_residual"],
            ],
            "[>0,<1e-12]",
        ),
        validation_row(
            "V5181_24_gap_90",
            "the exact 90-percent mass-to-momentum threshold is reproduced",
            close(
                calculation["finite_gap_ratio_90_threshold"],
                0.07919222016226816,
            ),
            calculation["finite_gap_ratio_90_threshold"],
            0.07919222016226816,
        ),
        validation_row(
            "V5181_25_gap_99",
            "the exact 99-percent mass-to-momentum threshold is reproduced",
            close(
                calculation["finite_gap_ratio_99_threshold"],
                0.007854627661832444,
            ),
            calculation["finite_gap_ratio_99_threshold"],
            0.007854627661832444,
        ),
        validation_row(
            "V5181_26_current_gap_ratio",
            "the current benchmark gap strongly suppresses the pair corridor",
            calculation["reference_gap_bubble_ratio_maximum"] < 1.0e-6,
            calculation["reference_gap_bubble_ratio_maximum"],
            "<1e-6",
        ),
        validation_row(
            "V5181_27_gap_reduction",
            "99-percent criticality needs more than ten orders of gap reduction",
            calculation["reference_gap_to_99_percent_bound"] > 1.0e10,
            calculation["reference_gap_to_99_percent_bound"],
            ">1e10",
        ),
        validation_row(
            "V5181_28_fourier_one_over_k",
            "the three-dimensional one-over-k tail coefficient is exact",
            close(
                calculation["tail_one_over_k_coefficient"],
                1.0 / (2.0 * math.pi**2),
            ),
            calculation["tail_one_over_k_coefficient"],
            1.0 / (2.0 * math.pi**2),
        ),
        validation_row(
            "V5181_29_fourier_k",
            "the contact-subtracted absolute-k tail coefficient is exact",
            close(
                calculation["tail_k_coefficient"],
                -1.0 / math.pi**2,
            ),
            calculation["tail_k_coefficient"],
            -1.0 / math.pi**2,
        ),
        validation_row(
            "V5181_30_fourier_k3",
            "the contact-subtracted k-cubed tail coefficient is exact",
            close(
                calculation["tail_k_cubed_coefficient"],
                12.0 / math.pi**2,
            ),
            calculation["tail_k_cubed_coefficient"],
            12.0 / math.pi**2,
        ),
        validation_row(
            "V5181_31_scaling_dimensions",
            "the conditional generalized-field dimensions follow from Cq",
            (
                close(calculation["required_IR_eta"], 1.0)
                and close(calculation["required_IR_dimension_4D_continuation"], 1.5)
                and close(calculation["required_UV_eta"], 0.23)
                and close(
                    calculation["required_UV_dimension_4D_continuation"],
                    1.115,
                )
            ),
            [
                calculation["required_IR_eta"],
                calculation["required_IR_dimension_4D_continuation"],
                calculation["required_UV_eta"],
                calculation["required_UV_dimension_4D_continuation"],
            ],
            [1.0, 1.5, 0.23, 1.115],
        ),
        validation_row(
            "V5181_32_elementary_eta_mismatch",
            "the current elementary psi eta does not fake the composite match",
            (
                abs(
                    calculation["parent_fixed_point_eta_dynamic"]
                    - calculation["required_UV_eta"]
                )
                > 0.1
                and abs(
                    calculation["parent_IR_eta_dynamic"]
                    - calculation["required_IR_eta"]
                )
                > 0.9
            ),
            [
                calculation["parent_fixed_point_eta_dynamic"],
                calculation["parent_IR_eta_dynamic"],
            ],
            "not [0.23,1]",
        ),
        validation_row(
            "V5181_33_relevant_exponent",
            "q is not silently identified with the current relevant mode",
            not calculation[
                "phase_exponent_matches_current_relevant_exponent"
            ],
            [
                calculation["q"],
                calculation["parent_relevant_exponent"],
            ],
            "different",
        ),
        validation_row(
            "V5181_34_parent_carrier",
            "the parent kinetic and O4 source clauses are locked",
            (
                signatures["4935_parent_kinetic"]
                and signatures["4935_O4_unique"]
                and signatures["5178_stress_kernel"]
            ),
            [
                signatures["4935_parent_kinetic"],
                signatures["4935_O4_unique"],
                signatures["5178_stress_kernel"],
            ],
            [True, True, True],
        ),
        validation_row(
            "V5181_35_normalization_gate",
            "a unit mu-normalized pair is far below the required stiffness",
            calculation["unit_pair_enhancement_minimum"] > 1.0e107,
            calculation["unit_pair_enhancement_minimum"],
            ">1e107",
        ),
        validation_row(
            "V5181_36_5180_no_repair",
            "the controlled X2-X3 route remains unable to close the gap",
            (
                not inputs["result_5180"]["summary"][
                    "controlled_collision_repair"
                ]
                and not inputs["result_5180"]["summary"][
                    "regular_clustering_gap_closure"
                ]
            ),
            [
                inputs["result_5180"]["summary"][
                    "controlled_collision_repair"
                ],
                inputs["result_5180"]["summary"][
                    "regular_clustering_gap_closure"
                ],
            ],
            [False, False],
        ),
        validation_row(
            "V5181_37_finite_local_no_go",
            "finite local completion is not promoted as an abs-k mechanism",
            not summary["finite_local_completion_can_generate_abs_k"],
            summary["finite_local_completion_can_generate_abs_k"],
            False,
        ),
        validation_row(
            "V5181_38_parent_open",
            "all four parent-ownership clauses remain explicitly open",
            not any(
                summary[key]
                for key in (
                    "parent_composite_logistic_flow_derived",
                    "parent_environmental_gap_collapse_derived",
                    "parent_Hilbert_pair_normalization_derived",
                    "parent_constraint_dressed_tensor_sign_derived",
                )
            ),
            [
                summary["parent_composite_logistic_flow_derived"],
                summary["parent_environmental_gap_collapse_derived"],
                summary["parent_Hilbert_pair_normalization_derived"],
                summary["parent_constraint_dressed_tensor_sign_derived"],
            ],
            [False, False, False, False],
        ),
        validation_row(
            "V5181_39_all_rows_nonclaim",
            "all generated theory rows remain full-MTS nonclaims",
            all(
                not parse_bool(row["valid_for_full_MTS_claim"])
                for row in all_theory_rows
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
                    PAIR_CSV,
                    HESSIAN_CSV,
                    OBSTRUCTION_CSV,
                    SCALING_CSV,
                    OWNERSHIP_CSV,
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

    write_csv(PAIR_CSV, generated_pair_rows)
    write_csv(HESSIAN_CSV, generated_hessian_rows)
    write_csv(OBSTRUCTION_CSV, generated_obstruction_rows)
    write_csv(SCALING_CSV, generated_scaling_rows)
    write_csv(OWNERSHIP_CSV, generated_ownership_rows)
    write_csv(DECISION_CSV, generated_decision_rows)
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
        PAIR_CSV,
        HESSIAN_CSV,
        OBSTRUCTION_CSV,
        SCALING_CSV,
        OWNERSHIP_CSV,
        DECISION_CSV,
        PROVENANCE_CSV,
    )
    output_text = "\n".join(
        path.read_text(encoding="utf-8") for path in output_tables
    )
    output_payload_digest = hashlib.sha256(
        output_text.encode("utf-8")
    ).hexdigest()
    full_checks = dry_checks + [
        validation_row(
            "V5181_40_sources_read_only",
            "all source hashes remain unchanged",
            source_hashes_before == source_hashes_after,
            sum(
                source_hashes_before[name] == source_hashes_after[name]
                for name in paths
            ),
            len(paths),
        ),
        validation_row(
            "V5181_41_formal_after",
            "formalization-workbench remains protected after execution",
            formal_after == formal_before == FORMAL_DIGEST_LOCK,
            formal_after,
            FORMAL_DIGEST_LOCK,
        ),
        validation_row(
            "V5181_42_5176_after",
            "checkpoint 5176 remains immutable after execution",
            checkpoint_5176_after
            == checkpoint_5176_before
            == CHECKPOINT_5176_TREE_LOCK,
            checkpoint_5176_after,
            CHECKPOINT_5176_TREE_LOCK,
        ),
        validation_row(
            "V5181_43_output_rows",
            "all generated evidence tables have exact row counts",
            [
                len(generated_pair_rows),
                len(generated_hessian_rows),
                len(generated_obstruction_rows),
                len(generated_scaling_rows),
                len(generated_ownership_rows),
                len(generated_decision_rows),
                len(provenance_rows),
            ]
            == [12, 11, 12, 11, 15, 9, len(paths)],
            [
                len(generated_pair_rows),
                len(generated_hessian_rows),
                len(generated_obstruction_rows),
                len(generated_scaling_rows),
                len(generated_ownership_rows),
                len(generated_decision_rows),
                len(provenance_rows),
            ],
            [12, 11, 12, 11, 15, 9, len(paths)],
        ),
        validation_row(
            "V5181_44_no_placeholders",
            "generated evidence contains no placeholder marker",
            "MISSING_" not in output_text,
            "MISSING_" in output_text,
            False,
        ),
        validation_row(
            "V5181_45_decision_unique",
            "exactly one row selects the next parent calculation",
            sum(
                row["decision"]
                == "CALCULATE_CONSTRAINT_DRESSED_HILBERT_STRESS_PAIR_VERTEX"
                for row in generated_decision_rows
            )
            == 1,
            sum(
                row["decision"]
                == "CALCULATE_CONSTRAINT_DRESSED_HILBERT_STRESS_PAIR_VERTEX"
                for row in generated_decision_rows
            ),
            1,
        ),
        validation_row(
            "V5181_46_local_unchanged",
            "local GR/Newton/Maxwell branch remains unchanged",
            not summary["local_GR_Newton_Maxwell_branch_modified"],
            summary["local_GR_Newton_Maxwell_branch_modified"],
            False,
        ),
        validation_row(
            "V5181_47_full_nonclaim",
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
        "output_payload_sha256": output_payload_digest,
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
            "Derive the critical pair bubble, construct a positive causal "
            "Hessian completion, and gate parent ownership."
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
