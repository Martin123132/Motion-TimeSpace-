from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import itertools
import json
import math
import sys
import time
import traceback
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TextIO

sys.dont_write_bytecode = True

import numpy as np


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
PREVIOUS_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5175_exact_low_mode_shared_isotropic_resolution_gate.py"
)
PREVIOUS_DOCUMENT = (
    POST
    / "5175-Y5-R2FR-exact-low-mode-shared-isotropic-resolution-discrimination-gate.md"
)
PREVIOUS_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5175"
    / "isotropic_resolution_results.json"
)
PREVIOUS_RUN_SCORES = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5175"
    / "isotropic_MTS_CDM_forward_scores.csv"
)
PREVIOUS_VALIDATION = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5175_VALIDATION.csv"
)
OUT = POST / "source-intake" / "functional_rg" / "5176"
SEED_ROOT = OUT / "seeds"
PROTOCOL_JSON = OUT / "ensemble_protocol.json"
SCHEDULE_CSV = OUT / "predeclared_seed_schedule.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
SEED_SCORE_CSV = OUT / "paired_seed_scores.csv"
STATISTICS_CSV = OUT / "paired_ensemble_statistics.csv"
STATUS_CSV = OUT / "seed_execution_status.csv"
DECISION_CSV = OUT / "route_decision.csv"
RESULT_JSON = OUT / "paired_ensemble_results.json"
VALIDATION_CSV = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5176_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5176-Y5-R2FR-predeclared-paired-high-mode-seed-ensemble.md"
)

MARKER = "MTS_5176_PREDECLARED_PAIRED_HIGH_MODE_SEED_ENSEMBLE"
CHECKED_DATE = "2026-07-21"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
PROTOCOL_NAMESPACE = "MTS_5176_CONFIRMATORY_HIGH_MODE_SEED_V1"
PILOT_SEED = 517500409
ENSEMBLE_SIZE = 12
INTERIM_SIZE = 6
BOOTSTRAP_REPLICATES = 20000
BOOTSTRAP_SEED = 517600777
ALPHA = 0.05
ALGORITHM_VERSION = "predeclared_paired_high_mode_ensemble_v1"


specification = importlib.util.spec_from_file_location(
    "mts_checkpoint_5175_for_5176", PREVIOUS_SCRIPT
)
if specification is None or specification.loader is None:
    raise RuntimeError(f"cannot load module: {PREVIOUS_SCRIPT}")
resolution = importlib.util.module_from_spec(specification)
specification.loader.exec_module(resolution)


class TeeStream:
    def __init__(self, terminal: TextIO, log: TextIO) -> None:
        self.terminal = terminal
        self.log = log

    def write(self, value: str) -> int:
        self.terminal.write(value)
        self.log.write(value)
        return len(value)

    def flush(self) -> None:
        self.terminal.flush()
        self.log.flush()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


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


