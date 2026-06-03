#!/usr/bin/env python3
"""Checkpoint 219: attempt compact-shell q_loc source projection."""

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

CHECKPOINT_219_NAME = "compact-shell-q_loc-source-projection-attempt"
CHECKPOINT_218_RUN = RUNS_ROOT / "20260601-000035-sidecar-readonly-join-contract-or-local-qloc"

STATUS = "compact_shell_q_loc_projection_conditional_Noether_identity_missing_leakage_budget_set"
CLAIM_CEILING = "q_loc_projection_attempt_no_local_GR_or_PPN_promotion"
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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 219 q_loc source projection script"),
        (WORK_DIR / "218-sidecar-readonly-join-contract-or-local-qloc.md", "q_loc proxy fork checkpoint"),
        (CHECKPOINT_218_RUN / "status.json", "checkpoint 218 machine status"),
        (CHECKPOINT_218_RUN / "results" / "local_q_proxy_readout.csv", "checkpoint 218 q proxy readout"),
        (CHECKPOINT_218_RUN / "results" / "ppn_residual_vector.csv", "checkpoint 218 residual vector"),
        (WORK_DIR / "179-local-GR-PPN-silence-contract.md", "local PPN silence contract"),
        (WORK_DIR / "143-domain-selector-variational-action-attempt.md", "domain/J_rel selector route"),
        (WORK_DIR / "207-domain-projector-action-and-Bianchi-identity.md", "domain projector/Bianchi accounting"),
        (WORK_DIR / "215-QJrel-load-morphology-parent-owner-attempt.md", "J_rel edge owner still missing"),
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


def theorem_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause": "C1_compact_vacuum_collar",
            "required_statement": "there exists an outer collar C subset D with dmu_L|_C=0 and compact_vacuum_shell sidecar class",
            "current_status": "conditional_pass",
            "failure_mode": "extended or ambiguous loads cannot use local shell projection",
        },
        {
            "clause": "C2_edge_current_zero",
            "required_statement": "J_rel outer representative vanishes on the local compact shell boundary",
            "current_status": "not_derived",
            "failure_mode": "F_edge=0 remains a closure input rather than a current theorem",
        },
        {
            "clause": "C3_stationary_coherent_load_zero",
            "required_statement": "Q_coh=0 or trace channel stationary in the exterior collar",
            "current_status": "conditional_pass",
            "failure_mode": "dynamic strain/collapse can activate local memory",
        },
        {
            "clause": "C4_Noether_source_identity",
            "required_statement": "nabla_mu Khat^{mu nu}-nabla^nu Gamma_eff = S_L^nu + d_rel J_rel^nu",
            "current_status": "missing",
            "failure_mode": "morphology does not force q_loc^nu=0 without the identity",
        },
        {
            "clause": "C5_projector_annihilation",
            "required_statement": "P_loc(S_L^nu+d_rel J_rel^nu)=0 in compact vacuum collar",
            "current_status": "conditional_on_C2_C4",
            "failure_mode": "only an integrated bound, not pointwise local GR",
        },
    ]


def derivation_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "Start from q_loc^nu=P_loc(nabla^nu Gamma_eff - nabla_mu Khat^{mu nu}).",
            "result": "definition",
            "gap": "",
        },
        {
            "step": 2,
            "statement": "In a compact vacuum collar, matter/load support vanishes: dmu_L|_C=0.",
            "result": "conditional_from_sidecar",
            "gap": "depends on fixed morphology closure",
        },
        {
            "step": 3,
            "statement": "If the parent variation gives the Noether identity nabla_mu Khat^{mu nu}-nabla^nu Gamma_eff=S_L^nu+d_rel J_rel^nu, then q_loc^nu=-P_loc(S_L^nu+d_rel J_rel^nu).",
            "result": "formal_route",
            "gap": "identity not derived in current parent action",
        },
        {
            "step": 4,
            "statement": "If S_L^nu=0 in the collar and J_rel has the local trivial representative, then q_loc^nu=0 pointwise in the projected collar.",
            "result": "conditional_theorem",
            "gap": "J_rel representative is missing",
        },
        {
            "step": 5,
            "statement": "Without the identity, checkpoint 218 gives only a residual magnitude budget.",
            "result": "fallback_bound",
            "gap": "not a GR derivation",
        },
    ]


