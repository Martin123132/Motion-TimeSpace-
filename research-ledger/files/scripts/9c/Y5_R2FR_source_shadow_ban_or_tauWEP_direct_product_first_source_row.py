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
QUARANTINE = MICROSCOPE / "quarantine" / "1839"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1839-Y5-R2FR-source-shadow-ban-or-tauWEP-direct-product-first-source-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1839_0_1838_next",
        "source_key": "1838_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1838_NEXT_TARGET.csv",
        "needles": ["NEXT1838_0_primary", "selected"],
        "role": "1838 selects source-shadow ban or tau_WEP/direct-product first source row.",
    },
    {
        "source_id": "SRC1839_1_1838_validation",
        "source_key": "1838_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1838_VALIDATION.csv",
        "needles": ["VAL1838_OVERALL", "PASS"],
        "role": "confirms 1838 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1839_2_1838_first_WEP_input",
        "source_key": "1838_first_WEP_input",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1838_FIRST_WEP_COMPONENT_BOUND_INPUT.csv",
        "needles": ["FWCB1838_1_tau_WEP", "MISSING_TAU_WEP"],
        "role": "1838 explicit Delta_w/tau/direct-product missing input row.",
    },
    {
        "source_id": "SRC1839_3_1767_identity",
        "source_key": "1767_source_map_identity",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1767_SINGLE_SOURCE_MAP_IDENTITY_THEOREM.csv",
        "needles": ["SMI1767_1_identity_source_map", "DERIVED_CONDITIONAL_THEOREM"],
        "role": "source map identity theorem is conditionally derived but parent unsigned.",
    },
    {
        "source_id": "SRC1839_4_1767_shadow",
        "source_key": "1767_source_shadow_zero",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1767_SOURCE_SHADOW_ZERO_ATTEMPT.csv",
        "needles": ["SSZ1767_4_current_verdict", "PARTIAL_THEOREM_NOT_FULL_PARENT_PROOF"],
        "role": "source-shadow zero attempt classifies but does not eliminate the shadow route.",
    },
    {
        "source_id": "SRC1839_5_1767_bound",
        "source_key": "1767_shadow_bound_interface",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1767_DELTAW_SHADOW_BOUND_INTERFACE.csv",
        "needles": ["DSH1767_0_delta_w_shadow", "MISSING_PARENT_NORMAL_FORM_OR_NUMERIC_BOUND"],
        "role": "delta_w_shadow remains a nonclaim residual interface.",
    },
    {
        "source_id": "SRC1839_6_1768_normal_form",
        "source_key": "1768_parent_action_normal_form",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_PARENT_ACTION_NORMAL_FORM_SIGNATURE.csv",
        "needles": ["ANF1768_6_current_verdict", "SIGNATURE_READY_PARENT_UNSIGNED"],
        "role": "parent action normal form is ready as a signature but not a complete parent proof.",
    },
    {
        "source_id": "SRC1839_7_1768_source_map_gate",
        "source_key": "1768_source_map_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_SOURCE_MAP_IDENTITY_GATE.csv",
        "needles": ["SMG1768_4_current_verdict", "NOT_CLAIMABLE"],
        "role": "source-map identity remains not claimable for current MTS.",
    },
    {
        "source_id": "SRC1839_8_tau_route",
        "source_key": "1703_tau_WEP_route",
        "source_path": MICROSCOPE_RESIDUALS / "R2FR_tau_WEP_route_1703.csv",
        "needles": ["TWR1703_7_verdict", "BLOCKED_MISSING_INPUTS"],
        "role": "tau_WEP route lists the missing official readout/source/material/product inputs.",
    },
    {
        "source_id": "SRC1839_9_direct_route",
        "source_key": "1703_direct_product_route",
        "source_path": MICROSCOPE_RESIDUALS / "R2FR_direct_product_route_1703.csv",
        "needles": ["DPR1703_3_verdict", "SELECTED_FOR_1704_PARSER_SHELL"],
        "role": "direct WEP product route is preferred once official/source-backed inputs exist.",
    },
    {
        "source_id": "SRC1839_10_direct_contract",
        "source_key": "1706_direct_product_contract",
        "source_path": MICROSCOPE_RESIDUALS / "R2FR_direct_product_only_contract_1706.csv",
        "needles": ["DPC1706_3_current_status", "BLOCKED_EXTERNAL_OR_PARENT_INPUTS"],
        "role": "direct product remains blocked by external or parent inputs.",
    },
    {
        "source_id": "SRC1839_11_tau_contraction",
        "source_key": "1596_tau_WEP_contraction",
        "source_path": MICROSCOPE_RESIDUALS / "R2FR_tau_WEP_contraction_law_nonclaim_1596.csv",
        "needles": ["TCL1596_1_product_bound", "SOURCE_BACKED_PRODUCT_BOUND_FROM_1595"],
        "role": "MICROSCOPE supplies a product-bound comparator, not a prediction or tau evaluation.",
    },
    {
        "source_id": "SRC1839_12_1769_GR_bridge",
        "source_key": "1769_GR_left_hand_bridge",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1769_EINSTEIN_LEFT_HAND_LIMIT_ATTEMPT.csv",
        "needles": ["ELH1769_4_current_verdict", "CONDITIONAL_THEOREM_NOT_PARENT_PROOF"],
        "role": "after source-side narrowing, GR/Newton requires EH dominance/residual silence.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1839_SOURCE_REGISTER.csv",
    "source_shadow_ban_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1839_SOURCE_SHADOW_BAN_ATTEMPT.csv",
    "source_map_normal_form_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1839_SOURCE_MAP_NORMAL_FORM_STATUS.csv",
    "tauWEP_direct_product_source_row": RESIDUALS / "P8_Y5_PARENT_QLOC_1839_TAUWEP_DIRECT_PRODUCT_SOURCE_ROW.csv",
    "GR_bridge_handoff": RESIDUALS / "P8_Y5_PARENT_QLOC_1839_GR_BRIDGE_HANDOFF.csv",
    "current_corpus_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1839_CURRENT_CORPUS_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1839_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1839_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1839_VALIDATION.csv",
}


