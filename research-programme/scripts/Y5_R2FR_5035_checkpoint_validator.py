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
SOURCE = POST / "source-intake" / "functional_rg" / "5035"
RESIDUALS = POST / "source-intake" / "mts_residuals"
RUN = SOURCE / "runs" / "central_eps008_004_002_s4_v1"
REPAIR = SOURCE / "repairs" / "pair_local_shrinking_radius_v1"
DOCUMENT = (
    POST
    / "5035-Y5-R2FR-paired-epsilon-zero-and-outer-scramble-convergence-ladder.md"
)
PROVENANCE = SOURCE / "PROVENANCE.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
RESULT = SOURCE / "paired_epsilon_ladder_results.json"
LADDER_CSV = SOURCE / "central_epsilon_ladder.csv"
PAIRED_CSV = SOURCE / "paired_epsilon_differences.csv"
AUDIT_CSV = SOURCE / "global_tier_audit.csv"
GATE_CSV = SOURCE / "epsilon_ladder_gate.csv"
OUTPUT = RESIDUALS / "P8_Y5_BRR545_5035_VALIDATION.csv"
MARKER = "MTS_5035_PAIRED_EPSILON_ZERO_OUTER_SCRAMBLE_LADDER"
REPAIR_MARKER = "MTS_5035_PAIR_LOCAL_RESIDUE_SHRINKING_RADIUS_REPAIR"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
SCRIPTS = (
    POST / "scripts" / "Y5_R2FR_5030_causal_relative_collision_homotopy_gate.py",
    POST / "scripts" / "Y5_R2FR_5032_multi_event_causal_topology_grid.py",
    POST / "scripts" / "Y5_R2FR_5034_bounded_adaptive_outer_phase_space_smoke.py",
    POST / "scripts" / "Y5_R2FR_5035_paired_epsilon_outer_scramble_ladder.py",
    POST / "scripts" / "Y5_R2FR_5035_pair_local_residue_radius_repair.py",
    Path(__file__).resolve(),
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


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


def finite_complex_row(value: dict[str, Any]) -> bool:
    return math.isfinite(float(value["real"])) and math.isfinite(
        float(value["imaginary"])
    )


def close(value: float, expected: float, tolerance: float = 1.0e-9) -> bool:
    return abs(value - expected) <= tolerance * max(1.0, abs(expected))


def check_rows() -> list[tuple[str, bool, str]]:
    config = load_json(RUN / "config.json")
    unsigned_config = dict(config)
    supplied_config_digest = unsigned_config.pop("config_digest")
    status = load_json(RUN / "status.json")
    result = load_json(RESULT)
    repair = load_json(REPAIR / "repair_summary.json")
    jobs = [load_json(path) for path in sorted((RUN / "jobs").glob("*.json"))]
    imported = [row for row in jobs if row["status"] == "IMPORTED_CONVERGED"]
    computed = [row for row in jobs if row["status"] == "COMPLETED_CONVERGED"]
    repaired = [row for row in jobs if "repair_contract" in row]
    computed_kernels = [
        load_json(RUN / "kernels" / f"{row['job_key']}.json")
        for row in computed
    ]
    repaired_kernels = [
        load_json(RUN / "kernels" / f"{row['job_key']}.json")
        for row in repaired
    ]
    source_digests_match = all(
        expected is not None and Path(path).exists() and digest(Path(path)) == expected
        for path, expected in config["source_files"].items()
    )
    imported_sources_match = all(
        Path(row["imported_from"]["source_job"]).exists()
        and digest(Path(row["imported_from"]["source_job"]))
        == row["imported_from"]["source_job_sha256"]
        for row in imported
    )
    topology_paths_exist = all(
        Path(row["topology_file"]).exists() for row in computed
    )
    repair_script = SCRIPTS[4]
    repair_contracts_match = all(
        row["repair_contract"]["repair_script_sha256"] == digest(repair_script)
        and row["repair_contract"]["checkpoint_marker"] == REPAIR_MARKER
        and digest(REPAIR / "original" / f"{row['job_key']}.json")
        == row["repair_contract"]["original_job_sha256"]
        and digest(
            REPAIR / "original" / f"kernel__{row['job_key']}.json"
        )
        == row["repair_contract"]["original_kernel_sha256"]
        for row in repaired
    )
    ladder = {
        (float(row["epsilon"]), row["tier"]): row
        for row in result["central_epsilon_ladder"]
    }
    primary_expected = {
        0.08: (-65.94549782722879, -16.312376295778865),
        0.04: (-76.81180655673512, -11.594497107418055),
        0.02: (-80.53964407852916, -6.541949195619981),
    }
    ladder_values_match = all(
        ladder[(epsilon, "primary24")]["completed_scrambles"] == 4
        and close(
            ladder[(epsilon, "primary24")]["estimate"]["mean"]["real"],
            expected[0],
        )
        and close(
            ladder[(epsilon, "primary24")]["estimate"]["mean"]["imaginary"],
            expected[1],
        )
        for epsilon, expected in primary_expected.items()
    )
    tier_audit = result["global_tier_audit"]
    paired = result["paired_epsilon_differences"]
    gate = result["gate"]
    repair_audit = repair["radius_audit"]
    ladder_csv = read_csv(LADDER_CSV)
    paired_csv = read_csv(PAIRED_CSV)
    audit_csv = read_csv(AUDIT_CSV)
    gate_csv = read_csv(GATE_CSV)
    document_text = DOCUMENT.read_text(encoding="utf-8")
    provenance_text = PROVENANCE.read_text(encoding="utf-8")
    resume_text = RESUME.read_text(encoding="utf-8")
    cited_relative_paths = [
        ROOT / value
        for value in re.findall(r"`(post-checkpoint-work/[^`]+)`", provenance_text)
    ]
    authoritative = (
        DOCUMENT,
        PROVENANCE,
        RESULT,
        LADDER_CSV,
        PAIRED_CSV,
        AUDIT_CSV,
        GATE_CSV,
        REPAIR / "repair_summary.json",
    )
    formal_digest = tree_digest(FORMAL)
    return [
        (
            "scripts_ast_parse",
            all(ast.parse(path.read_text(encoding="utf-8")) is not None for path in SCRIPTS),
            "5030/5032/5034 plus three 5035 scripts parse",
        ),
        (
            "immutable_config_digest",
            supplied_config_digest == canonical_digest(unsigned_config),
            supplied_config_digest,
        ),
        (
            "source_digest_lock",
            source_digests_match,
            f"{len(config['source_files'])} locked sources match",
        ),
        (
            "paired_design",
            config["epsilons"] == [0.08, 0.04, 0.02]
            and config["seeds"] == [503401, 503402, 503403, 503404]
            and config["power"] == 0
            and config["samples_per_seed"] == 1
            and len(config["arguments"]) == 9
            and config["estimator_contract"]["same_sobol_event_paired_across_epsilon"]
            and not config["estimator_contract"]["target_5018_fitted"],
            "three epsilon levels, four paired scrambles, exact central triplet",
        ),
        (
            "terminal_job_matrix",
            len(jobs) == 45
            and len(imported) == 9
            and len(computed) == 36
            and status["state"] == "COMPLETE_WITH_RESIDUE_RADIUS_REPAIR"
            and status["remaining_jobs"] == 0
            and status["failed_jobs"] == 0
            and status["unconverged_jobs"] == 0
            and (RUN / "COMPLETE").exists(),
            "45/45 terminal: 9 exact imports plus 36 computed",
        ),
        (
            "exact_import_provenance",
            imported_sources_match
            and all(row["topology_passed"] and row["integral_converged"] for row in imported),
            "all imported 5034 job hashes and convergence flags validate",
        ),
        (
            "computed_topologies_and_kernels",
            topology_paths_exist
            and len(computed_kernels) == 36
            and all(
                kernel["fixed_event_integral_gate"]["fixed_event_crossed_integral_converged"]
                and kernel["fixed_event_integral_gate"]["all_residues_stable"]
                for kernel in computed_kernels
            ),
            "36 computed jobs retain target-specific topologies and converged kernels",
        ),
        (
            "finite_direct_values",
            all(
                finite_complex_row(row["normalized_direct_D_hhh_over_G3"])
                for row in jobs
            ),
            "all 45 normalized direct values are finite",
        ),
        (
            "residue_repair_scope",
            len(repaired) == 6
            and len(repaired_kernels) == 6
            and len(repair["candidate_jobs"]) == 6
            and repair["repaired_jobs"] == repair["candidate_jobs"]
            and not repair["still_unconverged_jobs"]
            and not repair["remaining_unrepaired_candidates"],
            "only the six v3 residue-instability jobs were repaired",
        ),
        (
            "shrinking_radius_plateau",
            len(repair_audit) == 6
            and all(row["selected_fraction"] == 0.05 for row in repair_audit)
            and all(row["selected_stable"] for row in repair_audit)
            and all(not row["candidate_rows"][0]["stable"] for row in repair_audit)
            and all(row["candidate_rows"][1]["stable"] for row in repair_audit)
            and all(
                kernel["fixed_event_integral_gate"]["relative_residue_revision"]
                == "pair-local-double-residue-shrinking-radius-v4"
                for kernel in repaired_kernels
            ),
            "all six unstable 0.1 circles close on nested 0.05 circles",
        ),
        (
            "repair_hash_chain",
            repair_contracts_match
            and len(list((REPAIR / "original").glob("*.json"))) == 12
            and len(list((REPAIR / "repaired").glob("*.json"))) == 12,
            "original/repaired job and kernel hashes retained",
        ),
        (
            "central_ladder_values",
            ladder_values_match,
            "all primary means match the locked four-scramble result",
        ),
        (
            "paired_differences",
            len(paired) == 2
            and all(row["paired_scrambles"] == 4 for row in paired)
            and close(paired[0]["estimate"]["mean"]["real"], -10.866308729506335)
            and close(paired[1]["estimate"]["mean"]["real"], -3.72783752179404)
            and result["extrapolation_diagnostics"]["successive_mean_step_contracts"],
            "paired mean-step norm contracts from 11.8463 to 6.27893",
        ),
        (
            "effective_order_diagnostic",
            close(
                result["extrapolation_diagnostics"][
                    "effective_order_from_complex_step_norm"
                ],
                0.9158461197056401,
            )
            and result["extrapolation_diagnostics"][
                "linear_epsilon_model_tested_not_assumed"
            ]
            and not result["extrapolation_diagnostics"]["epsilon_zero_claimed"],
            "p_eff=0.915846 is diagnostic, not imposed",
        ),
        (
            "global_node_audit",
            len(tier_audit) == 3
            and all(row["complete"] for row in tier_audit)
            and max(row["relative_difference"] for row in tier_audit) < 2.0e-13,
            f"max relative tier difference={max(row['relative_difference'] for row in tier_audit)}",
        ),
        (
            "central_extension_gate",
            gate["all_expected_jobs_numeric_and_converged"]
            and gate["all_primary_epsilon_scrambles_complete"]
            and gate["global24_global32_within_threshold"]
            and gate["successive_mean_epsilon_step_contracts"]
            and gate["central_ladder_allows_full_vector_smoke"],
            "central smoke authorizes bounded full-vector extension",
        ),
        (
            "claim_boundary",
            not gate["epsilon_zero_limit_complete"]
            and not gate["production_precision_complete"]
            and not gate["crossing_complete_hhh_claim"]
            and not gate["valid_for_full_MTS_claim"]
            and not result["target_5018_fitted"]
            and "does **not** establish the epsilon-zero limit" in document_text,
            "epsilon zero, production hhh, local GR and full MTS remain open",
        ),
        (
            "csv_outputs_parse",
            len(ladder_csv) == 6
            and len(paired_csv) == 2
            and len(audit_csv) == 3
            and len(gate_csv) == len(gate),
            "ladder, paired, audit and gate CSVs parse with expected rows",
        ),
        (
            "provenance_paths_exist",
            len(cited_relative_paths) >= 2
            and all(path.exists() for path in cited_relative_paths),
            f"all {len(cited_relative_paths)} relative provenance paths exist",
        ),
        (
            "resume_handoff",
            MARKER in resume_text
            and "5036-Y5-R2FR-paired-epsilon-full-cyclic-vector" in resume_text
            and "No GitHub action was taken" in resume_text,
            "5035 result, boundary and 5036 target recorded",
        ),
        (
            "no_missing_markers",
            all(
                "MISSING_" not in path.read_text(encoding="utf-8", errors="ignore")
                for path in authoritative
            ),
            "no placeholder markers in authoritative 5035 artifacts",
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
                    "check_id": f"V5035_{index:02d}_{name}",
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
        raise RuntimeError(f"checkpoint 5035 validation failed: {failed}")


if __name__ == "__main__":
    main()
