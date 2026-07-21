from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

import numpy as np


POST = Path(__file__).resolve().parents[1]
SCRIPT_5052 = POST / "scripts" / "Y5_R2FR_5052_unit_richardson_seed_jackknife.py"
SOURCE_5052 = POST / "source-intake" / "functional_rg" / "5052"
SOURCE = POST / "source-intake" / "functional_rg" / "5053"
RESULT_JSON = SOURCE / "high_low_cost_provenance_and_reuse_audit.json"
ROW_CSV = SOURCE / "high_low_cost_rows.csv"
EVENT_CSV = SOURCE / "high_low_event_costs.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5053_VALIDATION.csv"
)
MARKER = "MTS_5053_HIGH_LOW_COST_PROVENANCE_AND_REUSE_AUDIT"
REVISION = "runtime-source-and-topology-reuse-v1"
PROFILE = "coarse12"
EXECUTION_CAP_HOURS = 10.0
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5052 = load_module("mts_5052_for_cost_audit", SCRIPT_5052)
M5051 = M5052.M5051
M5049 = M5052.M5049
M5044 = M5052.M5044


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def runtime_source(row: dict[str, Any]) -> tuple[dict[str, Any], Path]:
    current = row
    current_path: Path | None = None
    while float(current.get("job_runtime_seconds", 0.0) or 0.0) <= 0.0:
        imported = current.get("imported_from")
        if not imported:
            raise RuntimeError(f"no runtime source for {row['job_key']}")
        current_path = M5049.M5043.localize_stale_path(str(imported["source_job"]))
        current = json.loads(current_path.read_text(encoding="utf-8"))
    if current_path is None:
        key = str(current["job_key"])
        current_path = M5049.M5043.RUN_5040 / "jobs" / f"{key}.json"
        if not current_path.exists():
            raise FileNotFoundError(current_path)
    return current, current_path


def topology_artifact(source_job: Path, event_id: str, epsilon_id: str, base_id: str) -> Path:
    topologies = source_job.parent.parent / "topologies"
    alternate = M5049.M5043.CENTRAL_TOPOLOGY_IDS.get(base_id)
    names = [f"{event_id}__{epsilon_id}_{base_id}.json"]
    if alternate is not None:
        names.append(f"{event_id}__{epsilon_id}_{alternate}.json")
    candidates = [topologies / name for name in names]
    existing = [path for path in candidates if path.exists()]
    if len(existing) != 1:
        raise RuntimeError(
            f"expected one topology for {event_id}/{epsilon_id}/{base_id}, got {existing}"
        )
    return existing[0]


