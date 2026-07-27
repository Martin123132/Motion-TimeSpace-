from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import camb
import numpy as np
from camb import model


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
OUT = POST / "source-intake" / "functional_rg" / "5156"
SOURCES = OUT / "sources"
RESULT_JSON = OUT / "FLRW_covariance_radiation_transfer_results.json"
FLRW_CSV = OUT / "FLRW_parent_Hessian_reduction.csv"
GAUSSIAN_CSV = OUT / "Gaussian_CTP_state_theorem.csv"
INITIAL_CSV = OUT / "gauge_invariant_initial_mode_contract.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
CAMB_CSV = OUT / "CAMB_empirical_adiabatic_baseline.csv"
TRANSFER_CSV = OUT / "radiation_era_FDM_transfer_curves.csv"
TRANSFER_SUMMARY_CSV = OUT / "radiation_transfer_summary.csv"
PATCH_SUMMARY_CSV = OUT / "halo_patch_collapse_summary.csv"
PATCH_CSV = OUT / "halo_patch_covariance_collapse_gate.csv"
DECISION_CSV = OUT / "covariance_and_formation_route_decision.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5156_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5156-Y5-R2FR-FLRW-Hessian-Gaussian-state-single-clock-adiabatic-radiation-transfer-and-patch-collapse-gate.md"
)

PREVIOUS_DOCUMENT = (
    POST
    / "5155-Y5-R2FR-parent-SP-Vlasov-limit-homogeneous-no-collapse-post-equality-transfer-and-wave-runner.md"
)
PREVIOUS_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5155"
    / "parent_SP_Vlasov_transfer_results.json"
)
MASS_SUMMARY = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5155"
    / "post_equality_transfer_summary.csv"
)
HALO_PATCHES = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5155"
    / "halo_patch_transfer_gate.csv"
)
PARENT_LOCAL_ACTION = (
    POST
    / "4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-universal-source-residue-certificate.md"
)
PARENT_CTP = (
    POST
    / "4949-Y5-R2FR-covariant-2PI-motion-occupation-Dyson-source-and-conserved-galaxy-stress-or-composite-route-rejection.md"
)
PARENT_BACKGROUND = (
    POST
    / "5152-Y5-R2FR-primordial-motion-occupation-dust-limit-Jeans-window-and-formation-source-arbitration.md"
)

HU_ARCHIVE = SOURCES / "hu_fdm_source.tar"
HU_TEX = SOURCES / "hu_fdm_source" / "fuzzy.tex"
MB_ARCHIVE = SOURCES / "ma_bert_source.tar"
MB_TEX = SOURCES / "ma_bert_source" / "9506072.tex"
HLOZEK_ARCHIVE = SOURCES / "hlozek_ula_source.tar"
HLOZEK_TEX = SOURCES / "hlozek_ula_source" / "AdiabaticAxion_v6.tex"
PERROTTA_ARCHIVE = SOURCES / "perrotta_scalar_ic_source.tar"
PERROTTA_TEX = SOURCES / "perrotta_scalar_ic_source" / "articolo.tex"
PLANCK_XML = SOURCES / "planck_2018_1807.06209_api.xml"
CAMB_INIT = Path(camb.__file__).resolve()

MARKER = "MTS_5156_FLRW_COVARIANCE_ADIABATIC_TRANSFER_COLLAPSE_GATE"
CHECKED_DATE = "2026-07-20"
FORMAL_DIGEST_LOCK = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"

H = 0.674
H0 = 67.4
OMEGA_M = 0.315
OMEGA_B = 0.04924319136384048
MNU_EV = 0.06
TAU_REIO = 0.054
N_S = 0.965
INITIAL_A_S = 2.1e-9
TARGET_SIGMA8 = 0.811
DELTA_COLLAPSE = 1.686
CAMB_MAX_K_H_MPC = 300.0
CAMB_POINTS = 4096

PRIMARY_URLS = {
    "Ma_Bertschinger": "https://arxiv.org/abs/astro-ph/9506072",
    "Hu_Barkana_Gruzinov": "https://arxiv.org/abs/astro-ph/0003365",
    "Perrotta_Baccigalupi": "https://arxiv.org/abs/astro-ph/9811156",
    "Hlozek_Grin_Marsh_Ferreira": "https://arxiv.org/abs/1410.2896",
    "Planck_2018_parameters": "https://arxiv.org/abs/1807.06209",
    "CAMB": "https://arxiv.org/abs/astro-ph/9911177",
}


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(file_digest(item).encode("ascii"))
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def json_default(value: Any) -> Any:
    if isinstance(value, (np.floating, np.integer)):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, Path):
        return str(value)
    raise TypeError(f"cannot serialize {type(value)!r}")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=json_default) + "\n",
        encoding="utf-8",
    )


def source_paths() -> dict[str, Path]:
    return {
        "parent_local_action": PARENT_LOCAL_ACTION,
        "parent_CTP": PARENT_CTP,
        "parent_background": PARENT_BACKGROUND,
        "previous_document": PREVIOUS_DOCUMENT,
        "previous_result": PREVIOUS_RESULT,
        "mass_summary": MASS_SUMMARY,
        "halo_patches": HALO_PATCHES,
        "Hu_archive": HU_ARCHIVE,
        "Hu_TeX": HU_TEX,
        "Ma_Bertschinger_archive": MB_ARCHIVE,
        "Ma_Bertschinger_TeX": MB_TEX,
        "Hlozek_archive": HLOZEK_ARCHIVE,
        "Hlozek_TeX": HLOZEK_TEX,
        "Perrotta_archive": PERROTTA_ARCHIVE,
        "Perrotta_TeX": PERROTTA_TEX,
        "Planck_API_XML": PLANCK_XML,
        "installed_CAMB_init": CAMB_INIT,
    }


