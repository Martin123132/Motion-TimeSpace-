from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5220"
RUN_ID = "fresh_grouped_classifier_A00_pilot_v1"
RUN_DIRECTORY = SOURCE / "runs" / RUN_ID
CLASSIFIER_CACHE = RUN_DIRECTORY / "grouped-classifier-cache"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SCRIPT_5215_TRANSPORT = (
    POST
    / "scripts"
    / "Y5_R2FR_5215_transport_invalid_full_homotopy_repair.py"
)
SCRIPT_5219 = (
    POST
    / "scripts"
    / "Y5_R2FR_5219_general_grouped_owned_direct_classifier.py"
)
SOURCE_5215 = POST / "source-intake" / "functional_rg" / "5215"
SOURCE_5219 = POST / "source-intake" / "functional_rg" / "5219"
BASE_MANIFEST = SOURCE_5215 / "frozen_A00_control_pilot_manifest.json"
TRANSPORT_LOCK = SOURCE_5215 / "frozen_transport_repair_lock.json"
CLASSIFIER_GATE = (
    SOURCE_5219 / "general_grouped_owned_direct_classifier_gate.json"
)
MANIFEST = SOURCE / "frozen_fresh_grouped_classifier_manifest.json"
FROZEN_CONFIG = RUN_DIRECTORY / "config.json"
FROZEN_SCHEDULE = SOURCE / "frozen_fresh_grouped_classifier_schedule.csv"
PROTOCOL_LOCK = SOURCE / "frozen_fresh_grouped_classifier_protocol_lock.json"
ACTIVATION = SOURCE / "fresh_grouped_classifier_activation.json"
RESULT = SOURCE / "fresh_grouped_classifier_A00_pilot_results.json"
EVENT_ROWS = SOURCE / "fresh_grouped_classifier_event_rows.csv"
PAIR_ROWS = SOURCE / "fresh_grouped_classifier_pair_rows.csv"
CLASSIFIER_AUDIT = SOURCE / "general_grouped_classifier_runtime_audit.json"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5220_VALIDATION.csv"
DOCUMENT = (
    POST
    / "5220-Y5-R2FR-fresh-predeclared-grouped-classifier-A00-pilot.md"
)
MARKER = "MTS_5220_FRESH_PREDECLARED_GROUPED_CLASSIFIER_A00_PILOT"
REVISION = "fresh-independent-grouped-classifier-pilot-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
SEEDS = tuple(range(522001, 522013))
MAXIMUM_WALL_HOURS = 4.0


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


MTRANSPORT = load_module(
    "mts_5215_transport_for_5220",
    SCRIPT_5215_TRANSPORT,
)
M5215 = MTRANSPORT.M5215
M5212 = M5215.M5212
M5219 = load_module("mts_5219_for_5220", SCRIPT_5219)
ORIGINAL_CATALOG = M5212.certified_5212_catalog
RUNTIME_CLASSIFIER_ROWS: list[dict[str, Any]] = []


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def prior_seed_occurrences() -> list[dict[str, Any]]:
    functional = POST / "source-intake" / "functional_rg"
    candidates = {
        *functional.rglob("config.json"),
        *functional.rglob("*manifest*.json"),
        *functional.rglob("*activation*.json"),
    }
    expression = re.compile(
        r"(?<![0-9])(?:"
        + "|".join(str(seed) for seed in SEEDS)
        + r")(?![0-9])"
    )
    rows = []
    for candidate in sorted(candidates):
        try:
            candidate.resolve().relative_to(SOURCE.resolve())
            continue
        except ValueError:
            pass
        matches = sorted(
            {
                int(value)
                for value in expression.findall(
                    candidate.read_text(
                        encoding="utf-8",
                        errors="ignore",
                    )
                )
            }
        )
        if matches:
            rows.append(
                {
                    "path": str(candidate),
                    "seeds": matches,
                }
            )
    return rows


