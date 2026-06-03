#!/usr/bin/env python3
"""Checkpoint 201: BAO strict-alpha results and H0-r_d owner decision."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_201_NAME = "BAO-strict-alpha-results-and-H0-rd-owner-decision"
CHECKPOINT_200_RUN = RUNS_ROOT / "20260601-000017-BAO-strict-alpha-shape-stress-or-parent-H0-rd-contract"
CHECKPOINT_199_RUN = RUNS_ROOT / "20260601-000016-BAO-alpha-parent-or-shared-nuisance-policy"
CHECKPOINT_195_RUN = RUNS_ROOT / "20260601-000012-late-CMB-domain-rule-and-local-silence-gate"

STATUS = "BAO_alpha_domain_decision_late_common_mode_candidate_CMB_endpoint_alpha_demoted"
CLAIM_CEILING = "BAO_alpha_domain_decision_internal_only_parent_H0_rd_owner_missing"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"


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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 201 BAO alpha owner decision script"),
        (WORK_DIR / "200-BAO-strict-alpha-shape-stress-or-parent-H0-rd-contract.md", "strict alpha shape stress checkpoint"),
        (CHECKPOINT_200_RUN / "status.json", "checkpoint 200 machine status"),
        (CHECKPOINT_200_RUN / "results" / "alpha_candidate_scorecard.csv", "checkpoint 200 alpha candidate scorecard"),
        (CHECKPOINT_200_RUN / "results" / "alpha_candidate_manifest.csv", "checkpoint 200 alpha candidate manifest"),
        (CHECKPOINT_200_RUN / "results" / "claim_gate_results.csv", "checkpoint 200 gates"),
        (WORK_DIR / "199-BAO-alpha-parent-or-shared-nuisance-policy.md", "alpha shared-nuisance policy checkpoint"),
        (CHECKPOINT_199_RUN / "status.json", "checkpoint 199 machine status"),
        (WORK_DIR / "195-late-CMB-domain-rule-and-local-silence-gate.md", "endpoint domain rule checkpoint"),
        (CHECKPOINT_195_RUN / "status.json", "checkpoint 195 machine status"),
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


def release_consistency_rows(scorecard: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in scorecard:
        grouped[row["alpha_candidate"]].append(row)
    rows: list[dict[str, Any]] = []
    verdict_rank = {
        "strict_alpha_survives": 0,
        "strict_alpha_soft_warning": 1,
        "strict_alpha_pressure": 2,
    }
    for alpha_candidate, alpha_rows in sorted(grouped.items()):
        releases = ";".join(sorted(row["release"] for row in alpha_rows))
        worst_row = max(alpha_rows, key=lambda row: verdict_rank[row["verdict"]])
        total_delta = sum(float(row["locked_delta_chi2_vs_shared_alpha"]) for row in alpha_rows)
        max_delta = max(float(row["locked_delta_chi2_vs_shared_alpha"]) for row in alpha_rows)
        if all(row["verdict"] == "strict_alpha_survives" for row in alpha_rows):
            decision = "release_stable_survivor"
        elif worst_row["verdict"] == "strict_alpha_soft_warning":
            decision = "late_domain_candidate_with_DR2_warning"
        else:
            decision = "demote_for_BAO_alpha_owner"
        rows.append(
            {
                "alpha_candidate": alpha_candidate,
                "releases": releases,
                "worst_verdict": worst_row["verdict"],
                "max_delta_chi2_vs_shared_alpha": max_delta,
                "sum_delta_chi2_vs_shared_alpha": total_delta,
                "release_consistency_decision": decision,
            }
        )
    return rows


def H0_rd_owner_option_rows(consistency_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    consistency = {row["alpha_candidate"]: row for row in consistency_rows}
    candidate_meanings = {
        "DR1_locked_fit_readback": "BAO readback calibration from DESI DR1 locked branch",
        "DR2_locked_fit_readback": "BAO readback calibration from DESI DR2 locked branch",
        "late_reference_H0_rdrag": "late-reference H0 times CAMB rdrag",
        "same_density_CMB_profile_H0_rdrag": "same-density CMB-profile H0 times CAMB rdrag",
        "exp_half_memory_H0_rdrag": "half-memory CMB-bridged H0 times CAMB rdrag",
    }
    rows: list[dict[str, Any]] = []
    for alpha_candidate, meaning in sorted(candidate_meanings.items()):
        row = consistency[alpha_candidate]
        if alpha_candidate in {"same_density_CMB_profile_H0_rdrag", "exp_half_memory_H0_rdrag"}:
            owner_decision = "demoted_for_BAO_domain"
            reason = "strict-alpha pressure in both DR1 and DR2; BAO should not use CMB endpoint-jump alpha"
        elif "readback" in alpha_candidate:
            owner_decision = "empirical_anchor_not_parent_owner"
            reason = "release-stable survivor, but readback cannot become a prediction after seeing BAO"
        elif alpha_candidate == "late_reference_H0_rdrag":
            owner_decision = "lead_theorem_candidate_with_warning"
            reason = "survives DR1 and only soft-warns DR2; matches late common-mode domain logic"
        else:
            owner_decision = "unclassified"
            reason = "no rule"
        rows.append(
            {
                "alpha_candidate": alpha_candidate,
                "meaning": meaning,
                "worst_verdict": row["worst_verdict"],
                "max_delta_chi2_vs_shared_alpha": row["max_delta_chi2_vs_shared_alpha"],
                "owner_decision": owner_decision,
                "reason": reason,
            }
        )
    return rows


def domain_assignment_rows() -> list[dict[str, Any]]:
    return [
        {
            "observable_domain": "CMB acoustic angle",
            "endpoint_class": "early-to-late",
            "allowed_calibration": "half-memory clock bridge for theta/H0 profiling",
            "forbidden_calibration": "using BAO late-alpha readback as CMB proof",
            "status": "candidate_endpoint_jump_domain",
        },
        {
            "observable_domain": "BAO ratios",
            "endpoint_class": "late common-mode ruler calibration",
            "allowed_calibration": "late-reference or parent-derived late H0-r_d alpha",
            "forbidden_calibration": "CMB-profile or half-memory endpoint-jump alpha",
            "status": "lead_BAO_domain_assignment",
        },
        {
            "observable_domain": "SN/local ladder",
            "endpoint_class": "late local common-mode",
            "allowed_calibration": "late calibration if local/environmental silence holds",
            "forbidden_calibration": "unscreened global clock drift leaking locally",
            "status": "conditional_on_local_silence",
        },
        {
            "observable_domain": "growth",
            "endpoint_class": "path-dependent perturbation history",
            "allowed_calibration": "none from endpoint algebra alone",
            "forbidden_calibration": "borrowing background alpha/theta rules without perturbation owner",
            "status": "not_closed",
        },
    ]


def parent_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract": "late common-mode BAO alpha owner",
            "required_derivation": "show BAO uses late matter-unit H0-r_d calibration rather than CMB endpoint-jump calibration",
            "current_evidence": "late/readback alpha survives; CMB/half-memory alpha pressured",
            "status": "lead_theorem_target",
        },
        {
            "contract": "readback quarantine",
            "required_derivation": "prevent DR1/DR2 fit readbacks from becoming retroactive predictions",
            "current_evidence": "readbacks survive by construction or near-construction",
            "status": "guardrail_required",
        },
        {
            "contract": "release-independent alpha prediction",
            "required_derivation": "derive one alpha or controlled release-independent calibration before BAO scoring",
            "current_evidence": "DR1 and DR2 readbacks differ by about 0.091 in alpha",
            "status": "missing",
        },
        {
            "contract": "local silence consistency",
            "required_derivation": "same late common-mode rule must not introduce local clock/PPN drift",
            "current_evidence": "previous checkpoints require partial_mu C -> 0 and dot_C -> 0 locally",
            "status": "still_open",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]], consistency_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    demoted = [row for row in consistency_rows if row["release_consistency_decision"] == "demote_for_BAO_alpha_owner"]
    lead_candidate = [row for row in consistency_rows if row["release_consistency_decision"] == "late_domain_candidate_with_DR2_warning"]
    survivors = [row for row in consistency_rows if row["release_consistency_decision"] == "release_stable_survivor"]
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal decision gate",
        },
        {
            "gate": "CMB/half-memory alpha demoted for BAO",
            "status": "pass" if len(demoted) >= 2 else "fail",
            "evidence": f"demoted_candidates={len(demoted)}",
            "claim_allowed": "domain assignment guardrail",
        },
        {
            "gate": "late common-mode alpha candidate retained",
            "status": "pass" if lead_candidate else "warning",
            "evidence": f"lead_candidates={len(lead_candidate)}",
            "claim_allowed": "theorem target",
        },
        {
            "gate": "readbacks quarantined",
            "status": "pass" if survivors else "warning",
            "evidence": f"release_stable_readback_like_survivors={len(survivors)}",
            "claim_allowed": "empirical anchors only",
        },
        {
            "gate": "parent H0-r_d owner derived",
            "status": "fail",
            "evidence": "late common-mode owner is selected as theorem target, not derived",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "BAO support claim allowed",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows(consistency_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lead = next(row for row in consistency_rows if row["alpha_candidate"] == "late_reference_H0_rdrag")
    demoted_count = sum(row["release_consistency_decision"] == "demote_for_BAO_alpha_owner" for row in consistency_rows)
    survivor_count = sum(row["release_consistency_decision"] == "release_stable_survivor" for row in consistency_rows)
    return [
        {
            "decision": STATUS,
            "meaning": "BAO alpha ownership is assigned to the late common-mode theorem route. CMB-profile and half-memory endpoint-jump alpha are demoted for BAO. Readbacks remain empirical anchors, not predictions.",
            "lead_alpha_candidate": "late_reference_H0_rdrag",
            "lead_alpha_worst_verdict": lead["worst_verdict"],
            "lead_alpha_max_delta_chi2_vs_shared_alpha": lead["max_delta_chi2_vs_shared_alpha"],
            "demoted_alpha_candidate_count": demoted_count,
            "readback_survivor_count": survivor_count,
            "next_target": "202-late-common-mode-H0-rd-owner-derivation-attempt.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_201_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    scorecard = read_csv_rows(CHECKPOINT_200_RUN / "results" / "alpha_candidate_scorecard.csv")
    consistency = release_consistency_rows(scorecard)
    owner_options = H0_rd_owner_option_rows(consistency)
    domains = domain_assignment_rows()
    contract = parent_contract_rows()
    gates = claim_gate_rows(source_rows, consistency)
    decision = decision_rows(consistency)

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "alpha_release_consistency.csv": (
            consistency,
            ["alpha_candidate", "releases", "worst_verdict", "max_delta_chi2_vs_shared_alpha", "sum_delta_chi2_vs_shared_alpha", "release_consistency_decision"],
        ),
        "H0_rd_owner_options.csv": (
            owner_options,
            ["alpha_candidate", "meaning", "worst_verdict", "max_delta_chi2_vs_shared_alpha", "owner_decision", "reason"],
        ),
        "endpoint_domain_assignment.csv": (
            domains,
            ["observable_domain", "endpoint_class", "allowed_calibration", "forbidden_calibration", "status"],
        ),
        "parent_H0_rd_owner_contract.csv": (
            contract,
            ["contract", "required_derivation", "current_evidence", "status"],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            [
                "decision",
                "meaning",
                "lead_alpha_candidate",
                "lead_alpha_worst_verdict",
                "lead_alpha_max_delta_chi2_vs_shared_alpha",
                "demoted_alpha_candidate_count",
                "readback_survivor_count",
                "next_target",
                "promotion_allowed",
                "claim_ceiling",
            ],
        ),
    }
    for filename, (rows, fieldnames) in files.items():
        write_csv(results_dir / filename, rows, fieldnames)

    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "lead_alpha_candidate": decision[0]["lead_alpha_candidate"],
        "lead_alpha_worst_verdict": decision[0]["lead_alpha_worst_verdict"],
        "lead_alpha_max_delta_chi2_vs_shared_alpha": decision[0]["lead_alpha_max_delta_chi2_vs_shared_alpha"],
        "CMB_endpoint_alpha_demoted_for_BAO": True,
        "readbacks_quarantined_as_empirical_anchors": True,
        "parent_H0_rd_owner_derived": False,
        "promotion_allowed": False,
        "next_target": decision[0]["next_target"],
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(status_payload["status"] + "\n", encoding="utf-8")
    return status_payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timestamp", default=None, help="Optional run timestamp prefix.")
    args = parser.parse_args()
    payload = run(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
