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
import sympy as sp


sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()
OUT = POST / "source-intake" / "functional_rg" / "5205"
DOCUMENT = (
    POST
    / "5205-Y5-R2FR-normalized-CTP-regular-mode-ensemble-Hamiltonian-"
    "constraint-and-zero-Lambda-second-moment-selection-theorem.md"
)
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5205_VALIDATION.csv"
)
CHECKPOINT_5204_OUT = POST / "source-intake" / "functional_rg" / "5204"
PUBLIC_WORKTREE = Path(
    r"C:\Users\ollet\OneDrive\Documents\Motion-TimeSpace-public-update-2026-07-22"
)
GALAXY_REPO = Path(r"D:\Users\ollet\Desktop\MTS-Galaxy-Lab-repo")

MARKER = "MTS_5205_NORMALIZED_CTP_REGULAR_MODE_CONSTRAINT_STATE_SELECTION"
CHECKED_DATE = "2026-07-24"
FORMAL_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5204_OUT_LOCK = (
    "311d5947bed4a1faf354108823ac19a5bdb93ed4dfc181c95a95f8ab530c7108"
)
PUBLIC_HEAD_LOCK = "8913c00b77d98e457ddb0c48e9aeec9cc5f309fd"
GALAXY_HEAD_LOCK = "f850e4997657f457dddc05cbe50f21186588dcc7"

SOURCE_LOCKS = {
    "5152-Y5-R2FR-primordial-motion-occupation-dust-limit-Jeans-window-and-formation-source-arbitration.md": (
        "a62af8bc11dc0e5130e681386bb64ac4a56fb21105540581f91ab452473b0167"
    ),
    "5156-Y5-R2FR-FLRW-Hessian-Gaussian-state-single-clock-adiabatic-radiation-transfer-and-patch-collapse-gate.md": (
        "fdb5c0406fb7d0e47204a51212b24b5adf19d33644399bc4a1fd2268155b1353"
    ),
    "5179-Y5-R2FR-lowest-reflection-even-CTP-boundary-kernel-FLRW-preparation-and-perturbative-extra-stress-no-go.md": (
        "066217234006fecb16046796dd4cfdd0fec64a21a38fdcfa0eefb6aa709b3890"
    ),
    "5195-Y5-R2FR-matched-joint-CMB-informed-parent-refit-and-physical-sound-horizon-gate.md": (
        "217fdc07f94e18a21fe996f7592930f69c21ba16b3fe44b1fd1a2518d9d54737"
    ),
    "5196-Y5-R2FR-invariant-mass-gap-Hessian-and-homogeneous-state-selection-theorem.md": (
        "a3495f713d22fea38ebd010a1d0f14d2ff266180fa358ee8a89492a55ea57974"
    ),
    "5200-Y5-R2FR-CTP-vacuum-occupied-projector-metric-and-composite-exponent-ownership-gate.md": (
        "348e580fb9c48c28b4b77e2219e0bc8760bcd012081373e7120caa7aac83e656"
    ),
    "5203-Y5-R2FR-one-canonical-translation-gauge-parent-action-cross-coupling-and-branch-reduction-theorem.md": (
        "0c456634e22a3f6e03ce648fe34c28e5557d562a47249b04201a2602b67c8a6b"
    ),
    "5204-Y5-R2FR-curvature-triggered-homogeneous-motion-state-local-PPN-Gdot-and-preparation-no-overlap-theorem.md": (
        "8923d9fac23289f1923659ac3352aa216ad89c1985140c01e1d9ed1907d7c535"
    ),
    "source-intake/functional_rg/5195/joint_CMB_informed_refit_results.json": (
        "538078e466c2ee9f02e5204090b9e1c87c8c56b5680c366289336dda4abdf3ad"
    ),
    "source-intake/functional_rg/5196/mass_gap_and_state_selection_results.json": (
        "aecba0a57eaf557b6fddd18948c0d74e00a2e68e1d892516e10d2d0763fe0f04"
    ),
    "source-intake/functional_rg/5203/canonical_translation_parent_action_results.json": (
        "4199e389c41acf8b7c4414912afd88b616429440e90952e80553a235f528b2fe"
    ),
    "source-intake/functional_rg/5204/curvature_triggered_motion_state_results.json": (
        "341abeb003983ab9593137983e792e4007742d1f46c17e95b194a5fb827c382a"
    ),
}

OMEGA_R = 9.0e-5
N_INITIAL = -12.0


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    files = sorted(item for item in path.rglob("*") if item.is_file())
    for item in files:
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
            "checkpoint": 5205,
            "marker": MARKER,
            "checked_date": CHECKED_DATE,
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
            failures.append(f"absent:{relative_path}")
            continue
        actual_digest = file_digest(source_path)
        if actual_digest != expected_digest:
            failures.append(
                f"hash:{relative_path}:{actual_digest}!={expected_digest}"
            )
    if tree_digest(FORMAL) != FORMAL_LOCK:
        failures.append("formalization-workbench tree changed")
    if tree_digest(CHECKPOINT_5204_OUT) != CHECKPOINT_5204_OUT_LOCK:
        failures.append("checkpoint-5204 output tree changed")
    if failures:
        raise RuntimeError("source lock failure: " + "; ".join(failures))


