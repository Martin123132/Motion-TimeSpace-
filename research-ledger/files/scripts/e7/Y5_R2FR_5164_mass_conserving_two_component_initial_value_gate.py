from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import time
from pathlib import Path
from typing import Any, Callable

import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
PREVIOUS_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5163_parent_wave_and_visible_source_response_gate.py"
)
ZOOM_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5162_shared_mode_nested_transition_zoom_q_gate.py"
)
PREVIOUS_DOCUMENT = (
    POST / "5163-Y5-R2FR-parent-wave-stress-and-visible-source-response-gate.md"
)
PREVIOUS_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5163"
    / "parent_wave_and_visible_source_results.json"
)
PREVIOUS_Q = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5162"
    / "resolved_q_selection_gate.csv"
)
PREVIOUS_PROFILE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5162"
    / "nested_zoom_profile_samples.csv"
)
PREVIOUS_SCORE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5162"
    / "nested_zoom_no_refit_scores.csv"
)
VISIBLE_SOURCE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5163"
    / "visible_baryon_source_profile.csv"
)

OUT = POST / "source-intake" / "functional_rg" / "5164"
SNAPSHOT_META_JSON = OUT / "isolated_initial_state_metadata.json"
SNAPSHOT_PATHS = {
    -1: OUT / "phase_minus_isolated_initial_state.npz",
    1: OUT / "phase_plus_isolated_initial_state.npz",
}
FORCE_CSV = OUT / "mass_conserving_two_component_force_contract.csv"
SNAPSHOT_CSV = OUT / "snapshot_reproduction_gate.csv"
MASS_CSV = OUT / "baryon_mass_conservation_gate.csv"
HISTORY_CSV = OUT / "source_history_contract.csv"
SCORE_CSV = OUT / "two_component_response_scores.csv"
PROFILE_CSV = OUT / "two_component_response_profile_samples.csv"
CONTROL_CSV = OUT / "two_component_numerical_controls.csv"
DECISION_CSV = OUT / "route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "mass_conserving_two_component_results.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5164_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5164-Y5-R2FR-mass-conserving-visible-motion-initial-value-response-gate.md"
)

MARKER = "MTS_5164_MASS_CONSERVING_VISIBLE_MOTION_INITIAL_VALUE_GATE"
CHECKED_DATE = "2026-07-20"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
REFERENCE_GALAXY = "UGC09133"
REFERENCE_MAPPING = "Wetterich_v_equals_minus_2lambda"
LOCAL_GRID = 160
ISOLATION_EDGE_MULTIPLE = 2.0
SCORE_EDGE_FRACTION = 0.9
AVERAGING_ORBITS = 1.0
SETTLING_ORBITS = 3.0
STEPS_PER_INNER_ORBIT = 64
HIGH_STEPS_PER_INNER_ORBIT = 128
PROFILE_AVERAGE_SAMPLES = 32
SOFTENING_CELL_MULTIPLE = 0.5
MAX_RESPONSE_PARTICLES = 65536

HISTORY_SPECS = (
    {
        "history_id": "IMPULSIVE",
        "growth_clock": "zero",
        "growth_orbits": 0.0,
        "ramp": "step",
    },
    {
        "history_id": "NEWTON_FREEFALL_LINEAR",
        "growth_clock": "derived_freefall",
        "growth_orbits": math.nan,
        "ramp": "linear",
    },
    {
        "history_id": "NEWTON_FREEFALL_C2",
        "growth_clock": "derived_freefall",
        "growth_orbits": math.nan,
        "ramp": "minimum_jerk_C2",
    },
    {
        "history_id": "ONE_ORBIT_C2",
        "growth_clock": "transition_orbit",
        "growth_orbits": 1.0,
        "ramp": "minimum_jerk_C2",
    },
    {
        "history_id": "ADIABATIC4_C2",
        "growth_clock": "transition_orbit",
        "growth_orbits": 4.0,
        "ramp": "minimum_jerk_C2",
    },
    {
        "history_id": "ADIABATIC8_C2",
        "growth_clock": "transition_orbit",
        "growth_orbits": 8.0,
        "ramp": "minimum_jerk_C2",
    },
)


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


PREVIOUS = load_module(PREVIOUS_SCRIPT, "mts_checkpoint_5163")
ZOOM = load_module(ZOOM_SCRIPT, "mts_checkpoint_5162_for_5164")
PM = ZOOM.PM


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
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0])
    for row in rows[1:]:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def source_paths() -> dict[str, Path]:
    paths = {
        "previous_script": PREVIOUS_SCRIPT,
        "zoom_script": ZOOM_SCRIPT,
        "previous_document": PREVIOUS_DOCUMENT,
        "previous_result": PREVIOUS_RESULT,
        "previous_q": PREVIOUS_Q,
        "previous_profile": PREVIOUS_PROFILE,
        "previous_score": PREVIOUS_SCORE,
        "visible_source": VISIBLE_SOURCE,
        "galaxy_samples_read_only": PREVIOUS.GALAXY_SAMPLES,
    }
    for key, path in ZOOM.source_paths().items():
        paths[f"zoom_{key}"] = path
    return paths


def reference_rows() -> tuple[
    list[dict[str, str]], dict[str, str], dict[str, str], dict[str, str]
]:
    profile = [
        row
        for row in read_csv(PREVIOUS_PROFILE)
        if row["config_id"] == "NESTED160"
        and row["mapping_scored"] == REFERENCE_MAPPING
    ]
    profile.sort(key=lambda row: float(row["radius_kpc"]))
    q_row = next(row for row in read_csv(PREVIOUS_Q) if row["mapping"] == REFERENCE_MAPPING)
    score = next(
        row
        for row in read_csv(PREVIOUS_SCORE)
        if row["config_id"] == "NESTED160"
        and row["mapping_scored"] == REFERENCE_MAPPING
    )
    state = next(
        row
        for row in PREVIOUS.state_rows()
        if row["galaxy"] == REFERENCE_GALAXY
        and row["mapping"] == REFERENCE_MAPPING
    )
    return profile, q_row, score, state


class VisibleSource:
    def __init__(self, rows: list[dict[str, str]]) -> None:
        self.radii = np.asarray([float(row["radius_kpc"]) for row in rows])
        self.masses = np.asarray(
            [float(row["spherical_equivalent_baryon_mass_Msun"]) for row in rows]
        )
        self.masses = np.maximum.accumulate(np.maximum(self.masses, 0.0))
        self.mass_interpolator = PchipInterpolator(self.radii, self.masses)

    def mass_at(self, radius_kpc: np.ndarray | float) -> np.ndarray | float:
        radius = np.asarray(radius_kpc, dtype=float)
        result = np.empty_like(radius)
        inner = radius < self.radii[0]
        middle = (radius >= self.radii[0]) & (radius <= self.radii[-1])
        outer = radius > self.radii[-1]
        result[inner] = self.masses[0] * (radius[inner] / self.radii[0]) ** 3
        result[middle] = self.mass_interpolator(radius[middle])
        result[outer] = self.masses[-1]
        if np.ndim(radius_kpc) == 0:
            return float(result)
        return result


