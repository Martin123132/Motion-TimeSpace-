from __future__ import annotations

import ast
import csv
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5034"
RESIDUALS = POST / "source-intake" / "mts_residuals"
RUN_DIRECTORY = SOURCE / "runs" / "bounded_smoke_eps008_v2"
PILOT_DIRECTORY = SOURCE / "runs" / "bounded_smoke_v1"
DOCUMENT = (
    POST
    / "5034-Y5-R2FR-bounded-adaptive-outer-phase-space-smoke-and-cyclic-hhh-vector.md"
)
PROVENANCE = SOURCE / "PROVENANCE.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
RESULT = SOURCE / "outer_phase_space_smoke_results.json"
VECTOR_CSV = SOURCE / "cyclic_hhh_vector_smoke.csv"
GATE_CSV = SOURCE / "outer_phase_space_smoke_gate.csv"
REPAIR_GATE_CSV = SOURCE / "extreme_argument_repair_gate.csv"
PATH_AUDIT = SOURCE / "path_and_regulator_audit.json"
PATH_AUDIT_GATE_CSV = SOURCE / "path_and_regulator_audit_gate.csv"
MERGED_RESULT = RUN_DIRECTORY / "merged_results.json"
REPAIR_DIRECTORY = (
    RUN_DIRECTORY
    / "repairs"
    / "S503401_N0000__A00__primary24"
)
REPAIR_JOB = REPAIR_DIRECTORY / "job.json"
OUTPUT = RESIDUALS / "P8_Y5_BRR545_5034_VALIDATION.csv"
MARKER = "MTS_5034_BOUNDED_ADAPTIVE_OUTER_PHASE_SPACE_SMOKE"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
SCRIPTS = (
    POST / "scripts" / "Y5_R2FR_5030_causal_relative_collision_homotopy_gate.py",
    POST / "scripts" / "Y5_R2FR_5032_multi_event_causal_topology_grid.py",
    POST / "scripts" / "Y5_R2FR_5034_bounded_adaptive_outer_phase_space_smoke.py",
    POST / "scripts" / "Y5_R2FR_5034_extreme_argument_repair.py",
    POST / "scripts" / "Y5_R2FR_5034_path_regulator_audit.py",
    Path(__file__).resolve(),
)


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


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def resolve_recorded_path(value: str, fallback_directory: Path) -> Path:
    candidate = Path(value)
    if candidate.exists():
        return candidate
    fallback = fallback_directory / candidate.name
    if fallback.exists():
        return fallback
    raise FileNotFoundError(value)


def finite_complex_row(value: dict[str, Any]) -> bool:
    return math.isfinite(float(value["real"])) and math.isfinite(
        float(value["imaginary"])
    )


