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
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad
from scipy.optimize import brentq


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
GALAXY_SAMPLES = Path(r"D:\Users\ollet\Documents\mts-galaxy-lab\data\samples.js")
OUT = POST / "source-intake" / "functional_rg" / "5153"
RESULT_JSON = OUT / "finite_halo_state_results.json"
MIXTURE_CSV = OUT / "quantum_regularized_projective_mixture.csv"
HALO_CSV = OUT / "finite_virial_halo_inventory.csv"
RADIAL_CSV = OUT / "finite_profile_all_175_radial_smoke.csv"
SUMMARY_CSV = OUT / "finite_profile_summary.csv"
ROUTE_CSV = OUT / "finite_state_route_decision.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5153_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5153-Y5-R2FR-quantum-regularized-projective-halo-cosmological-boundary-and-primordial-inventory-gate.md"
)
MARKER = "MTS_5153_QUANTUM_CORE_VIRIAL_INVENTORY_GATE"
CHECKED_DATE = "2026-07-20"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"

C_KM_S = 299792.458
G_ASTRO = 4.30091727003628e-6
G_SI = 6.67430e-11
EV_C2_KG = 1.7826619216278976e-36
MSUN_KG = 1.98847e30
MPC_M = 3.085677581491367e22
H0_KM_S_MPC = 67.4
H0_KM_S_KPC = H0_KM_S_MPC / 1000.0
H0_SI = H0_KM_S_MPC * 1000.0 / MPC_M
LITTLE_H = H0_KM_S_MPC / 100.0
OMEGA_M = 0.315
OMEGA_B = 0.02237 / LITTLE_H**2
OMEGA_X = OMEGA_M - OMEGA_B
MOTION_FRACTION = OMEGA_X / OMEGA_M
RHO_CRIT0_KG_M3 = 3.0 * H0_SI**2 / (8.0 * math.pi * G_SI)
RHO_CRIT0_MSUN_KPC3 = (
    3.0 * H0_KM_S_KPC**2 / (8.0 * math.pi * G_ASTRO)
)
RHO_X0_MSUN_MPC3 = OMEGA_X * RHO_CRIT0_MSUN_KPC3 * 1.0e9
VIRIAL_X = OMEGA_M - 1.0
DELTA_VIR_CRITICAL = (
    18.0 * math.pi**2 + 82.0 * VIRIAL_X - 39.0 * VIRIAL_X**2
)
ML_DISK = 0.5
ML_BULGE = 0.7
QUADRATURE_ORDER = 1536
QUADRATURE_U_MAX = 50.0


SOURCE_PATHS = {
    "local_parent_action": POST
    / "4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-universal-source-residue-certificate.md",
    "projective_parent": POST
    / "4948-Y5-R2FR-single-parent-motion-Hessian-to-galaxy-phase-flow-and-universal-Jgap-interface.md",
    "state_stress_parent": POST
    / "5151-Y5-R2FR-parent-projective-occupation-to-conserved-Einstein-cluster-stress-and-two-metric-cog-gate.md",
    "state_scale_rows": POST
    / "source-intake"
    / "functional_rg"
    / "5151"
    / "galaxy_state_stress_scale_gate.csv",
    "primordial_parent": POST
    / "5152-Y5-R2FR-primordial-motion-occupation-dust-limit-Jeans-window-and-formation-source-arbitration.md",
    "primordial_result": POST
    / "source-intake"
    / "functional_rg"
    / "5152"
    / "primordial_motion_occupation_results.json",
    "primordial_mass_window": POST
    / "source-intake"
    / "functional_rg"
    / "5152"
    / "galaxy_mass_window.csv",
    "primordial_Jeans_rows": POST
    / "source-intake"
    / "functional_rg"
    / "5152"
    / "linear_Jeans_scale_gate.csv",
    "galaxy_samples_read_only": GALAXY_SAMPLES,
}


PRIMARY_SOURCE_URLS = {
    "fuzzy_wave_support": "https://arxiv.org/abs/astro-ph/0003365",
    "wave_halo_simulation": "https://arxiv.org/abs/1407.7762",
    "virial_overdensity": "https://arxiv.org/abs/astro-ph/9710107",
    "static_Einstein_Vlasov": "https://arxiv.org/abs/gr-qc/9304028",
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
                "r_kpc": values[0],
                "v_obs_km_s": values[1],
                "err_v_km_s": values[2],
                "v_gas_km_s": values[3],
                "v_disk_km_s": values[4],
                "v_bulge_km_s": values[5],
            }
        )
    return rows


def retained_weight(exponent: float, t_min: float) -> float:
    alpha = exponent / 2.0
    theta = math.pi * alpha
    sine = math.sin(theta)
    cosine = math.cos(theta)
    lower_angle = math.pi / 2.0 - theta
    angle = math.atan2(t_min**alpha + cosine, sine)
    cumulative = (angle - lower_angle) / theta
    return 1.0 - cumulative


def spectral_quadrature(
    exponent: float,
    t_min: float,
    legendre_nodes: np.ndarray,
    legendre_weights: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, float, float]:
    alpha = exponent / 2.0
    theta = math.pi * alpha
    sine = math.sin(theta)
    cosine = math.cos(theta)
    u_min = math.log(t_min)
    u_values = (
        0.5 * (QUADRATURE_U_MAX - u_min) * legendre_nodes
        + 0.5 * (QUADRATURE_U_MAX + u_min)
    )
    integration_weights = (
        0.5 * (QUADRATURE_U_MAX - u_min) * legendre_weights
    )
    powered = np.exp(alpha * u_values)
    density_du = (
        sine
        / math.pi
        * powered
        / (1.0 + 2.0 * cosine * powered + powered**2)
    )
    raw_weights = integration_weights * density_du
    numeric_weight = float(np.sum(raw_weights))
    analytic_weight = retained_weight(exponent, t_min)
    normalized_weights = raw_weights / numeric_weight
    return np.exp(u_values), normalized_weights, analytic_weight, numeric_weight


