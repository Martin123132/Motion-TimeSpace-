#!/usr/bin/env python3
"""Guarded non-CMB reproduction for the no-clock locked branch."""

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

READINESS_RUN = RUNS_ROOT / "20260531-235959-no-clock-Hz-growth-reproduction-readiness"
STATUS_PASS = "no_clock_nonCMB_reproduction_guard_passed"
STATUS_FAIL = "no_clock_nonCMB_reproduction_guard_failed"
CLAIM_CEILING = "non_CMB_guarded_reproduction_no_full_refresh_or_theory_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"
SIDECAR_BRANCH = "MTS_pair_ruler_half_kernel"
TOLERANCE = 1.0e-6

REFERENCE_RUNS = {
    "fresh_CC_Hz_source_locked_holdout": RUNS_ROOT / "20260531-221500-fresh-CC-Hz-source-locked-holdout",
    "source_locked_growth_covariance_holdout": RUNS_ROOT / "20260531-224500-source-locked-growth-covariance-holdout",
    "ELG_grid_likelihood_holdout": RUNS_ROOT / "20260531-231500-ELG-grid-likelihood-holdout",
}


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


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def import_script(module_name: str) -> Any:
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    return importlib.import_module(module_name)


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 175 guarded reproduction runner"),
        (SCRIPT_DIR / "fresh_CC_Hz_source_locked_holdout.py", "source-locked H(z) scorer"),
        (SCRIPT_DIR / "source_locked_growth_covariance_holdout.py", "source-locked growth covariance scorer"),
        (SCRIPT_DIR / "ELG_grid_likelihood_holdout.py", "ELG grid likelihood scorer"),
        (READINESS_RUN / "status.json", "checkpoint 174 readiness status"),
        (WORK_DIR / "174-no-clock-Hz-growth-reproduction-readiness.md", "checkpoint 174 note"),
    ]
    rows: list[dict[str, Any]] = []
    for path, role in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": role,
                "issue": "" if exists else "missing",
            }
        )
    return rows


def run_reproductions(reproduction_root: Path, timestamp: str) -> dict[str, Path]:
    hz = import_script("fresh_CC_Hz_source_locked_holdout")
    growth = import_script("source_locked_growth_covariance_holdout")
    elg = import_script("ELG_grid_likelihood_holdout")
    reproduction_root.mkdir(parents=True, exist_ok=True)
    return {
        "fresh_CC_Hz_source_locked_holdout": hz.run_holdout(reproduction_root, timestamp=timestamp),
        "source_locked_growth_covariance_holdout": growth.run_holdout(reproduction_root, timestamp=timestamp),
        "ELG_grid_likelihood_holdout": elg.run_holdout(reproduction_root, timestamp=timestamp),
    }


def csv_artifact_status(path: Path) -> tuple[str, int, str]:
    if not path.exists():
        return "missing", 0, "artifact missing"
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return "malformed", 0, "missing header"
            return "pass", len(rows), ""
    except Exception as exc:  # noqa: BLE001
        return "malformed", 0, f"{type(exc).__name__}: {exc}"


def artifact_manifest_rows(run_map: dict[str, Path]) -> list[dict[str, Any]]:
    required = {
        "fresh_CC_Hz_source_locked_holdout": [
            "source_register.csv",
            "source_url_register.csv",
            "row_lock_comparison.csv",
            "data_schema.csv",
            "fit_summary.csv",
            "prior_edge_table.csv",
            "residuals.csv",
            "baseline_comparisons.csv",
            "control_reproduction.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "source_locked_growth_covariance_holdout": [
            "source_register.csv",
            "fetch_hash_lock.csv",
            "data_schema.csv",
            "branch_manifest.csv",
            "fit_summary.csv",
            "baseline_comparisons.csv",
            "control_reproduction.csv",
            "jackknife_scorecard.csv",
            "residuals.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "ELG_grid_likelihood_holdout": [
            "source_register.csv",
            "fetch_hash_lock.csv",
            "grid_schema.csv",
            "fit_summary.csv",
            "baseline_comparisons.csv",
            "control_reproduction.csv",
            "nearest_grid_offsets.csv",
            "combined_gaussian_plus_ELG_diagnostic.csv",
            "gate_results.csv",
            "decision.csv",
        ],
    }
    rows: list[dict[str, Any]] = []
    for candidate_id, run_dir in run_map.items():
        for artifact in required[candidate_id]:
            path = run_dir / "results" / artifact
            status, row_count, issue = csv_artifact_status(path)
            rows.append(
                {
                    "candidate_id": candidate_id,
                    "artifact": artifact,
                    "path": str(path),
                    "exists": "yes" if path.exists() else "no",
                    "row_count": row_count,
                    "status": status,
                    "issue": issue,
                }
            )
    return rows


