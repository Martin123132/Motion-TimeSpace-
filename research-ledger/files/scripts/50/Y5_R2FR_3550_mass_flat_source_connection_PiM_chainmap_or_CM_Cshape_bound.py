from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3550-Y5-R2FR-mass-flat-source-connection-PiM-chainmap-or-CM-Cshape-bound.md"
CANONICAL_STATUS = OUT / "P8_Y5_mass_flat_source_connection_PiM_chainmap_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3550": {"path": Path(__file__).resolve(), "role": "3550 generator"},
    "doc_3549": {
        "path": ROOT / "3549-Y5-R2FR-Hilbert-source-denominator-PiM-Htau-local-Newton-bridge.md",
        "role": "Hilbert source denominator / Newton bridge handoff",
    },
    "next_3549": {
        "path": OUT / "P8_Y5_R2FR_3549_NEXT_TARGET.csv",
        "role": "3549 selected C_M/C_shape target",
    },
    "zero_audit_3549": {
        "path": OUT / "P8_Y5_R2FR_3549_ZERO_CLAUSE_AUDIT.csv",
        "role": "C_M/C_shape obstruction status from 3549",
    },
    "bound_interface_3549": {
        "path": OUT / "P8_Y5_R2FR_3549_COMPONENT_BOUND_INTERFACE.csv",
        "role": "3549 component bound interfaces",
    },
    "pim_htau_law_3514": {
        "path": OUT / "P8_EM_PiM_Htau_commutator_residual_law.csv",
        "role": "Pi_M/H_tau residual component law",
    },
    "pim_htau_derivation_3514": {
        "path": OUT / "P8_Y5_R2FR_3514_PIM_HTAU_COMMUTATOR_DERIVATION.csv",
        "role": "source branch coordinates and commutator derivation",
    },
    "source_flatness_3515": {
        "path": OUT / "P8_EM_source_branch_mass_connection_flatness_law.csv",
        "role": "source-branch connection flatness law",
    },
    "quotient_descent_3516": {
        "path": OUT / "P8_EM_quotient_source_coordinate_descent_certificate.csv",
        "role": "quotient source-coordinate descent certificate",
    },
    "pim_chainmap_2585": {
        "path": OUT / "P8_Y5_PIM_CHAINMAP_2585_THEOREM_AUDIT.csv",
        "role": "Pi_M chainmap theorem audit",
    },
    "pim_chainmap_2585_gate": {
        "path": OUT / "P8_Y5_PIM_CHAINMAP_2585_ANTECEDENT_GATE.csv",
        "role": "Pi_M chainmap antecedent gate",
    },
    "pim_commutator_bounds_2585": {
        "path": OUT / "P8_Y5_PIM_CHAINMAP_2585_ICOMMUTATOR_BOUND_ROWS.csv",
        "role": "nonclaim Pi_M commutator bound rows",
    },
    "pim_chainmap_3373": {
        "path": OUT / "P8_Y5_R2FR_3373_PIM_CHAINMAP_COMMUTATOR_THEOREM_ATTEMPT.csv",
        "role": "fixed topological chainmap attempt",
    },
    "pim_chainmap_3426": {
        "path": OUT / "P8_Y5_R2FR_3426_PIM_CHAIN_MAP_THEOREM.csv",
        "role": "Hilbert identity/inclusion Pi_M branch",
    },
    "field_quotient_2570": {
        "path": OUT / "P8_Y5_FIELD_QUOTIENT_2570_DQ_VERTICAL_GENERATOR_LEDGER.csv",
        "role": "Dq vertical generator ledger",
    },
    "common_descent_2643": {
        "path": OUT / "P8_Y5_COMMON_DESCENT_DQZ_2643_PARENT_SIGNATURE_THEOREM_GATE.csv",
        "role": "common quotient-descent signature gate",
    },
    "worldtube_2611": {
        "path": OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv",
        "role": "worldtube/source owner audit",
    },
    "htau_curl_2667": {
        "path": OUT / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv",
        "role": "H_tau integrability curl gate",
    },
    "mhref_reference_2938": {
        "path": OUT / "P8_Y5_R2FR_2938_MHREF_ELLJ_REFERENCE_LOCK_CONTRACT.csv",
        "role": "M_H_ref / H_ref / ell_J reference lock",
    },
}


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv_rows(path)
    except (csv.Error, OSError, UnicodeDecodeError):
        return False
    return True


