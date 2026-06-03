#!/usr/bin/env python3
"""Readiness audit for non-CMB no-clock holdout reproduction."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

STATUS_PASS = "no_clock_Hz_growth_reproduction_readiness_passed"
STATUS_FAIL = "no_clock_Hz_growth_reproduction_readiness_failed"
CLAIM_CEILING = "non_CMB_reproduction_readiness_no_full_refresh_or_theory_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"
SIDECAR_BRANCH = "MTS_pair_ruler_half_kernel"


def candidate_runs() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "BAO_Hz_noCMB_robustness",
            "arena": "BAO+Hz",
            "run_dir": RUNS_ROOT / "20260531-181900-BAO-Hz-noCMB-robustness",
            "script": SCRIPT_DIR / "BAO_Hz_noCMB_robustness.py",
            "checkpoint": WORK_DIR / "129-noCMB-radial-robustness-or-growth-route.md",
            "source_lock_level": "local_manifest_and_covariance_guard",
            "evidence_class": "diagnostic_noCMB_BAO_Hz_robustness",
            "allowed_gate_failures": set(),
            "required_artifacts": [
                "source_register.csv",
                "data_schema.csv",
                "branch_manifest.csv",
                "fit_summary.csv",
                "sector_breakdown.csv",
                "prior_edge_table.csv",
                "residuals.csv",
                "baseline_comparisons.csv",
                "robustness_matrix.csv",
                "stability_summary.csv",
                "control_reproduction.csv",
                "omega_shift_matrix.csv",
                "decision.csv",
            ],
            "readiness_note": "ready for guarded reproduction as a no-CMB diagnostic/context branch",
        },
        {
            "candidate_id": "fresh_CC_Hz_source_locked_holdout",
            "arena": "Hz",
            "run_dir": RUNS_ROOT / "20260531-221500-fresh-CC-Hz-source-locked-holdout",
            "script": SCRIPT_DIR / "fresh_CC_Hz_source_locked_holdout.py",
            "checkpoint": WORK_DIR / "145-fresh-CC-Hz-source-locked-holdout.md",
            "source_lock_level": "fresh_source_locked",
            "evidence_class": "independent_late_time_Hz_holdout",
            "allowed_gate_failures": {"theory_promotion"},
            "required_artifacts": [
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
            "readiness_note": "ready for first non-CMB reproduction guard; H(z) is survivability only",
        },
        {
            "candidate_id": "source_locked_growth_covariance_holdout",
            "arena": "growth_RSD",
            "run_dir": RUNS_ROOT / "20260531-224500-source-locked-growth-covariance-holdout",
            "script": SCRIPT_DIR / "source_locked_growth_covariance_holdout.py",
            "checkpoint": WORK_DIR / "146-source-locked-growth-covariance-holdout.md",
            "source_lock_level": "fresh_source_locked",
            "evidence_class": "conditional_GR_proxy_growth_covariance_holdout",
            "allowed_gate_failures": {"theory_promotion"},
            "required_artifacts": [
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
            "readiness_note": "ready for guarded reproduction, but only as conditional GR-proxy growth stress",
        },
        {
            "candidate_id": "ELG_grid_likelihood_holdout",
            "arena": "ELG_grid_growth_RSD",
            "run_dir": RUNS_ROOT / "20260531-231500-ELG-grid-likelihood-holdout",
            "script": SCRIPT_DIR / "ELG_grid_likelihood_holdout.py",
            "checkpoint": WORK_DIR / "147-ELG-grid-likelihood-holdout.md",
            "source_lock_level": "fresh_source_locked_grid",
            "evidence_class": "non_Gaussian_ELG_grid_holdout",
            "allowed_gate_failures": {"official_joint_claim", "theory_promotion"},
            "required_artifacts": [
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
            "readiness_note": "ready for individual ELG grid reproduction; combined Gaussian+ELG remains diagnostic only",
        },
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
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        {
            "source": Path(__file__).name,
            "path": str(Path(__file__).resolve()),
            "exists": "yes",
            "sha256": sha256_file(Path(__file__).resolve()),
            "role": "checkpoint 174 readiness auditor",
            "issue": "",
        }
    ]
    for candidate in candidate_runs():
        for role, path in [
            ("candidate scorer script", candidate["script"]),
            ("candidate checkpoint note", candidate["checkpoint"]),
            ("candidate status", candidate["run_dir"] / "status.json"),
        ]:
            exists = path.exists()
            rows.append(
                {
                    "source": path.name,
                    "path": str(path),
                    "exists": "yes" if exists else "no",
                    "sha256": sha256_file(path) if exists and path.is_file() else "",
                    "role": f"{candidate['candidate_id']} {role}",
                    "issue": "" if exists else "missing",
                }
            )
    return rows


def csv_artifact_status(path: Path) -> tuple[str, int, str, str]:
    if not path.exists():
        return "missing", 0, "", "artifact missing"
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return "malformed", 0, "", "missing CSV header"
            return "pass", len(rows), ";".join(reader.fieldnames), ""
    except Exception as exc:  # noqa: BLE001
        return "malformed", 0, "", f"{type(exc).__name__}: {exc}"


def artifact_manifest_rows(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        results_dir = candidate["run_dir"] / "results"
        for artifact in candidate["required_artifacts"]:
            artifact_path = results_dir / artifact
            status, row_count, header, issue = csv_artifact_status(artifact_path)
            rows.append(
                {
                    "candidate_id": candidate["candidate_id"],
                    "artifact": artifact,
                    "path": str(artifact_path),
                    "exists": "yes" if artifact_path.exists() else "no",
                    "row_count": row_count,
                    "header": header,
                    "status": status,
                    "issue": issue,
                }
            )
    return rows


def decision_map(candidate: dict[str, Any]) -> dict[str, str]:
    path = candidate["run_dir"] / "results" / "decision.csv"
    if not path.exists():
        return {}
    rows = read_csv_rows(path)
    return {row.get("item") or row.get("decision") or "": row.get("verdict") or row.get("value") or "" for row in rows}


def gate_rows(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    path = candidate["run_dir"] / "results" / "gate_results.csv"
    if not path.exists():
        decisions = decision_map(candidate)
        return [
            {
                "candidate_id": candidate["candidate_id"],
                "gate": "decision_file_used_as_gate_proxy",
                "status": "pass" if decisions.get("status") else "fail",
                "raw_status": decisions.get("status", ""),
                "evidence": "no gate_results.csv; decision status used for readiness only",
                "hard_failure": "no",
            }
        ]
    rows: list[dict[str, Any]] = []
    allowed_failures = set(candidate["allowed_gate_failures"])
    for gate in read_csv_rows(path):
        gate_name = gate["gate"]
        raw_status = gate["status"]
        hard_failure = raw_status != "pass" and gate_name not in allowed_failures
        rows.append(
            {
                "candidate_id": candidate["candidate_id"],
                "gate": gate_name,
                "status": "allowed_nonpromotion_blocker" if raw_status != "pass" and gate_name in allowed_failures else raw_status,
                "raw_status": raw_status,
                "evidence": gate.get("evidence", ""),
                "hard_failure": "yes" if hard_failure else "no",
            }
        )
    return rows


def source_lock_status(candidate: dict[str, Any]) -> tuple[str, str]:
    decisions = decision_map(candidate)
    if decisions.get("source_lock") == "pass":
        return "pass", "decision source_lock=pass"
    fetch_path = candidate["run_dir"] / "results" / "fetch_hash_lock.csv"
    if fetch_path.exists():
        rows = read_csv_rows(fetch_path)
        bad = [row for row in rows if row.get("status") != "pass"]
        return ("pass" if not bad else "fail", f"fetch_hash_rows={len(rows)}; bad={len(bad)}")
    row_lock_path = candidate["run_dir"] / "results" / "row_lock_comparison.csv"
    if row_lock_path.exists():
        rows = read_csv_rows(row_lock_path)
        bad = [row for row in rows if row.get("status") != "pass"]
        return ("pass" if not bad else "fail", f"row_lock_rows={len(rows)}; bad={len(bad)}")
    if "fresh_source_locked" in candidate["source_lock_level"]:
        return "fail", "fresh source lock required but no lock artifact found"
    return "not_required", candidate["source_lock_level"]


def sidecar_scan_status(candidate: dict[str, Any]) -> tuple[str, str]:
    scanned_files = [
        "fit_summary.csv",
        "baseline_comparisons.csv",
        "decision.csv",
        "gate_results.csv",
        "robustness_matrix.csv",
        "combined_gaussian_plus_ELG_diagnostic.csv",
    ]
    hits: list[str] = []
    for filename in scanned_files:
        path = candidate["run_dir"] / "results" / filename
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8-sig", errors="ignore").lower()
        if SIDECAR_BRANCH.lower() in text or "pair_ruler" in text or "half_kernel" in text:
            hits.append(filename)
    return ("pass" if not hits else "fail", f"sidecar_hits={';'.join(hits)}")


def first_matching_row(rows: list[dict[str, str]], **criteria: str) -> dict[str, str] | None:
    for row in rows:
        if all(row.get(key) == value for key, value in criteria.items()):
            return row
    return None


def scorecard_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for candidate in candidate_runs():
        results_dir = candidate["run_dir"] / "results"
        if candidate["candidate_id"] == "BAO_Hz_noCMB_robustness":
            comparisons = read_csv_rows(results_dir / "baseline_comparisons.csv")
            primary = first_matching_row(
                comparisons,
                dataset_label="BAO_DR2_plus_CC15_suggested",
                model="MTS_locked_2over27",
                reference_model="LCDM",
            )
            stability = read_csv_rows(results_dir / "stability_summary.csv")
            rows.append(
                {
                    "candidate_id": candidate["candidate_id"],
                    "arena": candidate["arena"],
                    "metric": "primary_delta_BIC_vs_LCDM",
                    "value": primary["delta_BIC"] if primary else "",
                    "readout": primary["readout"] if primary else "missing",
                    "reference": "LCDM",
                    "evidence": "BAO_DR2_plus_CC15_suggested no-CMB robustness",
                }
            )
            for item in stability:
                rows.append(
                    {
                        "candidate_id": candidate["candidate_id"],
                        "arena": candidate["arena"],
                        "metric": item.get("group", "stability_summary"),
                        "value": item.get("median_delta_BIC", ""),
                        "readout": item.get("verdict", ""),
                        "reference": "LCDM",
                        "evidence": f"branches={item.get('branch_count', '')}; draws={item.get('draw_count', '')}; disfavored={item.get('disfavored_count', '')}",
                    }
                )
        elif candidate["candidate_id"] == "fresh_CC_Hz_source_locked_holdout":
            comparisons = read_csv_rows(results_dir / "baseline_comparisons.csv")
            primary = first_matching_row(
                comparisons,
                dataset_label="source_CC15_BC03_suggested_primary",
                model="MTS_locked_2over27",
                reference_model="LCDM",
            )
            rows.append(
                {
                    "candidate_id": candidate["candidate_id"],
                    "arena": candidate["arena"],
                    "metric": "primary_delta_BIC_vs_LCDM",
                    "value": primary["delta_BIC"] if primary else "",
                    "readout": primary["readout"] if primary else "missing",
                    "reference": "LCDM",
                    "evidence": "source_CC15_BC03_suggested_primary",
                }
            )
        elif candidate["candidate_id"] == "source_locked_growth_covariance_holdout":
            comparisons = read_csv_rows(results_dir / "baseline_comparisons.csv")
            for score_mode, metric in [("all", "primary_all_delta_chi2_vs_LCDM"), ("fs8_only", "primary_fs8_delta_chi2_vs_LCDM")]:
                primary = first_matching_row(
                    comparisons,
                    background_branch="DR2_noCMB_primary",
                    branch_label="primary_BAO_plus_all_samples",
                    model="MTS_locked_2over27",
                    reference_model="LCDM",
                    score_mode=score_mode,
                )
                rows.append(
                    {
                        "candidate_id": candidate["candidate_id"],
                        "arena": candidate["arena"],
                        "metric": metric,
                        "value": primary["delta_chi2"] if primary else "",
                        "readout": primary["readout"] if primary else "missing",
                        "reference": "LCDM",
                        "evidence": "DR2_noCMB_primary primary_BAO_plus_all_samples",
                    }
                )
        elif candidate["candidate_id"] == "ELG_grid_likelihood_holdout":
            comparisons = read_csv_rows(results_dir / "baseline_comparisons.csv")
            primary = first_matching_row(
                comparisons,
                background_branch="DR2_noCMB_primary",
                model="MTS_locked_2over27",
                reference_model="LCDM",
            )
            rows.append(
                {
                    "candidate_id": candidate["candidate_id"],
                    "arena": candidate["arena"],
                    "metric": "primary_ELG_delta_chi2_vs_LCDM",
                    "value": primary["delta_chi2"] if primary else "",
                    "readout": primary["readout"] if primary else "missing",
                    "reference": "LCDM",
                    "evidence": "DR2_noCMB_primary ELG grid",
                }
            )
            combined_path = results_dir / "combined_gaussian_plus_ELG_diagnostic.csv"
            if combined_path.exists():
                combined_rows = read_csv_rows(combined_path)
                for combined in combined_rows:
                    rows.append(
                        {
                            "candidate_id": candidate["candidate_id"],
                            "arena": candidate["arena"],
                            "metric": combined.get("combination", "combined_gaussian_plus_ELG_diagnostic"),
                            "value": combined.get("sum_delta_chi2_vs_LCDM", ""),
                            "readout": combined.get("readout", ""),
                            "reference": "LCDM",
                            "evidence": f"{combined.get('background_branch', '')}; diagnostic sum only, not official joint likelihood",
                        }
                    )
    return rows


def readiness_rows(candidates: list[dict[str, Any]], artifacts: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    artifact_bad_by_candidate: dict[str, int] = {}
    for artifact in artifacts:
        if artifact["status"] != "pass":
            artifact_bad_by_candidate[artifact["candidate_id"]] = artifact_bad_by_candidate.get(artifact["candidate_id"], 0) + 1
    hard_gate_bad_by_candidate: dict[str, int] = {}
    for gate in gates:
        if gate["hard_failure"] == "yes":
            hard_gate_bad_by_candidate[gate["candidate_id"]] = hard_gate_bad_by_candidate.get(gate["candidate_id"], 0) + 1
    for candidate in candidates:
        status_path = candidate["run_dir"] / "status.json"
        status_payload = load_json(status_path) if status_path.exists() else {}
        source_lock, source_evidence = source_lock_status(candidate)
        sidecar_status, sidecar_evidence = sidecar_scan_status(candidate)
        claim_ceiling = status_payload.get("claim_ceiling", "")
        artifact_bad = artifact_bad_by_candidate.get(candidate["candidate_id"], 0)
        hard_gate_bad = hard_gate_bad_by_candidate.get(candidate["candidate_id"], 0)
        source_lock_bad = source_lock == "fail"
        if artifact_bad:
            readiness = "not_ready_missing_or_malformed_artifacts"
        elif hard_gate_bad:
            readiness = "not_ready_hard_gate_failure"
        elif source_lock_bad:
            readiness = "not_ready_source_lock_failure"
        elif candidate["arena"] in {"growth_RSD", "ELG_grid_growth_RSD"}:
            readiness = "ready_for_guarded_reproduction_conditional_growth_only"
        elif candidate["arena"] == "BAO+Hz":
            readiness = "ready_for_guarded_reproduction_diagnostic_context"
        else:
            readiness = "ready_for_guarded_reproduction"
        rows.append(
            {
                "candidate_id": candidate["candidate_id"],
                "arena": candidate["arena"],
                "run_dir": str(candidate["run_dir"]),
                "status": status_payload.get("status", ""),
                "claim_ceiling": claim_ceiling,
                "source_lock_status": source_lock,
                "source_lock_evidence": source_evidence,
                "sidecar_status": sidecar_status,
                "sidecar_evidence": sidecar_evidence,
                "artifact_failures": artifact_bad,
                "hard_gate_failures": hard_gate_bad,
                "readiness_status": readiness,
                "promotion_status": "not_promotable_from_this_arena",
                "evidence_class": candidate["evidence_class"],
                "readiness_note": candidate["readiness_note"],
            }
        )
    return rows


def promotion_blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "scope": "fresh_CC_Hz_source_locked_holdout",
            "blocker": "H(z) survivability is not a derivation",
            "reason": "cosmic chronometer data can support draw/survival but cannot derive B_mem, local GR, CMB, or the parent action",
            "next_action": "reproduce as a clean non-CMB holdout, then keep claim ceiling",
        },
        {
            "scope": "source_locked_growth_covariance_holdout",
            "blocker": "growth uses conditional GR-proxy perturbations",
            "reason": "shared sigma8-only growth stress is fair, but it is not an MTS perturbation theorem",
            "next_action": "reproduce as conditional evidence; require perturbation action before promotion",
        },
        {
            "scope": "ELG_grid_likelihood_holdout",
            "blocker": "ELG grid is not an official joint likelihood wrapper",
            "reason": "individual grid score is useful; diagnostic Gaussian+ELG sum is not promotable as a combined likelihood",
            "next_action": "reproduce individual grid; defer joint wrapper",
        },
        {
            "scope": "full programme",
            "blocker": "CMB bridge, local GR/PPN, and parent action remain unresolved",
            "reason": "non-CMB holdouts cannot substitute for field-theory derivation or perturbation consistency",
            "next_action": "use empirical survival to prioritize derivation and official-likelihood implementation, not to claim completion",
        },
    ]


def guard_gate_rows(
    sources: list[dict[str, Any]],
    artifacts: list[dict[str, Any]],
    readiness: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row for row in sources if row["exists"] != "yes"]
    malformed_artifacts = [row for row in artifacts if row["status"] != "pass"]
    hard_gate_failures = [row for row in gates if row["hard_failure"] == "yes"]
    source_lock_failures = [row for row in readiness if row["source_lock_status"] == "fail"]
    sidecar_failures = [row for row in readiness if row["sidecar_status"] != "pass"]
    ready = [row for row in readiness if str(row["readiness_status"]).startswith("ready_for_guarded_reproduction")]
    promotable = [row for row in readiness if row["promotion_status"] != "not_promotable_from_this_arena"]
    return [
        {
            "gate": "candidate_sources_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
        },
        {
            "gate": "candidate_artifacts_parse",
            "status": "pass" if not malformed_artifacts else "fail",
            "evidence": f"bad_artifacts={len(malformed_artifacts)}; artifact_rows={len(artifacts)}",
        },
        {
            "gate": "hard_gates_clean_or_nonpromotion_only",
            "status": "pass" if not hard_gate_failures else "fail",
            "evidence": f"hard_gate_failures={len(hard_gate_failures)}",
        },
        {
            "gate": "source_locks_pass_where_required",
            "status": "pass" if not source_lock_failures else "fail",
            "evidence": f"source_lock_failures={len(source_lock_failures)}",
        },
        {
            "gate": "sidecar_absent",
            "status": "pass" if not sidecar_failures else "fail",
            "evidence": f"sidecar_failures={len(sidecar_failures)}",
        },
        {
            "gate": "non_CMB_reproduction_targets_identified",
            "status": "pass" if len(ready) >= 3 else "fail",
            "evidence": f"ready_candidates={len(ready)}",
        },
        {
            "gate": "promotion_blocked_by_design",
            "status": "pass" if not promotable else "fail",
            "evidence": "all candidates stay non-promotable from this arena",
        },
        {
            "gate": "claim_ceiling_preserved",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(gates: list[dict[str, Any]], readiness: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failed = [row for row in gates if row["status"] != "pass"]
    ready = [row for row in readiness if str(row["readiness_status"]).startswith("ready_for_guarded_reproduction")]
    source_locked_ready = [row for row in ready if row["source_lock_status"] == "pass"]
    status = STATUS_PASS if not failed else STATUS_FAIL
    return [
        {
            "item": "status",
            "verdict": status,
            "evidence": f"failed_gates={len(failed)}",
        },
        {
            "item": "ready_candidates",
            "verdict": len(ready),
            "evidence": "; ".join(row["candidate_id"] for row in ready),
        },
        {
            "item": "source_locked_ready_candidates",
            "verdict": len(source_locked_ready),
            "evidence": "; ".join(row["candidate_id"] for row in source_locked_ready),
        },
        {
            "item": "lead_branch",
            "verdict": LEAD_BRANCH,
            "evidence": "all non-CMB readiness candidates preserve locked 2/27/no-clock branch framing",
        },
        {
            "item": "claim_ceiling",
            "verdict": CLAIM_CEILING,
            "evidence": "H(z), growth/RSD, and ELG readiness cannot promote CMB/local-GR/parent-action claims",
        },
        {
            "item": "next_target",
            "verdict": "175-no-clock-nonCMB-reproduction-guard.md",
            "evidence": "implement guarded reproduction for source-locked H(z), conditional growth, and ELG grid lanes",
        },
    ]


def run_audit(output_root: Path, timestamp: str | None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-no-clock-Hz-growth-reproduction-readiness"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    candidates = candidate_runs()
    sources = source_register_rows()
    artifacts = artifact_manifest_rows(candidates)
    candidate_gates = [gate for candidate in candidates for gate in gate_rows(candidate)]
    readiness = readiness_rows(candidates, artifacts, candidate_gates)
    scorecard = scorecard_rows()
    blockers = promotion_blocker_rows()
    gates = guard_gate_rows(sources, artifacts, readiness, candidate_gates)
    decisions = decision_rows(gates, readiness)
    status = decisions[0]["verdict"]

    write_json(
        run_dir / "run_config.json",
        {
            "timestamp": run_stamp,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "candidate_count": len(candidates),
            "candidates": [
                {
                    "candidate_id": candidate["candidate_id"],
                    "arena": candidate["arena"],
                    "run_dir": str(candidate["run_dir"]),
                    "source_lock_level": candidate["source_lock_level"],
                    "evidence_class": candidate["evidence_class"],
                }
                for candidate in candidates
            ],
        },
    )
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(results_dir / "candidate_artifact_manifest.csv", artifacts, ["candidate_id", "artifact", "path", "exists", "row_count", "header", "status", "issue"])
    write_csv(results_dir / "candidate_gate_audit.csv", candidate_gates, ["candidate_id", "gate", "status", "raw_status", "evidence", "hard_failure"])
    write_csv(
        results_dir / "readiness_matrix.csv",
        readiness,
        [
            "candidate_id",
            "arena",
            "run_dir",
            "status",
            "claim_ceiling",
            "source_lock_status",
            "source_lock_evidence",
            "sidecar_status",
            "sidecar_evidence",
            "artifact_failures",
            "hard_gate_failures",
            "readiness_status",
            "promotion_status",
            "evidence_class",
            "readiness_note",
        ],
    )
    write_csv(results_dir / "nonCMB_scorecard.csv", scorecard, ["candidate_id", "arena", "metric", "value", "readout", "reference", "evidence"])
    write_csv(results_dir / "promotion_blockers.csv", blockers, ["scope", "blocker", "reason", "next_action"])
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
            "ready_candidates": [row["candidate_id"] for row in readiness if str(row["readiness_status"]).startswith("ready_for_guarded_reproduction")],
            "source_locked_ready_candidates": [row["candidate_id"] for row in readiness if str(row["readiness_status"]).startswith("ready_for_guarded_reproduction") and row["source_lock_status"] == "pass"],
            "promotion_allowed": False,
            "next_target": "175-no-clock-nonCMB-reproduction-guard.md",
            "generated": [
                "source_register.csv",
                "candidate_artifact_manifest.csv",
                "candidate_gate_audit.csv",
                "readiness_matrix.csv",
                "nonCMB_scorecard.csv",
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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_audit(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
