#!/usr/bin/env python3
"""Build the readiness ledger for the canonical_R_closure T0 dry-run."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RUNS_ROOT = POST_CHECKPOINT / "runs"

SOURCE_CHECKPOINTS = [
    POST_CHECKPOINT / "98-canonical-R-closure-scorecard-plan.md",
    POST_CHECKPOINT / "scripts" / "cosmo_SN_BAO_closure_runner.py",
    POST_CHECKPOINT / "scripts" / "canonical_R_closure_scorecard_plan.py",
]

EXPECTED_ARTIFACTS = [
    ("status.json", "dry-run", True),
    ("run_config.json", "dry-run", True),
    ("results/model_matrix.csv", "dry-run", True),
    ("results/amplitude_policy.csv", "dry-run", True),
    ("results/baseline_fairness.csv", "dry-run", True),
    ("results/data_schema_report.csv", "dry-run", True),
    ("results/output_contract.csv", "dry-run", True),
    ("results/fit_summary.csv", "short-smoke", False),
    ("results/baseline_comparison.csv", "short-smoke", False),
    ("results/residuals.csv", "short-smoke", False),
    ("results/prior_edge_table.csv", "short-smoke", False),
]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def latest_dry_run() -> Path:
    candidates = sorted(RUNS_ROOT.glob("*-cosmo-SN-BAO-closure-dryrun"), key=lambda item: item.name)
    if not candidates:
        raise FileNotFoundError("No cosmo-SN-BAO closure dry-run directories found.")
    return candidates[-1]


def source_rows(dry_run_dir: Path) -> list[dict[str, Any]]:
    rows = [
        {
            "source": str(path),
            "exists": path.exists(),
            "role": {
                "98-canonical-R-closure-scorecard-plan.md": "scorecard plan and T0/T1 gate definitions",
                "cosmo_SN_BAO_closure_runner.py": "dry-run and short-smoke runner",
                "canonical_R_closure_scorecard_plan.py": "scorecard-plan artifact generator",
            }[path.name],
        }
        for path in SOURCE_CHECKPOINTS
    ]
    rows.extend(
        [
            {"source": str(dry_run_dir), "exists": dry_run_dir.exists(), "role": "strict T0 dry-run directory"},
            {"source": str(dry_run_dir / "status.json"), "exists": (dry_run_dir / "status.json").exists(), "role": "T0 status payload"},
            {"source": str(dry_run_dir / "run_config.json"), "exists": (dry_run_dir / "run_config.json").exists(), "role": "T0 frozen config"},
            {
                "source": str(dry_run_dir / "results" / "data_schema_report.csv"),
                "exists": (dry_run_dir / "results" / "data_schema_report.csv").exists(),
                "role": "T0 data shape report",
            },
        ]
    )
    return rows


def artifact_rows(dry_run_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for relative, phase, should_exist in EXPECTED_ARTIFACTS:
        path = dry_run_dir / relative
        rows.append(
            {
                "artifact": relative,
                "path": str(path),
                "phase": phase,
                "expected_now": should_exist,
                "exists": path.exists(),
                "gate_pass": path.exists() == should_exist,
            }
        )
    return rows


def data_shape_rows(data_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    expected_counts = {
        "SN_shape": 1701,
        "SN_covariance": 1701,
        "BAO_distances": 13,
        "BAO_covariance": 13,
    }
    output: list[dict[str, Any]] = []
    for row in data_rows:
        dataset = row["dataset"]
        row_count = int(row["row_count"] or 0)
        expected_count = expected_counts.get(dataset, "")
        gate_pass = (
            row["exists"] == "True"
            and row["readable"] == "True"
            and row["schema_status"] == "schema_valid"
            and (expected_count == "" or row_count == expected_count)
        )
        output.append(
            {
                "dataset": dataset,
                "path": row["path"],
                "exists": row["exists"],
                "readable": row["readable"],
                "row_count": row_count,
                "expected_count": expected_count,
                "schema_status": row["schema_status"],
                "issue": row["issue"],
                "gate_pass": gate_pass,
            }
        )
    return output


def command_string(status: dict[str, Any], config: dict[str, Any]) -> str:
    branch = config.get("requested_branch", {})
    paths = config.get("explicit_data_paths", {})
    python = POST_CHECKPOINT / ".venv-score" / "Scripts" / "python.exe"
    runner = Path(status["script"])
    sn_rows = branch.get("sn_max_rows")
    sn_max_rows = 0 if sn_rows is None else sn_rows
    return (
        f'& "{python}" "{runner}" --phase dry-run '
        f'--sn-observable {branch.get("sn_observable", "")} '
        f'--sn-covariance-mode {branch.get("sn_covariance_mode", "")} '
        f'--sn-max-rows {sn_max_rows} '
        f'--bao-label {branch.get("bao_label", "")} '
        f'--sn-data "{paths.get("SN_shape", "")}" '
        f'--sn-cov "{paths.get("SN_covariance", "")}" '
        f'--bao-data "{paths.get("BAO_distances", "")}" '
        f'--bao-cov "{paths.get("BAO_covariance", "")}"'
    )


def command_safety_rows(dry_run_dir: Path, status: dict[str, Any], config: dict[str, Any]) -> list[dict[str, Any]]:
    branch = config.get("requested_branch", {})
    paths = config.get("explicit_data_paths", {})
    expected = {
        "phase": ("dry-run", config.get("phase")),
        "scores_allowed": (False, config.get("scores_allowed")),
        "status_scores_written": (False, status.get("scores_written")),
        "sn_observable": ("mb-corr", branch.get("sn_observable")),
        "sn_covariance_mode": ("full", branch.get("sn_covariance_mode")),
        "sn_max_rows": (None, branch.get("sn_max_rows")),
        "sn_rows": ("full", branch.get("sn_rows")),
        "sn_include_calibrators": (False, branch.get("sn_include_calibrators")),
        "bao_label": ("DESI_DR2_primary", branch.get("bao_label")),
        "fit_summary_absent": (False, (dry_run_dir / "results" / "fit_summary.csv").exists()),
    }
    rows = [
        {
            "check": name,
            "expected": expected_value,
            "observed": observed_value,
            "gate_pass": expected_value == observed_value,
        }
        for name, (expected_value, observed_value) in expected.items()
    ]
    for label, raw_path in paths.items():
        path = Path(raw_path) if raw_path else None
        rows.append(
            {
                "check": f"explicit_path_exists:{label}",
                "expected": True,
                "observed": bool(path and path.exists()),
                "gate_pass": bool(path and path.exists()),
            }
        )
    rows.append(
        {
            "check": "strict_command_reconstructable",
            "expected": True,
            "observed": command_string(status, config),
            "gate_pass": True,
        }
    )
    return rows


def readiness_gate_rows(
    source_table: list[dict[str, Any]],
    artifacts: list[dict[str, Any]],
    shapes: list[dict[str, Any]],
    command_checks: list[dict[str, Any]],
    status: dict[str, Any],
    config: dict[str, Any],
) -> list[dict[str, Any]]:
    model_keys = {row.get("model_key") for row in config.get("models", [])}
    required_models = {"LCDM", "wCDM", "CPL", "MTS_fixed_p3_u3quarter", "MTS_Bmem_zero"}
    gates = [
        {
            "gate": "sources_exist",
            "gate_pass": all(row["exists"] for row in source_table),
            "notes": "all checkpoint and dry-run source paths resolve",
            "blocks_fit": True,
        },
        {
            "gate": "dryrun_artifacts_match_contract",
            "gate_pass": all(row["gate_pass"] for row in artifacts),
            "notes": "dry-run artifacts exist and scoring artifacts are absent",
            "blocks_fit": True,
        },
        {
            "gate": "data_shapes_pass",
            "gate_pass": all(row["gate_pass"] for row in shapes),
            "notes": "SN shape, SN covariance, DESI DR2 BAO mean, and BAO covariance validate",
            "blocks_fit": True,
        },
        {
            "gate": "command_branch_frozen",
            "gate_pass": all(row["gate_pass"] for row in command_checks if row["check"] != "strict_command_reconstructable"),
            "notes": "mb-corr, full covariance, full sample, no calibrators, and DESI DR2 are recorded",
            "blocks_fit": True,
        },
        {
            "gate": "status_allows_next_smoke",
            "gate_pass": status.get("data_ready_for_short_smoke") is True and status.get("failures") == [],
            "notes": str(status.get("readout", "")),
            "blocks_fit": True,
        },
        {
            "gate": "models_declared",
            "gate_pass": required_models <= model_keys,
            "notes": ";".join(sorted(model_keys)),
            "blocks_fit": True,
        },
        {
            "gate": "claim_ceiling_enforced",
            "gate_pass": config.get("scores_allowed") is False and status.get("stable_evidence_allowed") is False,
            "notes": "empirical closure only; no stable evidence language from T0",
            "blocks_fit": False,
        },
    ]
    return gates


def decision_rows(gates: list[dict[str, Any]], status: dict[str, Any]) -> list[dict[str, Any]]:
    blocking_failures = [row["gate"] for row in gates if row["blocks_fit"] and not row["gate_pass"]]
    verdict = "T0_dry_run_passed_primary_fit_not_started" if not blocking_failures else "T0_failed_fix_config_or_data_before_fit"
    return [
        {"decision": "verdict", "value": verdict},
        {"decision": "blocking_failures", "value": ";".join(blocking_failures)},
        {"decision": "dry_run_readout", "value": status.get("readout", "")},
        {"decision": "scores_written", "value": status.get("scores_written", False)},
        {"decision": "claim_ceiling", "value": "empirical_closure_scorecard_only"},
        {"decision": "next_target", "value": "launch_T1_clean_primary_fullcov_short_smoke_when_compute_time_is_available" if not blocking_failures else "repair_T0_before_any_fit"},
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run-dir", type=Path, default=None)
    args = parser.parse_args()

    dry_run_dir = args.dry_run_dir or latest_dry_run()
    status = read_json(dry_run_dir / "status.json")
    config = read_json(dry_run_dir / "run_config.json")
    data_rows = read_csv(dry_run_dir / "results" / "data_schema_report.csv")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{timestamp}-canonical-R-closure-dryrun-readiness"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_table = source_rows(dry_run_dir)
    artifacts = artifact_rows(dry_run_dir)
    shapes = data_shape_rows(data_rows)
    command_checks = command_safety_rows(dry_run_dir, status, config)
    gates = readiness_gate_rows(source_table, artifacts, shapes, command_checks, status, config)
    decisions = decision_rows(gates, status)

    write_csv(results_dir / "source_checkpoint_register.csv", source_table, ["source", "exists", "role"])
    write_csv(results_dir / "dryrun_artifact_register.csv", artifacts, ["artifact", "path", "phase", "expected_now", "exists", "gate_pass"])
    write_csv(results_dir / "data_shape_checks.csv", shapes, ["dataset", "path", "exists", "readable", "row_count", "expected_count", "schema_status", "issue", "gate_pass"])
    write_csv(results_dir / "command_safety_checks.csv", command_checks, ["check", "expected", "observed", "gate_pass"])
    write_csv(results_dir / "readiness_gates.csv", gates, ["gate", "gate_pass", "notes", "blocks_fit"])
    write_csv(results_dir / "decision.csv", decisions, ["decision", "value"])

    verdict = next(row["value"] for row in decisions if row["decision"] == "verdict")
    status_payload = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "dry_run_dir": str(dry_run_dir),
        "readout": verdict,
        "scores_written": False,
        "long_fit_started": False,
        "blocking_failures": [row["gate"] for row in gates if row["blocks_fit"] and not row["gate_pass"]],
        "next_action": next(row["value"] for row in decisions if row["decision"] == "next_target"),
    }
    (run_dir / "status.json").write_text(json.dumps(status_payload, indent=2), encoding="utf-8")
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()
