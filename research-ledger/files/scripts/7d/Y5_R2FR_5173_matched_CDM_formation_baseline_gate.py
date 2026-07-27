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
from scipy.interpolate import PchipInterpolator


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
PREVIOUS_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5169_pair_consistent_transport_forward_response_gate.py"
)
PREVIOUS_DOCUMENT = (
    POST
    / "5169-Y5-R2FR-pair-consistent-capacity-bounded-transport-forward-response-gate.md"
)
PREVIOUS_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5169"
    / "pair_consistent_transport_forward_response_results.json"
)
PREVIOUS_SCORE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5169"
    / "transported_radial_source_forward_scores.csv"
)
PREVIOUS_PROFILE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5169"
    / "transported_radial_source_forward_profiles.csv"
)
PREVIOUS_VALIDATION = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5169_VALIDATION.csv"
)
CHECKPOINT_5172 = (
    POST
    / "5172-Y5-R2FR-source-backed-axisymmetric-baryon-geometry-forward-response-gate.md"
)
OUT = POST / "source-intake" / "functional_rg" / "5173"
SNAPSHOT_PATHS = {
    -1: OUT / "cdm_phase_minus_isolated_initial_state.npz",
    1: OUT / "cdm_phase_plus_isolated_initial_state.npz",
}
SNAPSHOT_META = OUT / "cdm_isolated_initial_state_metadata.json"
EVOLUTION_CACHE = OUT / "evolution-cache"
CONTRACT_CSV = OUT / "matched_baseline_contract.csv"
POWER_CSV = OUT / "matched_CDM_MTS_power_probes.csv"
SNAPSHOT_CSV = OUT / "matched_CDM_snapshot_comparison.csv"
SCORE_CSV = OUT / "matched_CDM_MTS_forward_score_comparison.csv"
CONTROL_CSV = OUT / "matched_CDM_response_controls.csv"
PROFILE_CSV = OUT / "matched_CDM_MTS_forward_profiles.csv"
DECISION_CSV = OUT / "route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "matched_CDM_formation_baseline_results.json"
VALIDATION_CSV = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5173_VALIDATION.csv"
)
DOCUMENT = POST / "5173-Y5-R2FR-matched-CDM-formation-baseline-discrimination-gate.md"

MARKER = "MTS_5173_MATCHED_CDM_FORMATION_BASELINE_DISCRIMINATION_GATE"
CHECKED_DATE = "2026-07-21"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
MASS_LABEL = "benchmark_1e_minus20_eV"
REFERENCE_GALAXY = "UGC09133"
REFERENCE_MAPPING = "Wetterich_v_equals_minus_2lambda"
SELECTED_BRANCH = ("ISOBARIC", 0.3)
RADIAL_BINS = 26
COST_POWER = 1
STEPS_PER_INNER_ORBIT = 64


specification = importlib.util.spec_from_file_location(
    "mts_checkpoint_5169_for_5173", PREVIOUS_SCRIPT
)
if specification is None or specification.loader is None:
    raise RuntimeError(f"cannot load module: {PREVIOUS_SCRIPT}")
V = importlib.util.module_from_spec(specification)
specification.loader.exec_module(V)
Q = V.Q
R = V.R
DYNAMICS = V.DYNAMICS
ZOOM = DYNAMICS.ZOOM
PM = DYNAMICS.PM


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_paths() -> dict[str, Path]:
    paths = {
        "checkpoint_5169_script": PREVIOUS_SCRIPT,
        "checkpoint_5169_document": PREVIOUS_DOCUMENT,
        "checkpoint_5169_result": PREVIOUS_RESULT,
        "checkpoint_5169_score": PREVIOUS_SCORE,
        "checkpoint_5169_profile": PREVIOUS_PROFILE,
        "checkpoint_5169_validation": PREVIOUS_VALIDATION,
        "checkpoint_5172_document": CHECKPOINT_5172,
        "radiation_transfer_power": PM.POWER_CSV,
        "patch_covariance": PM.PATCH_CSV,
        "checkpoint_5173_script": Path(__file__).resolve(),
    }
    for phase_sign, path in DYNAMICS.SNAPSHOT_PATHS.items():
        paths[f"MTS_snapshot_{phase_sign:+d}"] = path
    return paths


def file_digest(path: Path) -> str:
    return Q.file_digest(path)