def stable_digest(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def source_paths() -> dict[str, Path]:
    return {
        "checkpoint_5175_script": PREVIOUS_SCRIPT,
        "checkpoint_5175_document": PREVIOUS_DOCUMENT,
        "checkpoint_5175_result": PREVIOUS_RESULT,
        "checkpoint_5175_run_scores": PREVIOUS_RUN_SCORES,
        "checkpoint_5175_validation": PREVIOUS_VALIDATION,
        "checkpoint_5174_result": resolution.PREVIOUS_RESULT,
        "checkpoint_5176_script": Path(__file__).resolve(),
    }


def derive_seed_schedule() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    used: set[int] = {PILOT_SEED}
    for seed_index in range(1, ENSEMBLE_SIZE + 1):
        token = f"{PROTOCOL_NAMESPACE}:{seed_index:02d}"
        digest = hashlib.sha256(token.encode("ascii")).hexdigest()
        seed_value = int(digest[:16], 16) % (2**32 - 1) + 1
        if seed_value in used:
            raise RuntimeError(f"seed collision at index {seed_index}")
        used.add(seed_value)
        rows.append(
            {
                "seed_index": seed_index,
                "high_mode_seed": seed_value,
                "derivation_token": token,
                "derivation_sha256": digest,
                "analysis_role": "confirmatory",
                "execution_order_locked": True,
                "pilot_seed_excluded": seed_value != PILOT_SEED,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows


def analysis_settings() -> dict[str, Any]:
    previous_5174 = json.loads(
        resolution.PREVIOUS_RESULT.read_text(encoding="utf-8")
    )
    previous_5175 = json.loads(PREVIOUS_RESULT.read_text(encoding="utf-8"))
    schedule = derive_seed_schedule()
    return {
        "protocol_namespace": PROTOCOL_NAMESPACE,
        "algorithm_version": ALGORITHM_VERSION,
        "pilot_seed": PILOT_SEED,
        "pilot_excluded_from_confirmatory_inference": True,
        "confirmatory_seed_count": ENSEMBLE_SIZE,
        "interim_seed_count": INTERIM_SIZE,
        "interim_use": "descriptive_only_no_preference_stop",
        "final_analysis_count": ENSEMBLE_SIZE,
        "alpha_two_sided": ALPHA,
        "bootstrap_replicates": BOOTSTRAP_REPLICATES,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "source_grid": resolution.SOURCE_GRID,
        "particle_grid": resolution.PARTICLE_GRID,
        "global_force_grid": resolution.ZOOM.GLOBAL_FORCE_GRID,
        "local_force_grid": resolution.DYNAMICS.LOCAL_GRID,
        "low_source_grid": resolution.LOW_SOURCE_GRID,
        "fixed_low_mode_seed": resolution.PM.FIXED_SEED,
        "taper_start_fraction": resolution.TAPER_START_FRACTION,
        "MTS_mass_eV": resolution.MASS_EV,
        "reference_galaxy": resolution.REFERENCE_GALAXY,
        "reference_mapping": resolution.REFERENCE_MAPPING,
        "selected_branch": list(resolution.SELECTED_BRANCH),
        "steps_per_inner_orbit": resolution.STEPS_PER_INNER_ORBIT,
        "radial_bins": resolution.RADIAL_BINS,
        "transport_cost_power": resolution.COST_POWER,
        "q_lower": float(previous_5174["summary"]["parent_q_lower"]),
        "q_upper": float(previous_5174["summary"]["parent_q_upper"]),
        "q_numerical_envelope": float(
            previous_5174["summary"]["q_numerical_envelope"]
        ),
        "RMSE_numerical_envelope_dex": float(
            previous_5174["summary"]["RMSE_numerical_envelope"]
        ),
        "source_axis_nyquist_Mpc_inverse": float(
            previous_5175["summary"]["source_axis_nyquist_Mpc_inverse"]
        ),
        "estimated_hours_per_seed": float(
            previous_5175["summary"]["estimated_total_wall_hours"]
        ),
        "runtime_cap_hours_per_invocation": 4.0,
        "primary_q_estimand": (
            "D_q=d_q(MTS)-d_q(CDM); positive favors CDM"
        ),
        "primary_RMSE_estimand": (
            "D_R=RMSE(MTS)-RMSE(CDM); positive favors CDM"
        ),
        "preference_rule": (
            "At N=12 only: both paired means and 95% deterministic bootstrap "
            "intervals must have the same nonzero sign, both exact two-sided "
            "sign-flip p-values must be <=0.05, and the same-direction joint "
            "win sign test must be <=0.05; otherwise report a statistical draw "
            "or metric split."
        ),
        "tie_rule": (
            "A seed is jointly decisive only when both absolute paired "
            "advantages exceed their inherited numerical envelopes in the "
            "same direction."
        ),
        "seed_schedule": [
            {
                "seed_index": int(row["seed_index"]),
                "high_mode_seed": int(row["high_mode_seed"]),
                "derivation_sha256": row["derivation_sha256"],
            }
            for row in schedule
        ],
        "physics_inputs_locked_to_checkpoint_5175": True,
        "target_used_to_define_evolution": False,
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }


def ensure_protocol() -> dict[str, Any]:
    OUT.mkdir(parents=True, exist_ok=True)
    settings = analysis_settings()
    protocol_sha256 = stable_digest(settings)
    schedule = derive_seed_schedule()
    if PROTOCOL_JSON.is_file():
        stored = json.loads(PROTOCOL_JSON.read_text(encoding="utf-8"))
        if stored.get("protocol_sha256") != protocol_sha256:
            raise RuntimeError("stored protocol differs from current protocol")
        if stored.get("settings") != settings:
            raise RuntimeError("stored protocol settings changed")
        stored_schedule = read_csv(SCHEDULE_CSV)
        expected_pairs = [
            (str(row["seed_index"]), str(row["high_mode_seed"]))
            for row in schedule
        ]
        stored_pairs = [
            (row["seed_index"], row["high_mode_seed"])
            for row in stored_schedule
        ]
        if stored_pairs != expected_pairs:
            raise RuntimeError("stored seed schedule changed")
        return stored
    if any(SEED_ROOT.rglob("COMPLETE.marker")):
        raise RuntimeError("cannot lock protocol after a seed completed")
    protocol = {
        "protocol_sha256": protocol_sha256,
        "locked_at_utc": utc_now(),
        "locked_before_first_confirmatory_seed": True,
        "settings": settings,
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }
    write_csv(SCHEDULE_CSV, schedule)
    resolution.Q.write_json(PROTOCOL_JSON, protocol)
    return protocol


def seed_paths(seed_index: int, seed_value: int) -> dict[str, Path]:
    seed_dir = SEED_ROOT / f"seed_{seed_index:02d}_{seed_value}"
    return {
        "dir": seed_dir,
        "runs": seed_dir / "runs",
        "log": seed_dir / "log.txt",
        "status": seed_dir / "status.json",
        "scores": seed_dir / "forward_scores.csv",
        "phases": seed_dir / "phase_diagnostics.csv",
        "result": seed_dir / "seed_result.json",
        "complete": seed_dir / "COMPLETE.marker",
    }


def common_context() -> dict[str, Any]:
    wavenumber, cdm_power, mts_power, _, _ = resolution.F.transfer_inputs()
    base_context, polynomial, _, solutions = resolution.R.build_parent_state()
    selected_solution = solutions[resolution.SELECTED_BRANCH]
    _, _, patch_radius, _ = resolution.ZOOM.PREVIOUS.target_lookup()
    box_size = resolution.PM.BOX_OVER_PATCH * patch_radius
    axis_nyquist = math.pi * resolution.SOURCE_GRID / box_size
    previous_5174 = json.loads(
        resolution.PREVIOUS_RESULT.read_text(encoding="utf-8")
    )
    return {
        "wavenumber": wavenumber,
        "cdm_power": cdm_power,
        "mts_power": mts_power,
        "base_context": base_context,
        "polynomial": polynomial,
        "selected_solution": selected_solution,
        "patch_radius": patch_radius,
        "axis_nyquist": axis_nyquist,
        "q_lower": float(previous_5174["summary"]["parent_q_lower"]),
        "q_upper": float(previous_5174["summary"]["parent_q_upper"]),
        "q_envelope": float(
            previous_5174["summary"]["q_numerical_envelope"]
        ),
        "rmse_envelope": float(
            previous_5174["summary"]["RMSE_numerical_envelope"]
        ),
    }


def q_band_distance(value: float, lower: float, upper: float) -> float:
    return max(lower - value, 0.0, value - upper)


def classify_seed(
    q_advantage: float,
    rmse_advantage: float,
    q_envelope: float,
    rmse_envelope: float,
) -> str:
    if q_advantage > q_envelope and rmse_advantage > rmse_envelope:
        return "CDM_JOINT_WIN"
    if q_advantage < -q_envelope and rmse_advantage < -rmse_envelope:
        return "MTS_JOINT_WIN"
    if abs(q_advantage) <= q_envelope and abs(rmse_advantage) <= rmse_envelope:
        return "NUMERICAL_TIE"
    return "MIXED_OR_SINGLE_METRIC"


def run_seed(
    protocol: dict[str, Any], schedule_row: dict[str, Any]
) -> dict[str, Any]:
    seed_index = int(schedule_row["seed_index"])
    seed_value = int(schedule_row["high_mode_seed"])
    paths = seed_paths(seed_index, seed_value)
    paths["dir"].mkdir(parents=True, exist_ok=True)
    if paths["complete"].is_file() and paths["result"].is_file():
        completed = json.loads(paths["result"].read_text(encoding="utf-8"))
        if completed.get("protocol_sha256") != protocol["protocol_sha256"]:
            raise RuntimeError("completed seed has wrong protocol hash")
        return completed
    status = {
        "seed_index": seed_index,
        "high_mode_seed": seed_value,
        "state": "RUNNING",
        "started_at_utc": utc_now(),
        "protocol_sha256": protocol["protocol_sha256"],
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }
    resolution.Q.write_json(paths["status"], status)
    source_hashes_before = {
        key: resolution.Q.file_digest(path)
        for key, path in source_paths().items()
    }
    formal_before = resolution.Q.tree_digest(FORMAL)
    if formal_before != FORMAL_DIGEST_LOCK:
        raise RuntimeError(f"protected digest mismatch: {formal_before}")
    start = time.perf_counter()
    with paths["log"].open("a", encoding="utf-8") as log_handle:
        tee_stdout = TeeStream(sys.stdout, log_handle)
        tee_stderr = TeeStream(sys.stderr, log_handle)
        with redirect_stdout(tee_stdout), redirect_stderr(tee_stderr):
            print(
                f"START seed_index={seed_index} high_mode_seed={seed_value} "
                f"protocol={protocol['protocol_sha256']}",
                flush=True,
            )
            try:
                context = common_context()
                resolution.HIGH_MODE_SEED = seed_value
                resolution.RUNS = paths["runs"]
                resolution.MARKER = MARKER
                resolution.ALGORITHM_VERSION = ALGORITHM_VERSION
                standardized_modes, basis = resolution.shared_standardized_modes()
                families = resolution.family_spectra(
                    context["wavenumber"],
                    context["cdm_power"],
                    context["mts_power"],
                    context["axis_nyquist"],
                )
                score_rows: list[dict[str, Any]] = []
                phase_rows: list[dict[str, Any]] = []
                for family in families:
                    snapshots, metadata = resolution.generate_snapshots(
                        family,
                        standardized_modes,
                        basis,
                        context["wavenumber"],
                        context["patch_radius"],
                        context["base_context"],
                        False,
                    )
                    family_context = resolution.B.make_cdm_context(
                        context["base_context"], snapshots
                    )
                    score, controls, _ = resolution.run_response(
                        family["family_id"],
                        family_context,
                        context["polynomial"],
                        context["selected_solution"],
                        False,
                    )
                    score_rows.append(
                        {
                            "seed_index": seed_index,
                            "high_mode_seed": seed_value,
                            "family_id": family["family_id"],
                            "model": family["model"],
                            "basis_sha256": basis["basis_sha256"],
                            "preassembly_q": float(
                                family_context["baseline_score"]["q"]
                            ),
                            "forward_q": float(score["q"]),
                            "forward_RMSE_dex": float(
                                score["velocity_squared_log10_RMSE"]
                            ),
                            "q_band_distance": q_band_distance(
                                float(score["q"]),
                                context["q_lower"],
                                context["q_upper"],
                            ),
                            "edge_mass_ratio_to_target": float(
                                score["edge_mass_ratio_to_target"]
                            ),
                            "maximum_constraint_error": float(
                                metadata["conditioning"][
                                    "maximum_constraint_error"
                                ]
                            ),
                            "maximum_imaginary_residual": float(
                                metadata["conditioning"][
                                    "maximum_imaginary_residual"
                                ]
                            ),
                            "target_used_to_define_evolution": False,
                            "valid_for_claim": False,
                            "checkpoint_marker": MARKER,
                        }
                    )
                    for control in controls:
                        phase_rows.append(
                            {
                                "seed_index": seed_index,
                                "high_mode_seed": seed_value,
                                "model": family["model"],
                                **control,
                            }
                        )
                by_model = {row["model"]: row for row in score_rows}
                mts_score = by_model["MTS_1e_minus20_eV"]
                cdm_score = by_model["CDM"]
                q_advantage = float(mts_score["q_band_distance"]) - float(
                    cdm_score["q_band_distance"]
                )
                rmse_advantage = float(mts_score["forward_RMSE_dex"]) - float(
                    cdm_score["forward_RMSE_dex"]
                )
                seed_result = {
                    "seed_index": seed_index,
                    "high_mode_seed": seed_value,
                    "protocol_sha256": protocol["protocol_sha256"],
                    "basis_sha256": basis["basis_sha256"],
                    "shared_standardized_mode_maximum_error": basis[
                        "shared_standardized_mode_maximum_error"
                    ],
                    "Hermitian_inverse_maximum_imaginary": basis[
                        "Hermitian_inverse_maximum_imaginary"
                    ],
                    "MTS_forward_q": float(mts_score["forward_q"]),
                    "CDM_forward_q": float(cdm_score["forward_q"]),
                    "MTS_q_band_distance": float(
                        mts_score["q_band_distance"]
                    ),
                    "CDM_q_band_distance": float(
                        cdm_score["q_band_distance"]
                    ),
                    "D_q_MTS_minus_CDM_band_distance": q_advantage,
                    "MTS_forward_RMSE_dex": float(
                        mts_score["forward_RMSE_dex"]
                    ),
                    "CDM_forward_RMSE_dex": float(
                        cdm_score["forward_RMSE_dex"]
                    ),
                    "D_RMSE_MTS_minus_CDM_dex": rmse_advantage,
                    "joint_classification": classify_seed(
                        q_advantage,
                        rmse_advantage,
                        context["q_envelope"],
                        context["rmse_envelope"],
                    ),
                    "maximum_constraint_error": max(
                        float(row["maximum_constraint_error"])
                        for row in score_rows
                    ),
                    "maximum_imaginary_residual": max(
                        float(row["maximum_imaginary_residual"])
                        for row in score_rows
                    ),
                    "maximum_transfer_relative_residual": max(
                        abs(float(row["source_transfer_relative_residual"]))
                        for row in phase_rows
                    ),
                    "maximum_angular_momentum_relative_residual": max(
                        max(
                            abs(
                                float(
                                    row[
                                        "source_angular_momentum_relative_residual"
                                    ]
                                )
                            ),
                            abs(
                                float(
                                    row[
                                        "control_angular_momentum_relative_residual"
                                    ]
                                )
                            ),
                        )
                        for row in phase_rows
                    ),
                    "wall_seconds": time.perf_counter() - start,
                    "completed_at_utc": utc_now(),
                    "target_used_to_define_evolution": False,
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
                write_csv(paths["scores"], score_rows)
                write_csv(paths["phases"], phase_rows)
                resolution.Q.write_json(paths["result"], seed_result)
                source_hashes_after = {
                    key: resolution.Q.file_digest(path)
                    for key, path in source_paths().items()
                }
                formal_after = resolution.Q.tree_digest(FORMAL)
                if source_hashes_before != source_hashes_after:
                    raise RuntimeError("source hash changed during seed run")
                if formal_after != FORMAL_DIGEST_LOCK:
                    raise RuntimeError("formalization workbench changed")
                completion_text = (
                    f"seed_index={seed_index}\n"
                    f"high_mode_seed={seed_value}\n"
                    f"protocol_sha256={protocol['protocol_sha256']}\n"
                    f"result_sha256={resolution.Q.file_digest(paths['result'])}\n"
                )
                paths["complete"].write_text(completion_text, encoding="utf-8")
                resolution.Q.write_json(
                    paths["status"],
                    {
                        **status,
                        "state": "COMPLETE",
                        "completed_at_utc": seed_result["completed_at_utc"],
                        "wall_seconds": seed_result["wall_seconds"],
                        "result_sha256": resolution.Q.file_digest(
                            paths["result"]
                        ),
                    },
                )
                print(json.dumps(seed_result, indent=2), flush=True)
                return seed_result
            except Exception as error:
                traceback.print_exc()
                resolution.Q.write_json(
                    paths["status"],
                    {
                        **status,
                        "state": "FAILED_OR_INTERRUPTED",
                        "updated_at_utc": utc_now(),
                        "error": repr(error),
                    },
                )
                raise


def exact_sign_flip_p(values: np.ndarray) -> float | None:
    if values.size < 2:
        return None
    observed = abs(float(np.mean(values)))
    extreme = 0
    total = 2 ** int(values.size)
    for signs in itertools.product((-1.0, 1.0), repeat=int(values.size)):
        trial = abs(float(np.mean(values * np.asarray(signs, dtype=float))))
        if trial >= observed - 1.0e-15:
            extreme += 1
    return extreme / total


def bootstrap_interval(
    values: np.ndarray, stream_offset: int
) -> tuple[float | None, float | None]:
    if values.size < 2:
        return None, None
    generator = np.random.default_rng(BOOTSTRAP_SEED + stream_offset)
    indices = generator.integers(
        0, values.size, size=(BOOTSTRAP_REPLICATES, values.size)
    )
    means = np.mean(values[indices], axis=1)
    lower, upper = np.quantile(means, [ALPHA / 2.0, 1.0 - ALPHA / 2.0])
    return float(lower), float(upper)


def exact_two_sided_sign_p(positive: int, negative: int) -> float | None:
    total = positive + negative
    if total == 0:
        return None
    majority = max(positive, negative)
    tail = sum(math.comb(total, count) for count in range(majority, total + 1))
    return min(1.0, 2.0 * tail / (2**total))


def metric_statistics(
    metric_id: str, values: np.ndarray, stream_offset: int
) -> dict[str, Any]:
    lower, upper = bootstrap_interval(values, stream_offset)
    return {
        "metric_id": metric_id,
        "completed_confirmatory_seeds": int(values.size),
        "mean": float(np.mean(values)) if values.size else None,
        "median": float(np.median(values)) if values.size else None,
        "sample_standard_deviation": (
            float(np.std(values, ddof=1)) if values.size >= 2 else None
        ),
        "standard_error": (
            float(np.std(values, ddof=1) / math.sqrt(values.size))
            if values.size >= 2
            else None
        ),
        "bootstrap_95_lower": lower,
        "bootstrap_95_upper": upper,
        "exact_two_sided_sign_flip_p": exact_sign_flip_p(values),
        "positive_favors": "CDM",
        "negative_favors": "MTS",
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }


def completed_seed_results(
    schedule: list[dict[str, Any]], protocol_sha256: str
) -> list[dict[str, Any]]:
    completed: list[dict[str, Any]] = []
    for row in schedule:
        seed_index = int(row["seed_index"])
        seed_value = int(row["high_mode_seed"])
        paths = seed_paths(seed_index, seed_value)
        if not paths["complete"].is_file():
            break
        result = json.loads(paths["result"].read_text(encoding="utf-8"))
        if result.get("protocol_sha256") != protocol_sha256:
            raise RuntimeError("completed seed protocol mismatch")
        if int(result["seed_index"]) != seed_index:
            raise RuntimeError("completed seed order mismatch")
        if int(result["high_mode_seed"]) != seed_value:
            raise RuntimeError("completed seed value mismatch")
        completed.append(result)
    for row in schedule[len(completed) :]:
        paths = seed_paths(int(row["seed_index"]), int(row["high_mode_seed"]))
        if paths["complete"].is_file():
            raise RuntimeError("out-of-order seed completion detected")
    return completed


def pilot_row() -> dict[str, Any]:
    previous = json.loads(PREVIOUS_RESULT.read_text(encoding="utf-8"))
    comparison = previous["comparison"]
    q_advantage = float(comparison["MTS_q_band_distance"]) - float(
        comparison["CDM_q_band_distance"]
    )
    rmse_advantage = float(comparison["MTS_forward_RMSE_dex"]) - float(
        comparison["CDM_forward_RMSE_dex"]
    )
    return {
        "analysis_role": "pilot_excluded_from_inference",
        "seed_index": 0,
        "high_mode_seed": PILOT_SEED,
        "MTS_forward_q": comparison["MTS_forward_q"],
        "CDM_forward_q": comparison["CDM_forward_q"],
        "MTS_q_band_distance": comparison["MTS_q_band_distance"],
        "CDM_q_band_distance": comparison["CDM_q_band_distance"],
        "D_q_MTS_minus_CDM_band_distance": q_advantage,
        "MTS_forward_RMSE_dex": comparison["MTS_forward_RMSE_dex"],
        "CDM_forward_RMSE_dex": comparison["CDM_forward_RMSE_dex"],
        "D_RMSE_MTS_minus_CDM_dex": rmse_advantage,
        "joint_classification": classify_seed(
            q_advantage,
            rmse_advantage,
            float(comparison["q_numerical_envelope"]),
            float(comparison["RMSE_numerical_envelope"]),
        ),
        "included_in_confirmatory_statistics": False,
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }


def final_verdict(
    completed_count: int,
    q_statistics: dict[str, Any],
    rmse_statistics: dict[str, Any],
    cdm_joint_wins: int,
    mts_joint_wins: int,
    joint_sign_p: float | None,
) -> str:
    if completed_count < ENSEMBLE_SIZE:
        return "INCOMPLETE_PREDECLARED_ENSEMBLE_NO_PREFERENCE_ALLOWED"
    q_mean = float(q_statistics["mean"])
    rmse_mean = float(rmse_statistics["mean"])
    q_lower = float(q_statistics["bootstrap_95_lower"])
    q_upper = float(q_statistics["bootstrap_95_upper"])
    rmse_lower = float(rmse_statistics["bootstrap_95_lower"])
    rmse_upper = float(rmse_statistics["bootstrap_95_upper"])
    q_p = float(q_statistics["exact_two_sided_sign_flip_p"])
    rmse_p = float(rmse_statistics["exact_two_sided_sign_flip_p"])
    joint_pass = joint_sign_p is not None and joint_sign_p <= ALPHA
    if (
        q_mean > 0.0
        and rmse_mean > 0.0
        and q_lower > 0.0
        and rmse_lower > 0.0
        and q_p <= ALPHA
        and rmse_p <= ALPHA
        and cdm_joint_wins > mts_joint_wins
        and joint_pass
    ):
        return "CDM_PREFERRED_WITHIN_THIS_LOCKED_FORMATION_GATE"
    if (
        q_mean < 0.0
        and rmse_mean < 0.0
        and q_upper < 0.0
        and rmse_upper < 0.0
        and q_p <= ALPHA
        and rmse_p <= ALPHA
        and mts_joint_wins > cdm_joint_wins
        and joint_pass
    ):
        return "MTS_PREFERRED_WITHIN_THIS_LOCKED_FORMATION_GATE"
    return "STATISTICAL_DRAW_OR_METRIC_SPLIT_WITHIN_THIS_LOCKED_FORMATION_GATE"


def aggregate(protocol: dict[str, Any]) -> dict[str, Any]:
    schedule = derive_seed_schedule()
    completed = completed_seed_results(schedule, protocol["protocol_sha256"])
    q_values = np.asarray(
        [row["D_q_MTS_minus_CDM_band_distance"] for row in completed],
        dtype=float,
    )
    rmse_values = np.asarray(
        [row["D_RMSE_MTS_minus_CDM_dex"] for row in completed], dtype=float
    )
    q_statistics = metric_statistics("D_q_band_distance", q_values, 1)
    rmse_statistics = metric_statistics("D_RMSE_dex", rmse_values, 2)
    cdm_joint_wins = sum(
        row["joint_classification"] == "CDM_JOINT_WIN" for row in completed
    )
    mts_joint_wins = sum(
        row["joint_classification"] == "MTS_JOINT_WIN" for row in completed
    )
    joint_ties = len(completed) - cdm_joint_wins - mts_joint_wins
    joint_sign_p = exact_two_sided_sign_p(cdm_joint_wins, mts_joint_wins)
    verdict = final_verdict(
        len(completed),
        q_statistics,
        rmse_statistics,
        cdm_joint_wins,
        mts_joint_wins,
        joint_sign_p,
    )
    score_rows = [pilot_row()]
    for row in completed:
        score_rows.append(
            {
                "analysis_role": "confirmatory",
                **row,
                "included_in_confirmatory_statistics": True,
            }
        )
    write_csv(SEED_SCORE_CSV, score_rows)
    write_csv(STATISTICS_CSV, [q_statistics, rmse_statistics])
    status_rows: list[dict[str, Any]] = []
    for row in schedule:
        paths = seed_paths(int(row["seed_index"]), int(row["high_mode_seed"]))
        status_value = "PENDING"
        wall_seconds: float | None = None
        if paths["status"].is_file():
            status = json.loads(paths["status"].read_text(encoding="utf-8"))
            status_value = str(status["state"])
            wall_seconds = status.get("wall_seconds")
        status_rows.append(
            {
                "seed_index": row["seed_index"],
                "high_mode_seed": row["high_mode_seed"],
                "state": status_value,
                "wall_seconds": wall_seconds,
                "complete_marker_exists": paths["complete"].is_file(),
                "protocol_sha256": protocol["protocol_sha256"],
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    write_csv(STATUS_CSV, status_rows)
    route_decision = (
        verdict
        if len(completed) == ENSEMBLE_SIZE
        else (
            f"LOCKED_CONFIRMATORY_ENSEMBLE_IN_PROGRESS_{len(completed)}_OF_"
            f"{ENSEMBLE_SIZE}_PILOT_EXCLUDED_NO_MODEL_PREFERENCE_ALLOWED"
        )
    )
    write_csv(
        DECISION_CSV,
        [
            {
                "route_decision": route_decision,
                "completed_confirmatory_seeds": len(completed),
                "final_seed_count": ENSEMBLE_SIZE,
                "pilot_excluded": True,
                "next_target": (
                    "run_next_predeclared_seed"
                    if len(completed) < ENSEMBLE_SIZE
                    else "interpret_locked_ensemble_without_retuning"
                ),
                "new_coupling_added": False,
                "local_GR_Newton_Maxwell_branch_modified": False,
                "target_used_to_define_evolution": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        ],
    )
    result = {
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "protocol_sha256": protocol["protocol_sha256"],
        "pilot_seed": PILOT_SEED,
        "pilot_excluded_from_inference": True,
        "completed_confirmatory_seeds": len(completed),
        "final_confirmatory_seed_count": ENSEMBLE_SIZE,
        "q_statistics": q_statistics,
        "RMSE_statistics": rmse_statistics,
        "CDM_joint_wins": cdm_joint_wins,
        "MTS_joint_wins": mts_joint_wins,
        "joint_ties_or_splits": joint_ties,
        "joint_exact_two_sided_sign_p": joint_sign_p,
        "verdict": verdict,
        "route_decision": route_decision,
        "formalization_workbench_tree_sha256": resolution.Q.tree_digest(FORMAL),
        "valid_for_claim": False,
    }
    resolution.Q.write_json(RESULT_JSON, result)
    return result


def add_validation(
    rows: list[dict[str, Any]], check_id: str, passed: bool, evidence: Any
) -> None:
    rows.append(
        {
            "check_id": check_id,
            "passed": bool(passed),
            "evidence": json.dumps(evidence, sort_keys=True, default=str),
        }
    )


def validate(protocol: dict[str, Any], result: dict[str, Any]) -> list[dict[str, Any]]:
    schedule = derive_seed_schedule()
    completed = completed_seed_results(schedule, protocol["protocol_sha256"])
    rows: list[dict[str, Any]] = []
    sources = source_paths()
    add_validation(
        rows,
        "all_sources_exist",
        all(path.is_file() for path in sources.values()),
        {key: str(path) for key, path in sources.items()},
    )
    add_validation(
        rows,
        "formalization_workbench_unchanged",
        resolution.Q.tree_digest(FORMAL) == FORMAL_DIGEST_LOCK,
        resolution.Q.tree_digest(FORMAL),
    )
    add_validation(
        rows,
        "protocol_locked_before_first_seed",
        bool(protocol["locked_before_first_confirmatory_seed"]),
        protocol["locked_at_utc"],
    )
    add_validation(
        rows,
        "protocol_hash_reproduces",
        stable_digest(protocol["settings"]) == protocol["protocol_sha256"],
        protocol["protocol_sha256"],
    )
    seeds = [int(row["high_mode_seed"]) for row in schedule]
    add_validation(
        rows,
        "schedule_complete_unique_and_pilot_excluded",
        len(seeds) == ENSEMBLE_SIZE
        and len(set(seeds)) == ENSEMBLE_SIZE
        and PILOT_SEED not in seeds,
        seeds,
    )
    add_validation(
        rows,
        "settings_locked_to_5175",
        protocol["settings"]["source_grid"] == resolution.SOURCE_GRID
        and protocol["settings"]["particle_grid"] == resolution.PARTICLE_GRID
        and protocol["settings"]["global_force_grid"]
        == resolution.ZOOM.GLOBAL_FORCE_GRID
        and protocol["settings"]["local_force_grid"]
        == resolution.DYNAMICS.LOCAL_GRID,
        protocol["settings"],
    )
    add_validation(
        rows,
        "completed_seeds_sequential",
        [int(row["seed_index"]) for row in completed]
        == list(range(1, len(completed) + 1)),
        [int(row["seed_index"]) for row in completed],
    )
    add_validation(
        rows,
        "completed_low_modes_exact",
        all(
            float(row["shared_standardized_mode_maximum_error"]) == 0.0
            and float(row["Hermitian_inverse_maximum_imaginary"]) < 1.0e-12
            for row in completed
        ),
        len(completed),
    )
    add_validation(
        rows,
        "completed_constraints_and_conservation",
        all(
            float(row["maximum_constraint_error"]) < 1.0e-12
            and float(row["maximum_imaginary_residual"]) < 1.0e-12
            and float(row["maximum_transfer_relative_residual"]) < 1.0e-10
            and float(row["maximum_angular_momentum_relative_residual"])
            < 1.0e-10
            for row in completed
        ),
        len(completed),
    )
    add_validation(
        rows,
        "completed_rows_nonclaim_and_target_blind",
        all(
            row["valid_for_claim"] is False
            and row["target_used_to_define_evolution"] is False
            for row in completed
        ),
        len(completed),
    )
    add_validation(
        rows,
        "incomplete_ensemble_cannot_prefer_model",
        len(completed) == ENSEMBLE_SIZE
        or result["verdict"]
        == "INCOMPLETE_PREDECLARED_ENSEMBLE_NO_PREFERENCE_ALLOWED",
        result["verdict"],
    )
    add_validation(
        rows,
        "pilot_excluded_from_inference",
        bool(result["pilot_excluded_from_inference"])
        and int(result["pilot_seed"]) == PILOT_SEED,
        PILOT_SEED,
    )
    failed = [row for row in rows if not row["passed"]]
    if failed:
        raise RuntimeError(f"validation failures: {failed}")
    write_csv(VALIDATION_CSV, rows)
    return rows


def format_statistic(statistic: dict[str, Any]) -> str:
    if int(statistic["completed_confirmatory_seeds"]) == 0:
        return "not yet available"
    return (
        f"mean={statistic['mean']}, median={statistic['median']}, "
        f"bootstrap95=[{statistic['bootstrap_95_lower']},"
        f"{statistic['bootstrap_95_upper']}], "
        f"exact sign-flip p={statistic['exact_two_sided_sign_flip_p']}"
    )


def document_text(
    protocol: dict[str, Any], result: dict[str, Any], validation_count: int
) -> str:
    schedule = derive_seed_schedule()
    schedule_lines = "\n".join(
        f"- {int(row['seed_index']):02d} -> {row['high_mode_seed']}"
        for row in schedule
    )
    return f"""# 5176 - Predeclared paired high-mode seed ensemble

Marker: {MARKER}.

Date: {CHECKED_DATE}.

## Decision discipline

Checkpoint 5175 showed a resolved MTS/CDM difference in one newly resolved
high-mode realization. This checkpoint freezes the required ensemble before
looking at another realization. The already observed seed {PILOT_SEED} is a
pilot and is excluded from confirmatory statistics.

The protocol hash is {protocol['protocol_sha256']}. It locks all checkpoint
5175 physics, grids, spectra, low modes, source history, score, numerical
envelopes and stopping rules. Each invocation runs only the next scheduled
seed, so a completed seed remains below the four-hour cap and interrupted
work can resume from phase caches.

## Frozen seed schedule

{schedule_lines}

No seed may be skipped, replaced, reordered or selected after inspecting an
outcome. The six-seed point is descriptive only. Model preference is assessed
once, after all {ENSEMBLE_SIZE} confirmatory seeds.

## Locked estimands and rule

D_q=d_q(MTS)-d_q(CDM) and D_R=RMSE(MTS)-RMSE(CDM). Positive values favor CDM;
negative values favor MTS. A seed is a joint win only if both advantages
exceed their inherited numerical envelopes in the same direction.

At the final seed, both paired means and deterministic 95 percent bootstrap
intervals must have the same nonzero sign, both exact two-sided sign-flip
tests must pass p<={ALPHA}, and the joint-win sign test must pass the same
threshold. Otherwise the result is a statistical draw or metric split. This
rule treats MTS and CDM symmetrically and does not require either theory to
win by a large information-criterion margin.

## Current execution state

Completed confirmatory seeds: {result['completed_confirmatory_seeds']} of
{result['final_confirmatory_seed_count']}.

- q-band-distance statistic: {format_statistic(result['q_statistics'])}
- RMSE statistic: {format_statistic(result['RMSE_statistics'])}
- joint outcomes: CDM {result['CDM_joint_wins']}, MTS
  {result['MTS_joint_wins']}, tie/split {result['joint_ties_or_splits']}
- current verdict: {result['verdict']}
- route decision: {result['route_decision']}

Until all twelve seeds complete, no model-preference statement is allowed.
Even a final preference would apply only to this locked UGC09133 formation
gate, not to the full theory.

All {validation_count} current validations pass. Every row remains nonclaim,
the protected formalization-workbench digest remains
{result['formalization_workbench_tree_sha256']}, and no GitHub action was
performed by checkpoint 5176.
"""


def refresh_outputs(protocol: dict[str, Any]) -> dict[str, Any]:
    sources = source_paths()
    source_hashes_before = {
        key: resolution.Q.file_digest(path) for key, path in sources.items()
    }
    provenance_rows = [
        {
            "source_id": key,
            "local_path": str(path),
            "sha256": source_hashes_before[key],
            "role": "read_only_input",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for key, path in sources.items()
    ]
    write_csv(PROVENANCE_CSV, provenance_rows)
    result = aggregate(protocol)
    validations = validate(protocol, result)
    source_hashes_after = {
        key: resolution.Q.file_digest(path) for key, path in sources.items()
    }
    if source_hashes_before != source_hashes_after:
        raise RuntimeError("source hashes changed while refreshing outputs")
    DOCUMENT.write_text(
        document_text(protocol, result, len(validations)), encoding="utf-8"
    )
    return result


def next_pending_row(
    schedule: list[dict[str, Any]], protocol_sha256: str
) -> dict[str, Any] | None:
    completed = completed_seed_results(schedule, protocol_sha256)
    if len(completed) == len(schedule):
        return None
    return schedule[len(completed)]


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--initialize", action="store_true")
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--run-next", action="store_true")
    arguments = parser.parse_args()
    missing = [str(path) for path in source_paths().values() if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing sources: {missing}")
    protocol = ensure_protocol()
    if arguments.dry_run:
        schedule = derive_seed_schedule()
        next_row = next_pending_row(schedule, protocol["protocol_sha256"])
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "protocol_sha256": protocol["protocol_sha256"],
                    "next_seed": next_row,
                    "settings": protocol["settings"],
                    "formalization_digest": resolution.Q.tree_digest(FORMAL),
                },
                indent=2,
            )
        )
        return
    if arguments.run_next:
        schedule = derive_seed_schedule()
        next_row = next_pending_row(schedule, protocol["protocol_sha256"])
        if next_row is None:
            print("all predeclared seeds are complete")
        else:
            run_seed(protocol, next_row)
    result = refresh_outputs(protocol)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

