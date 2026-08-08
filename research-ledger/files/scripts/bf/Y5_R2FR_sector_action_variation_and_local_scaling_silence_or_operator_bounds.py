from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1771"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1771_0_1770_handoff",
        "source_key": "1770_sector_variation_next",
        "source_path": ROOT / "1770-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack.md",
        "needles": ["SECTOR_ACTION_VARIATION_AND_LOCAL_SCALING_SILENCE_IS_NEXT", "NEXT1770_0_primary"],
    },
    {
        "source_id": "SRC1771_1_1770_validation",
        "source_key": "1770_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1770_VALIDATION.csv",
        "needles": ["VAL1770_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1771_2_1770_residual_silence",
        "source_key": "1770_residual_silence",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_RESIDUAL_SECTOR_SILENCE_AUDIT.csv",
        "needles": ["RSS1770_1_projector", "RSS1770_6_verdict"],
    },
    {
        "source_id": "SRC1771_3_1770_coefficients",
        "source_key": "1770_operator_coefficients",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_OPERATOR_COEFFICIENT_PACK.csv",
        "needles": ["OPC1770_0_total_DeltaE", "OPC1770_6_source_normalization"],
    },
    {
        "source_id": "SRC1771_4_1009_current_chain",
        "source_key": "1009_sector_variation_contract",
        "source_path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "needles": ["PCS1009_9_total_parent_contract", "REFUSED_INCOMPLETE_PARENT_CURRENT_CHAIN_CONTRACT"],
    },
    {
        "source_id": "SRC1771_5_1013_pim_flux",
        "source_key": "1013_pim_flux_obstruction",
        "source_path": ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
        "needles": ["PFC1013_2_product_rule", "OBS1013_1_PiM_commutator"],
    },
    {
        "source_id": "SRC1771_6_1013_projector_stress",
        "source_key": "1013_projector_stress",
        "source_path": ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
        "needles": ["OBS1013_5_projector_stress", "DEC1013_2_next_commutator"],
    },
    {
        "source_id": "SRC1771_7_1012_newton",
        "source_key": "1012_source_normalization_block",
        "source_path": ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
        "needles": ["Y5O1012_7_Newton_Poisson_orbit", "DEC1012_2_next_root"],
    },
    {
        "source_id": "SRC1771_8_1768_normal_form",
        "source_key": "1768_normal_form",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_PARENT_ACTION_NORMAL_FORM_SIGNATURE.csv",
        "needles": ["ANF1768_3_nonminimal_term_owner", "ANF1768_6_current_verdict"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1771_SOURCE_REGISTER.csv",
    "variation_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1771_SECTOR_ACTION_VARIATION_LEDGER.csv",
    "scaling_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1771_LOCAL_SCALING_LEDGER.csv",
    "silence_decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1771_SILENCE_DECISION_LEDGER.csv",
    "operator_bounds": RESIDUALS / "P8_Y5_PARENT_QLOC_1771_OPERATOR_BOUND_INPUT_PACK.csv",
    "priority": RESIDUALS / "P8_Y5_PARENT_QLOC_1771_SECTOR_PRIORITY_LEDGER.csv",
    "countermodel": RESIDUALS / "P8_Y5_PARENT_QLOC_1771_COUNTERMODEL_LEDGER.csv",
    "bridge_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1771_GR_BRIDGE_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1771_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1771_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1771_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1771_VALIDATION.csv",
}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": all(needle in text for needle in needles),
                "needles": ";".join(needles),
                "role": "sector action variation and local scaling silence or operator bounds",
                "valid_for_claim": False,
            }
        )
    return rows


