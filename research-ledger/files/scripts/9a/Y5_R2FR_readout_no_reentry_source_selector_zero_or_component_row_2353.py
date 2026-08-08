from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_READOUT_NO_REENTRY_SOURCE_SELECTOR_2353"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2353-Y5-R2FR-readout-no-reentry-source-selector-zero-or-component-row.md"

PATHS = {
    "2352_doc": ROOT / "2352-Y5-R2FR-source-charge-equals-measured-GM-or-selector-bound.md",
    "2352_validation": OUT / "P8_Y5_BRR545_2352_VALIDATION.csv",
    "2352_residuals": OUT / "P8_Y5_PARENT_QLOC_2352_BRIDGE_RESIDUAL_STATUS.csv",
    "2352_selector": OUT / "P8_Y5_PARENT_QLOC_2352_SELECTOR_BOUND_STACK.csv",
    "2352_next": OUT / "P8_Y5_PARENT_QLOC_2352_NEXT_TARGET.csv",
    "2346_components": OUT / "P8_Y5_PARENT_QLOC_2346_NONHILBERT_COMPONENT_BOUND_PACK.csv",
    "2335_certificate": OUT / "P8_Y5_PARENT_QLOC_2335_SOURCE_READOUT_ARGUMENT_CERTIFICATE.csv",
    "2324_zero": OUT / "P8_Y5_PARENT_QLOC_2324_ALPHA_READOUT_ZERO_PROOF_ATTEMPT.csv",
    "2324_bound": OUT / "P8_Y5_PARENT_QLOC_2324_FIRST_ALPHA_READOUT_BOUND_ROW.csv",
    "2203_fixed": OUT / "P8_Y5_PARENT_QLOC_2203_FIXED_BEFORE_READOUT_MAP_ATTEMPT.csv",
    "2203_alpha": OUT / "P8_Y5_PARENT_QLOC_2203_ALPHA_READOUT_ROW.csv",
    "2202_readout": OUT / "P8_Y5_PARENT_QLOC_2202_READOUT_ZERO_THEOREM_ATTEMPT.csv",
    "2177_gate": OUT / "P8_Y5_PARENT_QLOC_2177_OBSERVABLE_READOUT_GATE.csv",
    "2177_residuals": OUT / "P8_Y5_PARENT_QLOC_2177_READOUT_LOCK_RESIDUAL_ROWS.csv",
    "2122_lemma": OUT / "P8_Y5_PARENT_QLOC_2122_SOURCE_READOUT_OWNER_LEMMA.csv",
    "2118_zero": OUT / "P8_Y5_PARENT_QLOC_2118_SOURCE_READOUT_ZERO_THEOREM_ATTEMPT.csv",
    "1898_commutator": OUT / "P8_Y5_PARENT_QLOC_1898_READOUT_VARIATION_COMMUTATOR_ZERO_ATTEMPT.csv",
    "1888_stability": OUT / "P8_Y5_PARENT_QLOC_1888_READOUT_STABILITY_PROOF_ATTEMPT.csv",
    "1816_theorem": OUT / "P8_Y5_PARENT_QLOC_1816_VARIATION_BEFORE_READOUT_THEOREM.csv",
    "1816_selector": OUT / "P8_Y5_PARENT_QLOC_1816_SOURCE_SELECTOR_ORDER_AUDIT.csv",
    "1802_gate": OUT / "P8_Y5_PARENT_QLOC_1802_MATTER_READOUT_THEOREM_GATE.csv",
    "1802_type": OUT / "P8_Y5_PARENT_QLOC_1802_READOUT_TYPE_SPLIT.csv",
    "1701_no_reentry": OUT / "P8_Y5_PARENT_QLOC_1701_NO_REENTRY_THEOREM_ATTEMPT.csv",
    "1701_commutator": OUT / "P8_Y5_PARENT_QLOC_1701_READOUT_COMMUTATOR_AUDIT.csv",
    "1701_queue": OUT / "P8_Y5_PARENT_QLOC_1701_READOUT_RESIDUAL_QUEUE.csv",
    "1700_target": OUT / "P8_Y5_PARENT_QLOC_1700_READOUT_NO_REENTRY_TARGET.csv",
    "967_schema": OUT / "P8_Y5_R10_967_READOUT_SCHEMA_THEOREM_ATTEMPT.csv",
    "967_counter": OUT / "P8_Y5_R10_967_READOUT_COUNTERMODEL_AUDIT.csv",
    "968_clause": OUT / "P8_Y5_R10_968_READOUT_EXCLUSION_CLAUSE.csv",
    "969_certificate": OUT / "P8_Y5_R10_969_READOUT_DOMAIN_CERTIFICATE.csv",
    "1471_radiative": OUT / "P8_Y5_R10_1471_RADIATIVE_READOUT_CLOSURE_ATTEMPT.csv",
    "1490_species": OUT / "P8_Y5_R10_1490_SPECIES_READOUT_DEPENDENCY_AUDIT.csv",
}

