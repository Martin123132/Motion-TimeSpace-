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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1816"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1816-Y5-R2FR-variation-before-readout-source-selector-order-or-post-current-cA-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1816_0_1815_doc",
        "source_key": "1815_handoff_doc",
        "source_path": ROOT / "1815-Y5-R2FR-Noether-current-owner-and-no-current-rescale-proof-or-cA-bound-row.md",
        "needles": ["DEC1815_3_best_next", "NEXT1815_0_primary"],
        "role": "1815 selects variation-before-readout/source-selector order as the next theorem target.",
    },
    {
        "source_id": "SRC1816_1_1815_validation",
        "source_key": "1815_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1815_VALIDATION.csv",
        "needles": ["VAL1815_OVERALL", "PASS"],
        "role": "confirms 1815 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1816_2_1815_theorem",
        "source_key": "1815_no_current_rescale",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1815_NO_CURRENT_RESCALE_THEOREM.csv",
        "needles": ["NCR1815_0_target", "READOUT_ORDER_AND_PARENT_CURRENT_OWNER_UNSIGNED"],
        "role": "post-current rescale kill depends on readout order and parent current owner.",
    },
    {
        "source_id": "SRC1816_3_1815_split",
        "source_key": "1815_post_pre_split",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1815_POST_PRE_RESCALE_SPLIT_AUDIT.csv",
        "needles": ["PPR1815_1_post_selector", "KILLED_CONDITIONALLY"],
        "role": "post-selector route is conditionally killed, not claimed.",
    },
    {
        "source_id": "SRC1816_4_1454_theorem",
        "source_key": "1454_readout_order_theorem",
        "source_path": RESIDUALS / "P8_Y5_R10_1454_VARIATION_BEFORE_READOUT_THEOREM_ATTEMPT.csv",
        "needles": ["VBR1454_6_verdict", "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED"],
        "role": "prior readout-order theorem attempt and its exact status.",
    },
    {
        "source_id": "SRC1816_5_1454_audit",
        "source_key": "1454_source_readout_order_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_1454_SOURCE_READOUT_ORDER_AUDIT.csv",
        "needles": ["SOA1454_5_verdict", "FAIL_CURRENT_PROOF"],
        "role": "source/readout order remains unsigned after 1454.",
    },
    {
        "source_id": "SRC1816_6_1453_theorem",
        "source_key": "1453_current_source_owner",
        "source_path": RESIDUALS / "P8_Y5_R10_1453_CURRENT_SOURCE_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv",
        "needles": ["CSO1453_4_post_variation_rescaling", "KILLED_CONDITIONALLY"],
        "role": "post-variation current rescaling is only conditionally illegal.",
    },
    {
        "source_id": "SRC1816_7_1453_matrix",
        "source_key": "1453_rescaling_selector_matrix",
        "source_path": RESIDUALS / "P8_Y5_R10_1453_CURRENT_RESCALING_SELECTOR_MATRIX.csv",
        "needles": ["RSM1453_1_post_selector", "official/source readout order still unsigned"],
        "role": "selector matrix names the official/source readout-order gap.",
    },
    {
        "source_id": "SRC1816_8_1079_premises",
        "source_key": "1079_current_owner_premises",
        "source_path": RESIDUALS / "P8_Y5_R10_1079_CURRENT_OWNER_PREMISE_LEDGER.csv",
        "needles": ["PR1079_1_variation_before_readout", "CONDITIONAL_READOUT_CONTRACT"],
        "role": "variation-before-readout exists as a contract, not a parent-signed theorem.",
    },
    {
        "source_id": "SRC1816_9_1079_counterexamples",
        "source_key": "1079_counterexample_matrix",
        "source_path": RESIDUALS / "P8_Y5_R10_1079_COUNTEREXAMPLE_RESOLUTION_MATRIX.csv",
        "needles": ["CER1079_3_post_variation_selector", "KILLED_CONDITIONALLY"],
        "role": "post-variation selector is conditionally killed when readout order is signed.",
    },
    {
        "source_id": "SRC1816_10_1802_readout_gate",
        "source_key": "1802_matter_readout_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1802_MATTER_READOUT_THEOREM_GATE.csv",
        "needles": ["MRT1802_4_pure_postprocessing", "TYPE_THEOREM_CONDITIONAL"],
        "role": "pure postprocessing readout is safe only as a typed subdomain.",
    },
    {
        "source_id": "SRC1816_11_1802_type_split",
        "source_key": "1802_readout_type_split",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1802_READOUT_TYPE_SPLIT.csv",
        "needles": ["RTS1802_3_effective_action", "NO_REENTRY_FAILS_IF_PREVARIATION"],
        "role": "effective/prevariation readout routes defeat no-reentry unless separately excluded.",
    },
    {
        "source_id": "SRC1816_12_1451_no_slot",
        "source_key": "1451_no_source_only_slot",
        "source_path": RESIDUALS / "P8_Y5_R10_1451_NO_SOURCE_ONLY_SLOT_OPERATOR_GRAMMAR_THEOREM_ATTEMPT.csv",
        "needles": ["OG1451_6_verdict", "FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED"],
        "role": "source-only slots are not yet excluded by parent grammar.",
    },
    {
        "source_id": "SRC1816_13_1451_slot_matrix",
        "source_key": "1451_source_only_slot_matrix",
        "source_path": RESIDUALS / "P8_Y5_R10_1451_SOURCE_ONLY_SLOT_REDUCTION_MATRIX.csv",
        "needles": ["SM1451_0_wA_literal", "UNSIGNED"],
        "role": "literal pre-action weights remain an active countermodel.",
    },
]