def ensure_dirs() -> None:
    for directory in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing_needles = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and not missing_needles,
                "missing_needles": ";".join(missing_needles),
                "role": source["role"],
            }
        )
    return rows


def source_shadow_ban_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SSB1839_0_identity_source_map",
            "claim_piece": "active ordinary source is total Hilbert/coframe source",
            "formal_statement": "T_active := T_H := delta S_matter/delta e_obs, with no independent F_shadow(T_H,labels).",
            "proof_result": "DERIVED_CONDITIONAL_THEOREM",
            "current_gap": "field equation must be parent-signed as Euler-Lagrange from one complete action with no admitted post-variation source map",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SSB1839_1_shadow_trichotomy",
            "claim_piece": "source-shadow classification",
            "formal_statement": "J_shadow is an Euler variation of a real action term, a boundary/improvement term, or a nonvariational/conserved residual.",
            "proof_result": "TRICHOTOMY_DERIVED",
            "current_gap": "every MTS source-like term must be classified in the parent action normal form",
            "current_status": "CLASSIFICATION_READY_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SSB1839_2_nonvariational_filter",
            "claim_piece": "nonvariational source-shadow rejection",
            "formal_statement": "nabla_mu E_LHS^{mu nu}=0 requires J_shadow to be action-owned, boundary-silent, separately conserved, or bounded.",
            "proof_result": "BIANCHI_FILTER_DERIVED",
            "current_gap": "separately conserved real blocks require arena exclusion or finite source-backed bounds",
            "current_status": "FILTER_NOT_BOUND",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SSB1839_3_current_verdict",
            "claim_piece": "source-shadow zero for current MTS",
            "formal_statement": "delta_w_shadow=0 and no post-Hilbert material/readout source map exists.",
            "proof_result": "NOT_PROVED_CURRENT_CORPUS",
            "current_gap": "normal-form signature is not a complete parent inventory; nonminimal, boundary, projector and decoupled blocks remain possible residuals",
            "current_status": "SOURCE_SHADOW_NOT_ZEROED",
            "valid_for_claim": False,
        },
    ]