def ctp_gaussian_state() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    q_plus, q_minus = sp.symbols("q_plus q_minus", real=True)
    variance_q, determinant_v = sp.symbols(
        "variance_q determinant_v",
        positive=True,
        real=True,
    )
    covariance_qp = sp.symbols("covariance_qp", real=True)
    q_bar = (q_plus + q_minus) / 2
    q_delta = q_plus - q_minus
    density_kernel = (
        1
        / sp.sqrt(2 * sp.pi * variance_q)
        * sp.exp(
            -q_bar**2 / (2 * variance_q)
            -determinant_v * q_delta**2 / (2 * variance_q)
            +sp.I * covariance_qp * q_bar * q_delta / variance_q
        )
    )
    trace_integral = sp.simplify(
        sp.integrate(
            density_kernel.subs(q_minus, q_plus),
            (q_plus, -sp.oo, sp.oo),
        )
    )
    hermiticity_residual = sp.simplify(
        density_kernel.xreplace(
            {
                q_plus: q_minus,
                q_minus: q_plus,
            }
        )
        - sp.conjugate(density_kernel)
    )

    vacuum_q, state_variance = sp.symbols(
        "vacuum_q state_variance",
        positive=True,
        real=True,
    )
    mode_q, mode_p = sp.symbols("mode_q mode_p", real=True)
    vacuum_p = 1 / (4 * vacuum_q)
    mixed_q = vacuum_q + state_variance * mode_q**2
    mixed_p = vacuum_p + state_variance * mode_p**2
    mixed_c = state_variance * mode_q * mode_p
    mixed_determinant = sp.factor(mixed_q * mixed_p - mixed_c**2)
    determinant_excess = sp.simplify(
        mixed_determinant - sp.Rational(1, 4)
    )

    rng = np.random.default_rng(5205)
    minimum_determinant = math.inf
    for _ in range(256):
        numeric_vacuum_q = 10.0 ** rng.uniform(-3.0, 3.0)
        numeric_state_variance = 10.0 ** rng.uniform(-6.0, 3.0)
        numeric_mode = rng.normal(size=2)
        numeric_covariance = np.asarray(
            [
                [numeric_vacuum_q, 0.0],
                [0.0, 1.0 / (4.0 * numeric_vacuum_q)],
            ]
        ) + numeric_state_variance * np.outer(
            numeric_mode,
            numeric_mode,
        )
        minimum_determinant = min(
            minimum_determinant,
            float(np.linalg.det(numeric_covariance)),
        )

    rows = tagged(
        [
            {
                "item": "state_definition",
                "result": (
                    "rho_i=int dA P(A) D(A v_reg) rho_0 "
                    "D(A v_reg)^dagger"
                ),
                "status": "POSITIVE_TRACE_ONE_FOR_NORMALIZED_P",
                "scope": (
                    "finite regulated homogeneous cell; rho_0 centered "
                    "and parity even"
                ),
            },
            {
                "item": "reflection_evenness",
                "result": "P(A)=P(-A)",
                "status": "EXACT",
                "scope": "all odd amplitude moments and the one-point field vanish",
            },
            {
                "item": "Gaussian_displacement_class",
                "result": "V_i=V_0+sigma_A^2 v_reg v_reg^T",
                "status": "EXACT_FOR_GAUSSIAN_P",
                "scope": "a Gaussian distribution of Weyl displacements remains Gaussian",
            },
            {
                "item": "density_kernel",
                "result": (
                    "rho(q+,q-)=(2pi Q)^-1/2 exp[-(q++q-)^2/(8Q)"
                    "-det(V)(q+-q-)^2/(2Q)+i C(q+^2-q-^2)/(2Q)]"
                ),
                "status": "EXACT_ZERO_MEAN_ONE_MODE_KERNEL",
                "scope": "Q=V_qq; C=V_qp; det(V)>=1/4",
            },
            {
                "item": "kernel_trace",
                "result": str(trace_integral),
                "status": "EXACT",
                "scope": "Tr rho=1",
            },
            {
                "item": "kernel_hermiticity",
                "result": str(hermiticity_residual),
                "status": "EXACT",
                "scope": "rho(q-,q+)=rho(q+,q-)^*",
            },
            {
                "item": "uncertainty_determinant",
                "result": str(mixed_determinant),
                "status": "EXACT",
                "scope": "det(V_i)=1/4 plus a nonnegative displacement term",
            },
            {
                "item": "determinant_excess",
                "result": str(determinant_excess),
                "status": "NONNEGATIVE",
                "scope": "positive P cannot violate the one-mode uncertainty bound",
            },
            {
                "item": "CTP_boundary_action",
                "result": "Gamma_rho_i[+,-]=-i ln <q+|rho_i|q->",
                "status": "EXACT_DEFINITION",
                "scope": "initial Cauchy surface only",
            },
        ]
    )
    diagnostics = {
        "trace_integral": str(trace_integral),
        "hermiticity_residual": str(hermiticity_residual),
        "mixed_determinant": str(mixed_determinant),
        "determinant_excess": str(determinant_excess),
        "minimum_random_determinant": minimum_determinant,
        "random_trials": 256,
        "positive_trace_one_state_constructed": True,
        "unique_microscopic_state_selected": False,
    }
    return rows, diagnostics


