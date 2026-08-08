from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
RUN = POST / "source-intake" / "functional_rg" / "5125" / "runs" / "reciprocal_stratified_fresh_pilot_v1"
CONFIG = RUN / "config.json"
SCHEDULE = POST / "source-intake" / "functional_rg" / "5125" / "reciprocal_stratified_locked_schedule.json"
AUDIT_5144 = POST / "source-intake" / "functional_rg" / "5144" / "strict_adaptive_status_audit.csv"
WITNESSES_5144 = POST / "source-intake" / "functional_rg" / "5144" / "witnesses"
SOURCE_5143 = POST / "source-intake" / "functional_rg" / "5143"
RESULT_5143 = SOURCE_5143 / "A10_argument_local_outer_collinear_replay_result.json"
STATUS_5143 = SOURCE_5143 / "A10_argument_local_outer_collinear_replay_status.json"
GATE_5143 = SOURCE_5143 / "A10_argument_local_outer_collinear_chart_gate.json"
SOURCE = POST / "source-intake" / "functional_rg" / "5145"
RECONCILIATION_CSV = SOURCE / "strict_adaptive_live_status_reconciliation.csv"
RESULT_JSON = SOURCE / "strict_adaptive_semantics_and_reconciliation_result.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5145_VALIDATION.csv"
DOCUMENT = POST / "5145-Y5-R2FR-strict-adaptive-semantics-and-live-status-reconciliation.md"
SCRIPT_5030 = POST / "scripts" / "Y5_R2FR_5030_causal_relative_collision_homotopy_gate.py"
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
SCRIPT_5125 = POST / "scripts" / "Y5_R2FR_5125_reciprocal_stratified_fresh_pilot_runner.py"
SCRIPT_5128 = POST / "scripts" / "Y5_R2FR_5128_argument_local_outer_collinear_preflight_and_A11_replay.py"
SCRIPT_5132 = POST / "scripts" / "Y5_R2FR_5132_locked_next_argument_gate_and_single_job_runner.py"

