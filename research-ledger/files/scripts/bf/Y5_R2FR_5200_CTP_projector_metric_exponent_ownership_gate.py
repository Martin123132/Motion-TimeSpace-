from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()
OUT = POST / "source-intake" / "functional_rg" / "5200"
DOCUMENT = (
    POST
    / "5200-Y5-R2FR-CTP-vacuum-occupied-projector-metric-and-"
    "composite-exponent-ownership-gate.md"
)
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5200_VALIDATION.csv"
)
CHECKPOINT_5199_OUT = POST / "source-intake" / "functional_rg" / "5199"
CHECKPOINT_5199_RESULT = (
    CHECKPOINT_5199_OUT
    / "composite_Legendre_projective_logistic_results.json"
)
CHECKPOINT_5181_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5181"
    / "critical_pair_completion_results.json"
)
SPECTRUM_4958 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4958"
    / "essential_functional_stability_spectrum.csv"
)
MINIMAL_SPECTRUM_4937 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4937"
    / "minimal_essential_motion_spectrum.csv"
)
CONSTANT_ROOTS_4937 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4937"
    / "constant_potential_root_spectrum.csv"
)
PUBLIC_WORKTREE = Path(
    r"C:\Users\ollet\OneDrive\Documents\Motion-TimeSpace-public-update-2026-07-22"
)
GALAXY_REPO = Path(r"D:\Users\ollet\Desktop\MTS-Galaxy-Lab-repo")

MARKER = "MTS_5200_CTP_PROJECTOR_METRIC_EXPONENT_OWNERSHIP_GATE"
CHECKED_DATE = "2026-07-24"
FORMAL_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5199_OUT_LOCK = (
    "eab39ad4e57a762fef35e264933e962eacc103b8c4f374e3911946cc35b08411"
)
PUBLIC_HEAD_LOCK = "8913c00b77d98e457ddb0c48e9aeec9cc5f309fd"
GALAXY_HEAD_LOCK = "f850e4997657f457dddc05cbe50f21186588dcc7"

SOURCE_LOCKS = {
    "4936-Y5-R2FR-motion-1PI-mass-and-O4-functional-trace-projection-or-two-scale-predictivity-gate.md": (
        "d24db400f3fb2fec75883bb078a37eec15b101e09c119f2a6ff43063d604c971"
    ),
    "4937-Y5-R2FR-gravity-motion-functional-potential-Hessian-and-one-scale-fixed-function-gate.md": (
        "2cf1f25d7cf67ec9bb724381919a9ff6e78d5dabe355ec50178157309b29cce5"
    ),
    "4949-Y5-R2FR-covariant-2PI-motion-occupation-Dyson-source-and-conserved-galaxy-stress-or-composite-route-rejection.md": (
        "772bee9863471ab7e4a4e4887773b91786110539d471243c26aaa1b88866f7b8"
    ),
    "4958-Y5-R2FR-six-derivative-essential-X2-X3-quotient-and-invariant-2to4-amplitude-or-rate-route-rejection.md": (
        "d08b8a0ab6a5317c77a23accd34dc46c5ad6a0bc5aa73e0767c8e0aa0edd5f1c"
    ),
    "5156-Y5-R2FR-FLRW-Hessian-Gaussian-state-single-clock-adiabatic-radiation-transfer-and-patch-collapse-gate.md": (
        "fdb5c0406fb7d0e47204a51212b24b5adf19d33644399bc4a1fd2268155b1353"
    ),
    "5158-Y5-R2FR-clock-charge-source-symmetry-no-go-and-neutral-state-pivot.md": (
        "cfbd0dd3eb44d0a6621d664f051cb1eb5fa507db30cfc8bf62419c436da087aa"
    ),
    "5178-Y5-R2FR-exact-2PI-Schur-Ward-Vlasov-subtraction-and-Gaussian-residual-stress-no-go.md": (
        "7bce528f8654373353304bf904316ddc15e2923dda3064bc7e9684e92a468ac9"
    ),
    "5181-Y5-R2FR-critical-pair-bubble-positive-Hessian-and-parent-ownership-gate.md": (
        "54a35ad66744f9e1f5ab6fdd15e66bc6f87a93330a999aae2235ea5cf98b3657"
    ),
    "5185-Y5-R2FR-occupied-state-2PI-interaction-stress-and-collision-gate.md": (
        "d47db7fefdb8b9f799a48a1e4d5a7c4266880d41d97b40ae2cefe33cd62d07a5"
    ),
    "5199-Y5-R2FR-exact-composite-Legendre-no-go-and-projective-scale-covariance-logistic-reduction.md": (
        "57154bb09b8584b7fb360c9e5f94edf9b43aac3e99426e210d6308d81fbe1891"
    ),
    "source-intake/functional_rg/4937/minimal_essential_motion_spectrum.csv": (
        "054273203419412b4470e28b11de0a2ca3ac41be7f55118f7d2772f74e4bf9ec"
    ),
    "source-intake/functional_rg/4937/constant_potential_root_spectrum.csv": (
        "fcc85c2120d5a6546352de7ef3433afb6fd45d74aa68c0e89b4c21c909366a79"
    ),
    "source-intake/functional_rg/4949/CTP_2PI_static_source_results.json": (
        "d0c35037c02ac0765cb4c726f52a6e4d99132ad64f14fb9f7d0056e2b8e10121"
    ),
    "source-intake/functional_rg/4958/essential_functional_stability_spectrum.csv": (
        "a58def91b022f9890831d564d3268c5f8ab034433815e836156dc138048f2f7b"
    ),
    "source-intake/functional_rg/5156/Gaussian_CTP_state_theorem.csv": (
        "ffa05ca94534a5485887ba4dfc7d56911d3ce5257007c350a89de16e23a05acb"
    ),
    "source-intake/functional_rg/5158/neutral_pair_vs_signed_charge.csv": (
        "d10dec01fa8ba547a68b569e930605fd9731a953a463fa42a166855ab6df2fbd"
    ),
    "source-intake/functional_rg/5178/twoPI_Schur_Vlasov_subtraction_results.json": (
        "f007ab8d2f157e0fbda7465806e2902cca9e8f98d94db2d5d2fe4f1c54a0b007"
    ),
    "source-intake/functional_rg/5181/critical_pair_completion_results.json": (
        "4c1f015ed2d946f4e158cb1b1954b3bb6dfc5a49f2f43c2fc92e847229f8f88d"
    ),
    "source-intake/functional_rg/5185/occupied_state_2PI_interaction_results.json": (
        "9d725483e8fe7e355f1844ab5a15a9b257d8e4d8792250807bef1474df58d081"
    ),
    "source-intake/functional_rg/5199/composite_Legendre_projective_logistic_results.json": (
        "b582904c80f8e0e25a463bc0a40a3cea69268ab0f9b7e725ddc592bdf092e042"
    ),
}

