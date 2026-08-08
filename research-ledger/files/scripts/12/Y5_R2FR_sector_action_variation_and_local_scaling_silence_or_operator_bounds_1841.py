from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1841"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1841-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1841_0_1840_next",
        "source_key": "1840_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1840_NEXT_TARGET.csv",
        "needles": ["NEXT1840_0_primary", "1841-Y5-R2FR-sector-action-variation"],
        "role": "1840 selects sector action variation/local scaling as the next local-GR bridge target.",
    },
    {
        "source_id": "SRC1841_1_1840_validation",
        "source_key": "1840_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1840_VALIDATION.csv",
        "needles": ["VAL1840_OVERALL", "PASS"],
        "role": "confirms 1840 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1841_2_1840_residual_silence",
        "source_key": "1840_residual_silence",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1840_RESIDUAL_SECTOR_SILENCE_AUDIT.csv",
        "needles": ["RSS1840_6_verdict", "RESIDUAL_SECTORS_RETAINED_NONCLAIM"],
        "role": "1840 retained all non-EH sectors as explicit residual debt.",
    },
    {
        "source_id": "SRC1841_3_1840_operator_pack",
        "source_key": "1840_operator_coefficient_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1840_OPERATOR_COEFFICIENT_PACK.csv",
        "needles": ["OPC1840_0_total_DeltaE", "MISSING_ZERO_THEOREM_OR_BOUNDED_COEFFICIENTS"],
        "role": "1840 supplies the broad DeltaE operator coefficient pack.",
    },
    {
        "source_id": "SRC1841_4_1009_parent_contract",
        "source_key": "1009_parent_current_chain",
        "source_path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "needles": ["PCS1009_9_total_parent_contract", "REFUSED_INCOMPLETE_PARENT_CURRENT_CHAIN_CONTRACT"],
        "role": "total parent action remains contract-level until sector certificates exist.",
    },
    {
        "source_id": "SRC1841_5_1013_pim_obstruction",
        "source_key": "1013_pim_flux_obstruction",
        "source_path": ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
        "needles": ["PFC1013_2_product_rule", "OBS1013_1_PiM_commutator"],
        "role": "Pi_M product-rule obstruction is the concrete source-normalization blocker.",
    },
    {
        "source_id": "SRC1841_6_1014_commutator_attempt",
        "source_key": "1014_pim_commutator",
        "source_path": ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
        "needles": ["PCT1014_7_verdict", "fail_current_claim"],
        "role": "Pi_M commutator/projector-stress zero was attempted and not promoted.",
    },
    {
        "source_id": "SRC1841_7_1015_same_object",
        "source_key": "1015_topological_hilbert_equality",
        "source_path": ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
        "needles": ["SOL1015_6_verdict", "conditional_lemma_written_current_claim_fails"],
        "role": "same-object topological/Hilbert equality is mathematically clean but parent-unsigned.",
    },
    {
        "source_id": "SRC1841_8_1016_worldtube_selector",
        "source_key": "1016_parent_worldtube_selector",
        "source_path": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
        "needles": ["PSC1016_9_verdict", "fail_current_claim"],
        "role": "parent worldtube/source-measure selector is explicit but not signed.",
    },
    {
        "source_id": "SRC1841_9_1017_hamiltonian_lock",
        "source_key": "1017_hamiltonian_reference_lock",
        "source_path": ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
        "needles": ["HPT1017_5_verdict", "fail_current_claim"],
        "role": "Hamiltonian PiM/reference/integrability lock identifies the next source-charge owner gap.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1841_SOURCE_REGISTER.csv",
    "variation_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1841_SECTOR_ACTION_VARIATION_LEDGER.csv",
    "scaling_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1841_LOCAL_SCALING_LEDGER.csv",
    "obstruction_transfer": RESIDUALS / "P8_Y5_PARENT_QLOC_1841_OBSTRUCTION_TRANSFER_LEDGER.csv",
    "operator_bounds": RESIDUALS / "P8_Y5_PARENT_QLOC_1841_OPERATOR_BOUND_INPUT_PACK.csv",
    "priority": RESIDUALS / "P8_Y5_PARENT_QLOC_1841_SECTOR_PRIORITY_LEDGER.csv",
    "gr_bridge": RESIDUALS / "P8_Y5_PARENT_QLOC_1841_GR_BRIDGE_STATUS.csv",
    "current_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1841_CURRENT_CORPUS_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1841_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1841_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1841_VALIDATION.csv",
}


