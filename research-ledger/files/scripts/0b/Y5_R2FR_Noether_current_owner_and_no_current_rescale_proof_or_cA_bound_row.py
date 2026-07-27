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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1815"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1815-Y5-R2FR-Noether-current-owner-and-no-current-rescale-proof-or-cA-bound-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1815_0_1814_doc",
        "source_key": "1814_handoff_doc",
        "source_path": ROOT / "1814-Y5-R2FR-visible-gauge-connection-current-owner-or-DvA-DJ-alpha-residual-row.md",
        "needles": ["DEC1814_3_best_next", "NEXT1814_0_primary"],
        "role": "1814 selects Noether current owner/no-rescale as the next target.",
    },
    {
        "source_id": "SRC1815_1_1814_validation",
        "source_key": "1814_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1814_VALIDATION.csv",
        "needles": ["VAL1814_OVERALL", "PASS"],
        "role": "confirms 1814 connection/current checkpoint passed as nonclaim.",
    },
    {
        "source_id": "SRC1815_2_1814_theorem",
        "source_key": "1814_connection_current_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1814_VISIBLE_CONNECTION_CURRENT_OWNER_THEOREM.csv",
        "needles": ["VCC1814_3_rescaling_exclusion", "current rescaling is forbidden"],
        "role": "latest no-current-rescale theorem contract.",
    },
    {
        "source_id": "SRC1815_3_1814_current_audit",
        "source_key": "1814_current_owner_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1814_CURRENT_OWNER_AUDIT.csv",
        "needles": ["COA1814_2_no_current_rescale", "COUNTEREXAMPLE_SURVIVES"],
        "role": "current rescaling still survives after 1814.",
    },
    {
        "source_id": "SRC1815_4_1814_residual",
        "source_key": "1814_DvA_DJ_residual_schema",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1814_DVA_DJ_ALPHA_RESIDUAL_ROW_SCHEMA.csv",
        "needles": ["DJ1814_2_current_rescale", "MISSING_NO_CURRENT_RESCALE_THEOREM_OR_C_A_BOUND"],
        "role": "c_A residual fallback row from 1814.",
    },
    {
        "source_id": "SRC1815_5_1453_theorem",
        "source_key": "1453_current_source_owner",
        "source_path": RESIDUALS / "P8_Y5_R10_1453_CURRENT_SOURCE_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv",
        "needles": ["CSO1453_4_post_variation_rescaling", "KILLED_CONDITIONALLY"],
        "role": "post-variation current rescaling is conditionally killed.",
    },
    {
        "source_id": "SRC1815_6_1453_pre_weight",
        "source_key": "1453_pre_variation_limit",
        "source_path": RESIDUALS / "P8_Y5_R10_1453_CURRENT_SOURCE_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv",
        "needles": ["CSO1453_5_pre_variation_weight", "SURVIVES_PRE_VARIATION"],
        "role": "pre-variation weights survive current-owner proof.",
    },
    {
        "source_id": "SRC1815_7_1453_matrix",
        "source_key": "1453_rescaling_selector_matrix",
        "source_path": RESIDUALS / "P8_Y5_R10_1453_CURRENT_RESCALING_SELECTOR_MATRIX.csv",
        "needles": ["RSM1453_0_post_current_rescale", "RSM1453_2_pre_action_weight"],
        "role": "selector matrix distinguishes killed post-rescale from surviving pre-action weights.",
    },
    {
        "source_id": "SRC1815_8_1453_validation",
        "source_key": "1453_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1453_VALIDATION.csv",
        "needles": ["VAL1453_3_post_killed_conditional", "VAL1453_4_pre_survives"],
        "role": "1453 validation confirms the post/pre distinction.",
    },
    {
        "source_id": "SRC1815_9_1079_theorem",
        "source_key": "1079_narrow_current_owner",
        "source_path": RESIDUALS / "P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv",
        "needles": ["NCO1079_4_current_rescaling", "NCO1079_5_species_action_weight"],
        "role": "narrow current-owner proof and its pre-weight limitation.",
    },
    {
        "source_id": "SRC1815_10_1079_premises",
        "source_key": "1079_current_owner_premises",
        "source_path": RESIDUALS / "P8_Y5_R10_1079_CURRENT_OWNER_PREMISE_LEDGER.csv",
        "needles": ["PR1079_3_no_later_current_rescale", "PR1079_4_no_pre_action_species_weight"],
        "role": "premise ledger for later rescaling and pre-action species weights.",
    },
    {
        "source_id": "SRC1815_11_1079_counterexamples",
        "source_key": "1079_counterexample_matrix",
        "source_path": RESIDUALS / "P8_Y5_R10_1079_COUNTEREXAMPLE_RESOLUTION_MATRIX.csv",
        "needles": ["CER1079_0_species_action_weight", "CER1079_1_current_rescaling"],
        "role": "current rescale killed conditionally; species action weight survives.",
    },
    {
        "source_id": "SRC1815_12_1230_action_scale",
        "source_key": "1230_action_scale_owner",
        "source_path": RESIDUALS / "P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv",
        "needles": ["UAS1230_1_connected_naturality_lemma", "UAS1230_5_verdict"],
        "role": "connected naturality theorem for pre-action weights.",
    },
    {
        "source_id": "SRC1815_13_1230_failures",
        "source_key": "1230_owner_failure_modes",
        "source_path": RESIDUALS / "P8_Y5_R10_1230_OWNER_FAILURE_MODE_LEDGER.csv",
        "needles": ["FAIL1230_0_disconnected_category", "FAIL1230_4_readout_reentry"],
        "role": "failure modes that keep Delta_w alive.",
    },
    {
        "source_id": "SRC1815_14_1230_delta_w",
        "source_key": "1230_finite_Delta_w_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_1230_FINITE_DELTA_W_PRIOR_CONTRACT.csv",
        "needles": ["FDW1230_0_Delta_w_TiPt", "MISSING_NUMERIC_PRIOR_WIDTH"],
        "role": "finite Delta_w fallback if action-scale/naturality fails.",
    },
    {
        "source_id": "SRC1815_15_1594_action_weight",
        "source_key": "1594_action_weight_exclusion",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1594_ACTION_WEIGHT_EXCLUSION_THEOREM_ATTEMPT.csv",
        "needles": ["AWT1594_4_current_owner_limit", "AWT1594_5_naturality_limit"],
        "role": "1594 separates current-owner limit from naturality limit.",
    },
    {
        "source_id": "SRC1815_16_1594_decision",
        "source_key": "1594_decision",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1594_DECISION.csv",
        "needles": ["DEC1594_0_theorem_status", "ACTION_WEIGHT_EXCLUSION_NOT_DERIVED"],
        "role": "1594 says current owner kills post-variation tricks only, not pre-variation w_A.",
    },
    {
        "source_id": "SRC1815_17_1594_queue",
        "source_key": "1594_acquisition_queue",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1594_BETA_SOURCE_ACQUISITION_QUEUE.csv",
        "needles": ["BSQ1594_2_Delta_w_A", "highest"],
        "role": "Delta_w remains highest-priority source-normalization acquisition if theorem fails.",
    },
    {
        "source_id": "SRC1815_18_1414_current_owner",
        "source_key": "1414_beta_source_alpha_owner",
        "source_path": RESIDUALS / "P8_Y5_R10_1414_BETA_SOURCE_ALPHA_OWNER_ATTEMPT.csv",
        "needles": ["BSA1414_4_no_current_rescaling", "COUNTEREXAMPLE_SURVIVES"],
        "role": "source-alpha current owner still has surviving current/source rescaling counterexample.",
    },
    {
        "source_id": "SRC1815_19_1480_current_label",
        "source_key": "1480_current_label_obstruction",
        "source_path": RESIDUALS / "P8_Y5_R10_1480_HOM_OBSTRUCTION_LEDGER.csv",
        "needles": ["HOB1480_3_current_label", "CURRENT_OWNER_UNSIGNED"],
        "role": "current/source-normalization labels are still unsigned.",
    },
]