def variation_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "sector_id": "SAV1771_0_higher_derivative",
            "sector": "higher-curvature / higher-derivative",
            "candidate_action_block": "S_HD = int sqrt(-g) (c_R2 R^2 + c_Ricci2 R_munu R^munu + c_boxR R box R + ...)",
            "variation_target": "E_HD_munu",
            "variation_status": "FORM_KNOWN_TEMPLATE_NOT_PARENT_ADOPTED",
            "local_silence_test": "absent by normal form or suppressed by c_i/L_local^2",
            "verdict": "RETAIN_BOUND_INPUT",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "SAV1771_1_projector",
            "sector": "Pi_M/domain/projector source-measure",
            "candidate_action_block": "S_PiM or parent symplectic projector origin",
            "variation_target": "delta(Pi_M J_H)=Pi_M delta J_H + (delta Pi_M)J_H and [d,Pi_M]J_H",
            "variation_status": "EXACT_OBSTRUCTION_WRITTEN_NOT_SILENCED",
            "local_silence_test": "Pi_M fixed/identity and [d,Pi_M]J_H=0 in compact exterior",
            "verdict": "HARDEST_CONCRETE_NEXT_SECTOR",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "SAV1771_2_boundary",
            "sector": "boundary/reference/improvement",
            "candidate_action_block": "S_GHY + B_ref + exact/topological improvements",
            "variation_target": "theta_boundary, Q_boundary, DeltaE_boundary",
            "variation_status": "REFERENCE_SHAPE_KNOWN_FIXED_BEFORE_READOUT_UNSIGNED",
            "local_silence_test": "fixed before readout + falloff/local boundary no-flux",
            "verdict": "RETAIN_BOUND_INPUT",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "SAV1771_3_nonminimal",
            "sector": "nonminimal matter-geometry/MTS coupling",
            "candidate_action_block": "S_nonmin = int sqrt(-g) c_nonminimal f(X,Phi,labels)L_m or A(X)J_m",
            "variation_target": "E_nonmin_munu plus modified matter equations/source charge",
            "variation_status": "MUST_CLASSIFY_NOT_FORBIDDEN",
            "local_silence_test": "forbid by normal form or bound composition/time/PPN projections",
            "verdict": "RETAIN_BOUND_INPUT",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "SAV1771_4_memory_coframe",
            "sector": "memory/coframe/preferred-frame",
            "candidate_action_block": "S_memory/coframe with local frame-lock residual",
            "variation_target": "E_memory_munu + E_coframe_munu and PPN alpha_i",
            "variation_status": "LOCAL_FRAME_LOCK_UNSIGNED",
            "local_silence_test": "local vacuum/coframe lock kills preferred-frame stress",
            "verdict": "RETAIN_BOUND_INPUT",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "SAV1771_5_source_normalization",
            "sector": "worldtube/source normalization",
            "candidate_action_block": "Pi_M J_H flux/worldtube source-measure bridge",
            "variation_target": "d(Pi_M J_H), M_source[W], exterior Gauss flux",
            "variation_status": "EXACT_FLUX_OBSTRUCTION_WRITTEN_NOT_CLOSED",
            "local_silence_test": "d(Pi_M J_H)=0 and worldtube/exterior equality before orbital fitting",
            "verdict": "PARALLEL_ROOT_BLOCKER",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "SAV1771_6_verdict",
            "sector": "sector action variation for current MTS",
            "candidate_action_block": "all non-EH retained sectors",
            "variation_target": "all DeltaE_i",
            "variation_status": "NO_SECTOR_FULLY_SILENCED",
            "local_silence_test": "not achieved",
            "verdict": "EH_DOMINANCE_NOT_PROVED",
            "valid_for_claim": False,
        },
    ]