def ensure_dirs() -> None:
    for directory in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": not missing,
                "missing_needles": ";".join(missing),
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def variation_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "sector_id": "SAV1841_0_higher_derivative",
            "sector": "higher-curvature / higher-derivative",
            "candidate_action_block": "S_HD = int sqrt(-g)(c_R2 R^2 + c_Ricci2 R_munu R^munu + c_boxR R box R + ...)",
            "variation_target": "E_HD_munu",
            "variation_status": "FORM_TEMPLATE_KNOWN_PARENT_ADOPTION_UNSIGNED",
            "local_silence_test": "sector absent from parent normal form, topological, or c_HD/L_local^2 below all local tolerances",
            "result": "RETAIN_BOUND_INPUT",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "SAV1841_1_projector_PiM",
            "sector": "Pi_M/domain/projector source-measure",
            "candidate_action_block": "Hamiltonian/topological/projector source map Pi_M J_H",
            "variation_target": "d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H and delta_g Pi_M projector stress",
            "variation_status": "EXACT_OBSTRUCTION_NOT_SILENCED",
            "local_silence_test": "Pi_M is a fixed chain map on the same Hilbert worldtube and delta_g Pi_M stress vanishes or is bounded",
            "result": "CONCRETE_ROOT_BLOCKER_RETURNS_TO_SOURCE_CHARGE_OWNER",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "SAV1841_2_boundary_reference",
            "sector": "boundary/reference/improvement",
            "candidate_action_block": "S_GHY + B_ref + exact/topological improvements + symplectic boundary terms",
            "variation_target": "theta_boundary, Q_boundary, B_zero_flux, Delta_symp, H_ref_shift",
            "variation_status": "REFERENCE_LOCK_UNSIGNED",
            "local_silence_test": "fixed-before-readout reference plus zero compact linked-boundary flux",
            "result": "RETAIN_BOUND_INPUT",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "SAV1841_3_nonminimal",
            "sector": "nonminimal matter-geometry/MTS coupling",
            "candidate_action_block": "S_nonmin = int sqrt(-g)c_NM f(X,Phi,labels)L_m or A(X)J_m",
            "variation_target": "E_nonmin_munu plus modified matter/source equations",
            "variation_status": "NOT_FORBIDDEN_BY_COMPLETE_PARENT_ACTION",
            "local_silence_test": "normal form forbids the channel or maps it to WEP/clock/PPN/R10 coefficient bounds",
            "result": "RETAIN_BOUND_INPUT",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "SAV1841_4_memory_coframe",
            "sector": "memory/coframe/preferred-frame/current-chain",
            "candidate_action_block": "S_memory/coframe with theta_X,Q_X,C_tau and tau-lock terms",
            "variation_target": "E_memory_munu, E_coframe_munu, PPN alpha_i, clock drift residuals",
            "variation_status": "LOCAL_FRAME_AND_TAU_LOCK_UNSIGNED",
            "local_silence_test": "local coframe lock and tau_source=tau_charge=tau_clock=tau_readout make preferred-frame stress zero",
            "result": "RETAIN_BOUND_INPUT",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "SAV1841_5_source_normalization",
            "sector": "worldtube/source normalization/Hamiltonian source charge",
            "candidate_action_block": "Pi_M^H J_H, H_tau[S]-H_ref, M_H_ref, worldtube source measure",
            "variation_target": "M_H_ref, R_eq, I_commutator, Delta_ref, symplectic_boundary_flux",
            "variation_status": "EXACT_CONTRACT_WRITTEN_NOT_SIGNED",
            "local_silence_test": "M_H_ref is a same-frame dressed Hamiltonian/Hilbert charge before orbital/PPN readout",
            "result": "PRIMARY_ROOT_BLOCKER_FOR_NEWTON_GR_BRIDGE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "SAV1841_6_verdict",
            "sector": "sector action variation for current MTS",
            "candidate_action_block": "all retained non-EH sectors",
            "variation_target": "all DeltaE_i and source-normalization residuals",
            "variation_status": "NO_SECTOR_FULLY_SILENCED",
            "local_silence_test": "not achieved",
            "result": "EH_DOMINANCE_AND_NEWTON_REMAIN_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def scaling_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "scale_id": "SCL1841_0_higher_derivative",
            "sector": "higher-derivative",
            "dimensionless_ratio": "epsilon_HD ~ |c_HD|/L_local^2 plus operator-basis factors",
            "local_silence_condition": "epsilon_HD below PPN/R10/orbital tolerance or c_HD=0 by parent normal form",
            "status": "MISSING_COEFFICIENT_SCALE_AND_TOLERANCE",
            "bound_row": "OBI1841_1_higher_derivative",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "scale_id": "SCL1841_1_projector",
            "sector": "Pi_M/projector",
            "dimensionless_ratio": "epsilon_PiM ~ |I_commutator|/M_H_ref + |projector_stress_beta_equiv|",
            "local_silence_condition": "I_commutator=0 and projector stress=0, or both are source-backed below arena bounds",
            "status": "MISSING_I_COMMUTATOR_MHREF_AND_PROJECTOR_STRESS",
            "bound_row": "OBI1841_2_projector",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "scale_id": "SCL1841_2_boundary",
            "sector": "boundary/reference",
            "dimensionless_ratio": "epsilon_boundary ~ |B_zero_flux + Delta_symp + H_ref_shift|/M_H_ref",
            "local_silence_condition": "fixed reference and zero compact linked-boundary flux before readout",
            "status": "MISSING_BOUNDARY_REFERENCE_LOCK",
            "bound_row": "OBI1841_3_boundary",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "scale_id": "SCL1841_3_nonminimal",
            "sector": "nonminimal matter-geometry",
            "dimensionless_ratio": "epsilon_NM ~ |c_NM q_comp| or induced source/readout coupling leakage",
            "local_silence_condition": "channel forbidden by parent object-language or bounded by WEP/clock/PPN/R10",
            "status": "MISSING_NONMINIMAL_OPERATOR_AND_COMPOSITION_MAP",
            "bound_row": "OBI1841_4_nonminimal",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "scale_id": "SCL1841_4_memory_coframe",
            "sector": "memory/coframe/current-chain",
            "dimensionless_ratio": "epsilon_frame ~ preferred-frame alpha_i + clock drift + tau-lock mismatch",
            "local_silence_condition": "parent tau/coframe lock makes local preferred-frame and clock residuals zero",
            "status": "MISSING_LOCAL_FRAME_TAU_LOCK",
            "bound_row": "OBI1841_5_memory_coframe",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "scale_id": "SCL1841_5_source_normalization",
            "sector": "source normalization",
            "dimensionless_ratio": "epsilon_source ~ abs(R_eq,B_zero,I_commutator,Delta_ref,Delta_symp,delta_H_tau)/M_H_ref",
            "local_silence_condition": "same-frame M_H_ref plus zero/bounded numerator components with no cancellation",
            "status": "MISSING_MHREF_AND_NUMERATOR_COMPONENTS",
            "bound_row": "OBI1841_6_source_normalization",
            "valid_for_claim": False,
        },
    ]


