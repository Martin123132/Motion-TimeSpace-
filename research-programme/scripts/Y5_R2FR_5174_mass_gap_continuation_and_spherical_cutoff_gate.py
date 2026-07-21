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


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
BASELINE_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5173_matched_CDM_formation_baseline_gate.py"
)
BASELINE_DOCUMENT = (
    POST / "5173-Y5-R2FR-matched-CDM-formation-baseline-discrimination-gate.md"
)
BASELINE_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5173"
    / "matched_CDM_formation_baseline_results.json"
)
BASELINE_VALIDATION = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5173_VALIDATION.csv"
)
TRANSFER_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5156_FLRW_covariance_radiation_transfer_and_patch_collapse_gate.py"
)
TRANSFER_DOCUMENT = (
    POST
    / "5156-Y5-R2FR-FLRW-Hessian-Gaussian-state-single-clock-adiabatic-radiation-transfer-and-patch-collapse-gate.md"
)
TRANSFER_CURVES = (
    POST / "source-intake" / "functional_rg" / "5156" / "radiation_era_FDM_transfer_curves.csv"
)
TRANSFER_SUMMARY = (
    POST / "source-intake" / "functional_rg" / "5156" / "radiation_transfer_summary.csv"
)
OUT = POST / "source-intake" / "functional_rg" / "5174"
RUNS = OUT / "runs"
CONTRACT_CSV = OUT / "mass_gap_continuation_contract.csv"
SPECTRAL_CSV = OUT / "resolved_spectral_scale_hierarchy.csv"
RUN_CSV = OUT / "mass_gap_continuation_forward_scores.csv"
PHASE_CSV = OUT / "mass_gap_continuation_phase_diagnostics.csv"
PROFILE_CSV = OUT / "mass_gap_continuation_forward_profiles.csv"
BOUND_CSV = OUT / "conditional_mass_gap_bound.csv"
CUTOFF_CSV = OUT / "spherical_cutoff_discrimination_control.csv"
DECISION_CSV = OUT / "route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "mass_gap_continuation_and_cutoff_results.json"
VALIDATION_CSV = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5174_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5174-Y5-R2FR-mass-gap-continuation-and-spherical-cutoff-discrimination-gate.md"
)

MARKER = "MTS_5174_MASS_GAP_CONTINUATION_AND_SPHERICAL_CUTOFF_GATE"
CHECKED_DATE = "2026-07-21"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
REFERENCE_MASS_EV = 1.0e-20
REFERENCE_MASS_LABEL = "benchmark_1e_minus20_eV"
LOCKED_FLOOR_LABEL = "ten_times_WKB_floor"
LOCKED_HIGH_LABEL = "benchmark_1e_minus18_eV"
REFERENCE_GALAXY = "UGC09133"
REFERENCE_MAPPING = "Wetterich_v_equals_minus_2lambda"
SELECTED_BRANCH = ("ISOBARIC", 0.3)
SELECTED_RUN_ID = "ISOBARIC_Z0.3_RADIAL_COOLING_FREEFALL_OT_N26_P1_FULL_PRIMARY"
STEPS_PER_INNER_ORBIT = 64
RADIAL_BINS = 26
COST_POWER = 1
ALGORITHM_VERSION = "mass_gap_continuation_v1"
HU_SOURCE = "https://arxiv.org/abs/astro-ph/0003365"


specification = importlib.util.spec_from_file_location(
    "mts_checkpoint_5173_for_5174", BASELINE_SCRIPT
)
if specification is None or specification.loader is None:
    raise RuntimeError(f"cannot load module: {BASELINE_SCRIPT}")
B = importlib.util.module_from_spec(specification)
specification.loader.exec_module(B)
Q = B.Q
R = B.R
V = B.V
DYNAMICS = B.DYNAMICS
ZOOM = B.ZOOM
PM = B.PM


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_paths() -> dict[str, Path]:
    return {
        "checkpoint_5173_script": BASELINE_SCRIPT,
        "checkpoint_5173_document": BASELINE_DOCUMENT,
        "checkpoint_5173_result": BASELINE_RESULT,
        "checkpoint_5173_validation": BASELINE_VALIDATION,
        "checkpoint_5156_script": TRANSFER_SCRIPT,
        "checkpoint_5156_document": TRANSFER_DOCUMENT,
        "radiation_transfer_curves": TRANSFER_CURVES,
        "radiation_transfer_summary": TRANSFER_SUMMARY,
        "checkpoint_5169_result": B.PREVIOUS_RESULT,
        "checkpoint_5169_score": B.PREVIOUS_SCORE,
        "checkpoint_5169_profile": B.PREVIOUS_PROFILE,
        "checkpoint_5174_script": Path(__file__).resolve(),
    }


def file_digest(path: Path) -> str:
    return Q.file_digest(path)


def array_digest(*arrays: np.ndarray) -> str:
    digest = hashlib.sha256()
    for array in arrays:
        contiguous = np.ascontiguousarray(array, dtype=np.float64)
        digest.update(str(contiguous.shape).encode("ascii"))
        digest.update(contiguous.tobytes())
    return digest.hexdigest()


def transfer_inputs() -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
    dict[str, str],
    dict[str, dict[str, str]],
]:
    wavenumber, cdm_power, reference_power, patch = B.covariance_rows()
    summaries = {row["mass_label"]: row for row in read_csv(TRANSFER_SUMMARY)}
    return wavenumber, cdm_power, reference_power, patch, summaries


def mass_power(
    wavenumber: np.ndarray,
    cdm_power: np.ndarray,
    mass_eV: float,
    reference_k_jeans: float,
) -> tuple[np.ndarray, np.ndarray, float, float]:
    k_jeans = reference_k_jeans * math.sqrt(mass_eV / REFERENCE_MASS_EV)
    mass_22 = mass_eV / 1.0e-22
    argument = 1.61 * mass_22 ** (1.0 / 18.0) * wavenumber / k_jeans
    amplitude = np.cos(argument**3) / (1.0 + argument**8)
    transfer_power = amplitude**2
    power = np.maximum(cdm_power * transfer_power, cdm_power * 1.0e-30)
    half_power_formula = 4.5 * mass_22 ** (4.0 / 9.0)
    return power, transfer_power, k_jeans, half_power_formula


def cosine_spherical_cutoff(
    wavenumber: np.ndarray, power: np.ndarray, cutoff: float
) -> tuple[np.ndarray, np.ndarray]:
    lower = 0.9 * cutoff
    window = np.ones_like(wavenumber)
    transition = (wavenumber > lower) & (wavenumber < cutoff)
    window[transition] = 0.5 * (
        1.0
        + np.cos(math.pi * (wavenumber[transition] - lower) / (cutoff - lower))
    )
    window[wavenumber >= cutoff] = 1.0e-30
    return np.maximum(power * window, power * 1.0e-30), window


def full_sigma(
    wavenumber: np.ndarray, power: np.ndarray, patch_radius: float
) -> float:
    variance, _ = PM.point_top_hat_covariance(
        wavenumber, power, patch_radius, np.asarray([0.0])
    )
    return math.sqrt(variance)