OUTPUTS: dict[str, Path] = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1816_SOURCE_REGISTER.csv",
    "variation_before_readout_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1816_VARIATION_BEFORE_READOUT_THEOREM.csv",
    "source_selector_order_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1816_SOURCE_SELECTOR_ORDER_AUDIT.csv",
    "post_current_cA_row_schema": RESIDUALS / "P8_Y5_PARENT_QLOC_1816_POST_CURRENT_CA_ROW_SCHEMA.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1816_COUNTERMODEL_LEDGER.csv",
    "gr_newton_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1816_GR_NEWTON_IMPACT_LEDGER.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1816_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1816_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1816_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1816_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1816_VALIDATION.csv",
}


def ensure_dirs() -> None:
    for path in {RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "yes", "1", "pass", "passed"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    headers = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        text = read_text(path)
        exists = path.exists()
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and not missing,
                "missing_needles": ";".join(missing),
                "role": source["role"],
            }
        )
    return rows


def variation_before_readout_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "VBR1816_0_target",
            "claim": "variation-before-readout/source-selector order kills post-current c_A and F(T_A,A)",
            "mathematical_statement": "If a single parent action first defines J_Q := delta S_matter/delta A_Q^vis or T_H := delta S_matter/delta e_obs, and every material selector, source-worldtube map and arena readout is a downstream map R_post on the solved parent state with no arrow back into S_parent or S_eff, then post-current c_A and post-selector F(T_A,A) cannot redefine the parent source.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "current_corpus_status": "PARENT_READOUT_ORDER_AND_SOURCE_KERNEL_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "VBR1816_1_variation_operator",
            "claim": "functional derivative is taken before readout maps",
            "mathematical_statement": "A functional derivative of S_parent is evaluated on the parent field domain; a later map R_post[Phi_sol] can report an observable but cannot alter delta S_parent/delta field unless R has already entered the action or variation domain.",
            "proof_status": "EXACT_IF_PARENT_DOMAIN_TYPED",
            "current_corpus_status": "PARENT_DOMAIN_TYPING_NOT_GLOBAL",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "VBR1816_2_post_current_cA",
            "claim": "post-current c_A is not a source coupling",
            "mathematical_statement": "J_Q fixed by variation followed by J_eff=c_A R[J_Q] makes c_A a transfer/calibration coefficient, not a coefficient in the parent source equation, unless an object-language source-current slot exists.",
            "proof_status": "KILLED_CONDITIONALLY",
            "current_corpus_status": "NO_SOURCE_SLOT_AND_READOUT_ORDER_NOT_JOINTLY_SIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "VBR1816_3_post_selector_FTA",
            "claim": "post-selector F(T_A,A) cannot alter parent source",
            "mathematical_statement": "A selector applied after parent variation can choose a measured channel but cannot replace the variational Hilbert/Noether source used in the field equation.",
            "proof_status": "KILLED_CONDITIONALLY",
            "current_corpus_status": "OFFICIAL_SOURCE_WORLDTUBE_KERNEL_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "VBR1816_4_preaction_limit",
            "claim": "variation-before-readout kills pre-action weights",
            "mathematical_statement": "If S_matter already contains sum_A w_A S_A or an effective selector before variation, the extracted source inherits w_A; readout order cannot remove what is inside the action.",
            "proof_status": "LIMIT_THEOREM_COUNTERMODEL_SURVIVES",
            "current_corpus_status": "PRE_ACTION_DELTA_W_ROUTE_STILL_LIVE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "VBR1816_5_source_worldtube_limit",
            "claim": "source-worldtube projection is harmless",
            "mathematical_statement": "A source-worldtube or arena kernel K_arena is harmless only if it is fixed downstream postprocessing; if it selects support, normalization, boundary or effective source before variation, it remains a finite transfer residual.",
            "proof_status": "TYPE_SPLIT_NOT_ZERO_PROOF",
            "current_corpus_status": "K_ARENA_SOURCE_TRANSFER_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "VBR1816_6_verdict",
            "claim": "1816 proves post-current c_A/F(T_A,A) zero in the current corpus",
            "mathematical_statement": "VBR1816_0 through VBR1816_5 close only if parent variation order, pure readout typing, no source-only slot, no reentry and source-worldtube kernels are all signed together.",
            "proof_status": "CONDITIONAL_THEOREM_NOT_CURRENT_PROOF",
            "current_corpus_status": "DEMOTE_TO_POST_CURRENT_CA_AND_TRANSFER_ROWS",
            "valid_for_claim": False,
        },
    ]


