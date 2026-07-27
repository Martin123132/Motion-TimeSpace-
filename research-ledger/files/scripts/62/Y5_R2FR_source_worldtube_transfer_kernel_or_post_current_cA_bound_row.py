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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1817"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1817-Y5-R2FR-source-worldtube-transfer-kernel-or-post-current-cA-bound-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1817_0_1816_doc",
        "source_key": "1816_handoff_doc",
        "source_path": ROOT / "1816-Y5-R2FR-variation-before-readout-source-selector-order-or-post-current-cA-row.md",
        "needles": ["DEC1816_3_best_next", "NEXT1816_0_primary"],
        "role": "1816 selects the source-worldtube transfer kernel as the next target.",
    },
    {
        "source_id": "SRC1817_1_1816_validation",
        "source_key": "1816_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1816_VALIDATION.csv",
        "needles": ["VAL1816_OVERALL", "PASS"],
        "role": "confirms 1816 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1817_2_1816_post_current_schema",
        "source_key": "1816_post_current_schema",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1816_POST_CURRENT_CA_ROW_SCHEMA.csv",
        "needles": ["PCR1816_2_worldtube_transfer", "MISSING_SOURCE_WORLDTUBE_TRANSFER_KERNEL"],
        "role": "worldtube transfer is the explicit missing row from 1816.",
    },
    {
        "source_id": "SRC1817_3_1816_theorem",
        "source_key": "1816_variation_before_readout",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1816_VARIATION_BEFORE_READOUT_THEOREM.csv",
        "needles": ["VBR1816_5_source_worldtube_limit", "K_ARENA_SOURCE_TRANSFER_MISSING"],
        "role": "1816 states that source-worldtube projection is harmless only under strict downstream typing.",
    },
    {
        "source_id": "SRC1817_4_1718_selector_theorem",
        "source_key": "1718_worldtube_selector",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1718_WORLDTUBE_SELECTOR_THEOREM_ATTEMPT.csv",
        "needles": ["WST1718_2_current_verdict", "NOT_PROVED_FOR_CURRENT_MTS"],
        "role": "worldtube selector theorem remains conditional.",
    },
    {
        "source_id": "SRC1817_5_1718_support_owner",
        "source_key": "1718_support_owner",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1718_WORLDTUBE_SUPPORT_OWNER_AUDIT.csv",
        "needles": ["WTO1718_8_verdict", "WORLDTUBE_SUPPORT_OWNER_NOT_PROVED"],
        "role": "source worldtube support is not yet parent-owned.",
    },
    {
        "source_id": "SRC1817_6_1778_current_map",
        "source_key": "1778_worldtube_current_map",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1778_WORLDTUBE_CURRENT_MAP.csv",
        "needles": ["WCM1778_1_chain_identity", "MISSING_CHAIN_IDENTITY"],
        "role": "Hilbert/worldtube/charge chain identity is the main missing structural equality.",
    },
    {
        "source_id": "SRC1817_7_1456_projection_theorem",
        "source_key": "1456_source_worldtube_projection",
        "source_path": RESIDUALS / "P8_Y5_R10_1456_SOURCE_WORLDTUBE_PROJECTION_THEOREM_ATTEMPT.csv",
        "needles": ["SWP1456_6_verdict", "THEOREM_CONDITIONAL_NOT_PROMOTED"],
        "role": "downstream linear projection theorem exists only conditionally.",
    },
    {
        "source_id": "SRC1817_8_1456_file_ledger",
        "source_key": "1456_source_worldtube_files",
        "source_path": RESIDUALS / "P8_Y5_R10_1456_SOURCE_WORLDTUBE_FILE_LEDGER_NONCLAIM.csv",
        "needles": ["SFI1456_0_source_worldtube_file", "MISSING_SOURCE_WORLDTUBE_FILE"],
        "role": "official WEP/source-worldtube file is missing.",
    },
    {
        "source_id": "SRC1817_9_1608_tau_wep",
        "source_key": "1608_tau_wep_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1608_TAU_WEP_READOUT_CONTRACT.csv",
        "needles": ["TAU1608_4_verdict", "TAU_WEP_NOT_EVALUATED"],
        "role": "tau_WEP remains formal because official readout/source inputs are not imported.",
    },
    {
        "source_id": "SRC1817_10_1810_tau_chain",
        "source_key": "1810_tau_source_chain",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1810_TAU_WEP_R10_SOURCE_CHAIN.csv",
        "needles": ["TPC1810_5_verdict", "TRANSFER_BLOCKED"],
        "role": "cross-arena transfer remains blocked until tau roles and source/readout functors are parent-owned.",
    },
    {
        "source_id": "SRC1817_11_1760_worldtube_descent",
        "source_key": "1760_matter_worldtube_descent",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1760_MATTER_WORLDTUBE_DESCENT_ATTEMPT.csv",
        "needles": ["MWD1760_3_worldtube_support", "WORLDTUBE_OWNER_OPEN"],
        "role": "worldtube support descends only under unsigned Hilbert/tau assumptions.",
    },
    {
        "source_id": "SRC1817_12_1760_source_owner",
        "source_key": "1760_worldtube_source_owner",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1760_WORLDTUBE_SOURCE_OWNER_AUDIT.csv",
        "needles": ["WTA1760_3_matter_worldtube_verdict", "WORLDTUBE_DESCENT_NOT_PARENT_SIGNED"],
        "role": "worldtube terms still live in the matter/source residual.",
    },
    {
        "source_id": "SRC1817_13_1701_commutator",
        "source_key": "1701_readout_commutator",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1701_READOUT_COMMUTATOR_AUDIT.csv",
        "needles": ["RC1701_6_verdict", "GENERAL_NO_REENTRY_NOT_DERIVED"],
        "role": "general readout no-reentry is not theorem-zero.",
    },
    {
        "source_id": "SRC1817_14_1675_descent",
        "source_key": "1675_source_readout_descent",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1675_SOURCE_READOUT_DESCENT_GATE.csv",
        "needles": ["SRD1675_5_verdict", "SOURCE_READOUT_DESCENT_NOT_CLOSED"],
        "role": "source/readout descent remains unclosed.",
    },
]


