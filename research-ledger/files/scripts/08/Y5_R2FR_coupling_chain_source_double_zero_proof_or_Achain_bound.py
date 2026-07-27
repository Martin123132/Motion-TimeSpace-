from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1759"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1759 - Coupling-Chain Source Double-Zero Proof Or Achain Bound"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1759_0_1758_doc",
        "source_key": "1758_handoff",
        "source_path": ROOT / "1758-Y5-R2FR-primitive-minimality-invariant-algebra-or-Aaffine-bound.md",
        "needles": ["COUPLING_CHAIN_SOURCE_IS_NEXT_BEST_DERIVATION_ROUTE", "A_chain"],
    },
    {
        "source_id": "SRC1759_1_1756_hidden_source",
        "source_key": "1756_hidden_source_ledger",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1756_HIDDEN_SOURCE_COUNTEREXAMPLE_LEDGER.csv",
        "needles": ["HSC1756_3_coupling_chain_source", "f'(0)C_obs partial_X chi_D"],
    },
    {
        "source_id": "SRC1759_2_1756_Achain",
        "source_key": "1756_Achain_row",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1756_HIDDEN_SOURCE_FINITE_RESIDUAL_ROWS.csv",
        "needles": ["HSR1756_3_chain", "MISSING_COUPLING_DOUBLE_ZERO_OR_A_CHAIN"],
    },
    {
        "source_id": "SRC1759_3_double_zero_origin",
        "source_key": "double_zero_memory_origin",
        "source_path": RESIDUALS / "P8_DOUBLE_ZERO_MEMORY_ORIGIN_ATTEMPT.csv",
        "needles": ["O0_general_gate", "f(0)=0 and f_prime(0)=0"],
    },
    {
        "source_id": "SRC1759_4_double_zero_variation",
        "source_key": "double_zero_variation_test",
        "source_path": RESIDUALS / "P8_DOUBLE_ZERO_MEMORY_VARIATION_TEST.csv",
        "needles": ["f(chi_D)=chi_D", "fail_hidden_selector_exchange", "pass_as_sufficient_contract"],
    },
    {
        "source_id": "SRC1759_5_double_zero_power_gate",
        "source_key": "double_zero_power_gate",
        "source_path": RESIDUALS / "P8_DOUBLE_ZERO_MEMORY_POWER_GATE.csv",
        "needles": ["P0_power_condition", "P3_FLRW_normalization"],
    },
    {
        "source_id": "SRC1759_6_double_zero_decision",
        "source_key": "double_zero_decision",
        "source_path": RESIDUALS / "P8_DOUBLE_ZERO_MEMORY_DECISION.csv",
        "needles": ["D0_double_zero_requirement", "D1_origin"],
    },
    {
        "source_id": "SRC1759_7_domain_clause",
        "source_key": "domain_selector_parent_clause",
        "source_path": RESIDUALS / "P8_DOMAIN_SELECTOR_PARENT_ACTION_CLAUSE.csv",
        "needles": ["C3_double_zero_memory", "sufficient_clause_not_derived"],
    },
    {
        "source_id": "SRC1759_8_domain_variation",
        "source_key": "domain_selector_variation_chain",
        "source_path": RESIDUALS / "P8_DOMAIN_SELECTOR_PARENT_ACTION_VARIATION_CHAIN.csv",
        "needles": ["V1_chi_variation", "formal_pass_for_double_zero_clause"],
    },
    {
        "source_id": "SRC1759_9_domain_gate",
        "source_key": "domain_selector_gate",
        "source_path": RESIDUALS / "P8_DOMAIN_SELECTOR_PARENT_ACTION_GATE.csv",
        "needles": ["G2_double_zero_origin", "G3_local_zero"],
    },
    {
        "source_id": "SRC1759_10_active_vs_double_zero",
        "source_key": "active_vs_double_zero",
        "source_path": RESIDUALS / "P8_Y5_R10_970_ACTIVE_VS_DOUBLE_ZERO_BRANCH_AUDIT.csv",
        "needles": ["ADB970_1_double_zero_decoupling", "CLOSURE_SAFE_NOT_ZERO_PROOF"],
    },
    {
        "source_id": "SRC1759_11_coupling_contract",
        "source_key": "897_coupling_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_897_COUPLING_CONTRACT.csv",
        "needles": ["CC897_1_metric_leakage_contract", "not_signed"],
    },
    {
        "source_id": "SRC1759_12_coupling_bottleneck",
        "source_key": "896_coupling_bottleneck",
        "source_path": RESIDUALS / "P8_Y5_R10_896_COUPLING_BOTTLENECK_REGISTER.csv",
        "needles": ["CB896_1_double_zero", "criterion_exists_not_trace_signed"],
    },
    {
        "source_id": "SRC1759_13_coupling_prior_candidates",
        "source_key": "981_coupling_prior_candidates",
        "source_path": RESIDUALS / "P8_Y5_R10_981_COUPLING_PRIOR_CANDIDATES.csv",
        "needles": ["CP981_0_b_kappa_species_split_WEP", "blocked_nonclaim"],
    },
    {
        "source_id": "SRC1759_14_991_priority",
        "source_key": "991_live_obstruction_priority",
        "source_path": RESIDUALS / "P8_Y5_R10_991_LIVE_OBSTRUCTION_PRIORITY.csv",
        "needles": ["PRI991_3_coupling_source_measure", "coupling leakage can fake measured-GM"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1759_SOURCE_REGISTER.csv",
    "coupling_chain_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1759_COUPLING_CHAIN_SOURCE_ATTEMPT.csv",
    "double_zero_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1759_DOUBLE_ZERO_GATE_AUDIT.csv",
    "chi_independence": RESIDUALS / "P8_Y5_PARENT_QLOC_1759_CHID_INDEPENDENCE_AUDIT.csv",
    "achain_bound": RESIDUALS / "P8_Y5_PARENT_QLOC_1759_ACHAIN_BOUND_INTERFACE.csv",
    "source_zero_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1759_SOURCE_ZERO_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1759_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1759_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1759_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1759_VALIDATION.csv",
}


COPY_MAP = {
    "coupling_chain_attempt": "R2FR_1759_COUPLING_CHAIN_SOURCE_ATTEMPT.csv",
    "double_zero_gate": "R2FR_1759_DOUBLE_ZERO_GATE_AUDIT.csv",
    "chi_independence": "R2FR_1759_CHID_INDEPENDENCE_AUDIT.csv",
    "achain_bound": "R2FR_1759_ACHAIN_BOUND_INTERFACE.csv",
    "source_zero_status": "R2FR_1759_SOURCE_ZERO_STATUS.csv",
    "decision": "R2FR_1759_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1759_CLAIM_GATE.csv",
    "next_target": "R2FR_1759_NEXT_TARGET.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("|", "\\|").replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        needles_present = all(needle in text for needle in needles)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": yesno(exists),
                "needles": "; ".join(needles),
                "needles_present": yesno(needles_present),
                "used_for": "1759 coupling-chain source double-zero proof or Achain bound",
                "timestamp_utc": UTC,
            }
        )
    return rows