def source_selector_order_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SSO1816_0_parent_action_domain",
            "needed_clause": "one parent action/domain before projection",
            "source_anchor": "VBR1454_1_variational_identity; SOA1454_0_parent_domain",
            "current_status": "PARTIAL_CONTRACT_NOT_REDUCED",
            "if_missing": "post-selector can be interpreted as a stitched source rule",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SSO1816_1_variation_order",
            "needed_clause": "source/current variation before material/readout projection",
            "source_anchor": "PR1079_1_variation_before_readout; SOA1454_1_variation_order",
            "current_status": "CONDITIONAL_READOUT_CONTRACT",
            "if_missing": "post-current c_A remains a live transfer residual",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SSO1816_2_pure_readout_type",
            "needed_clause": "R_post is absent from S_parent, S_eff and field equations",
            "source_anchor": "MRT1802_4_pure_postprocessing; RTS1802_0_pure_postprocessing",
            "current_status": "PURE_POSTPROCESSING_SAFE_BUT_NOT_GENERAL",
            "if_missing": "readout can reenter as an effective action or projector",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SSO1816_3_source_worldtube_kernel",
            "needed_clause": "source-worldtube and arena kernels are fixed downstream maps",
            "source_anchor": "SOA1454_4_source_worldtube; VBR1816_5_source_worldtube_limit",
            "current_status": "MISSING_ARENA_TRANSFER_KERNEL",
            "if_missing": "K_arena[J_Q]-J_Q must be bounded instead of set to zero",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SSO1816_4_no_effective_reentry",
            "needed_clause": "no S_eff/readout/cutoff term feeds back before variation",
            "source_anchor": "RTS1802_3_effective_action; MRT1802_5_general_readout",
            "current_status": "READOUT_REENTRY_RESIDUAL_ACTIVE",
            "if_missing": "postprocessing theorem cannot be applied to radiative/effective branches",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SSO1816_5_no_source_only_slot",
            "needed_clause": "no c_A, w_A or material/source-only slot exists in the parent grammar",
            "source_anchor": "OG1451_6_verdict; SM1451_0_wA_literal",
            "current_status": "SOURCE_ONLY_SLOT_NOT_EXCLUDED",
            "if_missing": "post-current split can be hidden as a pre-action coupling",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SSO1816_6_verdict",
            "needed_clause": "full source-selector/readout-order theorem",
            "source_anchor": "VBR1816_0 through VBR1816_5",
            "current_status": "FAIL_CURRENT_ZERO_PROOF",
            "if_missing": "retain post-current c_A, selector and transfer rows as nonclaim",
            "valid_for_claim": False,
        },
    ]