def scaling_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "scale_id": "SCL1771_0_higher_derivative",
            "sector": "higher-derivative",
            "dimensionless_ratio": "epsilon_HD ~ c_HD / L_local^2 for curvature-squared terms",
            "local_silence_condition": "c_HD/L_local^2 << tolerance",
            "status": "MISSING_COEFFICIENT_SCALE_AND_TOLERANCE",
            "bound_row": "OBI1771_1_higher_derivative",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "scale_id": "SCL1771_1_projector",
            "sector": "projector/Pi_M",
            "dimensionless_ratio": "epsilon_PiM ~ M_eff^-1 int_A ([d,Pi_M]J_H - Pi_M dJ_extra)",
            "local_silence_condition": "commutator and projected extra flux vanish in compact exterior",
            "status": "MISSING_I_COMMUTATOR_AND_PROJECTOR_STRESS",
            "bound_row": "OBI1771_2_projector",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "scale_id": "SCL1771_2_boundary",
            "sector": "boundary/reference",
            "dimensionless_ratio": "epsilon_boundary ~ Q_boundary_residual / Q_EH",
            "local_silence_condition": "fixed boundary/reference and no material boundary flux",
            "status": "MISSING_FIXED_REFERENCE_AND_BOUNDARY_FLUX",
            "bound_row": "OBI1771_3_boundary",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "scale_id": "SCL1771_3_nonminimal",
            "sector": "nonminimal matter-geometry",
            "dimensionless_ratio": "epsilon_nonmin ~ c_nonminimal f(X,Phi) or induced composition charge",
            "local_silence_condition": "term absent/forbidden or coefficient below WEP/clock/PPN/R10 bounds",
            "status": "MISSING_OPERATOR_BASIS_AND_COMPOSITION_PROJECTION",
            "bound_row": "OBI1771_4_nonminimal",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "scale_id": "SCL1771_4_memory_coframe",
            "sector": "memory/coframe",
            "dimensionless_ratio": "epsilon_frame ~ preferred-frame/coframe residual amplitude",
            "local_silence_condition": "local frame-lock sets PPN alpha_i and clock drift residuals to zero",
            "status": "MISSING_LOCAL_FRAME_LOCK_OR_PPN_BOUND",
            "bound_row": "OBI1771_5_memory_coframe",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "scale_id": "SCL1771_5_source_normalization",
            "sector": "source normalization",
            "dimensionless_ratio": "epsilon_GM ~ (mu_obs - G_ref M_H_ref)/mu_obs",
            "local_silence_condition": "Poisson/Gauss/worldtube bridge owns measured GM before orbit fitting",
            "status": "MISSING_WORLDTUBE_EXTERIOR_CLOSURE",
            "bound_row": "OBI1771_6_source_normalization",
            "valid_for_claim": False,
        },
    ]


def silence_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "SD1771_0_higher_derivative",
            "sector": "higher-derivative",
            "zero_status": "not_zeroed",
            "bound_status": "bound_needed",
            "reason": "no parent normal-form absence theorem or coefficient scale",
            "next_action": "keep as operator coefficient row unless parent action forbids it",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "SD1771_1_projector",
            "sector": "projector/Pi_M",
            "zero_status": "not_zeroed",
            "bound_status": "highest_priority_bound_or_proof",
            "reason": "exact product-rule obstruction exists and blocks both EH dominance and measured GM",
            "next_action": "attack [d,Pi_M]J_H and projector stress directly",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "SD1771_2_boundary",
            "sector": "boundary/reference",
            "zero_status": "not_zeroed",
            "bound_status": "bound_needed",
            "reason": "fixed-before-readout and boundary no-flux are unsigned",
            "next_action": "require boundary condition/reference certificate",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "SD1771_3_nonminimal",
            "sector": "nonminimal matter-geometry",
            "zero_status": "not_zeroed",
            "bound_status": "bound_needed",
            "reason": "normal form has not forbidden direct matter-MTS couplings",
            "next_action": "forbid by object language or map to WEP/clock/PPN/R10 bounds",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "SD1771_4_memory_coframe",
            "sector": "memory/coframe",
            "zero_status": "not_zeroed",
            "bound_status": "bound_needed",
            "reason": "local frame-lock/preferred-frame silence remains unsigned",
            "next_action": "map to PPN alpha_i / clock residuals if theorem fails",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "SD1771_5_source_normalization",
            "sector": "source normalization",
            "zero_status": "not_zeroed",
            "bound_status": "parallel_root_blocker",
            "reason": "Poisson/Gauss/worldtube closure remains required before Newton/orbital claims",
            "next_action": "keep parallel with projector/Pi_M branch",
            "valid_for_claim": False,
        },
    ]