SOURCES = [
    ("SRC2353_00_2352_doc", "2352_doc", ["NEXT2352_0", "readout no-reentry/source-selector"], "2352 selected readout no-reentry/source-selector"),
    ("SRC2353_01_2352_validation", "2352_validation", ["VAL2352_OVERALL", "PASS"], "2352 validation"),
    ("SRC2353_02_2352_residuals", "2352_residuals", ["BRS2352_5_readout_reentry", "LIVE_SELECTED_NEXT"], "2352 residual status"),
    ("SRC2353_03_2352_selector", "2352_selector", ["SBS2352_3_readout", "LIVE_SELECTED_NEXT"], "2352 selector stack"),
    ("SRC2353_04_2352_next", "2352_next", ["NEXT2352_0", "2353-Y5-R2FR-readout-no-reentry-source-selector-zero-or-component-row.md"], "machine-readable 2353 target"),
    ("SRC2353_05_2346_components", "2346_components", ["NHC2346_3_readout", "MISSING_READOUT_REENTRY_ZERO_OR_LEAKAGE_VALUE"], "non-Hilbert readout component"),
    ("SRC2353_06_2335_certificate", "2335_certificate", ["SRNG2335_6_verdict", "PARTIAL_CERTIFICATE_READY_NOT_DERIVED"], "SRNG source/readout argument certificate"),
    ("SRC2353_07_2324_zero", "2324_zero", ["ARZ2324_4_verdict", "NOT_DERIVED_RETAIN_BOUND_ROW"], "alpha_readout zero attempt"),
    ("SRC2353_08_2324_bound", "2324_bound", ["ARB2324_1_readout_normal_form", "NORMAL_FORM_DERIVED_VALUES_MISSING"], "alpha_readout first bound row"),
    ("SRC2353_09_2203_fixed", "2203_fixed", ["FBR2203_7_verdict", "FIXED_BEFORE_READOUT_MAP_NOT_DERIVED"], "fixed-before-readout map attempt"),
    ("SRC2353_10_2203_alpha", "2203_alpha", ["ARW2203_0_alpha_readout", "READOUT_COMPONENT_RETAINED_NONCLAIM"], "alpha_readout row"),
    ("SRC2353_11_2202_readout", "2202_readout", ["RZT2202_4_verdict", "READOUT_ZERO_THEOREM_NOT_DERIVED"], "readout zero theorem attempt"),
    ("SRC2353_12_2177_gate", "2177_gate", ["ROG2177_7_gate_verdict", "PARTIAL_PASS_CONDITIONAL_NOT_CLAIMABLE"], "observable readout gate"),
    ("SRC2353_13_2177_residuals", "2177_residuals", ["RLR2177_5_total", "MISSING_COMPONENT_VALUES"], "readout lock residual rows"),
    ("SRC2353_14_2122_lemma", "2122_lemma", ["SRO2122_6_verdict", "CONDITIONAL_THEOREM_BLOCKED_BY_COMMUTATOR_AND_SOURCE_SUPPORT"], "source/readout owner lemma"),
    ("SRC2353_15_2118_zero", "2118_zero", ["SRZ2118_6_verdict", "ZERO_THEOREM_NOT_CLOSED"], "source/readout zero theorem attempt"),
    ("SRC2353_16_1898_commutator", "1898_commutator", ["RVC1898_5_verdict", "PURE_POSTPROCESSING_ZERO_ONLY_GENERAL_COMMUTATOR_NOT_DERIVED"], "readout variation commutator"),
    ("SRC2353_17_1888_stability", "1888_stability", ["ROS1888_6_verdict", "READOUT_STABILITY_NOT_PARENT_DERIVED"], "readout stability proof attempt"),
    ("SRC2353_18_1816_theorem", "1816_theorem", ["VBR1816_6_verdict", "CONDITIONAL_THEOREM_NOT_CURRENT_PROOF"], "variation-before-readout theorem"),
    ("SRC2353_19_1816_selector", "1816_selector", ["SSO1816_6_verdict", "FAIL_CURRENT_ZERO_PROOF"], "source-selector order audit"),
    ("SRC2353_20_1802_gate", "1802_gate", ["MRT1802_7_verdict", "JMatter_AND_READOUT_ZERO_NOT_SIGNED_COMPONENT_ROWS_REQUIRED"], "matter/readout theorem gate"),
    ("SRC2353_21_1802_type", "1802_type", ["RTS1802_0_pure_postprocessing", "CONDITIONAL_SAFE_DOMAIN_DEFINED"], "readout type split"),
    ("SRC2353_22_1701_no_reentry", "1701_no_reentry", ["NRE1701_5_verdict", "PURE_POSTPROCESSING_ONLY_GENERAL_BLOCKED"], "no-reentry theorem attempt"),
    ("SRC2353_23_1701_commutator", "1701_commutator", ["RC1701_6_verdict", "GENERAL_NO_REENTRY_NOT_DERIVED"], "readout commutator audit"),
    ("SRC2353_24_1701_queue", "1701_queue", ["RQ1701_0_C_R", "retained_nonclaim"], "readout residual queue"),
    ("SRC2353_25_1700_target", "1700_target", ["RNR1700_5_verdict", "READOUT_NO_REENTRY_SELECTED"], "older readout no-reentry target"),
    ("SRC2353_26_967_schema", "967_schema", ["RAV967_5_verdict", "CONDITIONAL_SCHEMA_THEOREM_WRITTEN_NOT_PARENT_SIGNED"], "readout schema theorem"),
    ("SRC2353_27_967_counter", "967_counter", ["RCM967_0_reduced_EFT", "legal_as_new_EFT"], "readout countermodel audit"),
    ("SRC2353_28_968_clause", "968_clause", ["REC968_5_verdict", "CERTIFICATE_READY_AS_CONTRACT_NOT_DERIVATION"], "readout exclusion clause"),
    ("SRC2353_29_969_certificate", "969_certificate", ["RDC969_5_verdict", "CERTIFIED_CLOSURE_NOT_DERIVATION"], "readout domain certificate"),
    ("SRC2353_30_1471_radiative", "1471_radiative", ["RRC1471_3_verdict", "REFUSE_PROMOTION_START_PREDICTION_FILL"], "radiative/readout closure attempt"),
    ("SRC2353_31_1490_species", "1490_species", ["SRD1490_4_verdict", "OPEN_DEPENDENCIES_RETAINED"], "species/readout dependency audit"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2353_SOURCE_REGISTER.csv",
    "audit": OUT / "P8_Y5_PARENT_QLOC_2353_READOUT_NO_REENTRY_ZERO_AUDIT.csv",
    "components": OUT / "P8_Y5_PARENT_QLOC_2353_READOUT_REENTRY_COMPONENT_ROWS.csv",
    "selector": OUT / "P8_Y5_PARENT_QLOC_2353_SOURCE_SELECTOR_GATE_STACK.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2353_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2353_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2353_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2353_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2353_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2353_VALIDATION.csv",
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
            "row_id": "RNE2353_0_target",
            "readout_piece": "readout no-reentry/source-selector zero",
            "statement": "C_R[A] := Pi_CoeffSource([delta_parent,R_A]T_H)+Pi_CoeffSource(delta_pre R_A)+Pi_CoeffSource(delta_cal R_A) must vanish or become a residual.",
            "status": "TARGET_SHARPENED",
            "proof_result": "turns readout/source-selector leakage into a named current component rather than a vague caveat",
            "remaining_gap": "general C_R[A]=0 not proven",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RNE2353_1_pure_postprocessing",
            "readout_piece": "pure data postprocessing",
            "statement": "If R_post: Sol(S_parent)/G -> Data_A is absent from S_parent, S_eff, Pi_M and source calibration, then it cannot alter delta S_parent/delta fields.",
            "status": "EXACT_CONDITIONAL_ZERO",
            "proof_result": "pure reporting maps are harmless by type/order",
            "remaining_gap": "corpus has not signed every physical readout as pure postprocessing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RNE2353_2_variation_before_readout",
            "readout_piece": "source variation before readout",
            "statement": "T_H := delta S_matter/delta e_obs is formed before material selector, orbit/readout kernel, calibration or source-worldtube projection.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_result": "post-variation c_A/F(T_A,A) cannot become a parent source if truly downstream",
            "remaining_gap": "parent domain, official readout model and source-worldtube kernels unsigned",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RNE2353_3_projector_worldtube",
            "readout_piece": "field-dependent projector/source-worldtube",
            "statement": "If Pi, support, boundary or source-worldtube depends on fields/domains/readout, delta(Pi J)=Pi delta J+(delta Pi)J can create source terms.",
            "status": "COUNTERMODEL_ACTIVE",
            "proof_result": "not covered by pure postprocessing theorem",
            "remaining_gap": "chain-map/source-worldtube descent or finite commutator row",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RNE2353_4_EFT_radiative",
            "readout_piece": "effective/radiative pre-variation readout",
            "statement": "If S_eff or cutoff/readout terms enter before variation, they define a retained EFT branch and may carry real source coefficients.",
            "status": "COUNTERMODEL_ACTIVE",
            "proof_result": "reduced action tax blocks theorem-zero credit",
            "remaining_gap": "radiative/readout closure as typed visible endofunctor unsigned",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RNE2353_5_calibration_material",
            "readout_piece": "calibration/material/clock response",
            "statement": "Calibration masks, material tensors, clock sensitivities, apparatus and source/profile choices must be fixed before variation or retained as arena product rows.",
            "status": "ARENA_PRODUCT_ROWS_REQUIRED",
            "proof_result": "prevents WEP/R10/clock/PPN transfer by vibes",
            "remaining_gap": "official kernels and response operators missing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RNE2353_6_SRNG_certificate",
            "readout_piece": "source-readout no-Gamma certificate",
            "statement": "SRNG gives a clean parent-action contract for Gamma-free source/readout sectors, but not a derivation from deeper quotient/naturality.",
            "status": "PARTIAL_CERTIFICATE_READY_NOT_DERIVED",
            "proof_result": "can be used as private branch discipline, not public local-GR proof",
            "remaining_gap": "parent adoption or quotient/naturality derivation",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RNE2353_7_verdict",
            "readout_piece": "general readout/source-selector no-reentry",
            "statement": "Current corpus proves pure postprocessing no-reentry conditionally, but does not prove C_R[A]=0 for all physical source/readout maps.",
            "status": "GENERAL_ZERO_NOT_DERIVED_COMPONENT_ROWS_REQUIRED",
            "proof_result": "safe readout class isolated; unsafe maps become explicit residual rows",
            "remaining_gap": "source-worldtube/projector chain-map is the next hard subgate",
            "valid_for_claim": "false",
        },
    ]