OUTPUTS: dict[str, Path] = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1815_SOURCE_REGISTER.csv",
    "no_current_rescale_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1815_NO_CURRENT_RESCALE_THEOREM.csv",
    "post_pre_rescale_split": RESIDUALS / "P8_Y5_PARENT_QLOC_1815_POST_PRE_RESCALE_SPLIT_AUDIT.csv",
    "naturality_action_weight_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1815_NATURALITY_ACTION_WEIGHT_GATE.csv",
    "cA_bound_row_schema": RESIDUALS / "P8_Y5_PARENT_QLOC_1815_C_A_BOUND_ROW_SCHEMA.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1815_COUNTERMODEL_LEDGER.csv",
    "gr_newton_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1815_GR_NEWTON_IMPACT_LEDGER.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1815_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1815_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1815_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1815_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1815_VALIDATION.csv",
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


def no_current_rescale_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NCR1815_0_target",
            "claim": "same Noether current owner bans post-variation current rescaling",
            "mathematical_statement": "If one parent matter action is varied before readout, J_Q=delta S_matter/delta A_Q^vis is the same Noether/Ward current that supplies source/test charge, and source/readout maps are downstream postprocessing, then a later J_A -> c_A J_A is not a parent source term and cannot alter the variational source.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "current_corpus_status": "READOUT_ORDER_AND_PARENT_CURRENT_OWNER_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NCR1815_1_post_variation_cA",
            "claim": "post-variation c_A is demoted to readout/calibration",
            "mathematical_statement": "After the parent source current is fixed by action variation, c_A can only be an arena/readout transfer coefficient unless the parent object-language contains a source-current coefficient slot.",
            "proof_status": "CONDITIONAL_SUBTHEOREM",
            "current_corpus_status": "SOURCE_READOUT_ORDER_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NCR1815_2_pre_variation_weight",
            "claim": "pre-variation w_A is not killed by current ownership",
            "mathematical_statement": "If S_matter already contains sum_A w_A S_A before variation, the Hilbert/Noether current inherits w_A; current ownership alone cannot distinguish this from a true action-scale or matter-category problem.",
            "proof_status": "LIMIT_THEOREM",
            "current_corpus_status": "PRE_ACTION_WEIGHT_SURVIVES",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NCR1815_3_connected_naturality",
            "claim": "connected matter-action naturality could kill relative w_A",
            "mathematical_statement": "A natural positive automorphism of the ordinary matter action-density functor is common inside a connected matter category, so w_A=w_* and only a measured-G common mode remains.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "current_corpus_status": "CONNECTED_MATTER_CATEGORY_AND_ACTION_SCALE_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NCR1815_4_verdict",
            "claim": "1815 proves no-current-rescale in the current corpus",
            "mathematical_statement": "NCR1815_0 through NCR1815_3 close together with no readout reentry, no source-only scalar, no disconnected components and no non-Hilbert bypass",
            "proof_status": "NO_CURRENT_RESCALE_CONTRACT_NOT_CURRENT_PROOF",
            "current_corpus_status": "DEMOTE_TO_C_A_AND_DELTA_W_BOUND_ROWS",
            "valid_for_claim": False,
        },
    ]