def operator_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "OBI1771_0_total_DeltaE",
            "quantity": "DeltaE_munu",
            "required_inputs": "sector basis, coefficient units, local scaling, no-cancellation guard, empirical map",
            "status": "MISSING_SECTOR_BOUNDS",
            "priority": "global",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OBI1771_1_higher_derivative",
            "quantity": "c_HD",
            "required_inputs": "operator basis, length units, local curvature scale, R10/PPN/cosmology map",
            "status": "MISSING_OPERATOR_BASIS_UNITS_BOUNDS",
            "priority": "medium",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OBI1771_2_projector",
            "quantity": "I_commutator,T_PiM,c_projector",
            "required_inputs": "Pi_M origin, [d,Pi_M]J_H integral, projector stress, source path, units",
            "status": "MISSING_PIM_COMMUTATOR_PROJECTOR_STRESS",
            "priority": "highest",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OBI1771_3_boundary",
            "quantity": "B_zero_flux,c_boundary",
            "required_inputs": "boundary/falloff condition, fixed reference, no fitted counterterm, flux integral",
            "status": "MISSING_BOUNDARY_REFERENCE_CERTIFICATE",
            "priority": "high",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OBI1771_4_nonminimal",
            "quantity": "c_nonminimal",
            "required_inputs": "operator basis, normal-form forbid theorem or WEP/clock/PPN/R10 projection",
            "status": "MISSING_NONMINIMAL_OPERATOR_MAP",
            "priority": "high",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OBI1771_5_memory_coframe",
            "quantity": "c_memory,c_frame",
            "required_inputs": "local frame-lock theorem or PPN alpha_i/clock projection",
            "status": "MISSING_FRAME_LOCK_OR_BOUND",
            "priority": "medium",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OBI1771_6_source_normalization",
            "quantity": "epsilon_GM",
            "required_inputs": "worldtube/Gauss/exterior closure and no orbital-GM laundering",
            "status": "MISSING_SOURCE_NORMALIZATION_BRIDGE",
            "priority": "highest_parallel",
            "valid_for_claim": False,
        },
    ]


