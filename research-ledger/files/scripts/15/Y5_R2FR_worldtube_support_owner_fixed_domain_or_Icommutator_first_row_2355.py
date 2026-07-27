from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_WORLDTUBE_SUPPORT_FIXED_DOMAIN_ICOMMUTATOR_2355"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2355-Y5-R2FR-worldtube-support-owner-fixed-domain-or-Icommutator-first-row.md"

PATHS = {
    "2354_doc": ROOT / "2354-Y5-R2FR-source-worldtube-projector-chainmap-zero-or-readout-reentry-bound-pack.md",
    "2354_validation": OUT / "P8_Y5_BRR545_2354_VALIDATION.csv",
    "2354_antecedents": OUT / "P8_Y5_PARENT_QLOC_2354_CHAINMAP_ANTECEDENT_STATUS.csv",
    "2354_bounds": OUT / "P8_Y5_PARENT_QLOC_2354_READOUT_REENTRY_BOUND_PACK.csv",
    "2354_decision": OUT / "P8_Y5_PARENT_QLOC_2354_DECISION_LEDGER.csv",
    "2354_next": OUT / "P8_Y5_PARENT_QLOC_2354_NEXT_TARGET.csv",
    "2183_worldtube_theorem": OUT / "P8_Y5_PARENT_QLOC_2183_WORLDTUBE_HILBERT_SELECTOR_THEOREM.csv",
    "2181_worldtube_glue": OUT / "P8_Y5_PARENT_QLOC_2181_WORLDTUBE_SOURCE_GLUE_AUDIT.csv",
    "2181_pim_commutator": OUT / "P8_Y5_PARENT_QLOC_2181_PIM_COMMUTATOR_ZERO_AUDIT.csv",
    "2124_chain_rule": OUT / "P8_Y5_PARENT_QLOC_2124_SOURCE_FEEDBACK_CHAIN_RULE.csv",
    "2123_zero_conditions": OUT / "P8_Y5_PARENT_QLOC_2123_COMMUTATOR_ZERO_CONDITIONS.csv",
    "2122_obstruction": OUT / "P8_Y5_PARENT_QLOC_2122_COMMUTATOR_OBSTRUCTION_LEDGER.csv",
    "2109_lift_test": OUT / "P8_Y5_PARENT_QLOC_2109_DOMAIN_PROJECTOR_LIFT_TEST.csv",
    "1818_identity": OUT / "P8_Y5_PARENT_QLOC_1818_HILBERT_WORLDTUBE_CHARGE_IDENTITY_THEOREM.csv",
    "1817_transfer": OUT / "P8_Y5_PARENT_QLOC_1817_SOURCE_WORLDTUBE_TRANSFER_KERNEL_THEOREM.csv",
    "1778_map": OUT / "P8_Y5_PARENT_QLOC_1778_WORLDTUBE_CURRENT_MAP.csv",
    "1760_owner": OUT / "P8_Y5_PARENT_QLOC_1760_WORLDTUBE_SOURCE_OWNER_AUDIT.csv",
    "1718_selector": OUT / "P8_Y5_PARENT_QLOC_1718_WORLDTUBE_SELECTOR_THEOREM_ATTEMPT.csv",
    "1718_owner": OUT / "P8_Y5_PARENT_QLOC_1718_WORLDTUBE_SUPPORT_OWNER_AUDIT.csv",
    "1716_contract": OUT / "P8_Y5_PARENT_QLOC_1716_FIXED_CHAINMAP_THEOREM_CONTRACT.csv",
    "1716_signature": OUT / "P8_Y5_PARENT_QLOC_1716_FIXED_CHAINMAP_PARENT_SIGNATURE_AUDIT.csv",
    "1715_commutator": OUT / "P8_Y5_PARENT_QLOC_1715_PIM_COMMUTATOR_ZERO_ATTEMPT.csv",
    "1715_profiles": OUT / "P8_Y5_PARENT_QLOC_1715_ICOMMUTATOR_SOURCE_PROFILE_ROWS.csv",
    "1714_equality": OUT / "P8_Y5_PARENT_QLOC_1714_WORLDTUBE_HILBERT_EQUALITY_ATTEMPT.csv",
    "1714_residuals": OUT / "P8_Y5_PARENT_QLOC_1714_REQ_ICOMMUTATOR_RESIDUAL_ROWS.csv",
    "2351_htau_href": OUT / "P8_Y5_PARENT_QLOC_2351_HTAU_HREF_SOURCE_ROW_STATUS.csv",
}

