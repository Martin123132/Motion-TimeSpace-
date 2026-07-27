from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_INTAKE = ROOT / "source-intake"
MICROSCOPE = SOURCE_INTAKE / "microscope"
EOTWASH = SOURCE_INTAKE / "eotwash"
R10 = SOURCE_INTAKE / "r10"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1492-Y5-R10-RAB-delta-w-source-acquisition-ledger-EotWash-R10-MICROSCOPE.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1491_next": OUT / "P8_Y5_R10_1491_NEXT_TARGET.csv",
    "1491_validation": OUT / "P8_Y5_BRR545_1491_VALIDATION.csv",
    "1491_bound_anchors": OUT / "P8_Y5_R10_1491_DELTA_W_BOUND_ANCHORS.csv",
    "1491_input_pack": OUT / "P8_Y5_R10_1491_REAL_DELTA_W_INPUT_PACK_NONCLAIM.csv",
    "1491_projection_requirements": OUT / "P8_Y5_R10_1491_ARENA_PROJECTION_REQUIREMENTS.csv",
    "1491_readiness": OUT / "P8_Y5_R10_1491_DELTA_W_READINESS_MATRIX.csv",
    "1491_rejections": OUT / "P8_Y5_R10_1491_REJECTION_LEDGER.csv",
    "1438_microscope_manifest": OUT / "P8_Y5_R10_1438_OFFICIAL_MICROSCOPE_SOURCE_PACK_MANIFEST.csv",
    "1482_microscope_dir_status": OUT / "P8_Y5_R10_1482_MICROSCOPE_INTAKE_DIRECTORY_STATUS.csv",
    "1070_microscope_external": OUT / "P8_Y5_R10_1070_EXTERNAL_MICROSCOPE_READOUT_SOURCE_LEDGER.csv",
    "1084_microscope_gate": OUT / "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
    "local_bounds": SOURCE_INTAKE / "local_bounds" / "local_bound_claims.csv",
}

