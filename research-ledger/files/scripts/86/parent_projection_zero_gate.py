from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Iterable, List


def write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    row_list = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not row_list:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: List[str] = []
    for row in row_list:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(row_list)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def projection_theorem_clause_rows() -> List[Dict[str, object]]:
    return [
        {
            "clause_id": "PTC4494_0_target",
            "target": "C_DeltaKTF=0",
            "required_statement": "The parent public metric map annihilates DeltaK_TF before local observables: P_public[DeltaK_TF]=0.",
            "mathematical_form": "delta g_public[DeltaK_TF]=0 or Sigma_metric[DeltaK_TF]=0 or P_PPN G_loc Sigma_metric[DeltaK_TF]=0",
            "current_verdict": "NOT_DERIVED",
            "reason": "4493 shows profile leakage is nonzero and older metric-null/solder gates do not prove the required public projection.",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PTC4494_1_identity_readout",
            "target": "same-frame identity readout",
            "required_statement": "If the public weak-field metric directly reads the Hessian carrier, DeltaK_TF must nevertheless be metric-null.",
            "mathematical_form": "G_ij^(1)=Sigma_H K_L,ij gives Psi-Phi=2 Sigma_H r^-3 P2 unless Sigma_H=0",
            "current_verdict": "FAILS_UNLESS_COEFFICIENT_ZERO",
            "reason": "4487 already shows metric-null fails on identity readout unless the response coefficient vanishes.",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PTC4494_2_projection_axiom",
            "target": "public metric equals projected Y_a channel only",
            "required_statement": "g_public depends on P_Y[K_L] and not on the non-Y_a tensor footprint.",
            "mathematical_form": "g_public = g_EH + R_Y(P_Y[K_L]); Dg_public[DeltaK_TF]=0",
            "current_verdict": "WOULD_SOLVE_BUT_AXIOMATIC_IF_ADDED_NOW",
            "reason": "No source file derives this as the parent public metric map; adding it would be a closure axiom, not a derivation.",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PTC4494_3_boundary_topological",
            "target": "boundary/topological/superpotential silence",
            "required_statement": "DeltaK_TF is a pure boundary, exact, topological, or Ward-inflow term with zero local residual.",
            "mathematical_form": "Sigma_metric[DeltaK_TF]=boundary/gauge and finite boundary response <= local bound",
            "current_verdict": "FAILED_FOR_GENERIC_ROUTE",
            "reason": "143 and 299/4283 say generic boundary/topological ownership fails: nontrivial ownership, finite boundary control, Ward identity, and K_perp guardrail do not close.",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PTC4494_4_finite_coefficient",
            "target": "nonzero C_DeltaKTF",
            "required_statement": "If C_DeltaKTF is nonzero, it must be parent-owned and below the 4493 scorer limits.",
            "mathematical_form": "C_DeltaKTF <= required_CDeltaKTF_max_given_profile_norm",
            "current_verdict": "ONLY_CURRENTLY_HONEST_ROUTE",
            "reason": "The branch can remain as an explicit closure/comparator coefficient, but not a derived local-GR theorem.",
            "valid_for_claim": False,
        },
    ]


def route_verdict_rows() -> List[Dict[str, object]]:
    return [
        {
            "route_id": "RV4494_0_metric_response_kernel",
            "route": "R_loc kernel theorem",
            "evidence": "136 says vector-current conservation is insufficient until Sigma_metric[q] is fixed by the parent theory.",
            "verdict": "FORMAL_ONLY_NOT_DERIVED",
            "effect_on_C_DeltaKTF": "does not set C_DeltaKTF=0",
            "valid_for_claim": False,
        },
        {
            "route_id": "RV4494_1_metric_null_contract",
            "route": "metric-null action block",
            "evidence": "138 writes C0-C9 but explicitly says the contract is not derived and the route is contract-only closure.",
            "verdict": "CONTRACT_ONLY",
            "effect_on_C_DeltaKTF": "can define what a future zero theorem must satisfy but cannot promote it",
            "valid_for_claim": False,
        },
        {
            "route_id": "RV4494_2_doubled_open_system",
            "route": "pure doubled open-system metric-null route",
            "evidence": "140 fails at hidden metric dependence in nabla, index raising, Gamma_eff and K_hat contractions.",
            "verdict": "FAILED_AS_ZERO_THEOREM",
            "effect_on_C_DeltaKTF": "does not set C_DeltaKTF=0",
            "valid_for_claim": False,
        },
        {
            "route_id": "RV4494_3_owner_solder",
            "route": "owner-spacetime solder map",
            "evidence": "142: metric tetrad reintroduces g_loc, fixed background breaks covariance, independent coframe needs another stress theorem.",
            "verdict": "BULK_HYBRID_FAILS",
            "effect_on_C_DeltaKTF": "does not set C_DeltaKTF=0",
            "valid_for_claim": False,
        },
        {
            "route_id": "RV4494_4_boundary_topological",
            "route": "boundary/topological/superpotential backup",
            "evidence": "143 demotes the branch because nontrivial ownership, finite boundary response, support locality, Ward identity and K_perp guardrail fail.",
            "verdict": "FAILED_FOR_GENERIC_ROUTE",
            "effect_on_C_DeltaKTF": "does not set C_DeltaKTF=0 except in support-separated/no-flux special cases",
            "valid_for_claim": False,
        },
        {
            "route_id": "RV4494_5_new_Ward_or_cohomology",
            "route": "new parent Ward/cohomology/inflow identity",
            "evidence": "Current corpus says this would be a real escape if derived, but no transition Ward/anomaly equation is present.",
            "verdict": "OPEN_NEW_THEOREM_NOT_CURRENT_EVIDENCE",
            "effect_on_C_DeltaKTF": "could set C_DeltaKTF=0 in future, but not in current branch",
            "valid_for_claim": False,
        },
    ]


