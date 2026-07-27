from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_SOURCE_WORLDTUBE_PROJECTOR_CHAINMAP_2354"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2354-Y5-R2FR-source-worldtube-projector-chainmap-zero-or-readout-reentry-bound-pack.md"

PATHS = {
    "2353_doc": ROOT / "2353-Y5-R2FR-readout-no-reentry-source-selector-zero-or-component-row.md",
    "2353_validation": OUT / "P8_Y5_BRR545_2353_VALIDATION.csv",
    "2353_audit": OUT / "P8_Y5_PARENT_QLOC_2353_READOUT_NO_REENTRY_ZERO_AUDIT.csv",
    "2353_components": OUT / "P8_Y5_PARENT_QLOC_2353_READOUT_REENTRY_COMPONENT_ROWS.csv",
    "2353_selector": OUT / "P8_Y5_PARENT_QLOC_2353_SOURCE_SELECTOR_GATE_STACK.csv",
    "2353_next": OUT / "P8_Y5_PARENT_QLOC_2353_NEXT_TARGET.csv",
    "2183_worldtube_theorem": OUT / "P8_Y5_PARENT_QLOC_2183_WORLDTUBE_HILBERT_SELECTOR_THEOREM.csv",
    "2181_worldtube_glue": OUT / "P8_Y5_PARENT_QLOC_2181_WORLDTUBE_SOURCE_GLUE_AUDIT.csv",
    "2181_pim_commutator": OUT / "P8_Y5_PARENT_QLOC_2181_PIM_COMMUTATOR_ZERO_AUDIT.csv",
    "2180_pim_jh": OUT / "P8_Y5_PARENT_QLOC_2180_PIM_JH_MASS_CURRENT_GLUE_AUDIT.csv",
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
    "1701_commutator": OUT / "P8_Y5_PARENT_QLOC_1701_READOUT_COMMUTATOR_AUDIT.csv",
    "2352_selector": OUT / "P8_Y5_PARENT_QLOC_2352_SELECTOR_BOUND_STACK.csv",
    "2350_boundary": OUT / "P8_Y5_PARENT_QLOC_2350_BOUNDARY_IMPROVEMENT_ZERO_AUDIT.csv",
    "2351_htau_href": OUT / "P8_Y5_PARENT_QLOC_2351_HTAU_HREF_SOURCE_ROW_STATUS.csv",
}

