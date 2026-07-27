from __future__ import annotations

import csv
import json
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
RUNS = POST_CHECKPOINT / "runs"

OUTPUT_DOC = POST_CHECKPOINT / "852-Y5-R10-fair-fixed-bmem-SN-BAO-fitted-comparator-dry-run.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_852_SOURCE_REGISTER.csv"
RUN_RESULT_PATH = RESIDUALS / "P8_Y5_R10_852_FITTED_COMPARATOR_RUN_RESULT.csv"
SCORE_PATH = RESIDUALS / "P8_Y5_R10_852_FAIR_FIXED_BMEM_SN_BAO_FIT_SCORES.csv"
READOUT_PATH = RESIDUALS / "P8_Y5_R10_852_FIT_READOUT.csv"
NULL_PARITY_PATH = RESIDUALS / "P8_Y5_R10_852_NULL_CONTROL_PARITY.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_852_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_852_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_852_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_852_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_852_VALIDATION.csv"

CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_847_STRICT_COSMOLOGY_CANDIDATES.csv"
COMPARATOR_PATH = POST_CHECKPOINT / "scripts" / "strict_fixed_bmem_SN_BAO_fitted_comparator.py"
CONFIG_PATH = FORMALIZATION / "configs" / "cosmology_background_R1_current.json"

STATUS = "Y5_R10_852_fair_fixed_bmem_SN_BAO_short_fit_complete_nonclaim"
CLAIM_CEILING = "short_fitted_comparator_only_no_support_no_parent_prediction"
NEXT_TARGET = "853-Y5-R10-fixed-bmem-fitted-readout-or-projection-repair.md"

