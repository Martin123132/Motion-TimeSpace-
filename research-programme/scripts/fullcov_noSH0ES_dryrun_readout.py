from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "fullcov-noSH0ES-dryrun-readout"
PASS_STATUS = "fullcov_noSH0ES_DR1_DR2_dryruns_pass_score_ready_no_scores_written"
FAIL_STATUS = "fullcov_noSH0ES_DR1_DR2_dryruns_incomplete_no_scores_allowed"
CLAIM_CEILING = "fullcov_noSH0ES_dryrun_only_no_scores_or_stable_evidence"

DR2_DRY_RUN = ROOT / "runs" / "20260601-000137-cosmo-SN-BAO-closure-dryrun"
DR1_DRY_RUN = ROOT / "runs" / "20260601-000138-cosmo-SN-BAO-closure-dryrun"
PRECHECK_RUN = ROOT / "runs" / "20260601-000136-official-likelihood-wrapper-preflight"


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


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def pass_fail(value: bool) -> str:
    return "pass" if value else "fail"


def dry_runs() -> dict[str, Path]:
    return {
        "DESI_DR2_fullcov_noSH0ES": DR2_DRY_RUN,
        "DESI_DR1_fullcov_noSH0ES": DR1_DRY_RUN,
    }


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "313-official-likelihood-wrapper-preflight.md", "preflight checkpoint"),
        (ROOT / "scripts" / "official_likelihood_wrapper_preflight.py", "preflight script"),
        (ROOT / "scripts" / "cosmo_SN_BAO_closure_runner.py", "patched SN+BAO runner"),
        (PRECHECK_RUN / "results" / "dryrun_command_queue.csv", "preflight command queue"),
        (ROOT / "scripts" / "fullcov_noSH0ES_dryrun_readout.py", "this readout script"),
    ]
    for label, run in dry_runs().items():
        sources.extend(
            [
                (run / "status.json", f"{label} dry-run status"),
                (run / "run_config.json", f"{label} dry-run config"),
                (run / "results" / "data_schema_report.csv", f"{label} schema report"),
                (run / "results" / "model_matrix.csv", f"{label} model matrix"),
                (run / "results" / "baseline_fairness.csv", f"{label} baseline fairness"),
                (run / "results" / "output_contract.csv", f"{label} output contract"),
            ]
        )
    return [{"source": relpath(path), "role": role, "exists": yes_no(path.exists())} for path, role in sources]


def dryrun_status_summary_rows() -> list[dict[str, Any]]:
    rows = []
    for label, run in dry_runs().items():
        status = read_json(run / "status.json")
        config = read_json(run / "run_config.json")
        branch = config["requested_branch"]
        rows.append(
            {
                "release_branch": label,
                "run_dir": relpath(run),
                "phase": status["phase"],
                "readout": status["readout"],
                "data_ready_for_short_smoke": status["data_ready_for_short_smoke"],
                "scores_written": status["scores_written"],
                "stable_evidence_allowed": status["stable_evidence_allowed"],
                "failures": "; ".join(status["failures"]),
                "sn_covariance_mode": branch["sn_covariance_mode"],
                "sn_observable": branch["sn_observable"],
                "sn_rows": branch["sn_rows"],
                "include_calibrators": branch["sn_include_calibrators"],
                "bao_label": branch["bao_label"],
            }
        )
    return rows


def schema_summary_rows() -> list[dict[str, Any]]:
    rows = []
    for label, run in dry_runs().items():
        for row in read_csv(run / "results" / "data_schema_report.csv"):
            rows.append(
                {
                    "release_branch": label,
                    "dataset": row["dataset"],
                    "schema_status": row["schema_status"],
                    "exists": row["exists"],
                    "readable": row["readable"],
                    "row_count": row["row_count"],
                    "columns": row["columns"],
                    "sha256": row["sha256"],
                    "issue": row["issue"],
                    "path": row["path"],
                }
            )
    return rows


def model_matrix_check_rows() -> list[dict[str, Any]]:
    expected = {
        "LCDM",
        "wCDM",
        "CPL",
        "MTS_fixed_p3_u3quarter",
        "MTS_fitted_p",
        "MTS_fitted_u3",
        "MTS_Bmem_zero",
    }
    rows = []
    for label, run in dry_runs().items():
        seen = set()
        for row in read_csv(run / "results" / "model_matrix.csv"):
            seen.add(row["model_key"])
            rows.append(
                {
                    "release_branch": label,
                    "model_key": row["model_key"],
                    "role": row["role"],
                    "k_count_dry_run": row["k_count_dry_run"],
                    "claim_ceiling": row["claim_ceiling"],
                    "expected_model_present": yes_no(row["model_key"] in expected),
                }
            )
        for missing in sorted(expected - seen):
            rows.append(
                {
                    "release_branch": label,
                    "model_key": missing,
                    "role": "missing",
                    "k_count_dry_run": "",
                    "claim_ceiling": "",
                    "expected_model_present": "no",
                }
            )
    return rows