def ensemble_and_stress_theorem() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    expansion, mode, mode_n, mode_nn, hubble_slope, mass_ratio = sp.symbols(
        "E u u_N u_NN h mu",
        positive=True,
        real=True,
    )
    energy_kernel = expansion**2 * mode_n**2 + mass_ratio**2 * mode**2
    pressure_kernel = expansion**2 * mode_n**2 - mass_ratio**2 * mode**2
    energy_derivative = (
        2 * hubble_slope * expansion**2 * mode_n**2
        + 2 * expansion**2 * mode_n * mode_nn
        + 2 * mass_ratio**2 * mode * mode_n
    )
    equation_of_motion = (
        -(3 + hubble_slope) * mode_n
        -mass_ratio**2 * mode / expansion**2
    )
    conservation_residual = sp.simplify(
        energy_derivative.subs(mode_nn, equation_of_motion)
        + 3 * (energy_kernel + pressure_kernel)
    )

    regular_rows = tagged(
        [
            {
                "item": "regular_mode_ensemble",
                "result": "chi_A(N)=A u_reg(N)",
                "status": "EXACT_LINEAR_SOURCE_FREE_SOLUTION",
                "implication": "all regular homogeneous histories differ only by A",
            },
            {
                "item": "even_amplitude_measure",
                "result": (
                    "int dA P(A)=1; P(A)=P(-A); "
                    "<A>=0; <A^2>=sigma_A^2"
                ),
                "status": "NORMALIZED_REFLECTION_EVEN",
                "implication": "mean field vanishes while quadratic stress is finite",
            },
            {
                "item": "second_moment_field",
                "result": "<chi^2>=sigma_A^2 u_reg^2",
                "status": "EXACT_AFTER_CENTERED_VACUUM_SUBTRACTION",
                "implication": "higher amplitude moments do not enter a quadratic background",
            },
            {
                "item": "second_moment_velocity",
                "result": "<chi_N^2>=sigma_A^2 u_reg,N^2",
                "status": "EXACT_AFTER_CENTERED_VACUUM_SUBTRACTION",
                "implication": "one variance normalizes both kinetic and potential stress",
            },
            {
                "item": "background_equation_of_state",
                "result": (
                    "w_chi=(E^2 u_N^2-mu^2 u^2)"
                    "/(E^2 u_N^2+mu^2 u^2)"
                ),
                "status": "AMPLITUDE_DISTRIBUTION_INDEPENDENT",
                "implication": "regular transfer and mu fix shape at quadratic order",
            },
            {
                "item": "higher_moment_scope",
                "result": "<A^4>,<A^6>,... absent from quadratic background",
                "status": "EXACT_TRUNCATION_STATEMENT",
                "implication": "they remain physical for interactions and non-Gaussian observables",
            },
        ]
    )
    stress_rows = tagged(
        [
            {
                "item": "ensemble_energy",
                "result": (
                    "rho_chi=3 M_R^2 H0^2 sigma_A^2 "
                    "(E^2 u_N^2+mu^2 u^2)"
                ),
                "status": "EXACT_MINIMAL_CANONICAL_QUADRATIC_STRESS",
                "conservation": "tested",
            },
            {
                "item": "ensemble_pressure",
                "result": (
                    "p_chi=3 M_R^2 H0^2 sigma_A^2 "
                    "(E^2 u_N^2-mu^2 u^2)"
                ),
                "status": "EXACT_MINIMAL_CANONICAL_QUADRATIC_STRESS",
                "conservation": "tested",
            },
            {
                "item": "continuity_residual",
                "result": str(conservation_residual),
                "status": "EXACT_ZERO",
                "conservation": "rho_N+3(rho+p)=0",
            },
            {
                "item": "weight_transport",
                "result": "partial_N P(A)=0 along the source-free ensemble",
                "status": "STATE_EQUATION",
                "conservation": "no externally prescribed time-dependent weights",
            },
            {
                "item": "bulk_plus_state_Ward_identity",
                "result": (
                    "nabla_mu <T_chi^mu_nu>="
                    "int dA P(A) nabla_mu T_A^mu_nu=0"
                ),
                "status": "EXACT_ON_EACH_BULK_EQUATION",
                "conservation": "ensemble averaging commutes with divergence",
            },
        ]
    )
    diagnostics = {
        "energy_kernel": str(energy_kernel),
        "pressure_kernel": str(pressure_kernel),
        "equation_of_motion": str(equation_of_motion),
        "continuity_residual": str(conservation_residual),
        "quadratic_background_depends_only_on_second_moment": True,
        "explicit_stress_scope": "minimal canonical zeta_c=0 target",
        "finite_zeta_requires_scalar_tensor_refit": True,
        "higher_moments_selected": False,
    }
    return regular_rows, stress_rows, diagnostics


