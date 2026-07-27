from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
DEFAULT_RUNS = POST_CHECKPOINT / "runs"

REQUIRED_FIELDS = {
    "candidate_id",
    "branch_class",
    "b_mem_mode",
    "b_mem_value_or_range",
    "shape_source",
    "parameter_count_delta",
    "claim_label",
    "execution_eligible_for_input_check",
    "execution_eligible_for_scoring",
    "support_claim_allowed",
    "valid_for_claim",
}

BRANCH_CLASSES = {"null_control", "C0_benchmark", "predeclared_corridor", "parent_predicted"}
B_MEM_MODES = {"zero_control", "benchmark_display_only", "fixed_predeclared", "fixed_parent"}
CLAIM_LABELS = {"benchmark_only", "exploratory_nonclaim", "support_grade_candidate_blocked"}
BOOL_VALUES = {"true", "false"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="No-fit strict cosmology candidate input checker.")
    parser.add_argument("--candidates", required=True, help="Candidate CSV path.")
    parser.add_argument("--dry-run", action="store_true", help="Require dry-run mode.")
    parser.add_argument("--no-fit", action="store_true", help="Require no-fit mode.")
    parser.add_argument("--write-run-dir", action="store_true", help="Write log/status/scorecard/marker outputs.")
    parser.add_argument("--output-root", default=str(DEFAULT_RUNS), help="Run output root.")
    return parser.parse_args()


def resolve_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    candidate = POST_CHECKPOINT / path
    if candidate.exists():
        return candidate
    return Path.cwd() / path


def parse_bool(value: str) -> bool | None:
    lower = str(value).strip().lower()
    if lower == "true":
        return True
    if lower == "false":
        return False
    return None


def validate_candidate(row: dict[str, str], row_number: int) -> dict[str, str]:
    errors: list[str] = []
    warnings: list[str] = []

    missing_fields = sorted(field for field in REQUIRED_FIELDS if field not in row)
    if missing_fields:
        errors.append("missing_fields=" + ";".join(missing_fields))

    candidate_id = row.get("candidate_id", "").strip()
    if not candidate_id:
        errors.append("candidate_id_missing")

    branch_class = row.get("branch_class", "").strip()
    if branch_class not in BRANCH_CLASSES:
        errors.append(f"invalid_branch_class={branch_class}")

    b_mem_mode = row.get("b_mem_mode", "").strip()
    if b_mem_mode not in B_MEM_MODES:
        errors.append(f"invalid_b_mem_mode={b_mem_mode}")

    claim_label = row.get("claim_label", "").strip()
    if claim_label not in CLAIM_LABELS:
        errors.append(f"invalid_claim_label={claim_label}")

    for bool_field in ("execution_eligible_for_input_check", "execution_eligible_for_scoring", "support_claim_allowed", "valid_for_claim"):
        if row.get(bool_field, "").strip().lower() not in BOOL_VALUES:
            errors.append(f"invalid_bool_{bool_field}={row.get(bool_field, '')}")

    support_claim_allowed = parse_bool(row.get("support_claim_allowed", ""))
    valid_for_claim = parse_bool(row.get("valid_for_claim", ""))
    scoring_allowed = parse_bool(row.get("execution_eligible_for_scoring", ""))

    if support_claim_allowed:
        errors.append("support_claim_allowed_true")
    if valid_for_claim:
        errors.append("valid_for_claim_true")

    blocker_text = " ".join(
        str(row.get(field, ""))
        for field in ("b_mem_value_or_range", "eta_assumption", "a_F_DeltaR_assumption", "shape_source", "notes")
    )
    contains_blocker = "MISSING" in blocker_text or "BLOCKED" in blocker_text

    b_mem_numeric = row.get("b_mem_numeric", "").strip()
    numeric_ok = False
    if b_mem_numeric:
        try:
            numeric_value = float(b_mem_numeric)
            numeric_ok = math.isfinite(numeric_value)
            if not numeric_ok:
                errors.append("b_mem_numeric_not_finite")
        except ValueError:
            errors.append(f"b_mem_numeric_not_float={b_mem_numeric}")
    elif scoring_allowed:
        errors.append("scoring_allowed_without_numeric_b_mem")

    if contains_blocker and scoring_allowed:
        errors.append("blocked_candidate_marked_scoring_allowed")
    if contains_blocker and claim_label != "support_grade_candidate_blocked":
        warnings.append("blocker_marker_on_non_support_placeholder")
    if branch_class == "parent_predicted" and not contains_blocker and claim_label != "support_grade_candidate_blocked":
        warnings.append("parent_predicted_row_present_but_not_blocked")

    return {
        "row_number": str(row_number),
        "candidate_id": candidate_id,
        "branch_class": branch_class,
        "b_mem_mode": b_mem_mode,
        "claim_label": claim_label,
        "numeric_b_mem_available": str(numeric_ok).lower(),
        "contains_blocker_marker": str(contains_blocker).lower(),
        "input_check_allowed": row.get("execution_eligible_for_input_check", ""),
        "scoring_allowed_after_user_go_ahead": row.get("execution_eligible_for_scoring", ""),
        "support_claim_allowed": row.get("support_claim_allowed", ""),
        "valid_for_claim": row.get("valid_for_claim", ""),
        "check_status": "fail" if errors else "pass",
        "errors": ";".join(errors),
        "warnings": ";".join(warnings),
    }