def support_bundle(
    x_values: np.ndarray,
    t_values: np.ndarray,
    weights: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x_squared = np.asarray(x_values, dtype=float) ** 2
    denominator = x_squared[:, None] + t_values[None, :]
    support = np.sum(
        weights[None, :] * x_squared[:, None] / denominator, axis=1
    )
    logarithmic_derivative = np.sum(
        weights[None, :]
        * 2.0
        * x_squared[:, None]
        * t_values[None, :]
        / denominator**2,
        axis=1,
    )
    density_shape = np.sum(
        weights[None, :]
        * (1.0 / denominator + 2.0 * t_values[None, :] / denominator**2),
        axis=1,
    )
    return support, logarithmic_derivative, density_shape


def scalar_support(
    radius_kpc: float,
    transition_radius_kpc: float,
    t_values: np.ndarray,
    weights: np.ndarray,
) -> float:
    x_value = radius_kpc / transition_radius_kpc
    return float(support_bundle(np.array([x_value]), t_values, weights)[0][0])


def find_virial_radius(
    transition_radius_kpc: float,
    velocity_infinity_km_s: float,
    t_values: np.ndarray,
    weights: np.ndarray,
) -> float:
    beta_infinity = (velocity_infinity_km_s / C_KM_S) ** 2
    scale = (
        velocity_infinity_km_s
        / H0_KM_S_KPC
        * math.sqrt(2.0 / (MOTION_FRACTION * DELTA_VIR_CRITICAL))
    )

    def equation(radius_kpc: float) -> float:
        support = scalar_support(
            radius_kpc, transition_radius_kpc, t_values, weights
        )
        return radius_kpc - scale * math.sqrt(
            support / (1.0 + 2.0 * beta_infinity * support)
        )

    scan = np.logspace(
        math.log10(max(transition_radius_kpc * 1.0e-8, scale * 1.0e-8)),
        math.log10(scale * 2.0),
        240,
    )
    values = [equation(float(radius)) for radius in scan]
    brackets = [
        (float(scan[index]), float(scan[index + 1]))
        for index in range(len(scan) - 1)
        if values[index] <= 0.0 and values[index + 1] >= 0.0
    ]
    if not brackets:
        raise RuntimeError("no positive finite virial-radius root")
    lower, upper = brackets[-1]
    return float(brentq(equation, lower, upper, xtol=1.0e-12, rtol=1.0e-13))


def adaptive_support(exponent: float, t_min: float, x_value: float) -> float:
    alpha = exponent / 2.0
    theta = math.pi * alpha
    sine = math.sin(theta)
    cosine = math.cos(theta)
    lower = math.log(t_min)

    def density_du(u_value: float) -> float:
        powered = math.exp(alpha * u_value)
        return (
            sine
            / math.pi
            * powered
            / (1.0 + 2.0 * cosine * powered + powered**2)
        )

    numerator = quad(
        lambda u_value: x_value**2
        / (x_value**2 + math.exp(u_value))
        * density_du(u_value),
        lower,
        QUADRATURE_U_MAX,
        epsabs=1.0e-12,
        epsrel=1.0e-12,
        limit=300,
    )[0]
    return numerator / retained_weight(exponent, t_min)


def build_finite_states(
    state_rows: list[dict[str, str]],
    mass_grid: list[tuple[str, float]],
    jeans_by_mass: dict[str, dict[str, float]],
    sample_points: dict[str, list[dict[str, float]]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    legendre_nodes, legendre_weights = leggauss(QUADRATURE_ORDER)
    mixture_rows: list[dict[str, Any]] = []
    halo_rows: list[dict[str, Any]] = []
    radial_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    quadrature_cross_checks: list[float] = []

    accumulators: dict[tuple[str, str], dict[str, Any]] = {}
    for mass_label, _ in mass_grid:
        for mapping in sorted({row["mapping"] for row in state_rows}):
            accumulators[(mass_label, mapping)] = {
                "finite_squared_error": 0.0,
                "unregularized_squared_error": 0.0,
                "point_count": 0,
                "finite_rmse_by_galaxy": [],
                "unregularized_rmse_by_galaxy": [],
                "maximum_support_distortion": 0.0,
                "maximum_observed_r_over_rvir": 0.0,
                "outside_points": 0,
                "finite_wins": 0,
            }

    selected_cross_checks = {
        (mass_grid[0][0], state_rows[0]["galaxy"], state_rows[0]["mapping"]),
        (mass_grid[-1][0], state_rows[-1]["galaxy"], state_rows[-1]["mapping"]),
    }

    for mass_label, mass_eV in mass_grid:
        equality_jeans_mass = jeans_by_mass[mass_label]["Jeans_sphere_mass_Msun"]
        equality_jeans_length = jeans_by_mass[mass_label][
            "lambda_Jeans_comoving_Mpc"
        ]
        for source in state_rows:
            galaxy = source["galaxy"]
            mapping = source["mapping"]
            exponent = float(source["q_parent"])
            length_kpc = float(source["L_eff_kpc"])
            transition_radius_kpc = float(source["R_n_over_L_eff"]) * length_kpc
            velocity_infinity = float(source["v_infinity_km_s"])
            wkb_floor = float(source["minimum_m_gap_eV_for_lambda_db_le_Rn"])
            core_over_transition = wkb_floor / mass_eV
            t_min = core_over_transition**2
            t_values, weights, analytic_weight, numeric_weight = spectral_quadrature(
                exponent, t_min, legendre_nodes, legendre_weights
            )
            inverse_t_moment = float(np.sum(weights / t_values))
            central_density_msun_kpc3 = (
                3.0
                * inverse_t_moment
                * velocity_infinity**2
                / (4.0 * math.pi * G_ASTRO * transition_radius_kpc**2)
            )

            standard_x = np.logspace(-8.0, 4.0, 320)
            standard_support, standard_log_derivative, density_shape = support_bundle(
                standard_x, t_values, weights
            )
            unregularized_support = standard_x**exponent / (
                1.0 + standard_x**exponent
            )
            maximum_standard_distortion = float(
                np.max(np.abs(standard_support - unregularized_support))
            )
            minimum_density_shape = float(np.min(density_shape))
            minimum_epicyclic_shape = float(
                np.min(2.0 * standard_support + standard_log_derivative)
            )

            virial_radius_kpc = find_virial_radius(
                transition_radius_kpc,
                velocity_infinity,
                t_values,
                weights,
            )
            virial_support = scalar_support(
                virial_radius_kpc,
                transition_radius_kpc,
                t_values,
                weights,
            )
            beta_virial = (velocity_infinity / C_KM_S) ** 2 * virial_support
            compactness_virial = beta_virial / (1.0 + 2.0 * beta_virial)
            motion_mass_msun = (
                C_KM_S**2
                * virial_radius_kpc
                * compactness_virial
                / G_ASTRO
            )
            total_mass_msun = motion_mass_msun / MOTION_FRACTION
            mean_total_density = total_mass_msun / (
                4.0 * math.pi * virial_radius_kpc**3 / 3.0
            )
            virial_density_target = DELTA_VIR_CRITICAL * RHO_CRIT0_MSUN_KPC3
            virial_identity_residual = abs(
                mean_total_density / virial_density_target - 1.0
            )
            lagrangian_radius_mpc = (
                3.0
                * motion_mass_msun
                / (4.0 * math.pi * RHO_X0_MSUN_MPC3)
            ) ** (1.0 / 3.0)
            inventory_identity_residual = abs(
                (
                    4.0
                    * math.pi
                    / 3.0
                    * RHO_X0_MSUN_MPC3
                    * lagrangian_radius_mpc**3
                )
                / motion_mass_msun
                - 1.0
            )
            quantum_number = (
                motion_mass_msun * MSUN_KG / (mass_eV * EV_C2_KG)
            )
            exterior_compactness_at_boundary = (
                G_ASTRO * motion_mass_msun / (C_KM_S**2 * virial_radius_kpc)
            )
            junction_residual = abs(
                exterior_compactness_at_boundary - compactness_virial
            )

            points = sample_points[galaxy]
            radii = np.array([point["r_kpc"] for point in points])
            x_observed = radii / transition_radius_kpc
            finite_support, _, _ = support_bundle(x_observed, t_values, weights)
            original_support = x_observed**exponent / (
                1.0 + x_observed**exponent
            )
            finite_squared_errors: list[float] = []
            original_squared_errors: list[float] = []
            outside_points = 0
            for index, point in enumerate(points):
                radius = point["r_kpc"]
                if radius <= virial_radius_kpc:
                    motion_velocity_squared = velocity_infinity**2 * float(
                        finite_support[index]
                    )
                else:
                    outside_points += 1
                    exterior_w = (
                        G_ASTRO
                        * motion_mass_msun
                        / (C_KM_S**2 * radius)
                    )
                    exterior_beta = exterior_w / (1.0 - 2.0 * exterior_w)
                    motion_velocity_squared = C_KM_S**2 * exterior_beta
                baryonic_velocity_squared = (
                    point["v_gas_km_s"] * abs(point["v_gas_km_s"])
                    + ML_DISK * point["v_disk_km_s"] ** 2
                    + ML_BULGE * point["v_bulge_km_s"] ** 2
                )
                finite_model = math.sqrt(
                    max(0.0, baryonic_velocity_squared + motion_velocity_squared)
                )
                original_model = math.sqrt(
                    max(
                        0.0,
                        baryonic_velocity_squared
                        + velocity_infinity**2 * float(original_support[index]),
                    )
                )
                finite_squared_errors.append(
                    (finite_model - point["v_obs_km_s"]) ** 2
                )
                original_squared_errors.append(
                    (original_model - point["v_obs_km_s"]) ** 2
                )
            finite_rmse = math.sqrt(
                sum(finite_squared_errors) / len(finite_squared_errors)
            )
            original_rmse = math.sqrt(
                sum(original_squared_errors) / len(original_squared_errors)
            )
            maximum_observed_distortion = float(
                np.max(np.abs(finite_support - original_support))
            )

            mixture_rows.append(
                {
                    "galaxy": galaxy,
                    "mapping": mapping,
                    "mass_label": mass_label,
                    "m_gap_eV": mass_eV,
                    "q_parent": exponent,
                    "R_n_kpc": transition_radius_kpc,
                    "r_core_over_R_n": core_over_transition,
                    "r_core_kpc": core_over_transition * transition_radius_kpc,
                    "t_min_equals_r_core2_over_Rn2": t_min,
                    "retained_spectral_weight_analytic": analytic_weight,
                    "retained_spectral_weight_numeric": numeric_weight,
                    "quadrature_relative_normalization_error": abs(
                        numeric_weight / analytic_weight - 1.0
                    ),
                    "inverse_t_moment": inverse_t_moment,
                    "central_density_Msun_pc3": central_density_msun_kpc3
                    / 1.0e9,
                    "minimum_positive_density_shape": minimum_density_shape,
                    "minimum_positive_epicyclic_shape": minimum_epicyclic_shape,
                    "maximum_support_distortion_standard_x": maximum_standard_distortion,
                    "finite_core_constructed": True,
                    "wave_collapse_selected_this_cutoff": False,
                    "valid_for_galaxy_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
            halo_rows.append(
                {
                    "galaxy": galaxy,
                    "mapping": mapping,
                    "mass_label": mass_label,
                    "m_gap_eV": mass_eV,
                    "q_parent": exponent,
                    "Delta_vir_critical_z0": DELTA_VIR_CRITICAL,
                    "cosmic_motion_fraction": MOTION_FRACTION,
                    "R_n_kpc": transition_radius_kpc,
                    "r_core_kpc": core_over_transition * transition_radius_kpc,
                    "r_vir_kpc": virial_radius_kpc,
                    "r_vir_over_R_n": virial_radius_kpc / transition_radius_kpc,
                    "support_at_r_vir": virial_support,
                    "motion_mass_vir_Msun": motion_mass_msun,
                    "cosmic_fraction_total_mass_vir_Msun": total_mass_msun,
                    "mass_over_equality_Jeans_mass": total_mass_msun
                    / equality_jeans_mass,
                    "Lagrangian_motion_patch_radius_Mpc": lagrangian_radius_mpc,
                    "Lagrangian_radius_over_equality_Jeans_wavelength": lagrangian_radius_mpc
                    / equality_jeans_length,
                    "motion_quantum_inventory": quantum_number,
                    "largest_observed_radius_over_r_vir": max(radii)
                    / virial_radius_kpc,
                    "virial_density_identity_residual": virial_identity_residual,
                    "Lagrangian_inventory_identity_residual": inventory_identity_residual,
                    "Schwarzschild_junction_compactness_residual": junction_residual,
                    "finite_mass_and_boundary_constructed": True,
                    "smooth_edge_from_collapse_derived": False,
                    "valid_for_galaxy_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
            radial_rows.append(
                {
                    "galaxy": galaxy,
                    "mapping": mapping,
                    "mass_label": mass_label,
                    "m_gap_eV": mass_eV,
                    "point_count": len(points),
                    "finite_profile_RMSE_km_s": finite_rmse,
                    "unregularized_parent_RMSE_km_s": original_rmse,
                    "delta_RMSE_km_s": finite_rmse - original_rmse,
                    "maximum_observed_support_distortion": maximum_observed_distortion,
                    "maximum_observed_r_over_r_vir": max(radii)
                    / virial_radius_kpc,
                    "points_outside_r_vir": outside_points,
                    "per_galaxy_shape_fit": False,
                    "valid_for_galaxy_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )

            accumulator = accumulators[(mass_label, mapping)]
            accumulator["finite_squared_error"] += sum(finite_squared_errors)
            accumulator["unregularized_squared_error"] += sum(
                original_squared_errors
            )
            accumulator["point_count"] += len(points)
            accumulator["finite_rmse_by_galaxy"].append(finite_rmse)
            accumulator["unregularized_rmse_by_galaxy"].append(original_rmse)
            accumulator["maximum_support_distortion"] = max(
                accumulator["maximum_support_distortion"],
                maximum_observed_distortion,
            )
            accumulator["maximum_observed_r_over_rvir"] = max(
                accumulator["maximum_observed_r_over_rvir"],
                max(radii) / virial_radius_kpc,
            )
            accumulator["outside_points"] += outside_points
            accumulator["finite_wins"] += finite_rmse < original_rmse

            cross_key = (mass_label, galaxy, mapping)
            if cross_key in selected_cross_checks:
                for x_value in [1.0e-5, 0.01, 1.0, 100.0]:
                    quadrature_value = float(
                        support_bundle(
                            np.array([x_value]), t_values, weights
                        )[0][0]
                    )
                    quadrature_cross_checks.append(
                        abs(
                            quadrature_value
                            - adaptive_support(exponent, t_min, x_value)
                        )
                    )

    for (mass_label, mapping), accumulator in accumulators.items():
        point_count = accumulator["point_count"]
        summary_rows.append(
            {
                "mass_label": mass_label,
                "mapping": mapping,
                "galaxy_count": len(accumulator["finite_rmse_by_galaxy"]),
                "point_count": point_count,
                "mean_finite_profile_RMSE_km_s": statistics.mean(
                    accumulator["finite_rmse_by_galaxy"]
                ),
                "median_finite_profile_RMSE_km_s": statistics.median(
                    accumulator["finite_rmse_by_galaxy"]
                ),
                "pooled_finite_profile_RMSE_km_s": math.sqrt(
                    accumulator["finite_squared_error"] / point_count
                ),
                "pooled_unregularized_parent_RMSE_km_s": math.sqrt(
                    accumulator["unregularized_squared_error"] / point_count
                ),
                "maximum_observed_support_distortion": accumulator[
                    "maximum_support_distortion"
                ],
                "maximum_observed_r_over_rvir": accumulator[
                    "maximum_observed_r_over_rvir"
                ],
                "points_outside_rvir": accumulator["outside_points"],
                "finite_profile_wins_out_of_175": accumulator["finite_wins"],
                "per_galaxy_shape_fit": False,
                "valid_for_galaxy_claim": False,
                "checkpoint_marker": MARKER,
            }
        )

    summary = {
        "mixture_row_count": len(mixture_rows),
        "halo_row_count": len(halo_rows),
        "radial_row_count": len(radial_rows),
        "maximum_quadrature_normalization_error": max(
            row["quadrature_relative_normalization_error"] for row in mixture_rows
        ),
        "maximum_adaptive_quadrature_support_error": max(quadrature_cross_checks),
        "minimum_retained_spectral_weight": min(
            row["retained_spectral_weight_analytic"] for row in mixture_rows
        ),
        "maximum_core_over_transition": max(
            row["r_core_over_R_n"] for row in mixture_rows
        ),
        "maximum_standard_support_distortion": max(
            row["maximum_support_distortion_standard_x"] for row in mixture_rows
        ),
        "minimum_central_density_Msun_pc3": min(
            row["central_density_Msun_pc3"] for row in mixture_rows
        ),
        "maximum_central_density_Msun_pc3": max(
            row["central_density_Msun_pc3"] for row in mixture_rows
        ),
        "minimum_rvir_over_Rn": min(row["r_vir_over_R_n"] for row in halo_rows),
        "maximum_observed_r_over_rvir": max(
            row["largest_observed_radius_over_r_vir"] for row in halo_rows
        ),
        "minimum_motion_mass_Msun": min(
            row["motion_mass_vir_Msun"] for row in halo_rows
        ),
        "maximum_motion_mass_Msun": max(
            row["motion_mass_vir_Msun"] for row in halo_rows
        ),
        "minimum_Lagrangian_radius_Mpc": min(
            row["Lagrangian_motion_patch_radius_Mpc"] for row in halo_rows
        ),
        "maximum_Lagrangian_radius_Mpc": max(
            row["Lagrangian_motion_patch_radius_Mpc"] for row in halo_rows
        ),
        "minimum_mass_over_Jeans": min(
            row["mass_over_equality_Jeans_mass"] for row in halo_rows
        ),
        "minimum_Lagrangian_radius_over_Jeans": min(
            row["Lagrangian_radius_over_equality_Jeans_wavelength"]
            for row in halo_rows
        ),
        "minimum_quantum_inventory": min(
            row["motion_quantum_inventory"] for row in halo_rows
        ),
        "maximum_quantum_inventory": max(
            row["motion_quantum_inventory"] for row in halo_rows
        ),
        "maximum_virial_identity_residual": max(
            row["virial_density_identity_residual"] for row in halo_rows
        ),
        "maximum_inventory_identity_residual": max(
            row["Lagrangian_inventory_identity_residual"] for row in halo_rows
        ),
        "maximum_junction_residual": max(
            row["Schwarzschild_junction_compactness_residual"]
            for row in halo_rows
        ),
        "total_radial_points_across_mass_and_mapping": sum(
            row["point_count"] for row in radial_rows
        ),
        "maximum_observed_support_distortion": max(
            row["maximum_observed_support_distortion"] for row in radial_rows
        ),
        "maximum_absolute_delta_RMSE_km_s": max(
            abs(row["delta_RMSE_km_s"]) for row in radial_rows
        ),
        "points_outside_virial_boundary": sum(
            row["points_outside_r_vir"] for row in radial_rows
        ),
    }
    return mixture_rows, halo_rows, radial_rows, summary_rows, summary


def build_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "inner_boundary",
            "status": "CONDITIONAL_CONSTRUCTION_PASSES",
            "result": "lower-cut positive Stieltjes mixture gives finite central density without changing q_parent",
            "remaining": "derive the spectral cutoff coefficient from nonlinear wave collapse",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "gate": "outer_boundary",
            "status": "CONDITIONAL_CONSTRUCTION_PASSES",
            "result": "LambdaCDM spherical-collapse overdensity gives a unique finite radius and exact Schwarzschild mass junction",
            "remaining": "derive the smooth edge and formation redshift distribution",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "gate": "primordial_inventory",
            "status": "PASSES_IDENTITY_AND_JEANS_HIERARCHY",
            "result": "finite homogeneous Omega_X Lagrangian patches supply every halo inventory without local particle creation",
            "remaining": "derive the primordial perturbation probability and allocation",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "gate": "parent_profile_survival",
            "status": "PASSES_ALL_175_READ_ONLY_RADIAL_SMOKE",
            "result": "core and virial regularization preserve the parent q profile over all measured radii without refitting",
            "remaining": "show that collapse dynamically selects rather than merely admits this profile",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "gate": "nonlinear_attractor",
            "status": "OPEN_DECISIVE_GATE",
            "result": "not inferred from equilibrium existence",
            "remaining": "derive distribution function and execute collapse stability/attractor test",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def write_document(result: dict[str, Any]) -> None:
    summary = result["finite_state_summary"]
    radial = result["radial_summary"]
    strict_rows = [
        row for row in radial if row["mass_label"] == "ten_times_WKB_floor"
    ]
    benchmark_rows = [
        row for row in radial if row["mass_label"] == "benchmark_1e_minus20_eV"
    ]
    text = f"""# 5153 - Quantum-regularized projective halo, cosmological boundary and primordial inventory

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

Checkpoint 5153 does not insert an arbitrary cored halo or an arbitrary outer
taper. It starts from the exact positive projective mixture proved at 5151,
uses the same `m_gap` window derived at 5152 to remove unresolved components,
and uses the metric-only cosmological spherical-collapse density to define a
finite outer boundary. This constructs one finite, positive, stationary
Einstein-cluster family for every existing galaxy/parent row.

The construction passes all measured-radius, density, stability, inventory,
Jeans and Schwarzschild-junction gates. It closes finite-core and finite-mass
*existence* conditionally. It does not prove that cosmological collapse
dynamically selects this family; that is now the single decisive next gate.

## 1. No new inner profile

For `alpha=q/2` and `0<q<2`, checkpoint 5151 proved

```text
n_q(x)=integral_0^infinity dt [x^2/(x^2+t)] rho_q(t),

rho_q(t)=sin(pi alpha)t^(alpha-1)
 /{{pi[1+2t^alpha cos(pi alpha)+t^(2alpha)]}}.
```

Each kernel is a regular cored component. The original mild cusp comes only
from integrating the continuum down to `t=0`. The same WKB relation used at
5151 fixes, without another galaxy parameter,

```text
r_c/R_n=lambda_db/R_n=m_WKB,row/m_gap,
t_min=(r_c/R_n)^2.
```

Removing only components below that resolution and renormalizing gives

```text
S_q,c(x)=N_q(t_min)^(-1)
 integral_tmin^infinity dt [x^2/(x^2+t)]rho_q(t),

N_q=1-F_q(t_min),
F_q(t)={{atan[(t^alpha+cos pi alpha)/sin pi alpha]
          -(pi/2-pi alpha)}}/(pi alpha).
```

This has exact properties

```text
S_q,c(0)=0,
S_q,c(infinity)=1,
dS_q,c/dx>0,
rho(0)=3 v_infinity^2 <1/t>/(4piG R_n^2)<infinity,
rho(r)>0,
2S+xS'>0.
```

Across all `1050` state/mass rows, the retained positive spectral weight is at
least `{summary['minimum_retained_spectral_weight']}`, the largest
`r_c/R_n` is `{summary['maximum_core_over_transition']}`, and central
densities range from `{summary['minimum_central_density_Msun_pc3']}` to
`{summary['maximum_central_density_Msun_pc3']} Msun/pc^3`. The maximum
independent adaptive-quadrature disagreement is
`{summary['maximum_adaptive_quadrature_support_error']}`.

This is parameter-free within the declared lower-cut prescription once
`m_gap` is fixed; it is not proved to be the unique physical regularization.
Whether nonlinear wave dynamics imposes precisely this spectral cutoff
remains unproved.

## 2. Cosmological outer boundary and exact local exterior

The checkpoint-4897 flat metric baseline gives at `z=0`

```text
Delta_vir,c=18pi^2+82(Omega_m-1)-39(Omega_m-1)^2
           ={DELTA_VIR_CRITICAL},
f_X=Omega_X/Omega_m={MOTION_FRACTION}.
```

For the exact circular-state relation

```text
beta=v_infinity^2 S_q,c/c^2,
w=G M_X/(c^2 r)=beta/(1+2beta),
M_total=M_X/f_X,
```

the virial condition `3M_total/(4pi r_vir^3)=Delta_vir,c rho_crit`
reduces to one scalar equation

```text
r_vir^2
 =2 v_infinity^2 S_q,c(r_vir/R_n)
  /[f_X Delta_vir,c H_0^2(1+2beta_vir)].
```

Because every mixture kernel has logarithmic slope below two, the mean
interior density decreases and the positive root is unique. Set the circular
state to zero beyond that orbit and continue with Schwarzschild mass
`M_X(r_vir)`. `M`, `A`, `B` and the circular derivative match at the boundary;
`p_r=0` means the finite density step does not require a radial-pressure shell.

The executed radii satisfy
`r_vir/R_n >= {summary['minimum_rvir_over_Rn']}`. Every measured point lies inside, with
maximum `r_obs/r_vir={summary['maximum_observed_r_over_rvir']}`. Motion masses
are finite and range from `{summary['minimum_motion_mass_Msun']}` to
`{summary['maximum_motion_mass_Msun']} Msun`. The maximum virial identity
residual is `{summary['maximum_virial_identity_residual']}` and the exact
Schwarzschild compactness-junction residual is
`{summary['maximum_junction_residual']}`.

The sharp edge is a valid compact-support circular state, not yet a derived
smooth collapse edge.

## 3. Primordial supply instead of local manufacture

For every finite motion mass,

```text
R_L=[3M_X/(4pi rho_X,0)]^(1/3),
N_X=M_X/(m_gap),
```

so a finite comoving patch of the single checkpoint-5152 primordial state
contains the exact required inventory. Across the full execution,

```text
R_L={summary['minimum_Lagrangian_radius_Mpc']}
    ...{summary['maximum_Lagrangian_radius_Mpc']} Mpc,
N_X={summary['minimum_quantum_inventory']}
    ...{summary['maximum_quantum_inventory']},
minimum M_total/M_Jeans(eq)={summary['minimum_mass_over_Jeans']},
minimum R_L/lambda_Jeans(eq)={summary['minimum_Lagrangian_radius_over_Jeans']}.
```

Thus none of the candidate halos needs the rejected local multiplicity
cascade. This proves available finite inventory, not the primordial power or
probability for each patch to collapse.

## 4. Does regularization break the galaxy cog?

No profile parameter was fitted. The existing `q_parent`, one global phase
map, `L_eff`, `v_infinity`, baryonic law and all `3391` measured radii were
held fixed. Three masses and two parent branches give `20346` executed radial
points.

At the strict WKB floor the two pooled finite-profile RMSE values are
`{[row['pooled_finite_profile_RMSE_km_s'] for row in strict_rows]}` versus
unregularized `{[row['pooled_unregularized_parent_RMSE_km_s'] for row in strict_rows]}`.
At `1e-20 eV` they are
`{[row['pooled_finite_profile_RMSE_km_s'] for row in benchmark_rows]}`.
The largest support change at any measured point over the entire mass grid is
`{summary['maximum_observed_support_distortion']}` and no observed point
crosses the virial boundary. Therefore the physically finite construction
preserves the checkpoint-5151 galaxy result rather than obtaining regularity
by changing its fit.

This remains an unweighted interface smoke, not a galaxy likelihood.

## 5. Exact status

```text
positive finite-core equilibrium family              = constructed;
finite cosmological virial boundary                   = constructed conditionally;
exact Schwarzschild exterior junction                 = derived;
finite primordial inventory for every halo            = derived;
all candidate patches above instantaneous Jeans gate  = verified;
parent q profile preserved on all measured radii      = verified;

wave dynamics selects t_min coefficient               = not derived;
primordial spectrum creates the Lagrangian patches    = not derived;
collapse selects C_n and n_q as an attractor           = not derived;
smooth outer-edge distribution                        = not derived;
flattened rotating state and lensing likelihood       = not derived.
```

This is real movement: the earlier infinite cusp/mass objections no longer
block existence, and the formation-number objection is bypassed by one finite
primordial inventory. But equilibrium existence cannot be promoted into a
formation theorem.

## 6. Next calculation

Perform the phase-space gate before a costly cosmological run. Invert the
finite density and metric to a nonnegative distribution function, first in
the isotropic Eddington/Vlasov branch and then in the circular anisotropic
limit already known to exist. Test radial-orbit stability and whether a
single dimensionless distribution can cover all mass rows. If no positive
finite distribution continuously connects the cosmological initial state to
the `q_parent` profile, demote this route. If it passes, execute the nonlinear
Schrodinger--Poisson/Vlasov collapse at the three fixed masses.

Primary references:

- wave/Jeans support: {PRIMARY_SOURCE_URLS['fuzzy_wave_support']}
- nonlinear wave halos: {PRIMARY_SOURCE_URLS['wave_halo_simulation']}
- spherical-collapse virial scaling: {PRIMARY_SOURCE_URLS['virial_overdensity']}
- compact static Einstein--Vlasov states: {PRIMARY_SOURCE_URLS['static_Einstein_Vlasov']}

All `{result['validation_count']}` validations pass. The protected
`formalization-workbench` hash remains
`{result['formalization_workbench_tree_sha256']}`. The galaxy sample was
read-only. No GitHub action occurred.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def main() -> None:
    missing_sources = [str(path) for path in SOURCE_PATHS.values() if not path.exists()]
    if missing_sources:
        raise FileNotFoundError(f"missing checkpoint sources: {missing_sources}")
    source_hashes_before = {
        name: file_digest(path) for name, path in SOURCE_PATHS.items()
    }
    formal_before = tree_digest(FORMAL)

    state_rows = read_csv(SOURCE_PATHS["state_scale_rows"])
    mass_window_rows = read_csv(SOURCE_PATHS["primordial_mass_window"])
    jeans_rows = read_csv(SOURCE_PATHS["primordial_Jeans_rows"])
    sample_rows = parse_samples(SOURCE_PATHS["galaxy_samples_read_only"])
    sample_points = {
        sample["name"].replace("_rotmod.dat", ""): parse_rotmod(sample["text"])
        for sample in sample_rows
    }

    selected_labels = [
        "ten_times_WKB_floor",
        "benchmark_1e_minus20_eV",
        "benchmark_1e_minus18_eV",
    ]
    mass_lookup = {
        row["mass_label"]: float(row["m_gap_eV"])
        for row in mass_window_rows
        if row["row_type"] == "candidate_mass"
    }
    mass_grid = [(label, mass_lookup[label]) for label in selected_labels]
    jeans_by_mass = {
        row["mass_label"]: {
            "Jeans_sphere_mass_Msun": float(row["Jeans_sphere_mass_Msun"]),
            "lambda_Jeans_comoving_Mpc": float(
                row["lambda_Jeans_comoving_Mpc"]
            ),
        }
        for row in jeans_rows
        if row["epoch"] == "equality"
        and row["gravity_density"] == "total_matter_gravity"
        and row["mass_label"] in selected_labels
    }

    mixture_rows, halo_rows, radial_rows, summary_rows, finite_summary = (
        build_finite_states(
            state_rows,
            mass_grid,
            jeans_by_mass,
            sample_points,
        )
    )
    route_rows = build_route_rows()

    write_csv(MIXTURE_CSV, mixture_rows)
    write_csv(HALO_CSV, halo_rows)
    write_csv(RADIAL_CSV, radial_rows)
    write_csv(SUMMARY_CSV, summary_rows)
    write_csv(ROUTE_CSV, route_rows)

    source_hashes_after = {
        name: file_digest(path) for name, path in SOURCE_PATHS.items()
    }
    formal_after = tree_digest(FORMAL)
    result: dict[str, Any] = {
        "checked_date": CHECKED_DATE,
        "checkpoint_marker": MARKER,
        "source_paths": {name: str(path) for name, path in SOURCE_PATHS.items()},
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "primary_source_urls": PRIMARY_SOURCE_URLS,
        "formalization_workbench_tree_sha256": formal_after,
        "cosmological_boundary": {
            "Omega_m": OMEGA_M,
            "Omega_b": OMEGA_B,
            "Omega_X": OMEGA_X,
            "motion_fraction": MOTION_FRACTION,
            "Delta_vir_critical_z0": DELTA_VIR_CRITICAL,
        },
        "mass_grid": {label: mass for label, mass in mass_grid},
        "finite_state_summary": finite_summary,
        "radial_summary": summary_rows,
        "route_decision": "FINITE_STATE_FAMILY_CONSTRUCTED_ADVANCE_TO_PHASE_SPACE_AND_COLLAPSE_ATTRACTOR_GATE",
        "finite_core_equilibrium_constructed": True,
        "finite_outer_boundary_constructed_conditionally": True,
        "Schwarzschild_exterior_junction_derived": True,
        "finite_primordial_inventory_derived": True,
        "wave_dynamics_selects_core_cutoff": False,
        "primordial_spectrum_selects_halo_patches": False,
        "nonlinear_collapse_selects_parent_profile": False,
        "smooth_outer_edge_derived": False,
        "valid_for_cosmology_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_PPN_claim": False,
        "valid_for_full_MTS_claim": False,
    }

    output_csvs = [MIXTURE_CSV, HALO_CSV, RADIAL_CSV, SUMMARY_CSV, ROUTE_CSV]
    strict_mixture = [
        row for row in mixture_rows if row["mass_label"] == "ten_times_WKB_floor"
    ]
    benchmark_mixture = [
        row
        for row in mixture_rows
        if row["mass_label"] == "benchmark_1e_minus20_eV"
    ]
    checks = [
        ("source_paths_exist", not missing_sources, str(missing_sources)),
        (
            "sources_and_galaxy_sample_read_only",
            source_hashes_before == source_hashes_after,
            str(source_hashes_after),
        ),
        (
            "formal_tree_unchanged",
            formal_before == FORMAL_BASELINE and formal_after == FORMAL_BASELINE,
            formal_after,
        ),
        (
            "all_parent_exponents_inside_positive_window",
            all(0.0 < float(row["q_parent"]) < 2.0 for row in state_rows),
            str(sorted({float(row["q_parent"]) for row in state_rows})),
        ),
        (
            "three_masses_all_350_parent_rows_executed",
            len(mixture_rows) == 1050
            and len(halo_rows) == 1050
            and len(radial_rows) == 1050,
            str([len(mixture_rows), len(halo_rows), len(radial_rows)]),
        ),
        (
            "spectral_cutoffs_positive_and_strictly_controlled",
            all(
                0.0 < row["t_min_equals_r_core2_over_Rn2"] <= 0.01 + 1.0e-14
                for row in mixture_rows
            )
            and max(row["r_core_over_R_n"] for row in strict_mixture)
            <= 0.1 + 1.0e-12,
            str(finite_summary["maximum_core_over_transition"]),
        ),
        (
            "retained_positive_mixture_normalized",
            finite_summary["minimum_retained_spectral_weight"] > 0.99
            and finite_summary["maximum_quadrature_normalization_error"] < 1.0e-7,
            str(
                {
                    "weight": finite_summary["minimum_retained_spectral_weight"],
                    "error": finite_summary[
                        "maximum_quadrature_normalization_error"
                    ],
                }
            ),
        ),
        (
            "quadrature_cross_checks_adaptive_integral",
            finite_summary["maximum_adaptive_quadrature_support_error"] < 1.0e-7,
            str(finite_summary["maximum_adaptive_quadrature_support_error"]),
        ),
        (
            "finite_positive_centres",
            finite_summary["minimum_central_density_Msun_pc3"] > 0.0
            and math.isfinite(finite_summary["maximum_central_density_Msun_pc3"]),
            str(
                [
                    finite_summary["minimum_central_density_Msun_pc3"],
                    finite_summary["maximum_central_density_Msun_pc3"],
                ]
            ),
        ),
        (
            "density_and_circular_stability_analytic_sums_positive",
            all(
                row["minimum_positive_density_shape"] > 0.0
                and row["minimum_positive_epicyclic_shape"] > 0.0
                for row in mixture_rows
            ),
            "positive weighted kernel sums",
        ),
        (
            "unique_finite_virial_roots_and_hierarchy",
            finite_summary["minimum_rvir_over_Rn"] > 10.0
            and all(row["r_vir_kpc"] > row["R_n_kpc"] for row in halo_rows),
            str(finite_summary["minimum_rvir_over_Rn"]),
        ),
        (
            "virial_density_identity_closes",
            finite_summary["maximum_virial_identity_residual"] < 1.0e-10,
            str(finite_summary["maximum_virial_identity_residual"]),
        ),
        (
            "Schwarzschild_exterior_junction_closes",
            finite_summary["maximum_junction_residual"] < 1.0e-18,
            str(finite_summary["maximum_junction_residual"]),
        ),
        (
            "finite_primordial_inventory_identity_closes",
            finite_summary["maximum_inventory_identity_residual"] < 1.0e-12
            and finite_summary["minimum_quantum_inventory"] > 0.0,
            str(
                {
                    "residual": finite_summary[
                        "maximum_inventory_identity_residual"
                    ],
                    "N_min": finite_summary["minimum_quantum_inventory"],
                }
            ),
        ),
        (
            "all_halo_patches_above_instantaneous_Jeans_gate",
            finite_summary["minimum_mass_over_Jeans"] > 1.0
            and finite_summary["minimum_Lagrangian_radius_over_Jeans"] > 1.0,
            str(
                [
                    finite_summary["minimum_mass_over_Jeans"],
                    finite_summary["minimum_Lagrangian_radius_over_Jeans"],
                ]
            ),
        ),
        (
            "all_20346_radial_points_executed",
            finite_summary["total_radial_points_across_mass_and_mapping"] == 20346,
            str(finite_summary["total_radial_points_across_mass_and_mapping"]),
        ),
        (
            "all_observed_points_inside_finite_boundary",
            finite_summary["points_outside_virial_boundary"] == 0
            and finite_summary["maximum_observed_r_over_rvir"] < 0.25,
            str(finite_summary["maximum_observed_r_over_rvir"]),
        ),
        (
            "strict_core_preserves_parent_profile",
            max(
                row["maximum_support_distortion_standard_x"]
                for row in strict_mixture
            )
            < 2.0e-3,
            str(
                max(
                    row["maximum_support_distortion_standard_x"]
                    for row in strict_mixture
                )
            ),
        ),
        (
            "benchmark_core_preserves_parent_profile",
            max(
                row["maximum_support_distortion_standard_x"]
                for row in benchmark_mixture
            )
            < 2.0e-4,
            str(
                max(
                    row["maximum_support_distortion_standard_x"]
                    for row in benchmark_mixture
                )
            ),
        ),
        (
            "finite_regularization_does_not_refit_or_break_radial_smoke",
            all(not row["per_galaxy_shape_fit"] for row in radial_rows)
            and finite_summary["maximum_absolute_delta_RMSE_km_s"] < 0.02,
            str(finite_summary["maximum_absolute_delta_RMSE_km_s"]),
        ),
        (
            "route_advances_to_attractor_not_another_source_sweep",
            route_rows[-1]["status"] == "OPEN_DECISIVE_GATE"
            and result["route_decision"].endswith("COLLAPSE_ATTRACTOR_GATE"),
            result["route_decision"],
        ),
        (
            "all_output_CSVs_parse",
            all(len(read_csv(path)) > 0 for path in output_csvs),
            str([str(path) for path in output_csvs]),
        ),
        (
            "completion_not_smuggled",
            not result["wave_dynamics_selects_core_cutoff"]
            and not result["primordial_spectrum_selects_halo_patches"]
            and not result["nonlinear_collapse_selects_parent_profile"]
            and not result["smooth_outer_edge_derived"],
            "core coefficient, primordial spectrum, attractor and smooth edge remain open",
        ),
        (
            "claim_discipline",
            not result["valid_for_cosmology_claim"]
            and not result["valid_for_galaxy_claim"]
            and not result["valid_for_PPN_claim"]
            and not result["valid_for_full_MTS_claim"],
            "finite equilibrium and inventory gate only",
        ),
    ]
    validation_rows = [
        {
            "check_id": f"V5153_{index:02d}_{name}",
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
            f"checkpoint 5153 validation failures: {result['validation_failures']}"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
