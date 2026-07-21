from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
import time
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5046 = POST / "scripts" / "Y5_R2FR_5046_restricted_scope_primary24_benchmark.py"
SOURCE = POST / "source-intake" / "functional_rg" / "5047"
RUN = SOURCE / "runs" / "restricted_fourth_scramble_primary24_v1"
DRY_RUN_JSON = SOURCE / "dry_run.json"
PILOT_JSON = SOURCE / "restricted_fourth_scramble_pilot.json"
MATRIX_JSON = SOURCE / "restricted_fourth_scramble_matrix.json"
COMPARISON_CSV = SOURCE / "restricted_vs_quarantined_comparison.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5047_VALIDATION.csv"
)
MARKER = "MTS_5047_RESTRICTED_FOURTH_SCRAMBLE_SCRATCH_MATRIX"
REVISION = "restricted-fourth-scramble-primary24-scratch-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
EVENT_ID = "S503404_N0001"
EPSILON_IDS = ("E020", "E040", "E080")
BASE_IDS = tuple(f"A{index:02d}" for index in range(15))
PILOT_BASE_IDS = ("A00", "A07", "A14")
PROFILE = {
    "relative_orders": (24,),
    "global_nodes": 24,
    "global_residue_nodes": 24,
    "relative_residue_nodes": 20,
    "model_distance": 0.65,
    "relative_quadrature_mode": "collision_scaled_adaptive",
    "relative_adaptive_tolerance": 5.0e-5,
    "relative_adaptive_maximum_intervals": 4096,
}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5046 = load_module("mts_5046_for_fourth_scratch", SCRIPT_5046)
M5045 = M5046.M5045
M5043 = M5046.M5043
N5030 = M5046.N5030
M5034 = M5043.M5034
ORIGINAL_CATALOG = N5030.chamber_residue_catalog
ORIGINAL_THEOREM = M5043.M5041.theorem_certificate
RUN_5040 = M5043.RUN_5040


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    if not path.exists():
        return "MISSING"
    for file_path in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(file_path.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(file_path).encode("ascii"))
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def serialized(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def complex_value(value: dict[str, float]) -> complex:
    return complex(float(value["real"]), float(value["imaginary"]))


def profile_digest() -> str:
    return canonical_digest(
        {
            "marker": MARKER,
            "revision": REVISION,
            "profile": PROFILE,
            "scope_source_sha256": digest(M5046.SCRIPT_5045_SCOPE),
            "broad_source_sha256": digest(M5043.SCRIPT_5041),
        }
    )


def configure_modules() -> None:
    M5045.EPSILON_IDS = EPSILON_IDS
    M5045.MARKER = MARKER
    M5045.REVISION = REVISION
    M5043.M5041.theorem_certificate = M5046.restricted_certificate
    N5030.chamber_residue_catalog = M5043.theorem_first_chamber_residue_catalog


def restore_modules() -> None:
    M5043.M5041.theorem_certificate = ORIGINAL_THEOREM
    N5030.chamber_residue_catalog = ORIGINAL_CATALOG


def config() -> dict[str, Any]:
    return M5043.load_config()


def event_lookup(document: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(row["event_id"]): row for row in document["events"]}


def argument_lookup(document: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    return {
        (str(row["epsilon_id"]), str(row["base_argument_id"])): row
        for row in document["arguments"]
        if str(row["epsilon_id"]) in EPSILON_IDS
    }


def topology_path(
    document: dict[str, Any], epsilon_id: str, base_id: str
) -> Path:
    return M5045.topology_path(document, EVENT_ID, epsilon_id, base_id)


def output_path(epsilon_id: str, base_id: str) -> Path:
    return RUN / "jobs" / f"{epsilon_id}__{EVENT_ID}__{base_id}.json"


def kernel_path(epsilon_id: str, base_id: str) -> Path:
    return RUN / "kernels" / f"{epsilon_id}__{EVENT_ID}__{base_id}.json"


def quarantined_source(epsilon_id: str, base_id: str) -> tuple[Path, dict[str, Any]]:
    path = (
        RUN_5040
        / "jobs"
        / f"{epsilon_id}__{EVENT_ID}__{base_id}__primary24.json"
    )
    if not path.exists():
        raise FileNotFoundError(path)
    return path, json.loads(path.read_text(encoding="utf-8"))


def evaluate(
    document: dict[str, Any], epsilon_id: str, base_id: str
) -> dict[str, Any]:
    output = output_path(epsilon_id, base_id)
    expected_profile_digest = profile_digest()
    if output.exists():
        existing = json.loads(output.read_text(encoding="utf-8"))
        if (
            existing.get("profile_digest") == expected_profile_digest
            and existing.get("status") == "COMPLETED_CONVERGED"
        ):
            return existing
    event = event_lookup(document)[EVENT_ID]
    argument = argument_lookup(document)[(epsilon_id, base_id)]
    topology_source = topology_path(document, epsilon_id, base_id)
    topology = json.loads(topology_source.read_text(encoding="utf-8"))
    target = complex_value(argument["target_cosine"])
    M5034.configure(event, target)
    M5043.CURRENT_JOB = f"restricted_fourth__{epsilon_id}__{EVENT_ID}__{base_id}"
    M5043.THEOREM_AUDIT.clear()
    M5043.CHART_AUDIT.clear()
    M5043.NUMERIC_AUDIT.clear()
    started = time.monotonic()
    try:
        gate = N5030.fixed_event_integral_gate(
            topology,
            tuple(int(value) for value in PROFILE["relative_orders"]),
            int(PROFILE["global_nodes"]),
            int(PROFILE["global_residue_nodes"]),
            int(PROFILE["relative_residue_nodes"]),
            float(PROFILE["model_distance"]),
            int(document["topology"]["boundary_tracking_steps"]),
            str(PROFILE["relative_quadrature_mode"]),
            float(PROFILE["relative_adaptive_tolerance"]),
            int(PROFILE["relative_adaptive_maximum_intervals"]),
        )
        raw_kernel = M5034.highest_value(gate)
        direct = M5034.KERNEL_MULTIPLIER * raw_kernel
        quarantined_path, quarantined = quarantined_source(epsilon_id, base_id)
        quarantined_direct = complex_value(
            quarantined["normalized_direct_D_hhh_over_G3"]
        )
        converged = bool(gate["fixed_event_crossed_integral_converged"])
        runtime = time.monotonic() - started
        result = {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "profile": PROFILE,
            "profile_digest": expected_profile_digest,
            "epsilon_id": epsilon_id,
            "event_id": EVENT_ID,
            "seed": int(event["seed"]),
            "sample_index": int(event["sample_index"]),
            "base_argument_id": base_id,
            "argument_id": argument["argument_id"],
            "target_cosine": argument["target_cosine"],
            "topology_source": str(topology_source),
            "topology_source_sha256": digest(topology_source),
            "status": "COMPLETED_CONVERGED" if converged else "COMPLETED_UNCONVERGED",
            "raw_fixed_event_kernel": serialized(raw_kernel),
            "normalized_direct_D_hhh_over_G3": serialized(direct),
            "quarantined_broad_zero_source": str(quarantined_path),
            "quarantined_broad_zero_source_sha256": digest(quarantined_path),
            "quarantined_broad_zero_direct_D_hhh_over_G3": serialized(
                quarantined_direct
            ),
            "restricted_minus_quarantined": serialized(direct - quarantined_direct),
            "restricted_quarantined_relative_difference": float(
                abs(direct - quarantined_direct) / max(1.0, abs(direct))
            ),
            "kernel_runtime_seconds": runtime,
            "all_residues_stable": bool(gate["all_residues_stable"]),
            "adaptive_quadrature_converged": all(
                bool(row["adaptive_quadrature_converged"])
                for row in gate["order_rows"]
            ),
            "highest_two_order_relative_residual": float(
                gate["highest_two_order_relative_residual"]
            ),
            "theorem_zero_residue_count": len(M5043.THEOREM_AUDIT),
            "numeric_residue_count": len(M5043.NUMERIC_AUDIT),
            "chart_origin_exclusion_count": len(M5043.CHART_AUDIT),
            "unstable_numeric_residue_count": sum(
                not bool(row["selected_stable"]) for row in M5043.NUMERIC_AUDIT
            ),
            "theorem_zero_rows": list(M5043.THEOREM_AUDIT),
            "numeric_residue_rows": list(M5043.NUMERIC_AUDIT),
            "chart_origin_exclusions": list(M5043.CHART_AUDIT),
            "full_gate_sha256": canonical_digest(gate),
            "valid_for_full_MTS_claim": False,
        }
        kernel = {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "profile_digest": expected_profile_digest,
            "epsilon_id": epsilon_id,
            "event_id": EVENT_ID,
            "base_argument_id": base_id,
            "event": event,
            "argument": argument,
            "topology_source": str(topology_source),
            "fixed_event_integral_gate": gate,
            "normalized_direct_D_hhh_over_G3": serialized(direct),
            "valid_for_full_MTS_claim": False,
        }
        atomic_json(kernel_path(epsilon_id, base_id), kernel)
    except Exception as error:
        result = {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "profile": PROFILE,
            "profile_digest": expected_profile_digest,
            "epsilon_id": epsilon_id,
            "event_id": EVENT_ID,
            "base_argument_id": base_id,
            "topology_source": str(topology_source),
            "status": "FAILED",
            "error": f"{type(error).__name__}: {error}",
            "kernel_runtime_seconds": time.monotonic() - started,
            "valid_for_full_MTS_claim": False,
        }
    atomic_json(output, result)
    return result


def dry_run(document: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for epsilon_id in EPSILON_IDS:
        for base_id in BASE_IDS:
            topology = topology_path(document, epsilon_id, base_id)
            quarantined_path, quarantined = quarantined_source(epsilon_id, base_id)
            rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "base_argument_id": base_id,
                    "topology": str(topology),
                    "quarantined_source": str(quarantined_path),
                    "quarantined_status": quarantined["status"],
                }
            )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "event_id": EVENT_ID,
        "expected_jobs": len(rows),
        "all_topologies_exist": all(Path(row["topology"]).exists() for row in rows),
        "all_quarantined_sources_exist": all(
            Path(row["quarantined_source"]).exists() for row in rows
        ),
        "rows": rows,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(DRY_RUN_JSON, result)
    return result


def run_set(
    document: dict[str, Any], jobs: list[tuple[str, str]], max_wall_seconds: float
) -> list[dict[str, Any]]:
    started = time.monotonic()
    rows = []
    for epsilon_id, base_id in jobs:
        if time.monotonic() - started >= max_wall_seconds:
            break
        print(f"starting {epsilon_id} {EVENT_ID} {base_id}", flush=True)
        row = evaluate(document, epsilon_id, base_id)
        rows.append(row)
        print(
            f"finished {epsilon_id} {base_id} status={row['status']} "
            f"seconds={row['kernel_runtime_seconds']:.3f}",
            flush=True,
        )
    return rows


def summarize(rows: list[dict[str, Any]], expected_jobs: int, scope: str) -> dict[str, Any]:
    completed = len(rows) == expected_jobs
    converged = completed and all(row["status"] == "COMPLETED_CONVERGED" for row in rows)
    stable = converged and all(
        bool(row["all_residues_stable"])
        and int(row["unstable_numeric_residue_count"]) == 0
        for row in rows
    )
    no_unproved_zeros = converged and all(
        int(row["theorem_zero_residue_count"]) == 0 for row in rows
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "scope": scope,
        "event_id": EVENT_ID,
        "expected_jobs": expected_jobs,
        "completed_jobs": len(rows),
        "converged_jobs": sum(row.get("status") == "COMPLETED_CONVERGED" for row in rows),
        "all_jobs_converged": converged,
        "all_residues_stable": stable,
        "no_exact_zero_outside_proved_scope": no_unproved_zeros,
        "total_theorem_zero_residues": sum(
            int(row.get("theorem_zero_residue_count", 0)) for row in rows
        ),
        "total_numeric_residues": sum(
            int(row.get("numeric_residue_count", 0)) for row in rows
        ),
        "total_chart_origin_exclusions": sum(
            int(row.get("chart_origin_exclusion_count", 0)) for row in rows
        ),
        "maximum_restricted_quarantined_relative_difference": max(
            (
                float(row.get("restricted_quarantined_relative_difference", math.inf))
                for row in rows
            ),
            default=math.inf,
        ),
        "total_runtime_seconds": sum(float(row["kernel_runtime_seconds"]) for row in rows),
        "jobs": rows,
        "formalization_workbench_tree_sha256": tree_digest(
            POST.parent / "formalization-workbench"
        ),
        "scratch_matrix_valid": bool(converged and stable and no_unproved_zeros),
        "live_5040_replacement_authorized": bool(
            scope == "matrix" and converged and stable and no_unproved_zeros
        ),
        "valid_for_full_MTS_claim": False,
    }
    return result


def write_validation(result: dict[str, Any]) -> None:
    checks = [
        ("all_jobs_completed", result["completed_jobs"] == result["expected_jobs"], f"{result['completed_jobs']}/{result['expected_jobs']}"),
        ("all_jobs_converged", result["all_jobs_converged"], str(result["converged_jobs"])),
        ("all_residues_stable", result["all_residues_stable"], str(result["total_numeric_residues"])),
        ("no_unproved_exact_zeros", result["no_exact_zero_outside_proved_scope"], str(result["total_theorem_zero_residues"])),
        ("claim_remains_false", not result["valid_for_full_MTS_claim"], "required false"),
        ("formalization_workbench_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE, result["formalization_workbench_tree_sha256"]),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check", "passed", "evidence"))
        writer.writeheader()
        writer.writerows(
            {
                "check": name,
                "passed": str(bool(passed)).lower(),
                "evidence": evidence,
            }
            for name, passed, evidence in checks
        )


def write_comparison(rows: list[dict[str, Any]]) -> None:
    fieldnames = (
        "epsilon_id",
        "base_argument_id",
        "status",
        "restricted_real",
        "restricted_imaginary",
        "quarantined_real",
        "quarantined_imaginary",
        "relative_difference",
        "theorem_zero_residue_count",
        "numeric_residue_count",
        "chart_origin_exclusion_count",
        "kernel_runtime_seconds",
    )
    output_rows = []
    for row in rows:
        restricted = row.get("normalized_direct_D_hhh_over_G3", {})
        quarantined = row.get("quarantined_broad_zero_direct_D_hhh_over_G3", {})
        output_rows.append(
            {
                "epsilon_id": row["epsilon_id"],
                "base_argument_id": row["base_argument_id"],
                "status": row["status"],
                "restricted_real": restricted.get("real"),
                "restricted_imaginary": restricted.get("imaginary"),
                "quarantined_real": quarantined.get("real"),
                "quarantined_imaginary": quarantined.get("imaginary"),
                "relative_difference": row.get("restricted_quarantined_relative_difference"),
                "theorem_zero_residue_count": row.get("theorem_zero_residue_count"),
                "numeric_residue_count": row.get("numeric_residue_count"),
                "chart_origin_exclusion_count": row.get("chart_origin_exclusion_count"),
                "kernel_runtime_seconds": row["kernel_runtime_seconds"],
            }
        )
    COMPARISON_CSV.parent.mkdir(parents=True, exist_ok=True)
    with COMPARISON_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("dry-run", "pilot", "matrix", "analyze"), default="dry-run"
    )
    parser.add_argument("--max-wall-seconds", type=float, default=28_800.0)
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    if arguments.max_wall_seconds <= 0.0 or arguments.max_wall_seconds > 32_400.0:
        raise ValueError("wall limit must be in (0,32400] seconds")
    configure_modules()
    try:
        document = config()
        if arguments.mode == "dry-run":
            result = dry_run(document)
        else:
            jobs = [
                (epsilon_id, base_id)
                for epsilon_id in EPSILON_IDS
                for base_id in (
                    PILOT_BASE_IDS if arguments.mode == "pilot" else BASE_IDS
                )
            ]
            if arguments.mode == "analyze":
                rows = [
                    json.loads(output_path(epsilon_id, base_id).read_text(encoding="utf-8"))
                    for epsilon_id, base_id in jobs
                    if output_path(epsilon_id, base_id).exists()
                ]
            else:
                rows = run_set(document, jobs, arguments.max_wall_seconds)
            scope = "pilot" if arguments.mode == "pilot" else "matrix"
            result = summarize(rows, len(jobs), scope)
            atomic_json(PILOT_JSON if scope == "pilot" else MATRIX_JSON, result)
            write_comparison(rows)
            write_validation(result)
    finally:
        restore_modules()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
