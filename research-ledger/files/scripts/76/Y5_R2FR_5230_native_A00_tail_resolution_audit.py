from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
import shutil
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
SOURCE_5229 = FUNCTIONAL_RG / "5229"
SOURCE = FUNCTIONAL_RG / "5230"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5229 = (
    POST / "scripts" / "Y5_R2FR_5229_fresh_native_chart_A00_replication.py"
)
CONFIG_5229 = SOURCE_5229 / "frozen_native_chart_A00_config.json"
RESULT_5229 = SOURCE_5229 / "fresh_native_chart_A00_results.json"
EVENT_ROWS_5229 = SOURCE_5229 / "fresh_native_chart_A00_event_rows.csv"
VALIDATION_5229 = RESIDUALS / "P8_Y5_BRR545_5229_VALIDATION.csv"
RUN_5229 = SOURCE_5229 / "runs" / "fresh_native_chart_A00_replication"

RUN_DIRECTORY = SOURCE / "runs" / "native_A00_tail_resolution_audit"
CLASSIFIER_CACHE = RUN_DIRECTORY / "grouped-classifier-cache"
MANIFEST = SOURCE / "frozen_tail_resolution_manifest.json"
CONFIG = SOURCE / "frozen_tail_resolution_config.json"
PROTOCOL_LOCK = SOURCE / "frozen_tail_resolution_protocol_lock.json"
RESULT = SOURCE / "native_A00_tail_resolution_audit.json"
COMPARISON = SOURCE / "native_A00_tail_resolution_comparison.csv"
DOCUMENT = POST / "5230-Y5-R2FR-native-A00-tail-resolution-audit.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5230_VALIDATION.csv"

MARKER = "MTS_5230_NATIVE_A00_TAIL_RESOLUTION_AUDIT"
RUN_ID = "native_A00_tail_resolution_audit"
TAIL_SEED = 731942010
PHYSICAL_A00_WEIGHT = -0.008
MAXIMUM_COMPONENT_RELATIVE_CHANGE = 1.0e-3
MAXIMUM_A00_RELATIVE_CHANGE = 0.05
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5229 = load_module(SCRIPT_5229, "mts_5229_for_5230")
M5224 = M5229.M5224
M5212 = M5229.M5212
M5036 = M5229.M5036


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


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
        raise RuntimeError(f"refusing to write empty CSV: {path}")
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


def all_pass(path: Path) -> bool:
    return all(
        row["passed"].strip().lower() == "true" for row in read_csv(path)
    )


def complex_from_row(value: dict[str, Any]) -> complex:
    return complex(float(value["real"]), float(value["imaginary"]))


def source_job(epsilon: str) -> dict[str, Any]:
    path = (
        RUN_5229
        / "topological-jobs"
        / (
            f"TOP__{epsilon}__S{TAIL_SEED}_N0000__"
            "A00__primary24.json"
        )
    )
    return read_json(path)


def jobs() -> list[dict[str, Any]]:
    return [
        {
            "schedule_key": (
                f"TOPOLOGICAL__{epsilon}__S{TAIL_SEED}_N0000__"
                "A00__audit32"
            ),
            "stratum": "topological",
            "job_key": (
                f"TAIL_AUDIT__{epsilon}__S{TAIL_SEED}_N0000__"
                "A00__audit32"
            ),
            "profile": "audit32",
            "epsilon_id": epsilon,
            "event_id": f"S{TAIL_SEED}_N0000",
            "seed": TAIL_SEED,
            "base_argument_id": "A00",
        }
        for epsilon in ("E040", "E020")
    ]


