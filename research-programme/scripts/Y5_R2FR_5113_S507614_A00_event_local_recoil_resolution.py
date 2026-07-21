from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from typing import Any

import mpmath as mp


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5112 = (
    POST
    / "scripts"
    / "Y5_R2FR_5112_recoil_holomorphy_scope_correction.py"
)
PARENT_GATE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5112"
    / "recoil_holomorphy_scope_correction.json"
)
PARENT_REGISTRY = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5112"
    / "event_local_direct_zero_registry.json"
)
RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5111"
    / "runs"
    / "E020_primary_complex_control_extension_v1"
)
JOB_KEY = "E020__S507614_N0000__A00__primary24"
JOB = RUN / "jobs" / f"{JOB_KEY}.json"
KERNEL = RUN / "kernels" / f"{JOB_KEY}.json"
SOURCE = POST / "source-intake" / "functional_rg" / "5113"
RESULT_JSON = SOURCE / "S507614_A00_event_local_recoil_resolution.json"
REGISTRY_JSON = SOURCE / "event_local_direct_zero_registry_v2.json"
AUDIT_CSV = SOURCE / "S507614_A00_direct_component_audit.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5113_VALIDATION.csv"
)
MARKER = "MTS_5113_S507614_A00_EVENT_LOCAL_RECOIL_RESOLUTION"
REVISION = "exact-job-direct-component-arbitrary-precision-extension-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5112 = load_module("mts_5112_for_5113", SCRIPT_5112)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def source_records() -> list[dict[str, Any]]:
    job = json.loads(JOB.read_text(encoding="utf-8"))
    kernel = json.loads(KERNEL.read_text(encoding="utf-8"))
    if job["status"] != "COMPLETED_UNCONVERGED":
        raise RuntimeError("5113 source job is no longer the unconverged record")
    adjustments = job["profile_audit"]["residue_radius_adjustments"]
    unresolved = [row for row in adjustments if not bool(row["selected_stable"])]
    return [
        {
            "scope": "5113_exact_unconverged_recoil_row",
            "job_key": JOB_KEY,
            "event": kernel["event"],
            "argument": kernel["argument"],
            "pairs": row["pairs"],
            "root": row["root"],
            "safe_scale": float(row["safe_scale"]),
            "source_job": str(JOB.resolve()),
            "source_job_sha256": digest(JOB),
            "source_kernel": str(KERNEL.resolve()),
            "source_kernel_sha256": digest(KERNEL),
            "double_precision_candidates": row["candidate_rows"],
        }
        for row in unresolved
    ]


def write_audit(rows: list[dict[str, Any]]) -> None:
    AUDIT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=(
                "job_key",
                "pairs",
                "root_real",
                "root_imaginary",
                "root_modulus",
                "mean_real",
                "mean_imaginary",
                "maximum_magnitude",
                "maximum_spread",
                "classification",
            ),
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "job_key": row["job_key"],
                    "pairs": json.dumps(row["pairs"], separators=(",", ":")),
                    "root_real": row["root"]["real"],
                    "root_imaginary": row["root"]["imaginary"],
                    "root_modulus": row["root_modulus"],
                    "mean_real": row["mean"]["real"],
                    "mean_imaginary": row["mean"]["imaginary"],
                    "maximum_magnitude": row["maximum_magnitude"],
                    "maximum_spread": row["maximum_spread"],
                    "classification": row["classification"],
                }
            )


def main() -> None:
    mp.mp.dps = 60
    records = source_records()
    evaluated = [
        M5112.evaluate_record(
            record,
            relative_nodes=24,
            global_nodes=24,
            relative_fractions=(0.1, 0.05),
            global_fractions=(0.15, 0.3),
        )
        for record in records
    ]
    parent_gate = json.loads(PARENT_GATE.read_text(encoding="utf-8"))
    parent_registry = json.loads(PARENT_REGISTRY.read_text(encoding="utf-8"))
    new_zero_rows = [
        M5112.registry_row(row)
        for row in evaluated
        if row["classification"] == "EVENT_LOCAL_ARBITRARY_PRECISION_ZERO"
    ]
    registry = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "policy": "merged exact-event arbitrary-precision zero registry",
        "parent_registry": str(PARENT_REGISTRY.resolve()),
        "parent_registry_sha256": digest(PARENT_REGISTRY),
        "rows": [*parent_registry["rows"], *new_zero_rows],
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(REGISTRY_JSON, registry)
    write_audit(evaluated)
    formal_hash = M5112.tree_digest(FORMAL)
    checks = [
        ("formalization_workbench_unchanged", formal_hash == FORMAL_BASELINE, formal_hash),
        ("source_job_is_unconverged", len(records) > 0, str(len(records))),
        ("exactly_two_unstable_rows", len(records) == 2, str(len(records))),
        (
            "all_rows_resolved",
            all(row["classification"] != "UNRESOLVED" for row in evaluated),
            json.dumps([row["classification"] for row in evaluated]),
        ),
        (
            "all_rows_are_event_local_zeros",
            len(new_zero_rows) == len(evaluated),
            str(len(new_zero_rows)),
        ),
        (
            "parent_5112_gate_passed",
            bool(parent_gate["passed"] and parent_gate["runner_integration_authorized"]),
            parent_gate["checkpoint_marker"],
        ),
        (
            "registry_count_extended_exactly",
            len(registry["rows"]) == len(parent_registry["rows"]) + len(new_zero_rows),
            str(len(registry["rows"])),
        ),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("check", "passed", "detail"))
        for name, passed, detail in checks:
            writer.writerow((name, str(bool(passed)).lower(), detail))
    passed = all(row[1] for row in checks)
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "job_key": JOB_KEY,
        "records": evaluated,
        "parent_scope_correction_gate": str(PARENT_GATE.resolve()),
        "parent_scope_correction_gate_sha256": digest(PARENT_GATE),
        "parent_registry": str(PARENT_REGISTRY.resolve()),
        "parent_registry_sha256": digest(PARENT_REGISTRY),
        "merged_registry": str(REGISTRY_JSON.resolve()),
        "merged_registry_sha256": digest(REGISTRY_JSON),
        "new_event_local_zero_count": len(new_zero_rows),
        "runner_integration_authorized": passed,
        "formalization_workbench_tree_sha256": formal_hash,
        "passed": passed,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "new_event_local_zero_count": len(new_zero_rows),
                "classifications": [row["classification"] for row in evaluated],
                "runner_integration_authorized": passed,
                "passed": passed,
            },
            indent=2,
        )
    )
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
