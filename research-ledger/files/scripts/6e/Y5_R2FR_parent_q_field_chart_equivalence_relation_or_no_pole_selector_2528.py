from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH_ID = "MTS_R2FR_PARENT_Q_FIELD_CHART_EQUIV_OR_NOPOLE_SELECTOR_2528"
CHECKPOINT_ID = "2528"
DOC = ROOT / "2528-Y5-R2FR-parent-q-field-chart-equivalence-relation-or-no-pole-selector.md"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2528_SOURCE_REGISTER.csv",
    "field_chart_audit": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2528_FIELD_CHART_EQUIVALENCE_AUDIT.csv",
    "nopole_selector_gate": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2528_NOPOLE_SELECTOR_GATE.csv",
    "second_class_preview": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2528_SECOND_CLASS_PREVIEW_FROM_2360.csv",
    "current_chain_veto": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2528_CURRENT_CHAIN_VETO_FROM_2361.csv",
    "finite_leak_rows": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2528_FINITE_SELECTOR_DQ_LEAK_ROWS.csv",
    "claim_gates": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2528_CLAIM_GATES.csv",
    "refusal_runner": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2528_REFUSAL_RUNNER.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2528_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2528_NEXT_TARGET.csv",
    "branch_copies": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2528_BRANCH_COPIES.csv",
    "validation": MTS_RESIDUALS / "P8_Y5_BRR545_2528_VALIDATION.csv",
}