def obstruction_transfer_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "transfer_id": "OT1841_0_broad_DeltaE_to_sector_list",
            "input_obstruction": "DeltaE_munu broad non-EH residual",
            "source_evidence": "1840 operator pack",
            "transfer_result": "split into higher-derivative, projector, boundary, nonminimal, memory/coframe and source-normalization sectors",
            "claim_status": "NONCLAIM",
            "next_requirement": "sector-specific variation/local scaling rows",
        },
        {
            "branch_id": BRANCH_ID,
            "transfer_id": "OT1841_1_projector_to_same_object",
            "input_obstruction": "[d,Pi_M]J_H and delta_g Pi_M stress",
            "source_evidence": "1013/1014",
            "transfer_result": "projector silence requires Pi_M to be a fixed chain map on the same Hilbert source worldtube",
            "claim_status": "NOT_PROVED",
            "next_requirement": "same-object Hilbert/topological equality and M_H_ref owner",
        },
        {
            "branch_id": BRANCH_ID,
            "transfer_id": "OT1841_2_same_object_to_worldtube",
            "input_obstruction": "closed topological current can be the wrong conserved object",
            "source_evidence": "1015",
            "transfer_result": "must parent-select W_source=closure(supp J_H[tau]) and same-frame source measure",
            "claim_status": "CONDITIONAL_LEMMA_ONLY",
            "next_requirement": "parent worldtube/source-measure selector",
        },
        {
            "branch_id": BRANCH_ID,
            "transfer_id": "OT1841_3_worldtube_to_Hamiltonian_lock",
            "input_obstruction": "source worldtube/source measure lacks stable charge denominator",
            "source_evidence": "1016/1017",
            "transfer_result": "need L_X, Theta_X, Q_X, boundary/reference class and tau lock before M_H_ref can normalize residuals",
            "claim_status": "PRIMARY_OWNER_GAP",
            "next_requirement": "sector Lagrangian/boundary owner or FB5540 source row",
        },
    ]


