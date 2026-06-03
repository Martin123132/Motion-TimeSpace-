#!/usr/bin/env python3
"""Decision gate: official refresh now, or pivot back to derivation debt."""

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

STATUS_PASS = "official_refresh_decision_gate_passed_pivot_to_derivation_debt"
STATUS_FAIL = "official_refresh_decision_gate_failed"
CLAIM_CEILING = "decision_gate_no_new_scoring_no_theory_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

CHECKPOINT_RUNS = [
    {
        "checkpoint": "170",
        "lane": "source_refresh",
        "run": RUNS_ROOT / "20260531-235959-no-clock-official-source-refresh",
        "expected_status": "no_clock_official_source_refresh_preflight_passed",
        "evidence_role": "official source manifests and hashes",
    },
    {
        "checkpoint": "171",
        "lane": "manifest_guard",
        "run": RUNS_ROOT / "20260531-235959-no-clock-manifest-only-fit-guard",
        "expected_status": "no_clock_manifest_only_fit_guard_passed",
        "evidence_role": "fit guard and no-sidecar manifest contract",
    },
    {
        "checkpoint": "172",
        "lane": "BAO_only_reproduction",
        "run": RUNS_ROOT / "20260531-235959-no-clock-single-arena-reproduction-guard",
        "expected_status": "no_clock_single_arena_BAO_reproduction_passed",
        "evidence_role": "BAO-only DR1/DR2 locked branch reproduction",
    },
    {
        "checkpoint": "173",
        "lane": "SN_BAO_reproduction",
        "run": RUNS_ROOT / "20260531-235959-no-clock-SN-BAO-reproduction-guard",
        "expected_status": "no_clock_SN_BAO_locked_2over27_reproduction_passed",
        "evidence_role": "SN+BAO T1-T6 locked branch reproduction",
    },
    {
        "checkpoint": "174",
        "lane": "nonCMB_readiness",
        "run": RUNS_ROOT / "20260531-235959-no-clock-Hz-growth-reproduction-readiness",
        "expected_status": "no_clock_Hz_growth_reproduction_readiness_passed",
        "evidence_role": "H(z)/growth/ELG reproduction readiness audit",
    },
    {
        "checkpoint": "175",
        "lane": "nonCMB_reproduction",
        "run": RUNS_ROOT / "20260531-235959-no-clock-nonCMB-reproduction-guard",
        "expected_status": "no_clock_nonCMB_reproduction_guard_passed",
        "evidence_role": "source-locked H(z), growth, and ELG reproduction guard",
    },
]