BRANCH_COPIES = {
    "field_chart_audit": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "Q_field_chart_equivalence_2528_NONCLAIM.csv",
    "nopole_selector_gate": ROOT
    / "source-intake"
    / "local_bounds"
    / "No_pole_selector_route_2528_NONCLAIM.csv",
    "finite_leak_rows": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "QSEL2528_FINITE_SELECTOR_DQ_LEAK_ROWS_NONCLAIM.csv",
    "next_target": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "QSEL2528_NEXT_TARGET_NONCLAIM.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": "False",
        "claim_allowed": "False",
        **row,
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def contains(path: Path, needle: str) -> bool:
    return needle in read_text(path)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


SOURCE_SPECS = [
    {
        "source_id": "SRC2528_0_2527_doc",
        "source_path": "2527-Y5-R2FR-q-object-vertical-generator-open-branch-proof-or-domain-bound.md",
        "needle": "NEXT2527_0_selected",
        "role": "current handoff: construct parent q field chart/equivalence or selector leak",
    },
    {
        "source_id": "SRC2528_1_2527_validation",
        "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2527_VALIDATION.csv",
        "needle": "VAL2527_OVERALL,PASS",
        "role": "2527 validation anchor",
    },
    {
        "source_id": "SRC2528_2_2527_q_audit",
        "source_path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2527_Q_VERTICAL_OPEN_BRANCH_REENTRY_AUDIT.csv",
        "needle": "QVA2527_2_q_map",
        "role": "q object remains unsigned in the current branch",
    },
    {
        "source_id": "SRC2528_3_2359_doc",
        "source_path": "2359-Y5-R2FR-parent-q-field-chart-equivalence-relation-or-no-pole-selector.md",
        "needle": "candidate-only",
        "role": "prior field-chart/equivalence route verdict",
    },
    {
        "source_id": "SRC2528_4_2359_validation",
        "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2359_VALIDATION.csv",
        "needle": "VAL2359_OVERALL,PASS",
        "role": "2359 validation anchor",
    },
    {
        "source_id": "SRC2528_5_2359_chart",
        "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2359_FIELD_CHART_EQUIVALENCE_AUDIT.csv",
        "needle": "FCE2359_5_chart_verdict",
        "role": "field chart/equivalence audit rows",
    },
    {
        "source_id": "SRC2528_6_2359_selector",
        "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2359_NOPOLE_SELECTOR_GATE.csv",
        "needle": "NPS2359_0_second_class_auxiliary",
        "role": "no-pole selector route selection",
    },
    {
        "source_id": "SRC2528_7_2360_doc",
        "source_path": "2360-Y5-R2FR-second-class-auxiliary-origin-no-derivative-grammar-or-finite-leak.md",
        "needle": "SCA2360_6_verdict",
        "role": "second-class auxiliary theorem audit",
    },
    {
        "source_id": "SRC2528_8_2360_validation",
        "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2360_VALIDATION.csv",
        "needle": "VAL2360_OVERALL,PASS",
        "role": "2360 validation anchor",
    },
    {
        "source_id": "SRC2528_9_2361_doc",
        "source_path": "2361-Y5-R2FR-parent-origin-of-CR-from-phase-cell-current-chain-or-finite-qR-row.md",
        "needle": "CR2361_6_psi_quotient",
        "role": "current-chain veto and psi quotient next route",
    },
    {
        "source_id": "SRC2528_10_2361_validation",
        "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2361_VALIDATION.csv",
        "needle": "VAL2361_OVERALL,PASS",
        "role": "2361 validation anchor",
    },
]


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = ROOT / spec["source_path"]
        rows.append(
            stamp(
                {
                    **spec,
                    "path_exists": str(path.exists()),
                    "needle_found": str(contains(path, spec["needle"])),
                    "status": "SOURCE_OK" if path.exists() and contains(path, spec["needle"]) else "SOURCE_BLOCKED",
                }
            )
        )
    return rows


def field_chart_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "FCE2528_0_visible_quotient",
            "object": "Q_vis",
            "candidate": "Q_vis=(e_obs,g_obs,A_obs,Omega_obs,mu_obs,source/readout class,theta_owned)",
            "required_for_theorem": "target space of q must be parent-owned before matter variation and readout",
            "status": "CANDIDATE_CONTRACT_ONLY",
            "why_not_closed": "visible data are listed but not constructed as quotient coordinates by a parent action or constraint algebra",
            "parent_signed": "False",
        },
        {
            "row_id": "FCE2528_1_parent_chart",
            "object": "Phi_parent",
            "candidate": "Phi_parent=(Q_vis,R_res,Z,psi,Psi_A,theta_A,boundary/readout variables)",
            "required_for_theorem": "smooth parent branch U with owned coordinates and transition rules",
            "status": "FIELD_CHART_CANDIDATE_NOT_PARENT_SIGNED",
            "why_not_closed": "this is a useful testing grammar, not a derived parent configuration chart",
            "parent_signed": "False",
        },
        {
            "row_id": "FCE2528_2_equivalence_relation",
            "object": "Phi~Phi'",
            "candidate": "same Q_vis, same fixed theta, same parent-owned support/readout class",
            "required_for_theorem": "quotient fibres must be generated by constraints/gauge/orbits or an adopted parent reduction",
            "status": "EQUIVALENCE_RELATION_NOT_DERIVED",
            "why_not_closed": "no source shows the relation follows from MTS core rather than being imposed to make matter silent",
            "parent_signed": "False",
        },
        {
            "row_id": "FCE2528_3_computable_q",
            "object": "q: U -> Q_vis",
            "candidate": "projection from parent branch to quotient-owned visible data",
            "required_for_theorem": "component formulas q^A(Phi) and Dq matrix with constant rank",
            "status": "Q_NOT_COMPUTABLE_CURRENT_CORPUS",
            "why_not_closed": "q components, tangent basis, and rank certificate remain unsigned",
            "parent_signed": "False",
        },
        {
            "row_id": "FCE2528_4_shape_only_option",
            "object": "shape-only / no-pole quotient",
            "candidate": "eliminate reciprocal cell-volume/residual pole while preserving visible shape/orientation",
            "required_for_theorem": "unit/cell normalization and observed coframe functor must be parent-owned",
            "status": "PROMISING_SELECTOR_ROUTE_NOT_Q_PROOF",
            "why_not_closed": "selector may be the route, but it must be derived as a constraint/auxiliary or retained as finite leak",
            "parent_signed": "False",
        },
        {
            "row_id": "FCE2528_5_chart_verdict",
            "object": "parent q field-chart/equivalence route",
            "candidate": "FCE2528_0..4 close together",
            "required_for_theorem": "q is a smooth constant-rank quotient with vertical kernel available to 2527",
            "status": "Q_FIELD_CHART_NOT_DERIVED",
            "why_not_closed": "current evidence reaches a disciplined contract, not parent kinematics",
            "parent_signed": "False",
        },
    ]
    return [stamp(row) for row in rows]


