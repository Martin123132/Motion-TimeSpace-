from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5079 = POST / "scripts" / "Y5_R2FR_5079_bounded_central_anchor_pilot_runner.py"
RUN = POST / "source-intake" / "functional_rg" / "5079" / "runs" / "bounded_central_anchor_pilot_v12"
THEOREM_GATE = POST / "source-intake" / "functional_rg" / "5101" / "S507622_projective_cluster_argument_independence.json"
SOURCE = POST / "source-intake" / "functional_rg" / "5103"
RESULT_JSON = SOURCE / "bounded_central_anchor_v12_matrix_closure.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5103_VALIDATION.csv"
MARKER = "MTS_5103_BOUNDED_CENTRAL_ANCHOR_V12_MATRIX_CLOSURE"
REVISION = "full-locked-matrix-provenance-audit-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
CONFIG_DIGEST = "bb930b0d2c11cd1bf4644b05db976f548e256d10add888144b98cfab95aa7a69"
SCHEDULE_DIGEST = "da19db9b4d7f5c1ca41babe2f1fcfafc2f9ed92a043cc4298f1fb5c4bee3f956"
TARGET_JOB = "E040__S507622_N0000__A14__coarse12"
UPSTREAM_VALIDATIONS = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5079_VALIDATION.csv",
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5101_VALIDATION.csv",
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5102_VALIDATION.csv",
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


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
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def validations_pass(paths: tuple[Path, ...]) -> tuple[bool, dict[str, int]]:
    failed_counts: dict[str, int] = {}
    for path in paths:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        failed_counts[str(path)] = sum(row["passed"].lower() != "true" for row in rows)
    return all(count == 0 for count in failed_counts.values()), failed_counts