SOURCES = [
    ("SRC2355_00_2354_doc", "2354_doc", ["Result:", "fixed topological `Pi_M` route"], "2354 result summary"),
    ("SRC2355_01_2354_validation", "2354_validation", ["VAL2354_OVERALL", "PASS"], "2354 validation"),
    ("SRC2355_02_2354_antecedent", "2354_antecedents", ["ANT2354_1_fixed_domain", "MISSING_FIXED_DOMAIN_OWNER"], "fixed-domain antecedent"),
    ("SRC2355_03_2354_bounds", "2354_bounds", ["BP2354_1_Icommutator", "MISSING_COMPONENT_VALUES"], "I_commutator bound pack"),
    ("SRC2355_04_2354_decision", "2354_decision", ["DEC2354_3_next", "fixed-domain"], "2354 next decision"),
    ("SRC2355_05_2354_next", "2354_next", ["NEXT2354_0", "2355-Y5-R2FR-worldtube-support-owner-fixed-domain-or-Icommutator-first-row.md"], "machine target for 2355"),
    ("SRC2355_06_2183_selector", "2183_worldtube_theorem", ["WST2183_1_worldtube_selector", "EXACT_SELECTOR_DEFINITION_CONDITIONAL"], "worldtube selector theorem"),
    ("SRC2355_07_2183_verdict", "2183_worldtube_theorem", ["WST2183_7_current_verdict", "SELECTOR_THEOREM_CONDITIONAL_CURRENT_CLAIM_FAILS"], "worldtube theorem verdict"),
    ("SRC2355_08_2181_domain", "2181_worldtube_glue", ["WTG2181_1_domain_selector", "MISSING_PARENT_DOMAIN_SELECTOR"], "worldtube/domain selector gap"),
    ("SRC2355_09_2181_commutator", "2181_pim_commutator", ["PCA2181_0_product_rule", "EXACT_PRODUCT_RULE"], "Pi_M product-rule obstruction"),
    ("SRC2355_10_2181_comm_status", "2181_pim_commutator", ["PCA2181_5_current_status", "COMMUTATOR_ZERO_NOT_DERIVED"], "commutator-zero status"),
    ("SRC2355_11_1760_owner", "1760_owner", ["WTA1760_3_matter_worldtube_verdict", "WORLDTUBE_DESCENT_NOT_PARENT_SIGNED"], "worldtube descent owner"),
    ("SRC2355_12_1718_support", "1718_owner", ["WTO1718_3_support_selector", "FORMAL_SELECTOR_CONDITIONAL_NOT_PARENT_SIGNED"], "support selector owner"),
    ("SRC2355_13_1718_compactness", "1718_owner", ["WTO1718_4_compactness_regular_support", "CONDITIONAL_TOPOLOGICAL_STEP"], "compact regular support"),
    ("SRC2355_14_1716_contract", "1716_contract", ["TCC1716_5_conditional_zero_theorem", "CONDITIONAL_ONLY"], "fixed-chainmap theorem contract"),
    ("SRC2355_15_1716_signature", "1716_signature", ["FCS1716_7_verdict", "PARENT_CHAINMAP_NOT_SIGNED"], "parent chainmap signature"),
    ("SRC2355_16_1715_product", "1715_commutator", ["PCZ1715_0_product_rule", "[d,Pi_M]J_H"], "older commutator product row"),
    ("SRC2355_17_1715_profiles", "1715_profiles", ["I_commutator", "valid_for_claim"], "I_commutator source profile rows"),
    ("SRC2355_18_1714_equality", "1714_equality", ["WHE1714", "valid_for_claim"], "worldtube-Hilbert equality attempt"),
    ("SRC2355_19_1714_residuals", "1714_residuals", ["I_commutator", "valid_for_claim"], "R_eq/I_commutator residual rows"),
    ("SRC2355_20_2124_chain_rule", "2124_chain_rule", ["CR2124_4_verdict", "NORMAL_FORM_CLOSED_NUMERIC_BOUND_OPEN"], "source-feedback chain rule"),
    ("SRC2355_21_2123_conditions", "2123_zero_conditions", ["ZC2123_5_no_cancellation", "RETAINED"], "commutator zero conditions"),
    ("SRC2355_22_2122_countermodel", "2122_obstruction", ["COM2122_2_countermodel", "COUNTERMODEL_ACTIVE"], "commutator countermodel"),
    ("SRC2355_23_2109_lift", "2109_lift_test", ["DPL2109_8_verdict", "FAIL_CURRENT_CLAIM"], "domain/projector lift test"),
    ("SRC2355_24_1818_identity", "1818_identity", ["HCI1818_7_verdict", "CONDITIONAL_IDENTITY_NOT_CURRENT_PROOF"], "Hilbert-worldtube charge identity"),
    ("SRC2355_25_1817_transfer", "1817_transfer", ["KWT1817_6_verdict", "CONDITIONAL_THEOREM_NOT_CURRENT_PROOF"], "source-worldtube transfer kernel"),
    ("SRC2355_26_1778_map", "1778_map", ["WCM1778_1_chain_identity", "MISSING_CHAIN_IDENTITY"], "worldtube current map"),
    ("SRC2355_27_2351_mhref", "2351_htau_href", ["HHS2351_3_MHref", "MISSING_H_TAU_H_REF_MHREF"], "M_H_ref denominator gap"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2355_SOURCE_REGISTER.csv",
    "audit": OUT / "P8_Y5_PARENT_QLOC_2355_FIXED_DOMAIN_THEOREM_AUDIT.csv",
    "clauses": OUT / "P8_Y5_PARENT_QLOC_2355_SUPPORT_OWNER_CLAUSES.csv",
    "icommutator": OUT / "P8_Y5_PARENT_QLOC_2355_ICOMMUTATOR_FIRST_ROW.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2355_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2355_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2355_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2355_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2355_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2355_VALIDATION.csv",
}


def b(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def has_needles(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return path.exists() and all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8", errors="replace") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, Any]]:
    rows = []
    for row_id, source_key, needles, role in SOURCES:
        path = PATHS[source_key]
        exists = path.exists()
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": source_key,
                "path": str(path),
                "exists": b(exists),
                "required_needles": ";".join(needles),
                "needles_found": b(has_needles(path, needles)),
                "source_role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def fixed_domain_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "FDT2355_0_source_worldtube_definition",
            "theorem_clause": "define W_source before readout",
            "mathematical_statement": "W_source := closure(supp J_H[e_obs,tau]) with J_H and tau parent-owned.",
            "status": "EXACT_CONDITIONAL_DEFINITION",
            "proof_result": "not a fitted radius if J_H and tau already descend from the parent action",
            "missing_signature": "parent source current; tau lock; same observed coframe",
            "residual_if_missing": "I_support_owner",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FDT2355_1_vertical_support_descent",
            "theorem_clause": "vertical variations do not move quotient support",
            "mathematical_statement": "If J_H=q^* Jbar_H, v in ker(Dq), and supp(Jbar_H) is regular, then D_v q(W_source)=0.",
            "status": "EXACT_CONDITIONAL_LEMMA",
            "proof_result": "the support can move only by representative gauge, not by quotient physics",
            "missing_signature": "J_H=q^*Jbar_H; regular support; no representative-dependent matter current",
            "residual_if_missing": "I_vertical_support",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FDT2355_2_fixed_annulus_linking_class",
            "theorem_clause": "exterior annulus and linking surfaces are fixed",
            "mathematical_statement": "A_ext and [S]_link are chosen from q(W_source) and the source-free exterior homology before orbital fitting.",
            "status": "CONDITIONAL_TOPOLOGICAL_STEP",
            "proof_result": "kills domain-mask reentry if the parent owns the topology",
            "missing_signature": "domain owner; source-free exterior; boundary class silence",
            "residual_if_missing": "I_domain",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FDT2355_3_stokes_fixed_domain",
            "theorem_clause": "Stokes theorem applies to the same fixed object",
            "mathematical_statement": "For fixed A_ext, compact support outside A_ext, fixed tau/reference, and zero anomaly channels, int_A d(Pi_W J_H)=int_dA Pi_W J_H.",
            "status": "EXACT_CONDITIONAL_STOKES",
            "proof_result": "boundary cancellation is legal only after same-object and fixed-domain clauses are signed",
            "missing_signature": "zero boundary flux; no hidden extra support; fixed reference Hamiltonian",
            "residual_if_missing": "I_boundary_flux",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FDT2355_4_commutator_normal_form",
            "theorem_clause": "moving/projector domain exposes the first row",
            "mathematical_statement": "[d,Pi_W]J_H = dchi_W wedge P_M J_H + chi_W[d,P_M]J_H + source/protocol terms.",
            "status": "NORMAL_FORM_RETAINED",
            "proof_result": "all failed fixed-domain clauses become explicit source-backed terms rather than invisible assumptions",
            "missing_signature": "dchi_W row; projector representative; source-current derivative; M_H_ref",
            "residual_if_missing": "I_commutator",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FDT2355_5_post_readout_mask_blocker",
            "theorem_clause": "post-readout support choice is not derivation",
            "mathematical_statement": "Choosing W_source, A_ext, or Pi_W after orbital/PPN readout is a closure, not a GR-limit proof.",
            "status": "FORBIDDEN_AS_LOCAL_GR_DERIVATION",
            "proof_result": "keeps MTS from smuggling measured GM/source masks into the derivation",
            "missing_signature": "pre-readout parent selector",
            "residual_if_missing": "I_readout_mask",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FDT2355_6_current_corpus_verdict",
            "theorem_clause": "promote fixed-domain zero",
            "mathematical_statement": "Current corpus does not parent-sign J_H descent, tau lock, fixed annulus, zero exterior support, zero boundary flux, or M_H_ref.",
            "status": "ZERO_NOT_DERIVED_FIRST_ROW_REQUIRED",
            "proof_result": "conditional theorem survives, but the public/local-GR route remains blocked",
            "missing_signature": "support owner chain; domain owner chain; numeric first I_commutator row",
            "residual_if_missing": "epsilon_chainmap_readout_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FDT2355_7_best_next_route",
            "theorem_clause": "next proof target",
            "mathematical_statement": "Prove parent source-current descent J_H=q^*Jbar_H and regular support invariance, or source the dchi/moving-boundary row.",
            "status": "NEXT_DERIVATION_SELECTED",
            "proof_result": "2356 should hit the source-current descent/coupling owner rather than loop on Stokes alone",
            "missing_signature": "parent matter coupling/source-current descent map",
            "residual_if_missing": "I_domain_mask_motion",
            "valid_for_claim": "false",
        },
    ]


def support_owner_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SOC2355_0_parent_current",
            "required_clause": "parent action defines the Hilbert source current",
            "required_form": "J_H[tau]=delta S_matter[e_obs,psi]/delta e_obs contracted with fixed tau",
            "current_status": "UNSIGNED_PARENT_ACTION_CURRENT",
            "why_it_matters": "without this, support can be an empirical mask",
            "zero_if_signed": "I_support_owner",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SOC2355_1_same_frame_tau",
            "required_clause": "same observed coframe and tau are used for matter, clocks, source and orbit readout",
            "required_form": "e_obs^matter=e_obs^clock=e_obs^orbit and tau_source=tau_readout=tau_charge",
            "current_status": "SAME_FRAME_TAU_LOCK_OPEN",
            "why_it_matters": "frame/time drift can move the support boundary",
            "zero_if_signed": "I_tau_drift",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SOC2355_2_quotient_descent",
            "required_clause": "source current descends through q",
            "required_form": "J_H=q^*Jbar_H and L_v J_H=0 modulo exact/gauge terms for v in ker(Dq)",
            "current_status": "MISSING_SOURCE_CURRENT_DESCENT_PROOF",
            "why_it_matters": "this is the clean way to make vertical support motion disappear",
            "zero_if_signed": "I_vertical_support",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SOC2355_3_regular_compact_support",
            "required_clause": "support is compact, regular, and has a buffer annulus",
            "required_form": "closure(supp J_H) compact; A_ext cap supp(J_H)=empty; no singular tail crosses S",
            "current_status": "CONDITIONAL_TOPOLOGICAL_STEP_ONLY",
            "why_it_matters": "Stokes/linking arguments need a stable source-free exterior",
            "zero_if_signed": "I_source_tail",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SOC2355_4_fixed_domain_owner",
            "required_clause": "exterior annulus and linking surfaces are parent-owned",
            "required_form": "D_v A_ext=0 and D_v[S]_link=0 before orbital fitting",
            "current_status": "MISSING_FIXED_DOMAIN_OWNER",
            "why_it_matters": "moving boundaries create dchi and i_v boundary terms",
            "zero_if_signed": "I_domain_mask_motion",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SOC2355_5_exterior_silence",
            "required_clause": "no hidden exterior source, anomaly, boundary, species or projector support",
            "required_form": "J_extra=dPi=dB_flux=anomaly=0 on A_ext, or bounded by sourced rows",
            "current_status": "MISSING_EXTERIOR_SILENCE_THEOREM",
            "why_it_matters": "otherwise an exact-looking flux hides finite matter/source leakage",
            "zero_if_signed": "I_exterior",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SOC2355_6_no_readout_mask",
            "required_clause": "domain/projector is not selected after seeing orbital GM",
            "required_form": "Pi_W and W_source are fixed by parent branch/topology, not by fitted readout",
            "current_status": "GUARDRAIL_INSTALLED_NOT_THEOREM",
            "why_it_matters": "post-readout masks can counterfeit a GR/Newton limit",
            "zero_if_signed": "I_readout_mask",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SOC2355_7_MHref_denominator",
            "required_clause": "same positive Hamiltonian denominator normalizes the row",
            "required_form": "M_H_ref=H_tau[S_outer]-H_ref >0 and is parent-derived, not observed orbital GM",
            "current_status": "MISSING_H_TAU_H_REF_MHREF",
            "why_it_matters": "the first commutator row cannot become dimensionless without the denominator",
            "zero_if_signed": "I_denominator",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SOC2355_8_verdict",
            "required_clause": "fixed-domain support owner chain",
            "required_form": "all SOC2355_0..7 signed by parent action or replaced by numeric source-backed rows",
            "current_status": "NOT_CLOSED",
            "why_it_matters": "local GR remains a derivation target, not a claimed theorem",
            "zero_if_signed": "epsilon_chainmap_readout_abs",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
    ]