C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1492_SOURCE_REGISTER.csv"
EXTERNAL_LEDGER = OUT / "P8_Y5_R10_1492_EXTERNAL_SOURCE_LEDGER.csv"
TARGET_MANIFEST = OUT / "P8_Y5_R10_1492_LOCAL_TARGET_FILE_MANIFEST.csv"
ACQUISITION_STATUS = OUT / "P8_Y5_R10_1492_ACQUISITION_STATUS.csv"
EXTRACTION_REQUIREMENTS = OUT / "P8_Y5_R10_1492_EXTRACTION_REQUIREMENTS.csv"
DELTA_W_BLOCKERS = OUT / "P8_Y5_R10_1492_DELTA_W_SCORING_BLOCKERS.csv"
C_PARENT_REFUSAL = OUT / "P8_Y5_R10_1492_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1492_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1492_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1492_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1492_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1492_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1492"
QUAR_EXTERNAL = QUARANTINE / "EXTERNAL_SOURCE_LEDGER_NONCLAIM.csv"
QUAR_TARGETS = QUARANTINE / "LOCAL_TARGET_FILE_MANIFEST_NONCLAIM.csv"
QUAR_STATUS = QUARANTINE / "ACQUISITION_STATUS_NONCLAIM.csv"
BRANCH_EXTERNAL = BRANCH_RESIDUALS / "external_source_ledger_nonclaim_1492.csv"
BRANCH_TARGETS = BRANCH_RESIDUALS / "local_target_file_manifest_nonclaim_1492.csv"
BRANCH_STATUS = BRANCH_RESIDUALS / "acquisition_status_nonclaim_1492.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def flags() -> dict[str, bool]:
    return {
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def source_rows() -> list[dict[str, Any]]:
    usage = {
        "1491_next": "authoritative 1492 handoff",
        "1491_validation": "previous validation state",
        "1491_bound_anchors": "delta_w bound anchor status",
        "1491_input_pack": "delta_w input pack status",
        "1491_projection_requirements": "projection requirement source",
        "1491_readiness": "arena readiness source",
        "1491_rejections": "previous rejection ledger",
        "1438_microscope_manifest": "MICROSCOPE target file manifest",
        "1482_microscope_dir_status": "MICROSCOPE directory readiness",
        "1070_microscope_external": "MICROSCOPE external source rows",
        "1084_microscope_gate": "MICROSCOPE official readout gate",
        "local_bounds": "local empirical bound table",
    }
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": f"SRC1492_{index}_{key}",
            "path_or_url": rel(path),
            "source_kind": "local_file",
            "exists_or_resolved": path.exists(),
            "usage": usage[key],
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def ensure_target_dirs() -> None:
    for directory in [
        EOTWASH / "raw",
        EOTWASH / "docs",
        EOTWASH / "derived",
        EOTWASH / "metadata",
        R10 / "raw",
        R10 / "docs",
        R10 / "derived",
        R10 / "metadata",
        MICROSCOPE / "raw",
        MICROSCOPE / "docs",
        MICROSCOPE / "official_readout",
        MICROSCOPE / "source_worldtube",
        MICROSCOPE / "product_convention",
        MICROSCOPE / "derived",
    ]:
        directory.mkdir(parents=True, exist_ok=True)


def external_source_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "EXT1492_0_EOTWASH_PRL_2008",
            "WEP_EotWash_material_pairs",
            "Test of the Equivalence Principle Using a Rotating Torsion Balance",
            "https://arxiv.org/abs/0712.0607",
            "https://doi.org/10.1103/PhysRevLett.100.041101",
            "2008",
            "EotWash Be/Ti rotating torsion-balance WEP result; source for material-pair eta anchor and extraction target",
            rel(EOTWASH / "raw" / "Schlamminger_2008_PRL_0712.0607.pdf"),
            "PDF table/text extraction",
            "source resolved by web; local PDF/table not acquired in this pass",
        ),
        (
            "EXT1492_1_EOTWASH_CQG_2012",
            "WEP_EotWash_material_pairs",
            "Torsion-balance tests of the weak equivalence principle",
            "https://arxiv.org/abs/1207.2442",
            "https://doi.org/10.1088/0264-9381/29/18/184002",
            "2012",
            "EotWash WEP review; source for Be-Al/Be-Ti context and material-pair table hunting",
            rel(EOTWASH / "docs" / "Wagner_2012_CQG_1207.2442.pdf"),
            "PDF review/table extraction",
            "source resolved by web; local PDF/table not acquired in this pass",
        ),
        (
            "EXT1492_2_R10_ARXIV_2020",
            "R10_short_range_inverse_square",
            "New Test of the Gravitational 1/r^2 Law at Separations down to 52 um",
            "https://arxiv.org/abs/2002.11761",
            "https://doi.org/10.1103/PhysRevLett.124.101101",
            "2020",
            "EotWash short-range inverse-square source; source for alpha(lambda) curve digitization",
            rel(R10 / "raw" / "Lee_2020_PRL_2002.11761.pdf"),
            "PDF figure digitization or machine-table acquisition",
            "source resolved by web; curve not digitized/promoted in this pass",
        ),
        (
            "EXT1492_3_R10_PUBMED_2020",
            "R10_short_range_inverse_square",
            "PubMed record for PRL 124 101101",
            "https://pubmed.ncbi.nlm.nih.gov/32216404/",
            "https://doi.org/10.1103/PhysRevLett.124.101101",
            "2020",
            "bibliographic cross-check for R10 source",
            rel(R10 / "docs" / "Lee_2020_PRL_pubmed_record.txt"),
            "metadata cross-check",
            "search result resolved; page itself may require browser challenge",
        ),
        (
            "EXT1492_4_MICROSCOPE_CMSM_PORTAL",
            "WEP_MICROSCOPE_TiPt",
            "MICROSCOPE science data portal",
            "https://cmsm-ds.onera.fr/user/microscope",
            "not_applicable_data_portal",
            "2022",
            "official data portal route for MICROSCOPE arrays/readout files",
            rel(MICROSCOPE / "raw" / "CMSM_portal_download_package"),
            "portal/manual or scripted authenticated download",
            "source resolved by web/search; no data package downloaded in this pass",
        ),
        (
            "EXT1492_5_MICROSCOPE_PRL_FINAL",
            "WEP_MICROSCOPE_TiPt",
            "MICROSCOPE Mission: Final Results of the Test of the Equivalence Principle",
            "https://arxiv.org/abs/2209.15487",
            "https://doi.org/10.1103/PhysRevLett.129.121102",
            "2022",
            "final Ti/Pt eta bound source",
            rel(MICROSCOPE / "docs" / "Touboul_2022_PRL_final_results.pdf"),
            "PDF text/table extraction",
            "bound already present locally as anchor; official source file not downloaded in this pass",
        ),
        (
            "EXT1492_6_MICROSCOPE_CQG_READOUT",
            "WEP_MICROSCOPE_TiPt",
            "Result of the MICROSCOPE Weak Equivalence Principle test",
            "https://arxiv.org/abs/2209.15488",
            "https://doi.org/10.1088/1361-6382/ac84be",
            "2022",
            "readout convention, eta formula, orbit/segment metadata, CMSM portal pointer",
            rel(MICROSCOPE / "docs" / "Touboul_2022_CQG_readout.pdf"),
            "PDF text/table extraction plus data portal follow-up",
            "source already referenced locally; official arrays still missing",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "external_id": external_id,
            "arena": arena,
            "title": title,
            "url": url,
            "doi_or_data_id": doi,
            "paper_year": paper_year,
            "source_role": source_role,
            "local_target_path": local_target_path,
            "extraction_method": extraction_method,
            "current_status": current_status,
            "resolved_by_browse": True,
            "file_acquired_now": False,
            "score_ready": False,
            **flags(),
        }
        for external_id, arena, title, url, doi, paper_year, source_role, local_target_path, extraction_method, current_status in rows
    ]


