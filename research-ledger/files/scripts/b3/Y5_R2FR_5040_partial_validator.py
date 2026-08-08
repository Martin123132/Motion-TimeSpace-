from __future__ import annotations

import ast
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5040"
RUN = SOURCE / "runs" / "nested_sobol_power1_s4_v1"
SCRIPT = POST / "scripts" / "Y5_R2FR_5040_nested_sobol_variance_reduction.py"
RESIDUE_SCRIPT = POST / "scripts" / "Y5_R2FR_5040_cross_source_residue_diagnostic.py"
BOUNDED_SCRIPT = POST / "scripts" / "Y5_R2FR_5040_bounded_pilot_inclusion_audit.py"
ZERO_SCRIPT = POST / "scripts" / "Y5_R2FR_5041_cross_source_additive_zero_repair.py"
RESUME_SCRIPT = POST / "scripts" / "Y5_R2FR_5041_theorem_guarded_5040_resume.py"
ZERO_AUDIT = POST / "source-intake" / "functional_rg" / "5041" / "cross_source_zero_audit.json"
ZERO_REPAIR = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5041"
    / "repairs"
    / "cross_source_additive_zero_v1"
    / "repair_summary.json"
)
RESUME_REFRESH = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5041"
    / "repairs"
    / "theorem_guarded_resume_contract_v2"
    / "refresh_summary.json"
)
DOCUMENT = POST / "5040-Y5-R2FR-nested-Sobol-variance-reduction-and-sequential-stopping.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
OUTPUT = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5040_PARTIAL_VALIDATION.csv"
)
MARKER = "MTS_5040_NESTED_SOBOL_VARIANCE_REDUCTION"
CONFIG_DIGEST = "39540edd7cae4b42a78ab0c72939aa9f3a7b0e96f27f3063fca3f005db6fc81f"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def check_rows() -> list[tuple[str, bool, str]]:
    config = load(RUN / "config.json")
    unsigned = dict(config)
    supplied_digest = unsigned.pop("config_digest")
    status = load(RUN / "status.json")
    result = load(RUN / "partial_results.json")
    design = load(SOURCE / "sequential_sampling_design.json")
    audit = load(SOURCE / "nested_sobol_variance_audit.json")
    residue_diagnostic = load(SOURCE / "cross_source_residue_diagnostic.json")
    bounded_pilot = load(SOURCE / "bounded_pilot_inclusion_audit.json")
    zero_audit = load(ZERO_AUDIT)
    zero_repair = load(ZERO_REPAIR)
    resume_refresh = load(RESUME_REFRESH)
    jobs = [load(path) for path in sorted((RUN / "jobs").glob("*.json"))]
    imported = [row for row in jobs if row["status"] == "IMPORTED_CONVERGED"]
    computed = [row for row in jobs if row["status"] == "COMPLETED_CONVERGED"]
    sample1_primary = [
        row for row in computed if row["sample_index"] == 1 and row["tier"] == "primary24"
    ]
    sample1_audit = [
        row for row in computed if row["sample_index"] == 1 and row["tier"] == "audit32"
    ]
    sample1_unconverged = [
        row
        for row in jobs
        if row["sample_index"] == 1 and row["status"] == "COMPLETED_UNCONVERGED"
    ]
    source_lock = all(
        expected is not None
        and Path(path).exists()
        and digest(Path(path)) == expected
        for path, expected in config["source_files"].items()
    )
    import_lock = all(
        Path(row["imported_from"]["source_job"]).exists()
        and digest(Path(row["imported_from"]["source_job"]))
        == row["imported_from"]["source_job_sha256"]
        for row in imported
    )
    target_rows = design["one_point_baseline"]["rows"]
    planning_counts = [
        row["normal_approximate_replicates_for_strict_statistical_budget"]
        for row in target_rows
    ]
    tier_rows = result["global_tier_audit"]
    formal_digest = tree_digest(FORMAL)
    document = DOCUMENT.read_text(encoding="utf-8")
    resume = RESUME.read_text(encoding="utf-8")
    return [
        (
            "scripts_parse",
            ast.parse(SCRIPT.read_text(encoding="utf-8")) is not None
            and ast.parse(RESIDUE_SCRIPT.read_text(encoding="utf-8")) is not None
            and ast.parse(BOUNDED_SCRIPT.read_text(encoding="utf-8")) is not None
            and ast.parse(ZERO_SCRIPT.read_text(encoding="utf-8")) is not None
            and ast.parse(RESUME_SCRIPT.read_text(encoding="utf-8")) is not None
            and ast.parse(Path(__file__).read_text(encoding="utf-8")) is not None,
            "runner, residue diagnostic, exact-zero repair/resume, bounded audit and validator parse",
        ),
        (
            "immutable_config_digest",
            supplied_digest == CONFIG_DIGEST
            and supplied_digest == canonical_digest(unsigned),
            supplied_digest,
        ),
        (
            "source_digest_lock",
            source_lock,
            f"{len(config['source_files'])} source hashes validate",
        ),
        (
            "partial_run_partition",
            status["state"] == "COMPLETE"
            and status["expected_jobs"] == 378
            and status["terminal_jobs"] == 378
            and status["remaining_jobs"] == 0
            and len(imported) == 189
            and len(computed) == 189
            and len(sample1_unconverged) == 0,
            "189 exact imports and 189 new converged kernels; no failed or unconverged row",
        ),
        (
            "exact_import_provenance",
            import_lock,
            "all sample-0 import hashes validate",
        ),
        (
            "sample1_primary_complete",
            len(sample1_primary) == 180
            and len({row["epsilon_id"] for row in sample1_primary}) == 3
            and {row["seed"] for row in sample1_primary}
            == {503401, 503402, 503403, 503404}
            and all(row["integral_converged"] for row in sample1_primary),
            "four nested events each close all 45 primary kernels",
        ),
        (
            "sample1_audit_complete",
            len(sample1_audit) == 9
            and all(row["seed"] == 503401 and row["integral_converged"] for row in sample1_audit),
            "first nested event has all nine order-32 checks",
        ),
        (
            "global_order_audit",
            len(tier_rows) == 3
            and all(row["complete"] for row in tier_rows)
            and max(row["relative_difference"] for row in tier_rows) < 1.6e-14
            and result["gate"]["global24_global32_within_threshold"],
            "maximum primary24/audit32 relative difference below 1.6e-14",
        ),
        (
            "strict_target_budget_derived",
            len(target_rows) == 5
            and all(
                abs(row["target_equivalence_margin"] - 0.5 * row["known_master_error"])
                < 1.0e-15
                for row in target_rows
            )
            and planning_counts == [9582816, 32208461, 2305997, 25011199, 2717914],
            "5018 half-error margins and one-point planning counts reproduce",
        ),
        (
            "equal_cost_design_locked",
            abs(
                design["equal_cost_design_contract"][
                    "nested_sd_ratio_required_to_beat_independent"
                ]
                - 0.5253951466465869
            )
            < 1.0e-15
            and audit["equal_cost_design_decision"]
            == "SWITCH_TO_ADDITIONAL_INDEPENDENT_SCRAMBLES"
            and audit["complete_nested_scrambles"]
            == [503401, 503402, 503403, 503404],
            "four production-clean nested replicates select the predeclared independent route",
        ),
        (
            "cross_source_obstruction_resolved",
            residue_diagnostic["candidate_count"] == 8
            and residue_diagnostic["zero_candidate_count"] == 2
            and residue_diagnostic["analytic_residue_required_count"] == 6
            and residue_diagnostic["maximum_empirical_cyclic_impact"] < 8.3e-9
            and zero_audit["candidate_count"] == 8
            and zero_audit["all_candidates_certified"]
            and zero_audit["arbitrary_precision_witness"]["passed"]
            and len(zero_repair["repaired_jobs"]) == 8
            and not zero_repair["still_open"]
            and zero_repair["unconverged_jobs"] == 0
            and resume_refresh["refreshed_jobs"] == 45
            and resume_refresh["total_certificates"] == 372
            and all(
                row["required_for_homotopy"] and not row["near_path"]
                for row in residue_diagnostic["rows"]
            ),
            "all eight direct/subtraction collisions have an exact additive-source zero certificate",
        ),
        (
            "completed_design_verdict",
            audit["equal_cost_design_decision"]
            == "SWITCH_TO_ADDITIONAL_INDEPENDENT_SCRAMBLES"
            and max(
                row["nested_to_independent_halfwidth_ratio"]
                for row in audit["component_rows"]
            )
            > 1.6
            and sum(
                row["nested_to_independent_halfwidth_ratio"] < 1.0
                for row in audit["component_rows"]
            )
            == 1
            and not any(row["target_equivalent"] for row in audit["component_rows"])
            and not any(row["imaginary_equivalent"] for row in audit["component_rows"])
            and sum(row["contraction_supported"] for row in audit["component_rows"])
            == 3,
            "nested wins 1/5 equal-cost components; strict target/imaginary gates fail and contraction passes 3/5",
        ),
        (
            "bounded_design_only_inclusion",
            bounded_pilot["bounded_nested_seeds"] == [503401, 503402, 503403]
            and bounded_pilot["components_below_nested_sd_ratio_threshold"] == [1]
            and bounded_pilot[
                "all_envelopes_below_one_part_in_100000_of_target_margin"
            ]
            and not bounded_pilot["production_precision_complete"]
            and not bounded_pilot["valid_for_full_MTS_claim"],
            "third scramble informs design only and cannot enter production",
        ),
        (
            "claim_boundary",
            not audit["target_fitted"]
            and not audit["reflection_symmetry_imposed"]
            and not audit["epsilon_zero_claimed"]
            and not audit["production_precision_complete"]
            and not audit["valid_for_full_MTS_claim"],
            "no target fit, symmetry, epsilon-zero, production or MTS claim",
        ),
        (
            "handoff_markers",
            MARKER in document
            and MARKER in resume
            and "378/378" in document
            and "378/378" in resume
            and "MTS_5041_THEOREM_GUARDED_5040_RESUME" in document
            and "MTS_5041_THEOREM_GUARDED_5040_RESUME" in resume,
            "document and resume agree",
        ),
        (
            "formalization_untouched",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "no_python_cache",
            not any(POST.rglob("__pycache__")) and not any(POST.rglob("*.pyc")),
            "post-checkpoint-work has no Python cache artifacts",
        ),
    ]


def main() -> None:
    rows = check_rows()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check", "passed", "detail"))
        writer.writeheader()
        for name, passed, detail in rows:
            writer.writerow(
                {"check": name, "passed": str(bool(passed)).lower(), "detail": detail}
            )
    failed = [name for name, passed, _ in rows if not passed]
    print(json.dumps({"passed": len(rows) - len(failed), "total": len(rows), "failed": failed}, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