def component_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "RRC2353_0_total",
            "quantity": "epsilon_readout_reentry_abs",
            "component": "absolute readout/source-selector reentry envelope",
            "formula": "E_pure_fail + E_projector + E_EFT + E_calibration + E_material_clock + E_worldtube + E_hidden_marker + E_arena_transfer",
            "units": "dimensionless after source/current normalization",
            "current_value": "MISSING_COMPONENT_VALUES",
            "source_needed": "zero theorem for each unsafe map or source-backed component bounds",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RRC2353_1_projector_worldtube",
            "quantity": "E_projector_worldtube",
            "component": "field-dependent projector/source-worldtube/domain support",
            "formula": "||Pi_CoeffSource([delta_parent,Pi_W]J_H)|| / ||P_source[J_Hilbert]||",
            "units": "dimensionless_or_declared_flux_norm",
            "current_value": "MISSING_CHAINMAP_OR_COMMUTATOR_VALUE",
            "source_needed": "Pi_W descends through q/e_obs, or I_commutator/R_eq/source-worldtube bound rows",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RRC2353_2_EFT_radiative",
            "quantity": "E_EFT_readout",
            "component": "effective/radiative readout action feedback",
            "formula": "||Pi_CoeffSource(delta DeltaS_eff[R,cutoff,fields])|| / ||P_source[J_Hilbert]||",
            "units": "dimensionless",
            "current_value": "MISSING_EFT_DOMAIN_CLOSURE_OR_COEFFICIENTS",
            "source_needed": "typed visible endofunctor theorem or coefficient rows",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RRC2353_3_calibration_feedback",
            "quantity": "E_calibration_feedback",
            "component": "measured-GM/PPN/calibration mask chosen from data then used as source normalizer",
            "formula": "||Pi_CoeffSource(delta_cal R_A)|| / ||P_source[J_Hilbert]||",
            "units": "dimensionless",
            "current_value": "MISSING_FIXED_BEFORE_READOUT_FUNCTOR",
            "source_needed": "fixed-before-readout map or explicit calibration-feedback bound",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RRC2353_4_material_clock",
            "quantity": "E_material_clock",
            "component": "material, clock, rod, light and apparatus response",
            "formula": "||Pi_CoeffSource(delta R_material_clock)|| / ||P_source[J_Hilbert]||",
            "units": "dimensionless_or_response_units",
            "current_value": "MISSING_RESPONSE_OPERATORS",
            "source_needed": "metric-only clock/rod/light operators and apparatus classification",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RRC2353_5_source_worldtube",
            "quantity": "E_source_worldtube",
            "component": "source support/profile/composition selector",
            "formula": "||K_source[J_H]-J_H|| / ||P_source[J_Hilbert]||",
            "units": "dimensionless_or_GM_flux_norm",
            "current_value": "MISSING_SOURCE_KERNEL",
            "source_needed": "worldtube/support/profile q/e_obs descent or finite source-kernel value",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RRC2353_6_hidden_marker",
            "quantity": "E_hidden_marker",
            "component": "material marker/species/source label renamed as readout data",
            "formula": "||Pi_CoeffSource(marker_reentry)|| / ||P_source[J_Hilbert]||",
            "units": "dimensionless",
            "current_value": "MISSING_NO_MARKER_THEOREM_OR_BOUND",
            "source_needed": "no-natural-marker theorem or retained source/readout marker row",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RRC2353_7_arena_transfer",
            "quantity": "E_arena_transfer",
            "component": "cross-arena readout transfer",
            "formula": "||K_A_to_B residual|| in declared arena units",
            "units": "arena_specific",
            "current_value": "MISSING_BRANCH_READOUT_FUNCTOR",
            "source_needed": "arena-specific product maps for WEP/R10/PPN/clock/orbit/EM",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def selector_rows() -> list[dict[str, Any]]:
    selector_specs = [
        ("SSG2353_0_parent_domain", "parent action domain excludes readout maps", "Conf_parent excludes P_read,R_read,fitted masks and readout-selected active blocks", "CERTIFICATE_READY_NOT_PRIMITIVE_DERIVATION", "E_pure_fail"),
        ("SSG2353_1_solution_map", "pure solution-to-data map", "R_read: Sol(S_parent)/G -> Obs with no arrow into S_parent or S_eff", "EXACT_CONDITIONAL_SAFE_CLASS", "none if globally signed"),
        ("SSG2353_2_variation_order", "variation before readout", "delta S_parent and T_H are formed before material/source/readout projection", "EXACT_CONDITIONAL_THEOREM", "post-current transfer row if unsigned"),
        ("SSG2353_3_source_worldtube", "source worldtube selector", "W_source and K_source are fixed downstream maps of J_H/e_obs/q, not source-normalizers fitted after data", "MISSING_ARENA_TRANSFER_KERNEL", "E_source_worldtube"),
        ("SSG2353_4_projector_chainmap", "projector/domain chain map", "delta Pi=0 and [d,Pi]J_H=0 for source/readout projector", "MISSING_CHAINMAP_THEOREM", "E_projector_worldtube"),
        ("SSG2353_5_no_EFT_reentry", "no pre-variation EFT/readout feedback", "readout-reduced action is retained as new EFT, not theorem-zero", "GUARDRAIL_READY_NOT_ZERO", "E_EFT_readout"),
        ("SSG2353_6_no_marker_relabel", "no marker/species/source label reentry", "readout labels cannot be hidden material/source markers inside parent action", "NO_MARKER_THEOREM_MISSING", "E_hidden_marker"),
        ("SSG2353_7_verdict", "source-selector gate stack", "all gates must close before C_R[A]=0 can be claimed", "GATE_STACK_NOT_CLOSED", "epsilon_readout_reentry_abs"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "gate": gate,
            "condition": condition,
            "status": status,
            "residual_if_missing": residual,
            "valid_for_claim": "false",
        }
        for row_id, gate, condition, status, residual in selector_specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2353_0_result",
            "decision": "do not claim general readout/source-selector no-reentry",
            "reason": "pure postprocessing is conditionally safe, but real source/projector/EFT/calibration/material maps are not all pure postprocessing",
            "effect": "local GR/Newton measured-GM bridge remains blocked by epsilon_readout_reentry_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2353_1_partial_win",
            "decision": "preserve pure-postprocessing zero as a conditional theorem",
            "reason": "readout maps that are genuinely solution-to-data and absent from the action cannot alter parent source variation",
            "effect": "safe readout class is separated from unsafe source-selector maps",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2353_2_component_pack",
            "decision": "install readout reentry component rows",
            "reason": "unsafe maps must be theorem-zeroed or bounded individually",
            "effect": "no cancellation, no hiding inside fitted GM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2353_3_next",
            "decision": "select source-worldtube/projector chain-map zero next",
            "reason": "projector/worldtube maps are the core source-selector route by which readout can become physical source coupling",
            "effect": "2354 targets delta Pi=0/[d,Pi]J_H=0 or keeps component bounds",
            "valid_for_claim": "false",
        },
    ]