def baseline_fairness_check_rows() -> list[dict[str, Any]]:
    rows = []
    for label, run in dry_runs().items():
        for row in read_csv(run / "results" / "baseline_fairness.csv"):
            rows.append(
                {
                    "release_branch": label,
                    "baseline_rule": row["baseline_rule"],
                    "requirement": row["requirement"],
                    "dry_run_status": row["dry_run_status"],
                    "parity_present": yes_no(row["dry_run_status"] == "required_before_scoring"),
                }
            )
    return rows


def runner_patch_check_rows() -> list[dict[str, Any]]:
    runner = ROOT / "scripts" / "cosmo_SN_BAO_closure_runner.py"
    text = runner.read_text(encoding="utf-8")
    configs = {label: read_json(run / "run_config.json") for label, run in dry_runs().items()}
    no_shoes_default = all(not config["requested_branch"]["sn_include_calibrators"] for config in configs.values())
    checks = [
        ("timestamp_arg_supported", '--timestamp' in text and "args.timestamp" in text),
        ("dry_run_timestamp_injection", "def run_dry_run(" in text and "timestamp: str | None = None" in text),
        ("short_smoke_timestamp_injection", "def run_short_smoke(" in text and "timestamp: str | None = None" in text),
        ("include_calibrators_flag_present", "--include-calibrators" in text),
        ("nonexistent_exclude_calibrators_absent", "--exclude-calibrators" not in text),
        ("noSH0ES_default_excludes_calibrators", no_shoes_default),
    ]
    return [
        {
            "check": check,
            "status": pass_fail(ok),
            "evidence": runner.name if check != "noSH0ES_default_excludes_calibrators" else "both run_config.json files set sn_include_calibrators=false",
        }
        for check, ok in checks
    ]


def score_readiness_gate_rows() -> list[dict[str, Any]]:
    sources_ok = all(row["exists"] == "yes" for row in source_register_rows())
    status_rows = dryrun_status_summary_rows()
    schema_rows = schema_summary_rows()
    model_rows = model_matrix_check_rows()
    fairness_rows = baseline_fairness_check_rows()
    runner_checks = runner_patch_check_rows()
    dr2_ready = next(row for row in status_rows if row["release_branch"].startswith("DESI_DR2"))[
        "data_ready_for_short_smoke"
    ] is True
    dr1_ready = next(row for row in status_rows if row["release_branch"].startswith("DESI_DR1"))[
        "data_ready_for_short_smoke"
    ] is True
    no_scores = all(row["scores_written"] is False for row in status_rows)
    sn_cov_ok = all(
        row["schema_status"] == "schema_valid"
        and row["dataset"] == "SN_covariance"
        and row["row_count"] == "1701"
        for row in schema_rows
        if row["dataset"] == "SN_covariance"
    )
    bao_cov_ok = all(
        row["schema_status"] == "schema_valid" and row["dataset"] == "BAO_covariance" for row in schema_rows if row["dataset"] == "BAO_covariance"
    )
    model_set_ok = all(row["expected_model_present"] == "yes" for row in model_rows)
    fairness_ok = len(fairness_rows) >= 10 and all(row["parity_present"] == "yes" for row in fairness_rows)
    patch_ok = all(row["status"] == "pass" for row in runner_checks)
    score_commands_ready = all([sources_ok, patch_ok, dr2_ready, dr1_ready, sn_cov_ok, bao_cov_ok, no_scores, model_set_ok, fairness_ok])
    gates = [
        ("source_paths_exist", sources_ok, "all dry-run, preflight, runner, and readout sources exist"),
        ("runner_timestamp_patch_active", patch_ok, "runner accepts fixed timestamps and no nonexistent exclude-calibrators flag"),
        ("DR2_dryrun_ready", dr2_ready, "DR2 full-cov no-SH0ES dry-run validates data candidates"),
        ("DR1_dryrun_ready", dr1_ready, "DR1 full-cov no-SH0ES dry-run validates data candidates"),
        ("full_SN_cov_schema", sn_cov_ok, "Pantheon+ full covariance validates at 1701 x 1701"),
        ("BAO_cov_schema", bao_cov_ok, "DR2 and DR1 BAO covariance files validate"),
        ("no_scores_written", no_scores, "dry-run phase created no fit scores"),
        ("baseline_parity_present", model_set_ok and fairness_ok, "LCDM/wCDM/CPL and MTS branches share data and nuisance policy"),
        ("stable_evidence_allowed", False, "deliberate fail: dry-run cannot support evidence language"),
        ("score_commands_ready", score_commands_ready, "short-smoke commands are now ready but not executed here"),
    ]
    return [{"gate": gate, "status": pass_fail(ok), "meaning": meaning} for gate, ok, meaning in gates]