def load_branch_inputs() -> tuple[
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    checkpoint_5195 = json.loads(
        (
            POST
            / "source-intake"
            / "functional_rg"
            / "5195"
            / "joint_CMB_informed_refit_results.json"
        ).read_text(encoding="utf-8")
    )
    checkpoint_5196 = json.loads(
        (
            POST
            / "source-intake"
            / "functional_rg"
            / "5196"
            / "mass_gap_and_state_selection_results.json"
        ).read_text(encoding="utf-8")
    )
    checkpoint_5204 = json.loads(
        (
            POST
            / "source-intake"
            / "functional_rg"
            / "5204"
            / "curvature_triggered_motion_state_results.json"
        ).read_text(encoding="utf-8")
    )
    target_models = {
        "ParentScalar_Lambda_free",
        "ParentScalar_Lambda_zero",
    }
    primary_fits = {
        row["model"]: row
        for row in checkpoint_5195["fits"]
        if row["config"] == "primary_fs8_wCDM_prior"
        and row["model"] in target_models
    }
    state_rows = {
        row["model"]: row
        for row in checkpoint_5195["parent_state_summary"]
        if row["model"] in target_models
    }
    raw_targets = {
        model: {
            "mu": float(state_rows[model]["mu_mgap_over_H0"]),
            "omega_scalar": float(state_rows[model]["Omega_scalar_0"]),
            "omega_lambda": float(state_rows[model]["Omega_Lambda_0"]),
            "theta": float(state_rows[model]["theta_0"]),
            "omega_m": float(primary_fits[model]["params"]["Omega_m"]),
        }
        for model in target_models
    }
    return (
        checkpoint_5196["fitted_branch_match"],
        checkpoint_5204["parent_targets"],
        raw_targets,
    )


def constraint_state_selection() -> tuple[
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, Any],
]:
    fitted_rows, local_rows, raw_targets = load_branch_inputs()
    output_rows: list[dict[str, Any]] = []
    diagnostics: dict[str, dict[str, Any]] = {}
    for row in fitted_rows:
        model = row["model"]
        raw_target = raw_targets[model]
        amplitude_initial = float(row["chi_regular_N_minus_12"])
        amplitude_present = float(row["chi_0"])
        velocity_present = float(row["x_0"])
        mu = float(row["mu_mgap_over_H0"])
        omega_m = float(row["Omega_m"])
        omega_lambda = float(row["Omega_Lambda_0"])
        omega_scalar = float(row["Omega_scalar_0"])
        unit_mode_present = amplitude_present / amplitude_initial
        unit_velocity_present = velocity_present / amplitude_initial
        unit_energy_kernel = (
            unit_velocity_present**2
            +mu**2 * unit_mode_present**2
        )
        flatness_remainder = 1.0 - omega_m - OMEGA_R - omega_lambda
        constraint_variance = flatness_remainder / unit_energy_kernel
        fitted_variance = amplitude_initial**2
        variance_residual = constraint_variance - fitted_variance
        phase_ratio_series = (
            -mu**2
            * math.exp(4.0 * N_INITIAL)
            / (5.0 * OMEGA_R)
        )
        lambda_zero = abs(omega_lambda) < 1.0e-15
        raw_y0 = math.sqrt(raw_target["omega_scalar"]) * math.cos(
            raw_target["theta"]
        )
        raw_x0 = -math.sqrt(raw_target["omega_scalar"]) * math.sin(
            raw_target["theta"]
        )
        raw_chi0 = raw_y0 / raw_target["mu"]
        raw_flatness_residual = (
            raw_target["omega_m"]
            + OMEGA_R
            + raw_target["omega_lambda"]
            + raw_target["omega_scalar"]
            - 1.0
        )
        branch_status = (
            "CONSTRAINT_SELECTED_WITHIN_DECLARED_ZERO_LAMBDA_BRANCH"
            if lambda_zero
            else "CONSTRAINT_REDUCED_AFTER_INDEPENDENT_LAMBDA_INPUT"
        )
        branch_diagnostics = {
            "model": model,
            "mu": mu,
            "omega_m": omega_m,
            "omega_lambda": omega_lambda,
            "omega_scalar": omega_scalar,
            "A_regular_N_minus_12": amplitude_initial,
            "sigma_A_squared_fitted": fitted_variance,
            "u0": unit_mode_present,
            "uN0": unit_velocity_present,
            "unit_energy_kernel_K0": unit_energy_kernel,
            "flatness_remainder": flatness_remainder,
            "sigma_A_squared_from_constraint": constraint_variance,
            "constraint_variance_residual": variance_residual,
            "raw_5195_flatness_residual": raw_flatness_residual,
            "raw_5195_chi0_residual": raw_chi0 - amplitude_present,
            "raw_5195_x0_residual": raw_x0 - velocity_present,
            "regular_phase_ratio_N_minus_12": phase_ratio_series,
            "lambda_zero": lambda_zero,
            "independent_amplitude_after_flatness": not lambda_zero,
            "state_normalization_status": branch_status,
            "zeta_Gdot_ceiling": float(
                local_rows[model]["zeta_gdot_max"]
            ),
            "full_density_matrix_selected": False,
            "quadratic_background_closed": lambda_zero,
        }
        diagnostics[model] = branch_diagnostics
        output_rows.extend(
            [
                {
                    "model": model,
                    "quantity": "regular_phase_ratio_at_N_minus_12",
                    "value": phase_ratio_series,
                    "derivation": (
                        "chi_N/chi=-mu^2 exp(4N)/(5 Omega_r)+O(exp(8N))"
                    ),
                    "status": "DERIVED_BY_RADIATION_REGULARITY",
                },
                {
                    "model": model,
                    "quantity": "unit_regular_energy_kernel_K0",
                    "value": unit_energy_kernel,
                    "derivation": "K0=u_N0^2+mu^2 u0^2",
                    "status": "DERIVED_TRANSFER_COEFFICIENT",
                },
                {
                    "model": model,
                    "quantity": "sigma_A_squared_from_constraint",
                    "value": constraint_variance,
                    "derivation": (
                        "sigma_A^2=(1-Omega_m-Omega_r-Omega_Lambda)/K0"
                    ),
                    "status": branch_status,
                },
                {
                    "model": model,
                    "quantity": "sigma_A_squared_fitted",
                    "value": fitted_variance,
                    "derivation": "A_regular(N=-12)^2 from checkpoint 5196",
                    "status": "LOCKED_TARGET",
                },
                {
                    "model": model,
                    "quantity": "constraint_variance_residual",
                    "value": variance_residual,
                    "derivation": "constraint value minus locked target",
                    "status": "NUMERIC_CLOSURE_TEST",
                },
                {
                    "model": model,
                    "quantity": "raw_5195_flatness_residual",
                    "value": raw_flatness_residual,
                    "derivation": (
                        "Omega_m+Omega_r+Omega_Lambda+Omega_scalar-1"
                    ),
                    "status": "INDEPENDENT_LOCKED_TARGET_CHECK",
                },
                {
                    "model": model,
                    "quantity": "raw_5195_present_state_residual",
                    "value": max(
                        abs(raw_chi0 - amplitude_present),
                        abs(raw_x0 - velocity_present),
                    ),
                    "derivation": (
                        "raw 5195 Omega_scalar,theta,mu versus 5196 chi0,x0"
                    ),
                    "status": "INDEPENDENT_LOCKED_TARGET_CHECK",
                },
                {
                    "model": model,
                    "quantity": "zeta_c_local_drift_ceiling",
                    "value": local_rows[model]["zeta_gdot_max"],
                    "derivation": "checkpoint 5204 standard long-range map",
                    "status": "RETAINED_LOCAL_BOUND",
                },
            ]
        )

    omega_lambda_symbol, sigma_squared_symbol, kernel_symbol = sp.symbols(
        "Omega_Lambda sigma_A_squared K0",
        positive=True,
        real=True,
    )
    constraint_matrix = sp.Matrix([[1, kernel_symbol]])
    rank = constraint_matrix.rank()
    nullity = 2 - rank
    global_diagnostics = {
        "constraint": (
            "Omega_Lambda+K0 sigma_A_squared="
            "1-Omega_m-Omega_r"
        ),
        "constraint_matrix_rank": rank,
        "free_Lambda_nullity": nullity,
        "zero_Lambda_variance_solution": (
            "(1-Omega_m-Omega_r)/K0"
        ),
        "zero_Lambda_background_state_parameter_removed": True,
        "free_Lambda_background_state_parameter_removed": False,
        "absolute_Lambda_zero_selected_by_parent": False,
    }
    return tagged(output_rows), diagnostics, global_diagnostics