SOURCES = [
    ("SRC2354_00_2353_doc", "2353_doc", ["NEXT2353_0", "source-worldtube/projector chain-map"], "2353 selected chain-map target"),
    ("SRC2354_01_2353_validation", "2353_validation", ["VAL2353_OVERALL", "PASS"], "2353 validation"),
    ("SRC2354_02_2353_audit", "2353_audit", ["RNE2353_7_verdict", "GENERAL_ZERO_NOT_DERIVED_COMPONENT_ROWS_REQUIRED"], "2353 readout no-reentry audit"),
    ("SRC2354_03_2353_components", "2353_components", ["RRC2353_1_projector_worldtube", "MISSING_CHAINMAP_OR_COMMUTATOR_VALUE"], "2353 projector/worldtube component"),
    ("SRC2354_04_2353_selector", "2353_selector", ["SSG2353_4_projector_chainmap", "MISSING_CHAINMAP_THEOREM"], "2353 selector gate stack"),
    ("SRC2354_05_2353_next", "2353_next", ["NEXT2353_0", "2354-Y5-R2FR-source-worldtube-projector-chainmap-zero-or-readout-reentry-bound-pack.md"], "machine-readable 2354 target"),
    ("SRC2354_06_2183_worldtube_theorem", "2183_worldtube_theorem", ["WST2183_7_current_verdict", "SELECTOR_THEOREM_CONDITIONAL_CURRENT_CLAIM_FAILS"], "worldtube Hilbert selector theorem"),
    ("SRC2354_07_2181_worldtube_glue", "2181_worldtube_glue", ["WTG2181_5_current_status", "WORLDTUBE_GLUE_NOT_DERIVED"], "worldtube source glue audit"),
    ("SRC2354_08_2181_pim_commutator", "2181_pim_commutator", ["PCA2181_5_current_status", "COMMUTATOR_ZERO_NOT_DERIVED"], "Pi_M commutator zero audit"),
    ("SRC2354_09_2180_pim_jh", "2180_pim_jh", ["MCG2180_5_success_package", "NOT_SATISFIED_CURRENT_CORPUS"], "Pi_M/J_H mass-current glue"),
    ("SRC2354_10_2124_chain_rule", "2124_chain_rule", ["CR2124_4_verdict", "NORMAL_FORM_CLOSED_NUMERIC_BOUND_OPEN"], "source-feedback chain-rule normal form"),
    ("SRC2354_11_2123_zero_conditions", "2123_zero_conditions", ["ZC2123_5_no_cancellation", "RETAINED"], "commutator zero conditions"),
    ("SRC2354_12_2122_obstruction", "2122_obstruction", ["COM2122_2_countermodel", "COUNTERMODEL_ACTIVE"], "commutator obstruction ledger"),
    ("SRC2354_13_2109_lift_test", "2109_lift_test", ["DPL2109_8_verdict", "FAIL_CURRENT_CLAIM"], "domain/projector lift test"),
    ("SRC2354_14_1818_identity", "1818_identity", ["HCI1818_7_verdict", "CONDITIONAL_IDENTITY_NOT_CURRENT_PROOF"], "Hilbert-worldtube charge identity"),
    ("SRC2354_15_1817_transfer", "1817_transfer", ["KWT1817_6_verdict", "CONDITIONAL_THEOREM_NOT_CURRENT_PROOF"], "source-worldtube transfer kernel theorem"),
    ("SRC2354_16_1778_map", "1778_map", ["WCM1778_1_chain_identity", "MISSING_CHAIN_IDENTITY"], "worldtube current map"),
    ("SRC2354_17_1760_owner", "1760_owner", ["WTA1760_3_matter_worldtube_verdict", "WORLDTUBE_DESCENT_NOT_PARENT_SIGNED"], "worldtube source owner audit"),
    ("SRC2354_18_1718_selector", "1718_selector", ["WST1718_2_current_verdict", "NOT_PROVED_FOR_CURRENT_MTS"], "worldtube selector attempt"),
    ("SRC2354_19_1718_owner", "1718_owner", ["WTO1718_8_verdict", "WORLDTUBE_SUPPORT_OWNER_NOT_PROVED"], "worldtube support owner audit"),
    ("SRC2354_20_1716_contract", "1716_contract", ["TCC1716_5_conditional_zero_theorem", "CONDITIONAL_ONLY"], "fixed chain-map theorem contract"),
    ("SRC2354_21_1716_signature", "1716_signature", ["FCS1716_7_verdict", "PARENT_CHAINMAP_NOT_SIGNED"], "fixed chain-map parent signature audit"),
    ("SRC2354_22_1715_commutator", "1715_commutator", ["PCZ1715_0_product_rule", "[d,Pi_M]J_H"], "older Pi_M commutator attempt"),
    ("SRC2354_23_1715_profiles", "1715_profiles", ["I_commutator", "valid_for_claim"], "I_commutator source profile rows"),
    ("SRC2354_24_1714_equality", "1714_equality", ["WHE1714", "valid_for_claim"], "worldtube-Hilbert equality attempt"),
    ("SRC2354_25_1714_residuals", "1714_residuals", ["I_commutator", "valid_for_claim"], "R_eq/I_commutator residual rows"),
    ("SRC2354_26_1701_commutator", "1701_commutator", ["RC1701_2_projection_operator", "retained_residual"], "readout commutator audit"),
    ("SRC2354_27_2352_selector", "2352_selector", ["SBS2352_2_commutator", "MISSING_I_COMMUTATOR_THEOREM_OR_BOUND"], "source-GM selector bound stack"),
    ("SRC2354_28_2350_boundary", "2350_boundary", ["BIC2350_5_projector_equality_gap", "MISSING_EQUALITY_AND_COMMUTATOR_THEOREMS"], "boundary projector equality gap"),
    ("SRC2354_29_2351_htau_href", "2351_htau_href", ["HHS2351_3_MHref", "MISSING_H_TAU_H_REF_MHREF"], "M_H_ref denominator status"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2354_SOURCE_REGISTER.csv",
    "audit": OUT / "P8_Y5_PARENT_QLOC_2354_CHAINMAP_ZERO_AUDIT.csv",
    "antecedents": OUT / "P8_Y5_PARENT_QLOC_2354_CHAINMAP_ANTECEDENT_STATUS.csv",
    "bounds": OUT / "P8_Y5_PARENT_QLOC_2354_READOUT_REENTRY_BOUND_PACK.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2354_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2354_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2354_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2354_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2354_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2354_VALIDATION.csv",
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
    with path.open(newline="", encoding="utf-8", errors="replace") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "source_key": key,
            "source_path": str(PATHS[key]),
            "exists": b(PATHS[key].exists()),
            "required_needles": ";".join(needles),
            "needles_found": b(has_needles(PATHS[key], needles)),
            "source_role": role,
            "valid_for_claim": "false",
        }
        for row_id, key, needles, role in SOURCES
    ]


def audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMA2354_0_target",
            "object": "source-worldtube/projector chain-map",
            "statement": "Prove delta Pi_W=0 and [d,Pi_W]J_H=0 for the source-worldtube/readout projector, or retain a readout-reentry bound pack.",
            "status": "TARGET_SHARPENED",
            "proof_result": "focuses source-measure leakage on the exact chain-map/product-rule obstruction",
            "obstruction": "general chain-map not signed for current MTS",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMA2354_1_product_rule",
            "object": "projected current product rule",
            "statement": "d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H and delta(Pi_M J_H)=Pi_M delta J_H+(delta Pi_M)J_H.",
            "status": "EXACT_OBSTRUCTION_IDENTITY",
            "proof_result": "commutator/projector stress is a real residual unless Pi_M is fixed or a chain-map",
            "obstruction": "not notation; must be zero-proved or bounded",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMA2354_2_fixed_topological_route",
            "object": "metric-silent topological Pi_M",
            "statement": "If Pi_M J=ell_M(J) omega_M_top with d omega_M_top=0, fixed domain, physical-current complex and exterior silence, then [d,Pi_M]J_H=0.",
            "status": "EXACT_CONDITIONAL_ZERO_THEOREM",
            "proof_result": "clean mathematical route exists",
            "obstruction": "parent selector, physical-current domain, exterior silence and tau/M_H_ref are unsigned",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMA2354_3_worldtube_selector",
            "object": "W_source := closure(supp J_H[tau])",
            "statement": "Worldtube support is a legitimate pre-readout selector only if parent action, same frame, tau lock, compact support and linked surfaces are signed.",
            "status": "CONDITIONAL_SELECTOR_NOT_PARENT_SIGNED",
            "proof_result": "forbids fitted source masks if signed",
            "obstruction": "support owner and fixed-domain clauses remain open",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMA2354_4_source_feedback_chain_rule",
            "object": "K_A(Phi)=Pi_A(y,sigma_A)J_A(y,sigma_A)",
            "statement": "For vertical v, D_v K_A=[D_sigma Pi_A[J_A]+Pi_A D_sigma J_A]D_v sigma_A when y=(q,e_obs,A_owned,theta) is fixed.",
            "status": "NORMAL_FORM_CLOSED_NUMERIC_BOUND_OPEN",
            "proof_result": "all dangerous leakage is concentrated in protocol/support/source-feedback variables sigma_A",
            "obstruction": "no source-backed values for D_v sigma_A or bracket operator",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMA2354_5_wrong_object",
            "object": "closed wrong charge",
            "statement": "A closed topological current does not prove measured source closure unless Pi_M J_H=J_M_top+dB_zero and boundary flux vanishes.",
            "status": "CONSERVATION_NOT_ENOUGH",
            "proof_result": "blocks topological-charge shortcut",
            "obstruction": "R_eq, B_zero_flux, I_commutator and M_H_ref still live",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMA2354_6_Hodge_projector_route",
            "object": "metric/domain/Hodge/readout projector",
            "statement": "If Pi_M depends on metric, domain, normal, Green operator, support or readout, delta Pi_M and [d,Pi_M]J_H become source/stress residuals.",
            "status": "PROJECTOR_STRESS_RETAINED_IF_USED",
            "proof_result": "allowed only with finite bounds or a parent zero theorem",
            "obstruction": "no parent zero theorem or numeric stress/source row",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMA2354_7_verdict",
            "object": "promote chain-map/source-worldtube zero",
            "statement": "Current corpus does not prove delta Pi_W=0, [d,Pi_W]J_H=0, or worldtube/Hilbert measured-source identity.",
            "status": "ZERO_NOT_DERIVED_BOUND_PACK_REQUIRED",
            "proof_result": "conditional theorem preserved; nonclaim bound pack installed",
            "obstruction": "source-worldtube support owner/fixed-domain proof is now the next live subgate",
            "valid_for_claim": "false",
        },
    ]