OUTPUTS: dict[str, Path] = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1817_SOURCE_REGISTER.csv",
    "transfer_kernel_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1817_SOURCE_WORLDTUBE_TRANSFER_KERNEL_THEOREM.csv",
    "arena_transfer_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1817_ARENA_TRANSFER_AUDIT.csv",
    "k_arena_residual_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1817_K_ARENA_RESIDUAL_ROWS.csv",
    "acquisition_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1817_SOURCE_TRANSFER_ACQUISITION_LEDGER.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1817_COUNTERMODEL_LEDGER.csv",
    "gr_newton_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1817_GR_NEWTON_IMPACT_LEDGER.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1817_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1817_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1817_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1817_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1817_VALIDATION.csv",
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


def transfer_kernel_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "KWT1817_0_target",
            "claim": "source-worldtube arena transfer is harmless after parent source extraction",
            "mathematical_statement": "If J_parent is fixed by the parent variation and K_arena is a fixed linear downstream functional from solved parent sources to reported data, then K_arena cannot redefine the parent source current; it can only weight the observed arena response.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "current_corpus_status": "K_ARENA_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "KWT1817_1_downstream_linearity",
            "claim": "linear downstream kernels do not create source couplings",
            "mathematical_statement": "For fixed K_arena, delta_parent of K_arena[J_parent] equals K_arena[delta_parent J_parent]; there is no independent source coefficient unless K_arena depends on the varied fields, source labels, support choice, calibration, or effective action.",
            "proof_status": "EXACT_IF_FIXED_LINEAR_MAP",
            "current_corpus_status": "FIXED_KERNEL_AND_OFFICIAL_ARRAYS_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "KWT1817_2_worldtube_support",
            "claim": "worldtube support is owned by the Hilbert source",
            "mathematical_statement": "W_source equals closure of support of J_H contracted with tau, and K_arena integrates only that already-defined support.",
            "proof_status": "CONDITIONAL_LEMMA",
            "current_corpus_status": "WORLDTUBE_SUPPORT_OWNER_NOT_PROVED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "KWT1817_3_charge_source_identity",
            "claim": "exterior Hamiltonian charge equals projected observed source",
            "mathematical_statement": "G_ref^-1 Q_tau equals Pi_M^H J_H^dress plus exact boundary and residual terms, with R_Hsrc equal to zero or bounded.",
            "proof_status": "KEY_IDENTITY_MISSING",
            "current_corpus_status": "WCM1778_CHAIN_IDENTITY_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "KWT1817_4_no_feedback_guard",
            "claim": "kernel support, masks, calibration and measured GM do not feed back into the source",
            "mathematical_statement": "K_arena may be applied to the solved source, but it may not define where the source exists, normalize the parent source, select the action domain, or absorb relative source residuals into a common calibration.",
            "proof_status": "GUARDRAIL_NOT_ZERO_PROOF",
            "current_corpus_status": "READOUT_COMMUTATOR_AND_CALIBRATION_FEEDBACK_OPEN",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "KWT1817_5_arena_limit",
            "claim": "one transfer theorem covers WEP, R10, clocks, PPN and orbital systems",
            "mathematical_statement": "A common theorem can type the maps, but each arena still needs its own kernel, units, normalizer, source profile, product convention and no-null-space guard.",
            "proof_status": "ARENA_SPLIT_REQUIRED",
            "current_corpus_status": "TRANSFER_PRODUCTS_BLOCKED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "KWT1817_6_verdict",
            "claim": "1817 proves K_arena transfer zero in the current corpus",
            "mathematical_statement": "KWT1817_0 through KWT1817_5 close only if downstream fixed-kernel typing, Hilbert worldtube ownership, charge/source identity, no feedback and arena kernels are all signed together.",
            "proof_status": "CONDITIONAL_THEOREM_NOT_CURRENT_PROOF",
            "current_corpus_status": "DEMOTE_TO_K_ARENA_AND_R_HSRC_ROWS",
            "valid_for_claim": False,
        },
    ]


