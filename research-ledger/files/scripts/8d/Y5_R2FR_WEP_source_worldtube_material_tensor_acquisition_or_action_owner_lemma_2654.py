from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2654"
WEP_SOURCE_CACHE = ROOT / "source-intake" / "wep-sources" / "1899"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2654-Y5-R2FR-WEP-source-worldtube-material-tensor-acquisition-or-action-owner-lemma.md"

CHECKPOINT = "2654"
BRANCH_ID = "Y5_R2FR_WEP_INPUT_PACK_OR_ACTION_OWNER_2654"
PREFIX = "P8_Y5_WEP_INPUT_OWNER_2654"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "web_cache": RESIDUALS / f"{PREFIX}_WEB_SOURCE_CACHE_LEDGER.csv",
    "action_owner_attempt": RESIDUALS / f"{PREFIX}_ACTION_CURRENT_OWNER_LEMMA_ATTEMPT.csv",
    "action_owner_gate": RESIDUALS / f"{PREFIX}_ACTION_CURRENT_OWNER_GATE.csv",
    "wep_input_pack": RESIDUALS / f"{PREFIX}_WEP_INPUT_PACK_NONCLAIM.csv",
    "wep_executability": RESIDUALS / f"{PREFIX}_WEP_INPUT_EXECUTABILITY_GATE.csv",
    "dryrun_cases": RESIDUALS / f"{PREFIX}_ACTION_WEP_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / f"{PREFIX}_ACTION_WEP_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2654_WEP_INPUT_EXECUTABILITY_GATE_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "WEP_input_pack_2654_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "WEP_INPUT_PACK_2654_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2654_ACTION_CURRENT_OWNER_LEMMA_ATTEMPT.csv",
    "quarantine": QUARANTINE / "P8_Y5_2654_ACTION_WEP_DRYRUN_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2653_doc": {
        "path": ROOT / "2653-Y5-R2FR-readout-variation-commutator-zero-or-WEP-projection-row-v1.md",
        "needles": ["WEP2653_7_verdict", "DEC2653_2_next", "VAL2653_OVERALL"],
        "role": "immediate WEP-row handoff",
    },
    "2652_doc": {
        "path": ROOT / "2652-Y5-R2FR-action-scale-readout-stability-or-Delta-w-projection-matrix.md",
        "needles": ["DPM2652_1_WEP_MICROSCOPE", "DPR2652_1_arena_tau_K"],
        "role": "projection matrix and arena kernel dependency",
    },
    "2651_doc": {
        "path": ROOT / "2651-Y5-R2FR-parent-sort-nohom-constructor-or-finite-Delta-w-basis.md",
        "needles": ["DWB2651_9_acceptance", "DWB2651_8_no_cancellation_policy"],
        "role": "finite Delta_w residual basis and no-cancellation policy",
    },
    "1225_doc": {
        "path": ROOT / "1225-Y5-R10-tau-WEP-source-worldtube-readout-projection.md",
        "needles": ["TAU1225_6_verdict", "ACQ1225_0_official_readout_arrays", "ACQ1225_4_material_tensor", "ACQ1225_5_delta_w"],
        "role": "tau/source/readout/material missing-source ledger",
    },
    "1080_doc": {
        "path": ROOT / "1080-Y5-R10-finite-WEP-source-vector-and-material-tensor-acquisition-pack.md",
        "needles": ["BOUND1080_0_MICROSCOPE_WEP_source_charge", "MAT1080_4_full_tensor_upgrade"],
        "role": "MICROSCOPE bound anchor and material tensor context",
    },
    "1899_doc": {
        "path": ROOT / "1899-Y5-R2FR-wep-source-worldtube-material-tensor-acquisition-or-action-owner-lemma.md",
        "needles": ["ACO1899_6_verdict", "WIP1899_8_verdict", "VAL1899_OVERALL"],
        "role": "older WEP input/action-owner analogue",
    },
}