def main() -> None:
    required = [
        SCRIPT_5079,
        THEOREM_GATE,
        RUN / "config.json",
        RUN / "activation.json",
        RUN / "status.json",
        RUN / "COMPLETED.json",
        FORMAL,
        *UPSTREAM_VALIDATIONS,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(missing)
    module = load_module("mts_5079_for_5103", SCRIPT_5079)
    manifest = module.read_json(module.MANIFEST)
    config = read_json(RUN / "config.json")
    activation = read_json(RUN / "activation.json")
    status = read_json(RUN / "status.json")
    completion = read_json(RUN / "COMPLETED.json")
    schedule = module.M5077.pilot_jobs(config, manifest)
    scheduled_keys = {row["job_key"] for row in schedule}
    job_paths = sorted((RUN / "jobs").glob("*.json"))
    jobs = [read_json(path) for path in job_paths]
    job_lookup = {row["job_key"]: row for row in jobs}
    linked_kernel_paths = {Path(row["kernel_file"]) for row in jobs}
    linked_topology_paths = {Path(row["topology_file"]) for row in jobs}
    link_paths = linked_kernel_paths | linked_topology_paths
    links_exist = all(path.exists() for path in link_paths)
    linked_records = [read_json(path) for path in link_paths] if links_exist else []
    target = job_lookup.get(TARGET_JOB, {})
    target_kernel = (
        read_json(Path(target["kernel_file"])) if target.get("kernel_file") else {}
    )
    target_integral = target_kernel.get("fixed_event_integral_gate", {})
    certificate_rows = target.get("profile_audit", {}).get(
        "projective_cluster_zero_certificate_rows", []
    )
    target_certificate = certificate_rows[0] if len(certificate_rows) == 1 else {}
    theorem_gate = read_json(THEOREM_GATE)
    theorem_A14_rows = theorem_gate.get("unstable_A14_rows", [])
    upstream_passed, upstream_failures = validations_pass(UPSTREAM_VALIDATIONS)
    formal_digest = tree_digest(FORMAL)
    pycache_paths = sorted(
        str(path) for path in POST.rglob("__pycache__") if path.is_dir()
    )
    guards = {
        "config_digest_exact": config.get("config_digest") == CONFIG_DIGEST,
        "schedule_digest_exact": module.M5077.M5036.canonical_digest(schedule)
        == SCHEDULE_DIGEST,
        "activation_authorized": bool(activation.get("pilot_execution_authorized")),
        "schedule_has_360_unique_jobs": len(schedule) == 360
        and len(scheduled_keys) == 360,
        "job_set_matches_schedule": len(jobs) == 360
        and set(job_lookup) == scheduled_keys,
        "all_jobs_converged": all(
            row.get("status") == "COMPLETED_CONVERGED" for row in jobs
        ),
        "all_jobs_use_exact_config": all(
            row.get("config_digest") == CONFIG_DIGEST for row in jobs
        ),
        "all_linked_records_exist": links_exist,
        "all_linked_records_use_exact_config": links_exist
        and all(row.get("config_digest") == CONFIG_DIGEST for row in linked_records),
        "status_is_complete": status.get("state") == "COMPLETE"
        and status.get("completed_converged") == 360
        and status.get("completed_unconverged") == 0
        and status.get("failed") == 0
        and status.get("missing") == 0
        and bool(status.get("pilot_numerical_matrix_complete")),
        "completion_marker_is_complete": completion.get("completed_converged") == 360
        and completion.get("completed_unconverged") == 0
        and completion.get("failed") == 0
        and completion.get("missing") == 0,
        "A14_fresh_job_converged": target.get("status") == "COMPLETED_CONVERGED"
        and bool(target.get("integral_converged")),
        "A14_exact_certificate_used_once": target.get("profile_audit", {}).get(
            "projective_cluster_zero_certificate_count"
        )
        == 1
        and len(certificate_rows) == 1,
        "A14_certificate_is_5101": target_certificate.get("certificate")
        == str(THEOREM_GATE)
        and target_certificate.get("certificate_sha256") == digest(THEOREM_GATE),
        "A14_certificate_guards_pass": len(theorem_A14_rows) == 1
        and bool(theorem_A14_rows[0].get("certificate", {}).get("passed"))
        and theorem_A14_rows[0]
        .get("certificate", {})
        .get("checkpoint_marker")
        == "MTS_5101_S507622_PROJECTIVE_CLUSTER_ARGUMENT_INDEPENDENCE"
        and all(
            bool(value)
            for value in theorem_A14_rows[0]
            .get("certificate", {})
            .get("guards", {})
            .values()
        ),
        "A14_integral_and_residues_converged": bool(
            target_integral.get("all_residues_stable")
        )
        and all(
            bool(row.get("adaptive_quadrature_converged"))
            for row in target_integral.get("order_rows", [])
        )
        and float(target_integral.get("highest_two_order_relative_residual", 1.0))
        < float(target_integral.get("relative_adaptive_tolerance", 0.0)),
        "theorem_gate_is_exact_and_accepted": bool(
            theorem_gate.get("argument_independent_projective_cluster_zero_passed")
        )
        and theorem_gate.get("authorized_job_scopes") == [TARGET_JOB],
        "upstream_validations_pass": upstream_passed,
        "formalization_unchanged": formal_digest == FORMAL_BASELINE,
        "no_python_cache": not pycache_paths,
    }
    matrix_closed = all(guards.values())
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "run": str(RUN),
        "config_digest": config.get("config_digest"),
        "schedule_digest": module.M5077.M5036.canonical_digest(schedule),
        "job_count": len(jobs),
        "kernel_count": len(linked_kernel_paths),
        "topology_count": len(linked_topology_paths),
        "A14_job_runtime_seconds": target.get("job_runtime_seconds"),
        "A14_adaptive_relative_residual": target_integral.get(
            "highest_two_order_relative_residual"
        ),
        "A14_projective_certificate_count": len(certificate_rows),
        "A14_theorem_certificate_count": len(theorem_A14_rows),
        "upstream_validation_failures": upstream_failures,
        "guards": guards,
        "locked_numerical_matrix_closed": matrix_closed,
        "statistical_analysis_complete": False,
        "formalization_workbench_tree_sha256": formal_digest,
        "python_cache_paths": pycache_paths,
        "claim_scope": "completion of the locked numerical kernel matrix only",
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("sources_exist", not missing, "all 5103 sources exist"),
        *[(name, passed, str(passed)) for name, passed in guards.items()],
        ("matrix_closed", matrix_closed, f"jobs={len(jobs)}"),
        ("claim_discipline", not result["valid_for_full_MTS_claim"], result["claim_scope"]),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("check_id", "passed", "detail", "checkpoint_marker"),
        )
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5103_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5103 validation failed: {failed}")


if __name__ == "__main__":
    main()
