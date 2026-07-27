from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SOURCE_5037 = POST / "source-intake" / "functional_rg" / "5037"
SOURCE_5039 = POST / "source-intake" / "functional_rg" / "5039"
RUN = SOURCE_5037 / "runs" / "paired_outer_precision_s4_v1"
OUTPUT = SOURCE_5039 / "provenance_ledger.json"
MARKER = "MTS_5039_PROVENANCE_LEDGER"
ENDPOINT_REPAIRS = (
    ("finite_endpoint_sector_e080_seed3_v1", "E080__S503403_N0000__A14__primary24"),
    ("finite_endpoint_sector_v1", "E040__S503403_N0000__A14__primary24"),
    ("finite_endpoint_sector_e020_seed3_v1", "E020__S503403_N0000__A14__primary24"),
)
CHART_REPAIRS = (
    "chart_origin_collision_v1",
    "chart_origin_collision_e020_seed3_v1",
    "chart_origin_collision_e080_seed3_v1",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def record(path: Path) -> dict[str, str]:
    if not path.exists():
        raise FileNotFoundError(path)
    return {"path": str(path.resolve()), "sha256": digest(path)}


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> None:
    status = load(RUN / "status.json")
    result = load(SOURCE_5037 / "paired_outer_precision_results.json")
    jobs = [load(path) for path in sorted((RUN / "jobs").glob("*.json"))]
    if not (
        status["state"] == "COMPLETE"
        and status["terminal_jobs"] == 189
        and result["run_state"] == "COMPLETE"
        and result["failed_jobs"] == 0
        and result["unconverged_jobs"] == 0
        and len(jobs) == 189
        and all(
            row["status"] in {"IMPORTED_CONVERGED", "COMPLETED_CONVERGED"}
            and row.get("integral_converged")
            for row in jobs
        )
    ):
        raise RuntimeError("final 5037 matrix is not complete and clean")

    endpoint_rows: dict[str, Any] = {}
    for repair_id, job_key in ENDPOINT_REPAIRS:
        directory = SOURCE_5037 / "repairs" / repair_id
        summary = load(directory / "repair_summary.json")
        if not (
            summary["accepted"]
            and summary["promoted"]
            and summary["kernel_relative_residual"] == 0.0
            and summary["job_key"] == job_key
        ):
            raise RuntimeError(f"invalid endpoint repair {repair_id}")
        repaired_job = directory / "repaired" / f"{job_key}.json"
        repaired_kernel = directory / "repaired" / f"kernel__{job_key}.json"
        live_job = RUN / "jobs" / f"{job_key}.json"
        live_kernel = RUN / "kernels" / f"{job_key}.json"
        if digest(repaired_job) != digest(live_job) or digest(repaired_kernel) != digest(
            live_kernel
        ):
            raise RuntimeError(f"endpoint live artifact mismatch {repair_id}")
        endpoint_rows[repair_id] = {
            "job_key": job_key,
            "summary": record(directory / "repair_summary.json"),
            "original_job": record(directory / "original" / f"{job_key}.json"),
            "repaired_job": record(repaired_job),
            "repaired_kernel": record(repaired_kernel),
            "live_job": record(live_job),
            "live_kernel": record(live_kernel),
            "primary_job": record(
                directory / "primary_scratch" / "jobs" / f"{job_key}.json"
            ),
            "audit_job": record(
                directory / "audit_scratch" / "jobs" / f"{job_key}.json"
            ),
        }

    chart_rows: dict[str, Any] = {}
    for repair_id in CHART_REPAIRS:
        directory = SOURCE_5037 / "repairs" / repair_id
        summary = load(directory / "repair_summary.json")
        if len(summary["repaired_jobs"]) != 2:
            raise RuntimeError(f"chart repair population mismatch {repair_id}")
        if repair_id != "chart_origin_collision_v1" and summary["still_open"]:
            raise RuntimeError(f"chart repair remains open {repair_id}")
        jobs_rows: dict[str, Any] = {}
        for job_key in summary["repaired_jobs"]:
            repaired_job = directory / "repaired" / f"{job_key}.json"
            live_job = RUN / "jobs" / f"{job_key}.json"
            if digest(repaired_job) != digest(live_job):
                raise RuntimeError(f"chart live artifact mismatch {job_key}")
            jobs_rows[job_key] = {
                "original_job": record(directory / "original" / f"{job_key}.json"),
                "repaired_job": record(repaired_job),
                "live_job": record(live_job),
            }
        chart_rows[repair_id] = {
            "summary": record(directory / "repair_summary.json"),
            "jobs": jobs_rows,
        }

    ledger = {
        "checkpoint_marker": MARKER,
        "ledger_script": record(Path(__file__).resolve()),
        "final_matrix": {
            "config": record(RUN / "config.json"),
            "status": record(RUN / "status.json"),
            "complete_marker": record(RUN / "COMPLETE"),
            "result": record(SOURCE_5037 / "paired_outer_precision_results.json"),
            "outer_precision_gate": record(SOURCE_5037 / "outer_precision_gate.csv"),
            "paired_convergence": record(SOURCE_5037 / "paired_vector_convergence.csv"),
            "reflection_control": record(SOURCE_5037 / "reflection_control.csv"),
            "job_count": 189,
            "imported_count": 117,
            "computed_count": 72,
        },
        "endpoint_repairs": endpoint_rows,
        "chart_repairs": chart_rows,
        "uncertainty_audit": {
            "script": record(
                POST / "scripts" / "Y5_R2FR_5039_completed_matrix_uncertainty_audit.py"
            ),
            "result": record(SOURCE_5039 / "completed_matrix_uncertainty_audit.json"),
            "contraction_csv": record(SOURCE_5039 / "contraction_uncertainty.csv"),
            "target_csv": record(SOURCE_5039 / "fixed_target_uncertainty.csv"),
            "reflection_csv": record(SOURCE_5039 / "reflection_uncertainty.csv"),
            "document": record(
                POST
                / "5039-Y5-R2FR-completed-four-scramble-uncertainty-and-target-audit.md"
            ),
            "resume": record(POST / "CURRENT_LOCAL_RESUME.md"),
        },
        "formalization_workbench_expected_digest": "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758",
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(OUTPUT, ledger)
    print(json.dumps({"marker": MARKER, "output": str(OUTPUT)}, indent=2))


if __name__ == "__main__":
    main()
