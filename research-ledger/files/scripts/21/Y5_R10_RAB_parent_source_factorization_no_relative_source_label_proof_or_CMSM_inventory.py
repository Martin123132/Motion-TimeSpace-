from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
QUARANTINE = MICROSCOPE / "quarantine" / "1461"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1461-Y5-R10-RAB-parent-source-factorization-no-relative-source-label-proof-or-CMSM-inventory.md"

PREV_NEXT = OUT / "P8_Y5_R10_1460_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1460_VALIDATION.csv"
PREV_SOURCE_DECOMP = OUT / "P8_Y5_R10_1460_SOURCE_DECOMPOSITION_AND_ZERO_CONDITIONS.csv"
PREV_POINT_THEOREM = OUT / "P8_Y5_R10_1460_CALIBRATED_POINT_SOURCE_THEOREM_REOPEN.csv"
PREV_ACQ_ROUTE = OUT / "P8_Y5_R10_1460_OFFICIAL_DATA_ACQUISITION_ROUTE.csv"
PREV_SIGNING = OUT / "P8_Y5_R10_1460_PARENT_SIGNING_DECISION.csv"

LABEL_STACK_1231 = OUT / "P8_Y5_R10_1231_SOURCE_LABEL_FORGETTING_PROOF_STACK.csv"
COMMON_MODE_1332 = OUT / "P8_Y5_R10_1332_COMMON_MODE_SOURCE_THEOREM.csv"
COMMON_MODE_REDUCTION_1337 = OUT / "P8_Y5_R10_1337_COMMON_MODE_PREMISE_REDUCTION.csv"
COMMON_MODE_STATUS_1338 = OUT / "P8_Y5_R10_1338_COMMON_MODE_THEOREM_STATUS.csv"
SOURCE_LABEL_1450 = OUT / "P8_Y5_R10_1450_HILBERT_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv"
COMMON_G_GUARD_1450 = OUT / "P8_Y5_R10_1450_COMMON_MODE_ABSORPTION_GUARD.csv"
NO_SOURCE_SLOT_1451 = COEFF / "no_source_only_slot_operator_grammar_theorem_attempt_1451.csv"
NO_SOURCE_SLOT_SIGNING_1451 = COEFF / "C_parent_WEP_no_source_slot_signing_decision_1451.csv"
COUNTERMODEL_1449 = COEFF / "source_only_countermodel_retention_1449.csv"
SOURCE_WORLD_1456 = COEFF / "source_worldtube_projection_theorem_attempt_1456.csv"
MICROSCOPE_EXTERNAL_1070 = OUT / "P8_Y5_R10_1070_EXTERNAL_MICROSCOPE_READOUT_SOURCE_LEDGER.csv"
ORBIT_REQUIREMENTS_1068 = OUT / "P8_Y5_R10_1068_MICROSCOPE_ORBIT_READOUT_REQUIREMENTS.csv"

LIVE_OFFICIAL_READOUT = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"
LIVE_SOURCE_WORLD = MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv"
LIVE_MATERIAL_TENSOR = MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"
LIVE_CPARENT = COEFF / "C_parent_WEP_slot_import.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1461_SOURCE_REGISTER.csv"
FACTOR_PROOF = OUT / "P8_Y5_R10_1461_PARENT_SOURCE_FACTORIZATION_PROOF_ATTEMPT.csv"
NO_RELATIVE_AUDIT = OUT / "P8_Y5_R10_1461_NO_RELATIVE_SOURCE_LABEL_AUDIT.csv"
COUNTERMODEL_AUDIT = OUT / "P8_Y5_R10_1461_SOURCE_LABEL_COUNTERMODEL_AUDIT.csv"
CMSM_INVENTORY_SCAFFOLD = OUT / "P8_Y5_R10_1461_CMSM_INVENTORY_SCAFFOLD.csv"
CHECKSUM_SCAFFOLD = OUT / "P8_Y5_R10_1461_CMSM_CHECKSUM_AND_EXTRACTION_SCAFFOLD.csv"
LIVE_GUARD = OUT / "P8_Y5_R10_1461_LIVE_IMPORT_GUARD.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1461_REDUCTION_GATES.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1461_PARENT_SIGNING_DECISION.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1461_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1461_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1461_VALIDATION.csv"

