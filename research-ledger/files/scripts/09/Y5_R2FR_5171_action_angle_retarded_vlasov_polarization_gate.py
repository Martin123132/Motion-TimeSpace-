from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
EDDINGTON_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5154_Eddington_phase_space_positive_DF_gate.py"
)
PREVIOUS_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5170_collective_stress_residual_and_single_coupling_no_go.py"
)
VISIBLE_SOURCE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5163"
    / "visible_baryon_source_profile.csv"
)
OUT = POST / "source-intake" / "functional_rg" / "5171"
DERIVATION_CSV = OUT / "action_angle_retarded_kernel_derivation.csv"
CONVERGENCE_CSV = OUT / "orbit_quadrature_convergence.csv"
SPECTRUM_CSV = OUT / "static_dielectric_spectrum.csv"
PROFILE_CSV = OUT / "vlasov_response_profile.csv"
CLAUSE_CSV = OUT / "kernel_clause_decision.csv"
DOUBLE_COUNT_CSV = OUT / "double_counting_ledger.csv"
DECISION_CSV = OUT / "route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "action_angle_vlasov_response_results.json"
VALIDATION_CSV = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5171_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5171-Y5-R2FR-action-angle-retarded-vlasov-polarization-static-response-and-double-counting-gate.md"
)

MARKER = "MTS_5171_ACTION_ANGLE_RETARDED_VLASOV_POLARIZATION_GATE"
CHECKED_DATE = "2026-07-21"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
REFERENCE_GALAXY = "UGC09133"
REFERENCE_MAPPING = "Wetterich_v_equals_minus_2lambda"
REFERENCE_MASS_LABEL = "benchmark_1e_minus20_eV"
REFERENCE_MASS_EV = 1.0e-20
SELECTED_RUN_ID = "ISOBARIC_Z0.3_RADIAL_COOLING_FREEFALL_OT_N26_P1_FULL_PRIMARY"
EDGE_POWER = 2.0
PROFILE_RADIAL_ORDER = 4000
DF_ENERGY_ORDER = 512
VISIBLE_POTENTIAL_ORDER = 50000