def selector_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "NPS2528_0_second_class_auxiliary",
            "route": "second-class / algebraic auxiliary compatibility",
            "test": "S_R=int mu_parent Lambda_R [R_AB-C_AB(q,theta,top)] with no derivative grammar",
            "status": "BEST_DERIVATION_ROUTE_CONDITIONAL",
            "missing": "parent origin; parent field sort; no-derivative operator exclusion; source-zero descent; boundary/readout stability",
            "selected_next": "False",
            "reason": "2360 already sharpens this and finds parent origin missing",
        },
        {
            "row_id": "NPS2528_1_first_class_constraint",
            "route": "first-class constraint / gauge quotient",
            "test": "closed brackets, differentiable generator, boundary charge zero, degree-count certificate",
            "status": "POSSIBLE_BUT_MORE_EXPENSIVE_AND_BLOCKED",
            "missing": "constraint algebra, boundary charge, no physical charge loss",
            "selected_next": "False",
            "reason": "second-class route needs fewer structures if parent origin exists",
        },
        {
            "row_id": "NPS2528_2_positive_nohair",
            "route": "positive source-free no-hair",
            "test": "Z_R>0, M_R^2>0, J_R=0, boundary flux=0, topology allowed",
            "status": "BLOCKED_BY_SOURCE_ZERO_AND_BOUNDARY_INPUTS",
            "missing": "operator signs, source-zero theorem, topology and boundary flux",
            "selected_next": "False",
            "reason": "too many independent empirical/theorem rows before q exists",
        },
        {
            "row_id": "NPS2528_3_absent_nonprimitive",
            "route": "absent / nonprimitive residual field",
            "test": "R_AB or q_R is not a primitive parent field; it is readout-derived and eliminated before variation",
            "status": "PROMISING_IF_PSI_DETERMINANT_MAP_EXISTS",
            "missing": "psi determinant / quotient map showing the residual is derived or stationary",
            "selected_next": "True",
            "reason": "2361 identifies this as the least circular next route after current-chain failure",
        },
        {
            "row_id": "NPS2528_4_finite_leak",
            "route": "finite selector / Dq / source-current leak",
            "test": "retain q_R, Dq_selector, source-current and boundary leak rows with values and units",
            "status": "FALLBACK_NONCLAIM",
            "missing": "numeric values, units, source paths, M_H_ref and arena projections",
            "selected_next": "fallback",
            "reason": "needed if psi determinant / quotient map fails",
        },
        {
            "row_id": "NPS2528_5_selector_verdict",
            "route": "route selection",
            "test": "choose next derivation target after straight q chart and current-chain routes fail",
            "status": "SELECT_PSI_DETERMINANT_QUOTIENT_NEXT",
            "missing": "not a claim; only branch routing",
            "selected_next": "True",
            "reason": "it attacks parent absence/frozenness before matter/readout rather than adding a multiplier by taste",
        },
    ]
    return [stamp(row) for row in rows]


