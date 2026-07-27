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
SOURCE_5037 = POST / "source-intake" / "functional_rg" / "5037"
SOURCE_5039 = POST / "source-intake" / "functional_rg" / "5039"
RUN = SOURCE_5037 / "runs" / "paired_outer_precision_s4_v1"
RESULT = SOURCE_5037 / "paired_outer_precision_results.json"
AUDIT = SOURCE_5039 / "completed_matrix_uncertainty_audit.json"
LEDGER = SOURCE_5039 / "provenance_ledger.json"
DOCUMENT = POST / "5039-Y5-R2FR-completed-four-scramble-uncertainty-and-target-audit.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
OUTPUT = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5039_VALIDATION.csv"
)
MARKER = "MTS_5039_COMPLETED_MATRIX_UNCERTAINTY_AUDIT"
CONFIG_DIGEST = "86e46b1d2663217182a1bd246c1367e6dfd1eca61694ec86c388d3182e502c49"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
ENDPOINT_REPAIRS = (
    "finite_endpoint_sector_e080_seed3_v1",
    "finite_endpoint_sector_v1",
    "finite_endpoint_sector_e020_seed3_v1",
)
CHART_REPAIRS = (
    "chart_origin_collision_v1",
    "chart_origin_collision_e020_seed3_v1",
    "chart_origin_collision_e080_seed3_v1",
)
SCRIPTS = (
    POST / "scripts" / "Y5_R2FR_5037_endpoint_sector_repair.py",
    POST / "scripts" / "Y5_R2FR_5037_chart_origin_collision_repair.py",
    POST / "scripts" / "Y5_R2FR_5039_completed_matrix_uncertainty_audit.py",
    POST / "scripts" / "Y5_R2FR_5039_provenance_ledger.py",
    Path(__file__).resolve(),
)


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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def records(value: Any) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if isinstance(value, dict):
        if set(value) == {"path", "sha256"}:
            rows.append(value)
        else:
            for child in value.values():
                rows.extend(records(child))
    elif isinstance(value, list):
        for child in value:
            rows.extend(records(child))
    return rows


def record_valid(row: dict[str, str]) -> bool:
    path = Path(row["path"])
    return path.exists() and digest(path) == row["sha256"]


