from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
WEP_SOURCES_1899 = ROOT / "source-intake" / "wep-sources" / "1899"
WEP_SOURCES_1900 = ROOT / "source-intake" / "wep-sources" / "1900"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1900"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1900-Y5-R2FR-wep-source-worldtube-point-source-reduction-or-official-readout-data-runner.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1899_doc": ROOT / "1899-Y5-R2FR-wep-source-worldtube-material-tensor-acquisition-or-action-owner-lemma.md",
    "1899_validation": OUT / "P8_Y5_BRR545_1899_VALIDATION.csv",
    "1899_action_owner": OUT / "P8_Y5_PARENT_QLOC_1899_ACTION_CURRENT_OWNER_LEMMA_ATTEMPT.csv",
    "1899_wep_pack": OUT / "P8_Y5_PARENT_QLOC_1899_WEP_INPUT_PACK_NONCLAIM.csv",
    "1899_next": OUT / "P8_Y5_PARENT_QLOC_1899_NEXT_TARGET.csv",
    "1899_web_cache": OUT / "P8_Y5_PARENT_QLOC_1899_WEB_SOURCE_CACHE_LEDGER.csv",
    "1456_worldtube_theorem": OUT / "P8_Y5_R10_1456_SOURCE_WORLDTUBE_PROJECTION_THEOREM_ATTEMPT.csv",
    "1817_transfer_kernel": OUT / "P8_Y5_PARENT_QLOC_1817_SOURCE_WORLDTUBE_TRANSFER_KERNEL_THEOREM.csv",
    "926_worldtube_equality": OUT / "P8_Y5_R10_926_SOURCE_WORLDTUBE_EQUALITY_ATTEMPT.csv",
    "1068_worldtube_requirements": OUT / "P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv",
    "1455_acquisition": OUT / "P8_Y5_R10_1455_SOURCE_WORLDTUBE_ACQUISITION_LEDGER_NONCLAIM.csv",
    "1456_file_ledger": OUT / "P8_Y5_R10_1456_SOURCE_WORLDTUBE_FILE_LEDGER_NONCLAIM.csv",
    "1457_pilot": OUT / "P8_Y5_R10_1457_SOURCE_WORLDTUBE_PILOT_LEDGER_NONCLAIM.csv",
    "1071_suep_segments": OUT / "P8_Y5_R10_1071_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv",
    "1075_surrogate_design": OUT / "P8_Y5_R10_1075_SURROGATE_DESIGN_MATRIX_SEGMENT210.csv",
    "1084_readout_gate": OUT / "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
    "1013_gm_obstruction": OUT / "P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv",
    "1244_gm_convention": OUT / "P8_Y5_R10_1244_GM_CONVENTION_PACK.csv",
    "683_same_frame": OUT / "P8_Y5_R10_683_SAME_FRAME_GM_GATE.csv",
    "1080_earth_candidates": OUT / "P8_Y5_R10_1080_EARTH_SOURCE_VECTOR_CANDIDATES.csv",
    "1083_dd_earth": OUT / "P8_Y5_R10_1083_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv",
    "1083_caveat_gate": OUT / "P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv",
    "1419_source_residual": OUT / "P8_Y5_R10_1419_SOURCE_RESIDUAL_COEFFICIENT_VECTOR.csv",
    "1424_source_contract": OUT / "P8_Y5_R10_1424_SOURCE_VECTOR_CONTRACT.csv",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
}


