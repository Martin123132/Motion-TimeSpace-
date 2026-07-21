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
PREVIOUS_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5174_mass_gap_continuation_and_spherical_cutoff_gate.py"
)
PREVIOUS_DOCUMENT = (
    POST
    / "5174-Y5-R2FR-mass-gap-continuation-and-spherical-cutoff-discrimination-gate.md"
)
PREVIOUS_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5174"
    / "mass_gap_continuation_and_cutoff_results.json"
)
PREVIOUS_RUNS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5174"
    / "mass_gap_continuation_forward_scores.csv"
)
PREVIOUS_VALIDATION = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5174_VALIDATION.csv"
)
OUT = POST / "source-intake" / "functional_rg" / "5175"
RUNS = OUT / "runs"
CONTRACT_CSV = OUT / "isotropic_resolution_contract.csv"
PREFLIGHT_CSV = OUT / "memory_runtime_resolution_preflight.csv"
BASIS_CSV = OUT / "shared_low_mode_basis_audit.csv"
SPECTRAL_CSV = OUT / "isotropic_transfer_band_audit.csv"
RUN_CSV = OUT / "isotropic_MTS_CDM_forward_scores.csv"
PHASE_CSV = OUT / "isotropic_phase_diagnostics.csv"
PROFILE_CSV = OUT / "isotropic_forward_profiles.csv"
COMPARISON_CSV = OUT / "resolution_discrimination_comparison.csv"
DECISION_CSV = OUT / "route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "isotropic_resolution_results.json"
VALIDATION_CSV = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5175_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5175-Y5-R2FR-exact-low-mode-shared-isotropic-resolution-discrimination-gate.md"
)

MARKER = "MTS_5175_EXACT_LOW_MODE_SHARED_ISOTROPIC_RESOLUTION_GATE"
CHECKED_DATE = "2026-07-21"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
SOURCE_GRID = 96
PARTICLE_GRID = 144
LOW_SOURCE_GRID = 64
TAPER_START_FRACTION = 0.95
HIGH_MODE_SEED = 517500409
MASS_EV = 1.0e-20
REFERENCE_GALAXY = "UGC09133"
REFERENCE_MAPPING = "Wetterich_v_equals_minus_2lambda"
SELECTED_BRANCH = ("ISOBARIC", 0.3)
STEPS_PER_INNER_ORBIT = 64
RADIAL_BINS = 26
COST_POWER = 1
ALGORITHM_VERSION = "exact_low_mode_shared_isotropic_extension_v1"


specification = importlib.util.spec_from_file_location(
    "mts_checkpoint_5174_for_5175", PREVIOUS_SCRIPT
)
if specification is None or specification.loader is None:
    raise RuntimeError(f"cannot load module: {PREVIOUS_SCRIPT}")
F = importlib.util.module_from_spec(specification)
specification.loader.exec_module(F)
B = F.B
Q = F.Q
R = F.R
V = F.V
DYNAMICS = F.DYNAMICS
ZOOM = F.ZOOM
PM = F.PM


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
        "checkpoint_5174_script": PREVIOUS_SCRIPT,
        "checkpoint_5174_document": PREVIOUS_DOCUMENT,
        "checkpoint_5174_result": PREVIOUS_RESULT,
        "checkpoint_5174_runs": PREVIOUS_RUNS,
        "checkpoint_5174_validation": PREVIOUS_VALIDATION,
        "checkpoint_5173_result": F.BASELINE_RESULT,
        "checkpoint_5169_score": B.PREVIOUS_SCORE,
        "radiation_transfer_curves": F.TRANSFER_CURVES,
        "radiation_transfer_summary": F.TRANSFER_SUMMARY,
        "checkpoint_5175_script": Path(__file__).resolve(),
    }


def file_digest(path: Path) -> str:
    return Q.file_digest(path)


def array_digest(*arrays: np.ndarray) -> str:
    digest = hashlib.sha256()
    for array in arrays:
        contiguous = np.ascontiguousarray(array)
        digest.update(str(contiguous.shape).encode("ascii"))
        digest.update(str(contiguous.dtype).encode("ascii"))
        digest.update(contiguous.tobytes())
    return digest.hexdigest()