def operator_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "OBI1841_0_total_DeltaE",
            "quantity": "DeltaE_munu",
            "required_inputs": "sector basis; coefficient units; local scaling; absolute-sum no-cancellation guard; arena map",
            "status": "MISSING_SECTOR_BOUNDS",
            "priority": "global",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OBI1841_1_higher_derivative",
            "quantity": "c_HD",
            "required_inputs": "parent action adoption/absence theorem; operator units; L_local; PPN/R10/orbit map",
            "status": "MISSING_OPERATOR_BASIS_UNITS_BOUNDS",
            "priority": "medium",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OBI1841_2_projector",
            "quantity": "I_commutator;projector_stress_beta_equiv;Delta_PiM",
            "required_inputs": "Pi_M owner; M_H_ref; finite annulus integral; weak-field stress map; source paths",
            "status": "MISSING_PIM_COMMUTATOR_PROJECTOR_STRESS",
            "priority": "highest",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OBI1841_3_boundary",
            "quantity": "B_zero_flux;Delta_symp;H_ref_shift",
            "required_inputs": "fixed reference; boundary/falloff rule; compact linked surface pair; M_H_ref; units",
            "status": "MISSING_BOUNDARY_REFERENCE_CERTIFICATE",
            "priority": "highest_coupled_to_MHref",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OBI1841_4_nonminimal",
            "quantity": "c_nonminimal;B_obs_source_measure_over_MH",
            "required_inputs": "normal-form forbid theorem or WEP/clock/PPN/R10 projection with units and source paths",
            "status": "MISSING_NONMINIMAL_OPERATOR_MAP",
            "priority": "high",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OBI1841_5_memory_coframe",
            "quantity": "c_memory;c_frame;tau_lock_mismatch",
            "required_inputs": "L_X/Theta_X/Q_X owner; tau generator lock; clock/PPN preferred-frame map",
            "status": "MISSING_FRAME_TAU_LOCK_OR_BOUND",
            "priority": "high",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OBI1841_6_source_normalization",
            "quantity": "M_H_ref;R_eq_integral;delta_H_tau_nonintegrable;Delta_ref;symplectic_boundary_flux;epsilon_HPiM_integrability_abs",
            "required_inputs": "same-frame Hamiltonian source charge denominator plus all numerator components with source paths",
            "status": "MISSING_MHREF_AND_FB5540_COMPONENTS",
            "priority": "highest_root",
            "valid_for_claim": False,
        },
    ]


def priority_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "rank": 1,
            "target": "sector Lagrangian/boundary owner",
            "why": "without L_X,Theta_X,Q_X,B_ref,B_class/tau ownership, sector variation is notation not derivation",
            "next_action": "derive owners or fill FB5540 source row",
            "selection_status": "primary_next",
        },
        {
            "branch_id": BRANCH_ID,
            "rank": 2,
            "target": "Hamiltonian PiM and M_H_ref denominator",
            "why": "Pi_M commutator/equality residuals cannot be normalized without a non-circular source charge",
            "next_action": "derive positive same-frame M_H_ref and reference lock",
            "selection_status": "coupled_primary",
        },
        {
            "branch_id": BRANCH_ID,
            "rank": 3,
            "target": "R_eq/I_commutator/projector-stress rows",
            "why": "these are the concrete residual quantities if zero proof fails",
            "next_action": "keep nonclaim until source-backed values or theorem zeros exist",
            "selection_status": "bound_fallback",
        },
        {
            "branch_id": BRANCH_ID,
            "rank": 4,
            "target": "nonminimal matter coupling descent",
            "why": "dangerous for WEP/clocks but downstream of parent action ownership",
            "next_action": "forbid by parent language or map to empirical coefficients",
            "selection_status": "queued",
        },
        {
            "branch_id": BRANCH_ID,
            "rank": 5,
            "target": "higher-derivative and memory/coframe tails",
            "why": "important but need operator bases and local scale hierarchy before scoring",
            "next_action": "operator basis and scale map",
            "selection_status": "queued",
        },
    ]


