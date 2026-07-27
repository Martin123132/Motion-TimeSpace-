from __future__ import annotations

import csv
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
RUNS = POST_CHECKPOINT / "runs"

OUTPUT_DOC = POST_CHECKPOINT / "850-Y5-R10-fixed-bmem-cosmology-score-evaluator-dry-run.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_850_SOURCE_REGISTER.csv"
RUN_RESULT_PATH = RESIDUALS / "P8_Y5_R10_850_EVALUATOR_RUN_RESULT.csv"
SCORE_PATH = RESIDUALS / "P8_Y5_R10_850_FIXED_BMEM_SN_BAO_SAMPLE_SCORES.csv"
BASELINE_REFERENCE_PATH = RESIDUALS / "P8_Y5_R10_850_BASELINE_REFERENCE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_850_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_850_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_850_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_850_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_850_VALIDATION.csv"

CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_847_STRICT_COSMOLOGY_CANDIDATES.csv"
EVALUATOR_PATH = POST_CHECKPOINT / "scripts" / "strict_fixed_bmem_SN_BAO_evaluator.py"
CONFIG_PATH = FORMALIZATION / "configs" / "cosmology_background_R1_current.json"

STATUS = "Y5_R10_850_fixed_bmem_SN_BAO_sample_scores_written_nonclaim"
CLAIM_CEILING = "sample_score_only_no_fit_no_support_no_parent_prediction"
NEXT_TARGET = "851-Y5-R10-fixed-bmem-SN-BAO-readout-and-eta-law-choice.md"