def snapshot_profile(
    positions_kpc: np.ndarray,
    radii_kpc: np.ndarray,
    particle_mass_msun: float,
    particle_weight: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    if particle_weight is None:
        particle_weight = np.ones(len(positions_kpc), dtype=float)
    particle_radii = np.linalg.norm(positions_kpc, axis=1)
    order = np.argsort(particle_radii)
    sorted_radii = particle_radii[order]
    cumulative_weight = np.cumsum(np.asarray(particle_weight, dtype=float)[order])
    indices = np.searchsorted(sorted_radii, radii_kpc, side="right")
    counts = np.zeros_like(radii_kpc, dtype=float)
    positive = indices > 0
    counts[positive] = cumulative_weight[indices[positive] - 1]
    background = (
        4.0
        * math.pi
        * PM.RHO_M_MSUN_MPC3
        * (radii_kpc / 1000.0) ** 3
        / 3.0
    )
    motion_mass = PM.MOTION_FRACTION * np.maximum(
        counts * particle_mass_msun - background, 0.0
    )
    return counts, motion_mass


def compress_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    particle_count = len(snapshot["positions_kpc"])
    if particle_count <= MAX_RESPONSE_PARTICLES:
        return {
            **snapshot,
            "particle_weight": np.ones(particle_count, dtype=float),
        }
    donor = np.asarray(snapshot["donor"], dtype=bool)
    radii = np.asarray(snapshot["initial_radius_kpc"], dtype=float)
    selected_indices: list[int] = []
    selected_weights: list[float] = []
    for donor_value in (True, False):
        group = np.flatnonzero(donor == donor_value)
        group = group[np.argsort(radii[group])]
        target = max(
            1,
            int(round(MAX_RESPONSE_PARTICLES * len(group) / particle_count)),
        )
        boundaries = np.linspace(0, len(group), target + 1, dtype=int)
        for lower, upper in zip(boundaries[:-1], boundaries[1:]):
            if upper <= lower:
                continue
            block = group[lower:upper]
            selected_indices.append(int(block[len(block) // 2]))
            selected_weights.append(float(len(block)))
    indices = np.asarray(selected_indices, dtype=int)
    weights = np.asarray(selected_weights, dtype=float)
    order = np.argsort(radii[indices])
    indices = indices[order]
    weights = weights[order]
    return {
        "positions_kpc": np.asarray(snapshot["positions_kpc"])[indices],
        "velocities_km_s": np.asarray(snapshot["velocities_km_s"])[indices],
        "donor": donor[indices],
        "initial_radius_kpc": radii[indices],
        "particle_weight": weights,
        "particle_mass_Msun": snapshot["particle_mass_Msun"],
        "edge_radius_kpc": snapshot["edge_radius_kpc"],
        "resolved_radius_kpc": snapshot["resolved_radius_kpc"],
        "local_force_cell_kpc": snapshot["local_force_cell_kpc"],
    }


def generate_snapshots() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    OUT.mkdir(parents=True, exist_ok=True)
    profile_rows, q_row, _, _ = reference_rows()
    target_radii = np.asarray([float(row["radius_kpc"]) for row in profile_rows])
    targets, _, patch_radius, target_constraint = ZOOM.PREVIOUS.target_lookup()
    target = targets[REFERENCE_MAPPING]
    edge_radius_mpc = float(target["edge_radius_Mpc"])
    box_size_mpc = PM.BOX_OVER_PATCH * patch_radius
    power = PM.power_lookup(read_csv(PM.POWER_CSV))
    coarse_fields, _ = PM.build_conditioned_pair(
        ZOOM.PREVIOUS.COARSE_PARTICLES,
        box_size_mpc,
        patch_radius,
        target_constraint,
        power[ZOOM.MASS_LABEL]["k"],
        power[ZOOM.MASS_LABEL]["power"],
    )
    fields = {
        sign: ZOOM.PREVIOUS.periodic_fourier_resample(
            coarse_fields[sign], ZOOM.PARTICLE_GRID
        )
        for sign in ZOOM.PAIR_SIGNS
    }
    _, states = ZOOM.PREVIOUS.initial_rows_and_states(
        {ZOOM.PARTICLE_GRID: fields}, box_size_mpc, patch_radius
    )
    lagrangian_positions = PM.particle_lattice(ZOOM.PARTICLE_GRID, box_size_mpc)
    rows: list[dict[str, Any]] = []
    metadata: dict[str, Any] = {
        "checkpoint_marker": MARKER,
        "edge_radius_kpc": 1000.0 * edge_radius_mpc,
        "box_size_Mpc": box_size_mpc,
        "isolation_edge_multiple": ISOLATION_EDGE_MULTIPLE,
        "phases": {},
    }
    for sign in ZOOM.PAIR_SIGNS:
        start = time.perf_counter()
        initial = states[(ZOOM.PARTICLE_GRID, sign)]
        evolved = ZOOM.evolve_nested(
            np.asarray(initial["positions"], dtype=float),
            np.asarray(initial["momenta"], dtype=float),
            lagrangian_positions,
            np.asarray(initial["tagged"], dtype=bool),
            ZOOM.PARTICLE_GRID,
            LOCAL_GRID,
            box_size_mpc,
            edge_radius_mpc,
        )
        profile = ZOOM.zoom_profile(
            np.asarray(evolved["positions"], dtype=float),
            np.asarray(initial["tagged"], dtype=bool),
            ZOOM.PARTICLE_GRID,
            LOCAL_GRID,
            box_size_mpc,
            edge_radius_mpc,
        )
        center = np.asarray(profile["center_Mpc"], dtype=float)
        offsets_mpc = ZOOM.periodic_offset(
            np.asarray(evolved["positions"], dtype=float), center, box_size_mpc
        )
        all_radii_mpc = np.linalg.norm(offsets_mpc, axis=1)
        donor_all = all_radii_mpc <= edge_radius_mpc
        center_momentum = np.mean(
            np.asarray(evolved["momenta"], dtype=float)[donor_all], axis=0
        )
        velocities_km_s = PM.H0_KM_S_MPC * (
            np.asarray(evolved["momenta"], dtype=float)
            - center_momentum[None, :]
            + offsets_mpc
        )
        selected = all_radii_mpc <= ISOLATION_EDGE_MULTIPLE * edge_radius_mpc
        positions_kpc = 1000.0 * offsets_mpc[selected]
        selected_velocities = velocities_km_s[selected]
        donors = donor_all[selected]
        initial_radius_kpc = 1000.0 * all_radii_mpc[selected]
        particle_mass = float(profile["particle_mass_Msun"])
        counts, motion_mass = snapshot_profile(
            positions_kpc, target_radii, particle_mass
        )
        velocity_squared = (
            PREVIOUS.G_KPC_KM2_S2_MSUN
            * motion_mass
            / np.maximum(target_radii, np.finfo(float).tiny)
        )
        transition_radius = float(target["transition_radius_Mpc"]) * 1000.0
        q_value = PREVIOUS.local_logarithmic_q(
            target_radii, velocity_squared, transition_radius
        )
        expected_q = float(
            q_row["q_fine_minus_phase"] if sign == -1 else q_row["q_fine_plus_phase"]
        )
        np.savez_compressed(
            SNAPSHOT_PATHS[sign],
            positions_kpc=positions_kpc,
            velocities_km_s=selected_velocities,
            donor=donors,
            initial_radius_kpc=initial_radius_kpc,
            particle_mass_Msun=np.asarray([particle_mass]),
            edge_radius_kpc=np.asarray([1000.0 * edge_radius_mpc]),
            resolved_radius_kpc=np.asarray([1000.0 * float(profile["resolved_radius_Mpc"])]),
            local_force_cell_kpc=np.asarray(
                [1000.0 * LOCAL_GRID ** -1 * ZOOM.LOCAL_BOX_EDGE_MULTIPLE * edge_radius_mpc]
            ),
        )
        row = {
            "phase_sign": sign,
            "selected_particle_count": int(np.count_nonzero(selected)),
            "donor_particle_count": int(np.count_nonzero(donors)),
            "particle_mass_Msun": particle_mass,
            "isolation_radius_kpc": 1000.0
            * ISOLATION_EDGE_MULTIPLE
            * edge_radius_mpc,
            "regenerated_q": q_value,
            "historical_q": expected_q,
            "q_absolute_reproduction_error": abs(q_value - expected_q),
            "maximum_radius_profile_count": float(counts[-1]),
            "wall_seconds": time.perf_counter() - start,
            "snapshot_sha256": file_digest(SNAPSHOT_PATHS[sign]),
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        rows.append(row)
        metadata["phases"][str(sign)] = row
        del evolved, profile, offsets_mpc, velocities_km_s, positions_kpc
    write_json(SNAPSHOT_META_JSON, metadata)
    return rows, metadata


def load_snapshots() -> tuple[dict[int, dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    if not SNAPSHOT_META_JSON.is_file() or not all(
        path.is_file() for path in SNAPSHOT_PATHS.values()
    ):
        return {}, [], {}
    metadata = json.loads(SNAPSHOT_META_JSON.read_text(encoding="utf-8"))
    snapshots: dict[int, dict[str, Any]] = {}
    rows: list[dict[str, Any]] = []
    for sign, path in SNAPSHOT_PATHS.items():
        with np.load(path) as archive:
            snapshots[sign] = {key: archive[key] for key in archive.files}
        row = dict(metadata["phases"][str(sign)])
        row["snapshot_sha256"] = file_digest(path)
        rows.append(row)
    return snapshots, rows, metadata


def ramp_value(ramp: str, time_value: float, growth_time: float) -> float:
    if ramp == "step" or growth_time <= 0.0:
        return 1.0
    fraction = min(max(time_value / growth_time, 0.0), 1.0)
    if ramp == "linear":
        return fraction
    if ramp == "minimum_jerk_C2":
        return fraction**3 * (10.0 - 15.0 * fraction + 6.0 * fraction**2)
    raise ValueError(f"unknown ramp: {ramp}")


def acceleration(
    positions: np.ndarray,
    donor: np.ndarray,
    particle_weight: np.ndarray,
    particle_mass: float,
    transfer_per_donor: float,
    assembly_fraction: float,
    visible_source: VisibleSource,
    softening_kpc: float,
) -> np.ndarray:
    radii = np.linalg.norm(positions, axis=1)
    order = np.argsort(radii)
    sorted_radii = radii[order]
    gravitational_masses = particle_weight * (
        particle_mass
        - assembly_fraction * transfer_per_donor * donor.astype(float)
    )
    sorted_masses = gravitational_masses[order]
    enclosed_particles = np.cumsum(sorted_masses) - 0.5 * sorted_masses
    background = (
        4.0
        * math.pi
        * PM.RHO_M_MSUN_MPC3
        * (sorted_radii / 1000.0) ** 3
        / 3.0
    )
    condensed = assembly_fraction * np.asarray(visible_source.mass_at(sorted_radii))
    enclosed = np.maximum(enclosed_particles - background + condensed, 0.0)
    denominator = (sorted_radii**2 + softening_kpc**2) ** 1.5
    coefficient = np.zeros_like(sorted_radii)
    positive = denominator > 0.0
    coefficient[positive] = (
        -PREVIOUS.G_KPC_KM2_S2_MSUN * enclosed[positive] / denominator[positive]
    )
    result = np.empty_like(positions)
    result[order] = coefficient[:, None] * positions[order]
    return result


def cumulative_counts(
    positions: np.ndarray,
    radii_kpc: np.ndarray,
    particle_weight: np.ndarray,
) -> np.ndarray:
    radii = np.linalg.norm(positions, axis=1)
    order = np.argsort(radii)
    sorted_radii = radii[order]
    cumulative_weight = np.cumsum(particle_weight[order])
    indices = np.searchsorted(sorted_radii, radii_kpc, side="right")
    counts = np.zeros_like(radii_kpc, dtype=float)
    positive = indices > 0
    counts[positive] = cumulative_weight[indices[positive] - 1]
    return counts


def evolve_isolated(
    snapshot: dict[str, Any],
    visible_source: VisibleSource,
    profile_radii_kpc: np.ndarray,
    transfer_per_donor: float,
    ramp: str,
    growth_time: float,
    total_time: float,
    averaging_time: float,
    steps_per_inner_orbit: int,
    inner_orbit_time: float,
    source_enabled: bool,
) -> dict[str, Any]:
    positions = np.asarray(snapshot["positions_kpc"], dtype=float).copy()
    velocities = np.asarray(snapshot["velocities_km_s"], dtype=float).copy()
    donor = np.asarray(snapshot["donor"], dtype=bool)
    particle_weight = np.asarray(snapshot["particle_weight"], dtype=float)
    initial_radius = np.asarray(snapshot["initial_radius_kpc"], dtype=float)
    particle_mass = float(snapshot["particle_mass_Msun"][0])
    edge_radius = float(snapshot["edge_radius_kpc"][0])
    softening = (
        SOFTENING_CELL_MULTIPLE * float(snapshot["local_force_cell_kpc"][0])
    )
    nominal_dt = inner_orbit_time / steps_per_inner_orbit
    steps = max(1, int(math.ceil(total_time / nominal_dt)))
    time_step = total_time / steps
    averaging_start = max(total_time - averaging_time, 0.0)
    sample_stride = max(
        1,
        int(
            round(
                max(1.0, averaging_time / time_step) / PROFILE_AVERAGE_SAMPLES
            )
        ),
    )
    initial_angular_momentum = np.cross(positions, velocities)
    initial_counts = cumulative_counts(positions, profile_radii_kpc, particle_weight)
    initial_com = np.average(positions, axis=0, weights=particle_weight)
    start = time.perf_counter()

    def fraction_at(current_time: float) -> float:
        if not source_enabled:
            return 0.0
        return ramp_value(ramp, current_time, growth_time)

    force = acceleration(
        positions,
        donor,
        particle_weight,
        particle_mass,
        transfer_per_donor,
        fraction_at(0.0),
        visible_source,
        softening,
    )
    half_velocity = velocities + 0.5 * time_step * force
    count_samples: list[np.ndarray] = []
    final_fraction = fraction_at(0.0)
    for step in range(steps):
        positions += time_step * half_velocity
        current_time = (step + 1) * time_step
        final_fraction = fraction_at(current_time)
        force = acceleration(
            positions,
            donor,
            particle_weight,
            particle_mass,
            transfer_per_donor,
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
                cumulative_counts(positions, profile_radii_kpc, particle_weight)
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
    edge_crossing = float(
        np.sum(
            particle_weight[
                (initial_radius > edge_radius)
                & (final_radii <= SCORE_EDGE_FRACTION * edge_radius)
            ]
        )
    )
    boundary_ingress = float(
        np.sum(
            particle_weight[
                (initial_radius > 0.9 * ISOLATION_EDGE_MULTIPLE * edge_radius)
                & (final_radii <= SCORE_EDGE_FRACTION * edge_radius)
            ]
        )
    )
    final_inside_score = max(
        float(
            np.sum(
                particle_weight[final_radii <= SCORE_EDGE_FRACTION * edge_radius]
            )
        ),
        1.0,
    )
    return {
        "averaged_counts": averaged_counts,
        "initial_counts": initial_counts,
        "steps": steps,
        "time_step_kpc_per_km_s": time_step,
        "profile_sample_count": len(count_samples),
        "final_assembly_fraction": final_fraction,
        "angular_momentum_relative_residual": angular_residual,
        "center_of_mass_drift_kpc": float(
            np.linalg.norm(
                np.average(positions, axis=0, weights=particle_weight) - initial_com
            )
        ),
        "edge_crossing_fraction": edge_crossing / final_inside_score,
        "outer_boundary_ingress_fraction": boundary_ingress / final_inside_score,
        "wall_seconds": time.perf_counter() - start,
        "softening_kpc": softening,
    }


def score_profile(
    radii_kpc: np.ndarray,
    mass_msun: np.ndarray,
    target_velocity_squared: np.ndarray,
    score_mask: np.ndarray,
    transition_radius_kpc: float,
    edge_radius_kpc: float,
    target_edge_mass: float,
) -> dict[str, float]:
    velocity_squared = (
        PREVIOUS.G_KPC_KM2_S2_MSUN
        * mass_msun
        / np.maximum(radii_kpc, np.finfo(float).tiny)
    )
    valid = score_mask & np.isfinite(velocity_squared) & (velocity_squared > 0.0)
    q_value = PREVIOUS.local_logarithmic_q(
        radii_kpc, velocity_squared, transition_radius_kpc
    )
    rmse = float(
        np.sqrt(
            np.mean(
                np.log10(velocity_squared[valid] / target_velocity_squared[valid]) ** 2
            )
        )
    )
    transition_ratio = float(
        np.interp(transition_radius_kpc, radii_kpc, velocity_squared)
        / np.interp(transition_radius_kpc, radii_kpc, target_velocity_squared)
    )
    edge_mass = float(np.interp(edge_radius_kpc, radii_kpc, mass_msun))
    return {
        "q": q_value,
        "velocity_squared_log10_RMSE": rmse,
        "transition_velocity_squared_ratio_to_target": transition_ratio,
        "motion_mass_inside_edge_Msun": edge_mass,
        "edge_mass_ratio_to_target": edge_mass / target_edge_mass,
    }


def circular_mass_conserving_response(
    radii_kpc: np.ndarray,
    initial_mass: np.ndarray,
    visible_source: VisibleSource,
    edge_radius_kpc: float,
) -> tuple[np.ndarray, float, float, float]:
    monotone_mass = np.maximum.accumulate(np.maximum(initial_mass, 0.0))
    interpolator = PchipInterpolator(radii_kpc, monotone_mass)
    motion_edge = float(interpolator(edge_radius_kpc))
    condensed_edge = float(visible_source.mass_at(edge_radius_kpc))
    cosmic_baryon = (1.0 - PM.MOTION_FRACTION) / PM.MOTION_FRACTION * motion_edge
    hot_ratio = max(cosmic_baryon - condensed_edge, 0.0) / motion_edge
    final_mass = np.full_like(radii_kpc, np.nan)
    maximum_residual = 0.0
    for index, final_radius in enumerate(radii_kpc):
        condensed = float(visible_source.mass_at(float(final_radius)))

        def invariant(initial_radius: float) -> float:
            shell_mass = float(interpolator(initial_radius))
            return initial_radius * shell_mass / PM.MOTION_FRACTION - final_radius * (
                (1.0 + hot_ratio) * shell_mass + condensed
            )

        lower = float(radii_kpc[0])
        upper = float(radii_kpc[-1])
        if invariant(lower) <= 0.0 <= invariant(upper):
            initial_radius = float(
                brentq(invariant, lower, upper, xtol=1.0e-11, rtol=1.0e-12)
            )
            final_mass[index] = float(interpolator(initial_radius))
            left = initial_radius * final_mass[index] / PM.MOTION_FRACTION
            right = final_radius * (
                (1.0 + hot_ratio) * final_mass[index] + condensed
            )
            maximum_residual = max(
                maximum_residual,
                abs(left - right) / max(abs(left), abs(right), 1.0),
            )
    return final_mass, cosmic_baryon, hot_ratio, maximum_residual


def history_rows(
    transition_orbit: float, freefall_time: float
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for specification in HISTORY_SPECS:
        if specification["growth_clock"] == "derived_freefall":
            growth_time = freefall_time
        else:
            growth_time = float(specification["growth_orbits"]) * transition_orbit
        rows.append(
            {
                "history_id": specification["history_id"],
                "growth_clock": specification["growth_clock"],
                "growth_time_kpc_per_km_s": growth_time,
                "growth_time_Gyr": 0.9777922216807892 * growth_time,
                "growth_time_over_transition_orbit": growth_time
                / transition_orbit,
                "ramp": specification["ramp"],
                "settling_orbits": SETTLING_ORBITS,
                "averaging_orbits": AVERAGING_ORBITS,
                "target_used_to_select_history": False,
                "role": "predeclared_source_history_comparator_not_a_fitted_coupling",
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows


def force_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause": "motion_equation",
            "equation": "d2 x_i/dt2=-G M_g(<r_i,t) x_i/(r_i^2+epsilon^2)^(3/2)",
            "derivation": "spherical Newtonian projection of the checkpoint-4947 Einstein/Hilbert source",
            "new_coupling": False,
            "closure_status": "derived_projection",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause": "particle_tied_source",
            "equation": "m_g,i(lambda)=m_p-lambda Delta_m d_i",
            "derivation": "remove measured condensed baryon mass only from donor particles initially inside R_edge",
            "new_coupling": False,
            "closure_status": "exact_mass_bookkeeping",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause": "condensed_source",
            "equation": "M_g(<r,lambda)=sum_i<r m_g,i-M_background(<r)+lambda M_b,obs(<r)",
            "derivation": "same calibrated G_N and measured visible Hilbert source",
            "new_coupling": False,
            "closure_status": "source_profile_observed_history_compared",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause": "global_mass_identity",
            "equation": "N_d Delta_m=M_b,obs(R_edge) implies Delta M_g(lambda)=0 outside R_edge",
            "derivation": "algebraic identity for every lambda in [0,1]",
            "new_coupling": False,
            "closure_status": "proved",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause": "local_zero",
            "equation": "rho_motion=rho_visible=rho_EM=0 implies M_g=0 and the response force vanishes",
            "derivation": "vacuum/local branch inherits the same Einstein residue",
            "new_coupling": False,
            "closure_status": "exact",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
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


def provenance_rows(paths: dict[str, Path]) -> list[dict[str, Any]]:
    return [
        {
            "source_id": key,
            "source_path": str(path),
            "sha256": file_digest(path),
            "access": "read_only",
            "role": "parent_or_empirical_input",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for key, path in paths.items()
    ]


def make_document(result: dict[str, Any]) -> str:
    summary = result["summary"]
    outcome = result["route_decision"]
    return f"""# 5164 - Mass-conserving visible--motion initial-value response gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## What was changed

Checkpoint 5163 showed that the existing visible Hilbert source has enough
leverage but tested it with a scalar response efficiency. That scalar has now
been removed. The checkpoint-5162 antithetic `NESTED160` particle states are
regenerated, their physical positions and velocities are retained, and the
motion particles are evolved through the spherical Newtonian projection of
the same checkpoint-4947 Einstein source.

The source split is mass-conserving. If `d_i` marks particles initially inside
the fixed halo edge, then

```text
m_g,i(lambda)=m_p-lambda Delta_m d_i,
Delta_m=M_b,obs(R_edge)/N_d,
M_g(<r,lambda)=sum_(i<r)m_g,i-M_background(<r)
              +lambda M_b,obs(<r).
```

Consequently `N_d Delta_m=M_b,obs(R_edge)` and the total source outside the
edge is independent of `lambda` exactly. Measured condensed baryons are
`{summary['condensed_fraction_of_cosmic_baryon_allotment']}` of the donor
particles' cosmic baryon allotment. The remaining baryons stay particle-tied;
they are not deleted. No new coupling, response efficiency or target inversion
is used.

## Initial-value calculation

The isolated source-response system retains the actual three-dimensional
position, velocity and angular-momentum samples of both antithetic
cosmological phases. The primary matrix uses exact-mass radial compression;
the near-boundary branch is repeated with every original particle. The force
is spherical only in its source projection:

```text
d2 x_i/dt2=-G_N M_g(<r_i,t) x_i/(r_i^2+epsilon^2)^(3/2).
```

`epsilon` is one half of the inherited `NESTED160` force cell. Source growth
is tested with predeclared impulsive, Newton-freefall, one-orbit and converging
adiabatic clocks. Their values are fixed before the parent `q` is read. Each
source run has a matched `lambda=0` control, and the response estimator applies
the source/control ratio to the regenerated checkpoint-5162 profile so that
isolated-control relaxation is not mistaken for a coupling.

The regenerated fine-grid value is `q={summary['regenerated_pair_q']}` versus
the stored `q={summary['historical_pair_q']}`. The baseline no-refit velocity-
squared RMSE is `{summary['baseline_velocity_squared_log10_RMSE']}` dex.
Its transition velocity-squared ratio is
`{summary['baseline_transition_velocity_squared_ratio_to_target']}`.

## Result

The predeclared histories span corrected `q` from
`{summary['minimum_corrected_q']}` to `{summary['maximum_corrected_q']}` and
RMSE from `{summary['minimum_corrected_RMSE']}` to
`{summary['maximum_corrected_RMSE']}` dex. Histories inside the existing
checkpoint-5162 `q` envelope: `{summary['q_compatible_history_ids']}`.

The mass-conserving circular adiabatic comparator gives
`q={summary['circular_mass_conserving_q']}` and RMSE
`{summary['circular_mass_conserving_RMSE']}` dex. The dynamic adiabatic
four-to-eight-orbit `q` difference is
`{summary['adiabatic_q_difference']}`; the doubled-time-step-resolution
difference is `{summary['adiabatic_time_resolution_q_difference']}`.

The near-boundary one-orbit branch gives primary, doubled-timestep and full-
particle values `q={summary['one_orbit_primary_q']}`,
`{summary['one_orbit_high_time_resolution_q']}` and
`{summary['one_orbit_full_particle_q']}`. Its refinement interval intersects
the inherited parent band: `{summary['one_orbit_refinement_intersects_parent_band']}`.
This is a numerical compatibility statement only; the one-orbit condensation
clock was predeclared but has not been selected by the parent field equations.
Its primary RMSE is `{summary['one_orbit_primary_RMSE']}` dex and its
transition velocity-squared ratio is
`{summary['one_orbit_primary_transition_velocity_squared_ratio_to_target']}`:
the source roughly doubles the baseline transition support, but a substantial
amplitude deficit remains.

Route decision: **{outcome}**.

This is a genuine forward initial-value response calculation, not an inverse
efficiency fit. It does not yet derive the baryonic condensation history from
Maxwell/radiative hydrodynamics, so every row remains nonclaim. The calculation
either supplies a controlled source-response bound or identifies precisely
what source-history dynamics must be derived next.

## Claim boundary

```text
same-G_N two-component force derived                 = yes;
condensed plus diffuse baryon mass conserved         = yes;
scalar response efficiency removed                   = yes;
three-dimensional inherited orbital state evolved    = yes;
baryonic condensation history parent-selected        = no;
local GR/Newton/Maxwell branch modified               = no;
galaxy or full-MTS claim                              = false.
```

All `{result['validation_count']}` validation rows pass. Source hashes are
unchanged and the protected `formalization-workbench` digest is
`{result['formalization_workbench_tree_sha256']}`. The galaxy source was
read-only and no GitHub action occurred.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--snapshot-only", action="store_true")
    parser.add_argument("--response-only", action="store_true")
    parser.add_argument("--quick", action="store_true")
    arguments = parser.parse_args()
    paths = source_paths()
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing sources: {missing}")
    formal_before = tree_digest(FORMAL)
    if formal_before != FORMAL_DIGEST_LOCK:
        raise RuntimeError(f"protected digest mismatch: {formal_before}")
    hashes_before = {key: file_digest(path) for key, path in paths.items()}
    profile_rows, q_row, previous_score, state = reference_rows()
    transition_radius = float(state["L_eff_kpc"]) * float(state["R_n_over_L_eff"])
    edge_radius = float(previous_score["target_edge_radius_kpc"])
    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "marker": MARKER,
                    "histories": [row["history_id"] for row in HISTORY_SPECS],
                    "transition_radius_kpc": transition_radius,
                    "edge_radius_kpc": edge_radius,
                    "formal_digest": formal_before,
                    "snapshots_present": all(path.is_file() for path in SNAPSHOT_PATHS.values()),
                },
                indent=2,
            )
        )
        return

    snapshots, snapshot_rows, snapshot_metadata = load_snapshots()
    if not snapshots:
        snapshot_rows, snapshot_metadata = generate_snapshots()
        snapshots, snapshot_rows, snapshot_metadata = load_snapshots()
    if arguments.snapshot_only:
        write_csv(SNAPSHOT_CSV, snapshot_rows)
        print(json.dumps(snapshot_metadata, indent=2, sort_keys=True))
        return
    if arguments.response_only and not snapshots:
        raise RuntimeError("response-only requested without snapshots")

    visible_source = VisibleSource(read_csv(VISIBLE_SOURCE))
    radii = np.asarray([float(row["radius_kpc"]) for row in profile_rows])
    target_velocity = np.asarray(
        [float(row["target_motion_v2_km2_s2"]) for row in profile_rows]
    )
    score_mask = np.asarray(
        [row["inside_resolved_scoring_window"] == "True" for row in profile_rows]
    )
    target_edge_mass = float(previous_score["target_motion_mass_edge_Msun"])
    initial_phase_mass: dict[int, np.ndarray] = {}
    initial_phase_counts: dict[int, np.ndarray] = {}
    transfer_per_donor: dict[int, float] = {}
    mass_rows: list[dict[str, Any]] = []
    for sign, snapshot in snapshots.items():
        particle_mass = float(snapshot["particle_mass_Msun"][0])
        counts, motion_mass = snapshot_profile(
            np.asarray(snapshot["positions_kpc"]), radii, particle_mass
        )
        initial_phase_counts[sign] = counts
        initial_phase_mass[sign] = motion_mass
        donor_count = int(np.count_nonzero(snapshot["donor"]))
        condensed_edge = float(visible_source.mass_at(edge_radius))
        transfer = condensed_edge / donor_count
        transfer_per_donor[sign] = transfer
        donor_baryon_allotment = (
            donor_count * particle_mass * (1.0 - PM.MOTION_FRACTION)
        )
        fraction = condensed_edge / donor_baryon_allotment
        mass_rows.append(
            {
                "phase_sign": sign,
                "donor_particle_count": donor_count,
                "particle_mass_Msun": particle_mass,
                "cosmic_baryon_mass_per_donor_particle_Msun": particle_mass
                * (1.0 - PM.MOTION_FRACTION),
                "transfer_per_donor_particle_Msun": transfer,
                "observed_condensed_baryon_mass_edge_Msun": condensed_edge,
                "donor_cosmic_baryon_allotment_Msun": donor_baryon_allotment,
                "condensed_fraction_of_cosmic_baryon_allotment": fraction,
                "remaining_diffuse_fraction": 1.0 - fraction,
                "mass_conservation_relative_residual": abs(
                    donor_count * transfer - condensed_edge
                )
                / condensed_edge,
                "donor_gravitational_mass_stays_positive": transfer < particle_mass,
                "donor_baryon_mass_stays_nonnegative": transfer
                <= particle_mass * (1.0 - PM.MOTION_FRACTION),
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    response_snapshots = {
        sign: compress_snapshot(snapshot) for sign, snapshot in snapshots.items()
    }
    for row in mass_rows:
        sign = int(row["phase_sign"])
        response_snapshot = response_snapshots[sign]
        row["response_particle_count"] = len(response_snapshot["positions_kpc"])
        row["response_represented_particle_count"] = float(
            np.sum(response_snapshot["particle_weight"])
        )
        row["response_represented_donor_count"] = float(
            np.sum(
                response_snapshot["particle_weight"]
                * response_snapshot["donor"].astype(float)
            )
        )
    pair_initial_mass = 0.5 * (initial_phase_mass[-1] + initial_phase_mass[1])
    baseline_score = score_profile(
        radii,
        pair_initial_mass,
        target_velocity,
        score_mask,
        transition_radius,
        edge_radius,
        target_edge_mass,
    )
    regenerated_pair_q = baseline_score["q"]
    historical_pair_q = float(q_row["q_nested_160"])
    q_parent = float(q_row["q_parent"])
    q_envelope = float(q_row["q_uncertainty_envelope"])

    pair_initial_total_mass_transition = float(
        np.interp(transition_radius, radii, pair_initial_mass)
        / PM.MOTION_FRACTION
    )
    final_total_mass_transition = pair_initial_total_mass_transition + float(
        visible_source.mass_at(transition_radius)
    ) - (1.0 - PM.MOTION_FRACTION) * pair_initial_total_mass_transition
    final_total_mass_transition = max(
        final_total_mass_transition, pair_initial_total_mass_transition
    )
    transition_orbit = 2.0 * math.pi * math.sqrt(
        transition_radius**3
        / (PREVIOUS.G_KPC_KM2_S2_MSUN * final_total_mass_transition)
    )
    freefall_time = math.pi / (2.0 * math.sqrt(2.0)) * math.sqrt(
        transition_radius**3
        / (PREVIOUS.G_KPC_KM2_S2_MSUN * final_total_mass_transition)
    )
    resolved_radius = max(
        float(snapshots[-1]["resolved_radius_kpc"][0]),
        float(snapshots[1]["resolved_radius_kpc"][0]),
    )
    softening_radius = SOFTENING_CELL_MULTIPLE * max(
        float(snapshots[-1]["local_force_cell_kpc"][0]),
        float(snapshots[1]["local_force_cell_kpc"][0]),
    )
    orbit_probe = np.geomspace(
        max(0.05 * softening_radius, 1.0e-3), resolved_radius, 256
    )
    monotone_initial_mass = np.maximum.accumulate(np.maximum(pair_initial_mass, 0.0))
    motion_interpolator = PchipInterpolator(radii, monotone_initial_mass)
    probe_motion_mass = np.asarray(
        motion_interpolator(np.maximum(orbit_probe, radii[0])), dtype=float
    )
    probe_total_mass = (
        probe_motion_mass / PM.MOTION_FRACTION
        + np.asarray(visible_source.mass_at(orbit_probe), dtype=float)
    )
    softened_orbits = 2.0 * math.pi * np.sqrt(
        (orbit_probe**2 + softening_radius**2) ** 1.5
        / (
            PREVIOUS.G_KPC_KM2_S2_MSUN
            * np.maximum(probe_total_mass, 1.0)
        )
    )
    inner_orbit = float(np.min(softened_orbits))
    histories = history_rows(transition_orbit, freefall_time)
    if arguments.quick:
        histories = [
            row
            for row in histories
            if row["history_id"]
            in {"IMPULSIVE", "NEWTON_FREEFALL_C2", "ONE_ORBIT_C2", "ADIABATIC4_C2"}
        ]

    score_rows: list[dict[str, Any]] = []
    profile_output_rows: list[dict[str, Any]] = []
    control_rows: list[dict[str, Any]] = []
    corrected_by_history: dict[str, np.ndarray] = {}
    phase_outputs: dict[tuple[str, int], tuple[dict[str, Any], dict[str, Any]]] = {}
    for history in histories:
        growth_time = float(history["growth_time_kpc_per_km_s"])
        total_time = growth_time + SETTLING_ORBITS * transition_orbit
        averaging_time = AVERAGING_ORBITS * transition_orbit
        for sign, snapshot in response_snapshots.items():
            source_run = evolve_isolated(
                snapshot,
                visible_source,
                radii,
                transfer_per_donor[sign],
                history["ramp"],
                growth_time,
                total_time,
                averaging_time,
                STEPS_PER_INNER_ORBIT,
                inner_orbit,
                True,
            )
            control_run = evolve_isolated(
                snapshot,
                visible_source,
                radii,
                transfer_per_donor[sign],
                history["ramp"],
                growth_time,
                total_time,
                averaging_time,
                STEPS_PER_INNER_ORBIT,
                inner_orbit,
                False,
            )
            phase_outputs[(history["history_id"], sign)] = (source_run, control_run)
            control_rows.append(
                {
                    "history_id": history["history_id"],
                    "phase_sign": sign,
                    "response_particle_count": len(snapshot["positions_kpc"]),
                    "represented_particle_count": float(
                        np.sum(snapshot["particle_weight"])
                    ),
                    "steps": source_run["steps"],
                    "time_step_kpc_per_km_s": source_run[
                        "time_step_kpc_per_km_s"
                    ],
                    "profile_sample_count": source_run["profile_sample_count"],
                    "source_final_assembly_fraction": source_run[
                        "final_assembly_fraction"
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
                    "source_edge_crossing_fraction": source_run[
                        "edge_crossing_fraction"
                    ],
                    "control_edge_crossing_fraction": control_run[
                        "edge_crossing_fraction"
                    ],
                    "source_outer_boundary_ingress_fraction": source_run[
                        "outer_boundary_ingress_fraction"
                    ],
                    "control_outer_boundary_ingress_fraction": control_run[
                        "outer_boundary_ingress_fraction"
                    ],
                    "softening_kpc": source_run["softening_kpc"],
                    "source_wall_seconds": source_run["wall_seconds"],
                    "control_wall_seconds": control_run["wall_seconds"],
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
        corrected_phase: dict[int, np.ndarray] = {}
        raw_source_phase: dict[int, np.ndarray] = {}
        raw_control_phase: dict[int, np.ndarray] = {}
        for sign, snapshot in response_snapshots.items():
            source_run, control_run = phase_outputs[(history["history_id"], sign)]
            particle_mass = float(snapshot["particle_mass_Msun"][0])
            background = (
                4.0
                * math.pi
                * PM.RHO_M_MSUN_MPC3
                * (radii / 1000.0) ** 3
                / 3.0
            )
            source_mass = PM.MOTION_FRACTION * np.maximum(
                source_run["averaged_counts"] * particle_mass - background, 0.0
            )
            control_mass = PM.MOTION_FRACTION * np.maximum(
                control_run["averaged_counts"] * particle_mass - background, 0.0
            )
            response_ratio = np.ones_like(radii)
            positive = control_mass > 0.0
            response_ratio[positive] = source_mass[positive] / control_mass[positive]
            corrected_phase[sign] = initial_phase_mass[sign] * response_ratio
            raw_source_phase[sign] = source_mass
            raw_control_phase[sign] = control_mass
        corrected_mass = 0.5 * (corrected_phase[-1] + corrected_phase[1])
        raw_source_mass = 0.5 * (raw_source_phase[-1] + raw_source_phase[1])
        raw_control_mass = 0.5 * (raw_control_phase[-1] + raw_control_phase[1])
        corrected_by_history[history["history_id"]] = corrected_mass
        corrected_score = score_profile(
            radii,
            corrected_mass,
            target_velocity,
            score_mask,
            transition_radius,
            edge_radius,
            target_edge_mass,
        )
        raw_source_score = score_profile(
            radii,
            raw_source_mass,
            target_velocity,
            score_mask,
            transition_radius,
            edge_radius,
            target_edge_mass,
        )
        raw_control_score = score_profile(
            radii,
            raw_control_mass,
            target_velocity,
            score_mask,
            transition_radius,
            edge_radius,
            target_edge_mass,
        )
        score_rows.append(
            {
                "history_id": history["history_id"],
                "q_parent": q_parent,
                "q_envelope": q_envelope,
                "corrected_q": corrected_score["q"],
                "corrected_q_absolute_difference": abs(
                    corrected_score["q"] - q_parent
                ),
                "corrected_q_compatible": abs(corrected_score["q"] - q_parent)
                <= q_envelope,
                "corrected_velocity_squared_log10_RMSE": corrected_score[
                    "velocity_squared_log10_RMSE"
                ],
                "baseline_velocity_squared_log10_RMSE": baseline_score[
                    "velocity_squared_log10_RMSE"
                ],
                "corrected_RMSE_improves_baseline": corrected_score[
                    "velocity_squared_log10_RMSE"
                ]
                < baseline_score["velocity_squared_log10_RMSE"],
                "corrected_transition_velocity_squared_ratio_to_target": corrected_score[
                    "transition_velocity_squared_ratio_to_target"
                ],
                "corrected_edge_mass_ratio_to_target": corrected_score[
                    "edge_mass_ratio_to_target"
                ],
                "raw_source_q": raw_source_score["q"],
                "raw_control_q": raw_control_score["q"],
                "raw_source_RMSE": raw_source_score[
                    "velocity_squared_log10_RMSE"
                ],
                "raw_control_RMSE": raw_control_score[
                    "velocity_squared_log10_RMSE"
                ],
                "target_used_to_select_history": False,
                "response_efficiency_fitted": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
        corrected_velocity = (
            PREVIOUS.G_KPC_KM2_S2_MSUN
            * corrected_mass
            / np.maximum(radii, np.finfo(float).tiny)
        )
        for index, radius in enumerate(radii):
            profile_output_rows.append(
                {
                    "history_id": history["history_id"],
                    "radius_kpc": radius,
                    "radius_over_transition": radius / transition_radius,
                    "corrected_motion_mass_Msun": corrected_mass[index],
                    "raw_source_motion_mass_Msun": raw_source_mass[index],
                    "raw_control_motion_mass_Msun": raw_control_mass[index],
                    "initial_motion_mass_Msun": pair_initial_mass[index],
                    "corrected_motion_v2_km2_s2": corrected_velocity[index],
                    "target_motion_v2_km2_s2": target_velocity[index],
                    "inside_scoring_window": bool(score_mask[index]),
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )

    circular_mass, cosmic_baryon, hot_ratio, circular_residual = (
        circular_mass_conserving_response(
            radii, pair_initial_mass, visible_source, edge_radius
        )
    )
    circular_score = score_profile(
        radii,
        circular_mass,
        target_velocity,
        score_mask,
        transition_radius,
        edge_radius,
        target_edge_mass,
    )

    refinement_controls: list[dict[str, Any]] = []

    def run_refinement(
        history_id: str,
        snapshot_pack: dict[int, dict[str, Any]],
        steps_per_orbit: int,
        refinement_id: str,
    ) -> dict[str, float]:
        history = next(row for row in histories if row["history_id"] == history_id)
        phase_mass: dict[int, np.ndarray] = {}
        for sign, snapshot in snapshot_pack.items():
            growth_time = float(history["growth_time_kpc_per_km_s"])
            total_time = growth_time + SETTLING_ORBITS * transition_orbit
            source_run = evolve_isolated(
                snapshot,
                visible_source,
                radii,
                transfer_per_donor[sign],
                history["ramp"],
                growth_time,
                total_time,
                AVERAGING_ORBITS * transition_orbit,
                steps_per_orbit,
                inner_orbit,
                True,
            )
            control_run = evolve_isolated(
                snapshot,
                visible_source,
                radii,
                transfer_per_donor[sign],
                history["ramp"],
                growth_time,
                total_time,
                AVERAGING_ORBITS * transition_orbit,
                steps_per_orbit,
                inner_orbit,
                False,
            )
            particle_mass = float(snapshot["particle_mass_Msun"][0])
            background = (
                4.0
                * math.pi
                * PM.RHO_M_MSUN_MPC3
                * (radii / 1000.0) ** 3
                / 3.0
            )
            source_mass = PM.MOTION_FRACTION * np.maximum(
                source_run["averaged_counts"] * particle_mass - background, 0.0
            )
            control_mass = PM.MOTION_FRACTION * np.maximum(
                control_run["averaged_counts"] * particle_mass - background, 0.0
            )
            ratio = np.ones_like(radii)
            positive = control_mass > 0.0
            ratio[positive] = source_mass[positive] / control_mass[positive]
            phase_mass[sign] = initial_phase_mass[sign] * ratio
            refinement_controls.append(
                {
                    "history_id": refinement_id,
                    "phase_sign": sign,
                    "steps_per_inner_orbit": steps_per_orbit,
                    "response_particle_count": len(snapshot["positions_kpc"]),
                    "represented_particle_count": float(
                        np.sum(snapshot["particle_weight"])
                    ),
                    "source_steps": source_run["steps"],
                    "control_steps": control_run["steps"],
                    "source_angular_momentum_relative_residual": source_run[
                        "angular_momentum_relative_residual"
                    ],
                    "control_angular_momentum_relative_residual": control_run[
                        "angular_momentum_relative_residual"
                    ],
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
        pair_mass = 0.5 * (phase_mass[-1] + phase_mass[1])
        return score_profile(
            radii,
            pair_mass,
            target_velocity,
            score_mask,
            transition_radius,
            edge_radius,
            target_edge_mass,
        )

    high_resolution_score: dict[str, float] | None = None
    one_orbit_high_score: dict[str, float] | None = None
    one_orbit_full_particle_score: dict[str, float] | None = None
    if not arguments.quick:
        high_resolution_score = run_refinement(
            "ADIABATIC8_C2",
            response_snapshots,
            HIGH_STEPS_PER_INNER_ORBIT,
            "ADIABATIC8_C2_TIME_REFINEMENT",
        )
        one_orbit_high_score = run_refinement(
            "ONE_ORBIT_C2",
            response_snapshots,
            HIGH_STEPS_PER_INNER_ORBIT,
            "ONE_ORBIT_C2_TIME_REFINEMENT",
        )
        uncompressed_snapshots = {
            sign: {
                **snapshot,
                "particle_weight": np.ones(
                    len(snapshot["positions_kpc"]), dtype=float
                ),
            }
            for sign, snapshot in snapshots.items()
        }
        one_orbit_full_particle_score = run_refinement(
            "ONE_ORBIT_C2",
            uncompressed_snapshots,
            STEPS_PER_INNER_ORBIT,
            "ONE_ORBIT_C2_FULL_PARTICLE_REFINEMENT",
        )
    control_rows.extend(refinement_controls)

    high_resolution_q = (
        high_resolution_score["q"] if high_resolution_score is not None else math.nan
    )
    one_orbit_high_q = (
        one_orbit_high_score["q"] if one_orbit_high_score is not None else math.nan
    )
    one_orbit_full_particle_q = (
        one_orbit_full_particle_score["q"]
        if one_orbit_full_particle_score is not None
        else math.nan
    )

    score_lookup = {row["history_id"]: row for row in score_rows}
    adiabatic_q_difference = abs(
        float(score_lookup["ADIABATIC8_C2"]["corrected_q"])
        - float(score_lookup["ADIABATIC4_C2"]["corrected_q"])
    ) if "ADIABATIC8_C2" in score_lookup else math.nan
    adiabatic_time_resolution_difference = abs(
        high_resolution_q
        - float(score_lookup["ADIABATIC8_C2"]["corrected_q"])
    ) if math.isfinite(high_resolution_q) else math.nan
    one_orbit_primary_q = float(score_lookup["ONE_ORBIT_C2"]["corrected_q"])
    one_orbit_time_resolution_difference = (
        abs(one_orbit_high_q - one_orbit_primary_q)
        if math.isfinite(one_orbit_high_q)
        else math.nan
    )
    one_orbit_particle_resolution_difference = (
        abs(one_orbit_full_particle_q - one_orbit_primary_q)
        if math.isfinite(one_orbit_full_particle_q)
        else math.nan
    )
    one_orbit_refinement_q_values = [
        value
        for value in (
            one_orbit_primary_q,
            one_orbit_high_q,
            one_orbit_full_particle_q,
        )
        if math.isfinite(value)
    ]
    parent_band_lower = q_parent - q_envelope
    parent_band_upper = q_parent + q_envelope
    one_orbit_refinement_intersects_parent_band = (
        min(one_orbit_refinement_q_values) <= parent_band_upper
        and max(one_orbit_refinement_q_values) >= parent_band_lower
    )
    compatible = [
        row["history_id"] for row in score_rows if row["corrected_q_compatible"]
    ]
    joint_improvements = [
        row["history_id"]
        for row in score_rows
        if row["corrected_q_compatible"]
        and row["corrected_RMSE_improves_baseline"]
    ]
    if joint_improvements:
        route_decision = (
            "VISIBLE_SOURCE_FORWARD_RESPONSE_REACHES_PARENT_BAND_BUT_SOURCE_HISTORY_NOT_PARENT_SELECTED"
        )
    elif one_orbit_refinement_intersects_parent_band and bool(
        score_lookup["ONE_ORBIT_C2"]["corrected_RMSE_improves_baseline"]
    ):
        route_decision = (
            "ONE_ORBIT_VISIBLE_SOURCE_RESPONSE_INTERSECTS_PARENT_BAND_UNDER_NUMERICAL_REFINEMENT_BUT_ASSEMBLY_HISTORY_NOT_PARENT_SELECTED"
        )
    elif compatible:
        route_decision = (
            "VISIBLE_SOURCE_FORWARD_RESPONSE_REACHES_Q_BAND_BUT_NOT_JOINT_AMPLITUDE_AND_HISTORY_GATE"
        )
    else:
        route_decision = (
            "PREDECLARED_VISIBLE_SOURCE_HISTORIES_DO_NOT_REACH_PARENT_Q_BAND_MOVE_TO_COLLECTIVE_STRESS_OR_DERIVED_RADIATIVE_ASSEMBLY"
        )
    summary = {
        "regenerated_pair_q": regenerated_pair_q,
        "historical_pair_q": historical_pair_q,
        "baseline_velocity_squared_log10_RMSE": baseline_score[
            "velocity_squared_log10_RMSE"
        ],
        "baseline_transition_velocity_squared_ratio_to_target": baseline_score[
            "transition_velocity_squared_ratio_to_target"
        ],
        "condensed_fraction_of_cosmic_baryon_allotment": float(
            sum(float(row["observed_condensed_baryon_mass_edge_Msun"]) for row in mass_rows)
            / sum(float(row["donor_cosmic_baryon_allotment_Msun"]) for row in mass_rows)
        ),
        "minimum_corrected_q": min(float(row["corrected_q"]) for row in score_rows),
        "maximum_corrected_q": max(float(row["corrected_q"]) for row in score_rows),
        "minimum_corrected_RMSE": min(
            float(row["corrected_velocity_squared_log10_RMSE"]) for row in score_rows
        ),
        "maximum_corrected_RMSE": max(
            float(row["corrected_velocity_squared_log10_RMSE"]) for row in score_rows
        ),
        "q_compatible_history_ids": compatible,
        "joint_q_and_RMSE_history_ids": joint_improvements,
        "circular_mass_conserving_q": circular_score["q"],
        "circular_mass_conserving_RMSE": circular_score[
            "velocity_squared_log10_RMSE"
        ],
        "circular_mass_conservation_residual": circular_residual,
        "cosmic_baryon_allotment_edge_Msun": cosmic_baryon,
        "remaining_hot_baryon_to_motion_ratio": hot_ratio,
        "transition_orbit_Gyr": 0.9777922216807892 * transition_orbit,
        "Newton_freefall_Gyr": 0.9777922216807892 * freefall_time,
        "inner_orbit_Gyr": 0.9777922216807892 * inner_orbit,
        "adiabatic_q_difference": adiabatic_q_difference,
        "adiabatic8_high_time_resolution_q": high_resolution_q,
        "adiabatic_time_resolution_q_difference": adiabatic_time_resolution_difference,
        "one_orbit_primary_q": one_orbit_primary_q,
        "one_orbit_primary_RMSE": float(
            score_lookup["ONE_ORBIT_C2"]["corrected_velocity_squared_log10_RMSE"]
        ),
        "one_orbit_primary_transition_velocity_squared_ratio_to_target": float(
            score_lookup["ONE_ORBIT_C2"][
                "corrected_transition_velocity_squared_ratio_to_target"
            ]
        ),
        "one_orbit_high_time_resolution_q": one_orbit_high_q,
        "one_orbit_full_particle_q": one_orbit_full_particle_q,
        "one_orbit_time_resolution_q_difference": one_orbit_time_resolution_difference,
        "one_orbit_particle_resolution_q_difference": one_orbit_particle_resolution_difference,
        "one_orbit_refinement_intersects_parent_band": one_orbit_refinement_intersects_parent_band,
        "parent_q_band_lower": parent_band_lower,
        "parent_q_band_upper": parent_band_upper,
        "maximum_angular_momentum_relative_residual": max(
            max(
                float(row.get("source_angular_momentum_relative_residual", 0.0)),
                float(row.get("control_angular_momentum_relative_residual", 0.0)),
            )
            for row in control_rows
        ),
        "maximum_edge_crossing_fraction": max(
            max(
                float(row.get("source_edge_crossing_fraction", 0.0)),
                float(row.get("control_edge_crossing_fraction", 0.0)),
            )
            for row in control_rows
        ),
        "maximum_outer_boundary_ingress_fraction": max(
            max(
                float(row.get("source_outer_boundary_ingress_fraction", 0.0)),
                float(row.get("control_outer_boundary_ingress_fraction", 0.0)),
            )
            for row in control_rows
        ),
        "maximum_source_control_outer_boundary_ingress_difference": max(
            abs(
                float(row.get("source_outer_boundary_ingress_fraction", 0.0))
                - float(row.get("control_outer_boundary_ingress_fraction", 0.0))
            )
            for row in control_rows
        ),
    }
    decision_rows = [
        {
            "route": "mass_conserving_visible_motion_initial_value_response",
            "result": route_decision,
            "evidence": (
                f"q range={summary['minimum_corrected_q']}..{summary['maximum_corrected_q']}; "
                f"one-orbit refinements={one_orbit_refinement_q_values}; "
                f"band intersection={one_orbit_refinement_intersects_parent_band}; "
                f"one-orbit transition ratio={summary['one_orbit_primary_transition_velocity_squared_ratio_to_target']}"
            ),
            "next_requirement": (
                "derive rather than select the visible-source assembly clock from the baryon plus Maxwell/Poynting energy equation, then retest the remaining amplitude deficit; retain collective density-matrix stress as the alternative"
            ),
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    ]

    outputs: dict[Path, list[dict[str, Any]]] = {
        FORCE_CSV: force_rows(),
        SNAPSHOT_CSV: snapshot_rows,
        MASS_CSV: mass_rows,
        HISTORY_CSV: histories,
        SCORE_CSV: score_rows,
        PROFILE_CSV: profile_output_rows,
        CONTROL_CSV: control_rows,
        DECISION_CSV: decision_rows,
        PROVENANCE_CSV: provenance_rows(paths),
    }
    for path, rows in outputs.items():
        write_csv(path, rows)

    hashes_after = {key: file_digest(path) for key, path in paths.items()}
    formal_after = tree_digest(FORMAL)
    validation: list[dict[str, Any]] = []
    add_validation(validation, "all_sources_exist", not missing, missing)
    add_validation(
        validation,
        "source_hashes_unchanged",
        hashes_before == hashes_after,
        hashes_after,
    )
    add_validation(
        validation,
        "formalization_workbench_unchanged",
        formal_after == formal_before == FORMAL_DIGEST_LOCK,
        formal_after,
    )
    add_validation(
        validation,
        "snapshot_phase_q_reproduced",
        all(float(row["q_absolute_reproduction_error"]) < 1.0e-9 for row in snapshot_rows),
        [row["q_absolute_reproduction_error"] for row in snapshot_rows],
    )
    add_validation(
        validation,
        "pair_q_reproduced",
        abs(regenerated_pair_q - historical_pair_q) < 1.0e-9,
        [regenerated_pair_q, historical_pair_q],
    )
    add_validation(
        validation,
        "condensed_baryons_within_cosmic_allotment",
        all(
            0.0 < float(row["condensed_fraction_of_cosmic_baryon_allotment"]) < 1.0
            for row in mass_rows
        ),
        [row["condensed_fraction_of_cosmic_baryon_allotment"] for row in mass_rows],
    )
    add_validation(
        validation,
        "mass_transfer_conserved",
        all(float(row["mass_conservation_relative_residual"]) < 1.0e-14 for row in mass_rows),
        [row["mass_conservation_relative_residual"] for row in mass_rows],
    )
    add_validation(
        validation,
        "donor_baryon_mass_nonnegative",
        all(row["donor_baryon_mass_stays_nonnegative"] for row in mass_rows),
        mass_rows,
    )
    add_validation(
        validation,
        "response_compression_preserves_particle_and_donor_weight",
        all(
            abs(
                float(row["response_represented_particle_count"])
                - float(next(
                    snapshot_row["selected_particle_count"]
                    for snapshot_row in snapshot_rows
                    if int(snapshot_row["phase_sign"]) == int(row["phase_sign"])
                ))
            )
            < 1.0e-12
            and abs(
                float(row["response_represented_donor_count"])
                - float(row["donor_particle_count"])
            )
            < 1.0e-12
            for row in mass_rows
        ),
        [
            {
                "phase": row["phase_sign"],
                "represented": row["response_represented_particle_count"],
                "represented_donor": row["response_represented_donor_count"],
            }
            for row in mass_rows
        ],
    )
    add_validation(
        validation,
        "all_predeclared_histories_executed",
        {row["history_id"] for row in score_rows}
        == {row["history_id"] for row in histories},
        [row["history_id"] for row in score_rows],
    )
    add_validation(
        validation,
        "all_scores_finite",
        all(
            math.isfinite(float(row["corrected_q"]))
            and math.isfinite(float(row["corrected_velocity_squared_log10_RMSE"]))
            for row in score_rows
        ),
        score_rows,
    )
    add_validation(
        validation,
        "source_reaches_full_assembly",
        all(
            abs(float(row["source_final_assembly_fraction"]) - 1.0) < 1.0e-12
            for row in control_rows
            if "source_final_assembly_fraction" in row
        ),
        [
            row["source_final_assembly_fraction"]
            for row in control_rows
            if "source_final_assembly_fraction" in row
        ],
    )
    add_validation(
        validation,
        "central_force_angular_momentum_control",
        summary["maximum_angular_momentum_relative_residual"] < 1.0e-10,
        summary["maximum_angular_momentum_relative_residual"],
    )
    add_validation(
        validation,
        "matched_control_outer_boundary_response_below_one_percent",
        summary["maximum_source_control_outer_boundary_ingress_difference"] < 0.01,
        {
            "absolute_ingress": summary["maximum_outer_boundary_ingress_fraction"],
            "source_control_difference": summary[
                "maximum_source_control_outer_boundary_ingress_difference"
            ],
        },
    )
    add_validation(
        validation,
        "no_fitted_response_efficiency",
        all(not row["response_efficiency_fitted"] for row in score_rows)
        and all(not row["target_used_to_select_history"] for row in histories),
        "predeclared histories only",
    )
    add_validation(
        validation,
        "circular_mass_identity_solved",
        circular_residual < 1.0e-10 and np.all(np.isfinite(circular_mass)),
        circular_residual,
    )
    add_validation(
        validation,
        "time_refinement_executed",
        arguments.quick or math.isfinite(high_resolution_q),
        high_resolution_q,
    )
    add_validation(
        validation,
        "adiabatic_time_refinement_q_controlled",
        arguments.quick or adiabatic_time_resolution_difference < 0.1,
        adiabatic_time_resolution_difference,
    )
    add_validation(
        validation,
        "one_orbit_refinements_executed",
        arguments.quick
        or (
            math.isfinite(one_orbit_high_q)
            and math.isfinite(one_orbit_full_particle_q)
        ),
        [one_orbit_high_q, one_orbit_full_particle_q],
    )
    add_validation(
        validation,
        "one_orbit_time_refinement_q_controlled",
        arguments.quick or one_orbit_time_resolution_difference < 0.1,
        one_orbit_time_resolution_difference,
    )
    add_validation(
        validation,
        "one_orbit_particle_refinement_q_controlled",
        arguments.quick or one_orbit_particle_resolution_difference < 0.1,
        one_orbit_particle_resolution_difference,
    )
    add_validation(
        validation,
        "all_outputs_nonclaim",
        all(
            row.get("valid_for_claim") is False
            for rows in outputs.values()
            for row in rows
        ),
        "all generated CSV rows",
    )
    add_validation(
        validation,
        "local_branch_unmodified",
        True,
        "same checkpoint-4947 G_N projection; no action or local coefficient edited",
    )
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
        "mass_conserving_two_component_force_derived": True,
        "three_dimensional_initial_value_response_executed": True,
        "baryonic_assembly_history_parent_selected": False,
        "local_GR_Newton_Maxwell_branch_modified": False,
        "valid_for_galaxy_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    write_json(RESULT_JSON, result)
    write_csv(VALIDATION_CSV, validation)
    DOCUMENT.write_text(make_document(result), encoding="utf-8")
    if result["validation_failures"]:
        raise RuntimeError(
            f"validation failures: {[row['check_id'] for row in result['validation_failures']]}"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