def read_candidates(path: Path) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    checks = [validate_candidate(row, index) for index, row in enumerate(rows, start=2)]
    return rows, checks


def make_run_dir(output_root: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{stamp}-strict-cosmology-input-check"
    run_dir.mkdir(parents=True, exist_ok=False)
    return run_dir


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(
    run_dir: Path,
    candidate_path: Path,
    rows: list[dict[str, str]],
    checks: list[dict[str, str]],
    args: argparse.Namespace,
) -> dict[str, object]:
    failures = [check for check in checks if check["check_status"] != "pass"]
    blocked = [check for check in checks if check["contains_blocker_marker"] == "true"]
    scoring_eligible = [check for check in checks if check["scoring_allowed_after_user_go_ahead"] == "true"]
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    status = {
        "status": "input_check_passed_nonclaim" if not failures else "input_check_failed",
        "dry_run_only": bool(args.dry_run),
        "no_fit": bool(args.no_fit),
        "fit_executed": False,
        "claim_allowed": False,
        "candidate_file": str(candidate_path),
        "candidate_count": len(rows),
        "scoring_eligible_count": len(scoring_eligible),
        "blocked_candidate_count": len(blocked),
        "failure_count": len(failures),
        "generated_utc": now,
    }

    scorecard_path = run_dir / "STRICT_BRANCH_SCORECARD.csv"
    write_csv(
        scorecard_path,
        checks,
        [
            "row_number",
            "candidate_id",
            "branch_class",
            "b_mem_mode",
            "claim_label",
            "numeric_b_mem_available",
            "contains_blocker_marker",
            "input_check_allowed",
            "scoring_allowed_after_user_go_ahead",
            "support_claim_allowed",
            "valid_for_claim",
            "check_status",
            "errors",
            "warnings",
        ],
    )

    status_path = run_dir / "status.json"
    status_path.write_text(json.dumps(status, indent=2, sort_keys=True), encoding="utf-8")

    log_lines = [
        "strict cosmology input check",
        f"generated_utc={now}",
        f"candidate_file={candidate_path}",
        f"dry_run_only={args.dry_run}",
        f"no_fit={args.no_fit}",
        "fit_executed=false",
        "claim_allowed=false",
        f"candidate_count={len(rows)}",
        f"scoring_eligible_count={len(scoring_eligible)}",
        f"blocked_candidate_count={len(blocked)}",
        f"failure_count={len(failures)}",
    ]
    for check in checks:
        log_lines.append(
            f"{check['candidate_id']}: {check['check_status']} "
            f"scoring={check['scoring_allowed_after_user_go_ahead']} "
            f"blocked={check['contains_blocker_marker']} "
            f"errors={check['errors']}"
        )
    (run_dir / "log.txt").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    (run_dir / "COMPLETE.marker").write_text(now + "\n", encoding="utf-8")
    return status


def main() -> None:
    args = parse_args()
    candidate_path = resolve_path(args.candidates)
    if not args.dry_run or not args.no_fit:
        raise SystemExit("strict input check requires --dry-run and --no-fit")
    if not candidate_path.exists():
        raise SystemExit(f"missing candidates file: {candidate_path}")

    rows, checks = read_candidates(candidate_path)
    if args.write_run_dir:
        run_dir = make_run_dir(Path(args.output_root))
        status = write_outputs(run_dir, candidate_path, rows, checks, args)
        print(f"run_dir={run_dir}")
        print(f"status={status['status']}")
        print(f"failure_count={status['failure_count']}")
        print(f"claim_allowed={status['claim_allowed']}")
    else:
        failures = [check for check in checks if check["check_status"] != "pass"]
        print(f"candidate_count={len(rows)}")
        print(f"failure_count={len(failures)}")
        print("claim_allowed=false")
        if failures:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