SOURCE_SPECS = [
    {
        "source_id": "851_doc",
        "path": POST_CHECKPOINT / "851-Y5-R10-fixed-bmem-SN-BAO-readout-and-eta-law-choice.md",
        "needles": [
            "fair fixed-`b_mem` fitted comparator",
            "852-Y5-R10-fair-fixed-bmem-SN-BAO-fitted-comparator-dry-run.md",
        ],
        "role": "route choice handoff",
    },
    {
        "source_id": "851_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_851_VALIDATION.csv",
        "needles": [
            "V851_5_route_selected,pass",
            "V851_8_next_target_selected,pass",
            "V851_9_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "852_comparator_script",
        "path": COMPARATOR_PATH,
        "needles": [
            "Short fair SN/BAO fitted comparator with b_mem fixed.",
            "FAIR_FIXED_BMEM_SN_BAO_FIT_SCORES.csv",
            "b_mem_fit_executed",
        ],
        "role": "new short fitted comparator",
    },
    {
        "source_id": "847_candidates",
        "path": CANDIDATE_PATH,
        "needles": ["S0_null_bmem_0", "S2_corridor_eta1_aFDeltaR_1p0", "S3_parent_predicted_placeholder"],
        "role": "strict fixed-bmem candidate rows",
    },
    {
        "source_id": "R1_cosmology_config",
        "path": CONFIG_PATH,
        "needles": ["R1_current_background", "\"id\": \"M6\"", "PantheonPlusSH0ES", "DESI_DR2_BAO"],
        "role": "SN/BAO data and sample-parameter config",
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


def finite_float(value: object) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def fmt(value: object) -> str:
    number = finite_float(value)
    return "" if number is None else f"{number:.12g}"


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


def run_comparator() -> tuple[Path, dict[str, object], str]:
    command = [
        "python",
        str(COMPARATOR_PATH),
        "--candidates",
        str(CANDIDATE_PATH),
        "--config",
        str(CONFIG_PATH),
        "--branches",
        "sh0es",
        "no_sh0es",
        "--integration-steps",
        "1024",
        "--maxiter",
        "80",
        "--starts",
        "2",
        "--short-fit",
        "--no-bmem-fit",
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
        timeout=240,
    )
    run_dir_text = ""
    for line in completed.stdout.splitlines():
        if line.startswith("run_dir="):
            run_dir_text = line.split("=", 1)[1].strip()
            break
    if not run_dir_text:
        raise RuntimeError("comparator did not print run_dir")
    run_dir = Path(run_dir_text)
    status = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    return run_dir, status, completed.stdout


def run_result_rows(run_dir: Path, status: dict[str, object], stdout: str, generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "run_id": run_dir.name,
            "run_dir": str(run_dir),
            "status": status.get("status"),
            "short_fit": str(status.get("short_fit")).lower(),
            "fit_executed": str(status.get("fit_executed")).lower(),
            "b_mem_fit_executed": str(status.get("b_mem_fit_executed")).lower(),
            "claim_allowed": str(status.get("claim_allowed")).lower(),
            "integration_steps": status.get("integration_steps"),
            "maxiter": status.get("maxiter"),
            "starts": status.get("starts"),
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
    rows: list[dict[str, object]] = []
    for row in read_csv(run_dir / "FAIR_FIXED_BMEM_SN_BAO_FIT_SCORES.csv"):
        rows.append({**row, "valid_for_claim": "false", "generated_utc": generated_utc})
    return rows


def best_fit_baseline(scores: list[dict[str, object]], branch: str) -> dict[str, object]:
    rows = [
        row
        for row in scores
        if row["branch"] == branch and row["row_type"] == "baseline_fit" and row["evaluation_status"] == "pass"
    ]
    return min(rows, key=lambda row: float(row["bic"]))


def readout_rows(scores: list[dict[str, object]], generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for branch in sorted({str(row["branch"]) for row in scores}):
        baseline = best_fit_baseline(scores, branch)
        candidates = [
            row
            for row in scores
            if row["branch"] == branch and row["row_type"] == "candidate_fixed_bmem_fit" and row["evaluation_status"] == "pass"
        ]
        best_candidate = min(candidates, key=lambda row: float(row["delta_bic_vs_best_fit_baseline"]))
        positives = [row for row in candidates if finite_float(row["b_mem_fixed"]) not in (None, 0.0)]
        best_positive = min(positives, key=lambda row: float(row["delta_bic_vs_best_fit_baseline"]))
        edge_count = sum(1 for row in candidates + [baseline] if str(row.get("edge_flags", "")))
        rows.append(
            {
                "branch": branch,
                "best_fit_baseline": baseline["config_id"],
                "best_fit_baseline_BIC": baseline["bic"],
                "best_candidate": best_candidate["candidate_id"],
                "best_candidate_delta_BIC": best_candidate["delta_bic_vs_best_fit_baseline"],
                "best_positive_candidate": best_positive["candidate_id"],
                "best_positive_delta_BIC": best_positive["delta_bic_vs_best_fit_baseline"],
                "edge_flagged_row_count": edge_count,
                "readout": "fair_comparator_completed_nonclaim",
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def null_parity_rows(scores: list[dict[str, object]], generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for branch in sorted({str(row["branch"]) for row in scores}):
        m0 = next(row for row in scores if row["branch"] == branch and row["config_id"] == "M0_fit_fair")
        null = next(row for row in scores if row["branch"] == branch and row["candidate_id"] == "S0_null_bmem_0")
        delta_chi2 = float(null["chi2_total"]) - float(m0["chi2_total"]) if null["evaluation_status"] == "pass" and m0["evaluation_status"] == "pass" else math.nan
        rows.append(
            {
                "branch": branch,
                "M0_chi2": m0["chi2_total"],
                "null_M6_chi2": null["chi2_total"],
                "null_minus_M0_chi2": fmt(delta_chi2),
                "parity_status": "numerically_close" if abs(delta_chi2) < 1.0e-2 else "not_identical_optimizer_or_model_difference",
                "interpretation": "b_mem=0 M6 should reduce to M0 when shared parameters are fitted",
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG852_0_no_parent_prediction",
            "claim": "fitted fixed-bmem rows are parent-predicted amplitudes",
            "status": "forbidden",
            "reason": "b_mem values remain candidate/benchmark/corridor rows, not derived eta/a_F/DeltaR values",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG852_1_no_bmem_fit",
            "claim": "b_mem was fitted by 852",
            "status": "forbidden",
            "reason": "comparator excludes b_mem from all fit_param_names",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG852_2_no_support_or_death",
            "claim": "852 decides support or death",
            "status": "forbidden",
            "reason": "short fit is a private branch diagnostic; full robustness and parent derivation remain open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG852_3_allowed_comparator",
            "claim": "fair fixed-bmem SN/BAO short comparator has run",
            "status": "allowed_private_nonclaim",
            "reason": "baselines and fixed-bmem candidates were fitted under the same SN/BAO data branch with b_mem fixed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(readouts: list[dict[str, object]], generated_utc: str) -> list[dict[str, object]]:
    worst_positive = max(float(row["best_positive_delta_BIC"]) for row in readouts)
    best_positive = min(float(row["best_positive_delta_BIC"]) for row in readouts)
    if best_positive > 10.0:
        decision = "positive_fixed_bmem_not_competitive_in_short_SN_BAO_fit"
        next_reason = "repair projection/BAO shape or revisit sign/amplitude before deriving a positive eta law"
    else:
        decision = "positive_fixed_bmem_remains_competitive_enough_for_parent_amplitude_work"
        next_reason = "feed the preferred fixed amplitude back into eta/a_F/DeltaR derivation"
    return [
        {
            "decision_id": "D852_0",
            "finding": decision,
            "reason": f"best positive candidate delta_BIC range across branches is {best_positive:.6g} to {worst_positive:.6g}",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D852_1",
            "finding": "next step chosen from fair comparator",
            "reason": next_reason,
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
            "objective": "decide whether fitted fixed-bmem results require projection repair, sign/amplitude revision, or renewed eta/a_F/DeltaR derivation",
            "include": "read fitted deltas, inspect BAO residual pressure, check null-control parity, select derivation or repair route",
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
            "what_changed": "ran a short fair SN/BAO fitted comparator with b_mem fixed",
            "comparator_status": run_result.get("status"),
            "what_is_not_claimed": "support, death, parent prediction, public evidence, local-GR progress",
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
    readouts: list[dict[str, object]],
    null_rows: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_851_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    run_ok = bool(run_rows) and run_rows[0]["status"] == "fair_fixed_bmem_SN_BAO_short_fit_written_nonclaim"
    row_count_ok = bool(run_rows) and str(run_rows[0]["row_count"]) == "20" and str(run_rows[0]["failure_count"]) == "0"
    no_bmem_fit = all("b_mem" not in str(row["fit_param_names"]).split(";") for row in scores if row["evaluation_status"] == "pass")
    baselines_ok = len([row for row in scores if row["row_type"] == "baseline_fit"]) == 6
    candidates_ok = len([row for row in scores if row["row_type"] == "candidate_fixed_bmem_fit"]) == 14
    parent_blocked = len([row for row in scores if row["candidate_id"] == "S3_parent_predicted_placeholder" and row["evaluation_status"] == "blocked"]) == 2
    readout_ok = len(readouts) == 2 and all(row["readout"] == "fair_comparator_completed_nonclaim" for row in readouts)
    null_ok = len(null_rows) == 2 and all(row["parity_status"] == "numerically_close" for row in null_rows)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions) and bool(run_rows) and run_rows[0]["claim_allowed"] == "false"
    nonclaim_ok = all_valid_for_claim_false([source_rows, run_rows, scores, readouts, null_rows, guards, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET
    return [
        {"check_id": "V852_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle"},
        {"check_id": "V852_1_prior_851_clean", "result": "pass" if prior_clean else "fail", "detail": prior_detail},
        {"check_id": "V852_2_run_status_clean", "result": "pass" if run_ok else "fail", "detail": "short fair comparator completed without fit failures"},
        {"check_id": "V852_3_row_count_and_failures", "result": "pass" if row_count_ok else "fail", "detail": "20 rows expected, failure_count=0"},
        {"check_id": "V852_4_no_bmem_fit", "result": "pass" if no_bmem_fit else "fail", "detail": "no passing fit_param_names include b_mem"},
        {"check_id": "V852_5_baseline_rows_present", "result": "pass" if baselines_ok else "fail", "detail": "3 baselines x 2 branches present"},
        {"check_id": "V852_6_candidate_rows_present", "result": "pass" if candidates_ok else "fail", "detail": "7 candidates x 2 branches present"},
        {"check_id": "V852_7_parent_placeholder_blocked", "result": "pass" if parent_blocked else "fail", "detail": "S3 parent-predicted placeholder blocked on both branches"},
        {"check_id": "V852_8_readouts_present", "result": "pass" if readout_ok else "fail", "detail": "branch readouts generated"},
        {"check_id": "V852_9_null_control_parity", "result": "pass" if null_ok else "fail", "detail": "b_mem=0 M6 tracks M0 after fair refit"},
        {"check_id": "V852_10_claim_allowed_false", "result": "pass" if no_claim else "fail", "detail": "runner and decision rows keep claim_allowed=false"},
        {"check_id": "V852_11_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V852_12_next_target_selected", "result": "pass" if next_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V852_13_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V852_14_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
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
    readouts: list[dict[str, object]],
    null_rows: list[dict[str, object]],
    guards: list[dict[str, object]],
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
            "delta_bic_vs_best_fit_baseline": row["delta_bic_vs_best_fit_baseline"],
            "edge_flags": row["edge_flags"],
            "evaluation_status": row["evaluation_status"],
            "valid_for_claim": row["valid_for_claim"],
        }
        for row in scores
    ]
    sections = [
        "# 852 - Y5 R10 Fair Fixed Bmem SN BAO Fitted Comparator Dry Run",
        "",
        "Current result: **a short fair SN/BAO fitted comparator has run with `b_mem` fixed**. Baselines and fixed-`b_mem` M6 candidates were refit over shared background/nuisance parameters, while `b_mem` itself was not fitted. This is still private nonclaim evidence: it can diagnose projection pressure, but it cannot prove support or death without parent-amplitude and robustness gates.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "comparator_status", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Run Result",
        "",
        csv_table(run_rows, ["run_id", "run_dir", "status", "short_fit", "fit_executed", "b_mem_fit_executed", "claim_allowed", "integration_steps", "maxiter", "starts", "row_count", "pass_count", "blocked_count", "failure_count", "valid_for_claim"]),
        "",
        "## Branch Readout",
        "",
        csv_table(readouts, ["branch", "best_fit_baseline", "best_candidate", "best_candidate_delta_BIC", "best_positive_candidate", "best_positive_delta_BIC", "edge_flagged_row_count", "readout", "valid_for_claim"]),
        "",
        "## Null Control Parity",
        "",
        csv_table(null_rows, ["branch", "M0_chi2", "null_M6_chi2", "null_minus_M0_chi2", "parity_status", "interpretation", "valid_for_claim"]),
        "",
        "## Score View",
        "",
        csv_table(score_view, ["branch", "row_type", "config_id", "candidate_id", "chi2_total", "delta_bic_vs_best_fit_baseline", "edge_flags", "evaluation_status", "valid_for_claim"]),
        "",
        "## Claim Guard",
        "",
        csv_table(guards, ["guard_id", "claim", "status", "reason", "valid_for_claim"]),
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
    run_dir, status, stdout = run_comparator()
    run_rows = run_result_rows(run_dir, status, stdout, generated_utc)
    scores = score_rows(run_dir, generated_utc)
    readouts = readout_rows(scores, generated_utc)
    null_rows = null_parity_rows(scores, generated_utc)
    guards = claim_guard_rows(generated_utc)
    decisions = decision_rows(readouts, generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(run_rows[0], generated_utc)
    validation = validation_rows(source_rows, run_rows, scores, readouts, null_rows, guards, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(RUN_RESULT_PATH, run_rows, ["run_id", "run_dir", "status", "short_fit", "fit_executed", "b_mem_fit_executed", "claim_allowed", "integration_steps", "maxiter", "starts", "row_count", "pass_count", "blocked_count", "failure_count", "runner_stdout", "valid_for_claim", "generated_utc"])
    write_csv(SCORE_PATH, scores, ["branch", "row_type", "config_id", "candidate_id", "claim_label", "physics_model", "b_mem_fixed", "fit_param_names", "effective_k_with_selection_penalty", "chi2_sn", "chi2_bao", "chi2_total", "n_data", "aic", "bic", "delta_chi2_vs_best_fit_baseline", "delta_aic_vs_best_fit_baseline", "delta_bic_vs_best_fit_baseline", "params_json", "edge_flags", "success", "message", "evaluation_status", "fit_executed", "b_mem_fit_executed", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(READOUT_PATH, readouts, ["branch", "best_fit_baseline", "best_fit_baseline_BIC", "best_candidate", "best_candidate_delta_BIC", "best_positive_candidate", "best_positive_delta_BIC", "edge_flagged_row_count", "readout", "valid_for_claim", "generated_utc"])
    write_csv(NULL_PARITY_PATH, null_rows, ["branch", "M0_chi2", "null_M6_chi2", "null_minus_M0_chi2", "parity_status", "interpretation", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guards, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "comparator_status", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, run_rows, scores, readouts, null_rows, guards, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"run_dir={run_dir}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