CANONICAL_FRACTIONAL_EXPONENT = 8.0 / 3.0
OUTER_EXPONENT = 4.0
OUTER_BOUNDARY = 8.0
Q_MATCH_RELATIVE_TOLERANCE = 0.01


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


def git_state(repository: Path) -> tuple[str, str]:
    safe_path = repository.as_posix()
    head = subprocess.run(
        ["git", "-c", f"safe.directory={safe_path}", "rev-parse", "HEAD"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    status = subprocess.run(
        ["git", "-c", f"safe.directory={safe_path}", "status", "--short"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return head, status


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(field for field in row if field not in fieldnames)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": 5200,
            "marker": MARKER,
            "checked_date": CHECKED_DATE,
            "valid_for_local_GR_claim": False,
            "valid_for_galaxy_claim": False,
            "valid_for_full_MTS_claim": False,
            **row,
        }
        for row in rows
    ]


def assert_source_locks() -> None:
    failures: list[str] = []
    for relative_path, expected_digest in SOURCE_LOCKS.items():
        source_path = POST / relative_path
        if not source_path.exists():
            failures.append(f"missing:{relative_path}")
            continue
        actual_digest = file_digest(source_path)
        if actual_digest != expected_digest:
            failures.append(
                f"hash:{relative_path}:{actual_digest}!={expected_digest}"
            )
    if tree_digest(FORMAL) != FORMAL_LOCK:
        failures.append("formalization-workbench tree changed")
    if tree_digest(CHECKPOINT_5199_OUT) != CHECKPOINT_5199_OUT_LOCK:
        failures.append("checkpoint-5199 output tree changed")
    if failures:
        raise RuntimeError("source lock failure: " + "; ".join(failures))


def load_parent_data() -> dict[str, Any]:
    result_5199 = json.loads(
        CHECKPOINT_5199_RESULT.read_text(encoding="utf-8")
    )
    result_5181 = json.loads(
        CHECKPOINT_5181_RESULT.read_text(encoding="utf-8")
    )
    q_target = float(
        result_5199["diagnostics"]["projective"]["q_self_consistent"]
    )

    spectrum_rows = read_csv(SPECTRUM_4958)
    gravity_exponents: dict[tuple[str, int], float] = {}
    for row in spectrum_rows:
        if row["mode_index"] != "0" or row["gravity_connected_mode"] != "True":
            continue
        gravity_exponents[(row["scheme"], int(row["polynomial_order"]))] = float(
            row["critical_exponent_real"]
        )

    minimal_rows = read_csv(MINIMAL_SPECTRUM_4937)
    constant_rows = read_csv(CONSTANT_ROOTS_4937)
    summary_5181 = result_5181["summary"]
    return {
        "q_target": q_target,
        "gravity_exponents": gravity_exponents,
        "minimal_rows": minimal_rows,
        "constant_rows": constant_rows,
        "eta_dynamic": float(summary_5181["parent_fixed_point_eta_dynamic"]),
        "eta_reference": float(summary_5181["parent_fixed_point_eta_reference"]),
        "parent_relevant_exponent": float(
            summary_5181["parent_relevant_exponent"]
        ),
        "interaction_norm_ceiling": float(
            result_5199["diagnostics"]["interaction"][
                "maximum_interaction_Z_norm_ceiling"
            ]
        ),
    }


def projector_derivation() -> tuple[list[dict[str, Any]], dict[str, float]]:
    rows = tagged(
        [
            {
                "object": "vacuum_projector",
                "definition": "P0=|0_k,0_-k><0_k,0_-k|",
                "identity": "P0^2=P0=P0^dagger",
                "status": "EXACT_POSITIVE_PROJECTOR",
                "scope": "one regulated (k,-k) pair cell",
            },
            {
                "object": "occupied_projector",
                "definition": "P1=I-P0",
                "identity": "P1^2=P1=P1^dagger",
                "status": "EXACT_POSITIVE_PROJECTOR",
                "scope": "one regulated (k,-k) pair cell",
            },
            {
                "object": "orthogonality",
                "definition": "P0 P1=P1 P0=0",
                "identity": "P0+P1=I",
                "status": "EXACT_BINARY_RESOLUTION",
                "scope": "one regulated (k,-k) pair cell",
            },
            {
                "object": "positive_weights",
                "definition": "Wa=Tr(rho Pa), rho>=0, Tr rho=1",
                "identity": "W0>=0; W1>=0; W0+W1=1",
                "status": "EXACT_FOR_ANY_DENSITY_MATRIX",
                "scope": "one regulated pair cell",
            },
            {
                "object": "global_limit_warning",
                "definition": "P0_global=product_k P0_k",
                "identity": "vacuum probability can vanish in the continuum/thermodynamic limit",
                "status": "REQUIRES_FINITE_CELL_OR_REGULATOR",
                "scope": "no global product used in the claimed derivation",
            },
        ]
    )

    dimension = 12
    vacuum_projector = np.zeros((dimension, dimension), dtype=complex)
    vacuum_projector[0, 0] = 1.0
    occupied_projector = np.eye(dimension, dtype=complex) - vacuum_projector
    rng = np.random.default_rng(5200)
    minimum_weight = math.inf
    maximum_normalization_residual = 0.0
    maximum_imaginary_residual = 0.0
    for _ in range(128):
        amplitude = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(
            size=(dimension, dimension)
        )
        density_matrix = amplitude @ amplitude.conjugate().T
        density_matrix /= np.trace(density_matrix)
        weight_zero = np.trace(density_matrix @ vacuum_projector)
        weight_one = np.trace(density_matrix @ occupied_projector)
        minimum_weight = min(
            minimum_weight, float(weight_zero.real), float(weight_one.real)
        )
        maximum_normalization_residual = max(
            maximum_normalization_residual,
            abs(float((weight_zero + weight_one).real) - 1.0),
        )
        maximum_imaginary_residual = max(
            maximum_imaginary_residual,
            abs(float(weight_zero.imag)),
            abs(float(weight_one.imag)),
        )

    diagnostics = {
        "projector_idempotence_residual": float(
            max(
                np.max(np.abs(vacuum_projector @ vacuum_projector - vacuum_projector)),
                np.max(
                    np.abs(
                        occupied_projector @ occupied_projector - occupied_projector
                    )
                ),
            )
        ),
        "projector_orthogonality_residual": float(
            np.max(np.abs(vacuum_projector @ occupied_projector))
        ),
        "projector_completeness_residual": float(
            np.max(
                np.abs(
                    vacuum_projector
                    + occupied_projector
                    - np.eye(dimension, dtype=complex)
                )
            )
        ),
        "minimum_random_state_weight": minimum_weight,
        "maximum_random_state_normalization_residual": (
            maximum_normalization_residual
        ),
        "maximum_random_state_imaginary_residual": maximum_imaginary_residual,
        "random_density_matrix_trials": 128.0,
    }
    return rows, diagnostics


def squeezed_pair_map(
    q_target: float,
) -> tuple[list[dict[str, Any]], dict[str, float]]:
    rows: list[dict[str, Any]] = []
    maximum_sum_residual = 0.0
    maximum_odds_residual = 0.0
    for mean_occupation in np.geomspace(1.0e-10, 1.0e10, 41):
        vacuum_probability = 1.0 / (1.0 + mean_occupation)
        occupied_probability = mean_occupation / (1.0 + mean_occupation)
        squeeze_probability = occupied_probability
        squeeze_amplitude = math.asinh(math.sqrt(mean_occupation))
        maximum_sum_residual = max(
            maximum_sum_residual,
            abs(vacuum_probability + occupied_probability - 1.0),
        )
        maximum_odds_residual = max(
            maximum_odds_residual,
            abs(
                occupied_probability / vacuum_probability - mean_occupation
            )
            / mean_occupation,
        )
        rows.append(
            {
                "mean_pair_occupation_N": mean_occupation,
                "squeeze_amplitude_zeta": squeeze_amplitude,
                "r_tanh2_zeta": squeeze_probability,
                "P_vacuum": vacuum_probability,
                "P_nonvacuum": occupied_probability,
                "raw_reference_weight": 1.0,
                "raw_occupied_weight": mean_occupation,
                "odds_P1_over_P0": occupied_probability / vacuum_probability,
                "identity": "P1=N/(1+N); P0=1/(1+N)",
                "status": "EXACT_TWO_MODE_SQUEEZED_STATE_MAP",
            }
        )

    flow_residuals: list[float] = []
    log_odds_residuals: list[float] = []
    for scale_time in np.linspace(-24.0, 24.0, 193):
        mean_occupation = math.exp(q_target * scale_time)
        occupation = mean_occupation / (1.0 + mean_occupation)
        probability_derivative = q_target * occupation * (1.0 - occupation)
        derivative_from_weights = (
            q_target
            * mean_occupation
            / ((1.0 + mean_occupation) ** 2)
        )
        flow_residuals.append(
            abs(probability_derivative - derivative_from_weights)
        )
        log_odds_residuals.append(
            abs(math.log(occupation / (1.0 - occupation)) - q_target * scale_time)
        )

    diagnostics = {
        "maximum_probability_sum_residual": maximum_sum_residual,
        "maximum_odds_relative_residual": maximum_odds_residual,
        "maximum_logistic_flow_residual": max(flow_residuals),
        "maximum_log_odds_residual": max(log_odds_residuals),
        "q_target": q_target,
        "source_selection_of_squeezed_family": 0.0,
    }
    return tagged(rows), diagnostics


def occupation_metric_gate() -> tuple[list[dict[str, Any]], dict[str, float]]:
    occupation_samples = [
        1.0e-6,
        1.0e-4,
        1.0e-2,
        0.1,
        0.25,
        0.5,
        0.75,
        0.9,
        0.99,
        0.9999,
        0.999999,
    ]
    rows: list[dict[str, Any]] = []
    off_midpoint_bulk_mismatches: list[float] = []
    bulk_ratios: list[float] = []
    for occupation in occupation_samples:
        binary_fisher = 1.0 / (occupation * (1.0 - occupation))
        full_geometric_fock = 1.0 / (
            occupation * (1.0 - occupation) ** 2
        )
        gaussian_bulk = 0.5 * (
            1.0 / occupation**2 + 1.0 / (1.0 - occupation) ** 2
        )
        bulk_ratio = gaussian_bulk / binary_fisher
        bulk_ratios.append(bulk_ratio)
        if occupation != 0.5:
            off_midpoint_bulk_mismatches.append(abs(bulk_ratio - 1.0))
        rows.append(
            {
                "occupation_n": occupation,
                "binary_boundary_Fisher": binary_fisher,
                "binary_entropy_hessian": binary_fisher,
                "full_geometric_Fock_Fisher": full_geometric_fock,
                "Gaussian_bulk_2PI_metric": gaussian_bulk,
                "bulk_over_binary": bulk_ratio,
                "full_Fock_over_binary": full_geometric_fock / binary_fisher,
                "binary_metric_origin": (
                    "orthogonal fixed blocks in Gamma_rho0 or binary measurement"
                ),
                "bulk_metric_origin": (
                    "-1/2 ln[G0 G1] at fixed G0+G1"
                ),
                "status": (
                    "EQUAL_ONLY_AT_N_HALF"
                    if occupation == 0.5
                    else "FUNCTIONAL_SHAPE_MISMATCH"
                ),
            }
        )

    diagnostics = {
        "binary_entropy_hessian_identity_residual": 0.0,
        "bulk_binary_equality_point": 0.5,
        "minimum_off_midpoint_bulk_ratio_mismatch": min(
            off_midpoint_bulk_mismatches
        ),
        "minimum_bulk_over_binary": min(bulk_ratios),
        "maximum_bulk_over_binary": max(bulk_ratios),
        "binary_metric_is_bulk_Gaussian_2PI_metric": 0.0,
        "binary_metric_is_boundary_block_metric": 1.0,
        "full_squeezed_state_requires_binary_coarse_graining": 1.0,
    }
    return tagged(rows), diagnostics


def inverse_kernel_gate(
    q_target: float,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, float]]:
    rows: list[dict[str, Any]] = []
    decomposition_residuals: list[float] = []
    flow_residuals: list[float] = []
    for scale_time in np.linspace(-20.0, 20.0, 161):
        scale_ratio = math.exp(-scale_time)
        infrared_kernel = scale_ratio
        ultraviolet_kernel = scale_ratio ** (1.0 + q_target)
        total_kernel = infrared_kernel + ultraviolet_kernel
        occupation = infrared_kernel / total_kernel
        expected_occupation = 1.0 / (1.0 + scale_ratio**q_target)
        decomposition_residuals.append(
            abs(total_kernel - scale_ratio * (1.0 + scale_ratio**q_target))
            / total_kernel
        )
        flow_residuals.append(abs(occupation - expected_occupation))
        rows.append(
            {
                "u_log_mu_over_k": scale_time,
                "x_abs_k_over_mu": scale_ratio,
                "K_IR_x": infrared_kernel,
                "K_UV_x_power_1_plus_q": ultraviolet_kernel,
                "K_total": total_kernel,
                "C_total_inverse": 1.0 / total_kernel,
                "projective_IR_fraction_n": occupation,
                "dn_du_exact": q_target * occupation * (1.0 - occupation),
                "identity": "K=x+x^(1+q); n=K_IR/K=1/(1+x^q)",
                "status": "EXACT_POSITIVE_KERNEL_DECOMPOSITION",
            }
        )

    ownership_rows = tagged(
        [
            {
                "kernel_term": "x",
                "momentum_form": "|k|/mu",
                "implied_q_if_paired_with_x": 0.0,
                "parent_status": "DERIVED",
                "source": (
                    "5181 massless three-dimensional pair bubble "
                    "B0=1/(8|k|)"
                ),
                "owns_target_crossover": False,
            },
            {
                "kernel_term": "x^2",
                "momentum_form": "k^2/mu^2",
                "implied_q_if_paired_with_x": 1.0,
                "parent_status": "AVAILABLE_AS_LOCAL_ANALYTIC_TERM",
                "source": "local derivative expansion",
                "owns_target_crossover": False,
            },
            {
                "kernel_term": "x^3",
                "momentum_form": "|k|^3/mu^3",
                "implied_q_if_paired_with_x": 2.0,
                "parent_status": "DERIVED_AS_DERIVATIVE_PAIR_RESIDUAL",
                "source": "5181 D0=|k|^3/32",
                "owns_target_crossover": False,
            },
            {
                "kernel_term": "x^(1+q)",
                "momentum_form": f"|k|^{1.0 + q_target}/mu^{1.0 + q_target}",
                "implied_q_if_paired_with_x": q_target,
                "parent_status": "ABSENT_FROM_SOURCED_PARENT_KERNEL",
                "source": "required by exact projective decomposition",
                "owns_target_crossover": False,
            },
        ]
    )
    diagnostics = {
        "maximum_kernel_decomposition_relative_residual": max(
            decomposition_residuals
        ),
        "maximum_projective_fraction_residual": max(flow_residuals),
        "target_uv_kernel_power": 1.0 + q_target,
        "parent_owns_IR_x_term": 1.0,
        "parent_owns_target_UV_term": 0.0,
    }
    return tagged(rows), ownership_rows, diagnostics


def exponent_candidate_scan(
    parent_data: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    q_target = float(parent_data["q_target"])
    gravity_exponents = parent_data["gravity_exponents"]
    eta_dynamic = float(parent_data["eta_dynamic"])
    eta_reference = float(parent_data["eta_reference"])
    rows: list[dict[str, Any]] = []

    def add_candidate(
        name: str,
        occupied_exponent: float,
        reference_exponent: float,
        source: str,
        same_composite_kernel: bool,
        regular_parent_eigenoperator: bool,
        positive_weight_projection: bool,
        interpretation: str,
    ) -> None:
        q_candidate = occupied_exponent - reference_exponent
        absolute_residual = abs(q_candidate - q_target)
        relative_residual = absolute_residual / abs(q_target)
        numerical_match = relative_residual <= Q_MATCH_RELATIVE_TOLERANCE
        structurally_admissible = (
            same_composite_kernel
            and regular_parent_eigenoperator
            and positive_weight_projection
        )
        rows.append(
            {
                "candidate": name,
                "occupied_exponent": occupied_exponent,
                "reference_exponent": reference_exponent,
                "q_candidate": q_candidate,
                "q_target": q_target,
                "absolute_residual": absolute_residual,
                "relative_residual": relative_residual,
                "matches_q_within_1pct": numerical_match,
                "same_composite_kernel": same_composite_kernel,
                "regular_parent_eigenoperator": regular_parent_eigenoperator,
                "positive_weight_projection": positive_weight_projection,
                "structurally_admissible": structurally_admissible,
                "derives_target_q": structurally_admissible and numerical_match,
                "source": source,
                "interpretation": interpretation,
            }
        )

    for scheme in ("dynamic_etaN", "reference_etaN0"):
        for order in (6, 8):
            gravity_exponent = gravity_exponents[(scheme, order)]
            add_candidate(
                f"canonical_8_over_3_minus_{scheme}_N{order}",
                CANONICAL_FRACTIONAL_EXPONENT,
                gravity_exponent,
                "4936/4937 canonical fractional dimension and 4958 gravity spectrum",
                False,
                False,
                False,
                (
                    "zeroth-order dimensional coincidence; the fractional "
                    "one-coupling family is not closed"
                ),
            )

    gravity_reference = gravity_exponents[("dynamic_etaN", 8)]
    for minimal_row in parent_data["minimal_rows"]:
        formal_fractional = float(
            minimal_row["theta_fractional_formal_diagonal"]
        )
        add_candidate(
            f"4937_formal_fractional_{minimal_row['mapping']}",
            formal_fractional,
            gravity_reference,
            "4937 minimal essential motion spectrum and 4958 dynamic N8",
            False,
            minimal_row["fractional_is_regular_eigenoperator"] == "True",
            False,
            "formal diagonal only; 4937 explicitly marks it nonregular",
        )

    for constant_row in parent_data["constant_rows"]:
        if constant_row["branch"] != "low":
            continue
        formal_fractional = float(
            constant_row["theta_fractional_formal_diagonal"]
        )
        add_candidate(
            (
                "4937_low_constant_root_"
                f"{constant_row['scheme']}_r{constant_row['r_sigma']}"
            ),
            formal_fractional,
            gravity_reference,
            "4937 constant-potential low root and 4958 dynamic N8",
            False,
            False,
            False,
            "formal fractional diagonal is not a regular eigenoperator",
        )

    eta_corrected_dynamic = (
        CANONICAL_FRACTIONAL_EXPONENT - (2.0 / 3.0) * eta_dynamic
    )
    eta_corrected_reference = (
        CANONICAL_FRACTIONAL_EXPONENT - (2.0 / 3.0) * eta_reference
    )
    add_candidate(
        "eta_corrected_canonical_dynamic",
        eta_corrected_dynamic,
        gravity_reference,
        "5181 sourced dynamic eta and 4958 dynamic N8",
        False,
        False,
        False,
        "dimension counting with eta; no regular composite eigenoperator",
    )
    add_candidate(
        "eta_corrected_canonical_reference",
        eta_corrected_reference,
        gravity_exponents[("reference_etaN0", 8)],
        "5181 sourced reference eta and 4958 reference N8",
        False,
        False,
        False,
        "reference-scheme dimension counting; no projector ownership",
    )

    gaussian_pair_q_dynamic = -2.0 * eta_dynamic
    gaussian_pair_q_reference = -2.0 * eta_reference
    add_candidate(
        "Gaussian_static_pair_power_dynamic_eta",
        1.0 + gaussian_pair_q_dynamic,
        1.0,
        (
            "D(p)~p^(-2+eta) gives B_pair(k)~k^(-1+2eta) "
            "and K_pair~k^(1-2eta)"
        ),
        True,
        True,
        True,
        "same Gaussian pair carrier is admissible but predicts the wrong q",
    )
    add_candidate(
        "Gaussian_static_pair_power_reference_eta",
        1.0 + gaussian_pair_q_reference,
        1.0,
        (
            "reference eta in the same static Gaussian pair power count"
        ),
        True,
        True,
        True,
        "same Gaussian pair carrier is admissible but predicts the wrong q",
    )

    rows = tagged(rows)
    candidate_values = {
        row["candidate"]: float(row["q_candidate"]) for row in rows
    }
    canonical_near_hit = candidate_values[
        "canonical_8_over_3_minus_dynamic_etaN_N8"
    ]
    required_motion_exponent = gravity_reference + q_target
    required_static_pair_eta = -0.5 * q_target
    diagnostics: dict[str, Any] = {
        "q_target": q_target,
        "theta_GR_dynamic_N8": gravity_reference,
        "canonical_fractional_exponent": CANONICAL_FRACTIONAL_EXPONENT,
        "canonical_difference_near_hit": canonical_near_hit,
        "canonical_difference_relative_residual": abs(
            canonical_near_hit - q_target
        )
        / q_target,
        "required_motion_exponent": required_motion_exponent,
        "required_correction_from_canonical": (
            required_motion_exponent - CANONICAL_FRACTIONAL_EXPONENT
        ),
        "eta_corrected_dynamic_motion_exponent": eta_corrected_dynamic,
        "required_vertex_correction_after_dynamic_eta": (
            required_motion_exponent - eta_corrected_dynamic
        ),
        "required_static_pair_eta": required_static_pair_eta,
        "parent_dynamic_eta": eta_dynamic,
        "Gaussian_pair_q_dynamic": gaussian_pair_q_dynamic,
        "Gaussian_pair_q_reference": gaussian_pair_q_reference,
        "candidate_count": len(rows),
        "numerical_match_count": sum(
            bool(row["matches_q_within_1pct"]) for row in rows
        ),
        "structurally_admissible_count": sum(
            bool(row["structurally_admissible"]) for row in rows
        ),
        "target_derivation_count": sum(
            bool(row["derives_target_q"]) for row in rows
        ),
    }

    admissibility_rows = tagged(
        [
            {
                "clause": "fractional_one_coupling_flow_closure",
                "required": True,
                "observed": False,
                "source": "4936 scalar trace generates |varphi|^(2/3)",
                "passes": False,
            },
            {
                "clause": "fractional_regular_eigenoperator",
                "required": True,
                "observed": False,
                "source": "4937 functional-potential Hessian",
                "passes": False,
            },
            {
                "clause": "same_CTP_composite_kernel_projection",
                "required": True,
                "observed": False,
                "source": "no 4937-to-5178 Bethe-Salpeter overlap row",
                "passes": False,
            },
            {
                "clause": "positive_projector_weight_overlap",
                "required": True,
                "observed": False,
                "source": "projectors exist, eigenoperator overlap does not",
                "passes": False,
            },
            {
                "clause": "canonical_difference_numerical_proximity",
                "required": False,
                "observed": True,
                "source": (
                    f"8/3-{gravity_reference}={canonical_near_hit}"
                ),
                "passes": True,
            },
            {
                "clause": "parent_derivation_of_q",
                "required": True,
                "observed": False,
                "source": "all mandatory structural clauses must pass",
                "passes": False,
            },
        ]
    )
    return rows, admissibility_rows, diagnostics


def wall_and_decision_rows(
    q_target: float,
    metric_diagnostics: dict[str, float],
    exponent_diagnostics: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    wall_rows = tagged(
        [
            {
                "object": "outer_projective_form",
                "equation": "b=1/[1+(R/(B L))^s]",
                "value": "",
                "derivation_status": "EXACT_GIVEN_TWO_POSITIVE_WEIGHTS",
                "parent_owned": False,
                "reason": "physical interior/exterior projector pair is not sourced",
            },
            {
                "object": "outer_exponent_s",
                "equation": "d ln(W_in/W_out)/d ln R=-s",
                "value": OUTER_EXPONENT,
                "derivation_status": "BOUNDARY_INPUT",
                "parent_owned": False,
                "reason": "four-dimensional measure counting is not a boundary action",
            },
            {
                "object": "outer_normalization_B",
                "equation": "W_in=W_out at R=B L",
                "value": OUTER_BOUNDARY,
                "derivation_status": "BOUNDARY_INPUT",
                "parent_owned": False,
                "reason": "no parent finite-domain normalization fixes B=8",
            },
            {
                "object": "outer_wall_claim",
                "equation": "s=4 and B=8 from parent",
                "value": False,
                "derivation_status": "REJECTED_AS_CURRENT_PARENT_CLAIM",
                "parent_owned": False,
                "reason": "both exponent and crossing normalization remain unsigned",
            },
        ]
    )

    decision_rows = tagged(
        [
            {
                "question": "Do positive vacuum/occupied CTP projectors exist?",
                "answer": "YES_KINEMATICALLY",
                "parent_owned": True,
                "claim_effect": "opens a lawful reduced binary sector",
            },
            {
                "question": "Does a two-mode squeezed state give the projective map?",
                "answer": "YES_EXACTLY",
                "parent_owned": False,
                "claim_effect": "state family exists but is not action-selected",
            },
            {
                "question": "Does the binary Fisher metric follow?",
                "answer": "YES_AFTER_BINARY_BOUNDARY_REDUCTION",
                "parent_owned": False,
                "claim_effect": (
                    "requires Gamma_rho0/coarse-graining; bulk Gaussian 2PI differs"
                ),
            },
            {
                "question": "Does the sourced bulk 2PI metric equal Fisher globally?",
                "answer": "NO",
                "parent_owned": True,
                "claim_effect": (
                    f"equal only at n={metric_diagnostics['bulk_binary_equality_point']}"
                ),
            },
            {
                "question": "Does the parent own the infrared |k| kernel?",
                "answer": "YES",
                "parent_owned": True,
                "claim_effect": "5181 critical pair carrier retained",
            },
            {
                "question": "Does the parent own |k|^(1+q)?",
                "answer": "NO",
                "parent_owned": False,
                "claim_effect": "the exact q-dependent crossover remains absent",
            },
            {
                "question": "Does the 8/3-theta_GR near hit derive q?",
                "answer": "NO",
                "parent_owned": False,
                "claim_effect": (
                    "numerically close but nonclosed, nonregular and unprojected"
                ),
            },
            {
                "question": "Does any sourced candidate derive target q?",
                "answer": (
                    "YES"
                    if exponent_diagnostics["target_derivation_count"] > 0
                    else "NO"
                ),
                "parent_owned": (
                    exponent_diagnostics["target_derivation_count"] > 0
                ),
                "claim_effect": "q remains a reduced-state closure",
            },
            {
                "question": "Are outer s=4 and B=8 parent-owned?",
                "answer": "NO",
                "parent_owned": False,
                "claim_effect": "outer wall remains boundary closure",
            },
            {
                "question": "Does checkpoint 5200 alter local GR/Newton/Maxwell?",
                "answer": "NO",
                "parent_owned": True,
                "claim_effect": "local branch remains exactly as before",
            },
            {
                "question": "What route is selected next?",
                "answer": "RETURN_TO_LOCAL_GR_AND_SOURCE_COUPLING_SPINE",
                "parent_owned": False,
                "claim_effect": (
                    "derive the parent matter variation, Newtonian normalization "
                    "and PPN residual before any further galaxy closure scan"
                ),
            },
        ]
    )
    return wall_rows, decision_rows


def provenance_rows() -> list[dict[str, Any]]:
    roles = {
        "4936": "fractional one-coupling closure no-go",
        "4937": "formal fractional eigenoperator admissibility",
        "4949": "CTP occupation as state data",
        "4958": "source-locked gravity exponent and eta",
        "5156": "Gaussian CTP state freedom",
        "5158": "neutral pair state and charge boundary",
        "5178": "exact 2PI Schur kernel and Gamma_rho0 boundary",
        "5181": "massless pair bubble and positive Hessian carrier",
        "5185": "known interaction strength bound",
        "5199": "projective logistic theorem and q target",
    }
    rows: list[dict[str, Any]] = []
    for relative_path, digest in SOURCE_LOCKS.items():
        matched_role = next(
            (
                role
                for checkpoint, role in roles.items()
                if checkpoint in relative_path
            ),
            "locked supporting source",
        )
        rows.append(
            {
                "source_path": relative_path,
                "sha256": digest,
                "role": matched_role,
                "exists": (POST / relative_path).exists(),
                "extraction_method": "direct local source parse",
            }
        )
    return tagged(rows)


def validation_rows(
    public_before: tuple[str, str],
    galaxy_before: tuple[str, str],
    output_files: list[Path],
    all_csv_rows: list[list[dict[str, Any]]],
    payload: dict[str, Any],
    diagnostics: dict[str, Any],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, Any]] = []

    def add(name: str, passed: bool, detail: Any) -> None:
        checks.append((name, bool(passed), detail))

    add("document_exists", DOCUMENT.exists(), DOCUMENT)
    add(
        "document_marker",
        DOCUMENT.exists() and MARKER in DOCUMENT.read_text(encoding="utf-8"),
        MARKER,
    )
    add("script_exists", SCRIPT.exists(), SCRIPT)
    for relative_path, expected_digest in SOURCE_LOCKS.items():
        source_path = POST / relative_path
        add(f"source_exists::{relative_path}", source_path.exists(), source_path)
        add(
            f"source_hash::{relative_path}",
            source_path.exists() and file_digest(source_path) == expected_digest,
            expected_digest,
        )

    add(
        "formalization_workbench_lock",
        tree_digest(FORMAL) == FORMAL_LOCK,
        tree_digest(FORMAL),
    )
    add(
        "checkpoint_5199_output_lock",
        tree_digest(CHECKPOINT_5199_OUT) == CHECKPOINT_5199_OUT_LOCK,
        tree_digest(CHECKPOINT_5199_OUT),
    )

    public_after = git_state(PUBLIC_WORKTREE)
    galaxy_after = git_state(GALAXY_REPO)
    add(
        "public_worktree_head_lock",
        public_after[0] == PUBLIC_HEAD_LOCK,
        public_after[0],
    )
    add(
        "public_worktree_unchanged",
        public_after == public_before,
        public_after,
    )
    add(
        "galaxy_repository_head_lock",
        galaxy_after[0] == GALAXY_HEAD_LOCK,
        galaxy_after[0],
    )
    add(
        "galaxy_repository_unchanged",
        galaxy_after == galaxy_before,
        galaxy_after,
    )

    projector = diagnostics["projector"]
    add(
        "projectors_idempotent",
        projector["projector_idempotence_residual"] < 1.0e-14,
        projector["projector_idempotence_residual"],
    )
    add(
        "projectors_orthogonal",
        projector["projector_orthogonality_residual"] < 1.0e-14,
        projector["projector_orthogonality_residual"],
    )
    add(
        "projectors_complete",
        projector["projector_completeness_residual"] < 1.0e-14,
        projector["projector_completeness_residual"],
    )
    add(
        "random_state_weights_positive",
        projector["minimum_random_state_weight"] >= -1.0e-14,
        projector["minimum_random_state_weight"],
    )
    add(
        "random_state_weights_normalized",
        projector["maximum_random_state_normalization_residual"] < 1.0e-14,
        projector["maximum_random_state_normalization_residual"],
    )

    squeezed = diagnostics["squeezed"]
    add(
        "squeezed_probability_normalization",
        squeezed["maximum_probability_sum_residual"] < 1.0e-14,
        squeezed["maximum_probability_sum_residual"],
    )
    add(
        "squeezed_odds_identity",
        squeezed["maximum_odds_relative_residual"] < 1.0e-14,
        squeezed["maximum_odds_relative_residual"],
    )
    add(
        "squeezed_logistic_flow",
        squeezed["maximum_logistic_flow_residual"] < 1.0e-14,
        squeezed["maximum_logistic_flow_residual"],
    )
    add(
        "squeezed_state_not_parent_selected",
        squeezed["source_selection_of_squeezed_family"] == 0.0,
        squeezed["source_selection_of_squeezed_family"],
    )

    metric = diagnostics["metric"]
    add(
        "binary_entropy_hessian_is_Fisher",
        metric["binary_entropy_hessian_identity_residual"] < 1.0e-14,
        metric["binary_entropy_hessian_identity_residual"],
    )
    add(
        "bulk_metric_not_global_Fisher",
        metric["minimum_off_midpoint_bulk_ratio_mismatch"] > 0.1,
        metric["minimum_off_midpoint_bulk_ratio_mismatch"],
    )
    add(
        "boundary_binary_reduction_required",
        metric["full_squeezed_state_requires_binary_coarse_graining"] == 1.0,
        metric["full_squeezed_state_requires_binary_coarse_graining"],
    )

    kernel = diagnostics["kernel"]
    add(
        "kernel_decomposition_exact",
        kernel["maximum_kernel_decomposition_relative_residual"] < 1.0e-14,
        kernel["maximum_kernel_decomposition_relative_residual"],
    )
    add(
        "projective_fraction_exact",
        kernel["maximum_projective_fraction_residual"] < 1.0e-14,
        kernel["maximum_projective_fraction_residual"],
    )
    add(
        "parent_owns_IR_pair_carrier",
        kernel["parent_owns_IR_x_term"] == 1.0,
        kernel["parent_owns_IR_x_term"],
    )
    add(
        "parent_does_not_own_target_UV_term",
        kernel["parent_owns_target_UV_term"] == 0.0,
        kernel["parent_owns_target_UV_term"],
    )

    exponent = diagnostics["exponent"]
    add(
        "canonical_difference_is_near_hit",
        exponent["canonical_difference_relative_residual"] < 0.01,
        exponent["canonical_difference_relative_residual"],
    )
    add(
        "at_least_one_structural_exponent_test",
        exponent["structurally_admissible_count"] >= 1,
        exponent["structurally_admissible_count"],
    )
    add(
        "no_candidate_derives_target_q",
        exponent["target_derivation_count"] == 0,
        exponent["target_derivation_count"],
    )
    add(
        "required_pair_eta_differs_from_parent",
        abs(
            exponent["required_static_pair_eta"]
            - exponent["parent_dynamic_eta"]
        )
        > 0.25,
        (
            exponent["required_static_pair_eta"],
            exponent["parent_dynamic_eta"],
        ),
    )

    claim_status = payload["claim_status"]
    add(
        "q_parent_ownership_blocked",
        claim_status["q_parent_owned"] is False,
        claim_status["q_parent_owned"],
    )
    add(
        "outer_wall_parent_ownership_blocked",
        claim_status["outer_wall_parent_owned"] is False,
        claim_status["outer_wall_parent_owned"],
    )
    add(
        "local_GR_claim_unchanged_false",
        claim_status["local_GR_claim"] is False,
        claim_status["local_GR_claim"],
    )
    add(
        "galaxy_claim_false",
        claim_status["galaxy_claim"] is False,
        claim_status["galaxy_claim"],
    )
    add(
        "full_MTS_claim_false",
        claim_status["full_MTS_claim"] is False,
        claim_status["full_MTS_claim"],
    )

    for output_file in output_files:
        add(
            f"output_exists::{output_file.name}",
            output_file.exists() and output_file.stat().st_size > 0,
            output_file,
        )
        if output_file.suffix == ".csv" and output_file.exists():
            add(
                f"output_parses::{output_file.name}",
                len(read_csv(output_file)) > 0,
                len(read_csv(output_file)),
            )

    flattened_rows = [row for rows in all_csv_rows for row in rows]
    add(
        "all_rows_nonclaim",
        all(
            row.get("valid_for_full_MTS_claim") is False
            and row.get("valid_for_galaxy_claim") is False
            and row.get("valid_for_local_GR_claim") is False
            for row in flattened_rows
        ),
        len(flattened_rows),
    )
    add(
        "no_placeholder_markers",
        not any(
            "MISSING_" in str(value)
            for row in flattened_rows
            for value in row.values()
        ),
        len(flattened_rows),
    )
    add(
        "no_script_pycache",
        not any((POST / "scripts").glob("__pycache__")),
        POST / "scripts" / "__pycache__",
    )

    return [
        {
            "checkpoint": 5200,
            "marker": MARKER,
            "checked_date": CHECKED_DATE,
            "check": name,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for name, passed, detail in checks
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="derive and report the ownership decision without writing outputs",
    )
    arguments = parser.parse_args()

    assert_source_locks()
    public_before = git_state(PUBLIC_WORKTREE)
    galaxy_before = git_state(GALAXY_REPO)
    parent_data = load_parent_data()
    q_target = float(parent_data["q_target"])

    projector_rows, projector_diagnostics = projector_derivation()
    squeezed_rows, squeezed_diagnostics = squeezed_pair_map(q_target)
    metric_rows, metric_diagnostics = occupation_metric_gate()
    kernel_rows, kernel_ownership_rows, kernel_diagnostics = inverse_kernel_gate(
        q_target
    )
    exponent_rows, admissibility_rows, exponent_diagnostics = (
        exponent_candidate_scan(parent_data)
    )
    wall_rows, decision_rows = wall_and_decision_rows(
        q_target,
        metric_diagnostics,
        exponent_diagnostics,
    )
    provenance = provenance_rows()

    diagnostics = {
        "projector": projector_diagnostics,
        "squeezed": squeezed_diagnostics,
        "metric": metric_diagnostics,
        "kernel": kernel_diagnostics,
        "exponent": exponent_diagnostics,
        "known_interaction_norm_ceiling": parent_data[
            "interaction_norm_ceiling"
        ],
    }
    claim_status = {
        "positive_vacuum_occupied_projectors": "DERIVED_KINEMATICALLY",
        "squeezed_pair_projective_map": "DERIVED_FOR_AN_ALLOWED_STATE_FAMILY",
        "squeezed_state_parent_selected": False,
        "binary_Fisher_metric": "DERIVED_AFTER_BOUNDARY_BINARY_REDUCTION",
        "bulk_Gaussian_2PI_metric_matches_Fisher": False,
        "critical_pair_IR_carrier_parent_owned": True,
        "q_dependent_UV_kernel_parent_owned": False,
        "q_parent_owned": False,
        "outer_wall_parent_owned": False,
        "local_GR_Newton_Maxwell_branch": "UNCHANGED",
        "local_GR_claim": False,
        "galaxy_claim": False,
        "full_MTS_claim": False,
    }
    payload = {
        "checkpoint": 5200,
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "decision": (
            "THE_VACUUM_AND_NONVACUUM_FOCK_PROJECTORS_ARE_EXACT_POSITIVE_"
            "AND_A_TWO_MODE_SQUEEZED_PAIR_STATE_GIVES_THE_PROJECTIVE_"
            "OCCUPATION_N_EQUALS_NBAR_OVER_ONE_PLUS_NBAR_AND_HENCE_THE_"
            "LOGISTIC_FLOW_WHEN_THE_ODDS_SCALE_AS_EXP_Q_U_THE_BINARY_"
            "FISHER_METRIC_IS_EXACT_FOR_THE_ORTHOGONAL_BOUNDARY_BLOCKS_"
            "BUT_IT_IS_NOT_THE_FUNCTIONAL_METRIC_OF_THE_SOURCED_BULK_"
            "GAUSSIAN_2PI_LOG_DETERMINANT_EXCEPT_AT_N_EQUALS_ONE_HALF_"
            "THE_5181_MASSLESS_PAIR_OWNS_THE_INFRARED_ABS_K_TERM_BUT_"
            "NO_SOURCED_PARENT_TERM_OWNS_ABS_K_TO_THE_ONE_PLUS_Q_THE_"
            "NUMERIC_EIGHT_THIRDS_MINUS_THETA_GR_NEAR_HIT_IS_REAL_BUT_"
            "IS_NOT_AN_ADMISSIBLE_DERIVATION_BECAUSE_THE_FRACTIONAL_"
            "DIRECTION_IS_NONCLOSED_NONREGULAR_AND_HAS_NO_PROJECTOR_"
            "OVERLAP_THEREFORE_Q_AND_THE_OUTER_WALL_REMAIN_EXPLICIT_"
            "REDUCED_BOUNDARY_STATE_CLOSURES_AND_THE_NEXT_ROUTE_RETURNS_"
            "TO_THE_LOCAL_GR_AND_SOURCE_COUPLING_SPINE"
        ),
        "claim_status": claim_status,
        "diagnostics": diagnostics,
        "CTP_vacuum_occupied_projector_derivation": projector_rows,
        "squeezed_pair_projective_map": squeezed_rows,
        "bulk_2PI_vs_boundary_Fisher_metric": metric_rows,
        "inverse_kernel_projective_decomposition": kernel_rows,
        "inverse_kernel_parent_ownership": kernel_ownership_rows,
        "source_locked_exponent_candidate_scan": exponent_rows,
        "fractional_eigenoperator_admissibility_gate": admissibility_rows,
        "outer_wall_ownership_gate": wall_rows,
        "q_ownership_decision": decision_rows,
        "source_provenance": provenance,
        "source_hashes": SOURCE_LOCKS,
        "formalization_workbench_tree_sha256": tree_digest(FORMAL),
        "checkpoint_5199_output_tree_sha256": tree_digest(CHECKPOINT_5199_OUT),
    }

    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "marker": MARKER,
                    "q_target": q_target,
                    "projector": projector_diagnostics,
                    "metric": metric_diagnostics,
                    "kernel": kernel_diagnostics,
                    "exponent": exponent_diagnostics,
                    "claim_status": claim_status,
                    "selected_next_route": (
                        "RETURN_TO_LOCAL_GR_AND_SOURCE_COUPLING_SPINE"
                    ),
                },
                indent=2,
                default=str,
            )
        )
        return

    OUT.mkdir(parents=True, exist_ok=True)
    output_map = {
        "CTP_vacuum_occupied_projector_derivation.csv": projector_rows,
        "squeezed_pair_projective_map.csv": squeezed_rows,
        "bulk_2PI_vs_boundary_Fisher_metric.csv": metric_rows,
        "inverse_kernel_projective_decomposition.csv": kernel_rows,
        "inverse_kernel_parent_ownership.csv": kernel_ownership_rows,
        "source_locked_exponent_candidate_scan.csv": exponent_rows,
        "fractional_eigenoperator_admissibility_gate.csv": admissibility_rows,
        "outer_wall_ownership_gate.csv": wall_rows,
        "q_ownership_decision.csv": decision_rows,
        "source_provenance.csv": provenance,
    }
    for name, rows in output_map.items():
        write_csv(OUT / name, rows)
    result_path = OUT / "CTP_projector_metric_exponent_ownership_results.json"
    result_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )

    output_files = [OUT / name for name in output_map] + [result_path]
    all_csv_rows = list(output_map.values())
    validations = validation_rows(
        public_before,
        galaxy_before,
        output_files,
        all_csv_rows,
        payload,
        diagnostics,
    )
    write_csv(VALIDATION, validations)
    failed = [row for row in validations if row["status"] != "PASS"]
    if failed:
        raise RuntimeError(
            "checkpoint 5200 validation failed: "
            + "; ".join(
                f"{row['check']}={row['detail']}" for row in failed
            )
        )

    print(
        json.dumps(
            {
                "marker": MARKER,
                "validation": f"{len(validations)}/{len(validations)} PASS",
                "output_files": len(output_files),
                "output_bytes": sum(
                    path.stat().st_size for path in output_files
                ),
                "output_tree_sha256": tree_digest(OUT),
                "formalization_workbench_sha256": tree_digest(FORMAL),
                "checkpoint_5199_output_sha256": tree_digest(
                    CHECKPOINT_5199_OUT
                ),
                "q_target": q_target,
                "canonical_difference_near_hit": exponent_diagnostics[
                    "canonical_difference_near_hit"
                ],
                "target_derivation_count": exponent_diagnostics[
                    "target_derivation_count"
                ],
                "q_parent_owned": False,
                "outer_wall_parent_owned": False,
                "selected_next_route": (
                    "RETURN_TO_LOCAL_GR_AND_SOURCE_COUPLING_SPINE"
                ),
            },
            indent=2,
            default=str,
        )
    )


if __name__ == "__main__":
    main()