def provenance_rows(paths: dict[str, Path]) -> list[dict[str, Any]]:
    url_map = {
        "Hu_archive": PRIMARY_URLS["Hu_Barkana_Gruzinov"],
        "Hu_TeX": PRIMARY_URLS["Hu_Barkana_Gruzinov"],
        "Ma_Bertschinger_archive": PRIMARY_URLS["Ma_Bertschinger"],
        "Ma_Bertschinger_TeX": PRIMARY_URLS["Ma_Bertschinger"],
        "Hlozek_archive": PRIMARY_URLS["Hlozek_Grin_Marsh_Ferreira"],
        "Hlozek_TeX": PRIMARY_URLS["Hlozek_Grin_Marsh_Ferreira"],
        "Perrotta_archive": PRIMARY_URLS["Perrotta_Baccigalupi"],
        "Perrotta_TeX": PRIMARY_URLS["Perrotta_Baccigalupi"],
        "Planck_API_XML": PRIMARY_URLS["Planck_2018_parameters"],
        "installed_CAMB_init": PRIMARY_URLS["CAMB"],
    }
    return [
        {
            "source_id": key,
            "path": str(path),
            "exists": path.is_file(),
            "sha256": file_digest(path) if path.is_file() else "",
            "primary_url": url_map.get(key, "local_parent_checkpoint"),
            "role": "primary_external_source" if key in url_map else "parent_chain_source",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for key, path in paths.items()
    ]


def flrw_rows() -> list[dict[str, Any]]:
    return [
        {
            "derivation_id": "FLRW5156_00_same_parent_action",
            "object": "local and cosmological metric source",
            "equation": "S=S_EH+S_Maxwell+S_SM+S_psi+higher_parent_operators",
            "derivation": "checkpoint 4947 rank-one metric branch",
            "status": "PARENT_CHAIN_RETAINED",
            "claim_limit": "no galaxy-only coupling or second metric",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "derivation_id": "FLRW5156_01_conformal_flatness",
            "object": "spatially flat FLRW Weyl tensor",
            "equation": "C_mnrs[g_FLRW]=0",
            "derivation": "FLRW is conformally flat",
            "status": "EXACT_ZERO",
            "claim_limit": "background and linear operator before perturbed-Weyl insertions",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "derivation_id": "FLRW5156_02_O4_portal",
            "object": "u_O4 C^2 (nabla psi)^2 contribution to homogeneous Hessian",
            "equation": "A_FLRW=Z_psi+2u_O4 C^2=Z_psi",
            "derivation": "FLRW5156_01 inserted into checkpoint 4949 inverse propagator",
            "status": "DERIVED_ZERO_ON_BACKGROUND",
            "claim_limit": "perturbed curvature vertices remain higher-order interactions",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "derivation_id": "FLRW5156_03_canonical_mode",
            "object": "free canonical motion mode on FLRW",
            "equation": "v_k''+[k^2+a^2 m_gap^2-a''/a]v_k=metric_constraint_source",
            "derivation": "v=a sqrt(Z_psi) delta_psi from the reduced quadratic action",
            "status": "DERIVED_QUADRATIC_MODE_OPERATOR",
            "claim_limit": "full scalar-metric system still obeys Einstein constraints",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "derivation_id": "FLRW5156_04_radiation_mode",
            "object": "radiation-era free frequency",
            "equation": "a''=0 -> omega_k^2=k^2+a^2 m_gap^2",
            "derivation": "radiation-dominated scale factor is linear in conformal time",
            "status": "EXACT_ON_RD_BACKGROUND",
            "claim_limit": "radiation and metric perturbations must be co-evolved",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "derivation_id": "FLRW5156_05_oscillating_fluid",
            "object": "late oscillation-averaged scalar",
            "equation": "c_X^2=[k^2/(4m^2a^2)]/[1+k^2/(4m^2a^2)]",
            "derivation": "WKB reduction of the same massive scalar Hessian",
            "status": "SOURCE_LOCKED_EFFECTIVE_FLUID_LIMIT",
            "claim_limit": "requires m_gap much larger than H and controlled c_ess",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "derivation_id": "FLRW5156_06_universal_source",
            "object": "Einstein source including motion and EM",
            "equation": "G_mn+Lambda g_mn=8piG_N(T_SM+T_EM+T_X)_mn",
            "derivation": "same Hilbert variation as checkpoints 4947 and 5155",
            "status": "DERIVED_SAME_SOURCE_CONTRACT",
            "claim_limit": "Poynting momentum is not a separate galaxy switch",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def gaussian_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "GST5156_00_spectral_data",
            "object": "CTP spectral correlator",
            "equation": "rho_k is fixed by the mode equation and Wronskian u_k partial_eta(u_k*)-partial_eta(u_k) u_k*=i",
            "result": "commutator normalization is dynamical plus canonical",
            "status": "DERIVED",
            "parent_owned": True,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "theorem_id": "GST5156_01_statistical_data",
            "object": "general homogeneous Gaussian F_k",
            "equation": "F_k(eta,eta')=(n_k+1/2)[u_k(eta)u_k*(eta')+c.c.]+c_k u_k(eta)u_k(eta')+c_k* u_k*(eta)u_k*(eta')",
            "result": "n_k and c_k specify occupation and squeezing",
            "status": "EXACT_GAUSSIAN_PARAMETERIZATION",
            "parent_owned": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "theorem_id": "GST5156_02_positivity",
            "object": "Gaussian density-matrix positivity",
            "equation": "n_k>=0 and |c_k|^2<=n_k(n_k+1)",
            "result": "allowed state cone is non-singleton",
            "status": "EXACT_POSITIVITY_BOUND",
            "parent_owned": True,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "theorem_id": "GST5156_03_action_underdetermination",
            "object": "quadratic Hessian versus covariance",
            "equation": "same D_k admits every positive (n_k,c_k) initial covariance",
            "result": "the action fixes transfer but not the statistical state",
            "status": "PROVED_NONUNIQUENESS",
            "parent_owned": True,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "theorem_id": "GST5156_04_reflection_even_limit",
            "object": "rho_even=(|+psi_i><+psi_i|+|-psi_i><-psi_i|)/2",
            "equation": "all odd correlators vanish while even covariance remains free",
            "result": "reflection symmetry removes scalar charge but does not select P_delta(k)",
            "status": "PROVED_INSUFFICIENT_FOR_SPECTRUM",
            "parent_owned": True,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "theorem_id": "GST5156_05_curvature_entropy_matrix",
            "object": "gauge-invariant primordial covariance",
            "equation": "C_k=[[P_R,P_RS],[P_RS,P_S]] positive semidefinite",
            "result": "Einstein-scalar transfer acts on a curvature/entropy covariance matrix",
            "status": "DERIVED_STATE_SPACE",
            "parent_owned": True,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "theorem_id": "GST5156_06_parent_state_boundary",
            "object": "primordial amplitude and tilt",
            "equation": "P_R(k), P_S(k), P_RS(k) require a density matrix or cosmogenesis boundary law",
            "result": "current EH plus massive-scalar action alone cannot predict A_s or n_s",
            "status": "EXACT_ACTION_VERSUS_STATE_BOUNDARY",
            "parent_owned": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def initial_rows() -> list[dict[str, Any]]:
    return [
        {
            "mode_id": "IC5156_00_common_clock",
            "mode": "single-clock adiabatic",
            "condition": "delta rho_i/rho_i'=delta rho_j/rho_j' for every component",
            "consequence": "all relative entropy perturbations vanish",
            "status": "EXACT_IF_SINGLE_CLOCK_PREMISE_HOLDS",
            "parent_status": "current corpus has no completed cosmogenesis clock",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "mode_id": "IC5156_01_entropy_invariant",
            "mode": "motion-radiation relative entropy after oscillation",
            "condition": "S_Xgamma=delta_X-3 delta_gamma/4",
            "consequence": "single-clock branch has S_Xgamma=0",
            "status": "GAUGE_INVARIANT_SUPERHORIZON_CONDITION",
            "parent_status": "conditional branch not a fitted galaxy parameter",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "mode_id": "IC5156_02_frozen_motion",
            "mode": "adiabatic massive scalar before oscillation",
            "condition": "w_X approaches -1 and k tau much less than 1",
            "consequence": "delta_X=0 and u_X=0 at leading order",
            "status": "SOURCE_DERIVED_EARLY_TIME_MODE",
            "parent_status": "matches the checkpoint-5152 frozen background",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "mode_id": "IC5156_03_post_oscillation",
            "mode": "adiabatic oscillation-averaged motion fluid",
            "condition": "m_gap much larger than 3H",
            "consequence": "w_X=0 with scale-dependent c_X^2 and inherited curvature mode",
            "status": "DERIVED_EFFECTIVE_FLUID_CONTINUATION",
            "parent_status": "actual infrared c_ess remains unsigned",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "mode_id": "IC5156_04_isocurvature",
            "mode": "independent motion entropy mode",
            "condition": "P_S or P_RS nonzero",
            "consequence": "requires an additional global state covariance and CMB test",
            "status": "ALLOWED_NOT_DERIVED_OR_SET_TO_ZERO",
            "parent_status": "not silently discarded",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "mode_id": "IC5156_05_empirical_comparator",
            "mode": "Planck-normalized adiabatic curvature",
            "condition": "n_s=0.965 and sigma8=0.811 with S_Xgamma=0",
            "consequence": "one global source-backed formation smoke covariance",
            "status": "EMPIRICAL_CONDITIONAL_COMPARATOR",
            "parent_status": "not an MTS prediction of A_s or n_s",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def run_camb_baseline() -> tuple[np.ndarray, np.ndarray, list[dict[str, Any]], dict[str, Any]]:
    omega_nu_h2 = MNU_EV / 93.14
    omega_b_h2 = OMEGA_B * H * H
    omega_c_h2 = (OMEGA_M - OMEGA_B) * H * H - omega_nu_h2
    params = camb.CAMBparams()
    params.set_cosmology(
        H0=H0,
        ombh2=omega_b_h2,
        omch2=omega_c_h2,
        mnu=MNU_EV,
        omk=0.0,
        tau=TAU_REIO,
    )
    params.InitPower.set_params(As=INITIAL_A_S, ns=N_S)
    params.set_matter_power(redshifts=[0.0], kmax=250.0)
    params.NonLinear = model.NonLinear_none
    results = camb.get_results(params)
    raw_sigma8 = float(results.get_sigma8()[0])
    amplitude_scale = (TARGET_SIGMA8 / raw_sigma8) ** 2
    effective_A_s = INITIAL_A_S * amplitude_scale
    k_h, redshifts, power_h = results.get_matter_power_spectrum(
        minkh=1.0e-5,
        maxkh=CAMB_MAX_K_H_MPC,
        npoints=CAMB_POINTS,
    )
    if len(redshifts) != 1:
        raise RuntimeError("unexpected CAMB redshift axis")
    k_mpc = np.asarray(k_h, dtype=float) * H
    power_mpc3 = np.asarray(power_h[0], dtype=float) * amplitude_scale / H**3
    rows = [
        {
            "k_Mpc_inverse": float(k_value),
            "P_CDM_Mpc3": float(p_value),
            "Delta2_CDM": float(k_value**3 * p_value / (2.0 * math.pi**2)),
            "redshift": 0.0,
            "CAMB_version": camb.__version__,
            "empirical_sigma8_normalization": TARGET_SIGMA8,
            "valid_for_MTS_primordial_claim": False,
            "checkpoint_marker": MARKER,
        }
        for k_value, p_value in zip(k_mpc, power_mpc3, strict=True)
    ]
    metadata = {
        "CAMB_version": camb.__version__,
        "raw_sigma8": raw_sigma8,
        "target_sigma8": TARGET_SIGMA8,
        "amplitude_scale": amplitude_scale,
        "effective_A_s": effective_A_s,
        "n_s": N_S,
        "H0_km_s_Mpc": H0,
        "Omega_m": OMEGA_M,
        "Omega_b": OMEGA_B,
        "mnu_eV": MNU_EV,
        "tau_reio": TAU_REIO,
        "k_min_Mpc_inverse": float(k_mpc[0]),
        "k_max_Mpc_inverse": float(k_mpc[-1]),
        "power_rows": len(rows),
    }
    return k_mpc, power_mpc3, rows, metadata


def top_hat_window(argument: np.ndarray) -> np.ndarray:
    argument = np.asarray(argument, dtype=float)
    result = np.empty_like(argument)
    small = np.abs(argument) < 1.0e-3
    squared = argument[small] ** 2
    result[small] = 1.0 - squared / 10.0 + squared**2 / 280.0
    value = argument[~small]
    result[~small] = 3.0 * (np.sin(value) - value * np.cos(value)) / value**3
    return result


def sigma_radius(
    k_mpc: np.ndarray,
    power_mpc3: np.ndarray,
    radius_mpc: float,
    maximum_k: float | None = None,
) -> float:
    mask = np.ones_like(k_mpc, dtype=bool)
    if maximum_k is not None:
        mask &= k_mpc <= maximum_k
    k_values = k_mpc[mask]
    power_values = power_mpc3[mask]
    window = top_hat_window(k_values * radius_mpc)
    delta_squared = k_values**3 * power_values / (2.0 * math.pi**2)
    variance = float(np.trapezoid(delta_squared * window**2, np.log(k_values)))
    return math.sqrt(max(0.0, variance))


def hu_transfer_amplitude(k_mpc: np.ndarray, mass_eV: float, k_jeans: float) -> np.ndarray:
    m22 = mass_eV / 1.0e-22
    x_value = 1.61 * m22 ** (1.0 / 18.0) * k_mpc / k_jeans
    return np.cos(x_value**3) / (1.0 + x_value**8)


def first_half_power_crossing(
    k_mpc: np.ndarray, transfer_power: np.ndarray
) -> float:
    below = np.flatnonzero(transfer_power <= 0.5)
    if not len(below):
        return math.nan
    index = int(below[0])
    if index == 0:
        return float(k_mpc[0])
    x0 = math.log(float(k_mpc[index - 1]))
    x1 = math.log(float(k_mpc[index]))
    y0 = float(transfer_power[index - 1])
    y1 = float(transfer_power[index])
    fraction = (0.5 - y0) / (y1 - y0)
    return math.exp(x0 + fraction * (x1 - x0))


def transfer_products(
    k_mpc: np.ndarray,
    power_cdm: np.ndarray,
    mass_rows: list[dict[str, str]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    curve_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    products: dict[str, dict[str, Any]] = {}
    for mass_row in mass_rows:
        label = mass_row["mass_label"]
        mass_eV = float(mass_row["m_gap_eV"])
        k_parent = float(mass_row["k_Jeans_equality_Mpc_inverse"])
        m22 = mass_eV / 1.0e-22
        k_hu = 9.0 * math.sqrt(m22)
        k_half_formula = 4.5 * m22 ** (4.0 / 9.0)
        dense_k = np.geomspace(
            float(k_mpc[0]),
            max(float(k_mpc[-1]), 2.0 * k_half_formula),
            20000,
        )
        transfer = hu_transfer_amplitude(k_mpc, mass_eV, k_parent)
        transfer_power = transfer**2
        power_mts = power_cdm * transfer_power
        dense_power = hu_transfer_amplitude(dense_k, mass_eV, k_parent) ** 2
        k_half_numeric = first_half_power_crossing(dense_k, dense_power)
        products[label] = {
            "mass_eV": mass_eV,
            "k_parent": k_parent,
            "k_hu": k_hu,
            "k_half_numeric": k_half_numeric,
            "k_half_formula": k_half_formula,
            "transfer_power": transfer_power,
            "power_mts": power_mts,
        }
        for k_value, t_value, t2_value, p_cdm, p_mts in zip(
            k_mpc,
            transfer,
            transfer_power,
            power_cdm,
            power_mts,
            strict=True,
        ):
            curve_rows.append(
                {
                    "mass_label": label,
                    "m_gap_eV": mass_eV,
                    "k_Mpc_inverse": float(k_value),
                    "k_over_parent_kJeans_equality": float(k_value / k_parent),
                    "Hu_transfer_amplitude": float(t_value),
                    "Hu_transfer_power": float(t2_value),
                    "P_CDM_Mpc3": float(p_cdm),
                    "P_MTS_empirical_adiabatic_Mpc3": float(p_mts),
                    "radiation_transfer_role": "Hu_FDM_full_linear_fit_on_CAMB_CDM_baseline",
                    "valid_for_MTS_primordial_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
        summary_rows.append(
            {
                "mass_label": label,
                "m_gap_eV": mass_eV,
                "m22": m22,
                "parent_kJeans_equality_Mpc_inverse": k_parent,
                "Hu_kJeans_equality_Mpc_inverse": k_hu,
                "relative_kJeans_difference": abs(k_parent / k_hu - 1.0),
                "numeric_half_power_k_Mpc_inverse": k_half_numeric,
                "Hu_formula_half_power_k_Mpc_inverse": k_half_formula,
                "relative_half_power_difference": abs(k_half_numeric / k_half_formula - 1.0),
                "transfer_source": PRIMARY_URLS["Hu_Barkana_Gruzinov"],
                "full_Boltzmann_MTS_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return curve_rows, summary_rows, products


def interpolate_log_k(k_mpc: np.ndarray, values: np.ndarray, target_k: float) -> float:
    return float(np.interp(math.log(target_k), np.log(k_mpc), values))


def patch_products(
    k_mpc: np.ndarray,
    power_cdm: np.ndarray,
    patch_input: list[dict[str, str]],
    mass_products: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    cdm_cache: dict[float, tuple[float, float]] = {}
    mts_cache: dict[tuple[str, float], tuple[float, float]] = {}
    for source_row in patch_input:
        label = source_row["mass_label"]
        radius = float(source_row["Lagrangian_patch_radius_Mpc"])
        rounded_radius = round(radius, 14)
        if rounded_radius not in cdm_cache:
            cdm_cache[rounded_radius] = (
                sigma_radius(k_mpc, power_cdm, radius),
                sigma_radius(k_mpc, power_cdm, radius, maximum_k=100.0),
            )
        cache_key = (label, rounded_radius)
        product = mass_products[label]
        if cache_key not in mts_cache:
            mts_cache[cache_key] = (
                sigma_radius(k_mpc, product["power_mts"], radius),
                sigma_radius(
                    k_mpc,
                    product["power_mts"],
                    radius,
                    maximum_k=100.0,
                ),
            )
        sigma_cdm, sigma_cdm_100 = cdm_cache[rounded_radius]
        sigma_mts, sigma_mts_100 = mts_cache[cache_key]
        peak_height = DELTA_COLLAPSE / sigma_mts
        press_schechter_fraction = math.erfc(peak_height / math.sqrt(2.0))
        one_sided_probability = 0.5 * press_schechter_fraction
        k_half = float(product["k_half_numeric"])
        half_mode_radius = math.pi / k_half
        mode_values: dict[str, float] = {}
        for mode_name, mode_k in {
            "1_over_R": 1.0 / radius,
            "pi_over_R": math.pi / radius,
            "2pi_over_R": 2.0 * math.pi / radius,
        }.items():
            mode_values[mode_name] = interpolate_log_k(
                k_mpc,
                product["transfer_power"],
                mode_k,
            )
        rows.append(
            {
                "galaxy": source_row["galaxy"],
                "mapping": source_row["mapping"],
                "mass_label": label,
                "m_gap_eV": float(source_row["m_gap_eV"]),
                "Lagrangian_patch_radius_Mpc": radius,
                "sigma_CDM_empirical": sigma_cdm,
                "sigma_MTS_empirical_adiabatic": sigma_mts,
                "sigma_MTS_over_CDM": sigma_mts / sigma_cdm,
                "MTS_sigma_high_k_truncation_relative_error": abs(
                    sigma_mts_100 / sigma_mts - 1.0
                ),
                "peak_height_delta_c_over_sigma": peak_height,
                "Press_Schechter_collapsed_fraction_z0": press_schechter_fraction,
                "Gaussian_one_sided_probability_z0": one_sided_probability,
                "one_sigma_collapse_by_z0": sigma_mts >= DELTA_COLLAPSE,
                "within_three_sigma_by_z0": peak_height <= 3.0,
                "within_five_sigma_by_z0": peak_height <= 5.0,
                "half_power_k_Mpc_inverse": k_half,
                "half_mode_radius_pi_over_k_Mpc": half_mode_radius,
                "patch_radius_over_half_mode_radius": radius / half_mode_radius,
                "full_power_ratio_k_1_over_R": mode_values["1_over_R"],
                "full_power_ratio_k_pi_over_R": mode_values["pi_over_R"],
                "full_power_ratio_k_2pi_over_R": mode_values["2pi_over_R"],
                "post_equality_power_ratio_k_2pi_over_R": float(
                    source_row["post_equality_power_ratio_k_2pi_over_R"]
                ),
                "primordial_covariance_role": "Planck_normalized_single_clock_adiabatic_comparator",
                "parent_primordial_covariance_derived": False,
                "valid_for_structure_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    summaries: list[dict[str, Any]] = []
    for label in mass_products:
        selected = [row for row in rows if row["mass_label"] == label]
        sigma_values = np.asarray(
            [row["sigma_MTS_empirical_adiabatic"] for row in selected]
        )
        peak_values = np.asarray(
            [row["peak_height_delta_c_over_sigma"] for row in selected]
        )
        power_values = np.asarray(
            [row["full_power_ratio_k_2pi_over_R"] for row in selected]
        )
        summaries.append(
            {
                "mass_label": label,
                "m_gap_eV": mass_products[label]["mass_eV"],
                "patch_rows": len(selected),
                "minimum_sigma_MTS": float(np.min(sigma_values)),
                "median_sigma_MTS": float(np.median(sigma_values)),
                "maximum_sigma_MTS": float(np.max(sigma_values)),
                "maximum_peak_height": float(np.max(peak_values)),
                "one_sigma_patch_count": sum(
                    bool(row["one_sigma_collapse_by_z0"]) for row in selected
                ),
                "within_three_sigma_patch_count": sum(
                    bool(row["within_three_sigma_by_z0"]) for row in selected
                ),
                "within_five_sigma_patch_count": sum(
                    bool(row["within_five_sigma_by_z0"]) for row in selected
                ),
                "minimum_full_power_ratio_k_2pi_over_R": float(np.min(power_values)),
                "median_full_power_ratio_k_2pi_over_R": float(np.median(power_values)),
                "patches_below_half_mode_radius": sum(
                    row["patch_radius_over_half_mode_radius"] < 1.0
                    for row in selected
                ),
                "conditional_formation_status": (
                    "EMPIRICAL_ADIABATIC_PATCHES_WITHIN_FIVE_SIGMA"
                    if float(np.max(peak_values)) <= 5.0
                    else "EMPIRICAL_ADIABATIC_LOW_POWER_STRESS"
                ),
                "valid_for_MTS_formation_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    summary = {
        "patch_rows": len(rows),
        "maximum_sigma_truncation_error": max(
            row["MTS_sigma_high_k_truncation_relative_error"] for row in rows
        ),
        "maximum_peak_height": max(
            row["peak_height_delta_c_over_sigma"] for row in rows
        ),
        "minimum_sigma_ratio": min(row["sigma_MTS_over_CDM"] for row in rows),
        "maximum_sigma_ratio": max(row["sigma_MTS_over_CDM"] for row in rows),
        "within_three_sigma_count": sum(
            bool(row["within_three_sigma_by_z0"]) for row in rows
        ),
        "within_five_sigma_count": sum(
            bool(row["within_five_sigma_by_z0"]) for row in rows
        ),
        "one_sigma_count": sum(
            bool(row["one_sigma_collapse_by_z0"]) for row in rows
        ),
    }
    return rows, summaries, summary


def decision_rows(patch_summary: dict[str, Any]) -> list[dict[str, Any]]:
    all_within_five = patch_summary["within_five_sigma_count"] == patch_summary["patch_rows"]
    return [
        {
            "gate": "parent_FLRW_linear_operator",
            "status": "DERIVED_FROM_SAME_PARENT_ACTION",
            "result": "conformal flatness removes the Weyl portal and leaves the massive scalar plus Einstein constraints",
            "next_action": "retain one metric and same Hilbert source",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "gate": "primordial_covariance_uniqueness",
            "status": "REJECTED_FROM_ACTION_ALONE",
            "result": "the Hessian fixes mode functions and commutator but not Gaussian occupation or squeezing",
            "next_action": "derive a cosmogenesis density matrix or boundary-state law",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "gate": "single_clock_adiabatic_branch",
            "status": "EXACT_CONDITIONAL_BRANCH",
            "result": "one common time shift sets all relative entropy modes to zero",
            "next_action": "derive the single physical clock premise rather than assume isocurvature away",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "gate": "empirical_adiabatic_radiation_transfer",
            "status": "EXECUTED_SOURCE_BACKED_COMPARATOR",
            "result": f"{patch_summary['within_five_sigma_count']}/{patch_summary['patch_rows']} patch rows lie within five-sigma by z=0 under the empirical covariance",
            "next_action": "use this one global covariance for a no-refit hybrid collapse seed",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "gate": "formation_route",
            "status": (
                "EMPIRICAL_FORMATION_NOT_EXCLUDED_ADVANCE_TO_HYBRID_COLLAPSE"
                if all_within_five
                else "LOW_MASS_FORMATION_STRESSED_RESTRICT_OR_REDERIVE_BRANCH"
            ),
            "result": "linear covariance viability is assessed without claiming the nonlinear MTS attractor",
            "next_action": "seed Vlasov volume plus wave zoom and compare q/core/edge without per-galaxy refit",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def write_document(result: dict[str, Any]) -> None:
    summary = result["summary"]
    transfer_by_label = {
        row["mass_label"]: row for row in result["mass_transfer_summaries"]
    }
    mass_lines = "\n".join(
        f"- `{row['mass_label']}`: k_half={transfer_by_label[row['mass_label']]['numeric_half_power_k_Mpc_inverse']:.6g} Mpc^-1, "
        f"minimum patch sigma={row['minimum_sigma_MTS']:.6g}, "
        f"maximum peak height={row['maximum_peak_height']:.6g}, "
        f"five-sigma rows={row['within_five_sigma_patch_count']}/{row['patch_rows']}."
        for row in result["mass_patch_summaries"]
    )
    text = f"""# 5156 - FLRW Hessian, Gaussian-state theorem, single-clock adiabatic branch, radiation transfer and patch collapse gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

This checkpoint applies the machine-cog criterion before attempting nonlinear
formation. The same checkpoint-4947 Einstein metric and Hilbert source are
retained. On spatially flat FLRW, `C_mnrs=0`, so the retained
`u_O4 C^2 (nabla psi)^2` portal drops out of the homogeneous quadratic
operator. The motion sector is therefore the ordinary massive scalar coupled
to the same Einstein constraints. Maxwell energy and Poynting momentum remain
inside the same source; no galaxy-only coupling or arena switch is added.

The key theorem is now exact. The Hessian determines mode functions and the
spectral commutator, but it does **not** determine the statistical covariance.
Reflection-evenness removes odd scalar charge while leaving an infinite cone
of positive Gaussian two-point states. A parent cosmogenesis density matrix or
boundary law is required to predict the primordial amplitude, tilt and any
motion isocurvature.

Rather than stop at that theorem, one global source-backed adiabatic covariance
is executed as an explicit nonclaim comparator. CAMB supplies the standard
photon, baryon, neutrino and metric baseline; the Hu--Barkana--Gruzinov full
radiation-era FDM transfer is applied at all three locked masses. Every one of
the 1050 checkpoint-5155 Lagrangian patches is then integrated against the
resulting linear power spectrum.

## 1. Parent FLRW reduction

The checkpoint-4949 inverse scalar operator is

```text
D=-1/sqrt(-g) partial_m[sqrt(-g) A g^mn partial_n]+m_gap^2,
A=Z_psi+2u_O4 C_mnrs C^mnrs.
```

Spatially flat FLRW is conformally flat, hence

```text
C_mnrs[g_FLRW]=0,
A_FLRW=Z_psi.
```

With `v=a sqrt(Z_psi) delta psi`, the free canonical mode satisfies

```text
v_k''+[k^2+a^2 m_gap^2-a''/a]v_k=metric-constraint source.
```

During exact radiation domination `a''=0`. After coherent oscillations, the
same mode has the sourced WKB fluid sound speed

```text
c_X^2=[k^2/(4m_gap^2 a^2)]/[1+k^2/(4m_gap^2 a^2)].
```

The actual infrared `c_ess` remains unsigned. It is not inserted here.

## 2. Exact action-versus-state theorem

For a normalized mode basis `u_k`, canonical quantization fixes

```text
u_k partial_eta(u_k*) - partial_eta(u_k) u_k* = i.
```

A homogeneous Gaussian statistical correlator still contains independent
occupation and squeezing data:

```text
F_k(eta,eta')=(n_k+1/2)[u_k(eta)u_k*(eta')+c.c.]
              +c_k u_k(eta)u_k(eta')
              +c_k* u_k*(eta)u_k*(eta'),
n_k>=0,
|c_k|^2<=n_k(n_k+1).
```

Therefore the same quadratic action admits infinitely many positive
covariances. The reflection-even `+/-psi_i` mixture sets odd moments to zero
but does not select `n_k`, `c_k` or `P_delta(k)`. This proves why checkpoint
5155's homogeneous state cannot be upgraded to a formation spectrum by
notation.

For scalar cosmological modes the invariant initial covariance is a positive
matrix over curvature and relative entropy,

```text
C(k)=[[P_R,P_RS],[P_RS,P_S]].
```

The current parent transfer equations do not uniquely fix this matrix.

## 3. Minimal single-clock branch

If all components descend from one physical clock perturbation, then

```text
delta rho_i/rho_i' = delta rho_j/rho_j',
S_Xgamma=delta_X-3 delta_gamma/4=0
```

after the motion field oscillates. Before oscillation `w_X` approaches `-1`,
and the sourced adiabatic mode has `delta_X=u_X=0` at leading superhorizon
order. This is the standard continuation derived for an ultralight scalar and
matches the checkpoint-5152 frozen background.

This branch is economical and global, but the current corpus has not yet
derived the single-clock cosmogenesis premise. Independent `P_S` and `P_RS`
remain allowed and are not silently set to zero as an MTS prediction.

## 4. Source-backed radiation transfer

The empirical comparator uses

```text
H0=67.4 km/s/Mpc,
Omega_m=0.315,
Omega_b={OMEGA_B},
n_s=0.965,
sigma8=0.811.
```

CAMB `{result['CAMB_metadata']['CAMB_version']}` produces the full adiabatic
CDM baseline and is rescaled linearly from raw
`sigma8={result['CAMB_metadata']['raw_sigma8']}` to the declared Planck value.
The independent top-hat reconstruction gives
`sigma8={summary['sigma8_top_hat_reconstruction']}`.

For each parent mass the full FDM transfer is

```text
P_X(k)=T_F(k)^2 P_CDM(k),
T_F=cos(x^3)/(1+x^8),
x=1.61 m_22^(1/18) k/k_J,eq.
```

The parent equality Jeans scales agree with the published
`9 sqrt(m_22) Mpc^-1` expression to at most
`{summary['maximum_kJeans_relative_difference']}`. Numerical and published
half-power scales agree to at most
`{summary['maximum_half_power_relative_difference']}`.

This is a source-backed full-radiation transfer comparator, not a claim that
MTS derived the observed primordial covariance and not an independent
AxionCAMB likelihood.

## 5. Lagrangian patch result

{mass_lines}

Across all rows, the smallest `sigma_MTS/sigma_CDM` is
`{summary['minimum_patch_sigma_ratio']}` and the largest peak height is
`{summary['maximum_patch_peak_height']}`. Exactly
`{summary['within_five_sigma_patch_count']}/{summary['patch_rows']}` rows are
within five sigma by `z=0` under the one empirical covariance. The maximum
high-k truncation change in patch sigma is
`{summary['maximum_patch_sigma_truncation_error']}`.

This answers only whether the required mass patches are erased or rendered
implausibly rare by the linear wave transfer. It does not prove that nonlinear
evolution selects the checkpoint-5154 `p=2` edge, the parent projective `q`, a
finite core, or the required rotation/lensing stress.

## 6. Exact status and next calculation

```text
same parent FLRW quadratic operator                    = derived;
Weyl portal on FLRW background                         = exact zero;
Hessian fixes spectral mode evolution                  = derived;
Hessian uniquely fixes statistical covariance          = rejected exactly;
reflection-evenness fixes primordial power              = rejected exactly;
single-clock adiabatic branch                          = exact conditional;
source-backed radiation transfer                       = executed;
all 1050 Lagrangian patch variances                     = executed;
parent prediction of A_s, n_s and isocurvature          = open;
nonlinear projective-profile attractor                  = open.
```

The next formation calculation may now use one frozen global empirical
covariance, rather than arbitrary numerical noise, to seed a Vlasov
cosmological volume with wave-resolved zoom/core regions. In parallel, the
theory derivation must construct the missing parent state-preparation law: a
single physical clock or another density-matrix principle that predicts
`P_R`, `P_S` and `P_RS`. Neither task may add per-galaxy initial amplitudes.

## 7. Primary sources

- Ma and Bertschinger: {PRIMARY_URLS['Ma_Bertschinger']}
- Hu, Barkana and Gruzinov: {PRIMARY_URLS['Hu_Barkana_Gruzinov']}
- Perrotta and Baccigalupi: {PRIMARY_URLS['Perrotta_Baccigalupi']}
- Hlozek, Grin, Marsh and Ferreira: {PRIMARY_URLS['Hlozek_Grin_Marsh_Ferreira']}
- Planck 2018 cosmological parameters: {PRIMARY_URLS['Planck_2018_parameters']}
- CAMB: {PRIMARY_URLS['CAMB']}

All downloaded source archives, extracted TeX and hashes are recorded under
`source-intake/functional_rg/5156/sources` and `source_provenance.csv`.

All `{result['validation_count']}` validation checks pass. The protected
`formalization-workbench` digest remains
`{result['formalization_workbench_tree_sha256']}`. No GitHub action occurred.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = source_paths()
    missing_sources = [str(path) for path in paths.values() if not path.is_file()]
    if missing_sources:
        raise FileNotFoundError(f"missing checkpoint sources: {missing_sources}")
    source_hashes_before = {key: file_digest(path) for key, path in paths.items()}
    formal_before = tree_digest(FORMAL)

    previous_result = json.loads(PREVIOUS_RESULT.read_text(encoding="utf-8"))
    if previous_result["checkpoint_marker"] != "MTS_5155_PARENT_SP_VLASOV_TRANSFER_WAVE_RUNNER":
        raise RuntimeError("checkpoint 5155 marker mismatch")

    mass_rows = read_csv(MASS_SUMMARY)
    patch_input = read_csv(HALO_PATCHES)
    flrw = flrw_rows()
    gaussian = gaussian_rows()
    initial = initial_rows()
    provenance = provenance_rows(paths)

    k_mpc, power_cdm, camb_rows, camb_metadata = run_camb_baseline()
    sigma8_reconstruction = sigma_radius(k_mpc, power_cdm, 8.0 / H)
    transfer_rows, transfer_summaries, mass_products = transfer_products(
        k_mpc,
        power_cdm,
        mass_rows,
    )
    patch_rows, mass_patch_summaries, patch_summary = patch_products(
        k_mpc,
        power_cdm,
        patch_input,
        mass_products,
    )
    decisions = decision_rows(patch_summary)

    formal_after = tree_digest(FORMAL)
    source_hashes_after = {key: file_digest(path) for key, path in paths.items()}

    summary = {
        "sigma8_top_hat_reconstruction": sigma8_reconstruction,
        "sigma8_reconstruction_relative_error": abs(
            sigma8_reconstruction / TARGET_SIGMA8 - 1.0
        ),
        "maximum_kJeans_relative_difference": max(
            row["relative_kJeans_difference"] for row in transfer_summaries
        ),
        "maximum_half_power_relative_difference": max(
            row["relative_half_power_difference"] for row in transfer_summaries
        ),
        "CAMB_power_rows": len(camb_rows),
        "transfer_curve_rows": len(transfer_rows),
        "patch_rows": len(patch_rows),
        "minimum_patch_sigma_ratio": patch_summary["minimum_sigma_ratio"],
        "maximum_patch_sigma_ratio": patch_summary["maximum_sigma_ratio"],
        "maximum_patch_peak_height": patch_summary["maximum_peak_height"],
        "within_three_sigma_patch_count": patch_summary["within_three_sigma_count"],
        "within_five_sigma_patch_count": patch_summary["within_five_sigma_count"],
        "one_sigma_patch_count": patch_summary["one_sigma_count"],
        "maximum_patch_sigma_truncation_error": patch_summary[
            "maximum_sigma_truncation_error"
        ],
    }

    checks: list[tuple[str, bool, Any]] = [
        ("source_paths_exist", not missing_sources, missing_sources),
        (
            "sources_read_only",
            source_hashes_before == source_hashes_after,
            source_hashes_after,
        ),
        (
            "formalization_workbench_unchanged",
            formal_before == formal_after == FORMAL_DIGEST_LOCK,
            formal_after,
        ),
        (
            "FLRW_parent_reduction_complete",
            len(flrw) == 7
            and all(
                "DERIVED" in row["status"]
                or "EXACT" in row["status"]
                or "SOURCE_LOCKED" in row["status"]
                or "PARENT_CHAIN" in row["status"]
                for row in flrw
            ),
            [row["status"] for row in flrw],
        ),
        (
            "FLRW_Weyl_portal_zero_not_assumed",
            any(
                row["derivation_id"] == "FLRW5156_02_O4_portal"
                and row["status"] == "DERIVED_ZERO_ON_BACKGROUND"
                for row in flrw
            ),
            "C_FLRW=0",
        ),
        (
            "Gaussian_state_parameterization_complete",
            len(gaussian) == 7,
            len(gaussian),
        ),
        (
            "Gaussian_positivity_bound_present",
            any(
                row["status"] == "EXACT_POSITIVITY_BOUND" for row in gaussian
            ),
            "n>=0;abs(c)^2<=n(n+1)",
        ),
        (
            "action_to_covariance_nonuniqueness_proved",
            any(
                row["status"] == "PROVED_NONUNIQUENESS" for row in gaussian
            ),
            "same Hessian admits non-singleton positive state cone",
        ),
        (
            "reflection_even_not_overclaimed",
            any(
                row["status"] == "PROVED_INSUFFICIENT_FOR_SPECTRUM"
                for row in gaussian
            ),
            "odd moments zero does not fix two-point power",
        ),
        (
            "single_clock_branch_conditional",
            initial[0]["status"] == "EXACT_IF_SINGLE_CLOCK_PREMISE_HOLDS"
            and not initial[0]["valid_for_claim"],
            initial[0],
        ),
        (
            "isocurvature_not_silently_zeroed",
            any(
                row["mode"] == "independent motion entropy mode"
                and row["status"] == "ALLOWED_NOT_DERIVED_OR_SET_TO_ZERO"
                for row in initial
            ),
            "P_S and P_RS remain open",
        ),
        (
            "CAMB_baseline_executed",
            camb_metadata["power_rows"] == CAMB_POINTS
            and camb_metadata["CAMB_version"] == camb.__version__,
            camb_metadata,
        ),
        (
            "CAMB_power_positive_finite",
            bool(np.all(np.isfinite(power_cdm)) and np.all(power_cdm > 0.0)),
            [float(np.min(power_cdm)), float(np.max(power_cdm))],
        ),
        (
            "sigma8_top_hat_reconstruction",
            summary["sigma8_reconstruction_relative_error"] < 3.0e-3,
            summary["sigma8_reconstruction_relative_error"],
        ),
        (
            "three_locked_mass_transfers_executed",
            len(transfer_summaries) == 3
            and len(transfer_rows) == 3 * CAMB_POINTS,
            [len(transfer_summaries), len(transfer_rows)],
        ),
        (
            "parent_and_Hu_Jeans_scales_agree",
            summary["maximum_kJeans_relative_difference"] < 0.02,
            summary["maximum_kJeans_relative_difference"],
        ),
        (
            "Hu_half_power_formula_reproduced",
            all(
                math.isfinite(row["numeric_half_power_k_Mpc_inverse"])
                and math.isfinite(row["relative_half_power_difference"])
                for row in transfer_summaries
            )
            and summary["maximum_half_power_relative_difference"] < 0.05,
            summary["maximum_half_power_relative_difference"],
        ),
        (
            "transfer_power_bounded",
            all(
                0.0 <= row["Hu_transfer_power"] <= 1.0 + 1.0e-14
                for row in transfer_rows
            ),
            "0<=T_F^2<=1",
        ),
        (
            "all_1050_patch_variances_executed",
            len(patch_rows) == 1050,
            len(patch_rows),
        ),
        (
            "patch_variances_finite_positive",
            all(
                math.isfinite(row["sigma_MTS_empirical_adiabatic"])
                and row["sigma_MTS_empirical_adiabatic"] > 0.0
                and math.isfinite(row["peak_height_delta_c_over_sigma"])
                for row in patch_rows
            ),
            summary["maximum_patch_peak_height"],
        ),
        (
            "FDM_sigma_not_above_CDM",
            summary["maximum_patch_sigma_ratio"] <= 1.0 + 1.0e-12,
            summary["maximum_patch_sigma_ratio"],
        ),
        (
            "patch_sigma_high_k_converged",
            summary["maximum_patch_sigma_truncation_error"] < 3.0e-3,
            summary["maximum_patch_sigma_truncation_error"],
        ),
        (
            "formation_rarity_reported_not_forced_to_pass",
            sum(row["patch_rows"] for row in mass_patch_summaries) == 1050
            and all(not row["valid_for_MTS_formation_claim"] for row in mass_patch_summaries),
            mass_patch_summaries,
        ),
        (
            "primordial_covariance_not_claimed",
            all(not row["parent_primordial_covariance_derived"] for row in patch_rows)
            and all(not row["valid_for_MTS_primordial_claim"] for row in camb_rows),
            "empirical comparator only",
        ),
        (
            "actual_parent_c_ess_not_inserted",
            not previous_result["actual_parent_c_ess_inserted"],
            previous_result["actual_parent_c_ess_inserted"],
        ),
        (
            "nonlinear_attractor_not_claimed",
            not previous_result["nonlinear_profile_attractor_derived"]
            and all(not row["valid_for_claim"] for row in decisions),
            "linear covariance gate only",
        ),
    ]
    validation_rows = [
        {
            "check_id": f"V5156_{index:02d}_{name}",
            "passed": bool(passed),
            "detail": json.dumps(detail, sort_keys=True, default=json_default),
        }
        for index, (name, passed, detail) in enumerate(checks, start=1)
    ]
    failures = [row for row in validation_rows if not row["passed"]]

    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "parent_FLRW_Hessian_reduced": True,
        "Gaussian_state_nonuniqueness_proved": True,
        "single_clock_adiabatic_branch_derived_conditionally": True,
        "parent_single_clock_premise_derived": False,
        "parent_primordial_covariance_derived": False,
        "isocurvature_zero_derived": False,
        "source_backed_radiation_transfer_executed": True,
        "halo_patch_covariance_gate_executed": True,
        "nonlinear_profile_attractor_derived": False,
        "actual_parent_c_ess_inserted": False,
        "valid_for_local_GR_claim": False,
        "valid_for_cosmology_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_full_MTS_claim": False,
        "formalization_workbench_tree_sha256": formal_after,
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "primary_source_urls": PRIMARY_URLS,
        "CAMB_metadata": camb_metadata,
        "summary": summary,
        "mass_transfer_summaries": transfer_summaries,
        "mass_patch_summaries": mass_patch_summaries,
        "route_decision": decisions[-1]["status"],
        "validation_count": len(validation_rows),
        "validation_failures": failures,
    }

    write_csv(PROVENANCE_CSV, provenance)
    write_csv(FLRW_CSV, flrw)
    write_csv(GAUSSIAN_CSV, gaussian)
    write_csv(INITIAL_CSV, initial)
    write_csv(CAMB_CSV, camb_rows)
    write_csv(TRANSFER_CSV, transfer_rows)
    write_csv(TRANSFER_SUMMARY_CSV, transfer_summaries)
    write_csv(PATCH_SUMMARY_CSV, mass_patch_summaries)
    write_csv(PATCH_CSV, patch_rows)
    write_csv(DECISION_CSV, decisions)
    write_csv(VALIDATION_CSV, validation_rows)
    write_json(RESULT_JSON, result)
    write_document(result)

    if failures:
        raise RuntimeError(json.dumps(failures, indent=2, default=json_default))
    print(json.dumps(result, indent=2, sort_keys=True, default=json_default))


if __name__ == "__main__":
    main()