SOURCE_NEEDLES = {
    "1899_doc": ["ACTION_CURRENT_OWNER_NOT_PARENT_DERIVED", "WEP_INPUT_PACK_NOT_EXECUTABLE_NONCLAIM"],
    "1899_validation": ["VAL1899_OVERALL,PASS"],
    "1899_action_owner": ["ACO1899_6_verdict", "ACTION_CURRENT_OWNER_NOT_PARENT_DERIVED"],
    "1899_wep_pack": ["WIP1899_8_verdict", "WEP_INPUT_PACK_NOT_EXECUTABLE_NONCLAIM"],
    "1899_next": ["NEXT1899_0_primary", "source-worldtube reduction"],
    "1899_web_cache": ["CACHED_VALID_PDF_NONCLAIM", "CACHE_PRESENT_BUT_NOT_VALID_PDF_NONCLAIM"],
    "1456_worldtube_theorem": ["SWP1456_6_verdict", "THEOREM_CONDITIONAL_NOT_PROMOTED"],
    "1817_transfer_kernel": ["KWT1817_6_verdict", "CONDITIONAL_THEOREM_NOT_CURRENT_PROOF"],
    "926_worldtube_equality": ["SWT926_0_observed_source_support", "SWT926_3_Gauss_readout_after_glue"],
    "1068_worldtube_requirements": ["SWT1068_5_verdict", "SOURCE_WORLDTUBE_NOT_ACQUIRED"],
    "1455_acquisition": ["SW1455_0_earth_source", "UNITY_FORBIDDEN"],
    "1456_file_ledger": ["SFI1456_0_source_worldtube_file", "MISSING_OFFICIAL_READOUT_FILE"],
    "1457_pilot": ["PILOT1457_7_verdict", "PILOT_BLOCKED_NONCLAIM"],
    "1071_suep_segments": ["SUEP1071_210", "segment/window metadata only"],
    "1075_surrogate_design": ["SURROGATE_DESIGN_MATRIX_NOT_OFFICIAL"],
    "1084_readout_gate": ["RIG1084_0_CMSM_arrays", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
    "1013_gm_obstruction": ["OBS1013_7_calibration_PPN_tail", "MISSING_GAUSS_ORBITAL_PPN_RESIDUAL"],
    "1244_gm_convention": ["GM1244_2_measured_GM", "CONVENTION_DECLARED_SOURCE_STILL_REQUIRED_FOR_RAW_QR"],
    "683_same_frame": ["SFG683_6_final", "six blocking gates remain open"],
    "1080_earth_candidates": ["EARTH1080_3_common_mode_alternative", "THEOREM_ROUTE_NOT_SIGNED"],
    "1083_dd_earth": ["DD_EARTH1083_0_bulk_weighted", "NUMERIC_BULK_EARTH_DD_SOURCE_VECTOR_NONCLAIM"],
    "1083_caveat_gate": ["SCG1083_0_profile_weighting", "NO_ABSORPTION_SHORTCUT_ALLOWED"],
    "1419_source_residual": ["SRCV1419_5_verdict", "VECTOR_DECLARED_VALUES_MISSING"],
    "1424_source_contract": ["SRCMAP1424_0_R_source", "MISSING_SOURCE_VECTOR"],
    "local_bound_claims": ["R1_WEP_source_charge", "2.8e-15"],
}


OFFICIAL_TARGETS = {
    "cmsm_ds_onera_root": {
        "url": "https://cmsm-ds.onera.fr/",
        "local_path": WEP_SOURCES_1900 / "cmsm_ds_onera_root.html",
        "expected_artifact": "portal or downloadable CMSM/SUEP export listing",
        "prefight_status": "REMOTE_CONNECT_FAILED_IN_1900_PREFLIGHT",
    },
    "cmsm_ds_onera_segment_22": {
        "url": "https://cmsm-ds.onera.fr/22",
        "local_path": WEP_SOURCES_1900 / "cmsm_ds_onera_22.html",
        "expected_artifact": "candidate segment/session data endpoint",
        "prefight_status": "REMOTE_CONNECT_FAILED_IN_1900_PREFLIGHT",
    },
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1900_SOURCE_REGISTER.csv",
    "point_source_attempt": OUT / "P8_Y5_PARENT_QLOC_1900_WEP_SOURCE_WORLDTUBE_POINT_SOURCE_REDUCTION_ATTEMPT.csv",
    "point_source_residuals": OUT / "P8_Y5_PARENT_QLOC_1900_WEP_POINT_SOURCE_RESIDUAL_LEDGER_NONCLAIM.csv",
    "official_data_targets": OUT / "P8_Y5_PARENT_QLOC_1900_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv",
    "data_runner_contract": OUT / "P8_Y5_PARENT_QLOC_1900_OFFICIAL_READOUT_DATA_RUNNER_CONTRACT.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1900_POINT_SOURCE_DATA_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1900_POINT_SOURCE_DATA_DRYRUN_RESULTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1900_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1900_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1900_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1900_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1900_VALIDATION.csv",
}


BRANCH_COPIES = {
    "point_source_attempt": MICROSCOPE_RESIDUALS / OUTPUTS["point_source_attempt"].name,
    "point_source_residuals": SOURCE_WEIGHT_DOCS / "WEP_POINT_SOURCE_RESIDUAL_LEDGER_1900_NONCLAIM.csv",
    "official_data_targets": QUEUE / "JR1900_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv",
    "dryrun_results": QUARANTINE / OUTPUTS["dryrun_results"].name,
}


def ensure_dirs() -> None:
    for path in [OUT, WEP_SOURCES_1900, MICROSCOPE_RESIDUALS, QUEUE, SOURCE_WEIGHT_DOCS, QUARANTINE]:
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
    return path.read_bytes()[:size].decode("ascii", errors="replace")


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


def point_source_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "PSR1900_0_target",
            "claim_piece": "WEP source worldtube point-source reduction",
            "formal_statement": "For the WEP source leg, the extended Earth worldtube may be replaced by a calibrated point-source monopole only for universal/common-mode coupling, with all relative source-weight residuals left outside measured GM.",
            "status": "TARGET_SHARP",
            "proof_or_obstruction": "this is the exact Newton/GR-style reduction wanted: exterior point mass for the universal source, not a hiding place for composition-dependent source weights",
            "source_anchor": "P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv:SWT1068_3_finite_source_correction; P8_Y5_R10_1456_SOURCE_WORLDTUBE_PROJECTION_THEOREM_ATTEMPT.csv:SWP1456_3_measured_G_guard",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "PSR1900_1_common_monopole_lemma",
            "claim_piece": "universal exterior monopole",
            "formal_statement": "If J_H is conserved, the source support is fixed before readout, G_ref is universal, and all source response is common-mode, then the exterior leading source leg is GM_Earth/r^2 plus bounded multipoles.",
            "status": "EXACT_CONDITIONAL_LEMMA",
            "proof_or_obstruction": "this is ordinary Newton/Gauss reasoning: outside the source, only total calibrated monopole controls the leading common acceleration",
            "source_anchor": "P8_Y5_R10_926_SOURCE_WORLDTUBE_EQUALITY_ATTEMPT.csv:SWT926_3_Gauss_readout_after_glue; P8_Y5_PARENT_QLOC_1817_SOURCE_WORLDTUBE_TRANSFER_KERNEL_THEOREM.csv:KWT1817_2_worldtube_support",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "PSR1900_2_no_relative_hiding",
            "claim_piece": "measured GM common-mode guard",
            "formal_statement": "GM calibration may absorb only the universal source normalization; Delta_w_source, material-dependent source composition, projector stress, and non-Hilbert residuals must remain explicit WEP product legs.",
            "status": "GUARDRAIL_ACTIVE_NOT_ZERO_PROOF",
            "proof_or_obstruction": "measured GM is exactly where a fake pass can hide relative source weights; the guard is written but not parent/numerically closed",
            "source_anchor": "P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv:OBS1013_0_projected_extra_current; P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv:SCG1083_3_no_measured_G_absorption",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "PSR1900_3_source_composition_obstruction",
            "claim_piece": "Earth source composition/worldtube weighting",
            "formal_statement": "A bulk Earth composition vector is not the same as the orbit/profile/worldtube-weighted source vector seen by MICROSCOPE; a point-source theorem must either prove universality or keep a finite source vector.",
            "status": "SOURCE_COMPOSITION_PROFILE_OBSTRUCTION_ACTIVE",
            "proof_or_obstruction": "a numeric DD bulk Earth vector exists only as nonclaim context; parent basis and profile weighting are missing",
            "source_anchor": "P8_Y5_R10_1083_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv:DD_EARTH1083_0_bulk_weighted; P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv:SCG1083_0_profile_weighting",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "PSR1900_4_finite_source_multipole",
            "claim_piece": "finite-size/multipole residual",
            "formal_statement": "At MICROSCOPE altitude, finite-source, J2/multipole, orbit-window, mask, and attitude terms belong in K_WEP unless a bounded point-source error theorem is supplied.",
            "status": "FINITE_SOURCE_ERROR_BOUND_MISSING",
            "proof_or_obstruction": "SUEP segment metadata and surrogate design matrices exist, but official orbit/readout arrays and finite-source error bounds are absent",
            "source_anchor": "P8_Y5_R10_1071_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv:SUEP1071_210; P8_Y5_R10_1075_SURROGATE_DESIGN_MATRIX_SEGMENT210.csv:DMROW1075_000",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "PSR1900_5_same_frame_obstruction",
            "claim_piece": "same observed frame/source pullback",
            "formal_statement": "The point-source reduction must use the same observed coframe/time generator for force law, source variation, clocks, orbit, and eta readout.",
            "status": "SAME_FRAME_SOURCE_PULLBACK_NOT_DERIVED",
            "proof_or_obstruction": "same-frame GM gate still has six blocking gates open; a point-source reduction cannot repair a frame/source split",
            "source_anchor": "P8_Y5_R10_683_SAME_FRAME_GM_GATE.csv:SFG683_6_final",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "PSR1900_6_verdict",
            "claim_piece": "promote point-source WEP source leg",
            "formal_statement": "Current MTS parent primitives prove the WEP source worldtube reduces to a calibrated point-source/common-mode leg with all relative residuals bounded or absent.",
            "status": "SOURCE_WORLDTUBE_POINT_SOURCE_REDUCTION_NOT_PARENT_DERIVED",
            "proof_or_obstruction": "common monopole reduction is exact conditionally, but source universality, measured-G guard, source composition/profile weighting, finite-source error bound, same-frame pullback, and official readout arrays are not closed",
            "source_anchor": "PSR1900_0_target through PSR1900_5_same_frame_obstruction",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def point_source_residual_rows() -> list[dict[str, Any]]:
    return [
        {"residual_id": "PSE1900_0_common_monopole", "term": "GM_common_mode", "definition": "universal calibrated monopole source leg", "current_status": "CONDITIONAL_ONLY_NOT_CLAIM", "required_for_claim": "same-frame source charge, universal G_ref, calibrated Hilbert/Hamiltonian source equality", "source_anchor": "P8_Y5_R10_926_SOURCE_WORLDTUBE_EQUALITY_ATTEMPT.csv:SWT926_3_Gauss_readout_after_glue", "units": "m^3 s^-2 or dimensionless after eta normalization", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"residual_id": "PSE1900_1_relative_source_vector", "term": "Delta_w_source_profile", "definition": "source composition/profile/worldtube weighted relative source residual", "current_status": "MISSING_SOURCE_VECTOR", "required_for_claim": "parent theorem of universality or source-backed profile/composition vector in Delta_w basis", "source_anchor": "P8_Y5_R10_1424_SOURCE_VECTOR_CONTRACT.csv:SRCMAP1424_0_R_source", "units": "dimensionless source-response vector", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"residual_id": "PSE1900_2_measured_G_guard", "term": "Delta_GM_absorption_guard", "definition": "equation proving only universal common mode is absorbed into measured GM", "current_status": "GUARD_WRITTEN_NOT_NUMERIC", "required_for_claim": "calibration equation and no relative source-weight hiding proof", "source_anchor": "P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv:SCG1083_3_no_measured_G_absorption", "units": "dimensionless calibration policy", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"residual_id": "PSE1900_3_multipole_error", "term": "epsilon_multipole_altitude", "definition": "finite-source, J2/multipole, altitude/orbit-window residual from extended Earth source", "current_status": "FINITE_SOURCE_ERROR_BOUND_MISSING", "required_for_claim": "source profile or conservative point-source error bound with orbit/readout convention", "source_anchor": "P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv:SWT1068_3_finite_source_correction", "units": "dimensionless envelope", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"residual_id": "PSE1900_4_same_frame", "term": "Delta_frame_source", "definition": "source/readout frame mismatch residual", "current_status": "SAME_FRAME_SOURCE_PULLBACK_NOT_DERIVED", "required_for_claim": "one observed coframe/time generator for force, source, clocks, orbit, and eta", "source_anchor": "P8_Y5_R10_683_SAME_FRAME_GM_GATE.csv:SFG683_6_final", "units": "dimensionless or frame-map units", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"residual_id": "PSE1900_5_kernel_nullspace", "term": "K_WEP_null_or_mask_transfer", "definition": "mask/orbit/attitude/readout nullspace or transfer residual", "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED", "required_for_claim": "official CMSM arrays or validated exact equivalent; surrogate not enough", "source_anchor": "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv:RIG1084_0_CMSM_arrays", "units": "readout kernel units", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"residual_id": "PSE1900_6_verdict", "term": "point_source_residual_pack", "definition": "all residuals required before point-source WEP row can execute", "current_status": "POINT_SOURCE_RESIDUAL_PACK_NOT_EXECUTABLE_NONCLAIM", "required_for_claim": "PSE1900_1 through PSE1900_5 filled or theorem-zero", "source_anchor": "PSE1900_0_common_monopole through PSE1900_5_kernel_nullspace", "units": "mixed", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
    ]


def official_data_target_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for target_id, info in OFFICIAL_TARGETS.items():
        local_path = info["local_path"]
        rows.append(
            {
                "target_id": target_id,
                "target_url": info["url"],
                "local_path": str(local_path),
                "expected_artifact": info["expected_artifact"],
                "exists": local_path.exists(),
                "size_bytes": local_path.stat().st_size if local_path.exists() else 0,
                "file_magic": file_magic(local_path),
                "prefight_status": info["prefight_status"],
                "current_status": "OFFICIAL_DATA_TARGET_NOT_ACQUIRED_NONCLAIM",
                "usable_for_claim": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    rows.extend(
        [
            {"target_id": "local_suep_segments_1071", "target_url": "local", "local_path": str(INPUTS["1071_suep_segments"]), "expected_artifact": "segment/window metadata", "exists": INPUTS["1071_suep_segments"].exists(), "size_bytes": INPUTS["1071_suep_segments"].stat().st_size if INPUTS["1071_suep_segments"].exists() else 0, "file_magic": "csv", "prefight_status": "LOCAL_METADATA_PRESENT", "current_status": "METADATA_ONLY_NOT_OFFICIAL_ARRAYS", "usable_for_claim": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False, "generated_utc": GENERATED_UTC},
            {"target_id": "local_surrogate_design_1075", "target_url": "local", "local_path": str(INPUTS["1075_surrogate_design"]), "expected_artifact": "surrogate design matrix preview", "exists": INPUTS["1075_surrogate_design"].exists(), "size_bytes": INPUTS["1075_surrogate_design"].stat().st_size if INPUTS["1075_surrogate_design"].exists() else 0, "file_magic": "csv", "prefight_status": "LOCAL_SURROGATE_PRESENT", "current_status": "SURROGATE_DESIGN_MATRIX_NOT_OFFICIAL", "usable_for_claim": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False, "generated_utc": GENERATED_UTC},
            {"target_id": "hal_candidates_1899", "target_url": "https://hal.science/hal-03564498/document; https://hal.science/hal-03854332v1/file/DPHY22007.1642068604.pdf", "local_path": str(WEP_SOURCES_1899), "expected_artifact": "data-processing/final-analysis PDFs", "exists": WEP_SOURCES_1899.exists(), "size_bytes": 0, "file_magic": "mixed", "prefight_status": "BOTCHECK_HTML_RECORDED_IN_1899", "current_status": "URL_PROVENANCE_ONLY_NOT_ARRAYS", "usable_for_claim": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False, "generated_utc": GENERATED_UTC},
        ]
    )
    return rows


def data_runner_contract_rows() -> list[dict[str, Any]]:
    return [
        {"contract_id": "ODR1900_0_target_files", "runner_piece": "official readout acquisition", "required_artifact": "P_WEP_K_CMSM_readout.csv; P_WEP_R_source_Earth_worldtube.csv; P_WEP_eta_product_convention.csv", "accepted_form": "files exist, parse, contain no MISSING/PENDING markers, and cite source URL/path/DOI", "current_status": "TARGET_FILES_NOT_ACQUIRED", "source_anchor": "P8_Y5_R10_1456_SOURCE_WORLDTUBE_FILE_LEDGER_NONCLAIM.csv:SFI1456_0_source_worldtube_file;SFI1456_1_official_readout_file", "blocks_claim": True, "score_ready": False, "valid_for_claim": False},
        {"contract_id": "ODR1900_1_schema", "runner_piece": "official readout schema", "required_artifact": "time_s;session_id;orbit_id;axis;gx_m_s2;gz_m_s2;Sxx;Sxz;mask_flag;calibration_flag;attitude_quaternion_or_axis;source_url_or_path", "accepted_form": "strict CSV schema with numeric units and branch lock", "current_status": "SCHEMA_DECLARED_NONCLAIM", "source_anchor": "P8_Y5_R10_1456_SOURCE_WORLDTUBE_FILE_LEDGER_NONCLAIM.csv:SFI1456_1_official_readout_file", "blocks_claim": True, "score_ready": False, "valid_for_claim": False},
        {"contract_id": "ODR1900_2_cache_validation", "runner_piece": "cache validation", "required_artifact": "downloaded resources must have expected file magic, nonzero size, and parseable contents", "accepted_form": "valid PDF/CSV/TXT markers; bot-check HTML rejected", "current_status": "CACHE_VALIDATION_RULE_WRITTEN_NONCLAIM", "source_anchor": "P8_Y5_PARENT_QLOC_1899_WEB_SOURCE_CACHE_LEDGER.csv", "blocks_claim": True, "score_ready": False, "valid_for_claim": False},
        {"contract_id": "ODR1900_3_surrogate_guard", "runner_piece": "surrogate handling", "required_artifact": "1075 surrogate design matrix may test code paths only", "accepted_form": "never promoted to official readout without validation theorem", "current_status": "SURROGATE_GUARD_ENFORCED_NONCLAIM", "source_anchor": "P8_Y5_R10_1075_SURROGATE_DESIGN_MATRIX_SEGMENT210.csv:DMROW1075_000", "blocks_claim": True, "score_ready": False, "valid_for_claim": False},
        {"contract_id": "ODR1900_4_no_unity_tau", "runner_piece": "tau/product normalization", "required_artifact": "tau_WEP derived or sourced from official source/readout/material/product rows", "accepted_form": "numeric source-backed value, theorem-zero, or retained nuisance with prior; tau_WEP=1 forbidden", "current_status": "TAU_WEP_NOT_DERIVED", "source_anchor": "P8_Y5_R10_1455_SOURCE_WORLDTUBE_ACQUISITION_LEDGER_NONCLAIM.csv:SW1455_6_no_unity_shortcut", "blocks_claim": True, "score_ready": False, "valid_for_claim": False},
        {"contract_id": "ODR1900_5_verdict", "runner_piece": "official data runner", "required_artifact": "all source/readout/material/product files filled or theorem-reduced", "accepted_form": "runner can create nonclaim previews but cannot score until all gates pass", "current_status": "OFFICIAL_READOUT_DATA_RUNNER_NOT_EXECUTABLE_NONCLAIM", "source_anchor": "ODR1900_0_target_files through ODR1900_4_no_unity_tau", "blocks_claim": True, "score_ready": False, "valid_for_claim": False},
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {"case_id": "DRY1900_0_no_reduction", "point_source_parent_signed": False, "hides_relative_in_gm": False, "source_vector_present": False, "official_readout_present": False, "uses_surrogate_as_official": False, "tau_wep_is_unity": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_POINT_SOURCE_REDUCTION_NOT_DERIVED", "valid_for_claim": False},
        {"case_id": "DRY1900_1_gm_hiding", "point_source_parent_signed": True, "hides_relative_in_gm": True, "source_vector_present": False, "official_readout_present": False, "uses_surrogate_as_official": False, "tau_wep_is_unity": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_MEASURED_GM_RELATIVE_WEIGHT_HIDING", "valid_for_claim": False},
        {"case_id": "DRY1900_2_source_vector", "point_source_parent_signed": True, "hides_relative_in_gm": False, "source_vector_present": False, "official_readout_present": False, "uses_surrogate_as_official": False, "tau_wep_is_unity": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_SOURCE_VECTOR_MISSING", "valid_for_claim": False},
        {"case_id": "DRY1900_3_official_readout", "point_source_parent_signed": True, "hides_relative_in_gm": False, "source_vector_present": True, "official_readout_present": False, "uses_surrogate_as_official": False, "tau_wep_is_unity": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_OFFICIAL_READOUT_MISSING", "valid_for_claim": False},
        {"case_id": "DRY1900_4_surrogate", "point_source_parent_signed": True, "hides_relative_in_gm": False, "source_vector_present": True, "official_readout_present": False, "uses_surrogate_as_official": True, "tau_wep_is_unity": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_SURROGATE_AS_OFFICIAL", "valid_for_claim": False},
        {"case_id": "DRY1900_5_tau_unity", "point_source_parent_signed": True, "hides_relative_in_gm": False, "source_vector_present": True, "official_readout_present": True, "uses_surrogate_as_official": False, "tau_wep_is_unity": True, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_TAU_WEP_UNITY_SHORTCUT", "valid_for_claim": False},
        {"case_id": "DRY1900_6_bound_anchor", "point_source_parent_signed": True, "hides_relative_in_gm": False, "source_vector_present": True, "official_readout_present": True, "uses_surrogate_as_official": False, "tau_wep_is_unity": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_BOUND_ANCHOR_ONLY", "valid_for_claim": False},
        {"case_id": "DRY1900_7_cancellation", "point_source_parent_signed": True, "hides_relative_in_gm": False, "source_vector_present": True, "official_readout_present": True, "uses_surrogate_as_official": False, "tau_wep_is_unity": False, "bound_anchor_only": False, "uses_cancellation": True, "expected_status": "REFUSED_CANCELLATION_ONLY", "valid_for_claim": False},
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    point_source_parent_signed = bool_string(row["point_source_parent_signed"]) == "true"
    hides_relative_in_gm = bool_string(row["hides_relative_in_gm"]) == "true"
    source_vector_present = bool_string(row["source_vector_present"]) == "true"
    official_readout_present = bool_string(row["official_readout_present"]) == "true"
    uses_surrogate_as_official = bool_string(row["uses_surrogate_as_official"]) == "true"
    tau_wep_is_unity = bool_string(row["tau_wep_is_unity"]) == "true"
    bound_anchor_only = bool_string(row["bound_anchor_only"]) == "true"
    uses_cancellation = bool_string(row["uses_cancellation"]) == "true"

    if not point_source_parent_signed:
        status = "REFUSED_POINT_SOURCE_REDUCTION_NOT_DERIVED"
    elif hides_relative_in_gm:
        status = "REFUSED_MEASURED_GM_RELATIVE_WEIGHT_HIDING"
    elif not source_vector_present:
        status = "REFUSED_SOURCE_VECTOR_MISSING"
    elif uses_surrogate_as_official:
        status = "REFUSED_SURROGATE_AS_OFFICIAL"
    elif not official_readout_present:
        status = "REFUSED_OFFICIAL_READOUT_MISSING"
    elif tau_wep_is_unity:
        status = "REFUSED_TAU_WEP_UNITY_SHORTCUT"
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
        {"gate_id": "CG1900_0_point_source", "condition": "source-worldtube point-source/common-mode reduction is parent-signed", "current_status": "FAIL_SOURCE_WORLDTUBE_POINT_SOURCE_REDUCTION_NOT_PARENT_DERIVED", "source_anchor": "P8_Y5_PARENT_QLOC_1900_WEP_SOURCE_WORLDTUBE_POINT_SOURCE_REDUCTION_ATTEMPT.csv:PSR1900_6_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1900_1_residual_pack", "condition": "relative source vector, measured-G guard, finite-source error, same-frame, and kernel residuals are filled or zero", "current_status": "FAIL_POINT_SOURCE_RESIDUAL_PACK_NOT_EXECUTABLE_NONCLAIM", "source_anchor": "P8_Y5_PARENT_QLOC_1900_WEP_POINT_SOURCE_RESIDUAL_LEDGER_NONCLAIM.csv:PSE1900_6_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1900_2_official_data", "condition": "official readout data targets are acquired and cache-validated", "current_status": "FAIL_OFFICIAL_DATA_TARGET_NOT_ACQUIRED_NONCLAIM", "source_anchor": "P8_Y5_PARENT_QLOC_1900_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv:cmsm_ds_onera_root", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1900_3_no_shortcuts", "condition": "no measured-G hiding, no tau=1, no surrogate-as-official, no bound-only pass", "current_status": "PASS_GUARDS_ENFORCED_BUT_NONCLAIM", "source_anchor": "P8_Y5_PARENT_QLOC_1900_POINT_SOURCE_DATA_DRYRUN_RESULTS.csv", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1900_4_verdict", "condition": "WEP source-worldtube/readout branch can support local-GR/WEP claim", "current_status": "CLAIM_BLOCKED", "source_anchor": "CG1900_0_point_source through CG1900_3_no_shortcuts", "gate_pass": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC1900_0_point_source", "decision": "do not promote point-source source-worldtube reduction", "reason": "common-mode monopole theorem is exact conditionally, but relative source weights, measured-G guard, finite-source error, same-frame pullback, and official kernel are unsigned", "status": "POINT_SOURCE_ROUTE_SHARP_BUT_UNSIGNED", "next_dependency": "derive measured-G/common-mode guard or fill source vector", "valid_for_claim": False},
        {"decision_id": "DEC1900_1_data_runner", "decision": "stage official readout/data runner targets nonclaim", "reason": "public portal target exists as URL, but local preflight cannot connect; local SUEP/surrogate rows are useful only for metadata/code-path checks", "status": "OFFICIAL_DATA_RUNNER_STAGED_NONCLAIM", "next_dependency": "manual/working official data access or validated source-backed export", "valid_for_claim": False},
        {"decision_id": "DEC1900_2_next", "decision": "attack measured-G common-mode guard next", "reason": "it is more derivable than the unavailable official arrays and directly controls whether source weights are being hidden", "status": "NEXT_TARGET_SELECTED", "next_dependency": "1901 measured-G common-mode guard or source-vector fill", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1900_0_primary",
            "selection_status": "selected",
            "target_doc": "1901-Y5-R2FR-measured-G-common-mode-guard-or-source-vector-fill.md",
            "target_script": "scripts/Y5_R2FR_measured_G_common_mode_guard_or_source_vector_fill_1901.py",
            "objective": "try to prove measured GM absorbs only universal common-mode source normalization and cannot hide relative source weights; if it fails, fill source-vector acquisition rows as nonclaim",
            "success_condition": "parent-signed measured-G common-mode guard, or source-vector input rows with explicit composition/profile/worldtube and no claim promotion",
            "do_not": "do not use measured GM to erase relative Delta_w_source, do not transfer bulk Earth DD vector as profile-weighted source without a map, and do not score WEP from surrogate arrays",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {"status_id": "STAT1900_0_theory", "area": "Newton/GR source reduction", "summary": "common exterior monopole reduction is exact conditionally, but it does not prove relative source-weight silence", "risk_level": "COMMON_MODE_GOOD_RELATIVE_SOURCE_OPEN", "project_meaning": "we are using the GR-to-Newton logic carefully: point mass is allowed for universal source, not for hiding WEP-active residuals", "next_action": "derive measured-G common-mode guard", "valid_for_claim": False},
        {"status_id": "STAT1900_1_data", "area": "MICROSCOPE data branch", "summary": "official portal targets are recorded, but local preflight failed and only metadata/surrogate rows are available", "risk_level": "DATA_ACCESS_BLOCKED_BUT_NOT_THEORY_BLOCKED", "project_meaning": "testing remains possible once data access works, while derivation can continue privately", "next_action": "manual official export or source-vector/GM guard derivation", "valid_for_claim": False},
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    cases = dryrun_case_rows()
    return {
        "source_register": source_register_rows(),
        "point_source_attempt": point_source_attempt_rows(),
        "point_source_residuals": point_source_residual_rows(),
        "official_data_targets": official_data_target_rows(),
        "data_runner_contract": data_runner_contract_rows(),
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
    fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass", "parent_signed", "usable_for_claim"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            for field in fields.intersection(row.keys()):
                if bool_string(row[field]) == "true":
                    bad.append(f"{path.name}:{index}:{field}=true")
    return not bad, "; ".join(bad) if bad else "all generated claim/scoring/signature flags remain false"


def blocked_rows_not_ready(paths: list[Path]) -> tuple[bool, str]:
    markers = ["MISSING", "UNSIGNED", "NOT_DERIVED", "NOT_PARENT", "BLOCKED", "FAIL", "COUNTER", "SURROGATE", "NONCLAIM", "CLAIM_BLOCKED", "NOT_EXECUTABLE", "NOT_ACQUIRED"]
    fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass", "parent_signed", "usable_for_claim"}
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
    checks.append({"validation_id": "VAL1900_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL", "detail": "all local source paths exist and needles found", "valid_for_claim": False})
    point_rows = csv_rows(OUTPUTS["point_source_attempt"])
    checks.append({"validation_id": "VAL1900_01_point_source_verdict", "status": "PASS" if any(row["attempt_id"] == "PSR1900_6_verdict" and row["status"] == "SOURCE_WORLDTUBE_POINT_SOURCE_REDUCTION_NOT_PARENT_DERIVED" for row in point_rows) else "FAIL", "detail": "point-source reduction remains unsigned", "valid_for_claim": False})
    residual_rows = csv_rows(OUTPUTS["point_source_residuals"])
    checks.append({"validation_id": "VAL1900_02_residual_pack", "status": "PASS" if len(residual_rows) >= 7 and all(row["score_ready"] == "False" and row["valid_prediction_row"] == "False" for row in residual_rows) else "FAIL", "detail": "point-source residual pack is nonclaim/not score-ready", "valid_for_claim": False})
    target_rows = csv_rows(OUTPUTS["official_data_targets"])
    checks.append({"validation_id": "VAL1900_03_official_targets", "status": "PASS" if all(row["usable_for_claim"] == "False" and row["valid_prediction_row"] == "False" for row in target_rows) else "FAIL", "detail": "official data targets remain nonclaim/not acquired; surrogate rows not promoted", "valid_for_claim": False})
    contract_rows = csv_rows(OUTPUTS["data_runner_contract"])
    checks.append({"validation_id": "VAL1900_04_runner_contract", "status": "PASS" if all(row["blocks_claim"] == "True" and row["score_ready"] == "False" for row in contract_rows) else "FAIL", "detail": "runner contract blocks claim until official files and tau/product convention exist", "valid_for_claim": False})
    dry_rows = csv_rows(OUTPUTS["dryrun_results"])
    checks.append({"validation_id": "VAL1900_05_dryrun", "status": "PASS" if all(row["status_match"] == "True" and row["claim_allowed"] == "False" for row in dry_rows) else "FAIL", "detail": "dry-run refuses point-source overpromotion, GM hiding, missing source/readout, surrogate, tau=1, bound-only, and cancellation", "valid_for_claim": False})
    gate_rows = csv_rows(OUTPUTS["claim_gate"])
    checks.append({"validation_id": "VAL1900_06_claim_gate", "status": "PASS" if any(row["gate_id"] == "CG1900_4_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in gate_rows) else "FAIL", "detail": "claim remains blocked", "valid_for_claim": False})
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append({"validation_id": "VAL1900_07_next_target", "status": "PASS" if any(row["route_id"] == "NEXT1900_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL", "detail": "1901 target selected", "valid_for_claim": False})
    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append({"validation_id": "VAL1900_08_claim_flags_false", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})
    blocked_ok, blocked_detail = blocked_rows_not_ready(generated_without_validation)
    checks.append({"validation_id": "VAL1900_09_blocked_markers_not_ready", "status": "PASS" if blocked_ok else "FAIL", "detail": blocked_detail, "valid_for_claim": False})
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1900_10_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})
    checks.append({"validation_id": "VAL1900_11_branch_copies", "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL", "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()), "valid_for_claim": False})
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1900_12_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})
    formalization_hits = list(FORMALIZATION.rglob("*1900*")) if FORMALIZATION.exists() else []
    checks.append({"validation_id": "VAL1900_13_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1900_count={len(formalization_hits)}", "valid_for_claim": False})
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1900_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1900 WEP source-worldtube point-source reduction or official readout data runner", "valid_for_claim": False})
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1900 - WEP Source-Worldtube Point-Source Reduction Or Official Readout Data Runner

## Purpose

This checkpoint tries to prove a GR/Newton-style source reduction for the WEP branch: the extended Earth source worldtube may reduce to a calibrated point-source/common-mode monopole only if relative source weights are not hidden in measured `GM`.

If that derivation does not close, it stages official MICROSCOPE readout/data targets and a nonclaim runner contract.

## Result

- The common exterior monopole lemma is exact conditionally.
- It does not prove relative source-weight silence.
- Measured `GM` is guarded: universal common mode may be calibrated, but relative source residuals must remain explicit.
- Official CMSM/readout data targets are recorded, but local preflight could not connect to the candidate portal.
- SUEP metadata and surrogate design matrices remain useful for plumbing only, not claims.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Source-Worldtube Point-Source Attempt

{markdown_table(rows_by_name["point_source_attempt"])}

## Point-Source Residual Ledger

{markdown_table(rows_by_name["point_source_residuals"])}

## Official Readout Data Targets

{markdown_table(rows_by_name["official_data_targets"])}

## Official Data Runner Contract

{markdown_table(rows_by_name["data_runner_contract"])}

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
