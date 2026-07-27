from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

import numpy as np
import sympy as sp
from scipy import optimize


sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()
OUT = POST / "source-intake" / "functional_rg" / "5204"
DOCUMENT = (
    POST
    / "5204-Y5-R2FR-curvature-triggered-homogeneous-motion-state-local-"
    "PPN-Gdot-and-preparation-no-overlap-theorem.md"
)
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5204_VALIDATION.csv"
)
CHECKPOINT_5203_OUT = POST / "source-intake" / "functional_rg" / "5203"
PUBLIC_WORKTREE = Path(
    r"C:\Users\ollet\OneDrive\Documents\Motion-TimeSpace-public-update-2026-07-22"
)
GALAXY_REPO = Path(r"D:\Users\ollet\Desktop\MTS-Galaxy-Lab-repo")

MARKER = "MTS_5204_CURVATURE_TRIGGERED_MOTION_STATE_NO_OVERLAP"
CHECKED_DATE = "2026-07-24"
FORMAL_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5203_OUT_LOCK = (
    "acb402fb2b8b9b5add00884ade75a720675b3f62fc3bf45a5de86038b00e9eeb"
)
PUBLIC_HEAD_LOCK = "8913c00b77d98e457ddb0c48e9aeec9cc5f309fd"
GALAXY_HEAD_LOCK = "f850e4997657f457dddc05cbe50f21186588dcc7"

SOURCE_LOCKS = {
    "4886-Y5-R2FR-canonical-memory-scalar-local-screening-scalarization-and-same-parent-cosmology-compatibility-gate.md": (
        "164ed70e5b269f98474a37b07aa52d46c2fdd80fa0f9b8f491351cb31bc61769"
    ),
    "4950-Y5-R2FR-reflection-even-pair-source-operator-Rpsi2-Tpsi2-and-stabilized-galaxy-bifurcation-window-or-route-rejection.md": (
        "64188638f5d19e125e5c1305cce898332267295b26625c1492610a3c529774cf"
    ),
    "4951-Y5-R2FR-coupled-motion-VFZX2-functional-flow-fixed-point-index-and-GR-connected-trajectory-or-even-pair-sector-rejection.md": (
        "1dd7f2632ab15370e7b44272c2439a6cf70d5559b1c7993b6f55d7e9fab9a131"
    ),
    "5193-Y5-R2FR-direct-parent-scalar-Pantheon-DESI-likelihood-and-model-selection-gate.md": (
        "277a74bf5d75238831d87a5c778a7ac8da2c226d2eafb5ec30203b6fda067dd9"
    ),
    "5195-Y5-R2FR-matched-joint-CMB-informed-parent-refit-and-physical-sound-horizon-gate.md": (
        "217fdc07f94e18a21fe996f7592930f69c21ba16b3fe44b1fd1a2518d9d54737"
    ),
    "5203-Y5-R2FR-one-canonical-translation-gauge-parent-action-cross-coupling-and-branch-reduction-theorem.md": (
        "0c456634e22a3f6e03ce648fe34c28e5557d562a47249b04201a2602b67c8a6b"
    ),
    "source-intake/functional_rg/4950/pair_operator_RG_and_bifurcation_results.json": (
        "9243cf84c42036cddb29a267e6d425cc0f443d74410af11965542e0470860860"
    ),
    "source-intake/functional_rg/4951/coupled_VFZX2_fixed_and_running_gate_results.json": (
        "d48c187595a71c3be6c2720a7545372d06361788a2fb242b902ef8e4bfe6ad8c"
    ),
    "source-intake/functional_rg/5195/joint_CMB_informed_refit_results.json": (
        "538078e466c2ee9f02e5204090b9e1c87c8c56b5680c366289336dda4abdf3ad"
    ),
    "source-intake/functional_rg/5203/canonical_translation_parent_action_results.json": (
        "4199e389c41acf8b7c4414912afd88b616429440e90952e80553a235f528b2fe"
    ),
    "source-intake/local_bounds/local_bound_claims.csv": (
        "a187baf4566ba59a76007d1b06a55dff3a638d70dd27a8eaf8dc089d7cf774ce"
    ),
    "scripts/Y5_R2FR_5193_direct_parent_scalar_SN_BAO_likelihood.py": (
        "8ae6018f911667c04b2780ff5247786e3c192f58397148b6ba07cebccc0ddb21"
    ),
}

OMEGA_R = 9.0e-5
MPC_KM = 3.0856775814913673e19
SECONDS_PER_YEAR = 365.25 * 86400.0
HBAR_EV_S = 6.582119569e-16
AU_LIGHT_SECONDS = 499.004783836
M_REDUCED_PLANCK_EV = 2.435323210689248e27
TRACKING_ZETA_FLOOR = 1.0 / 6.0
QUARTIC_ENERGY_FRACTION_CEILING = 0.1


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
            "checkpoint": 5204,
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
    if tree_digest(CHECKPOINT_5203_OUT) != CHECKPOINT_5203_OUT_LOCK:
        failures.append("checkpoint-5203 output tree changed")
    if failures:
        raise RuntimeError("source lock failure: " + "; ".join(failures))