def check_rows() -> list[tuple[str, bool, str]]:
    config = load_json(RUN_DIRECTORY / "config.json")
    status = load_json(RUN_DIRECTORY / "status.json")
    base_summary = load_json(RUN_DIRECTORY / "partial_results.json")
    merged = load_json(MERGED_RESULT)
    result = load_json(RESULT)
    repair = load_json(REPAIR_JOB)
    repair_config = load_json(REPAIR_DIRECTORY / "config.json")
    repair_topology = load_json(REPAIR_DIRECTORY / "topology.json")
    repair_kernel = load_json(REPAIR_DIRECTORY / "kernel.json")
    path_audit = load_json(PATH_AUDIT)
    pilot = load_json(PILOT_DIRECTORY / "partial_results.json")
    base_jobs = [load_json(path) for path in sorted((RUN_DIRECTORY / "jobs").glob("*.json"))]
    successful_jobs = [row for row in base_jobs if row["status"] == "COMPLETED_CONVERGED"]
    failed_jobs = [row for row in base_jobs if row["status"] == "FAILED"]
    kernel_paths = [
        resolve_recorded_path(row["kernel_file"], RUN_DIRECTORY / "kernels")
        for row in successful_jobs
    ] + [REPAIR_DIRECTORY / "kernel.json"]
    topology_paths = [
        resolve_recorded_path(row["topology_file"], RUN_DIRECTORY / "topologies")
        for row in successful_jobs
    ] + [REPAIR_DIRECTORY / "topology.json"]
    kernels = [load_json(path) for path in kernel_paths]
    topologies = [load_json(path) for path in topology_paths]
    vector_rows = read_csv(VECTOR_CSV)
    gate_rows = read_csv(GATE_CSV)
    repair_gate_rows = read_csv(REPAIR_GATE_CSV)
    path_gate_rows = read_csv(PATH_AUDIT_GATE_CSV)
    provenance_text = PROVENANCE.read_text(encoding="utf-8")
    document_text = DOCUMENT.read_text(encoding="utf-8")
    resume_text = RESUME.read_text(encoding="utf-8")
    cited_paths = [
        ROOT / value
        for value in re.findall(r"`(post-checkpoint-work/[^`]+)`", provenance_text)
    ]
    primary = result["tiers"]["primary24"]
    audit = result["tiers"]["audit32"]
    source_digests_match = all(
        Path(path).exists() and digest(Path(path)) == expected
        for path, expected in config["source_files"].items()
    )
    kernel_gates = [row["fixed_event_integral_gate"] for row in kernels]
    primary_vector_rows = [row for row in vector_rows if row["tier"] == "primary24"]
    numeric_comparisons = primary["nonlocal_target_comparison"]
    checkpoint_files = (
        DOCUMENT,
        PROVENANCE,
        RESULT,
        VECTOR_CSV,
        GATE_CSV,
        REPAIR_GATE_CSV,
        PATH_AUDIT,
        PATH_AUDIT_GATE_CSV,
        MERGED_RESULT,
        REPAIR_JOB,
    )
    formal_digest = tree_digest(FORMAL)
    return [
        (
            "scripts_ast_parse",
            all(ast.parse(path.read_text(encoding="utf-8")) is not None for path in SCRIPTS),
            "all six 5034 causal outer-integral scripts parse",
        ),
        (
            "source_digest_lock",
            source_digests_match,
            f"{len(config['source_files'])} run-time source digests match",
        ),
        (
            "provenance_paths_exist",
            bool(cited_paths) and all(path.exists() for path in cited_paths),
            f"all {len(cited_paths)} cited local paths exist",
        ),
        (
            "csv_outputs_parse",
            len(vector_rows) == 6
            and len(gate_rows) == 8
            and len(repair_gate_rows) == 4
            and len(path_gate_rows) == 5,
            "vector and three gate CSVs parse with expected rows",
        ),
        (
            "exact_outer_measure",
            config["measure_derivation"]["outer_jacobian_in_unit_cube"] == 1.0
            and abs(
                config["measure_derivation"]["kernel_multiplier"]
                + 2.0 / math.pi
            )
            < 1.0e-15
            and result["outer_measure_derived"],
            "dmu=du_x du_s du_d and D=(-2/pi)E[K]",
        ),
        (
            "bounded_scramble_contract",
            config["seeds"] == [503401, 503402]
            and config["power"] == 0
            and config["samples_per_seed"] == 1
            and set(config["tiers"]) == {"primary24", "audit32"},
            "two independent one-point scrambled Sobol replicates; global 24/32 tiers",
        ),
        (
            "positive_regulator_contract",
            config["evaluation_epsilon"] == 0.08
            and all(row["target_cosine"]["imaginary"] == 0.08 for row in config["arguments"])
            and not config["regulator_contract"]["real_boundary_extrapolated"]
            and not config["regulator_contract"]["raised_path_fallback_used"],
            "all fifteen direct arguments lie on Im(z)=0.08; epsilon zero remains open",
        ),
        (
            "restart_and_terminal_base_run",
            status["state"] == "COMPLETE"
            and status["expected_jobs"] == 36
            and status["terminal_jobs"] == 36
            and status["remaining_jobs"] == 0
            and (RUN_DIRECTORY / "COMPLETE").exists(),
            "base run persisted all 36 terminal job files",
        ),
        (
            "isolated_base_failure",
            len(base_jobs) == 36
            and len(successful_jobs) == 35
            and len(failed_jobs) == 1
            and failed_jobs[0]["job_key"] == "S503401_N0000__A00__primary24"
            and base_summary["failed_jobs"] == 1
            and base_summary["unconverged_jobs"] == 0,
            "only first-scramble z=-9 topology exhausted the original ceiling",
        ),
        (
            "canonical_extreme_repair",
            repair["status"] == "COMPLETED_CONVERGED"
            and repair["integral_converged"]
            and repair["effective_homotopy_steps"] == 24576
            and repair["maximum_collision_assignment_projective_step"] < 0.1
            and not repair["raised_path_fallback_used"]
            and repair_config["tier"] == config["tiers"]["primary24"]
            and repair_config["argument"] == config["arguments"][0]
            and repair_topology["path_kind"] == "feynman",
            f"projective={repair['maximum_collision_assignment_projective_step']}",
        ),
        (
            "all_merged_topologies",
            len(topologies) == 36
            and all(
                row["assignment_tracking_passed"]
                and row["crossing_groups_consistent"]
                and row["path_kind"] == "feynman"
                for row in topologies
            ),
            "36 target/event topologies pass on the canonical Feynman path",
        ),
        (
            "all_merged_kernels",
            len(kernels) == 36
            and all(gate["fixed_event_crossed_integral_converged"] for gate in kernel_gates)
            and all(gate["all_residues_stable"] for gate in kernel_gates)
            and max(gate["highest_two_order_relative_residual"] for gate in kernel_gates)
            < 2.0e-3,
            f"max residual={max(gate['highest_two_order_relative_residual'] for gate in kernel_gates)}",
        ),
        (
            "merged_matrix_complete",
            result["run_state"] == "COMPLETE_WITH_REPAIR"
            and result["terminal_jobs"] == 36
            and result["remaining_jobs"] == 0
            and result["failed_jobs"] == 0
            and result["unconverged_jobs"] == 0
            and result["repaired_job_keys"] == ["S503401_N0000__A00__primary24"],
            "all 36 merged jobs are finite and converged",
        ),
        (
            "primary_cyclic_vector",
            primary["full_requested_vector_complete"]
            and primary["complete_seed_vectors"] == [503401, 503402]
            and len(primary["cyclic_rows"]) == 5
            and all(row["completed_triplets"] == 2 for row in primary["cyclic_rows"])
            and all(row["converged_triplets"] == 2 for row in primary["cyclic_rows"])
            and len(primary_vector_rows) == 5,
            "five cyclic components from both independent scrambles",
        ),
        (
            "global_node_audit",
            audit["converged_jobs"] == 6
            and len(result["tier_comparisons"]) == 1
            and result["tier_comparisons"][0]["relative_difference"] < 1.0e-6,
            f"central relative difference={result['tier_comparisons'][0]['relative_difference']}",
        ),
        (
            "fixed_target_not_fitted",
            not result["target_fitted"]
            and not primary["target_fitted"]
            and len(numeric_comparisons) == 5
            and math.isfinite(primary["RMS_nonlocal_target_difference"])
            and primary["RMS_nonlocal_target_difference"] > 0.0,
            f"RMS mismatch={primary['RMS_nonlocal_target_difference']}",
        ),
        (
            "path_and_regulator_red_team",
            path_audit["canonical_feynman"]["assignment_tracking_passed"]
            and path_audit["raised_path"]["assignment_tracking_passed"]
            and not path_audit["path_signatures_match"]
            and path_audit["raised_path_fallback_rejected"]
            and pilot["failed_jobs"] == 12
            and pilot["unconverged_jobs"] == 3,
            "raised path changes winding signature; exact-boundary pilot rejected",
        ),
        (
            "finite_outputs",
            all(
                finite_complex_row(row["estimate"]["mean"])
                for row in primary["cyclic_rows"]
            )
            and all(
                math.isfinite(float(row["computed_nonlocal_component"]))
                and math.isfinite(float(row["computed_minus_target"]))
                for row in numeric_comparisons
            ),
            "cyclic vector and nonlocal comparison are finite",
        ),
        (
            "claim_boundary",
            not result["epsilon_limit_complete"]
            and not result["production_precision_complete"]
            and not result["crossing_complete_hhh_cut_claimed"]
            and not result["valid_for_full_MTS_claim"]
            and "not yet an `hhh` or MTS rejection" in document_text
            and "remain unclaimed" in resume_text,
            "epsilon-zero, production hhh, local GR and full MTS remain open",
        ),
        (
            "resume_handoff",
            MARKER in resume_text
            and "5035-Y5-R2FR-paired-epsilon-zero" in resume_text
            and "four wall-clock" in resume_text,
            "5034 result and bounded 5035 target recorded",
        ),
        (
            "no_missing_markers",
            all(
                "MISSING_" not in path.read_text(encoding="utf-8", errors="ignore")
                for path in checkpoint_files
            ),
            "no placeholder markers in authoritative checkpoint files",
        ),
        (
            "formalization_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "pycache_removed",
            not any(path.is_dir() for path in POST.rglob("__pycache__")),
            "no __pycache__ directory under post-checkpoint-work",
        ),
    ]


def main() -> None:
    rows = check_rows()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("check_id", "passed", "detail", "checkpoint_marker"),
        )
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(rows, start=1):
            writer.writerow(
                {
                    "check_id": f"V5034_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in rows if not passed]
    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "check_count": len(rows),
                "failed": failed,
                "passed": not failed,
                "output": str(OUTPUT),
            },
            indent=2,
        )
    )
    if failed:
        raise RuntimeError(f"checkpoint 5034 validation failed: {failed}")


if __name__ == "__main__":
    main()