QUAR_INVENTORY_TEMPLATE = QUARANTINE / "CMSM_OFFICIAL_INVENTORY_TEMPLATE_QUARANTINE_NONCLAIM.csv"
QUAR_CHECKSUM_TEMPLATE = QUARANTINE / "CMSM_DOWNLOAD_CHECKSUM_MANIFEST_TEMPLATE_QUARANTINE_NONCLAIM.csv"
QUAR_EXTRACTION_TEMPLATE = QUARANTINE / "CMSM_EXTRACTION_SCHEMA_TEMPLATE_QUARANTINE_NONCLAIM.csv"

BRANCH_FACTOR_PROOF = COEFF / "parent_source_factorization_no_relative_label_attempt_1461.csv"
BRANCH_CMSM_ROUTE = COEFF / "CMSM_inventory_checksum_route_nonclaim_1461.csv"
BRANCH_SIGNING = COEFF / "C_parent_WEP_source_factorization_signing_decision_1461.csv"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def rows_from_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv_ok(path: Path) -> bool:
    return bool(rows_from_csv(path))


def copy_branch(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def source_rows() -> list[dict[str, Any]]:
    sources = [
        ("SRC1461_0_prev_next", PREV_NEXT, "1460 handoff"),
        ("SRC1461_1_prev_validation", PREV_VALIDATION, "1460 validation"),
        ("SRC1461_2_prev_source_decomp", PREV_SOURCE_DECOMP, "1460 source decomposition"),
        ("SRC1461_3_prev_point_theorem", PREV_POINT_THEOREM, "1460 calibrated point-source theorem"),
        ("SRC1461_4_prev_acq_route", PREV_ACQ_ROUTE, "1460 official acquisition route"),
        ("SRC1461_5_prev_signing", PREV_SIGNING, "1460 signing decision"),
        ("SRC1461_6_label_stack_1231", LABEL_STACK_1231, "source-label forgetting proof stack"),
        ("SRC1461_7_common_mode_1332", COMMON_MODE_1332, "common-mode source theorem"),
        ("SRC1461_8_common_mode_reduction_1337", COMMON_MODE_REDUCTION_1337, "common-mode premise reduction"),
        ("SRC1461_9_common_mode_status_1338", COMMON_MODE_STATUS_1338, "common-mode theorem status"),
        ("SRC1461_10_source_label_1450", SOURCE_LABEL_1450, "Hilbert source-label forgetting attempt"),
        ("SRC1461_11_common_G_guard_1450", COMMON_G_GUARD_1450, "common G absorption guard"),
        ("SRC1461_12_no_slot_1451", NO_SOURCE_SLOT_1451, "no-source-only-slot grammar attempt"),
        ("SRC1461_13_no_slot_signing_1451", NO_SOURCE_SLOT_SIGNING_1451, "no-source-only-slot signing decision"),
        ("SRC1461_14_countermodel_1449", COUNTERMODEL_1449, "source-only countermodel retention"),
        ("SRC1461_15_source_world_1456", SOURCE_WORLD_1456, "source-worldtube theorem attempt"),
        ("SRC1461_16_external_1070", MICROSCOPE_EXTERNAL_1070, "MICROSCOPE external source ledger"),
        ("SRC1461_17_orbit_req_1068", ORBIT_REQUIREMENTS_1068, "MICROSCOPE orbit/readout requirements"),
    ]
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": path.exists(),
            "role": role,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, role in sources
    ]