def target_manifest_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "TGT1492_0_EotWash_bound",
            "WEP_EotWash_material_pairs",
            EOTWASH / "derived" / "P_WEP_EotWash_material_pair_bounds.csv",
            "test_body_A;test_body_B;source_attractor;eta;eta_sigma;confidence;units;range_or_source_direction;source_url_or_path;valid_for_claim",
            "published eta/material-pair bound row with source path and uncertainty",
        ),
        (
            "TGT1492_1_EotWash_vectors",
            "WEP_EotWash_material_pairs",
            EOTWASH / "derived" / "P_WEP_EotWash_material_response_vectors.csv",
            "material_id;component_id;response_value;units;basis;composition_source;double_count_rule;source_url_or_path;valid_for_claim",
            "material/source response vectors in same delta_w component basis",
        ),
        (
            "TGT1492_2_R10_curve",
            "R10_short_range_inverse_square",
            R10 / "derived" / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "lambda_value;lambda_units;alpha_bound;confidence;curve_source;digitization_method;valid_for_claim",
            "promoted alpha(lambda) curve or source-backed machine-readable table",
        ),
        (
            "TGT1492_3_R10_kernel",
            "R10_short_range_inverse_square",
            R10 / "derived" / "R10_delta_w_kernel_lambda.csv",
            "lambda_value;lambda_units;kernel_value;source_response_basis;test_response_basis;units;source_url_or_path;valid_for_claim",
            "maps delta_w component vector to alpha(lambda) prediction",
        ),
        (
            "TGT1492_4_MICROSCOPE_readout",
            "WEP_MICROSCOPE_TiPt",
            MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv",
            "time_s;session_id;orbit_id;axis;gx_m_s2;gz_m_s2;Sxx;Sxz;mask_flag;calibration_flag;attitude_quaternion_or_axis;source_url_or_path",
            "official or reproducible CMSM readout/design matrix",
        ),
        (
            "TGT1492_5_MICROSCOPE_source",
            "WEP_MICROSCOPE_TiPt",
            MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv",
            "time_s_or_orbit_phase;radius_m;density_kg_m3;source_component;kernel_weight;model_or_dataset;source_url_or_path",
            "Earth/source worldtube profile in the same projection convention",
        ),
        (
            "TGT1492_6_MICROSCOPE_product",
            "WEP_MICROSCOPE_TiPt",
            MICROSCOPE / "product_convention" / "P_WEP_eta_product_convention.csv",
            "eta_formula;sign_convention;tau_eff_definition;readout_kernel_units;source_kernel_units;orbit_average_rule;branch_lock",
            "same-branch eta/sign/product convention",
        ),
        (
            "TGT1492_7_MICROSCOPE_tensor",
            "WEP_MICROSCOPE_TiPt",
            MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv",
            "material_id;channel_id;response_value;units;basis;double_count_rule;source_url_or_path;valid_for_claim",
            "source-backed full material tensor for Ti/Pt/PtRh10/TA6V convention",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "target_id": target_id,
            "arena": arena,
            "target_path": rel(target_path),
            "target_parent_exists": target_path.parent.exists(),
            "target_exists": target_path.exists(),
            "required_columns_or_fields": required_columns,
            "acceptance_rule": acceptance_rule,
            "current_status": "TARGET_FILE_MISSING_OR_UNPROMOTED" if not target_path.exists() else "TARGET_EXISTS_REQUIRES_CONTENT_VALIDATION",
            "score_ready": False,
            **flags(),
        }
        for target_id, arena, target_path, required_columns, acceptance_rule in rows
    ]