def post_current_c_a_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": "PCR1816_0_cA_post",
            "quantity": "epsilon_cA_post_abs",
            "definition": "post-current source/test rescaling coefficient after parent current extraction",
            "formal_expression": "sup_A |c_A-1| or sup_A |D_v ln c_A| after J_Q/T_H is fixed",
            "zero_condition": "parent variation-before-readout plus no source-current coefficient slot",
            "required_inputs": "arena; species_or_source_id; c_A_or_zero_theorem; current_norm; units; source_path",
            "current_status": "MISSING_READOUT_ORDER_THEOREM_OR_C_A_VALUE",
            "units": "dimensionless_current_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_C_A_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "PCR1816_1_selector_FTA",
            "quantity": "epsilon_selector_FTA_abs",
            "definition": "post-variation material/source selector transfer residual",
            "formal_expression": "||F(T_A,A)-T_H||/||T_H|| after parent source extraction",
            "zero_condition": "F is strictly downstream readout and cannot enter S_parent or S_eff",
            "required_inputs": "selector_definition; source_tensor; arena; units; source_path",
            "current_status": "MISSING_SELECTOR_ORDER_THEOREM_OR_BOUND",
            "units": "dimensionless_source_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_SELECTOR_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "PCR1816_2_worldtube_transfer",
            "quantity": "epsilon_K_arena_transfer_abs",
            "definition": "source-worldtube/arena transfer from parent current/source to effective test source",
            "formal_expression": "||K_arena[J_Q]-J_Q||/||J_Q|| or ||K_arena[T_H]-T_H||/||T_H||",
            "zero_condition": "K_arena is a fixed post-solution reporting map with no support, boundary or normalization feedback",
            "required_inputs": "arena; K_arena; worldtube_definition; source_norm; units; source_path",
            "current_status": "MISSING_SOURCE_WORLDTUBE_TRANSFER_KERNEL",
            "units": "dimensionless_transfer_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_TRANSFER_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "PCR1816_3_effective_action_reentry",
            "quantity": "epsilon_Seff_reentry_abs",
            "definition": "effective/radiative/readout action feedback that enters before variation",
            "formal_expression": "||delta S_eff_readout/delta field||/||delta S_parent/delta field||",
            "zero_condition": "no readout, cutoff, calibration or radiative term enters the action domain before variation",
            "required_inputs": "effective_action_channel; variation_domain; source_norm; units; source_path",
            "current_status": "MISSING_NO_REENTRY_THEOREM_OR_BOUND",
            "units": "dimensionless_variation_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_REENTRY_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "PCR1816_4_total",
            "quantity": "epsilon_post_current_order_total_abs",
            "definition": "total no-cancellation envelope for post-current/readout-order uncertainty",
            "formal_expression": "abs(PCR1816_0)+abs(PCR1816_1)+abs(PCR1816_2)+abs(PCR1816_3)",
            "zero_condition": "all post-current c_A, selector, worldtube and reentry channels theorem-zero or source-backed",
            "required_inputs": "all PCR1816 components; common normalizers; units; source paths; arena projections",
            "current_status": "MISSING_COMPONENT_VALUES_AND_COMMON_NORMALIZER",
            "units": "absolute_no_cancellation_envelope",
            "source_path": "",
            "common_normalizer": "MISSING_TOTAL_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1816_0_pre_action_selector",
            "countermodel": "S_matter=sum_A w_A S_A or F_A S_A before variation",
            "why_it_defeats_claim": "variation-before-readout cannot remove a selector already inside the action",
            "blocked_by": "no-source-only-slot and action-scale connectedness theorem",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1816_1_unsigned_readout_order",
            "countermodel": "J_A -> c_A J_A between source extraction and empirical arena readout",
            "why_it_defeats_claim": "without a parent-signed order, c_A can be interpreted as source transfer rather than harmless calibration",
            "blocked_by": "variation-before-readout/source-selector order theorem",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1816_2_worldtube_transfer",
            "countermodel": "source-worldtube kernel K_arena changes support or normalization",
            "why_it_defeats_claim": "arena projection can become an effective source map unless fixed downstream",
            "blocked_by": "source-worldtube transfer kernel theorem or source-backed bound",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1816_3_effective_action_reentry",
            "countermodel": "readout/cutoff/radiative S_eff enters before variation",
            "why_it_defeats_claim": "then the readout object is no longer pure postprocessing",
            "blocked_by": "no-reentry theorem or finite reentry coefficient",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1816_4_nonhilbert_boundary_tail",
            "countermodel": "boundary/torsion/spin current bypasses Hilbert/Noether source",
            "why_it_defeats_claim": "readout order does not exclude non-Hilbert source channels by itself",
            "blocked_by": "non-Hilbert silence theorem or source-backed zeta row",
            "retained": True,
            "valid_for_claim": False,
        },
    ]