def coupling_chain_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "CCS1759_0_target",
            "claim_piece": "coupling-chain source zero",
            "mathematical_form": "J_chain = f'(0) C_obs partial_X chi_D + f(0) delta_X C_obs at chi_D=0",
            "status": "TARGET_EXACT",
            "proof_status": "ZERO_IF_DOUBLE_ZERO_OR_SELECTOR_INDEPENDENCE",
            "gap": "need parent-owned f(0)=f'(0)=0 or partial_X chi_D=0; neither is signed",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "CCS1759_1_direct_term",
            "claim_piece": "direct observed-coupling term",
            "mathematical_form": "f(0) delta_X C_obs",
            "status": "CONDITIONAL_ZERO_IF_F0_ZERO",
            "proof_status": "REQUIRED_BY_LOCAL_SILENCE_CONTRACT_NOT_PARENT_ORIGIN",
            "gap": "f(0)=0 is a necessary gate condition, not a derived parent activation law",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "CCS1759_2_chain_term",
            "claim_piece": "chain derivative term",
            "mathematical_form": "f'(0) C_obs partial_X chi_D",
            "status": "MAIN_OBSTRUCTION",
            "proof_status": "NOT_ZEROED",
            "gap": "linear gate f=chi_D fails; f'(0)=0 or partial_X chi_D=0 must be parent-derived",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "CCS1759_3_double_zero_sufficiency",
            "claim_piece": "quadratic or higher gate",
            "mathematical_form": "f(chi_D)=O(chi_D^2) gives f(0)=f'(0)=0",
            "status": "EXACT_SUFFICIENT_CONTRACT",
            "proof_status": "SUFFICIENT_NOT_PARENT_DERIVED",
            "gap": "determinant/norm-square/topological origins remain conditional and FLRW normalization is open",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "CCS1759_4_selector_independence",
            "claim_piece": "selector-independent local memory variable",
            "mathematical_form": "partial_X chi_D=0 on the local branch",
            "status": "ALTERNATIVE_ZERO_ROUTE",
            "proof_status": "NOT_PARENT_DERIVED",
            "gap": "chi_D/domain selector is still an uneliminated invariant generator from 1758",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "CCS1759_5_verdict",
            "claim_piece": "coupling-chain theorem verdict",
            "mathematical_form": "J_chain=0 is theorem-shaped but not parent-signed",
            "status": "THEOREM_CONTRACT_READY_PARENT_UNSIGNED",
            "proof_status": "A_CHAIN_RETAINED",
            "gap": "missing parent double-zero origin, local chi_D zero/independence, and same-branch FLRW normalization",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def double_zero_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "DZ1759_0_power_condition",
            "requirement": "Taylor order p>=2 at chi_D=0",
            "mathematical_form": "f(0)=0 and f'(0)=0",
            "current_status": "DERIVED_AS_REQUIREMENT",
            "why_needed": "kills memory stress and selector exchange at the local zero",
            "blocker": "MISSING_PARENT_ORIGIN_OF_DOUBLE_ZERO",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "DZ1759_1_linear_gate_rejected",
            "requirement": "reject p=1 gate",
            "mathematical_form": "f(chi_D)=chi_D has f(0)=0 but f'(0)=1",
            "current_status": "FAILS_LOCAL_BRANCH",
            "why_needed": "hidden selector exchange lambda=-L_mem returns",
            "blocker": "LINEAR_GATE_REQUIRES_EXPLICIT_COEFFICIENT_BRANCH",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "DZ1759_2_determinant_candidate",
            "requirement": "determinant/current route",
            "mathematical_form": "J_C ~ det(Q_coh) ~ amplitude^3",
            "current_status": "CONDITIONAL_SUPPORT_NOT_PARENT_OWNED",
            "why_needed": "could give p>=3 without hand insertion",
            "blocker": "MISSING_COHERENT_VOLUME_PARENT_KINEMATICS_AND_NORMALIZATION",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "DZ1759_3_norm_square_candidate",
            "requirement": "norm-square/Z2 route",
            "mathematical_form": "f(chi_D)=|A_D|^2 or chi_D^2 under chi_D -> -chi_D",
            "current_status": "CANDIDATE_NOT_PARENT_SIGNED",
            "why_needed": "natural source of p=2 activation",
            "blocker": "MISSING_SELECTOR_AMPLITUDE_Z2_OR_NORM_SQUARE_PARENT_OWNER",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "DZ1759_4_topological_pairing_candidate",
            "requirement": "quadratic class pairing route",
            "mathematical_form": "f_D ~ <J_rel,J_rel>_D or ||Pi_rel J_B||^2",
            "current_status": "CANDIDATE_NOT_PARENT_SIGNED",
            "why_needed": "could make double-zero topological rather than fitted",
            "blocker": "MISSING_RELATIVE_CHAIN_COHOMOLOGY_PROJECTOR_OWNER",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "DZ1759_5_FLRW_normalization",
            "requirement": "same gate keeps cosmology branch active with derived amplitude",
            "mathematical_form": "p>=2 local silence must not overstrong-zero the FLRW/cosmology memory branch",
            "current_status": "NOT_PARENT_DERIVED",
            "why_needed": "prevents local repair from killing the unified-field spine",
            "blocker": "MISSING_BRANCH_NORMALIZATION_AND_PARENT_SELECTOR_RULE",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def chi_independence_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CHI1759_0_auxiliary_scalar",
            "claim": "chi_D is auxiliary scalar with no kinetic/local vector term",
            "mathematical_form": "S_D includes lambda_D(chi_D-Sigma_D), no K_chi(g,nabla chi)",
            "current_status": "ADMISSIBLE_CONTRACT_NOT_PARENT_DERIVED",
            "failure_mode": "gradient/vector selector stress can survive locally",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CHI1759_1_local_zero",
            "claim": "chi_local=0",
            "mathematical_form": "b_local=0 or c_local=0 => Sigma_local=chi_local=0",
            "current_status": "NOT_PARENT_DERIVED",
            "failure_mode": "local memory activation and selector stress remain finite",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CHI1759_2_partial_X_chi",
            "claim": "partial_X chi_D=0 at local fixed point",
            "mathematical_form": "chi_D is independent of the local X direction or is a fixed topological class on the local branch",
            "current_status": "NOT_PARENT_DERIVED",
            "failure_mode": "even with f(0)=0, f'(0) C_obs partial_X chi_D sources J_chain",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CHI1759_3_topological_projector",
            "claim": "P_MTS,D is metric-independent and parent-owned",
            "mathematical_form": "relative-chain/cohomology projector, not Hodge/metric filter or after-solve readout",
            "current_status": "CONDITIONAL_NOT_PARENT_OWNED",
            "failure_mode": "projector variation can reintroduce stress/source terms",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CHI1759_4_R11_silence",
            "claim": "domain source-normalization operator is zero or executable",
            "mathematical_form": "c_domain_source_normalization_operator=0 or coefficient vector fills all mapped rows",
            "current_status": "FAIL_CURRENT_CORPUS",
            "failure_mode": "domain selector can reintroduce PPN/Newton source-normalization residuals",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
    ]


