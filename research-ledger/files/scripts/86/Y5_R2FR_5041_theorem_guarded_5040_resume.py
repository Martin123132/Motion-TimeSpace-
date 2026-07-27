from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_REPAIR = POST / "scripts" / "Y5_R2FR_5041_cross_source_additive_zero_repair.py"
RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5040"
    / "runs"
    / "nested_sobol_power1_s4_v1"
)
MARKER = "MTS_5041_THEOREM_GUARDED_5040_RESUME"
CONFIG_DIGEST = "39540edd7cae4b42a78ab0c72939aa9f3a7b0e96f27f3063fca3f005db6fc81f"
CONTRACT_REFRESH = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5041"
    / "repairs"
    / "theorem_guarded_resume_contract_v2"
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


REPAIR = load_module("mts_5041_for_guarded_resume", SCRIPT_REPAIR)
M5040 = REPAIR.M5040
M5036 = REPAIR.M5036
N5030 = REPAIR.N5030


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def theorem_certificates(kernel: dict[str, Any]) -> list[dict[str, Any]]:
    REPAIR.configure_from_kernel(kernel)
    _, ownerships = N5030.physical_chambers()
    certificates = []
    for chamber in kernel["fixed_event_integral_gate"]["chambers"]:
        ownership = ownerships[int(chamber["chamber_index"])]
        for residue in chamber["residue_catalog"]:
            if residue.get("residue_method") != REPAIR.REVISION:
                continue
            certificate = REPAIR.theorem_certificate(residue, ownership)
            if not certificate["passed"]:
                raise RuntimeError(
                    f"stored exact-zero row failed theorem recertification in {kernel['job_key']}"
                )
            certificate["job_key"] = kernel["job_key"]
            certificates.append(certificate)
    return certificates


def contract_payload(kernel: dict[str, Any]) -> dict[str, Any]:
    certificates = theorem_certificates(kernel)
    return {
        "checkpoint_marker": MARKER,
        "repair_marker": REPAIR.MARKER,
        "repair_revision": REPAIR.REVISION,
        "guarded_resume_script": str(Path(__file__).resolve()),
        "guarded_resume_script_sha256": digest(Path(__file__).resolve()),
        "repair_script": str(SCRIPT_REPAIR),
        "repair_script_sha256": digest(SCRIPT_REPAIR),
        "certificate_count": len(certificates),
        "certificates": certificates,
        "rule": "cross-source exact zero is applied only when every theorem guard passes",
        "valid_for_full_MTS_claim": False,
    }