def leakage_budget_rows() -> list[dict[str, Any]]:
    q_rows = read_csv_rows(CHECKPOINT_218_RUN / "results" / "local_q_proxy_readout.csv")
    rows: list[dict[str, Any]] = []
    for row in q_rows:
        if row["use_in_gate"] not in {"yes", "stress_only"}:
            continue
        q_total = float(row["q_total_proxy"])
        gate = float(row["q_R_like_gate"])
        budget = gate - q_total
        rows.append(
            {
                "case": row["case"],
                "use_in_gate": row["use_in_gate"],
                "q_total_proxy_before_source_leakage": q_total,
                "q_R_like_gate": gate,
                "remaining_unmodeled_source_leakage_budget": budget,
                "remaining_budget_fraction_of_gate": budget / gate,
                "source_projection_required": "yes" if row["use_in_gate"] == "yes" else "stress_diagnostic",
                "status": "budget_positive" if budget > 0 else "budget_exhausted",
            }
        )
    return rows


def claim_gate_rows(source_rows: list[dict[str, Any]], budget_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    compact_budget_failures = sum(
        row["status"] != "budget_positive" for row in budget_rows if row["use_in_gate"] == "yes"
    )
    worst_budget = min(
        float(row["remaining_unmodeled_source_leakage_budget"])
        for row in budget_rows
        if row["use_in_gate"] == "yes"
    )
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal q_loc source-projection attempt",
        },
        {
            "gate": "compact shell collar condition",
            "status": "conditional_pass",
            "evidence": "sidecar class supplies compact_vacuum_shell inputs",
            "claim_allowed": "closure premise",
        },
        {
            "gate": "Noether source identity derived",
            "status": "fail",
            "evidence": "identity written as contract, not derived from parent action",
            "claim_allowed": "no theorem",
        },
        {
            "gate": "J_rel local trivial representative derived",
            "status": "fail",
            "evidence": "checkpoint 215 still has J_rel edge owner missing",
            "claim_allowed": "no theorem",
        },
        {
            "gate": "source leakage budget positive",
            "status": "pass" if compact_budget_failures == 0 else "fail",
            "evidence": f"compact_budget_failures={compact_budget_failures}; worst_remaining_budget={worst_budget}",
            "claim_allowed": "bounded residual closure",
        },
        {
            "gate": "q_loc^nu pointwise zero promoted",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
        {
            "gate": "PPN local GR promoted",
            "status": "fail",
            "evidence": "metric map and source projection missing",
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "Compact-vacuum-shell morphology can support a conditional route to q_loc^nu=0 only if the parent theory supplies a Noether source identity and a local trivial J_rel representative. Those are not derived. The useful fallback is a positive leakage budget: the worst compact shell can tolerate only a finite additional source-projection residual before hitting the q_R-like gate.",
            "main_gain": "the local route now has exact theorem clauses and a numeric leakage budget",
            "main_failure": "Noether identity and J_rel local representative remain missing",
            "next_target": "220-Jrel-local-trivial-representative-or-closure-bound.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_219_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    contract_rows = theorem_contract_rows()
    derivation_rows = derivation_attempt_rows()
    budget_rows = leakage_budget_rows()
    gates = claim_gate_rows(source_rows, budget_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "theorem_contract.csv": (
            contract_rows,
            ["clause", "required_statement", "current_status", "failure_mode"],
        ),
        "derivation_attempt_chain.csv": (
            derivation_rows,
            ["step", "statement", "result", "gap"],
        ),
        "source_leakage_budget.csv": (
            budget_rows,
            [
                "case",
                "use_in_gate",
                "q_total_proxy_before_source_leakage",
                "q_R_like_gate",
                "remaining_unmodeled_source_leakage_budget",
                "remaining_budget_fraction_of_gate",
                "source_projection_required",
                "status",
            ],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            ["decision", "meaning", "main_gain", "main_failure", "next_target", "promotion_allowed", "claim_ceiling"],
        ),
    }
    for filename, (rows, fieldnames) in files.items():
        write_csv(results_dir / filename, rows, fieldnames)

    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    compact_budgets = [row for row in budget_rows if row["use_in_gate"] == "yes"]
    worst_remaining_budget = min(float(row["remaining_unmodeled_source_leakage_budget"]) for row in compact_budgets)
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "Noether_source_identity_derived": False,
        "J_rel_local_trivial_representative_derived": False,
        "compact_source_leakage_budget_positive": worst_remaining_budget > 0,
        "worst_remaining_compact_budget": worst_remaining_budget,
        "q_loc_pointwise_zero_promoted": False,
        "PPN_promoted": False,
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