def main() -> None:
    source_5052_path = SOURCE_5052 / "unit_richardson_seed_jackknife.json"
    if not SCRIPT_5052.exists() or not source_5052_path.exists():
        raise FileNotFoundError("checkpoint 5052 inputs are missing")
    M5049.configure_modules()
    try:
        scope = M5049.strict_scope_audit(PROFILE)
        if not scope["all_theorem_zeros_within_restricted_scope"]:
            raise RuntimeError("restricted theorem-scope audit failed")
        M5044.M5043 = M5049.M5043
        config = M5049.M5043.load_config()
        events = sorted(config["events"], key=lambda row: (row["seed"], row["sample_index"]))
        base_ids = sorted(M5049.M5043.argument_lookup(config))
        rows = []
        event_rows = []
        for event in events:
            event_id = str(event["event_id"])
            event_high_primary = 0.0
            event_high_topology = 0.0
            event_high_kernel = 0.0
            event_low_topology = 0.0
            event_low_kernel = 0.0
            event_topology_paths: list[str] = []
            for base_id in base_ids:
                low_path = M5049.M5043.result_path(PROFILE, event_id, base_id)
                low = json.loads(low_path.read_text(encoding="utf-8"))
                e020 = M5049.M5043.primary_job("E020", event_id, base_id)
                e040 = M5049.M5043.primary_job("E040", event_id, base_id)
                source020, path020 = runtime_source(e020)
                source040, path040 = runtime_source(e040)
                topology020 = topology_artifact(path020, event_id, "E020", base_id)
                topology040 = topology_artifact(path040, event_id, "E040", base_id)
                low_topology = M5049.M5043.localize_stale_path(str(low["topology_source"]))
                runtime020 = float(source020["job_runtime_seconds"])
                runtime040 = float(source040["job_runtime_seconds"])
                topology_runtime020 = float(source020["topology_runtime_seconds"])
                topology_runtime040 = float(source040["topology_runtime_seconds"])
                kernel_runtime020 = runtime020 - topology_runtime020
                kernel_runtime040 = runtime040 - topology_runtime040
                low_kernel_runtime = float(low["kernel_runtime_seconds"])
                if min(kernel_runtime020, kernel_runtime040, low_kernel_runtime) < 0.0:
                    raise RuntimeError("negative measured kernel runtime")
                event_high_primary += runtime020 + runtime040
                event_high_topology += topology_runtime020 + topology_runtime040
                event_high_kernel += kernel_runtime020 + kernel_runtime040
                event_low_topology += topology_runtime040
                event_low_kernel += low_kernel_runtime
                event_topology_paths.extend((str(topology020), str(topology040)))
                rows.append(
                    {
                        "event_id": event_id,
                        "base_argument_id": base_id,
                        "e020_source_job": str(path020),
                        "e040_source_job": str(path040),
                        "e020_topology": str(topology020),
                        "e040_topology": str(topology040),
                        "low_topology": str(low_topology),
                        "e020_topology_sha256": digest(topology020),
                        "e040_topology_sha256": digest(topology040),
                        "low_topology_sha256": digest(low_topology),
                        "e020_e040_topology_identical": digest(topology020) == digest(topology040),
                        "low_reuses_e040_topology": digest(low_topology) == digest(topology040),
                        "e020_job_runtime_seconds": runtime020,
                        "e040_job_runtime_seconds": runtime040,
                        "e020_topology_runtime_seconds": topology_runtime020,
                        "e040_topology_runtime_seconds": topology_runtime040,
                        "e020_kernel_runtime_seconds": kernel_runtime020,
                        "e040_kernel_runtime_seconds": kernel_runtime040,
                        "low_kernel_runtime_seconds": low_kernel_runtime,
                    }
                )
            distinct_topologies = len(set(event_topology_paths))
            high_correction_cost = event_high_primary + event_low_kernel
            low_only_cost = event_low_topology + event_low_kernel
            event_rows.append(
                {
                    "event_id": event_id,
                    "high_primary_cost_seconds": event_high_primary,
                    "high_topology_cost_seconds": event_high_topology,
                    "high_primary_kernel_cost_seconds": event_high_kernel,
                    "paired_low_kernel_cost_seconds": event_low_kernel,
                    "paired_high_correction_cost_seconds": high_correction_cost,
                    "low_only_topology_cost_seconds": event_low_topology,
                    "low_only_kernel_cost_seconds": event_low_kernel,
                    "low_only_total_cost_seconds": low_only_cost,
                    "expected_high_topology_artifacts": 2 * len(base_ids),
                    "distinct_high_topology_artifacts": distinct_topologies,
                    "duplicate_high_topology_charges": 2 * len(base_ids) - distinct_topologies,
                }
            )
        mean_high_primary = float(np.mean([row["high_primary_cost_seconds"] for row in event_rows]))
        mean_high_correction = float(
            np.mean([row["paired_high_correction_cost_seconds"] for row in event_rows])
        )
        mean_low_only = float(np.mean([row["low_only_total_cost_seconds"] for row in event_rows]))
        mean_low_kernel = float(np.mean([row["low_only_kernel_cost_seconds"] for row in event_rows]))
        mean_low_topology = float(
            np.mean([row["low_only_topology_cost_seconds"] for row in event_rows])
        )
        source_5052 = json.loads(source_5052_path.read_text(encoding="utf-8"))
        source_full = source_5052["full_panel"]
        source_5051_path = M5051.SOURCE / "phase_covariant_complex_control_gate.json"
        source_5051 = json.loads(source_5051_path.read_text(encoding="utf-8"))
        selected = source_5051["selected"]
        variance_high = np.asarray(selected["variance_high"], dtype=float)
        variance_correction = np.asarray(selected["variance_crossfit_correction"], dtype=float)
        variance_low = np.asarray(selected["variance_low_contribution"], dtype=float)
        real_margins = np.asarray(
            [
                float(row["target_equivalence_margin"])
                for row in config["target_precision_budgets"]
            ]
        )
        margins = np.concatenate((real_margins, real_margins))
        base_score = float(np.max(np.sqrt(variance_high * mean_high_primary) / margins))
        allocations = []
        for ratio in np.geomspace(0.25, 512.0, 4097):
            variance_cost = (
                variance_correction + variance_low / ratio
            ) * (mean_high_correction + ratio * mean_low_only)
            score = float(np.max(np.sqrt(np.maximum(variance_cost, 0.0)) / margins))
            allocations.append((float(ratio), score))
        optimal_ratio, score = min(allocations, key=lambda row: row[1])
        minimum_high_units = 4
        minimum_low_units = int(np.ceil(minimum_high_units * optimal_ratio))
        corrected_projected_hours = (
            minimum_high_units * mean_high_correction + minimum_low_units * mean_low_only
        ) / 3600.0
        e020_e040_identical = sum(bool(row["e020_e040_topology_identical"]) for row in rows)
        low_e040_reuse = sum(bool(row["low_reuses_e040_topology"]) for row in rows)
        duplicate_charges = sum(int(row["duplicate_high_topology_charges"]) for row in event_rows)
        result = {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "cost_contract": {
                "paired_high_correction": "cost(E020 primary)+cost(E040 primary)+cost(E040 coarse kernel)",
                "low_only": "cost(E040 topology)+cost(E040 coarse kernel)",
                "paired_reuse": "coarse E040 reuses the E040 primary topology within each high event",
            },
            "row_count": len(rows),
            "event_count": len(event_rows),
            "mean_high_primary_event_cost_seconds": mean_high_primary,
            "mean_paired_high_correction_event_cost_seconds": mean_high_correction,
            "mean_low_only_topology_event_cost_seconds": mean_low_topology,
            "mean_low_only_kernel_event_cost_seconds": mean_low_kernel,
            "mean_low_only_total_event_cost_seconds": mean_low_only,
            "paired_high_missing_low_kernel_charge_seconds": mean_high_correction - mean_high_primary,
            "e020_e040_identical_topology_rows": e020_e040_identical,
            "low_rows_reusing_e040_topology": low_e040_reuse,
            "duplicate_high_topology_charges": duplicate_charges,
            "reuse_safe_findings": {
                "paired_low_reuses_e040_topology": low_e040_reuse == len(rows),
                "e020_and_e040_topologies_reusable": e020_e040_identical == len(rows),
                "high_topology_cost_double_counted": duplicate_charges > 0,
                "fresh_low_only_topology_can_be_omitted": False,
            },
            "source_5052_projected_hours": source_full["projected_minimum_pilot_hours"],
            "corrected_optimal_low_to_high_sample_ratio": optimal_ratio,
            "corrected_equal_cost_score_ratio": score / base_score,
            "high_only_baseline_event_cost_seconds": mean_high_primary,
            "corrected_minimum_high_units": minimum_high_units,
            "corrected_minimum_low_units": minimum_low_units,
            "corrected_projected_minimum_pilot_hours": corrected_projected_hours,
            "execution_cap_hours": EXECUTION_CAP_HOURS,
            "execution_authorized": corrected_projected_hours <= EXECUTION_CAP_HOURS,
            "decision": (
                "PILOT_WITHIN_CAP"
                if corrected_projected_hours <= EXECUTION_CAP_HOURS
                else "NO_REUSE_SAFE_ROUTE_BELOW_CAP"
            ),
            "restricted_scope_audit": scope,
            "source_5052_sha256": digest(source_5052_path),
            "formalization_workbench_tree_sha256": M5049.M5043.tree_digest(
                POST.parent / "formalization-workbench"
            ),
            "valid_for_full_MTS_claim": False,
        }
        atomic_json(RESULT_JSON, result)
        SOURCE.mkdir(parents=True, exist_ok=True)
        with ROW_CSV.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        with EVENT_CSV.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(event_rows[0]))
            writer.writeheader()
            writer.writerows(event_rows)
        checks = [
            ("source_5052_exists", source_5052_path.exists(), str(source_5052_path)),
            ("all_120_rows_audited", len(rows) == 120, str(len(rows))),
            (
                "all_low_rows_reuse_exact_e040_topology",
                low_e040_reuse == len(rows),
                f"{low_e040_reuse}/{len(rows)}",
            ),
            (
                "e020_e040_reuse_not_assumed",
                not result["reuse_safe_findings"]["e020_and_e040_topologies_reusable"],
                f"identical={e020_e040_identical}/{len(rows)}",
            ),
            (
                "no_duplicate_high_topology_charges",
                duplicate_charges == 0,
                str(duplicate_charges),
            ),
            (
                "paired_high_includes_low_kernel",
                mean_high_correction > mean_high_primary,
                f"increment={mean_high_correction - mean_high_primary}",
            ),
            (
                "fresh_low_topology_retained",
                not result["reuse_safe_findings"]["fresh_low_only_topology_can_be_omitted"],
                "required false",
            ),
            (
                "restricted_scope_passes",
                scope["all_theorem_zeros_within_restricted_scope"],
                f"strict={scope['strict_scope_rows']}; total={scope['theorem_zero_rows']}",
            ),
            ("fresh_evidence_not_claimed", not result["valid_for_full_MTS_claim"], "required false"),
            (
                "formalization_workbench_unchanged",
                result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE,
                result["formalization_workbench_tree_sha256"],
            ),
        ]
        validation = [
            {"check": name, "passed": str(bool(passed)).lower(), "evidence": evidence}
            for name, passed, evidence in checks
        ]
        VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
        with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=("check", "passed", "evidence"))
            writer.writeheader()
            writer.writerows(validation)
        print(
            json.dumps(
                {
                    "mean_high_primary_seconds": mean_high_primary,
                    "mean_paired_high_correction_seconds": mean_high_correction,
                    "mean_low_only_seconds": mean_low_only,
                    "e020_e040_identical_topology_rows": e020_e040_identical,
                    "duplicate_high_topology_charges": duplicate_charges,
                    "corrected_score_ratio": result["corrected_equal_cost_score_ratio"],
                    "corrected_minimum_low_units": minimum_low_units,
                    "corrected_projected_hours": corrected_projected_hours,
                    "decision": result["decision"],
                    "validation_passed": sum(row["passed"] == "true" for row in validation),
                    "validation_total": len(validation),
                },
                indent=2,
            )
        )
    finally:
        M5049.restore_modules()


if __name__ == "__main__":
    main()