def first_matching_row(rows: list[dict[str, str]], **criteria: str) -> dict[str, str] | None:
    for row in rows:
        if all(row.get(key) == value for key, value in criteria.items()):
            return row
    return None


def metric_value(run_dir: Path, candidate_id: str, metric: str) -> tuple[float, str]:
    results_dir = run_dir / "results"
    if candidate_id == "fresh_CC_Hz_source_locked_holdout":
        row = first_matching_row(
            read_csv_rows(results_dir / "baseline_comparisons.csv"),
            dataset_label="source_CC15_BC03_suggested_primary",
            model="MTS_locked_2over27",
            reference_model="LCDM",
        )
        if row is None:
            raise ValueError("missing H(z) primary LCDM comparison")
        return float(row["delta_BIC"]), row["readout"]
    if candidate_id == "source_locked_growth_covariance_holdout":
        if metric == "primary_all_delta_chi2_vs_LCDM":
            score_mode = "all"
        elif metric == "primary_fs8_delta_chi2_vs_LCDM":
            score_mode = "fs8_only"
        else:
            raise ValueError(f"unknown growth metric {metric}")
        row = first_matching_row(
            read_csv_rows(results_dir / "baseline_comparisons.csv"),
            background_branch="DR2_noCMB_primary",
            branch_label="primary_BAO_plus_all_samples",
            model="MTS_locked_2over27",
            reference_model="LCDM",
            score_mode=score_mode,
        )
        if row is None:
            raise ValueError(f"missing growth primary {score_mode} comparison")
        return float(row["delta_chi2"]), row["readout"]
    if candidate_id == "ELG_grid_likelihood_holdout":
        if metric == "primary_ELG_delta_chi2_vs_LCDM":
            row = first_matching_row(
                read_csv_rows(results_dir / "baseline_comparisons.csv"),
                background_branch="DR2_noCMB_primary",
                model="MTS_locked_2over27",
                reference_model="LCDM",
            )
            if row is None:
                raise ValueError("missing ELG primary comparison")
            return float(row["delta_chi2"]), row["readout"]
        if metric == "DR2_diagnostic_sum_delta_chi2_vs_LCDM":
            row = first_matching_row(
                read_csv_rows(results_dir / "combined_gaussian_plus_ELG_diagnostic.csv"),
                background_branch="DR2_noCMB_primary",
                combination="primary_Gaussian_BAO_plus_all_plus_ELG_grid_diagnostic",
            )
            if row is None:
                raise ValueError("missing ELG DR2 diagnostic sum")
            return float(row["sum_delta_chi2_vs_LCDM"]), row["readout"]
        raise ValueError(f"unknown ELG metric {metric}")
    raise ValueError(f"unknown candidate {candidate_id}")


def reference_metric_rows(run_map: dict[str, Path]) -> list[dict[str, Any]]:
    checks = [
        ("fresh_CC_Hz_source_locked_holdout", "primary_delta_BIC_vs_LCDM"),
        ("source_locked_growth_covariance_holdout", "primary_all_delta_chi2_vs_LCDM"),
        ("source_locked_growth_covariance_holdout", "primary_fs8_delta_chi2_vs_LCDM"),
        ("ELG_grid_likelihood_holdout", "primary_ELG_delta_chi2_vs_LCDM"),
        ("ELG_grid_likelihood_holdout", "DR2_diagnostic_sum_delta_chi2_vs_LCDM"),
    ]
    rows: list[dict[str, Any]] = []
    for candidate_id, metric in checks:
        reference_value, reference_readout = metric_value(REFERENCE_RUNS[candidate_id], candidate_id, metric)
        reproduced_value, reproduced_readout = metric_value(run_map[candidate_id], candidate_id, metric)
        absolute_error = abs(reproduced_value - reference_value)
        rows.append(
            {
                "candidate_id": candidate_id,
                "metric": metric,
                "reference_value": reference_value,
                "reproduced_value": reproduced_value,
                "absolute_error": absolute_error,
                "tolerance": TOLERANCE,
                "reference_readout": reference_readout,
                "reproduced_readout": reproduced_readout,
                "status": "pass" if absolute_error <= TOLERANCE and reference_readout == reproduced_readout else "fail",
            }
        )
    return rows


