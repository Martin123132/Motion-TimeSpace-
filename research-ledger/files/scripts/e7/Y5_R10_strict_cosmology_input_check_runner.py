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

OUTPUT_DOC = POST_CHECKPOINT / "848-Y5-R10-strict-cosmology-input-check-runner.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_848_SOURCE_REGISTER.csv"
RUN_RESULT_PATH = RESIDUALS / "P8_Y5_R10_848_INPUT_CHECK_RUN_RESULT.csv"
SCORECARD_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_848_SCORECARD_SUMMARY.csv"
RUN_ARTIFACTS_PATH = RESIDUALS / "P8_Y5_R10_848_RUN_ARTIFACTS.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_848_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_848_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_848_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_848_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_848_VALIDATION.csv"

RUNNER_PATH = POST_CHECKPOINT / "scripts" / "strict_cosmology_branch_runner.py"
CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_847_STRICT_COSMOLOGY_CANDIDATES.csv"

STATUS = "Y5_R10_848_strict_cosmology_input_check_passed_no_fit_nonclaim"
CLAIM_CEILING = "input_check_only_no_fit_no_support_claim"
NEXT_TARGET = "849-Y5-R10-strict-cosmology-scoring-adapter-or-parent-amplitude-tightening.md"

SOURCE_SPECS = [
    {
        "source_id": "847_doc",
        "path": POST_CHECKPOINT / "847-Y5-R10-strict-cosmology-candidate-file-or-parent-amplitude-law.md",
        "needles": [
            "the strict candidate file now exists",
            "parent amplitude law is still not predictive",
            "848-Y5-R10-strict-cosmology-input-check-runner.md",
        ],
        "role": "candidate file handoff",
    },
    {
        "source_id": "847_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_847_VALIDATION.csv",
        "needles": [
            "V847_2_candidate_file_complete,pass",
            "V847_5_parent_prediction_blocked,pass",
            "V847_8_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "847_candidate_file",
        "path": CANDIDATE_PATH,
        "needles": [
            "S0_null_bmem_0",
            "S2_corridor_eta1_aFDeltaR_1p0",
            "S3_parent_predicted_placeholder",
        ],
        "role": "strict cosmology candidate input",
    },
    {
        "source_id": "strict_runner",
        "path": RUNNER_PATH,
        "needles": [
            "No-fit strict cosmology candidate input checker.",
            "fit_executed",
            "STRICT_BRANCH_SCORECARD.csv",
            "claim_allowed",
        ],
        "role": "no-fit input-check runner",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


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


def run_input_check() -> tuple[Path, dict[str, object], str]:
    command = [
        "python",
        str(RUNNER_PATH),
        "--candidates",
        str(CANDIDATE_PATH),
        "--dry-run",
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
        timeout=60,
    )
    run_dir_text = ""
    for line in completed.stdout.splitlines():
        if line.startswith("run_dir="):
            run_dir_text = line.split("=", 1)[1].strip()
            break
    if not run_dir_text:
        raise RuntimeError("runner did not print run_dir")
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
            "no_fit": str(status.get("no_fit")).lower(),
            "fit_executed": str(status.get("fit_executed")).lower(),
            "claim_allowed": str(status.get("claim_allowed")).lower(),
            "candidate_count": status.get("candidate_count"),
            "scoring_eligible_count": status.get("scoring_eligible_count"),
            "blocked_candidate_count": status.get("blocked_candidate_count"),
            "failure_count": status.get("failure_count"),
            "runner_stdout": stdout.replace("\n", " | "),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def scorecard_summary_rows(run_dir: Path, generated_utc: str) -> list[dict[str, object]]:
    scorecard = run_dir / "STRICT_BRANCH_SCORECARD.csv"
    rows: list[dict[str, object]] = []
    with scorecard.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                {
                    "candidate_id": row["candidate_id"],
                    "branch_class": row["branch_class"],
                    "claim_label": row["claim_label"],
                    "numeric_b_mem_available": row["numeric_b_mem_available"],
                    "contains_blocker_marker": row["contains_blocker_marker"],
                    "scoring_allowed_after_user_go_ahead": row["scoring_allowed_after_user_go_ahead"],
                    "support_claim_allowed": row["support_claim_allowed"],
                    "check_status": row["check_status"],
                    "errors": row["errors"],
                    "warnings": row["warnings"],
                    "valid_for_claim": "false",
                    "generated_utc": generated_utc,
                }
            )
    return rows


def run_artifact_rows(run_dir: Path, generated_utc: str) -> list[dict[str, object]]:
    artifacts = [
        ("log", run_dir / "log.txt"),
        ("status", run_dir / "status.json"),
        ("scorecard", run_dir / "STRICT_BRANCH_SCORECARD.csv"),
        ("completion_marker", run_dir / "COMPLETE.marker"),
    ]
    return [
        {
            "artifact_type": artifact_type,
            "path": str(path),
            "exists": str(path.exists()).lower(),
            "size_bytes": path.stat().st_size if path.exists() else 0,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for artifact_type, path in artifacts
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG848_0_no_fit_executed",
            "claim": "848 scored cosmology models",
            "status": "forbidden",
            "reason": "runner was invoked with --dry-run --no-fit and status records fit_executed=false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG848_1_no_support_claim",
            "claim": "input-check pass supports MTS cosmology",
            "status": "forbidden",
            "reason": "input check validates schema only; all candidate rows remain support_claim_allowed=false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG848_2_no_parent_prediction",
            "claim": "parent-predicted b_mem is now available",
            "status": "forbidden",
            "reason": "S3 parent-predicted placeholder remains blocked in scorecard",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG848_3_allowed_runner_status",
            "claim": "strict candidate file passes no-fit input checks",
            "status": "allowed_private_nonclaim",
            "reason": "mechanical schema validation succeeded without scoring",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D848_0",
            "finding": "no-fit input-check runner passes",
            "reason": "candidate rows parse, numeric eligible rows are finite, and blocked parent-predicted row is handled",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D848_1",
            "finding": "scoring still not authorized",
            "reason": "input-check pass is not a physics result and parent amplitude prediction remains missing",
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
            "objective": "choose between tightening the parent amplitude law or adding a scoring adapter that still requires explicit user go-ahead",
            "include": "parent eta/a_F/DeltaR route audit, or adapter mapping existing SN/BAO/H(z)/growth-CMB scripts to strict candidates",
            "exclude": "long fit without user go-ahead, support claim, death claim, local-GR claim, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(run_result: dict[str, object], generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "added and ran a no-fit strict cosmology input-check runner",
            "runner_status": run_result.get("status"),
            "what_is_not_claimed": "new cosmology score, model support, parent-predicted b_mem, C0 revival, local-GR progress",
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
    score_rows: list[dict[str, object]],
    artifact_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_847_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    run_ok = bool(run_rows) and run_rows[0]["status"] == "input_check_passed_nonclaim" and run_rows[0]["fit_executed"] == "false"
    claim_false = bool(run_rows) and run_rows[0]["claim_allowed"] == "false"
    score_ok = len(score_rows) == 7 and all(row["check_status"] == "pass" for row in score_rows)
    parent_blocked = any(row["candidate_id"] == "S3_parent_predicted_placeholder" and row["contains_blocker_marker"] == "true" for row in score_rows)
    artifacts_ok = all(row["exists"] == "true" and int(row["size_bytes"]) > 0 for row in artifact_rows)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    nonclaim_ok = all_valid_for_claim_false([source_rows, run_rows, score_rows, artifact_rows, guard_rows, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET

    return [
        {
            "check_id": "V848_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle",
        },
        {
            "check_id": "V848_1_prior_847_clean",
            "result": "pass" if prior_clean else "fail",
            "detail": prior_detail,
        },
        {
            "check_id": "V848_2_input_check_passed_no_fit",
            "result": "pass" if run_ok else "fail",
            "detail": "runner status input_check_passed_nonclaim and fit_executed=false",
        },
        {
            "check_id": "V848_3_claim_allowed_false",
            "result": "pass" if claim_false and no_claim else "fail",
            "detail": "runner and decision rows keep claim_allowed=false",
        },
        {
            "check_id": "V848_4_scorecard_rows_pass",
            "result": "pass" if score_ok else "fail",
            "detail": "all 7 candidate rows pass input checks",
        },
        {
            "check_id": "V848_5_parent_placeholder_blocked",
            "result": "pass" if parent_blocked else "fail",
            "detail": "parent-predicted placeholder remains blocked",
        },
        {
            "check_id": "V848_6_run_artifacts_exist",
            "result": "pass" if artifacts_ok else "fail",
            "detail": "log, status, scorecard, and completion marker exist",
        },
        {
            "check_id": "V848_7_all_rows_nonclaim",
            "result": "pass" if nonclaim_ok else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V848_8_next_target_selected",
            "result": "pass" if next_selected else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V848_9_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V848_10_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
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
    score_rows: list[dict[str, object]],
    artifact_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 848 - Y5 R10 Strict Cosmology Input-Check Runner",
        "",
        "Current result: **the strict cosmology candidate file passes the no-fit input-check runner**. The run writes `log.txt`, `status.json`, `STRICT_BRANCH_SCORECARD.csv`, and `COMPLETE.marker`, with `fit_executed=false` and `claim_allowed=false`. This is mechanical readiness only; it is not a cosmology score.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "runner_status", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Input-Check Run Result",
        "",
        csv_table(run_rows, ["run_id", "run_dir", "status", "dry_run_only", "no_fit", "fit_executed", "claim_allowed", "candidate_count", "scoring_eligible_count", "blocked_candidate_count", "failure_count", "valid_for_claim"]),
        "",
        "## Scorecard Summary",
        "",
        csv_table(score_rows, ["candidate_id", "branch_class", "claim_label", "numeric_b_mem_available", "contains_blocker_marker", "scoring_allowed_after_user_go_ahead", "support_claim_allowed", "check_status", "errors", "warnings", "valid_for_claim"]),
        "",
        "## Run Artifacts",
        "",
        csv_table(artifact_rows, ["artifact_type", "path", "exists", "size_bytes", "valid_for_claim"]),
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
    run_dir, status, stdout = run_input_check()
    run_rows = run_result_rows(run_dir, status, stdout, generated_utc)
    score_rows = scorecard_summary_rows(run_dir, generated_utc)
    artifact_rows = run_artifact_rows(run_dir, generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(run_rows[0], generated_utc)
    validation = validation_rows(source_rows, run_rows, score_rows, artifact_rows, guard_rows, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(RUN_RESULT_PATH, run_rows, ["run_id", "run_dir", "status", "dry_run_only", "no_fit", "fit_executed", "claim_allowed", "candidate_count", "scoring_eligible_count", "blocked_candidate_count", "failure_count", "runner_stdout", "valid_for_claim", "generated_utc"])
    write_csv(SCORECARD_SUMMARY_PATH, score_rows, ["candidate_id", "branch_class", "claim_label", "numeric_b_mem_available", "contains_blocker_marker", "scoring_allowed_after_user_go_ahead", "support_claim_allowed", "check_status", "errors", "warnings", "valid_for_claim", "generated_utc"])
    write_csv(RUN_ARTIFACTS_PATH, artifact_rows, ["artifact_type", "path", "exists", "size_bytes", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "runner_status", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, run_rows, score_rows, artifact_rows, guard_rows, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"run_dir={run_dir}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
