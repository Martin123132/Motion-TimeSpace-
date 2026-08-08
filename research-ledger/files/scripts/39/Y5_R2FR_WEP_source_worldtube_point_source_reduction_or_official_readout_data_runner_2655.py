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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2655"
WEP_SOURCE_CACHE = ROOT / "source-intake" / "wep-sources" / "1899"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2655-Y5-R2FR-WEP-source-worldtube-point-source-reduction-or-official-readout-data-runner.md"

CHECKPOINT = "2655"
BRANCH_ID = "Y5_R2FR_WEP_SOURCE_WORLDTUBE_OR_READOUT_RUNNER_2655"
PREFIX = "P8_Y5_WEP_WORLDTUBE_2655"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "web_cache": RESIDUALS / f"{PREFIX}_WEB_SOURCE_CACHE_LEDGER.csv",
    "point_source_attempt": RESIDUALS / f"{PREFIX}_POINT_SOURCE_REDUCTION_ATTEMPT.csv",
    "residual_ledger": RESIDUALS / f"{PREFIX}_POINT_SOURCE_RESIDUAL_LEDGER_NONCLAIM.csv",
    "official_targets": RESIDUALS / f"{PREFIX}_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv",
    "runner_contract": RESIDUALS / f"{PREFIX}_OFFICIAL_READOUT_DATA_RUNNER_CONTRACT.csv",
    "dryrun_cases": RESIDUALS / f"{PREFIX}_POINT_SOURCE_DATA_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / f"{PREFIX}_POINT_SOURCE_DATA_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2655_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "WEP_worldtube_residual_2655_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "WEP_SOURCE_WORLDTUBE_POINT_SOURCE_2655_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2655_OFFICIAL_READOUT_RUNNER_CONTRACT.csv",
    "quarantine": QUARANTINE / "P8_Y5_2655_POINT_SOURCE_DATA_DRYRUN_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2654_doc": {
        "path": ROOT / "2654-Y5-R2FR-WEP-source-worldtube-material-tensor-acquisition-or-action-owner-lemma.md",
        "needles": ["WIP2654_8_verdict", "WEG2654_6_verdict", "NEXT2654_0_selected", "VAL2654_OVERALL"],
        "role": "immediate WEP input-pack handoff",
    },
    "2653_doc": {
        "path": ROOT / "2653-Y5-R2FR-readout-variation-commutator-zero-or-WEP-projection-row-v1.md",
        "needles": ["WEP2653_7_verdict", "WRQ2653_1_source_worldtube", "WRQ2653_3_readout_arrays", "WRQ2653_5_tau_wep"],
        "role": "WEP projection row and missing readout/source/tau inputs",
    },
    "1225_doc": {
        "path": ROOT / "1225-Y5-R10-tau-WEP-source-worldtube-readout-projection.md",
        "needles": ["TAU1225_6_verdict", "ACQ1225_0_official_readout_arrays", "ACQ1225_4_material_tensor", "ACQ1225_5_delta_w"],
        "role": "tau_WEP and official readout acquisition ledger",
    },
    "1080_doc": {
        "path": ROOT / "1080-Y5-R10-finite-WEP-source-vector-and-material-tensor-acquisition-pack.md",
        "needles": ["BOUND1080_0_MICROSCOPE_WEP_source_charge", "MAT1080_4_full_tensor_upgrade"],
        "role": "MICROSCOPE bound anchor and material tensor precursor",
    },
    "1900_doc": {
        "path": ROOT / "1900-Y5-R2FR-wep-source-worldtube-point-source-reduction-or-official-readout-data-runner.md",
        "needles": ["PSR1900_6_verdict", "DEC1900_2_next", "VAL1900_OVERALL"],
        "role": "older point-source/readout-runner checkpoint to refine rather than bypass",
    },
}