def arena_transfer_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ATA1817_0_cross_arena_type",
            "arena": "cross_arena",
            "needed_clause": "K_arena is a fixed post-solution functional",
            "current_status": "TYPE_CONDITIONAL_ONLY",
            "missing_for_claim": "parent domain typing and no readout feedback for every arena",
            "finite_row_if_open": "epsilon_K_arena_type",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ATA1817_1_WEP",
            "arena": "MICROSCOPE_WEP",
            "needed_clause": "K_CMSM, Earth source worldtube, material tensor and product convention are official and branch-locked",
            "current_status": "MISSING_OFFICIAL_SOURCE_AND_READOUT_FILES",
            "missing_for_claim": "official readout file, source worldtube file, material tensor, tau_min or direct product",
            "finite_row_if_open": "epsilon_K_WEP_transfer",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ATA1817_2_R10",
            "arena": "R10_short_range",
            "needed_clause": "finite profile/Yukawa kernel maps parent source and test charges into alpha(lambda)",
            "current_status": "MISSING_R10_KERNEL_PROFILE_AND_BOUND_INPUTS",
            "missing_for_claim": "lambda_X, Z_X, K_X, source/test charges, profile integral and promoted bound curve",
            "finite_row_if_open": "epsilon_K_R10_transfer",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ATA1817_3_PPN_orbit",
            "arena": "PPN_orbital",
            "needed_clause": "source-normalized Newtonian/PPN response matrix is derived from same Hilbert/worldtube source",
            "current_status": "MISSING_PPN_RESPONSE_AND_HILBERT_CHARGE_IDENTITY",
            "missing_for_claim": "PPN response matrix, gauge split, measured-G guard and exterior charge equality",
            "finite_row_if_open": "epsilon_K_PPN_transfer",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ATA1817_4_clock_EM",
            "arena": "clock_EM",
            "needed_clause": "clock/EM product uses same parent alpha/current branch and no source-worldtube rescaling",
            "current_status": "PRODUCT_BOUND_ONLY",
            "missing_for_claim": "tau_clock_time, Xhat/chi_X normalization and EM-level owner",
            "finite_row_if_open": "epsilon_K_clock_EM_transfer",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ATA1817_5_verdict",
            "arena": "all",
            "needed_clause": "all arena transfer kernels are pure downstream maps or bounded",
            "current_status": "TRANSFER_KERNELS_NOT_CLOSED",
            "missing_for_claim": "arena kernels, source paths, units, normalizers and no-null-space guards",
            "finite_row_if_open": "K_arena residual envelope",
            "valid_for_claim": False,
        },
    ]