def refresh_contracts() -> dict[str, Any]:
    original = CONTRACT_REFRESH / "original"
    refreshed = CONTRACT_REFRESH / "refreshed"
    rows = []
    for job_path in sorted((RUN / "jobs").glob("*.json")):
        job = json.loads(job_path.read_text(encoding="utf-8"))
        if int(job.get("seed", -1)) != 503404 or int(job.get("sample_index", -1)) != 1:
            continue
        kernel_path = RUN / "kernels" / job_path.name
        kernel = json.loads(kernel_path.read_text(encoding="utf-8"))
        original.mkdir(parents=True, exist_ok=True)
        refreshed.mkdir(parents=True, exist_ok=True)
        if not (original / job_path.name).exists():
            shutil.copy2(job_path, original / job_path.name)
        original_kernel = original / f"kernel__{job_path.name}"
        if not original_kernel.exists():
            shutil.copy2(kernel_path, original_kernel)
        contract = contract_payload(kernel)
        job["cross_source_zero_contract"] = contract
        kernel["cross_source_zero_contract"] = contract
        M5036.atomic_json(job_path, job)
        M5036.atomic_json(kernel_path, kernel)
        M5036.atomic_json(refreshed / job_path.name, job)
        M5036.atomic_json(refreshed / f"kernel__{job_path.name}", kernel)
        rows.append(
            {
                "job_key": job["job_key"],
                "certificate_count": contract["certificate_count"],
            }
        )
    summary = {
        "checkpoint_marker": MARKER,
        "contract_revision": "theorem-guarded-resume-contract-v2",
        "refreshed_jobs": len(rows),
        "total_certificates": sum(row["certificate_count"] for row in rows),
        "rows": rows,
        "valid_for_full_MTS_claim": False,
    }
    M5036.atomic_json(CONTRACT_REFRESH / "refresh_summary.json", summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-wall-seconds", type=float, default=9000.0)
    parser.add_argument("--max-new-kernels", type=int, default=6)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--refresh-contracts", action="store_true")
    arguments = parser.parse_args()
    if arguments.max_wall_seconds <= 0.0 or arguments.max_wall_seconds > 10800.0:
        raise ValueError("wall limit must be in (0,10800] seconds")
    if arguments.max_new_kernels <= 0:
        raise ValueError("new-kernel limit must be positive")
    config = json.loads((RUN / "config.json").read_text(encoding="utf-8"))
    if config["config_digest"] != CONFIG_DIGEST:
        raise RuntimeError("locked 5040 config digest changed")
    if arguments.refresh_contracts:
        result = refresh_contracts()
        print(json.dumps(result, indent=2, allow_nan=False))
        return
    run_arguments = argparse.Namespace(
        run_id=config["run_id"],
        physical_cosines=",".join(str(value) for value in config["physical_cosines"]),
        epsilons=",".join(str(value) for value in config["epsilons"]),
        seeds=",".join(str(value) for value in config["seeds"]),
        power=int(config["power"]),
        topology_steps=int(config["topology"]["initial_steps"]),
        topology_maximum_steps=int(config["topology"]["maximum_steps"]),
        regulator=float(config["topology"]["regulator"]),
        boundary_tracking_steps=int(config["topology"]["boundary_tracking_steps"]),
        max_wall_seconds=float(arguments.max_wall_seconds),
        max_new_kernels=int(arguments.max_new_kernels),
        dry_run=bool(arguments.dry_run),
    )
    if arguments.dry_run:
        result = M5040.run(run_arguments)
        print(json.dumps(result, indent=2, allow_nan=False))
        return
    original_repair_catalog = M5036.MREPAIR.repaired_chamber_residue_catalog
    original_execute = M5036.execute_new_job

    def guarded_execute(
        run_directory: Path,
        current_config: dict[str, Any],
        job: dict[str, Any],
    ) -> dict[str, Any]:
        REPAIR.CURRENT_JOB = job["job_key"]
        REPAIR.REPAIR_AUDIT.clear()
        result = original_execute(run_directory, current_config, job)
        if not result.get("status", "").startswith("COMPLETED"):
            return result
        kernel_path = run_directory / "kernels" / f"{job['job_key']}.json"
        job_path = run_directory / "jobs" / f"{job['job_key']}.json"
        kernel = json.loads(kernel_path.read_text(encoding="utf-8"))
        contract = contract_payload(kernel)
        result["cross_source_zero_contract"] = contract
        kernel["cross_source_zero_contract"] = contract
        M5036.atomic_json(kernel_path, kernel)
        M5036.atomic_json(job_path, result)
        return result

    M5036.MREPAIR.repaired_chamber_residue_catalog = REPAIR.repaired_chamber_residue_catalog
    M5036.execute_new_job = guarded_execute
    try:
        result = M5040.run(run_arguments)
    finally:
        M5036.MREPAIR.repaired_chamber_residue_catalog = original_repair_catalog
        M5036.execute_new_job = original_execute
        N5030.chamber_residue_catalog = REPAIR.ORIGINAL_CATALOG
    console = {
        "checkpoint_marker": MARKER,
        "run_state": result["run_state"],
        "terminal_jobs": result["terminal_jobs"],
        "remaining_jobs": result["remaining_jobs"],
        "failed_jobs": result["failed_jobs"],
        "unconverged_jobs": result["unconverged_jobs"],
        "max_wall_seconds": arguments.max_wall_seconds,
        "max_new_kernels": arguments.max_new_kernels,
        "production_precision_complete": False,
        "valid_for_full_MTS_claim": False,
    }
    print(json.dumps(console, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