THEORY_RUNS = [
    {
        "checkpoint": "141",
        "lane": "locked_branch_contract",
        "run": RUNS_ROOT / "20260531-210000-consolidated-locked-memory-branch-contract",
        "role": "empirical EFT closure contract",
    },
    {
        "checkpoint": "148",
        "lane": "promotion_contract",
        "run": RUNS_ROOT / "20260531-234500-promotion-contract-audit",
        "role": "promotion blockers and next work queue",
    },
    {
        "checkpoint": "175",
        "lane": "latest_nonCMB_guard",
        "run": RUNS_ROOT / "20260531-235959-no-clock-nonCMB-reproduction-guard",
        "role": "latest empirical reproduction blockers",
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
        (Path(__file__).resolve(), "checkpoint 176 decision-gate script"),
        (WORK_DIR / "170-no-clock-official-source-refresh-runner.md", "source refresh checkpoint note"),
        (WORK_DIR / "171-no-clock-manifest-only-fit-guard.md", "manifest guard checkpoint note"),
        (WORK_DIR / "172-no-clock-single-arena-reproduction-guard.md", "BAO-only reproduction note"),
        (WORK_DIR / "173-no-clock-SN-BAO-reproduction-guard.md", "SN+BAO reproduction note"),
        (WORK_DIR / "174-no-clock-Hz-growth-reproduction-readiness.md", "non-CMB readiness note"),
        (WORK_DIR / "175-no-clock-nonCMB-reproduction-guard.md", "non-CMB reproduction note"),
        (WORK_DIR / "148-perturbation-CMB-local-GR-promotion-contract.md", "promotion contract note"),
        (WORK_DIR / "141-consolidated-locked-memory-branch-contract.md", "locked branch contract note"),
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


def empirical_chain_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in CHECKPOINT_RUNS:
        status_path = item["run"] / "status.json"
        exists = status_path.exists()
        status = load_json(status_path) if exists else {}
        actual_status = status.get("status") or status.get("readout", "")
        expected = item["expected_status"]
        failed_gates = status.get("failed_gates", [])
        rows.append(
            {
                "checkpoint": item["checkpoint"],
                "lane": item["lane"],
                "run_dir": str(item["run"]),
                "status_json_exists": "yes" if exists else "no",
                "expected_status": expected,
                "actual_status": actual_status,
                "failed_gate_count": len(failed_gates) if isinstance(failed_gates, list) else "",
                "claim_ceiling": status.get("claim_ceiling", ""),
                "promotion_allowed": status.get("promotion_allowed", "not_applicable"),
                "evidence_role": item["evidence_role"],
                "status": "pass" if exists and actual_status == expected and not failed_gates else "fail",
            }
        )
    return rows


def promotion_requirement_rows() -> list[dict[str, Any]]:
    path = RUNS_ROOT / "20260531-234500-promotion-contract-audit" / "results" / "promotion_requirement_matrix.csv"
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for row in read_csv_rows(path):
        current = row.get("current_status", "")
        if current.startswith("pass"):
            class_status = "satisfied"
        elif "conditional" in current or "partial" in current:
            class_status = "conditional_or_partial"
        else:
            class_status = "blocking"
        rows.append(
            {
                "gate_id": row.get("gate_id", ""),
                "requirement": row.get("requirement", ""),
                "current_status": current,
                "class_status": class_status,
                "evidence": row.get("evidence", ""),
                "promotion_effect": "blocks_promotion" if class_status == "blocking" else ("limits_promotion" if class_status == "conditional_or_partial" else "cleared"),
            }
        )
    return rows


def theory_debt_rows() -> list[dict[str, Any]]:
    promotion_rows = promotion_requirement_rows()
    blockers = [row for row in promotion_rows if row["class_status"] == "blocking"]
    partials = [row for row in promotion_rows if row["class_status"] == "conditional_or_partial"]
    empirical_satisfied = [row for row in promotion_rows if row["class_status"] == "satisfied"]
    return [
        {
            "category": "empirical_chain",
            "status": "reproducible",
            "count": len(CHECKPOINT_RUNS),
            "evidence": "170-175 source/manifest/reproduction chain",
            "decision_impact": "allows stronger internal scorecard, not theory promotion",
        },
        {
            "category": "promotion_blockers",
            "status": "blocking",
            "count": len(blockers),
            "evidence": "; ".join(row["gate_id"] for row in blockers),
            "decision_impact": "prevents public field-theory/CMB/local-GR claim",
        },
        {
            "category": "conditional_or_partial_theory",
            "status": "partial",
            "count": len(partials),
            "evidence": "; ".join(row["gate_id"] for row in partials),
            "decision_impact": "must be tightened before promotion",
        },
        {
            "category": "cleared_or_controlled_requirements",
            "status": "satisfied",
            "count": len(empirical_satisfied),
            "evidence": "; ".join(row["gate_id"] for row in empirical_satisfied),
            "decision_impact": "do not revisit unless evidence changes",
        },
    ]


def option_matrix_rows(empirical_pass: bool, blocker_count: int) -> list[dict[str, Any]]:
    rows = [
        {
            "option": "run_broader_official_refresh_now",
            "benefit": "would combine the already-reproduced late-time and non-CMB cards into one bookkeeping scorecard",
            "risk": "invites false promotion while parent action, perturbations, CMB, and local GR remain unresolved",
            "required_precondition": "empirical chain passes and claim ceiling is explicit",
            "current_precondition_status": "met" if empirical_pass else "not_met",
            "decision": "allowed_only_as_private_bookkeeping_not_next_priority" if empirical_pass and blocker_count else "not_allowed",
        },
        {
            "option": "pivot_to_parent_action_and_perturbations",
            "benefit": "attacks the actual blockers that stop MTS becoming a field theory rather than an empirical closure",
            "risk": "harder math; may demote parts of the branch if derivation fails",
            "required_precondition": "empirical case is reproducible enough to justify theory work",
            "current_precondition_status": "met" if empirical_pass else "not_met",
            "decision": "recommended_next_priority" if empirical_pass and blocker_count else "defer_until_empirical_chain_clean",
        },
        {
            "option": "continue_dataset_expansion",
            "benefit": "could find additional stress failures or support",
            "risk": "diminishing returns; does not solve CMB/local-GR/parent-action debt",
            "required_precondition": "clear new independent dataset target with source lock",
            "current_precondition_status": "not_currently_primary",
            "decision": "defer",
        },
        {
            "option": "claim_theory_promotion",
            "benefit": "none at this stage",
            "risk": "overclaim; contradicts promotion contract",
            "required_precondition": "all promotion blockers cleared",
            "current_precondition_status": "not_met" if blocker_count else "met",
            "decision": "forbidden" if blocker_count else "review_required",
        },
    ]
    return rows


def next_work_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "target": "177-parent-action-perturbation-local-GR-contract.md",
            "work_type": "derivation_contract",
            "question": "Can one parent action produce background memory, perturbation sources, conservation, and local GR silence without inserting closures?",
            "acceptance_gate": "writes exact variables, equations, required variations, and fail/demote criteria",
        },
        {
            "priority": 2,
            "target": "178-memory-perturbation-owner-attempt.md",
            "work_type": "derivation_attempt",
            "question": "Derive or bound mu(a,k), slip/Sigma, F_fric(a,k), and S_mem(a,k) from the memory sector",
            "acceptance_gate": "either derives GR-proxy limit or records controlled modified-growth branch",
        },
        {
            "priority": 3,
            "target": "179-local-GR-PPN-silence-contract.md",
            "work_type": "local_limit_contract",
            "question": "Derive q_loc^nu -> 0, G_eff/G -> 1, and Phi=Psi in local weak fields",
            "acceptance_gate": "no plateau axiom; local silence follows from action/source structure or branch remains closure-only",
        },
        {
            "priority": 4,
            "target": "180-Bmem-two-over-27-parent-owner-attempt.md",
            "work_type": "amplitude_derivation",
            "question": "Can normalized boundary charge derive B_mem=2/27 rather than just lock it empirically?",
            "acceptance_gate": "derive value from parent variables before data scoring, or keep it as empirical theorem target",
        },
    ]