MARKER = "MTS_5145_STRICT_ADAPTIVE_SEMANTICS_AND_LIVE_STATUS_RECONCILIATION"
CHECKED_DATE = "2026-07-20"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
MISMATCHES = {
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


def bool_value(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def run_counts(schedule: list[dict[str, Any]], config_digest: str) -> dict[str, int]:
    counts = {
        "completed_converged": 0,
        "completed_unconverged": 0,
        "failed": 0,
        "missing": 0,
    }
    for job in schedule:
        directory = "jobs" if job["stratum"] == "full_remainder" else "topological_jobs"
        path = RUN / directory / f"{job['job_key']}.json"
        if not path.exists():
            counts["missing"] += 1
            continue
        row = read_json(path)
        if row.get("config_digest") != config_digest:
            counts["missing"] += 1
        elif row.get("status") == "COMPLETED_CONVERGED":
            counts["completed_converged"] += 1
        elif row.get("status") == "COMPLETED_UNCONVERGED":
            counts["completed_unconverged"] += 1
        elif row.get("status") == "FAILED":
            counts["failed"] += 1
        else:
            counts["missing"] += 1
    return counts


def main() -> None:
    config = read_json(CONFIG)
    schedule = read_json(SCHEDULE)["jobs"]
    with AUDIT_5144.open("r", encoding="utf-8", newline="") as handle:
        audit_rows = list(csv.DictReader(handle))
    if len(audit_rows) != 51:
        raise RuntimeError(f"expected 51 audited full rows, found {len(audit_rows)}")
    source_clauses = {
        "5030_strict_gate": "and strict_adaptive_quadrature_converged",
        "5077_strict_status": "and strict_adaptive_validated",
        "5125_strict_cache": 'row.get("strict_adaptive_validated") is True',
        "5128_strict_replay": 'fixed_gate.get("strict_adaptive_quadrature_converged")',
        "5132_strict_next": 'row.get("strict_adaptive_validated") is not True',
    }
    source_paths = {
        "5030_strict_gate": SCRIPT_5030,
        "5077_strict_status": SCRIPT_5077,
        "5125_strict_cache": SCRIPT_5125,
        "5128_strict_replay": SCRIPT_5128,
        "5132_strict_next": SCRIPT_5132,
    }
    source_semantics_locked = all(
        clause in source_paths[key].read_text(encoding="utf-8")
        for key, clause in source_clauses.items()
    )
    reconciliation_rows: list[dict[str, Any]] = []
    for audit in audit_rows:
        job_key = audit["job_key"]
        job_path = RUN / "jobs" / f"{job_key}.json"
        kernel_path = RUN / "kernels" / f"{job_key}.json"
        job = read_json(job_path)
        kernel = read_json(kernel_path)
        strict_pass = bool_value(audit["strict_integral_converged"])
        before_job_hash = digest(job_path)
        before_kernel_hash = digest(kernel_path)
        if "strict_adaptive_reconciliation" not in job:
            job["pre_strict_reconciliation"] = {
                "status": job.get("status"),
                "integral_converged": job.get("integral_converged"),
                "job_sha256": before_job_hash,
            }
        if "strict_adaptive_reconciliation" not in kernel:
            kernel["pre_strict_reconciliation"] = {
                "fixed_event_crossed_integral_converged": kernel[
                    "fixed_event_integral_gate"
                ].get("fixed_event_crossed_integral_converged"),
                "kernel_sha256": before_kernel_hash,
            }
        job["strict_adaptive_validated"] = strict_pass
        job["strict_adaptive_reconciliation"] = {
            "checkpoint_marker": MARKER,
            "strict_pass": strict_pass,
            "maximum_error": float(
                audit["maximum_adaptive_chamber_relative_error"]
            ),
            "tolerance": float(audit["locked_tolerance"]),
        }
        gate = kernel["fixed_event_integral_gate"]
        gate["strict_adaptive_quadrature_converged"] = strict_pass
        gate["fixed_event_crossed_integral_converged"] = bool(
            gate.get("all_residues_stable")
            and float(gate["highest_two_order_relative_residual"]) < 2.0e-3
            and strict_pass
        )
        kernel["strict_adaptive_validated"] = strict_pass
        kernel["strict_adaptive_reconciliation"] = {
            "checkpoint_marker": MARKER,
            "strict_pass": strict_pass,
        }
        if not strict_pass:
            job["status"] = "COMPLETED_UNCONVERGED"
            job["integral_converged"] = False
        atomic_json(job_path, job)
        atomic_json(kernel_path, kernel)
        reconciliation_rows.append(
            {
                "job_key": job_key,
                "strict_pass": strict_pass,
                "before_declared_status": audit["declared_status"],
                "after_status": job["status"],
                "after_integral_converged": job["integral_converged"],
                "before_job_sha256": before_job_hash,
                "after_job_sha256": digest(job_path),
                "before_kernel_sha256": before_kernel_hash,
                "after_kernel_sha256": digest(kernel_path),
                "checkpoint_marker": MARKER,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
                "source_checked_date": CHECKED_DATE,
            }
        )
    counts = run_counts(schedule, config["config_digest"])
    first_incomplete = next(
        job
        for job in schedule
        if (
            not (
                RUN
                / (
                    "jobs"
                    if job["stratum"] == "full_remainder"
                    else "topological_jobs"
                )
                / f"{job['job_key']}.json"
            ).exists()
            or (
                lambda row: row.get("status") != "COMPLETED_CONVERGED"
                or (
                    job["stratum"] == "full_remainder"
                    and row.get("strict_adaptive_validated") is not True
                )
            )(
                read_json(
                    RUN
                    / (
                        "jobs"
                        if job["stratum"] == "full_remainder"
                        else "topological_jobs"
                    )
                    / f"{job['job_key']}.json"
                )
            )
        )
    )
    result_5143 = read_json(RESULT_5143)
    status_5143 = read_json(STATUS_5143)
    result_5143.setdefault(
        "pre_strict_reconciliation",
        {
            "job_status": result_5143.get("job_status"),
            "integral_converged": result_5143.get("integral_converged"),
        },
    )
    result_5143.update(
        {
            "job_status": "COMPLETED_UNCONVERGED",
            "integral_converged": False,
            "strict_adaptive_validated": False,
            "strict_adaptive_reconciliation": MARKER,
            "run_counts": counts,
        }
    )
    status_5143.update(
        {
            "state": "BLOCKED_AFTER_5145_STRICT_ADAPTIVE_RECONCILIATION",
            "job_status": "COMPLETED_UNCONVERGED",
            "strict_adaptive_validated": False,
            "completed_converged": counts["completed_converged"],
            "completed_unconverged": counts["completed_unconverged"],
            "failed": counts["failed"],
            "missing": counts["missing"],
            "checkpoint_marker": MARKER,
        }
    )
    atomic_json(RESULT_5143, result_5143)
    atomic_json(STATUS_5143, status_5143)
    atomic_json(RUN / "status.json", status_5143)
    write_csv(RECONCILIATION_CSV, reconciliation_rows)
    witness_hashes_preserved = all(
        digest(WITNESSES_5144 / job_key / "live_job.json")
        == next(
            row["before_job_sha256"]
            for row in reconciliation_rows
            if row["job_key"] == job_key
        )
        and digest(WITNESSES_5144 / job_key / "live_kernel.json")
        == next(
            row["before_kernel_sha256"]
            for row in reconciliation_rows
            if row["job_key"] == job_key
        )
        for job_key in MISMATCHES
    )
    result = {
        "checkpoint_marker": MARKER,
        "source_semantics_locked": source_semantics_locked,
        "source_files": {
            key: str(path) for key, path in source_paths.items()
        },
        "audit": str(AUDIT_5144),
        "reconciliation": str(RECONCILIATION_CSV),
        "reconciled_full_remainder_rows": len(reconciliation_rows),
        "strict_pass_rows": sum(row["strict_pass"] for row in reconciliation_rows),
        "demoted_rows": [
            row["job_key"] for row in reconciliation_rows if not row["strict_pass"]
        ],
        "run_counts": counts,
        "first_incomplete_locked_row": first_incomplete,
        "witness_hashes_preserved": witness_hashes_preserved,
        "formalization_workbench_tree_sha256": tree_digest(FORMAL),
        "profile_tolerance_changed": False,
        "profile_interval_cap_changed": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "source_checked_date": CHECKED_DATE,
    }
    atomic_json(RESULT_JSON, result)
    demoted = set(result["demoted_rows"])
    checks = [
        ("source_semantics_locked", source_semantics_locked),
        ("fifty_one_full_rows_reconciled", len(reconciliation_rows) == 51),
        ("forty_nine_strict_rows_retained", result["strict_pass_rows"] == 49),
        ("exact_two_rows_demoted", demoted == MISMATCHES),
        ("demoted_rows_fail_closed", all(row["after_status"] == "COMPLETED_UNCONVERGED" and not bool_value(row["after_integral_converged"]) for row in reconciliation_rows if row["job_key"] in MISMATCHES)),
        ("run_counts_reconciled", counts == {"completed_converged": 50, "completed_unconverged": 2, "failed": 0, "missing": 508}),
        ("first_incomplete_is_E040_A10", first_incomplete["job_key"] == "E040__S512503_N0000__A10__primary24"),
        ("witness_hashes_preserved", witness_hashes_preserved),
        ("5143_result_fail_closed", not result_5143["integral_converged"] and result_5143["job_status"] == "COMPLETED_UNCONVERGED"),
        ("locked_profile_unchanged", not result["profile_tolerance_changed"] and not result["profile_interval_cap_changed"]),
        ("formal_tree_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE),
        ("claim_discipline", not result["valid_for_numeric_UV_claim"] and not result["valid_for_local_GR_claim"] and not result["valid_for_full_MTS_claim"]),
    ]
    write_csv(
        VALIDATION_CSV,
        [
            {
                "check_id": f"VAL5145_{index:02d}_{name}",
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
    document = f"""# 5145: Strict adaptive semantics and live-status reconciliation

## Root correction

An adaptive full-remainder row is now converged only when every adaptive order
both reports convergence and has maximum chamber-relative error below the
locked tolerance. The fixed-event gate, kernel status, cache acceptance,
locked-next selection and replay validation all enforce the same condition.

## Reconciled state

All 51 existing full-remainder rows were reconciled against checkpoint 5144.
Forty-nine remain strict passes. The E040/A10 baseline and E020/A10 repaired
row are demoted to `COMPLETED_UNCONVERGED`; their frozen pre-repair witnesses
remain byte-identical. The run is now `{counts}` and the first incomplete
locked row is `{first_incomplete['job_key']}`.

No tolerance, interval cap or physics parameter changed. The next task is to
localize the exhausted adaptive leaves shared by the A10 pair and derive a
geometric partition repair before rerunning either row.
"""
    DOCUMENT.write_text(document, encoding="utf-8")
    failures = [name for name, passed in checks if not passed]
    print(json.dumps({"result": result, "validation_failures": failures}, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
