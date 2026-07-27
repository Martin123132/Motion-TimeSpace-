from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3085"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3085-Y5-R2FR-source-shadow-ban-or-tauWEP-direct-product-first-source-row-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3085_00_3084_doc": ROOT
    / "3084-Y5-R2FR-ordinary-matter-action-signature-source-label-forgetting-or-WEP-bound-first-fill-under-AX1090.md",
    "SRC3085_01_3084_next": RESIDUALS / "P8_Y5_R2FR_3084_NEXT_TARGET.csv",
    "SRC3085_02_3084_shadow": RESIDUALS / "P8_Y5_R2FR_3084_SOURCE_SHADOW_ESCAPE_LEDGER.csv",
    "SRC3085_03_3084_first_wep": RESIDUALS / "P8_Y5_R2FR_3084_FIRST_WEP_COMPONENT_BOUND_INPUT_NONCLAIM.csv",
    "SRC3085_04_3084_source_label": RESIDUALS / "P8_Y5_R2FR_3084_SOURCE_LABEL_FORGETTING_GATE.csv",
    "SRC3085_05_1839_doc": ROOT / "1839-Y5-R2FR-source-shadow-ban-or-tauWEP-direct-product-first-source-row.md",
    "SRC3085_06_1839_shadow_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1839_SOURCE_SHADOW_BAN_ATTEMPT.csv",
    "SRC3085_07_1839_normal_form": RESIDUALS / "P8_Y5_PARENT_QLOC_1839_SOURCE_MAP_NORMAL_FORM_STATUS.csv",
    "SRC3085_08_1839_tau_direct": RESIDUALS / "P8_Y5_PARENT_QLOC_1839_TAUWEP_DIRECT_PRODUCT_SOURCE_ROW.csv",
    "SRC3085_09_1839_gr_handoff": RESIDUALS / "P8_Y5_PARENT_QLOC_1839_GR_BRIDGE_HANDOFF.csv",
    "SRC3085_10_1767_source_identity": RESIDUALS / "P8_Y5_PARENT_QLOC_1767_SINGLE_SOURCE_MAP_IDENTITY_THEOREM.csv",
    "SRC3085_11_1768_source_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_SOURCE_MAP_IDENTITY_GATE.csv",
    "SRC3085_12_tau_route": MICROSCOPE / "branch_locked_wep" / "residuals" / "R2FR_tau_WEP_route_1703.csv",
    "SRC3085_13_tau_readout_contract": MICROSCOPE
    / "branch_locked_wep"
    / "residuals"
    / "R2FR_tau_WEP_readout_contract_nonclaim_1608.csv",
    "SRC3085_14_direct_route": MICROSCOPE
    / "branch_locked_wep"
    / "residuals"
    / "R2FR_direct_product_route_1703.csv",
    "SRC3085_15_direct_contract": MICROSCOPE
    / "branch_locked_wep"
    / "residuals"
    / "R2FR_direct_product_only_contract_1706.csv",
    "SRC3085_16_tau_contraction": MICROSCOPE
    / "branch_locked_wep"
    / "residuals"
    / "R2FR_tau_WEP_contraction_law_nonclaim_1596.csv",
    "SRC3085_17_1840_old_next": ROOT
    / "1840-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack.md",
    "SRC3085_18_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3085_SOURCE_REGISTER.csv",
    "shadow_attempt": RESIDUALS / "P8_Y5_R2FR_3085_SOURCE_SHADOW_BAN_ATTEMPT.csv",
    "normal_form": RESIDUALS / "P8_Y5_R2FR_3085_SOURCE_MAP_NORMAL_FORM_STATUS.csv",
    "tau_direct": RESIDUALS / "P8_Y5_R2FR_3085_TAUWEP_DIRECT_PRODUCT_SOURCE_ROW_NONCLAIM.csv",
    "gr_handoff": RESIDUALS / "P8_Y5_R2FR_3085_GR_BRIDGE_HANDOFF.csv",
    "corpus_gate": RESIDUALS / "P8_Y5_R2FR_3085_CURRENT_CORPUS_GATE.csv",
    "score_blockers": RESIDUALS / "P8_Y5_R2FR_3085_SCORE_BLOCKER_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3085_DECISION_LEDGER.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3085_CLAIM_STATUS.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3085_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3085_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3085_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "shadow_attempt_copy": LOCAL_BOUNDS / "source_shadow_ban_attempt_3085_NONCLAIM.csv",
    "normal_form_copy": LOCAL_BOUNDS / "source_map_normal_form_3085_NONCLAIM.csv",
    "tau_direct_copy": LOCAL_BOUNDS / "tauWEP_direct_product_source_row_3085_NONCLAIM.csv",
    "gr_handoff_copy": LOCAL_BOUNDS / "GR_bridge_handoff_3085_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3085_EH_dominance_operator_residual_NEXT_NONCLAIM.csv",
}