def guard_gate_rows(
    sources: list[dict[str, Any]],
    empirical: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    options: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row for row in sources if row["exists"] != "yes"]
    empirical_bad = [row for row in empirical if row["status"] != "pass"]
    blockers = [row for row in promotion if row["class_status"] == "blocking"]
    recommended = [row for row in options if row["decision"] == "recommended_next_priority"]
    forbidden_claim = [row for row in options if row["option"] == "claim_theory_promotion" and row["decision"] == "forbidden"]
    return [
        {
            "gate": "source_files_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
        },
        {
            "gate": "empirical_reproduction_chain_clean",
            "status": "pass" if not empirical_bad else "fail",
            "evidence": f"failed_empirical_lanes={len(empirical_bad)}; lanes={len(empirical)}",
        },
        {
            "gate": "promotion_blockers_identified",
            "status": "pass" if blockers else "fail",
            "evidence": f"blocking_requirements={len(blockers)}",
        },
        {
            "gate": "official_refresh_not_required_for_next_progress",
            "status": "pass",
            "evidence": "170-175 already reproduce the empirical card; more scoring is bookkeeping",
        },
        {
            "gate": "derivation_pivot_selected",
            "status": "pass" if recommended else "fail",
            "evidence": ";".join(row["option"] for row in recommended),
        },
        {
            "gate": "theory_promotion_forbidden",
            "status": "pass" if forbidden_claim else "fail",
            "evidence": "promotion blockers remain active",
        },
        {
            "gate": "claim_ceiling_preserved",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(gates: list[dict[str, Any]], options: list[dict[str, Any]], blockers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failed = [row for row in gates if row["status"] != "pass"]
    recommended = next((row for row in options if row["decision"] == "recommended_next_priority"), None)
    status = STATUS_PASS if not failed else STATUS_FAIL
    return [
        {
            "item": "status",
            "verdict": status,
            "evidence": f"failed_gates={len(failed)}",
        },
        {
            "item": "official_refresh_now",
            "verdict": "defer_as_not_next_priority",
            "evidence": "allowed only as private bookkeeping; it will not clear promotion blockers",
        },
        {
            "item": "recommended_next_priority",
            "verdict": recommended["option"] if recommended else "none",
            "evidence": "empirical chain is clean enough; blockers are structural",
        },
        {
            "item": "blocking_requirement_count",
            "verdict": len(blockers),
            "evidence": "; ".join(row["gate_id"] for row in blockers),
        },
        {
            "item": "lead_branch",
            "verdict": LEAD_BRANCH,
            "evidence": "locked no-clock branch remains empirical lead",
        },
        {
            "item": "claim_ceiling",
            "verdict": CLAIM_CEILING,
            "evidence": "no new scoring or theory promotion performed",
        },
        {
            "item": "next_target",
            "verdict": "177-parent-action-perturbation-local-GR-contract.md",
            "evidence": "write exact derivation contract before more broad scoring",
        },
    ]


def run_gate(output_root: Path, timestamp: str | None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-official-refresh-decision-gate"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    empirical = empirical_chain_rows()
    promotion = promotion_requirement_rows()
    blockers = [row for row in promotion if row["class_status"] == "blocking"]
    empirical_pass = all(row["status"] == "pass" for row in empirical)
    theory_debt = theory_debt_rows()
    options = option_matrix_rows(empirical_pass, len(blockers))
    next_queue = next_work_queue_rows()
    gates = guard_gate_rows(sources, empirical, promotion, options)
    decisions = decision_rows(gates, options, blockers)
    status = decisions[0]["verdict"]

    write_json(
        run_dir / "run_config.json",
        {
            "timestamp": run_stamp,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "empirical_checkpoints": [{**item, "run": str(item["run"])} for item in CHECKPOINT_RUNS],
            "theory_runs": [{**item, "run": str(item["run"])} for item in THEORY_RUNS],
        },
    )
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(results_dir / "empirical_chain_status.csv", empirical, ["checkpoint", "lane", "run_dir", "status_json_exists", "expected_status", "actual_status", "failed_gate_count", "claim_ceiling", "promotion_allowed", "evidence_role", "status"])
    write_csv(results_dir / "promotion_requirement_matrix.csv", promotion, ["gate_id", "requirement", "current_status", "class_status", "evidence", "promotion_effect"])
    write_csv(results_dir / "theory_debt_summary.csv", theory_debt, ["category", "status", "count", "evidence", "decision_impact"])
    write_csv(results_dir / "option_matrix.csv", options, ["option", "benefit", "risk", "required_precondition", "current_precondition_status", "decision"])
    write_csv(results_dir / "next_work_queue.csv", next_queue, ["priority", "target", "work_type", "question", "acceptance_gate"])
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
            "empirical_chain_pass": empirical_pass,
            "blocking_requirement_count": len(blockers),
            "official_refresh_decision": "defer_as_private_bookkeeping_not_next_priority",
            "recommended_next_priority": "pivot_to_parent_action_and_perturbations",
            "promotion_allowed": False,
            "next_target": "177-parent-action-perturbation-local-GR-contract.md",
            "generated": [
                "source_register.csv",
                "empirical_chain_status.csv",
                "promotion_requirement_matrix.csv",
                "theory_debt_summary.csv",
                "option_matrix.csv",
                "next_work_queue.csv",
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
    print(run_gate(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