def k_arena_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": "KAR1817_0_K_WEP",
            "quantity": "epsilon_K_WEP_transfer_abs",
            "definition": "MICROSCOPE source-worldtube/readout/material transfer mismatch",
            "formal_expression": "norm of K_WEP[J_parent] minus official WEP source response over source norm",
            "zero_condition": "official K_CMSM, Earth source worldtube and material tensor are fixed downstream maps",
            "required_inputs": "K_CMSM; Earth source worldtube; material tensor; product convention; units; source paths",
            "current_status": "MISSING_OFFICIAL_WEP_TRANSFER_INPUTS",
            "units": "dimensionless_transfer_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_WEP_TRANSFER_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "KAR1817_1_K_R10",
            "quantity": "epsilon_K_R10_transfer_abs",
            "definition": "R10 finite-source/readout/profile transfer mismatch",
            "formal_expression": "norm of K_R10[J_parent] minus Yukawa-profile source response over source norm",
            "zero_condition": "R10 kernel convention, source/test profiles and lambda_X are parent-signed or source-backed",
            "required_inputs": "lambda_X; Z_X; K_X; source/test charges; profile integral; units; source paths",
            "current_status": "MISSING_R10_TRANSFER_INPUTS",
            "units": "dimensionless_transfer_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_R10_TRANSFER_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "KAR1817_2_K_PPN_orbit",
            "quantity": "epsilon_K_PPN_orbit_transfer_abs",
            "definition": "PPN/orbital source response transfer mismatch",
            "formal_expression": "norm of K_PPN[T_H] minus weak-field response source over T_H norm",
            "zero_condition": "same Hilbert source generates Newtonian and PPN response with measured-G common mode removed",
            "required_inputs": "PPN response matrix; gauge convention; source profile; measured-G guard; units; source paths",
            "current_status": "MISSING_PPN_ORBIT_TRANSFER_INPUTS",
            "units": "dimensionless_transfer_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_PPN_TRANSFER_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "KAR1817_3_R_Hsrc",
            "quantity": "epsilon_R_Hsrc_abs",
            "definition": "residual between exterior Hamiltonian charge and projected Hilbert source",
            "formal_expression": "norm of G_ref^-1 Q_tau minus Pi_M^H J_H^dress minus dB_H over source norm",
            "zero_condition": "Hilbert/worldtube charge identity closes with zero-flux boundary term",
            "required_inputs": "Q_tau; Pi_M^H; J_H^dress; boundary term; source norm; units; source paths",
            "current_status": "MISSING_HILBERT_WORLDTUBE_CHARGE_IDENTITY",
            "units": "dimensionless_source_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_HSRC_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "KAR1817_4_readout_feedback",
            "quantity": "epsilon_K_feedback_abs",
            "definition": "kernel support, calibration or mask feedback into the source equation",
            "formal_expression": "norm of source-coefficient part of commutator between parent variation and K_arena",
            "zero_condition": "K_arena is independent of varied fields, source labels, support choice and calibration feedback",
            "required_inputs": "arena kernel; variation domain; feedback test; units; source paths",
            "current_status": "MISSING_NO_FEEDBACK_THEOREM_OR_BOUND",
            "units": "dimensionless_variation_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_FEEDBACK_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "KAR1817_5_total",
            "quantity": "epsilon_K_arena_total_abs",
            "definition": "total no-cancellation envelope for arena transfer uncertainty",
            "formal_expression": "abs(KAR1817_0)+abs(KAR1817_1)+abs(KAR1817_2)+abs(KAR1817_3)+abs(KAR1817_4)",
            "zero_condition": "all arena transfer, Hilbert charge identity and feedback channels theorem-zero or source-backed",
            "required_inputs": "all KAR1817 components; common normalizers; units; source paths; arena projections",
            "current_status": "MISSING_COMPONENT_VALUES_AND_COMMON_NORMALIZER",
            "units": "absolute_no_cancellation_envelope",
            "source_path": "",
            "common_normalizer": "MISSING_TOTAL_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def acquisition_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "item_id": "ACQ1817_0_WEP_source_worldtube",
            "target_quantity": "K_WEP source worldtube",
            "needed_file_or_theorem": "source-intake/microscope/source_worldtube/P_WEP_R_source_Earth_worldtube.csv",
            "required_fields": "time_s_or_orbit_phase; radius_m; density_kg_m3; source_component; kernel_weight; model_or_dataset; source_url_or_path",
            "current_status": "MISSING_SOURCE_WORLDTUBE_FILE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "item_id": "ACQ1817_1_WEP_official_readout",
            "target_quantity": "K_CMSM official readout",
            "needed_file_or_theorem": "source-intake/microscope/official_readout/P_WEP_K_CMSM_readout.csv",
            "required_fields": "time_s; session_id; orbit_id; axis; gx_m_s2; gz_m_s2; Sxx; Sxz; mask_flag; calibration_flag; source_url_or_path",
            "current_status": "MISSING_OFFICIAL_READOUT_FILE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "item_id": "ACQ1817_2_Hilbert_charge_identity",
            "target_quantity": "R_Hsrc",
            "needed_file_or_theorem": "1818 Hilbert-worldtube charge identity or residual row",
            "required_fields": "Q_tau; Pi_M_H; J_H_dress; boundary_flux; source_norm; theorem_status; source_path",
            "current_status": "MISSING_CHAIN_IDENTITY",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "item_id": "ACQ1817_3_R10_kernel",
            "target_quantity": "K_R10",
            "needed_file_or_theorem": "R10 finite-source Yukawa/profile kernel pack",
            "required_fields": "lambda_X; source_charge; test_charge; profile_integral; kernel_units; convention; source_path",
            "current_status": "MISSING_R10_TRANSFER_INPUTS",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "item_id": "ACQ1817_4_PPN_kernel",
            "target_quantity": "K_PPN_orbit",
            "needed_file_or_theorem": "PPN/orbital response matrix tied to Hilbert source",
            "required_fields": "response_parameter; gauge; source_norm; measured_G_guard; uncertainty; source_path",
            "current_status": "MISSING_PPN_ORBIT_TRANSFER_INPUTS",
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1817_0_field_dependent_kernel",
            "countermodel": "K_arena depends on fields varied in S_parent",
            "why_it_defeats_claim": "the variation of K_arena creates a source-coefficient commutator term",
            "blocked_by": "fixed downstream kernel theorem or finite feedback bound",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1817_1_support_selector",
            "countermodel": "worldtube support is chosen by mask, fitted radius or orbital calibration",
            "why_it_defeats_claim": "support choice can tune the effective source normalization",
            "blocked_by": "Hilbert support owner and compact linked-surface theorem",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1817_2_charge_source_mismatch",
            "countermodel": "exterior Hamiltonian charge differs from projected Hilbert source",
            "why_it_defeats_claim": "then orbital or Gauss mass may not be the same object as the parent source",
            "blocked_by": "Hilbert-worldtube charge identity or R_Hsrc bound",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1817_3_null_projection",
            "countermodel": "nonzero source/material residual lies in the kernel null space",
            "why_it_defeats_claim": "no lower bound follows from nonzero ingredients without alignment",
            "blocked_by": "tau_min or direct nonzero projection computation",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1817_4_measured_G_absorption",
            "countermodel": "relative source residual is hidden inside GM/G calibration",
            "why_it_defeats_claim": "this would fake local GR by absorbing a material/source residual into a common calibration",
            "blocked_by": "measured-G common-mode guard plus relative residual accounting",
            "retained": True,
            "valid_for_claim": False,
        },
    ]


