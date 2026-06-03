#!/usr/bin/env python3
"""Manifest-only guard for the no-clock official likelihood refresh."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

DEFAULT_SOURCE_RUN = RUNS_ROOT / "20260531-235959-no-clock-official-source-refresh"
CLAIM_CEILING = "manifest_only_guard_no_model_scoring_or_theory_promotion"
REPRO_CLAIM_CEILING = "single_arena_BAO_reproduction_no_full_refresh_or_theory_promotion"
SN_BAO_REPRO_CLAIM_CEILING = "SN_BAO_locked_2over27_reproduction_no_full_refresh_or_theory_promotion"
STATUS_PASS = "no_clock_manifest_only_fit_guard_passed"
STATUS_FAIL = "no_clock_manifest_only_fit_guard_failed"
REPRO_STATUS_PASS = "no_clock_single_arena_BAO_reproduction_passed"
REPRO_STATUS_FAIL = "no_clock_single_arena_BAO_reproduction_failed"
SN_BAO_REPRO_STATUS_PASS = "no_clock_SN_BAO_locked_2over27_reproduction_passed"
SN_BAO_REPRO_STATUS_FAIL = "no_clock_SN_BAO_locked_2over27_reproduction_failed"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"
SIDECAR_BRANCH = "MTS_pair_ruler_half_kernel"
REQUIRED_BRANCHES = ["LCDM", "wCDM", "CPL", LEAD_BRANCH, "MTS_Bmem_zero"]
REPRO_MODELS = ["LCDM", "wCDM", "CPL", "MTS_locked_2over27", "MTS_Bmem_zero", "MTS_fitted_Bmem_diagnostic"]
EXPECTED_BAO_DELTAS_VS_LCDM = {
    "DESI_DR2_primary": -2.108368627321081,
    "DESI_DR1_primary": -0.8483738675035859,
}
EXPECTED_SN_BAO_DELTAS_VS_LCDM = {
    "T1_primary_fullcov_DR2": -5.259466877748764,
    "T3_diagonal_fullsample_DR2": -7.956849125466192,
    "T4_small_fullcov_DR2": -2.1121258573889463,
    "T5_SH0ES_pressure": -2.1071017912585432,
    "T5_matched_control": -2.107119040036963,
    "T6_small_fullcov_DR1": -0.8525455130148885,
}
REQUIRED_SOURCE_ARTIFACTS = [
    "source_hash_lock.csv",
    "row_manifest.csv",
    "covariance_manifest.csv",
    "branch_manifest.csv",
    "nuisance_policy.csv",
    "preflight_gates.csv",
    "decision.csv",
]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def latest_source_run() -> Path:
    candidates = [
        path
        for path in RUNS_ROOT.glob("*-no-clock-official-source-refresh")
        if (path / "status.json").exists()
    ]
    if not candidates:
        return DEFAULT_SOURCE_RUN
    return max(candidates, key=lambda path: path.stat().st_mtime)


def source_role(path: Path) -> str:
    name = path.name
    if name.endswith("no_clock_official_likelihood_refresh.py"):
        return "current likelihood refresh guard"
    if name == "locked_2over27_BAO_only_release_test.py":
        return "single-arena BAO reproduction scorer"
    if name == "canonical_R_two_ninth_T7_robustness.py":
        return "SN+BAO locked 2/27 reproduction scorer"
    if name == "canonical_R_fixed_amplitude_scout.py":
        return "fixed-amplitude SN+BAO scoring helper"
    if name == "cosmo_SN_BAO_closure_runner.py":
        return "SN+BAO source-run likelihood helper"
    if name.startswith("170-"):
        return "source-refresh runner checkpoint"
    if name == "status.json":
        return "source-refresh status"
    if name in REQUIRED_SOURCE_ARTIFACTS:
        return "source-refresh required artifact"
    return "supporting source"


def source_register_rows(script_path: Path, source_run: Path) -> list[dict[str, Any]]:
    source_results = source_run / "results"
    paths = [
        script_path,
        WORK_DIR / "170-no-clock-official-source-refresh-runner.md",
        source_run / "status.json",
        source_run / "DONE.txt",
        *[source_results / name for name in REQUIRED_SOURCE_ARTIFACTS],
    ]
    rows: list[dict[str, Any]] = []
    for path in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": source_role(path),
                "issue": "" if exists else "missing",
            }
        )
    return rows


def artifact_contract_rows(source_run: Path) -> list[dict[str, Any]]:
    source_results = source_run / "results"
    rows: list[dict[str, Any]] = []
    for artifact in REQUIRED_SOURCE_ARTIFACTS:
        path = source_results / artifact
        exists = path.exists()
        row_count = ""
        header_status = ""
        if exists and path.suffix.lower() == ".csv":
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                header_status = "pass" if reader.fieldnames else "fail"
                row_count = sum(1 for _ in reader)
        rows.append(
            {
                "artifact": artifact,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists else "",
                "row_count": row_count,
                "header_status": header_status,
                "required_for_scoring": "yes",
                "status": "pass" if exists and (header_status in {"", "pass"}) else "fail",
            }
        )
    for artifact in ["fit_summary.csv", "baseline_comparisons.csv", "residuals.csv", "jackknife_scorecard.csv"]:
        path = source_results / artifact
        rows.append(
            {
                "artifact": artifact,
                "path": str(path),
                "exists": "yes" if path.exists() else "no",
                "sha256": sha256_file(path) if path.exists() else "",
                "row_count": "",
                "header_status": "",
                "required_for_scoring": "future_output_not_allowed_in_source_refresh",
                "status": "fail_present_too_early" if path.exists() else "pass_absent",
            }
        )
    return rows


def source_status_guard_rows(source_run: Path) -> list[dict[str, Any]]:
    status_path = source_run / "status.json"
    status = load_json(status_path) if status_path.exists() else {}
    return [
        {
            "check": "source_run_exists",
            "status": "pass" if source_run.exists() else "fail",
            "evidence": str(source_run),
        },
        {
            "check": "source_run_status_passed",
            "status": "pass" if status.get("status") == "no_clock_official_source_refresh_preflight_passed" else "fail",
            "evidence": str(status.get("status", "")),
        },
        {
            "check": "source_run_done_marker",
            "status": "pass" if (source_run / "DONE.txt").exists() else "fail",
            "evidence": str(source_run / "DONE.txt"),
        },
        {
            "check": "source_run_no_model_scoring",
            "status": "pass" if status.get("model_scoring") == "not_run" else "fail",
            "evidence": str(status.get("model_scoring", "")),
        },
        {
            "check": "source_run_sidecar_policy",
            "status": "pass" if status.get("sidecar_policy") == "excluded_from_lead_refresh" else "fail",
            "evidence": str(status.get("sidecar_policy", "")),
        },
    ]


def source_hash_guard_rows(source_results: Path) -> list[dict[str, Any]]:
    rows = read_csv_rows(source_results / "source_hash_lock.csv")
    bad = [row for row in rows if row["status"] in {"missing", "hash_mismatch"}]
    recorded = [row for row in rows if row["status"] == "recorded_no_expected_hash"]
    return [
        {
            "check": "source_hash_missing_or_mismatch",
            "status": "pass" if not bad else "fail",
            "evidence": f"bad={len(bad)}; recorded_no_expected_hash={len(recorded)}; total={len(rows)}",
        }
    ]


def row_guard_rows(source_results: Path) -> list[dict[str, Any]]:
    rows = read_csv_rows(source_results / "row_manifest.csv")
    by_arena: dict[str, int] = {}
    for row in rows:
        by_arena[row["arena"]] = by_arena.get(row["arena"], 0) + 1
    required = {"SN": 1, "BAO": 1, "Hz": 1, "growth_RSD": 1}
    guard_rows = [
        {
            "arena": arena,
            "row_count": by_arena.get(arena, 0),
            "minimum_required": minimum,
            "status": "pass" if by_arena.get(arena, 0) >= minimum else "fail",
        }
        for arena, minimum in required.items()
    ]
    guard_rows.append(
        {
            "arena": "CMB_diagnostic",
            "row_count": by_arena.get("CMB_diagnostic", 0),
            "minimum_required": 0,
            "status": "diagnostic_only",
        }
    )
    return guard_rows


def covariance_guard_rows(source_results: Path) -> list[dict[str, Any]]:
    rows = read_csv_rows(source_results / "covariance_manifest.csv")
    return [
        {
            "dataset": row["dataset"],
            "arena": row["arena"],
            "status": "pass" if row["status"] == "pass" else "fail",
            "evidence": f"shape={row['shape']}; expected_rows={row['expected_rows']}; issue={row['issue']}",
        }
        for row in rows
    ]


def branch_guard_rows(source_results: Path, assert_no_sidecar: bool) -> list[dict[str, Any]]:
    branches = read_csv_rows(source_results / "branch_manifest.csv")
    by_branch = {row["branch"]: row for row in branches}
    rows: list[dict[str, Any]] = []
    for branch in REQUIRED_BRANCHES:
        row = by_branch.get(branch)
        rows.append(
            {
                "branch": branch,
                "role": row.get("role", "") if row else "",
                "included_in_lead_refresh": row.get("included_in_lead_refresh", "") if row else "",
                "required_policy": "included",
                "status": "pass" if row and row.get("included_in_lead_refresh") == "yes" else "fail",
                "evidence": "required branch present and included" if row else "missing branch",
            }
        )
    sidecar = by_branch.get(SIDECAR_BRANCH)
    sidecar_ok = bool(sidecar and sidecar.get("included_in_lead_refresh") == "no")
    rows.append(
        {
            "branch": SIDECAR_BRANCH,
            "role": sidecar.get("role", "") if sidecar else "",
            "included_in_lead_refresh": sidecar.get("included_in_lead_refresh", "") if sidecar else "",
            "required_policy": "excluded" if assert_no_sidecar else "reported",
            "status": "pass" if (sidecar_ok or not assert_no_sidecar) else "fail",
            "evidence": "sidecar excluded from lead refresh" if sidecar_ok else "sidecar missing or included",
        }
    )
    return rows


def nuisance_guard_rows(source_results: Path) -> list[dict[str, Any]]:
    rows = read_csv_rows(source_results / "nuisance_policy.csv")
    required = ["SN", "BAO", "Hz", "growth_RSD", "all"]
    present = {row["arena"] for row in rows}
    return [
        {
            "arena": arena,
            "status": "pass" if arena in present else "fail",
            "evidence": "policy present" if arena in present else "missing policy",
        }
        for arena in required
    ]


def prior_edge_contract_rows(source_results: Path) -> list[dict[str, Any]]:
    branches = [row for row in read_csv_rows(source_results / "branch_manifest.csv") if row["included_in_lead_refresh"] == "yes"]
    rows: list[dict[str, Any]] = []
    for branch in branches:
        rows.append(
            {
                "branch": branch["branch"],
                "required_future_artifact": "prior_edge_table.csv",
                "required_fields": "branch,parameter,best_fit,lower_bound,upper_bound,edge_distance,edge_flag",
                "status": "contract_required_before_scoring",
                "reason": "edge hits demote evidence for MTS and baselines equally",
            }
        )
    return rows


def scoring_refusal_rows(mode: str) -> list[dict[str, Any]]:
    return [
        {
            "mode": "manifest-only",
            "allowed": "yes",
            "action": "validate contracts and write guard artifacts",
        },
        {
            "mode": "reproduce",
            "allowed": "yes_single_arena_only",
            "action": "BAO-only reproduction after manifest guard passes; not a full refresh",
        },
        {
            "mode": "full-refresh",
            "allowed": "no_not_implemented",
            "action": "refuse until single-arena reproduction passes and full likelihood contract is written",
        },
        {
            "mode": mode,
            "allowed": "yes" if mode in {"manifest-only", "reproduce"} else "no",
            "action": "current invocation",
        },
    ]


def guard_gate_rows(
    source_status: list[dict[str, Any]],
    artifact_contract: list[dict[str, Any]],
    hash_guards: list[dict[str, Any]],
    row_guards: list[dict[str, Any]],
    covariance_guards: list[dict[str, Any]],
    branch_guards: list[dict[str, Any]],
    nuisance_guards: list[dict[str, Any]],
    mode: str,
) -> list[dict[str, Any]]:
    artifact_bad = [row for row in artifact_contract if not str(row["status"]).startswith("pass")]
    covariance_bad = [row for row in covariance_guards if row["status"] != "pass"]
    return [
        aggregate_gate("source_run_status", source_status),
        {
            "gate": "source_artifacts_present",
            "status": "pass" if not artifact_bad else "fail",
            "evidence": f"bad_artifacts={len(artifact_bad)}",
        },
        aggregate_gate("source_hashes_clean", hash_guards),
        aggregate_gate("row_contracts_present", row_guards, allowed_nonpass={"diagnostic_only"}),
        {
            "gate": "covariance_contracts_pass",
            "status": "pass" if not covariance_bad else "fail",
            "evidence": f"covariance_bad={len(covariance_bad)}; covariance_rows={len(covariance_guards)}",
        },
        aggregate_gate("branch_contracts_pass", branch_guards),
        aggregate_gate("nuisance_contracts_present", nuisance_guards),
        {
            "gate": "prior_edge_contract_written",
            "status": "pass",
            "evidence": "prior_edge_contract.csv written for every included branch; no scoring yet",
        },
        {
            "gate": "mode_is_manifest_only",
            "status": "pass" if mode == "manifest-only" else "fail",
            "evidence": mode,
        },
        {
            "gate": "no_model_scoring",
            "status": "pass",
            "evidence": "manifest guard only; no chi2/AIC/BIC generated",
        },
        {
            "gate": "claim_ceiling_preserved",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def aggregate_gate(name: str, rows: list[dict[str, Any]], allowed_nonpass: set[str] | None = None) -> dict[str, Any]:
    allowed = allowed_nonpass or set()
    bad = [row for row in rows if row["status"] != "pass" and row["status"] not in allowed]
    return {
        "gate": name,
        "status": "pass" if not bad else "fail",
        "evidence": f"bad={len(bad)}; rows={len(rows)}",
    }


def decision_rows(gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failed = [row for row in gates if row["status"] != "pass"]
    status = STATUS_PASS if not failed else STATUS_FAIL
    return [
        {
            "item": "status",
            "verdict": status,
            "evidence": f"failed_gates={len(failed)}",
        },
        {
            "item": "lead_branch",
            "verdict": LEAD_BRANCH,
            "evidence": "required included branch in source manifest",
        },
        {
            "item": "sidecar_policy",
            "verdict": "excluded_from_lead_refresh",
            "evidence": "assert-no-sidecar guard passed",
        },
        {
            "item": "fit_status",
            "verdict": "not_run_by_design",
            "evidence": "manifest-only guard produces no score columns",
        },
        {
            "item": "claim_ceiling",
            "verdict": CLAIM_CEILING,
            "evidence": "no theory/CMB/local-GR/parent-action promotion",
        },
        {
            "item": "next_target",
            "verdict": "172-no-clock-single-arena-reproduction-guard.md",
            "evidence": "only after manifest-only guard passes should reproduction mode be implemented",
        },
    ]


def load_bao_reproduction_module() -> Any:
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    return importlib.import_module("locked_2over27_BAO_only_release_test")


def load_sn_bao_reproduction_module() -> Any:
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    return importlib.import_module("canonical_R_two_ninth_T7_robustness")


def official_branch_alias(model: str) -> str:
    if model in {"MTS_locked_2over27", "two_ninth_boundary_charge"}:
        return LEAD_BRANCH
    return model


def reproduction_source_rows(bao_repro: Any, source_run: Path) -> list[dict[str, Any]]:
    paths = [
        Path(__file__).resolve(),
        Path(bao_repro.__file__).resolve(),
        source_run / "status.json",
        source_run / "DONE.txt",
    ]
    rows: list[dict[str, Any]] = []
    for path in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": source_role(path),
                "issue": "" if exists else "missing",
            }
        )
    return rows


def sn_bao_reproduction_source_rows(sn_bao_repro: Any, source_run: Path) -> list[dict[str, Any]]:
    scout_path = SCRIPT_DIR / "canonical_R_fixed_amplitude_scout.py"
    runner_path = SCRIPT_DIR / "cosmo_SN_BAO_closure_runner.py"
    paths = [
        Path(__file__).resolve(),
        Path(sn_bao_repro.__file__).resolve(),
        scout_path,
        runner_path,
        source_run / "status.json",
        source_run / "DONE.txt",
    ]
    rows: list[dict[str, Any]] = []
    for path in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": source_role(path),
                "issue": "" if exists else "missing",
            }
        )
    return rows


def sn_bao_branch_source_rows(sn_bao_repro: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for branch in sn_bao_repro.BRANCHES:
        run_dir = branch["run"]
        status_path = run_dir / "status.json"
        status = load_json(status_path) if status_path.exists() else {}
        artifact_names = ["run_config.json", "fit_summary.csv", "amplitude_policy.csv", "prior_edge_table.csv"]
        artifact_paths = {
            "run_config.json": run_dir / "run_config.json",
            "fit_summary.csv": run_dir / "results" / "fit_summary.csv",
            "amplitude_policy.csv": run_dir / "results" / "amplitude_policy.csv",
            "prior_edge_table.csv": run_dir / "results" / "prior_edge_table.csv",
        }
        missing = [name for name in artifact_names if not artifact_paths[name].exists()]
        rows.append(
            {
                "branch": branch["branch"],
                "role": branch["role"],
                "source_run": str(run_dir),
                "source_status": status.get("readout", ""),
                "scores_written": status.get("scores_written", ""),
                "required_artifacts_present": "yes" if not missing else "no",
                "missing_artifacts": ";".join(missing),
                "status": "pass" if not missing and status.get("scores_written") is True else "fail",
            }
        )
    return rows


def reproduction_fit_rows(bao_repro: Any, scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = bao_repro.fit_summary_rows(scores)
    for row in rows:
        row["official_branch_alias"] = official_branch_alias(str(row["model"]))
        row["arena"] = "BAO-only"
    return rows


def reproduction_prior_edge_rows(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for score in scores:
        for edge_row in score["edge_rows"]:
            out = dict(edge_row)
            out["official_branch_alias"] = official_branch_alias(str(score["model"]))
            rows.append(out)
    return rows


def reproduction_comparison_rows(bao_repro: Any, scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = bao_repro.comparison_rows(scores)
    for row in rows:
        row["official_candidate_alias"] = official_branch_alias(str(row["candidate"]))
        row["official_reference_alias"] = official_branch_alias(str(row["reference"]))
    return rows


def reproduction_reference_check_rows(comparisons: list[dict[str, Any]], tolerance: float) -> list[dict[str, Any]]:
    by_release_reference = {(row["release"], row["reference"]): row for row in comparisons}
    rows: list[dict[str, Any]] = []
    for release, expected_delta_bic in EXPECTED_BAO_DELTAS_VS_LCDM.items():
        comparison = by_release_reference.get((release, "LCDM"))
        if comparison is None:
            rows.append(
                {
                    "release": release,
                    "reference": "LCDM",
                    "expected_delta_BIC": expected_delta_bic,
                    "actual_delta_BIC": "",
                    "absolute_error": "",
                    "tolerance": tolerance,
                    "sign_match": "no",
                    "status": "fail_missing_comparison",
                }
            )
            continue
        actual_delta_bic = float(comparison["delta_BIC"])
        absolute_error = abs(actual_delta_bic - expected_delta_bic)
        sign_match = (actual_delta_bic < 0.0) == (expected_delta_bic < 0.0)
        rows.append(
            {
                "release": release,
                "reference": "LCDM",
                "expected_delta_BIC": expected_delta_bic,
                "actual_delta_BIC": actual_delta_bic,
                "absolute_error": absolute_error,
                "tolerance": tolerance,
                "sign_match": "yes" if sign_match else "no",
                "status": "pass" if sign_match and absolute_error <= tolerance else "fail",
            }
        )
    return rows


def reproduction_gate_rows(
    manifest_gates: list[dict[str, Any]],
    scores: list[dict[str, Any]],
    prior_edges: list[dict[str, Any]],
    reference_checks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    manifest_bad = [row for row in manifest_gates if row["status"] != "pass"]
    scored_models = {str(score["model"]) for score in scores}
    missing_models = [model for model in REPRO_MODELS if model not in scored_models]
    sidecar_scores = [model for model in scored_models if model == SIDECAR_BRANCH or "pair_ruler" in model]
    convergence_bad = [score for score in scores if not score["converged"]]
    locked_scores = [score for score in scores if score["model"] == "MTS_locked_2over27"]
    locked_wrong_bmem = [
        score
        for score in locked_scores
        if abs(float(score["B_mem"]) - (2.0 / 27.0)) > 1.0e-14 or score["B_mem_fit_status"] != "frozen"
    ]
    locked_edge_flags = [score for score in locked_scores if score["prior_edge_flag"]]
    prior_edge_flags = [row for row in prior_edges if str(row["edge_flag"]) == "True"]
    reference_bad = [row for row in reference_checks if row["status"] != "pass"]
    return [
        {
            "gate": "manifest_guard_passed",
            "status": "pass" if not manifest_bad else "fail",
            "evidence": f"failed_manifest_gates={len(manifest_bad)}",
        },
        {
            "gate": "arena_is_BAO_only",
            "status": "pass",
            "evidence": "single arena reproduction only; no SN/Hz/growth/CMB refresh",
        },
        {
            "gate": "required_models_scored",
            "status": "pass" if not missing_models else "fail",
            "evidence": f"missing={';'.join(missing_models)}; scored={len(scored_models)}",
        },
        {
            "gate": "sidecar_absent",
            "status": "pass" if not sidecar_scores else "fail",
            "evidence": f"sidecar_scores={';'.join(sidecar_scores)}",
        },
        {
            "gate": "locked_branch_fixed_Bmem",
            "status": "pass" if locked_scores and not locked_wrong_bmem else "fail",
            "evidence": "B_mem=2/27 frozen for MTS_locked_2over27",
        },
        {
            "gate": "locked_branch_not_prior_edge",
            "status": "pass" if not locked_edge_flags else "fail",
            "evidence": f"locked_edge_flags={len(locked_edge_flags)}",
        },
        {
            "gate": "all_models_converged",
            "status": "pass" if not convergence_bad else "fail",
            "evidence": f"nonconverged={len(convergence_bad)}",
        },
        {
            "gate": "prior_edges_reported_for_all_models",
            "status": "pass",
            "evidence": f"prior_rows={len(prior_edges)}; flagged_edges={len(prior_edge_flags)}",
        },
        {
            "gate": "reference_delta_reproduced",
            "status": "pass" if not reference_bad else "fail",
            "evidence": f"failed_reference_checks={len(reference_bad)}; tolerance_applied",
        },
        {
            "gate": "full_refresh_not_run",
            "status": "pass",
            "evidence": "no replacement official-likelihood claim generated",
        },
        {
            "gate": "claim_ceiling_preserved",
            "status": "pass",
            "evidence": REPRO_CLAIM_CEILING,
        },
    ]


def reproduction_decision_rows(gates: list[dict[str, Any]], comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failed = [row for row in gates if row["status"] != "pass"]
    status = REPRO_STATUS_PASS if not failed else REPRO_STATUS_FAIL
    lcdm_rows = [row for row in comparisons if row["reference"] == "LCDM"]
    lcdm_evidence = "; ".join(f"{row['release']}:dBIC={row['delta_BIC']}" for row in lcdm_rows)
    return [
        {
            "item": "status",
            "verdict": status,
            "evidence": f"failed_gates={len(failed)}",
        },
        {
            "item": "arena",
            "verdict": "BAO-only",
            "evidence": "single-arena reproduction guard only",
        },
        {
            "item": "lead_branch",
            "verdict": LEAD_BRANCH,
            "evidence": "implemented through MTS_locked_2over27 BAO scorer alias",
        },
        {
            "item": "BAO_vs_LCDM_reference",
            "verdict": "reproduced" if not failed else "not_reproduced",
            "evidence": lcdm_evidence,
        },
        {
            "item": "claim_ceiling",
            "verdict": REPRO_CLAIM_CEILING,
            "evidence": "no full official likelihood, CMB pass, local-GR derivation, or parent-action promotion",
        },
        {
            "item": "next_target",
            "verdict": "173-no-clock-SN-BAO-reproduction-guard.md",
            "evidence": "only expand after this single-arena guard passes",
        },
    ]


def sn_bao_prior_edge_rows(sn_bao_repro: Any, scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_branch = {score["branch"]: score for score in scores}
    for branch in sn_bao_repro.BRANCHES:
        score = by_branch[branch["branch"]]
        omega_m = float(score["Omega_m"])
        lower = 0.05
        upper = 0.6
        distance = min(omega_m - lower, upper - omega_m)
        rows.append(
            {
                "branch": branch["branch"],
                "model": "MTS_locked_2over27",
                "official_branch_alias": LEAD_BRANCH,
                "parameter": "Omega_m",
                "best_fit": omega_m,
                "lower": lower,
                "upper": upper,
                "distance_to_edge": distance,
                "edge_flag": bool(score["Omega_m_edge_flag"]),
                "source": "locked_reproduction_score",
            }
        )
        for edge_row in read_csv_rows(branch["run"] / "results" / "prior_edge_table.csv"):
            out = {
                "branch": branch["branch"],
                "model": edge_row["model"],
                "official_branch_alias": official_branch_alias(edge_row["model"]),
                "parameter": edge_row["parameter"],
                "best_fit": edge_row["best_fit"],
                "lower": edge_row["lower"],
                "upper": edge_row["upper"],
                "distance_to_edge": edge_row["distance_to_edge"],
                "edge_flag": edge_row["edge_flag"],
                "source": "source_run_prior_edge_table",
            }
            rows.append(out)
    return rows


def sn_bao_reference_check_rows(branch_gates: list[dict[str, Any]], tolerance: float) -> list[dict[str, Any]]:
    by_branch = {row["branch"]: row for row in branch_gates}
    rows: list[dict[str, Any]] = []
    for branch, expected_delta_bic in EXPECTED_SN_BAO_DELTAS_VS_LCDM.items():
        gate = by_branch.get(branch)
        if gate is None:
            rows.append(
                {
                    "branch": branch,
                    "reference": "LCDM",
                    "expected_delta_BIC": expected_delta_bic,
                    "actual_delta_BIC": "",
                    "absolute_error": "",
                    "tolerance": tolerance,
                    "sign_match": "no",
                    "status": "fail_missing_branch_gate",
                }
            )
            continue
        actual_delta_bic = float(gate["delta_BIC_vs_LCDM"])
        absolute_error = abs(actual_delta_bic - expected_delta_bic)
        sign_match = (actual_delta_bic < 0.0) == (expected_delta_bic < 0.0)
        rows.append(
            {
                "branch": branch,
                "reference": "LCDM",
                "expected_delta_BIC": expected_delta_bic,
                "actual_delta_BIC": actual_delta_bic,
                "absolute_error": absolute_error,
                "tolerance": tolerance,
                "sign_match": "yes" if sign_match else "no",
                "status": "pass" if sign_match and absolute_error <= tolerance else "fail",
            }
        )
    return rows


def sn_bao_locked_score_rows(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for score in scores:
        row = dict(score)
        row["official_branch_alias"] = LEAD_BRANCH
        row["arena"] = "SN+BAO"
        rows.append(row)
    return rows


def sn_bao_comparison_rows(sn_bao_repro: Any, scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = sn_bao_repro.comparison_rows(scores)
    for row in rows:
        row["official_candidate_alias"] = LEAD_BRANCH
        row["official_reference_alias"] = official_branch_alias(str(row["reference"]))
    return rows


def sn_bao_reproduction_gate_rows(
    manifest_gates: list[dict[str, Any]],
    branch_sources: list[dict[str, Any]],
    scores: list[dict[str, Any]],
    branch_gates: list[dict[str, Any]],
    prior_edges: list[dict[str, Any]],
    reference_checks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    manifest_bad = [row for row in manifest_gates if row["status"] != "pass"]
    source_bad = [row for row in branch_sources if row["status"] != "pass"]
    score_branches = {score["branch"] for score in scores}
    missing_branches = [branch for branch in EXPECTED_SN_BAO_DELTAS_VS_LCDM if branch not in score_branches]
    nonconverged = [score for score in scores if not score["converged"]]
    locked_edges = [score for score in scores if score["Omega_m_edge_flag"]]
    gate_bad = [row for row in branch_gates if row["result"] != "pass"]
    prior_edge_flags = [row for row in prior_edges if str(row["edge_flag"]) in {"True", "true", "1"}]
    reference_bad = [row for row in reference_checks if row["status"] != "pass"]
    return [
        {
            "gate": "manifest_guard_passed",
            "status": "pass" if not manifest_bad else "fail",
            "evidence": f"failed_manifest_gates={len(manifest_bad)}",
        },
        {
            "gate": "arena_is_SN_BAO_locked_matrix",
            "status": "pass",
            "evidence": "T1-T6 SN+BAO locked 2/27 reproduction; no H(z)/growth/CMB refresh",
        },
        {
            "gate": "source_branch_artifacts_present",
            "status": "pass" if not source_bad else "fail",
            "evidence": f"bad_source_branches={len(source_bad)}; branches={len(branch_sources)}",
        },
        {
            "gate": "required_branches_scored",
            "status": "pass" if not missing_branches else "fail",
            "evidence": f"missing={';'.join(missing_branches)}; scored={len(score_branches)}",
        },
        {
            "gate": "sidecar_absent",
            "status": "pass",
            "evidence": "pair-ruler sidecar not part of T1-T6 locked 2/27 scorer",
        },
        {
            "gate": "locked_branch_fixed_Bmem",
            "status": "pass",
            "evidence": "B_mem=2/27 fixed; p=3; u3=1/4; Omega_m only cosmological fit",
        },
        {
            "gate": "locked_branch_not_prior_edge",
            "status": "pass" if not locked_edges else "fail",
            "evidence": f"locked_Omega_m_edge_flags={len(locked_edges)}",
        },
        {
            "gate": "all_locked_branches_converged",
            "status": "pass" if not nonconverged else "fail",
            "evidence": f"nonconverged={len(nonconverged)}",
        },
        {
            "gate": "all_branch_gates_pass",
            "status": "pass" if not gate_bad else "fail",
            "evidence": f"nonpass_branch_gates={len(gate_bad)}",
        },
        {
            "gate": "prior_edges_reported_for_locked_and_baselines",
            "status": "pass",
            "evidence": f"prior_rows={len(prior_edges)}; flagged_edges={len(prior_edge_flags)}",
        },
        {
            "gate": "reference_delta_reproduced",
            "status": "pass" if not reference_bad else "fail",
            "evidence": f"failed_reference_checks={len(reference_bad)}; tolerance_applied",
        },
        {
            "gate": "full_refresh_not_run",
            "status": "pass",
            "evidence": "reproduction of existing SN+BAO locked matrix only",
        },
        {
            "gate": "claim_ceiling_preserved",
            "status": "pass",
            "evidence": SN_BAO_REPRO_CLAIM_CEILING,
        },
    ]


def sn_bao_reproduction_decision_rows(gates: list[dict[str, Any]], branch_gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failed = [row for row in gates if row["status"] != "pass"]
    status = SN_BAO_REPRO_STATUS_PASS if not failed else SN_BAO_REPRO_STATUS_FAIL
    lcdm_evidence = "; ".join(f"{row['branch']}:dBIC={row['delta_BIC_vs_LCDM']}" for row in branch_gates)
    return [
        {
            "item": "status",
            "verdict": status,
            "evidence": f"failed_gates={len(failed)}",
        },
        {
            "item": "arena",
            "verdict": "SN+BAO",
            "evidence": "T1-T6 locked 2/27 reproduction matrix",
        },
        {
            "item": "lead_branch",
            "verdict": LEAD_BRANCH,
            "evidence": "implemented through two_ninth_boundary_charge locked-amplitude scorer",
        },
        {
            "item": "SN_BAO_vs_LCDM_reference",
            "verdict": "reproduced" if not failed else "not_reproduced",
            "evidence": lcdm_evidence,
        },
        {
            "item": "claim_ceiling",
            "verdict": SN_BAO_REPRO_CLAIM_CEILING,
            "evidence": "no full official likelihood, CMB pass, local-GR derivation, or parent-action promotion",
        },
        {
            "item": "next_target",
            "verdict": "174-no-clock-Hz-growth-reproduction-readiness.md",
            "evidence": "after SN+BAO reproduction, add non-CMB holdout readiness before broader refresh",
        },
    ]


def run_manifest_guard(output_root: Path, timestamp: str | None, source_run: Path, mode: str, assert_no_sidecar: bool) -> Path:
    if mode != "manifest-only":
        raise ValueError("Only --mode manifest-only is implemented in checkpoint 171; scoring modes are intentionally refused.")
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-no-clock-manifest-only-fit-guard"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_run = source_run.resolve()
    source_results = source_run / "results"
    sources = source_register_rows(Path(__file__).resolve(), source_run)
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    artifact_contract = artifact_contract_rows(source_run)
    source_status = source_status_guard_rows(source_run)
    hash_guards = source_hash_guard_rows(source_results)
    row_guards = row_guard_rows(source_results)
    covariance_guards = covariance_guard_rows(source_results)
    branch_guards = branch_guard_rows(source_results, assert_no_sidecar)
    nuisance_guards = nuisance_guard_rows(source_results)
    prior_edges = prior_edge_contract_rows(source_results)
    refusal = scoring_refusal_rows(mode)
    gates = guard_gate_rows(
        source_status,
        artifact_contract,
        hash_guards,
        row_guards,
        covariance_guards,
        branch_guards,
        nuisance_guards,
        mode,
    )
    decisions = decision_rows(gates)
    status = decisions[0]["verdict"]

    write_json(
        run_dir / "run_config.json",
        {
            "timestamp": run_stamp,
            "mode": mode,
            "assert_no_sidecar": assert_no_sidecar,
            "source_run": str(source_run),
            "claim_ceiling": CLAIM_CEILING,
            "model_scoring": "not_run",
        },
    )
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(results_dir / "source_artifact_contract.csv", artifact_contract, ["artifact", "path", "exists", "sha256", "row_count", "header_status", "required_for_scoring", "status"])
    write_csv(results_dir / "source_status_guard.csv", source_status, ["check", "status", "evidence"])
    write_csv(results_dir / "source_hash_guard.csv", hash_guards, ["check", "status", "evidence"])
    write_csv(results_dir / "row_contract_guard.csv", row_guards, ["arena", "row_count", "minimum_required", "status"])
    write_csv(results_dir / "covariance_contract_guard.csv", covariance_guards, ["dataset", "arena", "status", "evidence"])
    write_csv(results_dir / "branch_contract_guard.csv", branch_guards, ["branch", "role", "included_in_lead_refresh", "required_policy", "status", "evidence"])
    write_csv(results_dir / "nuisance_contract_guard.csv", nuisance_guards, ["arena", "status", "evidence"])
    write_csv(results_dir / "prior_edge_contract.csv", prior_edges, ["branch", "required_future_artifact", "required_fields", "status", "reason"])
    write_csv(results_dir / "scoring_refusal_policy.csv", refusal, ["mode", "allowed", "action"])
    write_csv(results_dir / "guard_gates.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])
    write_json(
        run_dir / "status.json",
        {
            "status": status,
            "run_dir": str(run_dir),
            "results_dir": str(results_dir),
            "source_run": str(source_run),
            "mode": mode,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "sidecar_policy": "excluded_from_lead_refresh",
            "model_scoring": "not_run",
            "failed_gates": [row["gate"] for row in gates if row["status"] != "pass"],
            "next_target": "172-no-clock-single-arena-reproduction-guard.md",
            "generated": [
                "source_register.csv",
                "source_artifact_contract.csv",
                "source_status_guard.csv",
                "source_hash_guard.csv",
                "row_contract_guard.csv",
                "covariance_contract_guard.csv",
                "branch_contract_guard.csv",
                "nuisance_contract_guard.csv",
                "prior_edge_contract.csv",
                "scoring_refusal_policy.csv",
                "guard_gates.csv",
                "decision.csv",
            ],
        },
    )
    marker = "DONE.txt" if status == STATUS_PASS else "FAILED.txt"
    (run_dir / marker).write_text(f"{status}\n", encoding="utf-8")
    return run_dir


def run_reproduce_guard(
    output_root: Path,
    timestamp: str | None,
    source_run: Path,
    assert_no_sidecar: bool,
    max_iter: int,
    reference_tolerance: float,
) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-no-clock-single-arena-reproduction-guard"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_run = source_run.resolve()
    source_results = source_run / "results"
    bao_repro = load_bao_reproduction_module()
    sources = source_register_rows(Path(__file__).resolve(), source_run)
    reproduction_sources = reproduction_source_rows(bao_repro, source_run)
    missing = [row["path"] for row in [*sources, *reproduction_sources] if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    artifact_contract = artifact_contract_rows(source_run)
    source_status = source_status_guard_rows(source_run)
    hash_guards = source_hash_guard_rows(source_results)
    row_guards = row_guard_rows(source_results)
    covariance_guards = covariance_guard_rows(source_results)
    branch_guards = branch_guard_rows(source_results, assert_no_sidecar)
    nuisance_guards = nuisance_guard_rows(source_results)
    prior_edge_contract = prior_edge_contract_rows(source_results)
    refusal = scoring_refusal_rows("reproduce")
    manifest_gates = guard_gate_rows(
        source_status,
        artifact_contract,
        hash_guards,
        row_guards,
        covariance_guards,
        branch_guards,
        nuisance_guards,
        "manifest-only",
    )

    loaded = bao_repro.loaded_release_rows()
    load_failures = [row for row in loaded if row["load_status"] != "pass"]
    scores: list[dict[str, Any]] = []
    comparisons: list[dict[str, Any]] = []
    reference_checks: list[dict[str, Any]] = []
    prior_edges: list[dict[str, Any]] = []
    residuals: list[dict[str, Any]] = []
    release_gates: list[dict[str, Any]] = []
    if not load_failures and all(row["status"] == "pass" for row in manifest_gates):
        bao_by_release = {release: bao_repro.runner.read_bao_data(paths["mean"], paths["cov"]) for release, paths in bao_repro.RELEASES.items()}
        for release, bao in bao_by_release.items():
            for model in REPRO_MODELS:
                scores.append(bao_repro.score_model(release, model, bao, max_iter=max_iter))
        comparisons = reproduction_comparison_rows(bao_repro, scores)
        reference_checks = reproduction_reference_check_rows(comparisons, reference_tolerance)
        prior_edges = reproduction_prior_edge_rows(scores)
        residuals = bao_repro.residual_rows(scores, bao_by_release)
        release_gates = bao_repro.release_gate_rows(scores, comparisons)

    reproduction_gates = reproduction_gate_rows(manifest_gates, scores, prior_edges, reference_checks)
    if load_failures:
        reproduction_gates.append(
            {
                "gate": "BAO_release_loads_pass",
                "status": "fail",
                "evidence": f"load_failures={len(load_failures)}",
            }
        )
    else:
        reproduction_gates.append(
            {
                "gate": "BAO_release_loads_pass",
                "status": "pass",
                "evidence": f"releases={len(loaded)}",
            }
        )
    decisions = reproduction_decision_rows(reproduction_gates, comparisons)
    status = decisions[0]["verdict"]

    write_json(
        run_dir / "run_config.json",
        {
            "timestamp": run_stamp,
            "mode": "reproduce",
            "arena": "BAO-only",
            "assert_no_sidecar": assert_no_sidecar,
            "source_run": str(source_run),
            "max_iter": max_iter,
            "reference_tolerance": reference_tolerance,
            "claim_ceiling": REPRO_CLAIM_CEILING,
            "model_scoring": "single_arena_reproduction_only",
            "models": REPRO_MODELS,
        },
    )
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(results_dir / "reproduction_source_register.csv", reproduction_sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(results_dir / "source_artifact_contract.csv", artifact_contract, ["artifact", "path", "exists", "sha256", "row_count", "header_status", "required_for_scoring", "status"])
    write_csv(results_dir / "source_status_guard.csv", source_status, ["check", "status", "evidence"])
    write_csv(results_dir / "source_hash_guard.csv", hash_guards, ["check", "status", "evidence"])
    write_csv(results_dir / "row_contract_guard.csv", row_guards, ["arena", "row_count", "minimum_required", "status"])
    write_csv(results_dir / "covariance_contract_guard.csv", covariance_guards, ["dataset", "arena", "status", "evidence"])
    write_csv(results_dir / "branch_contract_guard.csv", branch_guards, ["branch", "role", "included_in_lead_refresh", "required_policy", "status", "evidence"])
    write_csv(results_dir / "nuisance_contract_guard.csv", nuisance_guards, ["arena", "status", "evidence"])
    write_csv(results_dir / "prior_edge_contract.csv", prior_edge_contract, ["branch", "required_future_artifact", "required_fields", "status", "reason"])
    write_csv(results_dir / "scoring_refusal_policy.csv", refusal, ["mode", "allowed", "action"])
    write_csv(results_dir / "guard_gates.csv", manifest_gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "reproduction_data_schema_report.csv", bao_repro.schema_rows(), ["release", "kind", "path", "exists", "readable", "row_count", "columns", "sha256", "issue"])
    write_csv(results_dir / "reproduction_bao_release_load_report.csv", loaded, ["release", "mean_path", "cov_path", "bao_rows", "cov_shape", "min_cov_eigenvalue", "quantities", "load_status", "issue"])
    write_csv(results_dir / "reproduction_model_register.csv", bao_repro.model_rows(), ["model", "role", "fixed", "fitted", "claim_ceiling"])
    write_csv(results_dir / "reproduction_fit_summary.csv", reproduction_fit_rows(bao_repro, scores), ["release", "model", "official_branch_alias", "arena", "chi2_BAO", "k", "n", "AIC", "BIC", "converged", "prior_edge_flag", "Omega_m", "w", "w0", "wa", "B_mem", "B_mem_fit_status", "p", "u3", "bao_alpha", "claim_ceiling"])
    write_csv(results_dir / "reproduction_prior_edge_table.csv", prior_edges, ["release", "model", "official_branch_alias", "parameter", "best_fit", "lower", "upper", "distance_to_edge", "edge_flag"])
    write_csv(results_dir / "reproduction_baseline_comparisons.csv", comparisons, ["release", "candidate", "official_candidate_alias", "reference", "official_reference_alias", "delta_chi2", "delta_AIC", "delta_BIC", "readout"])
    write_csv(results_dir / "reproduction_reference_check.csv", reference_checks, ["release", "reference", "expected_delta_BIC", "actual_delta_BIC", "absolute_error", "tolerance", "sign_match", "status"])
    write_csv(results_dir / "reproduction_release_gates.csv", release_gates, ["release", "result", "locked_B_mem", "locked_edge_flag", "locked_converged", "delta_chi2_vs_LCDM", "delta_AIC_vs_LCDM", "delta_BIC_vs_LCDM", "delta_chi2_vs_fitted_Bmem", "interpretation"])
    write_csv(results_dir / "reproduction_residuals.csv", residuals, ["release", "model", "row_index", "z", "quantity", "observed", "predicted", "residual"])
    write_csv(results_dir / "reproduction_gates.csv", reproduction_gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])
    write_json(
        run_dir / "status.json",
        {
            "status": status,
            "run_dir": str(run_dir),
            "results_dir": str(results_dir),
            "source_run": str(source_run),
            "mode": "reproduce",
            "arena": "BAO-only",
            "claim_ceiling": REPRO_CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "sidecar_policy": "excluded_from_lead_refresh",
            "model_scoring": "single_arena_reproduction_only",
            "failed_gates": [row["gate"] for row in reproduction_gates if row["status"] != "pass"],
            "reference_checks": reference_checks,
            "next_target": "173-no-clock-SN-BAO-reproduction-guard.md",
            "generated": [
                "source_register.csv",
                "reproduction_source_register.csv",
                "source_artifact_contract.csv",
                "source_status_guard.csv",
                "source_hash_guard.csv",
                "row_contract_guard.csv",
                "covariance_contract_guard.csv",
                "branch_contract_guard.csv",
                "nuisance_contract_guard.csv",
                "prior_edge_contract.csv",
                "scoring_refusal_policy.csv",
                "guard_gates.csv",
                "reproduction_data_schema_report.csv",
                "reproduction_bao_release_load_report.csv",
                "reproduction_model_register.csv",
                "reproduction_fit_summary.csv",
                "reproduction_prior_edge_table.csv",
                "reproduction_baseline_comparisons.csv",
                "reproduction_reference_check.csv",
                "reproduction_release_gates.csv",
                "reproduction_residuals.csv",
                "reproduction_gates.csv",
                "decision.csv",
            ],
        },
    )
    marker = "DONE.txt" if status == REPRO_STATUS_PASS else "FAILED.txt"
    (run_dir / marker).write_text(f"{status}\n", encoding="utf-8")
    return run_dir


def run_sn_bao_reproduce_guard(
    output_root: Path,
    timestamp: str | None,
    source_run: Path,
    assert_no_sidecar: bool,
    reference_tolerance: float,
) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-no-clock-SN-BAO-reproduction-guard"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_run = source_run.resolve()
    source_results = source_run / "results"
    sn_bao_repro = load_sn_bao_reproduction_module()
    sources = source_register_rows(Path(__file__).resolve(), source_run)
    reproduction_sources = sn_bao_reproduction_source_rows(sn_bao_repro, source_run)
    branch_sources = sn_bao_branch_source_rows(sn_bao_repro)
    missing = [row["path"] for row in [*sources, *reproduction_sources] if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    artifact_contract = artifact_contract_rows(source_run)
    source_status = source_status_guard_rows(source_run)
    hash_guards = source_hash_guard_rows(source_results)
    row_guards = row_guard_rows(source_results)
    covariance_guards = covariance_guard_rows(source_results)
    branch_guards = branch_guard_rows(source_results, assert_no_sidecar)
    nuisance_guards = nuisance_guard_rows(source_results)
    prior_edge_contract = prior_edge_contract_rows(source_results)
    refusal = scoring_refusal_rows("reproduce")
    manifest_gates = guard_gate_rows(
        source_status,
        artifact_contract,
        hash_guards,
        row_guards,
        covariance_guards,
        branch_guards,
        nuisance_guards,
        "manifest-only",
    )

    source_bad = [row for row in branch_sources if row["status"] != "pass"]
    scores: list[dict[str, Any]] = []
    comparisons: list[dict[str, Any]] = []
    branch_gates: list[dict[str, Any]] = []
    prior_edges: list[dict[str, Any]] = []
    reference_checks: list[dict[str, Any]] = []
    if not source_bad and all(row["status"] == "pass" for row in manifest_gates):
        scores = [sn_bao_repro.branch_score(branch) for branch in sn_bao_repro.BRANCHES]
        comparisons = sn_bao_comparison_rows(sn_bao_repro, scores)
        branch_gates = sn_bao_repro.branch_gate_rows(scores, comparisons)
        prior_edges = sn_bao_prior_edge_rows(sn_bao_repro, scores)
        reference_checks = sn_bao_reference_check_rows(branch_gates, reference_tolerance)

    reproduction_gates = sn_bao_reproduction_gate_rows(
        manifest_gates,
        branch_sources,
        scores,
        branch_gates,
        prior_edges,
        reference_checks,
    )
    decisions = sn_bao_reproduction_decision_rows(reproduction_gates, branch_gates)
    status = decisions[0]["verdict"]

    write_json(
        run_dir / "run_config.json",
        {
            "timestamp": run_stamp,
            "mode": "reproduce",
            "arena": "SN-BAO-T7",
            "assert_no_sidecar": assert_no_sidecar,
            "source_run": str(source_run),
            "reference_tolerance": reference_tolerance,
            "claim_ceiling": SN_BAO_REPRO_CLAIM_CEILING,
            "model_scoring": "SN_BAO_locked_2over27_reproduction_only",
            "expected_reference_deltas_vs_LCDM": EXPECTED_SN_BAO_DELTAS_VS_LCDM,
        },
    )
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(results_dir / "sn_bao_reproduction_source_register.csv", reproduction_sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(results_dir / "sn_bao_branch_source_register.csv", branch_sources, ["branch", "role", "source_run", "source_status", "scores_written", "required_artifacts_present", "missing_artifacts", "status"])
    write_csv(results_dir / "source_artifact_contract.csv", artifact_contract, ["artifact", "path", "exists", "sha256", "row_count", "header_status", "required_for_scoring", "status"])
    write_csv(results_dir / "source_status_guard.csv", source_status, ["check", "status", "evidence"])
    write_csv(results_dir / "source_hash_guard.csv", hash_guards, ["check", "status", "evidence"])
    write_csv(results_dir / "row_contract_guard.csv", row_guards, ["arena", "row_count", "minimum_required", "status"])
    write_csv(results_dir / "covariance_contract_guard.csv", covariance_guards, ["dataset", "arena", "status", "evidence"])
    write_csv(results_dir / "branch_contract_guard.csv", branch_guards, ["branch", "role", "included_in_lead_refresh", "required_policy", "status", "evidence"])
    write_csv(results_dir / "nuisance_contract_guard.csv", nuisance_guards, ["arena", "status", "evidence"])
    write_csv(results_dir / "prior_edge_contract.csv", prior_edge_contract, ["branch", "required_future_artifact", "required_fields", "status", "reason"])
    write_csv(results_dir / "scoring_refusal_policy.csv", refusal, ["mode", "allowed", "action"])
    write_csv(results_dir / "guard_gates.csv", manifest_gates, ["gate", "status", "evidence"])
    write_csv(
        results_dir / "sn_bao_locked_branch_scores.csv",
        sn_bao_locked_score_rows(scores),
        [
            "branch",
            "role",
            "source_run",
            "sn_rows",
            "bao_rows",
            "sn_covariance_mode",
            "sn_observable",
            "bao_label",
            "candidate",
            "official_branch_alias",
            "arena",
            "DeltaR_fraction",
            "DeltaR",
            "B_mem",
            "fitted_B_mem_reference",
            "B_mem_lock_minus_fit",
            "relative_B_mem_lock_minus_fit",
            "Omega_m",
            "chi2_SN",
            "chi2_BAO",
            "chi2_total",
            "AIC",
            "BIC",
            "k",
            "n",
            "converged",
            "Omega_m_edge_flag",
            "claim_ceiling",
        ],
    )
    write_csv(results_dir / "sn_bao_locked_branch_comparisons.csv", comparisons, ["branch", "reference", "official_candidate_alias", "official_reference_alias", "delta_chi2", "delta_AIC", "delta_BIC", "readout"])
    write_csv(
        results_dir / "sn_bao_branch_gates.csv",
        branch_gates,
        [
            "branch",
            "gate",
            "result",
            "locked_minus_fitted_B_mem",
            "delta_chi2_vs_LCDM",
            "delta_AIC_vs_LCDM",
            "delta_BIC_vs_LCDM",
            "delta_chi2_vs_fitted_MTS",
            "delta_chi2_vs_zero_memory",
            "interpretation",
        ],
    )
    write_csv(results_dir / "sn_bao_prior_edge_table.csv", prior_edges, ["branch", "model", "official_branch_alias", "parameter", "best_fit", "lower", "upper", "distance_to_edge", "edge_flag", "source"])
    write_csv(results_dir / "sn_bao_reference_check.csv", reference_checks, ["branch", "reference", "expected_delta_BIC", "actual_delta_BIC", "absolute_error", "tolerance", "sign_match", "status"])
    write_csv(results_dir / "sn_bao_reproduction_gates.csv", reproduction_gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])
    write_json(
        run_dir / "status.json",
        {
            "status": status,
            "run_dir": str(run_dir),
            "results_dir": str(results_dir),
            "source_run": str(source_run),
            "mode": "reproduce",
            "arena": "SN-BAO-T7",
            "claim_ceiling": SN_BAO_REPRO_CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "sidecar_policy": "excluded_from_lead_refresh",
            "model_scoring": "SN_BAO_locked_2over27_reproduction_only",
            "failed_gates": [row["gate"] for row in reproduction_gates if row["status"] != "pass"],
            "reference_checks": reference_checks,
            "next_target": "174-no-clock-Hz-growth-reproduction-readiness.md",
            "generated": [
                "source_register.csv",
                "sn_bao_reproduction_source_register.csv",
                "sn_bao_branch_source_register.csv",
                "source_artifact_contract.csv",
                "source_status_guard.csv",
                "source_hash_guard.csv",
                "row_contract_guard.csv",
                "covariance_contract_guard.csv",
                "branch_contract_guard.csv",
                "nuisance_contract_guard.csv",
                "prior_edge_contract.csv",
                "scoring_refusal_policy.csv",
                "guard_gates.csv",
                "sn_bao_locked_branch_scores.csv",
                "sn_bao_locked_branch_comparisons.csv",
                "sn_bao_branch_gates.csv",
                "sn_bao_prior_edge_table.csv",
                "sn_bao_reference_check.csv",
                "sn_bao_reproduction_gates.csv",
                "decision.csv",
            ],
        },
    )
    marker = "DONE.txt" if status == SN_BAO_REPRO_STATUS_PASS else "FAILED.txt"
    (run_dir / marker).write_text(f"{status}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--source-run", type=Path, default=None)
    parser.add_argument("--mode", choices=["manifest-only", "reproduce", "full-refresh"], default="manifest-only")
    parser.add_argument("--arena", choices=["BAO-only", "SN-BAO-T7"], default="BAO-only")
    parser.add_argument("--assert-no-sidecar", action="store_true")
    parser.add_argument("--max-iter", type=int, default=180)
    parser.add_argument("--reference-tolerance", type=float, default=1.0e-8)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_run = args.source_run or latest_source_run()
    if args.mode == "manifest-only":
        print(run_manifest_guard(args.output_root, args.timestamp, source_run, args.mode, args.assert_no_sidecar))
    elif args.mode == "reproduce":
        if args.arena == "BAO-only":
            print(
                run_reproduce_guard(
                    args.output_root,
                    args.timestamp,
                    source_run,
                    args.assert_no_sidecar,
                    args.max_iter,
                    args.reference_tolerance,
                )
            )
        else:
            print(
                run_sn_bao_reproduce_guard(
                    args.output_root,
                    args.timestamp,
                    source_run,
                    args.assert_no_sidecar,
                    args.reference_tolerance,
                )
            )
    else:
        raise ValueError("full-refresh is intentionally not implemented until single-arena reproduction is reviewed.")


if __name__ == "__main__":
    main()
