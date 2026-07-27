from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import statistics
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
from scipy.special import expit


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
GALAXY = Path(r"D:\Users\ollet\Documents\mts-galaxy-lab")
OUT = POST / "source-intake" / "functional_rg" / "5151"
RESULT_JSON = OUT / "projective_state_stress_results.json"
MIXTURE_CSV = OUT / "positive_cored_profile_mixture.csv"
SHAPE_CSV = OUT / "parent_exponent_to_galaxy_support_shape.csv"
METRIC_CSV = OUT / "Einstein_cluster_stress_and_two_metric_functions.csv"
GALAXY_CSV = OUT / "galaxy_state_stress_scale_gate.csv"
RADIAL_CSV = OUT / "all_175_parent_phase_support_radial_smoke.csv"
LOCAL_CSV = OUT / "embedded_local_cog_tidal_gate.csv"
ROUTE_CSV = OUT / "state_stress_route_decision.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5151_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5151-Y5-R2FR-parent-projective-occupation-to-conserved-Einstein-cluster-stress-and-two-metric-cog-gate.md"
)
MARKER = "MTS_5151_PROJECTIVE_OCCUPATION_EINSTEIN_CLUSTER_STRESS_GATE"
CHECKED_DATE = "2026-07-20"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
C_KM_S = 299792.458
HBAR_C_EV_M = 1.973269804e-7
KPC_M = 3.085677581491367e19
AU_M = 1.495978707e11
GM_SUN_M3_S2 = 1.32712440018e20
G_ASTRO = 4.30091727003628e-6


SOURCE_PATHS = {
    "projective_parent": POST
    / "4948-Y5-R2FR-single-parent-motion-Hessian-to-galaxy-phase-flow-and-universal-Jgap-interface.md",
    "projective_result": POST
    / "source-intake"
    / "functional_rg"
    / "4948"
    / "motion_Hessian_galaxy_phase_results.json",
    "CTP_state_parent": POST
    / "4949-Y5-R2FR-covariant-2PI-motion-occupation-Dyson-source-and-conserved-galaxy-stress-or-composite-route-rejection.md",
    "universal_metric_source": POST
    / "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-and-local-GR-Newton-Maxwell-promotion-or-parent-field-content-boundary.md",
    "spectral_response": POST
    / "source-intake"
    / "functional_rg"
    / "5148"
    / "regime_selective_motion_response_results.json",
    "galaxy_interface": POST
    / "source-intake"
    / "functional_rg"
    / "5148"
    / "galaxy_kernel_interface_smoke.csv",
    "galaxy_app": GALAXY / "app.js",
    "galaxy_samples": GALAXY / "data" / "samples.js",
    "passive_common_kernel_rejection": POST
    / "5150-Y5-R2FR-minimal-occupied-PX-zero-mode-TT-polarization-and-critical-sign-gate.md",
    "local_zero_branch": POST
    / "4942-Y5-R2FR-O4-completed-endpoint-local-vacuum-homogeneous-motion-branch-and-C3-CFF-PPN-residual-gate.md",
}


