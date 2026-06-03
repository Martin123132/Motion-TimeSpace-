#!/usr/bin/env python3
"""Attempt to derive the DeltaR=2/9 boundary-charge contrast."""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RUNS_ROOT = POST_CHECKPOINT / "runs"

SOURCES = [
    ("relative_cohomology_boundary_contract", POST_CHECKPOINT / "60-relative-cohomology-boundary-contract.md"),
    ("relative_boundary_current", POST_CHECKPOINT / "71-relative-boundary-current-construction-attempt.md"),
    ("relative_current_action_owner", POST_CHECKPOINT / "72-relative-current-action-owner-attempt.md"),
    ("Ccoh_Bianchi_identity", POST_CHECKPOINT / "76-Ccoh-Bianchi-identity-attempt.md"),
    ("canonical_R_theorem_attempt", POST_CHECKPOINT / "97-canonical-R-theorem-attempt.md"),
    ("two_ninth_scout", POST_CHECKPOINT / "107-two-ninth-fixed-amplitude-scout.md"),
    ("two_ninth_robustness", POST_CHECKPOINT / "108-two-ninth-fixed-amplitude-robustness.md"),
]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_rows() -> list[dict[str, Any]]:
    return [{"source": label, "path": str(path), "exists": path.exists()} for label, path in SOURCES]


def route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "relative_form_degree_count",
            "candidate_chain": "(boundary 2-form / bulk 3-form) times spatial trace projection = (2/3)(1/3)=2/9",
            "what_it_would_need": "A parent charge inner product proving form degree ratios are actual normalized charge weights.",
            "result": "fail_as_derivation",
            "reason": "form degree is bookkeeping unless the action turns it into a charge measure",
        },
        {
            "route": "relative_boundary_pair_pairing",
            "candidate_chain": "J_rel=(j_3,b_2) supplies a 2-to-3 boundary/bulk pairing, then isotropic trace supplies 1/3",
            "what_it_would_need": "A variational pairing <b_2,j_3> with fixed coefficient ratio 2:3 and no adjustable polarization Pi(C_coh).",
            "result": "conditional_schema_only",
            "reason": "current closure can be imposed, but physical representative and coefficient selection are not derived",
        },
        {
            "route": "nine_component_deformation_charge",
            "candidate_chain": "Q^i_j has nine spatial deformation slots; two boundary-transverse slots carry the relaxed charge, giving 2/9",
            "what_it_would_need": "A projector proving exactly two of nine normalized deformation channels enter DeltaR.",
            "result": "fail_as_default",
            "reason": "FLRW coherent expansion is trace/isotropic, so a two-transverse-slot story is not automatically the cosmology memory channel",
        },
        {
            "route": "normalized_boundary_charge_postulate",
            "candidate_chain": "R=Q_boundary/Q_* and endpoint equations give (Q_early-Q_today)/Q_*=2/9",
            "what_it_would_need": "Endpoint equations that fix Q_early and Q_today before SN+BAO scoring.",
            "result": "best_contract_not_theorem",
            "reason": "this is the cleanest parent target but currently just moves the fitted number into endpoint data",
        },
        {
            "route": "empirical_locked_branch",
            "candidate_chain": "DeltaR=2/9, B_mem=2/27 is locked and survives T7 robustness",
            "what_it_would_need": "Independent prediction from parent action or successful predeclared external holdout tests.",
            "result": "empirical_motivation_pass",
            "reason": "robust score makes the theorem target worth pursuing, but score does not derive the number",
        },
    ]


def theorem_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause": "T0",
            "requirement": "Define a dimensionless boundary charge Q_boundary and fixed unit Q_* from the parent action.",
            "status": "missing",
        },
        {
            "clause": "T1",
            "requirement": "Prove R=Q_boundary/Q_* is the same R entering Gamma_eff and relaxation.",
            "status": "missing",
        },
        {
            "clause": "T2",
            "requirement": "Derive endpoint equations for Q_early and Q_today before using SN+BAO.",
            "status": "missing",
        },
        {
            "clause": "T3",
            "requirement": "Show (Q_early-Q_today)/Q_*=2/9 from topology, cell geometry, or Ward identity.",
            "status": "missing",
        },
        {
            "clause": "T4",
            "requirement": "Preserve eta=1, a_F=1, p=3, u3=1/4, local GR/PPN silence, and conservation.",
            "status": "open_guard",
        },
        {
            "clause": "T5",
            "requirement": "Freeze B_mem=2/27 in future tests without refitting amplitude.",
            "status": "passed_for_T7_SN_BAO_scout",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "two_ninth_empirical_target_exists",
            "result": "pass",
            "reason": "T7 locked amplitude matrix survived all six tested SN+BAO branches",
        },
        {
            "gate": "relative_boundary_language_exists",
            "result": "pass",
            "reason": "J_rel=(j_3,b_2) and H^3(D,boundary D) give a clean object to target",
        },
        {
            "gate": "boundary_charge_unit_defined",
            "result": "fail",
            "reason": "Q_* is not derived from the parent action",
        },
        {
            "gate": "two_over_three_factor_derived",
            "result": "fail",
            "reason": "2/3 can be motivated by boundary/bulk degree counting but not made into a charge ratio",
        },
        {
            "gate": "one_over_three_trace_factor_derived",
            "result": "partial",
            "reason": "spatial trace projection is natural, but the Ward-fixed coupling to R is still missing",
        },
        {
            "gate": "product_two_over_nine_derived",
            "result": "fail",
            "reason": "multiplying plausible factors is not a parent-action theorem",
        },
        {
            "gate": "post_fit_circularity_removed",
            "result": "fail",
            "reason": "2/9 was noticed after the fitted primary amplitude",
        },
        {
            "gate": "theorem_target_live",
            "result": "pass",
            "reason": "the locked branch performs well enough that deriving or rejecting 2/9 is now high value",
        },
        {
            "gate": "support_claim_allowed",
            "result": "fail",
            "reason": "no parent derivation yet",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision": "verdict", "value": "two_ninth_theorem_not_derived_but_target_sharpened"},
        {"decision": "best_failed_route", "value": "relative_boundary_degree_count_needs_charge_measure"},
        {"decision": "best_live_route", "value": "normalized_boundary_charge_with_endpoint_equations"},
        {"decision": "locked_empirical_branch", "value": "B_mem=2/27_remains_predeclared_scout"},
        {"decision": "promotion_allowed", "value": False},
        {"decision": "claim_ceiling", "value": "theorem_target_only_not_prediction"},
        {"decision": "next_action", "value": "derive_endpoint_charge_equations_or_freeze_2over27_for_external_holdouts"},
    ]


def main() -> None:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{timestamp}-boundary-charge-two-ninth-theorem-attempt"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    missing = [row for row in sources if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"Missing two-ninth theorem sources: {missing}")

    routes = route_rows()
    contract = theorem_contract_rows()
    gates = gate_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists"])
    write_csv(results_dir / "route_attempts.csv", routes, ["route", "candidate_chain", "what_it_would_need", "result", "reason"])
    write_csv(results_dir / "theorem_contract.csv", contract, ["clause", "requirement", "status"])
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "result", "reason"])
    write_csv(results_dir / "decision.csv", decisions, ["decision", "value"])

    status = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "readout": decisions[0]["value"],
        "locked_DeltaR": 2.0 / 9.0,
        "locked_B_mem": 2.0 / 27.0,
        "claim_ceiling": "theorem_target_only_not_prediction",
        "promotion_allowed": False,
        "next_action": "derive_endpoint_charge_equations_or_freeze_2over27_for_external_holdouts",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