def symbolic_derivations() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    psi, mass2, zeta, curvature, lambda4 = sp.symbols(
        "psi mass2 zeta curvature lambda4",
        real=True,
    )
    field_square = sp.symbols("field_square", real=True)
    effective_potential = (
        (mass2 - zeta * curvature) * psi**2 / 2
        + lambda4 * psi**4 / 24
    )
    first_derivative = sp.factor(sp.diff(effective_potential, psi))
    second_derivative = sp.diff(effective_potential, psi, 2)
    branch_square = 6 * (zeta * curvature - mass2) / lambda4
    branch_hessian = sp.simplify(
        second_derivative.subs(psi**2, branch_square)
    )
    potential_in_square = (
        (mass2 - zeta * curvature) * field_square / 2
        + lambda4 * field_square**2 / 24
    )
    branch_depth = sp.simplify(
        potential_in_square.subs(field_square, branch_square)
    )

    flow_denominator = 16 * sp.pi**2
    beta_lambda = 3 * lambda4**2 / flow_denominator
    beta_zeta = (
        lambda4 * (zeta - sp.Rational(1, 6)) / flow_denominator
    )
    flow_invariant = (zeta - sp.Rational(1, 6)) / lambda4 ** sp.Rational(
        1, 3
    )
    invariant_residual = sp.simplify(
        sp.diff(flow_invariant, lambda4) * beta_lambda
        + sp.diff(flow_invariant, zeta) * beta_zeta
    )

    phi = sp.symbols("phi", real=True)
    reduced_curvature_function = 1 + zeta * phi**2
    reduced_curvature_derivative = sp.diff(reduced_curvature_function, phi)
    alpha_squared = sp.factor(
        reduced_curvature_derivative**2
        / (
            2 * reduced_curvature_function
            + 3 * reduced_curvature_derivative**2
        )
    )
    log_einstein_matter_factor = -sp.log(reduced_curvature_function) / 2
    beta_direct_trace = sp.simplify(
        sp.diff(log_einstein_matter_factor, phi, 2).subs(phi, 0) / 2
    )

    rows = tagged(
        [
            {
                "derivation": "canonical_curvature_coordinate",
                "result": (
                    "chi=sqrt(Z0) psi; zeta_c=F_R''(0)/(2 Z0); "
                    "F_R=M_R^2+zeta_c chi^2+O(chi^4)"
                ),
                "status": "EXACT_FIELD_REDEFINITION",
                "implication": (
                    "xi_4951=zeta_c=xi2_5203/(2 Z0); the factor of two "
                    "is fixed before applying the Hessian or beta function"
                ),
            },
            {
                "derivation": "effective_potential",
                "result": str(effective_potential),
                "status": "EXACT_FIXED_CURVATURE_ONSET_FUNCTIONAL",
                "implication": "X2 and higher even derivative terms do not enter linear onset",
            },
            {
                "derivation": "stationarity_equation",
                "result": str(first_derivative),
                "status": "EXACT",
                "implication": "psi=0 remains an exact solution; no additive source appears",
            },
            {
                "derivation": "broken_branch_amplitude",
                "result": "chi_star^2=6(zeta_c R-m_pole^2)/lambda4",
                "status": "EXACT_FOR_LAMBDA4_POSITIVE",
                "implication": "nonzero extrema exist only for zeta_c R>m_pole^2",
            },
            {
                "derivation": "broken_branch_hessian",
                "result": str(branch_hessian),
                "status": "EXACT",
                "implication": "the two nonzero extrema are stable when lambda4>0",
            },
            {
                "derivation": "broken_branch_depth",
                "result": str(branch_depth),
                "status": "EXACT",
                "implication": "the pitchfork is continuous and returns to zero at restoration",
            },
            {
                "derivation": "matter_era_linear_exponent",
                "result": (
                    "s_plus=(-3/2+sqrt(9/4+12 zeta_c))/2 for "
                    "m_pole^2/H^2 negligible"
                ),
                "status": "EXACT_MATTER_ERA_LINEARIZATION",
                "implication": "s_plus=2 zeta_c+O(zeta_c^2) on the GR-connected branch",
            },
            {
                "derivation": "deep_matter_radial_tracking_mass",
                "result": "m_rad^2/H^2 -> 6 zeta_c",
                "status": "EXACT_DEEP_BROKEN_MATTER_LIMIT",
                "implication": "even the weak requirement m_rad>=H needs zeta_c>=1/6",
            },
            {
                "derivation": "Einstein_frame_matter_factor",
                "result": "A_E^2=M_R^2/F_R=(1+zeta_c phi^2)^-1",
                "status": "EXACT_JORDAN_TO_EINSTEIN_MAP",
                "implication": "Jordan-minimal matter still has scalar-tensor PPN pressure at phi0 nonzero",
            },
            {
                "derivation": "DEF_coupling",
                "result": str(alpha_squared),
                "status": "EXACT_CANONICAL_SINGLE_SCALAR_MAP",
                "implication": "gamma-1=-2 alpha0^2/(1+alpha0^2) in the long-range unscreened limit",
            },
            {
                "derivation": "relation_to_4886_direct_trace_beta",
                "result": f"beta_4886={beta_direct_trace}",
                "status": "EXACT_SMALL_FIELD_MAP",
                "implication": "4886 is not copied; its beta corresponds to -zeta_c/2 here",
            },
            {
                "derivation": "one_loop_joint_flow_invariant",
                "result": "(zeta_c-1/6)/lambda4^(1/3)=constant",
                "status": "EXACT_IN_4951_FIXED_BACKGROUND_COMPARATOR",
                "implication": "the comparator does not select the physical infrared zeta_c",
            },
        ]
    )
    diagnostics = {
        "first_derivative": str(first_derivative),
        "zero_branch_hessian": str(second_derivative.subs(psi, 0)),
        "broken_branch_hessian": str(branch_hessian),
        "broken_branch_depth": str(branch_depth),
        "flow_invariant_residual": str(invariant_residual),
        "alpha_squared": str(alpha_squared),
        "beta_4886_map": str(beta_direct_trace),
        "canonical_zeta_definition": "zeta_c=F_R''(0)/(2 Z0)",
    }
    return rows, diagnostics