def next_score_command_rows() -> list[dict[str, Any]]:
    rows = []
    for label, run, timestamp, max_iter in [
        ("DESI_DR2_fullcov_noSH0ES", DR2_DRY_RUN, "20260601-000140", 180),
        ("DESI_DR1_fullcov_noSH0ES", DR1_DRY_RUN, "20260601-000141", 180),
    ]:
        config = read_json(run / "run_config.json")
        paths = config["explicit_data_paths"]
        command = (
            "& $py $runner --phase short-smoke "
            f"--sn-data '{paths['SN_shape']}' "
            f"--sn-cov '{paths['SN_covariance']}' "
            "--sn-covariance-mode full --sn-observable mb-corr --sn-max-rows 0 "
            f"--bao-data '{paths['BAO_distances']}' "
            f"--bao-cov '{paths['BAO_covariance']}' "
            f"--bao-label {label} "
            "--cpl-w0-lower -4 --cpl-w0-upper 1 --cpl-wa-lower -5 --cpl-wa-upper 5 "
            f"--timestamp '{timestamp}' --max-iter {max_iter}"
        )
        rows.append(
            {
                "release_branch": label,
                "phase": "short-smoke",
                "command": command,
                "expected_run_dir": f"runs/{timestamp}-cosmo-SN-BAO-short-smoke",
                "run_policy": "run_from_VS_Code_terminal_or_Codex_only_when_ready; do_not_wait_hours",
            }
        )
    return rows


def decision_rows(score_ready: bool) -> list[dict[str, Any]]:
    status = PASS_STATUS if score_ready else FAIL_STATUS
    return [
        {"key": "status", "value": status},
        {"key": "claim_ceiling", "value": CLAIM_CEILING},
        {"key": "score_ready", "value": str(score_ready).lower()},
        {"key": "stable_evidence_allowed", "value": "false"},
        {"key": "scores_written", "value": "false"},
        {"key": "next_action", "value": "run_short_smoke_DR2_then_DR1_only_after_acknowledging_no_claim_from_edge_hits"},
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=None)
    args = parser.parse_args()
    timestamp = args.timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    status_rows = dryrun_status_summary_rows()
    schema_rows = schema_summary_rows()
    model_rows = model_matrix_check_rows()
    fairness_rows = baseline_fairness_check_rows()
    patch_rows = runner_patch_check_rows()
    gate_rows = score_readiness_gate_rows()
    command_rows = next_score_command_rows()
    score_ready = next(row for row in gate_rows if row["gate"] == "score_commands_ready")["status"] == "pass"
    status = PASS_STATUS if score_ready else FAIL_STATUS

    write_csv(result_dir / "source_register.csv", source_rows, ["source", "role", "exists"])
    write_csv(
        result_dir / "dryrun_status_summary.csv",
        status_rows,
        [
            "release_branch",
            "run_dir",
            "phase",
            "readout",
            "data_ready_for_short_smoke",
            "scores_written",
            "stable_evidence_allowed",
            "failures",
            "sn_covariance_mode",
            "sn_observable",
            "sn_rows",
            "include_calibrators",
            "bao_label",
        ],
    )
    write_csv(
        result_dir / "schema_summary.csv",
        schema_rows,
        ["release_branch", "dataset", "schema_status", "exists", "readable", "row_count", "columns", "sha256", "issue", "path"],
    )
    write_csv(
        result_dir / "model_matrix_check.csv",
        model_rows,
        ["release_branch", "model_key", "role", "k_count_dry_run", "claim_ceiling", "expected_model_present"],
    )
    write_csv(
        result_dir / "baseline_fairness_check.csv",
        fairness_rows,
        ["release_branch", "baseline_rule", "requirement", "dry_run_status", "parity_present"],
    )
    write_csv(result_dir / "runner_patch_check.csv", patch_rows, ["check", "status", "evidence"])
    write_csv(result_dir / "score_readiness_gates.csv", gate_rows, ["gate", "status", "meaning"])
    write_csv(
        result_dir / "next_score_commands.csv",
        command_rows,
        ["release_branch", "phase", "command", "expected_run_dir", "run_policy"],
    )
    write_csv(result_dir / "decision.csv", decision_rows(score_ready), ["key", "value"])

    payload = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": status,
        "claim_ceiling": CLAIM_CEILING,
        "score_ready": score_ready,
        "stable_evidence_allowed": False,
        "scores_written": False,
        "dry_run_branches": list(dry_runs().keys()),
        "next_action": "run short-smoke DR2 then DR1; still no stable evidence language from dry-run",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "COMPLETE.txt").write_text(status + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
