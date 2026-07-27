from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
WEP_SOURCES = ROOT / "source-intake" / "wep-sources" / "1899"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1899"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1899-Y5-R2FR-wep-source-worldtube-material-tensor-acquisition-or-action-owner-lemma.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1898_doc": ROOT / "1898-Y5-R2FR-readout-variation-commutator-zero-or-wep-projection-row-v1.md",
    "1898_validation": OUT / "P8_Y5_BRR545_1898_VALIDATION.csv",
    "1898_commutator": OUT / "P8_Y5_PARENT_QLOC_1898_READOUT_VARIATION_COMMUTATOR_ZERO_ATTEMPT.csv",
    "1898_wep_row": OUT / "P8_Y5_PARENT_QLOC_1898_WEP_PROJECTION_ROW_V1_NONCLAIM.csv",
    "1898_requirements": OUT / "P8_Y5_PARENT_QLOC_1898_WEP_ROW_REQUIREMENTS.csv",
    "1898_next": OUT / "P8_Y5_PARENT_QLOC_1898_NEXT_TARGET.csv",
    "1067_action_owner": OUT / "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv",
    "1067_hbar_measure": OUT / "P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv",
    "1067_consequence": OUT / "P8_Y5_R10_1067_SOURCE_WEIGHT_CONSEQUENCE_LEDGER.csv",
    "1420_wep_fill_attempt": OUT / "P8_Y5_R10_1420_WEP_PROJECTION_ROW_FILL_ATTEMPT.csv",
    "1420_wep_checklist": OUT / "P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv",
    "1695_tau_wep": OUT / "P8_Y5_PARENT_QLOC_1695_TAU_WEP_PROJECTION_READINESS.csv",
    "1066_tau_contract": OUT / "P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv",
    "1225_tau_attempt": OUT / "P8_Y5_R10_1225_TAU_WEP_PROJECTION_ATTEMPT.csv",
    "1061_material_convention": OUT / "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv",
    "1084_readout_gate": OUT / "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
}