def second_class_preview_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "SCP2528_0_conditional_theorem",
            "imported_from": "SCA2360_0_conditional_theorem",
            "statement": "second-class auxiliary/no-pole theorem is exact if parent origin, no-derivative grammar, source-zero and boundary/readout clauses all close",
            "status": "EXACT_CONDITIONAL_THEOREM_RETAINED",
            "effect_on_2528": "keeps no-pole selector as a serious derivation route",
        },
        {
            "row_id": "SCP2528_1_parent_origin",
            "imported_from": "SCA2360_1_parent_origin",
            "statement": "Lambda_R/C_R parent origin is missing",
            "status": "MISSING_PARENT_CONSTRAINT_ORIGIN",
            "effect_on_2528": "blocks promotion of selector route",
        },
        {
            "row_id": "SCP2528_2_no_derivative_grammar",
            "imported_from": "SCA2360_2_no_derivative_grammar",
            "statement": "operator grammar excluding derivative/kinetic pole is missing",
            "status": "MISSING_OPERATOR_SIGNATURE",
            "effect_on_2528": "keeps finite q_R/Dq rows live",
        },
        {
            "row_id": "SCP2528_3_zero_stress",
            "imported_from": "SCA2360_4_E_R_zero_stress",
            "statement": "R variation is stress-silent only if sources, boundary and readout reentry are also silent",
            "status": "PASS_ONLY_IF_SOURCES_ZERO",
            "effect_on_2528": "prevents treating the multiplier as harmless by definition",
        },
        {
            "row_id": "SCP2528_4_verdict",
            "imported_from": "SCA2360_6_verdict",
            "statement": "second-class route is clean but not closed for claim",
            "status": "CONDITIONAL_THEOREM_NOT_CLOSED_FOR_CLAIM",
            "effect_on_2528": "move beyond generic second-class language to parent origin / psi quotient",
        },
    ]
    return [stamp(row) for row in rows]


def current_chain_veto_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "CCV2528_0_identity",
            "imported_from": "CR2361_0_identity",
            "route": "configuration-cell identity",
            "verdict": "NAMES_TARGET_NOT_DYNAMICS",
            "reason": "an identity can define C_R but cannot select the local-GR branch",
        },
        {
            "row_id": "CCV2528_1_generic_liouville",
            "imported_from": "CR2361_1_generic_liouville",
            "route": "generic phase-volume preservation",
            "verdict": "TOO_WEAK",
            "reason": "generic conservation preserves many non-GR lanes too",
        },
        {
            "row_id": "CCV2528_2_current_chain",
            "imported_from": "CR2361_2_ordinary_current",
            "route": "ordinary radial/current conservation",
            "verdict": "REJECT_AS_STANDALONE_DERIVATION",
            "reason": "current conservation gives a charge Q_R; it does not set Q_R=0",
        },
        {
            "row_id": "CCV2528_3_multiplier_closure",
            "imported_from": "CR2361_4_nonpropagating_constraint",
            "route": "lambda_R C_R closure",
            "verdict": "CLOSURE_ONLY",
            "reason": "works as a benchmark but parent origin/backreaction remains unproved",
        },
        {
            "row_id": "CCV2528_4_psi_quotient",
            "imported_from": "CR2361_6_psi_quotient",
            "route": "psi determinant / quotient map",
            "verdict": "BEST_NEXT_NONCIRCULAR_ROUTE",
            "reason": "could show the residual is absent, vertical, or stationary before matter/readout",
        },
    ]
    return [stamp(row) for row in rows]