SOURCE_SPECS = [
    {
        "source_id": "849_doc",
        "path": POST_CHECKPOINT / "849-Y5-R10-strict-cosmology-scoring-adapter-or-parent-amplitude-tightening.md",
        "needles": [
            "no-fit scoring-adapter dry run",
            "850-Y5-R10-fixed-bmem-cosmology-score-evaluator-dry-run.md",
        ],
        "role": "adapter handoff",
    },
    {
        "source_id": "849_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_849_VALIDATION.csv",
        "needles": [
            "V849_4_adapter_dry_run_passed_no_fit,pass",
            "V849_6_no_run_authorized,pass",
            "V849_12_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "847_candidates",
        "path": CANDIDATE_PATH,
        "needles": ["S0_null_bmem_0", "S2_corridor_eta1_aFDeltaR_1p0", "S3_parent_predicted_placeholder"],
        "role": "strict fixed-bmem candidate rows",
    },
    {
        "source_id": "850_evaluator_script",
        "path": EVALUATOR_PATH,
        "needles": ["Sample-only fixed-b_mem SN/BAO evaluator.", "FIXED_BMEM_SN_BAO_SAMPLE_SCORES.csv", "optimizer_executed"],
        "role": "new fixed-bmem sample evaluator",
    },
    {
        "source_id": "R1_cosmology_config",
        "path": CONFIG_PATH,
        "needles": ["R1_current_background", "\"id\": \"M6\"", "PantheonPlusSH0ES", "DESI_DR2_BAO"],
        "role": "SN/BAO data and sample-parameter config",
    },
    {
        "source_id": "cosmology_likelihood_smoke_script",
        "path": FORMALIZATION / "scripts" / "cosmology_likelihood_smoke.py",
        "needles": ["def evaluate_model", "def load_pantheon", "def load_bao", "add_information_criteria"],
        "role": "reference likelihood functions imported read-only",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def check_needles(path: Path, needles: list[str]) -> str:
    text = read_text(path)
    if not text:
        return "missing_path"
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return "missing_needles:" + ";".join(missing)
    return "pass"


def validation_file_clean(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing={path}"
    failures: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{path.name} clean"


def formalization_workbench_modified_count() -> int:
    command = (
        "$fw='"
        + str(FORMALIZATION).replace("'", "''")
        + "'; "
        + "$cutoff=[datetime]'2026-05-31T14:42:00'; "
        + "(Get-ChildItem -LiteralPath $fw -Recurse -File | "
        + "Where-Object { $_.LastWriteTime -gt $cutoff }).Count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return int(completed.stdout.strip() or "0")


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = spec["path"]
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(path),
                "exists": str(path.exists()).lower(),
                "needle_check": check_needles(path, spec["needles"]),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def run_evaluator() -> tuple[Path, dict[str, object], str]:
    command = [
        "python",
        str(EVALUATOR_PATH),
        "--candidates",
        str(CANDIDATE_PATH),
        "--config",
        str(CONFIG_PATH),
        "--branches",
        "sh0es",
        "no_sh0es",
        "--integration-steps",
        "1024",
        "--dry-run",
        "--sample-score",
        "--no-fit",
        "--write-run-dir",
        "--output-root",
        str(RUNS),
    ]
    completed = subprocess.run(
        command,
        cwd=str(POST_CHECKPOINT),
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )
    run_dir_text = ""
    for line in completed.stdout.splitlines():
        if line.startswith("run_dir="):
            run_dir_text = line.split("=", 1)[1].strip()
            break
    if not run_dir_text:
        raise RuntimeError("evaluator did not print run_dir")
    run_dir = Path(run_dir_text)
    status = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    return run_dir, status, completed.stdout


def run_result_rows(run_dir: Path, status: dict[str, object], stdout: str, generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "run_id": run_dir.name,
            "run_dir": str(run_dir),
            "status": status.get("status"),
            "dry_run_only": str(status.get("dry_run_only")).lower(),
            "sample_score": str(status.get("sample_score")).lower(),
            "no_fit": str(status.get("no_fit")).lower(),
            "fit_executed": str(status.get("fit_executed")).lower(),
            "optimizer_executed": str(status.get("optimizer_executed")).lower(),
            "claim_allowed": str(status.get("claim_allowed")).lower(),
            "row_count": status.get("row_count"),
            "pass_count": status.get("pass_count"),
            "blocked_count": status.get("blocked_count"),
            "failure_count": status.get("failure_count"),
            "runner_stdout": stdout.replace("\n", " | "),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def score_rows(run_dir: Path, generated_utc: str) -> list[dict[str, object]]:
    source = run_dir / "FIXED_BMEM_SN_BAO_SAMPLE_SCORES.csv"
    rows: list[dict[str, object]] = []
    for row in read_csv(source):
        rows.append({**row, "valid_for_claim": "false", "generated_utc": generated_utc})
    return rows


def baseline_reference_rows(score_rows_in: list[dict[str, object]], generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for branch in sorted({str(row["branch"]) for row in score_rows_in}):
        branch_rows = [row for row in score_rows_in if row["branch"] == branch and row["row_type"] == "baseline_sample" and row["evaluation_status"] == "pass"]
        best = min(branch_rows, key=lambda row: float(row["bic_sample"])) if branch_rows else None
        rows.append(
            {
                "branch": branch,
                "baseline_count": len(branch_rows),
                "best_sample_baseline_by_BIC": best["config_id"] if best else "",
                "best_sample_baseline_BIC": best["bic_sample"] if best else "",
                "baseline_status": "sample_only_not_fitted",
                "warning": "baseline sample parameters are not optimized; deltas are sanity readout only",
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG850_0_sample_only",
            "claim": "850 provides fitted cosmology evidence",
            "status": "forbidden",
            "reason": "only sample parameters were evaluated; optimizer_executed=false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG850_1_no_parent_prediction",
            "claim": "fixed b_mem rows are parent predictions",
            "status": "forbidden",
            "reason": "847/849 still leave eta, a_F, DeltaR, and endpoint dynamics open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG850_2_no_model_selection_claim",
            "claim": "sample AIC/BIC decides MTS versus baselines",
            "status": "forbidden",
            "reason": "baselines are not fitted and candidate non-MTS parameters use fixed config values",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG850_3_allowed_sanity_readout",
            "claim": "fixed-bmem candidates can be mechanically evaluated against SN/BAO",
            "status": "allowed_private_nonclaim",
            "reason": "the evaluator writes finite chi-square rows or explicit blockers without running fits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D850_0",
            "finding": "fixed-bmem SN/BAO sample scoring now works",
            "reason": "candidate rows can be injected into M6 and evaluated without fitting b_mem",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D850_1",
            "finding": "readout is only a sanity test",
            "reason": "baseline and candidate nuisance/background parameters are sample values, not optimized under parity",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "read the fixed-bmem SN/BAO sample score and choose between a fair fitted baseline comparator or eta/a_F/DeltaR derivation",
            "include": "rank sanity, failures/blockers, baseline parity decision, parent-amplitude route choice",
            "exclude": "support claim, public evidence, local-GR claim, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(run_result: dict[str, object], generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "added and ran a sample-only fixed-bmem SN/BAO evaluator",
            "evaluator_status": run_result.get("status"),
            "what_is_not_claimed": "fitted evidence, support, parent prediction, model-selection win/loss, local-GR progress",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_valid_for_claim_false(row_groups: list[list[dict[str, object]]]) -> bool:
    for rows in row_groups:
        for row in rows:
            if row.get("valid_for_claim") != "false":
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, object]],
    run_rows: list[dict[str, object]],
    scores: list[dict[str, object]],
    baselines: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_849_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    run_ok = bool(run_rows) and run_rows[0]["status"] == "fixed_bmem_SN_BAO_sample_scores_written_nonclaim"
    row_count_ok = bool(run_rows) and str(run_rows[0]["row_count"]) == "20" and str(run_rows[0]["failure_count"]) == "0"
    no_fit = bool(run_rows) and run_rows[0]["fit_executed"] == "false" and run_rows[0]["optimizer_executed"] == "false"
    baselines_ok = len([row for row in scores if row["row_type"] == "baseline_sample"]) == 6
    candidates_ok = len([row for row in scores if row["row_type"] == "candidate_fixed_bmem"]) == 14
    parent_blocked = len([row for row in scores if row["candidate_id"] == "S3_parent_predicted_placeholder" and row["evaluation_status"] == "blocked"]) == 2
    finite_candidate_scores = all(
        row["chi2_total"] != ""
        for row in scores
        if row["row_type"] == "candidate_fixed_bmem" and row["evaluation_status"] == "pass"
    )
    baseline_refs_ok = len(baselines) == 2 and all(row["baseline_status"] == "sample_only_not_fitted" for row in baselines)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions) and bool(run_rows) and run_rows[0]["claim_allowed"] == "false"
    nonclaim_ok = all_valid_for_claim_false([source_rows, run_rows, scores, baselines, guard_rows, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET

    return [
        {"check_id": "V850_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle"},
        {"check_id": "V850_1_prior_849_clean", "result": "pass" if prior_clean else "fail", "detail": prior_detail},
        {"check_id": "V850_2_evaluator_status_clean", "result": "pass" if run_ok else "fail", "detail": "sample evaluator wrote nonclaim score rows"},
        {"check_id": "V850_3_row_count_and_failures", "result": "pass" if row_count_ok else "fail", "detail": "20 rows expected, failure_count=0"},
        {"check_id": "V850_4_no_fit_or_optimizer", "result": "pass" if no_fit else "fail", "detail": "fit_executed=false and optimizer_executed=false"},
        {"check_id": "V850_5_baseline_rows_present", "result": "pass" if baselines_ok else "fail", "detail": "3 baselines x 2 branches present"},
        {"check_id": "V850_6_candidate_rows_present", "result": "pass" if candidates_ok else "fail", "detail": "7 candidates x 2 branches present"},
        {"check_id": "V850_7_parent_placeholder_blocked", "result": "pass" if parent_blocked else "fail", "detail": "S3 parent-predicted placeholder blocked on both branches"},
        {"check_id": "V850_8_finite_candidate_scores", "result": "pass" if finite_candidate_scores else "fail", "detail": "all pass candidate rows have finite chi2_total"},
        {"check_id": "V850_9_baseline_reference_warning", "result": "pass" if baseline_refs_ok else "fail", "detail": "baseline reference rows explicitly warn sample-only not fitted"},
        {"check_id": "V850_10_claim_allowed_false", "result": "pass" if no_claim else "fail", "detail": "runner and decision rows keep claim_allowed=false"},
        {"check_id": "V850_11_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V850_12_next_target_selected", "result": "pass" if next_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V850_13_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V850_14_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def csv_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(text)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_document(
    source_rows: list[dict[str, object]],
    run_rows: list[dict[str, object]],
    scores: list[dict[str, object]],
    baselines: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    score_view = [
        {
            "branch": row["branch"],
            "row_type": row["row_type"],
            "config_id": row["config_id"],
            "candidate_id": row["candidate_id"],
            "chi2_total": row["chi2_total"],
            "delta_bic_vs_best_sample_baseline": row["delta_bic_vs_best_sample_baseline"],
            "evaluation_status": row["evaluation_status"],
            "valid_for_claim": row["valid_for_claim"],
        }
        for row in scores
    ]
    sections = [
        "# 850 - Y5 R10 Fixed Bmem Cosmology Score Evaluator Dry Run",
        "",
        "Current result: **fixed-`b_mem` SN/BAO sample scoring now runs**. This evaluates candidate amplitudes without fitting `b_mem`, without running an optimizer, and without allowing support language. It is a sanity readout only because the baselines and non-`b_mem` candidate parameters are still sample values rather than fair fitted competitors.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "evaluator_status", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Evaluator Run Result",
        "",
        csv_table(run_rows, ["run_id", "run_dir", "status", "dry_run_only", "sample_score", "no_fit", "fit_executed", "optimizer_executed", "claim_allowed", "row_count", "pass_count", "blocked_count", "failure_count", "valid_for_claim"]),
        "",
        "## Baseline Reference",
        "",
        csv_table(baselines, ["branch", "baseline_count", "best_sample_baseline_by_BIC", "best_sample_baseline_BIC", "baseline_status", "warning", "valid_for_claim"]),
        "",
        "## Sample Score View",
        "",
        csv_table(score_view, ["branch", "row_type", "config_id", "candidate_id", "chi2_total", "delta_bic_vs_best_sample_baseline", "evaluation_status", "valid_for_claim"]),
        "",
        "## Claim Guard",
        "",
        csv_table(guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim"]),
        "",
        "## Decision",
        "",
        csv_table(decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        csv_table(next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
        "## Source Register",
        "",
        csv_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        csv_table(validation, ["check_id", "result", "detail"]),
        "",
    ]
    OUTPUT_DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    source_rows = source_register_rows(generated_utc)
    run_dir, status, stdout = run_evaluator()
    run_rows = run_result_rows(run_dir, status, stdout, generated_utc)
    scores = score_rows(run_dir, generated_utc)
    baselines = baseline_reference_rows(scores, generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(run_rows[0], generated_utc)
    validation = validation_rows(source_rows, run_rows, scores, baselines, guard_rows, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(RUN_RESULT_PATH, run_rows, ["run_id", "run_dir", "status", "dry_run_only", "sample_score", "no_fit", "fit_executed", "optimizer_executed", "claim_allowed", "row_count", "pass_count", "blocked_count", "failure_count", "runner_stdout", "valid_for_claim", "generated_utc"])
    write_csv(SCORE_PATH, scores, ["branch", "row_type", "config_id", "candidate_id", "claim_label", "physics_model", "chi2_sn", "chi2_bao", "chi2_total", "n_data", "effective_k_sample_penalty", "aic_sample", "bic_sample", "delta_chi2_vs_best_sample_baseline", "delta_aic_vs_best_sample_baseline", "delta_bic_vs_best_sample_baseline", "sample_params_json", "evaluation_status", "failure_reason", "fit_executed", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(BASELINE_REFERENCE_PATH, baselines, ["branch", "baseline_count", "best_sample_baseline_by_BIC", "best_sample_baseline_BIC", "baseline_status", "warning", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "evaluator_status", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, run_rows, scores, baselines, guard_rows, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"run_dir={run_dir}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