def gr_newton_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1817_0_transfer_if_closed",
            "if_closed": "K_arena is proven fixed downstream or bounded in all local arenas",
            "would_buy": "post-current source/test transfer stops being an arbitrary coupling knob",
            "still_missing": "pre-action Delta_w, non-Hilbert tails, EH/Poisson/PPN reduction and measured-G absorption",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1817_1_charge_identity_if_closed",
            "if_closed": "Hilbert-worldtube charge identity is derived",
            "would_buy": "the source mass used by Newton/GR would be tied to parent Hilbert variation instead of orbital backfill",
            "still_missing": "boundary zero-flux proof, weak-field operator and PPN response matrix",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1817_2_local_GR",
            "if_closed": "K_arena and R_Hsrc both vanish",
            "would_buy": "one major source-side bridge toward derivable Newton/GR becomes structurally credible",
            "still_missing": "action-scale connectedness, q/Dq local plateau branch, EH source equation and empirical local bounds",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1817_3_verdict",
            "if_closed": "1817 alone proves local GR",
            "would_buy": "nothing claimable alone; this is a transfer/source bridge only",
            "still_missing": "current corpus keeps K_arena and R_Hsrc as nonclaim residual rows",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1817_0_theorem_contract",
            "gate": "source-worldtube transfer theorem written",
            "current_status": "PASS_CONTRACT_ONLY",
            "reason": "KWT1817 states the exact fixed-kernel theorem and its failure modes",
            "gate_pass": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1817_1_kernel_zero",
            "gate": "K_arena transfer theorem-zero",
            "current_status": "BLOCKED",
            "reason": "worldtube support, fixed kernel and no-feedback clauses are not signed",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1817_2_charge_identity",
            "gate": "Hilbert-worldtube charge identity derived",
            "current_status": "BLOCKED",
            "reason": "WCM1778 chain identity remains missing",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1817_3_residual_values",
            "gate": "K_arena/R_Hsrc residual rows source-backed",
            "current_status": "BLOCKED",
            "reason": "KAR1817 rows have missing component values, source paths and common normalizers",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1817_4_local_promotion",
            "gate": "WEP/R10/PPN/local-GR promotion allowed",
            "current_status": "REFUSED",
            "reason": "1817 is a transfer-kernel subgate and cannot claim local GR/Newton",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1817_0_K_arena_zero",
            "claim": "arena transfer kernels are theorem-zero",
            "status": "BLOCKED",
            "reason": "fixed downstream kernels and source-worldtube ownership are unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1817_1_R_Hsrc_zero",
            "claim": "exterior charge equals projected Hilbert source",
            "status": "BLOCKED",
            "reason": "charge/source chain identity is missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1817_2_WEP_R10_transfer",
            "claim": "WEP/R10 transfer rows can be scored",
            "status": "BLOCKED",
            "reason": "official files, kernels and normalizers are missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1817_3_local_GR_Newton",
            "claim": "local GR/Newton/PPN follows",
            "status": "REFUSED",
            "reason": "transfer-kernel work is not the full EH/Newton/PPN reduction",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1817_0_theorem_result",
            "decision": "FIXED_KERNEL_THEOREM_EXACT_CONDITIONAL",
            "reason": "a fixed downstream linear kernel cannot redefine the parent source, but that type condition is not globally signed",
            "next_action": "retain as contract-only until kernel and no-feedback clauses close",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1817_1_residual_status",
            "decision": "K_ARENA_AND_R_HSRC_ROWS_NONCLAIM",
            "reason": "arena kernels, source paths, component values and common normalizers are missing",
            "next_action": "do not score WEP/R10/PPN transfer until rows become source-backed",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1817_2_core_blocker",
            "decision": "HILBERT_WORLDTUBE_CHARGE_IDENTITY_IS_CORE",
            "reason": "without G_ref^-1 Q_tau equals projected Hilbert source, Newton/GR source mass is not derivably the same object",
            "next_action": "attack R_Hsrc directly before trying to promote arena transfer rows",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1817_3_best_next",
            "decision": "HILBERT_WORLDTUBE_CHARGE_IDENTITY_NEXT",
            "reason": "this is the least empirical and most GR-relevant missing bridge exposed by the K_arena audit",
            "next_action": "1818-Y5-R2FR-Hilbert-worldtube-charge-identity-or-R-Hsrc-bound-row.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1817_0_primary",
            "next_target": "1818-Y5-R2FR-Hilbert-worldtube-charge-identity-or-R-Hsrc-bound-row.md",
            "script": "scripts/Y5_R2FR_Hilbert_worldtube_charge_identity_or_R_Hsrc_bound_row.py",
            "objective": "derive G_ref^-1 Q_tau = Pi_M^H J_H^dress + dB_H with zero or bounded R_Hsrc; if not, emit a finite R_Hsrc residual row",
            "selection_status": "selected",
            "success_condition": "Hilbert/worldtube charge identity theorem-zero, or R_Hsrc row becomes source-backed and remains nonclaim until acceptance gates pass",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1817_1_parallel",
            "next_target": "1818b-Y5-R2FR-official-WEP-source-worldtube-acquisition-pack.md",
            "script": "scripts/Y5_R2FR_official_WEP_source_worldtube_acquisition_pack.py",
            "objective": "acquire or stage official WEP source-worldtube/readout/material files for K_WEP scoring",
            "selection_status": "held_parallel",
            "success_condition": "official files parse, carry units/source paths and remain nonclaim until theorem gates pass",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "transfer_kernel_theorem": transfer_kernel_theorem_rows(),
        "arena_transfer_audit": arena_transfer_rows(),
        "k_arena_residual_rows": k_arena_residual_rows(),
        "acquisition_ledger": acquisition_rows(),
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
    allowed_gate_pass = {"AC1817_0_theorem_contract"}
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
                or (boolish(row.get("gate_pass", False)) and row.get("gate_id") != "AC1817_0_theorem_contract")
            ):
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    exists_ok = all(boolish(row["exists"]) for row in source_rows)
    needles_ok = all(boolish(row["needles_present"]) for row in source_rows)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1817_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1817_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1817_2_theorem_contract_written",
            any(row["theorem_id"] == "KWT1817_0_target" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in rows_map["transfer_kernel_theorem"]),
            "source-worldtube transfer theorem is written as exact conditional",
        ),
        (
            "VAL1817_3_key_identity_blocked",
            any(row["theorem_id"] == "KWT1817_3_charge_source_identity" and row["proof_status"] == "KEY_IDENTITY_MISSING" for row in rows_map["transfer_kernel_theorem"]),
            "Hilbert/worldtube charge identity remains the key missing bridge",
        ),
        (
            "VAL1817_4_theorem_not_promoted",
            any(row["theorem_id"] == "KWT1817_6_verdict" and row["proof_status"] == "CONDITIONAL_THEOREM_NOT_CURRENT_PROOF" for row in rows_map["transfer_kernel_theorem"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["transfer_kernel_theorem"]),
            "1817 theorem is not promoted as current proof",
        ),
        (
            "VAL1817_5_arena_split_required",
            any(row["audit_id"] == "ATA1817_5_verdict" and row["current_status"] == "TRANSFER_KERNELS_NOT_CLOSED" for row in rows_map["arena_transfer_audit"]),
            "arena transfer audit remains split and blocked",
        ),
        (
            "VAL1817_6_residual_rows_nonclaim",
            any(row["residual_id"] == "KAR1817_5_total" for row in rows_map["k_arena_residual_rows"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["k_arena_residual_rows"]),
            "K_arena residual rows are schema-only and nonclaim",
        ),
        (
            "VAL1817_7_acquisition_rows_nonclaim",
            all(not boolish(row["valid_for_claim"]) for row in rows_map["acquisition_ledger"]),
            "acquisition rows remain nonclaim",
        ),
        (
            "VAL1817_8_countermodels_retained",
            all(boolish(row["retained"]) and not boolish(row["valid_for_claim"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain retained",
        ),
        (
            "VAL1817_9_gr_newton_nonclaim",
            all(not boolish(row["claim_allowed_now"]) and not boolish(row["valid_for_claim"]) for row in rows_map["gr_newton_impact"]),
            "GR/Newton impact rows remain nonclaim",
        ),
        (
            "VAL1817_10_acceptance_blocks",
            any(row["gate_id"] == "AC1817_0_theorem_contract" and boolish(row["gate_pass"]) and not boolish(row["claim_allowed"]) for row in rows_map["acceptance_gate"])
            and all(not boolish(row["claim_allowed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["acceptance_gate"]),
            "acceptance gate permits contract-only progress and blocks claims",
        ),
        (
            "VAL1817_11_claim_gates_blocked",
            all(row["status"] in {"BLOCKED", "REFUSED"} and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "all transfer/source/local claim gates remain blocked or refused",
        ),
        ("VAL1817_12_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1817_13_missing_not_ready", missing_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1817_14_decision_next",
            any(row["decision_id"] == "DEC1817_3_best_next" and row["decision"] == "HILBERT_WORLDTUBE_CHARGE_IDENTITY_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects Hilbert-worldtube charge identity next",
        ),
        (
            "VAL1817_15_next_selected",
            any(row["route_id"] == "NEXT1817_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1817_16_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1817 CSVs parse"),
        ("VAL1817_17_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1817_18_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1817_19_formalization_untouched", formalization_untouched(), "no 1817 outputs found under formalization-workbench"),
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
            "check_id": "VAL1817_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1817 source-worldtube transfer kernel or post-current cA bound row checkpoint",
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
            "# 1817 Y5 R2FR source-worldtube transfer kernel or post-current cA bound row",
            "",
            "**Progress:** 1817 pins down the transfer-kernel logic. A fixed downstream linear `K_arena` cannot change the parent source after variation. But the current corpus has not proven that the arena kernels, worldtube support, exterior charge, measured-G guard and no-feedback conditions are all fixed downstream objects.",
            "",
            "**Current verdict:** exact conditional theorem, not current proof. The biggest exposed blocker is the Hilbert-worldtube charge identity: `G_ref^-1 Q_tau = Pi_M^H J_H^dress + dB_H + R_Hsrc`. Without that bridge, Newton/GR source mass can still be a readout/imported object rather than a derived parent source.",
            "",
            "**Claim ceiling:** no `K_arena=0`, no `R_Hsrc=0`, no WEP/R10/PPN/local-GR/Newton pass, no GitHub action, and no `formalization-workbench` edit is allowed from 1817.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Source Worldtube Transfer Kernel Theorem",
            markdown_table(rows_map["transfer_kernel_theorem"], ["theorem_id", "claim", "mathematical_statement", "proof_status", "current_corpus_status", "valid_for_claim"]),
            "",
            "## Arena Transfer Audit",
            markdown_table(rows_map["arena_transfer_audit"], ["audit_id", "arena", "needed_clause", "current_status", "missing_for_claim", "finite_row_if_open", "valid_for_claim"]),
            "",
            "## K Arena Residual Rows",
            markdown_table(rows_map["k_arena_residual_rows"], ["residual_id", "quantity", "definition", "formal_expression", "zero_condition", "current_status", "units", "common_normalizer", "score_ready", "valid_for_claim"]),
            "",
            "## Source Transfer Acquisition Ledger",
            markdown_table(rows_map["acquisition_ledger"], ["item_id", "target_quantity", "needed_file_or_theorem", "required_fields", "current_status", "valid_for_claim"]),
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
            "This narrows the coupling problem again. The arena kernel itself is not evil if it is truly downstream. The real monster under the bed is whether the source mass/current entering Newton/GR is the same parent Hilbert source as the one being varied. So the next derivation should attack `R_Hsrc`: either prove the Hilbert-worldtube charge identity or admit it as a finite source residual.",
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
    print(f"1817 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