def source_map_normal_form_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "normal_form_id": "SMNF1839_0_parent_action_partition",
            "object": "S_parent",
            "required_form": "S_geom + S_MTS + S_matter_min + S_nonmin + S_boundary",
            "current_status": "SIGNATURE_READY_PARENT_UNSIGNED",
            "remaining_input": "complete parent action inventory and sector variation table",
            "effect_if_signed": "source-looking terms have legal owners or become residual coefficient rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "normal_form_id": "SMNF1839_1_hilbert_source",
            "object": "T_H",
            "required_form": "T_H = delta S_matter_min / delta e_obs",
            "current_status": "CONDITIONAL_SOURCE_IDENTITY",
            "remaining_input": "identity-only source-map object-language signature",
            "effect_if_signed": "post-variation material source maps are forbidden",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "normal_form_id": "SMNF1839_2_shadow_residuals",
            "object": "J_shadow basis",
            "required_form": "J_shadow in {nonminimal, boundary, projector, decoupled, connection/torsion}",
            "current_status": "INVENTORY_READY_NONCLAIM",
            "remaining_input": "zero theorem, reclassification, or bound for every shadow channel",
            "effect_if_signed": "delta_w_shadow can be eliminated or scored",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "normal_form_id": "SMNF1839_3_GR_left_hand",
            "object": "E_LHS",
            "required_form": "E_LHS = G_munu + Lambda g_munu + DeltaE_munu",
            "current_status": "NEXT_BRIDGE_REQUIRED",
            "remaining_input": "EH dominance and residual-sector silence or operator coefficient pack",
            "effect_if_signed": "source-side cleanup can actually connect to GR/Newton",
            "valid_for_claim": False,
        },
    ]