def closure_contract_rows(score_rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for score in score_rows:
        rows.append(
            {
                "contract_id": f"CDC4494_{score['profile_id']}_{score['abs_sK2_kappaSTF']}",
                "profile_id": score["profile_id"],
                "abs_sK2_kappaSTF": score["abs_sK2_kappaSTF"],
                "required_CDeltaKTF_max": score["required_CDeltaKTF_max_given_profile_norm"],
                "closure_status": "EXPLICIT_CLOSURE_COEFFICIENT_REQUIRED",
                "allowed_use": "private comparator or future parent-theorem target",
                "forbidden_use": "derived local-GR/J2/PPN pass",
                "promotion_condition": "derive C_DeltaKTF=0 from parent public metric projection, or source a nonzero C_DeltaKTF below this row and complete arena transfer",
                "valid_for_claim": False,
            }
        )
    return rows


def rescue_route_rows() -> List[Dict[str, object]]:
    return [
        {
            "rescue_id": "RR4494_0_Ward_inflow",
            "route": "derive a transition Ward/anomaly-inflow identity",
            "why_it_is_real": "a symmetry identity could cancel metric variation without making matter non-gravitating",
            "must_prove": "delta_g S_bulk + delta_g S_boundary = 0 for DeltaKTF and preserve owner balance",
            "current_status": "NEW_PARENT_THEOREM_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "rescue_id": "RR4494_1_cohomology_support",
            "route": "derive q_tr/DeltaKTF as an exact cohomology/support-separated current",
            "why_it_is_real": "support-separated exact forms can be locally silent in no-flux domains",
            "must_prove": "local PPN domain is disjoint from transition support and all boundary pullbacks vanish or are routed",
            "current_status": "SPECIAL_CASE_ONLY_NOT_GENERIC_LOCAL_GR",
            "valid_for_claim": False,
        },
        {
            "rescue_id": "RR4494_2_terminal_projection",
            "route": "derive terminal public metric/coframe projection from parent variables",
            "why_it_is_real": "a quotient-owned public metric map could annihilate non-Y_a footprint without a covariance cheat",
            "must_prove": "Dg_public[DeltaK_TF]=0 and ordinary matter still sources GR/Newton",
            "current_status": "BEST_THEOREM_TARGET_BUT_NOT_CURRENTLY_DERIVED",
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4494_0_zero_theorem_attempted",
            "finding": "C_DeltaKTF=0 is not derived by the current public metric/solder/topological chain",
            "reason": "identity readout is live; metric-null contract is only a contract; solder and boundary/topological routes failed as derivations",
            "effect": "do not promote the local DeltaKTF branch as derived local GR",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4494_1_explicit_closure",
            "finding": "DeltaKTF becomes an explicit closure coefficient branch",
            "reason": "4493 requires tiny C_DeltaKTF values unless a new parent theorem sets it exactly zero",
            "effect": "future tests can use it only as a transparent comparator, not hidden proof",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4494_2_next_real_route",
            "finding": "only serious rescue is a new parent Ward/cohomology/terminal-projection theorem",
            "reason": "profile-only and generic boundary/topological routes have been exhausted",
            "effect": "next work should either build that theorem target or move local branch to empirical closure testing",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    sources: List[Dict[str, object]],
    clause_rows: List[Dict[str, object]],
    route_rows: List[Dict[str, object]],
    closure_rows: List[Dict[str, object]],
    rescue_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4494_0_sources",
            "requirement": "all cited source paths exist and needles are found",
            "passed": all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
            "claim_allowed": False,
            "reason": "source-backed private theorem audit only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4494_1_zero_theorem_not_derived",
            "requirement": "C_DeltaKTF=0 is not marked derived",
            "passed": any(row.get("current_verdict") == "NOT_DERIVED" for row in clause_rows)
            and not any(row.get("current_verdict") == "DERIVED" for row in clause_rows),
            "claim_allowed": False,
            "reason": "zero theorem fails in current corpus",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4494_2_failed_routes_recorded",
            "requirement": "solder and boundary/topological failures are carried",
            "passed": any(row.get("verdict") == "BULK_HYBRID_FAILS" for row in route_rows)
            and any(row.get("verdict") == "FAILED_FOR_GENERIC_ROUTE" for row in route_rows),
            "claim_allowed": False,
            "reason": "old failed escape hatches are not resurrected",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4494_3_closure_contract_rows",
            "requirement": "closure coefficient rows exist for 4493 scorer cells",
            "passed": len(closure_rows) >= 4 and all(row.get("closure_status") == "EXPLICIT_CLOSURE_COEFFICIENT_REQUIRED" for row in closure_rows),
            "claim_allowed": False,
            "reason": "closure is explicit and visible",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4494_4_rescue_routes_are_new_theorems",
            "requirement": "rescue routes are classified as future theorem work only",
            "passed": len(rescue_rows) >= 3 and not any(str(row.get("current_status")) == "DERIVED" for row in rescue_rows),
            "claim_allowed": False,
            "reason": "future possibilities do not become current evidence",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4494_5_local_GR",
            "requirement": "local-GR/J2/PPN claim",
            "passed": False,
            "claim_allowed": False,
            "reason": "DeltaKTF is closure-only unless C_DeltaKTF=0 or tiny nonzero coefficient is parent-owned and arena transfers close",
            "valid_for_claim": False,
        },
    ]