def post_pre_rescale_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "split_id": "PPR1815_0_post_current_rescale",
            "loophole": "J_A -> c_A J_A after source extraction",
            "status": "KILLED_CONDITIONALLY",
            "reason": "Hilbert/Noether source is already fixed by parent variation if readout is downstream",
            "missing_for_claim": "variation-before-readout/source-readout order theorem plus parent current owner",
            "finite_row_if_open": "c_A post-variation transfer coefficient",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "split_id": "PPR1815_1_post_selector",
            "loophole": "F(T_A,A) after variation",
            "status": "KILLED_CONDITIONALLY",
            "reason": "postprocessing cannot retroactively redefine the variational parent source if readout order is signed",
            "missing_for_claim": "official readout/order kernel or parent type theorem",
            "finite_row_if_open": "K_arena[J_Q]-J_Q transfer row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "split_id": "PPR1815_2_pre_action_weight",
            "loophole": "S_matter=sum_A w_A S_A before variation",
            "status": "SURVIVES_CURRENT_OWNER",
            "reason": "variation inherits w_A and no post-variation theorem can remove it",
            "missing_for_claim": "action-scale owner, connected matter category, species-blind measure/current/readout descent",
            "finite_row_if_open": "Delta_w_A and beta_w rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "split_id": "PPR1815_3_disconnected_components",
            "loophole": "independent constants on disconnected ordinary matter components",
            "status": "SURVIVES_NATURALITY_UNLESS_CONNECTED",
            "reason": "naturality only forces common weights along actual parent morphisms",
            "missing_for_claim": "parent matter-category connectedness or finite material/source tensor",
            "finite_row_if_open": "component-wise Delta_w rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "split_id": "PPR1815_4_nonHilbert_bypass",
            "loophole": "J_src=kappa T_Hilbert+sum_A zeta_A J_NH,A",
            "status": "PARALLEL_GATE_OPEN",
            "reason": "non-Hilbert currents are not just current rescalings",
            "missing_for_claim": "non-Hilbert current theorem-zero or source-backed zeta_A bound",
            "finite_row_if_open": "zeta_A non-Hilbert current row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "split_id": "PPR1815_5_verdict",
            "loophole": "all current/source normalization rescaling routes",
            "status": "POST_VARIATION_ONLY_CONDITIONALLY_KILLED_PRE_VARIATION_STILL_LIVE",
            "reason": "1815 narrows the coupling debt rather than erasing it",
            "missing_for_claim": "readout order plus action-scale/connectedness plus non-Hilbert silence",
            "finite_row_if_open": "c_A, Delta_w_A, beta_w, zeta_A and transfer rows",
            "valid_for_claim": False,
        },
    ]