SOURCE_NEEDLES = {
    "1898_doc": ["PURE_POSTPROCESSING_ZERO_ONLY_GENERAL_COMMUTATOR_NOT_DERIVED", "WEP_PROJECTION_ROW_V1_NOT_EXECUTABLE_NONCLAIM"],
    "1898_validation": ["VAL1898_OVERALL,PASS"],
    "1898_commutator": ["RVC1898_5_verdict", "PURE_POSTPROCESSING_ZERO_ONLY_GENERAL_COMMUTATOR_NOT_DERIVED"],
    "1898_wep_row": ["WEP1898_7_verdict", "WEP_PROJECTION_ROW_V1_NOT_EXECUTABLE_NONCLAIM"],
    "1898_requirements": ["WRQ1898_0_parent_values", "WRQ1898_6_no_cancellation"],
    "1898_next": ["NEXT1898_0_primary", "action/current owner"],
    "1067_action_owner": ["ASO1067_5_verdict", "CONDITIONAL_NOT_PARENT_DERIVED"],
    "1067_hbar_measure": ["HMO1067_4_verdict", "OWNER_NOT_DERIVED"],
    "1067_consequence": ["SWC1067_4_verdict", "finite Delta_w*tau_WEP branch remains"],
    "1420_wep_fill_attempt": ["WPF1420_7_verdict", "WEP_PROJECTION_ROW_NOT_EXECUTABLE"],
    "1420_wep_checklist": ["WAC1420_10_executability_verdict", "NOT_EXECUTABLE"],
    "1695_tau_wep": ["TAU1695_7_parser_status", "BLOCKED"],
    "1066_tau_contract": ["TWP1066_7_verdict", "PROJECTION_CONTRACT_WRITTEN_NOT_DERIVED"],
    "1225_tau_attempt": ["TAU1225_6_verdict", "TAU_WEP_PROJECTION_NOT_DERIVED"],
    "1061_material_convention": ["MCON1061_2_eta_bound", "numeric_bound_anchor_filled"],
    "1084_readout_gate": ["RIG1084_0_CMSM_arrays", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
    "local_bound_claims": ["R1_WEP_source_charge", "2.8e-15"],
}


CACHED_WEB_SOURCES = {
    "MICROSCOPE_final_results_arxiv_2209_15487": {
        "url": "https://arxiv.org/pdf/2209.15487",
        "path": WEP_SOURCES / "MICROSCOPE_final_results_arxiv_2209_15487.pdf",
        "expected_magic": "%PDF",
        "role": "bound/provenance anchor for final MICROSCOPE Ti/Pt result",
    },
    "MICROSCOPE_data_processing_HAL_03564498": {
        "url": "https://hal.science/hal-03564498/document",
        "path": WEP_SOURCES / "MICROSCOPE_mission_scenario_ground_segment_data_processing_HAL_03564498.botcheck.html",
        "expected_magic": "%PDF",
        "role": "candidate source for CMSM/data-processing provenance; local fetch hit bot-check HTML",
    },
    "MICROSCOPE_final_data_analysis_HAL_03854332": {
        "url": "https://hal.science/hal-03854332v1/file/DPHY22007.1642068604.pdf",
        "path": WEP_SOURCES / "MICROSCOPE_final_data_analysis_HAL_03854332.botcheck.html",
        "expected_magic": "%PDF",
        "role": "candidate final-analysis source; local fetch hit bot-check HTML",
    },
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1899_SOURCE_REGISTER.csv",
    "web_cache": OUT / "P8_Y5_PARENT_QLOC_1899_WEB_SOURCE_CACHE_LEDGER.csv",
    "action_owner_attempt": OUT / "P8_Y5_PARENT_QLOC_1899_ACTION_CURRENT_OWNER_LEMMA_ATTEMPT.csv",
    "action_owner_gate": OUT / "P8_Y5_PARENT_QLOC_1899_ACTION_CURRENT_OWNER_GATE.csv",
    "wep_input_pack": OUT / "P8_Y5_PARENT_QLOC_1899_WEP_INPUT_PACK_NONCLAIM.csv",
    "wep_executability": OUT / "P8_Y5_PARENT_QLOC_1899_WEP_INPUT_EXECUTABILITY_GATE.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1899_ACTION_WEP_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1899_ACTION_WEP_DRYRUN_RESULTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1899_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1899_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1899_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1899_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1899_VALIDATION.csv",
}


BRANCH_COPIES = {
    "action_owner_attempt": MICROSCOPE_RESIDUALS / OUTPUTS["action_owner_attempt"].name,
    "wep_input_pack": SOURCE_WEIGHT_DOCS / "WEP_INPUT_PACK_1899_NONCLAIM.csv",
    "wep_executability": QUEUE / "JR1899_WEP_INPUT_EXECUTABILITY_GATE_NONCLAIM.csv",
    "dryrun_results": QUARANTINE / OUTPUTS["dryrun_results"].name,
}


def ensure_dirs() -> None:
    for path in [OUT, WEP_SOURCES, MICROSCOPE_RESIDUALS, QUEUE, SOURCE_WEIGHT_DOCS, QUARANTINE]:
        path.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value).strip().lower()


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def file_magic(path: Path, size: int = 8) -> str:
    if not path.exists() or path.stat().st_size == 0:
        return ""
    data = path.read_bytes()[:size]
    return data.decode("ascii", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in INPUTS.items():
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        needles = SOURCE_NEEDLES[source_id]
        missing_needles = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle_count": len(needles),
                "missing_needles": "; ".join(missing_needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing_needles else "SOURCE_OR_NEEDLE_MISSING",
                "valid_for_claim": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def web_cache_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, info in CACHED_WEB_SOURCES.items():
        path = info["path"]
        magic = file_magic(path)
        exists = path.exists()
        size_bytes = path.stat().st_size if exists else 0
        is_expected = exists and magic.startswith(info["expected_magic"])
        rows.append(
            {
                "source_id": source_id,
                "url": info["url"],
                "local_path": str(path),
                "role": info["role"],
                "exists": exists,
                "size_bytes": size_bytes,
                "file_magic": magic,
                "expected_magic": info["expected_magic"],
                "cache_status": "CACHED_VALID_PDF_NONCLAIM" if is_expected else "CACHE_PRESENT_BUT_NOT_VALID_PDF_NONCLAIM",
                "usable_for": "bound/provenance only" if is_expected else "URL/provenance only; refetch or manual browser download required",
                "valid_for_claim": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def action_owner_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "ACO1899_0_target",
            "claim_piece": "action/current owner zeroes WEP source weights",
            "formal_statement": "A single parent matter action, measure, hbar, Hilbert source, and Noether/current normalization must forbid species-relative source prefactors before WEP projection.",
            "status": "TARGET_SHARP",
            "proof_or_obstruction": "this is the clean derivation route: if signed, WEP source weights become common-mode or absent before any MICROSCOPE row is scored",
            "source_anchor": "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv:ASO1067_0_target; P8_Y5_PARENT_QLOC_1898_WEP_PROJECTION_ROW_V1_NONCLAIM.csv:WEP1898_2_residual_vector",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "ACO1899_1_conditional_lemma",
            "claim_piece": "single-owner naturality lemma",
            "formal_statement": "If S_matter is one natural parent functional over e_obs with one measure/hbar, one Hilbert source T_H:=delta S_matter/delta e_obs, and no Hom(SpeciesLabel,Coeff_active_source), then D_label T_H=0 up to common calibration.",
            "status": "EXACT_CONDITIONAL_LEMMA",
            "proof_or_obstruction": "the functional derivative has no species-coefficient argument slot; a label-only vertical generator cannot differentiate a source coefficient that is not in the domain",
            "source_anchor": "P8_Y5_PARENT_QLOC_1897_ACTION_SCALE_READOUT_STABILITY_ATTEMPT.csv:ASR1897_1_exact_conditional_theorem; P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv:ASO1067_4_species_blind_measure",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "ACO1899_2_current_owner_clause",
            "claim_piece": "Noether/current normalization owner",
            "formal_statement": "The same parent owner must fix matter current, source current, charge labels, and stress normalization so J_A -> c_A J_A is not an independent source coupling.",
            "status": "CURRENT_OWNER_CANDIDATE_NOT_SIGNED",
            "proof_or_obstruction": "a gauge/Noether current can be universal only after the parent representation and normalization map are fixed; current owner is still listed as missing",
            "source_anchor": "P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv:HMO1067_2_current_owner; P8_Y5_R10_1454_C_A_READOUT_CALIBRATION_SPLIT.csv:CAS1454_4_verdict",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "ACO1899_3_classical_rescale_obstruction",
            "claim_piece": "classical EOM rescaling does not remove source weights",
            "formal_statement": "delta(w_A S_A)/delta Psi_A can scale out of matter EOM, but delta(w_A S_A)/delta e_obs = w_A T_A, so the gravitational source still sees w_A.",
            "status": "OBSTRUCTION_ACTIVE",
            "proof_or_obstruction": "this blocks the tempting but wrong argument that action weights are irrelevant because matter equations can be divided by w_A",
            "source_anchor": "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv:ASO1067_1_classical_EOM_vs_source",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "ACO1899_4_measure_obstruction",
            "claim_piece": "quantum/statistical measure can reintroduce weights",
            "formal_statement": "Dmu_parent must factor without species-dependent source-only Jacobians, otherwise measure factors mimic w_A S_A or c_A J_A.",
            "status": "MEASURE_OWNER_UNSIGNED",
            "proof_or_obstruction": "the current corpus has no parent measure/path-integral/statistical owner that rules out species-only Jacobians",
            "source_anchor": "P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv:HMO1067_1_measure_parent; P8_Y5_R10_1067_SOURCE_WEIGHT_CONSEQUENCE_LEDGER.csv:SWC1067_2_quantum_measure_factor",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "ACO1899_5_wep_readout_limit",
            "claim_piece": "WEP input pack cannot prove parent owner",
            "formal_statement": "MICROSCOPE source worldtube/material/readout data can bound or test finite products, but cannot by itself prove the parent action/current owner.",
            "status": "EMPIRICAL_INPUT_NOT_DERIVATION",
            "proof_or_obstruction": "data helps the fallback branch; derivation still needs parent action/current/measure ownership",
            "source_anchor": "P8_Y5_R10_1420_WEP_PROJECTION_ROW_FILL_ATTEMPT.csv:WPF1420_7_verdict; P8_Y5_PARENT_QLOC_1898_WEP_ROW_REQUIREMENTS.csv:WRQ1898_0_parent_values",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "ACO1899_6_verdict",
            "claim_piece": "parent action/current owner theorem",
            "formal_statement": "Current MTS parent primitives prove the single action/current owner needed to set WEP source-weight residuals to zero.",
            "status": "ACTION_CURRENT_OWNER_NOT_PARENT_DERIVED",
            "proof_or_obstruction": "the conditional lemma is exact, but parent measure/hbar/current ownership, species-blind Jacobian descent, and no-Hom source coefficient exclusion are not jointly signed",
            "source_anchor": "ACO1899_0_target through ACO1899_5_wep_readout_limit",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def action_owner_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "AOG1899_0_single_action", "required_clause": "one parent action/hbar/measure owner for ordinary matter", "current_status": "FAIL_OWNER_NOT_DERIVED", "if_pass": "relative pre-action weights become ill-typed or common-mode", "if_fail": "Delta_w_species remains live", "source_anchor": "P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv:HMO1067_4_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "AOG1899_1_current_owner", "required_clause": "one Noether/Hilbert current normalization owner", "current_status": "FAIL_CURRENT_OWNER_CANDIDATE_MISSING", "if_pass": "c_A current rescale becomes calibration/readout only", "if_fail": "c_A_current_rescale remains finite component", "source_anchor": "P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv:HMO1067_2_current_owner", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "AOG1899_2_measure_descent", "required_clause": "measure/coframe/Jacobian descent is species-blind", "current_status": "FAIL_MEASURE_OWNER_UNSIGNED", "if_pass": "measure factors cannot mimic source weights", "if_fail": "quantum/statistical measure residual remains live", "source_anchor": "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv:ASO1067_4_species_blind_measure", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "AOG1899_3_no_source_hom", "required_clause": "no SpeciesLabel -> Coeff_active_source Hom in parent grammar", "current_status": "FAIL_NOHOM_UNSIGNED_IN_STABILITY_CONTEXT", "if_pass": "source prefactor cannot be formed", "if_fail": "finite Delta_w branch remains mandatory", "source_anchor": "P8_Y5_PARENT_QLOC_1897_STABILITY_GATE.csv:STG1897_4_parent_values", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "AOG1899_4_verdict", "required_clause": "action/current owner can zero WEP residuals", "current_status": "ACTION_CURRENT_OWNER_CLAIM_BLOCKED", "if_pass": "move to local-GR/WEP zero branch", "if_fail": "WEP input pack stays fallback", "source_anchor": "AOG1899_0_single_action through AOG1899_3_no_source_hom", "gate_pass": False, "valid_for_claim": False},
    ]


def wep_input_pack_rows() -> list[dict[str, Any]]:
    return [
        {"input_id": "WIP1899_0_bound_anchor", "input_group": "bound_anchor", "target_artifact": "MICROSCOPE_final_results_arxiv_2209_15487.pdf", "accepted_form": "cached PDF plus local_bound_claims R1_WEP_source_charge row", "current_artifact": str(WEP_SOURCES / "MICROSCOPE_final_results_arxiv_2209_15487.pdf"), "current_status": "SOURCE_PDF_CACHED_BOUND_ANCHOR_ONLY", "units_required": "dimensionless eta", "source_url": "https://arxiv.org/pdf/2209.15487", "source_anchor": "local_bound_claims.csv:R1_WEP_source_charge", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"input_id": "WIP1899_1_source_worldtube_profile", "input_group": "source_worldtube", "target_artifact": "P_WEP_R_source_Earth_worldtube.csv", "accepted_form": "Earth/source stress or mass-density profile in observed local frame, or parent theorem reducing to calibrated point source with error bound", "current_artifact": "MISSING", "current_status": "MISSING_SOURCE_PROFILE_WEIGHTING", "units_required": "SI density/profile units or normalized dimensionless kernel", "source_url": "not_acquired", "source_anchor": "P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv:WAC1420_0_source_worldtube_profile", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"input_id": "WIP1899_2_source_composition", "input_group": "source_worldtube", "target_artifact": "P_WEP_R_source_Earth_composition.csv", "accepted_form": "Earth/source composition or source-charge convention matching Delta_w basis", "current_artifact": "MISSING", "current_status": "MISSING_SOURCE_COMPOSITION_CONVENTION", "units_required": "mass fractions or declared source-charge basis", "source_url": "not_acquired", "source_anchor": "P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv:WAC1420_1_source_composition", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"input_id": "WIP1899_3_material_tensor", "input_group": "material_response", "target_artifact": "P_WEP_TiPt_material_response_tensor.csv", "accepted_form": "full TA6V-minus-PtRh10 response tensor to Delta_w_eff basis, or theorem reducing material response", "current_artifact": "MISSING", "current_status": "MISSING_FULL_MATERIAL_TENSOR", "units_required": "dimensionless sensitivities per residual basis entry", "source_url": "not_acquired", "source_anchor": "P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv:WAC1420_3_material_tensor", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"input_id": "WIP1899_4_readout_arrays", "input_group": "orbit_readout", "target_artifact": "P_WEP_K_CMSM_readout.csv", "accepted_form": "official MICROSCOPE CMSM/export arrays or validated exact equivalent with time, masks, orbit, attitude, and calibration flags", "current_artifact": "HAL candidate URLs cached as bot-check HTML only", "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED", "units_required": "time, radius/altitude, frame units, dimensionless projection kernel", "source_url": "https://hal.science/hal-03564498/document", "source_anchor": "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv:RIG1084_0_CMSM_arrays", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"input_id": "WIP1899_5_force_map", "input_group": "observed_force_map", "target_artifact": "P_WEP_force_map_eta_convention.md", "accepted_form": "source residual to differential acceleration map in same observed coframe, with eta sign/normalization and common-mode guard", "current_artifact": "MISSING", "current_status": "MISSING_FORCE_READOUT_MAP", "units_required": "m s^-2 internally; dimensionless eta after normalization", "source_url": "not_acquired", "source_anchor": "P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv:WAC1420_8_force_map", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"input_id": "WIP1899_6_tau_wep", "input_group": "projection_product", "target_artifact": "P_WEP_tau_wep_prior_or_formula.csv", "accepted_form": "derived or sourced tau_WEP; explicit retained nuisance with prior is allowed; tau_WEP=1 shortcut forbidden", "current_artifact": "MISSING", "current_status": "TAU_WEP_PROJECTION_NOT_DERIVED", "units_required": "dimensionless projection/contraction factor", "source_url": "not_acquired", "source_anchor": "P8_Y5_R10_1225_TAU_WEP_PROJECTION_ATTEMPT.csv:TAU1225_6_verdict", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"input_id": "WIP1899_7_parent_residuals", "input_group": "source_residual_vector", "target_artifact": "P_WEP_parent_residual_certificates.csv", "accepted_form": "parent residual values, uncertainties, or theorem-zero certificates for Delta_w_eff components", "current_artifact": "MISSING", "current_status": "MISSING_RESIDUAL_VALUES", "units_required": "dimensionless or declared current/projector units", "source_url": "not_acquired", "source_anchor": "P8_Y5_PARENT_QLOC_1898_WEP_ROW_REQUIREMENTS.csv:WRQ1898_0_parent_values", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"input_id": "WIP1899_8_verdict", "input_group": "wep_input_pack", "target_artifact": "executable WEP row v1", "accepted_form": "WIP1899_1 through WIP1899_7 filled or theorem-reduced with source paths and units", "current_artifact": "NONCLAIM_LEDGER_ONLY", "current_status": "WEP_INPUT_PACK_NOT_EXECUTABLE_NONCLAIM", "units_required": "dimensionless final eta", "source_url": "mixed", "source_anchor": "WIP1899_0_bound_anchor through WIP1899_7_parent_residuals", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
    ]


def wep_executability_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "WEG1899_0_bound", "required_clause": "real WEP bound anchor exists", "current_status": "PASS_BOUND_ANCHOR_ONLY_NONCLAIM", "gate_pass": False, "blocks_claim": True, "source_anchor": "WIP1899_0_bound_anchor", "valid_for_claim": False},
        {"gate_id": "WEG1899_1_parent_residuals", "required_clause": "parent residual values or theorem-zero certificates exist", "current_status": "FAIL_MISSING_RESIDUAL_VALUES", "gate_pass": False, "blocks_claim": True, "source_anchor": "WIP1899_7_parent_residuals", "valid_for_claim": False},
        {"gate_id": "WEG1899_2_source", "required_clause": "source worldtube/profile and composition convention acquired", "current_status": "FAIL_MISSING_SOURCE_PROFILE_WEIGHTING", "gate_pass": False, "blocks_claim": True, "source_anchor": "WIP1899_1_source_worldtube_profile;WIP1899_2_source_composition", "valid_for_claim": False},
        {"gate_id": "WEG1899_3_material", "required_clause": "full Ti/Pt material response tensor acquired", "current_status": "FAIL_MISSING_FULL_MATERIAL_TENSOR", "gate_pass": False, "blocks_claim": True, "source_anchor": "WIP1899_3_material_tensor", "valid_for_claim": False},
        {"gate_id": "WEG1899_4_readout_force", "required_clause": "official readout arrays and force/eta map acquired", "current_status": "FAIL_OFFICIAL_ARRAYS_AND_FORCE_MAP_MISSING", "gate_pass": False, "blocks_claim": True, "source_anchor": "WIP1899_4_readout_arrays;WIP1899_5_force_map", "valid_for_claim": False},
        {"gate_id": "WEG1899_5_tau", "required_clause": "tau_WEP derived or sourced without unity shortcut", "current_status": "FAIL_TAU_WEP_PROJECTION_NOT_DERIVED", "gate_pass": False, "blocks_claim": True, "source_anchor": "WIP1899_6_tau_wep", "valid_for_claim": False},
        {"gate_id": "WEG1899_6_verdict", "required_clause": "WEP input pack supports an executable nonclaim row", "current_status": "WEP_INPUT_PACK_NOT_EXECUTABLE", "gate_pass": False, "blocks_claim": True, "source_anchor": "WEG1899_0_bound through WEG1899_5_tau", "valid_for_claim": False},
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {"case_id": "DRY1899_0_owner_unsigned", "action_owner_signed": False, "web_cache_valid": True, "parent_residuals": False, "source_worldtube": False, "material_tensor": False, "readout_force": False, "tau_wep": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_ACTION_CURRENT_OWNER_UNSIGNED", "valid_for_claim": False},
        {"case_id": "DRY1899_1_cache_botcheck", "action_owner_signed": True, "web_cache_valid": False, "parent_residuals": False, "source_worldtube": False, "material_tensor": False, "readout_force": False, "tau_wep": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_WEB_CACHE_NOT_VALID_SOURCE_DATA", "valid_for_claim": False},
        {"case_id": "DRY1899_2_parent_residuals", "action_owner_signed": True, "web_cache_valid": True, "parent_residuals": False, "source_worldtube": False, "material_tensor": False, "readout_force": False, "tau_wep": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_PARENT_RESIDUAL_VALUES_MISSING", "valid_for_claim": False},
        {"case_id": "DRY1899_3_source", "action_owner_signed": True, "web_cache_valid": True, "parent_residuals": True, "source_worldtube": False, "material_tensor": False, "readout_force": False, "tau_wep": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_SOURCE_WORLDTUBE_MISSING", "valid_for_claim": False},
        {"case_id": "DRY1899_4_material", "action_owner_signed": True, "web_cache_valid": True, "parent_residuals": True, "source_worldtube": True, "material_tensor": False, "readout_force": False, "tau_wep": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_MATERIAL_TENSOR_MISSING", "valid_for_claim": False},
        {"case_id": "DRY1899_5_readout_force", "action_owner_signed": True, "web_cache_valid": True, "parent_residuals": True, "source_worldtube": True, "material_tensor": True, "readout_force": False, "tau_wep": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_READOUT_FORCE_MAP_MISSING", "valid_for_claim": False},
        {"case_id": "DRY1899_6_tau", "action_owner_signed": True, "web_cache_valid": True, "parent_residuals": True, "source_worldtube": True, "material_tensor": True, "readout_force": True, "tau_wep": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_TAU_WEP_NOT_DERIVED", "valid_for_claim": False},
        {"case_id": "DRY1899_7_bound_anchor", "action_owner_signed": True, "web_cache_valid": True, "parent_residuals": True, "source_worldtube": True, "material_tensor": True, "readout_force": True, "tau_wep": True, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_BOUND_ANCHOR_ONLY", "valid_for_claim": False},
        {"case_id": "DRY1899_8_cancellation", "action_owner_signed": True, "web_cache_valid": True, "parent_residuals": True, "source_worldtube": True, "material_tensor": True, "readout_force": True, "tau_wep": True, "bound_anchor_only": False, "uses_cancellation": True, "expected_status": "REFUSED_CANCELLATION_ONLY", "valid_for_claim": False},
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    action_owner_signed = bool_string(row["action_owner_signed"]) == "true"
    web_cache_valid = bool_string(row["web_cache_valid"]) == "true"
    parent_residuals = bool_string(row["parent_residuals"]) == "true"
    source_worldtube = bool_string(row["source_worldtube"]) == "true"
    material_tensor = bool_string(row["material_tensor"]) == "true"
    readout_force = bool_string(row["readout_force"]) == "true"
    tau_wep = bool_string(row["tau_wep"]) == "true"
    bound_anchor_only = bool_string(row["bound_anchor_only"]) == "true"
    uses_cancellation = bool_string(row["uses_cancellation"]) == "true"

    if not action_owner_signed:
        status = "REFUSED_ACTION_CURRENT_OWNER_UNSIGNED"
    elif not web_cache_valid:
        status = "REFUSED_WEB_CACHE_NOT_VALID_SOURCE_DATA"
    elif not parent_residuals:
        status = "REFUSED_PARENT_RESIDUAL_VALUES_MISSING"
    elif not source_worldtube:
        status = "REFUSED_SOURCE_WORLDTUBE_MISSING"
    elif not material_tensor:
        status = "REFUSED_MATERIAL_TENSOR_MISSING"
    elif not readout_force:
        status = "REFUSED_READOUT_FORCE_MAP_MISSING"
    elif not tau_wep:
        status = "REFUSED_TAU_WEP_NOT_DERIVED"
    elif bound_anchor_only:
        status = "REFUSED_BOUND_ANCHOR_ONLY"
    elif uses_cancellation:
        status = "REFUSED_CANCELLATION_ONLY"
    else:
        status = "WOULD_REQUIRE_FULL_NUMERIC_NONCLAIM_REVIEW"
    return {
        "case_id": row["case_id"],
        "computed_status": status,
        "expected_status": row["expected_status"],
        "status_match": status == row["expected_status"],
        "claim_allowed": False,
        "valid_for_claim": False,
        "generated_utc": GENERATED_UTC,
    }


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [validate_dryrun_case(row) for row in cases]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "CG1899_0_action_owner", "condition": "action/current owner is parent-signed", "current_status": "FAIL_ACTION_CURRENT_OWNER_NOT_PARENT_DERIVED", "source_anchor": "P8_Y5_PARENT_QLOC_1899_ACTION_CURRENT_OWNER_LEMMA_ATTEMPT.csv:ACO1899_6_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1899_1_wep_inputs", "condition": "WEP input pack is executable", "current_status": "FAIL_WEP_INPUT_PACK_NOT_EXECUTABLE", "source_anchor": "P8_Y5_PARENT_QLOC_1899_WEP_INPUT_EXECUTABILITY_GATE.csv:WEG1899_6_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1899_2_cached_sources", "condition": "cached web sources are not treated as model predictions or missing arrays", "current_status": "PASS_PROVENANCE_ONLY_NONCLAIM", "source_anchor": "P8_Y5_PARENT_QLOC_1899_WEB_SOURCE_CACHE_LEDGER.csv", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1899_3_verdict", "condition": "WEP/local-GR claim allowed", "current_status": "CLAIM_BLOCKED", "source_anchor": "CG1899_0_action_owner through CG1899_2_cached_sources", "gate_pass": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC1899_0_owner", "decision": "do not promote action/current owner theorem", "reason": "conditional lemma is exact, but hbar/measure/current ownership and species-blind descent are not parent-signed", "status": "ACTION_OWNER_ROUTE_SHARP_BUT_UNSIGNED", "next_dependency": "parent signature for action/current owner or Noether normalization", "valid_for_claim": False},
        {"decision_id": "DEC1899_1_wep_pack", "decision": "keep WEP input pack nonclaim", "reason": "bound PDF is cached, but source worldtube, composition, material tensor, readout/force map, tau_WEP, and parent residuals are missing", "status": "WEP_INPUT_PACK_STAGED_NONCLAIM", "next_dependency": "source-worldtube point-source theorem or official readout data acquisition", "valid_for_claim": False},
        {"decision_id": "DEC1899_2_next", "decision": "attack source-worldtube reduction next", "reason": "it is the narrowest WEP input that might be derivable rather than merely downloaded, and it controls tau_WEP and common-mode hiding", "status": "NEXT_TARGET_SELECTED", "next_dependency": "1900 source-worldtube point-source reduction or official readout data runner", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1899_0_primary",
            "selection_status": "selected",
            "target_doc": "1900-Y5-R2FR-wep-source-worldtube-point-source-reduction-or-official-readout-data-runner.md",
            "target_script": "scripts/Y5_R2FR_wep_source_worldtube_point_source_reduction_or_official_readout_data_runner_1900.py",
            "objective": "try to prove the WEP source worldtube reduces to a calibrated common-mode point-source leg with bounded residual; if it fails, build an official readout/data acquisition runner and keep every row nonclaim",
            "success_condition": "parent-signed source-worldtube reduction with no relative source-weight hiding, or source-backed acquisition rows for worldtube/readout data with cache validation",
            "do_not": "do not hide relative weights in measured GM, do not set tau_WEP=1, and do not claim WEP/local-GR from bound anchors or cached PDFs",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {"status_id": "STAT1899_0_theory", "area": "action/current owner", "summary": "the exact lemma exists, but parent ownership is still unsigned", "risk_level": "DERIVATION_GAP_NARROWED", "project_meaning": "local-GR source universality is now tied to one clear ownership theorem rather than broad vibes", "next_action": "derive owner or no-Hom source coefficient signature", "valid_for_claim": False},
        {"status_id": "STAT1899_1_wep", "area": "WEP input pack", "summary": "MICROSCOPE bound provenance is cached, but executable WEP inputs remain missing", "risk_level": "EMPIRICAL_BRANCH_STRUCTURED_NOT_EXECUTABLE", "project_meaning": "testing route is disciplined: we know exactly what files/theorems are missing before a WEP score", "next_action": "source-worldtube reduction or official readout/data acquisition", "valid_for_claim": False},
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    cases = dryrun_case_rows()
    return {
        "source_register": source_register_rows(),
        "web_cache": web_cache_rows(),
        "action_owner_attempt": action_owner_attempt_rows(),
        "action_owner_gate": action_owner_gate_rows(),
        "wep_input_pack": wep_input_pack_rows(),
        "wep_executability": wep_executability_rows(),
        "dryrun_cases": cases,
        "dryrun_results": dryrun_result_rows(cases),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }


def copy_branch_artifacts() -> None:
    for key, target in BRANCH_COPIES.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(OUTPUTS[key], target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass", "parent_signed"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            for field in fields.intersection(row.keys()):
                if bool_string(row[field]) == "true":
                    bad.append(f"{path.name}:{index}:{field}=true")
    return not bad, "; ".join(bad) if bad else "all generated claim/scoring/signature flags remain false"


def blocked_rows_not_ready(paths: list[Path]) -> tuple[bool, str]:
    markers = ["MISSING", "UNSIGNED", "NOT_DERIVED", "NOT_PARENT", "BLOCKED", "FAIL", "COUNTER", "SYMBOLIC", "NONCLAIM", "CLAIM_BLOCKED", "NOT_EXECUTABLE"]
    fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass", "parent_signed"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            text = " ".join(str(value) for value in row.values())
            if any(marker in text for marker in markers):
                for field in fields.intersection(row.keys()):
                    if bool_string(row[field]) == "true":
                        bad.append(f"{path.name}:{index}:{field}=true despite blocked marker")
    return not bad, "; ".join(bad) if bad else "blocked/unsigned/nonclaim rows are not score-ready"


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    for path in paths:
        try:
            rows = csv_rows(path)
            if not rows:
                bad.append(f"{path.name}:empty")
        except Exception as exc:
            bad.append(f"{path.name}:{exc}")
    return not bad, "; ".join(bad) if bad else f"parsed {len(paths)} csv files"


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []
    source_rows_loaded = csv_rows(OUTPUTS["source_register"])
    checks.append({"validation_id": "VAL1899_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL", "detail": "all local source paths exist and needles found", "valid_for_claim": False})
    cache_rows = csv_rows(OUTPUTS["web_cache"])
    valid_pdf_rows = [row for row in cache_rows if row["cache_status"] == "CACHED_VALID_PDF_NONCLAIM"]
    invalid_cache_safe = all(row["valid_for_claim"] == "False" and row["cache_status"] != "CACHED_VALID_PDF_CLAIM" for row in cache_rows)
    checks.append({"validation_id": "VAL1899_01_web_cache", "status": "PASS" if valid_pdf_rows and invalid_cache_safe else "FAIL", "detail": "at least one WEP source PDF cached; bot-check/invalid caches remain nonclaim", "valid_for_claim": False})
    owner_rows = csv_rows(OUTPUTS["action_owner_attempt"])
    checks.append({"validation_id": "VAL1899_02_owner_verdict", "status": "PASS" if any(row["attempt_id"] == "ACO1899_6_verdict" and row["status"] == "ACTION_CURRENT_OWNER_NOT_PARENT_DERIVED" for row in owner_rows) else "FAIL", "detail": "action/current owner remains unsigned", "valid_for_claim": False})
    wep_rows = csv_rows(OUTPUTS["wep_input_pack"])
    checks.append({"validation_id": "VAL1899_03_wep_pack", "status": "PASS" if len(wep_rows) >= 9 and all(row["score_ready"] == "False" and row["valid_prediction_row"] == "False" for row in wep_rows) else "FAIL", "detail": "WEP input pack is nonclaim/not score-ready", "valid_for_claim": False})
    executable_rows = csv_rows(OUTPUTS["wep_executability"])
    checks.append({"validation_id": "VAL1899_04_executability_block", "status": "PASS" if all(row["gate_pass"] == "False" and row["blocks_claim"] == "True" for row in executable_rows) else "FAIL", "detail": "WEP executable gates all block claim", "valid_for_claim": False})
    dry_rows = csv_rows(OUTPUTS["dryrun_results"])
    checks.append({"validation_id": "VAL1899_05_dryrun", "status": "PASS" if all(row["status_match"] == "True" and row["claim_allowed"] == "False" for row in dry_rows) else "FAIL", "detail": "dry-run refuses unsigned owner, invalid web cache, missing WEP inputs, bound-only, and cancellation", "valid_for_claim": False})
    gate_rows = csv_rows(OUTPUTS["claim_gate"])
    checks.append({"validation_id": "VAL1899_06_claim_gate", "status": "PASS" if any(row["gate_id"] == "CG1899_3_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in gate_rows) else "FAIL", "detail": "claim remains blocked", "valid_for_claim": False})
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append({"validation_id": "VAL1899_07_next_target", "status": "PASS" if any(row["route_id"] == "NEXT1899_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL", "detail": "1900 target selected", "valid_for_claim": False})
    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append({"validation_id": "VAL1899_08_claim_flags_false", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})
    blocked_ok, blocked_detail = blocked_rows_not_ready(generated_without_validation)
    checks.append({"validation_id": "VAL1899_09_blocked_markers_not_ready", "status": "PASS" if blocked_ok else "FAIL", "detail": blocked_detail, "valid_for_claim": False})
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1899_10_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})
    checks.append({"validation_id": "VAL1899_11_branch_copies", "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL", "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()), "valid_for_claim": False})
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1899_12_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})
    formalization_hits = list(FORMALIZATION.rglob("*1899*")) if FORMALIZATION.exists() else []
    checks.append({"validation_id": "VAL1899_13_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1899_count={len(formalization_hits)}", "valid_for_claim": False})
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1899_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1899 WEP source-worldtube/material tensor acquisition or action-owner lemma", "valid_for_claim": False})
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1899 - WEP Source-Worldtube Material Tensor Acquisition Or Action-Owner Lemma

## Purpose

This checkpoint tries the derivation-first route: prove the action/current owner needed to zero WEP source weights. If that does not close, it stages source-ready WEP input rows without claiming a pass.

## Result

- The action/current owner lemma is exact conditionally, but not parent-signed.
- Classical matter-equation rescaling does not remove source weights from the Hilbert source.
- The MICROSCOPE final-result PDF is cached as bound provenance.
- HAL/data-processing candidate downloads currently resolve to bot-check HTML locally, so they are URL/provenance only.
- The WEP input pack is explicit but not executable: source worldtube, composition, full Ti/Pt material tensor, readout/force map, tau_WEP, and parent residual values remain missing.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Web Source Cache Ledger

{markdown_table(rows_by_name["web_cache"])}

## Action / Current Owner Lemma Attempt

{markdown_table(rows_by_name["action_owner_attempt"])}

## Action / Current Owner Gate

{markdown_table(rows_by_name["action_owner_gate"])}

## WEP Input Pack

{markdown_table(rows_by_name["wep_input_pack"])}

## WEP Executability Gate

{markdown_table(rows_by_name["wep_executability"])}

## Dry-Run Cases

{markdown_table(rows_by_name["dryrun_cases"])}

## Dry-Run Results

{markdown_table(rows_by_name["dryrun_results"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status Snapshot

{markdown_table(rows_by_name["project_status"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = build_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