def decision_map(run_dir: Path) -> dict[str, str]:
    path = run_dir / "results" / "decision.csv"
    if not path.exists():
        return {}
    rows = read_csv_rows(path)
    return {row.get("item") or row.get("decision") or "": row.get("verdict") or row.get("value") or "" for row in rows}


def gate_audit_rows(run_map: dict[str, Path]) -> list[dict[str, Any]]:
    allowed_failures = {
        "fresh_CC_Hz_source_locked_holdout": {"theory_promotion"},
        "source_locked_growth_covariance_holdout": {"theory_promotion"},
        "ELG_grid_likelihood_holdout": {"official_joint_claim", "theory_promotion"},
    }
    rows: list[dict[str, Any]] = []
    for candidate_id, run_dir in run_map.items():
        gate_path = run_dir / "results" / "gate_results.csv"
        if not gate_path.exists():
            rows.append(
                {
                    "candidate_id": candidate_id,
                    "gate": "gate_results_present",
                    "raw_status": "missing",
                    "status": "fail",
                    "evidence": str(gate_path),
                    "hard_failure": "yes",
                }
            )
            continue
        for gate in read_csv_rows(gate_path):
            gate_name = gate["gate"]
            raw_status = gate["status"]
            hard_failure = raw_status != "pass" and gate_name not in allowed_failures[candidate_id]
            rows.append(
                {
                    "candidate_id": candidate_id,
                    "gate": gate_name,
                    "raw_status": raw_status,
                    "status": "allowed_nonpromotion_blocker" if raw_status != "pass" and not hard_failure else raw_status,
                    "evidence": gate.get("evidence", ""),
                    "hard_failure": "yes" if hard_failure else "no",
                }
            )
    return rows