def acquisition_status_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ACQ1492_0_EotWash",
            "WEP_EotWash_material_pairs",
            "SOURCE_URLS_IDENTIFIED_LOCAL_TABLE_MISSING",
            "arXiv 0712.0607 and 1207.2442 identified; local material-pair CSV not acquired",
            "extract eta bounds and material pairs into EotWash target files",
        ),
        (
            "ACQ1492_1_R10",
            "R10_short_range_inverse_square",
            "SOURCE_URLS_IDENTIFIED_CURVE_MISSING",
            "arXiv 2002.11761 / PRL 124.101101 identified; alpha(lambda) curve not digitized/promoted",
            "digitize or locate machine-readable alpha(lambda) curve and build delta_w kernel",
        ),
        (
            "ACQ1492_2_MICROSCOPE",
            "WEP_MICROSCOPE_TiPt",
            "PORTAL_AND_PAPER_SOURCES_IDENTIFIED_OFFICIAL_FILES_MISSING",
            "CMSM portal and final/readout papers identified; local official arrays/source/product files missing",
            "download/parse CMSM files or create reproducible official-kernel extraction",
        ),
        (
            "ACQ1492_3_delta_w",
            "all_delta_w_arenas",
            "SCORING_BLOCKED",
            "source acquisition has not produced claim-valid inputs in any arena",
            "do not run scoring until all required target files are filled and validated",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "arena": arena,
            "current_status": current_status,
            "detail": detail,
            "next_action": next_action,
            "score_ready": False,
            **flags(),
        }
        for status_id, arena, current_status, detail, next_action in rows
    ]


