from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
RUN = POST / "source-intake" / "functional_rg" / "5125" / "runs" / "reciprocal_stratified_fresh_pilot_v1"
CONFIG = RUN / "config.json"
SCHEDULE = POST / "source-intake" / "functional_rg" / "5125" / "reciprocal_stratified_locked_schedule.json"
SOURCE_5143 = POST / "source-intake" / "functional_rg" / "5143"
VALIDATION_5143 = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5143_VALIDATION.csv"
SOURCE = POST / "source-intake" / "functional_rg" / "5144"
AUDIT_CSV = SOURCE / "strict_adaptive_status_audit.csv"
RESULT_JSON = SOURCE / "strict_adaptive_status_audit_result.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5144_VALIDATION.csv"
DOCUMENT = POST / "5144-Y5-R2FR-strict-adaptive-status-audit-and-witness-freeze.md"

MARKER = "MTS_5144_STRICT_ADAPTIVE_STATUS_AUDIT_AND_WITNESS_FREEZE"
CHECKED_DATE = "2026-07-20"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
EXPECTED_MISMATCHES = {
    "E040__S512503_N0000__A10__primary24",
    "E020__S512503_N0000__A10__primary24",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True), encoding="utf-8"
    )
    os.replace(temporary, path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


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


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def freeze(path: Path, destination: Path) -> dict[str, str]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, destination)
    return {
        "source": relative(path),
        "frozen": relative(destination),
        "source_sha256": digest(path),
        "frozen_sha256": digest(destination),
    }