def fixed_families(axis_nyquist: float) -> list[dict[str, Any]]:
    return [
        {
            "family_id": "MTS_WKB_FLOOR_FULL",
            "mass_eV": 2.8166916621557602e-21,
            "mass_role": "locked_checkpoint_5156",
            "cutoff_Mpc_inverse": None,
        },
        {
            "family_id": "MTS_3P162277660E_MINUS20_FULL",
            "mass_eV": math.sqrt(10.0) * 1.0e-20,
            "mass_role": "predeclared_log_mass_continuation",
            "cutoff_Mpc_inverse": None,
        },
        {
            "family_id": "MTS_1E_MINUS19_FULL",
            "mass_eV": 1.0e-19,
            "mass_role": "predeclared_log_mass_continuation",
            "cutoff_Mpc_inverse": None,
        },
        {
            "family_id": "MTS_1E_MINUS18_FULL",
            "mass_eV": 1.0e-18,
            "mass_role": "locked_checkpoint_5156",
            "cutoff_Mpc_inverse": None,
        },
        {
            "family_id": "MTS_1E_MINUS20_SPHERICAL_NYQUIST",
            "mass_eV": 1.0e-20,
            "mass_role": "shared_resolution_control",
            "cutoff_Mpc_inverse": axis_nyquist,
        },
        {
            "family_id": "CDM_SPHERICAL_NYQUIST",
            "mass_eV": None,
            "mass_role": "shared_resolution_control",
            "cutoff_Mpc_inverse": axis_nyquist,
        },
    ]


def spectrum_for_family(
    family: dict[str, Any],
    wavenumber: np.ndarray,
    cdm_power: np.ndarray,
    reference_k_jeans: float,
) -> dict[str, Any]:
    mass_eV = family["mass_eV"]
    if mass_eV is None:
        power = cdm_power.copy()
        transfer_power = np.ones_like(power)
        k_jeans = math.inf
        half_power = math.inf
    else:
        power, transfer_power, k_jeans, half_power = mass_power(
            wavenumber, cdm_power, float(mass_eV), reference_k_jeans
        )
    cutoff = family["cutoff_Mpc_inverse"]
    cutoff_window = np.ones_like(power)
    if cutoff is not None:
        power, cutoff_window = cosine_spherical_cutoff(
            wavenumber, power, float(cutoff)
        )
    return {
        **family,
        "power": power,
        "transfer_power": transfer_power,
        "cutoff_window": cutoff_window,
        "k_Jeans_equality_Mpc_inverse": k_jeans,
        "half_power_k_Mpc_inverse": half_power,
        "spectrum_sha256": array_digest(wavenumber, power),
    }


def run_paths(family_id: str) -> dict[str, Any]:
    run_dir = RUNS / family_id
    return {
        "dir": run_dir,
        "snapshots": {
            -1: run_dir / "phase_minus_isolated_initial_state.npz",
            1: run_dir / "phase_plus_isolated_initial_state.npz",
        },
        "metadata": run_dir / "isolated_initial_state_metadata.json",
        "cache": run_dir / "evolution-cache",
    }