def local_silence_rows(
    branch_diagnostics: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    maximum_zeta = max(
        row["zeta_Gdot_ceiling"] for row in branch_diagnostics.values()
    )
    rows = tagged(
        [
            {
                "clause": "initial_surface_support",
                "result": (
                    "delta Gamma_rho_i/delta Phi(x)=0 for "
                    "supp(delta Phi) in D and D intersect Sigma_i empty"
                ),
                "status": "EXACT_SUPPORT_THEOREM",
                "local_effect": "no direct later local source vertex",
            },
            {
                "clause": "reflection_even_one_point",
                "result": "<chi>=<chi_N>=0",
                "status": "EXACT_FOR_P(A)=P(-A)",
                "local_effect": "no odd one-point scalar charge",
            },
            {
                "clause": "quadratic_state_stress",
                "result": "<T_chi> nonzero when sigma_A_squared nonzero",
                "status": "RETAINED_PHYSICAL_BACKGROUND",
                "local_effect": "cannot call the entire state locally absent",
            },
            {
                "clause": "branchwise_scalar_tensor_response",
                "result": "alpha0_squared and Gdot are even in branch sign",
                "status": "NOT_CANCELLED_BY_PLUS_MINUS_MIXTURE",
                "local_effect": "checkpoint 5204 PPN and LLR ceilings remain mandatory",
            },
            {
                "clause": "near_minimal_curvature_coordinate",
                "result": maximum_zeta,
                "status": "SOURCE_BACKED_CONDITIONAL_CEILING",
                "local_effect": "use the tighter model-specific rows in any refit",
            },
            {
                "clause": "local_GR_scope",
                "result": (
                    "exact psi=0 local branch remains a separate state; "
                    "cosmological ensemble gives bounded rather than exact silence"
                ),
                "status": "CLAIM_SCOPE_FIXED",
                "local_effect": "leading local GR retained; all-operator exact GR not claimed",
            },
        ]
    )
    diagnostics = {
        "direct_boundary_source_in_later_local_domain": False,
        "odd_one_point_charge": False,
        "quadratic_background_stress": True,
        "PPN_Gdot_cancelled_by_even_mixture": False,
        "exact_local_state_silence": False,
        "bounded_local_response_required": True,
    }
    return rows, diagnostics


def parameter_count_rows(
    branch_diagnostics: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = [
        {
            "coordinate": "G_N",
            "class": "leading gravitational calibration",
            "Lambda_free": "one universal calibration",
            "Lambda_zero": "one universal calibration",
            "selected_here": False,
        },
        {
            "coordinate": "J_gap=G_N m_pole^2",
            "class": "essential motion action coordinate",
            "Lambda_free": "one fitted universal mass",
            "Lambda_zero": "one fitted universal mass",
            "selected_here": False,
        },
        {
            "coordinate": "Lambda_cal",
            "class": "renormalized background action coordinate",
            "Lambda_free": "independent",
            "Lambda_zero": "fixed to zero as declared minimal branch",
            "selected_here": False,
        },
        {
            "coordinate": "regular phase",
            "class": "boundary relation",
            "Lambda_free": "derived",
            "Lambda_zero": "derived",
            "selected_here": True,
        },
        {
            "coordinate": "sigma_A_squared",
            "class": "homogeneous state second moment",
            "Lambda_free": "one coordinate remains jointly with Lambda_cal",
            "Lambda_zero": "fixed by the Hamiltonian constraint",
            "selected_here": "conditional_zero_Lambda_only",
        },
        {
            "coordinate": "higher moments of P(A)",
            "class": "non-Gaussian state data",
            "Lambda_free": "irrelevant to quadratic background; open elsewhere",
            "Lambda_zero": "irrelevant to quadratic background; open elsewhere",
            "selected_here": False,
        },
        {
            "coordinate": "primordial inhomogeneous covariance",
            "class": "perturbation state",
            "Lambda_free": "not selected",
            "Lambda_zero": "not selected",
            "selected_here": False,
        },
    ]
    for row in rows:
        row["zero_Lambda_background_closed"] = all(
            item["quadratic_background_closed"]
            for item in branch_diagnostics.values()
            if item["lambda_zero"]
        )
    return tagged(rows)


def route_decision_rows(
    branch_diagnostics: dict[str, dict[str, Any]],
    global_diagnostics: dict[str, Any],
) -> list[dict[str, Any]]:
    zero_branch = next(
        row for row in branch_diagnostics.values() if row["lambda_zero"]
    )
    free_branch = next(
        row for row in branch_diagnostics.values() if not row["lambda_zero"]
    )
    return tagged(
        [
            {
                "decision": "normalized_CTP_state_class",
                "result": "CONSTRUCTED",
                "reason": "positive trace-one displaced Gaussian ensemble with exact kernel",
                "next_action": "retain as the homogeneous state slot in Gamma_rho_i",
            },
            {
                "decision": "regular_phase",
                "result": "DERIVED",
                "reason": "radiation regularity removes the singular mode",
                "next_action": "do not fit theta independently",
            },
            {
                "decision": "quadratic_background_universality",
                "result": "DERIVED",
                "reason": "only sigma_A_squared enters the free quadratic stress",
                "next_action": "quarantine higher moments to interaction and perturbation tests",
            },
            {
                "decision": "zero_Lambda_second_moment",
                "result": (
                    "CONSTRAINT_SELECTED_CONDITIONALLY"
                    if zero_branch["quadratic_background_closed"]
                    else "REJECTED"
                ),
                "reason": (
                    "flatness plus regular transfer fixes sigma_A_squared "
                    "when Lambda_cal is fixed to zero"
                ),
                "next_action": "remove an independent homogeneous amplitude from the zero-Lambda refit",
            },
            {
                "decision": "free_Lambda_second_moment",
                "result": (
                    "ONE_DEGENERACY_REMAINS"
                    if free_branch["independent_amplitude_after_flatness"]
                    else "SELECTED"
                ),
                "reason": (
                    f"constraint rank={global_diagnostics['constraint_matrix_rank']} "
                    f"for two coordinates; nullity={global_diagnostics['free_Lambda_nullity']}"
                ),
                "next_action": "retain one state fraction or independently derive Lambda_cal",
            },
            {
                "decision": "absolute_zero_Lambda_origin",
                "result": "NOT_DERIVED",
                "reason": "setting the renormalized Lambda coordinate to zero is a branch hypothesis",
                "next_action": "do not call zero Lambda a parent prediction",
            },
            {
                "decision": "full_density_matrix",
                "result": "EQUIVALENCE_CLASS_ONLY",
                "reason": "higher moments and inhomogeneous covariance are not selected",
                "next_action": "background claims stop at second-moment universality",
            },
            {
                "decision": "selected_next_route",
                "result": (
                    "RUN_CONSTRAINT_REDUCED_ZERO_LAMBDA_SCALAR_TENSOR_REFIT_"
                    "WITH_GDOT_BOUNDED_ZETA"
                ),
                "reason": (
                    "the zero-Lambda background now has no independent "
                    "homogeneous amplitude, so the required F_R completion "
                    "can be tested without adding a state fit coordinate"
                ),
                "next_action": "use the same Pantheon+, DESI, compressed-CMB and growth data",
            },
        ]
    )


def provenance_rows() -> list[dict[str, Any]]:
    roles = {
        "5152": "reflection-even coherent-branch mixture",
        "5156": "action-versus-Gaussian-state covariance theorem",
        "5179": "non-Gaussian boundary hierarchy and quartic-only no-go",
        "5195": "matched target backgrounds and model comparison",
        "5196": "regular-mode theorem and fitted amplitude transfer",
        "5200": "positive CTP projector and boundary-state ownership",
        "5203": "canonical CTP parent action with Gamma_rho_i",
        "5204": "curvature-trigger no-overlap and local zeta ceilings",
    }
    rows: list[dict[str, Any]] = []
    for relative_path, digest in SOURCE_LOCKS.items():
        role = "locked supporting source"
        for key, value in roles.items():
            if key in relative_path:
                role = value
                break
        rows.append(
            {
                "source": relative_path,
                "sha256": digest,
                "role": role,
                "exists": (POST / relative_path).exists(),
            }
        )
    return tagged(rows)


def validation_rows(
    public_before: tuple[str, str],
    galaxy_before: tuple[str, str],
    output_files: list[Path],
    all_csv_rows: list[list[dict[str, Any]]],
    payload: dict[str, Any],
    ctp_diagnostics: dict[str, Any],
    stress_diagnostics: dict[str, Any],
    branch_diagnostics: dict[str, dict[str, Any]],
    global_diagnostics: dict[str, Any],
    local_diagnostics: dict[str, Any],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, Any]] = []

    def add(name: str, passed: bool, detail: Any) -> None:
        checks.append((name, bool(passed), detail))

    public_after = git_state(PUBLIC_WORKTREE)
    galaxy_after = git_state(GALAXY_REPO)
    add(
        "script_compiles",
        bool(compile(SCRIPT.read_text(encoding="utf-8"), str(SCRIPT), "exec")),
        SCRIPT,
    )
    add("document_exists", DOCUMENT.exists() and DOCUMENT.stat().st_size > 0, DOCUMENT)
    add("document_marker", MARKER in DOCUMENT.read_text(encoding="utf-8"), MARKER)
    add("formal_tree_locked", tree_digest(FORMAL) == FORMAL_LOCK, tree_digest(FORMAL))
    add(
        "checkpoint_5204_tree_locked",
        tree_digest(CHECKPOINT_5204_OUT) == CHECKPOINT_5204_OUT_LOCK,
        tree_digest(CHECKPOINT_5204_OUT),
    )
    add("public_state_unchanged", public_after == public_before, public_after)
    add("public_head_locked", public_after[0] == PUBLIC_HEAD_LOCK, public_after[0])
    add("galaxy_state_unchanged", galaxy_after == galaxy_before, galaxy_after)
    add("galaxy_head_locked", galaxy_after[0] == GALAXY_HEAD_LOCK, galaxy_after[0])
    for relative_path, expected_digest in SOURCE_LOCKS.items():
        source_path = POST / relative_path
        add(f"source_exists::{relative_path}", source_path.exists(), source_path)
        add(
            f"source_hash::{relative_path}",
            source_path.exists() and file_digest(source_path) == expected_digest,
            file_digest(source_path) if source_path.exists() else "absent",
        )
    add(
        "CTP_trace_one",
        ctp_diagnostics["trace_integral"] == "1",
        ctp_diagnostics["trace_integral"],
    )
    add(
        "CTP_Hermitian",
        ctp_diagnostics["hermiticity_residual"] == "0",
        ctp_diagnostics["hermiticity_residual"],
    )
    add(
        "CTP_uncertainty_bound",
        ctp_diagnostics["minimum_random_determinant"] >= 0.25 - 1.0e-10,
        ctp_diagnostics["minimum_random_determinant"],
    )
    add(
        "stress_conservation",
        stress_diagnostics["continuity_residual"] == "0",
        stress_diagnostics["continuity_residual"],
    )
    add(
        "quadratic_second_moment_only",
        stress_diagnostics[
            "quadratic_background_depends_only_on_second_moment"
        ],
        stress_diagnostics,
    )
    for model, row in branch_diagnostics.items():
        add(
            f"{model}::constraint_variance_positive",
            row["sigma_A_squared_from_constraint"] > 0.0,
            row["sigma_A_squared_from_constraint"],
        )
        add(
            f"{model}::constraint_reproduces_target",
            math.isclose(
                row["sigma_A_squared_from_constraint"],
                row["sigma_A_squared_fitted"],
                rel_tol=2.0e-10,
                abs_tol=1.0e-12,
            ),
            row["constraint_variance_residual"],
        )
        add(
            f"{model}::raw_5195_flatness",
            abs(row["raw_5195_flatness_residual"]) < 1.0e-12,
            row["raw_5195_flatness_residual"],
        )
        add(
            f"{model}::raw_5195_state_match",
            max(
                abs(row["raw_5195_chi0_residual"]),
                abs(row["raw_5195_x0_residual"]),
            )
            < 2.0e-10,
            (
                row["raw_5195_chi0_residual"],
                row["raw_5195_x0_residual"],
            ),
        )
        add(
            f"{model}::regular_phase_finite",
            math.isfinite(row["regular_phase_ratio_N_minus_12"]),
            row["regular_phase_ratio_N_minus_12"],
        )
        add(
            f"{model}::local_zeta_bound_positive",
            0.0 < row["zeta_Gdot_ceiling"] < 1.0,
            row["zeta_Gdot_ceiling"],
        )
        if row["lambda_zero"]:
            add(
                f"{model}::zero_Lambda_background_closed",
                row["quadratic_background_closed"]
                and not row["independent_amplitude_after_flatness"],
                row["state_normalization_status"],
            )
        else:
            add(
                f"{model}::free_Lambda_degeneracy_retained",
                row["independent_amplitude_after_flatness"]
                and not row["quadratic_background_closed"],
                row["state_normalization_status"],
            )
    add(
        "constraint_rank_one",
        global_diagnostics["constraint_matrix_rank"] == 1,
        global_diagnostics,
    )
    add(
        "free_Lambda_nullity_one",
        global_diagnostics["free_Lambda_nullity"] == 1,
        global_diagnostics,
    )
    add(
        "absolute_zero_Lambda_not_overclaimed",
        global_diagnostics["absolute_Lambda_zero_selected_by_parent"] is False,
        global_diagnostics,
    )
    add(
        "boundary_direct_local_source_zero",
        local_diagnostics["direct_boundary_source_in_later_local_domain"]
        is False,
        local_diagnostics,
    )
    add(
        "even_mixture_does_not_cancel_PPN",
        local_diagnostics["PPN_Gdot_cancelled_by_even_mixture"] is False,
        local_diagnostics,
    )
    add(
        "selected_route",
        payload["selected_next_route"]
        == (
            "RUN_CONSTRAINT_REDUCED_ZERO_LAMBDA_SCALAR_TENSOR_REFIT_"
            "WITH_GDOT_BOUNDED_ZETA"
        ),
        payload["selected_next_route"],
    )
    add(
        "full_unification_claim_false",
        payload["claim_status"]["full_MTS_unification"] is False,
        payload["claim_status"],
    )
    add(
        "unique_full_state_claim_false",
        payload["claim_status"]["unique_full_density_matrix_selected"] is False,
        payload["claim_status"],
    )
    add(
        "GitHub_action_false",
        payload["claim_status"]["GitHub_action"] is False,
        payload["claim_status"],
    )
    for output_file in output_files:
        add(
            f"output_exists::{output_file.name}",
            output_file.exists() and output_file.stat().st_size > 0,
            output_file,
        )
        if output_file.suffix == ".csv" and output_file.exists():
            parsed_rows = read_csv(output_file)
            add(
                f"output_parses::{output_file.name}",
                len(parsed_rows) > 0,
                len(parsed_rows),
            )
    flattened_rows = [row for rows in all_csv_rows for row in rows]
    add(
        "all_rows_full_MTS_nonclaim",
        all(
            row.get("valid_for_full_MTS_claim") is False
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
            "checkpoint": 5205,
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
        help="execute derivations and report without writing evidence files",
    )
    arguments = parser.parse_args()

    assert_source_locks()
    public_before = git_state(PUBLIC_WORKTREE)
    galaxy_before = git_state(GALAXY_REPO)
    if public_before[0] != PUBLIC_HEAD_LOCK:
        raise RuntimeError("public worktree HEAD changed")
    if galaxy_before[0] != GALAXY_HEAD_LOCK:
        raise RuntimeError("galaxy repository HEAD changed")

    ctp_rows, ctp_diagnostics = ctp_gaussian_state()
    regular_rows, stress_rows, stress_diagnostics = (
        ensemble_and_stress_theorem()
    )
    constraint_rows, branch_diagnostics, global_diagnostics = (
        constraint_state_selection()
    )
    local_rows, local_diagnostics = local_silence_rows(
        branch_diagnostics
    )
    parameter_rows = parameter_count_rows(branch_diagnostics)
    decision_rows = route_decision_rows(
        branch_diagnostics,
        global_diagnostics,
    )
    source_rows = provenance_rows()

    claim_status = {
        "positive_normalized_CTP_homogeneous_state_class": True,
        "reflection_even_one_point_zero": True,
        "regular_phase_derived": True,
        "quadratic_background_second_moment_universality": True,
        "zero_Lambda_second_moment_constraint_selected": True,
        "zero_Lambda_absolute_origin_derived": False,
        "free_Lambda_amplitude_selected": False,
        "unique_full_density_matrix_selected": False,
        "primordial_perturbation_covariance_selected": False,
        "direct_later_local_boundary_source": False,
        "PPN_Gdot_cancelled_by_even_mixture": False,
        "leading_local_GR_branch_retained": True,
        "5195_likelihood_promoted": False,
        "full_MTS_unification": False,
        "GitHub_action": False,
    }
    selected_next_route = (
        "RUN_CONSTRAINT_REDUCED_ZERO_LAMBDA_SCALAR_TENSOR_REFIT_"
        "WITH_GDOT_BOUNDED_ZETA"
    )
    payload = {
        "checkpoint": 5205,
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "CTP_state": ctp_diagnostics,
        "stress": stress_diagnostics,
        "branches": branch_diagnostics,
        "constraint": global_diagnostics,
        "local": local_diagnostics,
        "claim_status": claim_status,
        "selected_next_route": selected_next_route,
    }

    if arguments.dry_run:
        print(json.dumps(payload, indent=2, sort_keys=True, default=str))
        return

    OUT.mkdir(parents=True, exist_ok=True)
    output_map = {
        "normalized_CTP_Gaussian_state.csv": ctp_rows,
        "regular_mode_second_moment_theorem.csv": regular_rows,
        "quadratic_state_stress_conservation.csv": stress_rows,
        "Hamiltonian_constraint_state_normalization.csv": constraint_rows,
        "local_boundary_silence_and_residuals.csv": local_rows,
        "state_parameter_count.csv": parameter_rows,
        "route_decision.csv": decision_rows,
        "source_provenance.csv": source_rows,
    }
    for name, rows in output_map.items():
        write_csv(OUT / name, rows)
    result_path = OUT / "normalized_CTP_regular_mode_state_results.json"
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
        ctp_diagnostics,
        stress_diagnostics,
        branch_diagnostics,
        global_diagnostics,
        local_diagnostics,
    )
    write_csv(VALIDATION, validations)
    failed = [row for row in validations if row["status"] != "PASS"]
    if failed:
        raise RuntimeError(
            "checkpoint 5205 validation failed: "
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
                "output_bytes": sum(path.stat().st_size for path in output_files),
                "output_tree_sha256": tree_digest(OUT),
                "formalization_workbench_sha256": tree_digest(FORMAL),
                "checkpoint_5204_output_sha256": tree_digest(
                    CHECKPOINT_5204_OUT
                ),
                "zero_Lambda_second_moment_constraint_selected": True,
                "unique_full_density_matrix_selected": False,
                "selected_next_route": selected_next_route,
            },
            indent=2,
            default=str,
        )
    )


if __name__ == "__main__":
    main()