def achain_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "interface_id": "AC1759_0_zero_condition",
            "quantity": "Z_chain",
            "required_form": "Z_chain=True if f(0)=0 and either f'(0)=0 or partial_X chi_D=0, with parent-owned local chi_D=0",
            "current_status": "FALSE_PARENT_UNSIGNED",
            "formula": "J_chain=0 condition",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1756_HIDDEN_SOURCE_COUNTEREXAMPLE_LEDGER.csv"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "AC1759_1_A_f0",
            "quantity": "A_f0",
            "required_form": "||f(0) delta_X C_obs||_{E*} or theorem-zero from f(0)=0",
            "current_status": "MISSING_F0_ZERO_OR_A_F0",
            "formula": "direct observed-coupling source term",
            "source_path": str(RESIDUALS / "P8_DOUBLE_ZERO_MEMORY_VARIATION_TEST.csv"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "AC1759_2_A_fprime",
            "quantity": "A_fprime",
            "required_form": "||f'(0) C_obs partial_X chi_D||_{E*} or theorem-zero from f'(0)=0/partial_X chi_D=0",
            "current_status": "MISSING_FPRIME_ZERO_OR_CHI_INDEPENDENCE_OR_A_FPRIME",
            "formula": "chain derivative source term",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1756_HIDDEN_SOURCE_FINITE_RESIDUAL_ROWS.csv"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "AC1759_3_A_chain",
            "quantity": "A_chain",
            "required_form": "A_chain <= A_f0 + A_fprime in one declared E* norm",
            "current_status": "MISSING_COMMON_ESTAR_NORM_AND_CHAIN_VALUES",
            "formula": "||J_chain||_{E*} <= A_chain",
            "source_path": "AC1759_1_A_f0; AC1759_2_A_fprime",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "AC1759_4_R_chain",
            "quantity": "R_chain",
            "required_form": "||R_chain|| <= ||P_arena L_X^{-1}|| A_chain with operator/projection norms",
            "current_status": "MISSING_OPERATOR_INVERSE_ARENA_PROJECTION_AND_UNITS",
            "formula": "source residual response to coupling-chain hidden current",
            "source_path": str(RESIDUALS / "P8_Y5_R10_981_COUPLING_PRIOR_CANDIDATES.csv"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def source_zero_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1759_0_chain",
            "quantity": "J_chain",
            "current_status": "NOT_ZEROED",
            "evidence": "double-zero condition is exact but parent origin and chi_D independence/local-zero are unsigned",
            "remaining_gap": "A_chain remains missing/nonclaim",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1759_1_double_zero",
            "quantity": "f(0)=f'(0)=0",
            "current_status": "REQUIREMENT_DERIVED_NOT_PARENT_ORIGIN",
            "evidence": "variation test rejects linear gate and accepts p>=2 as sufficient",
            "remaining_gap": "determinant/norm-square/topological origins and FLRW normalization not derived",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1759_2_source_silence",
            "quantity": "S_cg(D_L=0,Y)",
            "current_status": "NOT_DERIVED",
            "evidence": "affine and coupling-chain hidden sources are nonzero/nonclaim, and matter/worldtube/boundary/history/tower/mu/kernel channels remain",
            "remaining_gap": "J_hidden not zero; matter/worldtube vertex is next derivation target",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1759_0_double_zero",
            "decision": "DOUBLE_ZERO_IS_REQUIRED_AND_SUFFICIENT_AS_CONTRACT",
            "reason": "p>=2 kills direct and chain selector exchange at chi_D=0, while p=1 fails",
            "next_action": "do not use linear selector for local-GR branch",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1759_1_parent_origin",
            "decision": "DOUBLE_ZERO_ORIGIN_NOT_PARENT_DERIVED",
            "reason": "determinant, norm-square/Z2, and topological-pairing origins are clues, not signed parent action derivations",
            "next_action": "retain A_chain unless a parent activation law is derived",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1759_2_selector_independence",
            "decision": "PARTIAL_X_CHID_ZERO_NOT_DERIVED",
            "reason": "chi_D/domain selector remains an invariant-generator debt and local zero is not parent-signed",
            "next_action": "do not claim chain source zero via selector independence",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1759_3_Achain",
            "decision": "A_CHAIN_INTERFACE_WRITTEN_NONCLAIM",
            "reason": "chain zero theorem failed, so A_f0/A_fprime/A_chain must remain explicit residual inputs",
            "next_action": "use A_chain interface only as nonclaim source-envelope plumbing",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1759_4_best_next",
            "decision": "MATTER_WORLDTUBE_VERTEX_IS_NEXT_BEST_DERIVATION_ROUTE",
            "reason": "affine and coupling-chain sources are now ledgered; next hidden source in J_hidden is ordinary matter/worldtube X coupling",
            "next_action": "build 1760 matter-worldtube quotient descent or A_matter bound",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1759_0_double_zero_contract",
            "claim": "f(0)=f'(0)=0 is parent-derived",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_PARENT_ORIGIN_OF_DOUBLE_ZERO",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1759_1_chi_independence",
            "claim": "partial_X chi_D=0 or chi_D local zero is parent-derived",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_SELECTOR_INDEPENDENCE_LOCAL_ZERO_AND_PROJECTOR_OWNER",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1759_2_Achain_zero",
            "claim": "A_chain=0",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_F0_FPRIME_CHI_INDEPENDENCE_NOT_SIGNED",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1759_3_Achain_bound",
            "claim": "A_chain is finite and sourced in a declared E* norm",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_A_F0_A_FPRIME_COMMON_ESTAR_NORM_MISSING",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1759_4_local_GR_Newton",
            "claim": "local GR/Newton/PPN/R10/WEP/clock/orbital branch can claim",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_CHAIN_AND_OTHER_HIDDEN_SOURCE_CHANNELS_ACTIVE",
            "claim_allowed": no(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1759_0_primary",
            "next_target": "1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md",
            "script": "scripts/Y5_R2FR_matter_worldtube_quotient_descent_or_Amatter_bound.py",
            "objective": "try to prove ordinary matter/worldtube terms descend through q and carry no direct X vertex; otherwise carry A_matter",
            "success_condition": "matter/worldtube source is theorem-zero or becomes an explicit finite residual row",
            "selection_status": "selected",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1759_1_fallback",
            "next_target": "1760b-Y5-R2FR-Achain-E-star-bound-runner.md",
            "script": "scripts/Y5_R2FR_Achain_E_star_bound_runner.py",
            "objective": "turn A_f0/A_fprime/A_chain into a runnable nonclaim source-envelope interface with units and operator/projection norms",
            "success_condition": "A_chain rows parse with declared E* units, sources, and valid_for_claim=false until bounds pass",
            "selection_status": "held_fallback",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "coupling_chain_attempt": coupling_chain_attempt_rows(),
        "double_zero_gate": double_zero_gate_rows(),
        "chi_independence": chi_independence_rows(),
        "achain_bound": achain_bound_rows(),
        "source_zero_status": source_zero_status_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1759_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1759_{key.upper()}.csv")


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            for field in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if row.get(field) == "True":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values())
            if "MISSING_" in text:
                for field in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                    if row.get(field) == "True":
                        return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1759_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1759_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1759*"):
        path_text = str(path)
        if "\\.venv\\" in path_text or "\\__pycache__\\" in path_text:
            continue
        if path.is_file():
            return False
    return True


def double_zero_contract_present(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["gate_id"] == "DZ1759_0_power_condition"
        and row["current_status"] == "DERIVED_AS_REQUIREMENT"
        for row in rows_map["double_zero_gate"]
    )


def chain_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "CCS1759_5_verdict"
        and row["proof_status"] == "A_CHAIN_RETAINED"
        for row in rows_map["coupling_chain_attempt"]
    )


def achain_interface_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["achain_bound"]
    return len(rows) >= 5 and all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in rows)


