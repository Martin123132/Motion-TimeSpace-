from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "generic-BAO-manifest-repair-readout"
STATUS = "generic_SN_BAO_runner_BAO_manifest_repaired_dryrun_passes_no_scores"
CLAIM_CEILING = "schema_repair_and_dryrun_only_no_empirical_support_claim"

BLOCKED_RUN = ROOT / "runs" / "20260601-093239-cosmo-SN-BAO-closure-dryrun"
EXPLICIT_PASS_RUN = ROOT / "runs" / "20260601-094538-cosmo-SN-BAO-closure-dryrun"
AUTO_PASS_RUN = ROOT / "runs" / "20260601-094657-cosmo-SN-BAO-closure-dryrun"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "282-empirical-preflight-readout-after-281.md", "pre-repair blocker readout"),
        (ROOT / "scripts" / "cosmo_SN_BAO_closure_runner.py", "generic SN+BAO runner patched to prioritize known Pantheon+/DESI files"),
        (BLOCKED_RUN / "status.json", "pre-repair blocked generic dry-run"),
        (BLOCKED_RUN / "results" / "data_schema_report.csv", "pre-repair schema report"),
        (EXPLICIT_PASS_RUN / "status.json", "explicit-path generic dry-run pass"),
        (EXPLICIT_PASS_RUN / "results" / "data_schema_report.csv", "explicit-path schema report"),
        (AUTO_PASS_RUN / "status.json", "auto-discovery generic dry-run pass after patch"),
        (AUTO_PASS_RUN / "results" / "data_schema_report.csv", "auto-discovery schema report after patch"),
        (ROOT / "scripts" / "generic_BAO_manifest_repair_readout.py", "this readout script"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def run_status_rows() -> list[dict[str, Any]]:
    rows = []
    for label, run in [
        ("before_repair_auto_discovery", BLOCKED_RUN),
        ("explicit_path_validation", EXPLICIT_PASS_RUN),
        ("after_repair_auto_discovery", AUTO_PASS_RUN),
    ]:
        status = read_json(run / "status.json")
        rows.append(
            {
                "run_label": label,
                "run": relpath(run),
                "readout": status["readout"],
                "data_ready_for_short_smoke": status["data_ready_for_short_smoke"],
                "scores_written": status["scores_written"],
                "failures": ";".join(status.get("failures", [])),
                "next_action": status["next_action"],
            }
        )
    return rows


def schema_readout_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for label, run in [
        ("before_repair", BLOCKED_RUN),
        ("explicit_pass", EXPLICIT_PASS_RUN),
        ("auto_pass_after_patch", AUTO_PASS_RUN),
    ]:
        for row in read_csv(run / "results" / "data_schema_report.csv"):
            rows.append(
                {
                    "run_label": label,
                    "dataset": row["dataset"],
                    "explicit_path": row["explicit_path"],
                    "path": row["path"],
                    "row_count": row["row_count"],
                    "columns": row["columns"],
                    "schema_status": row["schema_status"],
                    "issue": row["issue"],
                }
            )
    return rows


def gate_rows() -> list[dict[str, Any]]:
    blocked = read_json(BLOCKED_RUN / "status.json")
    explicit = read_json(EXPLICIT_PASS_RUN / "status.json")
    auto = read_json(AUTO_PASS_RUN / "status.json")
    auto_schema = read_csv(AUTO_PASS_RUN / "results" / "data_schema_report.csv")
    auto_valid_bao = [row for row in auto_schema if row["dataset"] == "BAO_distances" and row["schema_status"] == "schema_valid"]
    return [
        {
            "gate": "pre_repair_failure_reproduced",
            "status": "pass" if "BAO_distance_data_not_validated" in blocked.get("failures", []) else "fail",
            "evidence": ";".join(blocked.get("failures", [])),
            "claim_effect": "confirms original blocker",
        },
        {
            "gate": "explicit_DESI_DR2_paths_validate",
            "status": "pass" if explicit["data_ready_for_short_smoke"] else "fail",
            "evidence": explicit["readout"],
            "claim_effect": "known formalization-workbench data paths are valid",
        },
        {
            "gate": "auto_discovery_prioritizes_DESI",
            "status": "pass" if auto["data_ready_for_short_smoke"] and auto_valid_bao else "fail",
            "evidence": "; ".join(f"{row['row_count']} rows {Path(row['path']).name}" for row in auto_valid_bao),
            "claim_effect": "generic runner no longer blocked by source-intake BAO grids",
        },
        {
            "gate": "scores_generated",
            "status": "fail",
            "evidence": "dry-runs only",
            "claim_effect": "no empirical support claim",
        },
        {
            "gate": "short_smoke_ready",
            "status": "pass" if auto["data_ready_for_short_smoke"] else "fail",
            "evidence": auto["next_action"],
            "claim_effect": "generic short-smoke/no-SH0ES branch can now be attempted with labelled closure limits",
        },
    ]


def next_action_rows() -> list[dict[str, Any]]:
    return [
        {
            "order": 1,
            "action": "run_generic_SN_BAO_short_smoke",
            "reason": "auto-discovered Pantheon+/DESI DR2 data now pass schema",
            "claim_allowed_after": "short-smoke closure score only",
        },
        {
            "order": 2,
            "action": "run_no_SH0ES_shape_branch",
            "reason": "test whether MTS preference survives without local-H0 calibration pressure",
            "claim_allowed_after": "robustness diagnostic only",
        },
        {
            "order": 3,
            "action": "run_DESI_DR1_vs_DR2_release_split",
            "reason": "DESI DR1 and DR2 mean/cov pairs both validate under prioritized manifest",
            "claim_allowed_after": "BAO-release stability diagnostic",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The generic SN+BAO runner blocker is repaired. "
                "Before the patch, auto-discovery latched onto source-intake BAO grid files and failed BAO validation. "
                "Explicit Pantheon+/DESI DR2 paths validated, and after prioritizing known formalization-workbench Pantheon+/DESI files, auto-discovery validates SN, DESI DR2 BAO, and DESI DR1 BAO candidates. "
                "No scores are generated here."
            ),
            "next_target": "generic_SN_BAO_short_smoke_noSH0ES_and_DESI_release_robustness",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "run_status_matrix.csv": (
            run_status_rows(),
            ["run_label", "run", "readout", "data_ready_for_short_smoke", "scores_written", "failures", "next_action"],
        ),
        "schema_readout.csv": (
            schema_readout_rows(),
            ["run_label", "dataset", "explicit_path", "path", "row_count", "columns", "schema_status", "issue"],
        ),
        "gate_results.csv": (gate_rows(), ["gate", "status", "evidence", "claim_effect"]),
        "next_actions.csv": (next_action_rows(), ["order", "action", "reason", "claim_allowed_after"]),
        "decision.csv": (decision_rows(), ["decision", "claim_ceiling", "meaning", "next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    auto = read_json(AUTO_PASS_RUN / "status.json")
    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "generic_SN_BAO_schema_ready": bool(auto["data_ready_for_short_smoke"]),
        "scores_generated": False,
        "empirical_support_claim_allowed": False,
        "runner_patch": "candidate_files_prioritizes_formalization_workbench_Pantheon_DESI_paths",
        "next_target": "generic_SN_BAO_short_smoke_noSH0ES_and_DESI_release_robustness",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generic BAO manifest repair readout.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
