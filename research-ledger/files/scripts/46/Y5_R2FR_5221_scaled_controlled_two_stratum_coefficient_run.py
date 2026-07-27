from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5221"
RUN_DIRECTORY = SOURCE / "runs" / "scaled_controlled_two_stratum_v1"
CLASSIFIER_CACHE = RUN_DIRECTORY / "grouped-classifier-cache"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5220 = (
    POST
    / "scripts"
    / "Y5_R2FR_5220_fresh_predeclared_grouped_classifier_A00_pilot.py"
)
SCRIPT_5219 = (
    POST
    / "scripts"
    / "Y5_R2FR_5219_general_grouped_owned_direct_classifier.py"
)
SCRIPT_5215_TRANSPORT = (
    POST
    / "scripts"
    / "Y5_R2FR_5215_transport_invalid_full_homotopy_repair.py"
)
SCRIPT_5214 = (
    POST
    / "scripts"
    / "Y5_R2FR_5214_A00_source_pole_control_variate.py"
)
SCRIPT_5212 = (
    POST
    / "scripts"
    / "Y5_R2FR_5212_fresh_crossed_hhh_two_stratum_pilot.py"
)

SOURCE_5212 = POST / "source-intake" / "functional_rg" / "5212"
SOURCE_5214 = POST / "source-intake" / "functional_rg" / "5214"
SOURCE_5219 = POST / "source-intake" / "functional_rg" / "5219"
SOURCE_5220 = POST / "source-intake" / "functional_rg" / "5220"
MANIFEST_5212 = SOURCE_5212 / "locked_two_stratum_pilot_manifest.json"
RESULT_5212 = SOURCE_5212 / "fresh_two_stratum_pilot_results.json"
CONFIG_5212 = (
    SOURCE_5212 / "runs" / "fresh_two_stratum_pilot_v2" / "config.json"
)
RUN_5212 = SOURCE_5212 / "runs" / "fresh_two_stratum_pilot_v2"
PROVENANCE_5212 = SOURCE_5212 / "PROVENANCE.md"
CONTROL_AUDIT_5214 = SOURCE_5214 / "A00_source_pole_family_audit.json"
CONTROL_EVENTS_5214 = SOURCE_5214 / "A00_event_decomposition.csv"
CLASSIFIER_GATE_5219 = (
    SOURCE_5219 / "general_grouped_owned_direct_classifier_gate.json"
)
MANIFEST_5220 = SOURCE_5220 / "frozen_fresh_grouped_classifier_manifest.json"
RESULT_5220 = SOURCE_5220 / "fresh_grouped_classifier_A00_pilot_results.json"
TRANSPORT_LOCK = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5215"
    / "frozen_transport_repair_lock.json"
)

MANIFEST = SOURCE / "frozen_scaled_controlled_manifest.json"
FROZEN_CONFIG = SOURCE / "frozen_scaled_controlled_config.json"
FROZEN_SCHEDULE = SOURCE / "frozen_scaled_controlled_schedule.csv"
PROTOCOL_LOCK = SOURCE / "frozen_scaled_controlled_protocol_lock.json"
ACTIVATION = SOURCE / "scaled_controlled_activation.json"
ALLOCATION = SOURCE / "allocation_and_stopping_derivation.json"
RESULT = SOURCE / "scaled_controlled_two_stratum_results.json"
EVENT_ROWS = SOURCE / "scaled_controlled_event_rows.csv"
CONTROL_ROWS = SOURCE / "scaled_controlled_A00_event_rows.csv"
CLASSIFIER_AUDIT = SOURCE / "general_grouped_classifier_runtime_audit.json"
STATUS = RUN_DIRECTORY / "status.json"
DOCUMENT = (
    POST / "5221-Y5-R2FR-scaled-controlled-two-stratum-coefficient-run.md"
)
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5221_VALIDATION.csv"
RESUME = SOURCE / "RESUME.md"

MARKER = "MTS_5221_SCALED_CONTROLLED_TWO_STRATUM_COEFFICIENT_RUN"
REVISION = "scaled-controlled-two-stratum-v1"
RUN_ID = "scaled_controlled_two_stratum_v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
MAXIMUM_WALL_HOURS = 4.0
FULL_SEEDS = (522101, 522102)
TOPOLOGICAL_SEEDS = tuple(range(522111, 522135))
TRANCHE_FULL = {1: (522101,), 2: (522102,)}
TRANCHE_TOPOLOGICAL = {
    1: tuple(range(522111, 522123)),
    2: tuple(range(522123, 522135)),
}
ARGUMENT_IDS = (
    "A00",
    "A01",
    "A02",
    "A03",
    "A04",
    "A10",
    "A11",
    "A12",
    "A13",
    "A14",
)
EPSILON_IDS = ("E040", "E020")
PHYSICAL_COSINES = np.asarray(
    (-0.6, -0.3, 0.0, 0.3, 0.6), dtype=np.float64
)
PHYSICAL_SHAPE = 1.0 - PHYSICAL_COSINES**2
LOCAL_WEIGHTS = PHYSICAL_SHAPE / float(PHYSICAL_SHAPE @ PHYSICAL_SHAPE)
KNOWN_MASTER_LOCAL_COEFFICIENT = 161.42318077192922


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5220 = load_module(SCRIPT_5220, "mts_5220_for_5221")
M5215 = M5220.M5215
M5212 = M5215.M5212


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for candidate in sorted(item for item in path.rglob("*") if item.is_file()):
        value.update(candidate.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(candidate).encode("ascii"))
    return value.hexdigest()


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True), encoding="utf-8"
    )
    os.replace(temporary, path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def row_complex(value: Any) -> complex:
    if isinstance(value, str):
        return complex(value)
    return complex(float(value["real"]), float(value["imaginary"]))


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def scalar_summary(values: np.ndarray) -> dict[str, Any]:
    array = np.asarray(values, dtype=np.float64)
    count = len(array)
    return {
        "count": count,
        "mean": float(np.mean(array)) if count else None,
        "sample_standard_deviation": (
            float(np.std(array, ddof=1)) if count >= 2 else None
        ),
        "standard_error": (
            float(np.std(array, ddof=1) / math.sqrt(count))
            if count >= 2
            else None
        ),
        "minimum": float(np.min(array)) if count else None,
        "maximum": float(np.max(array)) if count else None,
        "median": float(np.median(array)) if count else None,
    }


def locked_source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5220,
        SCRIPT_5219,
        SCRIPT_5215_TRANSPORT,
        SCRIPT_5214,
        SCRIPT_5212,
        MANIFEST_5212,
        RESULT_5212,
        CONFIG_5212,
        PROVENANCE_5212,
        CONTROL_AUDIT_5214,
        CONTROL_EVENTS_5214,
        CLASSIFIER_GATE_5219,
        MANIFEST_5220,
        RESULT_5220,
        TRANSPORT_LOCK,
    )
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing locked sources: {missing}")
    return [
        {"path": relative(path), "sha256": digest(path)} for path in paths
    ]


def prior_seed_occurrences() -> list[dict[str, Any]]:
    functional = POST / "source-intake" / "functional_rg"
    candidates = {
        *functional.rglob("config.json"),
        *functional.rglob("*manifest*.json"),
        *functional.rglob("*activation*.json"),
    }
    expression = re.compile(
        r"(?<![0-9])(?:"
        + "|".join(str(seed) for seed in (*FULL_SEEDS, *TOPOLOGICAL_SEEDS))
        + r")(?![0-9])"
    )
    source_resolved = SOURCE.resolve()
    rows: list[dict[str, Any]] = []
    for candidate in sorted(candidates):
        try:
            candidate.resolve().relative_to(source_resolved)
            continue
        except ValueError:
            pass
        matches = sorted(
            {
                int(value)
                for value in expression.findall(
                    candidate.read_text(encoding="utf-8", errors="ignore")
                )
            }
        )
        if matches:
            rows.append({"path": relative(candidate), "seeds": matches})
    return rows