def tauWEP_direct_product_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "source_row_id": "TDP1839_0_tau_WEP",
            "quantity": "tau_WEP",
            "definition": "N_eta^-1 <K_CMSM, S_Earth x M_TiPt> in one branch-locked linear readout convention",
            "formula": "eta_material_TiPt = Delta_w_TiPt * tau_WEP",
            "accepted_evidence": "official MICROSCOPE readout/design matrix, source worldtube, material tensor, product convention and same-branch C_parent/zero certificate",
            "current_value": "MISSING_OFFICIAL_READOUT_SOURCE_MATERIAL_PRODUCT",
            "units": "dimensionless projection factor",
            "source_path": str(MICROSCOPE_RESIDUALS / "R2FR_tau_WEP_route_1703.csv"),
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "source_row_id": "TDP1839_1_tau_min",
            "quantity": "tau_min",
            "definition": "strictly positive lower bound abs(tau_WEP)>=tau_min>0 for converting product bound into Delta_w width",
            "formula": "abs(Delta_w_TiPt) <= 2.8e-15/tau_min",
            "accepted_evidence": "source-backed nonzero projection computation or parent nondegeneracy theorem",
            "current_value": "MISSING_TAU_MIN",
            "units": "dimensionless",
            "source_path": str(MICROSCOPE_RESIDUALS / "R2FR_tau_WEP_readout_contract_nonclaim_1608.csv"),
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "source_row_id": "TDP1839_2_direct_product",
            "quantity": "P_WEP_source_weight",
            "definition": "direct parent product in the reported MICROSCOPE Ti/Pt channel",
            "formula": "P_WEP_source_weight = N_eta^-1 <K_CMSM, C_parent[S_Earth,M_TiPt]>",
            "accepted_evidence": "source-backed product theorem or official readout/source/material/product parser output with units, signs, hashes and branch lock",
            "current_value": "MISSING_DIRECT_PRODUCT_INPUTS",
            "units": "dimensionless eta contribution",
            "source_path": str(MICROSCOPE_RESIDUALS / "R2FR_direct_product_route_1703.csv"),
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "source_row_id": "TDP1839_3_product_bound_comparator",
            "quantity": "abs(Delta_w_TiPt * tau_WEP)",
            "definition": "source-backed MICROSCOPE product comparator",
            "formula": "abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15",
            "accepted_evidence": "comparison-side bound anchor only; not a prediction and not an inversion rule",
            "current_value": "BOUND_COMPARATOR_ONLY_NONCLAIM",
            "units": "dimensionless",
            "source_path": str(MICROSCOPE_RESIDUALS / "R2FR_tau_WEP_contraction_law_nonclaim_1596.csv"),
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "source_row_id": "TDP1839_4_refusal_guard",
            "quantity": "tau/direct shortcut guard",
            "definition": "anti-smuggling rule for WEP source/product rows",
            "formula": "reject tau_WEP=1, bound inversion, measured-G absorption, cancellation, surrogate arrays and mixed branch rows",
            "accepted_evidence": "branch-locked source-backed product rows only",
            "current_value": "REFUSAL_ACTIVE",
            "units": "not_applicable",
            "source_path": str(MICROSCOPE_RESIDUALS / "R2FR_direct_product_only_contract_1706.csv"),
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def GR_bridge_handoff_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "handoff_id": "GBH1839_0_source_side_status",
            "object": "source-side coupling",
            "status": "NARROWED_NOT_CLAIMED",
            "evidence": "source-shadow is classified by trichotomy and normal-form contract, but not parent-zeroed",
            "next_requirement": "do not claim WEP/local-GR until residuals are zeroed or bounded",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "handoff_id": "GBH1839_1_left_hand_gate",
            "object": "E_LHS Einstein/Newton bridge",
            "status": "NOW_PRIMARY_PRESSURE_POINT",
            "evidence": "1769 shows EH LHS plus clean Hilbert source gives Einstein/Poisson conditionally",
            "next_requirement": "prove EH dominance/residual-sector silence or stage operator coefficients",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "handoff_id": "GBH1839_2_tau_product_sidecar",
            "object": "tau_WEP/direct product",
            "status": "ACQUISITION_READY_NONCLAIM",
            "evidence": "tau/direct rows have exact required inputs but no official/source-backed files",
            "next_requirement": "defer empirical WEP scoring until parent definitions and official inputs exist",
            "valid_for_claim": False,
        },
    ]


def current_corpus_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1839_0_source_shadow_zero",
            "claim": "source-shadow/readout label re-entry is parent-forbidden",
            "gate_pass": False,
            "reason": "identity source-map and normal-form signatures remain parent-unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1839_1_tau_WEP",
            "claim": "tau_WEP is numeric or theorem-zero",
            "gate_pass": False,
            "reason": "official readout, source worldtube, material tensor, product convention and tau_min are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1839_2_direct_product",
            "claim": "direct WEP source product is score-ready",
            "gate_pass": False,
            "reason": "direct parent product or parser output is missing; bound inversion is refused",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1839_3_GR_bridge",
            "claim": "GR/Newton reduction follows from current source-side work",
            "gate_pass": False,
            "reason": "source-side narrowing is not enough without EH dominance, residual silence and source normalization",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1839_4_local_claim",
            "claim": "local GR/WEP/Newton branch is promoted",
            "gate_pass": False,
            "reason": "all relevant routes remain nonclaim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1839_0_source_shadow",
            "decision": "SOURCE_SHADOW_CLASSIFIED_NOT_ZEROED",
            "reason": "shadow terms are action, boundary/improvement, nonvariational residual, projector, or decoupled block; current corpus does not parent-eliminate all cases",
            "next_action": "retain delta_w_shadow/operator residual rows",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1839_1_tau_direct",
            "decision": "TAUWEP_DIRECT_PRODUCT_FIRST_SOURCE_ROW_STAGED_NONCLAIM",
            "reason": "tau_WEP/direct product inputs are explicit but missing official/source-backed files and parent product theorem",
            "next_action": "do not score WEP; keep acquisition sidecar ready",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1839_2_best_next",
            "decision": "EH_DOMINANCE_AND_OPERATOR_RESIDUAL_SILENCE_NEXT",
            "reason": "source-side coupling is now narrowed enough that the serious GR/Newton route depends on the left-hand Einstein operator limit",
            "next_action": "1840-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1839_0_primary",
            "next_target": "1840-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack.md",
            "script": "scripts/Y5_R2FR_EH_dominance_and_residual_sector_silence_or_operator_coefficient_pack.py",
            "objective": "prove MTS parent LHS reduces to EH/Einstein operator in the local branch by zeroing/suppressing residual sectors, or stage operator coefficients for PPN/R10/orbital/clock bounds",
            "selection_status": "selected",
            "success_condition": "EH dominance is parent-signed or every retained operator residual becomes an explicit nonclaim coefficient row",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1839_1_sidecar",
            "next_target": "1840b-Y5-R2FR-tauWEP-direct-product-parser-source-acquisition.md",
            "script": "scripts/Y5_R2FR_tauWEP_direct_product_parser_source_acquisition.py",
            "objective": "only after parent components are stable, acquire official readout/source/material/product rows for tau_WEP or direct product without scoring",
            "selection_status": "held_sidecar",
            "success_condition": "official/source-backed WEP inputs exist with units, hashes, branch locks and valid_for_claim=false",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "source_shadow_ban_attempt": source_shadow_ban_rows(),
        "source_map_normal_form_status": source_map_normal_form_rows(),
        "tauWEP_direct_product_source_row": tauWEP_direct_product_rows(),
        "GR_bridge_handoff": GR_bridge_handoff_rows(),
        "current_corpus_gate": current_corpus_gate_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def copy_csvs(paths: list[Path]) -> None:
    for path in paths:
        for directory in [MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
            directory.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, directory / path.name)