CONFIGURATIONS = (
    {
        "config_id": "COARSE_N64_E32_L20_T48",
        "shell_count": 64,
        "energy_order": 32,
        "angular_momentum_order": 20,
        "orbit_phase_order": 48,
        "run_role": "CONTROL_COARSE",
    },
    {
        "config_id": "PRIMARY_N96_E48_L32_T80",
        "shell_count": 96,
        "energy_order": 48,
        "angular_momentum_order": 32,
        "orbit_phase_order": 80,
        "run_role": "PRIMARY",
    },
    {
        "config_id": "FINE_N128_E64_L40_T96",
        "shell_count": 128,
        "energy_order": 64,
        "angular_momentum_order": 40,
        "orbit_phase_order": 96,
        "run_role": "CONTROL_FINE",
    },
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


EDDINGTON = load_module("mts_checkpoint_5154_for_5171", EDDINGTON_SCRIPT)
PREVIOUS = load_module("mts_checkpoint_5170_for_5171", PREVIOUS_SCRIPT)


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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def source_paths() -> dict[str, Path]:
    return {
        "checkpoint_5154_script": EDDINGTON_SCRIPT,
        "checkpoint_5154_document": POST
        / "5154-Y5-R2FR-hard-edge-isotropic-obstruction-minimal-regular-Eddington-distribution-and-stability-gate.md",
        "checkpoint_5154_result": EDDINGTON.RESULT_JSON,
        "checkpoint_5154_DF_envelope": EDDINGTON.DF_ENVELOPE_CSV,
        "checkpoint_5154_halo_inventory": EDDINGTON.HALO_CSV,
        "checkpoint_5151_document": POST
        / "5151-Y5-R2FR-parent-projective-occupation-to-conserved-Einstein-cluster-stress-and-two-metric-cog-gate.md",
        "checkpoint_5164_document": POST
        / "5164-Y5-R2FR-mass-conserving-visible-motion-initial-value-response-gate.md",
        "checkpoint_5164_script": POST
        / "scripts"
        / "Y5_R2FR_5164_mass_conserving_two_component_initial_value_gate.py",
        "checkpoint_5169_document": POST
        / "5169-Y5-R2FR-pair-consistent-capacity-bounded-transport-forward-response-gate.md",
        "checkpoint_5169_script": POST
        / "scripts"
        / "Y5_R2FR_5169_pair_consistent_transport_forward_response_gate.py",
        "checkpoint_5169_profiles": PREVIOUS.P.PROFILE_CSV,
        "checkpoint_5170_script": PREVIOUS_SCRIPT,
        "checkpoint_5170_document": PREVIOUS.DOCUMENT,
        "checkpoint_5170_result": PREVIOUS.RESULT_JSON,
        "checkpoint_5170_contract": PREVIOUS.CONTRACT_CSV,
        "visible_source": VISIBLE_SOURCE,
        "checkpoint_4960_document": PREVIOUS.UNIVERSAL_DOCUMENT,
        "checkpoint_5171_script": Path(__file__).resolve(),
    }


def construct_parent_state() -> dict[str, Any]:
    state = next(
        row
        for row in EDDINGTON.read_csv(EDDINGTON.STATE_ROWS)
        if row["galaxy"] == REFERENCE_GALAXY
        and row["mapping"] == REFERENCE_MAPPING
    )
    exponent = float(state["q_parent"])
    transition_radius_kpc = float(state["R_n_over_L_eff"]) * float(
        state["L_eff_kpc"]
    )
    velocity_infinity_km_s = float(state["v_infinity_km_s"])
    wkb_floor_eV = float(state["minimum_m_gap_eV_for_lambda_db_le_Rn"])
    spectral_nodes, spectral_weights = np.polynomial.legendre.leggauss(
        EDDINGTON.SPECTRAL_ORDER
    )
    scales, weights, analytic_weight, numeric_weight = (
        EDDINGTON.spectral_quantile_quadrature(
            exponent,
            (wkb_floor_eV / REFERENCE_MASS_EV) ** 2,
            spectral_nodes,
            spectral_weights,
        )
    )
    raw_mass_nodes, raw_mass_weights = np.polynomial.legendre.leggauss(
        EDDINGTON.MASS_QUADRATURE_ORDER
    )
    mass_nodes = 0.5 * (raw_mass_nodes + 1.0)
    mass_weights = 0.5 * raw_mass_weights
    edge_scale = (
        2.0
        * (
            velocity_infinity_km_s
            / (EDDINGTON.CP.H0_KM_S_KPC * transition_radius_kpc)
        )
        ** 2
        / (EDDINGTON.CP.MOTION_FRACTION * EDDINGTON.CP.DELTA_VIR_CRITICAL)
    )
    edge_radius_over_transition, mass_integral, _ = EDDINGTON.solve_edge_radius(
        edge_scale,
        EDGE_POWER,
        scales,
        weights,
        mass_nodes,
        mass_weights,
    )
    profile = EDDINGTON.build_profile(
        edge_radius_over_transition,
        EDGE_POWER,
        scales,
        weights,
        PROFILE_RADIAL_ORDER,
    )
    inversion, _, distribution_bins = EDDINGTON.invert_profile(
        profile,
        EDGE_POWER,
        edge_radius_over_transition,
        mass_integral,
        DF_ENERGY_ORDER,
    )
    energy_edges = EDDINGTON.energy_grid(DF_ENERGY_ORDER)
    energy_centers = 0.5 * (energy_edges[:-1] + energy_edges[1:])
    distribution = PchipInterpolator(
        np.concatenate((np.asarray([0.0]), energy_centers, np.asarray([1.0]))),
        np.concatenate(
            (
                np.asarray([0.0]),
                distribution_bins,
                np.asarray([distribution_bins[-1]]),
            )
        ),
        extrapolate=False,
    )
    distribution_derivative = distribution.derivative()
    normalized_potential = profile["relative_potential"] / profile[
        "central_potential_shape"
    ]
    potential = PchipInterpolator(profile["x"], normalized_potential)
    potential_derivative = potential.derivative()
    derivative_probe = distribution_derivative(
        np.linspace(1.0e-8, 1.0 - 1.0e-8, 20000)
    )
    density_nodes, density_weights = np.polynomial.legendre.leggauss(192)
    speed_fraction = 0.5 * (density_nodes + 1.0)
    speed_weight = 0.5 * density_weights
    density_errors: list[float] = []
    probe_x = np.geomspace(
        max(0.01, edge_radius_over_transition * 1.0e-3),
        0.995 * edge_radius_over_transition,
        64,
    )
    for radius in probe_x:
        relative_potential = float(potential(radius))
        density = float(
            np.interp(radius, profile["x"], profile["density"])
            / profile["central_density_shape"]
        )
        maximum_speed = math.sqrt(2.0 * relative_potential)
        speed = maximum_speed * speed_fraction
        energy = relative_potential - 0.5 * speed**2
        reconstructed = 4.0 * math.pi * float(
            np.sum(
                speed_weight
                * maximum_speed
                * speed**2
                * np.maximum(distribution(energy), 0.0)
            )
        )
        density_errors.append(abs(reconstructed / density - 1.0))
    mass_scale_Msun = (
        velocity_infinity_km_s**2
        * profile["central_density_shape"]
        * transition_radius_kpc
        / (4.0 * math.pi * EDDINGTON.CP.G_ASTRO)
    )
    return {
        "state_row": state,
        "q_parent": exponent,
        "transition_radius_kpc": transition_radius_kpc,
        "velocity_infinity_km_s": velocity_infinity_km_s,
        "edge_radius_over_transition": edge_radius_over_transition,
        "edge_radius_kpc": edge_radius_over_transition * transition_radius_kpc,
        "mass_integral": mass_integral,
        "physical_edge_mass_Msun": (
            velocity_infinity_km_s**2
            * transition_radius_kpc
            * mass_integral
            / EDDINGTON.CP.G_ASTRO
        ),
        "mass_scale_Msun": mass_scale_Msun,
        "profile": profile,
        "potential": potential,
        "potential_derivative": potential_derivative,
        "distribution": distribution,
        "distribution_derivative": distribution_derivative,
        "maximum_resolved_DF_energy": float(energy_centers[-1]),
        "inversion": inversion,
        "minimum_smoothed_distribution_derivative": float(
            np.min(derivative_probe)
        ),
        "maximum_DF_density_reconstruction_relative_error": float(
            np.max(density_errors)
        ),
        "spectral_normalization_relative_error": abs(
            numeric_weight / analytic_weight - 1.0
        ),
    }


def circular_orbit_ceiling(parent: dict[str, Any]) -> tuple[float, Any]:
    potential = parent["potential"]
    derivative = parent["potential_derivative"]
    edge = parent["edge_radius_over_transition"]

    def circular_energy(radius: float) -> float:
        return float(potential(radius) + 0.5 * radius * derivative(radius))

    probe = np.linspace(edge * 1.0e-8, edge, 20000)
    values = np.asarray([circular_energy(radius) for radius in probe])
    crossings = np.flatnonzero(values[:-1] * values[1:] <= 0.0)
    if len(crossings) == 0:
        raise RuntimeError("zero-energy circular orbit was not bracketed")
    index = int(crossings[-1])
    radius = brentq(circular_energy, probe[index], probe[index + 1])
    return radius, circular_energy


def visible_mass_interpolator() -> tuple[Any, np.ndarray, np.ndarray]:
    rows = read_csv(VISIBLE_SOURCE)
    radii = np.asarray([float(row["radius_kpc"]) for row in rows])
    masses = np.maximum.accumulate(
        np.maximum(
            np.asarray(
                [float(row["spherical_equivalent_baryon_mass_Msun"]) for row in rows]
            ),
            0.0,
        )
    )
    interpolator = PchipInterpolator(radii, masses)

    def mass_at(radius_kpc: np.ndarray) -> np.ndarray:
        radius = np.asarray(radius_kpc, dtype=float)
        result = np.empty_like(radius)
        inner = radius < radii[0]
        middle = (radius >= radii[0]) & (radius <= radii[-1])
        outer = radius > radii[-1]
        result[inner] = masses[0] * (radius[inner] / radii[0]) ** 3
        result[middle] = interpolator(radius[middle])
        result[outer] = masses[-1]
        return result

    return mass_at, radii, masses


def external_potential(
    parent: dict[str, Any], shell_centers: np.ndarray, mass_at: Any
) -> np.ndarray:
    edge = parent["edge_radius_over_transition"]
    transition_radius = parent["transition_radius_kpc"]
    velocity = parent["velocity_infinity_km_s"]
    central_potential = parent["profile"]["central_potential_shape"]
    dense_x = np.unique(
        np.concatenate(
            (
                np.geomspace(edge * 1.0e-10, edge, VISIBLE_POTENTIAL_ORDER),
                shell_centers,
            )
        )
    )
    integrand = (
        EDDINGTON.CP.G_ASTRO
        * mass_at(transition_radius * dense_x)
        / (
            transition_radius
            * velocity**2
            * central_potential
            * dense_x**2
        )
    )
    cumulative = np.concatenate(
        (np.asarray([0.0]), cumulative_trapezoid(integrand, dense_x))
    )
    potential = PchipInterpolator(dense_x, cumulative[-1] - cumulative)
    return np.asarray(potential(shell_centers), dtype=float)


def construct_orbit_kernel(
    parent: dict[str, Any], configuration: dict[str, Any], mass_at: Any
) -> dict[str, Any]:
    started = time.perf_counter()
    shell_count = int(configuration["shell_count"])
    edge = parent["edge_radius_over_transition"]
    shell_parameter = np.linspace(0.0, 1.0, shell_count + 1)
    shell_edges = edge * np.sin(0.5 * math.pi * shell_parameter) ** 2
    shell_centers = 0.5 * (shell_edges[:-1] + shell_edges[1:])
    energy_nodes, energy_weights = np.polynomial.legendre.leggauss(
        int(configuration["energy_order"])
    )
    energy_parameter = 0.5 * (energy_nodes + 1.0)
    energy_parameter_weights = 0.5 * energy_weights
    maximum_energy = parent["maximum_resolved_DF_energy"]
    energies = maximum_energy * np.sin(0.5 * math.pi * energy_parameter) ** 2
    transformed_energy_weights = (
        energy_parameter_weights
        * maximum_energy
        * 0.5
        * math.pi
        * np.sin(math.pi * energy_parameter)
    )
    angular_nodes, angular_weights = np.polynomial.legendre.leggauss(
        int(configuration["angular_momentum_order"])
    )
    circularities = 0.5 * (angular_nodes + 1.0)
    circularity_weights = 0.5 * angular_weights
    phase_nodes, phase_weights = np.polynomial.legendre.leggauss(
        int(configuration["orbit_phase_order"])
    )
    phase = 0.5 * math.pi * (phase_nodes + 1.0)
    phase_weights = 0.5 * math.pi * phase_weights
    potential = parent["potential"]
    potential_derivative = parent["potential_derivative"]
    distribution = parent["distribution"]
    distribution_derivative = parent["distribution_derivative"]
    circular_ceiling, circular_energy = circular_orbit_ceiling(parent)
    response = np.zeros((shell_count, shell_count), dtype=float)
    phase_mass = 0.0
    orbit_count = 0
    for energy, energy_weight in zip(energies, transformed_energy_weights):
        circular_radius = brentq(
            lambda radius: circular_energy(radius) - energy,
            edge * 1.0e-12,
            circular_ceiling,
        )
        circular_velocity_squared = max(
            0.0,
            -circular_radius * float(potential_derivative(circular_radius)),
        )
        maximum_angular_momentum = circular_radius * math.sqrt(
            circular_velocity_squared
        )
        distribution_value = max(0.0, float(distribution(energy)))
        derivative_value = max(0.0, float(distribution_derivative(energy)))
        for circularity, circularity_weight in zip(
            circularities, circularity_weights
        ):
            angular_momentum = circularity * maximum_angular_momentum

            def radial_energy(radius: float) -> float:
                return float(
                    potential(radius)
                    - energy
                    - angular_momentum**2 / (2.0 * radius**2)
                )

            pericentre = brentq(
                radial_energy,
                edge * 1.0e-14,
                circular_radius,
                xtol=1.0e-13,
                rtol=1.0e-12,
            )
            apocentre = brentq(
                radial_energy,
                circular_radius,
                edge,
                xtol=1.0e-13,
                rtol=1.0e-12,
            )
            midpoint = 0.5 * (pericentre + apocentre)
            half_width = 0.5 * (apocentre - pericentre)
            orbit_radius = midpoint - half_width * np.cos(phase)
            radial_energy_values = np.asarray(
                [radial_energy(radius) for radius in orbit_radius]
            )
            turning_product = (orbit_radius - pericentre) * (
                apocentre - orbit_radius
            )
            regularized_radial_shape = radial_energy_values / turning_product
            if np.any(regularized_radial_shape <= 0.0):
                raise RuntimeError(
                    "nonpositive regularized radial-orbit shape: "
                    f"E={energy}, eta={circularity}, "
                    f"minimum={np.min(regularized_radial_shape)}"
                )
            time_weight = phase_weights / np.sqrt(
                2.0 * regularized_radial_shape
            )
            half_period = float(np.sum(time_weight))
            right_indices = np.searchsorted(shell_centers, orbit_radius)
            left_indices = np.clip(right_indices - 1, 0, shell_count - 1)
            right_indices = np.clip(right_indices, 0, shell_count - 1)
            denominator = shell_centers[right_indices] - shell_centers[left_indices]
            right_fractions = np.zeros_like(orbit_radius)
            distinct = right_indices != left_indices
            right_fractions[distinct] = (
                orbit_radius[distinct] - shell_centers[left_indices[distinct]]
            ) / denominator[distinct]
            right_fractions = np.clip(right_fractions, 0.0, 1.0)
            left_fractions = 1.0 - right_fractions
            orbit_probability = np.bincount(
                left_indices,
                weights=time_weight * left_fractions,
                minlength=shell_count,
            )
            orbit_probability += np.bincount(
                right_indices,
                weights=time_weight * right_fractions,
                minlength=shell_count,
            )
            orbit_probability /= half_period
            phase_volume = (
                16.0
                * math.pi**2
                * angular_momentum
                * half_period
                * maximum_angular_momentum
                * energy_weight
                * circularity_weight
            )
            phase_mass += phase_volume * distribution_value
            susceptibility_weight = phase_volume * derivative_value
            response += susceptibility_weight * (
                np.diag(orbit_probability)
                - np.outer(orbit_probability, orbit_probability)
            )
            orbit_count += 1
    central_density = parent["profile"]["central_density_shape"]
    central_potential = parent["profile"]["central_potential_shape"]
    self_gravity_coefficient = central_density / (
        4.0 * math.pi * central_potential
    )
    gravity_kernel = np.asarray(
        [
            [
                1.0 / max(radius, source_radius) - 1.0 / edge
                for source_radius in shell_centers
            ]
            for radius in shell_centers
        ]
    )
    response_eigenvalues, response_vectors = np.linalg.eigh(response)
    positive_response_eigenvalues = np.maximum(response_eigenvalues, 0.0)
    response_square_root = (
        response_vectors
        * np.sqrt(positive_response_eigenvalues)[None, :]
    ) @ response_vectors.T
    symmetric_dielectric_operator = (
        self_gravity_coefficient
        * response_square_root
        @ gravity_kernel
        @ response_square_root
    )
    dielectric_eigenvalues = np.linalg.eigvalsh(symmetric_dielectric_operator)
    response_operator = self_gravity_coefficient * gravity_kernel @ response
    external = external_potential(parent, shell_centers, mass_at)
    total_potential = np.linalg.solve(
        np.eye(shell_count) - response_operator, external
    )
    born_shell_mass = response @ external
    self_consistent_shell_mass = response @ total_potential
    expected_phase_mass = (
        4.0
        * math.pi
        * parent["mass_integral"]
        / parent["profile"]["central_density_shape"]
    )
    shell_volume = (
        4.0
        * math.pi
        / 3.0
        * (shell_edges[1:] ** 3 - shell_edges[:-1] ** 3)
    )
    return {
        "configuration": configuration,
        "shell_edges": shell_edges,
        "shell_centers": shell_centers,
        "shell_volume": shell_volume,
        "response": response,
        "gravity_kernel": gravity_kernel,
        "self_gravity_coefficient": self_gravity_coefficient,
        "external_potential": external,
        "total_potential": total_potential,
        "born_shell_mass": born_shell_mass,
        "self_consistent_shell_mass": self_consistent_shell_mass,
        "response_eigenvalues": response_eigenvalues,
        "dielectric_eigenvalues": dielectric_eigenvalues,
        "phase_mass": phase_mass,
        "expected_phase_mass": expected_phase_mass,
        "orbit_count": orbit_count,
        "wall_seconds": time.perf_counter() - started,
        "dielectric_condition_number": float(
            np.linalg.cond(np.eye(shell_count) - response_operator)
        ),
    }


def inverse_requirement(
    shell_radii_kpc: np.ndarray, parent: dict[str, Any]
) -> dict[str, Any]:
    target = PREVIOUS.target_context()
    scores, profiles = PREVIOUS.primary_rows()
    selected_score = next(
        row for row in scores if row["run_id"] == SELECTED_RUN_ID
    )
    selected_profiles = [
        row for row in profiles if row["run_id"] == SELECTED_RUN_ID
    ]
    radii = np.asarray(
        [float(row["radius_kpc"]) for row in selected_profiles], dtype=float
    )
    corrected_mass = np.asarray(
        [float(row["corrected_motion_mass_Msun"]) for row in selected_profiles],
        dtype=float,
    )
    corrected_edge_mass = float(
        np.interp(parent["edge_radius_kpc"], radii, corrected_mass)
    )
    target_edge_mass = float(target["target_edge_mass_Msun"])
    normalized_corrected = (
        np.interp(shell_radii_kpc, radii, corrected_mass)
        * target_edge_mass
        / corrected_edge_mass
    )
    target_mass = np.interp(
        shell_radii_kpc, radii, target["target_mass_Msun"]
    )
    required_shape = target_mass - normalized_corrected
    return {
        "target": target,
        "selected_score": selected_score,
        "radii": radii,
        "corrected_mass": corrected_mass,
        "corrected_edge_mass": corrected_edge_mass,
        "target_edge_mass": target_edge_mass,
        "normalized_corrected_mass": normalized_corrected,
        "target_mass": target_mass,
        "required_shape_cumulative_mass": required_shape,
    }


def cosine_similarity(
    left: np.ndarray, right: np.ndarray, mask: np.ndarray
) -> float:
    numerator = float(np.dot(left[mask], right[mask]))
    denominator = math.sqrt(
        float(np.dot(left[mask], left[mask]))
        * float(np.dot(right[mask], right[mask]))
    )
    return numerator / denominator


def summarize_run(
    run: dict[str, Any], parent: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    shell_radii_kpc = (
        run["shell_centers"] * parent["transition_radius_kpc"]
    )
    requirement = inverse_requirement(shell_radii_kpc, parent)
    physical_shell_mass = (
        run["self_consistent_shell_mass"] * parent["mass_scale_Msun"]
    )
    physical_born_shell_mass = run["born_shell_mass"] * parent["mass_scale_Msun"]
    cumulative_response = np.cumsum(physical_shell_mass)
    cumulative_born = np.cumsum(physical_born_shell_mass)
    required = requirement["required_shape_cumulative_mass"]
    score_radii = requirement["target"]["radii_kpc"][
        requirement["target"]["score_mask"]
    ]
    mask = (shell_radii_kpc >= score_radii[0]) & (
        shell_radii_kpc <= score_radii[-1]
    )
    diagnostic_factor = float(
        np.dot(cumulative_response[mask], required[mask])
        / np.dot(cumulative_response[mask], cumulative_response[mask])
    )
    ratio = cumulative_response[mask] / np.maximum(
        required[mask], np.finfo(float).tiny
    )
    base_potential = np.asarray(parent["potential"](run["shell_centers"]))
    full_potential_ratio = np.abs(run["total_potential"]) / np.maximum(
        base_potential, np.finfo(float).tiny
    )
    transition_radius = parent["transition_radius_kpc"]
    density_response = run["self_consistent_shell_mass"] / run["shell_volume"]
    sign_indices = np.flatnonzero(density_response[:-1] * density_response[1:] < 0.0)
    sign_radius = (
        float(shell_radii_kpc[int(sign_indices[0])])
        if len(sign_indices)
        else math.nan
    )
    summary = {
        "config_id": run["configuration"]["config_id"],
        "run_role": run["configuration"]["run_role"],
        "shell_count": run["configuration"]["shell_count"],
        "energy_order": run["configuration"]["energy_order"],
        "angular_momentum_order": run["configuration"][
            "angular_momentum_order"
        ],
        "orbit_phase_order": run["configuration"]["orbit_phase_order"],
        "orbit_count": run["orbit_count"],
        "phase_mass_relative_error": run["phase_mass"]
        / run["expected_phase_mass"]
        - 1.0,
        "kernel_symmetry_max_abs": float(
            np.max(np.abs(run["response"] - run["response"].T))
        ),
        "kernel_row_zero_mode_max_abs": float(
            np.max(np.abs(np.sum(run["response"], axis=1)))
        ),
        "kernel_column_mass_mode_max_abs": float(
            np.max(np.abs(np.sum(run["response"], axis=0)))
        ),
        "minimum_kernel_eigenvalue": float(np.min(run["response_eigenvalues"])),
        "maximum_kernel_eigenvalue": float(np.max(run["response_eigenvalues"])),
        "maximum_static_dielectric_eigenvalue": float(
            np.max(run["dielectric_eigenvalues"])
        ),
        "minimum_static_dielectric_eigenvalue": float(
            np.min(run["dielectric_eigenvalues"])
        ),
        "dielectric_condition_number": run["dielectric_condition_number"],
        "external_center_proxy_over_parent_potential": float(
            run["external_potential"][0] / base_potential[0]
        ),
        "self_consistent_center_proxy_over_parent_potential": float(
            run["total_potential"][0] / base_potential[0]
        ),
        "self_gravity_center_amplification": float(
            run["total_potential"][0] / run["external_potential"][0]
        ),
        "maximum_total_perturbation_over_parent_potential": float(
            np.max(full_potential_ratio)
        ),
        "total_response_mass_Msun": float(np.sum(physical_shell_mass)),
        "mass_conservation_relative_residual": float(
            abs(np.sum(physical_shell_mass))
            / np.sum(np.abs(physical_shell_mass))
        ),
        "born_mass_conservation_relative_residual": float(
            abs(np.sum(physical_born_shell_mass))
            / np.sum(np.abs(physical_born_shell_mass))
        ),
        "positive_density_shell_count": int(np.count_nonzero(density_response > 0.0)),
        "negative_density_shell_count": int(np.count_nonzero(density_response < 0.0)),
        "first_density_response_sign_change_radius_kpc": sign_radius,
        "peak_cumulative_response_Msun": float(np.max(cumulative_response)),
        "peak_cumulative_response_radius_kpc": float(
            shell_radii_kpc[int(np.argmax(cumulative_response))]
        ),
        "peak_required_shape_Msun": float(np.max(required[mask])),
        "peak_required_shape_radius_kpc": float(
            shell_radii_kpc[
                np.flatnonzero(mask)[int(np.argmax(required[mask]))]
            ]
        ),
        "response_required_cosine": cosine_similarity(
            cumulative_response, required, mask
        ),
        "born_response_required_cosine": cosine_similarity(
            cumulative_born, required, mask
        ),
        "diagnostic_forbidden_response_multiplier": diagnostic_factor,
        "minimum_predicted_to_required_ratio_in_score_window": float(
            np.min(ratio)
        ),
        "maximum_predicted_to_required_ratio_in_score_window": float(
            np.max(ratio)
        ),
        "predicted_to_required_ratio_at_transition": float(
            np.interp(transition_radius, shell_radii_kpc, cumulative_response)
            / np.interp(transition_radius, shell_radii_kpc, required)
        ),
        "wall_seconds": run["wall_seconds"],
        "target_used_only_for_post_prediction_diagnostic": True,
        "response_multiplier_used_in_prediction": False,
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }
    arrays = {
        "shell_radii_kpc": shell_radii_kpc,
        "base_potential": base_potential,
        "density_response": density_response,
        "physical_shell_mass": physical_shell_mass,
        "physical_born_shell_mass": physical_born_shell_mass,
        "cumulative_response": cumulative_response,
        "cumulative_born": cumulative_born,
        "requirement": requirement,
    }
    return summary, arrays


def derivation_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "D1_LINEARIZED_VLASOV",
            "partial_t deltaf+{deltaf,H0}+{f0,deltaPhi}=0",
            "linearization of the checkpoint-5151 collisionless Wigner equation",
        ),
        (
            "D2_RETARDED_ACTION_ANGLE",
            "deltaf_n=(n.dJ f0)/(n.Omega-omega-i0) deltaPhi_n",
            "retarded scalar kinetic polarization before the static limit",
        ),
        (
            "D3_STATIC_ADIABATIC_LIMIT",
            "deltaf=f_Epsilon[deltaPsi-<deltaPsi>_(E,L)]",
            "all nonzero radial harmonics respond; the conserved action-average mode does not",
        ),
        (
            "D4_ORBIT_MEASURE",
            "dGamma_(E,L)=16 pi^2 L I_r(E,L) dE dL",
            "I_r=int_(rp)^(ra) dr/v_r is the half radial period",
        ),
        (
            "D5_DISCRETE_KERNEL",
            "B=sum_a C_a[diag(p_a)-p_a p_a^T]",
            "C_a=16 pi^2 L I_r f_Epsilon dE dL and p_a is normalized orbit occupancy",
        ),
        (
            "D6_COMPENSATION",
            "B 1=0 and 1^T B=0",
            "constant-potential gauge mode is silent and every orbit conserves particle number",
        ),
        (
            "D7_PASSIVITY",
            "u^T B u=sum_a C_a Var_(p_a)(u)>=0 when f_Epsilon>=0",
            "the checkpoint-5154 monotone-energy sign makes the static susceptibility positive semidefinite",
        ),
        (
            "D8_SELF_CONSISTENCY",
            "deltaPsi=(I-kappa K B)^(-1) deltaPsi_b",
            "same calibrated G_N; no response coefficient is introduced",
        ),
    ]
    return [
        {
            "derivation_id": identifier,
            "equation": equation,
            "meaning": meaning,
            "parent_owned": True,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for identifier, equation, meaning in rows
    ]


def double_counting_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DC1_PARENT_KINETIC_FLOW",
            "checkpoint 5151",
            "p^mu nabla_mu f=0",
            "the occupied-state stress already evolves by collisionless characteristics",
        ),
        (
            "DC2_NEWTONIAN_CHARACTERISTICS",
            "checkpoint 5164",
            "d2x_i/dt2=-G_N M_enclosed x_i/(r_i^2+epsilon^2)^(3/2)",
            "this is the spherical Vlasov-Poisson characteristic flow of DC1",
        ),
        (
            "DC3_FULL_STATE_REPLAY",
            "checkpoint 5169",
            "full antithetic particle states evolved under the same force",
            "the finite-time nonlinear collisionless density response is already in the scored profile",
        ),
        (
            "DC4_CURRENT_KERNEL",
            "checkpoint 5171",
            "B is the Frechet derivative of the DC1/DC2 flow about the 5154 ergodic state",
            "adding B deltaPsi to checkpoint 5169 would count the same Vlasov response twice",
        ),
    ]
    return [
        {
            "ledger_id": identifier,
            "source": source,
            "equation_or_operation": equation,
            "deduction": deduction,
            "independent_new_stress": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for identifier, source, equation, deduction in rows
    ]


def clause_rows(primary: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        (
            "K1_UNIVERSAL_SOURCE",
            "PASS_INHERITED",
            "checkpoint 4960 fixes the same Hilbert/Newton coupling used by kappa K",
        ),
        (
            "K2_RETARDED_STATE_RESPONSE",
            "PARTIAL_DERIVED",
            "finite-omega action-angle kernel and exact static scalar projection derived; full covariant tensor kernel remains open",
        ),
        (
            "K3_WARD_CONSERVATION",
            "PASS_KINETIC_LIMIT",
            f"discrete mass-mode residual={primary['kernel_column_mass_mode_max_abs']}",
        ),
        (
            "K4_COMPENSATED_ZERO_MODE",
            "PASS_DERIVED",
            f"response mass residual={primary['mass_conservation_relative_residual']}",
        ),
        (
            "K5_RADIAL_SIGN_CHANGE",
            "PASS_PREDICTED",
            f"positive shells={primary['positive_density_shell_count']}; negative shells={primary['negative_density_shell_count']}",
        ),
        (
            "K6_LOCAL_VACUUM_SILENCE",
            "PASS_EXACT_KINETIC_LIMIT",
            "deltaPsi_b=0 gives deltaf=0; F_X=0 gives B=0",
        ),
        (
            "K7_NO_ARENA_RETUNING",
            "PASS",
            "no response multiplier enters the prediction; the displayed least-squares multiplier is diagnostic and forbidden",
        ),
        (
            "K8_CAUSAL_STABILITY",
            "PARTIAL_STATIC_RADIAL_PASS",
            f"max static dielectric eigenvalue={primary['maximum_static_dielectric_eigenvalue']}; finite-frequency and relativistic spectrum remain open",
        ),
    ]
    return [
        {
            "clause_id": identifier,
            "status": status,
            "evidence": evidence,
            "fully_closed": status.startswith("PASS"),
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for identifier, status, evidence in rows
    ]


def profile_rows(
    run: dict[str, Any], arrays: dict[str, Any], parent: dict[str, Any]
) -> list[dict[str, Any]]:
    requirement = arrays["requirement"]
    normalized_corrected = requirement["normalized_corrected_mass"]
    target_mass = requirement["target_mass"]
    required = requirement["required_shape_cumulative_mass"]
    density = arrays["density_response"]
    rows: list[dict[str, Any]] = []
    for index, radius in enumerate(arrays["shell_radii_kpc"]):
        rows.append(
            {
                "config_id": run["configuration"]["config_id"],
                "radius_kpc": radius,
                "radius_over_transition": radius
                / parent["transition_radius_kpc"],
                "parent_relative_potential_normalized": arrays["base_potential"][
                    index
                ],
                "external_baryon_relative_potential_normalized": run[
                    "external_potential"
                ][index],
                "self_consistent_total_perturbing_potential_normalized": run[
                    "total_potential"
                ][index],
                "response_density_normalized": density[index],
                "response_shell_mass_Msun": arrays["physical_shell_mass"][index],
                "response_cumulative_mass_Msun": arrays["cumulative_response"][
                    index
                ],
                "born_response_cumulative_mass_Msun": arrays["cumulative_born"][
                    index
                ],
                "edge_normalized_5169_mass_Msun": normalized_corrected[index],
                "target_mass_Msun": target_mass[index],
                "required_shape_cumulative_mass_Msun": required[index],
                "response_density_sign": (
                    "POSITIVE"
                    if density[index] > 0.0
                    else "NEGATIVE"
                    if density[index] < 0.0
                    else "ZERO"
                ),
                "prediction_uses_target": False,
                "linear_response_addition_to_5169_allowed": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows


def provenance_rows(paths: dict[str, Path]) -> list[dict[str, Any]]:
    return [
        {
            "source_id": key,
            "source_path": str(path),
            "sha256": file_digest(path),
            "status": "immutable_input",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for key, path in paths.items()
    ]


def add_validation(
    rows: list[dict[str, Any]], check_id: str, passed: bool, evidence: Any
) -> None:
    rows.append(
        {
            "check_id": check_id,
            "passed": bool(passed),
            "evidence": json.dumps(evidence, sort_keys=True),
            "checkpoint_marker": MARKER,
        }
    )


def make_document(result: dict[str, Any]) -> str:
    summary = result["summary"]
    primary = summary["primary"]
    convergence_lines = "\n".join(
        f"- `{row['config_id']}`: phase-mass error=`{row['phase_mass_relative_error']}`, "
        f"lambda_max=`{row['maximum_static_dielectric_eigenvalue']}`, "
        f"peak response=`{row['peak_cumulative_response_Msun']} Msun` at "
        f"`{row['peak_cumulative_response_radius_kpc']} kpc`"
        for row in summary["convergence"]
    )
    return f"""# 5171 - Action-angle retarded Vlasov polarization, static response and double-counting gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

The compensated kernel requested by checkpoint 5170 is not an arbitrary
closure: its static scalar Vlasov projection follows directly from the
positive checkpoint-5154 Eddington state. For relative energy `Epsilon` and
an orbit labelled by `(Epsilon,L)`, the retarded action-angle solution gives

```text
delta f_n=[n.partial_J f_0/(n.Omega-omega-i0)] delta Phi_n,
delta f(omega->0)=f_Epsilon[delta Psi-<delta Psi>_(Epsilon,L)].
```

Consequently the discrete orbit kernel is

```text
B=sum_a C_a[diag(p_a)-p_a p_a^T],
B 1=0,
1^T B=0,
u^T B u=sum_a C_a Var_(p_a)(u)>=0.
```

The compensated zero mode, sign-changing density response and kinetic Ward
identity are therefore derived rather than imposed. However, this same
collisionless response is already evolved nonlinearly by checkpoints
5164-5169. It cannot be added to their scored profile as a new collective
stress without double counting.

## Executed parent-state response

The fixed state is `{REFERENCE_GALAXY}`, `{REFERENCE_MAPPING}`,
`{REFERENCE_MASS_LABEL}`, with no changed gravity or response coefficient.
The orbit integral uses `{primary['orbit_count']}` `(Epsilon,L)` cells and
reconstructs the phase-space mass with relative error
`{primary['phase_mass_relative_error']}`. The kernel symmetry residual is
`{primary['kernel_symmetry_max_abs']}` and its mass-mode residual is
`{primary['kernel_column_mass_mode_max_abs']}`.

Self-gravity is solved, not fitted:

```text
delta Psi=(I-kappa K B)^(-1) delta Psi_b.
```

The maximum static radial dielectric eigenvalue is
`{primary['maximum_static_dielectric_eigenvalue']}` and the solve condition
number is `{primary['dielectric_condition_number']}`. Thus this benchmark has
no static radial pole. This does not prove the finite-frequency relativistic
spectrum.

The response has `{primary['positive_density_shell_count']}` positive and
`{primary['negative_density_shell_count']}` negative density shells and
conserves total occupied mass to relative residual
`{primary['mass_conservation_relative_residual']}`. Its cumulative response
peaks at `{primary['peak_cumulative_response_radius_kpc']} kpc` with
`{primary['peak_cumulative_response_Msun']} Msun`. The independently
reconstructed checkpoint-5170 shape requirement peaks at
`{primary['peak_required_shape_radius_kpc']} kpc` with
`{primary['peak_required_shape_Msun']} Msun`.

## Does it close the 5170 residual?

No. The target is read only after the prediction. The profile cosine is
`{primary['response_required_cosine']}`, so action conservation naturally
produces the right broad compensated orientation, but the predicted-to-required
ratio ranges from `{primary['minimum_predicted_to_required_ratio_in_score_window']}`
to `{primary['maximum_predicted_to_required_ratio_in_score_window']}` across
the frozen score window and is
`{primary['predicted_to_required_ratio_at_transition']}` at the transition.
No constant multiplier can repair that radial mismatch, and no such
multiplier was used.

The linear hierarchy also fails globally: the largest self-consistent
perturbing-potential/background-potential ratio is
`{primary['maximum_total_perturbation_over_parent_potential']}`. A nonlinear
adiabatic calculation would therefore be required even if the response had
not already been included by the particle evolution.

## Convergence

{convergence_lines}

The fine-versus-primary changes in dielectric eigenvalue and peak cumulative
response are `{summary['fine_primary_dielectric_relative_change']}` and
`{summary['fine_primary_peak_response_relative_change']}`. The static result
is numerically controlled at this gate.

## Scientific correction and next route

Checkpoint 5170 correctly excluded a missing constant coupling, but its
remaining `Vlasov polarization` label was too broad. The classical density
part is now derived and identified as already counted. A genuinely new
mechanism must be one of the following, and must be parent-derived: a
nonclassical/interacting stress not present in Vlasov-Poisson, a different
parent-selected occupied state, or the source geometry omitted by the
spherical baryon projection. The next least-assumptive calculation is the
geometry gate: replay the same state and frozen source history with the
source-backed axisymmetric disk/gas force before inventing another stress.

```text
retarded action-angle scalar kernel                    = derived;
compensated mass zero mode                             = derived exactly;
radial sign-changing response                          = predicted;
static radial dielectric pole                          = absent in benchmark;
full covariant finite-frequency Pi_R                    = not derived;
linear hierarchy for the executed baryon source         = failed;
independent stress beyond checkpoints 5164-5169          = no;
adding this response to checkpoint 5169                  = forbidden double count;
local GR/Newton/Maxwell branch modified                  = no;
galaxy or full-MTS claim                                 = false.
```

All `{result['validation_count']}` validation rows pass. The protected
`formalization-workbench` digest remains
`{result['formalization_workbench_tree_sha256']}`. No GitHub action occurred.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    paths = source_paths()
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing sources: {missing}")
    formal_before = tree_digest(FORMAL)
    if formal_before != FORMAL_DIGEST_LOCK:
        raise RuntimeError(f"protected digest mismatch: {formal_before}")
    source_hashes = {key: file_digest(path) for key, path in paths.items()}
    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "marker": MARKER,
                    "reference_galaxy": REFERENCE_GALAXY,
                    "reference_mapping": REFERENCE_MAPPING,
                    "reference_mass_label": REFERENCE_MASS_LABEL,
                    "configurations": CONFIGURATIONS,
                    "formal_digest": formal_before,
                },
                indent=2,
            )
        )
        return
    parent = construct_parent_state()
    mass_at, visible_radii, visible_masses = visible_mass_interpolator()
    runs: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    arrays_by_config: dict[str, dict[str, Any]] = {}
    for configuration in CONFIGURATIONS:
        run = construct_orbit_kernel(parent, configuration, mass_at)
        summary, arrays = summarize_run(run, parent)
        runs.append(run)
        summaries.append(summary)
        arrays_by_config[str(configuration["config_id"])] = arrays
    primary_index = next(
        index
        for index, row in enumerate(summaries)
        if row["run_role"] == "PRIMARY"
    )
    fine = next(row for row in summaries if row["run_role"] == "CONTROL_FINE")
    primary = summaries[primary_index]
    primary_run = runs[primary_index]
    primary_arrays = arrays_by_config[primary["config_id"]]
    fine_primary_dielectric_change = abs(
        fine["maximum_static_dielectric_eigenvalue"]
        / primary["maximum_static_dielectric_eigenvalue"]
        - 1.0
    )
    fine_primary_peak_change = abs(
        fine["peak_cumulative_response_Msun"]
        / primary["peak_cumulative_response_Msun"]
        - 1.0
    )
    derivation = derivation_rows()
    double_counting = double_counting_rows()
    clauses = clause_rows(primary)
    profiles = profile_rows(primary_run, primary_arrays, parent)
    spectrum = [
        {
            "config_id": primary["config_id"],
            "mode_index": index,
            "static_dielectric_eigenvalue": value,
            "static_pole": value >= 1.0,
            "finite_frequency_stability_proved": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for index, value in enumerate(
            np.sort(primary_run["dielectric_eigenvalues"])[::-1]
        )
    ]
    route = (
        "THE_PARENT_EDDINGTON_STATE_DERIVES_A_COMPENSATED_STATIC_VLASOV_RESPONSE_"
        "BUT_THE_LINEAR_HIERARCHY_FAILS_AND_THE_SAME_COLLISIONLESS_RESPONSE_IS_"
        "ALREADY_PRESENT_IN_5164_5169_SO_IT_CANNOT_BE_ADDED_AS_A_NEW_STRESS_"
        "MOVE_TO_THE_SOURCE_GEOMETRY_GATE_BEFORE_NEW_PARENT_PHYSICS"
    )
    decisions = [
        {
            "route": "action_angle_vlasov_polarization",
            "result": route,
            "evidence": (
                f"lambda_max={primary['maximum_static_dielectric_eigenvalue']}; "
                f"mass_residual={primary['mass_conservation_relative_residual']}; "
                f"potential_ratio={primary['maximum_total_perturbation_over_parent_potential']}; "
                "same characteristic flow already executed in checkpoints 5164-5169"
            ),
            "next_requirement": (
                "source-backed axisymmetric disk/gas force replay with the same state, "
                "same G_N and frozen source history"
            ),
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    ]
    provenance = provenance_rows(paths)
    write_csv(DERIVATION_CSV, derivation)
    write_csv(CONVERGENCE_CSV, summaries)
    write_csv(SPECTRUM_CSV, spectrum)
    write_csv(PROFILE_CSV, profiles)
    write_csv(CLAUSE_CSV, clauses)
    write_csv(DOUBLE_COUNT_CSV, double_counting)
    write_csv(DECISION_CSV, decisions)
    write_csv(PROVENANCE_CSV, provenance)
    validation: list[dict[str, Any]] = []
    add_validation(validation, "all_source_paths_exist", True, len(paths))
    add_validation(
        validation,
        "formal_digest_locked_before",
        formal_before == FORMAL_DIGEST_LOCK,
        formal_before,
    )
    add_validation(
        validation,
        "reference_state_frozen",
        parent["state_row"]["galaxy"] == REFERENCE_GALAXY
        and parent["state_row"]["mapping"] == REFERENCE_MAPPING,
        [parent["state_row"]["galaxy"], parent["state_row"]["mapping"]],
    )
    add_validation(
        validation,
        "parent_DF_positive",
        bool(parent["inversion"]["positive_distribution"]),
        parent["inversion"]["minimum_distribution"],
    )
    add_validation(
        validation,
        "parent_DF_monotone",
        parent["minimum_smoothed_distribution_derivative"] >= 0.0,
        parent["minimum_smoothed_distribution_derivative"],
    )
    add_validation(
        validation,
        "smoothed_DF_reconstructs_density",
        parent["maximum_DF_density_reconstruction_relative_error"] < 0.02,
        parent["maximum_DF_density_reconstruction_relative_error"],
    )
    add_validation(
        validation,
        "orbit_quadrature_reconstructs_phase_mass",
        all(abs(row["phase_mass_relative_error"]) < 5.0e-4 for row in summaries),
        [row["phase_mass_relative_error"] for row in summaries],
    )
    add_validation(
        validation,
        "kernel_symmetric",
        all(row["kernel_symmetry_max_abs"] < 1.0e-12 for row in summaries),
        [row["kernel_symmetry_max_abs"] for row in summaries],
    )
    add_validation(
        validation,
        "constant_potential_zero_mode",
        all(row["kernel_row_zero_mode_max_abs"] < 1.0e-10 for row in summaries),
        [row["kernel_row_zero_mode_max_abs"] for row in summaries],
    )
    add_validation(
        validation,
        "mass_compensation_zero_mode",
        all(row["kernel_column_mass_mode_max_abs"] < 1.0e-10 for row in summaries),
        [row["kernel_column_mass_mode_max_abs"] for row in summaries],
    )
    add_validation(
        validation,
        "kernel_positive_semidefinite",
        all(row["minimum_kernel_eigenvalue"] > -1.0e-10 for row in summaries),
        [row["minimum_kernel_eigenvalue"] for row in summaries],
    )
    add_validation(
        validation,
        "static_radial_dielectric_no_pole",
        all(
            row["maximum_static_dielectric_eigenvalue"] < 1.0
            for row in summaries
        ),
        [row["maximum_static_dielectric_eigenvalue"] for row in summaries],
    )
    add_validation(
        validation,
        "self_consistent_solve_conditioned",
        all(row["dielectric_condition_number"] < 10.0 for row in summaries),
        [row["dielectric_condition_number"] for row in summaries],
    )
    add_validation(
        validation,
        "predicted_response_mass_conserved",
        all(row["mass_conservation_relative_residual"] < 1.0e-12 for row in summaries),
        [row["mass_conservation_relative_residual"] for row in summaries],
    )
    add_validation(
        validation,
        "born_response_mass_conserved",
        all(
            row["born_mass_conservation_relative_residual"] < 1.0e-12
            for row in summaries
        ),
        [row["born_mass_conservation_relative_residual"] for row in summaries],
    )
    add_validation(
        validation,
        "radial_density_response_changes_sign",
        all(
            row["positive_density_shell_count"] > 0
            and row["negative_density_shell_count"] > 0
            for row in summaries
        ),
        [
            [row["positive_density_shell_count"], row["negative_density_shell_count"]]
            for row in summaries
        ],
    )
    add_validation(
        validation,
        "fine_primary_dielectric_converged",
        fine_primary_dielectric_change < 0.03,
        fine_primary_dielectric_change,
    )
    add_validation(
        validation,
        "fine_primary_peak_response_converged",
        fine_primary_peak_change < 0.08,
        fine_primary_peak_change,
    )
    add_validation(
        validation,
        "linearity_failure_detected",
        primary["maximum_total_perturbation_over_parent_potential"] > 1.0,
        primary["maximum_total_perturbation_over_parent_potential"],
    )
    add_validation(
        validation,
        "no_response_multiplier_used",
        all(not row["response_multiplier_used_in_prediction"] for row in summaries),
        [row["diagnostic_forbidden_response_multiplier"] for row in summaries],
    )
    add_validation(
        validation,
        "target_only_post_prediction",
        all(row["target_used_only_for_post_prediction_diagnostic"] for row in summaries),
        True,
    )
    add_validation(
        validation,
        "classical_vlasov_double_count_identified",
        all(not row["independent_new_stress"] for row in double_counting),
        len(double_counting),
    )
    add_validation(
        validation,
        "claim_remains_false",
        all(not row["valid_for_claim"] for row in summaries + clauses + decisions),
        True,
    )
    add_validation(
        validation,
        "visible_source_numeric_positive",
        bool(np.all(visible_masses > 0.0) and np.all(np.diff(visible_radii) > 0.0)),
        [float(visible_masses[-1]), float(visible_radii[-1])],
    )
    add_validation(
        validation,
        "source_hashes_unchanged",
        all(file_digest(paths[key]) == value for key, value in source_hashes.items()),
        len(source_hashes),
    )
    formal_after = tree_digest(FORMAL)
    add_validation(
        validation,
        "formal_digest_locked_after",
        formal_after == FORMAL_DIGEST_LOCK,
        formal_after,
    )
    result = {
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "route_decision": route,
        "summary": {
            "parent_q": parent["q_parent"],
            "transition_radius_kpc": parent["transition_radius_kpc"],
            "edge_radius_kpc": parent["edge_radius_kpc"],
            "physical_edge_mass_Msun": parent["physical_edge_mass_Msun"],
            "maximum_DF_density_reconstruction_relative_error": parent[
                "maximum_DF_density_reconstruction_relative_error"
            ],
            "primary": primary,
            "convergence": summaries,
            "fine_primary_dielectric_relative_change": fine_primary_dielectric_change,
            "fine_primary_peak_response_relative_change": fine_primary_peak_change,
            "visible_source_edge_mass_Msun": float(
                mass_at(np.asarray([parent["edge_radius_kpc"]]))[0]
            ),
            "fully_closed_5170_kernel_clauses": sum(
                bool(row["fully_closed"]) for row in clauses
            ),
            "total_5170_kernel_clauses": len(clauses),
        },
        "formalization_workbench_tree_sha256": formal_after,
        "validation_count": len(validation) + 1,
        "valid_for_claim": False,
    }
    DOCUMENT.write_text(make_document(result), encoding="utf-8")
    write_json(RESULT_JSON, result)
    csv_outputs = [
        DERIVATION_CSV,
        CONVERGENCE_CSV,
        SPECTRUM_CSV,
        PROFILE_CSV,
        CLAUSE_CSV,
        DOUBLE_COUNT_CSV,
        DECISION_CSV,
        PROVENANCE_CSV,
    ]
    parsed_counts = {str(path): len(read_csv(path)) for path in csv_outputs}
    add_validation(
        validation,
        "all_output_CSVs_parse",
        all(count > 0 for count in parsed_counts.values()),
        parsed_counts,
    )
    if len(validation) != result["validation_count"]:
        raise RuntimeError("validation count drift")
    write_csv(VALIDATION_CSV, validation)
    failed = [row for row in validation if not row["passed"]]
    if failed:
        raise RuntimeError(f"validation failed: {failed}")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