def markdown_escape(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join("---" for _ in fields) + " |"
    body = [
        "| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(item["path"]),
            "exists": bool_text(item["path"].exists()),
            "role": item["role"],
            "valid_for_claim": "False",
        }
        for source_id, item in SOURCES.items()
    ]


def source_connection_identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "identity_id": "SCI3550_0_source_coordinate_map",
            "claim_piece": "source coordinates",
            "mathematical_form": "Y^I(Phi) := (M_H_ref(Phi), sigma^a(Phi))",
            "derived_statement": "The C_M/C_shape obstruction is the failure of source coordinates to be constant along the residual direction.",
            "required_signature": "M_H_ref and sigma^a must be parent-selected before readout and must factor through q(Phi).",
            "current_status": "EXACT_DEFINITION_NONCLAIM",
            "source_path": str(SOURCES["source_flatness_3515"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "identity_id": "SCI3550_1_induced_connection",
            "claim_piece": "source branch connection",
            "mathematical_form": "A_X^I := D_X Y^I = dY^I(v_X)",
            "derived_statement": "A_X is not a free coupling in this route; it is the chain-rule derivative of source-coordinate readout along v_X.",
            "required_signature": "actual residual vector v_X and actual q map must be supplied.",
            "current_status": "DERIVED_IDENTITY_NOT_ZERO",
            "source_path": str(SOURCES["source_flatness_3515"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "identity_id": "SCI3550_2_commutator_lock",
            "claim_piece": "Pi_M denominator square",
            "mathematical_form": "[D_X,Pi_M]F = -(partial_M A_X^M) partial_M F - (partial_M A_X^a) partial_a F + R_domain + R_frame + R_ref",
            "derived_statement": "C_M and C_shape are exactly the mass derivative of this source connection, not a vague coupling problem.",
            "required_signature": "source coordinate chart and Pi_M branch must be fixed on the same Hilbert source object.",
            "current_status": "EXACT_COMPONENT_LOCK_NONCLAIM",
            "source_path": str(SOURCES["pim_htau_derivation_3514"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "identity_id": "SCI3550_3_quotient_pullback_zero",
            "claim_piece": "mass-flat zero theorem",
            "mathematical_form": "Y=Ybar(q(Phi)) and Dq(v_X)=0 => A_X^I=dYbar^I(Dq(v_X))=0",
            "derived_statement": "This is the cleanest available route: vertical residuals cannot change q-basic source coordinates.",
            "required_signature": "v_X in ker(Dq), M_H_ref q-basic, sigma^a q-basic, same tau/coframe/surface branch.",
            "current_status": "EXACT_CONDITIONAL_THEOREM_NOT_LIVE",
            "source_path": str(SOURCES["quotient_descent_3516"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "identity_id": "SCI3550_4_mass_flat_corollary",
            "claim_piece": "C_M/C_shape zero",
            "mathematical_form": "A_X^I=0 on the source branch => partial_M A_X^M=0 and partial_M A_X^a=0",
            "derived_statement": "If quotient pullback zero is parent-signed, both first algebraic denominator obstructions vanish without fitting.",
            "required_signature": "all quotient/source-coordinate clauses in the zero proof must be signed by parent action or source construction.",
            "current_status": "CONDITIONAL_COROLLARY_NOT_PROMOTED",
            "source_path": str(SOURCES["source_flatness_3515"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def zero_proof_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "ZP3550_0_vertical_residual",
            "clause": "residual direction is vertical",
            "condition": "Dq(v_X)=0",
            "math_result_if_true": "the source-coordinate pullback derivative can vanish",
            "current_evidence": "field quotient ledger exists, but no concrete q matrix / residual basis has been parent-signed here",
            "proof_status": "UNSIGNED",
            "zero_effect": "needed for both C_M and C_shape",
            "blocking_gap": "MISSING_ACTUAL_Q_MAP_AND_VX_KERNEL_CERTIFICATE",
            "source_path": str(SOURCES["field_quotient_2570"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "ZP3550_1_MHref_qbasic",
            "clause": "mass coordinate descends",
            "condition": "M_H_ref(Phi)=Mbar_H_ref(q(Phi))",
            "math_result_if_true": "A_X^M=0 for vertical v_X",
            "current_evidence": "3516 reduces this to q-basic H_tau and q-basic H_ref on the same branch",
            "proof_status": "UNSIGNED",
            "zero_effect": "kills C_M through partial_M A_X^M=0",
            "blocking_gap": "MISSING_HTAU_HREF_QBASIC_DESCENT_AND_POSITIVE_DENOMINATOR",
            "source_path": str(SOURCES["quotient_descent_3516"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "ZP3550_2_sigma_qbasic",
            "clause": "shape/support coordinates descend",
            "condition": "sigma^a(Phi)=sigmabar^a(q(Phi))",
            "math_result_if_true": "A_X^a=0 for vertical v_X",
            "current_evidence": "3516 reduces this to W_source=closure(supp J_H[tau]) with no fitted domain mask",
            "proof_status": "UNSIGNED",
            "zero_effect": "kills C_shape through partial_M A_X^a=0",
            "blocking_gap": "MISSING_WORLD_TUBE_SOURCE_CURRENT_OWNER_AND_COMPACT_SUPPORT_CERTIFICATE",
            "source_path": str(SOURCES["worldtube_2611"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "ZP3550_3_same_branch",
            "clause": "same source branch before readout",
            "condition": "tau, coframe, surface, H_ref and source support are fixed before orbital GM / PPN readout",
            "math_result_if_true": "prevents readout-defined mass/shape leakage",
            "current_evidence": "reference and worldtube contracts exist, but are conditional",
            "proof_status": "UNSIGNED",
            "zero_effect": "prevents C_ref/C_domain from re-entering C_M/C_shape",
            "blocking_gap": "MISSING_REFERENCE_SELECTOR_AND_SURFACE_BRANCH_SIGNATURE",
            "source_path": str(SOURCES["mhref_reference_2938"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "ZP3550_4_PiM_same_object",
            "clause": "Pi_M acts on same Hilbert source object",
            "condition": "Pi_M is identity/inclusion or fixed chainmap on the same source-current complex",
            "math_result_if_true": "kills the independent Pi_M-current commutator route",
            "current_evidence": "3426 shows the Hilbert identity/inclusion route is exact conditional; 2585/3373 keep old topological route unsigned",
            "proof_status": "PREFERRED_ROUTE_IDENTIFIED_NOT_SIGNED",
            "zero_effect": "stops projector stress from masquerading as source denominator drift",
            "blocking_gap": "MISSING_PARENT_DECLARATION_THAT_PIM_IS_THE_HILBERT_IDENTITY_INCLUSION_BRANCH",
            "source_path": str(SOURCES["pim_chainmap_3426"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "ZP3550_5_no_readout_laundering",
            "clause": "no fitted mask or representative-dependent source coordinate",
            "condition": "Y^I is not chosen by observational residual minimization or by a representative Weyl/disformal gauge",
            "math_result_if_true": "quotient zero is physical rather than a coordinate closure",
            "current_evidence": "3516 filter installed; current source-coordinate descent certificate is still not parent-owned",
            "proof_status": "UNSIGNED",
            "zero_effect": "keeps C_M/C_shape zero from being a closure axiom",
            "blocking_gap": "MISSING_NO_READOUT_SOURCE_COORDINATE_SIGNATURE",
            "source_path": str(SOURCES["quotient_descent_3516"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def chainmap_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "PCR3550_0_Hilbert_identity_inclusion",
            "route": "Hilbert same-object Pi_M",
            "exact_statement": "If Pi_M^H is the identity/inclusion on the Hilbert mass-charge current object, [d,Pi_M^H]J_H=0.",
            "helps_C_M_Cshape": "indirectly: removes independent projector-current hair, but still needs source-coordinate descent for A_X",
            "current_status": "BEST_ROUTE_CONDITIONAL",
            "why": "least extra structure and least scrutiny; no new topological projector stress",
            "source_path": str(SOURCES["pim_chainmap_3426"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "route_id": "PCR3550_1_fixed_basis_chainmap",
            "route": "fixed basis chainmap",
            "exact_statement": "If Pi_M is fixed before variation and d Pi_M=Pi_M d on the source complex, the chainmap commutator vanishes.",
            "helps_C_M_Cshape": "partially: still leaves mass/shape source-connection derivatives unless Y is q-basic",
            "current_status": "CONDITIONAL_WITH_MORE_ASSUMPTIONS",
            "why": "needs fixed basis, source complex and domain locks",
            "source_path": str(SOURCES["pim_chainmap_2585"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "route_id": "PCR3550_2_old_topological_PiM",
            "route": "old topological projector",
            "exact_statement": "Topological Pi_M can be bounded, but is not the clean local-GR route unless same-object theorem is supplied.",
            "helps_C_M_Cshape": "weakly: it risks introducing projector stress that then has to be separately bounded",
            "current_status": "DEMOTED_TO_BOUND_BRANCH",
            "why": "higher scrutiny burden than Hilbert identity/inclusion",
            "source_path": str(SOURCES["pim_chainmap_3373"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "route_id": "PCR3550_3_source_coordinate_descent",
            "route": "q-basic source coordinates",
            "exact_statement": "Y=Ybar(q(Phi)) and Dq(v_X)=0 imply A_X=0, hence C_M=C_shape=0.",
            "helps_C_M_Cshape": "directly: this is the actual mass-flat mechanism",
            "current_status": "MATHEMATICALLY_CLEAN_BUT_UNSIGNED",
            "why": "turns coupling problem into parent quotient/source-coordinate geometry",
            "source_path": str(SOURCES["quotient_descent_3516"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "B3550_0_C_M_direct",
            "component": "C_M",
            "residual_formula": "C_M = -(partial_M A_X^M) partial_M(H_tau-H_ref)/(Pi_M H_tau)",
            "needed_parent_inputs": "partial_M A_X^M; partial_M(H_tau-H_ref); positive Pi_M H_tau; source branch units",
            "available_source_basis": "3514/3515 formulas only; no numeric parent coefficient",
            "candidate_arena": "Gdot/orbital mass drift; local PPN source normalization; R10 source coupling",
            "units": "dimensionless residual or yr^-1 after arena projection",
            "prediction_value": "MISSING_MASS_CONNECTION_VALUE",
            "bound_value": "MISSING_ARENA_PROJECTION_BOUND",
            "status": "NONCLAIM_BOUND_ROW_READY_FOR_SOURCE_INPUT",
            "source_path": str(SOURCES["bound_interface_3549"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "B3550_1_C_M_time_anchor",
            "component": "C_M",
            "residual_formula": "|partial_t ln M_H_ref| <= local mass-variation / Gdot-style bound after projection",
            "needed_parent_inputs": "map from A_X^M to time drift; clock/orbital source projection; denominator lock",
            "available_source_basis": "3549 records a 4.0e-14 yr^-1 template anchor, not a complete claim row",
            "candidate_arena": "orbital timing / mass-variation proxy",
            "units": "yr^-1",
            "prediction_value": "MISSING_TIME_PROJECTION_FOR_PARTIAL_M_A_XM",
            "bound_value": "4.0e-14 anchor_from_3514_template_only",
            "status": "ANCHOR_ONLY_NONCLAIM",
            "source_path": str(SOURCES["bound_interface_3549"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "B3550_2_C_shape_direct",
            "component": "C_shape",
            "residual_formula": "C_shape = -(partial_M A_X^a) partial_a(H_tau-H_ref)/(Pi_M H_tau)",
            "needed_parent_inputs": "partial_M A_X^a; shape derivative of H_tau-H_ref; compact support/worldtube coordinates; projection units",
            "available_source_basis": "3514/3516 formulas only; no numeric parent shape coefficient",
            "candidate_arena": "PPN anisotropic source leakage; WEP/R10 profile dependence; orbital multipole residuals",
            "units": "dimensionless residual after source-profile projection",
            "prediction_value": "MISSING_SOURCE_SHAPE_CONNECTION_VALUE",
            "bound_value": "MISSING_SHAPE_PROJECTION_BOUND",
            "status": "NONCLAIM_BOUND_ROW_READY_FOR_SOURCE_INPUT",
            "source_path": str(SOURCES["bound_interface_3549"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "B3550_3_C_shape_worldtube",
            "component": "C_shape",
            "residual_formula": "|D_X sigma^a| bounded by source-support/readout leakage",
            "needed_parent_inputs": "worldtube owner; compact support; no fitted domain mask; shape-to-arena transfer matrix",
            "available_source_basis": "2611/3516 identify the owner, but no numeric support leakage coefficient",
            "candidate_arena": "composition dependence, R10 source profile, local PPN multipoles",
            "units": "dimensionless shape leakage",
            "prediction_value": "MISSING_WORLDTUBE_SHAPE_LEAKAGE_COEFFICIENT",
            "bound_value": "MISSING_PROFILE_DEPENDENT_BOUND",
            "status": "NONCLAIM_BOUND_ROW_READY_FOR_SOURCE_INPUT",
            "source_path": str(SOURCES["worldtube_2611"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D3550_0_zero_proof_verdict",
            "question": "Did 3550 prove parent-owned C_M=C_shape=0?",
            "decision": "No. It proves the exact conditional theorem, but the q-basic source-coordinate signatures are unsigned.",
            "basis": "A_X=dY(v_X), so Y=Ybar(q(Phi)) and Dq(v_X)=0 would force A_X=0; current corpus lacks the signed q map, M_H_ref descent and sigma descent.",
            "consequence": "No Newton/local-GR claim; C_M/C_shape remain closure/bound components.",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "D3550_1_route_choice",
            "question": "Which Pi_M route should survive?",
            "decision": "Prefer Hilbert identity/inclusion plus q-basic source coordinates; demote old topological Pi_M to a bound branch.",
            "basis": "3426 kills same-object Pi_M current hair conditionally with fewer extra structures; topological Pi_M adds scrutiny and projector stress.",
            "consequence": "Future derivations should not circle broad Pi_M audits; attack M_H_ref and sigma^a descent clauses directly.",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "D3550_2_next_target",
            "question": "What is the next narrow derivation target?",
            "decision": "Prove or bound M_H_ref q-basic descent first.",
            "basis": "C_M is the first algebraic obstruction and only needs H_tau/H_ref descent on the same branch.",
            "consequence": "Move to 3551: M_H_ref q-basic descent or H_tau-H_ref bound pack.",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS3550_0",
            "checkpoint": "3550 mass-flat source connection Pi_M chainmap or C_M/C_shape bound",
            "claim_allowed": "False",
            "C_M_status": "EXACT_ZERO_IF_MHref_QBASIC_AND_VX_VERTICAL; CURRENTLY_UNSIGNED",
            "C_shape_status": "EXACT_ZERO_IF_SIGMA_QBASIC_AND_VX_VERTICAL; CURRENTLY_UNSIGNED",
            "strongest_result": "A_X^I=dYbar^I(Dq(v_X)) proves a real mechanism, not a plateau axiom, but it is not parent-signed yet",
            "route_status": "Hilbert identity/inclusion Pi_M preferred; topological Pi_M demoted",
            "next_target": "3551-Y5-R2FR-MHref-qbasic-descent-or-Htau-Href-bound-pack.md",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3550_0",
            "target_doc": "3551-Y5-R2FR-MHref-qbasic-descent-or-Htau-Href-bound-pack.md",
            "target_script": "scripts/Y5_R2FR_3551_MHref_qbasic_descent_or_Htau_Href_bound_pack.py",
            "objective": "derive M_H_ref q-basic descent by proving H_tau and H_ref descend through q on the same tau/coframe/surface branch; if not, create finite nonclaim A_X^M / D_X M_H_ref bound rows",
            "success_gate": "either A_X^M=0 is parent-owned, or C_M obtains numeric/source-ready bound inputs with units and arena projections",
            "reason": "C_M is the first denominator obstruction and the mass-coordinate half of the source-connection zero theorem",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(
    generated_csvs: list[Path],
    sources: list[dict[str, Any]],
    zero_proof: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    all_sources_exist = all(row["exists"] == "True" for row in sources)
    csvs_parse = all(csv_parse_ok(path) for path in generated_csvs)
    required_clauses = {
        "ZP3550_0_vertical_residual",
        "ZP3550_1_MHref_qbasic",
        "ZP3550_2_sigma_qbasic",
        "ZP3550_4_PiM_same_object",
    }
    covered_clauses = {row["clause_id"] for row in zero_proof}
    required_zero_clauses_covered = required_clauses.issubset(covered_clauses)
    zero_nonclaim = all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in zero_proof)
    bounds_nonclaim = all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in bounds)
    missing_markers_present = all("MISSING_" in row["prediction_value"] or "anchor" in row["bound_value"] for row in bounds)
    decisions_nonclaim = all(row["valid_for_claim"] == "False" for row in decisions)
    no_formalization_outputs = all(not path.resolve().is_relative_to(FORMALIZATION.resolve()) for path in generated_csvs)

    return [
        {
            "validation_id": "VAL3550_0_sources_exist",
            "passes": bool_text(all_sources_exist),
            "status": "PASS" if all_sources_exist else "FAIL",
            "detail": f"{sum(row['exists'] == 'True' for row in sources)}/{len(sources)} cited source paths exist",
        },
        {
            "validation_id": "VAL3550_1_generated_csvs_parse",
            "passes": bool_text(csvs_parse),
            "status": "PASS" if csvs_parse else "FAIL",
            "detail": f"{len(generated_csvs)} generated CSV files parse with DictReader",
        },
        {
            "validation_id": "VAL3550_2_required_zero_clauses_covered",
            "passes": bool_text(required_zero_clauses_covered),
            "status": "PASS" if required_zero_clauses_covered else "FAIL",
            "detail": "vertical residual, M_H_ref descent, sigma descent and Pi_M same-object clauses are present",
        },
        {
            "validation_id": "VAL3550_3_zero_rows_nonclaim",
            "passes": bool_text(zero_nonclaim),
            "status": "PASS" if zero_nonclaim else "FAIL",
            "detail": "all zero-proof rows keep claim_allowed=false and valid_for_claim=false",
        },
        {
            "validation_id": "VAL3550_4_bounds_nonclaim_with_missing_markers",
            "passes": bool_text(bounds_nonclaim and missing_markers_present),
            "status": "PASS" if bounds_nonclaim and missing_markers_present else "FAIL",
            "detail": "C_M/C_shape bound rows remain nonclaim and expose missing parent inputs",
        },
        {
            "validation_id": "VAL3550_5_decisions_nonclaim",
            "passes": bool_text(decisions_nonclaim),
            "status": "PASS" if decisions_nonclaim else "FAIL",
            "detail": "decision ledger does not promote a Newton/local-GR claim",
        },
        {
            "validation_id": "VAL3550_6_formalization_workbench_untouched",
            "passes": bool_text(no_formalization_outputs),
            "status": "PASS" if no_formalization_outputs else "FAIL",
            "detail": "3550 generated outputs only inside post-checkpoint-work",
        },
    ]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3550 - Mass-flat source connection PiM chainmap or C_M/C_shape bound",
        "",
        "## Verdict",
        "",
        "- **Real progress:** the `C_M/C_shape` problem is no longer a vague coupling hole. It is exactly the derivative of the source-coordinate map `Y=(M_H_ref,sigma^a)` along the residual direction.",
        "- **Clean theorem:** if `Y=Ybar(q(Phi))` and `Dq(v_X)=0`, then `A_X=dY(v_X)=dYbar(Dq(v_X))=0`; therefore `partial_M A_X^M=partial_M A_X^a=0` and both `C_M` and `C_shape` vanish.",
        "- **Not a live claim yet:** the current corpus has not parent-signed the actual q map, vertical residual basis, `M_H_ref` q-basic descent, or `sigma^a` q-basic descent.",
        "- **Best route:** use Hilbert identity/inclusion `Pi_M` plus q-basic source coordinates; keep the older topological `Pi_M` branch demoted to explicit bounds.",
        "",
        "## Source Connection Identities",
        "",
        markdown_table(
            rows_by_name["identities"],
            ["identity_id", "claim_piece", "mathematical_form", "derived_statement", "current_status"],
        ),
        "",
        "## Zero-Proof Attempt",
        "",
        markdown_table(
            rows_by_name["zero_proof"],
            ["clause_id", "clause", "condition", "proof_status", "zero_effect", "blocking_gap"],
        ),
        "",
        "## PiM Route Compare",
        "",
        markdown_table(
            rows_by_name["chainmap_routes"],
            ["route_id", "route", "exact_statement", "helps_C_M_Cshape", "current_status"],
        ),
        "",
        "## Bound Rows If Zero Fails",
        "",
        markdown_table(
            rows_by_name["bounds"],
            ["bound_id", "component", "residual_formula", "prediction_value", "bound_value", "status"],
        ),
        "",
        "## Decisions",
        "",
        markdown_table(
            rows_by_name["decisions"],
            ["decision_id", "question", "decision", "consequence"],
        ),
        "",
        "## Validation",
        "",
        markdown_table(
            rows_by_name["validation"],
            ["validation_id", "passes", "status", "detail"],
        ),
        "",
        "## Next target",
        "",
        "Move to `3551-Y5-R2FR-MHref-qbasic-descent-or-Htau-Href-bound-pack.md`: prove or bound the mass-coordinate half first, because `M_H_ref` q-basic descent is the shortest path to `C_M=0`.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    identities = source_connection_identity_rows()
    zero_proof = zero_proof_attempt_rows()
    chainmap_routes = chainmap_route_rows()
    bounds = bound_rows()
    decisions = decision_rows()
    status = status_rows()
    next_target = next_target_rows()

    outputs: dict[Path, tuple[list[dict[str, Any]], list[str]]] = {
        OUT / "P8_Y5_R2FR_3550_SOURCE_REGISTER.csv": (
            sources,
            ["source_id", "path", "exists", "role", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3550_SOURCE_CONNECTION_IDENTITY.csv": (
            identities,
            [
                "identity_id",
                "claim_piece",
                "mathematical_form",
                "derived_statement",
                "required_signature",
                "current_status",
                "source_path",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3550_MASS_FLAT_ZERO_PROOF_ATTEMPT.csv": (
            zero_proof,
            [
                "clause_id",
                "clause",
                "condition",
                "math_result_if_true",
                "current_evidence",
                "proof_status",
                "zero_effect",
                "blocking_gap",
                "source_path",
                "claim_allowed",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3550_PIM_CHAINMAP_ROUTE_COMPARE.csv": (
            chainmap_routes,
            ["route_id", "route", "exact_statement", "helps_C_M_Cshape", "current_status", "why", "source_path", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3550_CM_CSHAPE_BOUND_ROWS.csv": (
            bounds,
            [
                "bound_id",
                "component",
                "residual_formula",
                "needed_parent_inputs",
                "available_source_basis",
                "candidate_arena",
                "units",
                "prediction_value",
                "bound_value",
                "status",
                "source_path",
                "claim_allowed",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3550_DECISION_LEDGER.csv": (
            decisions,
            ["decision_id", "question", "decision", "basis", "consequence", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3550_STATUS.csv": (
            status,
            [
                "status_id",
                "checkpoint",
                "claim_allowed",
                "C_M_status",
                "C_shape_status",
                "strongest_result",
                "route_status",
                "next_target",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3550_NEXT_TARGET.csv": (
            next_target,
            ["next_id", "target_doc", "target_script", "objective", "success_gate", "reason", "valid_for_claim"],
        ),
        CANONICAL_STATUS: (
            status,
            [
                "status_id",
                "checkpoint",
                "claim_allowed",
                "C_M_status",
                "C_shape_status",
                "strongest_result",
                "route_status",
                "next_target",
                "valid_for_claim",
            ],
        ),
    }

    generated_paths: list[Path] = []
    for path, (rows, fields) in outputs.items():
        write_csv(path, rows, fields)
        generated_paths.append(path)

    validation = validation_rows(generated_paths, sources, zero_proof, bounds, decisions)
    validation_path = OUT / "P8_Y5_BRR545_3550_VALIDATION.csv"
    write_csv(validation_path, validation, ["validation_id", "passes", "status", "detail"])
    generated_paths.append(validation_path)

    write_doc(
        {
            "identities": identities,
            "zero_proof": zero_proof,
            "chainmap_routes": chainmap_routes,
            "bounds": bounds,
            "decisions": decisions,
            "status": status,
            "validation": validation,
            "next_target": next_target,
        }
    )

    print(f"wrote {DOC}")
    for path in generated_paths:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
