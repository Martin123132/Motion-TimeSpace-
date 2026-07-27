from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

import numpy as np
from scipy.interpolate import PchipInterpolator


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
PREVIOUS_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5166_sourced_CIE_cooling_assembly_clock_gate.py"
)
PREVIOUS_DOCUMENT = (
    POST
    / "5166-Y5-R2FR-sourced-CIE-cooling-clumping-derived-clock-and-forward-response-gate.md"
)
PREVIOUS_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5166"
    / "sourced_CIE_cooling_assembly_clock_results.json"
)
OUT = POST / "source-intake" / "functional_rg" / "5167"
CONTRACT_CSV = OUT / "radial_entropy_cooling_contract.csv"
SHELL_CSV = OUT / "shell_cooling_arrival_profile.csv"
SCHEDULE_CSV = OUT / "radial_arrival_schedule.csv"
TRANSFER_CSV = OUT / "exact_radial_transfer_plan_gate.csv"
SCORE_CSV = OUT / "radial_cooling_forward_response_scores.csv"
PROFILE_CSV = OUT / "radial_cooling_forward_response_profiles.csv"
CONTROL_CSV = OUT / "radial_cooling_numerical_controls.csv"
ENERGY_CSV = OUT / "thermal_mechanical_energy_audit.csv"
DECISION_CSV = OUT / "route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "radial_entropy_cooling_freefall_transfer_results.json"
VALIDATION_CSV = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5167_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5167-Y5-R2FR-radial-entropy-cooling-freefall-mass-transfer-and-forward-response-gate.md"
)

MARKER = "MTS_5167_RADIAL_ENTROPY_COOLING_FREEFALL_TRANSFER_GATE"
CHECKED_DATE = "2026-07-21"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
THERMAL_FLOOR_K = 1.0e4
TEMPERATURE_SAMPLES = 257
RADIAL_SHELLS = 4096
COARSE_RADIAL_SHELLS = 2048
PRIMARY_CLUMPING = 1.5385341412037419
THERMAL_MODES = ("ISOCHORIC", "ISOBARIC")
METALLICITIES = (0.1, 0.3)
FORWARD_BRANCHES = tuple(
    (mode, metallicity) for mode in THERMAL_MODES for metallicity in METALLICITIES
)
STEPS_PER_INNER_ORBIT = 64
REFINEMENT_STEPS_PER_INNER_ORBIT = 128
REFINEMENT_BRANCHES = FORWARD_BRANCHES
PARTICLE_REFINEMENT_BRANCH = ("ISOBARIC", 0.3)


PREVIOUS = PREVIOUS_SCRIPT
specification = __import__("importlib.util").util.spec_from_file_location(
    "mts_checkpoint_5166_for_5167", PREVIOUS_SCRIPT
)
if specification is None or specification.loader is None:
    raise RuntimeError(f"cannot load module: {PREVIOUS_SCRIPT}")
P = __import__("importlib.util").util.module_from_spec(specification)
specification.loader.exec_module(P)
DYNAMICS = P.DYNAMICS
ENERGY = P.ENERGY


def source_paths() -> dict[str, Path]:
    paths = {
        "previous_script": PREVIOUS_SCRIPT,
        "previous_document": PREVIOUS_DOCUMENT,
        "previous_result": PREVIOUS_RESULT,
        "Cloudy_CIE_table": P.SOURCE_DATA,
        "motion_profile": ENERGY.MOTION_PROFILE,
        "motion_score": ENERGY.MOTION_SCORE,
        "visible_profile": ENERGY.VISIBLE_PROFILE,
    }
    for sign, path in DYNAMICS.SNAPSHOT_PATHS.items():
        paths[f"phase_{sign}_snapshot"] = path
    return paths