def finite_leak_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "FSL2528_0_selector_Dq_leak",
            "quantity": "epsilon_selector_Dq",
            "definition": "||Dq_selector[X_loc]|| / ||X_loc|| for the selector/no-pole quotient candidate",
            "required_inputs": "selector_formula;Dq_selector;Xloc_formula;norm_Q;norm_F;open_branch_domain",
            "status": "MISSING_SELECTOR_DQ_INPUTS",
        },
        {
            "row_id": "FSL2528_1_qR_charge",
            "quantity": "Q_R",
            "definition": "residual current/charge surviving ordinary phase-cell conservation",
            "required_inputs": "current_density;domain;boundary_condition;normalization;source_path",
            "status": "MISSING_QR_NUMERIC_OR_ZERO_THEOREM",
        },
        {
            "row_id": "FSL2528_2_operator_pole_leak",
            "quantity": "C_R_kinetic_or_derivative_pole",
            "definition": "finite leak if derivative/kinetic operator for residual mode is legal",
            "required_inputs": "operator_grammar;coefficient_bound;units;arena_projection",
            "status": "MISSING_OPERATOR_SIGNATURE",
        },
        {
            "row_id": "FSL2528_3_source_readout_reentry",
            "quantity": "epsilon_source_readout_selector",
            "definition": "source/readout regeneration of the residual after selector/no-pole reduction",
            "required_inputs": "source_map;readout_map;boundary_charge;M_H_ref;arena_projector",
            "status": "MISSING_SOURCE_READOUT_BOUND",
        },
        {
            "row_id": "FSL2528_4_public_claim_state",
            "quantity": "claim readiness",
            "definition": "whether selector/Dq finite rows can be scored",
            "required_inputs": "all FSL2528 rows numeric or theorem-zero with source paths",
            "status": "NOT_SCORE_READY",
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "CG2528_0_q_chart",
            "claim": "parent q field chart/equivalence relation constructed",
            "allowed": "False",
            "blocked_by": "FCE2528_1_parent_chart;FCE2528_2_equivalence_relation;FCE2528_3_computable_q",
        },
        {
            "row_id": "CG2528_1_nopole_selector",
            "claim": "no-pole/selector route removes local residual before matter/readout",
            "allowed": "False",
            "blocked_by": "SCP2528_1_parent_origin;SCP2528_2_no_derivative_grammar;SCP2528_3_zero_stress",
        },
        {
            "row_id": "CG2528_2_current_chain_origin",
            "claim": "ordinary phase-cell/current chain derives C_R=0 or q_R=0",
            "allowed": "False",
            "blocked_by": "CCV2528_2_current_chain",
        },
        {
            "row_id": "CG2528_3_local_GR_Newton",
            "claim": "local GR/Newton branch derived",
            "allowed": "False",
            "blocked_by": "CG2528_0_q_chart;CG2528_1_nopole_selector;FSL2528_4_public_claim_state",
        },
        {
            "row_id": "CG2528_4_public_or_github",
            "claim": "public/GitHub update recommended from 2528",
            "allowed": "False",
            "blocked_by": "q and selector rows remain nonclaim",
        },
    ]
    return [stamp(row) for row in rows]