def allocation_derivation() -> dict[str, Any]:
    result_5212 = read_json(RESULT_5212)["analysis"]
    audit_5214 = read_json(CONTROL_AUDIT_5214)["permutation_control"]
    full_count = int(result_5212["full_naive_local"]["count"])
    full_standard_error = float(
        result_5212["full_naive_local"]["real_standard_error"]
    )
    sigma_full = full_standard_error * math.sqrt(full_count)
    sigma_topological = float(
        audit_5214["topological_local_real_variance"]["adjusted"][
            "sample_standard_deviation"
        ]
    )
    cost_full = float(result_5212["mean_full_event_runtime_seconds"])
    cost_topological = float(
        result_5212["mean_topological_event_runtime_seconds"]
    )
    optimal_ratio = (sigma_topological / sigma_full) * math.sqrt(
        cost_full / cost_topological
    )
    frozen_ratio = 12.0
    estimated_tranche_seconds = cost_full + 12.0 * cost_topological
    result = {
        "checkpoint": 5221,
        "checkpoint_marker": MARKER,
        "derivation": (
            "For independent stratum means with per-event variances "
            "sigma_f^2 and sigma_t^2 and costs c_f and c_t, minimizing "
            "sigma_f^2/n_f + sigma_t^2/n_t at fixed cost gives "
            "n_t/n_f=(sigma_t/sigma_f)*sqrt(c_f/c_t)."
        ),
        "source_full_naive_real_sample_standard_deviation": sigma_full,
        "source_controlled_topological_real_sample_standard_deviation": (
            sigma_topological
        ),
        "source_mean_full_event_runtime_seconds": cost_full,
        "source_mean_topological_event_runtime_seconds": cost_topological,
        "derived_optimal_topological_per_full_ratio": optimal_ratio,
        "frozen_integer_topological_per_full_ratio": frozen_ratio,
        "rounding_rule": (
            "round 11.7194556826 upward to twelve; do not estimate or retune "
            "the ratio from checkpoint-5221 outcomes"
        ),
        "new_full_event_count": len(FULL_SEEDS),
        "new_topological_event_count": len(TOPOLOGICAL_SEEDS),
        "tranches": {
            str(tranche): {
                "full_seeds": list(TRANCHE_FULL[tranche]),
                "topological_seeds": list(TRANCHE_TOPOLOGICAL[tranche]),
                "estimated_runtime_seconds": estimated_tranche_seconds,
            }
            for tranche in (1, 2)
        },
        "estimated_total_runtime_seconds": 2.0 * estimated_tranche_seconds,
        "stopping_contract": {
            "both_tranches_are_mandatory": True,
            "no_favourable_or_unfavourable_coefficient_stopping_after_tranche_1": (
                True
            ),
            "permitted_early_stops": [
                "wall-clock cap",
                "explicit user pause",
                "first failed job",
                "first completed-unconverged job",
                "protocol digest mismatch",
            ],
            "threshold_retuning_after_outcomes_allowed": False,
        },
        "tail_contract": {
            "minimum_controlled_topological_events": 30,
            "maximum_leave_one_out_shift_standard_errors": 0.5,
            "maximum_ordered_half_difference_sigma": 1.0,
            "maximum_absolute_event_share": 0.2,
            "new_only_n24_cannot_close_tail_gate": True,
            "legacy_pool_target_count_after_compatibility": 36,
        },
        "coefficient_precision_contract": {
            "maximum_real_standard_error_fraction": 0.2,
            "real_scale_floor": 1.0,
            "maximum_imaginary_mean_standard_errors": 3.0,
            "maximum_nonlocal_mismatch_sigma": 4.0,
        },
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    if not 11.0 < optimal_ratio < 13.0:
        raise RuntimeError(f"allocation evidence changed: {optimal_ratio}")
    return result


def make_manifest() -> dict[str, Any]:
    control_manifest = read_json(MANIFEST_5220)
    control_result = read_json(RESULT_5220)
    if not (
        control_result["fresh_control_pilot_passed"]
        and control_result["scale_decision"]
        == "AUTHORIZE_SCALED_CONTROLLED_TOPOLOGICAL_RUN"
    ):
        raise RuntimeError("checkpoint-5220 did not authorize scaling")
    occurrences = prior_seed_occurrences()
    if occurrences:
        raise RuntimeError(f"reserved checkpoint-5221 seeds occur: {occurrences}")
    thresholds = {
        **control_manifest["acceptance_thresholds"],
        "minimum_nonzero_control_events": 4,
        "minimum_tail_event_count": 30,
        "maximum_leave_one_out_shift_standard_errors": 0.5,
        "maximum_ordered_half_difference_sigma": 1.0,
        "maximum_absolute_event_share": 0.2,
        "maximum_real_standard_error_fraction": 0.2,
        "real_precision_scale_floor": 1.0,
        "maximum_imaginary_mean_standard_errors": 3.0,
        "maximum_nonlocal_mismatch_sigma": 4.0,
    }
    return {
        "checkpoint": 5221,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "locked_date": "2026-07-25",
        "design_source": relative(ALLOCATION),
        "locked_sources": locked_source_rows(),
        "fresh_full_scramble_seeds": list(FULL_SEEDS),
        "fresh_topological_scramble_seeds": list(TOPOLOGICAL_SEEDS),
        "fresh_high_scramble_seeds": list(FULL_SEEDS),
        "fresh_low_scramble_seeds": list(TOPOLOGICAL_SEEDS),
        "required_base_argument_ids": list(ARGUMENT_IDS),
        "epsilon_ids": list(EPSILON_IDS),
        "profile": "primary24",
        "full_event_count": len(FULL_SEEDS),
        "topological_event_count": len(TOPOLOGICAL_SEEDS),
        "topological_per_full_ratio": 12.0,
        "expected_job_count": (
            (len(FULL_SEEDS) + len(TOPOLOGICAL_SEEDS))
            * len(ARGUMENT_IDS)
            * len(EPSILON_IDS)
        ),
        "tranches": {
            str(tranche): {
                "full_seeds": list(TRANCHE_FULL[tranche]),
                "topological_seeds": list(TRANCHE_TOPOLOGICAL[tranche]),
                "expected_job_count": 260,
            }
            for tranche in (1, 2)
        },
        "control_identity": control_manifest["control_identity"],
        "dominant_family_signature": control_manifest[
            "dominant_family_signature"
        ],
        "permuted_family_signature": control_manifest[
            "permuted_family_signature"
        ],
        "partition_ratio": control_manifest["partition_ratio"],
        "real_control_coefficient": 1.0,
        "imaginary_control_coefficient": 0.0,
        "control_application": "real A00 component only before local projection",
        "physical_A00_weight_at_z_minus_0p6": -0.008,
        "epsilon_extrapolation": "A00(0)=2*A00(E020)-A00(E040)",
        "acceptance_thresholds": thresholds,
        "argument_topology_rule": control_manifest["argument_topology_rule"],
        "epsilon_topology_rule": control_manifest["epsilon_topology_rule"],
        "quadrature_breakpoint_rule": control_manifest[
            "quadrature_breakpoint_rule"
        ],
        "maximum_wall_hours_per_invocation": MAXIMUM_WALL_HOURS,
        "stop_on_first_failed_or_unconverged_job": True,
        "resume_completed_converged_jobs": True,
        "both_tranches_mandatory": True,
        "interim_coefficient_stopping_allowed": False,
        "threshold_retuning_after_outcomes_allowed": False,
        "legacy_pooling_rule": (
            "report new-only and pooled estimates separately; pool checkpoint-"
            "5212 events only after source, estimator, epsilon, argument, "
            "profile, control-replay and converged-job compatibility all pass"
        ),
        "prior_seed_occurrences_at_lock": occurrences,
        "allocation_locked_before_fresh_outcomes": True,
        "pole_model_and_smooth_must_remain_paired": True,
        "unsafe_reciprocal_pairs_evaluate_both_roots": True,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def make_config(manifest: dict[str, Any]) -> dict[str, Any]:
    config = M5212.make_config(manifest, RUN_ID)
    control_manifest = read_json(MANIFEST_5220)
    config["checkpoint_marker"] = MARKER
    config["schema_revision"] = REVISION
    config["pilot_manifest"] = str(MANIFEST)
    config["pilot_manifest_digest"] = digest(MANIFEST)
    config["two_stratum_contract"]["pilot_only"] = False
    config["two_stratum_contract"]["controlled_A00_real"] = True
    config["two_stratum_contract"]["allocation_ratio"] = 12.0
    config["fresh_A00_control_contract"] = {
        "control_identity": manifest["control_identity"],
        "dominant_family_signature": manifest[
            "dominant_family_signature"
        ],
        "permuted_family_signature": manifest[
            "permuted_family_signature"
        ],
        "partition_ratio": manifest["partition_ratio"],
        "real_control_coefficient": 1.0,
        "imaginary_control_coefficient": 0.0,
        "control_application": manifest["control_application"],
        "acceptance_thresholds": manifest["acceptance_thresholds"],
        "diagnostic_only": control_manifest["diagnostic_only"],
        "scale_decision": (
            "fixed control used in checkpoint-5221 coefficient run"
        ),
    }
    config["predeclared_transport_invalid_fallback"] = {
        "runner": str(SCRIPT_5215_TRANSPORT),
        "runner_sha256": digest(SCRIPT_5215_TRANSPORT),
        "lock": str(TRANSPORT_LOCK),
        "lock_sha256": digest(TRANSPORT_LOCK),
        "trigger": (
            "reject transported topology if either locked root diagnostic "
            "fails; use unchanged original full homotopy"
        ),
    }
    config["general_grouped_owned_direct_classifier"] = {
        "runner": str(SCRIPT_5219),
        "runner_sha256": digest(SCRIPT_5219),
        "gate": str(CLASSIFIER_GATE_5219),
        "gate_sha256": digest(CLASSIFIER_GATE_5219),
        "contract": read_json(CLASSIFIER_GATE_5219)["classifier_contract"],
        "unresolved_action": "fail_closed",
    }
    config["source_files"][str(Path(__file__).resolve())] = digest(
        Path(__file__).resolve()
    )
    for row in manifest["locked_sources"]:
        config["source_files"][str(ROOT / row["path"])] = row["sha256"]
    config.pop("config_digest", None)
    config["config_digest"] = M5215.canonical_digest(config)
    return config


def build_schedule(
    config: dict[str, Any], manifest: dict[str, Any]
) -> list[dict[str, Any]]:
    events = {int(row["seed"]): row for row in config["events"]}
    jobs: list[dict[str, Any]] = []
    for tranche in (1, 2):
        groups = [
            *(("full", seed) for seed in TRANCHE_FULL[tranche]),
            *(
                ("topological", seed)
                for seed in TRANCHE_TOPOLOGICAL[tranche]
            ),
        ]
        for event_order, (stratum, seed) in enumerate(groups, start=1):
            for job in M5212.event_jobs(
                events[seed], stratum, manifest
            ):
                jobs.append(
                    {
                        **job,
                        "tranche": tranche,
                        "tranche_event_order": event_order,
                    }
                )
    if len(jobs) != int(manifest["expected_job_count"]):
        raise RuntimeError("checkpoint-5221 schedule size changed")
    return jobs


def schedule_rows(jobs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"schedule_index": index, **job}
        for index, job in enumerate(jobs, start=1)
    ]


def protocol_lock(
    manifest: dict[str, Any],
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
) -> dict[str, Any]:
    if PROTOCOL_LOCK.exists():
        locked = read_json(PROTOCOL_LOCK)
        expected = locked["contract"]
        checks = {
            "manifest_sha256": digest(MANIFEST),
            "config_sha256": digest(FROZEN_CONFIG),
            "schedule_sha256": digest(FROZEN_SCHEDULE),
            "runner_sha256": digest(Path(__file__).resolve()),
        }
        if any(expected[key] != value for key, value in checks.items()):
            raise RuntimeError("checkpoint-5221 frozen protocol digest changed")
        return locked
    outcome_files = [
        *RUN_DIRECTORY.glob("jobs/*.json"),
        *RUN_DIRECTORY.glob("topological-jobs/*.json"),
    ]
    if outcome_files:
        raise RuntimeError("outcomes exist before checkpoint-5221 lock")
    locked = {
        "checkpoint": 5221,
        "checkpoint_marker": MARKER,
        "contract": {
            "manifest_sha256": digest(MANIFEST),
            "config_sha256": digest(FROZEN_CONFIG),
            "schedule_sha256": digest(FROZEN_SCHEDULE),
            "runner_sha256": digest(Path(__file__).resolve()),
            "allocation_sha256": digest(ALLOCATION),
            "fresh_seeds": [*FULL_SEEDS, *TOPOLOGICAL_SEEDS],
            "required_tranches": [1, 2],
            "threshold_retuning_after_outcomes_allowed": False,
        },
        "outcomes_present_at_lock": False,
        "valid_for_numeric_UV_claim": False,
    }
    atomic_json(PROTOCOL_LOCK, locked)
    return locked


def prepare() -> tuple[
    dict[str, Any], dict[str, Any], list[dict[str, Any]], dict[str, Any]
]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    RUN_DIRECTORY.mkdir(parents=True, exist_ok=True)
    if ALLOCATION.exists():
        allocation = read_json(ALLOCATION)
    else:
        allocation = allocation_derivation()
        atomic_json(ALLOCATION, allocation)
    if MANIFEST.exists():
        manifest = read_json(MANIFEST)
    else:
        manifest = make_manifest()
        atomic_json(MANIFEST, manifest)
    if manifest["fresh_full_scramble_seeds"] != list(FULL_SEEDS):
        raise RuntimeError("frozen full seeds changed")
    if manifest["fresh_topological_scramble_seeds"] != list(
        TOPOLOGICAL_SEEDS
    ):
        raise RuntimeError("frozen topological seeds changed")
    if FROZEN_CONFIG.exists():
        config = read_json(FROZEN_CONFIG)
    else:
        config = make_config(manifest)
        atomic_json(FROZEN_CONFIG, config)
    jobs = build_schedule(config, manifest)
    if not FROZEN_SCHEDULE.exists():
        write_csv(FROZEN_SCHEDULE, schedule_rows(jobs))
    lock = protocol_lock(manifest, config, jobs)
    activation = {
        "checkpoint": 5221,
        "checkpoint_marker": MARKER,
        "protocol_lock_sha256": digest(PROTOCOL_LOCK),
        "manifest_sha256": digest(MANIFEST),
        "config_sha256": digest(FROZEN_CONFIG),
        "schedule_sha256": digest(FROZEN_SCHEDULE),
        "allocation_sha256": digest(ALLOCATION),
        "fresh_seed_count": len(FULL_SEEDS) + len(TOPOLOGICAL_SEEDS),
        "expected_job_count": len(jobs),
        "prior_seed_occurrences_at_lock": manifest[
            "prior_seed_occurrences_at_lock"
        ],
        "control_scale_authorized_by_5220": True,
        "both_tranches_mandatory": True,
        "threshold_retuning_after_outcomes_allowed": False,
        "valid_for_numeric_UV_claim": False,
    }
    atomic_json(ACTIVATION, activation)
    if lock["contract"]["allocation_sha256"] != digest(ALLOCATION):
        raise RuntimeError("allocation derivation changed after lock")
    return manifest, config, jobs, activation


def run_counts(
    config: dict[str, Any], jobs: list[dict[str, Any]]
) -> dict[str, int]:
    return M5212.run_counts(RUN_DIRECTORY, config, jobs)


def tranche_counts(
    config: dict[str, Any], jobs: list[dict[str, Any]]
) -> dict[str, dict[str, int]]:
    return {
        str(tranche): run_counts(
            config, [job for job in jobs if int(job["tranche"]) == tranche]
        )
        for tranche in (1, 2)
    }


def event_is_complete(
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
    stratum: str,
    seed: int,
) -> bool:
    return M5212.event_complete(
        RUN_DIRECTORY, config, jobs, stratum, seed
    )


def controlled_topological_event(
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
    seed: int,
    manifest: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    event = M5212.projected_event(
        RUN_DIRECTORY, config, jobs, "topological", seed
    )
    selected = {
        (job["epsilon_id"], job["base_argument_id"]): job
        for job in jobs
        if job["stratum"] == "topological" and int(job["seed"]) == seed
    }
    rows = {
        epsilon_id: read_json(
            M5212.output_path(
                RUN_DIRECTORY, selected[(epsilon_id, "A00")]
            )
        )
        for epsilon_id in EPSILON_IDS
    }
    raw_e040 = row_complex(
        rows["E040"]["normalized_topological_D_hhh_over_G3"]
    )
    raw_e020 = row_complex(
        rows["E020"]["normalized_topological_D_hhh_over_G3"]
    )
    control_e040 = row_complex(
        rows["E040"]["permutation_zero_control"]
    )
    control_e020 = row_complex(
        rows["E020"]["permutation_zero_control"]
    )
    physical_weight = float(
        manifest["physical_A00_weight_at_z_minus_0p6"]
    )
    raw_a00 = physical_weight * (2.0 * raw_e020 - raw_e040)
    control = physical_weight * (
        2.0 * control_e020 - control_e040
    )
    adjusted_a00 = complex(raw_a00.real - control.real, raw_a00.imag)
    raw_cyclic = np.asarray(
        event["cyclic"]["topological"], dtype=np.complex128
    )
    controlled_cyclic = raw_cyclic.copy()
    controlled_cyclic[0] = complex(
        controlled_cyclic[0].real - control.real,
        controlled_cyclic[0].imag,
    )
    raw_local = complex(event["local"]["topological"])
    controlled_local = complex(LOCAL_WEIGHTS @ controlled_cyclic)
    expected_controlled_local = complex(
        raw_local.real - LOCAL_WEIGHTS[0] * control.real,
        raw_local.imag,
    )
    projection_closure = abs(
        controlled_local - expected_controlled_local
    )
    if projection_closure > 1.0e-9:
        raise RuntimeError(
            f"controlled local projection closure failed for seed {seed}"
        )
    event["raw_topological_local"] = raw_local
    event["controlled_topological_local"] = controlled_local
    event["raw_topological_cyclic"] = raw_cyclic
    event["controlled_topological_cyclic"] = controlled_cyclic
    event["A00_control"] = control
    event["A00_raw"] = raw_a00
    event["A00_adjusted"] = adjusted_a00
    event["control_projection_closure"] = projection_closure
    nonzero_tolerance = float(
        manifest["acceptance_thresholds"][
            "relative_nonzero_control_tolerance"
        ]
    )
    control_row = {
        "source": "fresh_5221",
        "seed": seed,
        "event_id": event["event_id"],
        "tranche": (
            1 if seed in TRANCHE_TOPOLOGICAL[1] else 2
        ),
        "raw_A00_real": raw_a00.real,
        "raw_A00_imaginary": raw_a00.imag,
        "control_real": control.real,
        "control_imaginary_diagnostic_only": control.imag,
        "adjusted_A00_real": adjusted_a00.real,
        "adjusted_A00_imaginary_unchanged": adjusted_a00.imag,
        "raw_topological_local_real": raw_local.real,
        "raw_topological_local_imaginary": raw_local.imag,
        "controlled_topological_local_real": controlled_local.real,
        "controlled_topological_local_imaginary": controlled_local.imag,
        "local_projector_weight_z_minus_0p6": float(LOCAL_WEIGHTS[0]),
        "control_projection_closure": projection_closure,
        "control_nonzero_under_frozen_tolerance": (
            abs(control.real)
            > nonzero_tolerance * max(1.0, abs(raw_a00.real))
        ),
        "E040_selected_control_pair_count": rows["E040"][
            "selected_control_pair_count"
        ],
        "E020_selected_control_pair_count": rows["E020"][
            "selected_control_pair_count"
        ],
        "status": "FRESH_SCALED_CONTROLLED_EVENT",
        "valid_for_numeric_UV_claim": False,
    }
    return event, control_row


def legacy_control_rows() -> dict[int, dict[str, str]]:
    with CONTROL_EVENTS_5214.open(
        newline="", encoding="utf-8"
    ) as handle:
        return {
            int(row["seed"]): row for row in csv.DictReader(handle)
        }


def legacy_events() -> tuple[
    list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]
]:
    manifest = read_json(MANIFEST_5212)
    config = read_json(CONFIG_5212)
    jobs = M5212.build_schedule(config, manifest)
    counts = M5212.run_counts(RUN_5212, config, jobs)
    control_rows = legacy_control_rows()
    full: list[dict[str, Any]] = []
    topological: list[dict[str, Any]] = []
    local_closures: list[float] = []
    for seed in manifest["fresh_full_scramble_seeds"]:
        if M5212.event_complete(
            RUN_5212, config, jobs, "full", int(seed)
        ):
            full.append(
                M5212.projected_event(
                    RUN_5212, config, jobs, "full", int(seed)
                )
            )
    for seed_value in manifest["fresh_topological_scramble_seeds"]:
        seed = int(seed_value)
        if not M5212.event_complete(
            RUN_5212, config, jobs, "topological", seed
        ):
            continue
        event = M5212.projected_event(
            RUN_5212, config, jobs, "topological", seed
        )
        control = float(control_rows[seed]["permutation_zero_control_real"])
        raw_cyclic = np.asarray(
            event["cyclic"]["topological"], dtype=np.complex128
        )
        controlled_cyclic = raw_cyclic.copy()
        controlled_cyclic[0] = complex(
            controlled_cyclic[0].real - control,
            controlled_cyclic[0].imag,
        )
        raw_local = complex(event["local"]["topological"])
        controlled_local = complex(LOCAL_WEIGHTS @ controlled_cyclic)
        stored_controlled = complex(
            float(
                control_rows[seed][
                    "adjusted_topological_local_real"
                ]
            ),
            raw_local.imag,
        )
        closure = abs(controlled_local - stored_controlled)
        local_closures.append(closure)
        event["raw_topological_local"] = raw_local
        event["controlled_topological_local"] = controlled_local
        event["raw_topological_cyclic"] = raw_cyclic
        event["controlled_topological_cyclic"] = controlled_cyclic
        event["A00_control"] = complex(control, 0.0)
        topological.append(event)
    audit = read_json(CONTROL_AUDIT_5214)
    result_5212 = read_json(RESULT_5212)
    current_source_digest = digest(SCRIPT_5212)
    source_digest_matches = (
        current_source_digest
        in PROVENANCE_5212.read_text(encoding="utf-8")
    )
    compatibility_checks = {
        "legacy_matrix_has_280_converged_jobs": (
            counts["completed_converged"] == 280
            and counts["failed"] == 0
            and counts["completed_unconverged"] == 0
        ),
        "legacy_event_counts_are_2_and_12": (
            len(full) == 2 and len(topological) == 12
        ),
        "argument_ids_match": (
            manifest["required_base_argument_ids"] == list(ARGUMENT_IDS)
        ),
        "epsilon_ids_match": (
            manifest["epsilon_ids"] == list(EPSILON_IDS)
        ),
        "profile_matches": manifest["profile"] == "primary24",
        "physical_cosines_match": np.allclose(
            np.asarray(config["physical_cosines"], dtype=np.float64),
            PHYSICAL_COSINES,
            rtol=0.0,
            atol=0.0,
        ),
        "5212_provenance_runner_digest_is_current": source_digest_matches,
        "5214_control_replay_passed": bool(
            audit["passed"]
            and audit["control_variate_derived"]
            and audit["control_variate_retrospective_gate"]
        ),
        "legacy_control_local_projection_reproduced": (
            bool(local_closures) and max(local_closures) <= 1.0e-9
        ),
        "legacy_result_is_nonclaim": (
            not result_5212["valid_for_numeric_UV_claim"]
        ),
        "fresh_control_identity_independently_passed": bool(
            read_json(RESULT_5220)["fresh_control_pilot_passed"]
        ),
    }
    compatibility = {
        "checks": compatibility_checks,
        "passed": all(compatibility_checks.values()),
        "maximum_legacy_control_local_projection_closure": (
            max(local_closures) if local_closures else None
        ),
        "legacy_counts": counts,
        "pooling_scope": (
            "internal coefficient statistics only; no local-GR, full-MTS "
            "or numeric-UV claim follows from pooling"
        ),
    }
    return full, topological, compatibility


def distribution_diagnostics(
    values: np.ndarray, seeds: list[int]
) -> dict[str, Any]:
    return M5212.scalar_distribution_diagnostics(values, seeds)


def coefficient_estimate(
    full: list[dict[str, Any]],
    topological: list[dict[str, Any]],
    thresholds: dict[str, Any],
) -> dict[str, Any] | None:
    if len(full) < 2 or len(topological) < 2:
        return None
    naive_local = np.asarray(
        [row["local"]["naive"] for row in full], dtype=np.complex128
    )
    paired_local = np.asarray(
        [row["local"]["total"] for row in full], dtype=np.complex128
    )
    raw_topological_local = np.asarray(
        [row["raw_topological_local"] for row in topological],
        dtype=np.complex128,
    )
    controlled_topological_local = np.asarray(
        [row["controlled_topological_local"] for row in topological],
        dtype=np.complex128,
    )
    topological_seeds = [int(row["seed"]) for row in topological]
    crossed_local = complex(
        np.mean(naive_local) + np.mean(controlled_topological_local)
    )
    crossed_real_variance = float(
        np.var(naive_local.real, ddof=1) / len(naive_local)
        + np.var(controlled_topological_local.real, ddof=1)
        / len(controlled_topological_local)
    )
    crossed_imaginary_variance = float(
        np.var(naive_local.imag, ddof=1) / len(naive_local)
        + np.var(controlled_topological_local.imag, ddof=1)
        / len(controlled_topological_local)
    )
    physical_samples = M5212.physical_samples_5123()
    physical_local_samples = physical_samples @ LOCAL_WEIGHTS
    physical_local = float(np.mean(physical_local_samples))
    physical_local_variance = float(
        np.var(physical_local_samples, ddof=1)
        / len(physical_local_samples)
    )
    hhh_local = physical_local + crossed_local
    hhh_real_error = math.sqrt(
        physical_local_variance + crossed_real_variance
    )
    hhh_imaginary_error = math.sqrt(crossed_imaginary_variance)
    full_master = KNOWN_MASTER_LOCAL_COEFFICIENT + 2.0 * hhh_local
    k_mu = -4.0 * full_master
    k_mu_real_error = 8.0 * hhh_real_error
    k_mu_imaginary_error = 8.0 * hhh_imaginary_error

    naive_cyclic = np.asarray(
        [row["cyclic"]["naive"] for row in full],
        dtype=np.complex128,
    )
    topological_cyclic = np.asarray(
        [row["controlled_topological_cyclic"] for row in topological],
        dtype=np.complex128,
    )
    crossed_cyclic = np.mean(naive_cyclic, axis=0) + np.mean(
        topological_cyclic, axis=0
    )
    real_covariance = (
        M5212.covariance_of_mean(naive_cyclic.real)
        + M5212.covariance_of_mean(topological_cyclic.real)
        + M5212.covariance_of_mean(physical_samples)
    )
    imaginary_covariance = (
        M5212.covariance_of_mean(naive_cyclic.imag)
        + M5212.covariance_of_mean(topological_cyclic.imag)
    )
    hybrid_cyclic = np.mean(physical_samples, axis=0) + crossed_cyclic
    projector = np.eye(len(PHYSICAL_SHAPE)) - np.outer(
        PHYSICAL_SHAPE, LOCAL_WEIGHTS
    )
    nonlocal_value = projector @ hybrid_cyclic
    nonlocal_real_covariance = projector @ real_covariance @ projector.T
    target = np.asarray(
        read_json(M5212.TARGET_5018)["target"][
            "required_hhh_nonlocal"
        ],
        dtype=np.float64,
    )
    mismatch = nonlocal_value.real - target
    mismatch_error = np.sqrt(
        np.maximum(np.diag(nonlocal_real_covariance), 0.0)
    )
    maximum_mismatch_sigma = float(
        np.max(np.abs(mismatch) / np.maximum(mismatch_error, 1.0e-30))
    )
    controlled_real_distribution = distribution_diagnostics(
        controlled_topological_local.real, topological_seeds
    )
    controlled_imaginary_distribution = distribution_diagnostics(
        controlled_topological_local.imag, topological_seeds
    )
    raw_real_distribution = distribution_diagnostics(
        raw_topological_local.real, topological_seeds
    )
    tail_gate = bool(
        len(topological) >= int(thresholds["minimum_tail_event_count"])
        and controlled_real_distribution[
            "maximum_leave_one_out_shift_standard_errors"
        ]
        <= float(
            thresholds[
                "maximum_leave_one_out_shift_standard_errors"
            ]
        )
        and controlled_real_distribution["ordered_half_means"][
            "difference_sigma"
        ]
        <= float(
            thresholds["maximum_ordered_half_difference_sigma"]
        )
        and controlled_real_distribution["maximum_absolute_event_share"]
        <= float(thresholds["maximum_absolute_event_share"])
    )
    precision_gate = bool(
        k_mu_real_error
        <= float(thresholds["maximum_real_standard_error_fraction"])
        * max(
            abs(k_mu.real),
            float(thresholds["real_precision_scale_floor"]),
        )
        and abs(k_mu.imag)
        <= float(thresholds["maximum_imaginary_mean_standard_errors"])
        * max(k_mu_imaginary_error, 1.0e-30)
        and maximum_mismatch_sigma
        <= float(thresholds["maximum_nonlocal_mismatch_sigma"])
    )
    return {
        "full_event_count": len(full),
        "topological_event_count": len(topological),
        "full_naive_local": {
            "real": scalar_summary(naive_local.real),
            "imaginary": scalar_summary(naive_local.imag),
        },
        "paired_full_local": {
            "real": scalar_summary(paired_local.real),
            "imaginary": scalar_summary(paired_local.imag),
        },
        "raw_topological_local": {
            "real": raw_real_distribution,
            "imaginary": distribution_diagnostics(
                raw_topological_local.imag, topological_seeds
            ),
        },
        "controlled_topological_local": {
            "real": controlled_real_distribution,
            "imaginary": controlled_imaginary_distribution,
        },
        "crossed_local_coefficient": {
            "value": complex_row(crossed_local),
            "real_standard_error": math.sqrt(crossed_real_variance),
            "imaginary_standard_error": math.sqrt(
                crossed_imaginary_variance
            ),
        },
        "physical_local_coefficient": {
            "value": physical_local,
            "standard_error": math.sqrt(physical_local_variance),
        },
        "hhh_local_coefficient": {
            "value": complex_row(hhh_local),
            "real_standard_error": hhh_real_error,
            "imaginary_standard_error": hhh_imaginary_error,
        },
        "candidate_K_mu": {
            "value": complex_row(k_mu),
            "real_standard_error": k_mu_real_error,
            "imaginary_standard_error": k_mu_imaginary_error,
        },
        "maximum_nonlocal_mismatch_sigma": maximum_mismatch_sigma,
        "controlled_real_tail_gate": tail_gate,
        "coefficient_precision_gate": precision_gate,
        "imaginary_mean_zero_compatible": (
            controlled_imaginary_distribution["mean_to_standard_error"]
            <= float(
                thresholds[
                    "maximum_imaginary_mean_standard_errors"
                ]
            )
        ),
        "real_covariance_of_mean": real_covariance.tolist(),
        "imaginary_covariance_of_mean": imaginary_covariance.tolist(),
        "valid_for_numeric_UV_claim": False,
    }


def fresh_control_diagnostics(
    rows: list[dict[str, Any]],
    manifest: dict[str, Any],
    complete_design: bool,
) -> dict[str, Any] | None:
    if len(rows) < 2:
        return None
    thresholds = manifest["acceptance_thresholds"]
    raw = np.asarray([float(row["raw_A00_real"]) for row in rows])
    control = np.asarray([float(row["control_real"]) for row in rows])
    adjusted = np.asarray(
        [float(row["adjusted_A00_real"]) for row in rows]
    )
    raw_sd = float(np.std(raw, ddof=1))
    adjusted_sd = float(np.std(adjusted, ddof=1))
    ratio = adjusted_sd / raw_sd if raw_sd > 0.0 else None
    control_summary = scalar_summary(control)
    control_se = float(control_summary["standard_error"])
    if control_se > 0.0:
        control_mean_se = abs(float(control_summary["mean"])) / control_se
    elif float(control_summary["mean"]) == 0.0:
        control_mean_se = 0.0
    else:
        control_mean_se = None
    nonzero_count = sum(
        bool(row["control_nonzero_under_frozen_tolerance"]) for row in rows
    )
    monitor_gate = bool(
        ratio is not None
        and ratio
        < float(
            thresholds["maximum_A00_real_standard_deviation_ratio"]
        )
        and control_mean_se is not None
        and control_mean_se
        <= float(
            thresholds[
                "maximum_absolute_control_mean_standard_errors"
            ]
        )
    )
    return {
        "event_count": len(rows),
        "raw_A00_real": scalar_summary(raw),
        "control_real": control_summary,
        "adjusted_A00_real": scalar_summary(adjusted),
        "standard_deviation_ratio": ratio,
        "variance_reduction_factor": (
            1.0 / ratio**2 if ratio is not None and ratio > 0.0 else None
        ),
        "control_mean_in_standard_errors": control_mean_se,
        "nonzero_control_event_count": nonzero_count,
        "interim_monitor_only": not complete_design,
        "interim_monitor_gate": monitor_gate,
        "final_control_gate": bool(
            complete_design
            and monitor_gate
            and nonzero_count
            >= int(thresholds["minimum_nonzero_control_events"])
        ),
        "thresholds_retuned_after_outcomes": False,
    }


def event_csv_rows(
    full: list[dict[str, Any]],
    topological: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for event in full:
        row: dict[str, Any] = {
            "source": "fresh_5221",
            "stratum": "full",
            "seed": event["seed"],
            "event_id": event["event_id"],
            "tranche": 1 if int(event["seed"]) in TRANCHE_FULL[1] else 2,
            "runtime_seconds": event["runtime_seconds"],
            "naive_local_real": event["local"]["naive"].real,
            "naive_local_imaginary": event["local"]["naive"].imag,
            "paired_total_local_real": event["local"]["total"].real,
            "paired_total_local_imaginary": event["local"]["total"].imag,
            "status": "COMPLETE_FRESH_FULL_EVENT",
            "valid_for_numeric_UV_claim": False,
        }
        for index, cosine in enumerate(PHYSICAL_COSINES):
            label = (
                f"z{cosine:+.1f}"
                .replace("+", "p")
                .replace("-", "m")
                .replace(".", "p")
            )
            row[f"naive_{label}_real"] = event["cyclic"]["naive"][
                index
            ].real
            row[f"naive_{label}_imaginary"] = event["cyclic"][
                "naive"
            ][index].imag
        rows.append(row)
    for event in topological:
        row = {
            "source": "fresh_5221",
            "stratum": "topological",
            "seed": event["seed"],
            "event_id": event["event_id"],
            "tranche": (
                1
                if int(event["seed"]) in TRANCHE_TOPOLOGICAL[1]
                else 2
            ),
            "runtime_seconds": event["runtime_seconds"],
            "raw_topological_local_real": event[
                "raw_topological_local"
            ].real,
            "raw_topological_local_imaginary": event[
                "raw_topological_local"
            ].imag,
            "controlled_topological_local_real": event[
                "controlled_topological_local"
            ].real,
            "controlled_topological_local_imaginary": event[
                "controlled_topological_local"
            ].imag,
            "A00_control_real": event["A00_control"].real,
            "status": "COMPLETE_FRESH_CONTROLLED_TOPOLOGICAL_EVENT",
            "valid_for_numeric_UV_claim": False,
        }
        for index, cosine in enumerate(PHYSICAL_COSINES):
            label = (
                f"z{cosine:+.1f}"
                .replace("+", "p")
                .replace("-", "m")
                .replace(".", "p")
            )
            row[f"raw_{label}_real"] = event[
                "raw_topological_cyclic"
            ][index].real
            row[f"controlled_{label}_real"] = event[
                "controlled_topological_cyclic"
            ][index].real
            row[f"imaginary_{label}"] = event[
                "controlled_topological_cyclic"
            ][index].imag
        rows.append(row)
    return rows


def classifier_rows() -> list[dict[str, Any]]:
    rows = []
    for path in sorted(CLASSIFIER_CACHE.rglob("*.json")):
        value = read_json(path)
        rows.append(
            {
                "path": str(path),
                "sha256": digest(path),
                "status": value.get("status"),
                "level_id": value.get("contract", {})
                .get("level", {})
                .get("level_id"),
                "maximum_magnitude": value.get("maximum_magnitude"),
                "valid_for_numeric_UV_claim": False,
            }
        )
    return rows


def analyse(
    state: str,
    manifest: dict[str, Any],
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
) -> dict[str, Any]:
    counts = run_counts(config, jobs)
    by_tranche = tranche_counts(config, jobs)
    fresh_full: list[dict[str, Any]] = []
    fresh_topological: list[dict[str, Any]] = []
    fresh_control_rows: list[dict[str, Any]] = []
    for seed in FULL_SEEDS:
        if event_is_complete(config, jobs, "full", seed):
            fresh_full.append(
                M5212.projected_event(
                    RUN_DIRECTORY, config, jobs, "full", seed
                )
            )
    for seed in TOPOLOGICAL_SEEDS:
        if event_is_complete(config, jobs, "topological", seed):
            event, control_row = controlled_topological_event(
                config, jobs, seed, manifest
            )
            fresh_topological.append(event)
            fresh_control_rows.append(control_row)
    complete_design = bool(
        counts["completed_converged"] == len(jobs)
        and counts["failed"] == 0
        and counts["completed_unconverged"] == 0
    )
    thresholds = manifest["acceptance_thresholds"]
    new_only = coefficient_estimate(
        fresh_full, fresh_topological, thresholds
    )
    legacy_full, legacy_topological, compatibility = legacy_events()
    pooled = None
    if compatibility["passed"]:
        pooled = coefficient_estimate(
            [*legacy_full, *fresh_full],
            [*legacy_topological, *fresh_topological],
            thresholds,
        )
    control_diagnostics = fresh_control_diagnostics(
        fresh_control_rows, manifest, complete_design
    )
    write_csv(
        EVENT_ROWS, event_csv_rows(fresh_full, fresh_topological)
    )
    write_csv(CONTROL_ROWS, fresh_control_rows)
    cache_rows = classifier_rows()
    atomic_json(
        CLASSIFIER_AUDIT,
        {
            "checkpoint": 5221,
            "checkpoint_marker": MARKER,
            "invocation_rows": list(M5220.RUNTIME_CLASSIFIER_ROWS),
            "cache_rows": cache_rows,
            "cache_row_count": len(cache_rows),
            "unresolved_action": "fail_closed",
            "valid_for_numeric_UV_claim": False,
        },
    )
    coefficient_gate = bool(
        complete_design
        and compatibility["passed"]
        and control_diagnostics is not None
        and control_diagnostics["final_control_gate"]
        and pooled is not None
        and pooled["controlled_real_tail_gate"]
        and pooled["coefficient_precision_gate"]
    )
    if not complete_design:
        decision = "RUN_MANDATORY_REMAINING_TRANCHE"
    elif not compatibility["passed"]:
        decision = "HOLD_FOR_LEGACY_PROTOCOL_COMPATIBILITY"
    elif control_diagnostics is None or not control_diagnostics[
        "final_control_gate"
    ]:
        decision = "REJECT_CONTROLLED_SCALE_WITHOUT_RETUNING"
    elif pooled is None or not pooled["controlled_real_tail_gate"]:
        decision = "SCALE_FURTHER_UNDER_FROZEN_ESTIMATOR"
    elif not pooled["coefficient_precision_gate"]:
        decision = "SCALE_FURTHER_FOR_COEFFICIENT_PRECISION"
    else:
        decision = (
            "CROSSED_HHH_COEFFICIENT_STATISTICALLY_CLOSED_"
            "PENDING_SURVIVING_CUT_CLASSES"
        )
    analysis = {
        "state": state,
        "counts": counts,
        "tranche_counts": by_tranche,
        "fresh_complete_full_events": len(fresh_full),
        "fresh_expected_full_events": len(FULL_SEEDS),
        "fresh_complete_topological_events": len(fresh_topological),
        "fresh_expected_topological_events": len(TOPOLOGICAL_SEEDS),
        "complete_scaled_design": complete_design,
        "both_tranches_mandatory": True,
        "interim_coefficient_stopping_allowed": False,
        "fresh_control_diagnostics": control_diagnostics,
        "new_only_estimate": new_only,
        "legacy_pool_compatibility": compatibility,
        "pooled_estimate": pooled,
        "coefficient_run_gate": coefficient_gate,
        "decision": decision,
        "classifier_cache_row_count": len(cache_rows),
        "thresholds_retuned_after_outcomes": False,
        "numeric_UV_coefficient_complete": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    return analysis


def current_state(
    counts: dict[str, int],
    by_tranche: dict[str, dict[str, int]],
    requested_tranche: str | None = None,
    paused_state: str | None = None,
) -> str:
    if counts["failed"] or counts["completed_unconverged"]:
        return "BLOCKED_JOB_FAILURE"
    if counts["completed_converged"] == 520:
        return "COMPLETE_DESIGN"
    if paused_state is not None:
        return paused_state
    tranche_one = by_tranche["1"]
    tranche_two = by_tranche["2"]
    if tranche_one["completed_converged"] == 260:
        if requested_tranche == "1":
            return "TRANCHE_1_COMPLETE"
        if tranche_two["completed_converged"] == 260:
            return "COMPLETE_DESIGN"
    return "FROZEN_RUN_INCOMPLETE"


def validation_rows(
    state: str,
    manifest: dict[str, Any],
    counts: dict[str, int],
    jobs: list[dict[str, Any]],
    analysis: dict[str, Any],
) -> list[tuple[str, bool, str]]:
    lock = read_json(PROTOCOL_LOCK)["contract"]
    formal_digest = tree_digest(FORMAL)
    source_checks = [
        (ROOT / row["path"]).exists()
        and digest(ROOT / row["path"]) == row["sha256"]
        for row in manifest["locked_sources"]
    ]
    return [
        (
            "formalization_workbench_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "protocol_files_match_lock",
            digest(MANIFEST) == lock["manifest_sha256"]
            and digest(FROZEN_CONFIG) == lock["config_sha256"]
            and digest(FROZEN_SCHEDULE) == lock["schedule_sha256"]
            and digest(Path(__file__).resolve()) == lock["runner_sha256"]
            and digest(ALLOCATION) == lock["allocation_sha256"],
            digest(PROTOCOL_LOCK),
        ),
        (
            "all_locked_source_paths_and_digests_exist",
            all(source_checks),
            f"{sum(source_checks)}/{len(source_checks)}",
        ),
        (
            "fresh_seeds_absent_from_prior_protocols",
            not manifest["prior_seed_occurrences_at_lock"],
            str(manifest["prior_seed_occurrences_at_lock"]),
        ),
        (
            "no_failed_or_unconverged_jobs",
            counts["failed"] == 0
            and counts["completed_unconverged"] == 0,
            str(counts),
        ),
        (
            "completed_plus_missing_equals_schedule",
            counts["completed_converged"] + counts["missing"]
            == len(jobs),
            str(counts),
        ),
        (
            "complete_state_requires_all_520_jobs",
            state != "COMPLETE_DESIGN"
            or counts["completed_converged"] == 520,
            str(counts["completed_converged"]),
        ),
        (
            "legacy_pool_is_fail_closed",
            analysis["legacy_pool_compatibility"]["passed"]
            or analysis["pooled_estimate"] is None,
            str(analysis["legacy_pool_compatibility"]["passed"]),
        ),
        (
            "thresholds_not_retuned_after_outcomes",
            not analysis["thresholds_retuned_after_outcomes"],
            "false",
        ),
        (
            "all_claim_flags_remain_false",
            not analysis["valid_for_numeric_UV_claim"]
            and not analysis["valid_for_local_GR_claim"]
            and not analysis["valid_for_full_MTS_claim"],
            "numeric UV, local GR and full MTS remain false",
        ),
    ]


def render_document(
    state: str,
    counts: dict[str, int],
    analysis: dict[str, Any],
) -> None:
    new_estimate = analysis["new_only_estimate"]
    pooled = analysis["pooled_estimate"]
    lines = [
        "# 5221 - Scaled controlled two-stratum coefficient run",
        "",
        "## Frozen design",
        "",
        "The checkpoint-5212 variance and cost evidence gives",
        "`n_top/n_full = 11.7194556826`. The design rounds this upward",
        "to `12:1` and freezes two mandatory tranches. Each tranche",
        "contains one paired full event and twelve controlled topological",
        "events, with ten arguments and two epsilon values per event.",
        "",
        "The A00 real control is the checkpoint-5220 independently",
        "validated, symmetry-fixed unit-coefficient control. It is applied",
        "before the physical local projection. No coefficient-dependent",
        "stopping or threshold retuning is allowed after tranche one.",
        "",
        "## Current state",
        "",
        f"- State: `{state}`.",
        f"- Converged jobs: `{counts['completed_converged']}/520`.",
        f"- Missing jobs: `{counts['missing']}`.",
        (
            "- Failed or completed-unconverged jobs: "
            f"`{counts['failed'] + counts['completed_unconverged']}`."
        ),
        (
            "- Complete fresh events: "
            f"`{analysis['fresh_complete_full_events']}/2` full and "
            f"`{analysis['fresh_complete_topological_events']}/24` "
            "topological."
        ),
        f"- Decision: `{analysis['decision']}`.",
        "",
        "## Estimates",
        "",
    ]
    if new_estimate is None:
        lines.append(
            "The new-only estimate is unavailable until at least two "
            "events are complete in both strata."
        )
    else:
        value = new_estimate["candidate_K_mu"]["value"]
        lines.extend(
            [
                (
                    "- New-only provisional "
                    f"`K_mu={value['real']:.10g}"
                    f"{value['imaginary']:+.10g} i`, real SE "
                    f"`{new_estimate['candidate_K_mu']['real_standard_error']:.8g}` "
                    "and imaginary SE "
                    f"`{new_estimate['candidate_K_mu']['imaginary_standard_error']:.8g}`."
                ),
                (
                    "- New-only tail gate: "
                    f"`{new_estimate['controlled_real_tail_gate']}`; "
                    "new `n=24` is predeclared insufficient by itself."
                ),
            ]
        )
    if pooled is not None:
        value = pooled["candidate_K_mu"]["value"]
        lines.extend(
            [
                (
                    "- Compatibility-gated pooled "
                    f"`K_mu={value['real']:.10g}"
                    f"{value['imaginary']:+.10g} i`, real SE "
                    f"`{pooled['candidate_K_mu']['real_standard_error']:.8g}` "
                    "and imaginary SE "
                    f"`{pooled['candidate_K_mu']['imaginary_standard_error']:.8g}`."
                ),
                (
                    "- Pooled controlled-tail gate: "
                    f"`{pooled['controlled_real_tail_gate']}`; coefficient "
                    f"precision gate: `{pooled['coefficient_precision_gate']}`."
                ),
            ]
        )
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "This run can close only the crossed-hhh coefficient statistic.",
            "It does not by itself close the remaining cut classes, a",
            "canonical ultraviolet coefficient, local GR, or full MTS.",
            "All corresponding claim flags remain false.",
            "",
            "## Evidence",
            "",
            f"- Manifest: `{MANIFEST}`",
            f"- Allocation derivation: `{ALLOCATION}`",
            f"- Protocol lock: `{PROTOCOL_LOCK}`",
            f"- Result: `{RESULT}`",
            f"- Validation: `{VALIDATION}`",
            f"- Resume note: `{RESUME}`",
        ]
    )
    atomic_text(DOCUMENT, "\n".join(lines) + "\n")


def finalize(
    state: str,
    manifest: dict[str, Any],
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
) -> dict[str, Any]:
    analysis = analyse(state, manifest, config, jobs)
    counts = analysis["counts"]
    validations = validation_rows(
        state, manifest, counts, jobs, analysis
    )
    with VALIDATION.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("check", "passed", "detail"))
        for name, passed, detail in validations:
            writer.writerow((name, str(bool(passed)).lower(), detail))
    result = {
        "checkpoint": 5221,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "run_id": RUN_ID,
        "state": state,
        "counts": counts,
        "analysis": analysis,
        "protocol_lock_sha256": digest(PROTOCOL_LOCK),
        "classifier_audit_sha256": digest(CLASSIFIER_AUDIT),
        "validation_all_passed": all(row[1] for row in validations),
        "validation_check_count": len(validations),
        "formalization_workbench_tree_sha256": tree_digest(FORMAL),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT, result)
    render_document(state, counts, analysis)
    remaining_one = analysis["tranche_counts"]["1"]["missing"]
    remaining_two = analysis["tranche_counts"]["2"]["missing"]
    atomic_text(
        RESUME,
        "\n".join(
            [
                "# Checkpoint 5221 resume",
                "",
                f"- Current state: `{state}`.",
                f"- Tranche 1 missing jobs: `{remaining_one}`.",
                f"- Tranche 2 missing jobs: `{remaining_two}`.",
                "- Both tranches are mandatory; do not stop on an interim coefficient.",
                "- Resume tranche one:",
                (
                    f"  `{sys.executable} {Path(__file__).resolve()} "
                    "--mode run --tranche 1 --wall-cap-hours 4`"
                ),
                "- Resume tranche two:",
                (
                    f"  `{sys.executable} {Path(__file__).resolve()} "
                    "--mode run --tranche 2 --wall-cap-hours 4`"
                ),
                "- Analyse without running:",
                (
                    f"  `{sys.executable} {Path(__file__).resolve()} "
                    "--mode analyse`"
                ),
                "",
            ]
        ),
    )
    atomic_json(
        STATUS,
        {
            "checkpoint": 5221,
            "state": state,
            "counts": counts,
            "tranche_counts": analysis["tranche_counts"],
            "decision": analysis["decision"],
            "updated_unix_time": time.time(),
        },
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def install_runtime(config: dict[str, Any]) -> Any:
    M5220.CLASSIFIER_CACHE = CLASSIFIER_CACHE
    M5220.RUNTIME_CLASSIFIER_ROWS.clear()
    return M5220.install_runtime(config)


def execute(
    manifest: dict[str, Any],
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
    requested_tranche: str,
    wall_cap_hours: float,
    maximum_new_jobs: int,
) -> dict[str, Any]:
    if not (0.0 < wall_cap_hours <= MAXIMUM_WALL_HOURS):
        raise ValueError("wall cap must be in (0, 4] hours")
    selected_tranches = (
        {1, 2}
        if requested_tranche == "all"
        else {int(requested_tranche)}
    )
    selected_jobs = [
        job for job in jobs if int(job["tranche"]) in selected_tranches
    ]
    manager = install_runtime(config)
    started = time.monotonic()
    newly_executed = 0
    paused_state: str | None = None
    for index, job in enumerate(selected_jobs, start=1):
        if (time.monotonic() - started) / 3600.0 >= wall_cap_hours:
            paused_state = "PAUSED_WALL_CAP"
            break
        cached = M5212.cached_result(RUN_DIRECTORY, config, job)
        if job["stratum"] == "topological" and job[
            "base_argument_id"
        ] == "A00":
            row = M5215.execute_job(
                RUN_DIRECTORY, config, manager, job
            )
        else:
            row = M5212.execute_job(
                RUN_DIRECTORY, config, manager, job
            )
        if cached is None:
            newly_executed += 1
        row = {
            **row,
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "owning_checkpoint_marker": MARKER,
            "tranche": job["tranche"],
            "general_grouped_classifier_predeclared": True,
            "controlled_A00_real_predeclared": (
                job["stratum"] == "topological"
                and job["base_argument_id"] == "A00"
            ),
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        atomic_json(M5212.output_path(RUN_DIRECTORY, job), row)
        counts = run_counts(config, jobs)
        by_tranche = tranche_counts(config, jobs)
        atomic_json(
            STATUS,
            {
                "checkpoint": 5221,
                "state": "RUNNING",
                "requested_tranche": requested_tranche,
                "current_schedule_index": index,
                "current_schedule_key": job["schedule_key"],
                "last_job_status": row["status"],
                "counts": counts,
                "tranche_counts": by_tranche,
                "elapsed_seconds": time.monotonic() - started,
                "updated_unix_time": time.time(),
            },
        )
        print(
            json.dumps(
                {
                    "requested_schedule_index": index,
                    "schedule_key": job["schedule_key"],
                    "status": row["status"],
                    "resumed_from_cache": bool(
                        row.get("resumed_from_cache")
                    ),
                    "elapsed_seconds": time.monotonic() - started,
                    "all_counts": counts,
                }
            ),
            flush=True,
        )
        if row["status"] != "COMPLETED_CONVERGED":
            paused_state = "BLOCKED_JOB_FAILURE"
            break
        if maximum_new_jobs > 0 and newly_executed >= maximum_new_jobs:
            paused_state = "PAUSED_JOB_CAP"
            break
    counts = run_counts(config, jobs)
    by_tranche = tranche_counts(config, jobs)
    state = current_state(
        counts,
        by_tranche,
        requested_tranche=requested_tranche,
        paused_state=paused_state,
    )
    for tranche in (1, 2):
        if by_tranche[str(tranche)]["completed_converged"] == 260:
            atomic_text(
                RUN_DIRECTORY / f"TRANCHE_{tranche}_COMPLETE.marker",
                f"checkpoint=5221\ntranche={tranche}\n",
            )
    if counts["completed_converged"] == 520:
        atomic_text(
            RUN_DIRECTORY / "COMPLETE.marker",
            "checkpoint=5221\nstate=COMPLETE_DESIGN\n",
        )
    return finalize(state, manifest, config, jobs)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("prepare", "run", "analyse"), default="prepare"
    )
    parser.add_argument(
        "--tranche", choices=("1", "2", "all"), default="1"
    )
    parser.add_argument(
        "--wall-cap-hours", type=float, default=MAXIMUM_WALL_HOURS
    )
    parser.add_argument("--maximum-new-jobs", type=int, default=0)
    arguments = parser.parse_args()
    manifest, config, jobs, activation = prepare()
    if arguments.mode == "prepare":
        counts = run_counts(config, jobs)
        state = current_state(counts, tranche_counts(config, jobs))
        result = finalize(state, manifest, config, jobs)
        print(
            json.dumps(
                {
                    "prepared": True,
                    "activation": activation,
                    "state": result["state"],
                    "counts": result["counts"],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    if arguments.mode == "analyse":
        counts = run_counts(config, jobs)
        state = current_state(counts, tranche_counts(config, jobs))
        finalize(state, manifest, config, jobs)
        return
    execute(
        manifest,
        config,
        jobs,
        arguments.tranche,
        arguments.wall_cap_hours,
        arguments.maximum_new_jobs,
    )


if __name__ == "__main__":
    main()