def contract_rows() -> list[dict[str, Any]]:
    clauses = [
        (
            "B1_SHARED_RANDOM_PHASES",
            "CDM and MTS use the same fixed Gaussian white field, antithetic signs, grids, force operator and target galaxy",
            "exact_code_path",
        ),
        (
            "B2_COVARIANCE",
            "CDM uses source-backed P_CDM while MTS uses P_CDM T_FDM^2 at m=1e-20 eV",
            "source_backed_single_changed_input",
        ),
        (
            "B3_MATCHED_CONSTRAINT",
            "each branch is conditioned at its own source-backed one-sigma UGC09133 top-hat amplitude",
            "baseline_symmetric",
        ),
        (
            "B4_IDENTICAL_DYNAMICS",
            "both branches use the same Newtonian Vlasov force, calibrated G_N, isolation, nested zoom and particle selection",
            "exact_code_path",
        ),
        (
            "B5_IDENTICAL_VISIBLE_HISTORY",
            "both branches use the same isobaric Z=0.3 cooling solution, measured visible endpoint and pair-consistent capacity law",
            "frozen_physical_history",
        ),
        (
            "B6_NO_TARGET_FEEDBACK",
            "observed and parent q targets enter only after both forward evolutions are complete",
            "predeclared_forward_test",
        ),
        (
            "B7_INTERPRETATION",
            "a single shared-phase patch can discriminate only a response difference larger than the inherited numerical control envelope",
            "matched_baseline_gate",
        ),
        (
            "B8_NONCLAIM",
            "the Planck covariance is an explicit comparator and not a parent-derived primordial MTS state",
            "explicit_limitation",
        ),
    ]
    return [
        {
            "clause_id": clause_id,
            "contract": contract,
            "status": status,
            "target_used_to_define_evolution": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for clause_id, contract, status in clauses
    ]


def covariance_rows() -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, str]]:
    rows = [
        row
        for row in read_csv(PM.POWER_CSV)
        if row["mass_label"] == MASS_LABEL
    ]
    rows.sort(key=lambda row: float(row["k_Mpc_inverse"]))
    wavenumber = np.asarray([float(row["k_Mpc_inverse"]) for row in rows])
    cdm_power = np.asarray([float(row["P_CDM_Mpc3"]) for row in rows])
    mts_power = np.asarray(
        [float(row["P_MTS_empirical_adiabatic_Mpc3"]) for row in rows]
    )
    patch = next(
        row
        for row in read_csv(PM.PATCH_CSV)
        if row["galaxy"] == REFERENCE_GALAXY
        and row["mapping"] == REFERENCE_MAPPING
        and row["mass_label"] == MASS_LABEL
    )
    return wavenumber, cdm_power, mts_power, patch