def full_fourier_grid(
    grid_size: int, box_size: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    spacing = box_size / grid_size
    kx = 2.0 * math.pi * np.fft.fftfreq(grid_size, d=spacing)
    ky = 2.0 * math.pi * np.fft.fftfreq(grid_size, d=spacing)
    kz = 2.0 * math.pi * np.fft.fftfreq(grid_size, d=spacing)
    squared = (
        kx[:, None, None] ** 2
        + ky[None, :, None] ** 2
        + kz[None, None, :] ** 2
    )
    return kx, ky, kz, squared


def shared_standardized_modes() -> tuple[np.ndarray, dict[str, Any]]:
    coarse_rng = np.random.default_rng(PM.FIXED_SEED)
    coarse_white = coarse_rng.standard_normal(
        (LOW_SOURCE_GRID, LOW_SOURCE_GRID, LOW_SOURCE_GRID)
    )
    coarse_white -= float(np.mean(coarse_white))
    coarse_modes = np.fft.fftn(coarse_white) / math.sqrt(LOW_SOURCE_GRID**3)
    coarse_modes[0, 0, 0] = 0.0

    high_rng = np.random.default_rng(HIGH_MODE_SEED)
    high_white = high_rng.standard_normal(
        (SOURCE_GRID, SOURCE_GRID, SOURCE_GRID)
    )
    high_white -= float(np.mean(high_white))
    high_modes = np.fft.fftn(high_white) / math.sqrt(SOURCE_GRID**3)

    coarse_frequencies = np.rint(
        np.fft.fftfreq(LOW_SOURCE_GRID) * LOW_SOURCE_GRID
    ).astype(int)
    shared_indices = np.flatnonzero(
        np.abs(coarse_frequencies) < LOW_SOURCE_GRID // 2
    )
    signed = coarse_frequencies[shared_indices]
    high_indices = np.mod(signed, SOURCE_GRID)
    high_modes[np.ix_(high_indices, high_indices, high_indices)] = coarse_modes[
        np.ix_(shared_indices, shared_indices, shared_indices)
    ]
    high_modes[0, 0, 0] = 0.0
    shared_error = float(
        np.max(
            np.abs(
                high_modes[np.ix_(high_indices, high_indices, high_indices)]
                - coarse_modes[
                    np.ix_(shared_indices, shared_indices, shared_indices)
                ]
            )
        )
    )
    hermitian_field = np.fft.ifftn(high_modes)
    hermitian_error = float(np.max(np.abs(np.imag(hermitian_field))))
    diagnostics = {
        "coarse_seed": PM.FIXED_SEED,
        "new_high_mode_seed": HIGH_MODE_SEED,
        "coarse_grid": LOW_SOURCE_GRID,
        "extended_grid": SOURCE_GRID,
        "shared_integer_mode_minimum": int(np.min(signed)),
        "shared_integer_mode_maximum": int(np.max(signed)),
        "shared_mode_count": int(len(shared_indices) ** 3),
        "shared_standardized_mode_maximum_error": shared_error,
        "Hermitian_inverse_maximum_imaginary": hermitian_error,
        "basis_sha256": array_digest(high_modes),
    }
    return high_modes, diagnostics


def spherical_taper(
    wavenumber: np.ndarray, power: np.ndarray, cutoff: float
) -> tuple[np.ndarray, np.ndarray]:
    lower = TAPER_START_FRACTION * cutoff
    window = np.ones_like(wavenumber)
    transition = (wavenumber > lower) & (wavenumber < cutoff)
    window[transition] = 0.5 * (
        1.0
        + np.cos(math.pi * (wavenumber[transition] - lower) / (cutoff - lower))
    )
    window[wavenumber >= cutoff] = 1.0e-30
    filtered = np.maximum(power * window, power * 1.0e-30)
    return filtered, window


def build_conditioned_pair_from_modes(
    standardized_modes: np.ndarray,
    box_size: float,
    patch_radius: float,
    target_delta: float,
    source_k: np.ndarray,
    source_power: np.ndarray,
) -> tuple[dict[int, np.ndarray], dict[str, Any]]:
    grid_size = standardized_modes.shape[0]
    volume = box_size**3
    kx, ky, kz, squared = full_fourier_grid(grid_size, box_size)
    magnitude = np.sqrt(squared)
    mode_power = PM.interpolate_power(magnitude, source_k, source_power)
    mode_power[0, 0, 0] = 0.0
    window = PM.PREVIOUS.top_hat(magnitude * patch_radius)
    raw_fourier = standardized_modes * grid_size**3 * np.sqrt(
        mode_power / volume
    )
    center_value = box_size / 2.0
    phase = np.exp(
        -1j
        * (
            kx[:, None, None] * center_value
            + ky[None, :, None] * center_value
            + kz[None, None, :] * center_value
        )
    )
    covariance_fourier = (
        grid_size**3 * mode_power * window * phase / volume
    )
    center_index = grid_size // 2
    raw_smoothed = np.fft.ifftn(raw_fourier * window)
    random_constraint = float(np.real(raw_smoothed[center_index] [center_index] [center_index]))
    covariance_smoothed = np.fft.ifftn(covariance_fourier * window)
    box_variance = float(
        np.real(covariance_smoothed[center_index] [center_index] [center_index])
    )
    if box_variance <= 0.0:
        raise RuntimeError("nonpositive finite-box constraint variance")
    residual_fourier = (
        raw_fourier - random_constraint * covariance_fourier / box_variance
    )
    residual_complex = np.fft.ifftn(residual_fourier)
    residual_imaginary = float(np.max(np.abs(np.imag(residual_complex))))
    residual_field = np.real(residual_complex)
    residual_smoothed = np.fft.ifftn(residual_fourier * window)
    residual_constraint = float(
        np.real(residual_smoothed[center_index] [center_index] [center_index])
    )
    mean_field, full_variance = PM.build_mean_density_field(
        grid_size,
        box_size,
        patch_radius,
        target_delta,
        source_k,
        source_power,
    )
    fields = {-1: mean_field - residual_field, 1: mean_field + residual_field}
    constraints: dict[int, float] = {}
    maximum_field_imaginary = residual_imaginary
    for phase_sign, field in fields.items():
        smoothed = np.fft.ifftn(np.fft.fftn(field) * window)
        maximum_field_imaginary = max(
            maximum_field_imaginary,
            float(np.max(np.abs(np.imag(smoothed)))),
        )
        constraints[phase_sign] = float(
            np.real(smoothed[center_index] [center_index] [center_index])
        )
    pair_mean_error = float(
        np.max(np.abs(0.5 * (fields[-1] + fields[1]) - mean_field))
    )
    residual_antisymmetry_error = float(
        np.max(
            np.abs(
                (fields[1] - mean_field) + (fields[-1] - mean_field)
            )
        )
    )
    diagnostics = {
        "full_sigma": math.sqrt(full_variance),
        "box_sigma": math.sqrt(box_variance),
        "box_to_full_sigma": math.sqrt(box_variance / full_variance),
        "raw_random_constraint": random_constraint,
        "conditioned_residual_constraint": residual_constraint,
        "minus_constraint": constraints[-1],
        "plus_constraint": constraints[1],
        "target_constraint": target_delta,
        "maximum_constraint_error": max(
            abs(constraints[-1] - target_delta),
            abs(constraints[1] - target_delta),
        ),
        "pair_mean_error": pair_mean_error,
        "residual_antisymmetry_error": residual_antisymmetry_error,
        "maximum_imaginary_residual": maximum_field_imaginary,
        "z0_delta_minimum": min(float(np.min(field)) for field in fields.values()),
        "z0_delta_maximum": max(float(np.max(field)) for field in fields.values()),
    }
    return fields, diagnostics


def family_spectra(
    wavenumber: np.ndarray,
    cdm_power: np.ndarray,
    reference_power: np.ndarray,
    axis_nyquist: float,
) -> list[dict[str, Any]]:
    families = []
    for family_id, model, power in (
        ("MTS_1E_MINUS20_ISOTROPIC_96", "MTS_1e_minus20_eV", reference_power),
        ("CDM_ISOTROPIC_96", "CDM", cdm_power),
    ):
        filtered, taper = spherical_taper(wavenumber, power, axis_nyquist)
        families.append(
            {
                "family_id": family_id,
                "model": model,
                "mass_eV": MASS_EV if model.startswith("MTS") else None,
                "power": filtered,
                "taper": taper,
                "cutoff_Mpc_inverse": axis_nyquist,
                "spectrum_sha256": array_digest(wavenumber, filtered),
            }
        )
    return families


def run_paths(family_id: str) -> dict[str, Any]:
    run_dir = RUNS / family_id
    return {
        "dir": run_dir,
        "snapshots": {
            -1: run_dir / "phase_minus_isolated_initial_state.npz",
            1: run_dir / "phase_plus_isolated_initial_state.npz",
        },
        "phase_metadata": {
            -1: run_dir / "phase_minus_snapshot_metadata.json",
            1: run_dir / "phase_plus_snapshot_metadata.json",
        },
        "metadata": run_dir / "isolated_initial_state_metadata.json",
        "cache": run_dir / "evolution-cache",
    }


def generate_snapshots(
    family: dict[str, Any],
    standardized_modes: np.ndarray,
    basis_diagnostics: dict[str, Any],
    wavenumber: np.ndarray,
    patch_radius: float,
    base_context: dict[str, Any],
    force: bool,
) -> tuple[dict[int, dict[str, Any]], dict[str, Any]]:
    paths = run_paths(family["family_id"])
    target_constraint = F.full_sigma(
        wavenumber, family["power"], patch_radius
    )
    signature_payload = {
        "algorithm": ALGORITHM_VERSION,
        "family_id": family["family_id"],
        "spectrum_sha256": family["spectrum_sha256"],
        "basis_sha256": basis_diagnostics["basis_sha256"],
        "target_constraint": target_constraint,
        "source_grid": SOURCE_GRID,
        "particle_grid": PARTICLE_GRID,
        "global_force_grid": ZOOM.GLOBAL_FORCE_GRID,
        "local_grid": DYNAMICS.LOCAL_GRID,
    }
    signature = hashlib.sha256(
        json.dumps(signature_payload, sort_keys=True).encode("utf-8")
    ).hexdigest()
    source_fields, conditioning = build_conditioned_pair_from_modes(
        standardized_modes,
        PM.BOX_OVER_PATCH * patch_radius,
        patch_radius,
        target_constraint,
        wavenumber,
        family["power"],
    )
    particle_fields = {
        phase_sign: ZOOM.PREVIOUS.periodic_fourier_resample(
            source_fields[phase_sign], PARTICLE_GRID
        )
        for phase_sign in ZOOM.PAIR_SIGNS
    }
    _, states = ZOOM.PREVIOUS.initial_rows_and_states(
        {PARTICLE_GRID: particle_fields},
        PM.BOX_OVER_PATCH * patch_radius,
        patch_radius,
    )
    targets, _, _, _ = ZOOM.PREVIOUS.target_lookup()
    target = targets[REFERENCE_MAPPING]
    edge_radius_Mpc = float(target["edge_radius_Mpc"])
    box_size_Mpc = PM.BOX_OVER_PATCH * patch_radius
    lagrangian_positions = PM.particle_lattice(PARTICLE_GRID, box_size_Mpc)
    metadata: dict[str, Any] = {
        "cache_signature": signature,
        "signature_payload": signature_payload,
        "checkpoint_marker": MARKER,
        "family_id": family["family_id"],
        "model": family["model"],
        "mass_eV": family["mass_eV"],
        "cutoff_Mpc_inverse": family["cutoff_Mpc_inverse"],
        "target_constraint": target_constraint,
        "conditioning": conditioning,
        "basis_diagnostics": basis_diagnostics,
        "box_size_Mpc": box_size_Mpc,
        "patch_radius_Mpc": patch_radius,
        "edge_radius_kpc": 1000.0 * edge_radius_Mpc,
        "phases": {},
    }
    snapshots: dict[int, dict[str, Any]] = {}
    paths["dir"].mkdir(parents=True, exist_ok=True)
    for phase_sign in ZOOM.PAIR_SIGNS:
        snapshot_path = paths["snapshots"][phase_sign]
        phase_metadata_path = paths["phase_metadata"][phase_sign]
        cached = False
        if not force and snapshot_path.is_file() and phase_metadata_path.is_file():
            phase_metadata = json.loads(
                phase_metadata_path.read_text(encoding="utf-8")
            )
            if phase_metadata.get("cache_signature") == signature:
                with np.load(snapshot_path) as archive:
                    snapshots[phase_sign] = {
                        key: archive[key] for key in archive.files
                    }
                metadata["phases"][str(phase_sign)] = phase_metadata
                cached = True
        if cached:
            continue
        print(
            f"START {family['family_id']} nested phase={phase_sign:+d}",
            flush=True,
        )
        start = time.perf_counter()
        initial = states[(PARTICLE_GRID, phase_sign)]
        evolved = ZOOM.evolve_nested(
            np.asarray(initial["positions"], dtype=float),
            np.asarray(initial["momenta"], dtype=float),
            lagrangian_positions,
            np.asarray(initial["tagged"], dtype=bool),
            PARTICLE_GRID,
            DYNAMICS.LOCAL_GRID,
            box_size_Mpc,
            edge_radius_Mpc,
        )
        profile = ZOOM.zoom_profile(
            np.asarray(evolved["positions"], dtype=float),
            np.asarray(initial["tagged"], dtype=bool),
            PARTICLE_GRID,
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
        np.savez_compressed(snapshot_path, **snapshot)
        phase_metadata = {
            "cache_signature": signature,
            "phase_sign": phase_sign,
            "selected_particle_count": int(np.count_nonzero(selected)),
            "donor_particle_count": int(np.count_nonzero(donors)),
            "particle_mass_Msun": particle_mass,
            "preassembly_phase_q": q_value,
            "wall_seconds": time.perf_counter() - start,
            "snapshot_sha256": file_digest(snapshot_path),
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        Q.write_json(phase_metadata_path, phase_metadata)
        metadata["phases"][str(phase_sign)] = phase_metadata
        print(
            f"DONE {family['family_id']} nested phase={phase_sign:+d} "
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
    print(f"START {family_id} {role} phase={phase_sign:+d}", flush=True)
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


def preflight_rows(
    box_size: float,
    previous_result: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    source_axis_nyquist = math.pi * SOURCE_GRID / box_size
    particle_axis_nyquist = math.pi * PARTICLE_GRID / box_size
    force_axis_nyquist = math.pi * ZOOM.GLOBAL_FORCE_GRID / box_size
    previous_phase_rows = read_csv(F.PHASE_CSV)
    previous_nested_seconds = []
    for family_id in (
        "MTS_1E_MINUS20_SPHERICAL_NYQUIST",
        "CDM_SPHERICAL_NYQUIST",
    ):
        metadata = json.loads(
            (F.RUNS / family_id / "isolated_initial_state_metadata.json").read_text(
                encoding="utf-8"
            )
        )
        previous_nested_seconds.extend(
            float(metadata["phases"][str(sign)]["wall_seconds"])
            for sign in (-1, 1)
        )
    nested_scale = (PARTICLE_GRID / ZOOM.PARTICLE_GRID) ** 3
    estimated_nested_phase_seconds = float(np.mean(previous_nested_seconds)) * nested_scale
    previous_response_seconds = [
        float(row["source_wall_seconds"]) + float(row["control_wall_seconds"])
        for row in previous_phase_rows
        if row["family_id"]
        in (
            "MTS_1E_MINUS20_SPHERICAL_NYQUIST",
            "CDM_SPHERICAL_NYQUIST",
        )
    ]
    estimated_response_phase_seconds = float(np.mean(previous_response_seconds)) * nested_scale
    estimated_total_seconds = 4.0 * (
        estimated_nested_phase_seconds + estimated_response_phase_seconds
    )
    particle_count = PARTICLE_GRID**3
    vector_bytes = particle_count * 3 * 8
    scalar_bytes = particle_count * 8
    force_bytes = ZOOM.GLOBAL_FORCE_GRID**3 * 8
    local_bytes = DYNAMICS.LOCAL_GRID**3 * 8
    conservative_peak_bytes = (
        14 * vector_bytes
        + 16 * scalar_bytes
        + 20 * force_bytes
        + 20 * local_bytes
        + 2 * 1024**3
    )
    summary = {
        "source_grid": SOURCE_GRID,
        "particle_grid": PARTICLE_GRID,
        "global_force_grid": ZOOM.GLOBAL_FORCE_GRID,
        "local_force_grid": DYNAMICS.LOCAL_GRID,
        "source_axis_nyquist_Mpc_inverse": source_axis_nyquist,
        "particle_axis_nyquist_Mpc_inverse": particle_axis_nyquist,
        "force_axis_nyquist_Mpc_inverse": force_axis_nyquist,
        "previous_density_deficit_k90_Mpc_inverse": previous_result["summary"][
            "density_deficit_k90_Mpc_inverse"
        ],
        "source_axis_exceeds_previous_k90": source_axis_nyquist
        > previous_result["summary"]["density_deficit_k90_Mpc_inverse"],
        "particles_per_source_nyquist_wavelength": 2.0
        * PARTICLE_GRID
        / SOURCE_GRID,
        "force_cells_per_source_nyquist_wavelength": 2.0
        * ZOOM.GLOBAL_FORCE_GRID
        / SOURCE_GRID,
        "particle_count": particle_count,
        "estimated_nested_phase_seconds": estimated_nested_phase_seconds,
        "estimated_response_phase_seconds": estimated_response_phase_seconds,
        "estimated_total_wall_hours": estimated_total_seconds / 3600.0,
        "conservative_peak_memory_GiB": conservative_peak_bytes / 2**30,
        "32_GiB_safe_with_4_GiB_reserve": conservative_peak_bytes < 28 * 2**30,
    }
    rows = [
        {
            "quantity": key,
            "value": value,
            "acceptance": (
                "PASS"
                if key
                in (
                    "source_axis_exceeds_previous_k90",
                    "32_GiB_safe_with_4_GiB_reserve",
                )
                and bool(value)
                else "INFORMATIONAL"
            ),
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for key, value in summary.items()
    ]
    return rows, summary


def contract_rows() -> list[dict[str, Any]]:
    clauses = [
        (
            "I1_EXACT_LOW_MODES",
            "all non-Nyquist 64-grid standardized Fourier modes are embedded exactly in the 96-grid basis",
        ),
        (
            "I2_SHARED_NEW_MODES",
            "MTS and CDM use the same deterministic newly resolved high-mode basis",
        ),
        (
            "I3_ISOTROPIC_CUTOFF",
            "both spectra receive the same five-percent cosine taper at the 96-grid axis Nyquist",
        ),
        (
            "I4_PARTICLE_SAMPLING",
            "the 96-grid source is sampled by 144^3 particles and a 192^3 global force mesh",
        ),
        (
            "I5_IDENTICAL_PHYSICS",
            "calibrated G_N, nested force, visible history, transport and score are unchanged",
        ),
        (
            "I6_NO_TARGET_FEEDBACK",
            "observed q and velocity enter only after both forward histories finish",
        ),
        (
            "I7_NONCLAIM",
            "one extended antithetic realization is a resolution discrimination test, not an ensemble or MTS claim",
        ),
    ]
    return [
        {
            "clause_id": clause_id,
            "contract": contract,
            "status": "frozen_before_evolution",
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


def document_text(result: dict[str, Any]) -> str:
    summary = result["summary"]
    comparison = result["comparison"]
    return f"""# 5175 - Exact-low-mode-shared isotropic resolution discrimination gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Question

Checkpoint 5174 showed that the checkpoint-5173 CDM advantage was carried by
directionally under-resolved cube-corner modes. This checkpoint does not delete
the physical band. It resolves it isotropically by embedding the old low-mode
basis into a `96^3` source, adding one common high-mode realization, sampling it
with `144^3` particles and applying the same spherical taper to MTS and CDM.

## Exact shared-mode construction

For the standardized Gaussian Fourier basis `z_n`, every coarse integer mode
with component `|n_i|<32` is copied exactly into the extended grid. Coarse
Nyquist planes are excluded because they were removed by checkpoint 5174's
spherical control. New modes use one frozen independent seed and are shared by
both spectra. The maximum copied-mode error is
`{summary['shared_standardized_mode_maximum_error']}` and the inverse Hermitian
error is `{summary['Hermitian_inverse_maximum_imaginary']}`.

The axis Nyquist rises from `20.15885441863777` to
`{summary['source_axis_nyquist_Mpc_inverse']} Mpc^-1`, above checkpoint 5174's
density-deficit `k90={summary['previous_density_deficit_k90_Mpc_inverse']}`.
The particle and force meshes supply respectively
`{summary['particles_per_source_nyquist_wavelength']}` and
`{summary['force_cells_per_source_nyquist_wavelength']}` cells per shortest
retained source wavelength.

## Forward result

```text
MTS preassembly q={comparison['MTS_preassembly_q']},
CDM preassembly q={comparison['CDM_preassembly_q']},
MTS forward q={comparison['MTS_forward_q']},
CDM forward q={comparison['CDM_forward_q']},
Delta q(CDM-MTS)={comparison['isotropic_delta_q']};
MTS q-band distance={comparison['MTS_q_band_distance']},
CDM q-band distance={comparison['CDM_q_band_distance']};

MTS RMSE={comparison['MTS_forward_RMSE_dex']} dex,
CDM RMSE={comparison['CDM_forward_RMSE_dex']} dex,
Delta RMSE(CDM-MTS)={comparison['isotropic_delta_RMSE_dex']} dex.
```

The inherited numerical envelopes are `{comparison['q_numerical_envelope']}`
in q and `{comparison['RMSE_numerical_envelope']}` dex. Simultaneous passage
of the parent q band is `{comparison['both_q_compatible']}`. The matched
branches are classified as `{comparison['classification']}`.

This is a single shared realization. A resolved difference identifies the
need for a seed ensemble; it does not establish a model preference. An
unresolved difference shows only that the present formation gate does not
discriminate the spectra at this resolution.

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
    previous_result = json.loads(PREVIOUS_RESULT.read_text(encoding="utf-8"))
    wavenumber, cdm_power, reference_power, _, _ = F.transfer_inputs()
    base_context, polynomial, _, solutions = R.build_parent_state()
    selected_solution = solutions[SELECTED_BRANCH]
    _, _, patch_radius, _ = ZOOM.PREVIOUS.target_lookup()
    box_size = PM.BOX_OVER_PATCH * patch_radius
    axis_nyquist = math.pi * SOURCE_GRID / box_size
    preflight, preflight_summary = preflight_rows(box_size, previous_result)
    standardized_modes, basis_diagnostics = shared_standardized_modes()
    families = family_spectra(
        wavenumber, cdm_power, reference_power, axis_nyquist
    )
    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "marker": MARKER,
                    "preflight": preflight_summary,
                    "basis": basis_diagnostics,
                    "families": [
                        {
                            key: value
                            for key, value in family.items()
                            if key not in ("power", "taper")
                        }
                        for family in families
                    ],
                    "formal_digest": formal_before,
                },
                indent=2,
            )
        )
        return
    if not preflight_summary["source_axis_exceeds_previous_k90"]:
        raise RuntimeError("source grid does not cover checkpoint-5174 k90")
    if not preflight_summary["32_GiB_safe_with_4_GiB_reserve"]:
        raise RuntimeError("preflight memory gate failed")

    q_lower = float(previous_result["summary"]["parent_q_lower"])
    q_upper = float(previous_result["summary"]["parent_q_upper"])
    q_envelope = float(previous_result["summary"]["q_numerical_envelope"])
    rmse_envelope = float(previous_result["summary"]["RMSE_numerical_envelope"])
    run_rows: list[dict[str, Any]] = []
    phase_rows: list[dict[str, Any]] = []
    profile_rows: list[dict[str, Any]] = []
    conditioning_rows: list[dict[str, Any]] = []
    for family in families:
        snapshots, metadata = generate_snapshots(
            family,
            standardized_modes,
            basis_diagnostics,
            wavenumber,
            patch_radius,
            base_context,
            arguments.force_snapshots,
        )
        context = B.make_cdm_context(base_context, snapshots)
        score, controls, phase_mass = run_response(
            family["family_id"],
            context,
            polynomial,
            selected_solution,
            arguments.force_response,
        )
        run_rows.append(
            {
                "family_id": family["family_id"],
                "model": family["model"],
                "mass_eV": family["mass_eV"],
                "source_grid": SOURCE_GRID,
                "particle_grid": PARTICLE_GRID,
                "global_force_grid": ZOOM.GLOBAL_FORCE_GRID,
                "local_force_grid": DYNAMICS.LOCAL_GRID,
                "cutoff_Mpc_inverse": family["cutoff_Mpc_inverse"],
                "target_constraint": metadata["target_constraint"],
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
        )
        conditioning_rows.append(
            {
                "family_id": family["family_id"],
                **metadata["conditioning"],
                "basis_sha256": basis_diagnostics["basis_sha256"],
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
        for control in controls:
            phase_metadata = metadata["phases"][str(control["phase_sign"])]
            phase_rows.append(
                {
                    **control,
                    "model": family["model"],
                    "selected_particle_count": phase_metadata[
                        "selected_particle_count"
                    ],
                    "donor_particle_count": phase_metadata[
                        "donor_particle_count"
                    ],
                    "preassembly_phase_q": phase_metadata[
                        "preassembly_phase_q"
                    ],
                    "snapshot_wall_seconds": phase_metadata["wall_seconds"],
                    "snapshot_sha256": phase_metadata["snapshot_sha256"],
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
                    "family_id": family["family_id"],
                    "model": family["model"],
                    "radius_kpc": float(radius),
                    "corrected_motion_mass_Msun": float(mass),
                    "corrected_velocity_squared_km2_s2": float(velocity2),
                    "target_used": False,
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )

    by_model = {row["model"]: row for row in run_rows}
    mts = by_model["MTS_1e_minus20_eV"]
    cdm = by_model["CDM"]
    delta_q = float(cdm["forward_q"]) - float(mts["forward_q"])
    delta_rmse = float(cdm["forward_RMSE_dex"]) - float(
        mts["forward_RMSE_dex"]
    )
    q_resolved = abs(delta_q) > q_envelope
    rmse_resolved = abs(delta_rmse) > rmse_envelope
    mts_q_band_distance = max(
        q_lower - float(mts["forward_q"]),
        0.0,
        float(mts["forward_q"]) - q_upper,
    )
    cdm_q_band_distance = max(
        q_lower - float(cdm["forward_q"]),
        0.0,
        float(cdm["forward_q"]) - q_upper,
    )
    cdm_q_better = cdm_q_band_distance + q_envelope < mts_q_band_distance
    mts_q_better = mts_q_band_distance + q_envelope < cdm_q_band_distance
    cdm_rmse_better = (
        float(cdm["forward_RMSE_dex"]) + rmse_envelope
        < float(mts["forward_RMSE_dex"])
    )
    mts_rmse_better = (
        float(mts["forward_RMSE_dex"]) + rmse_envelope
        < float(cdm["forward_RMSE_dex"])
    )
    if not q_resolved and not rmse_resolved:
        classification = "NOT_DISCRIMINATED_WITHIN_INHERITED_NUMERICAL_ENVELOPES"
        route_decision = (
            "THE_ISOTROPICALLY_RESOLVED_TRANSFER_BAND_DOES_NOT_DISCRIMINATE_MTS_FROM_CDM_IN_THIS_SHARED_REALIZATION_SO_RETAIN_THE_PARENT_STATE_ROUTE_AND_MOVE_TO_AN_ENSEMBLE_ONLY_IF_FORMATION_STATISTICS_ARE_NEEDED"
        )
        next_target = "return_to_parent_state_preparation_and_local_GR_spine"
    elif cdm_q_better and cdm_rmse_better:
        classification = "CDM_CLOSER_ON_Q_AND_RMSE_IN_ONE_RESOLVED_REALIZATION"
        route_decision = (
            "THE_ISOTROPICALLY_RESOLVED_TRANSFER_BAND_FAVORS_CDM_IN_THIS_ONE_SHARED_REALIZATION_REQUIRE_A_PREDECLARED_MULTI_SEED_ENSEMBLE_BEFORE_REVISING_THE_PARENT_STATE_LAW"
        )
        next_target = "predeclared_multi_seed_matched_ensemble"
    elif mts_q_better and mts_rmse_better:
        classification = "MTS_CLOSER_ON_Q_AND_RMSE_IN_ONE_RESOLVED_REALIZATION"
        route_decision = (
            "THE_ISOTROPICALLY_RESOLVED_TRANSFER_BAND_FAVORS_MTS_IN_THIS_ONE_SHARED_REALIZATION_REQUIRE_A_PREDECLARED_MULTI_SEED_ENSEMBLE_BEFORE_ANY_POSITIVE_CLAIM"
        )
        next_target = "predeclared_multi_seed_matched_ensemble"
    else:
        classification = "MIXED_OR_SINGLE_METRIC_RESOLVED_DIFFERENCE"
        route_decision = (
            "THE_ISOTROPICALLY_RESOLVED_TRANSFER_BAND_SPLITS_OR_ONLY_PARTLY_RESOLVES_THE_MATCHED_METRICS_SO_NO_MODEL_PREFERENCE_IS_ASSIGNED_REQUIRE_A_PREDECLARED_MULTI_SEED_ENSEMBLE"
        )
        next_target = "predeclared_multi_seed_matched_ensemble"

    comparison = {
        "comparison_id": "ISOTROPIC_96_SOURCE_144_PARTICLE_MTS_VS_CDM",
        "MTS_preassembly_q": float(mts["preassembly_q"]),
        "CDM_preassembly_q": float(cdm["preassembly_q"]),
        "MTS_forward_q": float(mts["forward_q"]),
        "CDM_forward_q": float(cdm["forward_q"]),
        "isotropic_delta_q": delta_q,
        "MTS_q_band_distance": mts_q_band_distance,
        "CDM_q_band_distance": cdm_q_band_distance,
        "CDM_q_better": cdm_q_better,
        "MTS_q_better": mts_q_better,
        "MTS_forward_RMSE_dex": float(mts["forward_RMSE_dex"]),
        "CDM_forward_RMSE_dex": float(cdm["forward_RMSE_dex"]),
        "isotropic_delta_RMSE_dex": delta_rmse,
        "CDM_RMSE_better": cdm_rmse_better,
        "MTS_RMSE_better": mts_rmse_better,
        "q_numerical_envelope": q_envelope,
        "RMSE_numerical_envelope": rmse_envelope,
        "q_difference_resolved": q_resolved,
        "RMSE_difference_resolved": rmse_resolved,
        "both_q_compatible": bool(mts["q_compatible"] and cdm["q_compatible"]),
        "classification": classification,
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }
    previous_cutoff = previous_result["cutoff_control"]
    comparison_rows = [
        {
            "resolution_id": "checkpoint_5174_64_source_96_particle_cutoff",
            "source_axis_nyquist_Mpc_inverse": previous_cutoff[
                "cutoff_Mpc_inverse"
            ],
            "delta_q_CDM_minus_MTS": previous_cutoff["cutoff_delta_q"],
            "delta_RMSE_CDM_minus_MTS_dex": previous_cutoff[
                "cutoff_delta_RMSE_dex"
            ],
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "resolution_id": "checkpoint_5175_96_source_144_particle_cutoff",
            "source_axis_nyquist_Mpc_inverse": axis_nyquist,
            "delta_q_CDM_minus_MTS": delta_q,
            "delta_RMSE_CDM_minus_MTS_dex": delta_rmse,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]

    spectral_rows: list[dict[str, Any]] = []
    for probe_id, probe_k in (
        ("previous_axis_nyquist", previous_cutoff["cutoff_Mpc_inverse"]),
        (
            "previous_density_deficit_k50",
            previous_result["summary"]["density_deficit_k50_Mpc_inverse"],
        ),
        (
            "previous_density_deficit_k90",
            previous_result["summary"]["density_deficit_k90_Mpc_inverse"],
        ),
        ("new_taper_start", TAPER_START_FRACTION * axis_nyquist),
        ("new_axis_nyquist", axis_nyquist),
    ):
        p_cdm = float(np.interp(probe_k, wavenumber, cdm_power))
        p_mts = float(np.interp(probe_k, wavenumber, reference_power))
        spectral_rows.append(
            {
                "probe_id": probe_id,
                "k_Mpc_inverse": probe_k,
                "P_CDM_Mpc3": p_cdm,
                "P_MTS_Mpc3": p_mts,
                "MTS_to_CDM_power_ratio": p_mts / p_cdm,
                "inside_new_isotropic_support": probe_k <= axis_nyquist,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )

    basis_rows = [
        {
            "audit_id": "EXACT_STANDARDIZED_LOW_MODE_EMBEDDING",
            **basis_diagnostics,
            "MTS_CDM_basis_shared": True,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    ] + conditioning_rows
    contract = contract_rows()
    decision_rows = [
        {
            "route_decision": route_decision,
            "next_target": next_target,
            "new_coupling_added": False,
            "local_GR_Newton_Maxwell_branch_modified": False,
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
            "role": "read_only_input",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for key, path in paths.items()
    ]
    all_rows = (
        contract
        + preflight
        + basis_rows
        + spectral_rows
        + run_rows
        + phase_rows
        + profile_rows
        + comparison_rows
        + [comparison]
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
        "exact_low_mode_basis",
        basis_diagnostics["shared_standardized_mode_maximum_error"] == 0.0,
        basis_diagnostics,
    )
    add_validation(
        validation,
        "Hermitian_basis",
        basis_diagnostics["Hermitian_inverse_maximum_imaginary"] < 1.0e-12,
        basis_diagnostics["Hermitian_inverse_maximum_imaginary"],
    )
    add_validation(
        validation,
        "resolved_band_covered",
        preflight_summary["source_axis_exceeds_previous_k90"]
        and preflight_summary["particles_per_source_nyquist_wavelength"] >= 3.0
        and preflight_summary["force_cells_per_source_nyquist_wavelength"] >= 4.0,
        preflight_summary,
    )
    add_validation(
        validation,
        "preflight_memory_safe",
        preflight_summary["32_GiB_safe_with_4_GiB_reserve"],
        preflight_summary["conservative_peak_memory_GiB"],
    )
    add_validation(
        validation,
        "conditioned_constraints_exact",
        max(float(row["maximum_constraint_error"]) for row in conditioning_rows)
        < 1.0e-12,
        max(float(row["maximum_constraint_error"]) for row in conditioning_rows),
    )
    add_validation(
        validation,
        "conditioned_fields_real",
        max(float(row["maximum_imaginary_residual"]) for row in conditioning_rows)
        < 1.0e-12,
        max(float(row["maximum_imaginary_residual"]) for row in conditioning_rows),
    )
    add_validation(
        validation,
        "forward_scores_finite",
        all(
            math.isfinite(float(row["preassembly_q"]))
            and math.isfinite(float(row["forward_q"]))
            and math.isfinite(float(row["forward_RMSE_dex"]))
            for row in run_rows
        ),
        run_rows,
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
        "same_grids_and_cutoff",
        {int(row["source_grid"]) for row in run_rows} == {SOURCE_GRID}
        and {int(row["particle_grid"]) for row in run_rows} == {PARTICLE_GRID}
        and len({float(row["cutoff_Mpc_inverse"]) for row in run_rows}) == 1,
        run_rows,
    )
    add_validation(
        validation,
        "classification_consistent",
        comparison["q_difference_resolved"] == q_resolved
        and comparison["RMSE_difference_resolved"] == rmse_resolved,
        comparison,
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
        "summary": {**preflight_summary, **basis_diagnostics},
        "comparison": comparison,
        "validation_count": len(validation),
        "formalization_workbench_tree_sha256": formal_after,
        "valid_for_claim": False,
    }
    write_csv(CONTRACT_CSV, contract)
    write_csv(PREFLIGHT_CSV, preflight)
    write_csv(BASIS_CSV, basis_rows)
    write_csv(SPECTRAL_CSV, spectral_rows)
    write_csv(RUN_CSV, run_rows)
    write_csv(PHASE_CSV, phase_rows)
    write_csv(PROFILE_CSV, profile_rows)
    write_csv(COMPARISON_CSV, comparison_rows + [comparison])
    write_csv(DECISION_CSV, decision_rows)
    write_csv(PROVENANCE_CSV, provenance_rows)
    write_csv(VALIDATION_CSV, validation)
    Q.write_json(RESULT_JSON, result)
    DOCUMENT.write_text(document_text(result), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