def naturality_action_weight_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "NAW1815_0_action_density_line",
            "required_clause": "ordinary matter actions are sections of one parent action-density line",
            "current_status": "NOT_PARENT_SIGNED",
            "would_close": "removes independent action-scale automorphisms by object language",
            "source_anchor": "UAS1230_0_target; CMT1452_0_target",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "NAW1815_1_connected_category",
            "required_clause": "ordinary matter category is connected by parent morphisms relevant to action density",
            "current_status": "CONNECTEDNESS_NOT_DERIVED",
            "would_close": "naturality forces w_A=w_* across ordinary matter sectors",
            "source_anchor": "UAS1230_1_connected_naturality_lemma; FAIL1230_0_disconnected_category",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "NAW1815_2_species_blind_measure",
            "required_clause": "path/statistical measure and Jacobian are species-blind",
            "current_status": "MEASURE_DESCENT_UNSIGNED",
            "would_close": "blocks J_A measure-induced source weights",
            "source_anchor": "UAS1230_3_measure_owner_extension; CMC1594_1_species_blind_measure",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "NAW1815_3_common_absorption_guard",
            "required_clause": "any common w_* is constant, universal, range-independent and derivative-silent before measured-G absorption",
            "current_status": "MEASURED_G_GUARD_ACTIVE",
            "would_close": "prevents hiding source physics inside calibration",
            "source_anchor": "THM1063_4_measured_G_absorption; CMC1594_6_common_G_absorption",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "NAW1815_4_verdict",
            "required_clause": "all action-scale/naturality clauses close",
            "current_status": "ACTION_WEIGHT_EXCLUSION_NOT_DERIVED",
            "would_close": "would demote Delta_w_A to zero theorem",
            "source_anchor": "UAS1230_5_verdict; DEC1594_0_theorem_status",
            "valid_for_claim": False,
        },
    ]