def claim_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2353_0_pure_postprocessing", "pure postprocessing no-reentry", "true", "conditional theorem only"),
        ("CG2353_1_parent_domain", "parent domain excludes readout variables globally", "false", "certificate/adoption exists but primitive derivation unsigned"),
        ("CG2353_2_variation_order", "variation-before-readout globally signed", "false", "conditional theorem not current proof"),
        ("CG2353_3_projector_worldtube", "source-worldtube/projector chain-map zero", "false", "delta Pi/I_commutator/source kernel open"),
        ("CG2353_4_EFT_radiative", "radiative/readout closure preserves visible grammar", "false", "typed endofunctor theorem unsigned"),
        ("CG2353_5_material_clock", "material/clock/light response metric-only", "false", "response operators missing"),
        ("CG2353_6_hidden_marker", "no marker/species label reentry", "false", "no-natural-marker theorem missing"),
        ("CG2353_7_general_no_reentry", "C_R[A]=0 for all local readout maps", "false", "only pure postprocessing class closes"),
        ("CG2353_8_local_GR_Newton", "local GR/Newton source readout recovered", "false", "readout/source-selector bridge remains nonclaim"),
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
    refusal_specs = [
        ("REF2353_0_all_readout_safe", "treat every readout map as pure postprocessing", "false", "projector/worldtube/EFT/calibration/material maps can re-enter before or during variation", "RNE2353_3_projector_worldtube;RNE2353_4_EFT_radiative"),
        ("REF2353_1_postprocessing_to_claim", "pure-postprocessing theorem proves local GR/Newton", "false", "it only closes one strictly typed class, not source-measure equality or Poisson/Gauss", "CG2353_0_pure_postprocessing;CG2353_8_local_GR_Newton"),
        ("REF2353_2_reduced_action_zero", "vary a readout-reduced action and count it as parent-zero", "false", "that is a new EFT branch and must pay residual tax", "RAV967_3_reduced_action_tax;RNE2353_4_EFT_radiative"),
        ("REF2353_3_GM_calibration_hide", "hide readout reentry in measured GM calibration", "false", "fixed-before-readout map is not derived and relative/protocol components are observable", "FBR2203_7_verdict;RRC2353_3_calibration_feedback"),
        ("REF2353_4_arena_transfer", "use one arena readout bound as another arena pass", "false", "arena-specific no-transfer rule requires signed branch functor or finite product rows", "NRE1701_4_arena_transfer;RRC2353_7_arena_transfer"),
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
        for row_id, shortcut, allowed, reason, sources in refusal_specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2353_0",
            "next_target": "2354-Y5-R2FR-source-worldtube-projector-chainmap-zero-or-readout-reentry-bound-pack.md",
            "why": "the unsafe readout route is now localized to source-worldtube/projector chain-map terms: prove delta Pi=0 and [d,Pi]J_H=0 or keep the bound pack",
            "route_type": "private_derivation_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2353_1",
            "next_target": "2354b-Y5-R2FR-parent-readout-domain-closure-adoption-decision.md",
            "why": "parallel closure route: decide whether the readout-domain certificate becomes an explicit private parent-domain axiom",
            "route_type": "closure_or_adoption_decision",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2353_2",
            "next_target": "2354c-Y5-R2FR-readout-reentry-component-acquisition-pack.md",
            "why": "fallback route: source E_projector, E_EFT, E_calibration, E_material_clock, E_worldtube and E_hidden_marker rows",
            "route_type": "fallback_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("COPY2353_0_audit", OUTPUTS["audit"], BETA_DOCS / "READOUT_NO_REENTRY_ZERO_AUDIT_2353_NONCLAIM.csv", "beta-source readout theorem audit"),
        ("COPY2353_1_components", OUTPUTS["components"], MICRO_RESIDUALS / "READOUT_REENTRY_COMPONENT_ROWS_2353_NONCLAIM.csv", "local residual component inputs"),
        ("COPY2353_2_decision", OUTPUTS["decision"], RAB_QUEUE / "JR2353_READOUT_NO_REENTRY_DECISION_LEDGER_NONCLAIM.csv", "RAB derivation/acquisition decision"),
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
    for path in FORMALIZATION.rglob("*2353*"):
        if not path.is_file():
            continue
        parts = {part.lower() for part in path.parts}
        if ".venv" in parts or "site-packages" in parts or "__pycache__" in parts:
            continue
        if path.name.startswith(("2353-", "P8_Y5_PARENT_QLOC_2353", "P8_Y5_BRR545_2353")):
            hits.append(path)
    return hits


def validation_rows(sources: list[dict[str, Any]], copies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    produced = [path for key, path in OUTPUTS.items() if key != "validation"]
    audit_text = read_text(OUTPUTS["audit"])
    component_rows_data = read_csv(OUTPUTS["components"])
    claims = read_csv(OUTPUTS["claims"])
    next_text = read_text(OUTPUTS["next"])
    output_text = "".join(read_text(path) for path in produced)
    checks = [
        ("VAL2353_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "every required source path exists"),
        ("VAL2353_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all required source needles were found"),
        ("VAL2353_02_outputs_exist", all(path.exists() and path.stat().st_size > 0 for path in produced), "all 2353 outputs written"),
        ("VAL2353_03_pure_postprocessing_preserved", "RNE2353_1_pure_postprocessing" in audit_text, "pure postprocessing conditional zero preserved"),
        ("VAL2353_04_general_zero_rejected", "RNE2353_7_verdict" in audit_text and "GENERAL_ZERO_NOT_DERIVED" in audit_text, "general no-reentry theorem rejected"),
        ("VAL2353_05_component_rows_nonclaim", component_rows_data and all(row.get("score_ready") == "false" and row.get("valid_for_claim") == "false" for row in component_rows_data), "readout reentry component rows remain non-score-ready"),
        ("VAL2353_06_claim_gates_blocked", claims and all(row.get("passes_public_claim") == "false" and row.get("valid_for_claim") == "false" for row in claims), "all public claim gates blocked"),
        ("VAL2353_07_next_selected", "2354-Y5-R2FR-source-worldtube-projector-chainmap-zero-or-readout-reentry-bound-pack.md" in next_text, "2354 source-worldtube/projector chain-map target selected"),
        ("VAL2353_08_branch_copies_parse", copies and all(row["copy_exists"] == "true" for row in copies), "branch copies exist"),
        ("VAL2353_09_formalization_untouched", not formalization_hits(), "no 2353 checkpoint output appears in formalization-workbench"),
        ("VAL2353_10_no_claim_flags", "valid_for_claim,true" not in output_text and "passes_public_claim,true" not in output_text and "score_ready,true" not in output_text, "no generated row has claim/score-ready true flags"),
        ("VAL2353_11_no_github_policy", True, "public GitHub update not recommended from 2353"),
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
            "row_id": "VAL2353_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2353 preserves pure-postprocessing zero, rejects general readout/source-selector zero, installs readout reentry component rows, and selects source-worldtube/projector chain-map as 2354.",
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
    components: list[dict[str, Any]],
    selector: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    now = datetime.now(timezone.utc).isoformat()
    content = f"""# 2353 — Y5 R2FR Readout No-Reentry Source-Selector Zero Or Component Row

Generated: `{now}`

## Summary

2353 attacks the source-measure throat selected by 2352: whether readout/source-worldtube maps can recreate
source/species labels after parent variation.

Result: **pure postprocessing is conditionally safe**, but **general readout/source-selector zero is not derived**.
If a readout map is only `R_post: Sol(S_parent)/G -> Data`, absent from `S_parent`, absent from `S_eff`, and has no
source-coefficient codomain, it cannot alter the parent source variation. But projector/domain/source-worldtube maps,
EFT/radiative maps, calibration feedback, material/clock response, hidden marker reentry and arena-transfer maps are
not proven pure. They stay as explicit component rows.

So the next hard target is the source-worldtube/projector chain-map:
`delta Pi_W = 0` and `[d,Pi_W]J_H = 0`, or a retained readout-reentry bound pack.

## Output Files

- `{OUTPUTS["sources"]}`
- `{OUTPUTS["audit"]}`
- `{OUTPUTS["components"]}`
- `{OUTPUTS["selector"]}`
- `{OUTPUTS["decision"]}`
- `{OUTPUTS["claims"]}`
- `{OUTPUTS["refusal"]}`
- `{OUTPUTS["next"]}`
- `{OUTPUTS["copies"]}`
- `{OUTPUTS["validation"]}`

## Source Register

{table(sources, ["row_id", "source_key", "exists", "needles_found", "source_role"])}

## Readout No-Reentry Zero Audit

{table(audit, ["row_id", "readout_piece", "status", "proof_result", "remaining_gap", "valid_for_claim"])}

## Readout Reentry Component Rows

{table(components, ["row_id", "quantity", "component", "current_value", "source_needed", "score_ready", "valid_for_claim"])}

## Source Selector Gate Stack

{table(selector, ["row_id", "gate", "condition", "status", "residual_if_missing", "valid_for_claim"])}

## Decision Ledger

{table(decision, ["row_id", "decision", "reason", "effect", "valid_for_claim"])}

## Claim Gates

{table(claims, ["row_id", "gate", "passes_private_or_partial", "passes_public_claim", "why", "valid_for_claim"])}

## Refusal Runner

{table(refusal, ["row_id", "shortcut", "allowed", "reason", "source_rows", "valid_for_claim"])}

## Next Targets

{table(next_targets, ["row_id", "next_target", "why", "route_type", "valid_for_claim"])}

## Validation

{table(validation, ["row_id", "status", "detail", "valid_for_claim"])}

## Working Read

This is a useful reduction. We are not saying “readout is bad” or “readout is solved”. We now have a typed split:

1. pure solution-to-data readout is harmless by conditional theorem;
2. source/projector/worldtube/readout kernels are not harmless unless they descend through the parent quotient/coframe;
3. if they do not descend, they become explicit residuals rather than hidden calibration.

That is exactly the kind of discipline needed before local GR/Newton can be claimed.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    audit = audit_rows()
    components = component_rows()
    selector = selector_rows()
    decision = decision_rows()
    claims = claim_rows()
    refusal = refusal_rows()
    next_targets = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["components"], components)
    write_csv(OUTPUTS["selector"], selector)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["next"], next_targets)
    copies = copy_rows()
    write_csv(OUTPUTS["copies"], copies)
    validation = validation_rows(sources, copies)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, audit, components, selector, decision, claims, refusal, next_targets, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        failed_ids = ", ".join(row["row_id"] for row in failed)
        raise SystemExit(f"2353 validation failed: {failed_ids}")
    print(f"2353 checkpoint written: {DOC}")


if __name__ == "__main__":
    main()