def refusal_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "REF2528_0_chart_as_parent",
            "shortcut": "treat a useful parent-field chart candidate as the actual parent chart",
            "verdict": "REJECT",
            "reason": "testing grammar is not parent kinematics",
        },
        {
            "row_id": "REF2528_1_equivalence_by_desire",
            "shortcut": "define Phi~Phi' exactly to erase the local residual",
            "verdict": "REJECT",
            "reason": "equivalence relation must come from constraints/gauge/orbits or adopted parent reduction",
        },
        {
            "row_id": "REF2528_2_multiplier_by_taste",
            "shortcut": "insert Lambda_R C_R as closure and call it derived",
            "verdict": "REJECT",
            "reason": "second-class route needs parent origin, no-derivative grammar and zero-stress proof",
        },
        {
            "row_id": "REF2528_3_current_conservation_loop",
            "shortcut": "keep deriving with ordinary currents until C_R vanishes",
            "verdict": "REJECT",
            "reason": "2361 shows current conservation preserves a charge unless a separate no-charge theorem exists",
        },
        {
            "row_id": "REF2528_4_public_claim",
            "shortcut": "present the q/selector contract as local-GR derivation",
            "verdict": "REJECT",
            "reason": "contracts are exact but unsigned; local-GR/Newton remains blocked",
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "DEC2528_0_field_chart",
            "decision": "do not promote straight q field-chart/equivalence construction",
            "reason": "current evidence gives a disciplined candidate but not parent-owned kinematics",
            "effect": "q/v theorem remains blocked",
            "status": "BLOCK_CLAIM",
        },
        {
            "row_id": "DEC2528_1_selector_route",
            "decision": "retain no-pole/second-class route as the best conditional theorem path",
            "reason": "it removes the residual before matter coupling rather than labeling it vertical after the fact",
            "effect": "route remains serious but needs parent origin/no-derivative/zero-stress clauses",
            "status": "ACTIVE",
        },
        {
            "row_id": "DEC2528_2_current_chain",
            "decision": "do not loop ordinary current conservation",
            "reason": "ordinary current conservation leaves Q_R hair unless a no-charge/absence theorem is supplied",
            "effect": "move to psi determinant/quotient route",
            "status": "REJECT_STANDALONE",
        },
        {
            "row_id": "DEC2528_3_next",
            "decision": "select psi determinant / quotient map next",
            "reason": "it is the least circular route to show the local residual is absent, vertical, or stationary before matter/readout",
            "effect": "2529 attacks parent origin directly",
            "status": "SELECTED",
        },
        {
            "row_id": "DEC2528_4_finite_rows",
            "decision": "keep selector/Dq/q_R finite rows live",
            "reason": "if psi quotient fails, the theory must pay the residual bill numerically",
            "effect": "fallback remains nonclaim",
            "status": "HELD_PARALLEL",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "NEXT2528_0_selected",
            "priority": "selected",
            "next_target": "2529-Y5-R2FR-psi-determinant-quotient-map-or-finite-qR-coefficients.md",
            "script": "scripts/Y5_R2FR_psi_determinant_quotient_map_or_finite_qR_coefficients_2529.py",
            "objective": "construct q from psi determinant/quotient data and prove the local residual is absent, quotient-vertical, or stationary before matter/readout; otherwise promote finite q_R coefficients",
            "acceptance_gate": "psi map, determinant/volume relation, residual variable, Dq action, branch regularity, and matter/readout silence are all parent-signed, or q_R remains explicit finite nonclaim input",
            "do_not": "do not use ordinary current conservation alone; do not insert a closure multiplier without parent origin; do not claim local GR/Newton",
        },
        {
            "row_id": "NEXT2528_1_parallel",
            "priority": "parallel_nonclaim",
            "next_target": "2529b-Y5-R2FR-q-field-chart-adoption-certificate.md",
            "script": "scripts/Y5_R2FR_q_field_chart_adoption_certificate_2529b.py",
            "objective": "look for a direct source/adoption certificate for the q field chart if the corpus contains one",
            "acceptance_gate": "adoption source names the parent variables, equivalence relation, q components and variation order",
            "do_not": "do not adopt the chart because it is convenient",
        },
        {
            "row_id": "NEXT2528_2_fallback",
            "priority": "fallback_nonclaim",
            "next_target": "2529c-Y5-R2FR-finite-selector-Dq-qR-input-pack.md",
            "script": "scripts/Y5_R2FR_finite_selector_Dq_qR_input_pack_2529c.py",
            "objective": "source finite q_R, Dq selector, operator-pole and source/readout leak rows with units and arena projections",
            "acceptance_gate": "all finite rows have source paths, units, values or explicit blockers",
            "do_not": "do not score placeholders",
        },
    ]
    return [stamp(row) for row in rows]


def branch_copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    copies = [
        ("field_chart_audit", OUTPUTS["field_chart_audit"], BRANCH_COPIES["field_chart_audit"]),
        ("nopole_selector_gate", OUTPUTS["nopole_selector_gate"], BRANCH_COPIES["nopole_selector_gate"]),
        ("finite_leak_rows", OUTPUTS["finite_leak_rows"], BRANCH_COPIES["finite_leak_rows"]),
        ("next_target", OUTPUTS["next_target"], BRANCH_COPIES["next_target"]),
    ]
    for copy_id, source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            stamp(
                {
                    "copy_id": copy_id,
                    "source_path": str(source.relative_to(ROOT)),
                    "destination_path": str(destination.relative_to(ROOT)),
                    "destination_exists": str(destination.exists()),
                    "status": "COPIED_NONCLAIM",
                }
            )
        )
    return rows