def alpha_squared(zeta: float, phi: float) -> float:
    reduced_f = 1.0 + zeta * phi**2
    reduced_f_prime = 2.0 * zeta * phi
    return reduced_f_prime**2 / (
        2.0 * reduced_f + 3.0 * reduced_f_prime**2
    )


def gamma_minus_one(zeta: float, phi: float) -> float:
    coupling_squared = alpha_squared(zeta, phi)
    return -2.0 * coupling_squared / (1.0 + coupling_squared)


def gcav_ratio(zeta: float, phi: float) -> float:
    reduced_f = 1.0 + zeta * phi**2
    reduced_f_prime = 2.0 * zeta * phi
    return (
        (2.0 * reduced_f + 4.0 * reduced_f_prime**2)
        / (2.0 * reduced_f + 3.0 * reduced_f_prime**2)
        / reduced_f
    )


def dln_gcav_dphi(zeta: float, phi: float) -> float:
    reduced_f = 1.0 + zeta * phi**2
    reduced_f_prime = 2.0 * zeta * phi
    reduced_f_second = 2.0 * zeta
    numerator = 2.0 * reduced_f + 4.0 * reduced_f_prime**2
    denominator = 2.0 * reduced_f + 3.0 * reduced_f_prime**2
    return (
        -reduced_f_prime / reduced_f
        + (
            2.0 * reduced_f_prime
            + 8.0 * reduced_f_prime * reduced_f_second
        )
        / numerator
        - (
            2.0 * reduced_f_prime
            + 6.0 * reduced_f_prime * reduced_f_second
        )
        / denominator
    )


def matter_growth_exponent(zeta: float) -> float:
    return (-1.5 + math.sqrt(2.25 + 12.0 * zeta)) / 2.0


def first_gr_connected_root(
    function: Callable[[float], float],
    target: float,
) -> float:
    grid = np.geomspace(1.0e-12, 1.0, 6000)
    previous_x = float(grid[0])
    previous_value = function(previous_x) - target
    for current in grid[1:]:
        current_x = float(current)
        current_value = function(current_x) - target
        if current_value == 0.0:
            return current_x
        if previous_value * current_value < 0.0:
            return float(
                optimize.brentq(
                    lambda value: function(value) - target,
                    previous_x,
                    current_x,
                    xtol=1.0e-14,
                    rtol=1.0e-13,
                )
            )
        previous_x = current_x
        previous_value = current_value
    raise RuntimeError("no GR-connected positive root in scan domain")


def load_bound_anchors() -> dict[str, Any]:
    path = POST / "source-intake" / "local_bounds" / "local_bound_claims.csv"
    rows = {row["row_id"]: row for row in read_csv(path)}
    cassini = rows["R3_gamma"]
    gdot = rows["R9_Gdot"]
    cassini_envelope = abs(float(cassini["measured_value"])) + 2.0 * float(
        cassini["one_sigma"]
    )
    gdot_envelope = abs(float(gdot["measured_value"])) + 2.0 * float(
        gdot["one_sigma"]
    )
    return {
        "cassini_row": cassini,
        "gdot_row": gdot,
        "cassini_absolute_two_sigma_envelope": cassini_envelope,
        "alpha_squared_envelope": cassini_envelope
        / (2.0 - cassini_envelope),
        "gdot_absolute_two_sigma_envelope_yr_inv": gdot_envelope,
    }


def load_parent_state_targets() -> list[dict[str, Any]]:
    path = (
        POST
        / "source-intake"
        / "functional_rg"
        / "5195"
        / "joint_CMB_informed_refit_results.json"
    )
    payload = json.loads(path.read_text(encoding="utf-8"))
    target_models = {
        "ParentScalar_Lambda_free",
        "ParentScalar_Lambda_zero",
    }
    primary_fits = {
        row["model"]: row
        for row in payload["fits"]
        if row["config"] == "primary_fs8_wCDM_prior"
        and row["model"] in target_models
    }
    state_rows = {
        row["model"]: row
        for row in payload["parent_state_summary"]
        if row["model"] in target_models
    }
    if set(primary_fits) != target_models or set(state_rows) != target_models:
        raise RuntimeError("5195 primary parent rows are incomplete")
    targets: list[dict[str, Any]] = []
    for model in sorted(target_models):
        fit = primary_fits[model]
        state = state_rows[model]
        targets.append(
            {
                "model": model,
                "mu": float(state["mu_mgap_over_H0"]),
                "omega_scalar": float(state["Omega_scalar_0"]),
                "omega_lambda": float(state["Omega_Lambda_0"]),
                "theta": float(state["theta_0"]),
                "w_scalar": float(state["w_scalar_0"]),
                "omega_m": float(fit["params"]["Omega_m"]),
                "H0_km_s_Mpc": float(fit["H0"]),
                "selection_status": state["selection_status"],
            }
        )
    return targets


def load_local_thresholds() -> dict[str, float]:
    path = (
        POST
        / "source-intake"
        / "functional_rg"
        / "4950"
        / "pair_operator_RG_and_bifurcation_results.json"
    )
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {
        key: float(value)
        for key, value in payload["local_massless_thresholds"].items()
    }