def gr_bridge_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1841_0_sector_variation",
            "bridge_piece": "sector-by-sector action variation",
            "current_status": "INCOMPLETE_NONCLAIM",
            "evidence": "SAV1841 rows",
            "remaining_gap": "no retained non-EH sector has action owner + first variation + local scaling + empirical bound certificate",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1841_1_EH_dominance",
            "bridge_piece": "EH dominance",
            "current_status": "NOT_PROVED",
            "evidence": "RSS1840 plus SAV1841_6",
            "remaining_gap": "DeltaE sectors retained and source normalization unresolved",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1841_2_Newton_Poisson",
            "bridge_piece": "Newton/Poisson/source normalization",
            "current_status": "BLOCKED_AT_HAMILTONIAN_SOURCE_CHARGE",
            "evidence": "1016/1017 plus OBI1841_6",
            "remaining_gap": "M_H_ref, reference lock, tau lock, and no-cancellation numerator components missing",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1841_3_empirical_route",
            "bridge_piece": "PPN/R10/clock/orbit residual scoring",
            "current_status": "NOT_SCORE_READY",
            "evidence": "OBI1841 rows",
            "remaining_gap": "rows have quantities but no source-backed numeric values or theorem zeros",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1841_4_next",
            "bridge_piece": "next derivation owner",
            "current_status": "SECTOR_LAGRANGIAN_BOUNDARY_OWNER_OR_FB5540_SOURCE_ROW_IS_NEXT",
            "evidence": "priority rank 1; 1017 next target",
            "remaining_gap": "derive L_X/Theta_X/Q_X plus boundary/tau ownership, or fill first FB5540 row",
            "valid_for_claim": False,
        },
    ]


def current_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1841_0_sector_silence",
            "claim": "all non-EH sectors are locally silent or suppressed",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "NO_SECTOR_HAS_FULL_VARIATION_SCALING_CERTIFICATE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1841_1_EH_dominance",
            "claim": "EH dominance follows for current MTS",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "PROJECTOR_BOUNDARY_NONMINIMAL_FRAME_SOURCE_RESIDUALS_RETAINED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1841_2_MHref",
            "claim": "M_H_ref is a stable same-frame Hamiltonian source denominator",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "L_X_THETA_X_Q_X_REFERENCE_TAU_OWNERS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1841_3_Newton_GR",
            "claim": "Newton/local GR recovery is derived",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "EH_DOMINANCE_AND_SOURCE_NORMALIZATION_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1841_4_empirical_scoring",
            "claim": "PPN/R10/clock/orbit residual rows are score-ready",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "NO_SOURCE_BACKED_THEOREM_ZERO_OR_NUMERIC_ROWS",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1841_0_sector_result",
            "decision": "NO_NON_EH_SECTOR_FULLY_SILENCED",
            "reason": "each sector lacks at least one of action ownership, variation, theta/Q accounting, boundary/reference lock, local scaling, or empirical coefficient",
            "next_action": "retain operator bound pack",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1841_1_projector_result",
            "decision": "PIM_COMMUTATOR_REDUCES_TO_SOURCE_CHARGE_OWNER",
            "reason": "1014-1017 show fixed-chain-map/equality/selector/reference-lock clauses are the real blockers",
            "next_action": "do not repeat broad Pi_M slogans; attack Hamiltonian source owner",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1841_2_no_claim",
            "decision": "LOCAL_GR_NEWTON_NOT_CLAIMED",
            "reason": "EH dominance and source-normalization gates remain blocked",
            "next_action": "keep all local and empirical gates false",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1841_3_best_next",
            "decision": "SECTOR_LAGRANGIAN_BOUNDARY_OWNER_OR_FB5540_SOURCE_ROW_IS_NEXT",
            "reason": "this is the first missing structure that could make Pi_M^H, M_H_ref, boundary lock, and tau lock derivable rather than fitted",
            "next_action": "1842-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1841_0_primary",
            "next_target": "1842-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
            "script": "scripts/Y5_R2FR_sector_Lagrangian_boundary_owner_or_FB5540_source_row_1842.py",
            "objective": "derive L_X/Theta_X/Q_X plus B_ref/B_class/tau ownership for the Hamiltonian source charge, or fill a source-backed FB5540 row with M_H_ref and all numerator components",
            "selection_status": "selected",
            "success_condition": "M_H_ref and every FB5540 numerator component are theorem-zero or source-backed nonclaim rows with units, signs, source paths and no-cancellation bookkeeping",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1841_1_parallel",
            "next_target": "1842b-Y5-R2FR-Poisson-Gauss-worldtube-source-normalization-pack.md",
            "script": "scripts/Y5_R2FR_Poisson_Gauss_worldtube_source_normalization_pack_1842b.py",
            "objective": "derive parent source charge to exterior Gauss flux and measured GM without orbital backfill",
            "selection_status": "parallel_held",
            "success_condition": "Poisson/Gauss/worldtube equality is derived after the Hamiltonian source owner is stable",
        },
    ]