def csv_parse_ok(paths: list[Path]) -> bool:
    try:
        for path in paths:
            with path.open("r", encoding="utf-8", newline="") as handle:
                list(csv.DictReader(handle))
    except Exception:
        return False
    return True


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    guarded_keys = {"valid_for_claim", "claim_allowed", "gate_pass", "score_ready"}
    for rows in rows_map.values():
        for row in rows:
            for guarded_key in guarded_keys.intersection(row):
                if str(row[guarded_key]).lower() == "true":
                    return False
    return True


def no_formalization_outputs() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        name = path.name
        if "1839-Y5-R2FR" in name or name.startswith("P8_Y5_PARENT_QLOC_1839") or name.startswith("P8_Y5_BRR545_1839"):
            return False
    return True


def branch_copies_exist(paths: list[Path]) -> bool:
    for path in paths:
        for directory in [MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
            if not (directory / path.name).exists():
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]], copied_paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    output_paths = [OUTPUTS[key] for key in rows_map.keys()]
    shadow_rows = rows_map["source_shadow_ban_attempt"]
    tau_rows = rows_map["tauWEP_direct_product_source_row"]
    bridge_rows = rows_map["GR_bridge_handoff"]
    gate_rows = rows_map["current_corpus_gate"]
    checks: list[tuple[str, bool, str]] = [
        ("VAL1839_0_sources_exist", all(str(row["exists"]).lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL1839_1_needles_present", all(str(row["needles_present"]).lower() == "true" for row in source_rows), "all cited source needles are present"),
        (
            "VAL1839_2_source_shadow_not_zeroed",
            any(row["attempt_id"] == "SSB1839_3_current_verdict" and row["current_status"] == "SOURCE_SHADOW_NOT_ZEROED" for row in shadow_rows),
            "source-shadow remains classified but not zeroed",
        ),
        (
            "VAL1839_3_tau_direct_rows_present",
            {"TDP1839_0_tau_WEP", "TDP1839_2_direct_product", "TDP1839_4_refusal_guard"}.issubset({row["source_row_id"] for row in tau_rows}),
            "tau_WEP, direct-product and refusal rows are present",
        ),
        (
            "VAL1839_4_tau_direct_nonclaim",
            all(row["valid_for_claim"] is False and row["score_ready"] is False for row in tau_rows),
            "all tau/direct rows remain nonclaim and not score-ready",
        ),
        (
            "VAL1839_5_GR_bridge_handoff",
            any(row["handoff_id"] == "GBH1839_1_left_hand_gate" and row["status"] == "NOW_PRIMARY_PRESSURE_POINT" for row in bridge_rows),
            "GR left-hand gate is selected as pressure point",
        ),
        (
            "VAL1839_6_current_gates_block",
            all(row["gate_pass"] is False and row["claim_allowed"] is False for row in gate_rows),
            "all current corpus gates remain blocked/nonclaim",
        ),
        (
            "VAL1839_7_next_selected",
            any(row["route_id"] == "NEXT1839_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selects EH dominance/residual-sector silence",
        ),
        ("VAL1839_8_no_claim_flags", no_claim_flags(rows_map), "no generated claim flags are true"),
        ("VAL1839_9_csv_parse", csv_parse_ok(output_paths), "all generated 1839 CSVs parse"),
        ("VAL1839_10_branch_copies", branch_copies_exist(copied_paths), "branch/quarantine/queue copies exist"),
        ("VAL1839_11_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1839_12_formalization_untouched", no_formalization_outputs(), "no 1839 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1839_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1839 source-shadow ban or tauWEP/direct-product first source row checkpoint",
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
            "# 1839 Y5 R2FR source-shadow ban or tauWEP direct-product first source row",
            "",
            "**Progress:** 1839 consolidates the source-shadow result. A shadow source is no longer a vague coupling loophole: it must be an action term, a boundary/improvement term, a nonvariational/conserved residual, a projector, or a decoupled block. Current MTS still does not parent-eliminate every case, so the zero claim is refused.",
            "",
            "**Current verdict:** source-shadow is classified but not killed. `tau_WEP` and the direct WEP source product are staged as acquisition-ready nonclaim rows, but no WEP score is allowed. The next serious derivation target is the left-hand Einstein/Newton operator limit.",
            "",
            "**Claim ceiling:** no source-shadow zero claim, no tau shortcut, no direct-product score, no WEP pass, no local GR/Newton promotion, no GitHub action, and no `formalization-workbench` edit is allowed from 1839.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Source-Shadow Ban Attempt",
            markdown_table(rows_map["source_shadow_ban_attempt"], ["attempt_id", "claim_piece", "formal_statement", "proof_result", "current_gap", "current_status", "valid_for_claim"]),
            "",
            "## Source-Map Normal Form Status",
            markdown_table(rows_map["source_map_normal_form_status"], ["normal_form_id", "object", "required_form", "current_status", "remaining_input", "effect_if_signed", "valid_for_claim"]),
            "",
            "## tauWEP Direct Product Source Row",
            markdown_table(rows_map["tauWEP_direct_product_source_row"], ["source_row_id", "quantity", "definition", "formula", "accepted_evidence", "current_value", "units", "source_path", "score_ready", "valid_for_claim"]),
            "",
            "## GR Bridge Handoff",
            markdown_table(rows_map["GR_bridge_handoff"], ["handoff_id", "object", "status", "evidence", "next_requirement", "valid_for_claim"]),
            "",
            "## Current Corpus Gate",
            markdown_table(rows_map["current_corpus_gate"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
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
            "This is a clean tactical handoff. The source side is no longer the foggiest part: it has named residuals and strict refusal rows. The project now has to attack the left-hand operator: prove EH dominance/residual silence, or accept that MTS predicts explicit non-EH operator coefficients to be bounded by PPN, R10, clocks, orbital systems, and cosmology.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = rows_by_key()
    nonvalidation_paths: list[Path] = []
    for key, rows in rows_map.items():
        path = OUTPUTS[key]
        write_csv(path, rows)
        nonvalidation_paths.append(path)
    copy_csvs(nonvalidation_paths)
    validation_rows = build_validation(rows_map, nonvalidation_paths)
    write_csv(OUTPUTS["validation"], validation_rows)
    copy_csvs([OUTPUTS["validation"]])
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1839 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