def extraction_requirement_rows() -> list[dict[str, Any]]:
    rows = [
        ("EXTREQ1492_0_EotWash_bound", "WEP_EotWash_material_pairs", "eta bound plus uncertainty/confidence", "PDF table/text extraction", "must preserve test-body pair, source direction/range, units, DOI/arXiv URL"),
        ("EXTREQ1492_1_EotWash_material", "WEP_EotWash_material_pairs", "material response vectors", "composition/model extraction", "must declare basis and double-counting rule"),
        ("EXTREQ1492_2_R10_curve", "R10_short_range_inverse_square", "alpha(lambda) bound curve", "figure digitization or machine table", "anchor-only threshold cannot be valid_for_claim=true"),
        ("EXTREQ1492_3_R10_kernel", "R10_short_range_inverse_square", "delta_w-to-alpha kernel", "theory/projection construction", "must declare source/test response basis and lambda convention"),
        ("EXTREQ1492_4_MICROSCOPE_arrays", "WEP_MICROSCOPE_TiPt", "official readout arrays/design matrix", "CMSM portal extraction", "must include masks/calibration flags/orbit/session/axis"),
        ("EXTREQ1492_5_MICROSCOPE_source", "WEP_MICROSCOPE_TiPt", "Earth/source worldtube profile", "dataset/model plus orbit projection", "must share units and branch convention with readout kernel"),
        ("EXTREQ1492_6_MICROSCOPE_product", "WEP_MICROSCOPE_TiPt", "eta product convention", "schema fill from official readout convention", "must define tau_eff and sign convention before scoring"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": requirement_id,
            "arena": arena,
            "required_object": required_object,
            "extraction_method": extraction_method,
            "acceptance_rule": acceptance_rule,
            "current_status": "REQUIRED_NOT_FILLED",
            **flags(),
        }
        for requirement_id, arena, required_object, extraction_method, acceptance_rule in rows
    ]


def delta_w_blocker_rows() -> list[dict[str, Any]]:
    rows = [
        ("BLK1492_0_EotWash", "EOTWASH_TABLE_MISSING", "local material-pair eta/source-vector rows absent"),
        ("BLK1492_1_R10", "R10_CURVE_MISSING", "alpha(lambda) bound curve and delta_w kernel absent"),
        ("BLK1492_2_MICROSCOPE", "MICROSCOPE_OFFICIAL_FILES_MISSING", "official arrays/source/product/material tensor absent"),
        ("BLK1492_3_same_branch", "SAME_BRANCH_LOCK_MISSING", "input factors do not yet share one units/sign/basis convention"),
        ("BLK1492_4_projection", "PROJECTION_KERNELS_MISSING", "tau_WEP/tau_R10/tau_clock/orbital projection maps missing"),
        ("BLK1492_5_no_claim", "CLAIM_PROMOTION_FORBIDDEN", "source acquisition ledger is not a score or a local-GR proof"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "blocking_marker": marker,
            "reason": reason,
            "score_ready": False,
            **flags(),
        }
        for blocker_id, marker, reason in rows
    ]


def c_parent_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "refusal_id": "CPR1492_0_live_import",
            "forbidden_object": rel(C_PARENT_IMPORT),
            "exists": C_PARENT_IMPORT.exists(),
            "current_status": "ABSENT_OK" if not C_PARENT_IMPORT.exists() else "ERROR_LIVE_IMPORT_PRESENT",
            "reason": "1492 is source acquisition only; no theorem-zero coupling or C_parent import is allowed",
            "action_taken": "no C_parent import written",
            "parent_signed": False,
            **flags(),
        }
    ]