def icommutator_first_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ICFR2355_0_total_first_row",
            "quantity": "I_commutator_abs_over_MHref",
            "component": "first explicit domain/projector commutator envelope",
            "normal_form": "abs(I_domain_mask+I_boundary_crossing+I_source_tail+I_tau_drift+I_projector_rep+I_current_escape)/M_H_ref",
            "source_required": "all component rows numeric; M_H_ref parent-derived; no placeholder source paths",
            "units": "dimensionless",
            "status": "MISSING_COMPONENT_VALUES",
            "valid_for_claim": "false",
            "score_ready": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ICFR2355_1_domain_mask_motion",
            "quantity": "I_domain_mask",
            "component": "moving support/domain mask",
            "normal_form": "abs(int_A dchi_W wedge P_M J_H)/M_H_ref",
            "source_required": "source-backed dchi_W or theorem D_v W_source=0",
            "units": "source_flux_over_M_H_ref",
            "status": "MISSING_DCHI_OR_FIXED_DOMAIN_THEOREM",
            "valid_for_claim": "false",
            "score_ready": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ICFR2355_2_boundary_crossing",
            "quantity": "I_boundary_crossing",
            "component": "moving boundary/linking surface crossing term",
            "normal_form": "abs(int_boundary(A_ext) i_v(Pi_W J_H))/M_H_ref",
            "source_required": "boundary velocity/support flux or theorem i_v(Pi_W J_H)=0 on boundary",
            "units": "source_flux_over_M_H_ref",
            "status": "MISSING_BOUNDARY_FLUX_BOUND",
            "valid_for_claim": "false",
            "score_ready": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ICFR2355_3_source_tail",
            "quantity": "I_source_tail",
            "component": "unowned source/anomaly/species support in exterior annulus",
            "normal_form": "abs(int_A chi_W P_M dJ_H_extra)/M_H_ref",
            "source_required": "extra-channel silence theorem or finite exterior source row",
            "units": "source_flux_over_M_H_ref",
            "status": "MISSING_EXTERIOR_SILENCE_OR_BOUND",
            "valid_for_claim": "false",
            "score_ready": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ICFR2355_4_tau_drift",
            "quantity": "I_tau_drift",
            "component": "source support changes under tau/readout generator drift",
            "normal_form": "norm(partial_tau(Pi_W J_H))*abs(delta_tau)/M_H_ref",
            "source_required": "tau lock theorem or numeric tau-drift response",
            "units": "dimensionless",
            "status": "MISSING_TAU_LOCK_OR_RESPONSE_BOUND",
            "valid_for_claim": "false",
            "score_ready": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ICFR2355_5_projector_representative",
            "quantity": "I_projector_rep",
            "component": "non-topological projector/Hodge/domain representative",
            "normal_form": "abs(int_A chi_W [d,P_M]J_H)/M_H_ref",
            "source_required": "fixed topological representative proof or projector-stress bound",
            "units": "source_flux_over_M_H_ref",
            "status": "MISSING_PROJECTOR_REPRESENTATIVE_DECISION",
            "valid_for_claim": "false",
            "score_ready": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ICFR2355_6_current_escape",
            "quantity": "I_current_escape",
            "component": "physical current outside fixed chain-map/source complex",
            "normal_form": "norm(P_source[J_escape])/M_H_ref",
            "source_required": "allowed-current theorem or source-backed escape norm",
            "units": "dimensionless",
            "status": "MISSING_CURRENT_DOMAIN_LOCK",
            "valid_for_claim": "false",
            "score_ready": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ICFR2355_7_row_acceptance_rule",
            "quantity": "I_commutator_first_row_acceptance",
            "component": "acceptance gate for replacing zero proof by a finite row",
            "normal_form": "row accepted only if every numerator, M_H_ref, units, source path and extraction method are real",
            "source_required": "no MISSING_* statuses; valid_for_claim can flip only after parent/sourced numeric closure",
            "units": "gate",
            "status": "NONCLAIM_ACCEPTANCE_RULE_INSTALLED",
            "valid_for_claim": "false",
            "score_ready": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2355_0_result",
            "decision": "do not claim fixed-domain/source-worldtube zero",
            "reason": "the quotient support-descent theorem is clean but not parent-signed in the corpus",
            "effect": "I_commutator remains live and gets a first explicit row",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2355_1_progress",
            "decision": "preserve the derivation route",
            "reason": "if J_H=q^*Jbar_H and W_source is quotient-owned, vertical support motion disappears without tuning",
            "effect": "the next mathematical target is source-current descent through q",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2355_2_bound_fallback",
            "decision": "install first I_commutator row",
            "reason": "if support/domain ownership fails, dchi and boundary-crossing terms must be sourced rather than suppressed",
            "effect": "domain/projector leakage becomes auditable instead of hidden",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2355_3_next",
            "decision": "select parent source-current descent next",
            "reason": "this is the least handwavy route to fixed W_source and local-GR/Newton source ownership",
            "effect": "2356 targets J_H=q^*Jbar_H or fills the moving-domain row",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2355_0_fixed_domain_zero",
            "claim": "D_v W_source=0 and D_v A_ext=0",
            "passes_public_claim": "false",
            "blocked_by": "SOC2355_0_parent_current;SOC2355_1_same_frame_tau;SOC2355_2_quotient_descent;SOC2355_4_fixed_domain_owner",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2355_1_Icommutator_zero",
            "claim": "I_commutator=0",
            "passes_public_claim": "false",
            "blocked_by": "ICFR2355_1_domain_mask_motion;ICFR2355_2_boundary_crossing;ICFR2355_5_projector_representative",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2355_2_local_GR_Newton_source_limit",
            "claim": "local GR/Newton source normalization derived",
            "passes_public_claim": "false",
            "blocked_by": "M_H_ref missing; source-current descent missing; R_eq/I_commutator still nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2355_3_github_public_update",
            "claim": "ready for public GitHub update from 2355",
            "passes_public_claim": "false",
            "blocked_by": "private nonclaim checkpoint; fixed-domain proof not closed",
            "valid_for_claim": "false",
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2355_0_definition_only",
            "temptation": "claim W_source is fixed because it is defined as supp(J_H)",
            "allowed": "false",
            "why_not": "definitions do not prove parent ownership, tau lock, or vertical support invariance",
            "blocking_rows": "SOC2355_0_parent_current;SOC2355_2_quotient_descent",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2355_1_stokes_only",
            "temptation": "use Stokes/exactness alone to set domain terms to zero",
            "allowed": "false",
            "why_not": "Stokes acts on a fixed object; moving masks and boundary crossing produce dchi/i_v terms",
            "blocking_rows": "FDT2355_4_commutator_normal_form;ICFR2355_1_domain_mask_motion",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2355_2_observed_GM_backfill",
            "temptation": "normalize the row with observed orbital GM",
            "allowed": "false",
            "why_not": "that would import the measured Newtonian limit into the proof",
            "blocking_rows": "SOC2355_7_MHref_denominator",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2355_3_public_claim",
            "temptation": "treat the clean conditional theorem as a local-GR pass",
            "allowed": "false",
            "why_not": "the antecedents are still unsigned; the first commutator row is nonnumeric",
            "blocking_rows": "CG2355_0_fixed_domain_zero;CG2355_1_Icommutator_zero",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2355_0",
            "next_target": "2356-Y5-R2FR-parent-source-current-descent-or-domain-motion-bound.md",
            "why": "source-current descent through q is the clean route to fixed W_source and zero domain-motion terms",
            "route_type": "derivation_first",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2355_1",
            "next_target": "2356b-Y5-R2FR-Icommutator-domain-motion-source-acquisition-pack.md",
            "why": "fallback if J_H descent cannot be parent-signed: source dchi/boundary/current escape rows",
            "route_type": "fallback_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2355_2",
            "next_target": "2356c-Y5-R2FR-topological-PiW-representative-or-projector-stress-bound.md",
            "why": "parallel route if support descent closes but projector representative remains metric/domain dependent",
            "route_type": "parallel_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def copy_branch_artifacts() -> list[dict[str, Any]]:
    copies = [
        (OUTPUTS["clauses"], BETA_DOCS / "SUPPORT_OWNER_CLAUSES_2355_NONCLAIM.csv", "beta docs support-owner clauses"),
        (OUTPUTS["icommutator"], MICRO_RESIDUALS / "ICOMMUTATOR_FIRST_ROW_2355_NONCLAIM.csv", "microscope residual first row"),
        (OUTPUTS["decision"], RAB_QUEUE / "JR2355_FIXED_DOMAIN_DECISION_LEDGER_NONCLAIM.csv", "RAB queue decision ledger"),
    ]
    rows = []
    for src, dst, role in copies:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": f"COPY2355_{len(rows)}",
                "source": str(src),
                "destination": str(dst),
                "copy_role": role,
                "copy_exists": b(dst.exists() and dst.stat().st_size > 0),
                "valid_for_claim": "false",
            }
        )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body]) + "\n"