def make_manifest() -> dict[str, Any]:
    base = read_json(BASE_MANIFEST)
    gate = read_json(CLASSIFIER_GATE)
    if (
        not gate["validation_all_passed"]
        or not gate["future_fresh_runner_integration_authorized"]
    ):
        raise RuntimeError("checkpoint-5219 classifier is not authorized")
    occurrences = prior_seed_occurrences()
    if occurrences:
        raise RuntimeError(
            f"reserved checkpoint-5220 seeds already occur: {occurrences}"
        )
    locked_sources = list(base["locked_sources"])
    locked_sources.extend(
        (
            {
                "path": str(
                    SCRIPT_5215_TRANSPORT.relative_to(POST)
                ).replace("\\", "/"),
                "sha256": digest(SCRIPT_5215_TRANSPORT),
            },
            {
                "path": str(TRANSPORT_LOCK.relative_to(POST)).replace(
                    "\\",
                    "/",
                ),
                "sha256": digest(TRANSPORT_LOCK),
            },
            {
                "path": str(SCRIPT_5219.relative_to(POST)).replace(
                    "\\",
                    "/",
                ),
                "sha256": digest(SCRIPT_5219),
            },
            {
                "path": str(CLASSIFIER_GATE.relative_to(POST)).replace(
                    "\\",
                    "/",
                ),
                "sha256": digest(CLASSIFIER_GATE),
            },
        )
    )
    return {
        **base,
        "checkpoint": 5220,
        "checkpoint_marker": MARKER,
        "locked_date": datetime.now(timezone.utc).date().isoformat(),
        "design_source": (
            "post-checkpoint-work/"
            "5219-Y5-R2FR-general-grouped-owned-direct-classifier.md"
        ),
        "fresh_topological_scramble_seeds": list(SEEDS),
        "fresh_low_scramble_seeds": list(SEEDS),
        "seed_selection_rule": (
            "the consecutive reserved block 522001 through 522012 was "
            "searched against all prior functional-RG manifests, "
            "activations and configs before checkpoint-5220 outcomes"
        ),
        "prior_seed_occurrences_at_lock": occurrences,
        "argument_topology_rule": (
            "bidirectional canonical path composition from A08 with "
            "predeclared transport-invalid full-homotopy fallback"
        ),
        "general_grouped_owned_direct_classifier": {
            "gate": str(CLASSIFIER_GATE),
            "gate_sha256": digest(CLASSIFIER_GATE),
            "runner": str(SCRIPT_5219),
            "runner_sha256": digest(SCRIPT_5219),
            "activation": (
                "only after all pre-existing certified catalog repairs "
                "leave a direct-only grouped row unstable"
            ),
            "unresolved_action": "fail_closed",
        },
        "maximum_wall_hours_per_invocation": MAXIMUM_WALL_HOURS,
        "allocation_locked_before_fresh_outcomes": True,
        "locked_sources": locked_sources,
        "scale_decision": (
            "authorize a larger controlled topological coefficient run "
            "only if all 24 fresh jobs and every structural/control "
            "acceptance gate pass under the predeclared grouped classifier"
        ),
        "pilot_only": True,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def make_config(
    manifest: dict[str, Any],
) -> dict[str, Any]:
    config = M5215.make_config(manifest, RUN_ID)
    config["checkpoint_marker"] = MARKER
    config["schema_revision"] = REVISION
    config["pilot_manifest"] = str(MANIFEST)
    config["pilot_manifest_digest"] = digest(MANIFEST)
    config["predeclared_transport_invalid_fallback"] = {
        "runner": str(SCRIPT_5215_TRANSPORT),
        "runner_sha256": digest(SCRIPT_5215_TRANSPORT),
        "lock": str(TRANSPORT_LOCK),
        "lock_sha256": digest(TRANSPORT_LOCK),
        "trigger": (
            "reject transported topology if either locked root "
            "diagnostic fails; use unchanged original full homotopy"
        ),
    }
    config["general_grouped_owned_direct_classifier"] = {
        "runner": str(SCRIPT_5219),
        "runner_sha256": digest(SCRIPT_5219),
        "gate": str(CLASSIFIER_GATE),
        "gate_sha256": digest(CLASSIFIER_GATE),
        "contract": read_json(CLASSIFIER_GATE)["classifier_contract"],
        "unresolved_action": "fail_closed",
    }
    config["source_files"][str(Path(__file__).resolve())] = digest(
        Path(__file__).resolve()
    )
    config["source_files"][str(SCRIPT_5219)] = digest(SCRIPT_5219)
    config["source_files"][str(CLASSIFIER_GATE)] = digest(
        CLASSIFIER_GATE
    )
    config.pop("config_digest", None)
    config["config_digest"] = M5215.canonical_digest(config)
    return config


def activation_record(
    manifest: dict[str, Any],
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
) -> dict[str, Any]:
    source_rows = []
    for declaration in manifest["locked_sources"]:
        path = POST / declaration["path"]
        actual = digest(path) if path.is_file() else ""
        source_rows.append(
            {
                "path": str(path),
                "expected_sha256": declaration["sha256"],
                "actual_sha256": actual,
                "matches": bool(
                    path.is_file()
                    and actual == declaration["sha256"]
                ),
            }
        )
    prerequisites = {
        "all_locked_sources_match": all(
            row["matches"] for row in source_rows
        ),
        "classifier_gate_authorized": bool(
            read_json(CLASSIFIER_GATE)[
                "future_fresh_runner_integration_authorized"
            ]
        ),
        "fresh_seed_set_is_exact": {
            int(event["seed"]) for event in config["events"]
        }
        == set(SEEDS),
        "fresh_seeds_absent_from_prior_protocols": not manifest[
            "prior_seed_occurrences_at_lock"
        ],
        "schedule_has_exactly_24_jobs": len(jobs) == 24,
        "schedule_is_A00_topological_only": all(
            job["stratum"] == "topological"
            and job["base_argument_id"] == "A00"
            and job["epsilon_id"] in {"E040", "E020"}
            for job in jobs
        ),
        "formalization_workbench_unchanged": (
            tree_digest(FORMAL) == FORMAL_BASELINE
        ),
        "pilot_is_nonclaim": bool(
            manifest["pilot_only"]
            and not manifest["valid_for_numeric_UV_claim"]
            and not manifest["valid_for_local_GR_claim"]
            and not manifest["valid_for_full_MTS_claim"]
        ),
    }
    return {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "manifest_sha256": digest(MANIFEST),
        "runner_sha256": digest(Path(__file__).resolve()),
        "config_digest": config["config_digest"],
        "schedule_digest": M5215.canonical_digest(jobs),
        "fresh_seeds": list(SEEDS),
        "locked_source_rows": source_rows,
        "prerequisites": prerequisites,
        "execution_authorized": all(prerequisites.values()),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def prepare() -> tuple[
    dict[str, Any],
    dict[str, Any],
    list[dict[str, Any]],
    dict[str, Any],
    dict[str, Any],
]:
    if MANIFEST.exists():
        manifest = read_json(MANIFEST)
    else:
        manifest = make_manifest()
        atomic_json(MANIFEST, manifest)
    if manifest["fresh_topological_scramble_seeds"] != list(SEEDS):
        raise RuntimeError("checkpoint-5220 frozen seed set changed")
    config = make_config(manifest)
    jobs = M5215.build_schedule(config, manifest)
    activation = activation_record(manifest, config, jobs)
    if not activation["execution_authorized"]:
        raise RuntimeError(
            f"checkpoint-5220 prerequisites failed: {activation['prerequisites']}"
        )
    RUN_DIRECTORY.mkdir(parents=True, exist_ok=True)
    if FROZEN_CONFIG.exists():
        existing = read_json(FROZEN_CONFIG)
        if existing["config_digest"] != config["config_digest"]:
            raise RuntimeError("checkpoint-5220 frozen config changed")
    else:
        atomic_json(FROZEN_CONFIG, config)
    if FROZEN_SCHEDULE.exists():
        existing_rows = list(
            csv.DictReader(
                FROZEN_SCHEDULE.open(
                    "r",
                    encoding="utf-8",
                    newline="",
                )
            )
        )
        if len(existing_rows) != len(jobs):
            raise RuntimeError("checkpoint-5220 schedule changed")
    else:
        M5215.write_csv(FROZEN_SCHEDULE, jobs)
    atomic_json(ACTIVATION, activation)
    contract = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "runner_sha256": digest(Path(__file__).resolve()),
        "manifest_sha256": digest(MANIFEST),
        "config_sha256": digest(FROZEN_CONFIG),
        "config_digest": config["config_digest"],
        "schedule_sha256": digest(FROZEN_SCHEDULE),
        "schedule_digest": M5215.canonical_digest(jobs),
        "classifier_runner_sha256": digest(SCRIPT_5219),
        "classifier_gate_sha256": digest(CLASSIFIER_GATE),
        "transport_runner_sha256": digest(SCRIPT_5215_TRANSPORT),
        "transport_lock_sha256": digest(TRANSPORT_LOCK),
        "acceptance_thresholds": manifest["acceptance_thresholds"],
        "seed_schedule": list(SEEDS),
        "unresolved_action": "fail_closed",
    }
    if PROTOCOL_LOCK.exists():
        protocol = read_json(PROTOCOL_LOCK)
        if protocol["contract"] != contract:
            raise RuntimeError("checkpoint-5220 protocol changed")
    else:
        outcome_files = [
            *RUN_DIRECTORY.glob("topological-jobs/*.json"),
            *RUN_DIRECTORY.glob("topologies/*.json"),
        ]
        if outcome_files:
            raise RuntimeError(
                "checkpoint-5220 outcomes exist before protocol lock"
            )
        protocol = {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "locked_at_utc": datetime.now(timezone.utc).isoformat(),
            "contract": contract,
            "outcomes_present_at_lock": False,
            "threshold_retuning_allowed": False,
            "valid_for_numeric_UV_claim": False,
        }
        atomic_json(PROTOCOL_LOCK, protocol)
    return manifest, config, jobs, activation, protocol


def generalized_catalog(
    ownership: dict[str, bool],
    start: complex,
    end: complex,
    required_roots: list[complex],
    global_nodes: int,
    global_residue_nodes: int,
    relative_residue_nodes: int,
    model_distance: float,
) -> tuple[list[dict[str, Any]], bool]:
    catalog, stable = ORIGINAL_CATALOG(
        ownership,
        start,
        end,
        required_roots,
        global_nodes,
        global_residue_nodes,
        relative_residue_nodes,
        model_distance,
    )
    if stable:
        return catalog, stable
    event = M5212.M5077.CURRENT_EVENT
    argument = M5212.M5077.CURRENT_ARGUMENT
    job_key = M5212.M5077.M5036.MREPAIR.CURRENT_JOB
    if event is None or argument is None or job_key is None:
        return catalog, False
    repaired = []
    for row in catalog:
        if bool(row["stable"]):
            repaired.append(row)
            continue
        replacement, audit = (
            M5219.resolve_grouped_owned_direct_row(
                row,
                ownership,
                job_key,
                event,
                argument,
                CLASSIFIER_CACHE,
            )
        )
        RUNTIME_CLASSIFIER_ROWS.append(audit)
        repaired.append(replacement)
    return repaired, all(bool(row["stable"]) for row in repaired)


def install_runtime(
    config: dict[str, Any],
) -> Any:
    MTRANSPORT.M5077.CentralTopologyManager.write_composed = (
        MTRANSPORT.repaired_write_composed
    )
    M5212.certified_5212_catalog = generalized_catalog
    M5212.M5077.certified_primary_catalog = generalized_catalog
    M5212.M5077.M5085.CertifiedRemovableGlobalExtension = (
        M5212.AdaptiveRemovableGlobalExtension
    )
    M5212.source_separated_cluster_gate()
    M5212.M5077.install_history_invariant_breakpoints(
        M5212.M5077.M5036.N5030
    )
    return M5212.M5077.CentralTopologyManager(
        RUN_DIRECTORY,
        config,
    )


def runtime_classifier_cache_rows() -> list[dict[str, Any]]:
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


def finalize(
    state: str,
    manifest: dict[str, Any],
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
) -> dict[str, Any]:
    counts = M5215.run_counts(RUN_DIRECTORY, config, jobs)
    analysis, event_rows, pair_rows = M5215.analyse(
        RUN_DIRECTORY,
        config,
        manifest,
        jobs,
    )
    if event_rows:
        M5215.write_csv(EVENT_ROWS, event_rows)
    if pair_rows:
        M5215.write_csv(PAIR_ROWS, pair_rows)
    cache_rows = runtime_classifier_cache_rows()
    atomic_json(
        CLASSIFIER_AUDIT,
        {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "invocation_rows": RUNTIME_CLASSIFIER_ROWS,
            "cache_rows": cache_rows,
            "cache_row_count": len(cache_rows),
            "unresolved_action": "fail_closed",
            "valid_for_numeric_UV_claim": False,
        },
    )
    formal_digest = tree_digest(FORMAL)
    blocking = counts["failed"] + counts["completed_unconverged"]
    validations = [
        (
            "formalization_workbench_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "protocol_files_match_lock",
            bool(
                digest(MANIFEST)
                == read_json(PROTOCOL_LOCK)["contract"][
                    "manifest_sha256"
                ]
                and digest(FROZEN_CONFIG)
                == read_json(PROTOCOL_LOCK)["contract"][
                    "config_sha256"
                ]
                and digest(FROZEN_SCHEDULE)
                == read_json(PROTOCOL_LOCK)["contract"][
                    "schedule_sha256"
                ]
            ),
            digest(PROTOCOL_LOCK),
        ),
        (
            "no_failed_or_unconverged_jobs",
            blocking == 0,
            str(blocking),
        ),
        (
            "completed_jobs_are_converged",
            counts["completed_converged"]
            + counts["missing"]
            == len(jobs),
            str(counts),
        ),
        (
            "complete_run_has_all_24_jobs",
            state != "COMPLETE"
            or counts["completed_converged"] == len(jobs),
            str(counts["completed_converged"]),
        ),
        (
            "claim_flags_remain_false",
            True,
            "numeric UV, local GR and full MTS remain false",
        ),
    ]
    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("check", "passed", "detail"))
        for name, passed, detail in validations:
            writer.writerow((name, str(bool(passed)).lower(), detail))
    validations_passed = all(row[1] for row in validations)
    result = {
        "checkpoint": 5220,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "run_id": RUN_ID,
        "state": state,
        "counts": counts,
        "analysis": analysis,
        "protocol_lock_sha256": digest(PROTOCOL_LOCK),
        "classifier_audit_sha256": digest(CLASSIFIER_AUDIT),
        "fresh_control_pilot_passed": bool(
            state == "COMPLETE"
            and validations_passed
            and analysis.get("fresh_control_pilot_passed", False)
        ),
        "scale_decision": (
            analysis.get("scale_decision")
            if state == "COMPLETE"
            else "FROZEN_RUN_INCOMPLETE"
        ),
        "formalization_workbench_tree_sha256": formal_digest,
        "validation_all_passed": validations_passed,
        "validation_check_count": len(validations),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT, result)
    lines = [
        "# 5220 - Fresh predeclared grouped-classifier A00 pilot",
        "",
        "## Design",
        "",
        "This is the independent replacement for the outcome-exposed",
        "checkpoint-5215 development pilot. Twelve previously unused",
        "scramble seeds, two epsilon values and only `A00` were frozen",
        "before any checkpoint-5220 topology or residue outcome.",
        "",
        "The checkpoint-5219 grouped-owned-direct classifier and the",
        "transport-invalid full-homotopy fallback are predeclared. Both",
        "remain fail closed outside their exact scopes.",
        "",
        "## Current state",
        "",
        f"- State: `{state}`.",
        f"- Converged jobs: `{counts['completed_converged']}/24`.",
        f"- Missing jobs: `{counts['missing']}`.",
        f"- Failed/unconverged jobs: `{blocking}`.",
        f"- Classifier cache rows: `{len(cache_rows)}`.",
        f"- Scale decision: `{result['scale_decision']}`.",
        "",
        "## Claim boundary",
        "",
        "This remains a control-efficiency pilot. Even a pass authorizes",
        "a larger coefficient calculation; it is not itself a canonical",
        "MTS ultraviolet coefficient or a full-MTS claim.",
        "",
        "## Evidence",
        "",
        f"- Manifest: `{MANIFEST}`",
        f"- Protocol lock: `{PROTOCOL_LOCK}`",
        f"- Result: `{RESULT}`",
        f"- Runtime classifier audit: `{CLASSIFIER_AUDIT}`",
        f"- Validation: `{VALIDATION}`",
    ]
    atomic_text(DOCUMENT, "\n".join(lines) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def execute(
    manifest: dict[str, Any],
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
    wall_cap_hours: float,
    maximum_new_jobs: int,
) -> dict[str, Any]:
    if not (0.0 < wall_cap_hours <= MAXIMUM_WALL_HOURS):
        raise ValueError("wall cap must be in (0, 4] hours")
    manager = install_runtime(config)
    started = time.monotonic()
    newly_executed = 0
    state = "RUNNING"
    for index, job in enumerate(jobs, start=1):
        if (time.monotonic() - started) / 3600.0 >= wall_cap_hours:
            state = "PAUSED_WALL_CAP"
            break
        cached = M5215.cached_result(RUN_DIRECTORY, config, job)
        row = M5215.execute_job(
            RUN_DIRECTORY,
            config,
            manager,
            job,
        )
        if cached is None:
            newly_executed += 1
        row = {
            **row,
            "owning_checkpoint_marker": MARKER,
            "general_grouped_classifier_predeclared": True,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        atomic_json(M5215.output_path(RUN_DIRECTORY, job), row)
        print(
            json.dumps(
                {
                    "schedule_index": index,
                    "schedule_key": job["schedule_key"],
                    "status": row["status"],
                    "resumed_from_cache": bool(
                        row.get("resumed_from_cache")
                    ),
                    "elapsed_seconds": time.monotonic() - started,
                }
            ),
            flush=True,
        )
        if row["status"] != "COMPLETED_CONVERGED":
            state = "BLOCKED_JOB_FAILURE"
            break
        if (
            maximum_new_jobs > 0
            and newly_executed >= maximum_new_jobs
        ):
            state = "PAUSED_JOB_CAP"
            break
    counts = M5215.run_counts(RUN_DIRECTORY, config, jobs)
    if counts["completed_converged"] == len(jobs):
        state = "COMPLETE"
    return finalize(state, manifest, config, jobs)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("prepare", "run", "analyse"),
        default="prepare",
    )
    parser.add_argument(
        "--wall-cap-hours",
        type=float,
        default=4.0,
    )
    parser.add_argument(
        "--maximum-new-jobs",
        type=int,
        default=0,
    )
    arguments = parser.parse_args()
    manifest, config, jobs, activation, protocol = prepare()
    if arguments.mode == "prepare":
        result = finalize(
            "FROZEN_AWAITING_EXECUTION",
            manifest,
            config,
            jobs,
        )
        print(
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "execution_authorized": activation[
                        "execution_authorized"
                    ],
                    "protocol_lock_sha256": digest(PROTOCOL_LOCK),
                    "expected_job_count": len(jobs),
                    "fresh_seed_count": len(SEEDS),
                    "state": result["state"],
                    "valid_for_numeric_UV_claim": False,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    if arguments.mode == "analyse":
        finalize("ANALYSE_ONLY", manifest, config, jobs)
        return
    execute(
        manifest,
        config,
        jobs,
        arguments.wall_cap_hours,
        arguments.maximum_new_jobs,
    )


if __name__ == "__main__":
    main()