def local_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("LRS1492_0_sources", "delta_w source acquisition", "source URLs/targets ledgered", "LEDGER_BUILT_INPUTS_NOT_ACQUIRED", "target data files still missing/unpromoted", "empirical branch not score-ready"),
        ("LRS1492_1_WEP", "WEP/MICROSCOPE/EotWash", "MICROSCOPE anchor and EotWash source leads identified", "SOURCE_ACQUISITION_OPEN", "official files/material/source vectors missing", "WEP claim blocked"),
        ("LRS1492_2_R10", "R10 short-range", "2020 source identified", "CURVE_DIGITIZATION_OPEN", "full alpha(lambda) curve and delta_w kernel missing", "R10 claim blocked"),
        ("LRS1492_3_local_GR", "local GR/Newton", "delta_w remains finite residual branch", "NOT_CLOSED", "universal coupling not derived and empirical branch not scored", "no local-GR/Newton claim"),
        ("LRS1492_4_verdict", "overall", "source acquisition ledger complete for current pass", "NEXT_TARGET_EXTRACTION_OR_DOWNLOAD", "need actual files/extractions", "no WEP/R10/local claim from 1492"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "target": target,
            "evidence_status": evidence_status,
            "current_status": current_status,
            "missing_for_claim": missing_for_claim,
            "claim_effect": claim_effect,
            "parent_signed": False,
            **flags(),
        }
        for status_id, target, evidence_status, current_status, missing_for_claim, claim_effect in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1492_0_downloads", "SOURCE_FILES_NOT_DOWNLOADED_OR_PARSED", "external sources identified but target data files are not populated"),
        ("REJ1492_1_EotWash", "EOTWASH_MATERIAL_PAIR_ROWS_MISSING", "EotWash tables/vectors must be extracted before scoring"),
        ("REJ1492_2_R10", "R10_ALPHA_LAMBDA_CURVE_MISSING", "R10 remains symbolic until curve/kernel exists"),
        ("REJ1492_3_MICROSCOPE", "MICROSCOPE_OFFICIAL_ARRAYS_MISSING", "CMSM/readout/source/product files missing"),
        ("REJ1492_4_projection", "DELTA_W_PROJECTION_KERNELS_MISSING", "source-backed bounds do not become predictions without kernels"),
        ("REJ1492_5_Cparent", "C_PARENT_IMPORT_FORBIDDEN", "source acquisition does not prove coupling"),
        ("REJ1492_6_claim", "CLAIM_PROMOTION_FORBIDDEN", "no WEP/R10/local-GR/Newton claim allowed"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "blocking_marker": marker,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rejection_id, marker, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC1492_0_ledger_not_claim", "treat source acquisition as ledger only", "no target data files were populated", "do not score delta_w yet"),
        ("DEC1492_1_EotWash", "use EotWash 2008 PRL plus 2012 review as source leads", "they identify material-pair WEP context and bounds", "extract bound/material rows next"),
        ("DEC1492_2_R10", "use R10 2020 PRL/arXiv as curve lead", "it is the modern short-range anchor", "digitize alpha(lambda) curve or find machine table"),
        ("DEC1492_3_MICROSCOPE", "use CMSM portal plus final/readout papers as official route", "local directories exist but official files are missing", "download/parse official files or document access blocker"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1492_0_1493",
            "next_target": "1493-Y5-R10-RAB-download-or-extract-delta-w-source-files-R10-EotWash-MICROSCOPE.md",
            "script": "scripts/Y5_R10_RAB_download_or_extract_delta_w_source_files_R10_EotWash_MICROSCOPE.py",
            "objective": "attempt actual source-file acquisition or extraction: download PDFs/portal metadata where accessible, stage R10 curve digitization skeleton, and create EotWash/MICROSCOPE parse blockers if access fails",
            "include": "local download targets; hash/provenance rows; extraction blockers; no-claim validation; curve digitization status",
            "exclude": "GitHub action; formalization-workbench edits; C_parent import; score-ready claim without populated target files",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_csvs() -> list[Path]:
    return [
        SOURCE_REGISTER,
        EXTERNAL_LEDGER,
        TARGET_MANIFEST,
        ACQUISITION_STATUS,
        EXTRACTION_REQUIREMENTS,
        DELTA_W_BLOCKERS,
        C_PARENT_REFUSAL,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(EXTERNAL_LEDGER, QUAR_EXTERNAL)
    shutil.copyfile(TARGET_MANIFEST, QUAR_TARGETS)
    shutil.copyfile(ACQUISITION_STATUS, QUAR_STATUS)
    shutil.copyfile(EXTERNAL_LEDGER, BRANCH_EXTERNAL)
    shutil.copyfile(TARGET_MANIFEST, BRANCH_TARGETS)
    shutil.copyfile(ACQUISITION_STATUS, BRANCH_STATUS)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows() -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    external = read_csv(EXTERNAL_LEDGER)
    targets = read_csv(TARGET_MANIFEST)
    status = read_csv(ACQUISITION_STATUS)
    requirements = read_csv(EXTRACTION_REQUIREMENTS)
    blockers = read_csv(DELTA_W_BLOCKERS)
    c_parent = read_csv(C_PARENT_REFUSAL)
    local = read_csv(LOCAL_STATUS)
    rejections = read_csv(REJECTION_LEDGER)
    decisions = read_csv(DECISION_LEDGER)
    next_rows = read_csv(NEXT_TARGET)

    checks: list[tuple[str, bool, str]] = [
        ("VAL1492_0_local_sources", all(row["exists_or_resolved"].lower() == "true" for row in sources), "all cited local source paths exist"),
        ("VAL1492_1_external_urls", all(row["url"].startswith("https://") and row["resolved_by_browse"].lower() == "true" for row in external), "external URLs are recorded and browser-resolved"),
        ("VAL1492_2_no_download_claim", all(row["file_acquired_now"].lower() == "false" for row in external), "external sources are ledgered, not falsely marked downloaded"),
        ("VAL1492_3_target_parents", all(row["target_parent_exists"].lower() == "true" for row in targets), "all local target parent directories exist"),
        ("VAL1492_4_targets_nonclaim", all(row["claim_allowed"].lower() == "false" and row["score_ready"].lower() == "false" for row in targets), "target files are nonclaim and not score-ready"),
        ("VAL1492_5_status_blocked", all(row["score_ready"].lower() == "false" for row in status), "all acquisition status rows remain blocked/non-score"),
        ("VAL1492_6_requirements", len(requirements) >= 7 and all(row["current_status"] == "REQUIRED_NOT_FILLED" for row in requirements), "extraction requirements are explicit and unfilled"),
        ("VAL1492_7_blockers", len(blockers) >= 6 and all(row["claim_allowed"].lower() == "false" for row in blockers), "delta_w scoring blockers remain active"),
        ("VAL1492_8_no_Cparent_import", (not C_PARENT_IMPORT.exists()) and all(row["claim_allowed"].lower() == "false" for row in c_parent), "live C_parent import remains absent and refused"),
        ("VAL1492_9_local_blocked", any(row["current_status"] == "NEXT_TARGET_EXTRACTION_OR_DOWNLOAD" for row in local), "local GR/Newton/WEP remains blocked pending extraction/download"),
        ("VAL1492_10_rejections", len(rejections) >= 7 and all(row["claim_allowed"].lower() == "false" for row in rejections), "rejection ledger blocks claim promotion"),
        ("VAL1492_11_decisions", any(row["decision_id"] == "DEC1492_3_MICROSCOPE" for row in decisions), "decision ledger covers MICROSCOPE source route"),
        ("VAL1492_12_next", len(next_rows) == 1 and next_rows[0]["next_id"] == "NEXT1492_0_1493", "1493 handoff written"),
        ("VAL1492_13_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1492 CSVs parse cleanly"),
        ("VAL1492_14_branch_copies", all(path.exists() for path in [QUAR_EXTERNAL, QUAR_TARGETS, QUAR_STATUS, BRANCH_EXTERNAL, BRANCH_TARGETS, BRANCH_STATUS]), "branch/quarantine nonclaim copies written"),
    ]
    remove_pycache()
    checks.append(("VAL1492_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"))
    modified_count = formalization_modified_count()
    checks.append(("VAL1492_16_formalization_untouched", modified_count == 0, f"formalization modified-file count since start={modified_count}"))
    claim_paths = generated_csvs() + [QUAR_EXTERNAL, QUAR_TARGETS, QUAR_STATUS, BRANCH_EXTERNAL, BRANCH_TARGETS, BRANCH_STATUS]
    claim_flags_false = True
    for path in claim_paths:
        for row in read_csv(path):
            for flag in ("valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if flag in row and row[flag].lower() != "false":
                    claim_flags_false = False
    checks.append(("VAL1492_17_claim_flags_false", claim_flags_false, "all prediction/claim flags remain false"))
    overall = all(result for _, result, _ in checks)
    checks.append(("VAL1492_18_overall", overall, "1492 records source URLs/targets and blocks delta_w scoring until extraction/download succeeds"))
    return [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "generated_utc": utc_now(),
        }
        for check_id, result, detail in checks
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("|", "/") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def write_doc() -> None:
    external = read_csv(EXTERNAL_LEDGER)
    targets = read_csv(TARGET_MANIFEST)
    status = read_csv(ACQUISITION_STATUS)
    requirements = read_csv(EXTRACTION_REQUIREMENTS)
    blockers = read_csv(DELTA_W_BLOCKERS)
    local = read_csv(LOCAL_STATUS)
    rejections = read_csv(REJECTION_LEDGER)
    decisions = read_csv(DECISION_LEDGER)
    validation = read_csv(VALIDATION)
    next_rows = read_csv(NEXT_TARGET)

    lines = [
        "# 1492 - delta_w Source Acquisition Ledger: EotWash, R10, MICROSCOPE",
        "",
        "## Verdict",
        "- Source leads are now explicit for EotWash WEP, R10 short-range inverse-square, and MICROSCOPE official files.",
        "- This pass does not claim acquisition of the actual data products; it writes local target paths, required columns, extraction methods, and claim gates.",
        "- `delta_w` scoring remains blocked until the target files are populated, parsed, sourced, and projected in one same-branch convention.",
        "",
        "## External Source Ledger",
        markdown_table(external, ["external_id", "arena", "title", "url", "doi_or_data_id", "current_status"]),
        "",
        "## Local Target Manifest",
        markdown_table(targets, ["target_id", "arena", "target_path", "target_exists", "current_status"]),
        "",
        "## Acquisition Status",
        markdown_table(status, ["status_id", "arena", "current_status", "next_action"]),
        "",
        "## Extraction Requirements",
        markdown_table(requirements, ["requirement_id", "arena", "required_object", "extraction_method", "current_status"]),
        "",
        "## Delta w Scoring Blockers",
        markdown_table(blockers, ["blocker_id", "blocking_marker", "reason"]),
        "",
        "## Local GR/Newton Status",
        markdown_table(local, ["status_id", "target", "current_status", "claim_effect"]),
        "",
        "## Rejection Ledger",
        markdown_table(rejections, ["rejection_id", "blocking_marker", "reason"]),
        "",
        "## Decision Ledger",
    ]
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} - {row['next_action']}.")
    lines.extend(
        [
            "",
            "## Validation",
            markdown_table(validation, ["check_id", "result", "detail"]),
            "",
            "## Next Target",
            markdown_table(next_rows, ["next_id", "next_target", "script", "objective"]),
            "",
        ]
    )
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    remove_pycache()
    ensure_target_dirs()
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(EXTERNAL_LEDGER, external_source_rows())
    write_csv(TARGET_MANIFEST, target_manifest_rows())
    write_csv(ACQUISITION_STATUS, acquisition_status_rows())
    write_csv(EXTRACTION_REQUIREMENTS, extraction_requirement_rows())
    write_csv(DELTA_W_BLOCKERS, delta_w_blocker_rows())
    write_csv(C_PARENT_REFUSAL, c_parent_refusal_rows())
    write_csv(LOCAL_STATUS, local_status_rows())
    write_csv(REJECTION_LEDGER, rejection_rows())
    write_csv(DECISION_LEDGER, decision_rows())
    write_csv(NEXT_TARGET, next_target_rows())
    copy_outputs()
    write_csv(VALIDATION, validation_rows())
    write_doc()
    remove_pycache()
    print(f"Wrote {DOC}")
    print(f"Wrote {VALIDATION}")


if __name__ == "__main__":
    main()