def priority_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "rank": 1,
            "sector": "projector/Pi_M commutator",
            "why": "it is an exact product-rule obstruction already written and contaminates both DeltaE and measured GM",
            "next_action": "derive [d,Pi_M]J_H=0 plus projector-stress silence, or fill I_commutator/T_PiM bounds",
            "selection_status": "primary_next",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "rank": 2,
            "sector": "source normalization/worldtube",
            "why": "even EH dominance cannot yield Newton/orbits until parent charge equals measured source before fitting",
            "next_action": "keep as parallel blocker; Gauss/worldtube closure after Pi_M commutator",
            "selection_status": "parallel_root",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "rank": 3,
            "sector": "boundary/reference",
            "why": "boundary counterterms can fake charge closure if not fixed before readout",
            "next_action": "fixed-reference and no-flux certificate",
            "selection_status": "queued",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "rank": 4,
            "sector": "nonminimal matter-geometry",
            "why": "direct matter-MTS terms are dangerous for WEP/clocks but less concrete than Pi_M obstruction",
            "next_action": "forbid by normal form or bound",
            "selection_status": "queued",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "rank": 5,
            "sector": "higher-derivative and memory/coframe",
            "why": "important for PPN/R10/cosmology, but currently need operator bases before derivation can sharpen",
            "next_action": "operator basis and empirical map",
            "selection_status": "queued",
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1771_0_projector_leak",
            "countermodel": "Pi_M is fixed algebraically but has nonzero commutator/stress",
            "mathematical_form": "d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H with [d,Pi_M]J_H != 0",
            "survives_current_constraints": True,
            "why_survives": "1013 writes the obstruction and no zero theorem exists",
            "what_kills_it": "derive Pi_M origin plus commutator/projector-stress silence or bound it",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1771_1_scaling_smallness_without_units",
            "countermodel": "a residual is declared locally small without coefficient units or scale hierarchy",
            "mathematical_form": "epsilon_i E_i << G_munu asserted without c_i,L_local,tolerance",
            "survives_current_constraints": True,
            "why_survives": "1770/1771 have no source-backed coefficients or tolerance map",
            "what_kills_it": "operator units, local scale, absolute-sum/no-cancellation guard, and empirical bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1771_2_worldtube_gap",
            "countermodel": "EH-like LHS and clean Hilbert source still use the wrong measured mass",
            "mathematical_form": "M_source[W] != exterior charge or mu_obs until Pi_M/worldtube closure",
            "survives_current_constraints": True,
            "why_survives": "source normalization remains a parallel root blocker",
            "what_kills_it": "Poisson/Gauss/worldtube bridge before orbital fitting",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1771_3_verdict",
            "countermodel": "sector silence remains unproved",
            "mathematical_form": "at least one DeltaE_i or source-normalization obstruction survives",
            "survives_current_constraints": True,
            "why_survives": "no sector has a full variation + local scaling + empirical bound certificate",
            "what_kills_it": "1772 projector/Pi_M proof or bound, then parallel source-normalization closure",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def bridge_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1771_0_sector_variation",
            "bridge_piece": "sector-by-sector action variation",
            "current_status": "INCOMPLETE_NONCLAIM",
            "evidence": "SAV1771 rows",
            "remaining_gap": "no sector has complete action, variation, theta/Q, stress, boundary, and scaling certificate",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1771_1_EH_dominance",
            "bridge_piece": "EH dominance",
            "current_status": "NOT_PROVED",
            "evidence": "no sector fully silenced",
            "remaining_gap": "projector/source-normalization and other residuals retained",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1771_2_Newton",
            "bridge_piece": "Newton/Poisson/source normalization",
            "current_status": "BLOCKED_PARALLEL",
            "evidence": "SAV1771_5 and OBI1771_6",
            "remaining_gap": "worldtube/exterior/Gauss closure without orbital GM backfill",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1771_3_next",
            "bridge_piece": "next derivation owner",
            "current_status": "PROJECTOR_PIM_COMMUTATOR_IS_NEXT",
            "evidence": "priority rank 1",
            "remaining_gap": "derive or bound [d,Pi_M]J_H and projector stress",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1771_0_sector_result",
            "decision": "NO_NON_EH_SECTOR_FULLY_SILENCED",
            "reason": "each sector is missing action ownership, variation, local scaling, or source-backed bounds",
            "next_action": "retain operator coefficient pack",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1771_1_priority",
            "decision": "PROJECTOR_PIM_COMMUTATOR_IS_SHARPEST_NEXT_TARGET",
            "reason": "it is concrete, algebraic, already sourced, and blocks both EH dominance and Newton/source normalization",
            "next_action": "derive [d,Pi_M]J_H=0 or fill I_commutator/T_PiM bound rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1771_2_no_claim",
            "decision": "LOCAL_GR_NEWTON_NOT_CLAIMED",
            "reason": "EH dominance and source-normalization gates remain blocked",
            "next_action": "keep all local/empirical gates false",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1771_3_best_next",
            "decision": "PIM_COMMUTATOR_PROJECTOR_VARIATION_ZERO_OR_BOUND_IS_NEXT",
            "reason": "this is the smallest live obstruction with exact equations and immediate GR/Newton relevance",
            "next_action": "build 1772 Pi_M commutator/projector variation zero or coefficient-bound checkpoint",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1771_0_sector_silence",
            "claim": "all non-EH sectors are locally silent/suppressed",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_NO_SECTOR_HAS_FULL_VARIATION_SCALING_CERTIFICATE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1771_1_EH_dominance",
            "claim": "EH dominance follows",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PROJECTOR_BOUNDARY_NONMINIMAL_FRAME_SOURCE_RESIDUALS",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1771_2_projector",
            "claim": "Pi_M commutator/projector stress is zero",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_I_COMMUTATOR_TPIM_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1771_3_source_normalization",
            "claim": "Poisson/Gauss/worldtube source normalization closes",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_WORLDTUBE_EXTERIOR_CLOSURE_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1771_4_local_GR_Newton",
            "claim": "local GR/Newton recovery is derived",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_EH_DOMINANCE_AND_SOURCE_NORMALIZATION_OPEN",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1771_0_primary",
            "next_target": "1772-Y5-R2FR-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
            "script": "scripts/Y5_R2FR_PiM_commutator_projector_variation_zero_or_coefficient_bound.py",
            "objective": "derive [d,Pi_M]J_H=0 and projector-stress silence from a fixed parent charge map, or fill I_commutator/T_PiM coefficient-bound rows",
            "selection_status": "selected",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1771_1_parallel",
            "next_target": "1772b-Y5-R2FR-Poisson-Gauss-worldtube-source-normalization-pack.md",
            "script": "scripts/Y5_R2FR_Poisson_Gauss_worldtube_source_normalization_pack.py",
            "objective": "derive parent source charge to exterior Gauss flux and measured GM without orbital backfill",
            "selection_status": "parallel_held",
            "valid_for_claim": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "variation_ledger": variation_ledger_rows(),
        "scaling_ledger": scaling_ledger_rows(),
        "silence_decision": silence_decision_rows(),
        "operator_bounds": operator_bound_rows(),
        "priority": priority_rows(),
        "countermodel": countermodel_rows(),
        "bridge_status": bridge_status_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv_ok(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1771_SOURCE_REGISTER.csv")
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        shutil.copy2(path, MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(path, QUARANTINE / filename)
        shutil.copy2(path, RAB_QUEUE / f"JR1771_{key.upper()}.csv")


def claim_like_field(key: str) -> bool:
    return key.lower() in {
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "prediction_allowed",
        "score_allowed",
        "claim_pass",
        "selected",
    }


def boolish_claim_true(key: str, value: Any) -> bool:
    if key.lower() == "selected":
        return False
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if claim_like_field(key) and boolish_claim_true(key, value):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    status_keys = {"current_status", "status", "variation_status", "verdict", "zero_status", "bound_status"}
    for rows in rows_map.values():
        for row in rows:
            combined_status = " ".join(str(row.get(key, "")) for key in status_keys)
            if "MISSING_" in combined_status:
                for key, value in row.items():
                    if claim_like_field(key) and boolish_claim_true(key, value):
                        return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1771_SOURCE_REGISTER.csv").exists():
        return False
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1771_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched_for_1771() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1771*"))


def csv_parse_all() -> bool:
    return all(parse_csv_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def variation_attempt_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["sector_id"] == "SAV1771_6_verdict"
        and row["variation_status"] == "NO_SECTOR_FULLY_SILENCED"
        for row in rows_map["variation_ledger"]
    )


def projector_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["rank"] == 1
        and row["sector"] == "projector/Pi_M commutator"
        and row["selection_status"] == "primary_next"
        for row in rows_map["priority"]
    )


def operator_bounds_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["operator_bounds"]
    return any(row["row_id"] == "OBI1771_2_projector" for row in rows) and all(
        row["valid_for_claim"] is False for row in rows
    )


def countermodel_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["countermodel_id"] == "CM1771_3_verdict"
        and row["survives_current_constraints"] is True
        and row["valid_for_claim"] is False
        for row in rows_map["countermodel"]
    )


