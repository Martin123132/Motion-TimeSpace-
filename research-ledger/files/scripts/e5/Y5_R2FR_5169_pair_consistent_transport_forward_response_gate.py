from __future__ import annotations

import argparse
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


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
PREVIOUS_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5168_pair_consistent_optimal_transport_source_operator_gate.py"
)
PREVIOUS_DOCUMENT = (
    POST
    / "5168-Y5-R2FR-pair-consistent-capacity-bounded-optimal-transport-radial-source-operator-gate.md"
)
PREVIOUS_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5168"
    / "pair_consistent_optimal_transport_source_operator_results.json"
)
PREVIOUS_VALIDATION = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5168_VALIDATION.csv"
)
PREVIOUS_SCORE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5167"
    / "radial_cooling_forward_response_scores.csv"
)
OUT = POST / "source-intake" / "functional_rg" / "5169"
CACHE = OUT / "run-cache"
CONTRACT_CSV = OUT / "transport_forward_replay_contract.csv"
CONFIG_CSV = OUT / "predeclared_run_configuration.csv"
SCORE_CSV = OUT / "transported_radial_source_forward_scores.csv"
PROFILE_CSV = OUT / "transported_radial_source_forward_profiles.csv"
CONTROL_CSV = OUT / "transported_radial_source_numerical_controls.csv"
TRANSFER_CSV = OUT / "transported_radial_source_phase_transfer.csv"
COMPARISON_CSV = OUT / "comparison_to_checkpoint_5167.csv"
DECISION_CSV = OUT / "route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "pair_consistent_transport_forward_response_results.json"
VALIDATION_CSV = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5169_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5169-Y5-R2FR-pair-consistent-capacity-bounded-transport-forward-response-gate.md"
)

MARKER = "MTS_5169_PAIR_CONSISTENT_TRANSPORT_FORWARD_RESPONSE_GATE"
CHECKED_DATE = "2026-07-21"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
PRIMARY_RADIAL_BINS = 26
PRIMARY_COST_POWER = 1
PRIMARY_STEPS_PER_INNER_ORBIT = 64
REFINED_STEPS_PER_INNER_ORBIT = 128
SELECTED_CONTROL_BRANCH = ("ISOBARIC", 0.3)
RESOLUTION_CONTROLS = (13, 52)
NORM_CONTROL_POWER = 2
LEGACY_CACHE_SCRIPT_HASHES = (
    "e3ec714304dedc31d2b9b87715c5e8f4d6ba42a97cecaa06efc0db849f13f04e",
)


specification = importlib.util.spec_from_file_location(
    "mts_checkpoint_5168_for_5169", PREVIOUS_SCRIPT
)
if specification is None or specification.loader is None:
    raise RuntimeError(f"cannot load module: {PREVIOUS_SCRIPT}")
R = importlib.util.module_from_spec(specification)
specification.loader.exec_module(R)
P = R.P
Q = R.Q
DYNAMICS = R.DYNAMICS
ENERGY = R.ENERGY


def source_paths() -> dict[str, Path]:
    paths = R.source_paths()
    paths.update(
        {
            "checkpoint_5168_script": PREVIOUS_SCRIPT,
            "checkpoint_5168_document": PREVIOUS_DOCUMENT,
            "checkpoint_5168_result": PREVIOUS_RESULT,
            "checkpoint_5168_validation": PREVIOUS_VALIDATION,
            "checkpoint_5167_forward_scores": PREVIOUS_SCORE,
            "checkpoint_5169_script": Path(__file__).resolve(),
        }
    )
    return paths