def c_a_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": "CAB1815_0_cA_post",
            "quantity": "epsilon_cA_post_abs",
            "definition": "post-variation current/source-test rescaling coefficient",
            "formal_expression": "sup_A |c_A-1| or sup_A |D_v ln c_A| after parent current extraction",
            "zero_condition": "variation-before-readout and no source-current coefficient slot theorem",
            "required_inputs": "species_or_source_id; c_A_or_zero_theorem; readout_order_status; arena; units; source_path",
            "current_status": "MISSING_READOUT_ORDER_THEOREM_OR_C_A_BOUND",
            "units": "dimensionless_current_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_C_A_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "CAB1815_1_Delta_w_pre",
            "quantity": "epsilon_Delta_w_pre_abs",
            "definition": "pre-variation relative action/source weight",
            "formal_expression": "sup_AB |w_A-w_B|/|w_*|",
            "zero_condition": "connected matter-action naturality plus species-blind measure/current/readout descent",
            "required_inputs": "material_pair_or_sector; Delta_w_or_zero_theorem; action_scale_owner; units; source_path",
            "current_status": "MISSING_ACTION_SCALE_THEOREM_OR_DELTA_W_BOUND",
            "units": "dimensionless_action_weight_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_DELTA_W_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "CAB1815_2_readout_transfer",
            "quantity": "epsilon_current_transfer_abs",
            "definition": "post-variation arena/source-worldtube transfer from parent J_Q to effective source/test current",
            "formal_expression": "||K_arena[J_Q]-J_Q||/||J_Q||",
            "zero_condition": "source/test readout is typed as downstream postprocessing and cannot change source current",
            "required_inputs": "arena; transfer_kernel_or_zero_theorem; source_worldtube; units; source_path",
            "current_status": "MISSING_SOURCE_TEST_TRANSFER_OR_VALUE",
            "units": "dimensionless_transfer_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_TRANSFER_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "CAB1815_3_zeta_nonhilbert",
            "quantity": "epsilon_zeta_nonhilbert_abs",
            "definition": "non-Hilbert source current bypass",
            "formal_expression": "sup_A |zeta_A J_NH,A|/||T_H||",
            "zero_condition": "non-Hilbert currents vanish, are exact/projected-silent, or are source-backed finite tails",
            "required_inputs": "nonHilbert_channel; zeta_A_or_zero_theorem; projection; units; source_path",
            "current_status": "MISSING_NONHILBERT_SILENCE_OR_BOUND",
            "units": "dimensionless_source_current_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_NONHILBERT_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "CAB1815_4_total",
            "quantity": "epsilon_no_current_rescale_total_abs",
            "definition": "total no-cancellation source/current normalization envelope",
            "formal_expression": "abs(CAB1815_0)+abs(CAB1815_1)+abs(CAB1815_2)+abs(CAB1815_3)",
            "zero_condition": "post-current c_A, pre-action Delta_w, transfer and non-Hilbert channels theorem-zero or source-backed",
            "required_inputs": "all CAB1815 component values; common normalizer; units; source paths; arena projections",
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
            "countermodel_id": "CM1815_0_post_cA_without_readout_order",
            "countermodel": "J_A -> c_A J_A after variation but before arena readout",
            "why_it_defeats_claim": "without readout-order typing, c_A can be interpreted as source transfer rather than harmless calibration",
            "blocked_by": "variation-before-readout/source-readout order theorem",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1815_1_pre_wA",
            "countermodel": "S_matter=sum_A w_A S_A before variation",
            "why_it_defeats_claim": "Hilbert/Noether current inherits w_A and current ownership cannot remove it",
            "blocked_by": "action-scale owner and connected matter-category naturality",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1815_2_disconnected_components",
            "countermodel": "independent source weights on disconnected matter-category components",
            "why_it_defeats_claim": "naturality only equalizes weights inside connected components",
            "blocked_by": "parent matter-category connectedness or finite component tensor",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1815_3_nonhilbert_bypass",
            "countermodel": "J_src=kappa T_H+sum_A zeta_A J_NH,A",
            "why_it_defeats_claim": "non-Hilbert currents are not current rescalings and can bypass Hilbert-source ownership",
            "blocked_by": "non-Hilbert silence theorem or source-backed zeta_A residual",
            "retained": True,
            "valid_for_claim": False,
        },
    ]