def source_zero_blocked(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["status_id"] == "SZ1759_2_source_silence"
        and row["current_status"] == "NOT_DERIVED"
        for row in rows_map["source_zero_status"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["route_id"] == "NEXT1759_0_primary"
        and row["selection_status"] == "selected"
        for row in rows_map["next_target"]
    )


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    sources = rows_map["source_register"]
    claims = rows_map["claim_gate"]

    validation = [
        check("VAL1759_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1759_1_needles_present", all(row["needles_present"] == "True" for row in sources), "required source needles are present", "one or more source needles missing"),
        check("VAL1759_2_double_zero_contract", double_zero_contract_present(rows_map), "double-zero condition recorded as exact requirement", "double-zero requirement missing"),
        check("VAL1759_3_chain_not_promoted", chain_not_promoted(rows_map), "coupling-chain source remains unpromoted", "coupling-chain verdict missing or promoted"),
        check("VAL1759_4_achain_interface_nonclaim", achain_interface_nonclaim(rows_map), "A_chain interface remains nonclaim", "A_chain interface missing or promoted"),
        check("VAL1759_5_source_zero_blocked", source_zero_blocked(rows_map), "source-zero status remains blocked", "source-zero status missing or promoted"),
        check("VAL1759_6_claim_gates_safe", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claims), "all claim gates remain blocked", "one or more claim gates opened"),
        check("VAL1759_7_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check("VAL1759_8_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check("VAL1759_9_decision_next", any(row["decision_id"] == "DEC1759_4_best_next" and row["decision"] == "MATTER_WORLDTUBE_VERTEX_IS_NEXT_BEST_DERIVATION_ROUTE" for row in rows_map["decision"]), "decision selects matter/worldtube source route", "best-next decision missing"),
        check("VAL1759_10_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check("VAL1759_11_csv_parse", parsed_ok, "all generated 1759 CSVs parse", "one or more generated 1759 CSVs failed to parse"),
        check("VAL1759_12_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1759_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1759_14_formalization_untouched", formalization_untouched(), "no 1759 outputs found under formalization-workbench", "1759 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1759_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1759 coupling-chain source double-zero proof or Achain bound" if overall else "one or more 1759 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1759 attacks the coupling-chain source `J_chain = f'(0) C_obs partial_X chi_D + f(0) delta_X C_obs`.",
        "- The math is crisp: local selector silence requires `f(0)=f'(0)=0`; a linear `f(chi_D)=chi_D` gate fails.",
        "- A quadratic-or-higher gate is sufficient as a contract, but its parent origin is not derived: determinant, norm-square/Z2, and topological-pairing routes remain candidates only.",
        "- The alternative `partial_X chi_D=0` route is also unsigned because `chi_D`/domain selector is still an invariant-generator debt and local `chi_D=0` is not parent-proved.",
        "- Therefore `A_chain` is retained as an explicit nonclaim residual interface.",
        "- No GitHub, public, local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Coupling-Chain Source Attempt",
        markdown_table(rows_map["coupling_chain_attempt"], ["attempt_id", "claim_piece", "mathematical_form", "status", "proof_status", "gap"]),
        "",
        "## Double-Zero Gate Audit",
        markdown_table(rows_map["double_zero_gate"], ["gate_id", "requirement", "mathematical_form", "current_status", "why_needed", "blocker"]),
        "",
        "## Chi-D Independence Audit",
        markdown_table(rows_map["chi_independence"], ["audit_id", "claim", "mathematical_form", "current_status", "failure_mode"]),
        "",
        "## A-chain Bound Interface",
        markdown_table(rows_map["achain_bound"], ["interface_id", "quantity", "required_form", "current_status", "formula"]),
        "",
        "## Source-Zero Status",
        markdown_table(rows_map["source_zero_status"], ["status_id", "quantity", "current_status", "evidence", "remaining_gap"]),
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
        "This checkpoint is a good example of disciplined progress: the double-zero law is not optional anymore; it is the exact condition that prevents selector exchange from leaking back into the local source equation. But it is still not a parent theorem. Since the coupling chain is now ledgered as `A_chain`, the next derivation-first target should be the ordinary matter/worldtube vertex: prove matter descends through `q` with no direct `X` source, or carry `A_matter` explicitly.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1759-Y5-R2FR-coupling-chain-source-double-zero-proof-or-Achain-bound.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1759_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1759 validation FAIL")
    print("1759 validation PASS")


if __name__ == "__main__":
    main()