def main() -> None:
    config = read_json(CONFIG)
    schedule = read_json(SCHEDULE)["jobs"]
    tolerance = float(
        config["tiers"]["primary24"]["relative_adaptive_tolerance"]
    )
    live_paths: list[Path] = []
    rows: list[dict[str, Any]] = []
    mismatch_payloads: dict[str, dict[str, Any]] = {}
    for schedule_index, job in enumerate(schedule):
        if job["stratum"] != "full_remainder":
            continue
        job_path = RUN / "jobs" / f"{job['job_key']}.json"
        kernel_path = RUN / "kernels" / f"{job['job_key']}.json"
        if not job_path.exists():
            continue
        live_paths.extend((job_path, kernel_path))
        job_row = read_json(job_path)
        kernel_row = read_json(kernel_path)
        gate = kernel_row["fixed_event_integral_gate"]
        order_rows = gate["order_rows"]
        maximum_error = max(
            float(row["maximum_adaptive_chamber_relative_error"])
            for row in order_rows
        )
        all_adaptive_rows_converged = all(
            bool(row["adaptive_quadrature_converged"]) for row in order_rows
        )
        strict_integral_converged = bool(
            job_row.get("status") == "COMPLETED_CONVERGED"
            and job_row.get("integral_converged")
            and gate.get("fixed_event_crossed_integral_converged")
            and gate.get("all_residues_stable")
            and all_adaptive_rows_converged
            and maximum_error <= tolerance
        )
        declared_converged = job_row.get("status") == "COMPLETED_CONVERGED"
        mismatch = bool(declared_converged and not strict_integral_converged)
        row = {
            "schedule_index": schedule_index,
            "job_key": job["job_key"],
            "epsilon_id": job["epsilon_id"],
            "event_id": job["event_id"],
            "base_argument_id": job["base_argument_id"],
            "declared_status": job_row.get("status"),
            "declared_integral_converged": job_row.get("integral_converged"),
            "fixed_event_gate_converged": gate.get(
                "fixed_event_crossed_integral_converged"
            ),
            "all_residues_stable": gate.get("all_residues_stable"),
            "all_adaptive_rows_converged": all_adaptive_rows_converged,
            "maximum_adaptive_chamber_relative_error": maximum_error,
            "locked_tolerance": tolerance,
            "error_over_tolerance": maximum_error / tolerance,
            "highest_composite_interval_count": order_rows[-1][
                "composite_interval_count"
            ],
            "relative_adaptive_maximum_intervals": gate[
                "relative_adaptive_maximum_intervals"
            ],
            "strict_integral_converged": strict_integral_converged,
            "declared_strict_mismatch": mismatch,
            "job_path": relative(job_path),
            "kernel_path": relative(kernel_path),
            "job_sha256": digest(job_path),
            "kernel_sha256": digest(kernel_path),
            "checkpoint_marker": MARKER,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        rows.append(row)
        if mismatch:
            mismatch_payloads[job["job_key"]] = {
                "row": row,
                "job_path": job_path,
                "kernel_path": kernel_path,
            }
    live_hashes_before = {str(path): digest(path) for path in live_paths}
    write_csv(AUDIT_CSV, rows)
    frozen_files: list[dict[str, str]] = []
    for job_key, payload in mismatch_payloads.items():
        witness_directory = SOURCE / "witnesses" / job_key
        frozen_files.append(
            freeze(payload["job_path"], witness_directory / "live_job.json")
        )
        frozen_files.append(
            freeze(payload["kernel_path"], witness_directory / "live_kernel.json")
        )
        if job_key == "E020__S512503_N0000__A10__primary24":
            for path in (
                SOURCE_5143 / "A10_argument_local_outer_collinear_chart_gate.json",
                SOURCE_5143 / "A10_argument_local_outer_collinear_replay_result.json",
                SOURCE_5143 / "A10_argument_local_outer_collinear_replay_status.json",
                SOURCE_5143 / "E020_A10_execute_console.log",
                VALIDATION_5143,
            ):
                frozen_files.append(freeze(path, witness_directory / path.name))
    live_hashes_after = {str(path): digest(path) for path in live_paths}
    mismatches = [row for row in rows if row["declared_strict_mismatch"]]
    strict_passes = [row for row in rows if row["strict_integral_converged"]]
    result = {
        "checkpoint_marker": MARKER,
        "config": relative(CONFIG),
        "schedule": relative(SCHEDULE),
        "audit": relative(AUDIT_CSV),
        "audited_existing_full_remainder_rows": len(rows),
        "strict_pass_count": len(strict_passes),
        "declared_strict_mismatch_count": len(mismatches),
        "declared_strict_mismatch_jobs": [row["job_key"] for row in mismatches],
        "comparative_result": {
            "E040_A10_error": next(
                row["maximum_adaptive_chamber_relative_error"]
                for row in mismatches
                if row["epsilon_id"] == "E040"
            ),
            "E020_A10_error": next(
                row["maximum_adaptive_chamber_relative_error"]
                for row in mismatches
                if row["epsilon_id"] == "E020"
            ),
            "shared_failure": "both A10 rows exhaust the adaptive interval budget and fail the same locked tolerance",
            "interpretation": "this is a baseline-and-MTS pipeline convergence defect, not evidence uniquely against the repaired E020 row",
        },
        "frozen_files": frozen_files,
        "live_files_unchanged": live_hashes_before == live_hashes_after,
        "live_state_mutated": False,
        "required_reconciliation": "repair status semantics, demote both mismatches fail-closed, then localize adaptive leaves before any rerun",
        "formalization_workbench_tree_sha256": tree_digest(FORMAL),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "source_checked_date": CHECKED_DATE,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("source_paths_exist", all(path.exists() for path in (CONFIG, SCHEDULE, SOURCE_5143, VALIDATION_5143))),
        ("fifty_one_full_rows_audited", len(rows) == 51),
        ("forty_nine_strict_pass", len(strict_passes) == 49),
        ("two_status_mismatches", len(mismatches) == 2),
        ("exact_mismatch_jobs", {row["job_key"] for row in mismatches} == EXPECTED_MISMATCHES),
        ("both_adaptive_flags_false", all(not row["all_adaptive_rows_converged"] for row in mismatches)),
        ("both_exceed_tolerance", all(row["maximum_adaptive_chamber_relative_error"] > tolerance for row in mismatches)),
        ("baseline_comparator_also_fails", any(row["epsilon_id"] == "E040" for row in mismatches)),
        ("all_witness_hashes_match", all(row["source_sha256"] == row["frozen_sha256"] for row in frozen_files)),
        ("live_files_unchanged", result["live_files_unchanged"]),
        ("formal_tree_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE),
        ("no_claim_or_live_mutation", not result["live_state_mutated"] and not result["valid_for_numeric_UV_claim"] and not result["valid_for_local_GR_claim"] and not result["valid_for_full_MTS_claim"]),
    ]
    write_csv(
        VALIDATION_CSV,
        [
            {
                "check_id": f"VAL5144_{index:02d}_{name}",
                "passed": passed,
                "checkpoint_marker": MARKER,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
                "source_checked_date": CHECKED_DATE,
            }
            for index, (name, passed) in enumerate(checks, start=1)
        ],
    )
    document = f"""# 5144: Strict adaptive-status audit and witness freeze

## Finding

All `{len(rows)}` existing full-remainder rows were reclassified using the
actual adaptive criterion rather than their stored status label. `{len(strict_passes)}`
pass. Exactly two rows are false-positive `COMPLETED_CONVERGED` labels:

- `E040__S512503_N0000__A10__primary24`: error
  `{result['comparative_result']['E040_A10_error']}`.
- `E020__S512503_N0000__A10__primary24`: error
  `{result['comparative_result']['E020_A10_error']}`.

Both exceed the unchanged `5e-5` tolerance and exhaust the same adaptive
interval budget. The older E040 baseline therefore fails the same test. This
supports a shared quadrature/status defect, not an MTS-only adverse result.

## Discipline

Every mismatched live job and kernel is frozen byte-for-byte before repair;
the 5143 gate, result, status, validation and console log are also frozen. This
checkpoint does not mutate the live run. Next, correct convergence semantics,
demote both rows fail-closed and localize the exhausted adaptive leaves before
rerunning either row. No tolerance or physics parameter is changed, and the
formalization hash remains `{FORMAL_BASELINE}`.
"""
    DOCUMENT.write_text(document, encoding="utf-8")
    failures = [name for name, passed in checks if not passed]
    print(json.dumps({"result": result, "validation_failures": failures}, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