def gr_newton_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1815_0_post_current",
            "if_closed": "post-variation c_A is theorem-zero",
            "would_buy": "removes a clean source/test current-rescaling route before WEP/R10 readout",
            "still_missing": "pre-action weights, non-Hilbert bypass, arena transfer and alpha-level/unique-F2 gates",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1815_1_pre_action",
            "if_closed": "connected action-scale naturality kills Delta_w_A",
            "would_buy": "source universality moves much closer to derivable GR/Newton source coupling",
            "still_missing": "parent matter category/action-scale/measure signature is not signed",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1815_2_local_GR",
            "if_closed": "all current/source-normalization routes theorem-zero",
            "would_buy": "one large family of arbitrary local couplings disappears from the residual vector",
            "still_missing": "EH/Poisson/measured-G/PPN/qDq/boundary and source-worldtube gates remain",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1815_3_verdict",
            "if_closed": "1815 closes no-current-rescale",
            "would_buy": "serious source-side progress but not a standalone local-GR pass",
            "still_missing": "current corpus only closes conditional distinctions; finite rows stay missing",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1815_0_theorem_contract",
            "gate": "no-current-rescale theorem written",
            "current_status": "PASS_CONTRACT_ONLY",
            "reason": "NCR1815 distinguishes post-current c_A from pre-action w_A and writes exact conditional routes",
            "gate_pass": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1815_1_post_cA",
            "gate": "post-variation c_A theorem-zero",
            "current_status": "BLOCKED",
            "reason": "source/readout order and parent current owner remain unsigned",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1815_2_pre_wA",
            "gate": "pre-variation Delta_w theorem-zero",
            "current_status": "BLOCKED",
            "reason": "connected matter category, action-scale owner and measure descent remain unsigned",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1815_3_residual_values",
            "gate": "c_A/Delta_w residual rows source-backed",
            "current_status": "BLOCKED",
            "reason": "CAB1815 rows have missing component values, source paths and common normalizers",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1815_4_local_promotion",
            "gate": "WEP/R10/PPN/local-GR promotion allowed",
            "current_status": "REFUSED",
            "reason": "theorem is contract-only and source/current residuals are not score-ready",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1815_0_no_current_rescale",
            "claim": "J_A -> c_A J_A is fully forbidden",
            "status": "BLOCKED",
            "reason": "post-variation c_A is only conditionally killed and readout-order/current-owner premises are unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1815_1_no_source_weights",
            "claim": "pre-variation source/action weights are theorem-zero",
            "status": "BLOCKED",
            "reason": "action-scale owner and connected matter-category naturality remain unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1815_2_alpha_WEP_R10",
            "claim": "alpha/source WEP/R10 branches pass",
            "status": "BLOCKED",
            "reason": "c_A/Delta_w rows are missing and non-Hilbert/readout tails remain open",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1815_3_local_GR_Newton",
            "claim": "local GR/Newton/PPN follows",
            "status": "REFUSED",
            "reason": "1815 is a source-normalization subgate, not the full GR reduction",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1815_0_theorem_result",
            "decision": "POST_VARIATION_C_A_EXACT_CONDITIONAL",
            "reason": "if parent current and variation-before-readout are signed, a later c_A cannot redefine the parent source current",
            "next_action": "keep as contract-only until readout order and parent current owner close",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1815_1_limit_result",
            "decision": "PRE_VARIATION_W_A_SURVIVES_CURRENT_OWNER",
            "reason": "current ownership cannot remove weights already inside the action before variation",
            "next_action": "route w_A/Delta_w to action-scale connectedness or finite source rows",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1815_2_residual_status",
            "decision": "C_A_DELTA_W_BOUND_ROWS_READY_NONCLAIM",
            "reason": "c_A, Delta_w, transfer and non-Hilbert rows are explicit but unsourced",
            "next_action": "fill no row without units, source path, common normalizer and no-cancellation guard",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1815_3_best_next",
            "decision": "VARIATION_BEFORE_READOUT_ORDER_NEXT",
            "reason": "the least diffuse next theorem is to sign the readout-order premise that would actually kill post-variation c_A/F(T_A,A)",
            "next_action": "1816-Y5-R2FR-variation-before-readout-source-selector-order-or-post-current-cA-row.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1815_0_primary",
            "next_target": "1816-Y5-R2FR-variation-before-readout-source-selector-order-or-post-current-cA-row.md",
            "script": "scripts/Y5_R2FR_variation_before_readout_source_selector_order_or_post_current_cA_row.py",
            "objective": "try to parent-sign variation-before-readout/source-selector order so post-current c_A/F(T_A,A) is theorem-zero; if not, source a post-current c_A/transfer row",
            "selection_status": "selected",
            "success_condition": "readout-order theorem-zero, or c_A/transfer residual row is source-backed and remains nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1815_1_parallel",
            "next_target": "1816b-Y5-R2FR-action-scale-connected-matter-owner-or-Delta-w-bound-row.md",
            "script": "scripts/Y5_R2FR_action_scale_connected_matter_owner_or_Delta_w_bound_row.py",
            "objective": "attack the pre-variation w_A/Delta_w route through action-scale connectedness after post-current ordering is settled",
            "selection_status": "held_parallel",
            "success_condition": "Delta_w theorem-zero from connected action-scale owner, or finite Delta_w row is source-backed",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "no_current_rescale_theorem": no_current_rescale_theorem_rows(),
        "post_pre_rescale_split": post_pre_rescale_rows(),
        "naturality_action_weight_gate": naturality_action_weight_rows(),
        "cA_bound_row_schema": c_a_bound_rows(),
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
    allowed_gate_pass = {"AC1815_0_theorem_contract"}
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
                or (boolish(row.get("gate_pass", False)) and row.get("gate_id") != "AC1815_0_theorem_contract")
            ):
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    exists_ok = all(boolish(row["exists"]) for row in source_rows)
    needles_ok = all(boolish(row["needles_present"]) for row in source_rows)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1815_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1815_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1815_2_theorem_contract_written",
            any(row["theorem_id"] == "NCR1815_0_target" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in rows_map["no_current_rescale_theorem"]),
            "no-current-rescale theorem is written as exact conditional",
        ),
        (
            "VAL1815_3_post_pre_split",
            any(row["split_id"] == "PPR1815_0_post_current_rescale" and row["status"] == "KILLED_CONDITIONALLY" for row in rows_map["post_pre_rescale_split"])
            and any(row["split_id"] == "PPR1815_2_pre_action_weight" and row["status"] == "SURVIVES_CURRENT_OWNER" for row in rows_map["post_pre_rescale_split"]),
            "post-current c_A and pre-action w_A are separated correctly",
        ),
        (
            "VAL1815_4_theorem_not_promoted",
            any(row["theorem_id"] == "NCR1815_4_verdict" and row["proof_status"] == "NO_CURRENT_RESCALE_CONTRACT_NOT_CURRENT_PROOF" for row in rows_map["no_current_rescale_theorem"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["no_current_rescale_theorem"]),
            "no-current-rescale theorem is not promoted as current proof",
        ),
        (
            "VAL1815_5_naturality_gate_blocked",
            any(row["gate_id"] == "NAW1815_4_verdict" and row["current_status"] == "ACTION_WEIGHT_EXCLUSION_NOT_DERIVED" for row in rows_map["naturality_action_weight_gate"]),
            "action-scale/naturality gate remains blocked",
        ),
        (
            "VAL1815_6_bound_rows_nonclaim",
            any(row["residual_id"] == "CAB1815_4_total" for row in rows_map["cA_bound_row_schema"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["cA_bound_row_schema"]),
            "c_A/Delta_w residual rows are schema-only and nonclaim",
        ),
        (
            "VAL1815_7_countermodels_retained",
            all(boolish(row["retained"]) and not boolish(row["valid_for_claim"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain retained",
        ),
        (
            "VAL1815_8_gr_newton_nonclaim",
            all(not boolish(row["claim_allowed_now"]) and not boolish(row["valid_for_claim"]) for row in rows_map["gr_newton_impact"]),
            "GR/Newton impact rows remain nonclaim",
        ),
        (
            "VAL1815_9_acceptance_blocks",
            any(row["gate_id"] == "AC1815_0_theorem_contract" and boolish(row["gate_pass"]) and not boolish(row["claim_allowed"]) for row in rows_map["acceptance_gate"])
            and all(not boolish(row["claim_allowed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["acceptance_gate"]),
            "acceptance gate permits contract-only progress and blocks claims",
        ),
        (
            "VAL1815_10_claim_gates_blocked",
            all(row["status"] in {"BLOCKED", "REFUSED"} and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "all current/source/local claim gates remain blocked or refused",
        ),
        ("VAL1815_11_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1815_12_missing_not_ready", missing_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1815_13_decision_next",
            any(row["decision_id"] == "DEC1815_3_best_next" and row["decision"] == "VARIATION_BEFORE_READOUT_ORDER_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects variation-before-readout order next",
        ),
        (
            "VAL1815_14_next_selected",
            any(row["route_id"] == "NEXT1815_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1815_15_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1815 CSVs parse"),
        ("VAL1815_16_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1815_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1815_18_formalization_untouched", formalization_untouched(), "no 1815 outputs found under formalization-workbench"),
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
            "check_id": "VAL1815_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1815 Noether current owner and no-current-rescale proof or cA bound row checkpoint",
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
            "# 1815 Y5 R2FR Noether-current owner and no-current-rescale proof or cA bound row",
            "",
            "**Progress:** 1815 separates the coupling gremlin into two different beasts. A post-variation `J_A -> c_A J_A` is killable by a parent Noether/Hilbert current plus variation-before-readout theorem. A pre-variation `w_A S_A` is not killed by current ownership and must be handled by action-scale/connected-matter naturality or finite `Delta_w` rows.",
            "",
            "**Current verdict:** exact conditional theorem, not current proof. We have sharpened the route, but the corpus still lacks parent-signed readout order, connected ordinary matter/action-scale ownership, species-blind measure descent, and non-Hilbert silence.",
            "",
            "**Claim ceiling:** no no-current-rescale claim, no `Delta_w=0`, no `c_A=0`, no alpha WEP/R10/clock pass, no PPN/local-GR/Newton pass, no GitHub action, and no `formalization-workbench` edit is allowed from 1815.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## No Current Rescale Theorem",
            markdown_table(rows_map["no_current_rescale_theorem"], ["theorem_id", "claim", "mathematical_statement", "proof_status", "current_corpus_status", "valid_for_claim"]),
            "",
            "## Post Pre Rescale Split Audit",
            markdown_table(rows_map["post_pre_rescale_split"], ["split_id", "loophole", "status", "reason", "missing_for_claim", "finite_row_if_open", "valid_for_claim"]),
            "",
            "## Naturality Action Weight Gate",
            markdown_table(rows_map["naturality_action_weight_gate"], ["gate_id", "required_clause", "current_status", "would_close", "source_anchor", "valid_for_claim"]),
            "",
            "## cA Bound Row Schema",
            markdown_table(rows_map["cA_bound_row_schema"], ["residual_id", "quantity", "definition", "formal_expression", "zero_condition", "current_status", "units", "common_normalizer", "score_ready", "valid_for_claim"]),
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
            "This is a good tightening. The current-owner theorem is not dead; it kills the post-variation trick if readout order is signed. But it cannot kill weights already inserted into the action. So the next best target is readout order for post-current `c_A`, while the pre-action `Delta_w` route stays as a parallel action-scale/connectedness problem.",
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
    print(f"1815 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