def antecedent_rows() -> list[dict[str, Any]]:
    specs = [
        ("ANT2354_0_parent_selector", "parent selects mass/source channel before readout", "MISSING_PARENT_SELECTOR", "parent selector equation; no post-readout mask certificate", "I_selector"),
        ("ANT2354_1_fixed_domain", "source worldtube, exterior annulus and linking surface are fixed", "MISSING_FIXED_DOMAIN_OWNER", "domain selector; boundary class; radial/deformation silence theorem", "I_domain"),
        ("ANT2354_2_metric_silent_PiM", "Pi_M representative is topological and metric-independent", "CONDITIONAL_TEMPLATE_ONLY", "parent-normalized representative; metric-variation silence certificate", "I_projector_stress"),
        ("ANT2354_3_chainmap_complex", "Pi_M is a chain-map on physical Hilbert-current complex", "CONDITIONAL_MATH_ONLY", "physical current complex; parent ownership of Pi_M; allowed-current theorem", "I_commutator"),
        ("ANT2354_4_current_membership", "J_H and extra/source/frame/species channels lie in fixed complex or are theorem-zero", "MISSING_CURRENT_DOMAIN_LOCK", "Hilbert-current decomposition; species/material inclusion; frame-source theorem", "I_current_escape"),
        ("ANT2354_5_exterior_silence", "compact exterior annulus has no hidden source/anomaly/boundary/projector support", "MISSING_EXTERIOR_SILENCE_THEOREM", "no-hair/boundary theorem; anomaly operator silence; exterior support certificate", "I_exterior"),
        ("ANT2354_6_tau_MHref", "same tau and positive same-frame M_H_ref normalize projected source", "MISSING_TAU_MHREF_DENOMINATOR", "tau lock; Hamiltonian integrability; positive denominator; no orbital-GM import", "I_denominator"),
        ("ANT2354_7_worldtube_glue", "M_source[W]=integral_S Pi_M J_H=M_eff before orbital fitting", "WORLDTUBE_GLUE_NOT_DERIVED", "domain selector; Hilbert equality; extra-channel silence; calibration owner", "R_Hsrc"),
        ("ANT2354_8_verdict", "all chain-map antecedents jointly signed", "PARENT_CHAINMAP_NOT_SIGNED", "all antecedents above", "epsilon_chainmap_abs"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "antecedent": antecedent,
            "status": status,
            "missing_inputs": missing,
            "residual_if_missing": residual,
            "valid_for_claim": "false",
        }
        for row_id, antecedent, status, missing, residual in specs
    ]


def bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BP2354_0_total",
            "quantity": "epsilon_chainmap_readout_abs",
            "component": "absolute source-worldtube/projector chain-map envelope",
            "formula": "abs(I_commutator)/M_H_ref + abs(R_eq)/M_H_ref + E_projector_stress + E_worldtube + E_sigma_feedback + E_current_escape + E_exterior",
            "units": "dimensionless after M_H_ref/source-current normalization",
            "current_value": "MISSING_COMPONENT_VALUES;MISSING_M_H_REF",
            "source_needed": "all components theorem-zero or numeric source-backed rows",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BP2354_1_Icommutator",
            "quantity": "I_commutator_abs",
            "component": "[d,Pi_M]J_H exterior/source projector commutator",
            "formula": "abs(integral_A [d,Pi_M]J_H)/M_H_ref",
            "units": "dimensionless_or_GM_flux_over_M_H_ref",
            "current_value": "MISSING_I_COMMUTATOR;MISSING_M_H_REF",
            "source_needed": "fixed chain-map theorem or I_commutator source-profile row",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BP2354_2_Req",
            "quantity": "R_eq_abs",
            "component": "Hilbert/topological source equality residual",
            "formula": "abs(integral(Pi_M J_H - J_M_top - dB_zero))/M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_R_EQ_INTEGRAL;MISSING_M_H_REF",
            "source_needed": "same-object worldtube theorem, Hilbert equality and boundary zero-flux certificate",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BP2354_3_worldtube",
            "quantity": "E_worldtube",
            "component": "source support/domain selector variation",
            "formula": "||D_v W_source|| or ||D_v sigma_source|| contribution to K_source[J_H]",
            "units": "dimensionless_or_declared_source_kernel_norm",
            "current_value": "MISSING_WORLDTUBE_SUPPORT_OWNER",
            "source_needed": "W_source=closure(supp J_H[tau]) parent-owned, compact and fixed under allowed variations",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BP2354_4_projector_stress",
            "quantity": "E_projector_stress",
            "component": "metric/domain/Hodge projector stress",
            "formula": "||P_source[(delta Pi_M)J_H]|| / ||P_source[J_Hilbert]||",
            "units": "dimensionless_or_operator_norm",
            "current_value": "MISSING_PROJECTOR_STRESS_VALUE",
            "source_needed": "metric-independent Pi_M or finite Hodge/domain projector stress row",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BP2354_5_sigma_feedback",
            "quantity": "E_sigma_feedback",
            "component": "source-feedback protocol variable leakage",
            "formula": "(||D_sigma Pi_A|| ||J_A|| + ||Pi_A|| ||D_sigma J_A||) ||D_v sigma_A|| / norm_source",
            "units": "dimensionless_or_declared_kernel_norm",
            "current_value": "MISSING_SIGMA_FEEDBACK_VALUE",
            "source_needed": "sigma_A q/e_obs descent or source-backed L_A and epsilon_sigma_A rows",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BP2354_6_current_escape",
            "quantity": "E_current_escape",
            "component": "physical current outside fixed complex",
            "formula": "||P_source[J_escape]|| / ||P_source[J_Hilbert]||",
            "units": "dimensionless",
            "current_value": "MISSING_CURRENT_DOMAIN_LOCK",
            "source_needed": "Hilbert-current decomposition and extra/source/species/frame channel silence or bounds",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BP2354_7_exterior",
            "quantity": "E_exterior",
            "component": "hidden source/anomaly/boundary/projector support in exterior annulus",
            "formula": "||support(dPi_M,A_parent,B_flux,J_extra) in A_ext|| normalized by source",
            "units": "dimensionless_or_support_flux_norm",
            "current_value": "MISSING_EXTERIOR_SILENCE_THEOREM",
            "source_needed": "no-hair/boundary/anomaly/projector exterior support certificate",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2354_0_result",
            "decision": "do not claim source-worldtube/projector chain-map zero",
            "reason": "conditional theorem exists, but parent selector, fixed domain, Pi_M representative, current complex, exterior silence and M_H_ref are unsigned",
            "effect": "epsilon_chainmap_readout_abs remains live and nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2354_1_progress",
            "decision": "preserve fixed topological Pi_M route as exact conditional theorem",
            "reason": "if its antecedents close, [d,Pi_M]J_H vanishes without tuning or cancellation",
            "effect": "the next work can target antecedents rather than re-argue the product rule",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2354_2_bound_pack",
            "decision": "install chain-map/readout-reentry bound pack",
            "reason": "unsafe projector/worldtube maps must become explicit source-backed rows if theorem-zero fails",
            "effect": "no hiding source-selector leakage inside measured GM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2354_3_next",
            "decision": "select worldtube support owner/fixed-domain proof next",
            "reason": "domain selector is the first antecedent that controls both delta Pi_W and sigma_A feedback",
            "effect": "2355 targets W_source ownership and fixed domain, or fills first I_commutator/worldtube row",
            "valid_for_claim": "false",
        },
    ]