for output_path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    output_path.parent.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


def file_hash(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "passed"}


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def row_count(path: Path) -> int:
    if not path.exists():
        return 0
    if path.suffix.lower() == ".csv":
        return len(rows(path))
    return len(path.read_text(encoding="utf-8").splitlines())


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for output_row in output_rows:
            writer.writerow({key: output_row.get(key, "") for key in fieldnames})


def under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def has_claim_true(input_rows: list[dict[str, Any]]) -> bool:
    claim_fields = {
        "valid_for_claim",
        "claim_allowed",
        "valid_prediction_row",
        "score_ready",
        "claim_active",
        "gate_pass",
        "score_allowed",
        "operator_ready",
        "source_shadow_zero",
        "numeric_ready",
        "bridge_claim",
    }
    for input_row in input_rows:
        for field in claim_fields:
            if field in input_row and boolish(input_row[field]):
                return True
    return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": "false",
        "valid_prediction_row": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(table_rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not table_rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for table_row in table_rows:
        lines.append("| " + " | ".join(md_escape(table_row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def copy_csv(source_path: Path, destination_path: Path) -> None:
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_path, destination_path)


remove_pycache()
dotg_hash_before = file_hash(DOTG_TARGET)

source_register = [
    base(
        {
            "source_id": source_id,
            "source_path": str(source_path),
            "exists": str(source_path.exists()),
            "parse_ok": str(source_parse_ok(source_path)),
            "row_count": row_count(source_path),
            "role": "source_shadow_tau_direct_evidence"
            if source_id != "SRC3085_18_dotg_target"
            else "append_guard_target",
            "status": "PRESENT" if source_path.exists() else "MISSING_SOURCE",
        }
    )
    for source_id, source_path in SOURCE_PATHS.items()
]

shadow_attempt_rows = [
    base(
        {
            "attempt_id": "SSB3085_0_identity_source_map",
            "claim_piece": "active ordinary source is total Hilbert/coframe source",
            "formal_statement": "T_active := T_H := delta S_matter/delta e_obs, with no independent F_shadow(T_H,labels).",
            "proof_result": "DERIVED_CONDITIONAL_THEOREM",
            "current_gap": "field equation must be parent-signed as Euler-Lagrange from one complete action with no admitted post-variation source map",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "source_shadow_zero": "false",
        }
    ),
    base(
        {
            "attempt_id": "SSB3085_1_shadow_trichotomy",
            "claim_piece": "source-shadow classification",
            "formal_statement": "J_shadow is an Euler variation of a real action term, a boundary/improvement term, a projector/readout term, a decoupled block, or a nonvariational/conserved residual.",
            "proof_result": "TRICHOTOMY_DERIVED",
            "current_gap": "every MTS source-like term must be classified in the parent action normal form",
            "current_status": "CLASSIFICATION_READY_NONCLAIM",
            "source_shadow_zero": "false",
        }
    ),
    base(
        {
            "attempt_id": "SSB3085_2_nonvariational_filter",
            "claim_piece": "nonvariational source-shadow rejection",
            "formal_statement": "nabla_mu E_LHS^{mu nu}=0 requires J_shadow to be action-owned, boundary-silent, separately conserved, or bounded.",
            "proof_result": "BIANCHI_FILTER_DERIVED",
            "current_gap": "separately conserved real blocks require arena exclusion or finite source-backed bounds",
            "current_status": "FILTER_NOT_BOUND",
            "source_shadow_zero": "false",
        }
    ),
    base(
        {
            "attempt_id": "SSB3085_3_current_verdict",
            "claim_piece": "source-shadow zero for current MTS",
            "formal_statement": "delta_w_shadow=0 and no post-Hilbert material/readout source map exists.",
            "proof_result": "NOT_PROVED_CURRENT_CORPUS",
            "current_gap": "normal-form signature is not a complete parent inventory; nonminimal, boundary, projector and decoupled blocks remain possible residuals",
            "current_status": "SOURCE_SHADOW_NOT_ZEROED",
            "source_shadow_zero": "false",
        }
    ),
]

normal_form_rows = [
    base(
        {
            "normal_form_id": "SMNF3085_0_parent_action_partition",
            "object": "S_parent",
            "required_form": "S_geom + S_MTS + S_matter_min + S_nonmin + S_boundary + S_readout_rule",
            "current_status": "SIGNATURE_READY_PARENT_UNSIGNED",
            "remaining_input": "complete parent action inventory and sector variation table",
            "effect_if_signed": "source-looking terms have legal owners or become residual coefficient rows",
        }
    ),
    base(
        {
            "normal_form_id": "SMNF3085_1_hilbert_source",
            "object": "T_H",
            "required_form": "T_H = delta S_matter_min / delta e_obs",
            "current_status": "CONDITIONAL_SOURCE_IDENTITY",
            "remaining_input": "identity-only source-map object-language signature",
            "effect_if_signed": "post-variation material source maps are forbidden",
        }
    ),
    base(
        {
            "normal_form_id": "SMNF3085_2_shadow_residuals",
            "object": "J_shadow basis",
            "required_form": "J_shadow in {nonminimal, boundary, projector, decoupled, connection/torsion}",
            "current_status": "INVENTORY_READY_NONCLAIM",
            "remaining_input": "zero theorem, reclassification, or bound for every shadow channel",
            "effect_if_signed": "delta_w_shadow can be eliminated or scored",
        }
    ),
    base(
        {
            "normal_form_id": "SMNF3085_3_GR_left_hand",
            "object": "E_LHS",
            "required_form": "E_LHS = G_munu + Lambda g_munu + DeltaE_munu",
            "current_status": "NEXT_BRIDGE_REQUIRED",
            "remaining_input": "EH dominance and residual-sector silence or operator coefficient pack",
            "effect_if_signed": "source-side cleanup can actually connect to GR/Newton",
        }
    ),
]

tau_direct_rows = [
    base(
        {
            "source_row_id": "TDP3085_0_tau_WEP",
            "quantity": "tau_WEP",
            "definition": "N_eta^-1 <K_CMSM, S_Earth x M_TiPt> in one branch-locked linear readout convention",
            "formula": "eta_material_TiPt = Delta_w_TiPt * tau_WEP",
            "accepted_evidence": "official MICROSCOPE readout/design matrix, source worldtube, material tensor, product convention and same-branch C_parent/zero certificate",
            "current_value": "MISSING_OFFICIAL_READOUT_SOURCE_MATERIAL_PRODUCT",
            "units": "dimensionless projection factor",
            "source_path": str(SOURCE_PATHS["SRC3085_12_tau_route"]),
            "numeric_ready": "false",
        }
    ),
    base(
        {
            "source_row_id": "TDP3085_1_tau_min",
            "quantity": "tau_min",
            "definition": "strictly positive lower bound abs(tau_WEP)>=tau_min>0 for converting product bound into Delta_w width",
            "formula": "abs(Delta_w_TiPt) <= eta_bound/tau_min",
            "accepted_evidence": "source-backed nonzero projection computation or parent nondegeneracy theorem",
            "current_value": "MISSING_TAU_MIN",
            "units": "dimensionless",
            "source_path": str(SOURCE_PATHS["SRC3085_13_tau_readout_contract"]),
            "numeric_ready": "false",
        }
    ),
    base(
        {
            "source_row_id": "TDP3085_2_direct_product",
            "quantity": "P_WEP_source_weight",
            "definition": "direct parent product in the reported WEP Ti/Pt channel",
            "formula": "P_WEP_source_weight = N_eta^-1 <K_CMSM, C_parent[S_Earth,M_TiPt]>",
            "accepted_evidence": "source-backed product theorem or official readout/source/material/product parser output with units, signs, hashes and branch lock",
            "current_value": "MISSING_DIRECT_PRODUCT_INPUTS",
            "units": "dimensionless eta contribution",
            "source_path": str(SOURCE_PATHS["SRC3085_14_direct_route"]),
            "numeric_ready": "false",
        }
    ),
    base(
        {
            "source_row_id": "TDP3085_3_product_bound_comparator",
            "quantity": "abs(Delta_w_TiPt * tau_WEP)",
            "definition": "source-backed WEP product comparator",
            "formula": "abs(Delta_w_TiPt * tau_WEP) <= eta_bound",
            "accepted_evidence": "comparison-side bound anchor only; not a prediction and not an inversion rule",
            "current_value": "BOUND_COMPARATOR_ONLY_NONCLAIM",
            "units": "dimensionless",
            "source_path": str(SOURCE_PATHS["SRC3085_16_tau_contraction"]),
            "numeric_ready": "false",
        }
    ),
    base(
        {
            "source_row_id": "TDP3085_4_refusal_guard",
            "quantity": "tau/direct shortcut guard",
            "definition": "anti-smuggling rule for WEP source/product rows",
            "formula": "reject tau_WEP=1, bound inversion, measured-G absorption, cancellation, surrogate arrays and mixed branch rows",
            "accepted_evidence": "branch-locked source-backed product rows only",
            "current_value": "REFUSAL_ACTIVE",
            "units": "not_applicable",
            "source_path": str(SOURCE_PATHS["SRC3085_15_direct_contract"]),
            "numeric_ready": "false",
        }
    ),
]

gr_handoff_rows = [
    base(
        {
            "handoff_id": "GBH3085_0_source_side_status",
            "object": "source-side coupling",
            "status": "NARROWED_NOT_CLAIMED",
            "evidence": "source-shadow is classified by trichotomy and normal-form contract, but not parent-zeroed",
            "next_requirement": "do not claim WEP/local-GR until residuals are zeroed or bounded",
            "bridge_claim": "false",
        }
    ),
    base(
        {
            "handoff_id": "GBH3085_1_left_hand_gate",
            "object": "E_LHS Einstein/Newton bridge",
            "status": "NOW_PRIMARY_PRESSURE_POINT",
            "evidence": "old 1839/1840 trail selects EH dominance plus clean Hilbert source as the Einstein/Poisson route",
            "next_requirement": "prove EH dominance/residual-sector silence or stage operator coefficients",
            "bridge_claim": "false",
        }
    ),
    base(
        {
            "handoff_id": "GBH3085_2_tau_product_sidecar",
            "object": "tau_WEP/direct product",
            "status": "ACQUISITION_READY_NONCLAIM",
            "evidence": "tau/direct rows have exact required inputs but no official/source-backed files",
            "next_requirement": "defer empirical WEP scoring until parent definitions and official inputs exist",
            "bridge_claim": "false",
        }
    ),
]

corpus_gate_rows = [
    base(
        {
            "gate_id": "CG3085_0_source_shadow_zero",
            "claim": "source-shadow/readout label re-entry is parent-forbidden",
            "gate_pass": "false",
            "reason": "identity source-map and normal-form signatures remain parent-unsigned",
        }
    ),
    base(
        {
            "gate_id": "CG3085_1_tau_WEP",
            "claim": "tau_WEP is numeric or theorem-zero",
            "gate_pass": "false",
            "reason": "official readout, source worldtube, material tensor, product convention and tau_min are missing",
        }
    ),
    base(
        {
            "gate_id": "CG3085_2_direct_product",
            "claim": "direct WEP source product is score-ready",
            "gate_pass": "false",
            "reason": "direct parent product or parser output is missing; bound inversion is refused",
        }
    ),
    base(
        {
            "gate_id": "CG3085_3_GR_bridge",
            "claim": "GR/Newton reduction follows from current source-side work",
            "gate_pass": "false",
            "reason": "source-side narrowing is not enough without EH dominance, residual silence and source normalization",
        }
    ),
    base(
        {
            "gate_id": "CG3085_4_local_claim",
            "claim": "local GR/WEP/Newton branch is promoted",
            "gate_pass": "false",
            "reason": "all relevant routes remain nonclaim",
        }
    ),
]

score_blocker_rows = [
    base(
        {
            "blocker_id": "SBL3085_0_shadow_inventory",
            "blocks": "source-shadow zero",
            "missing": "complete parent action inventory classifying every source-like term",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
    base(
        {
            "blocker_id": "SBL3085_1_tau_inputs",
            "blocks": "tau_WEP branch",
            "missing": "official readout/design matrix, source worldtube, material tensor and tau_min",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
    base(
        {
            "blocker_id": "SBL3085_2_direct_product",
            "blocks": "direct WEP product branch",
            "missing": "parent product theorem or source-backed parser output with branch lock",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
    base(
        {
            "blocker_id": "SBL3085_3_EH_left_hand",
            "blocks": "local GR/Newton bridge",
            "missing": "EH dominance and residual-sector silence/operator coefficient pack",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3085_0_shadow_result",
            "decision": "SOURCE_SHADOW_CLASSIFIED_NOT_ZEROED",
            "reason": "source-shadow must be action-owned, boundary/improvement, projector/readout, decoupled, or nonvariational/conserved residual, but the parent inventory is incomplete",
            "next_action": "do not set delta_w_shadow=0",
        }
    ),
    base(
        {
            "decision_id": "DEC3085_1_tau_direct",
            "decision": "TAUWEP_DIRECT_PRODUCT_FIRST_SOURCE_ROW_STAGED_NONCLAIM",
            "reason": "tau_WEP/direct product inputs are explicit but missing official/source-backed files and parent product theorem",
            "next_action": "do not score WEP; keep acquisition sidecar ready",
        }
    ),
    base(
        {
            "decision_id": "DEC3085_2_best_next",
            "decision": "EH_DOMINANCE_AND_OPERATOR_RESIDUAL_SILENCE_NEXT",
            "reason": "source-side coupling is now narrowed enough that the serious GR/Newton route depends on the left-hand Einstein operator limit",
            "next_action": "3086-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack-under-AX1090.md",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3085_0_source_shadow_zero",
            "claim": "source-shadow/readout label re-entry is zero",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "normal-form parent inventory remains incomplete",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3085_1_tau_direct",
            "claim": "tau_WEP or direct product is score-ready",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "official/source-backed product inputs are missing",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3085_2_WEP",
            "claim": "WEP branch passes",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "WEP inputs remain acquisition-ready but invalid for claim",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3085_3_local_GR",
            "claim": "local GR/Newton recovery follows",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "left-hand EH/operator reduction is still unresolved",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3085_0_3086",
            "next_checkpoint": "3086-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack-under-AX1090.md",
            "script": "scripts/Y5_R2FR_EH_dominance_and_residual_sector_silence_or_operator_coefficient_pack_under_AX1090_3086.py",
            "mission": "prove the MTS parent left-hand operator reduces to Einstein-Hilbert/Einstein in the local branch by zeroing or suppressing residual sectors, or stage operator coefficients for PPN/R10/orbital/clock bounds",
            "starting_equation": "E_LHS = G_munu + Lambda g_munu + DeltaE_munu; require DeltaE_munu=0 or bounded in local arenas",
            "claim_policy": "no GR/Newton claim until EH dominance, residual-sector silence/operator bounds, source normalization and WEP/readout gates are all signed or source-backed",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["shadow_attempt"], shadow_attempt_rows)
write_csv(OUTPUTS["normal_form"], normal_form_rows)
write_csv(OUTPUTS["tau_direct"], tau_direct_rows)
write_csv(OUTPUTS["gr_handoff"], gr_handoff_rows)
write_csv(OUTPUTS["corpus_gate"], corpus_gate_rows)
write_csv(OUTPUTS["score_blockers"], score_blocker_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["shadow_attempt"], BRANCH_OUTPUTS["shadow_attempt_copy"])
copy_csv(OUTPUTS["normal_form"], BRANCH_OUTPUTS["normal_form_copy"])
copy_csv(OUTPUTS["tau_direct"], BRANCH_OUTPUTS["tau_direct_copy"])
copy_csv(OUTPUTS["gr_handoff"], BRANCH_OUTPUTS["gr_handoff_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "source_path": str(source_path),
            "copy_path": str(copy_path),
            "copy_exists": str(copy_path.exists()),
            "copy_parse_ok": str(csv_ok(copy_path)),
            "status": "BRANCH_COPY_READY_NONCLAIM" if copy_path.exists() else "BRANCH_COPY_MISSING",
        }
    )
    for copy_id, source_path, copy_path in [
        ("BR3085_0_shadow_attempt", OUTPUTS["shadow_attempt"], BRANCH_OUTPUTS["shadow_attempt_copy"]),
        ("BR3085_1_normal_form", OUTPUTS["normal_form"], BRANCH_OUTPUTS["normal_form_copy"]),
        ("BR3085_2_tau_direct", OUTPUTS["tau_direct"], BRANCH_OUTPUTS["tau_direct_copy"]),
        ("BR3085_3_gr_handoff", OUTPUTS["gr_handoff"], BRANCH_OUTPUTS["gr_handoff_copy"]),
        ("BR3085_4_next", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
]
write_csv(OUTPUTS["branches"], branch_rows)

DOC.write_text("# 3085 - Source Shadow Ban\n\nPreparing validation.\n", encoding="utf-8")

dotg_hash_after = file_hash(DOTG_TARGET)
generated_csvs = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
generated_rows = (
    source_register
    + shadow_attempt_rows
    + normal_form_rows
    + tau_direct_rows
    + gr_handoff_rows
    + corpus_gate_rows
    + score_blocker_rows
    + decision_rows
    + claim_rows
    + next_rows
    + branch_rows
)
formalization_output_count = sum(1 for output_path in generated_csvs + [DOC] if under(output_path, FORMALIZATION))
required_shadow_ids = {
    "SSB3085_0_identity_source_map",
    "SSB3085_1_shadow_trichotomy",
    "SSB3085_2_nonvariational_filter",
    "SSB3085_3_current_verdict",
}
required_normal_ids = {
    "SMNF3085_0_parent_action_partition",
    "SMNF3085_1_hilbert_source",
    "SMNF3085_2_shadow_residuals",
    "SMNF3085_3_GR_left_hand",
}
required_tau_ids = {
    "TDP3085_0_tau_WEP",
    "TDP3085_1_tau_min",
    "TDP3085_2_direct_product",
    "TDP3085_3_product_bound_comparator",
    "TDP3085_4_refusal_guard",
}
required_gr_ids = {
    "GBH3085_0_source_side_status",
    "GBH3085_1_left_hand_gate",
    "GBH3085_2_tau_product_sidecar",
}
shadow_verdict = next(row for row in shadow_attempt_rows if row["attempt_id"] == "SSB3085_3_current_verdict")
left_hand_gate = next(row for row in gr_handoff_rows if row["handoff_id"] == "GBH3085_1_left_hand_gate")

validation_rows = [
    base(
        {
            "validation_id": "VAL3085_00_sources_exist",
            "passed": str(all(row["exists"] == "True" for row in source_register)),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3085_01_sources_parse",
            "passed": str(all(row["parse_ok"] == "True" for row in source_register)),
            "requirement": "all cited CSV sources parse and markdown sources exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3085_02_csv_parse",
            "passed": str(all(csv_ok(output_path) for output_path in generated_csvs if output_path != OUTPUTS["validation"])),
            "requirement": "all generated and branch-copy CSVs parse cleanly before validation write",
            "evidence": "csv.DictReader parse check",
        }
    ),
    base(
        {
            "validation_id": "VAL3085_03_shadow_attempt_complete",
            "passed": str(required_shadow_ids.issubset({row["attempt_id"] for row in shadow_attempt_rows}) and not has_claim_true(shadow_attempt_rows)),
            "requirement": "source-shadow identity, trichotomy, Bianchi filter and current verdict rows are present and nonclaim",
            "evidence": OUTPUTS["shadow_attempt"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3085_04_shadow_zero_refused",
            "passed": str(shadow_verdict["current_status"] == "SOURCE_SHADOW_NOT_ZEROED" and shadow_verdict["source_shadow_zero"] == "false"),
            "requirement": "source-shadow zero is not promoted",
            "evidence": OUTPUTS["shadow_attempt"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3085_05_normal_form_complete",
            "passed": str(required_normal_ids.issubset({row["normal_form_id"] for row in normal_form_rows}) and not has_claim_true(normal_form_rows)),
            "requirement": "source-map normal form covers parent action partition, Hilbert source, shadow residuals and GR left-hand bridge",
            "evidence": OUTPUTS["normal_form"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3085_06_tau_direct_rows_present_nonclaim",
            "passed": str(required_tau_ids.issubset({row["source_row_id"] for row in tau_direct_rows}) and not has_claim_true(tau_direct_rows)),
            "requirement": "tau_WEP, tau_min, direct product, product comparator and refusal guard rows are present as nonclaim",
            "evidence": OUTPUTS["tau_direct"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3085_07_gr_handoff_selected",
            "passed": str(required_gr_ids.issubset({row["handoff_id"] for row in gr_handoff_rows}) and left_hand_gate["status"] == "NOW_PRIMARY_PRESSURE_POINT" and not has_claim_true(gr_handoff_rows)),
            "requirement": "GR bridge handoff selects EH left-hand gate without promoting a claim",
            "evidence": OUTPUTS["gr_handoff"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3085_08_current_gates_block",
            "passed": str(not has_claim_true(corpus_gate_rows) and all(row["gate_pass"] == "false" for row in corpus_gate_rows)),
            "requirement": "all current corpus gates remain blocked/nonclaim",
            "evidence": OUTPUTS["corpus_gate"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3085_09_score_blockers_active",
            "passed": str(not has_claim_true(score_blocker_rows) and all(row["status"] == "BLOCKS_SCORE" for row in score_blocker_rows)),
            "requirement": "shadow inventory, tau inputs, direct product and EH left-hand blockers remain active",
            "evidence": OUTPUTS["score_blockers"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3085_10_no_claim_promoted",
            "passed": str(not has_claim_true(generated_rows)),
            "requirement": "no source-shadow, tau/direct product, WEP, local-GR or Newton claim is promoted",
            "evidence": "claim field scan",
        }
    ),
    base(
        {
            "validation_id": "VAL3085_11_next_target_selected",
            "passed": str(next_rows[0]["next_checkpoint"].startswith("3086-Y5-R2FR-EH-dominance")),
            "requirement": "next target moves to EH dominance and residual-sector silence/operator coefficient pack",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3085_12_branch_copies_exist",
            "passed": str(all(row["copy_exists"] == "True" and row["copy_parse_ok"] == "True" for row in branch_rows)),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3085_13_dotg_unchanged",
            "passed": str(dotg_hash_before == dotg_hash_after),
            "requirement": "P8_time_drift_residual_or_zero.csv is not modified",
            "evidence": f"{dotg_hash_before}->{dotg_hash_after}",
        }
    ),
    base(
        {
            "validation_id": "VAL3085_14_outputs_under_post_checkpoint",
            "passed": str(all(under(output_path, ROOT) for output_path in generated_csvs + [DOC])),
            "requirement": "all outputs are under post-checkpoint-work",
            "evidence": "path containment check",
        }
    ),
    base(
        {
            "validation_id": "VAL3085_15_no_formalization_outputs",
            "passed": str(formalization_output_count == 0),
            "requirement": "formalization-workbench modified-file count for 3085 outputs remains zero",
            "evidence": f"formalization_3085_output_paths={formalization_output_count}",
        }
    ),
    base(
        {
            "validation_id": "VAL3085_16_pycache_absent",
            "passed": str(not PYCACHE.exists()),
            "requirement": "scripts __pycache__ is absent at generator completion",
            "evidence": str(PYCACHE),
        }
    ),
    base(
        {
            "validation_id": "VAL3085_17_doc_written",
            "passed": str(DOC.exists()),
            "requirement": "checkpoint markdown document is written",
            "evidence": str(DOC),
        }
    ),
]

write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3085 - Source-Shadow Ban or tau_WEP/Direct Product First Source Row

Status: `Y5_R2FR_3085_source_shadow_classified_tau_direct_nonclaim_EH_next`

Generated: `{RUN_UTC}`

## Verdict

3085 closes the current WEP source-side sweep as far as it can honestly go right now.

The useful result is that source-shadow is no longer vague. Any label re-entry must be one of a finite set of objects: an action-owned term, a boundary/improvement term, a projector/readout term, a decoupled block, or a nonvariational/conserved residual.

The hard result is that the current corpus does **not** parent-eliminate all of those cases. Therefore `delta_w_shadow=0`, `tau_WEP`, direct WEP product, WEP pass, and local GR/Newton recovery are not claimed.

The sidecar empirical route is now clean: `tau_WEP`, `tau_min`, direct product, product comparator, and refusal guard rows are acquisition-ready. But they remain nonclaim until sourced with official/readout/material/product inputs and branch locks.

The next serious pressure point is the left-hand operator: prove EH dominance and residual-sector silence, or stage operator coefficient rows. Source-side narrowing alone cannot deliver GR reduction.

## Source-Shadow Ban Attempt

{md_table(shadow_attempt_rows, ["attempt_id", "claim_piece", "proof_result", "current_status", "source_shadow_zero"])}

## Source-Map Normal Form

{md_table(normal_form_rows, ["normal_form_id", "object", "required_form", "current_status", "remaining_input"])}

## tau_WEP / Direct Product Source Rows

{md_table(tau_direct_rows, ["source_row_id", "quantity", "formula", "current_value", "numeric_ready"])}

## GR Bridge Handoff

{md_table(gr_handoff_rows, ["handoff_id", "object", "status", "next_requirement", "bridge_claim"])}

## Current Corpus Gate

{md_table(corpus_gate_rows, ["gate_id", "claim", "gate_pass", "reason"])}

## Score Blockers

{md_table(score_blocker_rows, ["blocker_id", "blocks", "missing", "status"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "reason", "next_action"])}

## Claim Status

{md_table(claim_rows, ["claim_id", "claim", "claim_active", "status", "reason"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "claim_policy"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files

- Source register: `{OUTPUTS["sources"]}`
- Source-shadow ban attempt: `{OUTPUTS["shadow_attempt"]}`
- Source-map normal form: `{OUTPUTS["normal_form"]}`
- tau_WEP/direct product source rows: `{OUTPUTS["tau_direct"]}`
- GR bridge handoff: `{OUTPUTS["gr_handoff"]}`
- Current corpus gate: `{OUTPUTS["corpus_gate"]}`
- Score blockers: `{OUTPUTS["score_blockers"]}`
- Claim status: `{OUTPUTS["claim_status"]}`
- Next target: `{OUTPUTS["next"]}`
- Validation: `{OUTPUTS["validation"]}`
- Branch copy: `{BRANCH_OUTPUTS["shadow_attempt_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["normal_form_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["tau_direct_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["gr_handoff_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["next_copy"]}`
"""

DOC.write_text(doc_text, encoding="utf-8")
remove_pycache()

print(f"Wrote {DOC}")
print(f"Wrote {OUTPUTS['validation']}")
print(f"Validation passed {sum(1 for row in validation_rows if row['passed'] == 'True')}/{len(validation_rows)}")