def make_manifest() -> dict[str, Any]:
    result_5229 = read_json(RESULT_5229)
    rows = read_csv(EVENT_ROWS_5229)
    selected = max(rows, key=lambda row: abs(float(row["A00_real"])))
    if not (
        result_5229["state"] == "COMPLETE_FRESH_NATIVE_CHART_REPLICATION"
        and result_5229["decision"]
        == "KEEP_A00_TRANCHES_SEPARATE_AND_DIAGNOSE_NATIVE_TAILS"
        and result_5229["validation_all_passed"]
        and all_pass(VALIDATION_5229)
        and int(selected["seed"]) == TAIL_SEED
    ):
        raise RuntimeError("checkpoint-5229 tail-selection chain changed")
    sources = [
        Path(__file__).resolve(),
        SCRIPT_5229,
        CONFIG_5229,
        RESULT_5229,
        EVENT_ROWS_5229,
        VALIDATION_5229,
    ]
    return {
        "checkpoint": 5230,
        "checkpoint_marker": MARKER,
        "locked_date": "2026-07-25",
        "source_outcomes_known_at_lock": True,
        "audit_outcomes_present_at_lock": False,
        "selection_rule": (
            "largest absolute fresh A00 event from checkpoint 5229"
        ),
        "selected_seed": TAIL_SEED,
        "source_A00_real": float(selected["A00_real"]),
        "source_profile": "primary24",
        "audit_profile": {
            "global_nodes": 32,
            "global_residue_nodes": 32,
            "relative_residue_nodes": 24,
            "relative_orders": [24],
        },
        "prelocked_gates": {
            "maximum_component_relative_change": (
                MAXIMUM_COMPONENT_RELATIVE_CHANGE
            ),
            "maximum_A00_relative_change": MAXIMUM_A00_RELATIVE_CHANGE,
            "retuning_after_outcomes_allowed": False,
        },
        "locked_sources": [
            {"path": str(path), "sha256": digest(path)}
            for path in sources
        ],
        "formalization_workbench_tree_sha256": M5229.tree_digest(FORMAL),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def make_config() -> dict[str, Any]:
    config = read_json(CONFIG_5229)
    config["checkpoint_marker"] = MARKER
    config["schema_revision"] = "native-A00-tail-audit32-v1"
    config["run_id"] = RUN_ID
    config["pilot_manifest"] = str(MANIFEST)
    config["pilot_manifest_digest"] = digest(MANIFEST)
    config["tiers"]["primary24"] = dict(config["tiers"]["audit32"])
    config["topology_cache_scope_correction"] = {
        "manager_run_directory": str(RUN_DIRECTORY),
        "source_checkpoint": 5230,
        "topology_generating_contract_unchanged": True,
    }
    config["source_files"][str(Path(__file__).resolve())] = digest(
        Path(__file__).resolve()
    )
    config.pop("config_digest", None)
    config["config_digest"] = M5036.canonical_digest(config)
    return config


def copy_classifier_cache() -> None:
    source = RUN_5229 / "grouped-classifier-cache"
    CLASSIFIER_CACHE.mkdir(parents=True, exist_ok=True)
    for candidate in source.rglob("*.json"):
        target = CLASSIFIER_CACHE / candidate.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            shutil.copy2(candidate, target)


def prepare() -> tuple[dict[str, Any], dict[str, Any]]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    RUN_DIRECTORY.mkdir(parents=True, exist_ok=True)
    if MANIFEST.exists():
        manifest = read_json(MANIFEST)
    else:
        if list(RUN_DIRECTORY.glob("topological-jobs/*.json")):
            raise RuntimeError("audit outcomes exist before manifest lock")
        manifest = make_manifest()
        atomic_json(MANIFEST, manifest)
    if CONFIG.exists():
        config = read_json(CONFIG)
    else:
        config = make_config()
        atomic_json(CONFIG, config)
    contract = {
        "manifest_sha256": digest(MANIFEST),
        "config_sha256": digest(CONFIG),
        "runner_sha256": digest(Path(__file__).resolve()),
        "jobs": jobs(),
        "gates": manifest["prelocked_gates"],
    }
    if PROTOCOL_LOCK.exists():
        if read_json(PROTOCOL_LOCK)["contract"] != contract:
            raise RuntimeError("checkpoint-5230 protocol changed after lock")
    else:
        if list(RUN_DIRECTORY.glob("topological-jobs/*.json")):
            raise RuntimeError("audit outcomes exist before protocol lock")
        atomic_json(
            PROTOCOL_LOCK,
            {
                "checkpoint": 5230,
                "checkpoint_marker": MARKER,
                "contract": contract,
                "audit_outcomes_present_at_lock": False,
                "threshold_retuning_after_outcomes_allowed": False,
            },
        )
    copy_classifier_cache()
    return manifest, config


def run(config: dict[str, Any]) -> None:
    M5224.RUN_DIRECTORY = RUN_DIRECTORY
    M5224.CLASSIFIER_CACHE = CLASSIFIER_CACHE
    M5224.RUNTIME_ROWS.clear()
    manager = M5224.install_runtime(config)
    for job in jobs():
        if M5212.cached_result(RUN_DIRECTORY, config, job) is not None:
            continue
        row = M5212.execute_job(RUN_DIRECTORY, config, manager, job)
        row.update(
            {
                "checkpoint_marker": MARKER,
                "source_profile": "primary24",
                "audit_profile": "audit32",
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
        M5229.atomic_json(M5212.output_path(RUN_DIRECTORY, job), row)
        print(
            json.dumps(
                {
                    "job": job["job_key"],
                    "status": row["status"],
                    "runtime_seconds": row["job_runtime_seconds"],
                }
            ),
            flush=True,
        )
        if row["status"] != "COMPLETED_CONVERGED":
            raise RuntimeError(f"tail audit failed: {row}")


def analyse(manifest: dict[str, Any], config: dict[str, Any]) -> None:
    source_values: dict[str, complex] = {}
    audit_values: dict[str, complex] = {}
    comparison_rows: list[dict[str, Any]] = []
    all_converged = True
    for job in jobs():
        epsilon = job["epsilon_id"]
        source = source_job(epsilon)
        audit = read_json(M5212.output_path(RUN_DIRECTORY, job))
        all_converged = all_converged and (
            audit["status"] == "COMPLETED_CONVERGED"
        )
        source_value = complex_from_row(
            source["normalized_topological_D_hhh_over_G3"]
        )
        audit_value = complex_from_row(
            audit["normalized_topological_D_hhh_over_G3"]
        )
        relative_change = abs(audit_value - source_value) / max(
            abs(source_value), 1.0e-300
        )
        source_values[epsilon] = source_value
        audit_values[epsilon] = audit_value
        comparison_rows.append(
            {
                "epsilon_id": epsilon,
                "source_real": source_value.real,
                "source_imaginary": source_value.imag,
                "audit_real": audit_value.real,
                "audit_imaginary": audit_value.imag,
                "absolute_change": abs(audit_value - source_value),
                "relative_change": relative_change,
                "source_crossings": source["crossing_count"],
                "audit_crossings": audit["crossing_count"],
                "audit_status": audit["status"],
            }
        )
    write_csv(COMPARISON, comparison_rows)
    source_a00 = PHYSICAL_A00_WEIGHT * (
        2.0 * source_values["E020"] - source_values["E040"]
    )
    audit_a00 = PHYSICAL_A00_WEIGHT * (
        2.0 * audit_values["E020"] - audit_values["E040"]
    )
    a00_relative_change = abs(audit_a00 - source_a00) / max(
        abs(source_a00), 1.0e-300
    )
    component_gate = all(
        float(row["relative_change"]) <= MAXIMUM_COMPONENT_RELATIVE_CHANGE
        for row in comparison_rows
    )
    a00_gate = a00_relative_change <= MAXIMUM_A00_RELATIVE_CHANGE
    stable = all_converged and component_gate and a00_gate
    decision = (
        "CLASSIFY_FRESH_A00_SPIKE_AS_NUMERICALLY_STABLE_NATIVE_TAIL"
        if stable
        else "TAIL_REQUIRES_NUMERICAL_REPAIR_BEFORE_INFERENCE"
    )
    formal_digest = M5229.tree_digest(FORMAL)
    result = {
        "checkpoint": 5230,
        "checkpoint_marker": MARKER,
        "state": "COMPLETE_TAIL_RESOLUTION_AUDIT",
        "decision": decision,
        "selected_seed": TAIL_SEED,
        "all_audit_jobs_converged": all_converged,
        "component_gate_passed": component_gate,
        "A00_gate_passed": a00_gate,
        "source_A00": {
            "real": source_a00.real,
            "imaginary": source_a00.imag,
        },
        "audit_A00": {
            "real": audit_a00.real,
            "imaginary": audit_a00.imag,
        },
        "A00_relative_change": a00_relative_change,
        "comparison_rows": comparison_rows,
        "next_action": (
            "derive a heavy-tail-compatible estimator and validate it on "
            "a new native-chart tranche; do not relax checkpoint-5229's "
            "pooling gate"
            if stable
            else "repair or refine the tail event before any pooling"
        ),
        "protocol_lock_sha256": digest(PROTOCOL_LOCK),
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    expected_decision = (
        "CLASSIFY_FRESH_A00_SPIKE_AS_NUMERICALLY_STABLE_NATIVE_TAIL"
        if stable
        else "TAIL_REQUIRES_NUMERICAL_REPAIR_BEFORE_INFERENCE"
    )
    validation_rows = [
        {
            "check": "checkpoint_5229_source_is_valid",
            "passed": (
                read_json(RESULT_5229)["validation_all_passed"]
                and all_pass(VALIDATION_5229)
            ),
            "detail": read_json(RESULT_5229)["decision"],
        },
        {
            "check": "protocol_lock_matches_current_runner",
            "passed": read_json(PROTOCOL_LOCK)["contract"][
                "runner_sha256"
            ]
            == digest(Path(__file__).resolve()),
            "detail": digest(Path(__file__).resolve()),
        },
        {
            "check": "tail_selection_rule_is_reproducible",
            "passed": max(
                read_csv(EVENT_ROWS_5229),
                key=lambda row: abs(float(row["A00_real"])),
            )["seed"]
            == str(TAIL_SEED),
            "detail": str(TAIL_SEED),
        },
        {
            "check": "both_audit_jobs_converged",
            "passed": all_converged,
            "detail": "2/2" if all_converged else "audit failure",
        },
        {
            "check": "decision_matches_frozen_resolution_gates",
            "passed": decision == expected_decision,
            "detail": (
                f"component={component_gate}; A00={a00_gate}; "
                f"A00_relative_change={a00_relative_change}"
            ),
        },
        {
            "check": "thresholds_not_retuned",
            "passed": not manifest["prelocked_gates"][
                "retuning_after_outcomes_allowed"
            ],
            "detail": "frozen before audit outcomes",
        },
        {
            "check": "formalization_workbench_unchanged",
            "passed": formal_digest == FORMAL_BASELINE,
            "detail": formal_digest,
        },
        {
            "check": "all_claim_flags_remain_false",
            "passed": not any(
                (
                    result["valid_for_numeric_UV_claim"],
                    result["valid_for_local_GR_claim"],
                    result["valid_for_full_MTS_claim"],
                )
            ),
            "detail": "numeric UV, local GR and full MTS remain false",
        },
    ]
    validation_all_passed = all(
        bool(row["passed"]) for row in validation_rows
    )
    result["validation_all_passed"] = validation_all_passed
    result["validation_check_count"] = len(validation_rows)
    atomic_json(RESULT, result)
    write_csv(VALIDATION, validation_rows)
    document = f"""# 5230 - Native A00 tail resolution audit

## Result

Checkpoint 5229's largest fresh event was selected by a frozen rule and
rerun with the established `audit32` quadrature profile.

Decision: `{decision}`.

## Comparison

- Seed: `{TAIL_SEED}`.
- Source A00: `{source_a00.real:.12g} {source_a00.imag:+.12g} i`.
- Audit A00: `{audit_a00.real:.12g} {audit_a00.imag:+.12g} i`.
- A00 relative change: `{a00_relative_change:.9g}`.
- Maximum component relative change:
  `{max(float(row['relative_change']) for row in comparison_rows):.9g}`.
- Both audit jobs converged: `{all_converged}`.

## Interpretation

If stable, the positive spike is not removed as a numerical accident. It
is evidence that the native A00 distribution is genuinely heavy-tailed:
the old tranche contained a comparable negative spike, while the fresh
tranche contains this positive one. The checkpoint-5229 pooling gate
therefore remains binding rather than being relaxed after inspection.

The next admissible step is a mathematically specified robust estimator
validated on another unseen native-chart tranche, not clipping or deleting
the event.

## Claim boundary

This audit does not establish a numerical ultraviolet coefficient, local
GR, the galaxy branch, or full MTS.

## Evidence

- Manifest: `{MANIFEST}`
- Comparison: `{COMPARISON}`
- Result: `{RESULT}`
- Validation: `{VALIDATION}`
"""
    atomic_text(DOCUMENT, document)
    if not validation_all_passed:
        raise RuntimeError(
            "checkpoint-5230 validation failed: "
            + json.dumps(
                [row for row in validation_rows if not row["passed"]],
                indent=2,
            )
        )
    print(json.dumps(result, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("prepare", "run", "analyse", "all"), default="all"
    )
    arguments = parser.parse_args()
    manifest, config = prepare()
    if arguments.mode == "prepare":
        print(
            json.dumps(
                {
                    "checkpoint": 5230,
                    "state": "PREPARED",
                    "seed": TAIL_SEED,
                    "protocol_lock_sha256": digest(PROTOCOL_LOCK),
                },
                indent=2,
            )
        )
        return
    if arguments.mode in ("run", "all"):
        run(config)
    analyse(manifest, config)


if __name__ == "__main__":
    main()