def source_lock_rows(run_map: dict[str, Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for candidate_id, run_dir in run_map.items():
        decisions = decision_map(run_dir)
        fetch_path = run_dir / "results" / "fetch_hash_lock.csv"
        row_lock_path = run_dir / "results" / "row_lock_comparison.csv"
        if decisions.get("source_lock") == "pass":
            status = "pass"
            evidence = "decision source_lock=pass"
        elif fetch_path.exists():
            locks = read_csv_rows(fetch_path)
            bad = [row for row in locks if row.get("status") != "pass"]
            status = "pass" if not bad else "fail"
            evidence = f"fetch_hash_rows={len(locks)}; bad={len(bad)}"
        elif row_lock_path.exists():
            locks = read_csv_rows(row_lock_path)
            bad = [row for row in locks if row.get("status") != "pass"]
            status = "pass" if not bad else "fail"
            evidence = f"row_lock_rows={len(locks)}; bad={len(bad)}"
        else:
            status = "fail"
            evidence = "no source lock artifact"
        rows.append(
            {
                "candidate_id": candidate_id,
                "status": status,
                "evidence": evidence,
            }
        )
    return rows


def sidecar_scan_rows(run_map: dict[str, Path]) -> list[dict[str, Any]]:
    filenames = [
        "fit_summary.csv",
        "baseline_comparisons.csv",
        "decision.csv",
        "gate_results.csv",
        "combined_gaussian_plus_ELG_diagnostic.csv",
    ]
    rows: list[dict[str, Any]] = []
    for candidate_id, run_dir in run_map.items():
        hits: list[str] = []
        for filename in filenames:
            path = run_dir / "results" / filename
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8-sig", errors="ignore").lower()
            if SIDECAR_BRANCH.lower() in text or "pair_ruler" in text or "half_kernel" in text:
                hits.append(filename)
        rows.append(
            {
                "candidate_id": candidate_id,
                "status": "pass" if not hits else "fail",
                "evidence": f"hits={';'.join(hits)}",
            }
        )
    return rows


def reproduction_run_register_rows(run_map: dict[str, Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for candidate_id, run_dir in run_map.items():
        status_path = run_dir / "status.json"
        status_payload = load_json(status_path) if status_path.exists() else {}
        rows.append(
            {
                "candidate_id": candidate_id,
                "reference_run": str(REFERENCE_RUNS[candidate_id]),
                "reproduction_run": str(run_dir),
                "status": status_payload.get("status", ""),
                "claim_ceiling": status_payload.get("claim_ceiling", ""),
                "status_json_exists": "yes" if status_path.exists() else "no",
            }
        )
    return rows


def promotion_blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "scope": "H(z)",
            "blocker": "survivability only",
            "reason": "H(z) draw does not derive B_mem, local GR, CMB, or a parent action",
        },
        {
            "scope": "growth/RSD",
            "blocker": "conditional GR-proxy perturbations",
            "reason": "fair stress test but not an MTS perturbation theorem",
        },
        {
            "scope": "ELG grid",
            "blocker": "no official joint wrapper",
            "reason": "individual non-Gaussian grid reproduction is useful; Gaussian+ELG sum stays diagnostic",
        },
        {
            "scope": "full programme",
            "blocker": "CMB/local-GR/parent-action debts remain",
            "reason": "non-CMB reproduction cannot finish the fundamental field-theory case",
        },
    ]


def guard_gate_rows(
    sources: list[dict[str, Any]],
    artifacts: list[dict[str, Any]],
    metrics: list[dict[str, Any]],
    gate_audit: list[dict[str, Any]],
    locks: list[dict[str, Any]],
    sidecars: list[dict[str, Any]],
    run_register: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row for row in sources if row["exists"] != "yes"]
    bad_artifacts = [row for row in artifacts if row["status"] != "pass"]
    bad_metrics = [row for row in metrics if row["status"] != "pass"]
    hard_gate_failures = [row for row in gate_audit if row["hard_failure"] == "yes"]
    bad_locks = [row for row in locks if row["status"] != "pass"]
    bad_sidecars = [row for row in sidecars if row["status"] != "pass"]
    missing_status = [row for row in run_register if row["status_json_exists"] != "yes"]
    return [
        {
            "gate": "source_files_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
        },
        {
            "gate": "reproduction_runs_completed",
            "status": "pass" if not missing_status else "fail",
            "evidence": f"runs={len(run_register)}; missing_status={len(missing_status)}",
        },
        {
            "gate": "reproduction_artifacts_parse",
            "status": "pass" if not bad_artifacts else "fail",
            "evidence": f"bad_artifacts={len(bad_artifacts)}; artifact_rows={len(artifacts)}",
        },
        {
            "gate": "source_locks_pass",
            "status": "pass" if not bad_locks else "fail",
            "evidence": f"bad_locks={len(bad_locks)}",
        },
        {
            "gate": "reference_metrics_reproduced",
            "status": "pass" if not bad_metrics else "fail",
            "evidence": f"bad_metrics={len(bad_metrics)}; metrics={len(metrics)}; tolerance={TOLERANCE}",
        },
        {
            "gate": "hard_gates_clean_or_nonpromotion_only",
            "status": "pass" if not hard_gate_failures else "fail",
            "evidence": f"hard_gate_failures={len(hard_gate_failures)}",
        },
        {
            "gate": "sidecar_absent",
            "status": "pass" if not bad_sidecars else "fail",
            "evidence": f"sidecar_failures={len(bad_sidecars)}",
        },
        {
            "gate": "full_refresh_not_run",
            "status": "pass",
            "evidence": "only H(z), conditional growth/RSD, and ELG grid reproductions were run",
        },
        {
            "gate": "promotion_blocked_by_design",
            "status": "pass",
            "evidence": "theory_promotion and official_joint_claim failures remain allowed blockers",
        },
        {
            "gate": "claim_ceiling_preserved",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(gates: list[dict[str, Any]], metrics: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failed = [row for row in gates if row["status"] != "pass"]
    status = STATUS_PASS if not failed else STATUS_FAIL
    metric_evidence = "; ".join(f"{row['candidate_id']}:{row['metric']}={row['reproduced_value']}" for row in metrics)
    return [
        {
            "item": "status",
            "verdict": status,
            "evidence": f"failed_gates={len(failed)}",
        },
        {
            "item": "reproduced_metrics",
            "verdict": len(metrics),
            "evidence": metric_evidence,
        },
        {
            "item": "lead_branch",
            "verdict": LEAD_BRANCH,
            "evidence": "source-locked non-CMB lanes retain locked 2/27/no-clock branch framing",
        },
        {
            "item": "claim_ceiling",
            "verdict": CLAIM_CEILING,
            "evidence": "no full official likelihood, CMB pass, local-GR derivation, or parent-action promotion",
        },
        {
            "item": "next_target",
            "verdict": "176-official-refresh-decision-gate.md",
            "evidence": "decide whether to implement broader official refresh now or return to parent-action/perturbation derivation",
        },
    ]


def run_guard(output_root: Path, timestamp: str | None, reference_tolerance: float) -> Path:
    global TOLERANCE
    TOLERANCE = reference_tolerance
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-no-clock-nonCMB-reproduction-guard"
    results_dir = run_dir / "results"
    reproduction_root = run_dir / "reproduction-runs"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    if any(row["exists"] != "yes" for row in sources):
        missing = [row["path"] for row in sources if row["exists"] != "yes"]
        raise FileNotFoundError(f"missing required source files: {missing}")

    run_map = run_reproductions(reproduction_root, run_stamp)
    run_register = reproduction_run_register_rows(run_map)
    artifacts = artifact_manifest_rows(run_map)
    metrics = reference_metric_rows(run_map)
    gate_audit = gate_audit_rows(run_map)
    locks = source_lock_rows(run_map)
    sidecars = sidecar_scan_rows(run_map)
    blockers = promotion_blocker_rows()
    gates = guard_gate_rows(sources, artifacts, metrics, gate_audit, locks, sidecars, run_register)
    decisions = decision_rows(gates, metrics)
    status = decisions[0]["verdict"]

    write_json(
        run_dir / "run_config.json",
        {
            "timestamp": run_stamp,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "readiness_run": str(READINESS_RUN),
            "reference_tolerance": TOLERANCE,
            "reproduction_root": str(reproduction_root),
            "candidates": list(REFERENCE_RUNS),
        },
    )
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(results_dir / "reproduction_run_register.csv", run_register, ["candidate_id", "reference_run", "reproduction_run", "status", "claim_ceiling", "status_json_exists"])
    write_csv(results_dir / "artifact_manifest.csv", artifacts, ["candidate_id", "artifact", "path", "exists", "row_count", "status", "issue"])
    write_csv(results_dir / "source_lock_audit.csv", locks, ["candidate_id", "status", "evidence"])
    write_csv(results_dir / "reference_metric_check.csv", metrics, ["candidate_id", "metric", "reference_value", "reproduced_value", "absolute_error", "tolerance", "reference_readout", "reproduced_readout", "status"])
    write_csv(results_dir / "candidate_gate_audit.csv", gate_audit, ["candidate_id", "gate", "raw_status", "status", "evidence", "hard_failure"])
    write_csv(results_dir / "sidecar_scan.csv", sidecars, ["candidate_id", "status", "evidence"])
    write_csv(results_dir / "promotion_blockers.csv", blockers, ["scope", "blocker", "reason"])
    write_csv(results_dir / "guard_gates.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])
    write_json(
        run_dir / "status.json",
        {
            "status": status,
            "run_dir": str(run_dir),
            "results_dir": str(results_dir),
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "failed_gates": [row["gate"] for row in gates if row["status"] != "pass"],
            "reproduced_candidates": list(run_map),
            "promotion_allowed": False,
            "next_target": "176-official-refresh-decision-gate.md",
            "generated": [
                "source_register.csv",
                "reproduction_run_register.csv",
                "artifact_manifest.csv",
                "source_lock_audit.csv",
                "reference_metric_check.csv",
                "candidate_gate_audit.csv",
                "sidecar_scan.csv",
                "promotion_blockers.csv",
                "guard_gates.csv",
                "decision.csv",
            ],
        },
    )
    marker = "DONE.txt" if status == STATUS_PASS else "FAILED.txt"
    (run_dir / marker).write_text(f"{status}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--reference-tolerance", type=float, default=TOLERANCE)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_guard(args.output_root, args.timestamp, args.reference_tolerance))


if __name__ == "__main__":
    main()