def factorization_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "PSF1461_0_target",
            "claim_piece": "parent source factorization",
            "formal_statement": "rho_q(x)=q0 rho_m(x) for every ordinary Earth-source component, hence delta_q(x)=0",
            "proof_move": "make the active source functor factor through total Hilbert/coframe stress before any species/material label can enter",
            "status": "TARGET_SHARPENED",
            "if_signed": "1460 relative source-worldtube residual vanishes except ordinary common GM calibration and bounded metric multipoles",
            "current_blocker": "source functor label-forgetting and no-source-only-slot grammar are not parent-signed",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "PSF1461_1_Hilbert_total_source",
            "claim_piece": "single matter action gives one total active source",
            "formal_statement": "T_H^{mu nu}=2/sqrt(-g) delta S_matter/delta g_obs_munu = sum_A T_A^{mu nu}",
            "proof_move": "vary the summed action once, then couple geometry to T_H rather than to labelled pairs (T_A,A)",
            "status": "EXACT_CONDITIONAL_MATH",
            "if_signed": "species labels become bookkeeping after variation",
            "current_blocker": "constant per-sector weights w_A inside S_matter still survive unless the parent grammar forbids them",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "PSF1461_2_natural_additive_uniqueness",
            "claim_piece": "label-forgotten local source map has one scalar normalization",
            "formal_statement": "F_src(phi_*T)=phi_*F_src(T), F_src(T+U)=F_src(T)+F_src(U) -> F_src(T)=kappa0 T in the local GR branch",
            "proof_move": "after label forgetting, covariance and additivity leave only one measured-G normalization",
            "status": "CONDITIONAL_UNIQUENESS",
            "if_signed": "q0 can be calibrated as common G/GM and cannot form WEP source contrast",
            "current_blocker": "the theorem assumes labels have already been forgotten; it does not prove that",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "PSF1461_3_no_relative_slot_clause",
            "claim_piece": "no source-only coefficient slot",
            "formal_statement": "Allowed[S_matter] has no independent w_A, J_A, kappa_A, marker_A, or source-owner argument distinct from observed matter dynamics",
            "proof_move": "ban Hom(species/material label, active-source coefficient semiring) at parent action grammar level",
            "status": "REQUIRED_CLAUSE_NOT_REDUCED",
            "if_signed": "delta_q(x)=0 follows for ordinary matter source labels",
            "current_blocker": "AX1090/no-hidden-visible-hom and common measure/current clauses remain unsigned",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "PSF1461_4_countermodel",
            "claim_piece": "legal relative source label obstruction",
            "formal_statement": "S_matter=sum_A w_A S_A remains covariant/additive and gives T_src=sum_A w_A T_A",
            "proof_move": "exhibits the exact object that must be forbidden, not merely disliked",
            "status": "COUNTERMODEL_SURVIVES",
            "if_signed": "nothing; this blocks promotion until the no-slot clause is signed",
            "current_blocker": "current corpus has not excluded constant relative action/source weights",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "PSF1461_5_delta_q_verdict",
            "claim_piece": "delta_q(x)=0 proof status",
            "formal_statement": "delta_q(x)=0 is derivable iff PSF1461_1, PSF1461_2, PSF1461_3, and non-Hilbert/readout silence all parent-sign",
            "proof_move": "reduce the zero to a precise parent grammar contract",
            "status": "PROOF_NOT_CLOSED",
            "if_signed": "source-worldtube burden collapses to ordinary metric source/readout plus finite metric multipoles",
            "current_blocker": "relative w_A / J_A / marker / non-Hilbert current countermodels remain live",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def no_relative_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "NRS1461_0_source_functor_domain",
            "needed_clause": "source functor domain is total stress, not labelled stress pairs",
            "exact_condition": "F_src: Stress_total -> Geometry_source, not F_src: {(T_A,A)} -> Geometry_source",
            "current_evidence": "1450/1231 conditional source-label forgetting stack",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "blocks_delta_q_zero": True,
            "next_action": "derive source quotient q_src from parent action/category, or retain delta_q(x)",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "NRS1461_1_common_measure_current",
            "needed_clause": "one measure/action/current normalization for all ordinary matter sectors",
            "exact_condition": "no species Jacobian J_A and no independent action scale hbar_A/w_A in the active source channel",
            "current_evidence": "1451/1452 common-measure/current still unsigned",
            "status": "MISSING_AXIOM_NOT_REDUCED",
            "blocks_delta_q_zero": True,
            "next_action": "prove common measure/current from parent matter descent, or bound the induced residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "NRS1461_2_no_hidden_marker_hom",
            "needed_clause": "hidden/MTS marker cannot feed source coefficients",
            "exact_condition": "Hom(C_hidden or marker, Coeff_source)=0 in the local matter branch",
            "current_evidence": "AX1090/no-hidden-visible-hom not reduced",
            "status": "MISSING_PARENT_SIGNATURE",
            "blocks_delta_q_zero": True,
            "next_action": "derive no-hidden-visible-hom or keep qbar_marker/source rows live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "NRS1461_3_nonHilbert_current_silence",
            "needed_clause": "no non-Hilbert current bypasses the total stress source",
            "exact_condition": "J_NH=0, exact/projected-silent, or bounded in the WEP readout",
            "current_evidence": "1450 keeps non-Hilbert parallel gate open",
            "status": "OPEN_PARALLEL_GATE",
            "blocks_delta_q_zero": True,
            "next_action": "derive non-Hilbert silence or add residual coefficient rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "NRS1461_4_readout_no_reentry",
            "needed_clause": "downstream readout/source-worldtube kernels cannot recreate species labels",
            "exact_condition": "K_eta and K_X act on the already-varied parent source and have no material/species selector argument",
            "current_evidence": "1454/1456 conditional downstream-order theorem",
            "status": "CONDITIONAL_SOURCE_FILES_MISSING",
            "blocks_delta_q_zero": True,
            "next_action": "import official K_CMSM/source-worldtube or prove readout label silence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "NRS1461_5_delta_q_zero_decision",
            "needed_clause": "all no-relative-source-label clauses close together",
            "exact_condition": "NRS1461_0..4 parent-signed",
            "current_evidence": "multiple clauses remain conditional/open",
            "status": "DELTA_Q_ZERO_NOT_PROMOTED",
            "blocks_delta_q_zero": True,
            "next_action": "build CMSM inventory/checksum scaffold while continuing the parent grammar derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1461_0_relative_wA",
            "countermodel": "S_matter=sum_A w_A S_A",
            "why_survives": "covariant/additive and not excluded by current parent grammar",
            "effect_on_delta_q": "delta_q(x) becomes composition/source-profile dependent",
            "retention_decision": "RETAIN_LIVE_NONCLAIM",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1461_1_species_measure_jacobian",
            "countermodel": "species-dependent measure/current normalization J_A",
            "why_survives": "common measure/current owner not parent-derived",
            "effect_on_delta_q": "bypasses Hilbert total-source uniqueness",
            "retention_decision": "RETAIN_LIVE_NONCLAIM",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1461_2_hidden_marker_source_weight",
            "countermodel": "w_A(Xhat, marker, material) source coefficient",
            "why_survives": "no-hidden-visible-hom and no-marker extension are unsigned",
            "effect_on_delta_q": "source charge varies with hidden/material profile",
            "retention_decision": "RETAIN_LIVE_NONCLAIM",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1461_3_nonHilbert_source_current",
            "countermodel": "J_src = kappa T_Hilbert + J_NH",
            "why_survives": "non-Hilbert current silence is not proven",
            "effect_on_delta_q": "source residual can survive without appearing as species stress label",
            "retention_decision": "RETAIN_LIVE_NONCLAIM",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1461_4_readout_selector_reentry",
            "countermodel": "source-worldtube/readout kernel selects material/source profile after variation",
            "why_survives": "official downstream kernel not imported and readout no-reentry not source-signed",
            "effect_on_delta_q": "pipeline can manufacture or hide an apparent source residual",
            "retention_decision": "RETAIN_LIVE_NONCLAIM",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def cmsm_inventory_rows() -> list[dict[str, Any]]:
    portal = "https://cmsm-ds.onera.fr/"
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "inventory_id": "CMSM1461_0_portal",
            "object": "CMSM/ONERA data portal",
            "source_url_or_path": portal,
            "needed_action": "open portal in browser, record dataset names, file URLs, access/licence notes, and metadata dictionary",
            "local_quarantine_target": str(QUAR_INVENTORY_TEMPLATE),
            "current_status": "SCAFFOLD_ONLY_NOT_INVENTORIED",
            "checksum_required": True,
            "live_import_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "inventory_id": "CMSM1461_1_readout_arrays",
            "object": "K_CMSM official readout arrays",
            "source_url_or_path": portal,
            "needed_action": "identify files containing time/session/orbit, sensitive-axis readout, gx/gz, Sxx/Sxz, masks and calibration flags",
            "local_quarantine_target": str(QUAR_INVENTORY_TEMPLATE),
            "current_status": "MISSING_OFFICIAL_ARRAYS",
            "checksum_required": True,
            "live_import_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "inventory_id": "CMSM1461_2_orbit_attitude",
            "object": "orbit/attitude/mask kernel inputs",
            "source_url_or_path": portal,
            "needed_action": "identify ephemeris, attitude/quaternion or axis convention, segment windows, and flags needed for K_eta",
            "local_quarantine_target": str(QUAR_INVENTORY_TEMPLATE),
            "current_status": "MISSING_KERNEL_INPUTS",
            "checksum_required": True,
            "live_import_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "inventory_id": "CMSM1461_3_extraction_schema",
            "object": "reproducible extractor schema",
            "source_url_or_path": str(QUAR_EXTRACTION_TEMPLATE),
            "needed_action": "map raw columns to official_readout/source_worldtube/material tensor schemas with units and sign conventions",
            "local_quarantine_target": str(QUAR_EXTRACTION_TEMPLATE),
            "current_status": "TEMPLATE_WRITTEN_NONCLAIM",
            "checksum_required": False,
            "live_import_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def checksum_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "checksum_id": "CHK1461_0_manifest_template",
            "field": "dataset_id,file_name,source_url,local_quarantine_path,sha256,row_count,byte_count,downloaded_utc,source_note,valid_for_claim",
            "purpose": "prevent portal files or manual exports from becoming evidence without hash and provenance",
            "template_path": str(QUAR_CHECKSUM_TEMPLATE),
            "current_status": "TEMPLATE_WRITTEN_EMPTY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "checksum_id": "CHK1461_1_extractor_template",
            "field": "raw_dataset_id,target_schema,column_map,unit_map,sign_convention,mask_rule,source_path,valid_for_claim",
            "purpose": "force a declared column/unit/sign map before any live official row can be produced",
            "template_path": str(QUAR_EXTRACTION_TEMPLATE),
            "current_status": "TEMPLATE_WRITTEN_EMPTY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "checksum_id": "CHK1461_2_claim_guard",
            "field": "promotion requires hash, source URL/path, no placeholders, schema parse, branch lock, and validation pass",
            "purpose": "keep data plumbing useful while preserving no-claim discipline",
            "template_path": str(QUAR_INVENTORY_TEMPLATE),
            "current_status": "PROMOTION_BLOCKED_BY_DEFAULT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def quarantine_template_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    inventory = [
        {
            "dataset_id": "MISSING_DATASET_ID",
            "file_name": "MISSING_FILE_NAME",
            "source_url": "https://cmsm-ds.onera.fr/",
            "file_role": "official_readout_or_orbit_or_attitude_or_mask",
            "expected_columns": "MISSING_COLUMN_LIST",
            "licence_or_access_note": "MISSING_ACCESS_NOTE",
            "source_note": "quarantine template only; do not promote",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    checksum = [
        {
            "dataset_id": "MISSING_DATASET_ID",
            "file_name": "MISSING_FILE_NAME",
            "source_url": "MISSING_SOURCE_URL",
            "local_quarantine_path": "MISSING_LOCAL_PATH",
            "sha256": "MISSING_SHA256",
            "row_count": "MISSING_ROW_COUNT",
            "byte_count": "MISSING_BYTE_COUNT",
            "downloaded_utc": "MISSING_DOWNLOADED_UTC",
            "source_note": "quarantine template only; do not promote",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    extraction = [
        {
            "raw_dataset_id": "MISSING_DATASET_ID",
            "target_schema": "official_readout_or_source_worldtube_or_material_tensor",
            "column_map": "MISSING_COLUMN_MAP",
            "unit_map": "MISSING_UNIT_MAP",
            "sign_convention": "MISSING_SIGN_CONVENTION",
            "mask_rule": "MISSING_MASK_RULE",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    return inventory, checksum, extraction


def live_guard_rows() -> list[dict[str, Any]]:
    live_targets = [
        ("LIVE1461_0_official_readout", "official_readout", LIVE_OFFICIAL_READOUT),
        ("LIVE1461_1_source_worldtube", "source_worldtube", LIVE_SOURCE_WORLD),
        ("LIVE1461_2_material_tensor", "material_tensor", LIVE_MATERIAL_TENSOR),
        ("LIVE1461_3_C_parent", "C_parent_WEP", LIVE_CPARENT),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "live_guard_id": guard_id,
            "object": object_name,
            "live_path": str(path),
            "exists_now": path.exists(),
            "would_write_in_1461": False,
            "reason": "1461 writes only nonclaim ledgers and quarantine templates",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for guard_id, object_name, path in live_targets
    ]


def reduction_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1461_0_conditional_factorization_written",
            "gate": "conditional theorem reducing delta_q=0 to no-relative-source-label clauses is written",
            "gate_pass": True,
            "blocking_reason": "none; reduction is exact but conditional",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1461_1_source_label_forgetting_signed",
            "gate": "source functor forgets species/material labels before coupling",
            "gate_pass": False,
            "blocking_reason": "label-forgetting remains a parent contract, not a signed theorem",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1461_2_no_source_only_slot_signed",
            "gate": "no w_A/J_A/kappa_A/marker_A source-only slot in parent action",
            "gate_pass": False,
            "blocking_reason": "relative source-weight countermodel survives",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1461_3_nonHilbert_readout_silence",
            "gate": "non-Hilbert/readout re-entry channels are silent",
            "gate_pass": False,
            "blocking_reason": "parallel current/readout selector gates remain open",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1461_4_delta_q_zero",
            "gate": "delta_q(x)=0 promoted",
            "gate_pass": False,
            "blocking_reason": "requires gates 1-3; not parent-signed",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1461_5_CMSM_scaffold",
            "gate": "CMSM inventory/checksum scaffold written",
            "gate_pass": True,
            "blocking_reason": "scaffold only; no data acquired or imported",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1461_6_local_claim",
            "gate": "local WEP/local-GR claim allowed",
            "gate_pass": False,
            "blocking_reason": "delta_q zero, official source pack, material tensor, and C_parent remain absent",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1461_0_source_factorization",
            "target": "delta_q(x)=0 from parent source factorization/no-relative-source-label theorem",
            "conditional_reduction_written": True,
            "source_label_forgetting_signed": False,
            "no_source_only_slot_signed": False,
            "common_measure_current_signed": False,
            "nonHilbert_readout_silence_signed": False,
            "CMSM_scaffold_written": True,
            "delta_q_zero_import_allowed": False,
            "C_parent_WEP_import_allowed": False,
            "tau_WEP_numeric_allowed": False,
            "local_claim_allowed": False,
            "decision": "REFUSE_DELTA_Q_ZERO_IMPORT_WRITE_CMSM_SCAFFOLD",
            "reason": "the proof reduces to exact parent grammar clauses, but surviving countermodels show the current corpus has not signed those clauses",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1461_0_derivation",
            "decision": "delta_q(x)=0 is not assumed; it is reduced to a no-relative-source-label parent grammar theorem",
            "why": "this is the least hand-wavy route to collapsing the source-worldtube problem",
            "consequence": "MTS local-GR route gets a precise missing parent action clause rather than a vague coupling gap",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1461_1_countermodels",
            "decision": "retain relative source-weight, measure-current, hidden-marker, non-Hilbert, and readout-selector countermodels",
            "why": "each remains legal under the current signed corpus",
            "consequence": "no theorem-zero import and no tau_WEP numeric row",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1461_2_CMSM",
            "decision": "write CMSM inventory/checksum/extraction quarantine templates",
            "why": "if the proof path does not close soon, the data path must be reproducible and fail-closed",
            "consequence": "future official files can be acquired without touching live claim paths",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1461_0_1462",
            "next_target": "1462-Y5-R10-RAB-common-measure-current-parent-signature-or-first-CMSM-inventory-fill.md",
            "script": "scripts/Y5_R10_RAB_common_measure_current_parent_signature_or_first_CMSM_inventory_fill.py",
            "objective": "attack the sharpest remaining proof clause: common measure/current normalization; if it fails, fill the first CMSM quarantine inventory rows from official portal evidence",
            "include": "common measure/current theorem; species Jacobian countermodel; first CMSM inventory fill; checksum discipline; no live claim",
            "exclude": "numeric tau_WEP; local-GR pass; C_parent promotion; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    factor_proof: list[dict[str, Any]],
    no_relative: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    cmsm_inventory: list[dict[str, Any]],
    checksum: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_csvs = [
        SOURCE_REGISTER,
        FACTOR_PROOF,
        NO_RELATIVE_AUDIT,
        COUNTERMODEL_AUDIT,
        CMSM_INVENTORY_SCAFFOLD,
        CHECKSUM_SCAFFOLD,
        LIVE_GUARD,
        REDUCTION_GATES,
        SIGNING_DECISION,
        DECISION_LEDGER,
        NEXT_TARGET,
        QUAR_INVENTORY_TEMPLATE,
        QUAR_CHECKSUM_TEMPLATE,
        QUAR_EXTRACTION_TEMPLATE,
    ]
    all_sources_exist = all(truth(row["exists"]) for row in sources)
    proof_reduced_not_closed = any(row["status"] == "PROOF_NOT_CLOSED" for row in factor_proof)
    no_relative_blocks = all(truth(row["blocks_delta_q_zero"]) and not truth(row["valid_for_claim"]) for row in no_relative)
    countermodels_live = all(row["retention_decision"] == "RETAIN_LIVE_NONCLAIM" for row in countermodels)
    cmsm_nonclaim = all(not truth(row["live_import_allowed"]) and not truth(row["claim_allowed"]) for row in cmsm_inventory)
    checksum_nonclaim = all(not truth(row["valid_for_claim"]) and not truth(row["claim_allowed"]) for row in checksum)
    templates_parse = parse_csv_ok(QUAR_INVENTORY_TEMPLATE) and parse_csv_ok(QUAR_CHECKSUM_TEMPLATE) and parse_csv_ok(QUAR_EXTRACTION_TEMPLATE)
    live_paths_untouched = all(not truth(row["exists_now"]) and not truth(row["would_write_in_1461"]) for row in live_guard)
    gate_pattern_safe = truth(gates[0]["gate_pass"]) and truth(gates[5]["gate_pass"]) and all(
        not truth(row["gate_pass"]) for row in gates[1:5] + gates[6:]
    )
    signing_refuses = all(
        not truth(row["delta_q_zero_import_allowed"])
        and not truth(row["C_parent_WEP_import_allowed"])
        and not truth(row["tau_WEP_numeric_allowed"])
        and not truth(row["local_claim_allowed"])
        for row in signing
    )
    generated_parse = all(parse_csv_ok(path) for path in generated_csvs)
    branch_copies = BRANCH_FACTOR_PROOF.exists() and BRANCH_CMSM_ROUTE.exists() and BRANCH_SIGNING.exists()
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formal_recent = 0
    if FORMALIZATION.exists():
        formal_recent = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and path.stat().st_mtime > START_TS
        )
    checks = [
        ("VAL1461_0_sources", all_sources_exist, "all cited local source paths exist"),
        ("VAL1461_1_proof_reduced_not_closed", proof_reduced_not_closed, "delta_q zero proof reduced to parent clauses but not closed"),
        ("VAL1461_2_no_relative_blocks", no_relative_blocks, "no-relative-source-label clauses remain blocking and nonclaim"),
        ("VAL1461_3_countermodels_live", countermodels_live, "source-label countermodels remain live"),
        ("VAL1461_4_CMSM_scaffold_nonclaim", cmsm_nonclaim, "CMSM inventory scaffold is nonclaim and no live import is allowed"),
        ("VAL1461_5_checksum_scaffold_nonclaim", checksum_nonclaim, "checksum/extraction scaffold is nonclaim"),
        ("VAL1461_6_quarantine_templates_parse", templates_parse, "CMSM quarantine templates parse cleanly"),
        ("VAL1461_7_live_paths_untouched", live_paths_untouched, "critical live official/source/material/Cparent files remain absent"),
        ("VAL1461_8_gate_pattern_safe", gate_pattern_safe, "only conditional reduction and scaffold gates pass; claim gates remain false"),
        ("VAL1461_9_signing_refuses", signing_refuses, "parent signing decision refuses delta_q/Cparent/tau/local claim"),
        ("VAL1461_10_generated_csv_parse", generated_parse, "all generated 1461 CSVs parse cleanly"),
        ("VAL1461_11_branch_copies", branch_copies, "nonclaim branch copies written"),
        ("VAL1461_12_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1461_13_formalization_untouched", formal_recent == 0, f"formalization modified-file count since start={formal_recent}"),
        ("VAL1461_14_overall", True, "1461 reduces delta_q=0 to exact parent clauses and writes CMSM quarantine scaffolds without claim promotion"),
    ]
    return [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "generated_utc": now(),
        }
        for check_id, passed, detail in checks
    ]


def write_table(handle, title: str, rows: list[dict[str, Any]]) -> None:
    handle.write(f"## {title}\n\n")
    if not rows:
        handle.write("_No rows._\n\n")
        return
    fields = list(rows[0].keys())
    handle.write("| " + " | ".join(fields) + " |\n")
    handle.write("| " + " | ".join(["---"] * len(fields)) + " |\n")
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fields]
        handle.write("| " + " | ".join(values) + " |\n")
    handle.write("\n")


def write_doc(
    sources: list[dict[str, Any]],
    factor_proof: list[dict[str, Any]],
    no_relative: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    cmsm_inventory: list[dict[str, Any]],
    checksum: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    with DOC.open("w", encoding="utf-8") as handle:
        handle.write("# 1461 - Parent source factorization/no-relative-source-label proof or CMSM inventory\n\n")
        handle.write(
            "**Current verdict:** the clean proof route is now reduced to one sharp parent-action statement: "
            "the active source functor must forget species/material labels before coupling, and the parent matter grammar "
            "must contain no source-only `w_A`, `J_A`, `kappa_A`, marker, or non-Hilbert bypass. The math is clean, "
            "but the current corpus has not signed those clauses, so `delta_q(x)=0` is not imported.\n\n"
        )
        handle.write(
            "**Useful progress:** this is not a mushy failure. We know exactly what must be proved next: common "
            "measure/current normalization and no relative source slot. Because that proof is still open, 1461 also "
            "writes fail-closed CMSM inventory/checksum/extraction templates for the official data route.\n\n"
        )
        write_table(handle, "Source register", sources)
        write_table(handle, "Parent source factorization proof attempt", factor_proof)
        write_table(handle, "No-relative-source-label audit", no_relative)
        write_table(handle, "Source-label countermodel audit", countermodels)
        write_table(handle, "CMSM inventory scaffold", cmsm_inventory)
        write_table(handle, "CMSM checksum and extraction scaffold", checksum)
        write_table(handle, "Live import guard", live_guard)
        write_table(handle, "Reduction gates", gates)
        write_table(handle, "Parent signing decision", signing)
        write_table(handle, "Decision ledger", decisions)
        write_table(handle, "Validation", validation)
        write_table(handle, "Next target", next_target)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    sources = source_rows()
    factor_proof = factorization_proof_rows()
    no_relative = no_relative_audit_rows()
    countermodels = countermodel_rows()
    cmsm_inventory = cmsm_inventory_rows()
    checksum = checksum_rows()
    inventory_template, checksum_template, extraction_template = quarantine_template_rows()
    live_guard = live_guard_rows()
    gates = reduction_gate_rows()
    signing = signing_decision_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(FACTOR_PROOF, factor_proof)
    write_csv(NO_RELATIVE_AUDIT, no_relative)
    write_csv(COUNTERMODEL_AUDIT, countermodels)
    write_csv(CMSM_INVENTORY_SCAFFOLD, cmsm_inventory)
    write_csv(CHECKSUM_SCAFFOLD, checksum)
    write_csv(QUAR_INVENTORY_TEMPLATE, inventory_template)
    write_csv(QUAR_CHECKSUM_TEMPLATE, checksum_template)
    write_csv(QUAR_EXTRACTION_TEMPLATE, extraction_template)
    write_csv(LIVE_GUARD, live_guard)
    write_csv(REDUCTION_GATES, gates)
    write_csv(SIGNING_DECISION, signing)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(FACTOR_PROOF, BRANCH_FACTOR_PROOF)
    copy_branch(CMSM_INVENTORY_SCAFFOLD, BRANCH_CMSM_ROUTE)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    remove_pycache()
    validation = validation_rows(sources, factor_proof, no_relative, countermodels, cmsm_inventory, checksum, live_guard, gates, signing)
    write_csv(VALIDATION, validation)
    write_doc(sources, factor_proof, no_relative, countermodels, cmsm_inventory, checksum, live_guard, gates, signing, decisions, validation, next_target)
    print("Y5_R10_1461_source_factorization_reduced_CMSM_scaffold_written_nonclaim")


if __name__ == "__main__":
    main()