def any_claim_enabled(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    truthy = {"true", "yes", "1", "claim_ready", "score_ready"}
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key in {"path_exists", "needle_found", "destination_exists", "selected_next"}:
                    continue
                if key in {"valid_for_claim", "claim_allowed", "claim_ready", "allowed", "parent_signed"} and str(value).strip().lower() in truthy:
                    return True
    return False


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    sources = rows_by_name["source_register"]
    checks.append(("VAL2528_00_sources_exist", all(row["path_exists"] == "True" for row in sources), "every required source path exists"))
    checks.append(("VAL2528_01_source_needles", all(row["needle_found"] == "True" for row in sources), "all required source needles found"))
    checks.append(("VAL2528_02_q_chart_not_promoted", any(row["row_id"] == "FCE2528_5_chart_verdict" and row["status"] == "Q_FIELD_CHART_NOT_DERIVED" for row in rows_by_name["field_chart_audit"]), "q field-chart/equivalence route not promoted"))
    checks.append(("VAL2528_03_selector_route_retained", any(row["row_id"] == "NPS2528_0_second_class_auxiliary" and row["status"] == "BEST_DERIVATION_ROUTE_CONDITIONAL" for row in rows_by_name["nopole_selector_gate"]), "second-class/no-pole route retained as conditional"))
    checks.append(("VAL2528_04_current_chain_rejected", any(row["row_id"] == "CCV2528_2_current_chain" and "REJECT" in row["verdict"] for row in rows_by_name["current_chain_veto"]), "ordinary current-chain shortcut rejected"))
    checks.append(("VAL2528_05_psi_next_selected", any(row["row_id"] == "NEXT2528_0_selected" and "psi" in row["next_target"] for row in rows_by_name["next_target"]), "psi determinant quotient target selected"))
    checks.append(("VAL2528_06_finite_rows_nonclaim", all(row["valid_for_claim"] == "False" for row in rows_by_name["finite_leak_rows"]), "finite q/Dq/qR rows remain nonclaim"))
    checks.append(("VAL2528_07_claim_gates_blocked", all(row["allowed"] == "False" for row in rows_by_name["claim_gates"]), "all claim gates blocked"))
    checks.append(("VAL2528_08_refusals_cover_shortcuts", len(rows_by_name["refusal_runner"]) >= 5 and all("REJECT" in row["verdict"] for row in rows_by_name["refusal_runner"]), "shortcuts refused"))
    checks.append(("VAL2528_09_no_claim_flags", not any_claim_enabled(rows_by_name), "no generated row enables claim flags"))
    checks.append(("VAL2528_10_branch_copies", all(row["destination_exists"] == "True" for row in rows_by_name["branch_copies"]), "branch copies exist"))
    checks.append(("VAL2528_11_no_formalization_artifacts", not any("formalization-workbench" in str(path).lower() for path in [DOC, *OUTPUTS.values(), *BRANCH_COPIES.values()]), "no outputs target formalization-workbench"))
    checks.append(("VAL2528_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))

    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        try:
            parsed = csv_rows(path)
            checks.append((f"VAL2528_CSV_{path.stem}", len(parsed) > 0, f"{path.name} parses"))
        except Exception as exc:
            checks.append((f"VAL2528_CSV_{path.stem}", False, f"{path.name} parse failed: {exc}"))
    for copy_id, path in BRANCH_COPIES.items():
        try:
            parsed = csv_rows(path)
            checks.append((f"VAL2528_COPY_CSV_{copy_id}", len(parsed) > 0, f"{path.name} parses"))
        except Exception as exc:
            checks.append((f"VAL2528_COPY_CSV_{copy_id}", False, f"{path.name} parse failed: {exc}"))

    overall = all(ok for _, ok, _ in checks)
    checks.append(
        (
            "VAL2528_OVERALL",
            overall,
            "2528 refuses to promote the straight q field-chart route, retains the no-pole/second-class route as conditional, rejects ordinary current-chain closure as standalone, and selects the psi determinant quotient map next.",
        )
    )
    return [stamp({"check_id": check_id, "status": "PASS" if ok else "FAIL", "details": detail}) for check_id, ok, detail in checks]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def slim(rows: list[dict[str, Any]], columns: list[str]) -> list[dict[str, Any]]:
    return [{column: row.get(column, "") for column in columns} for row in rows]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 2528 - Parent `q` Field Chart / Equivalence Relation or No-Pole Selector",
                "**Current verdict:** the straight `q` field-chart/equivalence route remains candidate-only. It gives the right theorem shape, but current evidence still does not parent-sign the field chart, equivalence relation, computable `q`, or constant-rank `Dq`.",
                "**Main gain:** this pass stops the loop. The best conditional route is not another generic current argument; it is the no-pole/second-class selector path, sharpened by 2360, plus the 2361 warning that ordinary current conservation leaves `Q_R` hair. The next noncircular target is therefore a `psi` determinant / quotient map showing the residual is absent, vertical, or stationary before matter/readout.",
                "**Claim discipline:** no local-GR/Newton/R10/PPN/clock/orbital/GitHub claim is allowed from 2528. The result is branch selection plus nonclaim finite leak rows.",
                "## Source Register",
                markdown_table(
                    slim(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needle_found", "status", "role"]),
                    ["source_id", "source_path", "path_exists", "needle_found", "status", "role"],
                ),
                "## Field Chart / Equivalence Audit",
                markdown_table(
                    slim(rows_by_name["field_chart_audit"], ["row_id", "object", "candidate", "required_for_theorem", "status", "why_not_closed", "parent_signed"]),
                    ["row_id", "object", "candidate", "required_for_theorem", "status", "why_not_closed", "parent_signed"],
                ),
                "## No-Pole Selector Gate",
                markdown_table(
                    slim(rows_by_name["nopole_selector_gate"], ["row_id", "route", "test", "status", "missing", "selected_next", "reason"]),
                    ["row_id", "route", "test", "status", "missing", "selected_next", "reason"],
                ),
                "## Second-Class Preview",
                markdown_table(
                    slim(rows_by_name["second_class_preview"], ["row_id", "imported_from", "statement", "status", "effect_on_2528"]),
                    ["row_id", "imported_from", "statement", "status", "effect_on_2528"],
                ),
                "## Current-Chain Veto",
                markdown_table(
                    slim(rows_by_name["current_chain_veto"], ["row_id", "imported_from", "route", "verdict", "reason"]),
                    ["row_id", "imported_from", "route", "verdict", "reason"],
                ),
                "## Finite Selector / `Dq` Leak Rows",
                markdown_table(
                    slim(rows_by_name["finite_leak_rows"], ["row_id", "quantity", "definition", "required_inputs", "status", "valid_for_claim"]),
                    ["row_id", "quantity", "definition", "required_inputs", "status", "valid_for_claim"],
                ),
                "## Claim Gates",
                markdown_table(
                    slim(rows_by_name["claim_gates"], ["row_id", "claim", "allowed", "blocked_by"]),
                    ["row_id", "claim", "allowed", "blocked_by"],
                ),
                "## Refusal Runner",
                markdown_table(
                    slim(rows_by_name["refusal_runner"], ["row_id", "shortcut", "verdict", "reason"]),
                    ["row_id", "shortcut", "verdict", "reason"],
                ),
                "## Decision Ledger",
                markdown_table(
                    slim(rows_by_name["decision_ledger"], ["row_id", "decision", "reason", "effect", "status"]),
                    ["row_id", "decision", "reason", "effect", "status"],
                ),
                "## Next Target",
                markdown_table(
                    slim(rows_by_name["next_target"], ["row_id", "priority", "next_target", "script", "objective", "acceptance_gate", "do_not"]),
                    ["row_id", "priority", "next_target", "script", "objective", "acceptance_gate", "do_not"],
                ),
                "## Branch Copies",
                markdown_table(
                    slim(rows_by_name["branch_copies"], ["copy_id", "source_path", "destination_path", "destination_exists", "status"]),
                    ["copy_id", "source_path", "destination_path", "destination_exists", "status"],
                ),
                "## Validation",
                markdown_table(
                    slim(rows_by_name["validation"], ["check_id", "status", "details"]),
                    ["check_id", "status", "details"],
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    remove_pycache()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "field_chart_audit": field_chart_rows(),
        "nopole_selector_gate": selector_rows(),
        "second_class_preview": second_class_preview_rows(),
        "current_chain_veto": current_chain_veto_rows(),
        "finite_leak_rows": finite_leak_rows(),
        "claim_gates": claim_gate_rows(),
        "refusal_runner": refusal_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()

    print(f"wrote {DOC}")
    for name, path in OUTPUTS.items():
        print(f"wrote {name}: {path}")
    for key, path in BRANCH_COPIES.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
