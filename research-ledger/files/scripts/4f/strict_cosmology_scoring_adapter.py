from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
DEFAULT_CANDIDATES = POST_CHECKPOINT / "source-intake" / "mts_residuals" / "P8_Y5_R10_847_STRICT_COSMOLOGY_CANDIDATES.csv"
DEFAULT_RUNS = POST_CHECKPOINT / "runs"

ARENAS = [
    {
        "arena": "SN_BAO_background",
        "reference_script": FORMALIZATION / "scripts" / "cosmology_likelihood_smoke.py",
        "reference_command": (
            "powershell -ExecutionPolicy Bypass -File "
            + str(FORMALIZATION / "scripts" / "run_cosmology_robustness_smoke_R1.ps1")
        ),
        "baseline_parity": "LambdaCDM,wCDM,CPL same Pantheon+/DESI branch",
        "adapter_gap": "existing runner fits/varies M6; strict fixed-b_mem candidate injection is not wired yet",
    },
    {
        "arena": "Hz_chronometer_covariance",
        "reference_script": FORMALIZATION / "scripts" / "Hz_covariance_likelihood_smoke.py",
        "reference_command": (
            "python "
            + str(FORMALIZATION / "scripts" / "Hz_covariance_likelihood_smoke.py")
            + " --out-dir <post-checkpoint-run-dir>"
        ),
        "baseline_parity": "M0,wCDM,CPL and fixed-shape MTS on the same 15-row covariance branch",
        "adapter_gap": "script reads a prior fit table; strict candidate rows need a generated candidate fit-table or wrapper",
    },
    {
        "arena": "growth_CMB_radflat",
        "reference_script": FORMALIZATION / "scripts" / "joint_growth_CMB_radflat_readout.py",
        "reference_command": (
            "python "
            + str(FORMALIZATION / "scripts" / "joint_growth_CMB_radflat_readout.py")
            + " --out-dir <post-checkpoint-run-dir>"
        ),
        "baseline_parity": "LCDM,wCDM,CPL/C0 radflat readout with same growth and compressed CMB inputs",
        "adapter_gap": "current readout consumes previous radflat branches; strict fixed-b_mem candidate rows need injection",
    },
    {
        "arena": "full_joint_radflat_reference",
        "reference_script": FORMALIZATION / "scripts" / "full_joint_radflat_phenomenology_fit.py",
        "reference_command": (
            "python "
            + str(FORMALIZATION / "scripts" / "full_joint_radflat_phenomenology_fit.py")
            + " --out-dir <post-checkpoint-run-dir>"
        ),
        "baseline_parity": "reference only; joint fit cannot be used as a no-fit parent prediction",
        "adapter_gap": "phenomenology fit is not a strict no-fit score; use only as demoted reference unless wrapped",
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dry-run strict cosmology scoring adapter planner.")
    parser.add_argument("--candidates", default=str(DEFAULT_CANDIDATES), help="Strict candidate CSV path.")
    parser.add_argument("--dry-run", action="store_true", help="Require dry-run mode.")
    parser.add_argument("--no-fit", action="store_true", help="Require no-fit mode.")
    parser.add_argument("--write-run-dir", action="store_true", help="Write log/status/command-plan/marker outputs.")
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


def read_candidates(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def bool_text(value: str) -> bool:
    return str(value).strip().lower() == "true"


def make_run_dir(output_root: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{stamp}-strict-cosmology-scoring-adapter-dry-run"
    run_dir.mkdir(parents=True, exist_ok=False)
    return run_dir


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def candidate_blocked(row: dict[str, str]) -> bool:
    joined = " ".join(
        str(row.get(field, ""))
        for field in ("b_mem_value_or_range", "b_mem_numeric", "eta_assumption", "a_F_DeltaR_assumption", "shape_source", "notes")
    )
    return "MISSING" in joined or "BLOCKED" in joined or not bool_text(row.get("execution_eligible_for_scoring", "false"))


def command_plan_rows(candidates: list[dict[str, str]], generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for candidate in candidates:
        blocked = candidate_blocked(candidate)
        for arena in ARENAS:
            reference_script = Path(arena["reference_script"])
            if blocked:
                adapter_status = "blocked_candidate_or_parent_prediction"
                blocker = "candidate_not_scoring_eligible_or_parent_prediction_missing"
                needed_adapter_change = "none_until_candidate_unblocked"
            else:
                adapter_status = "dry_run_plan_ready_but_scoring_adapter_not_executable"
                blocker = "requires_fixed_b_mem_candidate_injection_wrapper_before_scoring"
                needed_adapter_change = arena["adapter_gap"]
            rows.append(
                {
                    "candidate_id": candidate.get("candidate_id", ""),
                    "branch_class": candidate.get("branch_class", ""),
                    "claim_label": candidate.get("claim_label", ""),
                    "b_mem_numeric": candidate.get("b_mem_numeric", ""),
                    "arena": arena["arena"],
                    "reference_script": str(reference_script),
                    "reference_exists": str(reference_script.exists()).lower(),
                    "baseline_parity": arena["baseline_parity"],
                    "reference_command": arena["reference_command"],
                    "adapter_status": adapter_status,
                    "blocker": blocker,
                    "needed_adapter_change": needed_adapter_change,
                    "run_authorized": "false",
                    "fit_executed": "false",
                    "claim_allowed": "false",
                    "valid_for_claim": "false",
                    "generated_utc": generated_utc,
                }
            )
    return rows


def write_outputs(run_dir: Path, candidate_path: Path, candidates: list[dict[str, str]], args: argparse.Namespace) -> dict[str, object]:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    plan_rows = command_plan_rows(candidates, generated_utc)
    blocked_rows = [row for row in plan_rows if row["adapter_status"] == "blocked_candidate_or_parent_prediction"]
    executable_rows = [row for row in plan_rows if row["run_authorized"] == "true"]
    missing_references = [row for row in plan_rows if row["reference_exists"] != "true"]
    status = {
        "status": "adapter_dry_run_passed_blocked_for_scoring" if not missing_references else "adapter_dry_run_failed_missing_reference",
        "dry_run_only": bool(args.dry_run),
        "no_fit": bool(args.no_fit),
        "fit_executed": False,
        "claim_allowed": False,
        "candidate_file": str(candidate_path),
        "candidate_count": len(candidates),
        "arena_count": len(ARENAS),
        "command_plan_row_count": len(plan_rows),
        "blocked_plan_row_count": len(blocked_rows),
        "run_authorized_row_count": len(executable_rows),
        "missing_reference_count": len(missing_references),
        "generated_utc": generated_utc,
    }

    plan_path = run_dir / "STRICT_COSMOLOGY_COMMAND_PLAN.csv"
    write_csv(
        plan_path,
        plan_rows,
        [
            "candidate_id",
            "branch_class",
            "claim_label",
            "b_mem_numeric",
            "arena",
            "reference_script",
            "reference_exists",
            "baseline_parity",
            "reference_command",
            "adapter_status",
            "blocker",
            "needed_adapter_change",
            "run_authorized",
            "fit_executed",
            "claim_allowed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    (run_dir / "status.json").write_text(json.dumps(status, indent=2, sort_keys=True), encoding="utf-8")
    log_lines = [
        "strict cosmology scoring adapter dry-run",
        f"generated_utc={generated_utc}",
        f"candidate_file={candidate_path}",
        f"dry_run_only={args.dry_run}",
        f"no_fit={args.no_fit}",
        "fit_executed=false",
        "claim_allowed=false",
        f"candidate_count={len(candidates)}",
        f"arena_count={len(ARENAS)}",
        f"command_plan_row_count={len(plan_rows)}",
        f"blocked_plan_row_count={len(blocked_rows)}",
        f"run_authorized_row_count={len(executable_rows)}",
        f"missing_reference_count={len(missing_references)}",
    ]
    for row in plan_rows:
        log_lines.append(
            f"{row['candidate_id']}::{row['arena']}: {row['adapter_status']} "
            f"authorized={row['run_authorized']} blocker={row['blocker']}"
        )
    (run_dir / "log.txt").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    (run_dir / "COMPLETE.marker").write_text(generated_utc + "\n", encoding="utf-8")
    return status


def main() -> None:
    args = parse_args()
    if not args.dry_run or not args.no_fit:
        raise SystemExit("strict scoring adapter requires --dry-run and --no-fit")
    candidate_path = resolve_path(args.candidates)
    if not candidate_path.exists():
        raise SystemExit(f"missing candidates file: {candidate_path}")
    candidates = read_candidates(candidate_path)
    if args.write_run_dir:
        run_dir = make_run_dir(Path(args.output_root))
        status = write_outputs(run_dir, candidate_path, candidates, args)
        print(f"run_dir={run_dir}")
        print(f"status={status['status']}")
        print(f"command_plan_row_count={status['command_plan_row_count']}")
        print(f"run_authorized_row_count={status['run_authorized_row_count']}")
        print(f"claim_allowed={status['claim_allowed']}")
    else:
        print(f"candidate_count={len(candidates)}")
        print(f"arena_count={len(ARENAS)}")
        print("fit_executed=false")
        print("claim_allowed=false")


if __name__ == "__main__":
    main()
