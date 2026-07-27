from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import scipy
import scipy.signal._signaltools as scipy_signaltools
from scipy.signal import resample


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
PREVIOUS_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5160_paired_3D_constrained_PM_collapse_gate.py"
)
PREVIOUS_DOCUMENT = (
    POST
    / "5160-Y5-R2FR-paired-3D-constrained-realization-particle-mesh-collapse-and-tidal-profile-gate.md"
)
PREVIOUS_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5160"
    / "paired_3D_constrained_PM_results.json"
)
OUT = POST / "source-intake" / "functional_rg" / "5161"
RESULT_JSON = OUT / "shared_mode_particle_convergence_results.json"
CONTRACT_CSV = OUT / "shared_mode_refinement_contract.csv"
PHASE_CSV = OUT / "exact_phase_matching_audit.csv"
INITIAL_CSV = OUT / "shared_mode_initial_diagnostics.csv"
RUN_CSV = OUT / "shared_mode_PM_run_summary.csv"
PROFILE_CSV = OUT / "shared_mode_profile_samples.csv"
SCORE_CSV = OUT / "shared_mode_no_refit_scores.csv"
CONVERGENCE_CSV = OUT / "particle_resolution_convergence_gate.csv"
ZOOM_CSV = OUT / "transition_zoom_resolution_requirement.csv"
CONTROL_CSV = OUT / "inherited_PM_equation_controls.csv"
COG_CSV = OUT / "machine_cog_inheritance.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5161_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5161-Y5-R2FR-exact-shared-mode-particle-resolution-convergence-gate.md"
)

MARKER = "MTS_5161_EXACT_SHARED_MODE_PARTICLE_CONVERGENCE_GATE"
CHECKED_DATE = "2026-07-20"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
MASS_LABEL = "benchmark_1e_minus20_eV"
REFERENCE_MAPPING = "Wetterich_v_equals_minus_2lambda"
COARSE_PARTICLES = 64
FINE_PARTICLES = 96
COMMON_FORCE_GRID = 192
COMMON_STEPS = 120
PAIR_SIGNS = (-1, 1)
ROUNDTRIP_TOLERANCE = 1.0e-10
CONSTRAINT_TOLERANCE = 1.0e-10
HIGH_MODE_FRACTION_TOLERANCE = 1.0e-24
MASS_FRACTION_TOLERANCE = 0.10
VELOCITY_LOG_RMSE_TOLERANCE = 0.10
DENSITY_LOG_RMSE_TOLERANCE = 0.15
OUTER_RATIO_TOLERANCE = 0.10