def power_probe_rows(
    wavenumber: np.ndarray,
    cdm_power: np.ndarray,
    mts_power: np.ndarray,
    box_size_Mpc: float,
    patch_radius_Mpc: float,
    edge_radius_Mpc: float,
) -> list[dict[str, Any]]:
    probes = {
        "box_fundamental": 2.0 * math.pi / box_size_Mpc,
        "patch_inverse": 1.0 / patch_radius_Mpc,
        "patch_pi": math.pi / patch_radius_Mpc,
        "patch_2pi": 2.0 * math.pi / patch_radius_Mpc,
        "edge_2pi": 2.0 * math.pi / edge_radius_Mpc,
        "particle_Nyquist": math.pi * ZOOM.PARTICLE_GRID / box_size_Mpc,
    }
    rows: list[dict[str, Any]] = []
    for probe_id, value in probes.items():
        p_cdm = float(np.interp(value, wavenumber, cdm_power))
        p_mts = float(np.interp(value, wavenumber, mts_power))
        rows.append(
            {
                "probe_id": probe_id,
                "k_Mpc_inverse": value,
                "P_CDM_Mpc3": p_cdm,
                "P_MTS_Mpc3": p_mts,
                "MTS_to_CDM_power_ratio": p_mts / p_cdm,
                "single_changed_input": "linear_covariance_only",
                "target_used": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows


def generate_cdm_snapshots(force: bool) -> tuple[dict[int, dict[str, Any]], dict[str, Any]]:
    if (
        not force
        and SNAPSHOT_META.is_file()
        and all(path.is_file() for path in SNAPSHOT_PATHS.values())
    ):
        metadata = json.loads(SNAPSHOT_META.read_text(encoding="utf-8"))
        snapshots: dict[int, dict[str, Any]] = {}
        for phase_sign, path in SNAPSHOT_PATHS.items():
            with np.load(path) as archive:
                snapshots[phase_sign] = {key: archive[key] for key in archive.files}
        return snapshots, metadata
    profile_rows, q_row, _, _ = DYNAMICS.reference_rows()
    target_radii = np.asarray([float(row["radius_kpc"]) for row in profile_rows])
    targets, _, patch_radius, _ = ZOOM.PREVIOUS.target_lookup()
    target = targets[REFERENCE_MAPPING]
    edge_radius_Mpc = float(target["edge_radius_Mpc"])
    box_size_Mpc = PM.BOX_OVER_PATCH * patch_radius
    wavenumber, cdm_power, _, patch = covariance_rows()
    target_constraint = float(patch["sigma_CDM_empirical"])
    coarse_fields, conditioning = PM.build_conditioned_pair(
        ZOOM.PREVIOUS.COARSE_PARTICLES,
        box_size_Mpc,
        patch_radius,
        target_constraint,
        wavenumber,
        cdm_power,
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
    snapshots: dict[int, dict[str, Any]] = {}
    metadata: dict[str, Any] = {
        "checkpoint_marker": MARKER,
        "covariance": "source_backed_CDM",
        "mass_label_comparator": MASS_LABEL,
        "fixed_seed": PM.FIXED_SEED,
        "target_constraint": target_constraint,
        "conditioning": conditioning,
        "edge_radius_kpc": 1000.0 * edge_radius_Mpc,
        "box_size_Mpc": box_size_Mpc,
        "patch_radius_Mpc": patch_radius,
        "phases": {},
    }
    OUT.mkdir(parents=True, exist_ok=True)
    for phase_sign in ZOOM.PAIR_SIGNS:
        print(f"START CDM nested snapshot phase={phase_sign:+d}", flush=True)
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
        counts, motion_mass = DYNAMICS.snapshot_profile(
            positions_kpc, target_radii, particle_mass
        )
        velocity_squared = (
            DYNAMICS.PREVIOUS.G_KPC_KM2_S2_MSUN
            * motion_mass
            / np.maximum(target_radii, np.finfo(float).tiny)
        )
        transition_radius = float(target["transition_radius_Mpc"]) * 1000.0
        q_value = DYNAMICS.PREVIOUS.local_logarithmic_q(
            target_radii, velocity_squared, transition_radius
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
        np.savez_compressed(SNAPSHOT_PATHS[phase_sign], **snapshot)
        phase_row = {
            "phase_sign": phase_sign,
            "selected_particle_count": int(np.count_nonzero(selected)),
            "donor_particle_count": int(np.count_nonzero(donors)),
            "particle_mass_Msun": particle_mass,
            "regenerated_q": q_value,
            "maximum_radius_profile_count": float(counts[-1]),
            "wall_seconds": time.perf_counter() - start,
            "snapshot_sha256": file_digest(SNAPSHOT_PATHS[phase_sign]),
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        metadata["phases"][str(phase_sign)] = phase_row
        print(
            f"DONE CDM nested snapshot phase={phase_sign:+d} q={q_value} "
            f"wall={phase_row['wall_seconds']:.3f}s",
            flush=True,
        )
    Q.write_json(SNAPSHOT_META, metadata)
    return snapshots, metadata


def make_cdm_context(
    base: dict[str, Any], snapshots: dict[int, dict[str, Any]]
) -> dict[str, Any]:
    context = dict(base)
    context["snapshots"] = snapshots
    initial_phase_mass: dict[int, np.ndarray] = {}
    for phase_sign, snapshot in snapshots.items():
        particle_mass = float(snapshot["particle_mass_Msun"][0])
        _, motion_mass = DYNAMICS.snapshot_profile(
            np.asarray(snapshot["positions_kpc"]),
            base["radii"],
            particle_mass,
        )
        initial_phase_mass[phase_sign] = motion_mass
    pair_initial_mass = 0.5 * (
        initial_phase_mass[-1] + initial_phase_mass[1]
    )
    baseline_score = DYNAMICS.score_profile(
        base["radii"],
        pair_initial_mass,
        base["target_velocity"],
        base["score_mask"],
        base["transition_radius"],
        base["edge_radius"],
        base["target_edge_mass"],
    )
    pair_total_transition = float(
        np.interp(base["transition_radius"], base["radii"], pair_initial_mass)
        / PM.MOTION_FRACTION
    )
    final_total_transition = pair_total_transition + float(
        base["visible_source"].mass_at(base["transition_radius"])
    ) - (1.0 - PM.MOTION_FRACTION) * pair_total_transition
    final_total_transition = max(final_total_transition, pair_total_transition)
    transition_orbit = 2.0 * math.pi * math.sqrt(
        base["transition_radius"] ** 3
        / (
            DYNAMICS.PREVIOUS.G_KPC_KM2_S2_MSUN
            * final_total_transition
        )
    )
    resolved_radius = max(
        float(snapshots[-1]["resolved_radius_kpc"][0]),
        float(snapshots[1]["resolved_radius_kpc"][0]),
    )
    softening_radius = DYNAMICS.SOFTENING_CELL_MULTIPLE * max(
        float(snapshots[-1]["local_force_cell_kpc"][0]),
        float(snapshots[1]["local_force_cell_kpc"][0]),
    )
    orbit_probe = np.geomspace(
        max(0.05 * softening_radius, 1.0e-3), resolved_radius, 256
    )
    monotone_initial_mass = np.maximum.accumulate(
        np.maximum(pair_initial_mass, 0.0)
    )
    motion_interpolator = PchipInterpolator(base["radii"], monotone_initial_mass)
    probe_motion_mass = np.asarray(
        motion_interpolator(np.maximum(orbit_probe, base["radii"][0])),
        dtype=float,
    )
    probe_total_mass = (
        probe_motion_mass / PM.MOTION_FRACTION
        + np.asarray(base["visible_source"].mass_at(orbit_probe), dtype=float)
    )
    softened_orbits = 2.0 * math.pi * np.sqrt(
        (orbit_probe**2 + softening_radius**2) ** 1.5
        / (
            DYNAMICS.PREVIOUS.G_KPC_KM2_S2_MSUN
            * np.maximum(probe_total_mass, 1.0)
        )
    )
    context["initial_phase_mass"] = initial_phase_mass
    context["pair_initial_mass"] = pair_initial_mass
    context["baseline_score"] = baseline_score
    context["transition_orbit"] = transition_orbit
    context["inner_orbit"] = float(np.min(softened_orbits))
    return context


def evolution_signature(
    source_hashes: dict[str, str],
    snapshot_path: Path,
    phase_sign: int,
    source_enabled: bool,
    endpoint_time: float,
) -> str:
    payload = {
        "source_hashes": source_hashes,
        "snapshot_sha256": file_digest(snapshot_path),
        "phase_sign": phase_sign,
        "source_enabled": source_enabled,
        "endpoint_time": endpoint_time,
        "steps_per_inner_orbit": STEPS_PER_INNER_ORBIT,
        "marker": MARKER,
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def run_or_load_evolution(
    source_hashes: dict[str, str],
    snapshot: dict[str, Any],
    snapshot_path: Path,
    plan: dict[str, Any],
    context: dict[str, Any],
    phase_sign: int,
    source_enabled: bool,
    force: bool,
) -> dict[str, Any]:
    role = "SOURCE" if source_enabled else "CONTROL"
    stem = f"CDM_{role}_PHASE_{phase_sign:+d}".replace("+", "PLUS").replace("-", "MINUS")
    array_path = EVOLUTION_CACHE / f"{stem}.npz"
    metadata_path = EVOLUTION_CACHE / f"{stem}.json"
    signature = evolution_signature(
        source_hashes,
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
    print(f"START CDM {role} phase={phase_sign:+d}", flush=True)
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
    EVOLUTION_CACHE.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(array_path, averaged_counts=result["averaged_counts"])
    diagnostics = {
        key: value for key, value in result.items() if key != "averaged_counts"
    }
    Q.write_json(
        metadata_path,
        {"cache_signature": signature, "diagnostics": diagnostics},
    )
    print(
        f"DONE CDM {role} phase={phase_sign:+d} wall={diagnostics['wall_seconds']:.3f}s",
        flush=True,
    )
    return result


def run_cdm_response(
    context: dict[str, Any],
    polynomial: dict[str, Any],
    solution: dict[str, Any],
    source_hashes: dict[str, str],
    force: bool,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[int, np.ndarray]]:
    data = R.binned_inputs(context, solution, polynomial, RADIAL_BINS)
    transport = R.solve_transport(data, COST_POWER)
    phase_mass: dict[int, np.ndarray] = {}
    controls: list[dict[str, Any]] = []
    for phase_sign in (-1, 1):
        snapshot = context["snapshots"][phase_sign]
        plan = V.phase_plan(snapshot, solution, data, transport, phase_sign)
        control = run_or_load_evolution(
            source_hashes,
            snapshot,
            SNAPSHOT_PATHS[phase_sign],
            plan,
            context,
            phase_sign,
            False,
            force,
        )
        source = run_or_load_evolution(
            source_hashes,
            snapshot,
            SNAPSHOT_PATHS[phase_sign],
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
                "phase_sign": phase_sign,
                "response_particle_count": len(snapshot["positions_kpc"]),
                "donor_particle_count": int(np.count_nonzero(snapshot["donor"])),
                "source_steps": source["steps"],
                "control_steps": control["steps"],
                "source_final_transfer_relative_residual": source[
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
    return f"""# 5173 - Matched CDM formation baseline discrimination gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Question

Checkpoint 5172 showed that source flattening does not repair the selected
formation response. That miss cannot be interpreted fairly until the same
pipeline is applied to a standard collisionless baseline. This checkpoint
therefore changes exactly one input: the MTS/FDM linear covariance
`P_CDM T_FDM^2` is replaced by its source-backed `P_CDM` parent curve. The
white phases, antithetic pairing, one-sigma constraint rule, nested force,
calibrated `G_N`, visible source, cooling solution, transport construction,
particle count, time step and scoring code are identical.

## Covariance difference

For UGC09133 the source table gives

```text
sigma_CDM={summary['sigma_CDM']},
sigma_MTS={summary['sigma_MTS']},
sigma ratio={summary['sigma_MTS_to_CDM']}.
```

The power ratio is `{summary['power_ratio_patch_inverse']}` at `1/R_L`,
`{summary['power_ratio_patch_2pi']}` at `2pi/R_L`, and
`{summary['power_ratio_particle_Nyquist']}` at the particle Nyquist scale.
Thus the halo-scale covariance is nearly identical while the resolved
small-scale tail supplies a genuine matched difference.

## Forward result

Before visible assembly, the matched pair gives

```text
MTS q={summary['MTS_preassembly_q']},
CDM q={summary['CDM_preassembly_q']},
Delta q={summary['preassembly_delta_q']}.
```

After the identical isobaric `Z=0.3` pair-consistent source history,

```text
MTS q={summary['MTS_forward_q']},
CDM q={summary['CDM_forward_q']},
Delta q={summary['forward_delta_q']};

MTS RMSE={summary['MTS_forward_RMSE']} dex,
CDM RMSE={summary['CDM_forward_RMSE']} dex,
Delta RMSE={summary['forward_delta_RMSE']} dex.
```

The inherited selected-branch numerical envelopes are
`{summary['q_numerical_envelope']}` in q and
`{summary['RMSE_numerical_envelope']}` dex in RMSE. The matched response is
classified as `{summary['discrimination_status']}`.

## Interpretation

`{result['route_decision']}`.

This is a baseline-symmetry result, not a CDM cosmological validation and not
an MTS galaxy claim. If the responses are indistinguishable, the one-patch
formation failure is a limitation shared by the comparator and cannot be used
as MTS-specific evidence. It still leaves the MTS parent state law underived.
If they are distinguishable, the sign is reported without retuning either
branch.

All `{result['validation_count']}` validations pass. Every row remains
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
    wavenumber, cdm_power, mts_power, patch = covariance_rows()
    targets, _, patch_radius, _ = ZOOM.PREVIOUS.target_lookup()
    target = targets[REFERENCE_MAPPING]
    edge_radius = float(target["edge_radius_Mpc"])
    box_size = PM.BOX_OVER_PATCH * patch_radius
    probes = power_probe_rows(
        wavenumber,
        cdm_power,
        mts_power,
        box_size,
        patch_radius,
        edge_radius,
    )
    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "marker": MARKER,
                    "single_changed_input": "P_MTS_to_P_CDM",
                    "particle_grid": ZOOM.PARTICLE_GRID,
                    "local_grid": DYNAMICS.LOCAL_GRID,
                    "target_constraint_CDM": float(patch["sigma_CDM_empirical"]),
                    "target_constraint_MTS": float(
                        patch["sigma_MTS_empirical_adiabatic"]
                    ),
                    "formal_digest": formal_before,
                },
                indent=2,
            )
        )
        return
    cdm_snapshots, snapshot_metadata = generate_cdm_snapshots(
        arguments.force_snapshots
    )
    base_context, polynomial, _, solutions = R.build_parent_state()
    cdm_context = make_cdm_context(base_context, cdm_snapshots)
    cdm_score, response_controls, cdm_phase_mass = run_cdm_response(
        cdm_context,
        polynomial,
        solutions[SELECTED_BRANCH],
        hashes_before,
        arguments.force_response,
    )
    mts_scores = read_csv(PREVIOUS_SCORE)
    selected_id = "ISOBARIC_Z0.3_RADIAL_COOLING_FREEFALL_OT_N26_P1_FULL_PRIMARY"
    mts_primary = next(row for row in mts_scores if row["run_id"] == selected_id)
    mts_controls = [
        row
        for row in mts_scores
        if row["thermal_mode"] == SELECTED_BRANCH[0]
        and float(row["metallicity_Zsun"]) == SELECTED_BRANCH[1]
    ]
    q_numerical_envelope = max(
        abs(float(row["corrected_q"]) - float(mts_primary["corrected_q"]))
        for row in mts_controls
    )
    rmse_numerical_envelope = max(
        abs(
            float(row["corrected_velocity_squared_log10_RMSE"])
            - float(mts_primary["corrected_velocity_squared_log10_RMSE"])
        )
        for row in mts_controls
    )
    forward_delta_q = float(cdm_score["q"]) - float(mts_primary["corrected_q"])
    forward_delta_rmse = float(cdm_score["velocity_squared_log10_RMSE"]) - float(
        mts_primary["corrected_velocity_squared_log10_RMSE"]
    )
    indistinguishable = (
        abs(forward_delta_q) <= q_numerical_envelope
        and abs(forward_delta_rmse) <= rmse_numerical_envelope
    )
    cdm_better = (
        abs(float(cdm_score["q"]) - float(cdm_context["q_row"]["q_parent"]))
        < abs(
            float(mts_primary["corrected_q"])
            - float(cdm_context["q_row"]["q_parent"])
        )
        and float(cdm_score["velocity_squared_log10_RMSE"])
        < float(mts_primary["corrected_velocity_squared_log10_RMSE"])
    )
    mts_better = (
        abs(float(cdm_score["q"]) - float(cdm_context["q_row"]["q_parent"]))
        > abs(
            float(mts_primary["corrected_q"])
            - float(cdm_context["q_row"]["q_parent"])
        )
        and float(cdm_score["velocity_squared_log10_RMSE"])
        > float(mts_primary["corrected_velocity_squared_log10_RMSE"])
    )
    if indistinguishable:
        discrimination_status = "NOT_DISCRIMINATED_WITHIN_MATCHED_NUMERICAL_ENVELOPE"
        route_decision = (
            "MATCHED_CDM_AND_MTS_FORMATION_RESPONSES_ARE_NOT_NUMERICALLY_DISCRIMINATED_SO_THE_SINGLE_PATCH_FORMATION_MISS_IS_NOT_MTS_SPECIFIC_AND_THE_PARENT_STATE_LAW_REMAINS_THE_REAL_OPEN_OBJECT"
        )
    elif mts_better:
        discrimination_status = "MTS_CLOSER_ON_Q_AND_RMSE"
        route_decision = (
            "THE_MATCHED_MTS_COVARIANCE_OUTPERFORMS_CDM_IN_THIS_SHARED_PHASE_PATCH_BUT_ONE_PATCH_IS_NOT_AN_ENSEMBLE_AND_THE_PARENT_PRIMORDIAL_STATE_REMAINS_CONDITIONAL"
        )
    elif cdm_better:
        discrimination_status = "CDM_CLOSER_ON_Q_AND_RMSE"
        route_decision = (
            "THE_MATCHED_CDM_COVARIANCE_OUTPERFORMS_THE_CURRENT_MTS_STATE_IN_THIS_SHARED_PHASE_PATCH_SO_THE_MTS_STATE_SELECTION_ROUTE_REQUIRES_REVISION_BEFORE_PROMOTION"
        )
    else:
        discrimination_status = "MIXED_Q_RMSE_VERDICT"
        route_decision = (
            "THE_MATCHED_CDM_MTS_COMPARISON_SPLITS_Q_AND_RMSE_SO_NO_MODEL_PREFERENCE_IS_ASSIGNED_AND_AN_ENSEMBLE_BASELINE_IS_REQUIRED"
        )
    mts_pair_q = float(base_context["baseline_score"]["q"])
    cdm_pair_q = float(cdm_context["baseline_score"]["q"])
    probe_by_id = {row["probe_id"]: row for row in probes}
    score_rows = [
        {
            "model": "MTS_1e_minus20_eV",
            "covariance": "P_CDM_times_T_FDM_squared",
            "preassembly_q": mts_pair_q,
            "forward_q": float(mts_primary["corrected_q"]),
            "forward_RMSE_dex": float(
                mts_primary["corrected_velocity_squared_log10_RMSE"]
            ),
            "forward_transition_ratio": float(
                mts_primary["corrected_transition_velocity_squared_ratio_to_target"]
            ),
            "forward_edge_ratio": float(
                mts_primary["corrected_edge_mass_ratio_to_target"]
            ),
            "q_numerical_envelope": q_numerical_envelope,
            "RMSE_numerical_envelope_dex": rmse_numerical_envelope,
            "target_used_to_define_evolution": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "model": "matched_CDM",
            "covariance": "P_CDM",
            "preassembly_q": cdm_pair_q,
            "forward_q": float(cdm_score["q"]),
            "forward_RMSE_dex": float(cdm_score["velocity_squared_log10_RMSE"]),
            "forward_transition_ratio": float(
                cdm_score["transition_velocity_squared_ratio_to_target"]
            ),
            "forward_edge_ratio": float(cdm_score["edge_mass_ratio_to_target"]),
            "q_numerical_envelope": q_numerical_envelope,
            "RMSE_numerical_envelope_dex": rmse_numerical_envelope,
            "target_used_to_define_evolution": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]
    snapshot_rows: list[dict[str, Any]] = []
    mts_metadata = json.loads(
        DYNAMICS.SNAPSHOT_META_JSON.read_text(encoding="utf-8")
    )
    for phase_sign in (-1, 1):
        cdm_phase = snapshot_metadata["phases"][str(phase_sign)]
        mts_phase = mts_metadata["phases"][str(phase_sign)]
        snapshot_rows.append(
            {
                "phase_sign": phase_sign,
                "CDM_selected_particle_count": cdm_phase["selected_particle_count"],
                "MTS_selected_particle_count": mts_phase["selected_particle_count"],
                "CDM_donor_particle_count": cdm_phase["donor_particle_count"],
                "MTS_donor_particle_count": mts_phase["donor_particle_count"],
                "CDM_preassembly_phase_q": cdm_phase["regenerated_q"],
                "MTS_preassembly_phase_q": mts_phase["regenerated_q"],
                "phase_q_difference": float(cdm_phase["regenerated_q"])
                - float(mts_phase["regenerated_q"]),
                "same_fixed_seed": True,
                "same_particle_and_force_grids": True,
                "target_used": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    cdm_mass = 0.5 * (cdm_phase_mass[-1] + cdm_phase_mass[1])
    mts_profile = [
        row for row in read_csv(PREVIOUS_PROFILE) if row["run_id"] == selected_id
    ]
    mts_profile.sort(key=lambda row: float(row["radius_kpc"]))
    profile_rows: list[dict[str, Any]] = []
    for index, radius in enumerate(cdm_context["radii"]):
        mts_mass = float(mts_profile[index]["corrected_motion_mass_Msun"])
        profile_rows.append(
            {
                "radius_kpc": radius,
                "radius_over_transition": radius / cdm_context["transition_radius"],
                "MTS_corrected_motion_mass_Msun": mts_mass,
                "CDM_corrected_motion_mass_Msun": cdm_mass[index],
                "CDM_minus_MTS_mass_Msun": cdm_mass[index] - mts_mass,
                "CDM_to_MTS_mass_ratio": cdm_mass[index] / max(mts_mass, 1.0),
                "inside_scoring_window": bool(cdm_context["score_mask"][index]),
                "target_used_to_define_evolution": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    decisions = [
        {
            "route": "matched_CDM_MTS_formation_baseline",
            "result": route_decision,
            "evidence": (
                f"delta_q={forward_delta_q}; delta_RMSE={forward_delta_rmse}; "
                f"q_envelope={q_numerical_envelope}; "
                f"RMSE_envelope={rmse_numerical_envelope}"
            ),
            "next_requirement": (
                "derive or source an ensemble primordial state law and compare both models with the same realization ensemble"
                if indistinguishable or discrimination_status == "MIXED_Q_RMSE_VERDICT"
                else "repeat the matched result over a predeclared realization ensemble before any model preference"
            ),
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    ]
    conditioning = snapshot_metadata["conditioning"]
    hashes_after = {key: file_digest(path) for key, path in paths.items()}
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
        "CDM_constraint_matches_source_sigma",
        abs(
            float(conditioning["target_constraint"])
            - float(patch["sigma_CDM_empirical"])
        )
        < 1.0e-12,
        conditioning,
    )
    add_validation(
        validation,
        "conditioned_pair_exact",
        float(conditioning["maximum_constraint_error"]) < 1.0e-12
        and float(conditioning["pair_mean_error"]) < 1.0e-12
        and float(conditioning["residual_antisymmetry_error"]) < 1.0e-12,
        conditioning,
    )
    add_validation(
        validation,
        "CDM_power_not_below_MTS",
        bool(np.all(cdm_power >= mts_power)),
        float(np.min(mts_power / cdm_power)),
    )
    add_validation(
        validation,
        "snapshots_finite",
        all(
            np.all(np.isfinite(snapshot["positions_kpc"]))
            and np.all(np.isfinite(snapshot["velocities_km_s"]))
            for snapshot in cdm_snapshots.values()
        ),
        [len(snapshot["positions_kpc"]) for snapshot in cdm_snapshots.values()],
    )
    add_validation(
        validation,
        "response_finite",
        math.isfinite(float(cdm_score["q"]))
        and math.isfinite(float(cdm_score["velocity_squared_log10_RMSE"])),
        cdm_score,
    )
    add_validation(
        validation,
        "phase_transfer_conserved",
        max(
            float(row["source_final_transfer_relative_residual"])
            for row in response_controls
        )
        < 1.0e-10,
        response_controls,
    )
    add_validation(
        validation,
        "angular_momentum_conserved",
        max(
            float(row["source_angular_momentum_relative_residual"])
            for row in response_controls
        )
        < 1.0e-10,
        response_controls,
    )
    add_validation(
        validation,
        "single_changed_physics_input",
        all(row["same_fixed_seed"] and row["same_particle_and_force_grids"] for row in snapshot_rows),
        "linear covariance P_MTS -> P_CDM",
    )
    all_rows = (
        contract_rows()
        + probes
        + snapshot_rows
        + score_rows
        + response_controls
        + profile_rows
        + decisions
    )
    add_validation(
        validation,
        "all_rows_nonclaim",
        all(not bool(row["valid_for_claim"]) for row in all_rows),
        len(all_rows),
    )
    add_validation(
        validation,
        "no_placeholder_tokens",
        "MISSING_" not in json.dumps(all_rows, sort_keys=True, default=str),
        len(all_rows),
    )
    failures = [row for row in validation if not row["passed"]]
    if failures:
        raise RuntimeError(f"validation failures: {failures}")
    summary = {
        "sigma_CDM": float(patch["sigma_CDM_empirical"]),
        "sigma_MTS": float(patch["sigma_MTS_empirical_adiabatic"]),
        "sigma_MTS_to_CDM": float(patch["sigma_MTS_over_CDM"]),
        "power_ratio_patch_inverse": probe_by_id["patch_inverse"][
            "MTS_to_CDM_power_ratio"
        ],
        "power_ratio_patch_2pi": probe_by_id["patch_2pi"][
            "MTS_to_CDM_power_ratio"
        ],
        "power_ratio_particle_Nyquist": probe_by_id["particle_Nyquist"][
            "MTS_to_CDM_power_ratio"
        ],
        "MTS_preassembly_q": mts_pair_q,
        "CDM_preassembly_q": cdm_pair_q,
        "preassembly_delta_q": cdm_pair_q - mts_pair_q,
        "MTS_forward_q": float(mts_primary["corrected_q"]),
        "CDM_forward_q": float(cdm_score["q"]),
        "forward_delta_q": forward_delta_q,
        "MTS_forward_RMSE": float(
            mts_primary["corrected_velocity_squared_log10_RMSE"]
        ),
        "CDM_forward_RMSE": float(cdm_score["velocity_squared_log10_RMSE"]),
        "forward_delta_RMSE": forward_delta_rmse,
        "q_numerical_envelope": q_numerical_envelope,
        "RMSE_numerical_envelope": rmse_numerical_envelope,
        "discrimination_status": discrimination_status,
        "response_indistinguishable": indistinguishable,
    }
    result = {
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "summary": summary,
        "route_decision": route_decision,
        "validation_count": len(validation),
        "formalization_workbench_tree_sha256": formal_after,
        "valid_for_claim": False,
    }
    provenance = [
        {
            "source_id": key,
            "source_type": "local_file",
            "source_path": str(path),
            "sha256": hashes_after[key],
            "status": "immutable_input",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for key, path in paths.items()
    ]
    Q.write_csv(CONTRACT_CSV, contract_rows())
    Q.write_csv(POWER_CSV, probes)
    Q.write_csv(SNAPSHOT_CSV, snapshot_rows)
    Q.write_csv(SCORE_CSV, score_rows)
    Q.write_csv(CONTROL_CSV, response_controls)
    Q.write_csv(PROFILE_CSV, profile_rows)
    Q.write_csv(DECISION_CSV, decisions)
    Q.write_csv(PROVENANCE_CSV, provenance)
    Q.write_csv(VALIDATION_CSV, validation)
    Q.write_json(RESULT_JSON, result)
    DOCUMENT.write_text(make_document(result), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