CACHED_WEB_SOURCES: dict[str, dict[str, Any]] = {
    "MICROSCOPE_final_results_arxiv_2209_15487": {
        "url": "https://arxiv.org/pdf/2209.15487",
        "path": WEP_SOURCE_CACHE / "MICROSCOPE_final_results_arxiv_2209_15487.pdf",
        "expected_magic": b"%PDF",
        "role": "bound/provenance anchor for final MICROSCOPE Ti/Pt result",
    },
    "MICROSCOPE_data_processing_HAL_03564498": {
        "url": "https://hal.science/hal-03564498/document",
        "path": WEP_SOURCE_CACHE / "MICROSCOPE_mission_scenario_ground_segment_data_processing_HAL_03564498.botcheck.html",
        "expected_magic": b"%PDF",
        "role": "candidate source for CMSM/data-processing provenance; local fetch hit bot-check HTML",
    },
    "MICROSCOPE_final_data_analysis_HAL_03854332": {
        "url": "https://hal.science/hal-03854332v1/file/DPHY22007.1642068604.pdf",
        "path": WEP_SOURCE_CACHE / "MICROSCOPE_final_data_analysis_HAL_03854332.botcheck.html",
        "expected_magic": b"%PDF",
        "role": "candidate final-analysis source; local fetch hit bot-check HTML",
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in list(OUTPUTS.values()) + list(BRANCH_COPIES.values()) + [DOC_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def file_magic(path: Path, size: int = 8) -> bytes:
    if not path.exists() or not path.is_file():
        return b""
    with path.open("rb") as handle:
        return handle.read(size)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as csvfile:
        return list(csv.DictReader(csvfile))


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    header = "| " + " | ".join(fieldnames) + " |"
    separator = "| " + " | ".join("---" for _ in fieldnames) + " |"
    body: list[str] = []
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fieldnames]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for source_id, spec in SOURCE_SPECS.items():
        path = Path(spec["path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": f"SRC2654_{source_id}",
                "role": spec["role"],
                "path": str(path),
                "exists": path.exists(),
                "needles_required": len(spec["needles"]),
                "missing_needles": "; ".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def web_cache_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for source_id, spec in CACHED_WEB_SOURCES.items():
        path = Path(spec["path"])
        magic = file_magic(path)
        magic_ok = magic.startswith(spec["expected_magic"])
        rows.append(
            {
                "source_id": f"WEB2654_{source_id}",
                "url": spec["url"],
                "local_path": str(path),
                "role": spec["role"],
                "exists": path.exists(),
                "size_bytes": path.stat().st_size if path.exists() else 0,
                "file_magic": magic[:8].decode("latin1", errors="replace"),
                "expected_magic": spec["expected_magic"].decode("ascii"),
                "cache_status": "VALID_PDF_PROVENANCE_ONLY" if magic_ok else "INVALID_OR_BOTCHECK_CACHE_NONCLAIM",
                "usable_for": "bound/provenance anchor only" if magic_ok else "not usable as official arrays/data",
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def action_owner_attempt_rows() -> list[dict[str, Any]]:
    return [
        {"attempt_id": "ACO2654_0_target", "claim_piece": "action/current owner zeroes WEP source weights", "formal_statement": "A single parent matter action, measure, hbar, Hilbert source and Noether/current normalization must forbid species-relative source prefactors before WEP projection.", "status": "TARGET_SHARP", "proof_or_obstruction": "if signed, WEP source weights become common-mode or absent before any MICROSCOPE row is scored", "source_anchor": "2653:WEP2653_2_residual_vector;2651:DWB2651_1_preaction_species", "parent_signed": False, "valid_for_claim": False, "claim_allowed": False},
        {"attempt_id": "ACO2654_1_conditional_lemma", "claim_piece": "single-owner naturality lemma", "formal_statement": "If S_matter is one natural parent functional over e_obs with one measure/hbar, one Hilbert source T_H:=delta S_matter/delta e_obs, and no Hom(SpeciesLabel,Coeff_active_source), then D_label T_H=0 up to common calibration.", "status": "EXACT_CONDITIONAL_LEMMA", "proof_or_obstruction": "the functional derivative has no species-coefficient argument slot; a label-only vertical generator cannot differentiate a source coefficient absent from the domain", "source_anchor": "2652:ASR2652_1_exact_conditional_theorem;2651:NH2651_5_verdict", "parent_signed": False, "valid_for_claim": False, "claim_allowed": False},
        {"attempt_id": "ACO2654_2_current_owner_clause", "claim_piece": "Noether/current normalization owner", "formal_statement": "The same parent owner must fix matter current, source current, charge labels and stress normalization so J_A -> c_A J_A is not an independent source coupling.", "status": "CURRENT_OWNER_CANDIDATE_NOT_SIGNED", "proof_or_obstruction": "a gauge/Noether current is universal only after the parent representation and normalization map are fixed", "source_anchor": "2651:DWB2651_2_current_rescale;2652:STG2652_0_action_owner", "parent_signed": False, "valid_for_claim": False, "claim_allowed": False},
        {"attempt_id": "ACO2654_3_classical_rescale_obstruction", "claim_piece": "classical EOM rescaling does not remove source weights", "formal_statement": "delta(w_A S_A)/delta Psi_A can scale out of isolated matter equations, but delta(w_A S_A)/delta e_obs = w_A T_A, so the gravitational source still sees w_A.", "status": "OBSTRUCTION_ACTIVE", "proof_or_obstruction": "this blocks the tempting argument that action weights are irrelevant because matter equations can be divided by w_A", "source_anchor": "2651:DWB2651_1_preaction_species;2650:NSP2650_3_disconnected_species_countermodel", "parent_signed": False, "valid_for_claim": False, "claim_allowed": False},
        {"attempt_id": "ACO2654_4_measure_obstruction", "claim_piece": "quantum/statistical measure can reintroduce weights", "formal_statement": "Dmu_parent must factor without species-dependent source-only Jacobians; otherwise measure factors mimic w_A S_A, Delta_w_measure or c_A J_A.", "status": "MEASURE_OWNER_UNSIGNED", "proof_or_obstruction": "current corpus has no parent measure/path-integral/statistical owner that rules out species-only Jacobians", "source_anchor": "2651:DWB2651_4_action_measure_jacobian;2652:ASR2652_2_action_scale_gap", "parent_signed": False, "valid_for_claim": False, "claim_allowed": False},
        {"attempt_id": "ACO2654_5_wep_input_limit", "claim_piece": "WEP input pack cannot prove parent owner", "formal_statement": "MICROSCOPE source worldtube/material/readout data can bound or test finite products, but cannot by itself prove parent action/current ownership.", "status": "EMPIRICAL_INPUT_NOT_DERIVATION", "proof_or_obstruction": "data helps the fallback branch; derivation still needs parent action/current/measure ownership", "source_anchor": "2653:WEP2653_7_verdict", "parent_signed": False, "valid_for_claim": False, "claim_allowed": False},
        {"attempt_id": "ACO2654_6_verdict", "claim_piece": "parent action/current owner theorem", "formal_statement": "Current MTS parent primitives prove the single action/current owner needed to set WEP source-weight residuals to zero.", "status": "ACTION_CURRENT_OWNER_NOT_PARENT_DERIVED", "proof_or_obstruction": "the conditional lemma is exact, but parent measure/hbar/current ownership, species-blind Jacobian descent and no-Hom source coefficient exclusion are not jointly signed", "source_anchor": "ACO2654_0_target through ACO2654_5_wep_input_limit", "parent_signed": False, "valid_for_claim": False, "claim_allowed": False},
    ]


def action_owner_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "AOG2654_0_single_action", "required_clause": "one parent action/hbar/measure owner for ordinary matter", "current_status": "FAIL_OWNER_NOT_DERIVED", "if_pass": "relative pre-action weights become ill-typed or common-mode", "if_fail": "Delta_w_species and Delta_w_measure remain live", "source_anchor": "ACO2654_3_classical_rescale_obstruction;ACO2654_4_measure_obstruction", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "AOG2654_1_current_owner", "required_clause": "one Noether/Hilbert current normalization owner", "current_status": "FAIL_CURRENT_OWNER_CANDIDATE_MISSING", "if_pass": "c_A current rescale becomes calibration/readout only", "if_fail": "c_A_current_rescale remains finite component", "source_anchor": "ACO2654_2_current_owner_clause", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "AOG2654_2_measure_descent", "required_clause": "measure/coframe/Jacobian descent is species-blind", "current_status": "FAIL_MEASURE_OWNER_UNSIGNED", "if_pass": "measure factors cannot mimic source weights", "if_fail": "quantum/statistical measure residual remains live", "source_anchor": "ACO2654_4_measure_obstruction", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "AOG2654_3_no_source_hom", "required_clause": "no SpeciesLabel -> Coeff_active_source Hom in parent grammar", "current_status": "FAIL_NOHOM_UNSIGNED_IN_STABILITY_CONTEXT", "if_pass": "source prefactor cannot be formed", "if_fail": "finite Delta_w branch remains mandatory", "source_anchor": "2651:NH2651_5_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "AOG2654_4_verdict", "required_clause": "action/current owner can zero WEP residuals", "current_status": "ACTION_CURRENT_OWNER_CLAIM_BLOCKED", "if_pass": "move to local-GR/WEP zero branch", "if_fail": "WEP input pack stays fallback", "source_anchor": "AOG2654_0_single_action through AOG2654_3_no_source_hom", "gate_pass": False, "valid_for_claim": False},
    ]


def wep_input_pack_rows() -> list[dict[str, Any]]:
    bound_path = WEP_SOURCE_CACHE / "MICROSCOPE_final_results_arxiv_2209_15487.pdf"
    return [
        {"input_id": "WIP2654_0_bound_anchor", "input_group": "bound_anchor", "target_artifact": "MICROSCOPE_final_results_arxiv_2209_15487.pdf", "accepted_form": "cached PDF plus 1080/2653 bound-anchor rows", "current_artifact": str(bound_path), "current_status": "SOURCE_PDF_CACHED_BOUND_ANCHOR_ONLY", "units_required": "dimensionless eta", "source_url": "https://arxiv.org/pdf/2209.15487", "source_anchor": "1080:BOUND1080_0_MICROSCOPE_WEP_source_charge;2653:WEP2653_0_bound_anchor", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"input_id": "WIP2654_1_source_worldtube_profile", "input_group": "source_worldtube", "target_artifact": "P_WEP_R_source_Earth_worldtube.csv", "accepted_form": "Earth/source stress or mass-density profile in observed local frame, or parent theorem reducing to calibrated point source with error bound", "current_artifact": "MISSING", "current_status": "MISSING_SOURCE_PROFILE_WEIGHTING", "units_required": "SI density/profile units or normalized dimensionless kernel", "source_url": "not_acquired", "source_anchor": "2653:WRQ2653_1_source_worldtube", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"input_id": "WIP2654_2_source_composition", "input_group": "source_worldtube", "target_artifact": "P_WEP_R_source_Earth_composition.csv", "accepted_form": "Earth/source composition or source-charge convention matching Delta_w basis", "current_artifact": "MISSING", "current_status": "MISSING_SOURCE_COMPOSITION_CONVENTION", "units_required": "mass fractions or declared source-charge basis", "source_url": "not_acquired", "source_anchor": "2653:WEP2653_3_source_worldtube", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"input_id": "WIP2654_3_material_tensor", "input_group": "material_response", "target_artifact": "P_WEP_TA6V_PtRh10_material_response_tensor.csv", "accepted_form": "full TA6V-minus-PtRh10 response tensor to Delta_w_eff basis, or theorem reducing material response", "current_artifact": "MISSING", "current_status": "MISSING_FULL_MATERIAL_TENSOR", "units_required": "dimensionless sensitivities per residual basis entry", "source_url": "not_acquired", "source_anchor": "2653:WRQ2653_2_material_tensor;1080:MAT1080_4_full_tensor_upgrade", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"input_id": "WIP2654_4_readout_arrays", "input_group": "orbit_readout", "target_artifact": "P_WEP_K_CMSM_readout.csv", "accepted_form": "official MICROSCOPE CMSM/export arrays or validated exact equivalent with time, masks, orbit, attitude, and calibration flags", "current_artifact": "HAL candidate URLs cached as bot-check HTML only", "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED", "units_required": "time, radius/altitude, frame units, dimensionless projection kernel", "source_url": "https://hal.science/hal-03564498/document", "source_anchor": "2653:WRQ2653_3_readout_arrays;1225:ACQ1225_0_official_readout_arrays", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"input_id": "WIP2654_5_force_map", "input_group": "observed_force_map", "target_artifact": "P_WEP_force_map_eta_convention.md", "accepted_form": "source residual to differential acceleration map in same observed coframe, with eta sign/normalization and common-mode guard", "current_artifact": "MISSING", "current_status": "MISSING_FORCE_READOUT_MAP", "units_required": "m s^-2 internally; dimensionless eta after normalization", "source_url": "not_acquired", "source_anchor": "2653:WRQ2653_4_force_map", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"input_id": "WIP2654_6_tau_wep", "input_group": "projection_product", "target_artifact": "P_WEP_tau_wep_prior_or_formula.csv", "accepted_form": "derived or sourced tau_WEP; explicit retained nuisance with prior is allowed; tau_WEP=1 shortcut forbidden", "current_artifact": "MISSING", "current_status": "TAU_WEP_PROJECTION_NOT_DERIVED", "units_required": "dimensionless projection/contraction factor", "source_url": "not_acquired", "source_anchor": "2653:WRQ2653_5_tau_wep;1225:TAU1225_6_verdict", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"input_id": "WIP2654_7_parent_residuals", "input_group": "source_residual_vector", "target_artifact": "P_WEP_parent_residual_certificates.csv", "accepted_form": "parent residual values, uncertainties, or theorem-zero certificates for Delta_w_eff components", "current_artifact": "MISSING", "current_status": "MISSING_RESIDUAL_VALUES", "units_required": "dimensionless or declared current/projector units", "source_url": "not_acquired", "source_anchor": "2653:WRQ2653_0_parent_values;2651:DWB2651_9_acceptance", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"input_id": "WIP2654_8_verdict", "input_group": "wep_input_pack", "target_artifact": "executable WEP row v1", "accepted_form": "WIP2654_1 through WIP2654_7 filled or theorem-reduced with source paths and units", "current_artifact": "NONCLAIM_LEDGER_ONLY", "current_status": "WEP_INPUT_PACK_NOT_EXECUTABLE_NONCLAIM", "units_required": "dimensionless final eta", "source_url": "mixed", "source_anchor": "WIP2654_0_bound_anchor through WIP2654_7_parent_residuals", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
    ]


def wep_executability_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "WEG2654_0_bound", "required_clause": "real WEP bound anchor exists", "current_status": "PASS_BOUND_ANCHOR_ONLY_NONCLAIM", "gate_pass": False, "blocks_claim": True, "source_anchor": "WIP2654_0_bound_anchor", "valid_for_claim": False},
        {"gate_id": "WEG2654_1_parent_residuals", "required_clause": "parent residual values or theorem-zero certificates exist", "current_status": "FAIL_MISSING_RESIDUAL_VALUES", "gate_pass": False, "blocks_claim": True, "source_anchor": "WIP2654_7_parent_residuals", "valid_for_claim": False},
        {"gate_id": "WEG2654_2_source", "required_clause": "source worldtube/profile and composition convention acquired", "current_status": "FAIL_MISSING_SOURCE_PROFILE_WEIGHTING", "gate_pass": False, "blocks_claim": True, "source_anchor": "WIP2654_1_source_worldtube_profile;WIP2654_2_source_composition", "valid_for_claim": False},
        {"gate_id": "WEG2654_3_material", "required_clause": "full TA6V/PtRh10 material response tensor acquired", "current_status": "FAIL_MISSING_FULL_MATERIAL_TENSOR", "gate_pass": False, "blocks_claim": True, "source_anchor": "WIP2654_3_material_tensor", "valid_for_claim": False},
        {"gate_id": "WEG2654_4_readout_force", "required_clause": "official readout arrays and force/eta map acquired", "current_status": "FAIL_OFFICIAL_ARRAYS_AND_FORCE_MAP_MISSING", "gate_pass": False, "blocks_claim": True, "source_anchor": "WIP2654_4_readout_arrays;WIP2654_5_force_map", "valid_for_claim": False},
        {"gate_id": "WEG2654_5_tau", "required_clause": "tau_WEP derived or sourced without unity shortcut", "current_status": "FAIL_TAU_WEP_PROJECTION_NOT_DERIVED", "gate_pass": False, "blocks_claim": True, "source_anchor": "WIP2654_6_tau_wep", "valid_for_claim": False},
        {"gate_id": "WEG2654_6_verdict", "required_clause": "WEP input pack supports an executable nonclaim row", "current_status": "WEP_INPUT_PACK_NOT_EXECUTABLE", "gate_pass": False, "blocks_claim": True, "source_anchor": "WEG2654_0_bound through WEG2654_5_tau", "valid_for_claim": False},
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {"case_id": "DRY2654_0_owner_unsigned", "action_owner_signed": False, "web_cache_valid": True, "parent_residuals": False, "source_worldtube": False, "material_tensor": False, "readout_force": False, "tau_wep": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_ACTION_CURRENT_OWNER_UNSIGNED", "valid_for_claim": False},
        {"case_id": "DRY2654_1_cache_botcheck", "action_owner_signed": True, "web_cache_valid": False, "parent_residuals": False, "source_worldtube": False, "material_tensor": False, "readout_force": False, "tau_wep": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_WEB_CACHE_NOT_VALID_SOURCE_DATA", "valid_for_claim": False},
        {"case_id": "DRY2654_2_parent_residuals", "action_owner_signed": True, "web_cache_valid": True, "parent_residuals": False, "source_worldtube": False, "material_tensor": False, "readout_force": False, "tau_wep": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_PARENT_RESIDUAL_VALUES_MISSING", "valid_for_claim": False},
        {"case_id": "DRY2654_3_source", "action_owner_signed": True, "web_cache_valid": True, "parent_residuals": True, "source_worldtube": False, "material_tensor": False, "readout_force": False, "tau_wep": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_SOURCE_WORLDTUBE_MISSING", "valid_for_claim": False},
        {"case_id": "DRY2654_4_material", "action_owner_signed": True, "web_cache_valid": True, "parent_residuals": True, "source_worldtube": True, "material_tensor": False, "readout_force": False, "tau_wep": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_MATERIAL_TENSOR_MISSING", "valid_for_claim": False},
        {"case_id": "DRY2654_5_readout_force", "action_owner_signed": True, "web_cache_valid": True, "parent_residuals": True, "source_worldtube": True, "material_tensor": True, "readout_force": False, "tau_wep": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_READOUT_FORCE_MAP_MISSING", "valid_for_claim": False},
        {"case_id": "DRY2654_6_tau", "action_owner_signed": True, "web_cache_valid": True, "parent_residuals": True, "source_worldtube": True, "material_tensor": True, "readout_force": True, "tau_wep": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_TAU_WEP_NOT_DERIVED", "valid_for_claim": False},
        {"case_id": "DRY2654_7_bound_anchor", "action_owner_signed": True, "web_cache_valid": True, "parent_residuals": True, "source_worldtube": True, "material_tensor": True, "readout_force": True, "tau_wep": True, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_BOUND_ANCHOR_ONLY", "valid_for_claim": False},
        {"case_id": "DRY2654_8_cancellation", "action_owner_signed": True, "web_cache_valid": True, "parent_residuals": True, "source_worldtube": True, "material_tensor": True, "readout_force": True, "tau_wep": True, "bound_anchor_only": False, "uses_cancellation": True, "expected_status": "REFUSED_CANCELLATION_ONLY", "valid_for_claim": False},
    ]


def evaluate_dryrun(row: dict[str, Any]) -> str:
    if not row["action_owner_signed"]:
        return "REFUSED_ACTION_CURRENT_OWNER_UNSIGNED"
    if not row["web_cache_valid"]:
        return "REFUSED_WEB_CACHE_NOT_VALID_SOURCE_DATA"
    if not row["parent_residuals"]:
        return "REFUSED_PARENT_RESIDUAL_VALUES_MISSING"
    if not row["source_worldtube"]:
        return "REFUSED_SOURCE_WORLDTUBE_MISSING"
    if not row["material_tensor"]:
        return "REFUSED_MATERIAL_TENSOR_MISSING"
    if not row["readout_force"]:
        return "REFUSED_READOUT_FORCE_MAP_MISSING"
    if not row["tau_wep"]:
        return "REFUSED_TAU_WEP_NOT_DERIVED"
    if row["bound_anchor_only"]:
        return "REFUSED_BOUND_ANCHOR_ONLY"
    if row["uses_cancellation"]:
        return "REFUSED_CANCELLATION_ONLY"
    return "COUNTERFACTUAL_READY_NOT_CURRENT_CLAIM"


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = stamp()
    return [
        {"case_id": row["case_id"], "computed_status": evaluate_dryrun(row), "expected_status": row["expected_status"], "status_match": evaluate_dryrun(row) == row["expected_status"], "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": generated}
        for row in cases
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "CG2654_0_action_owner", "condition": "action/current owner is parent-signed", "current_status": "FAIL_ACTION_CURRENT_OWNER_NOT_PARENT_DERIVED", "source_anchor": f"{OUTPUTS['action_owner_attempt'].name}:ACO2654_6_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2654_1_wep_inputs", "condition": "WEP input pack is executable", "current_status": "FAIL_WEP_INPUT_PACK_NOT_EXECUTABLE", "source_anchor": f"{OUTPUTS['wep_executability'].name}:WEG2654_6_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2654_2_cached_sources", "condition": "cached web sources are not treated as model predictions or official arrays", "current_status": "PASS_PROVENANCE_ONLY_NONCLAIM", "source_anchor": OUTPUTS["web_cache"].name, "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2654_3_verdict", "condition": "WEP/local-GR claim allowed", "current_status": "CLAIM_BLOCKED", "source_anchor": "CG2654_0_action_owner through CG2654_2_cached_sources", "gate_pass": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC2654_0_owner", "decision": "DO_NOT_PROMOTE_ACTION_CURRENT_OWNER_THEOREM", "reason": "conditional lemma is exact, but hbar/measure/current ownership and species-blind descent are not parent-signed", "status": "ACTION_OWNER_ROUTE_SHARP_BUT_UNSIGNED", "next_dependency": "parent signature for action/current owner or Noether normalization", "valid_for_claim": False},
        {"decision_id": "DEC2654_1_wep_pack", "decision": "WEP_INPUT_PACK_STAGED_NONCLAIM", "reason": "bound PDF is cached, but source worldtube, composition, material tensor, readout/force map, tau_WEP and parent residuals are missing", "status": "WEP_INPUT_PACK_STAGED_NONCLAIM", "next_dependency": "source-worldtube point-source theorem or official readout data acquisition", "valid_for_claim": False},
        {"decision_id": "DEC2654_2_next", "decision": "SELECT_2655_SOURCE_WORLDTUBE_REDUCTION_OR_READOUT_DATA_RUNNER", "reason": "source worldtube is the narrowest WEP input that might be derivable and it controls tau_WEP/common-mode hiding", "status": "NEXT_TARGET_SELECTED", "next_dependency": "2655 source-worldtube point-source reduction or official readout data runner", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2654_0_selected",
            "status": "selected",
            "next_doc": "2655-Y5-R2FR-WEP-source-worldtube-point-source-reduction-or-official-readout-data-runner.md",
            "next_script": "scripts/Y5_R2FR_WEP_source_worldtube_point_source_reduction_or_official_readout_data_runner_2655.py",
            "target": "Try to prove the WEP source worldtube reduces to a calibrated common-mode point-source leg with bounded residual; if it fails, build official readout/data acquisition rows and keep every row nonclaim.",
            "must_include": "source-worldtube reduction; common-mode point-source theorem; readout/data acquisition rows; cache validation; tau_WEP dependency; refusal states",
            "must_exclude": "hiding relative weights in measured GM, tau_WEP=1 shortcut, WEP/local-GR claim from bound anchors or cached PDFs, GitHub action, formalization-workbench edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {"status_id": "STAT2654_0_theory", "area": "action/current owner", "summary": "the exact lemma exists, but parent ownership is still unsigned", "risk_level": "DERIVATION_GAP_NARROWED", "project_meaning": "local-GR source universality is tied to a clear ownership theorem rather than broad vibes", "next_action": "derive owner or no-Hom source coefficient signature", "valid_for_claim": False},
        {"status_id": "STAT2654_1_wep", "area": "WEP input pack", "summary": "MICROSCOPE bound provenance is cached, but executable WEP inputs remain missing", "risk_level": "EMPIRICAL_BRANCH_STRUCTURED_NOT_EXECUTABLE", "project_meaning": "testing route is disciplined: exact files/theorems are named before any WEP score", "next_action": "source-worldtube reduction or official readout/data acquisition", "valid_for_claim": False},
        {"status_id": "STAT2654_2_project_overview", "area": "GR/Newton reduction bridge", "summary": "the theory proof and WEP test route are now separated by explicit gates", "risk_level": "ACTIONABLE_SPLIT", "project_meaning": "we can keep deriving while preparing a real local test without smuggling claims", "next_action": "2655 source-worldtube/readout-data branch", "valid_for_claim": False},
    ]


def branch_copy_rows(owner_rows: list[dict[str, Any]], pack_rows: list[dict[str, Any]], gate_rows: list[dict[str, Any]], dry_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    write_csv(BRANCH_COPIES["queue"], gate_rows)
    write_csv(BRANCH_COPIES["local_bounds"], pack_rows)
    write_csv(BRANCH_COPIES["source_weight"], pack_rows)
    write_csv(BRANCH_COPIES["microscope"], owner_rows)
    write_csv(BRANCH_COPIES["quarantine"], dry_rows)
    return [
        {"copy_id": copy_id, "path": str(path), "exists": path.exists(), "parseable_csv": path.exists() and len(csv_rows(path)) >= 1, "purpose": "2654 WEP input/action-owner nonclaim handoff", "valid_for_claim": False}
        for copy_id, path in BRANCH_COPIES.items()
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    owner = action_owner_attempt_rows()
    pack = wep_input_pack_rows()
    exec_gate = wep_executability_rows()
    dry_cases = dryrun_case_rows()
    dry = dryrun_result_rows(dry_cases)
    rows = {
        "source_register": source_register_rows(),
        "web_cache": web_cache_rows(),
        "action_owner_attempt": owner,
        "action_owner_gate": action_owner_gate_rows(),
        "wep_input_pack": pack,
        "wep_executability": exec_gate,
        "dryrun_cases": dry_cases,
        "dryrun_results": dry,
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }
    rows["branch_copies"] = branch_copy_rows(owner, pack, exec_gate, dry)
    return rows


def generated_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_COPIES.values())


def all_csv_parse(paths: list[Path]) -> bool:
    for path in paths:
        if path.suffix.lower() != ".csv":
            continue
        try:
            csv_rows(path)
        except Exception:
            return False
    return True


def formalization_hit_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = [
        "*2654-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2654*",
        "*Y5_R2FR_WEP_source_worldtube_material_tensor_acquisition_or_action_owner_lemma_2654*",
        "*JR2654*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows["source_register"])
    valid_pdf_rows = [row for row in rows["web_cache"] if row["cache_status"] == "VALID_PDF_PROVENANCE_ONLY"]
    invalid_cache_safe = all(not row["valid_for_claim"] for row in rows["web_cache"] if row["cache_status"] != "VALID_PDF_PROVENANCE_ONLY")
    web_ok = bool(valid_pdf_rows) and invalid_cache_safe
    owner_ok = any(row["attempt_id"] == "ACO2654_6_verdict" and row["status"] == "ACTION_CURRENT_OWNER_NOT_PARENT_DERIVED" for row in rows["action_owner_attempt"])
    pack_ok = len(rows["wep_input_pack"]) >= 9 and all(not row["score_ready"] and not row["valid_prediction_row"] for row in rows["wep_input_pack"])
    exec_ok = all(not row["gate_pass"] and row["blocks_claim"] and not row["valid_for_claim"] for row in rows["wep_executability"])
    dry_ok = all(row["status_match"] and not row["claim_allowed"] for row in rows["dryrun_results"])
    claim_ok = any(row["gate_id"] == "CG2654_3_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]) and all(not row["gate_pass"] for row in rows["claim_gates"])
    next_ok = any("2655-Y5-R2FR-WEP-source-worldtube-point-source-reduction" in row["next_doc"] for row in rows["next_target"])
    branch_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2654_00_sources", source_ok, "all cited source paths exist and required needles are present"),
        ("VAL2654_01_web_cache", web_ok, "at least one WEP source PDF cached; bot-check/invalid caches remain nonclaim"),
        ("VAL2654_02_owner_verdict", owner_ok, "action/current owner remains unsigned"),
        ("VAL2654_03_wep_pack", pack_ok, "WEP input pack is nonclaim/not score-ready"),
        ("VAL2654_04_executability_block", exec_ok, "WEP executable gates all block claim"),
        ("VAL2654_05_dryrun", dry_ok, "dry-run refuses unsigned owner, invalid web cache, missing WEP inputs, bound-only, and cancellation"),
        ("VAL2654_06_claim_gates_false", claim_ok, "claim remains blocked"),
        ("VAL2654_07_next_target", next_ok, "2655 target is recorded"),
        ("VAL2654_08_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2654_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2654_10_formalization_untouched", formal_ok, "no 2654 outputs are written under formalization-workbench"),
        ("VAL2654_11_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
    ]
    generated = stamp()
    out = [
        {"timestamp_utc": generated, "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "valid_for_claim": False, "claim_allowed": False, "validation_id": validation_id, "status": "PASS" if passed else "FAIL", "detail": detail}
        for validation_id, passed, detail in checks
    ]
    out.append(
        {"timestamp_utc": generated, "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "valid_for_claim": False, "claim_allowed": False, "validation_id": "VAL2654_OVERALL", "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL", "detail": "2654 keeps action/current owner unsigned, stages WEP input pack, and selects source-worldtube reduction or official readout data next"}
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 2654 - WEP Source-Worldtube Material Tensor Acquisition Or Action-Owner Lemma

## Purpose

This checkpoint tries the theory route first: derive the action/current owner needed to zero WEP source weights. If that remains unsigned, it stages the WEP input pack required to make the 2653 WEP row executable without claiming a pass.

## Result

- The action/current owner lemma is exact conditionally, but not parent-derived.
- Cached MICROSCOPE material is provenance-only: one PDF bound anchor is valid, while bot-check HTML files are not official arrays/data.
- The WEP input pack is structured but non-executable: source worldtube, source composition, material tensor, readout/force map, tau_WEP and parent residual certificates are missing.
- The next target is the source-worldtube reduction or official readout-data runner.

## Source Register

{markdown_table(rows["source_register"])}

## Web Source Cache Ledger

{markdown_table(rows["web_cache"])}

## Action Current Owner Lemma Attempt

{markdown_table(rows["action_owner_attempt"])}

## Action Current Owner Gate

{markdown_table(rows["action_owner_gate"])}

## WEP Input Pack

{markdown_table(rows["wep_input_pack"])}

## WEP Executability Gate

{markdown_table(rows["wep_executability"])}

## Dry-Run Cases

{markdown_table(rows["dryrun_cases"])}

## Dry-Run Results

{markdown_table(rows["dryrun_results"])}

## Claim Gates

{markdown_table(rows["claim_gates"])}

## Decision Ledger

{markdown_table(rows["decision"])}

## Next Target

{markdown_table(rows["next_target"])}

## Project Status Snapshot

{markdown_table(rows["project_status"])}

## Branch Copies

{markdown_table(rows["branch_copies"])}

## Validation

{markdown_table(validation)}
"""
    DOC_PATH.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows = build_rows()
    for name, table in rows.items():
        if name in OUTPUTS and name != "validation":
            write_csv(OUTPUTS[name], table)
    remove_pycache()
    rows["validation"] = validation_rows(rows, generated_paths())
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)
    remove_pycache()


if __name__ == "__main__":
    main()
