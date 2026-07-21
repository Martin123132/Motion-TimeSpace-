from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
    POST
    / "scripts"
    / "Y5_R2FR_5034_bounded_adaptive_outer_phase_space_smoke.py"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5034"
OUTPUT_JSON = SOURCE / "path_and_regulator_audit.json"
OUTPUT_CSV = SOURCE / "path_and_regulator_audit_gate.csv"
MARKER = "MTS_5034_PATH_AND_REGULATOR_AUDIT"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


RUNNER = load_module("mts_5034_runner_for_path_audit", RUNNER_PATH)


def serialized_signature(document: dict[str, Any]) -> list[list[list[Any]]]:
    return [
        [list(row) for row in chamber]
        for chamber in RUNNER.M5032.topology_signature(document)
    ]


def audit() -> dict[str, Any]:
    final_directory = RUNNER.RUNS / "bounded_smoke_eps008_v2"
    pilot_directory = RUNNER.RUNS / "bounded_smoke_v1"
    config = json.loads((final_directory / "config.json").read_text(encoding="utf-8"))
    event = next(row for row in config["events"] if row["seed"] == 503401)
    argument = next(
        row for row in config["arguments"] if abs(row["argument"] + 3.0) < 1.0e-12
    )
    target = RUNNER.complex_from_row(argument["target_cosine"])
    RUNNER.configure(event, target)
    feynman = RUNNER.M5030.homotopy_gate(6144, 1.0e-3, "feynman", 64)
    RUNNER.configure(event, target)
    raised = RUNNER.M5030.homotopy_gate(768, 1.0e-3, "raised", 64)
    feynman_signature = serialized_signature(feynman)
    raised_signature = serialized_signature(raised)
    pilot = json.loads(
        (pilot_directory / "partial_results.json").read_text(encoding="utf-8")
    )
    final = json.loads(RUNNER.RESULT_JSON.read_text(encoding="utf-8"))
    result = {
        "checkpoint_marker": MARKER,
        "event": event,
        "target_cosine": argument["target_cosine"],
        "canonical_feynman": {
            "steps": 6144,
            "assignment_tracking_passed": feynman["assignment_tracking_passed"],
            "crossing_groups_consistent": feynman["crossing_groups_consistent"],
            "maximum_projective_step": feynman[
                "maximum_collision_assignment_projective_step"
            ],
            "surface_crossing_count": feynman["total_surface_crossings"],
            "signature_digest": RUNNER.canonical_digest(feynman_signature),
        },
        "raised_path": {
            "steps": 768,
            "assignment_tracking_passed": raised["assignment_tracking_passed"],
            "crossing_groups_consistent": raised["crossing_groups_consistent"],
            "maximum_projective_step": raised[
                "maximum_collision_assignment_projective_step"
            ],
            "surface_crossing_count": raised["total_surface_crossings"],
            "signature_digest": RUNNER.canonical_digest(raised_signature),
        },
        "path_signatures_match": feynman_signature == raised_signature,
        "raised_path_fallback_rejected": feynman_signature != raised_signature,
        "real_endpoint_pilot": {
            "run_id": pilot["run_id"],
            "failed_jobs": pilot["failed_jobs"],
            "unconverged_jobs": pilot["unconverged_jobs"],
            "primary_vector_complete": pilot["tiers"]["primary12"][
                "full_requested_vector_complete"
            ],
        },
        "positive_regulator_run": {
            "run_id": final["run_id"],
            "evaluation_epsilon": config["evaluation_epsilon"],
            "failed_jobs_after_repair": final["failed_jobs"],
            "unconverged_jobs": final["unconverged_jobs"],
            "primary_vector_complete": final["tiers"]["primary24"][
                "full_requested_vector_complete"
            ],
            "central_global_tier_relative_difference": final[
                "tier_comparisons"
            ][0]["relative_difference"],
        },
        "decision": "retain canonical near-boundary Feynman path; use finite positive epsilon for the bounded smoke; require a later epsilon-to-zero ladder",
        "target_fitted": False,
        "valid_for_full_MTS_claim": False,
    }
    RUNNER.atomic_json(OUTPUT_JSON, result)
    rows = [
        {
            "gate": "canonical_feynman_tracked",
            "passed": feynman["assignment_tracking_passed"]
            and feynman["crossing_groups_consistent"],
            "evidence": f"steps=6144;projective={feynman['maximum_collision_assignment_projective_step']}",
        },
        {
            "gate": "raised_path_not_substituted",
            "passed": feynman_signature != raised_signature,
            "evidence": "net winding signatures differ at z=-3+0.08i",
        },
        {
            "gate": "real_endpoint_pilot_rejected",
            "passed": pilot["failed_jobs"] > 0
            and pilot["unconverged_jobs"] > 0
            and not pilot["tiers"]["primary12"]["full_requested_vector_complete"],
            "evidence": f"failed={pilot['failed_jobs']};unconverged={pilot['unconverged_jobs']}",
        },
        {
            "gate": "finite_epsilon_smoke_complete",
            "passed": final["failed_jobs"] == 0
            and final["unconverged_jobs"] == 0
            and final["tiers"]["primary24"]["full_requested_vector_complete"],
            "evidence": f"epsilon={config['evaluation_epsilon']}",
        },
        {
            "gate": "epsilon_zero_or_full_MTS_claim",
            "passed": False,
            "evidence": "epsilon ladder and outer convergence remain open",
        },
    ]
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("gate", "passed", "evidence", "checkpoint_marker"),
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({**row, "checkpoint_marker": MARKER})
    return result


def main() -> None:
    print(json.dumps(audit(), indent=2))


if __name__ == "__main__":
    main()