def generate_snapshots(
    spectrum: dict[str, Any],
    wavenumber: np.ndarray,
    patch_radius: float,
    base_context: dict[str, Any],
    force: bool,
) -> tuple[dict[int, dict[str, Any]], dict[str, Any]]:
    paths = run_paths(spectrum["family_id"])
    target_constraint = full_sigma(wavenumber, spectrum["power"], patch_radius)
    signature = hashlib.sha256(
        json.dumps(
            {
                "algorithm": ALGORITHM_VERSION,
                "family_id": spectrum["family_id"],
                "spectrum_sha256": spectrum["spectrum_sha256"],
                "target_constraint": target_constraint,
                "coarse_grid": ZOOM.PREVIOUS.COARSE_PARTICLES,
                "particle_grid": ZOOM.PARTICLE_GRID,
                "local_grid": DYNAMICS.LOCAL_GRID,
                "fixed_seed": PM.FIXED_SEED,
            },
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()
    if (
        not force
        and paths["metadata"].is_file()
        and all(path.is_file() for path in paths["snapshots"].values())
    ):
        metadata = json.loads(paths["metadata"].read_text(encoding="utf-8"))
        if metadata.get("cache_signature") == signature:
            snapshots: dict[int, dict[str, Any]] = {}
            for phase_sign, path in paths["snapshots"].items():
                with np.load(path) as archive:
                    snapshots[phase_sign] = {
                        key: archive[key] for key in archive.files
                    }
            return snapshots, metadata
    targets, _, _, _ = ZOOM.PREVIOUS.target_lookup()
    target = targets[REFERENCE_MAPPING]
    edge_radius_Mpc = float(target["edge_radius_Mpc"])
    box_size_Mpc = PM.BOX_OVER_PATCH * patch_radius
    coarse_fields, conditioning = PM.build_conditioned_pair(
        ZOOM.PREVIOUS.COARSE_PARTICLES,
        box_size_Mpc,
        patch_radius,
        target_constraint,
        wavenumber,
        spectrum["power"],
    )
    fields = {
        phase_sign: ZOOM.PREVIOUS.periodic_fourier_resample(
            coarse_fields[phase_sign], ZOOM.PARTICLE_GRID
        )
        for phase_sign in ZOOM.PAIR_SIGNS
    }
    _, states = ZOOM.PREVIOUS.initial_rows_and_states(
        {ZOOM.PARTICLE_GRID: fields}, box_size_Mpc, patch_radius
    )
    lagrangian_positions = PM.particle_lattice(
        ZOOM.PARTICLE_GRID, box_size_Mpc
    )
    metadata: dict[str, Any] = {
        "cache_signature": signature,
        "checkpoint_marker": MARKER,
        "algorithm_version": ALGORITHM_VERSION,
        "family_id": spectrum["family_id"],
        "mass_eV": spectrum["mass_eV"],
        "mass_role": spectrum["mass_role"],
        "cutoff_Mpc_inverse": spectrum["cutoff_Mpc_inverse"],
        "spectrum_sha256": spectrum["spectrum_sha256"],
        "target_constraint": target_constraint,
        "conditioning": conditioning,
        "box_size_Mpc": box_size_Mpc,
        "patch_radius_Mpc": patch_radius,
        "edge_radius_kpc": 1000.0 * edge_radius_Mpc,
        "fixed_seed": PM.FIXED_SEED,
        "phases": {},
    }
    snapshots: dict[int, dict[str, Any]] = {}
    paths["dir"].mkdir(parents=True, exist_ok=True)
    for phase_sign in ZOOM.PAIR_SIGNS:
        print(
            f"START {spectrum['family_id']} nested phase={phase_sign:+d}",
            flush=True,
        )
        start = time.perf_counter()
        initial = states[(ZOOM.PARTICLE_GRID, phase_sign)]
        evolved = ZOOM.evolve_nested(
            np.asarray(initial["positions"], dtype=float),
            np.asarray(initial["momenta"], dtype=float),
            lagrangian_positions,
            np.asarray(initial["tagged"], dtype=bool),
            ZOOM.PARTICLE_GRID,
            DYNAMICS.LOCAL_GRID,
            box_size_Mpc,
            edge_radius_Mpc,
        )
        profile = ZOOM.zoom_profile(
            np.asarray(evolved["positions"], dtype=float),
            np.asarray(initial["tagged"], dtype=bool),
            ZOOM.PARTICLE_GRID,
            DYNAMICS.LOCAL_GRID,
            box_size_Mpc,
            edge_radius_Mpc,
        )
        center = np.asarray(profile["center_Mpc"], dtype=float)
        offsets_Mpc = ZOOM.periodic_offset(
            np.asarray(evolved["positions"], dtype=float), center, box_size_Mpc
        )
        all_radii_Mpc = np.linalg.norm(offsets_Mpc, axis=1)
        donor_all = all_radii_Mpc <= edge_radius_Mpc
        center_momentum = np.mean(
            np.asarray(evolved["momenta"], dtype=float)[donor_all], axis=0
        )
        velocities_km_s = PM.H0_KM_S_MPC * (
            np.asarray(evolved["momenta"], dtype=float)
            - center_momentum[None, :]
            + offsets_Mpc
        )
        selected = (
            all_radii_Mpc
            <= DYNAMICS.ISOLATION_EDGE_MULTIPLE * edge_radius_Mpc
        )
        positions_kpc = 1000.0 * offsets_Mpc[selected]
        selected_velocities = velocities_km_s[selected]
        donors = donor_all[selected]
        initial_radius_kpc = 1000.0 * all_radii_Mpc[selected]
        particle_mass = float(profile["particle_mass_Msun"])
        _, motion_mass = DYNAMICS.snapshot_profile(
            positions_kpc, base_context["radii"], particle_mass
        )
        velocity_squared = (
            DYNAMICS.PREVIOUS.G_KPC_KM2_S2_MSUN
            * motion_mass
            / np.maximum(base_context["radii"], np.finfo(float).tiny)
        )
        q_value = DYNAMICS.PREVIOUS.local_logarithmic_q(
            base_context["radii"],
            velocity_squared,
            base_context["transition_radius"],
        )
        snapshot = {
            "positions_kpc": positions_kpc,
            "velocities_km_s": selected_velocities,
            "donor": donors,
            "initial_radius_kpc": initial_radius_kpc,
            "particle_mass_Msun": np.asarray([particle_mass]),
            "edge_radius_kpc": np.asarray([1000.0 * edge_radius_Mpc]),
            "resolved_radius_kpc": np.asarray(
                [1000.0 * float(profile["resolved_radius_Mpc"])]
            ),
            "local_force_cell_kpc": np.asarray(
                [
                    1000.0
                    * DYNAMICS.LOCAL_GRID ** -1
                    * ZOOM.LOCAL_BOX_EDGE_MULTIPLE
                    * edge_radius_Mpc
                ]
            ),
        }
        snapshots[phase_sign] = snapshot
        np.savez_compressed(paths["snapshots"][phase_sign], **snapshot)
        phase_metadata = {
            "phase_sign": phase_sign,
            "selected_particle_count": int(np.count_nonzero(selected)),
            "donor_particle_count": int(np.count_nonzero(donors)),
            "particle_mass_Msun": particle_mass,
            "preassembly_phase_q": q_value,
            "wall_seconds": time.perf_counter() - start,
            "snapshot_sha256": file_digest(paths["snapshots"][phase_sign]),
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        metadata["phases"][str(phase_sign)] = phase_metadata
        print(
            f"DONE {spectrum['family_id']} nested phase={phase_sign:+d} "
            f"q={q_value} wall={phase_metadata['wall_seconds']:.3f}s",
            flush=True,
        )
    Q.write_json(paths["metadata"], metadata)
    return snapshots, metadata


def evolution_signature(
    family_id: str,
    snapshot_path: Path,
    phase_sign: int,
    source_enabled: bool,
    endpoint_time: float,
) -> str:
    payload = {
        "algorithm": ALGORITHM_VERSION,
        "family_id": family_id,
        "snapshot_sha256": file_digest(snapshot_path),
        "phase_sign": phase_sign,
        "source_enabled": source_enabled,
        "endpoint_time": endpoint_time,
        "steps_per_inner_orbit": STEPS_PER_INNER_ORBIT,
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def run_or_load_evolution(
    family_id: str,
    snapshot: dict[str, Any],
    snapshot_path: Path,
    plan: dict[str, Any],
    context: dict[str, Any],
    phase_sign: int,
    source_enabled: bool,
    force: bool,
) -> dict[str, Any]:
    paths = run_paths(family_id)
    role = "SOURCE" if source_enabled else "CONTROL"
    stem = f"{role}_PHASE_{phase_sign:+d}".replace("+", "PLUS").replace("-", "MINUS")
    array_path = paths["cache"] / f"{stem}.npz"
    metadata_path = paths["cache"] / f"{stem}.json"
    signature = evolution_signature(
        family_id,
        snapshot_path,
        phase_sign,
        source_enabled,
        float(plan["endpoint_time_internal"]),
    )
    if not force and array_path.is_file() and metadata_path.is_file():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if metadata.get("cache_signature") == signature:
            with np.load(array_path) as archive:
                counts = np.asarray(archive["averaged_counts"], dtype=float)
            return {**metadata["diagnostics"], "averaged_counts": counts}
    print(
        f"START {family_id} {role} phase={phase_sign:+d}", flush=True
    )
    result = V.evolve(
        snapshot,
        plan,
        context["visible_source"],
        context["radii"],
        context["transition_orbit"],
        context["inner_orbit"],
        STEPS_PER_INNER_ORBIT,
        source_enabled,
    )
    paths["cache"].mkdir(parents=True, exist_ok=True)
    np.savez_compressed(array_path, averaged_counts=result["averaged_counts"])
    diagnostics = {
        key: value for key, value in result.items() if key != "averaged_counts"
    }
    Q.write_json(
        metadata_path,
        {"cache_signature": signature, "diagnostics": diagnostics},
    )
    print(
        f"DONE {family_id} {role} phase={phase_sign:+d} "
        f"wall={diagnostics['wall_seconds']:.3f}s",
        flush=True,
    )
    return result


def run_response(
    family_id: str,
    context: dict[str, Any],
    polynomial: dict[str, Any],
    solution: dict[str, Any],
    force: bool,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[int, np.ndarray]]:
    data = R.binned_inputs(context, solution, polynomial, RADIAL_BINS)
    transport = R.solve_transport(data, COST_POWER)
    phase_mass: dict[int, np.ndarray] = {}
    controls: list[dict[str, Any]] = []
    paths = run_paths(family_id)
    for phase_sign in (-1, 1):
        snapshot = context["snapshots"][phase_sign]
        plan = V.phase_plan(snapshot, solution, data, transport, phase_sign)
        control = run_or_load_evolution(
            family_id,
            snapshot,
            paths["snapshots"][phase_sign],
            plan,
            context,
            phase_sign,
            False,
            force,
        )
        source = run_or_load_evolution(
            family_id,
            snapshot,
            paths["snapshots"][phase_sign],
            plan,
            context,
            phase_sign,
            True,
            force,
        )
        particle_mass = float(snapshot["particle_mass_Msun"][0])
        background = (
            4.0
            * math.pi
            * PM.RHO_M_MSUN_MPC3
            * (context["radii"] / 1000.0) ** 3
            / 3.0
        )
        source_mass = PM.MOTION_FRACTION * np.maximum(
            source["averaged_counts"] * particle_mass - background, 0.0
        )
        control_mass = PM.MOTION_FRACTION * np.maximum(
            control["averaged_counts"] * particle_mass - background, 0.0
        )
        ratio = np.ones_like(context["radii"])
        positive = control_mass > 0.0
        ratio[positive] = source_mass[positive] / control_mass[positive]
        phase_mass[phase_sign] = context["initial_phase_mass"][phase_sign] * ratio
        controls.append(
            {
                "family_id": family_id,
                "phase_sign": phase_sign,
                "source_steps": source["steps"],
                "control_steps": control["steps"],
                "source_transfer_relative_residual": source[
                    "final_transfer_relative_residual"
                ],
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
                "capacity_representation_relative_residual": plan[
                    "capacity_representation_relative_residual"
                ],
                "source_wall_seconds": source["wall_seconds"],
                "control_wall_seconds": control["wall_seconds"],
                "target_used": False,
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
    return score, controls, phase_mass


def spectral_hierarchy_rows(
    wavenumber: np.ndarray,
    cdm_power: np.ndarray,
    reference_power: np.ndarray,
    box_size: float,
) -> tuple[list[dict[str, Any]], dict[str, float]]:
    coarse = int(ZOOM.PREVIOUS.COARSE_PARTICLES)
    kx, ky, kz, squared = PM.fourier_grid(coarse, box_size)
    magnitude = np.sqrt(squared)
    p_cdm_modes = PM.interpolate_power(magnitude, wavenumber, cdm_power)
    p_mts_modes = PM.interpolate_power(magnitude, wavenumber, reference_power)
    deficit = np.maximum(p_cdm_modes - p_mts_modes, 0.0)
    weights = np.full(kz.shape, 2.0)
    weights[0] = 1.0
    if coarse % 2 == 0:
        weights[-1] = 1.0
    mode_weights = np.broadcast_to(weights[None, None, :], magnitude.shape)
    nonzero = magnitude > 0.0
    density_weight = deficit * mode_weights
    displacement_weight = np.zeros_like(deficit)
    displacement_weight[nonzero] = (
        deficit[nonzero]
        * mode_weights[nonzero]
        / squared[nonzero]
    )
    axis_nyquist = math.pi * coarse / box_size
    corner_nyquist = math.sqrt(3.0) * axis_nyquist

    def quantile(scale_weight: np.ndarray, fraction: float) -> float:
        mask = nonzero & (scale_weight > 0.0)
        order = np.argsort(magnitude[mask])
        values = scale_weight[mask][order]
        cumulative = np.cumsum(values)
        index = int(np.searchsorted(cumulative, fraction * cumulative[-1]))
        return float(magnitude[mask][order[min(index, len(order) - 1)]])

    summary = {
        "box_fundamental_Mpc_inverse": 2.0 * math.pi / box_size,
        "coarse_axis_nyquist_Mpc_inverse": axis_nyquist,
        "coarse_corner_nyquist_Mpc_inverse": corner_nyquist,
        "density_deficit_k50_Mpc_inverse": quantile(density_weight, 0.5),
        "density_deficit_k90_Mpc_inverse": quantile(density_weight, 0.9),
        "displacement_deficit_k50_Mpc_inverse": quantile(displacement_weight, 0.5),
        "displacement_deficit_k90_Mpc_inverse": quantile(displacement_weight, 0.9),
        "density_deficit_fraction_above_axis_nyquist": float(
            np.sum(density_weight[magnitude > axis_nyquist])
            / np.sum(density_weight)
        ),
        "displacement_deficit_fraction_above_axis_nyquist": float(
            np.sum(displacement_weight[magnitude > axis_nyquist])
            / np.sum(displacement_weight)
        ),
    }
    edges = np.geomspace(
        summary["box_fundamental_Mpc_inverse"], corner_nyquist, 18
    )
    rows: list[dict[str, Any]] = []
    density_total = float(np.sum(density_weight))
    displacement_total = float(np.sum(displacement_weight))
    for index in range(len(edges) - 1):
        mask = (magnitude >= edges[index]) & (magnitude < edges[index + 1])
        rows.append(
            {
                "shell_index": index,
                "k_low_Mpc_inverse": float(edges[index]),
                "k_high_Mpc_inverse": float(edges[index + 1]),
                "mode_count_weighted": float(np.sum(mode_weights[mask])),
                "density_deficit_fraction": float(
                    np.sum(density_weight[mask]) / density_total
                ),
                "displacement_deficit_fraction": float(
                    np.sum(displacement_weight[mask]) / displacement_total
                ),
                "above_axis_nyquist": bool(edges[index] >= axis_nyquist),
                "target_used": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows, summary


def contract_rows() -> list[dict[str, Any]]:
    clauses = [
        (
            "C1_SINGLE_PARENT_TRANSFER",
            "all finite-mass spectra use the checkpoint-5156 Hu transfer on the same CAMB CDM baseline",
        ),
        (
            "C2_SHARED_PHASES",
            "all families use the same fixed Gaussian field, antithetic signs and one-sigma conditioning rule",
        ),
        (
            "C3_SHARED_DYNAMICS",
            "all families use the same nested force, calibrated G_N, visible source history and score",
        ),
        (
            "C4_PREDECLARED_MASS_LADDER",
            "locked masses plus sqrt(10) logarithmic continuation are evaluated before one geometric bound refinement",
        ),
        (
            "C5_SHARED_CUTOFF",
            "the MTS and CDM resolution controls use the identical spherical cosine cutoff at the coarse-axis Nyquist",
        ),
        (
            "C6_NO_TARGET_FEEDBACK",
            "the target does not enter any spectrum, constraint, force or source history; q_upper enters only the post-run bound bracket",
        ),
        (
            "C7_CONDITIONAL_BOUND",
            "any inferred mass bracket is one-patch empirical evidence and not a parent-derived mass or universal claim",
        ),
    ]
    return [
        {
            "clause_id": clause_id,
            "contract": contract,
            "status": "frozen_before_forward_evolution",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for clause_id, contract in clauses
    ]


def add_validation(
    rows: list[dict[str, Any]], check_id: str, passed: bool, evidence: Any
) -> None:
    rows.append(
        {
            "check_id": check_id,
            "passed": bool(passed),
            "evidence": json.dumps(evidence, sort_keys=True),
        }
    )


def document_text(result: dict[str, Any], run_rows: list[dict[str, Any]]) -> str:
    summary = result["summary"]
    ordered = sorted(
        [row for row in run_rows if row["cutoff_Mpc_inverse"] in (None, "")],
        key=lambda row: (
            math.inf if row["mass_eV"] in (None, "") else float(row["mass_eV"])
        ),
    )
    table_lines = []
    for row in ordered:
        mass = "infinity/CDM" if row["mass_eV"] in (None, "") else f"{float(row['mass_eV']):.9e}"
        table_lines.append(
            f"| `{row['family_id']}` | `{mass}` | `{float(row['half_power_k_Mpc_inverse']):.8g}` | "
            f"`{float(row['preassembly_q']):.9g}` | `{float(row['forward_q']):.9g}` | "
            f"`{float(row['forward_RMSE_dex']):.9g}` | `{row['q_compatible']}` |"
        )
    table = "\n".join(table_lines)
    bound = result["conditional_mass_bound"]
    cutoff = result["cutoff_control"]
    return f"""# 5174 - Mass-gap continuation and spherical-cutoff discrimination gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Question

Checkpoint 5173 found a matched CDM advantage over the empirical adiabatic
`m_gap=1e-20 eV` MTS/FDM comparator. This checkpoint asks two calculations
before changing the parent state law: is the response ordered along the
source-backed parent mass transfer, and does it survive removal of Fourier-cube
corner modes above the coarse-grid axis Nyquist?

## Derived continuation

The same checkpoint-5156 transfer is used without a new response coefficient,

```text
k_J,eq(m)=k_J,eq(m_ref) sqrt(m/m_ref),
x=1.61 m_22^(1/18) k/k_J,eq,
P_m(k)=P_CDM(k)[cos(x^3)/(1+x^8)]^2.
```

Every family uses its own covariance-derived one-sigma patch constraint, the
same fixed phases, nested force, calibrated `G_N`, visible history and scoring
operator. Only the spectrum changes. The target slope enters after evolution
solely to bracket a conditional empirical mass bound.

| family | m_gap (eV) | k_half (Mpc^-1) | preassembly q | forward q | RMSE (dex) | q band |
|---|---:|---:|---:|---:|---:|---:|
{table}

## Resolved-mode audit

The actual seed field is a `{summary['coarse_grid']}^3` Fourier cube resampled
onto `{summary['particle_grid']}^3` particles. Its axis Nyquist is
`{summary['coarse_axis_nyquist_Mpc_inverse']}` Mpc^-1 and its corner magnitude
is `{summary['coarse_corner_nyquist_Mpc_inverse']}` Mpc^-1. The CDM-minus-MTS
density-deficit median is `{summary['density_deficit_k50_Mpc_inverse']}`
Mpc^-1; the displacement-deficit median is
`{summary['displacement_deficit_k50_Mpc_inverse']}` Mpc^-1.

The shared spherical-cutoff control gives

```text
full Delta q (CDM-MTS)={cutoff['full_delta_q']},
cutoff Delta q={cutoff['cutoff_delta_q']},
retained absolute fraction={cutoff['retained_delta_q_fraction']},
q advantage survives={cutoff['q_advantage_survives']},
full Delta RMSE={cutoff['full_delta_RMSE_dex']},
cutoff Delta RMSE={cutoff['cutoff_delta_RMSE_dex']},
RMSE same sign={cutoff['RMSE_same_sign']},
checkpoint-5173 CDM advantage survives={cutoff['checkpoint_5173_CDM_advantage_survives']}.
```

## Conditional mass diagnostic

```text
status={bound['status']},
lower_mass_eV={bound['lower_mass_eV']},
upper_mass_eV={bound['upper_mass_eV']},
lower_q={bound['lower_q']},
upper_q={bound['upper_q']},
parent_q_upper={bound['parent_q_upper']}.
```

This is not a derived parent mass and not a universal galaxy limit. A numerical
crossing is a bound only if the continuation is monotone within the numerical
envelope. Otherwise it is retained solely as evidence of UV/realization
sensitivity. An isotropically resolved calculation, an ensemble and a parent
state-preparation law remain necessary.

## Decision

`{result['route_decision']}`.

All `{result['validation_count']}` generated validations pass. Every output is
nonclaim. The protected `formalization-workbench` digest remains
`{result['formalization_workbench_tree_sha256']}`. No GitHub action occurred.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force-snapshots", action="store_true")
    parser.add_argument("--force-response", action="store_true")
    arguments = parser.parse_args()
    paths = source_paths()
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing sources: {missing}")
    formal_before = Q.tree_digest(FORMAL)
    if formal_before != FORMAL_DIGEST_LOCK:
        raise RuntimeError(f"protected digest mismatch: {formal_before}")
    hashes_before = {key: file_digest(path) for key, path in paths.items()}
    wavenumber, cdm_power, reference_power, patch, summaries = transfer_inputs()
    base_context, polynomial, _, solutions = R.build_parent_state()
    selected_solution = solutions[SELECTED_BRANCH]
    targets, _, patch_radius, _ = ZOOM.PREVIOUS.target_lookup()
    target = targets[REFERENCE_MAPPING]
    box_size = PM.BOX_OVER_PATCH * patch_radius
    axis_nyquist = math.pi * ZOOM.PREVIOUS.COARSE_PARTICLES / box_size
    spectral_rows, spectral_summary = spectral_hierarchy_rows(
        wavenumber, cdm_power, reference_power, box_size
    )
    reference_k_jeans = float(
        summaries[REFERENCE_MASS_LABEL]["parent_kJeans_equality_Mpc_inverse"]
    )
    families = fixed_families(axis_nyquist)
    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "marker": MARKER,
                    "fixed_new_family_count": len(families),
                    "maximum_new_family_count": len(families) + 1,
                    "coarse_grid": ZOOM.PREVIOUS.COARSE_PARTICLES,
                    "particle_grid": ZOOM.PARTICLE_GRID,
                    "axis_nyquist_Mpc_inverse": axis_nyquist,
                    "corner_nyquist_Mpc_inverse": spectral_summary[
                        "coarse_corner_nyquist_Mpc_inverse"
                    ],
                    "families": families,
                    "single_adaptive_rule": "one geometric midpoint of the first q_upper mass bracket",
                    "formal_digest": formal_before,
                },
                indent=2,
            )
        )
        return

    baseline_result = json.loads(BASELINE_RESULT.read_text(encoding="utf-8"))
    previous_result = json.loads(B.PREVIOUS_RESULT.read_text(encoding="utf-8"))
    selected_mts_row = next(
        row
        for row in read_csv(B.PREVIOUS_SCORE)
        if row["run_id"] == SELECTED_RUN_ID
    )
    q_lower = float(previous_result["summary"]["parent_q_lower"])
    q_upper = float(previous_result["summary"]["parent_q_upper"])
    q_envelope = float(
        previous_result["summary"]["maximum_selected_control_delta_q"]
    )
    rmse_envelope = max(
        abs(
            float(row["corrected_velocity_squared_log10_RMSE"])
            - float(selected_mts_row["corrected_velocity_squared_log10_RMSE"])
        )
        for row in read_csv(B.PREVIOUS_SCORE)
        if row["thermal_mode"] == SELECTED_BRANCH[0]
        and float(row["metallicity_Zsun"]) == SELECTED_BRANCH[1]
    )

    run_rows: list[dict[str, Any]] = [
        {
            "family_id": "MTS_1E_MINUS20_FULL",
            "mass_eV": REFERENCE_MASS_EV,
            "mass_role": "existing_checkpoint_5169_endpoint",
            "cutoff_Mpc_inverse": None,
            "k_Jeans_equality_Mpc_inverse": reference_k_jeans,
            "half_power_k_Mpc_inverse": float(
                summaries[REFERENCE_MASS_LABEL][
                    "numeric_half_power_k_Mpc_inverse"
                ]
            ),
            "target_constraint": float(patch["sigma_MTS_empirical_adiabatic"]),
            "preassembly_q": float(base_context["baseline_score"]["q"]),
            "forward_q": float(selected_mts_row["corrected_q"]),
            "forward_RMSE_dex": float(
                selected_mts_row["corrected_velocity_squared_log10_RMSE"]
            ),
            "q_compatible": q_lower
            <= float(selected_mts_row["corrected_q"])
            <= q_upper,
            "target_used_to_define_evolution": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "family_id": "CDM_FULL",
            "mass_eV": None,
            "mass_role": "existing_checkpoint_5173_endpoint",
            "cutoff_Mpc_inverse": None,
            "k_Jeans_equality_Mpc_inverse": math.inf,
            "half_power_k_Mpc_inverse": math.inf,
            "target_constraint": float(patch["sigma_CDM_empirical"]),
            "preassembly_q": float(
                baseline_result["summary"]["CDM_preassembly_q"]
            ),
            "forward_q": float(baseline_result["summary"]["CDM_forward_q"]),
            "forward_RMSE_dex": float(
                baseline_result["summary"]["CDM_forward_RMSE"]
            ),
            "q_compatible": q_lower
            <= float(baseline_result["summary"]["CDM_forward_q"])
            <= q_upper,
            "target_used_to_define_evolution": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]
    phase_rows: list[dict[str, Any]] = []
    profile_rows: list[dict[str, Any]] = []

    locked_curve_rows = read_csv(TRANSFER_CURVES)
    locked_power_by_label = {
        label: np.asarray(
            [
                float(row["P_MTS_empirical_adiabatic_Mpc3"])
                for row in locked_curve_rows
                if row["mass_label"] == label
            ]
        )
        for label in (LOCKED_FLOOR_LABEL, REFERENCE_MASS_LABEL, LOCKED_HIGH_LABEL)
    }
    formula_checks: dict[str, float] = {}
    for label in (LOCKED_FLOOR_LABEL, REFERENCE_MASS_LABEL, LOCKED_HIGH_LABEL):
        mass_eV = float(summaries[label]["m_gap_eV"])
        calculated, _, _, _ = mass_power(
            wavenumber, cdm_power, mass_eV, reference_k_jeans
        )
        source_power = locked_power_by_label[label]
        formula_checks[label] = float(
            np.max(
                np.abs(calculated - source_power)
                / np.maximum(source_power, np.finfo(float).tiny)
            )
        )

    def execute_family(family: dict[str, Any]) -> dict[str, Any]:
        spectrum = spectrum_for_family(
            family, wavenumber, cdm_power, reference_k_jeans
        )
        snapshots, metadata = generate_snapshots(
            spectrum,
            wavenumber,
            patch_radius,
            base_context,
            arguments.force_snapshots,
        )
        context = B.make_cdm_context(base_context, snapshots)
        score, controls, phase_mass = run_response(
            spectrum["family_id"],
            context,
            polynomial,
            selected_solution,
            arguments.force_response,
        )
        row = {
            "family_id": spectrum["family_id"],
            "mass_eV": spectrum["mass_eV"],
            "mass_role": spectrum["mass_role"],
            "cutoff_Mpc_inverse": spectrum["cutoff_Mpc_inverse"],
            "k_Jeans_equality_Mpc_inverse": spectrum[
                "k_Jeans_equality_Mpc_inverse"
            ],
            "half_power_k_Mpc_inverse": spectrum["half_power_k_Mpc_inverse"],
            "spectrum_sha256": spectrum["spectrum_sha256"],
            "target_constraint": metadata["target_constraint"],
            "finite_box_sigma": metadata["conditioning"]["box_sigma"],
            "maximum_constraint_error": metadata["conditioning"][
                "maximum_constraint_error"
            ],
            "preassembly_q": float(context["baseline_score"]["q"]),
            "forward_q": float(score["q"]),
            "forward_RMSE_dex": float(
                score["velocity_squared_log10_RMSE"]
            ),
            "q_compatible": q_lower <= float(score["q"]) <= q_upper,
            "edge_mass_ratio_to_target": float(
                score["edge_mass_ratio_to_target"]
            ),
            "target_used_to_define_evolution": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        run_rows.append(row)
        for control in controls:
            phase_metadata = metadata["phases"][str(control["phase_sign"])]
            phase_rows.append(
                {
                    **control,
                    "mass_eV": spectrum["mass_eV"],
                    "cutoff_Mpc_inverse": spectrum["cutoff_Mpc_inverse"],
                    "selected_particle_count": phase_metadata[
                        "selected_particle_count"
                    ],
                    "donor_particle_count": phase_metadata[
                        "donor_particle_count"
                    ],
                    "preassembly_phase_q": phase_metadata[
                        "preassembly_phase_q"
                    ],
                    "snapshot_sha256": phase_metadata["snapshot_sha256"],
                    "constraint_error": metadata["conditioning"][
                        "maximum_constraint_error"
                    ],
                }
            )
        corrected_mass = 0.5 * (phase_mass[-1] + phase_mass[1])
        velocity_squared = (
            DYNAMICS.PREVIOUS.G_KPC_KM2_S2_MSUN
            * corrected_mass
            / np.maximum(context["radii"], np.finfo(float).tiny)
        )
        for radius, mass, velocity2 in zip(
            context["radii"], corrected_mass, velocity_squared, strict=True
        ):
            profile_rows.append(
                {
                    "family_id": spectrum["family_id"],
                    "mass_eV": spectrum["mass_eV"],
                    "cutoff_Mpc_inverse": spectrum["cutoff_Mpc_inverse"],
                    "radius_kpc": float(radius),
                    "corrected_motion_mass_Msun": float(mass),
                    "corrected_velocity_squared_km2_s2": float(velocity2),
                    "target_used": False,
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
        return row

    for family in families:
        execute_family(family)

    full_mass_rows = sorted(
        [
            row
            for row in run_rows
            if row["mass_eV"] not in (None, "")
            and row["cutoff_Mpc_inverse"] in (None, "")
        ],
        key=lambda row: float(row["mass_eV"]),
    )
    initial_bracket: tuple[dict[str, Any], dict[str, Any]] | None = None
    for lower, upper in zip(full_mass_rows[:-1], full_mass_rows[1:], strict=True):
        if float(lower["forward_q"]) > q_upper and float(upper["forward_q"]) <= q_upper:
            initial_bracket = (lower, upper)
            break
    adaptive_family: dict[str, Any] | None = None
    if initial_bracket is not None:
        midpoint = math.sqrt(
            float(initial_bracket[0]["mass_eV"])
            * float(initial_bracket[1]["mass_eV"])
        )
        adaptive_family = {
            "family_id": f"MTS_BOUND_MID_{midpoint:.9E}"
            .replace("+", "PLUS")
            .replace("-", "MINUS")
            .replace(".", "P"),
            "mass_eV": midpoint,
            "mass_role": "single_predeclared_geometric_bound_refinement",
            "cutoff_Mpc_inverse": None,
        }
        execute_family(adaptive_family)

    full_mass_rows = sorted(
        [
            row
            for row in run_rows
            if row["mass_eV"] not in (None, "")
            and row["cutoff_Mpc_inverse"] in (None, "")
        ],
        key=lambda row: float(row["mass_eV"]),
    )
    final_bracket: tuple[dict[str, Any], dict[str, Any]] | None = None
    for lower, upper in zip(full_mass_rows[:-1], full_mass_rows[1:], strict=True):
        if float(lower["forward_q"]) > q_upper and float(upper["forward_q"]) <= q_upper:
            final_bracket = (lower, upper)
            break
    monotone_q = all(
        float(upper["forward_q"])
        <= float(lower["forward_q"]) + q_envelope
        for lower, upper in zip(full_mass_rows[:-1], full_mass_rows[1:], strict=True)
    )
    if final_bracket is None:
        conditional_bound = {
            "status": "NO_Q_UPPER_CROSSING_IN_EXECUTED_MASS_RANGE",
            "lower_mass_eV": None,
            "upper_mass_eV": None,
            "lower_q": None,
            "upper_q": None,
            "parent_q_upper": q_upper,
            "monotone_within_numerical_envelope": monotone_q,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    elif not monotone_q:
        conditional_bound = {
            "status": "NUMERIC_Q_UPPER_CROSSING_PRESENT_BUT_NONMONOTONE_NO_STABLE_MASS_BOUND",
            "lower_mass_eV": float(final_bracket[0]["mass_eV"]),
            "upper_mass_eV": float(final_bracket[1]["mass_eV"]),
            "lower_q": float(final_bracket[0]["forward_q"]),
            "upper_q": float(final_bracket[1]["forward_q"]),
            "parent_q_upper": q_upper,
            "monotone_within_numerical_envelope": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    else:
        conditional_bound = {
            "status": "ONE_PATCH_CONDITIONAL_Q_UPPER_MASS_BRACKET",
            "lower_mass_eV": float(final_bracket[0]["mass_eV"]),
            "upper_mass_eV": float(final_bracket[1]["mass_eV"]),
            "lower_q": float(final_bracket[0]["forward_q"]),
            "upper_q": float(final_bracket[1]["forward_q"]),
            "parent_q_upper": q_upper,
            "monotone_within_numerical_envelope": monotone_q,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }

    by_id = {row["family_id"]: row for row in run_rows}
    full_delta_q = float(by_id["CDM_FULL"]["forward_q"]) - float(
        by_id["MTS_1E_MINUS20_FULL"]["forward_q"]
    )
    cutoff_delta_q = float(
        by_id["CDM_SPHERICAL_NYQUIST"]["forward_q"]
    ) - float(by_id["MTS_1E_MINUS20_SPHERICAL_NYQUIST"]["forward_q"])
    cutoff_delta_rmse = float(
        by_id["CDM_SPHERICAL_NYQUIST"]["forward_RMSE_dex"]
    ) - float(
        by_id["MTS_1E_MINUS20_SPHERICAL_NYQUIST"]["forward_RMSE_dex"]
    )
    full_delta_rmse = float(by_id["CDM_FULL"]["forward_RMSE_dex"]) - float(
        by_id["MTS_1E_MINUS20_FULL"]["forward_RMSE_dex"]
    )
    q_same_sign = bool(full_delta_q * cutoff_delta_q > 0.0)
    rmse_same_sign = bool(full_delta_rmse * cutoff_delta_rmse > 0.0)
    q_advantage_survives = bool(
        q_same_sign and abs(cutoff_delta_q) > q_envelope
    )
    rmse_advantage_survives = bool(
        rmse_same_sign and abs(cutoff_delta_rmse) > rmse_envelope
    )
    baseline_advantage_survives = bool(
        q_advantage_survives and rmse_advantage_survives
    )
    cutoff_control = {
        "control_id": "SHARED_SPHERICAL_COSINE_CUTOFF_AT_COARSE_AXIS_NYQUIST",
        "cutoff_Mpc_inverse": axis_nyquist,
        "full_delta_q": full_delta_q,
        "cutoff_delta_q": cutoff_delta_q,
        "retained_delta_q_fraction": abs(cutoff_delta_q)
        / max(abs(full_delta_q), np.finfo(float).tiny),
        "q_same_sign": q_same_sign,
        "q_advantage_survives": q_advantage_survives,
        "full_delta_RMSE_dex": full_delta_rmse,
        "cutoff_delta_RMSE_dex": cutoff_delta_rmse,
        "RMSE_same_sign": rmse_same_sign,
        "RMSE_advantage_survives": rmse_advantage_survives,
        "any_cutoff_difference_resolved": bool(
            abs(cutoff_delta_q) > q_envelope
            or abs(cutoff_delta_rmse) > rmse_envelope
        ),
        "checkpoint_5173_CDM_advantage_survives": baseline_advantage_survives,
        "both_cutoff_q_compatible": bool(
            by_id["CDM_SPHERICAL_NYQUIST"]["q_compatible"]
            and by_id["MTS_1E_MINUS20_SPHERICAL_NYQUIST"]["q_compatible"]
        ),
        "q_numerical_envelope": q_envelope,
        "RMSE_numerical_envelope": rmse_envelope,
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }

    if not baseline_advantage_survives:
        route_decision = (
            "THE_5173_CDM_ADVANTAGE_DOES_NOT_SURVIVE_THE_SHARED_SPHERICAL_NYQUIST_CONTROL_THE_Q_SEPARATION_COLLAPSES_AND_THE_RMSE_SIGN_REVERSES_SO_DO_NOT_REVISE_THE_PARENT_STATE_LAW_FROM_THE_CUBE_CORNER_RESULT_REQUIRE_HIGHER_RESOLUTION_ISOTROPIC_SHARED_MODES"
        )
    elif final_bracket is None or not monotone_q:
        route_decision = (
            "THE_MATCHED_SEPARATION_SURVIVES_THE_SPHERICAL_NYQUIST_CONTROL_BUT_THE_MASS_CONTINUATION_DOES_NOT_SUPPORT_A_STABLE_ONE_PATCH_BOUND_SO_MOVE_TO_A_MULTI_SEED_STATE_SELECTION_ENSEMBLE"
        )
    else:
        route_decision = (
            "THE_MATCHED_SEPARATION_SURVIVES_THE_SPHERICAL_NYQUIST_CONTROL_AND_THE_SOURCE_BACKED_MASS_CONTINUATION_BRACKETS_THE_ONE_PATCH_FORMATION_REQUIREMENT_SO_THE_PARENT_MASS_STATE_PREPARATION_LAW_MUST_NOW_DERIVE_OR_EXCLUDE_THIS_RANGE"
        )

    contract = contract_rows()
    bound_rows = [conditional_bound]
    cutoff_rows = [cutoff_control]
    decision_rows = [
        {
            "route_decision": route_decision,
            "next_target": (
                "higher_resolution_isotropic_shared_modes"
                if not baseline_advantage_survives
                else "parent_mass_and_state_preparation_law"
                if final_bracket is not None and monotone_q
                else "multi_seed_matched_formation_ensemble"
            ),
            "local_GR_Newton_Maxwell_branch_modified": False,
            "new_coupling_added": False,
            "target_used_to_define_evolution": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    ]
    provenance_rows = [
        {
            "source_id": key,
            "local_path": str(path),
            "sha256": hashes_before[key],
            "source_url": HU_SOURCE if "5156" in key or "transfer" in key else "local_checkpoint",
            "role": "read_only_input",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for key, path in paths.items()
    ]

    all_rows = (
        contract
        + spectral_rows
        + run_rows
        + phase_rows
        + profile_rows
        + bound_rows
        + cutoff_rows
        + decision_rows
        + provenance_rows
    )
    validation: list[dict[str, Any]] = []
    add_validation(validation, "all_sources_exist", not missing, missing)
    hashes_after = {key: file_digest(path) for key, path in paths.items()}
    add_validation(
        validation,
        "source_hashes_unchanged",
        hashes_before == hashes_after,
        hashes_after,
    )
    formal_after = Q.tree_digest(FORMAL)
    add_validation(
        validation,
        "formalization_workbench_unchanged",
        formal_after == FORMAL_DIGEST_LOCK,
        formal_after,
    )
    add_validation(
        validation,
        "Hu_formula_reproduces_locked_curves",
        max(formula_checks.values()) < 1.0e-10,
        formula_checks,
    )
    add_validation(
        validation,
        "all_spectra_positive_and_finite",
        all(
            np.all(np.isfinite(spectrum_for_family(f, wavenumber, cdm_power, reference_k_jeans)["power"]))
            and np.all(spectrum_for_family(f, wavenumber, cdm_power, reference_k_jeans)["power"] > 0.0)
            for f in families + ([adaptive_family] if adaptive_family is not None else [])
        ),
        len(families) + int(adaptive_family is not None),
    )
    add_validation(
        validation,
        "all_conditioned_constraints_exact",
        all(float(row.get("maximum_constraint_error", 0.0)) < 1.0e-12 for row in run_rows),
        max(float(row.get("maximum_constraint_error", 0.0)) for row in run_rows),
    )
    add_validation(
        validation,
        "all_forward_scores_finite",
        all(
            math.isfinite(float(row["preassembly_q"]))
            and math.isfinite(float(row["forward_q"]))
            and math.isfinite(float(row["forward_RMSE_dex"]))
            for row in run_rows
        ),
        len(run_rows),
    )
    add_validation(
        validation,
        "phase_transfer_conserved",
        max(abs(float(row["source_transfer_relative_residual"])) for row in phase_rows)
        < 1.0e-10,
        max(abs(float(row["source_transfer_relative_residual"])) for row in phase_rows),
    )
    add_validation(
        validation,
        "angular_momentum_conserved",
        max(
            max(
                abs(float(row["source_angular_momentum_relative_residual"])),
                abs(float(row["control_angular_momentum_relative_residual"])),
            )
            for row in phase_rows
        )
        < 1.0e-10,
        len(phase_rows),
    )
    add_validation(
        validation,
        "shared_spherical_cutoff",
        float(by_id["CDM_SPHERICAL_NYQUIST"]["cutoff_Mpc_inverse"])
        == float(by_id["MTS_1E_MINUS20_SPHERICAL_NYQUIST"]["cutoff_Mpc_inverse"]),
        axis_nyquist,
    )
    add_validation(
        validation,
        "cutoff_advantage_classification_consistent",
        baseline_advantage_survives
        == (
            cutoff_control["q_advantage_survives"]
            and cutoff_control["RMSE_advantage_survives"]
        ),
        cutoff_control,
    )
    add_validation(
        validation,
        "fixed_seed_and_dynamics",
        PM.FIXED_SEED == 407571340
        and ZOOM.PREVIOUS.COARSE_PARTICLES == 64
        and ZOOM.PARTICLE_GRID == 96
        and DYNAMICS.LOCAL_GRID == 160,
        [PM.FIXED_SEED, ZOOM.PREVIOUS.COARSE_PARTICLES, ZOOM.PARTICLE_GRID, DYNAMICS.LOCAL_GRID],
    )
    add_validation(
        validation,
        "all_rows_nonclaim",
        all(row.get("valid_for_claim") is False for row in all_rows),
        len(all_rows),
    )
    placeholder_tokens = ("MISSING_", "PLACEHOLDER", "TODO")
    add_validation(
        validation,
        "no_placeholder_tokens",
        not any(token in str(row) for row in all_rows for token in placeholder_tokens),
        len(all_rows),
    )
    failed = [row for row in validation if not row["passed"]]
    if failed:
        raise RuntimeError(f"validation failures: {failed}")

    result = {
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "route_decision": route_decision,
        "summary": {
            **spectral_summary,
            "coarse_grid": ZOOM.PREVIOUS.COARSE_PARTICLES,
            "particle_grid": ZOOM.PARTICLE_GRID,
            "local_grid": DYNAMICS.LOCAL_GRID,
            "executed_family_count": len(run_rows),
            "new_family_count": len(run_rows) - 2,
            "adaptive_family_executed": adaptive_family is not None,
            "mass_q_monotone_within_numerical_envelope": monotone_q,
            "parent_q_lower": q_lower,
            "parent_q_upper": q_upper,
            "q_numerical_envelope": q_envelope,
            "RMSE_numerical_envelope": rmse_envelope,
        },
        "conditional_mass_bound": conditional_bound,
        "cutoff_control": cutoff_control,
        "formula_reproduction_relative_errors": formula_checks,
        "validation_count": len(validation),
        "formalization_workbench_tree_sha256": formal_after,
        "valid_for_claim": False,
    }
    write_csv(CONTRACT_CSV, contract)
    write_csv(SPECTRAL_CSV, spectral_rows)
    write_csv(RUN_CSV, run_rows)
    write_csv(PHASE_CSV, phase_rows)
    write_csv(PROFILE_CSV, profile_rows)
    write_csv(BOUND_CSV, bound_rows)
    write_csv(CUTOFF_CSV, cutoff_rows)
    write_csv(DECISION_CSV, decision_rows)
    write_csv(PROVENANCE_CSV, provenance_rows)
    write_csv(VALIDATION_CSV, validation)
    Q.write_json(RESULT_JSON, result)
    DOCUMENT.write_text(document_text(result, run_rows), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
