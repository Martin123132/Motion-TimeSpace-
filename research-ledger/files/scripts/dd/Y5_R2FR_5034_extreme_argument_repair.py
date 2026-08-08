from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import time
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
    POST
    / "scripts"
    / "Y5_R2FR_5034_bounded_adaptive_outer_phase_space_smoke.py"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5034"
MARKER = "MTS_5034_EXTREME_ARGUMENT_PROJECTIVE_REPAIR"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


RUNNER = load_module("mts_5034_runner_for_repair", RUNNER_PATH)


def repair(
    base_run_id: str,
    job_key: str,
    initial_steps: int,
    maximum_steps: int,
) -> dict[str, Any]:
    base_directory = RUNNER.RUNS / base_run_id
    config = json.loads((base_directory / "config.json").read_text(encoding="utf-8"))
    jobs = RUNNER.load_jobs(base_directory)
    if job_key not in jobs or jobs[job_key].get("status") != "FAILED":
        raise RuntimeError(f"repair target is not a failed base job: {job_key}")
    expected = {row["job_key"]: row for row in RUNNER.expected_jobs(config)}
    job = expected[job_key]
    event = RUNNER.event_lookup(config)[job["event_id"]]
    argument = RUNNER.argument_lookup(config)[job["argument_id"]]
    tier = config["tiers"][job["tier"]]
    repair_directory = base_directory / "repairs" / job_key
    repair_config = {
        "checkpoint_marker": MARKER,
        "base_run_id": base_run_id,
        "base_config_digest": config["config_digest"],
        "job": job,
        "event": event,
        "argument": argument,
        "tier": tier,
        "path_kind": "feynman",
        "regulator": config["topology"]["regulator"],
        "initial_steps": initial_steps,
        "maximum_steps": maximum_steps,
        "boundary_tracking_steps": config["topology"]["boundary_tracking_steps"],
        "raised_path_fallback_used": False,
        "valid_for_full_MTS_claim": False,
    }
    repair_config["repair_config_digest"] = RUNNER.canonical_digest(repair_config)
    RUNNER.atomic_json(repair_directory / "config.json", repair_config)
    started = time.monotonic()
    target = RUNNER.complex_from_row(argument["target_cosine"])
    RUNNER.configure(event, target)
    steps = initial_steps
    while True:
        topology = RUNNER.M5030.homotopy_gate(
            steps,
            float(repair_config["regulator"]),
            "feynman",
            int(repair_config["boundary_tracking_steps"]),
        )
        if topology["assignment_tracking_passed"] and topology["crossing_groups_consistent"]:
            break
        if steps >= maximum_steps:
            raise RuntimeError(
                "extreme-argument topology did not validate at the repair ceiling"
            )
        steps = min(2 * steps, maximum_steps)
    topology.update(
        {
            "checkpoint_marker": MARKER,
            "base_config_digest": config["config_digest"],
            "repair_config_digest": repair_config["repair_config_digest"],
            "event_id": event["event_id"],
            "argument_id": argument["argument_id"],
            "topology_class_descriptor": RUNNER.topology_descriptor(topology),
            "topology_signature_digest": RUNNER.topology_signature_digest(topology),
            "raised_path_fallback_used": False,
            "valid_for_full_MTS_claim": False,
        }
    )
    topology_file = repair_directory / "topology.json"
    RUNNER.atomic_json(topology_file, topology)
    RUNNER.configure(event, target)
    kernel_started = time.monotonic()
    gate = RUNNER.M5030.fixed_event_integral_gate(
        topology,
        tuple(int(value) for value in tier["relative_orders"]),
        int(tier["global_nodes"]),
        int(tier["global_residue_nodes"]),
        int(tier["relative_residue_nodes"]),
        float(tier["model_distance"]),
        int(config["topology"]["boundary_tracking_steps"]),
        str(tier["relative_quadrature_mode"]),
        float(tier["relative_adaptive_tolerance"]),
        int(tier["relative_adaptive_maximum_intervals"]),
    )
    kernel_seconds = time.monotonic() - kernel_started
    kernel = RUNNER.highest_value(gate)
    direct_value = RUNNER.KERNEL_MULTIPLIER * kernel
    if not RUNNER.finite_complex(direct_value):
        raise RuntimeError("repair produced a non-finite direct kernel")
    kernel_file = repair_directory / "kernel.json"
    RUNNER.atomic_json(
        kernel_file,
        {
            "checkpoint_marker": MARKER,
            "base_config_digest": config["config_digest"],
            "repair_config_digest": repair_config["repair_config_digest"],
            **job,
            "event": event,
            "argument": argument,
            "topology_file": str(topology_file),
            "fixed_event_integral_gate": gate,
            "valid_for_full_MTS_claim": False,
        },
    )
    converged = bool(gate["fixed_event_crossed_integral_converged"])
    result = {
        "checkpoint_marker": MARKER,
        "config_digest": config["config_digest"],
        "repair_config_digest": repair_config["repair_config_digest"],
        **job,
        "seed": event["seed"],
        "sample_index": event["sample_index"],
        "argument": argument["argument"],
        "target_cosine": argument["target_cosine"],
        "status": "COMPLETED_CONVERGED" if converged else "COMPLETED_UNCONVERGED",
        "topology_passed": True,
        "integral_converged": converged,
        "topology_class_descriptor": topology["topology_class_descriptor"],
        "topology_signature_digest": topology["topology_signature_digest"],
        "topology_file": str(topology_file),
        "kernel_file": str(kernel_file),
        "raw_fixed_event_kernel": RUNNER.complex_row(kernel),
        "normalized_direct_D_hhh_over_G3": RUNNER.complex_row(direct_value),
        "highest_two_order_relative_residual": gate[
            "highest_two_order_relative_residual"
        ],
        "effective_homotopy_steps": topology["homotopy_steps"],
        "maximum_collision_assignment_projective_step": topology[
            "maximum_collision_assignment_projective_step"
        ],
        "kernel_runtime_seconds": kernel_seconds,
        "job_runtime_seconds": time.monotonic() - started,
        "replaces_failed_base_job": str(RUNNER.job_path(base_directory, job_key)),
        "representative_kernel_interpolation_used": False,
        "raised_path_fallback_used": False,
        "valid_for_full_MTS_claim": False,
    }
    RUNNER.atomic_json(repair_directory / "job.json", result)
    merged_jobs = dict(jobs)
    merged_jobs[job_key] = result
    summary = RUNNER.build_summary(config, merged_jobs, "COMPLETE_WITH_REPAIR")
    summary.update(
        {
            "base_failed_jobs_before_repairs": sum(
                row.get("status") == "FAILED" for row in jobs.values()
            ),
            "repaired_job_keys": [job_key],
            "repair_files": [
                str(repair_directory / "config.json"),
                str(topology_file),
                str(kernel_file),
                str(repair_directory / "job.json"),
            ],
            "raised_path_fallback_used": False,
            "valid_for_full_MTS_claim": False,
        }
    )
    RUNNER.atomic_json(base_directory / "merged_results.json", summary)
    RUNNER.write_checkpoint_artifacts(config, summary, base_directory)
    authoritative = json.loads(RUNNER.RESULT_JSON.read_text(encoding="utf-8"))
    authoritative["merged_results_file"] = str(base_directory / "merged_results.json")
    authoritative["repair_job_file"] = str(repair_directory / "job.json")
    RUNNER.atomic_json(RUNNER.RESULT_JSON, authoritative)
    document = RUNNER.DOCUMENT.read_text(encoding="utf-8")
    repair_section = f"""
## Extreme-argument repair

The sole terminal failure in the bounded matrix was the first scramble at
`z=-9+0.08i`. Its canonical Feynman root tracker had projective step `0.1312`
at the original 12288-step ceiling. The isolated repair changed no event,
target, contour, residue rule, quadrature tier, or normalization. It only
increased the same canonical path to `{topology['homotopy_steps']}` steps,
where the maximum projective step is
`{topology['maximum_collision_assignment_projective_step']:.6g}`. The repaired
kernel is `{kernel.real:.12g}{kernel.imag:+.12g}i`; its adaptive residual is
`{gate['highest_two_order_relative_residual']:.6g}`. No raised-path result or
representative-class interpolation enters the merged vector.

"""
    if "## Extreme-argument repair" not in document:
        document = document.replace("Marker: `", repair_section + "Marker: `")
        RUNNER.atomic_text(RUNNER.DOCUMENT, document)
    provenance = RUNNER.PROVENANCE.read_text(encoding="utf-8")
    repair_line = (
        f"- Extreme canonical-path repair: `post-checkpoint-work/source-intake/functional_rg/5034/runs/{base_run_id}/repairs/{job_key}/job.json`."
    )
    if repair_line not in provenance:
        RUNNER.atomic_text(RUNNER.PROVENANCE, provenance.rstrip() + "\n" + repair_line + "\n")
    gate_rows = [
        {
            "gate": "repair_topology",
            "passed": topology["assignment_tracking_passed"]
            and topology["crossing_groups_consistent"],
            "evidence": f"steps={topology['homotopy_steps']};projective={topology['maximum_collision_assignment_projective_step']}",
        },
        {
            "gate": "repair_kernel",
            "passed": converged,
            "evidence": f"residual={gate['highest_two_order_relative_residual']}",
        },
        {
            "gate": "merged_primary_vector",
            "passed": next(iter(summary["tiers"].values()))[
                "full_requested_vector_complete"
            ],
            "evidence": f"repaired={job_key}",
        },
        {
            "gate": "full_MTS_claim",
            "passed": False,
            "evidence": "finite-epsilon two-scramble smoke only",
        },
    ]
    repair_gate = SOURCE / "extreme_argument_repair_gate.csv"
    with repair_gate.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("gate", "passed", "evidence", "checkpoint_marker"),
        )
        writer.writeheader()
        for row in gate_rows:
            writer.writerow({**row, "checkpoint_marker": MARKER})
    return {
        "checkpoint_marker": MARKER,
        "job_key": job_key,
        "effective_homotopy_steps": topology["homotopy_steps"],
        "maximum_projective_step": topology[
            "maximum_collision_assignment_projective_step"
        ],
        "kernel": RUNNER.complex_row(kernel),
        "kernel_converged": converged,
        "merged_failed_jobs": summary["failed_jobs"],
        "primary_vector_complete": next(iter(summary["tiers"].values()))[
            "full_requested_vector_complete"
        ],
        "output": str(repair_directory / "job.json"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-run-id", default="bounded_smoke_eps008_v2")
    parser.add_argument(
        "--job-key", default="S503401_N0000__A00__primary24"
    )
    parser.add_argument("--initial-steps", type=int, default=24576)
    parser.add_argument("--maximum-steps", type=int, default=49152)
    arguments = parser.parse_args()
    if arguments.initial_steps <= 12288:
        raise ValueError("repair must strictly refine the exhausted base ceiling")
    if arguments.maximum_steps < arguments.initial_steps:
        raise ValueError("maximum steps must not be below initial steps")
    print(
        json.dumps(
            repair(
                arguments.base_run_id,
                arguments.job_key,
                arguments.initial_steps,
                arguments.maximum_steps,
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