CACHED_WEB_SOURCES: dict[str, dict[str, Any]] = {
    "MICROSCOPE_final_results_arxiv_2209_15487": {
        "url": "https://arxiv.org/pdf/2209.15487",
        "path": WEP_SOURCE_CACHE / "MICROSCOPE_final_results_arxiv_2209_15487.pdf",
        "expected_magic": b"%PDF",
        "role": "valid final-result PDF provenance/bound anchor, not a model prediction",
    },
    "MICROSCOPE_data_processing_HAL_03564498": {
        "url": "https://hal.science/hal-03564498/document",
        "path": WEP_SOURCE_CACHE / "MICROSCOPE_mission_scenario_ground_segment_data_processing_HAL_03564498.botcheck.html",
        "expected_magic": b"%PDF",
        "role": "candidate readout/data-processing source; local cache is bot-check HTML",
    },
    "MICROSCOPE_final_data_analysis_HAL_03854332": {
        "url": "https://hal.science/hal-03854332v1/file/DPHY22007.1642068604.pdf",
        "path": WEP_SOURCE_CACHE / "MICROSCOPE_final_data_analysis_HAL_03854332.botcheck.html",
        "expected_magic": b"%PDF",
        "role": "candidate final-analysis source; local cache is bot-check HTML",
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
                "source_id": f"SRC2655_{source_id}",
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
                "source_id": f"WEB2655_{source_id}",
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


def point_source_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "PSR2655_0_target",
            "claim_piece": "WEP source worldtube point-source/common-mode reduction",
            "formal_statement": "The extended Earth/source worldtube may be replaced by one calibrated common-mode monopole plus a bounded residual vector, with relative source weights kept outside measured GM.",
            "status": "TARGET_SHARP",
            "proof_or_obstruction": "this is the desired Newton/GR-style exterior-source reduction, but only for universal/common-mode source coupling",
            "source_anchor": "2654:WIP2654_1_source_worldtube_profile;1900:PSR1900_0_target",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "PSR2655_1_conditional_monopole_lemma",
            "claim_piece": "universal exterior monopole",
            "formal_statement": "If the active source current is conserved, compactly supported, pulled back to the observed frame, and species-blind, then the exterior leading source leg is the calibrated total monopole GM/r^2 plus declared multipole corrections.",
            "status": "EXACT_CONDITIONAL_LEMMA",
            "proof_or_obstruction": "ordinary Gauss/Newton exterior-source reasoning works for the universal leg; it does not erase non-universal source charges",
            "source_anchor": "1900:PSR1900_1_common_monopole_lemma;2654:WIP2654_5_force_map",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "PSR2655_2_relative_weight_guard",
            "claim_piece": "measured-G/GM cannot hide relative source weights",
            "formal_statement": "GM calibration may absorb only a universal source normalization; Delta_w_source, material/source composition response, projector stress and non-Hilbert residuals must remain explicit product legs.",
            "status": "GUARDRAIL_ACTIVE_NOT_ZERO_PROOF",
            "proof_or_obstruction": "without a parent common-mode theorem, a WEP pass could be faked by folding relative source weights into measured GM",
            "source_anchor": "1900:PSR1900_2_no_relative_hiding;2654:ACO2654_3_classical_rescale_obstruction",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "PSR2655_3_source_composition_profile",
            "claim_piece": "Earth source composition/profile weighting",
            "formal_statement": "The WEP source leg needs an orbit/profile-weighted Earth source vector in the same residual basis as Delta_w_eff, or a theorem proving all such finite-source composition legs are common-mode.",
            "status": "SOURCE_COMPOSITION_PROFILE_OBSTRUCTION_ACTIVE",
            "proof_or_obstruction": "bulk Earth composition is not automatically the same object as the observed-frame worldtube-weighted source vector sampled by MICROSCOPE",
            "source_anchor": "2653:WRQ2653_1_source_worldtube;1225:ACQ1225_2_source_worldtube",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "PSR2655_4_finite_size_orbit_bound",
            "claim_piece": "finite-source multipole and orbit/readout residual",
            "formal_statement": "Finite Earth multipoles, altitude/orbit windows, attitude, masks and force-readout conventions must either be bounded below the WEP tolerance or retained inside K_WEP and tau_WEP.",
            "status": "FINITE_SOURCE_ERROR_BOUND_MISSING",
            "proof_or_obstruction": "the source-worldtube shortcut is not valid until the same observed readout frame controls source, force, orbit, clocks and eta normalization",
            "source_anchor": "2653:WEP2653_5_orbit_readout_force;1225:TAU1225_6_verdict",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "PSR2655_5_tau_dependency",
            "claim_piece": "tau_WEP is not a unity shortcut",
            "formal_statement": "tau_WEP must be derived, sourced, or kept as an explicit nuisance contraction; setting tau_WEP=1 is allowed only after the source, material, readout and coframe maps prove it.",
            "status": "TAU_WEP_PROJECTION_NOT_DERIVED",
            "proof_or_obstruction": "tau_WEP is exactly where source-worldtube, material tensor and official readout meet, so it cannot be guessed away",
            "source_anchor": "2654:WIP2654_6_tau_wep;2653:WRQ2653_5_tau_wep",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "PSR2655_6_verdict",
            "claim_piece": "promote point-source WEP source leg",
            "formal_statement": "Current MTS parent primitives prove the WEP source worldtube reduces to a calibrated common-mode point-source leg with all relative residuals absent or bounded.",
            "status": "SOURCE_WORLDTUBE_POINT_SOURCE_REDUCTION_NOT_PARENT_DERIVED",
            "proof_or_obstruction": "the common monopole lemma is exact conditionally, but source universality, GM-hiding guard, source composition/profile, finite-size/readout error and tau_WEP remain unsigned",
            "source_anchor": "PSR2655_0_target through PSR2655_5_tau_dependency",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def residual_ledger_rows() -> list[dict[str, Any]]:
    return [
        {"residual_id": "PSL2655_0_common_monopole", "residual": "universal/common-mode source normalization", "required_for_zero_or_bound": "parent-signed common-mode current or calibrated universal GM only", "current_status": "CONDITIONAL_COMMON_MODE_ONLY", "units": "m^3 s^-2 or dimensionless after eta normalization", "source_anchor": "PSR2655_1_conditional_monopole_lemma", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"residual_id": "PSL2655_1_relative_source_weights", "residual": "Delta_w_source or source-charge basis coefficients", "required_for_zero_or_bound": "parent theorem-zero, finite prior, or acquired source vector in same basis", "current_status": "MISSING_SOURCE_WEIGHT_VALUES_OR_THEOREM_ZERO", "units": "dimensionless source-charge weights", "source_anchor": "PSR2655_2_relative_weight_guard", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"residual_id": "PSL2655_2_composition_profile", "residual": "orbit/profile-weighted Earth composition/source vector", "required_for_zero_or_bound": "source density/composition profile or theorem reducing it to common mode", "current_status": "MISSING_SOURCE_PROFILE_WEIGHTING", "units": "density/profile SI or normalized kernel", "source_anchor": "PSR2655_3_source_composition_profile", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"residual_id": "PSL2655_3_multipole_finite_size", "residual": "finite-size, J2/multipole and altitude/orbit sampling error", "required_for_zero_or_bound": "finite-source error theorem or official orbit/readout kernel bound", "current_status": "FINITE_SOURCE_ERROR_BOUND_MISSING", "units": "dimensionless eta contribution after readout", "source_anchor": "PSR2655_4_finite_size_orbit_bound", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"residual_id": "PSL2655_4_readout_frame", "residual": "force-map, coframe, attitude and eta-convention residual", "required_for_zero_or_bound": "official readout arrays and same-frame force-to-eta map", "current_status": "OFFICIAL_ARRAYS_AND_FORCE_MAP_MISSING", "units": "m s^-2 internally; dimensionless eta externally", "source_anchor": "2653:WEP2653_5_orbit_readout_force", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"residual_id": "PSL2655_5_tau_contract", "residual": "tau_WEP projection/contraction product", "required_for_zero_or_bound": "derived/sourced tau_WEP or retained nuisance with declared prior", "current_status": "TAU_WEP_PROJECTION_NOT_DERIVED", "units": "dimensionless", "source_anchor": "PSR2655_5_tau_dependency", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"residual_id": "PSL2655_6_acceptance", "residual": "point-source source-worldtube residual pack", "required_for_zero_or_bound": "PSL2655_1 through PSL2655_5 zeroed, bounded, or acquired with sources", "current_status": "POINT_SOURCE_RESIDUAL_PACK_NOT_EXECUTABLE_NONCLAIM", "units": "dimensionless eta envelope", "source_anchor": "PSL2655_0_common_monopole through PSL2655_5_tau_contract", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
    ]


def official_target_rows() -> list[dict[str, Any]]:
    bound_path = WEP_SOURCE_CACHE / "MICROSCOPE_final_results_arxiv_2209_15487.pdf"
    hal_processing = WEP_SOURCE_CACHE / "MICROSCOPE_mission_scenario_ground_segment_data_processing_HAL_03564498.botcheck.html"
    hal_analysis = WEP_SOURCE_CACHE / "MICROSCOPE_final_data_analysis_HAL_03854332.botcheck.html"
    return [
        {"target_id": "ODT2655_0_bound_pdf", "target": "MICROSCOPE final-result bound PDF", "required_form": "source-backed bound/provenance PDF", "local_candidate": str(bound_path), "source_url": "https://arxiv.org/pdf/2209.15487", "current_status": "SOURCE_PDF_CACHED_BOUND_ANCHOR_ONLY", "units": "dimensionless eta", "source_anchor": "WEB2655_MICROSCOPE_final_results_arxiv_2209_15487", "blocks_claim": True, "usable_for_claim": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"target_id": "ODT2655_1_processing_pdf", "target": "MICROSCOPE data-processing publication", "required_form": "valid PDF or source-backed official data-processing file", "local_candidate": str(hal_processing), "source_url": "https://hal.science/hal-03564498/document", "current_status": "LOCAL_CACHE_BOTCHECK_HTML_NOT_USABLE", "units": "provenance only", "source_anchor": "WEB2655_MICROSCOPE_data_processing_HAL_03564498", "blocks_claim": True, "usable_for_claim": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"target_id": "ODT2655_2_final_analysis_pdf", "target": "MICROSCOPE final analysis publication", "required_form": "valid PDF or source-backed official data-analysis file", "local_candidate": str(hal_analysis), "source_url": "https://hal.science/hal-03854332v1/file/DPHY22007.1642068604.pdf", "current_status": "LOCAL_CACHE_BOTCHECK_HTML_NOT_USABLE", "units": "provenance only", "source_anchor": "WEB2655_MICROSCOPE_final_data_analysis_HAL_03854332", "blocks_claim": True, "usable_for_claim": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"target_id": "ODT2655_3_official_arrays", "target": "official MICROSCOPE CMSM/export readout arrays", "required_form": "time, segment/session id, orbit/attitude, masks, calibration flags, readout axes and uncertainties", "local_candidate": "MISSING", "source_url": "not_acquired", "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED", "units": "time, frame, m s^-2 or declared readout units", "source_anchor": "1225:ACQ1225_0_official_readout_arrays", "blocks_claim": True, "usable_for_claim": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"target_id": "ODT2655_4_source_worldtube", "target": "Earth/source worldtube and composition profile", "required_form": "observed-frame stress/density/composition profile or theorem-reduced common-mode source", "local_candidate": "MISSING", "source_url": "not_acquired", "current_status": "MISSING_SOURCE_PROFILE_WEIGHTING", "units": "SI density/profile or normalized dimensionless kernel", "source_anchor": "2654:WIP2654_1_source_worldtube_profile", "blocks_claim": True, "usable_for_claim": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"target_id": "ODT2655_5_material_tensor", "target": "TA6V minus PtRh10 material response tensor", "required_form": "full response tensor to Delta_w_eff/source-weight basis", "local_candidate": "MISSING", "source_url": "not_acquired", "current_status": "MISSING_FULL_MATERIAL_TENSOR", "units": "dimensionless sensitivities per residual basis entry", "source_anchor": "2654:WIP2654_3_material_tensor;1080:MAT1080_4_full_tensor_upgrade", "blocks_claim": True, "usable_for_claim": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"target_id": "ODT2655_6_force_eta_map", "target": "force-to-eta readout map and convention", "required_form": "same-frame map from residual source acceleration to eta_TiPt with sign/normalization", "local_candidate": "MISSING", "source_url": "not_acquired", "current_status": "MISSING_FORCE_READOUT_MAP", "units": "m s^-2 internally; dimensionless eta after normalization", "source_anchor": "2654:WIP2654_5_force_map", "blocks_claim": True, "usable_for_claim": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"target_id": "ODT2655_7_tau_wep", "target": "tau_WEP contraction/projection input", "required_form": "derived/sourced tau_WEP or explicit nuisance prior; unity shortcut forbidden", "local_candidate": "MISSING", "source_url": "not_acquired", "current_status": "TAU_WEP_PROJECTION_NOT_DERIVED", "units": "dimensionless", "source_anchor": "2654:WIP2654_6_tau_wep;1225:TAU1225_6_verdict", "blocks_claim": True, "usable_for_claim": False, "valid_prediction_row": False, "valid_for_claim": False},
    ]


def runner_contract_rows() -> list[dict[str, Any]]:
    return [
        {"contract_id": "RDR2655_0_purpose", "contract_piece": "official readout/data runner role", "requirement": "dry-run only until official arrays, source worldtube, material tensor, force map and tau_WEP exist", "current_status": "RUNNER_CONTRACT_STAGED_NONCLAIM", "blocks_claim": True, "score_ready": False, "valid_for_claim": False},
        {"contract_id": "RDR2655_1_inputs", "contract_piece": "required inputs", "requirement": "CMSM/export arrays, orbit/attitude, masks/calibration, eta convention, source register, material tensor, checksum/manifest", "current_status": "INPUTS_NOT_ACQUIRED", "blocks_claim": True, "score_ready": False, "valid_for_claim": False},
        {"contract_id": "RDR2655_2_cache_validation", "contract_piece": "cache validation", "requirement": "reject bot-check HTML and require PDF/CSV/netCDF/HDF5/official archive magic, source URL, checksum and units", "current_status": "BOTCHECK_HTML_REJECTED", "blocks_claim": True, "score_ready": False, "valid_for_claim": False},
        {"contract_id": "RDR2655_3_outputs", "contract_piece": "future run output layout", "requirement": "runs/<timestamp>/log.txt, status.json, manifest.csv, source_register.csv, readout_schema.csv and completion marker", "current_status": "OUTPUT_LAYOUT_DECLARED_ONLY", "blocks_claim": True, "score_ready": False, "valid_for_claim": False},
        {"contract_id": "RDR2655_4_no_claim_policy", "contract_piece": "claim discipline", "requirement": "data acquisition and bound anchors do not count as a prediction or local-GR/WEP pass", "current_status": "NO_CLAIM_POLICY_ACTIVE", "blocks_claim": True, "score_ready": False, "valid_for_claim": False},
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {"case_id": "DRY2655_0_no_reduction", "point_source_parent_signed": False, "hides_relative_in_gm": False, "source_vector_present": False, "material_tensor_present": False, "official_readout_present": False, "force_map_present": False, "tau_wep_is_unity": False, "bound_anchor_only": True, "uses_surrogate_as_official": False, "botcheck_as_data": False, "uses_cancellation": False, "expected_status": "REFUSED_POINT_SOURCE_REDUCTION_NOT_DERIVED", "valid_for_claim": False},
        {"case_id": "DRY2655_1_gm_hiding", "point_source_parent_signed": True, "hides_relative_in_gm": True, "source_vector_present": True, "material_tensor_present": True, "official_readout_present": True, "force_map_present": True, "tau_wep_is_unity": False, "bound_anchor_only": False, "uses_surrogate_as_official": False, "botcheck_as_data": False, "uses_cancellation": False, "expected_status": "REFUSED_MEASURED_GM_RELATIVE_WEIGHT_HIDING", "valid_for_claim": False},
        {"case_id": "DRY2655_2_source_vector", "point_source_parent_signed": True, "hides_relative_in_gm": False, "source_vector_present": False, "material_tensor_present": True, "official_readout_present": True, "force_map_present": True, "tau_wep_is_unity": False, "bound_anchor_only": False, "uses_surrogate_as_official": False, "botcheck_as_data": False, "uses_cancellation": False, "expected_status": "REFUSED_SOURCE_VECTOR_MISSING", "valid_for_claim": False},
        {"case_id": "DRY2655_3_material_tensor", "point_source_parent_signed": True, "hides_relative_in_gm": False, "source_vector_present": True, "material_tensor_present": False, "official_readout_present": True, "force_map_present": True, "tau_wep_is_unity": False, "bound_anchor_only": False, "uses_surrogate_as_official": False, "botcheck_as_data": False, "uses_cancellation": False, "expected_status": "REFUSED_MATERIAL_TENSOR_MISSING", "valid_for_claim": False},
        {"case_id": "DRY2655_4_surrogate", "point_source_parent_signed": True, "hides_relative_in_gm": False, "source_vector_present": True, "material_tensor_present": True, "official_readout_present": False, "force_map_present": True, "tau_wep_is_unity": False, "bound_anchor_only": False, "uses_surrogate_as_official": True, "botcheck_as_data": False, "uses_cancellation": False, "expected_status": "REFUSED_SURROGATE_AS_OFFICIAL", "valid_for_claim": False},
        {"case_id": "DRY2655_5_botcheck", "point_source_parent_signed": True, "hides_relative_in_gm": False, "source_vector_present": True, "material_tensor_present": True, "official_readout_present": True, "force_map_present": True, "tau_wep_is_unity": False, "bound_anchor_only": False, "uses_surrogate_as_official": False, "botcheck_as_data": True, "uses_cancellation": False, "expected_status": "REFUSED_BOTCHECK_HTML_AS_OFFICIAL_DATA", "valid_for_claim": False},
        {"case_id": "DRY2655_6_official_readout", "point_source_parent_signed": True, "hides_relative_in_gm": False, "source_vector_present": True, "material_tensor_present": True, "official_readout_present": False, "force_map_present": True, "tau_wep_is_unity": False, "bound_anchor_only": False, "uses_surrogate_as_official": False, "botcheck_as_data": False, "uses_cancellation": False, "expected_status": "REFUSED_OFFICIAL_READOUT_MISSING", "valid_for_claim": False},
        {"case_id": "DRY2655_7_force_map", "point_source_parent_signed": True, "hides_relative_in_gm": False, "source_vector_present": True, "material_tensor_present": True, "official_readout_present": True, "force_map_present": False, "tau_wep_is_unity": False, "bound_anchor_only": False, "uses_surrogate_as_official": False, "botcheck_as_data": False, "uses_cancellation": False, "expected_status": "REFUSED_FORCE_MAP_MISSING", "valid_for_claim": False},
        {"case_id": "DRY2655_8_tau_unity", "point_source_parent_signed": True, "hides_relative_in_gm": False, "source_vector_present": True, "material_tensor_present": True, "official_readout_present": True, "force_map_present": True, "tau_wep_is_unity": True, "bound_anchor_only": False, "uses_surrogate_as_official": False, "botcheck_as_data": False, "uses_cancellation": False, "expected_status": "REFUSED_TAU_WEP_UNITY_SHORTCUT", "valid_for_claim": False},
        {"case_id": "DRY2655_9_bound_anchor", "point_source_parent_signed": True, "hides_relative_in_gm": False, "source_vector_present": True, "material_tensor_present": True, "official_readout_present": True, "force_map_present": True, "tau_wep_is_unity": False, "bound_anchor_only": True, "uses_surrogate_as_official": False, "botcheck_as_data": False, "uses_cancellation": False, "expected_status": "REFUSED_BOUND_ANCHOR_ONLY", "valid_for_claim": False},
        {"case_id": "DRY2655_10_cancellation", "point_source_parent_signed": True, "hides_relative_in_gm": False, "source_vector_present": True, "material_tensor_present": True, "official_readout_present": True, "force_map_present": True, "tau_wep_is_unity": False, "bound_anchor_only": False, "uses_surrogate_as_official": False, "botcheck_as_data": False, "uses_cancellation": True, "expected_status": "REFUSED_CANCELLATION_ONLY", "valid_for_claim": False},
        {"case_id": "DRY2655_11_counterfactual", "point_source_parent_signed": True, "hides_relative_in_gm": False, "source_vector_present": True, "material_tensor_present": True, "official_readout_present": True, "force_map_present": True, "tau_wep_is_unity": False, "bound_anchor_only": False, "uses_surrogate_as_official": False, "botcheck_as_data": False, "uses_cancellation": False, "expected_status": "COUNTERFACTUAL_READY_NOT_CURRENT_CLAIM", "valid_for_claim": False},
    ]


def evaluate_dryrun(row: dict[str, Any]) -> str:
    if not row["point_source_parent_signed"]:
        return "REFUSED_POINT_SOURCE_REDUCTION_NOT_DERIVED"
    if row["hides_relative_in_gm"]:
        return "REFUSED_MEASURED_GM_RELATIVE_WEIGHT_HIDING"
    if not row["source_vector_present"]:
        return "REFUSED_SOURCE_VECTOR_MISSING"
    if not row["material_tensor_present"]:
        return "REFUSED_MATERIAL_TENSOR_MISSING"
    if row["uses_surrogate_as_official"]:
        return "REFUSED_SURROGATE_AS_OFFICIAL"
    if row["botcheck_as_data"]:
        return "REFUSED_BOTCHECK_HTML_AS_OFFICIAL_DATA"
    if not row["official_readout_present"]:
        return "REFUSED_OFFICIAL_READOUT_MISSING"
    if not row["force_map_present"]:
        return "REFUSED_FORCE_MAP_MISSING"
    if row["tau_wep_is_unity"]:
        return "REFUSED_TAU_WEP_UNITY_SHORTCUT"
    if row["bound_anchor_only"]:
        return "REFUSED_BOUND_ANCHOR_ONLY"
    if row["uses_cancellation"]:
        return "REFUSED_CANCELLATION_ONLY"
    return "COUNTERFACTUAL_READY_NOT_CURRENT_CLAIM"


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = stamp()
    return [
        {
            "case_id": row["case_id"],
            "computed_status": evaluate_dryrun(row),
            "expected_status": row["expected_status"],
            "status_match": evaluate_dryrun(row) == row["expected_status"],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in cases
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "CG2655_0_point_source", "condition": "source-worldtube point-source/common-mode reduction is parent-signed", "current_status": "FAIL_SOURCE_WORLDTUBE_POINT_SOURCE_REDUCTION_NOT_PARENT_DERIVED", "source_anchor": f"{OUTPUTS['point_source_attempt'].name}:PSR2655_6_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2655_1_residual_pack", "condition": "relative source vector, finite-source residual, readout frame and tau_WEP are zeroed/bounded/acquired", "current_status": "FAIL_POINT_SOURCE_RESIDUAL_PACK_NOT_EXECUTABLE_NONCLAIM", "source_anchor": f"{OUTPUTS['residual_ledger'].name}:PSL2655_6_acceptance", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2655_2_official_data", "condition": "official readout data targets are acquired and cache-validated", "current_status": "FAIL_OFFICIAL_DATA_TARGETS_NOT_ACQUIRED_NONCLAIM", "source_anchor": f"{OUTPUTS['official_targets'].name}:ODT2655_3_official_arrays", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2655_3_no_shortcuts", "condition": "no measured-G hiding, tau=1, surrogate-as-official, bot-check-as-data, bound-only, or cancellation pass", "current_status": "PASS_GUARDS_ENFORCED_BUT_NONCLAIM", "source_anchor": OUTPUTS["dryrun_results"].name, "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2655_4_verdict", "condition": "WEP source-worldtube/readout branch can support local-GR/WEP claim", "current_status": "CLAIM_BLOCKED", "source_anchor": "CG2655_0_point_source through CG2655_3_no_shortcuts", "gate_pass": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC2655_0_point_source", "decision": "DO_NOT_PROMOTE_POINT_SOURCE_REDUCTION", "reason": "the exterior common-mode monopole lemma is exact, but the relative source-weight, source-composition, finite-size/readout and tau_WEP clauses are unsigned", "status": "POINT_SOURCE_ROUTE_SHARP_BUT_UNSIGNED", "next_dependency": "derive/bound residual pack or acquire official source/readout/material inputs", "valid_for_claim": False},
        {"decision_id": "DEC2655_1_data_runner", "decision": "OFFICIAL_READOUT_DATA_RUNNER_STAGED_NONCLAIM", "reason": "the valid PDF is a bound/provenance anchor only; HAL candidate caches are bot-check HTML and official arrays are not imported", "status": "OFFICIAL_DATA_RUNNER_CONTRACT_STAGED_NONCLAIM", "next_dependency": "official MICROSCOPE readout arrays or source-backed exact equivalent", "valid_for_claim": False},
        {"decision_id": "DEC2655_2_next", "decision": "SELECT_2656_OFFICIAL_READOUT_DRY_RUN_OR_SOURCE_RESIDUAL_BOUND", "reason": "2655 narrows the WEP local branch to two honest paths: acquire official readout data or prove a finite source-worldtube residual bound", "status": "NEXT_TARGET_SELECTED", "next_dependency": "2656 official MICROSCOPE readout data dry-run or source-worldtube residual bound", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2655_0_selected",
            "status": "selected",
            "next_doc": "2656-Y5-R2FR-official-MICROSCOPE-readout-data-dry-run-or-source-worldtube-residual-bound.md",
            "next_script": "scripts/Y5_R2FR_official_MICROSCOPE_readout_data_dry_run_or_source_worldtube_residual_bound_2656.py",
            "target": "Try the least-scrutinized honest path: either dry-run acquisition of official MICROSCOPE readout arrays, or derive a finite source-worldtube residual bound that makes the point-source branch legitimate.",
            "must_include": "official data source manifest; cache magic/checksum rules; source-worldtube residual inequality; tau_WEP dependency; no-shortcut refusal cases",
            "must_exclude": "GitHub action, formalization-workbench edits, bound-only WEP claim, measured-G hiding, tau_WEP=1 shortcut, bot-check HTML as data",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {"status_id": "STAT2655_0_theory", "area": "source-worldtube reduction", "summary": "the common-mode exterior point-source theorem is exact conditionally, but MTS has not yet proved the non-universal residuals vanish or are bounded", "risk_level": "DERIVATION_GAP_NARROWED", "project_meaning": "the local-GR bridge is not dead; it has a precise unsigned clause instead of a vague gap", "next_action": "prove residual bound or keep worldtube/readout kernel explicit", "valid_for_claim": False},
        {"status_id": "STAT2655_1_data", "area": "MICROSCOPE WEP readout", "summary": "valid final-result PDF exists as provenance, but official arrays/material/source/tau inputs are still absent", "risk_level": "EMPIRICAL_BRANCH_STRUCTURED_NOT_EXECUTABLE", "project_meaning": "the WEP test branch is prepared but not allowed to score itself from a bound anchor", "next_action": "acquire official arrays or create a dry-run manifest that refuses missing data", "valid_for_claim": False},
        {"status_id": "STAT2655_2_project_overview", "area": "GR/Newton reduction bridge", "summary": "WEP/local-GR now has a clean fork: derive a source-worldtube residual theorem or run official-data acquisition without shortcuts", "risk_level": "HARD_BUT_ACTIONABLE", "project_meaning": "this is the right kind of hard: fewer escape hatches, clearer mathematical pressure", "next_action": "2656 official readout dry-run or finite source-worldtube residual bound", "valid_for_claim": False},
    ]


def branch_copy_rows(point_rows: list[dict[str, Any]], residual_rows: list[dict[str, Any]], target_rows: list[dict[str, Any]], contract_rows: list[dict[str, Any]], dry_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    write_csv(BRANCH_COPIES["queue"], target_rows)
    write_csv(BRANCH_COPIES["local_bounds"], residual_rows)
    write_csv(BRANCH_COPIES["source_weight"], point_rows)
    write_csv(BRANCH_COPIES["microscope"], contract_rows)
    write_csv(BRANCH_COPIES["quarantine"], dry_rows)
    return [
        {"copy_id": copy_id, "path": str(path), "exists": path.exists(), "parseable_csv": path.exists() and len(csv_rows(path)) >= 1, "purpose": "2655 WEP source-worldtube/readout nonclaim handoff", "valid_for_claim": False}
        for copy_id, path in BRANCH_COPIES.items()
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    point = point_source_attempt_rows()
    residual = residual_ledger_rows()
    targets = official_target_rows()
    contract = runner_contract_rows()
    dry_cases = dryrun_case_rows()
    dry = dryrun_result_rows(dry_cases)
    rows = {
        "source_register": source_register_rows(),
        "web_cache": web_cache_rows(),
        "point_source_attempt": point,
        "residual_ledger": residual,
        "official_targets": targets,
        "runner_contract": contract,
        "dryrun_cases": dry_cases,
        "dryrun_results": dry,
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }
    rows["branch_copies"] = branch_copy_rows(point, residual, targets, contract, dry)
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
        "*2655-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2655*",
        "*Y5_R2FR_WEP_source_worldtube_point_source_reduction_or_official_readout_data_runner_2655*",
        "*JR2655*",
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
    point_ok = any(row["attempt_id"] == "PSR2655_6_verdict" and row["status"] == "SOURCE_WORLDTUBE_POINT_SOURCE_REDUCTION_NOT_PARENT_DERIVED" for row in rows["point_source_attempt"])
    residual_ok = any(row["residual_id"] == "PSL2655_6_acceptance" and row["current_status"] == "POINT_SOURCE_RESIDUAL_PACK_NOT_EXECUTABLE_NONCLAIM" for row in rows["residual_ledger"]) and all(not row["score_ready"] and not row["valid_prediction_row"] for row in rows["residual_ledger"])
    target_ok = len(rows["official_targets"]) >= 8 and all(not row["usable_for_claim"] and not row["valid_prediction_row"] for row in rows["official_targets"])
    contract_ok = all(row["blocks_claim"] and not row["score_ready"] and not row["valid_for_claim"] for row in rows["runner_contract"])
    dry_ok = all(row["status_match"] and not row["claim_allowed"] for row in rows["dryrun_results"])
    claim_ok = any(row["gate_id"] == "CG2655_4_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]) and all(not row["gate_pass"] for row in rows["claim_gates"])
    next_ok = any("2656-Y5-R2FR-official-MICROSCOPE-readout-data-dry-run" in row["next_doc"] for row in rows["next_target"])
    branch_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2655_00_sources", source_ok, "all cited source paths exist and required needles are present"),
        ("VAL2655_01_web_cache", web_ok, "valid PDF is provenance-only; bot-check/invalid caches remain nonclaim"),
        ("VAL2655_02_point_source_verdict", point_ok, "point-source source-worldtube reduction remains unsigned"),
        ("VAL2655_03_residual_ledger", residual_ok, "point-source residual ledger is nonclaim/not score-ready"),
        ("VAL2655_04_official_targets", target_ok, "official readout targets remain nonclaim/not acquired; bound PDF not promoted"),
        ("VAL2655_05_runner_contract", contract_ok, "runner contract blocks claim until source/readout/material/tau inputs exist"),
        ("VAL2655_06_dryrun", dry_ok, "dry-run refuses overpromotion, GM hiding, missing inputs, surrogate, bot-check, tau=1, bound-only and cancellation"),
        ("VAL2655_07_claim_gates_false", claim_ok, "claim remains blocked"),
        ("VAL2655_08_next_target", next_ok, "2656 target is recorded"),
        ("VAL2655_09_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2655_10_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2655_11_formalization_untouched", formal_ok, "no 2655 outputs are written under formalization-workbench"),
        ("VAL2655_12_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
    ]
    generated = stamp()
    out = [
        {"timestamp_utc": generated, "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "valid_for_claim": False, "claim_allowed": False, "validation_id": validation_id, "status": "PASS" if passed else "FAIL", "detail": detail}
        for validation_id, passed, detail in checks
    ]
    out.append(
        {"timestamp_utc": generated, "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "valid_for_claim": False, "claim_allowed": False, "validation_id": "VAL2655_OVERALL", "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL", "detail": "2655 keeps point-source source-worldtube reduction unsigned, stages official readout runner, and selects 2656 residual-bound/data dry-run fork"}
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 2655 - WEP Source-Worldtube Point-Source Reduction Or Official Readout Data Runner

## Purpose

This checkpoint tries the derivation-first route for the WEP source leg: can the source worldtube be reduced to a calibrated common-mode point source without hiding relative source weights in measured GM? If not, it stages the official readout/data runner contract and keeps every row nonclaim.

## Result

- The exterior common-mode monopole lemma is exact conditionally.
- The full MTS point-source WEP source-worldtube reduction is not parent-derived yet.
- The residual pack is now explicit: relative source weights, source profile, finite-size/orbit terms, readout frame and tau_WEP all remain live.
- The official readout/data runner is staged as a nonclaim contract; valid PDF evidence is provenance-only and bot-check HTML is rejected as data.
- The next target is 2656: either acquire/dry-run official MICROSCOPE readout data, or derive a finite source-worldtube residual bound.

## Source Register

{markdown_table(rows["source_register"])}

## Web Source Cache Ledger

{markdown_table(rows["web_cache"])}

## Point-Source Reduction Attempt

{markdown_table(rows["point_source_attempt"])}

## Point-Source Residual Ledger

{markdown_table(rows["residual_ledger"])}

## Official Readout Data Targets

{markdown_table(rows["official_targets"])}

## Official Readout Data Runner Contract

{markdown_table(rows["runner_contract"])}

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