def claim_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2354_0_product_rule", "product-rule obstruction identified", "true", "identity only, not a local-GR claim"),
        ("CG2354_1_fixed_topological_theorem", "fixed topological Pi_M zero theorem", "true", "conditional theorem only"),
        ("CG2354_2_worldtube_owner", "worldtube support parent-owned", "false", "support owner/fixed-domain clauses unsigned"),
        ("CG2354_3_chainmap_signed", "Pi_M chain-map on physical Hilbert-current complex", "false", "current complex and parent Pi_M owner unsigned"),
        ("CG2354_4_Icommutator_zero", "[d,Pi_M]J_H=0", "false", "antecedents missing"),
        ("CG2354_5_Req_zero", "Pi_M J_H=J_M_top+dB_zero", "false", "same-object Hilbert/topological equality and boundary zero flux missing"),
        ("CG2354_6_bound_score_ready", "chain-map bound pack score-ready", "false", "numeric values and M_H_ref missing"),
        ("CG2354_7_measured_GM_bridge", "measured source-GM bridge closed", "false", "source-worldtube/projector chain-map remains open"),
        ("CG2354_8_local_GR_Newton", "local GR/Newton source readout recovered", "false", "requires measured source bridge and Poisson/Gauss"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "gate": gate,
            "passes_private_or_partial": partial,
            "passes_public_claim": "false",
            "why": why,
            "valid_for_claim": "false",
        }
        for row_id, gate, partial, why in specs
    ]


def refusal_rows() -> list[dict[str, Any]]:
    specs = [
        ("REF2354_0_closed_wrong_object", "closed topological current equals measured source by conservation alone", "false", "a closed wrong charge can conserve the wrong object unless Hilbert/topological equality and B_zero flux close", "CMA2354_5_wrong_object;BP2354_2_Req"),
        ("REF2354_1_post_readout_mask", "choose Pi_M after orbital/readout calibration", "false", "post-readout projector mask is forbidden as derivation and closure-only at best", "PCA2181_4_post_readout_mask;ANT2354_0_parent_selector"),
        ("REF2354_2_Hodge_free", "use Hodge/domain projector without stress row", "false", "metric/domain-dependent Pi_M produces delta Pi_M source/stress residuals", "CMA2354_6_Hodge_projector_route;BP2354_4_projector_stress"),
        ("REF2354_3_exactness_only", "use exactness/Stokes alone to remove R_eq/I_commutator", "false", "fixed domain, compact support, boundary zero flux and same-object selector are separate premises", "ANT2354_1_fixed_domain;BP2354_1_Icommutator;BP2354_2_Req"),
        ("REF2354_4_orbital_GM_denominator", "normalize commutator rows with observed orbital GM", "false", "M_H_ref must be parent-derived before orbital GM is used as readout", "ANT2354_6_tau_MHref;BP2354_0_total"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "shortcut": shortcut,
            "allowed": allowed,
            "reason": reason,
            "source_rows": sources,
            "valid_for_claim": "false",
        }
        for row_id, shortcut, allowed, reason, sources in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2354_0",
            "next_target": "2355-Y5-R2FR-worldtube-support-owner-fixed-domain-or-Icommutator-first-row.md",
            "why": "worldtube support/fixed-domain ownership is the first antecedent controlling both delta Pi_W and sigma_A source-feedback leakage",
            "route_type": "private_derivation_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2354_1",
            "next_target": "2355b-Y5-R2FR-topological-PiM-representative-adoption-or-projector-stress-row.md",
            "why": "parallel route: decide whether Pi_M is the fixed topological representative or a metric/domain projector requiring stress bounds",
            "route_type": "parallel_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2354_2",
            "next_target": "2355c-Y5-R2FR-chainmap-readout-reentry-component-acquisition-pack.md",
            "why": "fallback route: source I_commutator, R_eq, worldtube, projector stress, sigma feedback and current escape rows",
            "route_type": "fallback_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("COPY2354_0_audit", OUTPUTS["audit"], BETA_DOCS / "CHAINMAP_ZERO_AUDIT_2354_NONCLAIM.csv", "beta-source chain-map audit"),
        ("COPY2354_1_bounds", OUTPUTS["bounds"], MICRO_RESIDUALS / "READOUT_REENTRY_BOUND_PACK_2354_NONCLAIM.csv", "local residual bound-pack inputs"),
        ("COPY2354_2_decision", OUTPUTS["decision"], RAB_QUEUE / "JR2354_CHAINMAP_DECISION_LEDGER_NONCLAIM.csv", "RAB derivation/acquisition decision"),
    ]
    rows = []
    for row_id, src, dst, purpose in copies:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": str(src),
                "branch_copy_path": str(dst),
                "copy_exists": b(dst.exists()),
                "purpose": purpose,
                "valid_for_claim": "false",
            }
        )
    return rows