def build_rows_map() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "variation_ledger": variation_ledger_rows(),
        "scaling_ledger": scaling_ledger_rows(),
        "obstruction_transfer": obstruction_transfer_rows(),
        "operator_bounds": operator_bound_rows(),
        "priority": priority_rows(),
        "gr_bridge": gr_bridge_rows(),
        "current_gate": current_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }


def fieldnames(rows: list[dict[str, Any]]) -> list[str]:
    names: list[str] = []
    for row in rows:
        for key in row:
            if key not in names:
                names.append(key)
    return names


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames(rows))
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        for target in [
            MICROSCOPE_RESIDUALS / path.name,
            QUARANTINE / path.name,
            RAB_QUEUE / f"JR1841_{key.upper()}.csv",
        ]:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def parse_csv_ok(path: Path) -> bool:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def csv_parse_all() -> bool:
    return all(parse_csv_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        if not (MICROSCOPE_RESIDUALS / path.name).exists():
            return False
        if not (QUARANTINE / path.name).exists():
            return False
        if not (RAB_QUEUE / f"JR1841_{key.upper()}.csv").exists():
            return False
    return True


def no_formalization_outputs() -> bool:
    if not FORMALIZATION.exists():
        return True
    markers = [
        "1841-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_1841",
        "P8_Y5_BRR545_1841",
        "Y5_R2FR_sector_action_variation_and_local_scaling_silence_or_operator_bounds_1841",
    ]
    return not any(any(marker in path.name for marker in markers) for path in FORMALIZATION.rglob("*"))


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            for field in ["valid_for_claim", "claim_allowed", "gate_pass", "score_ready"]:
                if row.get(field) is True:
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            has_missing = any("MISSING_" in str(value) for value in row.values())
            if not has_missing:
                continue
            for field in ["valid_for_claim", "claim_allowed", "gate_pass", "score_ready"]:
                if row.get(field) is True:
                    return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    checks = [
        ("VAL1841_0_sources_exist", all(row["exists"] is True for row in source_rows), "all cited source paths exist"),
        ("VAL1841_1_needles_present", all(row["needles_present"] is True for row in source_rows), "all cited source needles are present"),
        (
            "VAL1841_2_variation_attempt",
            any(row["sector_id"] == "SAV1841_6_verdict" and row["variation_status"] == "NO_SECTOR_FULLY_SILENCED" for row in rows_map["variation_ledger"]),
            "sector variation attempt records no full silence",
        ),
        (
            "VAL1841_3_source_charge_owner_selected",
            any(row["rank"] == 1 and row["target"] == "sector Lagrangian/boundary owner" for row in rows_map["priority"]),
            "sector Lagrangian/boundary owner selected as primary next target",
        ),
        (
            "VAL1841_4_operator_bounds_nonclaim",
            all(row["valid_for_claim"] is False for row in rows_map["operator_bounds"]) and any(row["row_id"] == "OBI1841_6_source_normalization" for row in rows_map["operator_bounds"]),
            "operator bound inputs remain nonclaim and include source-normalization root row",
        ),
        (
            "VAL1841_5_obstruction_transfer_written",
            any(row["transfer_id"] == "OT1841_3_worldtube_to_Hamiltonian_lock" for row in rows_map["obstruction_transfer"]),
            "obstruction transfer reaches Hamiltonian source owner gap",
        ),
        (
            "VAL1841_6_bridge_next",
            any(row["status_id"] == "GB1841_4_next" and row["current_status"] == "SECTOR_LAGRANGIAN_BOUNDARY_OWNER_OR_FB5540_SOURCE_ROW_IS_NEXT" for row in rows_map["gr_bridge"]),
            "bridge status selects source-owner/FB5540 next",
        ),
        (
            "VAL1841_7_current_gates_block",
            all(row["gate_pass"] is False and row["claim_allowed"] is False for row in rows_map["current_gate"]),
            "all local/empirical claim gates remain blocked",
        ),
        ("VAL1841_8_no_claim_flags", no_claim_flags(rows_map), "no generated claim flags are true"),
        ("VAL1841_9_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1841_10_decision_next",
            any(row["decision_id"] == "DEC1841_3_best_next" and row["decision"] == "SECTOR_LAGRANGIAN_BOUNDARY_OWNER_OR_FB5540_SOURCE_ROW_IS_NEXT" for row in rows_map["decision"]),
            "decision selects sector Lagrangian/boundary owner or FB5540 row",
        ),
        (
            "VAL1841_11_next_selected",
            any(row["route_id"] == "NEXT1841_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1841_12_csv_parse", csv_parse_all(), "all generated 1841 CSVs parse"),
        ("VAL1841_13_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1841_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1841_15_formalization_untouched", no_formalization_outputs(), "no 1841 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1841_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1841 sector action variation and local scaling silence or operator bounds",
        }
    )
    return rows


def markdown_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1841 Y5 R2FR sector action variation and local scaling silence or operator bounds",
            "",
            "**Progress:** 1841 forces every retained non-EH local sector through the same test: action owner, first variation, boundary/theta/Q accounting, local scaling, and empirical fallback row.",
            "",
            "**Current verdict:** no non-EH sector is fully silenced. The generic `DeltaE_munu` problem has been sharpened into a source-charge owner problem: without `L_X`, `Theta_X`, `Q_X`, boundary/reference ownership, tau lock, and a stable `M_H_ref`, the PiM/worldtube route cannot derive Newton or local GR.",
            "",
            "**Claim ceiling:** no EH-dominance, Newton, local-GR, PPN, WEP, R10, clock, orbital, source-normalization, or GitHub/public claim is made from 1841.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Sector Action Variation Ledger",
            markdown_table(rows_map["variation_ledger"], ["sector_id", "sector", "variation_status", "local_silence_test", "result", "valid_for_claim"]),
            "",
            "## Local Scaling Ledger",
            markdown_table(rows_map["scaling_ledger"], ["scale_id", "sector", "dimensionless_ratio", "local_silence_condition", "status", "bound_row", "valid_for_claim"]),
            "",
            "## Obstruction Transfer Ledger",
            markdown_table(rows_map["obstruction_transfer"], ["transfer_id", "input_obstruction", "source_evidence", "transfer_result", "claim_status", "next_requirement"]),
            "",
            "## Operator Bound Input Pack",
            markdown_table(rows_map["operator_bounds"], ["row_id", "quantity", "required_inputs", "status", "priority", "valid_for_claim"]),
            "",
            "## Sector Priority Ledger",
            markdown_table(rows_map["priority"], ["rank", "target", "why", "next_action", "selection_status"]),
            "",
            "## GR Bridge Status",
            markdown_table(rows_map["gr_bridge"], ["status_id", "bridge_piece", "current_status", "evidence", "remaining_gap", "valid_for_claim"]),
            "",
            "## Current Corpus Gate",
            markdown_table(rows_map["current_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decisions",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is a useful narrowing, not a retreat. The project is no longer waving at 'extra sectors' in the abstract. The hard GR/Newton bridge has a named owner: derive the sector Lagrangians and boundary/tau/Hamiltonian charge machinery, or the local branch remains a closure/bound programme rather than a derivation.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = build_rows_map()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1841 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