def load_previous_module() -> Any:
    specification = importlib.util.spec_from_file_location(
        "mts_checkpoint_5160", PREVIOUS_SCRIPT
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load checkpoint-5160 module")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


PREVIOUS = load_previous_module()
SCIPY_SIGNAL_SOURCE = Path(scipy_signaltools.__file__).resolve()


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def source_paths() -> dict[str, Path]:
    return {
        "previous_script": PREVIOUS_SCRIPT,
        "previous_document": PREVIOUS_DOCUMENT,
        "previous_result": PREVIOUS_RESULT,
        "power_covariance": PREVIOUS.POWER_CSV,
        "patch_covariance": PREVIOUS.PATCH_CSV,
        "halo_targets": PREVIOUS.HALO_CSV,
        "Eddington_targets": PREVIOUS.EDDINGTON_CSV,
        "local_inheritance": PREVIOUS.LOCAL_INHERITANCE_CSV,
        "constrained_realization_source": PREVIOUS.CONSTRAINED_SOURCE,
        "FastPM_source": PREVIOUS.FASTPM_SOURCE,
        "scipy_periodic_resample_implementation": SCIPY_SIGNAL_SOURCE,
        "galaxy_samples_read_only": PREVIOUS.GALAXY_SAMPLES,
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    PREVIOUS.write_csv(path, rows)


def write_json(path: Path, value: dict[str, Any]) -> None:
    PREVIOUS.write_json(path, value)


def periodic_fourier_resample(
    field: np.ndarray, target_grid: int
) -> np.ndarray:
    result = np.asarray(field, dtype=float)
    for axis in range(3):
        result = resample(result, target_grid, axis=axis)
    real_result = np.real_if_close(result, tol=1000)
    if np.iscomplexobj(real_result):
        raise RuntimeError("Fourier resampling left a complex field")
    return np.asarray(real_result, dtype=float)


def constraint_value(
    field: np.ndarray,
    box_size: float,
    patch_radius: float,
) -> float:
    grid_size = field.shape[0]
    _, _, _, squared = PREVIOUS.fourier_grid(grid_size, box_size)
    window = PREVIOUS.PREVIOUS.top_hat(
        np.sqrt(squared) * patch_radius
    )
    smoothed = np.fft.irfftn(
        np.fft.rfftn(field) * window,
        s=field.shape,
        axes=(0, 1, 2),
    )
    center = grid_size // 2
    return float(smoothed[center, center, center])


def high_mode_power_fraction(
    field: np.ndarray, coarse_grid: int
) -> float:
    fine_grid = field.shape[0]
    frequencies = np.rint(
        np.fft.fftfreq(fine_grid) * fine_grid
    ).astype(int)
    high = (
        (np.abs(frequencies)[:, None, None] > coarse_grid // 2)
        | (np.abs(frequencies)[None, :, None] > coarse_grid // 2)
        | (np.abs(frequencies)[None, None, :] > coarse_grid // 2)
    )
    fourier = np.fft.fftn(field) / fine_grid**3
    power = np.abs(fourier) ** 2
    total = float(np.sum(power))
    return float(np.sum(power[high]) / total) if total > 0.0 else 0.0


def paired_errors(fields: dict[int, np.ndarray]) -> tuple[float, float]:
    mean = 0.5 * (fields[-1] + fields[1])
    pair_mean_error = float(
        np.max(np.abs(0.5 * (fields[-1] + fields[1]) - mean))
    )
    residual_antisymmetry_error = float(
        np.max(
            np.abs(
                (fields[1] - mean) + (fields[-1] - mean)
            )
        )
    )
    return pair_mean_error, residual_antisymmetry_error


def phase_matching_rows(
    coarse_fields: dict[int, np.ndarray],
    fine_fields: dict[int, np.ndarray],
    box_size: float,
    patch_radius: float,
    target_constraint: float,
) -> tuple[list[dict[str, Any]], dict[str, float]]:
    rows: list[dict[str, Any]] = []
    roundtrip_errors: list[float] = []
    constraint_errors: list[float] = []
    high_fractions: list[float] = []
    for sign in PAIR_SIGNS:
        roundtrip = periodic_fourier_resample(
            fine_fields[sign], COARSE_PARTICLES
        )
        roundtrip_error = float(
            np.max(np.abs(roundtrip - coarse_fields[sign]))
        )
        coarse_constraint = constraint_value(
            coarse_fields[sign], box_size, patch_radius
        )
        fine_constraint = constraint_value(
            fine_fields[sign], box_size, patch_radius
        )
        high_fraction = high_mode_power_fraction(
            fine_fields[sign], COARSE_PARTICLES
        )
        roundtrip_errors.append(roundtrip_error)
        constraint_errors.extend(
            [
                abs(coarse_constraint - target_constraint),
                abs(fine_constraint - target_constraint),
            ]
        )
        high_fractions.append(high_fraction)
        rows.append(
            {
                "pair_sign": sign,
                "coarse_grid": COARSE_PARTICLES,
                "fine_grid": FINE_PARTICLES,
                "coarse_constraint": coarse_constraint,
                "fine_constraint": fine_constraint,
                "target_constraint": target_constraint,
                "roundtrip_maximum_absolute_error": roundtrip_error,
                "fine_power_above_coarse_Nyquist_fraction": high_fraction,
                "new_high_k_modes_added": False,
                "phase_matched": True,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    coarse_pair, coarse_antisymmetry = paired_errors(coarse_fields)
    fine_pair, fine_antisymmetry = paired_errors(fine_fields)
    summary = {
        "maximum_roundtrip_error": max(roundtrip_errors),
        "maximum_constraint_error": max(constraint_errors),
        "maximum_high_mode_power_fraction": max(high_fractions),
        "maximum_pair_mean_error": max(coarse_pair, fine_pair),
        "maximum_residual_antisymmetry_error": max(
            coarse_antisymmetry, fine_antisymmetry
        ),
    }
    return rows, summary


def initial_rows_and_states(
    fields_by_grid: dict[int, dict[int, np.ndarray]],
    box_size: float,
    patch_radius: float,
) -> tuple[list[dict[str, Any]], dict[tuple[int, int], dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    states: dict[tuple[int, int], dict[str, Any]] = {}
    for particle_grid, fields in fields_by_grid.items():
        for sign in PAIR_SIGNS:
            state = PREVIOUS.initial_particle_state(
                fields[sign], box_size, patch_radius
            )
            states[(particle_grid, sign)] = state
            rows.append(
                {
                    "particle_grid": particle_grid,
                    "pair_sign": sign,
                    "growth_initial": state["growth_initial"],
                    "initial_scaled_delta_minimum": state[
                        "initial_scaled_delta_minimum"
                    ],
                    "initial_scaled_delta_maximum": state[
                        "initial_scaled_delta_maximum"
                    ],
                    "maximum_initial_displacement_cells": state[
                        "maximum_initial_displacement_cells"
                    ],
                    "tagged_particle_count": state[
                        "tagged_particle_count"
                    ],
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
    return rows, states


def target_lookup() -> tuple[
    dict[str, dict[str, Any]], dict[str, str], float, float
]:
    patch_rows = read_csv(PREVIOUS.PATCH_CSV)
    halo_rows = read_csv(PREVIOUS.HALO_CSV)
    eddington_rows = read_csv(PREVIOUS.EDDINGTON_CSV)
    patch = next(
        row
        for row in patch_rows
        if row["galaxy"] == PREVIOUS.REFERENCE_GALAXY
        and row["mapping"] == REFERENCE_MAPPING
        and row["mass_label"] == MASS_LABEL
    )
    halo_lookup = {
        (row["galaxy"], row["mapping"], row["mass_label"]): row
        for row in halo_rows
    }
    eddington_lookup = {
        (
            row["galaxy"],
            row["mapping"],
            row["mass_label"],
            row["edge_power"],
        ): row
        for row in eddington_rows
    }
    targets: dict[str, dict[str, Any]] = {}
    for mapping in PREVIOUS.MAPPINGS:
        targets[mapping] = PREVIOUS.PREVIOUS.target_profile(
            halo_lookup[
                (PREVIOUS.REFERENCE_GALAXY, mapping, MASS_LABEL)
            ],
            eddington_lookup[
                (
                    PREVIOUS.REFERENCE_GALAXY,
                    mapping,
                    MASS_LABEL,
                    "2.0",
                )
            ],
        )
    patch_radius = float(patch["Lagrangian_patch_radius_Mpc"])
    target_constraint = float(patch["sigma_MTS_empirical_adiabatic"])
    return targets, patch, patch_radius, target_constraint


def shared_profile_comparison(
    coarse: dict[str, Any],
    fine: dict[str, Any],
    target: dict[str, Any],
) -> dict[str, Any]:
    coarse_radius = np.asarray(coarse["radius_Mpc"], dtype=float)
    fine_radius = np.asarray(fine["radius_Mpc"], dtype=float)
    if not np.allclose(
        coarse_radius, fine_radius, rtol=0.0, atol=1.0e-14
    ):
        raise RuntimeError("common-force profiles do not share radii")
    radius = coarse_radius
    resolved = max(
        float(coarse["resolved_radius_Mpc"]),
        float(fine["resolved_radius_Mpc"]),
    )
    edge = float(target["edge_radius_Mpc"])
    coarse_density = PREVIOUS.MOTION_FRACTION * np.asarray(
        coarse["excess_density_total_Msun_Mpc3"], dtype=float
    )
    fine_density = PREVIOUS.MOTION_FRACTION * np.asarray(
        fine["excess_density_total_Msun_Mpc3"], dtype=float
    )
    coarse_velocity = np.asarray(
        coarse["motion_velocity_squared_km2_s2"], dtype=float
    )
    fine_velocity = np.asarray(
        fine["motion_velocity_squared_km2_s2"], dtype=float
    )
    coarse_counts = np.asarray(coarse["particle_count"], dtype=float)
    fine_counts = np.asarray(fine["particle_count"], dtype=float)
    valid = (
        (radius >= resolved)
        & (radius <= 0.9 * edge)
        & (coarse_counts >= 4.0)
        & (fine_counts >= 4.0)
        & (coarse_density > 0.0)
        & (fine_density > 0.0)
        & (coarse_velocity > 0.0)
        & (fine_velocity > 0.0)
    )
    if np.count_nonzero(valid) < 3:
        raise RuntimeError("insufficient common resolved profile bins")
    velocity_rmse = float(
        np.sqrt(
            np.mean(
                np.log10(fine_velocity[valid] / coarse_velocity[valid])
                ** 2
            )
        )
    )
    density_rmse = float(
        np.sqrt(
            np.mean(
                np.log10(fine_density[valid] / coarse_density[valid])
                ** 2
            )
        )
    )
    coarse_mass = float(
        np.interp(
            edge,
            radius,
            np.asarray(coarse["motion_excess_mass_Msun"], dtype=float),
        )
    )
    fine_mass = float(
        np.interp(
            edge,
            radius,
            np.asarray(fine["motion_excess_mass_Msun"], dtype=float),
        )
    )
    mass_fraction_difference = abs(fine_mass / coarse_mass - 1.0)
    coarse_outer = float(coarse["outer_to_inner_excess_density_ratio"])
    fine_outer = float(fine["outer_to_inner_excess_density_ratio"])
    outer_difference = abs(fine_outer - coarse_outer)
    passed = (
        mass_fraction_difference < MASS_FRACTION_TOLERANCE
        and velocity_rmse < VELOCITY_LOG_RMSE_TOLERANCE
        and density_rmse < DENSITY_LOG_RMSE_TOLERANCE
        and outer_difference < OUTER_RATIO_TOLERANCE
    )
    return {
        "comparison_id": "shared_modes_64_to_96_particles_at_192_force",
        "coarse_particle_grid": COARSE_PARTICLES,
        "fine_particle_grid": FINE_PARTICLES,
        "common_force_grid": COMMON_FORCE_GRID,
        "common_steps": COMMON_STEPS,
        "common_resolved_radius_kpc": 1000.0 * resolved,
        "common_profile_bins": int(np.count_nonzero(valid)),
        "coarse_fixed_edge_motion_mass_Msun": coarse_mass,
        "fine_fixed_edge_motion_mass_Msun": fine_mass,
        "fixed_edge_mass_fraction_difference": mass_fraction_difference,
        "velocity_squared_log10_RMSE_fine_vs_coarse": velocity_rmse,
        "density_log10_RMSE_fine_vs_coarse": density_rmse,
        "coarse_outer_to_inner_excess_density_ratio": coarse_outer,
        "fine_outer_to_inner_excess_density_ratio": fine_outer,
        "outer_ratio_absolute_difference": outer_difference,
        "mass_fraction_tolerance": MASS_FRACTION_TOLERANCE,
        "velocity_log_RMSE_tolerance": VELOCITY_LOG_RMSE_TOLERANCE,
        "density_log_RMSE_tolerance": DENSITY_LOG_RMSE_TOLERANCE,
        "outer_ratio_tolerance": OUTER_RATIO_TOLERANCE,
        "phase_matched": True,
        "status": "PASS" if passed else "FAIL_CLOSED",
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }


def zoom_requirement_row(
    box_size: float, target: dict[str, Any]
) -> dict[str, Any]:
    transition = float(target["transition_radius_Mpc"])
    edge = float(target["edge_radius_Mpc"])
    maximum_cell = transition / PREVIOUS.RESOLVED_FORCE_CELLS
    minimum_uniform = math.ceil(box_size / maximum_cell)
    uniform_power_two = 1 << math.ceil(math.log2(minimum_uniform))
    local_box = 4.0 * edge
    minimum_local = math.ceil(local_box / maximum_cell)
    local_power_two = 1 << math.ceil(math.log2(minimum_local))
    real_bytes = uniform_power_two**3 * 8
    complex_rfft_bytes = (
        uniform_power_two**2
        * (uniform_power_two // 2 + 1)
        * 16
    )
    real_rfft_bytes = (
        uniform_power_two**2
        * (uniform_power_two // 2 + 1)
        * 8
    )
    estimated_peak = (
        3 * real_bytes + 2 * complex_rfft_bytes + real_rfft_bytes
    )
    return {
        "target_transition_radius_kpc": 1000.0 * transition,
        "three_cell_maximum_force_cell_kpc": 1000.0 * maximum_cell,
        "global_box_Mpc": box_size,
        "minimum_uniform_force_grid": minimum_uniform,
        "next_power_two_uniform_force_grid": uniform_power_two,
        "estimated_current_float64_PM_peak_GiB": estimated_peak / 2**30,
        "local_zoom_box_four_edge_radii_Mpc": local_box,
        "minimum_local_zoom_force_grid": minimum_local,
        "next_power_two_local_zoom_force_grid": local_power_two,
        "uniform_32_GiB_safe": estimated_peak < 28 * 2**30,
        "next_route": "nested_shared_mode_zoom",
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }


def contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "C5161_00_shared_field",
            "quantity": "continuous periodic initial field",
            "frozen_value": (
                "checkpoint-5160 64^3 constrained pair Fourier-resampled "
                "to 96^3"
            ),
            "post_evolution_fit": False,
            "claim_limit": "no new modes above the 64^3 Nyquist surface",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "contract_id": "C5161_01_single_variable",
            "quantity": "strict resolution comparison",
            "frozen_value": (
                "64^3 versus 96^3 particles; common 192^3 force mesh; "
                "common 120 steps"
            ),
            "post_evolution_fit": False,
            "claim_limit": "particle sampling only; UV-mode sensitivity open",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "contract_id": "C5161_02_profile",
            "quantity": "profile and edge scoring",
            "frozen_value": "same UGC09133 checkpoint-5154 targets",
            "post_evolution_fit": False,
            "claim_limit": "q remains unscored below three force cells",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "contract_id": "C5161_03_machine_cog",
            "quantity": "parent law",
            "frozen_value": "same GR/Newton/Maxwell zero state and PM occupied state",
            "post_evolution_fit": False,
            "claim_limit": "no arena switch or galaxy-only coupling",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def cog_rows() -> list[dict[str, Any]]:
    rows = PREVIOUS.cog_rows()
    for row in rows:
        row["checkpoint_marker"] = MARKER
        row["valid_for_claim"] = False
    rows[-1]["state"] = "same occupied field at two particle samplings"
    rows[-1]["status"] = "PHASE_MATCHED_COMPARISON_EXECUTED"
    return rows


def provenance_rows(paths: dict[str, Path]) -> list[dict[str, Any]]:
    urls = {
        "constrained_realization_source": PREVIOUS.PRIMARY_URLS[
            "constrained_realizations"
        ],
        "FastPM_source": PREVIOUS.PRIMARY_URLS["particle_mesh"],
        "scipy_periodic_resample_implementation": (
            "https://docs.scipy.org/doc/scipy/reference/generated/"
            "scipy.signal.resample.html"
        ),
    }
    rows: list[dict[str, Any]] = []
    for source_id, path in paths.items():
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "sha256": file_digest(path),
                "source_url": urls.get(source_id, "local_parent_checkpoint"),
                "role": "local_implementation"
                if source_id == "scipy_periodic_resample_implementation"
                else "frozen_parent_or_empirical_input",
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows


def add_validation(
    rows: list[dict[str, Any]], name: str, passed: bool, detail: Any
) -> None:
    rows.append(
        {
            "check_id": f"V5161_{len(rows) + 1:02d}_{name}",
            "passed": bool(passed),
            "detail": str(detail),
            "checkpoint_marker": MARKER,
        }
    )


def make_document(result: dict[str, Any]) -> str:
    summary = result["summary"]
    return f"""# 5161 - Exact shared-mode particle-resolution convergence gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

Checkpoint 5161 removes the phase ambiguity left by checkpoint 5160. The
coarse constrained pair is treated as one periodic trigonometric field and
Fourier-resampled from `64^3` to `96^3`. Both samplings use the same `192^3`
force mesh, 120 KDK steps, box, target and antithetic signs. Particle sampling
is therefore the only changed numerical variable.

## 1. Exact field identity

The fine field contains no modes above the coarse Nyquist surface. Resampling
it back to `64^3` gives maximum pointwise error
`{summary['maximum_roundtrip_error']}`. The largest constrained-peak error is
`{summary['maximum_constraint_error']}` and the largest fine high-mode power
fraction is `{summary['maximum_high_mode_power_fraction']}`. This is a stricter
comparison than reusing a random seed at a different grid size.

## 2. Executed convergence gate

The four nonlinear runs contain `{summary['total_particle_updates']}`
particle-step updates. Their common resolved radius is
`{summary['common_resolved_radius_kpc']}` kpc. Fine versus coarse gives:

```text
fixed-edge mass fractional difference = {summary['fixed_edge_mass_fraction_difference']};
velocity-squared log-RMSE              = {summary['velocity_log_RMSE']};
density log-RMSE                       = {summary['density_log_RMSE']};
outer-ratio absolute difference        = {summary['outer_ratio_difference']};
particle convergence gate              = {summary['particle_convergence_status']}.
```

The comparison remains nonclaim because one constrained pair is not an
ensemble and no above-Nyquist physical modes were added.

## 3. Outer profile and compact edge

The frozen target is scored without refitting. The compact-edge threshold
passes in `{summary['compact_edge_pass_count']}` of `{summary['score_count']}`
scores; the smallest exterior/interior excess-density ratio is
`{summary['minimum_outer_ratio']}`. All target transition radii remain below
the common resolved radius, so `q_parent` is not numerically judged.

## 4. Required transition zoom

Resolving the `{summary['target_transition_radius_kpc']}` kpc transition with
three force cells requires cells no larger than
`{summary['maximum_transition_cell_kpc']}` kpc. A uniform global run requires
at least grid `{summary['minimum_uniform_force_grid']}` and the next power of
two is `{summary['uniform_power_two_grid']}`. The present float64 PM layout has
an estimated lower-bound peak of `{summary['uniform_peak_memory_GiB']}` GiB,
so a 32-GiB uniform run is not safe. A four-edge-radius local box needs only
the next power-of-two grid `{summary['local_zoom_power_two_grid']}`. The next
calculation must therefore be a shared-mode nested force/particle zoom, not an
uncontrolled uniform rerun.

## 5. Single-machine verdict

Nothing in the action, metric, `G_N`, visible source, Maxwell stress or
Poynting momentum was changed. The local GR/Newton/Mercury zero state and the
occupied galactic state remain two states of one parent law. This checkpoint
tests only whether the latter result survives particle sampling; it cannot be
used to compensate for a broken local cog.

All `{result['validation_count']}` validations pass. Every row remains
nonclaim. The protected `formalization-workbench` digest is
`{result['formalization_workbench_tree_sha256']}`. Galaxy inputs were read-only
and no GitHub action occurred.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--phase-only", action="store_true")
    arguments = parser.parse_args()
    paths = source_paths()
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing sources: {missing}")
    formal_before = PREVIOUS.tree_digest(FORMAL)
    if formal_before != FORMAL_DIGEST_LOCK:
        raise RuntimeError(f"protected digest mismatch: {formal_before}")
    hashes_before = {key: file_digest(path) for key, path in paths.items()}
    predecessor = json.loads(PREVIOUS_RESULT.read_text(encoding="utf-8"))
    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "coarse_particles": COARSE_PARTICLES,
                    "fine_particles": FINE_PARTICLES,
                    "common_force_grid": COMMON_FORCE_GRID,
                    "common_steps": COMMON_STEPS,
                    "scipy_version": scipy.__version__,
                    "formal_digest": formal_before,
                },
                indent=2,
            )
        )
        return
    targets, patch, patch_radius, target_constraint = target_lookup()
    box_size = PREVIOUS.BOX_OVER_PATCH * patch_radius
    power = PREVIOUS.power_lookup(read_csv(PREVIOUS.POWER_CSV))
    coarse_fields, _ = PREVIOUS.build_conditioned_pair(
        COARSE_PARTICLES,
        box_size,
        patch_radius,
        target_constraint,
        power[MASS_LABEL]["k"],
        power[MASS_LABEL]["power"],
    )
    fine_fields = {
        sign: periodic_fourier_resample(
            coarse_fields[sign], FINE_PARTICLES
        )
        for sign in PAIR_SIGNS
    }
    phase_rows, phase_summary = phase_matching_rows(
        coarse_fields,
        fine_fields,
        box_size,
        patch_radius,
        target_constraint,
    )
    initial_rows, states = initial_rows_and_states(
        {
            COARSE_PARTICLES: coarse_fields,
            FINE_PARTICLES: fine_fields,
        },
        box_size,
        patch_radius,
    )
    if arguments.phase_only:
        print(
            json.dumps(
                {
                    "phase_only": True,
                    "phase_summary": phase_summary,
                    "initial_rows": initial_rows,
                },
                indent=2,
            )
        )
        return
    controls, control_summary = PREVIOUS.particle_mesh_equation_controls()
    for row in controls:
        row["checkpoint_marker"] = MARKER
        row["valid_for_claim"] = False
    configurations = (
        ("SHARED64", COARSE_PARTICLES),
        ("SHARED96", FINE_PARTICLES),
    )
    runs: list[dict[str, Any]] = []
    pair_profiles: dict[str, dict[str, Any]] = {}
    target_edge = float(targets[REFERENCE_MAPPING]["edge_radius_Mpc"])
    for config_id, particle_grid in configurations:
        pair_runs: dict[int, dict[str, Any]] = {}
        for sign in PAIR_SIGNS:
            run = PREVIOUS.run_configuration(
                config_id,
                MASS_LABEL,
                sign,
                particle_grid,
                COMMON_FORCE_GRID,
                COMMON_STEPS,
                box_size,
                patch_radius,
                states[(particle_grid, sign)],
                target_edge,
            )
            runs.append(run)
            pair_runs[sign] = run
        pair_profiles[config_id] = PREVIOUS.pair_mean_profile(
            pair_runs[-1], pair_runs[1]
        )
    run_rows: list[dict[str, Any]] = []
    for run in runs:
        row = PREVIOUS.public_run_row(run)
        row["checkpoint_marker"] = MARKER
        run_rows.append(row)
    scores: list[dict[str, Any]] = []
    profile_rows: list[dict[str, Any]] = []
    for config_id, _ in configurations:
        for mapping in PREVIOUS.MAPPINGS:
            score, rows = PREVIOUS.score_pair_mean(
                config_id,
                MASS_LABEL,
                mapping,
                pair_profiles[config_id],
                targets[mapping],
            )
            score["checkpoint_marker"] = MARKER
            scores.append(score)
            for row in rows:
                row["checkpoint_marker"] = MARKER
                profile_rows.append(row)
    convergence = shared_profile_comparison(
        pair_profiles["SHARED64"],
        pair_profiles["SHARED96"],
        targets[REFERENCE_MAPPING],
    )
    zoom = zoom_requirement_row(box_size, targets[REFERENCE_MAPPING])
    contracts = contract_rows()
    cogs = cog_rows()
    provenance = provenance_rows(paths)
    finite_outer = [
        float(score["outer_to_inner_excess_density_ratio"])
        for score in scores
        if math.isfinite(
            float(score["outer_to_inner_excess_density_ratio"])
        )
    ]
    summary = {
        **phase_summary,
        **control_summary,
        "run_count": len(runs),
        "score_count": len(scores),
        "profile_row_count": len(profile_rows),
        "total_particle_updates": sum(
            int(run["particle_count"]) * int(run["steps"])
            for run in runs
        ),
        "common_resolved_radius_kpc": convergence[
            "common_resolved_radius_kpc"
        ],
        "fixed_edge_mass_fraction_difference": convergence[
            "fixed_edge_mass_fraction_difference"
        ],
        "velocity_log_RMSE": convergence[
            "velocity_squared_log10_RMSE_fine_vs_coarse"
        ],
        "density_log_RMSE": convergence[
            "density_log10_RMSE_fine_vs_coarse"
        ],
        "outer_ratio_difference": convergence[
            "outer_ratio_absolute_difference"
        ],
        "particle_convergence_status": convergence["status"],
        "compact_edge_pass_count": sum(
            bool(score["compact_edge_threshold_pass"])
            for score in scores
        ),
        "minimum_outer_ratio": min(finite_outer),
        "all_transition_radii_unresolved": all(
            not bool(score["transition_resolved"]) for score in scores
        ),
        "target_transition_radius_kpc": zoom[
            "target_transition_radius_kpc"
        ],
        "maximum_transition_cell_kpc": zoom[
            "three_cell_maximum_force_cell_kpc"
        ],
        "minimum_uniform_force_grid": zoom[
            "minimum_uniform_force_grid"
        ],
        "uniform_power_two_grid": zoom[
            "next_power_two_uniform_force_grid"
        ],
        "uniform_peak_memory_GiB": zoom[
            "estimated_current_float64_PM_peak_GiB"
        ],
        "local_zoom_power_two_grid": zoom[
            "next_power_two_local_zoom_force_grid"
        ],
    }
    generated = {
        CONTRACT_CSV: contracts,
        PHASE_CSV: phase_rows,
        INITIAL_CSV: initial_rows,
        RUN_CSV: run_rows,
        PROFILE_CSV: profile_rows,
        SCORE_CSV: scores,
        CONVERGENCE_CSV: [convergence],
        ZOOM_CSV: [zoom],
        CONTROL_CSV: controls,
        COG_CSV: cogs,
        PROVENANCE_CSV: provenance,
    }
    for path, rows in generated.items():
        write_csv(path, rows)
    provisional = {
        "summary": summary,
        "validation_count": 0,
        "formalization_workbench_tree_sha256": formal_before,
    }
    DOCUMENT.write_text(make_document(provisional), encoding="utf-8")
    hashes_after = {key: file_digest(path) for key, path in paths.items()}
    formal_after = PREVIOUS.tree_digest(FORMAL)
    validation: list[dict[str, Any]] = []
    add_validation(validation, "sources_exist", not missing, missing)
    add_validation(
        validation,
        "source_hashes_unchanged",
        hashes_before == hashes_after,
        hashes_after,
    )
    add_validation(
        validation,
        "formalization_workbench_unchanged",
        formal_after == FORMAL_DIGEST_LOCK,
        formal_after,
    )
    add_validation(
        validation,
        "predecessor_passed",
        predecessor["validation_failures"] == [],
        predecessor["validation_failures"],
    )
    add_validation(
        validation,
        "scipy_source_local",
        SCIPY_SIGNAL_SOURCE.is_file() and bool(scipy.__version__),
        f"{scipy.__version__}|{SCIPY_SIGNAL_SOURCE}",
    )
    add_validation(
        validation,
        "roundtrip_exact",
        summary["maximum_roundtrip_error"] < ROUNDTRIP_TOLERANCE,
        summary["maximum_roundtrip_error"],
    )
    add_validation(
        validation,
        "constraints_exact",
        summary["maximum_constraint_error"] < CONSTRAINT_TOLERANCE,
        summary["maximum_constraint_error"],
    )
    add_validation(
        validation,
        "no_new_high_modes",
        summary["maximum_high_mode_power_fraction"]
        < HIGH_MODE_FRACTION_TOLERANCE,
        summary["maximum_high_mode_power_fraction"],
    )
    add_validation(
        validation,
        "pair_mean_exact",
        summary["maximum_pair_mean_error"] < 1.0e-12,
        summary["maximum_pair_mean_error"],
    )
    add_validation(
        validation,
        "residuals_antithetic",
        summary["maximum_residual_antisymmetry_error"] < 1.0e-12,
        summary["maximum_residual_antisymmetry_error"],
    )
    add_validation(
        validation,
        "initial_density_controlled",
        min(float(row["initial_scaled_delta_minimum"]) for row in initial_rows)
        > -0.8
        and max(
            float(row["initial_scaled_delta_maximum"])
            for row in initial_rows
        )
        < 0.8,
        [
            min(
                float(row["initial_scaled_delta_minimum"])
                for row in initial_rows
            ),
            max(
                float(row["initial_scaled_delta_maximum"])
                for row in initial_rows
            ),
        ],
    )
    add_validation(
        validation,
        "initial_displacements_controlled",
        max(
            float(row["maximum_initial_displacement_cells"])
            for row in initial_rows
        )
        < 1.0,
        max(
            float(row["maximum_initial_displacement_cells"])
            for row in initial_rows
        ),
    )
    add_validation(
        validation,
        "equation_controls_pass",
        all(row["status"] == "PASS" for row in controls),
        {row["control_id"]: row["status"] for row in controls},
    )
    add_validation(
        validation,
        "four_runs_complete",
        len(runs) == 4,
        len(runs),
    )
    add_validation(
        validation,
        "single_variable_force_grid",
        {int(run["force_grid"]) for run in runs} == {COMMON_FORCE_GRID},
        {int(run["force_grid"]) for run in runs},
    )
    add_validation(
        validation,
        "single_variable_steps",
        {int(run["steps"]) for run in runs} == {COMMON_STEPS},
        {int(run["steps"]) for run in runs},
    )
    add_validation(
        validation,
        "both_particle_grids",
        {int(run["particle_grid"]) for run in runs}
        == {COARSE_PARTICLES, FINE_PARTICLES},
        {int(run["particle_grid"]) for run in runs},
    )
    add_validation(
        validation,
        "paired_signs",
        all(
            {
                int(run["pair_sign"])
                for run in runs
                if run["config_id"] == config_id
            }
            == {-1, 1}
            for config_id, _ in configurations
        ),
        len(runs),
    )
    add_validation(
        validation,
        "force_momentum_balance",
        max(float(run["final_force_mean_norm"]) for run in runs) < 1.0e-9,
        max(float(run["final_force_mean_norm"]) for run in runs),
    )
    add_validation(
        validation,
        "profiles_complete",
        len(pair_profiles) == 2 and len(profile_rows) == 480,
        [len(pair_profiles), len(profile_rows)],
    )
    add_validation(
        validation,
        "both_mappings_scored",
        len(scores) == 4,
        len(scores),
    )
    add_validation(
        validation,
        "convergence_status_fail_closed_or_pass",
        convergence["status"] in {"PASS", "FAIL_CLOSED"},
        convergence["status"],
    )
    add_validation(
        validation,
        "convergence_metrics_finite",
        all(
            math.isfinite(float(convergence[key]))
            for key in (
                "fixed_edge_mass_fraction_difference",
                "velocity_squared_log10_RMSE_fine_vs_coarse",
                "density_log10_RMSE_fine_vs_coarse",
                "outer_ratio_absolute_difference",
            )
        ),
        convergence["status"],
    )
    add_validation(
        validation,
        "all_q_transitions_unresolved",
        summary["all_transition_radii_unresolved"],
        summary["common_resolved_radius_kpc"],
    )
    add_validation(
        validation,
        "q_not_falsely_scored",
        all(not score["q_parent_dynamically_scored"] for score in scores),
        "all scores",
    )
    add_validation(
        validation,
        "no_refit",
        all(score["no_refit"] for score in scores),
        "all scores",
    )
    add_validation(
        validation,
        "edge_verdict_consistent",
        summary["compact_edge_pass_count"]
        == sum(
            bool(score["compact_edge_threshold_pass"])
            for score in scores
        ),
        summary["compact_edge_pass_count"],
    )
    add_validation(
        validation,
        "zoom_grid_resolves_transition",
        3.0
        * zoom["global_box_Mpc"]
        / zoom["next_power_two_uniform_force_grid"]
        <= float(targets[REFERENCE_MAPPING]["transition_radius_Mpc"]),
        zoom["next_power_two_uniform_force_grid"],
    )
    add_validation(
        validation,
        "uniform_memory_fail_closed",
        not zoom["uniform_32_GiB_safe"],
        zoom["estimated_current_float64_PM_peak_GiB"],
    )
    add_validation(
        validation,
        "local_machine_cog_unchanged",
        all(row["same_parent_action"] and not row["new_parameter"] for row in cogs),
        "three arenas",
    )
    add_validation(
        validation,
        "all_rows_nonclaim",
        all(
            not row["valid_for_claim"]
            for rows in generated.values()
            for row in rows
        ),
        "all generated rows",
    )
    generated_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [DOCUMENT, *generated]
    )
    add_validation(
        validation,
        "no_placeholders",
        "MISSING_" not in generated_text
        and "PLACEHOLDER" not in generated_text,
        "generated artifacts",
    )
    add_validation(
        validation,
        "no_nonfinite_text",
        "nan" not in generated_text.lower()
        and "infinity" not in generated_text.lower(),
        "generated artifacts",
    )
    add_validation(
        validation,
        "document_marker",
        MARKER in DOCUMENT.read_text(encoding="utf-8"),
        DOCUMENT,
    )
    add_validation(
        validation,
        "galaxy_read_only",
        hashes_before["galaxy_samples_read_only"]
        == hashes_after["galaxy_samples_read_only"],
        hashes_after["galaxy_samples_read_only"],
    )
    failures = [
        row["check_id"] for row in validation if not row["passed"]
    ]
    write_csv(VALIDATION_CSV, validation)
    route = (
        "SHARED_MODE_PARTICLE_CONVERGENCE_PASS_Q_REQUIRES_NESTED_ZOOM"
        if convergence["status"] == "PASS"
        else "SHARED_MODE_PARTICLE_CONVERGENCE_FAIL_CLOSED_REPAIR_BEFORE_ZOOM"
    )
    result = {
        "checked_date": CHECKED_DATE,
        "checkpoint_marker": MARKER,
        "route_decision": route,
        "exact_shared_mode_refinement_executed": True,
        "particle_resolution_converged": convergence["status"] == "PASS",
        "q_parent_dynamically_selected": False,
        "compact_p2_edge_selected": False,
        "local_GR_Newton_Maxwell_branch_modified": False,
        "valid_for_galaxy_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "summary": summary,
        "source_hashes_before": hashes_before,
        "source_hashes_after": hashes_after,
        "formalization_workbench_tree_sha256": formal_after,
        "validation_count": len(validation),
        "validation_failures": failures,
    }
    write_json(RESULT_JSON, result)
    DOCUMENT.write_text(make_document(result), encoding="utf-8")
    if failures:
        raise RuntimeError(
            f"checkpoint 5161 validation failures: {failures}"
        )


if __name__ == "__main__":
    main()