def check_rows() -> list[tuple[str, bool, str]]:
    config = load(RUN / "config.json")
    unsigned = dict(config)
    supplied_digest = unsigned.pop("config_digest")
    status = load(RUN / "status.json")
    result = load(RESULT)
    audit = load(AUDIT)
    ledger = load(LEDGER)
    jobs = [load(path) for path in sorted((RUN / "jobs").glob("*.json"))]
    imported = [row for row in jobs if row["status"] == "IMPORTED_CONVERGED"]
    computed = [row for row in jobs if row["status"] == "COMPLETED_CONVERGED"]
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
    endpoint_summaries = [
        load(SOURCE_5037 / "repairs" / repair_id / "repair_summary.json")
        for repair_id in ENDPOINT_REPAIRS
    ]
    endpoint_certificates = [
        certificate
        for summary in endpoint_summaries
        for certificate in summary["repair_contract"]["primary_certificates"]
    ]
    chart_summaries = [
        load(SOURCE_5037 / "repairs" / repair_id / "repair_summary.json")
        for repair_id in CHART_REPAIRS
    ]
    chart_keys = {
        key for summary in chart_summaries for key in summary["repaired_jobs"]
    }
    contraction = read_csv(SOURCE_5039 / "contraction_uncertainty.csv")
    target = read_csv(SOURCE_5039 / "fixed_target_uncertainty.csv")
    reflection = read_csv(SOURCE_5039 / "reflection_uncertainty.csv")
    ledger_rows = records(ledger)
    document = DOCUMENT.read_text(encoding="utf-8")
    resume = RESUME.read_text(encoding="utf-8")
    formal_digest = tree_digest(FORMAL)
    return [
        (
            "scripts_parse",
            all(ast.parse(path.read_text(encoding="utf-8")) is not None for path in SCRIPTS),
            "production repairs, uncertainty audit, ledger and validator parse",
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
            f"{len(config['source_files'])} locked sources match",
        ),
        (
            "complete_matrix_state",
            status["state"] == "COMPLETE"
            and status["expected_jobs"] == 189
            and status["terminal_jobs"] == 189
            and status["remaining_jobs"] == 0
            and status["failed_jobs"] == 0
            and status["unconverged_jobs"] == 0
            and (RUN / "COMPLETE").exists(),
            "189/189 terminal with no open row",
        ),
        (
            "numeric_job_partition",
            len(jobs) == 189
            and len(imported) == 117
            and len(computed) == 72
            and all(
                row["status"] in {"IMPORTED_CONVERGED", "COMPLETED_CONVERGED"}
                and row.get("integral_converged")
                for row in jobs
            ),
            "117 imports plus 72 computed-converged kernels",
        ),
        (
            "exact_import_provenance",
            import_lock,
            "all 117 import hashes validate",
        ),
        (
            "three_endpoint_repairs",
            len(endpoint_summaries) == 3
            and all(
                summary["accepted"]
                and summary["promoted"]
                and summary["kernel_relative_residual"] == 0.0
                and summary["primary"]["status"] == "COMPLETED_CONVERGED"
                and summary["audit"]["status"] == "COMPLETED_CONVERGED"
                for summary in endpoint_summaries
            ),
            "A14 at all three epsilons has an independent two-floor repair",
        ),
        (
            "endpoint_certificate_gates",
            len(endpoint_certificates) == 24
            and all(row["boundary_valid"] for row in endpoint_certificates)
            and max(
                row["residue_probe"]["maximum_residue_magnitude"]
                for row in endpoint_certificates
            )
            < 1.1e-14
            and max(row["limit_relative_residual"] for row in endpoint_certificates)
            < 1.0e-8
            and max(
                row["adjacent_limit_relative_residual"]
                for row in endpoint_certificates
            )
            < 1.0e-8,
            "24 endpoint sides pass residue and two-sided-limit gates",
        ),
        (
            "six_chart_repairs",
            len(chart_keys) == 6
            and all(len(summary["repaired_jobs"]) == 2 for summary in chart_summaries)
            and all(
                load(RUN / "jobs" / f"{key}.json")["status"]
                == "COMPLETED_CONVERGED"
                for key in chart_keys
            ),
            "six chart-origin-only jobs close under v5",
        ),
        (
            "four_scramble_gate",
            result["gate"]["all_expected_jobs_numeric_and_converged"]
            and result["gate"]["four_scramble_linear_matrix_complete"]
            and result["gate"]["minimum_four_scramble_precision_smoke"]
            and result["outer_precision_diagnostic"]["completed_paired_scrambles"] == 4,
            "complete four-scramble minimum smoke passes",
        ),
        (
            "deterministic_convergence_boundary",
            result["gate"]["full_vector_mean_step_contracts"]
            and result["gate"]["local_coefficient_mean_step_contracts"]
            and not result["gate"]["all_five_nonlocal_mean_steps_contract"]
            and not result["gate"]["paired_full_vector_ladder_stable"],
            "raw nonlocal components 0 and 3 prevent deterministic promotion",
        ),
        (
            "uncertainty_audit_sources",
            audit["source_result_sha256"] == digest(RESULT)
            and audit["source_status_sha256"] == digest(RUN / "status.json")
            and audit["paired_scrambles"] == 4
            and audit["maximum_recomputed_projection_residual"] < 1.0e-12,
            "audit is tied to the final complete matrix",
        ),
        (
            "contraction_uncertainty",
            len(contraction) == 5
            and audit["summary"]["raw_mean_contraction_failed_components"] == [0, 3]
            and not audit["summary"]["noncontraction_supported_95_components"]
            and audit["summary"]["all_linear_defects_include_zero_in_hotelling_95"]
            and sum(
                row["classification"] == "contraction_supported_95"
                for row in contraction
            )
            == 1
            and sum(
                row["classification"] == "unresolved_at_four_scrambles"
                for row in contraction
            )
            == 4,
            "no component supports noncontraction; four remain unresolved",
        ),
        (
            "fixed_target_uncertainty",
            len(target) == 5
            and not audit["summary"]["fixed_target_components_excluded_95"]
            and not audit["summary"]["imaginary_zero_excluded_95_components"]
            and [int(row["planning_count"]) for row in target]
            == [48, 14, 40, 33, 10],
            "target is not excluded or matched; planning counts are recorded",
        ),
        (
            "reflection_uncertainty",
            len(reflection) == 2
            and not audit["summary"]["reflection_target_odd_excluded_95"]
            and all(row["target_odd_excluded_95"] == "False" for row in reflection),
            "neither measured odd component excludes the target",
        ),
        (
            "claim_boundary",
            not audit["target_fitted"]
            and not audit["epsilon_zero_claimed"]
            and not audit["production_precision_complete"]
            and not audit["valid_for_full_MTS_claim"]
            and not result["gate"]["fixed_target_verdict_ready"],
            "no target, epsilon-zero, production or MTS promotion",
        ),
        (
            "provenance_ledger",
            ledger["checkpoint_marker"] == "MTS_5039_PROVENANCE_LEDGER"
            and len(ledger_rows) >= 50
            and all(record_valid(row) for row in ledger_rows),
            f"{len(ledger_rows)} final artifact hashes validate",
        ),
        (
            "handoff_markers",
            MARKER in document
            and MARKER in resume
            and "189/189" in document
            and "189/189" in resume,
            "5039 document and resume handoff agree",
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