def gr_newton_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1816_0_post_current",
            "if_closed": "variation-before-readout/source-selector order is parent-signed",
            "would_buy": "post-current c_A and post-selector F(T_A,A) become readout/calibration rather than source couplings",
            "still_missing": "pre-action Delta_w, no-source-slot, non-Hilbert currents, source-worldtube transfer and local EH/Poisson gates",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1816_1_source_transfer",
            "if_closed": "K_arena/source-worldtube is fixed downstream or bounded",
            "would_buy": "WEP/R10/clock/orbital source-test comparisons stop being vulnerable to hidden readout normalization",
            "still_missing": "real arena kernels, units, source paths and no-cancellation normalizers",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1816_2_local_GR",
            "if_closed": "all post-current order residuals vanish",
            "would_buy": "one clean family of source coupling ambiguity is removed from the local GR reduction path",
            "still_missing": "action-scale connectedness, measured-G absorption, EH/PPN/boundary/qDq and empirical local bounds",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1816_3_verdict",
            "if_closed": "1816 alone closes the local-GR source side",
            "would_buy": "nothing claimable alone; it is a subgate, not the full reduction",
            "still_missing": "the current corpus does not parent-sign the order theorem or source-worldtube transfer",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1816_0_theorem_contract",
            "gate": "variation-before-readout theorem written",
            "current_status": "PASS_CONTRACT_ONLY",
            "reason": "VBR1816 writes the exact conditional theorem and its failure modes",
            "gate_pass": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1816_1_order_parent_signed",
            "gate": "readout/source-selector order parent-signed",
            "current_status": "BLOCKED",
            "reason": "parent action/domain typing, no-source-slot and no-reentry are not jointly signed",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1816_2_worldtube_kernel",
            "gate": "source-worldtube transfer kernel derived or bounded",
            "current_status": "BLOCKED",
            "reason": "K_arena/source-worldtube map is still missing for local arenas",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1816_3_residual_values",
            "gate": "post-current c_A/transfer residual rows source-backed",
            "current_status": "BLOCKED",
            "reason": "PCR1816 rows have missing component values, source paths and common normalizers",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1816_4_local_promotion",
            "gate": "WEP/R10/PPN/local-GR promotion allowed",
            "current_status": "REFUSED",
            "reason": "1816 is a readout-order subgate and cannot claim GR/Newton or local tests",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1816_0_post_current_cA_zero",
            "claim": "post-current c_A is theorem-zero",
            "status": "BLOCKED",
            "reason": "readout-order/no-source-slot/source-worldtube clauses are unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1816_1_selector_source_zero",
            "claim": "post-selector F(T_A,A) cannot act as a source",
            "status": "BLOCKED",
            "reason": "pure postprocessing typing is conditional and not global to all arenas",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1816_2_alpha_WEP_R10",
            "claim": "alpha/source WEP/R10 branches pass",
            "status": "BLOCKED",
            "reason": "post-current transfer rows are missing and nonclaim",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1816_3_local_GR_Newton",
            "claim": "local GR/Newton/PPN follows",
            "status": "REFUSED",
            "reason": "readout-order progress is not the EH/Poisson/PPN reduction",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1816_0_theorem_result",
            "decision": "EXACT_CONDITIONAL_ORDER_THEOREM_ONLY",
            "reason": "post-current c_A/F(T_A,A) are impossible as parent source terms only after source/readout order and no-reentry are signed",
            "next_action": "keep theorem as contract-only and do not promote local claims",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1816_1_residual_status",
            "decision": "POST_CURRENT_CA_AND_TRANSFER_ROWS_NONCLAIM",
            "reason": "source-worldtube transfer, selector and effective-action reentry remain missing",
            "next_action": "treat PCR1816 rows as explicit nonclaim acquisition targets",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1816_2_pre_action_status",
            "decision": "PRE_ACTION_DELTA_W_ROUTE_UNTOUCHED",
            "reason": "variation-before-readout cannot kill weights already inside S_matter",
            "next_action": "keep action-scale connectedness/Delta_w as a parallel branch after the post-current transfer row",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1816_3_best_next",
            "decision": "SOURCE_WORLDTUBE_TRANSFER_KERNEL_NEXT",
            "reason": "the least diffuse next missing object is K_arena/source-worldtube transfer; it either proves downstream silence or becomes a finite c_A/transfer bound row",
            "next_action": "1817-Y5-R2FR-source-worldtube-transfer-kernel-or-post-current-cA-bound-row.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1816_0_primary",
            "next_target": "1817-Y5-R2FR-source-worldtube-transfer-kernel-or-post-current-cA-bound-row.md",
            "script": "scripts/Y5_R2FR_source_worldtube_transfer_kernel_or_post_current_cA_bound_row.py",
            "objective": "derive the source-worldtube/arena transfer kernel as pure downstream readout; if not, emit source-backed post-current c_A/K_arena transfer rows",
            "selection_status": "selected",
            "success_condition": "K_arena transfer theorem-zero, or PCR1816-style rows become source-backed and remain nonclaim until acceptance gates pass",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1816_1_parallel",
            "next_target": "1817b-Y5-R2FR-action-scale-connected-matter-owner-or-Delta-w-bound-row.md",
            "script": "scripts/Y5_R2FR_action_scale_connected_matter_owner_or_Delta_w_bound_row.py",
            "objective": "attack the surviving pre-action Delta_w route by action-scale connectedness after the post-current transfer branch is sharpened",
            "selection_status": "held_parallel",
            "success_condition": "Delta_w theorem-zero or finite source-backed Delta_w row",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "variation_before_readout_theorem": variation_before_readout_rows(),
        "source_selector_order_audit": source_selector_order_rows(),
        "post_current_cA_row_schema": post_current_c_a_rows(),
        "countermodel_ledger": countermodel_rows(),
        "gr_newton_impact": gr_newton_impact_rows(),
        "acceptance_gate": acceptance_gate_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def copy_outputs() -> None:
    for output in generated_csvs():
        for target_dir in (MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE):
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(output, target_dir / output.name)