def write_markdown(
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    icommutator: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    refusals: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    created = datetime.now(timezone.utc).isoformat()
    text = f"""# 2355 — Worldtube Support Owner / Fixed Domain Or `I_commutator` First Row

Created UTC: `{created}`

Branch: `{BRANCH_ID}`

## Result

Result: the **fixed-domain worldtube route has a clean conditional theorem**, but the current corpus still does **not**
parent-sign the source-current descent and support-owner chain needed to claim

`D_v W_source = 0`, `D_v A_ext = 0`, or `I_commutator = 0`.

The useful progress is sharper than a failure: the obstruction has now been compressed into a first explicit row,

`[d,Pi_W]J_H = dchi_W wedge P_M J_H + chi_W[d,P_M]J_H + source/protocol terms`.

So we do **not** claim local GR/Newton yet. We preserve the proof route and make the fallback auditable.

## Source Audit

{md_table(sources, ["row_id", "source_key", "exists", "needles_found", "source_role"])}

## Fixed-Domain Theorem Audit

{md_table(audit, ["row_id", "theorem_clause", "status", "proof_result", "missing_signature", "residual_if_missing", "valid_for_claim"])}

## Support Owner Clauses

{md_table(clauses, ["row_id", "required_clause", "current_status", "why_it_matters", "zero_if_signed", "parent_signed", "valid_for_claim"])}

## First `I_commutator` Row

{md_table(icommutator, ["row_id", "quantity", "component", "normal_form", "status", "units", "score_ready", "valid_for_claim"])}

## Decision Ledger

{md_table(decisions, ["row_id", "decision", "reason", "effect", "valid_for_claim"])}

## Claim Gates

{md_table(claims, ["row_id", "claim", "passes_public_claim", "blocked_by", "valid_for_claim"])}

## Refusal Runner

{md_table(refusals, ["row_id", "temptation", "allowed", "why_not", "blocking_rows", "valid_for_claim"])}

## Next Targets

{md_table(next_targets, ["row_id", "next_target", "why", "route_type", "valid_for_claim"])}

## Validation

{md_table(validation, ["row_id", "status", "detail", "valid_for_claim"])}
"""
    DOC.write_text(text, encoding="utf-8")


def formalization_hits() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    hits: list[Path] = []
    for path in FORMALIZATION.rglob("*2355*"):
        if not path.is_file():
            continue
        parts = {part.lower() for part in path.parts}
        if ".venv" in parts or "site-packages" in parts or "__pycache__" in parts:
            continue
        if path.name.startswith(("2355-", "P8_Y5_PARENT_QLOC_2355", "P8_Y5_BRR545_2355")):
            hits.append(path)
    return hits


def no_true_claim_flags(paths: list[Path]) -> bool:
    guarded_columns = {
        "valid_for_claim",
        "passes_public_claim",
        "score_ready",
        "claim_allowed",
        "valid_prediction_row",
        "parent_signed",
    }
    for path in paths:
        if path.suffix.lower() != ".csv":
            continue
        for row in read_csv(path):
            for column in guarded_columns:
                if row.get(column, "").strip().lower() == "true":
                    return False
    return True


def validation_rows(sources: list[dict[str, Any]], copies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    produced = [path for key, path in OUTPUTS.items() if key != "validation"]
    audit_text = read_text(OUTPUTS["audit"])
    clauses = read_csv(OUTPUTS["clauses"])
    icommutator = read_csv(OUTPUTS["icommutator"])
    claims = read_csv(OUTPUTS["claims"])
    next_text = read_text(OUTPUTS["next"])
    checks = [
        ("VAL2355_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "every required source path exists"),
        ("VAL2355_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all required source needles were found"),
        ("VAL2355_02_outputs_exist", all(path.exists() and path.stat().st_size > 0 for path in produced), "all 2355 outputs written"),
        ("VAL2355_03_conditional_theorem_preserved", "FDT2355_1_vertical_support_descent" in audit_text, "vertical support descent conditional theorem preserved"),
        ("VAL2355_04_zero_not_promoted", "FDT2355_6_current_corpus_verdict" in audit_text and "ZERO_NOT_DERIVED" in audit_text, "fixed-domain/I_commutator zero not promoted"),
        ("VAL2355_05_support_clauses_nonclaim", clauses and all(row.get("parent_signed") == "false" and row.get("valid_for_claim") == "false" for row in clauses), "support-owner clauses remain nonclaim"),
        ("VAL2355_06_icommutator_rows_nonclaim", icommutator and all(row.get("score_ready") == "false" and row.get("valid_for_claim") == "false" for row in icommutator), "I_commutator first rows remain non-score-ready"),
        ("VAL2355_07_claim_gates_blocked", claims and all(row.get("passes_public_claim") == "false" and row.get("valid_for_claim") == "false" for row in claims), "all public claim gates blocked"),
        ("VAL2355_08_next_selected", "2356-Y5-R2FR-parent-source-current-descent-or-domain-motion-bound.md" in next_text, "2356 source-current descent target selected"),
        ("VAL2355_09_branch_copies_parse", copies and all(row["copy_exists"] == "true" for row in copies), "branch copies exist"),
        ("VAL2355_10_formalization_untouched", not formalization_hits(), "no 2355 checkpoint output appears in formalization-workbench"),
        ("VAL2355_11_no_claim_flags", no_true_claim_flags(produced), "no generated row has claim/score-ready/parent-signed true flags"),
        ("VAL2355_12_no_github_policy", True, "public GitHub update not recommended from 2355"),
    ]
    rows = [
        {
            "row_id": row_id,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, ok, detail in checks
    ]
    rows.append(
        {
            "row_id": "VAL2355_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2355 preserves the clean fixed-domain support theorem as conditional, refuses zero promotion, installs the first explicit I_commutator row, and selects parent source-current descent as 2356.",
            "valid_for_claim": "false",
        }
    )
    return rows


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    audit = fixed_domain_audit_rows()
    clauses = support_owner_clause_rows()
    icommutator = icommutator_first_rows()
    decisions = decision_rows()
    claims = claim_gate_rows()
    refusals = refusal_rows()
    next_targets = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["clauses"], clauses)
    write_csv(OUTPUTS["icommutator"], icommutator)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["next"], next_targets)

    copies = copy_branch_artifacts()
    write_csv(OUTPUTS["copies"], copies)

    validation = validation_rows(sources, copies)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(sources, audit, clauses, icommutator, decisions, claims, refusals, next_targets, validation)

    if validation[-1]["status"] != "PASS":
        failed = ", ".join(row["row_id"] for row in validation if row["status"] != "PASS")
        raise SystemExit(f"2355 validation failed: {failed}")
    print(f"2355 checkpoint written: {DOC}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