def bridge_next(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["status_id"] == "GB1771_3_next"
        and row["current_status"] == "PROJECTOR_PIM_COMMUTATOR_IS_NEXT"
        for row in rows_map["bridge_status"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["route_id"] == "NEXT1771_0_primary" and row["selection_status"] == "selected"
        for row in rows_map["next_target"]
    )


def check_row(check_id: str, condition: bool, pass_detail: str, fail_detail: str) -> dict[str, str]:
    return {
        "branch_id": BRANCH_ID,
        "check_id": check_id,
        "result": "PASS" if condition else "FAIL",
        "detail": pass_detail if condition else fail_detail,
    }


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    sources = rows_map["source_register"]
    claim_gates = rows_map["claim_gate"]
    checks = [
        check_row("VAL1771_0_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check_row("VAL1771_1_needles_present", all(row["needles_present"] for row in sources), "required source needles are present", "one or more source needles missing"),
        check_row("VAL1771_2_variation_attempt", variation_attempt_recorded(rows_map), "sector variation attempt recorded", "sector variation attempt missing"),
        check_row("VAL1771_3_projector_selected", projector_selected(rows_map), "projector/Pi_M commutator selected as next target", "projector/Pi_M priority missing"),
        check_row("VAL1771_4_operator_bounds_nonclaim", operator_bounds_nonclaim(rows_map), "operator bound inputs remain nonclaim", "operator bound inputs missing or promoted"),
        check_row("VAL1771_5_countermodel_retained", countermodel_retained(rows_map), "sector-silence countermodel remains retained", "countermodel missing or promoted"),
        check_row("VAL1771_6_bridge_next", bridge_next(rows_map), "bridge status selects Pi_M commutator next", "bridge next status missing"),
        check_row(
            "VAL1771_7_claim_gates_safe",
            all(row["gate_pass"] is False and row["status"] == "BLOCKED" for row in claim_gates),
            "all claim gates remain blocked",
            "one or more claim gates opened",
        ),
        check_row("VAL1771_8_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check_row("VAL1771_9_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check_row(
            "VAL1771_10_decision_next",
            any(row["decision_id"] == "DEC1771_3_best_next" and row["decision"] == "PIM_COMMUTATOR_PROJECTOR_VARIATION_ZERO_OR_BOUND_IS_NEXT" for row in rows_map["decision"]),
            "decision selects Pi_M commutator/projector route",
            "best-next decision missing",
        ),
        check_row("VAL1771_11_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check_row("VAL1771_12_csv_parse", csv_parse_all(), "all generated 1771 CSVs parse", "one or more generated 1771 CSVs fail to parse"),
        check_row("VAL1771_13_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "branch copies missing"),
        check_row("VAL1771_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check_row("VAL1771_15_formalization_untouched", formalization_untouched_for_1771(), "no 1771 outputs found under formalization-workbench", "1771 outputs found under formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in checks)
    checks.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1771_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1771 sector action variation and local scaling silence or operator bounds",
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    sections = [
        "# 1771 - Sector Action Variation And Local Scaling Silence Or Operator Bounds",
        "",
        "## Verdict",
        "- 1771 forces the non-EH residuals through a sector-by-sector variation and local-scaling audit.",
        "- No retained sector is fully silenced in the current corpus: every one is missing action ownership, first variation, stress/theta/Q accounting, boundary conditions, local scaling, or a source-backed bound.",
        "- The sharpest next target is not the generic higher-derivative tail; it is the concrete `Pi_M` commutator/projector obstruction because `[d,Pi_M]J_H` is already the exact product-rule blocker for both EH dominance and measured-GM/source normalization.",
        "- EH dominance and Newton/Poisson recovery remain nonclaim. The operator-bound pack stays live.",
        "- No GitHub, public, local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Sector Action Variation Ledger",
        markdown_table(rows_map["variation_ledger"], ["sector_id", "sector", "candidate_action_block", "variation_target", "variation_status", "local_silence_test", "verdict"]),
        "",
        "## Local Scaling Ledger",
        markdown_table(rows_map["scaling_ledger"], ["scale_id", "sector", "dimensionless_ratio", "local_silence_condition", "status", "bound_row"]),
        "",
        "## Silence Decision Ledger",
        markdown_table(rows_map["silence_decision"], ["decision_id", "sector", "zero_status", "bound_status", "reason", "next_action"]),
        "",
        "## Operator Bound Input Pack",
        markdown_table(rows_map["operator_bounds"], ["row_id", "quantity", "required_inputs", "status", "priority"]),
        "",
        "## Sector Priority Ledger",
        markdown_table(rows_map["priority"], ["rank", "sector", "why", "next_action", "selection_status"]),
        "",
        "## Countermodel Ledger",
        markdown_table(rows_map["countermodel"], ["countermodel_id", "countermodel", "mathematical_form", "survives_current_constraints", "why_survives", "what_kills_it"]),
        "",
        "## GR Bridge Status",
        markdown_table(rows_map["bridge_status"], ["status_id", "bridge_piece", "current_status", "evidence", "remaining_gap"]),
        "",
        "## Decisions",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "This checkpoint tells us where to swing next. Generic `DeltaE` is too broad; the `Pi_M` commutator is exact, local, and already tied to measured mass. If it can be proved zero from a fixed parent charge map, the GR/Newton bridge tightens sharply. If it cannot, it becomes a real coefficient row rather than a vague objection.",
        "",
    ]
    return "\n".join(sections)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1771-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1771 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