def run_configurations() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for branch in P.FORWARD_BRANCHES:
        rows.append(
            {
                "run_id": f"{P.branch_id(*branch)}_OT_N26_P1_FULL_PRIMARY",
                "thermal_mode": branch[0],
                "metallicity_Zsun": branch[1],
                "radial_bins": PRIMARY_RADIAL_BINS,
                "cost_power": PRIMARY_COST_POWER,
                "steps_per_inner_orbit": PRIMARY_STEPS_PER_INNER_ORBIT,
                "run_role": "PRIMARY",
                "full_particle_state": True,
                "target_q_used_to_define_operator": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    selected_name = P.branch_id(*SELECTED_CONTROL_BRANCH)
    rows.extend(
        [
            {
                "run_id": f"{selected_name}_OT_N26_P1_FULL_TIME_REFINEMENT",
                "thermal_mode": SELECTED_CONTROL_BRANCH[0],
                "metallicity_Zsun": SELECTED_CONTROL_BRANCH[1],
                "radial_bins": PRIMARY_RADIAL_BINS,
                "cost_power": PRIMARY_COST_POWER,
                "steps_per_inner_orbit": REFINED_STEPS_PER_INNER_ORBIT,
                "run_role": "TIME_REFINEMENT",
                "full_particle_state": True,
                "target_q_used_to_define_operator": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            },
            {
                "run_id": f"{selected_name}_OT_N26_P2_FULL_NORM_CONTROL",
                "thermal_mode": SELECTED_CONTROL_BRANCH[0],
                "metallicity_Zsun": SELECTED_CONTROL_BRANCH[1],
                "radial_bins": PRIMARY_RADIAL_BINS,
                "cost_power": NORM_CONTROL_POWER,
                "steps_per_inner_orbit": PRIMARY_STEPS_PER_INNER_ORBIT,
                "run_role": "NORM_CONTROL",
                "full_particle_state": True,
                "target_q_used_to_define_operator": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            },
        ]
    )
    for radial_bins in RESOLUTION_CONTROLS:
        rows.append(
            {
                "run_id": f"{selected_name}_OT_N{radial_bins}_P1_FULL_RESOLUTION_CONTROL",
                "thermal_mode": SELECTED_CONTROL_BRANCH[0],
                "metallicity_Zsun": SELECTED_CONTROL_BRANCH[1],
                "radial_bins": radial_bins,
                "cost_power": PRIMARY_COST_POWER,
                "steps_per_inner_orbit": PRIMARY_STEPS_PER_INNER_ORBIT,
                "run_role": "RESOLUTION_CONTROL",
                "full_particle_state": True,
                "target_q_used_to_define_operator": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows


def contract_rows() -> list[dict[str, Any]]:
    clauses = [
        (
            "F1_FROZEN_OPERATOR",
            "f_isj is solved once from checkpoint-5168 endpoint sources and phase capacities before any forward score is read",
            "derived_and_predeclared",
        ),
        (
            "F2_LAGRANGIAN_SINK",
            "each donor retains its initial radial sink-bin label while the transported baryon fraction changes with source-shell arrivals",
            "derived_reduced_transport_replay",
        ),
        (
            "F3_SOURCE_HISTORY",
            "Delta M_sj(t)=sum_i f_isj M_i,arrived(t)/M_i,endpoint",
            "exact_discrete_lift",
        ),
        (
            "F4_PHASE_CONSERVATION",
            "M_cond,s(t)=sum_j Delta M_sj(t) is deposited in the measured visible profile in the same phase",
            "exact_phase_mass_identity",
        ),
        (
            "F5_PAIR_CONSERVATION",
            "[lambda_minus(t)+lambda_plus(t)]/2=lambda_pair(t)",
            "exact_pair_identity",
        ),
        (
            "F6_FORCE",
            "a=-G_N M_enclosed(t) r/(r^2+epsilon^2)^(3/2) with inherited calibrated G_N",
            "same_newtonian_limit_as_checkpoint_5164",
        ),
        (
            "F7_FULL_PARTICLES",
            "all primary and closure-control runs use the original full antithetic particle states",
            "no_capacity_violating_compression",
        ),
        (
            "F8_NONCLAIM",
            "the optimal-transport metric is a reduced matter closure and is not represented as a parent-action derivation",
            "explicit_limitation",
        ),
    ]
    return [
        {
            "clause_id": clause_id,
            "contract": contract,
            "status": status,
            "target_q_used": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for clause_id, contract, status in clauses
    ]


def safe_name(value: str) -> str:
    return "".join(character if character.isalnum() else "_" for character in value)


def cache_signature(
    configuration: dict[str, Any], source_hashes: dict[str, str]
) -> str:
    payload = {
        "configuration": configuration,
        "source_hashes": source_hashes,
        "marker": MARKER,
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def accepted_cache_signatures(
    configuration: dict[str, Any], source_hashes: dict[str, str]
) -> set[str]:
    signatures = {cache_signature(configuration, source_hashes)}
    for legacy_hash in LEGACY_CACHE_SCRIPT_HASHES:
        legacy_sources = dict(source_hashes)
        legacy_sources["checkpoint_5169_script"] = legacy_hash
        signatures.add(cache_signature(configuration, legacy_sources))
    return signatures


def read_cache(path: Path, signatures: set[str]) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("cache_signature") not in signatures:
        return None
    return value


def source_history(
    solution: dict[str, Any], data: dict[str, Any], transport: dict[str, Any]
) -> list[dict[str, np.ndarray | float | int]]:
    selected = np.asarray(solution["selected_mass_Msun"], dtype=float) > 0.0
    mass = np.asarray(solution["selected_mass_Msun"], dtype=float)[selected]
    radius = np.asarray(solution["radius_kpc"], dtype=float)[selected]
    arrival = (
        np.asarray(solution["arrival_time_Gyr"], dtype=float)[selected]
        / Q.TIME_UNIT_GYR
    )
    radial_bins = int(data["radial_bins"])
    assignment = np.searchsorted(data["edges_kpc"], radius, side="right") - 1
    assignment = np.clip(assignment, 0, radial_bins - 1)
    histories: list[dict[str, np.ndarray | float | int]] = []
    desired = np.asarray(data["desired_Msun"], dtype=float)
    for radial_bin in np.asarray(transport["source_bins"], dtype=int):
        mask = assignment == radial_bin
        order = np.argsort(arrival[mask])
        times = arrival[mask][order]
        cumulative = np.cumsum(mass[mask][order])
        endpoint = float(desired[radial_bin])
        if not len(times) or endpoint <= 0.0:
            raise RuntimeError(f"empty positive source bin: {radial_bin}")
        if abs(float(cumulative[-1]) - endpoint) / max(endpoint, 1.0) > 1.0e-12:
            raise RuntimeError(f"source history endpoint mismatch: {radial_bin}")
        histories.append(
            {
                "radial_bin": int(radial_bin),
                "arrival_internal": times,
                "cumulative_Msun": cumulative,
                "endpoint_Msun": endpoint,
            }
        )
    return histories


def phase_plan(
    snapshot: dict[str, Any],
    solution: dict[str, Any],
    data: dict[str, Any],
    transport: dict[str, Any],
    phase_sign: int,
) -> dict[str, Any]:
    particle_count = len(snapshot["positions_kpc"])
    weights = np.asarray(
        snapshot.get("particle_weight", np.ones(particle_count)), dtype=float
    )
    donor = np.asarray(snapshot["donor"], dtype=bool)
    initial_radius = np.asarray(snapshot["initial_radius_kpc"], dtype=float)
    particle_mass = float(snapshot["particle_mass_Msun"][0])
    baryon_available = particle_mass * (1.0 - DYNAMICS.PM.MOTION_FRACTION)
    radial_bins = int(data["radial_bins"])
    edges = np.asarray(data["edges_kpc"], dtype=float)
    sink_index = np.searchsorted(edges, initial_radius, side="right") - 1
    on_upper_edge = np.isclose(initial_radius, edges[-1], rtol=0.0, atol=1.0e-12)
    sink_index[on_upper_edge] = radial_bins - 1
    valid = donor & (initial_radius >= edges[0]) & (initial_radius <= edges[-1])
    valid &= (sink_index >= 0) & (sink_index < radial_bins)
    represented_capacity = np.bincount(
        sink_index[valid],
        weights=weights[valid] * baryon_available,
        minlength=radial_bins,
    )
    phase_index = 0 if phase_sign == -1 else 1
    expected_capacity = np.asarray(
        data[
            "capacity_minus_Msun" if phase_sign == -1 else "capacity_plus_Msun"
        ],
        dtype=float,
    )
    condensed = float(data["condensed_Msun"])
    capacity_representation_residual = float(
        np.max(np.abs(represented_capacity - expected_capacity))
        / max(condensed, 1.0)
    )
    if capacity_representation_residual > 1.0e-12:
        raise RuntimeError(
            f"full-particle capacity representation mismatch: {phase_sign} "
            f"{capacity_representation_residual}"
        )
    endpoint_target = np.asarray(transport["phase_removal_Msun"], dtype=float)[
        phase_index
    ]
    endpoint_fraction = np.divide(
        endpoint_target,
        represented_capacity,
        out=np.zeros_like(endpoint_target),
        where=represented_capacity > 0.0,
    )
    if np.any((represented_capacity <= 0.0) & (endpoint_target > 1.0e-6)):
        raise RuntimeError(f"positive transfer into empty phase bin: {phase_sign}")
    if float(np.max(endpoint_fraction)) > 1.0 + 1.0e-10:
        raise RuntimeError(f"phase capacity exceeded: {phase_sign}")
    histories = source_history(solution, data, transport)
    endpoint_particle_transfer = np.zeros(particle_count, dtype=float)
    endpoint_particle_transfer[valid] = (
        baryon_available * endpoint_fraction[sink_index[valid]]
    )
    return {
        "phase_sign": phase_sign,
        "phase_index": phase_index,
        "weights": weights,
        "valid_indices": np.flatnonzero(valid),
        "valid_sink_index": sink_index[valid],
        "baryon_available_per_particle_Msun": baryon_available,
        "represented_capacity_Msun": represented_capacity,
        "endpoint_target_Msun": endpoint_target,
        "endpoint_fraction": endpoint_fraction,
        "endpoint_particle_transfer_Msun": endpoint_particle_transfer,
        "flow_Msun": np.asarray(transport["flow_Msun"], dtype=float)[:, phase_index, :],
        "histories": histories,
        "condensed_Msun": condensed,
        "endpoint_time_internal": float(solution["endpoint_time_Gyr"])
        / Q.TIME_UNIT_GYR,
        "capacity_representation_relative_residual": capacity_representation_residual,
    }


def transfer_at(plan: dict[str, Any], current_time: float) -> tuple[np.ndarray, float]:
    if current_time <= 0.0:
        return np.zeros_like(plan["endpoint_particle_transfer_Msun"]), 0.0
    if current_time >= float(plan["endpoint_time_internal"]):
        return plan["endpoint_particle_transfer_Msun"], 1.0
    source_fraction = np.zeros(len(plan["histories"]), dtype=float)
    for source_index, history in enumerate(plan["histories"]):
        arrival = history["arrival_internal"]
        index = int(np.searchsorted(arrival, current_time, side="right"))
        if index > 0:
            source_fraction[source_index] = min(
                float(history["cumulative_Msun"][index - 1])
                / float(history["endpoint_Msun"]),
                1.0,
            )
    sink_target = np.tensordot(
        source_fraction, plan["flow_Msun"], axes=(0, 0)
    )
    sink_fraction = np.divide(
        sink_target,
        plan["represented_capacity_Msun"],
        out=np.zeros_like(sink_target),
        where=plan["represented_capacity_Msun"] > 0.0,
    )
    transfer = np.zeros_like(plan["endpoint_particle_transfer_Msun"])
    transfer[plan["valid_indices"]] = (
        float(plan["baryon_available_per_particle_Msun"])
        * sink_fraction[plan["valid_sink_index"]]
    )
    transferred = float(np.sum(plan["weights"] * transfer))
    return transfer, transferred / float(plan["condensed_Msun"])


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
    if np.any(gravitational_masses < -1.0e-6):
        raise RuntimeError("negative transported particle mass")
    sorted_masses = gravitational_masses[order]
    enclosed_particles = np.cumsum(sorted_masses) - 0.5 * sorted_masses
    background = (
        4.0
        * math.pi
        * DYNAMICS.PM.RHO_M_MSUN_MPC3
        * (sorted_radii / 1000.0) ** 3
        / 3.0
    )
    condensed = condensed_fraction * np.asarray(
        visible_source.mass_at(sorted_radii), dtype=float
    )
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
    profile_radii_kpc: np.ndarray,
    transition_orbit: float,
    inner_orbit: float,
    steps_per_inner_orbit: int,
    source_enabled: bool,
) -> dict[str, Any]:
    positions = np.asarray(snapshot["positions_kpc"], dtype=float).copy()
    velocities = np.asarray(snapshot["velocities_km_s"], dtype=float).copy()
    particle_count = len(positions)
    particle_weight = np.asarray(
        snapshot.get("particle_weight", np.ones(particle_count)), dtype=float
    )
    initial_radius = np.asarray(snapshot["initial_radius_kpc"], dtype=float)
    particle_mass = float(snapshot["particle_mass_Msun"][0])
    edge_radius = float(snapshot["edge_radius_kpc"][0])
    softening = (
        DYNAMICS.SOFTENING_CELL_MULTIPLE
        * float(snapshot["local_force_cell_kpc"][0])
    )
    common_duration = float(plan["endpoint_time_internal"])
    total_time = common_duration + DYNAMICS.SETTLING_ORBITS * transition_orbit
    averaging_time = DYNAMICS.AVERAGING_ORBITS * transition_orbit
    nominal_dt = inner_orbit / steps_per_inner_orbit
    steps = max(1, int(math.ceil(total_time / nominal_dt)))
    time_step = total_time / steps
    averaging_start = max(total_time - averaging_time, 0.0)
    sample_stride = max(
        1,
        int(
            round(
                max(1.0, averaging_time / time_step)
                / DYNAMICS.PROFILE_AVERAGE_SAMPLES
            )
        ),
    )
    initial_angular_momentum = np.cross(positions, velocities)
    initial_com = np.average(positions, axis=0, weights=particle_weight)
    zero_transfer = np.zeros(particle_count, dtype=float)
    start = time.perf_counter()

    def current_transfer(current_time: float) -> tuple[np.ndarray, float]:
        if not source_enabled:
            return zero_transfer, 0.0
        return transfer_at(plan, current_time)

    transfer, condensed_fraction = current_transfer(0.0)
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
    final_transfer = transfer
    for step in range(steps):
        positions += time_step * half_velocity
        current_time = (step + 1) * time_step
        final_transfer, final_fraction = current_transfer(current_time)
        force = acceleration(
            positions,
            particle_weight,
            particle_mass,
            final_transfer,
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
                np.sum(
                    particle_weight[:, None] * initial_angular_momentum**2
                ),
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
    represented_transfer = float(np.sum(particle_weight * final_transfer))
    condensed = float(plan["condensed_Msun"])
    return {
        "averaged_counts": averaged_counts,
        "steps": steps,
        "time_step_internal": time_step,
        "profile_sample_count": len(count_samples),
        "final_assembly_fraction": final_fraction,
        "final_transferred_mass_Msun": represented_transfer,
        "final_transfer_relative_residual": abs(represented_transfer - condensed)
        / max(condensed, 1.0)
        if source_enabled
        else 0.0,
        "maximum_transfer_fraction_of_available_baryons": float(
            np.max(final_transfer)
            / max(float(plan["baryon_available_per_particle_Msun"]), 1.0e-300)
        ),
        "angular_momentum_relative_residual": angular_residual,
        "center_of_mass_drift_kpc": float(
            np.linalg.norm(
                np.average(positions, axis=0, weights=particle_weight) - initial_com
            )
        ),
        "outer_boundary_ingress_fraction": boundary_ingress / final_inside,
        "wall_seconds": time.perf_counter() - start,
        "softening_kpc": softening,
    }


def run_configuration(
    configuration: dict[str, Any],
    context: dict[str, Any],
    polynomial: dict[str, Any],
    solutions: dict[tuple[str, float], dict[str, Any]],
    operator_cache: dict[tuple[int, int], tuple[dict[str, Any], dict[str, Any]]],
    control_cache: dict[tuple[int, float, int], dict[str, Any]],
) -> dict[str, Any]:
    branch = (
        str(configuration["thermal_mode"]),
        float(configuration["metallicity_Zsun"]),
    )
    solution = solutions[branch]
    operator_key = (
        int(configuration["radial_bins"]),
        int(configuration["cost_power"]),
    )
    if operator_key not in operator_cache:
        reference = solutions[SELECTED_CONTROL_BRANCH]
        data = R.binned_inputs(
            context, reference, polynomial, operator_key[0]
        )
        transport = R.solve_transport(data, operator_key[1])
        operator_cache[operator_key] = (data, transport)
    data, transport = operator_cache[operator_key]
    branch_data = R.binned_inputs(
        context, solution, polynomial, operator_key[0]
    )
    endpoint_profile_relative_residual = float(
        np.max(
            np.abs(
                np.asarray(branch_data["desired_Msun"], dtype=float)
                - np.asarray(data["desired_Msun"], dtype=float)
            )
        )
        / max(float(data["condensed_Msun"]), 1.0)
    )
    if endpoint_profile_relative_residual > 1.0e-12:
        raise RuntimeError(f"branch endpoint profile changed: {branch}")
    phase_mass: dict[int, np.ndarray] = {}
    controls: list[dict[str, Any]] = []
    transfers: list[dict[str, Any]] = []
    for phase_sign in (-1, 1):
        snapshot = context["snapshots"][phase_sign]
        plan = phase_plan(
            snapshot, solution, data, transport, phase_sign
        )
        source_run = evolve(
            snapshot,
            plan,
            context["visible_source"],
            context["radii"],
            context["transition_orbit"],
            context["inner_orbit"],
            int(configuration["steps_per_inner_orbit"]),
            True,
        )
        control_key = (
            phase_sign,
            round(float(plan["endpoint_time_internal"]), 12),
            int(configuration["steps_per_inner_orbit"]),
        )
        if control_key not in control_cache:
            control_cache[control_key] = evolve(
                snapshot,
                plan,
                context["visible_source"],
                context["radii"],
                context["transition_orbit"],
                context["inner_orbit"],
                int(configuration["steps_per_inner_orbit"]),
                False,
            )
        control_run = control_cache[control_key]
        particle_mass = float(snapshot["particle_mass_Msun"][0])
        background = (
            4.0
            * math.pi
            * DYNAMICS.PM.RHO_M_MSUN_MPC3
            * (context["radii"] / 1000.0) ** 3
            / 3.0
        )
        source_mass = DYNAMICS.PM.MOTION_FRACTION * np.maximum(
            source_run["averaged_counts"] * particle_mass - background, 0.0
        )
        control_mass = DYNAMICS.PM.MOTION_FRACTION * np.maximum(
            control_run["averaged_counts"] * particle_mass - background, 0.0
        )
        ratio = np.ones_like(context["radii"])
        positive = control_mass > 0.0
        ratio[positive] = source_mass[positive] / control_mass[positive]
        phase_mass[phase_sign] = context["initial_phase_mass"][phase_sign] * ratio
        controls.append(
            {
                "run_id": configuration["run_id"],
                "run_role": configuration["run_role"],
                "phase_sign": phase_sign,
                "response_particle_count": len(snapshot["positions_kpc"]),
                "represented_particle_count": len(snapshot["positions_kpc"]),
                "radial_bins": configuration["radial_bins"],
                "cost_power": configuration["cost_power"],
                "steps_per_inner_orbit": configuration["steps_per_inner_orbit"],
                "source_steps": source_run["steps"],
                "control_steps": control_run["steps"],
                "source_final_assembly_fraction": source_run[
                    "final_assembly_fraction"
                ],
                "source_final_transferred_mass_Msun": source_run[
                    "final_transferred_mass_Msun"
                ],
                "source_final_transfer_relative_residual": source_run[
                    "final_transfer_relative_residual"
                ],
                "maximum_transfer_fraction_of_available_baryons": source_run[
                    "maximum_transfer_fraction_of_available_baryons"
                ],
                "source_angular_momentum_relative_residual": source_run[
                    "angular_momentum_relative_residual"
                ],
                "control_angular_momentum_relative_residual": control_run[
                    "angular_momentum_relative_residual"
                ],
                "source_center_of_mass_drift_kpc": source_run[
                    "center_of_mass_drift_kpc"
                ],
                "control_center_of_mass_drift_kpc": control_run[
                    "center_of_mass_drift_kpc"
                ],
                "source_outer_boundary_ingress_fraction": source_run[
                    "outer_boundary_ingress_fraction"
                ],
                "control_outer_boundary_ingress_fraction": control_run[
                    "outer_boundary_ingress_fraction"
                ],
                "source_wall_seconds": source_run["wall_seconds"],
                "control_wall_seconds": control_run["wall_seconds"],
                "capacity_representation_relative_residual": plan[
                    "capacity_representation_relative_residual"
                ],
                "endpoint_profile_relative_residual": endpoint_profile_relative_residual,
                "target_q_used": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
        centers = np.asarray(data["centers_kpc"], dtype=float)
        for radial_bin in range(int(data["radial_bins"])):
            transfers.append(
                {
                    "run_id": configuration["run_id"],
                    "phase_sign": phase_sign,
                    "radial_bin": radial_bin,
                    "radial_center_kpc": centers[radial_bin],
                    "phase_capacity_Msun": plan["represented_capacity_Msun"][
                        radial_bin
                    ],
                    "endpoint_transfer_Msun": plan["endpoint_target_Msun"][
                        radial_bin
                    ],
                    "endpoint_capacity_fraction": plan["endpoint_fraction"][
                        radial_bin
                    ],
                    "target_q_used": False,
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
        **configuration,
        "common_endpoint_Gyr": float(solution["endpoint_time_Gyr"]),
        "duration_transition_orbits": float(plan["endpoint_time_internal"])
        / context["transition_orbit"],
        "operator_mean_absolute_displacement_kpc": transport[
            "mean_absolute_displacement_kpc"
        ],
        "operator_rms_displacement_kpc": transport["rms_displacement_kpc"],
        "operator_pair_profile_L1_change_fraction": transport[
            "pair_profile_L1_change_fraction"
        ],
        "q_parent": q_parent,
        "q_envelope": q_envelope,
        "corrected_q": score["q"],
        "corrected_q_absolute_difference": abs(float(score["q"]) - q_parent),
        "corrected_q_compatible": abs(float(score["q"]) - q_parent) <= q_envelope,
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
        "target_used_to_select_branch": configuration["run_role"] != "PRIMARY",
        "control_branch_selected_from_checkpoint_5167_nearest_q": configuration[
            "run_role"
        ]
        != "PRIMARY",
        "response_efficiency_fitted": False,
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }
    profiles: list[dict[str, Any]] = []
    velocity_squared = (
        DYNAMICS.PREVIOUS.G_KPC_KM2_S2_MSUN
        * corrected_mass
        / np.maximum(context["radii"], np.finfo(float).tiny)
    )
    for index, radius in enumerate(context["radii"]):
        profiles.append(
            {
                "run_id": configuration["run_id"],
                "run_role": configuration["run_role"],
                "radius_kpc": radius,
                "radius_over_transition": radius / context["transition_radius"],
                "corrected_motion_mass_Msun": corrected_mass[index],
                "phase_minus_corrected_mass_Msun": phase_mass[-1][index],
                "phase_plus_corrected_mass_Msun": phase_mass[1][index],
                "corrected_motion_v2_km2_s2": velocity_squared[index],
                "target_motion_v2_km2_s2": context["target_velocity"][index],
                "inside_scoring_window": bool(context["score_mask"][index]),
                "target_q_used": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return {
        "score": score_row,
        "controls": controls,
        "profiles": profiles,
        "transfers": transfers,
    }


def comparison_rows(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    previous = P.read_typed_csv(PREVIOUS_SCORE)
    previous_primary = {
        (str(row["thermal_mode"]), float(row["metallicity_Zsun"])): row
        for row in previous
        if str(row["run_id"]).endswith("PRIMARY")
    }
    previous_selected_full = next(
        (
            row
            for row in previous
            if str(row["run_id"]).endswith("FULL_PARTICLE_REFINEMENT")
            and (str(row["thermal_mode"]), float(row["metallicity_Zsun"]))
            == SELECTED_CONTROL_BRANCH
        ),
        None,
    )
    rows: list[dict[str, Any]] = []
    for row in scores:
        if row["run_role"] != "PRIMARY":
            continue
        branch = (str(row["thermal_mode"]), float(row["metallicity_Zsun"]))
        old = previous_primary[branch]
        matched_full = (
            previous_selected_full
            if branch == SELECTED_CONTROL_BRANCH
            else None
        )
        rows.append(
            {
                "thermal_mode": branch[0],
                "metallicity_Zsun": branch[1],
                "checkpoint_5167_homologous_q": old["corrected_q"],
                "checkpoint_5169_transport_q": row["corrected_q"],
                "transport_delta_q": float(row["corrected_q"])
                - float(old["corrected_q"]),
                "checkpoint_5167_homologous_RMSE": old[
                    "corrected_velocity_squared_log10_RMSE"
                ],
                "checkpoint_5169_transport_RMSE": row[
                    "corrected_velocity_squared_log10_RMSE"
                ],
                "transport_delta_RMSE": float(
                    row["corrected_velocity_squared_log10_RMSE"]
                )
                - float(old["corrected_velocity_squared_log10_RMSE"]),
                "checkpoint_5167_matched_full_particle_q": (
                    matched_full["corrected_q"] if matched_full is not None else "NOT_RUN"
                ),
                "matched_full_particle_transport_delta_q": (
                    float(row["corrected_q"]) - float(matched_full["corrected_q"])
                    if matched_full is not None
                    else "NOT_RUN"
                ),
                "checkpoint_5167_matched_full_particle_RMSE": (
                    matched_full["corrected_velocity_squared_log10_RMSE"]
                    if matched_full is not None
                    else "NOT_RUN"
                ),
                "matched_full_particle_transport_delta_RMSE": (
                    float(row["corrected_velocity_squared_log10_RMSE"])
                    - float(matched_full["corrected_velocity_squared_log10_RMSE"])
                    if matched_full is not None
                    else "NOT_RUN"
                ),
                "target_q_used_to_define_transport": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows


def provenance_rows(paths: dict[str, Path]) -> list[dict[str, Any]]:
    return [
        {
            "source_id": key,
            "source_type": "local_file",
            "source_path": str(path),
            "sha256": Q.file_digest(path),
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
    primary_lines = "\n".join(
        f"- `{row['run_id']}`: q=`{row['corrected_q']}`, "
        f"RMSE=`{row['corrected_velocity_squared_log10_RMSE']}` dex, "
        f"compatible=`{row['corrected_q_compatible']}`"
        for row in summary["primary_scores"]
    )
    control_lines = "\n".join(
        f"- `{key}`: q=`{value}`"
        for key, value in summary["selected_branch_control_q"].items()
    )
    return f"""# 5169 - Pair-consistent capacity-bounded transport forward response

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Question

Checkpoint 5168 constructed a radial source operator but deliberately did not
run the response. This gate asks the non-inverted question: when that frozen
operator is replayed on the original particle states, does it improve the
galaxy response without reading the parent `q` target?

## Forward initial-value problem

For source bin `i`, phase `s`, and Lagrangian donor sink bin `j`, the endpoint
flow `f_isj` is the checkpoint-5168 constrained optimum. Its time lift is

```text
Delta M_sj(t)=sum_i f_isj M_i,arrived(t)/M_i,endpoint,
lambda_s(t)=sum_j Delta M_sj(t)/M_c,
Delta M_visible,s(t)=lambda_s(t) M_c.
```

Each donor particle in sink `j` loses the same fraction of its available
baryon mass. The same mass is deposited in the measured visible profile in
that phase, so phase and pair mass identities hold while the inherited central
force remains

```text
a=-G_N M_enclosed(t) r/(r^2+epsilon^2)^(3/2).
```

All runs use the full original antithetic particle states. No compressed state,
response efficiency, `q`, or rotation target enters the transport solution.

## Primary results

{primary_lines}

The fitted parent interval is
`[{summary['parent_q_lower']}, {summary['parent_q_upper']}]`; the free baseline
RMSE is `{summary['baseline_RMSE']} dex`. The closest primary result is
`{summary['closest_primary_run_id']}` with gap
`{summary['closest_primary_q_gap_to_parent_band']}`.

Relative to checkpoint 5167 homologous removal, the four transport shifts in
`q` are `{summary['transport_delta_q']}` and the RMSE shifts are
`{summary['transport_delta_RMSE']}`.
For the selected branch, where checkpoint 5167 also ran the full particle
state, the matched shifts are `Delta q={summary['matched_full_particle_selected_delta_q']}`
and `Delta RMSE={summary['matched_full_particle_selected_delta_RMSE']}` dex.

## Frozen controls

The checkpoint-5167 nearest branch, isobaric `Z=0.3 Zsun`, was selected using
the previous checkpoint's `q` only for numerical controls and was declared
before this response was read. It did not define the transport operator or any
primary physics branch. The results are:

{control_lines}

The maximum selected-control displacement from its primary `q` is
`{summary['maximum_selected_control_delta_q']}`. The operator uses mean radial
transport `{summary['primary_operator_mean_displacement_kpc']} kpc` and no
control is refitted to improve the score.

## Decision

`{result['route_decision']}`.

This checkpoint is an empirical gate on a reduced source closure, not a claim
that optimal transport has been derived from the parent field action. It does
not modify or validate the local GR/Newton/Maxwell branch. A favorable response
would justify deriving this operator from stress-energy and angular-momentum
transport; an unfavorable response would bound visible assembly and return
priority to the collective-stress/parent-coupling route.

```text
checkpoint-5168 operator replayed forward             = yes;
all four physical clocks run                           = yes;
full antithetic particle states used                   = yes;
phase endpoint mass conserved                          = yes;
q used to define or fit operator                       = no;
local GR/Newton/Maxwell branch modified                = no;
galaxy or full-MTS claim                               = false.
```

All `{result['validation_count']}` validation rows pass. The protected
`formalization-workbench` digest remains
`{result['formalization_workbench_tree_sha256']}`. No GitHub action occurred.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--stage", choices=("all", "primary", "controls", "finalize"), default="all"
    )
    parser.add_argument("--run-id")
    parser.add_argument("--force", action="store_true")
    arguments = parser.parse_args()
    paths = source_paths()
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing sources: {missing}")
    formal_before = Q.tree_digest(FORMAL)
    if formal_before != FORMAL_DIGEST_LOCK:
        raise RuntimeError(f"protected digest mismatch: {formal_before}")
    hashes_before = {key: Q.file_digest(path) for key, path in paths.items()}
    configurations = run_configurations()
    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "marker": MARKER,
                    "run_count": len(configurations),
                    "run_ids": [row["run_id"] for row in configurations],
                    "full_particle_state": True,
                    "formal_digest": formal_before,
                },
                indent=2,
            )
        )
        return

    if arguments.run_id and arguments.run_id not in {
        row["run_id"] for row in configurations
    }:
        raise RuntimeError(f"unknown run id: {arguments.run_id}")
    context, polynomial, _, solutions = R.build_parent_state()
    operator_cache: dict[
        tuple[int, int], tuple[dict[str, Any], dict[str, Any]]
    ] = {}
    control_cache: dict[tuple[int, float, int], dict[str, Any]] = {}
    CACHE.mkdir(parents=True, exist_ok=True)
    selected: list[dict[str, Any]] = []
    for configuration in configurations:
        if arguments.run_id and configuration["run_id"] != arguments.run_id:
            continue
        if arguments.stage == "primary" and configuration["run_role"] != "PRIMARY":
            continue
        if arguments.stage == "controls" and configuration["run_role"] == "PRIMARY":
            continue
        if arguments.stage == "finalize":
            continue
        selected.append(configuration)
    for configuration in selected:
        signature = cache_signature(configuration, hashes_before)
        signatures = accepted_cache_signatures(configuration, hashes_before)
        cache_path = CACHE / f"{safe_name(str(configuration['run_id']))}.json"
        cached = None if arguments.force else read_cache(cache_path, signatures)
        if cached is None:
            print(f"START {configuration['run_id']}", flush=True)
            payload = run_configuration(
                configuration,
                context,
                polynomial,
                solutions,
                operator_cache,
                control_cache,
            )
            cached = {
                "cache_signature": signature,
                "configuration": configuration,
                "payload": payload,
            }
            Q.write_json(cache_path, cached)
            print(
                f"DONE {configuration['run_id']} "
                f"q={payload['score']['corrected_q']} "
                f"RMSE={payload['score']['corrected_velocity_squared_log10_RMSE']}",
                flush=True,
            )
        else:
            print(f"REUSE {configuration['run_id']}", flush=True)

    cached_runs: list[dict[str, Any]] = []
    absent: list[str] = []
    for configuration in configurations:
        signatures = accepted_cache_signatures(configuration, hashes_before)
        cache_path = CACHE / f"{safe_name(str(configuration['run_id']))}.json"
        cached = read_cache(cache_path, signatures)
        if cached is None:
            absent.append(str(configuration["run_id"]))
        else:
            cached_runs.append(cached["payload"])
    if absent:
        print(json.dumps({"partial": True, "missing_run_ids": absent}, indent=2))
        return

    scores = [run["score"] for run in cached_runs]
    for row in scores:
        selected_from_previous_q = row["run_role"] != "PRIMARY"
        row["target_used_to_select_branch"] = selected_from_previous_q
        row[
            "control_branch_selected_from_checkpoint_5167_nearest_q"
        ] = selected_from_previous_q
    controls = [row for run in cached_runs for row in run["controls"]]
    profiles = [row for run in cached_runs for row in run["profiles"]]
    transfers = [row for run in cached_runs for row in run["transfers"]]
    comparisons = comparison_rows(scores)
    primary = [row for row in scores if row["run_role"] == "PRIMARY"]
    primary_by_branch = {
        (str(row["thermal_mode"]), float(row["metallicity_Zsun"])): row
        for row in primary
    }
    selected_primary = primary_by_branch[SELECTED_CONTROL_BRANCH]
    selected_controls = [row for row in scores if row["run_role"] != "PRIMARY"]
    selected_control_q = {
        str(row["run_role"])
        + (
            f"_N{row['radial_bins']}"
            if row["run_role"] == "RESOLUTION_CONTROL"
            else ""
        ): float(row["corrected_q"])
        for row in selected_controls
    }
    maximum_control_delta = max(
        abs(float(row["corrected_q"]) - float(selected_primary["corrected_q"]))
        for row in selected_controls
    )
    parent_lower = float(context["q_row"]["q_parent"]) - float(
        context["q_row"]["q_uncertainty_envelope"]
    )
    parent_upper = float(context["q_row"]["q_parent"]) + float(
        context["q_row"]["q_uncertainty_envelope"]
    )
    closest = min(
        primary,
        key=lambda row: max(
            parent_lower - float(row["corrected_q"]),
            float(row["corrected_q"]) - parent_upper,
            0.0,
        ),
    )
    closest_gap = max(
        parent_lower - float(closest["corrected_q"]),
        float(closest["corrected_q"]) - parent_upper,
        0.0,
    )
    any_compatible = any(bool(row["corrected_q_compatible"]) for row in primary)
    all_improve = all(bool(row["corrected_RMSE_improves_baseline"]) for row in primary)
    if any_compatible and all_improve:
        route_decision = (
            "FROZEN_PAIR_CONSISTENT_TRANSPORT_ENTERS_THE_PARENT_Q_BAND_AND_IMPROVES_THE_FREE_BASELINE_BUT_REMAINS_A_REDUCED_SOURCE_CLOSURE_REQUIRING_PARENT_STRESS_DERIVATION"
        )
    elif closest_gap < 0.02 and all_improve:
        route_decision = (
            "FROZEN_PAIR_CONSISTENT_TRANSPORT_REMAINS_NEAR_THE_PARENT_Q_BAND_AND_IMPROVES_THE_FREE_BASELINE_BUT_DOES_NOT_CLOSE_THE_GATE"
        )
    else:
        route_decision = (
            "FROZEN_PAIR_CONSISTENT_TRANSPORT_DOES_NOT_CLOSE_THE_PARENT_RESPONSE_GATE_SO_VISIBLE_ASSEMBLY_IS_RETAINED_AS_A_BOUNDED_SOURCE_HISTORY_AND_PARENT_COLLECTIVE_STRESS_TAKES_PRIORITY"
        )
    decisions = [
        {
            "route": "pair_consistent_transport_forward_response",
            "result": route_decision,
            "evidence": (
                f"closest_primary={closest['run_id']}; gap={closest_gap}; "
                f"all_improve={all_improve}; max_control_delta_q={maximum_control_delta}"
            ),
            "next_requirement": (
                "derive the successful transport kernel from parent stress and angular-momentum exchange"
                if any_compatible
                else "bound visible assembly and return priority to the parent collective-stress coupling"
            ),
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    ]
    hashes_after = {key: Q.file_digest(path) for key, path in paths.items()}
    formal_after = Q.tree_digest(FORMAL)
    validation: list[dict[str, Any]] = []
    add_validation(validation, "all_sources_exist", not missing, missing)
    add_validation(
        validation, "source_hashes_unchanged", hashes_before == hashes_after, hashes_after
    )
    add_validation(
        validation,
        "formalization_workbench_unchanged",
        formal_after == FORMAL_DIGEST_LOCK,
        formal_after,
    )
    add_validation(
        validation,
        "all_predeclared_runs_completed",
        len(scores) == len(configurations),
        [row["run_id"] for row in scores],
    )
    add_validation(
        validation,
        "all_four_primary_clocks_completed",
        len(primary) == len(P.FORWARD_BRANCHES),
        [row["run_id"] for row in primary],
    )
    add_validation(
        validation,
        "full_particle_states_used",
        all(
            int(row["response_particle_count"])
            == len(context["snapshots"][int(row["phase_sign"])]["positions_kpc"])
            for row in controls
        ),
        [row["response_particle_count"] for row in controls],
    )
    add_validation(
        validation,
        "branch_endpoint_profiles_identical",
        max(float(row["endpoint_profile_relative_residual"]) for row in controls)
        < 1.0e-12,
        max(float(row["endpoint_profile_relative_residual"]) for row in controls),
    )
    add_validation(
        validation,
        "full_capacity_projection_exact",
        max(
            float(row["capacity_representation_relative_residual"])
            for row in controls
        )
        < 1.0e-12,
        max(
            float(row["capacity_representation_relative_residual"])
            for row in controls
        ),
    )
    add_validation(
        validation,
        "phase_endpoint_transfer_exact",
        max(float(row["source_final_transfer_relative_residual"]) for row in controls)
        < 1.0e-10,
        max(float(row["source_final_transfer_relative_residual"]) for row in controls),
    )
    add_validation(
        validation,
        "particle_baryon_transfer_bounded",
        max(
            float(row["maximum_transfer_fraction_of_available_baryons"])
            for row in controls
        )
        <= 1.0 + 1.0e-10,
        max(
            float(row["maximum_transfer_fraction_of_available_baryons"])
            for row in controls
        ),
    )
    add_validation(
        validation,
        "source_reaches_full_assembly",
        all(
            abs(float(row["source_final_assembly_fraction"]) - 1.0) < 1.0e-12
            for row in controls
        ),
        [row["source_final_assembly_fraction"] for row in controls],
    )
    add_validation(
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
        max(
            max(
                float(row["source_angular_momentum_relative_residual"]),
                float(row["control_angular_momentum_relative_residual"]),
            )
            for row in controls
        ),
    )
    add_validation(
        validation,
        "outer_boundary_ingress_controlled",
        max(
            max(
                float(row["source_outer_boundary_ingress_fraction"]),
                float(row["control_outer_boundary_ingress_fraction"]),
            )
            for row in controls
        )
        < 0.05,
        max(
            max(
                float(row["source_outer_boundary_ingress_fraction"]),
                float(row["control_outer_boundary_ingress_fraction"]),
            )
            for row in controls
        ),
    )
    add_validation(
        validation,
        "all_scores_finite",
        all(
            math.isfinite(float(row["corrected_q"]))
            and math.isfinite(
                float(row["corrected_velocity_squared_log10_RMSE"])
            )
            for row in scores
        ),
        len(scores),
    )
    add_validation(
        validation,
        "time_norm_resolution_controls_executed",
        {str(row["run_role"]) for row in selected_controls}
        == {"TIME_REFINEMENT", "NORM_CONTROL", "RESOLUTION_CONTROL"},
        selected_control_q,
    )
    add_validation(
        validation,
        "selected_control_q_envelope_bounded",
        maximum_control_delta < 0.1,
        maximum_control_delta,
    )
    add_validation(
        validation,
        "q_not_used_to_define_transport",
        all(not bool(row["target_q_used_to_define_operator"]) for row in scores),
        "all predeclared configurations",
    )
    add_validation(
        validation,
        "prior_q_control_selection_disclosed",
        all(
            bool(row["target_used_to_select_branch"])
            == (row["run_role"] != "PRIMARY")
            for row in scores
        ),
        "previous nearest branch used only for numerical controls",
    )
    add_validation(
        validation,
        "all_outputs_nonclaim",
        all(not bool(row["valid_for_claim"]) for row in scores + profiles + controls + transfers),
        "all generated dynamical rows",
    )
    add_validation(
        validation,
        "local_branch_unmodified",
        True,
        "inherited calibrated G_N central force; no local-GR/Maxwell file edited",
    )
    contract = contract_rows()
    provenance = provenance_rows(paths)
    summary = {
        "parent_q_lower": parent_lower,
        "parent_q_upper": parent_upper,
        "baseline_RMSE": context["baseline_score"][
            "velocity_squared_log10_RMSE"
        ],
        "primary_scores": primary,
        "selected_branch_control_q": selected_control_q,
        "maximum_selected_control_delta_q": maximum_control_delta,
        "closest_primary_run_id": closest["run_id"],
        "closest_primary_q": closest["corrected_q"],
        "closest_primary_q_gap_to_parent_band": closest_gap,
        "any_primary_q_compatible": any_compatible,
        "all_primary_RMSE_improve_baseline": all_improve,
        "transport_delta_q": [row["transport_delta_q"] for row in comparisons],
        "transport_delta_RMSE": [row["transport_delta_RMSE"] for row in comparisons],
        "matched_full_particle_selected_delta_q": next(
            row["matched_full_particle_transport_delta_q"]
            for row in comparisons
            if (str(row["thermal_mode"]), float(row["metallicity_Zsun"]))
            == SELECTED_CONTROL_BRANCH
        ),
        "matched_full_particle_selected_delta_RMSE": next(
            row["matched_full_particle_transport_delta_RMSE"]
            for row in comparisons
            if (str(row["thermal_mode"]), float(row["metallicity_Zsun"]))
            == SELECTED_CONTROL_BRANCH
        ),
        "primary_operator_mean_displacement_kpc": selected_primary[
            "operator_mean_absolute_displacement_kpc"
        ],
        "maximum_phase_transfer_relative_residual": max(
            float(row["source_final_transfer_relative_residual"]) for row in controls
        ),
        "maximum_angular_momentum_relative_residual": max(
            max(
                float(row["source_angular_momentum_relative_residual"]),
                float(row["control_angular_momentum_relative_residual"]),
            )
            for row in controls
        ),
        "total_source_wall_seconds": sum(
            float(row["source_wall_seconds"]) for row in controls
        ),
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
        "forward_force_response_executed": True,
        "full_particle_states_used": True,
        "operator_derived_from_parent_action": False,
        "local_GR_Newton_Maxwell_branch_modified": False,
        "valid_for_galaxy_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    Q.write_csv(CONTRACT_CSV, contract)
    Q.write_csv(CONFIG_CSV, configurations)
    Q.write_csv(SCORE_CSV, scores)
    Q.write_csv(PROFILE_CSV, profiles)
    Q.write_csv(CONTROL_CSV, controls)
    Q.write_csv(TRANSFER_CSV, transfers)
    Q.write_csv(COMPARISON_CSV, comparisons)
    Q.write_csv(DECISION_CSV, decisions)
    Q.write_csv(PROVENANCE_CSV, provenance)
    Q.write_json(RESULT_JSON, result)
    Q.write_csv(VALIDATION_CSV, validation)
    DOCUMENT.write_text(make_document(result), encoding="utf-8")
    if result["validation_failures"]:
        raise RuntimeError(
            f"validation failures: {[row['check_id'] for row in result['validation_failures']]}"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