def evaluate_parent_targets(
    bounds: dict[str, Any],
    local_thresholds: dict[str, float],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    branch_rows: list[dict[str, Any]] = []
    scan_rows: list[dict[str, Any]] = []
    diagnostics: dict[str, dict[str, Any]] = {}
    neutron_star_threshold = local_thresholds[
        "1.4_solar_mass_12km_neutron_star"
    ]
    for target in load_parent_state_targets():
        model = target["model"]
        mu = target["mu"]
        omega_scalar = target["omega_scalar"]
        theta = target["theta"]
        omega_m = target["omega_m"]
        omega_lambda = target["omega_lambda"]
        w_scalar = target["w_scalar"]
        hubble = target["H0_km_s_Mpc"]
        x0 = -math.sqrt(omega_scalar) * math.sin(theta)
        y0 = math.sqrt(omega_scalar) * math.cos(theta)
        phi0 = math.sqrt(6.0) * y0 / mu
        phi_n0 = math.sqrt(6.0) * x0
        ricci0_over_h02 = (
            3.0 * omega_m
            + 12.0 * omega_lambda
            + 3.0 * omega_scalar * (1.0 - 3.0 * w_scalar)
        )
        hubble_yr_inv = hubble / MPC_KM * SECONDS_PER_YEAR
        hubble_ev = hubble / MPC_KM * HBAR_EV_S
        alpha_squared_limit = bounds["alpha_squared_envelope"]
        gdot_limit = bounds["gdot_absolute_two_sigma_envelope_yr_inv"]

        zeta_ppn = first_gr_connected_root(
            lambda value: alpha_squared(value, phi0),
            alpha_squared_limit,
        )
        zeta_gdot = first_gr_connected_root(
            lambda value: abs(
                dln_gcav_dphi(value, phi0) * phi_n0
            )
            * hubble_yr_inv,
            gdot_limit,
        )
        zeta_broken_today = mu**2 / ricci0_over_h02
        equality_redshift = omega_m / OMEGA_R - 1.0
        exit_redshift_ppn = (
            mu**2 / (3.0 * zeta_ppn * omega_m)
        ) ** (1.0 / 3.0) - 1.0
        exit_redshift_gdot = (
            mu**2 / (3.0 * zeta_gdot * omega_m)
        ) ** (1.0 / 3.0) - 1.0
        ppn_growth_all_matter = math.exp(
            matter_growth_exponent(zeta_ppn)
            * math.log1p(equality_redshift)
        )
        gdot_growth_all_matter = math.exp(
            matter_growth_exponent(zeta_gdot)
            * math.log1p(equality_redshift)
        )
        ppn_growth_to_exit = math.exp(
            matter_growth_exponent(zeta_ppn)
            * math.log(
                (1.0 + equality_redshift)
                / (1.0 + exit_redshift_ppn)
            )
        )
        gdot_growth_to_exit = math.exp(
            matter_growth_exponent(zeta_gdot)
            * math.log(
                (1.0 + equality_redshift)
                / (1.0 + exit_redshift_gdot)
            )
        )
        lambda4_ten_percent_ceiling = (
            12.0
            * QUARTIC_ENERGY_FRACTION_CEILING
            * (mu * hubble_ev) ** 2
            / (phi0**2 * M_REDUCED_PLANCK_EV**2)
        )
        compton_exponent_au = mu * (hubble / MPC_KM) * AU_LIGHT_SECONDS
        conformal_alpha_squared = alpha_squared(TRACKING_ZETA_FLOOR, phi0)
        conformal_gamma = gamma_minus_one(TRACKING_ZETA_FLOOR, phi0)
        conformal_gdot = abs(
            dln_gcav_dphi(TRACKING_ZETA_FLOOR, phi0) * phi_n0
        ) * hubble_yr_inv

        diagnostic = {
            **target,
            "x0": x0,
            "y0": y0,
            "phi0_over_MR": phi0,
            "dphi_dN_0": phi_n0,
            "R0_over_H0_squared": ricci0_over_h02,
            "H0_yr_inv": hubble_yr_inv,
            "H0_eV": hubble_ev,
            "zeta_ppn_max": zeta_ppn,
            "zeta_gdot_max": zeta_gdot,
            "zeta_broken_today_min": zeta_broken_today,
            "zeta_tracking_min": TRACKING_ZETA_FLOOR,
            "broken_to_ppn_ratio": zeta_broken_today / zeta_ppn,
            "broken_to_gdot_ratio": zeta_broken_today / zeta_gdot,
            "tracking_to_ppn_ratio": TRACKING_ZETA_FLOOR / zeta_ppn,
            "tracking_to_gdot_ratio": TRACKING_ZETA_FLOOR / zeta_gdot,
            "delta_F_over_MR2_at_ppn_max": zeta_ppn * phi0**2,
            "delta_F_over_MR2_at_gdot_max": zeta_gdot * phi0**2,
            "alpha_squared_at_gdot_max": alpha_squared(zeta_gdot, phi0),
            "gamma_minus_one_at_ppn_max": gamma_minus_one(
                zeta_ppn, phi0
            ),
            "gamma_minus_one_at_gdot_max": gamma_minus_one(
                zeta_gdot, phi0
            ),
            "gdot_at_ppn_max_yr_inv": abs(
                dln_gcav_dphi(zeta_ppn, phi0) * phi_n0
            )
            * hubble_yr_inv,
            "gdot_at_gdot_max_yr_inv": abs(
                dln_gcav_dphi(zeta_gdot, phi0) * phi_n0
            )
            * hubble_yr_inv,
            "deep_matter_mrad2_over_H2_at_ppn_max": 6.0 * zeta_ppn,
            "deep_matter_mrad2_over_H2_at_gdot_max": 6.0 * zeta_gdot,
            "equality_redshift": equality_redshift,
            "exit_redshift_ppn_matter_comparator": exit_redshift_ppn,
            "exit_redshift_gdot_matter_comparator": exit_redshift_gdot,
            "max_growth_eq_to_today_ppn": ppn_growth_all_matter,
            "max_growth_eq_to_today_gdot": gdot_growth_all_matter,
            "max_growth_eq_to_exit_ppn": ppn_growth_to_exit,
            "max_growth_eq_to_exit_gdot": gdot_growth_to_exit,
            "lambda4_10pct_quadratic_ceiling": lambda4_ten_percent_ceiling,
            "mass_times_AU": compton_exponent_au,
            "minimum_local_compact_threshold": neutron_star_threshold,
            "local_threshold_over_zeta_gdot": neutron_star_threshold
            / zeta_gdot,
            "conformal_alpha_squared": conformal_alpha_squared,
            "conformal_gamma_minus_one": conformal_gamma,
            "conformal_gdot_yr_inv": conformal_gdot,
            "present_broken_and_ppn_overlap": zeta_broken_today <= zeta_ppn,
            "present_broken_and_gdot_overlap": zeta_broken_today <= zeta_gdot,
            "tracking_and_ppn_overlap": TRACKING_ZETA_FLOOR <= zeta_ppn,
            "tracking_and_gdot_overlap": TRACKING_ZETA_FLOOR <= zeta_gdot,
            "curvature_trigger_derives_state": False,
        }
        diagnostics[model] = diagnostic
        branch_rows.append(
            {
                "model": model,
                "quantity": "5195_target_state",
                "value": (
                    f"mu={mu:.16g};Omega_psi={omega_scalar:.16g};"
                    f"theta={theta:.16g};phi0/MR={phi0:.16g};"
                    f"dphi/dN={phi_n0:.16g}"
                ),
                "status": "EMPIRICAL_TARGET_NOT_PARENT_DERIVED",
                "consequence": "nonzero long-range scalar target used for a no-overlap test",
            }
        )
        for quantity, value, status, consequence in [
            (
                "zeta_c_Cassini_ceiling",
                zeta_ppn,
                "SOURCE_BACKED_CONDITIONAL_BOUND",
                "standard long-range Jordan-minimal single-scalar map",
            ),
            (
                "zeta_c_Gdot_ceiling",
                zeta_gdot,
                "SOURCE_BACKED_CONDITIONAL_BOUND",
                "conservative absolute two-sigma LLR envelope",
            ),
            (
                "zeta_c_present_broken_floor",
                zeta_broken_today,
                "DERIVED_TARGET_STATE_FLOOR",
                "zeta_c R0>m_pole^2 required for a nonzero minimum today",
            ),
            (
                "zeta_c_tracking_floor",
                TRACKING_ZETA_FLOOR,
                "DERIVED_MINIMAL_ADIABATIC_FLOOR",
                "m_rad^2/H^2=6 zeta_c >=1 in deep matter",
            ),
            (
                "maximum_linear_growth_equality_to_today_Gdot",
                gdot_growth_all_matter,
                "CONSERVATIVE_DERIVED_UPPER_BOUND",
                "assumes matter curvature and removes the stabilizing mass for the whole interval",
            ),
            (
                "maximum_linear_growth_equality_to_exit_Gdot",
                gdot_growth_to_exit,
                "DERIVED_MATTER_COMPARATOR",
                "actual tachyonic interval is shorter than the all-matter bound",
            ),
            (
                "quartic_10pct_ceiling",
                lambda4_ten_percent_ceiling,
                "DERIVED_FIT_COMPATIBILITY_SCALE",
                "larger lambda4 changes the 5195 quadratic target by more than ten percent",
            ),
            (
                "mass_times_one_AU",
                compton_exponent_au,
                "DERIVED_LONG_RANGE_CHECK",
                "solar-system Yukawa attenuation is negligible",
            ),
            (
                "minimum_local_compact_threshold",
                neutron_star_threshold,
                "INHERITED_4950_SPECTRAL_THRESHOLD",
                "the local compact instability is far weaker than PPN/Gdot pressure here",
            ),
        ]:
            branch_rows.append(
                {
                    "model": model,
                    "quantity": quantity,
                    "value": value,
                    "status": status,
                    "consequence": consequence,
                }
            )

        scan_values = {
            0.0,
            zeta_gdot,
            zeta_ppn,
            zeta_broken_today,
            TRACKING_ZETA_FLOOR,
            neutron_star_threshold,
        }
        scan_values.update(float(value) for value in np.geomspace(1.0e-8, 1.0, 181))
        for scan_zeta in sorted(scan_values):
            scan_alpha_squared = alpha_squared(scan_zeta, phi0)
            scan_gamma = gamma_minus_one(scan_zeta, phi0)
            scan_gdot = abs(
                dln_gcav_dphi(scan_zeta, phi0) * phi_n0
            ) * hubble_yr_inv
            present_broken = (
                scan_zeta * ricci0_over_h02 > mu**2
            )
            ppn_pass = abs(scan_gamma) <= bounds[
                "cassini_absolute_two_sigma_envelope"
            ]
            gdot_pass = scan_gdot <= gdot_limit
            tracking_pass = 6.0 * scan_zeta >= 1.0
            compact_pass = scan_zeta < neutron_star_threshold
            scan_rows.append(
                {
                    "model": model,
                    "zeta_c": scan_zeta,
                    "alpha_squared": scan_alpha_squared,
                    "gamma_minus_one": scan_gamma,
                    "abs_Gdot_over_G_yr_inv": scan_gdot,
                    "present_broken": present_broken,
                    "PPN_pass": ppn_pass,
                    "Gdot_pass": gdot_pass,
                    "tracking_pass": tracking_pass,
                    "compact_stability_pass": compact_pass,
                    "simultaneous_present_selection_and_local_pass": (
                        present_broken
                        and ppn_pass
                        and gdot_pass
                        and tracking_pass
                        and compact_pass
                    ),
                }
            )
    return tagged(branch_rows), tagged(scan_rows), diagnostics


def rg_rows(
    branch_diagnostics: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = tagged(
        [
            {
                "item": "fixed_background_beta_lambda4",
                "result": "beta_lambda4=3 lambda4^2/(16 pi^2)",
                "status": "RECONSTRUCTED_4951_COMPARATOR",
                "decision": "retained as an infrared comparator, not an MTS UV prediction",
            },
            {
                "item": "fixed_background_beta_zeta",
                "result": "beta_zeta=lambda4(zeta_c-1/6)/(16 pi^2)",
                "status": "RECONSTRUCTED_4951_COMPARATOR",
                "decision": "zeta_c=0 is not invariant when lambda4 is nonzero",
            },
            {
                "item": "joint_flow_first_integral",
                "result": "(zeta_c-1/6)/lambda4^(1/3)=constant",
                "status": "EXACT",
                "decision": "one-loop running transports an input invariant; it does not select it",
            },
            {
                "item": "physical_quartic_scale",
                "result": min(
                    row["lambda4_10pct_quadratic_ceiling"]
                    for row in branch_diagnostics.values()
                ),
                "status": "TARGET_COMPATIBILITY_CEILING",
                "decision": (
                    "at the ultralight 5195 target the quartic is so small "
                    "that this infrared beta function cannot dynamically "
                    "select zeta_c over finite cosmological running"
                ),
            },
            {
                "item": "common_packet_status",
                "result": "F_R,V_even,Z,c_X2 trajectory not fully selected",
                "status": "OPEN_BUT_NARROWED",
                "decision": (
                    "near-minimal PPN-safe F_R remains viable; curvature "
                    "triggering is rejected as the missing state selector"
                ),
            },
        ]
    )
    diagnostics = {
        "flow_invariant": "(zeta_c-1/6)/lambda4^(1/3)",
        "physical_zeta_selected": False,
        "physical_lambda4_selected": False,
        "common_packet_rejected": False,
        "curvature_trigger_state_selector_rejected": True,
    }
    return rows, diagnostics


def decision_rows(
    branch_diagnostics: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    all_no_present_overlap = all(
        not row["present_broken_and_gdot_overlap"]
        for row in branch_diagnostics.values()
    )
    all_no_tracking_overlap = all(
        not row["tracking_and_gdot_overlap"]
        for row in branch_diagnostics.values()
    )
    all_growth_small = all(
        row["max_growth_eq_to_today_gdot"] < 1.02
        for row in branch_diagnostics.values()
    )
    return tagged(
        [
            {
                "decision": "4886_scope",
                "result": "NOT_BLINDLY_REUSED",
                "reason": (
                    "4886 tested A=exp(beta phi^2) as a direct trace owner; "
                    "5204 derives A_E^2=M_R^2/F_R from Jordan-minimal matter"
                ),
                "next_action": "retain 4886 only as a normalization cross-check",
            },
            {
                "decision": "current_broken_branch",
                "result": (
                    "REJECTED_BY_NO_OVERLAP"
                    if all_no_present_overlap
                    else "REQUIRES_FURTHER_TEST"
                ),
                "reason": (
                    "zeta_c needed for zeta_c R0>m^2 exceeds the conservative "
                    "LLR Gdot ceiling on both 5195 targets"
                ),
                "next_action": "do not use an instantaneous curvature minimum as the fitted present state",
            },
            {
                "decision": "adiabatic_curvature_preparation",
                "result": (
                    "REJECTED_BY_NO_OVERLAP"
                    if all_no_tracking_overlap
                    else "REQUIRES_FURTHER_TEST"
                ),
                "reason": (
                    "m_rad^2/H^2 tends to 6 zeta_c; local long-range bounds "
                    "force the broken branch to remain overdamped"
                ),
                "next_action": "do not claim the pitchfork dynamically selects the homogeneous amplitude",
            },
            {
                "decision": "linear_seed_amplification",
                "result": (
                    "INSUFFICIENT_AS_SELECTOR"
                    if all_growth_small
                    else "REQUIRES_NONLINEAR_INTEGRATION"
                ),
                "reason": (
                    "a deliberately generous equality-to-today bound changes "
                    "the seed by less than two percent at the Gdot ceiling"
                ),
                "next_action": "treat any surviving amplitude as initial-state data",
            },
            {
                "decision": "common_motion_packet",
                "result": "RETAIN_NEAR_MINIMAL_F_R_ONLY",
                "reason": (
                    "the local GR branch and a small nonminimal coordinate "
                    "survive; the curvature coordinate does not close state selection"
                ),
                "next_action": (
                    "derive a CTP homogeneous-state preparation functional "
                    "or demote the 5195 parent-scalar cosmology to fitted closure"
                ),
            },
            {
                "decision": "selected_next_route",
                "result": (
                    "DERIVE_CTP_HOMOGENEOUS_STATE_PREPARATION_OR_DEMOTE_"
                    "PARENT_SCALAR_COSMOLOGY"
                ),
                "reason": "the bulk curvature-trigger route is now decided rather than left as a coefficient gap",
                "next_action": "start from Gamma_rho_i and require a normalized, conserved, local-GR-safe state",
            },
        ]
    )


def provenance_rows(bounds: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for relative_path, digest in SOURCE_LOCKS.items():
        rows.append(
            {
                "source": relative_path,
                "sha256": digest,
                "role": {
                    "4886": "prior direct-trace scalar-tensor rejection and normalization",
                    "4950": "curvature onset and local compact spectral thresholds",
                    "4951": "canonical Hessian and one-loop joint flow",
                    "5193": "canonical homogeneous scalar coordinates",
                    "5195": "matched fitted target states",
                    "5203": "one canonical translation-gauge parent action",
                    "local_bound": "Cassini gamma and LLR Gdot source anchors",
                }.get(
                    next(
                        (
                            key
                            for key in [
                                "4886",
                                "4950",
                                "4951",
                                "5193",
                                "5195",
                                "5203",
                                "local_bound",
                            ]
                            if key in relative_path
                        ),
                        "",
                    ),
                    "locked supporting source",
                ),
                "exists": (POST / relative_path).exists(),
            }
        )
    rows.extend(
        [
            {
                "source": bounds["cassini_row"]["reference_path_or_url"],
                "sha256": "",
                "role": "Cassini gamma external anchor recorded in local_bound_claims.csv",
                "exists": True,
            },
            {
                "source": bounds["gdot_row"]["reference_path_or_url"],
                "sha256": "",
                "role": "LLR Gdot external anchor recorded in local_bound_claims.csv",
                "exists": True,
            },
        ]
    )
    return tagged(rows)


def validation_rows(
    public_before: tuple[str, str],
    galaxy_before: tuple[str, str],
    output_files: list[Path],
    all_csv_rows: list[list[dict[str, Any]]],
    payload: dict[str, Any],
    symbolic: dict[str, Any],
    branch_diagnostics: dict[str, dict[str, Any]],
    scan_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, Any]] = []

    def add(name: str, passed: bool, detail: Any) -> None:
        checks.append((name, bool(passed), detail))

    public_after = git_state(PUBLIC_WORKTREE)
    galaxy_after = git_state(GALAXY_REPO)
    add("script_compiles", bool(compile(SCRIPT.read_text(encoding="utf-8"), str(SCRIPT), "exec")), SCRIPT)
    add("document_exists", DOCUMENT.exists() and DOCUMENT.stat().st_size > 0, DOCUMENT)
    add("document_marker", MARKER in DOCUMENT.read_text(encoding="utf-8"), MARKER)
    add("formal_tree_locked", tree_digest(FORMAL) == FORMAL_LOCK, tree_digest(FORMAL))
    add(
        "checkpoint_5203_tree_locked",
        tree_digest(CHECKPOINT_5203_OUT) == CHECKPOINT_5203_OUT_LOCK,
        tree_digest(CHECKPOINT_5203_OUT),
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
        "symbolic_flow_invariant",
        symbolic["flow_invariant_residual"] == "0",
        symbolic["flow_invariant_residual"],
    )
    add(
        "canonical_zeta_map",
        symbolic["canonical_zeta_definition"]
        == "zeta_c=F_R''(0)/(2 Z0)",
        symbolic["canonical_zeta_definition"],
    )
    for model, row in branch_diagnostics.items():
        add(
            f"{model}::PPN_ceiling_positive",
            0.0 < row["zeta_ppn_max"] < 1.0,
            row["zeta_ppn_max"],
        )
        add(
            f"{model}::Gdot_ceiling_positive",
            0.0 < row["zeta_gdot_max"] < row["zeta_ppn_max"],
            row["zeta_gdot_max"],
        )
        add(
            f"{model}::PPN_root_reproduces_envelope",
            math.isclose(
                abs(row["gamma_minus_one_at_ppn_max"]),
                payload["bounds"]["Cassini_absolute_two_sigma_envelope"],
                rel_tol=1.0e-9,
                abs_tol=1.0e-12,
            ),
            row["gamma_minus_one_at_ppn_max"],
        )
        add(
            f"{model}::Gdot_root_reproduces_envelope",
            math.isclose(
                row["gdot_at_gdot_max_yr_inv"],
                payload["bounds"]["Gdot_absolute_two_sigma_envelope_yr_inv"],
                rel_tol=1.0e-9,
                abs_tol=1.0e-20,
            ),
            row["gdot_at_gdot_max_yr_inv"],
        )
        finite_difference_step = 1.0e-6
        numeric_dln_gcav_dphi = (
            math.log(
                gcav_ratio(
                    row["zeta_gdot_max"],
                    row["phi0_over_MR"] + finite_difference_step,
                )
            )
            - math.log(
                gcav_ratio(
                    row["zeta_gdot_max"],
                    row["phi0_over_MR"] - finite_difference_step,
                )
            )
        ) / (2.0 * finite_difference_step)
        add(
            f"{model}::analytic_Gdot_derivative",
            math.isclose(
                numeric_dln_gcav_dphi,
                dln_gcav_dphi(
                    row["zeta_gdot_max"],
                    row["phi0_over_MR"],
                ),
                rel_tol=1.0e-7,
                abs_tol=1.0e-10,
            ),
            numeric_dln_gcav_dphi,
        )
        add(
            f"{model}::present_broken_no_overlap",
            row["present_broken_and_gdot_overlap"] is False,
            row["broken_to_gdot_ratio"],
        )
        add(
            f"{model}::tracking_no_overlap",
            row["tracking_and_gdot_overlap"] is False,
            row["tracking_to_gdot_ratio"],
        )
        add(
            f"{model}::growth_bound_small",
            row["max_growth_eq_to_today_gdot"] < 1.02,
            row["max_growth_eq_to_today_gdot"],
        )
        add(
            f"{model}::long_range",
            row["mass_times_AU"] < 1.0e-12,
            row["mass_times_AU"],
        )
        add(
            f"{model}::compact_stability",
            row["zeta_gdot_max"]
            < row["minimum_local_compact_threshold"],
            row["local_threshold_over_zeta_gdot"],
        )
        add(
            f"{model}::curvature_selector_false",
            row["curvature_trigger_derives_state"] is False,
            row["curvature_trigger_derives_state"],
        )
    add(
        "scan_has_no_simultaneous_corridor",
        not any(
            row["simultaneous_present_selection_and_local_pass"]
            for row in scan_rows
        ),
        len(scan_rows),
    )
    add(
        "selected_route",
        payload["selected_next_route"]
        == (
            "DERIVE_CTP_HOMOGENEOUS_STATE_PREPARATION_OR_DEMOTE_"
            "PARENT_SCALAR_COSMOLOGY"
        ),
        payload["selected_next_route"],
    )
    add(
        "full_unification_claim_false",
        payload["claim_status"]["full_MTS_unification"] is False,
        payload["claim_status"],
    )
    add(
        "curvature_preparation_claim_false",
        payload["claim_status"]["curvature_trigger_prepares_5195_state"]
        is False,
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
            "checkpoint": 5204,
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

    bounds = load_bound_anchors()
    local_thresholds = load_local_thresholds()
    symbolic_rows, symbolic_diagnostics = symbolic_derivations()
    branch_rows, scan_rows, branch_diagnostics = evaluate_parent_targets(
        bounds,
        local_thresholds,
    )
    flow_rows, flow_diagnostics = rg_rows(branch_diagnostics)
    route_rows = decision_rows(branch_diagnostics)
    source_rows = provenance_rows(bounds)

    claim_status = {
        "canonical_nonminimal_coordinate_derived": True,
        "homogeneous_pitchfork_law_derived": True,
        "Jordan_minimal_PPN_and_Gdot_map_derived": True,
        "long_range_condition_verified_for_5195_targets": True,
        "local_compact_stability_at_allowed_zeta": True,
        "present_broken_branch_local_bound_overlap": False,
        "adiabatic_tracking_local_bound_overlap": False,
        "curvature_trigger_prepares_5195_state": False,
        "near_minimal_F_R_EFT_coordinate_retained": True,
        "common_F_R_V_Z_X2_trajectory_fully_selected": False,
        "leading_local_GR_branch_retained": True,
        "5195_likelihood_promoted": False,
        "full_MTS_unification": False,
        "GitHub_action": False,
    }
    payload = {
        "checkpoint": 5204,
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "bounds": {
            "Cassini_absolute_two_sigma_envelope": bounds[
                "cassini_absolute_two_sigma_envelope"
            ],
            "alpha_squared_envelope": bounds["alpha_squared_envelope"],
            "Gdot_absolute_two_sigma_envelope_yr_inv": bounds[
                "gdot_absolute_two_sigma_envelope_yr_inv"
            ],
        },
        "symbolic": symbolic_diagnostics,
        "parent_targets": branch_diagnostics,
        "RG": flow_diagnostics,
        "claim_status": claim_status,
        "selected_next_route": (
            "DERIVE_CTP_HOMOGENEOUS_STATE_PREPARATION_OR_DEMOTE_"
            "PARENT_SCALAR_COSMOLOGY"
        ),
    }

    if arguments.dry_run:
        print(json.dumps(payload, indent=2, sort_keys=True, default=str))
        return

    OUT.mkdir(parents=True, exist_ok=True)
    output_map = {
        "canonical_curvature_and_bifurcation_derivation.csv": symbolic_rows,
        "parent_scalar_local_bound_and_preparation_rows.csv": branch_rows,
        "curvature_trigger_corridor_scan.csv": scan_rows,
        "joint_flow_invariant_and_trajectory_status.csv": flow_rows,
        "route_decision.csv": route_rows,
        "source_provenance.csv": source_rows,
    }
    for name, rows in output_map.items():
        write_csv(OUT / name, rows)
    result_path = OUT / "curvature_triggered_motion_state_results.json"
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
        symbolic_diagnostics,
        branch_diagnostics,
        scan_rows,
    )
    write_csv(VALIDATION, validations)
    failed = [row for row in validations if row["status"] != "PASS"]
    if failed:
        raise RuntimeError(
            "checkpoint 5204 validation failed: "
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
                "checkpoint_5203_output_sha256": tree_digest(
                    CHECKPOINT_5203_OUT
                ),
                "curvature_trigger_prepares_5195_state": False,
                "common_packet_rejected": False,
                "selected_next_route": payload["selected_next_route"],
            },
            indent=2,
            default=str,
        )
    )


if __name__ == "__main__":
    main()