def formalization_hits() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    hits: list[Path] = []
    for path in FORMALIZATION.rglob("*2354*"):
        if not path.is_file():
            continue
        parts = {part.lower() for part in path.parts}
        if ".venv" in parts or "site-packages" in parts or "__pycache__" in parts:
            continue
        if path.name.startswith(("2354-", "P8_Y5_PARENT_QLOC_2354", "P8_Y5_BRR545_2354")):
            hits.append(path)
    return hits


def no_true_claim_flags(paths: list[Path]) -> bool:
    guarded_columns = {
        "valid_for_claim",
        "passes_public_claim",
        "score_ready",
        "claim_allowed",
        "valid_prediction_row",
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
    antecedents = read_csv(OUTPUTS["antecedents"])
    bounds = read_csv(OUTPUTS["bounds"])
    claims = read_csv(OUTPUTS["claims"])
    next_text = read_text(OUTPUTS["next"])
    checks = [
        ("VAL2354_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "every required source path exists"),
        ("VAL2354_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all required source needles were found"),
        ("VAL2354_02_outputs_exist", all(path.exists() and path.stat().st_size > 0 for path in produced), "all 2354 outputs written"),
        ("VAL2354_03_conditional_theorem_preserved", "CMA2354_2_fixed_topological_route" in audit_text, "fixed topological Pi_M conditional zero theorem preserved"),
        ("VAL2354_04_zero_not_promoted", "CMA2354_7_verdict" in audit_text and "ZERO_NOT_DERIVED" in audit_text, "chain-map zero not promoted"),
        ("VAL2354_05_antecedents_nonclaim", antecedents and all(row.get("valid_for_claim") == "false" for row in antecedents), "all chain-map antecedents remain nonclaim"),
        ("VAL2354_06_bound_pack_nonclaim", bounds and all(row.get("score_ready") == "false" and row.get("valid_for_claim") == "false" for row in bounds), "bound pack remains non-score-ready"),
        ("VAL2354_07_claim_gates_blocked", claims and all(row.get("passes_public_claim") == "false" and row.get("valid_for_claim") == "false" for row in claims), "all public claim gates blocked"),
        ("VAL2354_08_next_selected", "2355-Y5-R2FR-worldtube-support-owner-fixed-domain-or-Icommutator-first-row.md" in next_text, "2355 worldtube support owner/fixed-domain target selected"),
        ("VAL2354_09_branch_copies_parse", copies and all(row["copy_exists"] == "true" for row in copies), "branch copies exist"),
        ("VAL2354_10_formalization_untouched", not formalization_hits(), "no 2354 checkpoint output appears in formalization-workbench"),
        ("VAL2354_11_no_claim_flags", no_true_claim_flags(produced), "no generated row has claim/score-ready true flags"),
        ("VAL2354_12_no_github_policy", True, "public GitHub update not recommended from 2354"),
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
            "row_id": "VAL2354_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2354 preserves the fixed-chainmap conditional theorem, rejects source-worldtube/projector zero promotion, installs a readout-reentry bound pack, and selects worldtube support owner/fixed-domain as 2355.",
            "valid_for_claim": "false",
        }
    )
    return rows


def table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |\n"
    separator = "| " + " | ".join("---" for _ in columns) + " |\n"
    body = ""
    for row in rows:
        body += "| " + " | ".join(str(row.get(column, "")).replace("|", "\\|") for column in columns) + " |\n"
    return header + separator + body


def write_doc(
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    antecedents: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    refusals: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    now = datetime.now(timezone.utc).isoformat()
    content = f"""# 2354 — Y5 R2FR Source-Worldtube Projector Chainmap Zero Or Readout-Reentry Bound Pack

Generated: `{now}`

## Summary

2354 attacks the chain-map throat selected by 2353: prove `delta Pi_W = 0` and `[d,Pi_W]J_H = 0`, or keep the
readout/source-selector bound pack.

Result: the **fixed topological `Pi_M` route is an exact conditional zero theorem**, but the current MTS corpus does
not parent-sign its antecedents. The product-rule obstruction is real:

`d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H`.

So the chain-map zero is **not** promoted. The next best derivation target is worldtube support owner / fixed-domain:
prove `W_source = closure(supp J_H[tau])` is parent-owned and fixed before readout, or retain the first
`I_commutator/worldtube` source row.

## Output Files

- `{OUTPUTS["sources"]}`
- `{OUTPUTS["audit"]}`
- `{OUTPUTS["antecedents"]}`
- `{OUTPUTS["bounds"]}`
- `{OUTPUTS["decision"]}`
- `{OUTPUTS["claims"]}`
- `{OUTPUTS["refusal"]}`
- `{OUTPUTS["next"]}`
- `{OUTPUTS["copies"]}`
- `{OUTPUTS["validation"]}`

## Source Register

{table(sources, ["row_id", "source_key", "exists", "needles_found", "source_role"])}

## Chainmap Zero Audit

{table(audit, ["row_id", "object", "status", "proof_result", "obstruction", "valid_for_claim"])}

## Chainmap Antecedent Status

{table(antecedents, ["row_id", "antecedent", "status", "missing_inputs", "residual_if_missing", "valid_for_claim"])}

## Readout-Reentry Bound Pack

{table(bounds, ["row_id", "quantity", "component", "current_value", "source_needed", "score_ready", "valid_for_claim"])}

## Decision Ledger

{table(decisions, ["row_id", "decision", "reason", "effect", "valid_for_claim"])}

## Claim Gates

{table(claims, ["row_id", "gate", "passes_private_or_partial", "passes_public_claim", "why", "valid_for_claim"])}

## Refusal Runner

{table(refusals, ["row_id", "shortcut", "allowed", "reason", "source_rows", "valid_for_claim"])}

## Next Targets

{table(next_targets, ["row_id", "next_target", "why", "route_type", "valid_for_claim"])}

## Validation

{table(validation, ["row_id", "status", "detail", "valid_for_claim"])}

## Working Read

This step is progress because it prevents a very common cheat: conserving a topological object and then quietly calling
it the measured source mass. The theorem we need is now precise. If the worldtube, domain, `Pi_M` representative, current
complex, exterior annulus, `tau`, and `M_H_ref` are fixed by the parent branch, then the commutator route can close.
Without that, the residual is not philosophy; it is an explicit bound-pack object.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    audit = audit_rows()
    antecedents = antecedent_rows()
    bounds = bound_rows()
    decisions = decision_rows()
    claims = claim_rows()
    refusals = refusal_rows()
    next_targets = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["antecedents"], antecedents)
    write_csv(OUTPUTS["bounds"], bounds)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["next"], next_targets)
    copies = copy_rows()
    write_csv(OUTPUTS["copies"], copies)
    validation = validation_rows(sources, copies)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, audit, antecedents, bounds, decisions, claims, refusals, next_targets, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        failed_ids = ", ".join(row["row_id"] for row in failed)
        raise SystemExit(f"2354 validation failed: {failed_ids}")
    print(f"2354 checkpoint written: {DOC}")


if __name__ == "__main__":
    main()