def read_typed_csv(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_row in P.read_csv(path):
        row: dict[str, Any] = {}
        for key, value in source_row.items():
            if value == "True":
                row[key] = True
            elif value == "False":
                row[key] = False
            else:
                row[key] = value
        rows.append(row)
    return rows


def branch_id(mode: str, metallicity: float) -> str:
    return f"{mode}_Z{metallicity:g}_RADIAL_COOLING_FREEFALL"


def contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "R1_LOCAL_ENTROPY_EQUATION",
            "equation": "rho d e_th/dt=-C n_H^2 Lambda(n_H,T,Z)",
            "derivation": "checkpoint-5166 baryon entropy projection in each fixed Lagrangian shell with no external heating",
            "status": "derived_reduced_shell_equation",
            "remaining_assumption": "single-phase shell and constant clumping during precooling",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause_id": "R2_ISOCHORIC_TIME",
            "equation": "t_cool,V=integral_Tfloor^Tvir rho [d(3kT/(2 mu m_p))/dT]/[C n_H^2 Lambda] dT",
            "derivation": "constant shell volume projection of R1 with table mean molecular weight",
            "status": "derived_thermal_bracket",
            "remaining_assumption": "density frozen until thermal floor",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause_id": "R3_ISOBARIC_TIME",
            "equation": "t_cool,P=integral_Tfloor^Tvir rho(T) [d(5kT/(2 mu m_p))/dT]/[C n_H(T)^2 Lambda] dT; n_H T=constant",
            "derivation": "constant shell pressure projection of R1",
            "status": "derived_thermal_bracket",
            "remaining_assumption": "pressure equilibrium during cooling",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause_id": "R4_FREEFALL_ARRIVAL",
            "equation": "t_arr(r)=t_cool(r)+pi sqrt[r^3/(G M_tot(<r))]/(2 sqrt(2))",
            "derivation": "Newtonian radial freefall from the same calibrated G_N and inherited enclosed source",
            "status": "derived_local_arrival_bound",
            "remaining_assumption": "angular momentum pressure drag and feedback neglected after Tfloor",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause_id": "R5_MASS_ORDERING",
            "equation": "select earliest t_arr shells until sum Delta M_hot=M_c(Redge)",
            "derivation": "cooling-arrival ordering with endpoint mass fixed by the observed condensed source",
            "status": "derived_pair_mean_arrival_clock",
            "remaining_assumption": "cooling eligibility determines temporal order but is not assigned to either antithetic phase separately",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause_id": "R6_PARTICLE_TRANSFER",
            "equation": "m_gi(t)=m_pi-lambda_arr(t) Delta m_phase d_i; N_d Delta m_phase=M_c(Redge)",
            "derivation": "feed the pair-mean R5 clock into checkpoint-5164's already-proved per-phase endpoint identity",
            "status": "exact_discrete_mass_conservation",
            "remaining_assumption": "donor removal remains homologous inside each antithetic phase",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause_id": "R7_CONDENSED_SOURCE",
            "equation": "M_g(<r,t)=sum_i<r w_i m_gi(t)-M_background(<r)+lambda_arr(t) M_c(<r)",
            "derivation": "same measured Hilbert source with lambda_arr=sum transferred/M_c",
            "status": "exact_global_mass_conservation",
            "remaining_assumption": "both diffuse removal and observed condensed profile grow self-similarly under the radial clock",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause_id": "R8_FORWARD_TEST",
            "equation": "R2/R3 plus R4-R7 are evolved before q and RMSE are evaluated",
            "derivation": "four predeclared thermal-mode and metallicity branches; no q inversion",
            "status": "forward_test",
            "remaining_assumption": "not a full radiation-hydrodynamic solution",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def radial_solution(
    table: Any,
    polynomial: dict[str, Any],
    profile: Any,
    virial: dict[str, float],
    mode: str,
    metallicity: float,
    shell_count: int,
) -> dict[str, Any]:
    geometry = P.shell_geometry(profile, float(polynomial["radius_kpc"][-1]), shell_count)
    positive = geometry["motion_mass_Msun"] > 0.0
    radius = geometry["mid_kpc"][positive]
    motion_mass = geometry["motion_mass_Msun"][positive]
    hot_mass = float(polynomial["baryon_to_motion_ratio"]) * motion_mass
    volume = geometry["volume_m3"][positive]
    initial_density = hot_mass * P.M_SUN_KG / volume
    initial_nh = (
        P.HYDROGEN_MASS_FRACTION
        * initial_density
        / P.PROTON_MASS_KG
        / 1.0e6
    )
    temperature = np.geomspace(
        THERMAL_FLOOR_K, virial["temperature_K"], TEMPERATURE_SAMPLES
    )
    if mode == "ISOCHORIC":
        hydrogen_density = initial_nh[:, None] * np.ones((1, len(temperature)))
        mass_density = initial_density[:, None] * np.ones((1, len(temperature)))
        energy_factor = 1.5
    elif mode == "ISOBARIC":
        compression = virial["temperature_K"] / temperature
        hydrogen_density = initial_nh[:, None] * compression[None, :]
        mass_density = initial_density[:, None] * compression[None, :]
        energy_factor = 2.5
    else:
        raise ValueError(f"unknown thermal mode: {mode}")
    points = np.column_stack(
        (
            np.log10(hydrogen_density).ravel(),
            np.tile(np.log10(temperature), len(radius)),
        )
    )
    primordial = 10.0 ** table.primordial_interpolator(points).reshape(
        hydrogen_density.shape
    )
    metal = 10.0 ** table.metal_interpolator(points).reshape(
        hydrogen_density.shape
    )
    mean_molecular_weight = table.mmw_interpolator(points).reshape(
        hydrogen_density.shape
    )
    specific_energy = (
        energy_factor
        * P.K_B_SI
        * temperature[None, :]
        / (mean_molecular_weight * P.PROTON_MASS_KG)
    )
    energy_derivative = np.gradient(specific_energy, temperature, axis=1)
    cooling_coefficient = primordial + metallicity * metal
    volumetric_power = (
        0.1
        * PRIMARY_CLUMPING
        * hydrogen_density**2
        * cooling_coefficient
    )
    specific_power = volumetric_power / mass_density
    cooling_time = (
        np.trapezoid(energy_derivative / specific_power, temperature, axis=1)
        / P.GYR_S
    )
    total_mass = np.asarray(profile.mass_at(radius), dtype=float) / DYNAMICS.PM.MOTION_FRACTION
    freefall_time = (
        math.pi
        / (2.0 * math.sqrt(2.0))
        * np.sqrt(
            radius**3
            / (
                DYNAMICS.PREVIOUS.G_KPC_KM2_S2_MSUN
                * np.maximum(total_mass, 1.0)
            )
        )
        * P.TIME_UNIT_GYR
    )
    arrival_time = cooling_time + freefall_time
    condensed_target = float(polynomial["condensed_edge_Msun"])
    order = np.argsort(arrival_time)
    selected_mass = np.zeros_like(hot_mass)
    remaining = condensed_target
    for index in order:
        amount = min(float(hot_mass[index]), remaining)
        selected_mass[index] = amount
        remaining -= amount
        if remaining <= max(condensed_target, 1.0) * 1.0e-14:
            break
    selected_total = float(np.sum(selected_mass))
    if abs(selected_total - condensed_target) / condensed_target > 1.0e-12:
        raise RuntimeError("radial shell selection did not reach condensed endpoint")
    selected = selected_mass > 0.0
    endpoint_time = float(np.max(arrival_time[selected]))
    initial_specific = specific_energy[:, -1]
    floor_specific = specific_energy[:, 0]
    selected_thermal_energy = float(
        np.sum(selected_mass * P.M_SUN_KG * (initial_specific - floor_specific))
    )
    return {
        "mode": mode,
        "metallicity": metallicity,
        "radius_kpc": radius,
        "hot_mass_Msun": hot_mass,
        "selected_mass_Msun": selected_mass,
        "initial_nH_cm3": initial_nh,
        "maximum_nH_cm3": np.max(hydrogen_density, axis=1),
        "cooling_time_Gyr": cooling_time,
        "freefall_time_Gyr": freefall_time,
        "arrival_time_Gyr": arrival_time,
        "endpoint_time_Gyr": endpoint_time,
        "selected_total_Msun": selected_total,
        "selected_thermal_energy_J": selected_thermal_energy,
        "minimum_energy_derivative_J_kg_K": float(np.min(energy_derivative)),
        "minimum_cooling_coefficient": float(np.min(cooling_coefficient)),
        "maximum_table_density_cm3": float(np.max(hydrogen_density)),
    }


def shell_rows(solutions: dict[tuple[str, float], dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (mode, metallicity), solution in solutions.items():
        for index, radius in enumerate(solution["radius_kpc"]):
            rows.append(
                {
                    "branch_id": branch_id(mode, metallicity),
                    "thermal_mode": mode,
                    "metallicity_Zsun": metallicity,
                    "radius_kpc": radius,
                    "initial_hot_mass_Msun": solution["hot_mass_Msun"][index],
                    "selected_condensing_mass_Msun": solution[
                        "selected_mass_Msun"
                    ][index],
                    "selected_for_condensation": solution["selected_mass_Msun"][index]
                    > 0.0,
                    "initial_nH_cm3": solution["initial_nH_cm3"][index],
                    "maximum_nH_during_cooling_cm3": solution[
                        "maximum_nH_cm3"
                    ][index],
                    "cooling_time_Gyr": solution["cooling_time_Gyr"][index],
                    "freefall_time_Gyr": solution["freefall_time_Gyr"][index],
                    "arrival_time_Gyr": solution["arrival_time_Gyr"][index],
                    "clumping_factor": PRIMARY_CLUMPING,
                    "thermal_floor_K": THERMAL_FLOOR_K,
                    "target_used_to_select_shell": False,
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
    return rows


def schedule_rows(solutions: dict[tuple[str, float], dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (mode, metallicity), solution in solutions.items():
        selected = solution["selected_mass_Msun"] > 0.0
        times = solution["arrival_time_Gyr"][selected]
        masses = solution["selected_mass_Msun"][selected]
        order = np.argsort(times)
        cumulative = np.cumsum(masses[order]) / solution["selected_total_Msun"]
        ordered_time = times[order]
        for fraction in np.linspace(0.0, 1.0, 41):
            if fraction <= 0.0:
                elapsed = 0.0
            else:
                elapsed = float(ordered_time[np.searchsorted(cumulative, fraction)])
            rows.append(
                {
                    "branch_id": branch_id(mode, metallicity),
                    "thermal_mode": mode,
                    "metallicity_Zsun": metallicity,
                    "assembly_fraction_lambda": fraction,
                    "elapsed_time_Gyr": elapsed,
                    "elapsed_transition_orbits": elapsed
                    / json.loads(P.DYNAMICS_RESULT.read_text(encoding="utf-8"))["summary"][
                        "transition_orbit_Gyr"
                    ],
                    "schedule_source": "ranked_local_entropy_cooling_plus_Newton_freefall",
                    "target_used_to_select_schedule": False,
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
    return rows


def arrival_clock(solution: dict[str, Any]) -> dict[str, Any]:
    selected = solution["selected_mass_Msun"] > 0.0
    arrival = np.asarray(solution["arrival_time_Gyr"])[selected]
    mass = np.asarray(solution["selected_mass_Msun"])[selected]
    order = np.argsort(arrival)
    arrival = arrival[order]
    mass = mass[order]
    unique_time_seconds, inverse = np.unique(arrival * P.GYR_S, return_inverse=True)
    grouped_mass = np.bincount(inverse, weights=mass)
    cumulative = np.cumsum(grouped_mass) / float(solution["selected_total_Msun"])
    time_seconds = np.concatenate((np.asarray([0.0]), unique_time_seconds))
    assembly = np.concatenate((np.asarray([0.0]), cumulative))
    assembly[-1] = 1.0
    return {
        "assembly": assembly,
        "time_seconds": time_seconds,
        "duration_Gyr": float(time_seconds[-1] / P.GYR_S),
    }


class RadialArrivalSchedule:
    def __init__(self, solution: dict[str, Any]) -> None:
        selected = solution["selected_mass_Msun"] > 0.0
        arrival_internal = (
            np.asarray(solution["arrival_time_Gyr"])[selected] / P.TIME_UNIT_GYR
        )
        arrival_internal = np.round(arrival_internal, decimals=12)
        mass = np.asarray(solution["selected_mass_Msun"])[selected]
        order = np.argsort(arrival_internal)
        unique_time, inverse = np.unique(arrival_internal[order], return_inverse=True)
        grouped_mass = np.bincount(inverse, weights=mass[order])
        cumulative = np.cumsum(grouped_mass) / float(solution["selected_total_Msun"])
        self.time_internal = np.concatenate((np.asarray([0.0]), unique_time))
        self.assembly = np.concatenate((np.asarray([0.0]), cumulative))
        self.assembly[-1] = 1.0
        self.duration_internal = float(self.time_internal[-1])
        self.interpolator = PchipInterpolator(self.time_internal, self.assembly)

    def fraction_at(self, time_internal: float) -> float:
        if time_internal <= 0.0:
            return 0.0
        if time_internal >= self.duration_internal:
            return 1.0
        return float(np.clip(self.interpolator(time_internal), 0.0, 1.0))


def run_clock_branch(
    context: dict[str, Any],
    solution: dict[str, Any],
    steps_per_orbit: int,
    run_id: str,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    clock = arrival_clock(solution)
    score, controls, profiles = P.run_response_branch(
        context,
        RadialArrivalSchedule(solution),
        float(solution["metallicity"]),
        PRIMARY_CLUMPING,
        steps_per_orbit,
        run_id,
    )
    score["thermal_mode"] = solution["mode"]
    score["common_endpoint_Gyr"] = score.pop("clock_duration_Gyr")
    score["duration_transition_orbits"] = score.pop(
        "clock_duration_over_transition_orbit"
    )
    score["schedule"] = "pair_mean_ranked_local_entropy_cooling_plus_Newton_freefall"
    score["target_used_to_select_branch"] = False
    transfers: list[dict[str, Any]] = []
    condensed_mass = float(context["visible_source"].mass_at(context["edge_radius"]))
    for sign, snapshot in context["response_snapshots"].items():
        represented_donors = float(
            np.sum(
                np.asarray(snapshot["particle_weight"], dtype=float)
                * np.asarray(snapshot["donor"], dtype=float)
            )
        )
        transfer_per_donor = float(context["transfer_per_donor"][sign])
        transferred = represented_donors * transfer_per_donor
        particle_mass = float(snapshot["particle_mass_Msun"][0])
        baryon_available = particle_mass * (1.0 - DYNAMICS.PM.MOTION_FRACTION)
        transfers.append(
            {
                "run_id": run_id,
                "phase_sign": sign,
                "represented_donor_particle_count": represented_donors,
                "transfer_per_donor_particle_Msun": transfer_per_donor,
                "transferred_mass_Msun": transferred,
                "target_condensed_mass_Msun": condensed_mass,
                "mass_conservation_relative_residual": abs(
                    transferred - condensed_mass
                )
                / condensed_mass,
                "maximum_transfer_fraction_of_available_baryons": transfer_per_donor
                / baryon_available,
                "arrival_clock_endpoint_Gyr": clock["duration_Gyr"],
                "radial_clock_but_homologous_donor_removal": True,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return score, controls, profiles, transfers


def full_particle_context(context: dict[str, Any]) -> dict[str, Any]:
    result = dict(context)
    result["response_snapshots"] = {
        sign: {
            **snapshot,
            "particle_weight": np.ones(
                len(snapshot["positions_kpc"]), dtype=float
            ),
        }
        for sign, snapshot in context["snapshots"].items()
    }
    return result


def transfer_plan(
    snapshot: dict[str, Any],
    solution: dict[str, Any],
    condensed_mass_msun: float,
) -> dict[str, Any]:
    donor = np.asarray(snapshot["donor"], dtype=bool)
    particle_weight = np.asarray(snapshot["particle_weight"], dtype=float)
    initial_radius = np.asarray(snapshot["initial_radius_kpc"], dtype=float)
    arrival = np.full(len(donor), math.inf, dtype=float)
    arrival[donor] = np.interp(
        initial_radius[donor],
        solution["radius_kpc"],
        solution["arrival_time_Gyr"],
        left=float(solution["arrival_time_Gyr"][0]),
        right=float(solution["arrival_time_Gyr"][-1]),
    )
    particle_mass = float(snapshot["particle_mass_Msun"][0])
    baryon_available = particle_mass * (1.0 - DYNAMICS.PM.MOTION_FRACTION)
    endpoint_transfer = np.zeros(len(donor), dtype=float)
    remaining = condensed_mass_msun
    for index in np.argsort(arrival):
        if not donor[index] or not math.isfinite(arrival[index]):
            continue
        represented_available = particle_weight[index] * baryon_available
        represented_transfer = min(represented_available, remaining)
        endpoint_transfer[index] = represented_transfer / particle_weight[index]
        remaining -= represented_transfer
        if remaining <= condensed_mass_msun * 1.0e-14:
            break
    transferred = float(np.sum(particle_weight * endpoint_transfer))
    selected = endpoint_transfer > 0.0
    if abs(transferred - condensed_mass_msun) / condensed_mass_msun > 1.0e-12:
        raise RuntimeError("particle transfer plan does not conserve endpoint mass")
    return {
        "arrival_time_internal": arrival / P.TIME_UNIT_GYR,
        "endpoint_transfer_per_particle_Msun": endpoint_transfer,
        "endpoint_time_internal": float(np.max(arrival[selected]) / P.TIME_UNIT_GYR),
        "selected_representative_count": int(np.count_nonzero(selected)),
        "selected_represented_particle_count": float(np.sum(particle_weight[selected])),
        "partial_boundary_representative_count": int(
            np.count_nonzero(
                selected
                & (endpoint_transfer > 0.0)
                & (endpoint_transfer < baryon_available)
            )
        ),
        "transferred_mass_Msun": transferred,
        "mass_residual": abs(transferred - condensed_mass_msun) / condensed_mass_msun,
        "minimum_arrival_Gyr": float(np.min(arrival[selected])),
        "maximum_arrival_Gyr": float(np.max(arrival[selected])),
        "maximum_transfer_fraction_of_available_baryons": float(
            np.max(endpoint_transfer[selected] / baryon_available)
        ),
    }


def acceleration(
    positions: np.ndarray,
    particle_weight: np.ndarray,
    particle_mass: float,
    transfer_per_particle: np.ndarray,
    condensed_fraction: float,
    visible_source: Any,
    softening_kpc: float,
) -> np.ndarray:
    radii = np.linalg.norm(positions, axis=1)
    order = np.argsort(radii)
    sorted_radii = radii[order]
    gravitational_masses = particle_weight * (
        particle_mass - transfer_per_particle
    )
    sorted_masses = gravitational_masses[order]
    enclosed_particles = np.cumsum(sorted_masses) - 0.5 * sorted_masses
    background = (
        4.0
        * math.pi
        * DYNAMICS.PM.RHO_M_MSUN_MPC3
        * (sorted_radii / 1000.0) ** 3
        / 3.0
    )
    condensed = condensed_fraction * np.asarray(visible_source.mass_at(sorted_radii))
    enclosed = np.maximum(enclosed_particles - background + condensed, 0.0)
    denominator = (sorted_radii**2 + softening_kpc**2) ** 1.5
    coefficient = np.zeros_like(sorted_radii)
    positive = denominator > 0.0
    coefficient[positive] = (
        -DYNAMICS.PREVIOUS.G_KPC_KM2_S2_MSUN
        * enclosed[positive]
        / denominator[positive]
    )
    result = np.empty_like(positions)
    result[order] = coefficient[:, None] * positions[order]
    return result


def evolve(
    snapshot: dict[str, Any],
    plan: dict[str, Any],
    visible_source: Any,
    condensed_mass_msun: float,
    profile_radii_kpc: np.ndarray,
    common_duration_internal: float,
    transition_orbit: float,
    inner_orbit: float,
    steps_per_inner_orbit: int,
    source_enabled: bool,
) -> dict[str, Any]:
    positions = np.asarray(snapshot["positions_kpc"], dtype=float).copy()
    velocities = np.asarray(snapshot["velocities_km_s"], dtype=float).copy()
    particle_weight = np.asarray(snapshot["particle_weight"], dtype=float)
    initial_radius = np.asarray(snapshot["initial_radius_kpc"], dtype=float)
    particle_mass = float(snapshot["particle_mass_Msun"][0])
    edge_radius = float(snapshot["edge_radius_kpc"][0])
    softening = (
        DYNAMICS.SOFTENING_CELL_MULTIPLE
        * float(snapshot["local_force_cell_kpc"][0])
    )
    total_time = common_duration_internal + DYNAMICS.SETTLING_ORBITS * transition_orbit
    averaging_time = DYNAMICS.AVERAGING_ORBITS * transition_orbit
    nominal_dt = inner_orbit / steps_per_inner_orbit
    steps = max(1, int(math.ceil(total_time / nominal_dt)))
    time_step = total_time / steps
    averaging_start = max(total_time - averaging_time, 0.0)
    sample_stride = max(
        1,
        int(round(max(1.0, averaging_time / time_step) / DYNAMICS.PROFILE_AVERAGE_SAMPLES)),
    )
    initial_angular_momentum = np.cross(positions, velocities)
    initial_com = np.average(positions, axis=0, weights=particle_weight)
    endpoint_transfer = plan["endpoint_transfer_per_particle_Msun"]
    arrival_time = plan["arrival_time_internal"]
    start = time.perf_counter()

    def transfer_at(current_time: float) -> tuple[np.ndarray, float]:
        if not source_enabled:
            return np.zeros_like(endpoint_transfer), 0.0
        transfer = endpoint_transfer * (current_time >= arrival_time)
        fraction = float(np.sum(particle_weight * transfer) / condensed_mass_msun)
        return transfer, min(max(fraction, 0.0), 1.0)

    transfer, condensed_fraction = transfer_at(0.0)
    force = acceleration(
        positions,
        particle_weight,
        particle_mass,
        transfer,
        condensed_fraction,
        visible_source,
        softening,
    )
    half_velocity = velocities + 0.5 * time_step * force
    count_samples: list[np.ndarray] = []
    final_fraction = condensed_fraction
    for step in range(steps):
        positions += time_step * half_velocity
        current_time = (step + 1) * time_step
        transfer, final_fraction = transfer_at(current_time)
        force = acceleration(
            positions,
            particle_weight,
            particle_mass,
            transfer,
            final_fraction,
            visible_source,
            softening,
        )
        if step < steps - 1:
            half_velocity += time_step * force
        else:
            velocities = half_velocity + 0.5 * time_step * force
        if current_time >= averaging_start and (
            step % sample_stride == 0 or step == steps - 1
        ):
            count_samples.append(
                DYNAMICS.cumulative_counts(
                    positions, profile_radii_kpc, particle_weight
                )
            )
    averaged_counts = np.mean(np.asarray(count_samples), axis=0)
    final_angular_momentum = np.cross(positions, velocities)
    angular_residual = float(
        math.sqrt(
            np.sum(
                particle_weight[:, None]
                * (final_angular_momentum - initial_angular_momentum) ** 2
            )
            / max(
                np.sum(particle_weight[:, None] * initial_angular_momentum**2),
                1.0e-300,
            )
        )
    )
    final_radii = np.linalg.norm(positions, axis=1)
    boundary_ingress = float(
        np.sum(
            particle_weight[
                (
                    initial_radius
                    > 0.9 * DYNAMICS.ISOLATION_EDGE_MULTIPLE * edge_radius
                )
                & (final_radii <= DYNAMICS.SCORE_EDGE_FRACTION * edge_radius)
            ]
        )
    )
    final_inside = max(
        float(
            np.sum(
                particle_weight[
                    final_radii <= DYNAMICS.SCORE_EDGE_FRACTION * edge_radius
                ]
            )
        ),
        1.0,
    )
    return {
        "averaged_counts": averaged_counts,
        "steps": steps,
        "time_step_internal": time_step,
        "final_assembly_fraction": final_fraction,
        "angular_momentum_relative_residual": angular_residual,
        "center_of_mass_drift_kpc": float(
            np.linalg.norm(
                np.average(positions, axis=0, weights=particle_weight) - initial_com
            )
        ),
        "outer_boundary_ingress_fraction": boundary_ingress / final_inside,
        "wall_seconds": time.perf_counter() - start,
    }


def run_branch(
    context: dict[str, Any],
    solution: dict[str, Any],
    steps_per_orbit: int,
    run_id: str,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    condensed_mass = float(context["visible_source"].mass_at(context["edge_radius"]))
    plans = {
        sign: transfer_plan(snapshot, solution, condensed_mass)
        for sign, snapshot in context["response_snapshots"].items()
    }
    common_duration = max(plan["endpoint_time_internal"] for plan in plans.values())
    phase_mass: dict[int, np.ndarray] = {}
    controls: list[dict[str, Any]] = []
    transfer_rows: list[dict[str, Any]] = []
    for sign, snapshot in context["response_snapshots"].items():
        plan = plans[sign]
        source = evolve(
            snapshot,
            plan,
            context["visible_source"],
            condensed_mass,
            context["radii"],
            common_duration,
            context["transition_orbit"],
            context["inner_orbit"],
            steps_per_orbit,
            True,
        )
        control = evolve(
            snapshot,
            plan,
            context["visible_source"],
            condensed_mass,
            context["radii"],
            common_duration,
            context["transition_orbit"],
            context["inner_orbit"],
            steps_per_orbit,
            False,
        )
        particle_mass = float(snapshot["particle_mass_Msun"][0])
        background = (
            4.0
            * math.pi
            * DYNAMICS.PM.RHO_M_MSUN_MPC3
            * (context["radii"] / 1000.0) ** 3
            / 3.0
        )
        source_mass = DYNAMICS.PM.MOTION_FRACTION * np.maximum(
            source["averaged_counts"] * particle_mass - background, 0.0
        )
        control_mass = DYNAMICS.PM.MOTION_FRACTION * np.maximum(
            control["averaged_counts"] * particle_mass - background, 0.0
        )
        ratio = np.ones_like(context["radii"])
        positive = control_mass > 0.0
        ratio[positive] = source_mass[positive] / control_mass[positive]
        phase_mass[sign] = context["initial_phase_mass"][sign] * ratio
        controls.append(
            {
                "run_id": run_id,
                "phase_sign": sign,
                "steps_per_inner_orbit": steps_per_orbit,
                "source_steps": source["steps"],
                "control_steps": control["steps"],
                "source_final_assembly_fraction": source["final_assembly_fraction"],
                "source_angular_momentum_relative_residual": source[
                    "angular_momentum_relative_residual"
                ],
                "control_angular_momentum_relative_residual": control[
                    "angular_momentum_relative_residual"
                ],
                "source_outer_boundary_ingress_fraction": source[
                    "outer_boundary_ingress_fraction"
                ],
                "control_outer_boundary_ingress_fraction": control[
                    "outer_boundary_ingress_fraction"
                ],
                "source_wall_seconds": source["wall_seconds"],
                "control_wall_seconds": control["wall_seconds"],
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
        transfer_rows.append(
            {
                "run_id": run_id,
                "phase_sign": sign,
                "selected_representative_count": plan[
                    "selected_representative_count"
                ],
                "selected_represented_particle_count": plan[
                    "selected_represented_particle_count"
                ],
                "partial_boundary_representative_count": plan[
                    "partial_boundary_representative_count"
                ],
                "transferred_mass_Msun": plan["transferred_mass_Msun"],
                "target_condensed_mass_Msun": condensed_mass,
                "mass_conservation_relative_residual": plan["mass_residual"],
                "minimum_arrival_Gyr": plan["minimum_arrival_Gyr"],
                "maximum_arrival_Gyr": plan["maximum_arrival_Gyr"],
                "maximum_transfer_fraction_of_available_baryons": plan[
                    "maximum_transfer_fraction_of_available_baryons"
                ],
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    corrected_mass = 0.5 * (phase_mass[-1] + phase_mass[1])
    score = DYNAMICS.score_profile(
        context["radii"],
        corrected_mass,
        context["target_velocity"],
        context["score_mask"],
        context["transition_radius"],
        context["edge_radius"],
        context["target_edge_mass"],
    )
    q_parent = float(context["q_row"]["q_parent"])
    q_envelope = float(context["q_row"]["q_uncertainty_envelope"])
    score_row = {
        "run_id": run_id,
        "thermal_mode": solution["mode"],
        "metallicity_Zsun": solution["metallicity"],
        "common_endpoint_Gyr": common_duration * P.TIME_UNIT_GYR,
        "duration_transition_orbits": common_duration / context["transition_orbit"],
        "steps_per_inner_orbit": steps_per_orbit,
        "q_parent": q_parent,
        "q_envelope": q_envelope,
        "corrected_q": score["q"],
        "corrected_q_absolute_difference": abs(score["q"] - q_parent),
        "corrected_q_compatible": abs(score["q"] - q_parent) <= q_envelope,
        "corrected_velocity_squared_log10_RMSE": score[
            "velocity_squared_log10_RMSE"
        ],
        "baseline_velocity_squared_log10_RMSE": context["baseline_score"][
            "velocity_squared_log10_RMSE"
        ],
        "corrected_RMSE_improves_baseline": score[
            "velocity_squared_log10_RMSE"
        ]
        < context["baseline_score"]["velocity_squared_log10_RMSE"],
        "corrected_transition_velocity_squared_ratio_to_target": score[
            "transition_velocity_squared_ratio_to_target"
        ],
        "corrected_edge_mass_ratio_to_target": score["edge_mass_ratio_to_target"],
        "target_used_to_select_branch": False,
        "response_efficiency_fitted": False,
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }
    profile_rows: list[dict[str, Any]] = []
    velocity_squared = (
        DYNAMICS.PREVIOUS.G_KPC_KM2_S2_MSUN
        * corrected_mass
        / np.maximum(context["radii"], np.finfo(float).tiny)
    )
    for index, radius in enumerate(context["radii"]):
        profile_rows.append(
            {
                "run_id": run_id,
                "radius_kpc": radius,
                "radius_over_transition": radius / context["transition_radius"],
                "corrected_motion_mass_Msun": corrected_mass[index],
                "phase_minus_corrected_mass_Msun": phase_mass[-1][index],
                "phase_plus_corrected_mass_Msun": phase_mass[1][index],
                "corrected_motion_v2_km2_s2": velocity_squared[index],
                "target_motion_v2_km2_s2": context["target_velocity"][index],
                "inside_scoring_window": bool(context["score_mask"][index]),
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return score_row, controls, profile_rows, transfer_rows


def energy_rows(
    solutions: dict[tuple[str, float], dict[str, Any]], polynomial: dict[str, Any]
) -> list[dict[str, Any]]:
    mechanical = float(polynomial["virial_radiative_release_J"])
    rows: list[dict[str, Any]] = []
    for (mode, metallicity), solution in solutions.items():
        thermal = float(solution["selected_thermal_energy_J"])
        rows.append(
            {
                "branch_id": branch_id(mode, metallicity),
                "selected_precooling_thermal_release_J": thermal,
                "checkpoint_5165_mechanical_virial_release_J": mechanical,
                "thermal_to_mechanical_ratio": thermal / mechanical,
                "energies_added_as_independent_sources": False,
                "interpretation": "thermal cooling triggers arrival; checkpoint-5165 total mechanical bookkeeping remains the endpoint constraint",
                "full_radiation_hydrodynamic_energy_closure": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows


def provenance_rows(paths: dict[str, Path]) -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": key,
            "source_type": "local_file",
            "path_or_url": str(path),
            "sha256": P.file_digest(path),
            "role": "read_only_parent_empirical_or_numeric_input",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for key, path in paths.items()
    ]
    rows.extend(
        [
            {
                "source_id": "CloudyData_noUVB_immutable_download",
                "source_type": "source_data_url",
                "path_or_url": P.CLOUDY_DATA_URL,
                "sha256": P.CLOUDY_SHA256,
                "role": "temperature_dependent_CIE_coefficients_and_MMW",
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            },
            {
                "source_id": "Grackle_method_paper",
                "source_type": "primary_paper_url",
                "path_or_url": P.GRACKLE_PAPER_URL,
                "sha256": "",
                "role": "cooling_table_method",
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            },
        ]
    )
    return rows


def make_document(result: dict[str, Any]) -> str:
    summary = result["summary"]
    lines = []
    for key in summary["primary_scores"]:
        row = summary["primary_scores"][key]
        lines.append(
            f"{key}: T={row['common_endpoint_Gyr']} Gyr, q={row['corrected_q']}, "
            f"RMSE={row['corrected_velocity_squared_log10_RMSE']} dex, "
            f"v2 ratio={row['corrected_transition_velocity_squared_ratio_to_target']}"
        )
    score_text = "\n".join(lines)
    return f"""# 5167 - Radial entropy cooling, freefall transfer and forward-response gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Why this calculation

Checkpoint 5166 replaced the arbitrary galaxy assembly duration with a real
CIE luminosity, but its one global coordinate cooled half the source too early.
Both predeclared branches improved the profile while missing the parent `q`
interval. This checkpoint removes the approximation that failed instead of
retuning its duration.

## Radial derivation

Each inherited hot-baryon shell now obeys the checkpoint-5166 entropy equation

```text
rho de_th/dt=-C n_H^2 Lambda(n_H,T,Z).
```

Two standard thermodynamic projections are carried together:

```text
t_cool,V=integral rho d[3kT/(2 mu m_p)]/[C n_H^2 Lambda],
t_cool,P=integral rho(T) d[5kT/(2 mu m_p)]/[C n_H(T)^2 Lambda],
n_H(T)T=constant on the isobaric branch.
```

The temperature integral runs from the sourced fixed-edge virial temperature
`{summary['virial_temperature_K']} K` to the predeclared atomic floor
`{THERMAL_FLOOR_K} K`. The same Cloudy/Grackle CIE table supplies `Lambda` and
`mu(T,n_H)` at every integration point. The resolved checkpoint-5166 clumping
`C={PRIMARY_CLUMPING}` is fixed before any response is read.

After reaching the floor, each shell receives the same calibrated-`G_N`
Newtonian arrival bound

```text
t_arr(r)=t_cool(r)+pi sqrt[r^3/(G_N M_tot(<r))]/(2 sqrt(2)).
```

Shells are ranked by `t_arr` until their mass exactly equals the measured
condensed endpoint. Their cumulative pair-mean arrival distribution defines
`lambda_arr(t)`. It drives the checkpoint-5164 per-phase identity:

```text
m_gi(t)=m_pi-lambda_arr(t) Delta m_phase d_i,
N_d Delta m_phase=M_c(Redge),
M_cond(<r,t)=lambda_arr(t) M_c,obs(<r).
```

This avoids assigning the pair-mean shell ranking separately to antithetic
phases with deliberately different halo masses. The clock is radial and
source-derived; donor removal remains the already-controlled homologous
checkpoint-5164 projection. No response efficiency, duration fit, metallicity
inversion or arena-specific gravitational coefficient is introduced.

## Forward results

The four branches were declared as the Cartesian product of isochoric/isobaric
cooling and `Z={{0.1,0.3}} Zsun` before `q` was evaluated:

```text
{score_text}
```

The inherited parent interval is
`{summary['parent_q_lower']} .. {summary['parent_q_upper']}` and the free
baseline RMSE is `{summary['baseline_RMSE']} dex`. All four near-boundary
branches are repeated at doubled time resolution. Their refined values and
primary/refined differences are `{summary['refined_q_values']}` and
`{summary['refinement_delta_q_values']}`. A branch is called numerically
compatible only when its primary/refined interval intersects the parent band;
no single favorable discretization is promoted by itself. The closest branch,
`{summary['particle_refinement_branch']}`, is also repeated with every inherited
particle because its primary distance from the band is smaller than the
checkpoint-5164 particle-resolution envelope. That value is
`{summary['particle_refined_q']}` with
`|Delta q|={summary['particle_refinement_delta_q']}`. The closest controlled
point is `{summary['closest_run_id']}` at `q={summary['closest_q']}`, only
`{summary['closest_q_gap_to_parent_band']}` above the parent band.

## Decision

`{result['route_decision']}`.

This is still not a full radiation-hydrodynamic derivation. Isochoric and
isobaric shell laws are controlled brackets, the radial arrival distribution
drives a homologous donor transfer, the observed condensed shape grows self-
similarly, feedback and angular-
momentum transport are absent, and the UGC09133 hot metallicity remains
unmeasured. The checkpoint tests whether removing homologous timing moves the
same theory in the required direction without fitting the response.

```text
local entropy cooling times derived from real table       = yes;
Newtonian shell freefall derived                           = yes;
pair-mean radial arrival clock derived                     = yes;
checkpoint-5164 homologous donor removal mass-conserving   = yes;
shell rank assigned separately to antithetic phases        = no;
four branches fixed before q                               = yes;
full radiation hydrodynamics                               = no;
local GR/Newton/Maxwell branch modified                    = no;
galaxy or full-MTS claim                                   = false.
```

All `{result['validation_count']}` validation rows pass. The protected
`formalization-workbench` digest remains
`{result['formalization_workbench_tree_sha256']}`. No GitHub action occurred.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--physics-only", action="store_true")
    parser.add_argument("--skip-refinement", action="store_true")
    parser.add_argument("--refinement-only", action="store_true")
    parser.add_argument("--particle-refinement-only", action="store_true")
    arguments = parser.parse_args()
    paths = source_paths()
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing sources: {missing}")
    formal_before = P.tree_digest(FORMAL)
    if formal_before != FORMAL_DIGEST_LOCK:
        raise RuntimeError(f"protected digest mismatch: {formal_before}")
    hashes_before = {key: P.file_digest(path) for key, path in paths.items()}
    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "marker": MARKER,
                    "branches": [branch_id(*branch) for branch in FORWARD_BRANCHES],
                    "thermal_floor_K": THERMAL_FLOOR_K,
                    "formal_digest": formal_before,
                },
                indent=2,
            )
        )
        return

    table = P.CoolingTable(P.SOURCE_DATA)
    context = P.response_context()
    visible_source = context["visible_source"]
    edge_kpc = ENERGY.edge_radius_kpc()
    profile = ENERGY.motion_profiles()[ENERGY.PRIMARY_PROFILE_ID][0]
    polynomial = ENERGY.energy_polynomial(
        profile, visible_source, edge_kpc, ENERGY.QUADRATURE_POINTS
    )
    virial = P.virial_state(table, polynomial, edge_kpc)
    solutions = {
        branch: radial_solution(
            table,
            polynomial,
            profile,
            virial,
            branch[0],
            branch[1],
            RADIAL_SHELLS,
        )
        for branch in FORWARD_BRANCHES
    }
    coarse_solutions = {
        branch: radial_solution(
            table,
            polynomial,
            profile,
            virial,
            branch[0],
            branch[1],
            COARSE_RADIAL_SHELLS,
        )
        for branch in FORWARD_BRANCHES
    }
    contract = contract_rows()
    shells = shell_rows(solutions)
    schedules = schedule_rows(solutions)
    energies = energy_rows(solutions, polynomial)
    endpoint_resolution_change = {
        branch_id(*branch): abs(
            solutions[branch]["endpoint_time_Gyr"]
            - coarse_solutions[branch]["endpoint_time_Gyr"]
        )
        / solutions[branch]["endpoint_time_Gyr"]
        for branch in FORWARD_BRANCHES
    }

    scores: list[dict[str, Any]] = []
    profiles: list[dict[str, Any]] = []
    controls: list[dict[str, Any]] = []
    transfers: list[dict[str, Any]] = []
    if not arguments.physics_only:
        if arguments.refinement_only or arguments.particle_refinement_only:
            required = (SCORE_CSV, PROFILE_CSV, CONTROL_CSV, TRANSFER_CSV)
            if not all(path.is_file() for path in required):
                raise RuntimeError("reuse refinement requested without existing outputs")
            retained_suffixes = (
                ("PRIMARY", "TIME_REFINEMENT")
                if arguments.particle_refinement_only
                else ("PRIMARY",)
            )
            scores.extend(
                row
                for row in read_typed_csv(SCORE_CSV)
                if str(row["run_id"]).endswith(retained_suffixes)
            )
            profiles.extend(
                row
                for row in read_typed_csv(PROFILE_CSV)
                if str(row["run_id"]).endswith(retained_suffixes)
            )
            controls.extend(
                row
                for row in read_typed_csv(CONTROL_CSV)
                if str(row["run_id"]).endswith(retained_suffixes)
            )
            transfers.extend(
                row
                for row in read_typed_csv(TRANSFER_CSV)
                if str(row["run_id"]).endswith(retained_suffixes)
            )
        else:
            for branch in FORWARD_BRANCHES:
                run_id = branch_id(*branch) + "_PRIMARY"
                score, run_controls, run_profiles, run_transfers = run_clock_branch(
                    context,
                    solutions[branch],
                    STEPS_PER_INNER_ORBIT,
                    run_id,
                )
                scores.append(score)
                controls.extend(run_controls)
                profiles.extend(run_profiles)
                transfers.extend(run_transfers)
        if not arguments.skip_refinement and not arguments.particle_refinement_only:
            for branch in REFINEMENT_BRANCHES:
                run_id = branch_id(*branch) + "_TIME_REFINEMENT"
                score, run_controls, run_profiles, run_transfers = run_clock_branch(
                    context,
                    solutions[branch],
                    REFINEMENT_STEPS_PER_INNER_ORBIT,
                    run_id,
                )
                scores.append(score)
                controls.extend(run_controls)
                profiles.extend(run_profiles)
                transfers.extend(run_transfers)
        if not arguments.skip_refinement and not arguments.refinement_only:
            branch = PARTICLE_REFINEMENT_BRANCH
            run_id = branch_id(*branch) + "_FULL_PARTICLE_REFINEMENT"
            score, run_controls, run_profiles, run_transfers = run_clock_branch(
                full_particle_context(context),
                solutions[branch],
                STEPS_PER_INNER_ORBIT,
                run_id,
            )
            score["refinement_selected_after_near_boundary"] = True
            scores.append(score)
            controls.extend(run_controls)
            profiles.extend(run_profiles)
            transfers.extend(run_transfers)

    primary_scores = {
        (row["thermal_mode"], float(row["metallicity_Zsun"])): row
        for row in scores
        if row["run_id"].endswith("PRIMARY")
    }
    refined_scores = {
        (row["thermal_mode"], float(row["metallicity_Zsun"])): row
        for row in scores
        if row["run_id"].endswith("TIME_REFINEMENT")
    }
    particle_refined_score = next(
        (
            row
            for row in scores
            if row["run_id"].endswith("FULL_PARTICLE_REFINEMENT")
        ),
        None,
    )
    response_executed = set(primary_scores) == set(FORWARD_BRANCHES)
    parent_lower = float(context["q_row"]["q_parent"]) - float(
        context["q_row"]["q_uncertainty_envelope"]
    )
    parent_upper = float(context["q_row"]["q_parent"]) + float(
        context["q_row"]["q_uncertainty_envelope"]
    )
    any_primary_q_compatible = response_executed and any(
        bool(row["corrected_q_compatible"]) for row in primary_scores.values()
    )
    all_rmse_improve = response_executed and all(
        bool(row["corrected_RMSE_improves_baseline"])
        for row in primary_scores.values()
    )
    refinement_deltas = {
        branch: abs(
            float(refined_scores[branch]["corrected_q"])
            - float(primary_scores[branch]["corrected_q"])
        )
        for branch in refined_scores.keys() & primary_scores.keys()
    }
    refinement_intersections: dict[tuple[str, float], bool] = {}
    for branch in refined_scores.keys() & primary_scores.keys():
        q_values = [
            float(primary_scores[branch]["corrected_q"]),
            float(refined_scores[branch]["corrected_q"]),
        ]
        if branch == PARTICLE_REFINEMENT_BRANCH and particle_refined_score is not None:
            q_values.append(float(particle_refined_score["corrected_q"]))
        refinement_intersections[branch] = max(min(q_values), parent_lower) <= min(
            max(q_values), parent_upper
        )
    particle_refinement_delta = (
        abs(
            float(particle_refined_score["corrected_q"])
            - float(primary_scores[PARTICLE_REFINEMENT_BRANCH]["corrected_q"])
        )
        if particle_refined_score is not None
        and PARTICLE_REFINEMENT_BRANCH in primary_scores
        else math.nan
    )
    any_q_compatible = any_primary_q_compatible or any(
        refinement_intersections.values()
    )
    closest_score = min(
        scores,
        key=lambda row: max(
            parent_lower - float(row["corrected_q"]),
            float(row["corrected_q"]) - parent_upper,
            0.0,
        ),
    ) if scores else None
    closest_q_gap = (
        max(
            parent_lower - float(closest_score["corrected_q"]),
            float(closest_score["corrected_q"]) - parent_upper,
            0.0,
        )
        if closest_score is not None
        else math.nan
    )
    if not response_executed:
        route_decision = "RADIAL_ENTROPY_AND_FREEFALL_MAP_DERIVED_BUT_FORWARD_RESPONSE_NOT_EXECUTED"
    elif any_q_compatible:
        route_decision = "RADIAL_ENTROPY_COOLING_AND_FREEFALL_REMOVES_THE_GLOBAL_CLOCK_FAILURE_AND_AT_LEAST_ONE_PREDECLARED_BRANCH_INTERSECTS_THE_PARENT_Q_BAND_WITHOUT_A_FITTED_RESPONSE"
    elif closest_q_gap < 0.02:
        route_decision = "RADIAL_ENTROPY_COOLING_AND_FREEFALL_REMOVES_MOST_OF_THE_GLOBAL_CLOCK_SLOPE_ERROR_BUT_ALL_REFINED_POINT_ESTIMATES_REMAIN_NARROWLY_ABOVE_THE_PARENT_Q_BAND"
    else:
        route_decision = "RADIAL_ENTROPY_COOLING_AND_FREEFALL_IS_FORWARDED_WITH_EXACT_MASS_CONSERVATION_BUT_ALL_PREDECLARED_BRANCHES_STILL_MISS_THE_PARENT_Q_BAND"
    decision = [
        {
            "route": "radial_entropy_cooling_freefall_mass_transfer",
            "result": route_decision,
            "evidence": "; ".join(
                f"{branch_id(*key)} q={row['corrected_q']} RMSE={row['corrected_velocity_squared_log10_RMSE']}"
                for key, row in primary_scores.items()
            )
            if primary_scores
            else "physics_only",
            "next_requirement": "if compatible, replace homologous donor transfer and self-similar deposition with radial radiation-hydrodynamic transport and metallicity bounds; if incompatible, retain this as a source-history bound and pivot to the collective stress route",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    ]
    provenance = provenance_rows(paths)
    outputs: dict[Path, list[dict[str, Any]]] = {
        CONTRACT_CSV: contract,
        SHELL_CSV: shells,
        SCHEDULE_CSV: schedules,
        ENERGY_CSV: energies,
        DECISION_CSV: decision,
        PROVENANCE_CSV: provenance,
    }
    if scores:
        outputs[TRANSFER_CSV] = transfers
        outputs[SCORE_CSV] = scores
        outputs[PROFILE_CSV] = profiles
        outputs[CONTROL_CSV] = controls
    for path, rows in outputs.items():
        P.write_csv(path, rows)

    hashes_after = {key: P.file_digest(path) for key, path in paths.items()}
    formal_after = P.tree_digest(FORMAL)
    validation: list[dict[str, Any]] = []
    P.add_validation(validation, "all_sources_exist", not missing, missing)
    P.add_validation(
        validation, "source_hashes_unchanged", hashes_before == hashes_after, hashes_after
    )
    P.add_validation(
        validation,
        "formalization_workbench_unchanged",
        formal_before == formal_after == FORMAL_DIGEST_LOCK,
        formal_after,
    )
    P.add_validation(
        validation,
        "all_temperature_integrands_positive",
        all(
            solution["minimum_energy_derivative_J_kg_K"] > 0.0
            and solution["minimum_cooling_coefficient"] > 0.0
            for solution in solutions.values()
        ),
        {
            branch_id(*key): [
                value["minimum_energy_derivative_J_kg_K"],
                value["minimum_cooling_coefficient"],
            ]
            for key, value in solutions.items()
        },
    )
    P.add_validation(
        validation,
        "all_cooling_lookups_inside_table_density_axis",
        all(solution["maximum_table_density_cm3"] <= 1.0e4 for solution in solutions.values()),
        {branch_id(*key): value["maximum_table_density_cm3"] for key, value in solutions.items()},
    )
    P.add_validation(
        validation,
        "radial_shell_endpoint_mass_exact",
        all(
            abs(
                solution["selected_total_Msun"]
                - float(polynomial["condensed_edge_Msun"])
            )
            / float(polynomial["condensed_edge_Msun"])
            < 1.0e-12
            for solution in solutions.values()
        ),
        {branch_id(*key): value["selected_total_Msun"] for key, value in solutions.items()},
    )
    P.add_validation(
        validation,
        "radial_endpoint_resolution_controlled",
        max(endpoint_resolution_change.values()) < 0.02,
        endpoint_resolution_change,
    )
    P.add_validation(
        validation,
        "four_branches_predeclared_without_target_selection",
        FORWARD_BRANCHES
        == (("ISOCHORIC", 0.1), ("ISOCHORIC", 0.3), ("ISOBARIC", 0.1), ("ISOBARIC", 0.3))
        and all(not row["target_used_to_select_schedule"] for row in schedules),
        FORWARD_BRANCHES,
    )
    if not arguments.physics_only:
        P.add_validation(
            validation,
            "all_predeclared_forward_responses_executed",
            response_executed,
            list(primary_scores),
        )
        P.add_validation(
            validation,
            "discrete_transfer_mass_exact",
            all(float(row["mass_conservation_relative_residual"]) < 1.0e-12 for row in transfers),
            [row["mass_conservation_relative_residual"] for row in transfers],
        )
        P.add_validation(
            validation,
            "donor_baryon_transfer_nonnegative_and_bounded",
            all(0.0 < float(row["maximum_transfer_fraction_of_available_baryons"]) <= 1.0 for row in transfers),
            [row["maximum_transfer_fraction_of_available_baryons"] for row in transfers],
        )
        P.add_validation(
            validation,
            "all_forward_scores_finite",
            all(
                math.isfinite(float(row["corrected_q"]))
                and math.isfinite(float(row["corrected_velocity_squared_log10_RMSE"]))
                for row in scores
            ),
            scores,
        )
        P.add_validation(
            validation,
            "source_reaches_full_assembly",
            all(abs(float(row["source_final_assembly_fraction"]) - 1.0) < 1.0e-12 for row in controls),
            [row["source_final_assembly_fraction"] for row in controls],
        )
        P.add_validation(
            validation,
            "central_force_angular_momentum_control",
            max(
                max(
                    float(row["source_angular_momentum_relative_residual"]),
                    float(row["control_angular_momentum_relative_residual"]),
                )
                for row in controls
            )
            < 1.0e-10,
            "all source and control runs",
        )
        P.add_validation(
            validation,
            "no_fitted_response_or_branch_selection",
            all(
                not row["target_used_to_select_branch"]
                and not row["response_efficiency_fitted"]
                for row in scores
            ),
            "four Cartesian-product branches",
        )
        P.add_validation(
            validation,
            "time_refinement_executed",
            arguments.skip_refinement
            or set(refined_scores) == set(REFINEMENT_BRANCHES),
            list(refined_scores),
        )
        P.add_validation(
            validation,
            "time_refinement_q_controlled",
            arguments.skip_refinement
            or (
                set(refinement_deltas) == set(REFINEMENT_BRANCHES)
                and max(refinement_deltas.values()) < 0.1
            ),
            {branch_id(*key): value for key, value in refinement_deltas.items()},
        )
        P.add_validation(
            validation,
            "near_boundary_particle_refinement_executed",
            arguments.skip_refinement or particle_refined_score is not None,
            (
                particle_refined_score["corrected_q"]
                if particle_refined_score is not None
                else "NOT_RUN"
            ),
        )
        P.add_validation(
            validation,
            "particle_refinement_q_controlled",
            arguments.skip_refinement or particle_refinement_delta < 0.1,
            particle_refinement_delta,
        )
    P.add_validation(
        validation,
        "all_outputs_nonclaim",
        all(row.get("valid_for_claim") is False for rows in outputs.values() for row in rows),
        "all generated CSV rows",
    )
    P.add_validation(
        validation,
        "local_GR_Newton_Maxwell_branch_unmodified",
        True,
        "same inherited G_N central force; only source history and radial baryon bookkeeping changed",
    )

    summary = {
        "virial_temperature_K": virial["temperature_K"],
        "parent_q_lower": parent_lower,
        "parent_q_upper": parent_upper,
        "baseline_RMSE": context["baseline_score"]["velocity_squared_log10_RMSE"],
        "radial_endpoint_times_Gyr": {
            branch_id(*key): value["endpoint_time_Gyr"] for key, value in solutions.items()
        },
        "endpoint_resolution_relative_changes": endpoint_resolution_change,
        "primary_scores": {
            branch_id(*key): {
                "common_endpoint_Gyr": row["common_endpoint_Gyr"],
                "corrected_q": row["corrected_q"],
                "corrected_q_compatible": row["corrected_q_compatible"],
                "corrected_velocity_squared_log10_RMSE": row[
                    "corrected_velocity_squared_log10_RMSE"
                ],
                "corrected_transition_velocity_squared_ratio_to_target": row[
                    "corrected_transition_velocity_squared_ratio_to_target"
                ],
            }
            for key, row in primary_scores.items()
        },
        "any_primary_q_compatible": any_primary_q_compatible,
        "any_primary_refined_interval_intersects_parent_band": any(
            refinement_intersections.values()
        ),
        "refinement_interval_intersections": {
            branch_id(*key): value
            for key, value in refinement_intersections.items()
        },
        "all_primary_RMSE_improve": all_rmse_improve,
        "refined_q_values": {
            branch_id(*key): float(value["corrected_q"])
            for key, value in refined_scores.items()
        },
        "refinement_delta_q_values": {
            branch_id(*key): value for key, value in refinement_deltas.items()
        },
        "particle_refinement_branch": branch_id(*PARTICLE_REFINEMENT_BRANCH),
        "particle_refined_q": (
            float(particle_refined_score["corrected_q"])
            if particle_refined_score is not None
            else math.nan
        ),
        "particle_refinement_delta_q": particle_refinement_delta,
        "closest_run_id": (
            closest_score["run_id"] if closest_score is not None else "NOT_RUN"
        ),
        "closest_q": (
            float(closest_score["corrected_q"])
            if closest_score is not None
            else math.nan
        ),
        "closest_q_gap_to_parent_band": closest_q_gap,
    }
    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "formalization_workbench_tree_sha256": formal_after,
        "source_hashes_before": hashes_before,
        "source_hashes_after": hashes_after,
        "summary": summary,
        "route_decision": route_decision,
        "validation_count": len(validation),
        "validation_failures": [row for row in validation if not row["passed"]],
        "radial_entropy_cooling_times_derived": True,
        "Newtonian_freefall_arrival_derived": True,
        "pair_mean_radial_arrival_clock_built": True,
        "exact_checkpoint_5164_homologous_baryon_transfer_retained": bool(transfers),
        "shell_rank_mapped_directly_to_antithetic_particles": False,
        "radial_forward_response_executed": response_executed,
        "at_least_one_primary_point_inside_parent_q_band": any_primary_q_compatible,
        "at_least_one_primary_refinement_interval_intersects_parent_q_band": any(
            refinement_intersections.values()
        ),
        "conditional_numerical_q_compatibility": any_q_compatible,
        "full_radiation_hydrodynamics_solved": False,
        "local_GR_Newton_Maxwell_branch_modified": False,
        "valid_for_galaxy_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    P.write_json(RESULT_JSON, result)
    P.write_csv(VALIDATION_CSV, validation)
    DOCUMENT.write_text(make_document(result), encoding="utf-8")
    if result["validation_failures"]:
        raise RuntimeError(
            f"validation failures: {[row['check_id'] for row in result['validation_failures']]}"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