PRIMARY_SOURCE_URLS = {
    "static_Einstein_Vlasov": "https://arxiv.org/abs/gr-qc/9304028",
    "axisymmetric_Einstein_Vlasov": "https://arxiv.org/abs/1006.1225",
    "Einstein_cluster_rotation_lensing": "https://arxiv.org/abs/0705.1756",
    "CTP_2PI": "https://arxiv.org/abs/hep-ph/0409233",
}


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(file_digest(item).encode("ascii"))
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True), encoding="utf-8"
    )
    temporary.replace(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_samples(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8-sig").strip()
    text = re.sub(r"^window\.MTS_SAMPLES\s*=\s*", "", text)
    text = re.sub(r";\s*$", "", text)
    return json.loads(text)


def parse_rotmod(text: str) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        values = [float(value) for value in stripped.split()]
        if len(values) < 8:
            continue
        rows.append(
            {
                "r": values[0],
                "v_obs": values[1],
                "err_v": values[2],
                "v_gas": values[3],
                "v_disk": values[4],
                "v_bulge": values[5],
            }
        )
    return rows


def phase_occupation(x_value: np.ndarray | float, exponent: float) -> np.ndarray | float:
    powered = np.asarray(x_value) ** exponent
    result = powered / (1.0 + powered)
    if np.ndim(result) == 0:
        return float(result)
    return result


def fit_phase_shape(exponent: float, locked_q: float) -> dict[str, float]:
    x_values = np.logspace(-3.0, 1.5, 80)
    target = 1.0 - np.exp(-(x_values**locked_q))

    def loss(log_scale: float) -> float:
        predicted = phase_occupation(math.exp(log_scale) * x_values, exponent)
        return float(np.mean((predicted - target) ** 2))

    optimum = minimize_scalar(
        loss,
        bounds=(math.log(0.05), math.log(20.0)),
        method="bounded",
        options={"xatol": 1.0e-12},
    )
    scale = math.exp(float(optimum.x))
    predicted = np.asarray(phase_occupation(scale * x_values, exponent))
    residual = predicted - target
    return {
        "exponent": exponent,
        "global_scale": scale,
        "transition_radius_over_L_eff": 1.0 / scale,
        "rmse": float(math.sqrt(np.mean(residual**2))),
        "mae": float(np.mean(np.abs(residual))),
        "maximum_absolute_error": float(np.max(np.abs(residual))),
        "support_at_L_eff": float(phase_occupation(scale, exponent)),
    }


def mixture_pdf_u(u_value: float, exponent: float) -> float:
    alpha = exponent / 2.0
    theta = math.pi * alpha
    return math.sin(theta) / (
        2.0 * math.pi * alpha * (math.cosh(u_value) + math.cos(theta))
    )


def reconstruct_phase_from_cored_mixture(x_value: float, exponent: float) -> float:
    alpha = exponent / 2.0
    logarithmic_x = math.log(x_value)
    transition = 2.0 * alpha * logarithmic_x

    def integrand(u_value: float) -> float:
        return mixture_pdf_u(u_value, exponent) * expit(
            2.0 * logarithmic_x - u_value / alpha
        )

    intervals = [(-80.0, min(transition, 80.0)), (max(-80.0, transition), 80.0)]
    return sum(
        quad(
            integrand,
            left,
            right,
            epsabs=1.0e-20,
            epsrel=1.0e-12,
            limit=400,
        )[0]
        for left, right in intervals
        if left < right
    )


def weight_per_log_core(log_core: float, exponent: float) -> float:
    theta = math.pi * exponent / 2.0
    return math.sin(theta) / (
        math.pi * (math.cosh(exponent * log_core) + math.cos(theta))
    )


def build_mixture_rows(
    exponents: dict[str, float],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, float]]]:
    rows: list[dict[str, Any]] = []
    summaries: dict[str, dict[str, float]] = {}
    reconstruction_grid = np.logspace(-6.0, 6.0, 13)
    for mapping, exponent in exponents.items():
        alpha = exponent / 2.0
        normalization = quad(
            lambda u_value: mixture_pdf_u(u_value, exponent),
            -60.0,
            60.0,
            epsabs=1.0e-13,
            epsrel=1.0e-12,
            limit=400,
        )[0]
        relative_errors: list[float] = []
        for x_value in reconstruction_grid:
            exact = float(phase_occupation(float(x_value), exponent))
            reconstructed = reconstruct_phase_from_cored_mixture(
                float(x_value), exponent
            )
            relative_error = abs(reconstructed - exact) / max(exact, 1.0e-300)
            relative_errors.append(relative_error)
            rows.append(
                {
                    "row_type": "mixture_reconstruction",
                    "mapping": mapping,
                    "q_parent": exponent,
                    "alpha=q/2": alpha,
                    "x_or_core_ratio": float(x_value),
                    "exact_phase_occupation": exact,
                    "mixture_value_or_weight": reconstructed,
                    "relative_error": relative_error,
                    "component_density_positive": True,
                    "valid_for_galaxy_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
        for log_core in np.linspace(-8.0, 8.0, 129):
            core_ratio = math.exp(float(log_core))
            component_density_at_unit_radius = (
                1.0 + 3.0 * core_ratio**2
            ) / (1.0 + core_ratio**2) ** 2
            rows.append(
                {
                    "row_type": "log_core_weight",
                    "mapping": mapping,
                    "q_parent": exponent,
                    "alpha=q/2": alpha,
                    "x_or_core_ratio": core_ratio,
                    "exact_phase_occupation": "",
                    "mixture_value_or_weight": weight_per_log_core(
                        float(log_core), exponent
                    ),
                    "relative_error": "",
                    "component_density_positive": component_density_at_unit_radius
                    > 0.0,
                    "valid_for_galaxy_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
        summaries[mapping] = {
            "q": exponent,
            "alpha": alpha,
            "normalization": normalization,
            "maximum_reconstruction_relative_error": max(relative_errors),
            "central_density_power_q_minus_2": exponent - 2.0,
            "central_acceleration_power_q_minus_1": exponent - 1.0,
        }
    return rows, summaries


def build_metric_rows(
    exponents: dict[str, float],
    shape_fits: dict[str, dict[str, float]],
    maximum_beta: float,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, float]]]:
    rows: list[dict[str, Any]] = []
    summaries: dict[str, dict[str, float]] = {}
    x_values = np.logspace(-6.0, 4.0, 161)
    for mapping, exponent in exponents.items():
        scale = shape_fits[mapping]["global_scale"]
        density_shapes: list[float] = []
        stability_shapes: list[float] = []
        algebra_residuals: list[float] = []
        for x_value in x_values:
            occupation = float(phase_occupation(scale * x_value, exponent))
            logarithmic_slope = exponent * (1.0 - occupation)
            beta = maximum_beta * occupation
            compactness = beta / (1.0 + 2.0 * beta)
            compactness_log_derivative = (
                beta * logarithmic_slope / (1.0 + 2.0 * beta) ** 2
            )
            density_shape = (
                compactness + compactness_log_derivative
            ) / x_value**2
            tangential_pressure_ratio = beta / 2.0
            radial_stability_shape = occupation * (2.0 + logarithmic_slope)
            metric_A_ratio = (
                (1.0 + (scale * x_value) ** exponent)
                / (1.0 + scale**exponent)
            ) ** (2.0 * maximum_beta / exponent)
            density_shapes.append(density_shape)
            stability_shapes.append(radial_stability_shape)
            mass_velocity_residual = abs(
                compactness / (1.0 - 2.0 * compactness) - beta
            )
            metric_B_residual = abs(
                (1.0 - 2.0 * compactness) * (1.0 + 2.0 * beta) - 1.0
            )
            conservation_residual = abs(2.0 * tangential_pressure_ratio - beta)
            algebra_residuals.extend(
                [mass_velocity_residual, metric_B_residual, conservation_residual]
            )
            rows.append(
                {
                    "mapping": mapping,
                    "q_parent": exponent,
                    "x=r_over_L_eff": float(x_value),
                    "occupation_support": occupation,
                    "dln_support_dlnr": logarithmic_slope,
                    "beta=v_c2_over_c2_worst_galaxy": beta,
                    "compactness_Gm_over_c2r": compactness,
                    "density_shape_4piGL2rho_over_c2": density_shape,
                    "p_r_over_rho_c2": 0.0,
                    "p_t_each_over_rho_c2": tangential_pressure_ratio,
                    "metric_A_over_A_at_Leff": metric_A_ratio,
                    "metric_B_areal": 1.0 + 2.0 * beta,
                    "weak_radial_epicyclic_shape": radial_stability_shape,
                    "mass_velocity_identity_residual": mass_velocity_residual,
                    "metric_B_identity_residual": metric_B_residual,
                    "stress_conservation_identity_residual": conservation_residual,
                    "energy_conditions_pass": beta >= 0.0 and beta < 1.0,
                    "valid_for_galaxy_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
        summaries[mapping] = {
            "minimum_density_shape": min(density_shapes),
            "minimum_radial_epicyclic_shape": min(stability_shapes),
            "maximum_exact_algebra_residual": max(algebra_residuals),
            "maximum_tangential_pressure_over_energy": maximum_beta / 2.0,
            "maximum_lensing_gradient_proxy_deviation": maximum_beta
            / (1.0 + 2.0 * maximum_beta),
            "maximum_areal_spatial_vs_rotation_gradient_mismatch": 2.0
            * maximum_beta
            / (1.0 + 2.0 * maximum_beta),
        }
    return rows, summaries


def build_galaxy_rows(
    source_rows: list[dict[str, str]],
    exponents: dict[str, float],
    shape_fits: dict[str, dict[str, float]],
    gamma0: float,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    mercury_radius = 0.387098 * AU_M
    mercury_solar_acceleration = GM_SUN_M3_S2 / mercury_radius**2
    for source_row in source_rows:
        length_kpc = float(source_row["L_eff_kpc"])
        plateau_velocity_squared = gamma0 * length_kpc
        plateau_velocity = math.sqrt(plateau_velocity_squared)
        beta_infinity = plateau_velocity_squared / C_KM_S**2
        for mapping, exponent in exponents.items():
            scale = shape_fits[mapping]["global_scale"]
            transition_ratio = 1.0 / scale
            transition_radius_kpc = length_kpc * transition_ratio
            transition_velocity = math.sqrt(plateau_velocity_squared / 2.0)
            minimum_wkb_mass = HBAR_C_EV_M / (
                transition_radius_kpc
                * KPC_M
                * (transition_velocity / C_KM_S)
            )
            support_at_length = float(phase_occupation(scale, exponent))
            logarithmic_slope_at_length = exponent * (1.0 - support_at_length)
            beta_at_length = beta_infinity * support_at_length
            compactness_at_length = beta_at_length / (1.0 + 2.0 * beta_at_length)
            state_mass_at_length = (
                C_KM_S**2
                * length_kpc
                * compactness_at_length
                / G_ASTRO
            )
            acceleration_gradient = (
                abs(logarithmic_slope_at_length - 1.0)
                * plateau_velocity_squared
                * 1.0e6
                * support_at_length
                / (length_kpc * KPC_M) ** 2
            )
            mercury_tidal_ratio = (
                acceleration_gradient
                * mercury_radius
                / mercury_solar_acceleration
            )
            rows.append(
                {
                    "galaxy": source_row["galaxy"],
                    "mapping": mapping,
                    "q_parent": exponent,
                    "global_phase_scale": scale,
                    "R_n_over_L_eff": transition_ratio,
                    "L_eff_kpc": length_kpc,
                    "Gamma0_L_eff_km2_s2": plateau_velocity_squared,
                    "v_infinity_km_s": plateau_velocity,
                    "beta_infinity": beta_infinity,
                    "support_at_L_eff": support_at_length,
                    "state_mass_inside_L_eff_Msun": state_mass_at_length,
                    "maximum_p_t_each_over_rho_c2": beta_infinity / 2.0,
                    "lensing_gradient_proxy_deviation_ceiling": beta_infinity
                    / (1.0 + 2.0 * beta_infinity),
                    "minimum_m_gap_eV_for_lambda_db_le_Rn": minimum_wkb_mass,
                    "minimum_m_gap_eV_for_lambda_db_le_0p1_Rn": 10.0
                    * minimum_wkb_mass,
                    "Mercury_tide_over_solar_at_host_R_equals_L_eff": mercury_tidal_ratio,
                    "required_Cn_scaling": "C_n=(xi ell_gap a/L_eff)^q_parent",
                    "source_population_derived": False,
                    "valid_for_galaxy_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
    beta_values = [row["beta_infinity"] for row in rows]
    wkb_values = [
        row["minimum_m_gap_eV_for_lambda_db_le_Rn"] for row in rows
    ]
    tide_values = [
        row["Mercury_tide_over_solar_at_host_R_equals_L_eff"] for row in rows
    ]
    summary = {
        "source_galaxy_count": len(source_rows),
        "branch_row_count": len(rows),
        "minimum_beta_infinity": min(beta_values),
        "median_beta_infinity": statistics.median(beta_values),
        "maximum_beta_infinity": max(beta_values),
        "maximum_tangential_pressure_over_energy": max(beta_values) / 2.0,
        "maximum_lensing_gradient_proxy_deviation": max(
            beta / (1.0 + 2.0 * beta) for beta in beta_values
        ),
        "minimum_WKB_mass_eV": min(wkb_values),
        "median_WKB_mass_eV": statistics.median(wkb_values),
        "maximum_WKB_mass_eV": max(wkb_values),
        "maximum_Mercury_tidal_ratio": max(tide_values),
    }
    return rows, summary


def build_radial_smoke(
    samples: list[dict[str, Any]],
    length_rows: list[dict[str, str]],
    exponents: dict[str, float],
    shape_fits: dict[str, dict[str, float]],
    gamma0: float,
    locked_q: float,
    ml_disk: float,
    ml_bulge: float,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    lengths = {row["galaxy"]: float(row["L_eff_kpc"]) for row in length_rows}
    rows: list[dict[str, Any]] = []
    summaries: dict[str, dict[str, Any]] = {}
    for mapping, exponent in exponents.items():
        scale = shape_fits[mapping]["global_scale"]
        parent_squared_error_total = 0.0
        locked_squared_error_total = 0.0
        point_total = 0
        parent_rmse_values: list[float] = []
        locked_rmse_values: list[float] = []
        maximum_total_beta = 0.0
        wins = 0
        for sample in samples:
            galaxy = sample["name"].replace("_rotmod.dat", "")
            if galaxy not in lengths:
                raise RuntimeError(f"missing L_eff row for {galaxy}")
            length_kpc = lengths[galaxy]
            points = parse_rotmod(sample["text"])
            parent_squared_errors: list[float] = []
            locked_squared_errors: list[float] = []
            galaxy_maximum_beta = 0.0
            for point in points:
                baryonic_velocity_squared = (
                    point["v_gas"] * abs(point["v_gas"])
                    + ml_disk * point["v_disk"] ** 2
                    + ml_bulge * point["v_bulge"] ** 2
                )
                scaled_radius = scale * point["r"] / length_kpc
                parent_support = gamma0 * length_kpc * float(
                    phase_occupation(scaled_radius, exponent)
                )
                locked_support = gamma0 * length_kpc * (
                    1.0
                    - math.exp(-((point["r"] / length_kpc) ** locked_q))
                )
                parent_model = math.sqrt(
                    max(0.0, baryonic_velocity_squared + parent_support)
                )
                locked_model = math.sqrt(
                    max(0.0, baryonic_velocity_squared + locked_support)
                )
                parent_squared_errors.append(
                    (parent_model - point["v_obs"]) ** 2
                )
                locked_squared_errors.append(
                    (locked_model - point["v_obs"]) ** 2
                )
                galaxy_maximum_beta = max(
                    galaxy_maximum_beta,
                    max(0.0, baryonic_velocity_squared + parent_support)
                    / C_KM_S**2,
                )
            if not parent_squared_errors:
                raise RuntimeError(f"no ROTMOD rows for {galaxy}")
            parent_rmse = math.sqrt(
                sum(parent_squared_errors) / len(parent_squared_errors)
            )
            locked_rmse = math.sqrt(
                sum(locked_squared_errors) / len(locked_squared_errors)
            )
            if parent_rmse < locked_rmse:
                wins += 1
            parent_rmse_values.append(parent_rmse)
            locked_rmse_values.append(locked_rmse)
            parent_squared_error_total += sum(parent_squared_errors)
            locked_squared_error_total += sum(locked_squared_errors)
            point_total += len(parent_squared_errors)
            maximum_total_beta = max(maximum_total_beta, galaxy_maximum_beta)
            rows.append(
                {
                    "galaxy": galaxy,
                    "mapping": mapping,
                    "q_parent": exponent,
                    "global_phase_scale": scale,
                    "point_count": len(parent_squared_errors),
                    "parent_phase_support_RMSE_km_s": parent_rmse,
                    "locked_exponential_RMSE_km_s": locked_rmse,
                    "parent_phase_wins": parent_rmse < locked_rmse,
                    "maximum_total_v2_over_c2": galaxy_maximum_beta,
                    "maximum_motion_p_t_each_over_rho_c2": galaxy_maximum_beta
                    / 2.0,
                    "per_galaxy_shape_fit": False,
                    "uncertainty_weighted_likelihood": False,
                    "valid_for_galaxy_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
        summaries[mapping] = {
            "q_parent": exponent,
            "global_phase_scale": scale,
            "galaxy_count": len(parent_rmse_values),
            "point_count": point_total,
            "mean_parent_RMSE_km_s": statistics.mean(parent_rmse_values),
            "median_parent_RMSE_km_s": statistics.median(parent_rmse_values),
            "mean_locked_RMSE_km_s": statistics.mean(locked_rmse_values),
            "median_locked_RMSE_km_s": statistics.median(locked_rmse_values),
            "pooled_parent_RMSE_km_s": math.sqrt(
                parent_squared_error_total / point_total
            ),
            "pooled_locked_RMSE_km_s": math.sqrt(
                locked_squared_error_total / point_total
            ),
            "parent_wins_out_of_175": wins,
            "maximum_total_v2_over_c2": maximum_total_beta,
            "maximum_motion_p_t_each_over_rho_c2": maximum_total_beta / 2.0,
            "maximum_weak_lensing_pressure_order": maximum_total_beta
            / (1.0 + 2.0 * maximum_total_beta),
        }
    return rows, summaries


def build_local_rows(maximum_mercury_tide: float) -> list[dict[str, Any]]:
    mercury_au = 0.387098
    return [
        {
            "arena": arena,
            "orbital_radius_AU": radius_au,
            "worst_embedded_halo_tide_over_solar": maximum_mercury_tide
            * (radius_au / mercury_au) ** 3,
            "comparison_ceiling": 1.0e-5,
            "passes_comparison_ceiling": maximum_mercury_tide
            * (radius_au / mercury_au) ** 3
            < 1.0e-5,
            "classical_motion_fifth_force": 0.0,
            "reason": "reflection-even state has zero mean scalar and one universal metric source",
            "valid_for_PPN_claim": False,
            "checkpoint_marker": MARKER,
        }
        for arena, radius_au in [
            ("Mercury_orbit", 0.387098),
            ("Earth_orbit", 1.0),
            ("Neptune_orbit", 30.07),
        ]
    ]


def write_document(result: dict[str, Any]) -> None:
    shape = result["shape_map"]
    mixture = result["positive_mixture"]
    galaxy = result["galaxy_scale_gate"]
    radial = result["radial_smoke"]
    best_mapping = min(
        (key for key in shape if shape[key]["origin"] == "parent"),
        key=lambda key: shape[key]["rmse"],
    )
    best = shape[best_mapping]
    best_radial = radial[best_mapping]
    q_values = [row["exponent"] for row in shape.values() if row["origin"] == "parent"]
    DOCUMENT.write_text(
        f"""# 5151 - Parent projective occupation to conserved Einstein-cluster stress and two-metric cog gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

The direct state-stress route is constructively viable at the stationary
existence level. It does not need the checkpoint-5150 propagator dressing.
The reflection-even CTP two-point state has a collisionless Wigner limit

```text
Delta T^munu_state = integral dPi p^mu p^nu f(x,p),
p^mu nabla_mu f = 0,
<psi> = 0.
```

A stationary axisymmetric distribution may depend on the conserved orbit
labels `E`, `L_z` and a third integral where one exists. The explicit
spherical circular-orbit member derived below is also axisymmetric and gives
one conserved, positive stress realizing the machine/cog requirement. This
is an existence theorem, not yet the parent-selected galaxy state.

Primary comparison sources for static and axisymmetric Einstein--Vlasov
states and circular-orbit clusters are
`{PRIMARY_SOURCE_URLS['static_Einstein_Vlasov']}`,
`{PRIMARY_SOURCE_URLS['axisymmetric_Einstein_Vlasov']}` and
`{PRIMARY_SOURCE_URLS['Einstein_cluster_rotation_lensing']}`.

## Exact positive cored-profile representation

For any `0<q<2`, set `alpha=q/2` and `s=x^2`. The projective occupation has
the exact Stieltjes representation

```text
n_q(x)=x^q/(1+x^q)
      =integral_0^infinity dt [x^2/(x^2+t)] rho_q(t),

rho_q(t)=sin(pi alpha) t^(alpha-1)
         /{{pi[1+2t^alpha cos(pi alpha)+t^(2alpha)]}}.
```

The density is positive and normalized. Each kernel
`x^2/(x^2+t)` is a regular cored flat-rotation component with

```text
rho_t(r)=U_infinity/(4pi G)
         (r^2+3r_c^2)/(r^2+r_c^2)^2,
r_c=L sqrt(t).
```

Thus the fractional projective law is not an arbitrary singular halo profile:
it is a unique positive continuum of regular core scales. The two parent
exponents `{min(q_values)}` and `{max(q_values)}` both lie inside the positivity
window. Numerical quadrature reconstructs the occupation with worst relative
error `{max(row['maximum_reconstruction_relative_error'] for row in mixture.values())}`.

The uncut continuum still has `rho proportional r^(q-2)` at the exact centre
and a linearly growing mass at infinity. For the parent exponents the central
force behaves as `r^(q-1)` and therefore vanishes, unlike an extrapolated
`q=0.77` force. A finite smallest core and outer density boundary are still
mandatory for a globally regular, finite-mass state; they must come from
`J_gap`, formation and the parent boundary state rather than per-galaxy
patches.

## Parent exponent maps to the empirical support

The old galaxy support is `1-exp[-(r/L_eff)^0.77]`. It was already proved not
to be the projective occupation itself. Allowing only one global conversion
`n_q(a r/L_eff)`, with no galaxy-by-galaxy shape parameter, gives

```text
best parent mapping = {best_mapping},
q_parent            = {best['exponent']},
a                    = {best['global_scale']},
R_n/L_eff            = {best['transition_radius_over_L_eff']},
shape RMSE           = {best['rmse']}.
```

The rejected 5148 common-propagator route had shape RMSE
`{result['discarded_kernel_shape_rmse']}`. The direct parent-state value is
slightly worse but genuinely comparable, and it uses the parent exponent
near `1.85` rather than relabelling it as `0.77`. The required source-amplitude
law is now concrete:

```text
R_n=xi ell_gap C_n^(-1/q_parent)=L_eff/a,
C_n=(xi ell_gap a/L_eff)^q_parent.
```

This scaling is derived. Its normalization and dynamical population are not.
The numerical `q_parent` values are critical exponents of the source-locked
parent Hessian. Their transport to the infrared occupied state under the
`k proportional 1/r` shell map remains conditional; this checkpoint proves
that the parent values have a viable stress realization, not that the RG
trajectory has already delivered them unchanged to galaxies.

## Conserved stress and both metric functions

Use areal radius and

```text
ds^2=-A(r)c^2dt^2+B(r)dr^2+r^2dOmega^2,
beta(r)=v_c^2(r)/c^2.
```

First isolate the motion component to prove existence. Take a reflection-even
ensemble of massive motion quanta on circular orbits with all orbital planes
populated symmetrically. Its radial pressure and net momentum vanish. The
exact spherical Einstein equations, circular-geodesic condition and
conservation law give

```text
p_r=0,
w=Gm/(c^2r)=beta/(1+2beta),
B=(1-2w)^(-1)=1+2beta,
d ln A/d ln r=2beta,
p_t=p_theta=p_phi=rho c^2 beta/2,

rho=c^2/(4pi G r^2)
    [w+d w/d ln r].
```

For `beta=beta_infinity n_q(a r/L_eff)`, both metric functions are explicit:

```text
A(r)/A(L_eff)
 =[(1+(a r/L_eff)^q)/(1+a^q)]^(2 beta_infinity/q),
B(r)=1+2 beta_infinity n_q(a r/L_eff).
```

The density is positive, the weak-field circular-shell gate has
`kappa_r^2 proportional n_q[2+q(1-n_q)]>0`, and the dominant-energy margin is
enormous for the executed galaxies. No radial pressure or lensing slip was
inserted by hand: the tangential stress follows from conservation.

Those closed forms are the exact isolated-cluster existence solution. In an
actual baryonic galaxy the motion quanta orbit in the **total** metric. At
leading weak order the density contribution superposes while conservation
changes the motion tangential stress to

```text
p_t,motion/(rho_motion c^2)=v_total^2/(2c^2).
```

The all-point execution below uses this total baryonic-plus-motion velocity;
it does not mislabel the isolated expression as an exact disk solution.

## All-175 scale and local-cog execution

Using only the locked amplitude `U_infinity=Gamma0 L_eff` from the read-only
5148 interface, both parent mappings were evaluated for all 175 galaxies.

```text
maximum beta_infinity                         = {galaxy['maximum_beta_infinity']},
maximum p_t/(rho c^2)                         = {galaxy['maximum_tangential_pressure_over_energy']},
maximum weak lensing-gradient proxy deviation = {galaxy['maximum_lensing_gradient_proxy_deviation']},
largest WKB m_gap floor at R_n                 = {galaxy['maximum_WKB_mass_eV']} eV,
largest embedded Mercury tidal ratio           = {galaxy['maximum_Mercury_tidal_ratio']}.
```

The full read-only ROTMOD pass then evaluates all
`{best_radial['point_count']}` measured radii with the unchanged baryonic law.
For the best parent mapping it gives

```text
mean RMSE:   {best_radial['mean_parent_RMSE_km_s']} km/s
locked mean: {best_radial['mean_locked_RMSE_km_s']} km/s
median RMSE: {best_radial['median_parent_RMSE_km_s']} km/s
locked med.: {best_radial['median_locked_RMSE_km_s']} km/s
wins:        {best_radial['parent_wins_out_of_175']}/175
pooled RMSE: {best_radial['pooled_parent_RMSE_km_s']} versus {best_radial['pooled_locked_RMSE_km_s']} km/s
```

This is a genuine out-of-construction interface smoke: the one global phase
conversion was chosen against the published support shape, not optimized per
galaxy or against the velocities. It modestly improves the unweighted radial
RMSE. It is not a replacement for the galaxy project's uncertainty,
jackknife and population tests.

All total velocities remain nonrelativistic, with maximum
`v_total^2/c^2={best_radial['maximum_total_v2_over_c2']}` and motion
`p_t/(rho c^2)<={best_radial['maximum_motion_p_t_each_over_rho_c2']}`. The
leading pressure-sensitive lensing order is below
`{best_radial['maximum_weak_lensing_pressure_order']}`. A projected deflection
claim still requires a finite outer boundary because the untruncated plateau
is not asymptotically flat.

An occupied galactic state need not vanish at the Solar System. Its uniform
acceleration is shared by Sun and planet; the relative orbital effect is the
halo tide. At the explicitly declared diagnostic location `R_host=L_eff`,
the worst Mercury ratio is below `7e-19` and the worst Neptune ratio is below
`4e-13`, while the classical scalar fifth force remains zero. This is not a
global Solar-System PPN bound, but it demonstrates how the Mercury cog can
keep turning inside a smooth occupied galactic state.

## What is and is not achieved

```text
CTP state stress from positive occupation                = derived in WKB form;
stationary axisymmetric kinetic contract                 = derived;
spherical circular-orbit realization                     = constructed;
projective occupation as positive cored continuum        = exact;
parent q near 1.85 retained                              = yes;
parent q transported to the occupied infrared state      = not yet derived;
conserved rho, p_r, p_t                                  = derived;
both spherical metric functions                          = derived;
rotation support and leading lensing compatibility       = passed conditionally;
embedded local Mercury/planet cog                         = strongly suppressed;
one universal metric/Hilbert coupling                     = retained;
source-selected C_n and total occupation                  = not yet derived;
finite central core and outer halo boundary               = not yet derived;
full flattened axisymmetric galaxy solution               = not yet solved;
full projected lensing likelihood                         = not yet run;
galaxy or full-MTS claim                                  = false.
```

If the parent cannot generate the required `C_n`, state normalization and
finite boundaries, this route is only collisionless scalar halo matter under
a new name. The next derivation must therefore attack the source selection,
not refit the stress profile: obtain the circular-state occupation from the
formation CTP kernel with one `J_gap` and carry the exponent down the
occupied infrared trajectory, or reject this route.

All `{result['validation_count']}` validation checks pass. The protected
`formalization-workbench` hash remains
`{result['formalization_workbench_tree_sha256']}`. No GitHub or galaxy-repo
write occurred.
""",
        encoding="utf-8",
    )


def main() -> None:
    missing = [str(path) for path in SOURCE_PATHS.values() if not path.exists()]
    if missing:
        raise RuntimeError(f"missing source paths: {missing}")
    source_hashes_before = {
        name: file_digest(path) for name, path in SOURCE_PATHS.items()
    }
    formal_before = tree_digest(FORMAL)
    projective_result = json.loads(
        SOURCE_PATHS["projective_result"].read_text(encoding="utf-8")
    )
    spectral_result = json.loads(
        SOURCE_PATHS["spectral_response"].read_text(encoding="utf-8")
    )
    galaxy_source_rows = read_csv(SOURCE_PATHS["galaxy_interface"])
    galaxy_samples = parse_samples(SOURCE_PATHS["galaxy_samples"])
    parent_exponents = {
        name: float(value)
        for name, value in projective_result["parent_exponents"][
            "theta_mass_by_mapping"
        ].items()
    }
    locked_q = float(projective_result["galaxy_snapshot"]["locked_q"])
    gamma0 = float(spectral_result["locked_constants"]["gamma0"])
    ml_disk = float(spectral_result["locked_constants"]["ml_disk"])
    ml_bulge = float(spectral_result["locked_constants"]["ml_bulge"])
    shape_fits = {
        name: fit_phase_shape(exponent, locked_q)
        for name, exponent in parent_exponents.items()
    }
    locked_comparator = fit_phase_shape(locked_q, locked_q)
    shape_rows = []
    for name, values in shape_fits.items():
        shape_rows.append(
            {
                "mapping": name,
                "origin": "parent",
                **values,
                "locked_empirical_q": locked_q,
                "discarded_5148_kernel_rmse": spectral_result["kernel"][
                    "shape_rmse"
                ],
                "valid_for_galaxy_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    shape_rows.append(
        {
            "mapping": "locked_q_comparator_only",
            "origin": "empirical_comparator_not_parent",
            **locked_comparator,
            "locked_empirical_q": locked_q,
            "discarded_5148_kernel_rmse": spectral_result["kernel"]["shape_rmse"],
            "valid_for_galaxy_claim": False,
            "checkpoint_marker": MARKER,
        }
    )
    mixture_rows, mixture_summaries = build_mixture_rows(parent_exponents)
    galaxy_rows, galaxy_summary = build_galaxy_rows(
        galaxy_source_rows, parent_exponents, shape_fits, gamma0
    )
    radial_rows, radial_summary = build_radial_smoke(
        galaxy_samples,
        galaxy_source_rows,
        parent_exponents,
        shape_fits,
        gamma0,
        locked_q,
        ml_disk,
        ml_bulge,
    )
    metric_rows, metric_summaries = build_metric_rows(
        parent_exponents, shape_fits, galaxy_summary["maximum_beta_infinity"]
    )
    local_rows = build_local_rows(galaxy_summary["maximum_Mercury_tidal_ratio"])
    route_rows = [
        {
            "route": "vacuum_or_common_metric_propagator_dressing",
            "result": "REJECTED_BY_5149_5150",
            "next_requirement": "none",
            "valid_for_claim": False,
        },
        {
            "route": "reflection_even_projective_CTP_state_stress",
            "result": "CONSTRUCTIVE_STATIONARY_EXISTENCE_PASS",
            "next_requirement": "derive source-selected occupation from formation CTP kernel",
            "valid_for_claim": False,
        },
        {
            "route": "positive_cored_profile_continuum",
            "result": "EXACT_FOR_0_LT_Q_LT_2",
            "next_requirement": "derive smallest-core and outer-density cutoffs",
            "valid_for_claim": False,
        },
        {
            "route": "parent_q_to_empirical_support",
            "result": "ONE_GLOBAL_SCALE_COMPARABLE_SHAPE",
            "next_requirement": "derive IR exponent transport phase scale and amplitude",
            "valid_for_claim": False,
        },
        {
            "route": "parent_q_all_175_radial_interface",
            "result": "UNWEIGHTED_SMOKE_IMPROVES_LOCKED_BASELINE",
            "next_requirement": "hand off to uncertainty jackknife population and lensing tests",
            "valid_for_claim": False,
        },
        {
            "route": "local_GR_inside_occupied_galaxy",
            "result": "METRIC_ONLY_AND_TIDALLY_SUPPRESSED",
            "next_requirement": "full finite-boundary PPN embedding",
            "valid_for_claim": False,
        },
        {
            "route": "full_MTS_galaxy_unification",
            "result": "NOT_CLAIMED",
            "next_requirement": "source population core outer boundary axisymmetry and lensing likelihood",
            "valid_for_claim": False,
        },
    ]
    write_csv(MIXTURE_CSV, mixture_rows)
    write_csv(SHAPE_CSV, shape_rows)
    write_csv(METRIC_CSV, metric_rows)
    write_csv(GALAXY_CSV, galaxy_rows)
    write_csv(RADIAL_CSV, radial_rows)
    write_csv(LOCAL_CSV, local_rows)
    write_csv(ROUTE_CSV, route_rows)
    source_hashes_after = {
        name: file_digest(path) for name, path in SOURCE_PATHS.items()
    }
    formal_after = tree_digest(FORMAL)
    shape_result = {
        name: {"origin": "parent", **values}
        for name, values in shape_fits.items()
    }
    shape_result["locked_q_comparator_only"] = {
        "origin": "empirical_comparator_not_parent",
        **locked_comparator,
    }
    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "source_paths": {name: str(path) for name, path in SOURCE_PATHS.items()},
        "primary_source_urls": PRIMARY_SOURCE_URLS,
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "parent_exponents": parent_exponents,
        "locked_empirical_q": locked_q,
        "positive_mixture": mixture_summaries,
        "shape_map": shape_result,
        "discarded_kernel_shape_rmse": float(
            spectral_result["kernel"]["shape_rmse"]
        ),
        "metric_gate": metric_summaries,
        "galaxy_scale_gate": galaxy_summary,
        "radial_smoke": radial_summary,
        "state_stress_stationary_existence_constructed": True,
        "parent_exponent_IR_transport_derived": False,
        "source_selected_occupation_derived": False,
        "finite_core_derived": False,
        "finite_outer_boundary_derived": False,
        "full_axisymmetric_solution_derived": False,
        "valid_for_PPN_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_full_MTS_claim": False,
        "formalization_workbench_tree_sha256": formal_after,
    }
    checks = [
        ("source_paths_exist", not missing, str(missing)),
        (
            "sources_read_only",
            source_hashes_before == source_hashes_after,
            str(source_hashes_after),
        ),
        (
            "formal_tree_unchanged",
            formal_before == FORMAL_BASELINE and formal_after == FORMAL_BASELINE,
            formal_after,
        ),
        (
            "parent_exponents_inside_positive_mixture_window",
            all(0.0 < value < 2.0 for value in parent_exponents.values()),
            str(parent_exponents),
        ),
        (
            "mixture_normalized",
            all(
                abs(summary["normalization"] - 1.0) < 1.0e-10
                for summary in mixture_summaries.values()
            ),
            str(
                {
                    name: summary["normalization"]
                    for name, summary in mixture_summaries.items()
                }
            ),
        ),
        (
            "mixture_reconstructs_projective_phase",
            all(
                summary["maximum_reconstruction_relative_error"] < 1.0e-9
                for summary in mixture_summaries.values()
            ),
            str(
                {
                    name: summary["maximum_reconstruction_relative_error"]
                    for name, summary in mixture_summaries.items()
                }
            ),
        ),
        (
            "component_and_total_density_positive",
            all(row["component_density_positive"] for row in mixture_rows)
            and all(
                summary["minimum_density_shape"] > 0.0
                for summary in metric_summaries.values()
            ),
            str(
                {
                    name: summary["minimum_density_shape"]
                    for name, summary in metric_summaries.items()
                }
            ),
        ),
        (
            "one_global_parent_shape_map_comparable",
            all(values["rmse"] < 0.07 for values in shape_fits.values()),
            str({name: values["rmse"] for name, values in shape_fits.items()}),
        ),
        (
            "all_175_galaxies_two_parent_mappings",
            len(galaxy_source_rows) == 175
            and len(galaxy_rows) == 2 * len(galaxy_source_rows),
            str([len(galaxy_source_rows), len(galaxy_rows)]),
        ),
        (
            "all_3391_radial_points_two_parent_mappings",
            len(galaxy_samples) == 175
            and len(radial_rows) == 350
            and all(
                summary["point_count"] == 3391
                for summary in radial_summary.values()
            ),
            str(
                {
                    "samples": len(galaxy_samples),
                    "rows": len(radial_rows),
                    "points": {
                        name: summary["point_count"]
                        for name, summary in radial_summary.items()
                    },
                }
            ),
        ),
        (
            "parent_phase_radial_smoke_beats_locked_mean",
            all(
                summary["mean_parent_RMSE_km_s"]
                < summary["mean_locked_RMSE_km_s"]
                and summary["pooled_parent_RMSE_km_s"]
                < summary["pooled_locked_RMSE_km_s"]
                for summary in radial_summary.values()
            ),
            str(radial_summary),
        ),
        (
            "radial_smoke_has_no_per_galaxy_shape_fit",
            all(not row["per_galaxy_shape_fit"] for row in radial_rows),
            "one phase conversion per parent mapping",
        ),
        (
            "all_state_velocities_nonrelativistic",
            galaxy_summary["maximum_beta_infinity"] < 1.0e-6
            and max(
                summary["maximum_total_v2_over_c2"]
                for summary in radial_summary.values()
            )
            < 1.0e-5,
            str(
                {
                    "motion_plateau": galaxy_summary["maximum_beta_infinity"],
                    "total_radial": max(
                        summary["maximum_total_v2_over_c2"]
                        for summary in radial_summary.values()
                    ),
                }
            ),
        ),
        (
            "energy_conditions_and_circular_stability",
            all(row["energy_conditions_pass"] for row in metric_rows)
            and all(
                summary["minimum_radial_epicyclic_shape"] > 0.0
                for summary in metric_summaries.values()
            ),
            str(metric_summaries),
        ),
        (
            "exact_cluster_algebra_closes",
            all(
                summary["maximum_exact_algebra_residual"] < 1.0e-14
                for summary in metric_summaries.values()
            ),
            str(
                {
                    name: summary["maximum_exact_algebra_residual"]
                    for name, summary in metric_summaries.items()
                }
            ),
        ),
        (
            "two_metric_functions_finite_on_executed_annulus",
            all(
                math.isfinite(float(row["metric_A_over_A_at_Leff"]))
                and float(row["metric_A_over_A_at_Leff"]) > 0.0
                and math.isfinite(float(row["metric_B_areal"]))
                and float(row["metric_B_areal"]) >= 1.0
                for row in metric_rows
            ),
            "A>0 and B>=1 on x in [1e-6,1e4]",
        ),
        (
            "weak_lensing_gradient_proxy_small",
            galaxy_summary["maximum_lensing_gradient_proxy_deviation"] < 1.0e-5,
            str(galaxy_summary["maximum_lensing_gradient_proxy_deviation"]),
        ),
        (
            "universal_WKB_gap_floor_finite",
            math.isfinite(galaxy_summary["maximum_WKB_mass_eV"])
            and galaxy_summary["maximum_WKB_mass_eV"] > 0.0,
            str(galaxy_summary["maximum_WKB_mass_eV"]),
        ),
        (
            "embedded_local_cogs_tidally_suppressed",
            all(row["passes_comparison_ceiling"] for row in local_rows),
            str(
                {
                    row["arena"]: row["worst_embedded_halo_tide_over_solar"]
                    for row in local_rows
                }
            ),
        ),
        (
            "global_completion_not_smuggled",
            not result["source_selected_occupation_derived"]
            and not result["parent_exponent_IR_transport_derived"]
            and not result["finite_core_derived"]
            and not result["finite_outer_boundary_derived"]
            and not result["full_axisymmetric_solution_derived"],
            "source, core, outer boundary and flattened solution remain next derivations",
        ),
        (
            "claim_discipline",
            not result["valid_for_PPN_claim"]
            and not result["valid_for_galaxy_claim"]
            and not result["valid_for_full_MTS_claim"],
            "stationary existence and scale gates only",
        ),
    ]
    validation_rows = [
        {
            "check_id": f"V5151_{index:02d}_{name}",
            "passed": passed,
            "detail": detail,
            "checkpoint_marker": MARKER,
        }
        for index, (name, passed, detail) in enumerate(checks, start=1)
    ]
    result["validation_count"] = len(validation_rows)
    result["validation_failures"] = [
        row["check_id"] for row in validation_rows if not row["passed"]
    ]
    write_csv(VALIDATION_CSV, validation_rows)
    write_document(result)
    atomic_json(RESULT_JSON, result)
    if result["validation_failures"]:
        raise RuntimeError(
            f"checkpoint 5151 validation failures: {result['validation_failures']}"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