def branch_copies_exist() -> bool:
    for output in generated_csvs():
        for target_dir in (MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE):
            if not (target_dir / output.name).exists():
                return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    names = {DOC_PATH.name, OUTPUTS["validation"].name} | {path.name for path in generated_csvs()}
    return not any(path.name in names for path in FORMALIZATION.rglob("*") if path.is_file())


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    allowed_gate_pass = {"AC1816_0_theorem_contract"}
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            for field in ("valid_for_claim", "claim_allowed_now", "claim_allowed", "score_ready", "gate_pass"):
                if field in row and boolish(row[field]):
                    if field == "gate_pass" and row.get("gate_id") in allowed_gate_pass:
                        continue
                    return False
    return True


def missing_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            text = " ".join(str(value) for value in row.values())
            if "MISSING_" in text and (
                boolish(row.get("score_ready", False))
                or boolish(row.get("valid_for_claim", False))
                or boolish(row.get("claim_allowed", False))
                or boolish(row.get("claim_allowed_now", False))
                or (boolish(row.get("gate_pass", False)) and row.get("gate_id") != "AC1816_0_theorem_contract")
            ):
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    exists_ok = all(boolish(row["exists"]) for row in source_rows)
    needles_ok = all(boolish(row["needles_present"]) for row in source_rows)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1816_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1816_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1816_2_theorem_contract_written",
            any(row["theorem_id"] == "VBR1816_0_target" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in rows_map["variation_before_readout_theorem"]),
            "variation-before-readout theorem is written as exact conditional",
        ),
        (
            "VAL1816_3_post_current_conditionally_killed",
            any(row["theorem_id"] == "VBR1816_2_post_current_cA" and row["proof_status"] == "KILLED_CONDITIONALLY" for row in rows_map["variation_before_readout_theorem"])
            and any(row["theorem_id"] == "VBR1816_3_post_selector_FTA" and row["proof_status"] == "KILLED_CONDITIONALLY" for row in rows_map["variation_before_readout_theorem"]),
            "post-current c_A and post-selector F(T_A,A) are conditionally killed only",
        ),
        (
            "VAL1816_4_preaction_limit_retained",
            any(row["theorem_id"] == "VBR1816_4_preaction_limit" and row["proof_status"] == "LIMIT_THEOREM_COUNTERMODEL_SURVIVES" for row in rows_map["variation_before_readout_theorem"]),
            "pre-action weights remain outside the theorem",
        ),
        (
            "VAL1816_5_theorem_not_promoted",
            any(row["theorem_id"] == "VBR1816_6_verdict" and row["proof_status"] == "CONDITIONAL_THEOREM_NOT_CURRENT_PROOF" for row in rows_map["variation_before_readout_theorem"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["variation_before_readout_theorem"]),
            "1816 theorem is not promoted as current proof",
        ),
        (
            "VAL1816_6_order_audit_blocked",
            any(row["audit_id"] == "SSO1816_6_verdict" and row["current_status"] == "FAIL_CURRENT_ZERO_PROOF" for row in rows_map["source_selector_order_audit"]),
            "source-selector/readout-order audit remains blocked",
        ),
        (
            "VAL1816_7_residual_rows_nonclaim",
            any(row["residual_id"] == "PCR1816_4_total" for row in rows_map["post_current_cA_row_schema"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["post_current_cA_row_schema"]),
            "post-current c_A/transfer rows are schema-only and nonclaim",
        ),
        (
            "VAL1816_8_countermodels_retained",
            all(boolish(row["retained"]) and not boolish(row["valid_for_claim"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain retained",
        ),
        (
            "VAL1816_9_gr_newton_nonclaim",
            all(not boolish(row["claim_allowed_now"]) and not boolish(row["valid_for_claim"]) for row in rows_map["gr_newton_impact"]),
            "GR/Newton impact rows remain nonclaim",
        ),
        (
            "VAL1816_10_acceptance_blocks",
            any(row["gate_id"] == "AC1816_0_theorem_contract" and boolish(row["gate_pass"]) and not boolish(row["claim_allowed"]) for row in rows_map["acceptance_gate"])
            and all(not boolish(row["claim_allowed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["acceptance_gate"]),
            "acceptance gate permits contract-only progress and blocks claims",
        ),
        (
            "VAL1816_11_claim_gates_blocked",
            all(row["status"] in {"BLOCKED", "REFUSED"} and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "all readout/source/local claim gates remain blocked or refused",
        ),
        ("VAL1816_12_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1816_13_missing_not_ready", missing_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1816_14_decision_next",
            any(row["decision_id"] == "DEC1816_3_best_next" and row["decision"] == "SOURCE_WORLDTUBE_TRANSFER_KERNEL_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects source-worldtube transfer kernel next",
        ),
        (
            "VAL1816_15_next_selected",
            any(row["route_id"] == "NEXT1816_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1816_16_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1816 CSVs parse"),
        ("VAL1816_17_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1816_18_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1816_19_formalization_untouched", formalization_untouched(), "no 1816 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1816_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1816 variation-before-readout source-selector order or post-current cA row checkpoint",
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1816 Y5 R2FR variation-before-readout source-selector order or post-current cA row",
            "",
            "**Progress:** 1816 gives the clean theorem shape: once the parent action has already varied to define `J_Q`/`T_H`, a later `c_A` or `F(T_A,A)` cannot be a parent source coupling. It is only a readout/transfer object unless it was smuggled into the action before variation.",
            "",
            "**Current verdict:** exact conditional theorem, not current proof. The corpus still lacks a parent-signed readout/source-selector order, a source-worldtube transfer kernel, no effective-action reentry, and a no-source-only-slot grammar theorem.",
            "",
            "**Claim ceiling:** no `c_A=0`, no `F(T_A,A)=0`, no WEP/R10/clock/orbital pass, no PPN/local-GR/Newton pass, no GitHub action, and no `formalization-workbench` edit is allowed from 1816.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Variation Before Readout Theorem",
            markdown_table(rows_map["variation_before_readout_theorem"], ["theorem_id", "claim", "mathematical_statement", "proof_status", "current_corpus_status", "valid_for_claim"]),
            "",
            "## Source Selector Order Audit",
            markdown_table(rows_map["source_selector_order_audit"], ["audit_id", "needed_clause", "source_anchor", "current_status", "if_missing", "valid_for_claim"]),
            "",
            "## Post Current cA Row Schema",
            markdown_table(rows_map["post_current_cA_row_schema"], ["residual_id", "quantity", "definition", "formal_expression", "zero_condition", "current_status", "units", "common_normalizer", "score_ready", "valid_for_claim"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel_ledger"], ["countermodel_id", "countermodel", "why_it_defeats_claim", "blocked_by", "retained", "valid_for_claim"]),
            "",
            "## GR Newton Impact Ledger",
            markdown_table(rows_map["gr_newton_impact"], ["impact_id", "if_closed", "would_buy", "still_missing", "claim_allowed_now", "valid_for_claim"]),
            "",
            "## Acceptance Gate",
            markdown_table(rows_map["acceptance_gate"], ["gate_id", "gate", "current_status", "reason", "gate_pass", "claim_allowed", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason", "gate_pass", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is another tightening, not a celebration lap. The post-current trick is now boxed in: if the source/readout order is parent-signed, it dies. But the theorem cannot touch pre-action weights or an arena kernel that feeds support/normalization back into the source. The best next attack is therefore the source-worldtube transfer kernel: prove it is pure downstream readout, or turn it into a finite nonclaim `c_A/K_arena` row.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1816 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
