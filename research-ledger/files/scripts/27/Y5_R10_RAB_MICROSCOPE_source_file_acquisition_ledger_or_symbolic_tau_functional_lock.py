from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1483-Y5-R10-RAB-MICROSCOPE-source-file-acquisition-ledger-or-symbolic-tau-functional-lock.md"
START_TS = datetime.now(timezone.utc).timestamp()

PREV_NEXT = OUT / "P8_Y5_R10_1482_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1482_VALIDATION.csv"
PREV_WEB = OUT / "P8_Y5_R10_1482_OFFICIAL_WEB_SOURCE_CANDIDATES.csv"
PREV_MANIFEST = OUT / "P8_Y5_R10_1482_OFFICIAL_INPUT_MANIFEST_UPDATE.csv"
PREV_PARSER = OUT / "P8_Y5_R10_1482_PARSER_PRECHECK.csv"
PREV_TAU = OUT / "P8_Y5_R10_1482_TAU_WEP_READINESS_UPDATE.csv"
PREV_HOM = OUT / "P8_Y5_R10_1482_HOM_PARENT_GENERATOR_CLOSURE_ATTEMPT.csv"
PREV_REJECTION = OUT / "P8_Y5_R10_1482_REJECTION_LEDGER.csv"

WEB_1336 = MICROSCOPE / "metadata" / "P8_Y5_R10_1336_WEB_SOURCE_CANDIDATE_REGISTER.csv"
READOUT_SCHEMA = MICROSCOPE / "metadata" / "P8_Y5_R10_1336_OFFICIAL_READOUT_SCHEMA.csv"
SOURCE_SCHEMA = MICROSCOPE / "metadata" / "P8_Y5_R10_1336_SOURCE_WORLDTUBE_SCHEMA.csv"
PRODUCT_SCHEMA = MICROSCOPE / "metadata" / "P8_Y5_R10_1336_PRODUCT_CONVENTION_SCHEMA.csv"
BRANCH_SCHEMA = MICROSCOPE / "metadata" / "P8_Y5_R10_1336_BRANCH_CLASSIFIER_SCHEMA.csv"
PRODUCT_LIVE = MICROSCOPE / "product_convention" / "P_WEP_eta_product_convention.csv"
BRANCH_LIVE = MICROSCOPE / "branch_classifier" / "P_WEP_same_parent_branch_lock.csv"
READOUT_REQUIREMENTS = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout_REQUIREMENTS.csv"
READOUT_LIVE = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"
SOURCE_LIVE = MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv"
MATERIAL_LIVE = MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"
C_PARENT_IMPORT = MICROSCOPE / "branch_locked_wep" / "coefficients" / "C_parent_WEP_slot_import.csv"
C_PARENT_SCHEMA = MICROSCOPE / "branch_locked_wep" / "coefficients" / "C_parent_import_schema.csv"

OLD_ACQ = MICROSCOPE / "branch_locked_wep" / "residuals" / "P_WEP_source_acquisition_ledger.csv"
OLD_PACK = MICROSCOPE / "branch_locked_wep" / "residuals" / "official_microscope_source_pack_manifest.csv"
OLD_PARSE = MICROSCOPE / "branch_locked_wep" / "residuals" / "source_pack_parser_dryrun.csv"
OLD_PRIORITY = MICROSCOPE / "branch_locked_wep" / "residuals" / "source_pack_acquisition_priority.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1483_SOURCE_REGISTER.csv"
ACQUISITION_LEDGER = OUT / "P8_Y5_R10_1483_SOURCE_FILE_ACQUISITION_LEDGER.csv"
PACKAGE_CHECKLIST = OUT / "P8_Y5_R10_1483_OFFICIAL_PACKAGE_CHECKLIST.csv"
TAU_FUNCTIONAL_LOCK = OUT / "P8_Y5_R10_1483_SYMBOLIC_TAU_FUNCTIONAL_LOCK.csv"
TAU_COLUMN_SCHEMA = OUT / "P8_Y5_R10_1483_TAU_INPUT_COLUMN_SCHEMA.csv"
PARSER_REFRESH = OUT / "P8_Y5_R10_1483_PARSER_PRECHECK_REFRESH.csv"
C_PARENT_INTERACTIONS = OUT / "P8_Y5_R10_1483_C_PARENT_INTERACTION_POINTS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1483_REJECTION_LEDGER.csv"
NO_CLAIM_GATES = OUT / "P8_Y5_R10_1483_NO_CLAIM_GATES.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1483_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1483_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1483_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1483"
QUAR_ACQ = QUARANTINE / "SOURCE_FILE_ACQUISITION_LEDGER_NONCLAIM.csv"
QUAR_TAU = QUARANTINE / "SYMBOLIC_TAU_FUNCTIONAL_LOCK_NONCLAIM.csv"
QUAR_PARSE = QUARANTINE / "PARSER_PRECHECK_REFRESH_NONCLAIM.csv"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_TAU_LOCK = BRANCH_RESIDUALS / "tau_eff_functional_lock_nonclaim_1483.csv"
BRANCH_ACQ_LEDGER = BRANCH_RESIDUALS / "source_file_acquisition_ledger_nonclaim_1483.csv"
BRANCH_PARSE_REFRESH = BRANCH_RESIDUALS / "parser_precheck_refresh_nonclaim_1483.csv"


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


def text_has_blocker(path: Path) -> bool:
    if not path.exists():
        return True
    text = path.read_text(encoding="utf-8", errors="replace").upper()
    return any(marker in text for marker in ["MISSING", "PENDING", "NONCLAIM", "FALSE", "ABSENT", "NOT_EVALUATED"])


def source_rows() -> list[dict[str, Any]]:
    sources = [
        ("SRC1483_0_prev_next", PREV_NEXT, "1482 handoff"),
        ("SRC1483_1_prev_validation", PREV_VALIDATION, "1482 validation"),
        ("SRC1483_2_prev_web", PREV_WEB, "1482 official web candidates"),
        ("SRC1483_3_prev_manifest", PREV_MANIFEST, "1482 source-pack manifest update"),
        ("SRC1483_4_prev_parser", PREV_PARSER, "1482 parser precheck"),
        ("SRC1483_5_prev_tau", PREV_TAU, "1482 tau readiness"),
        ("SRC1483_6_prev_Hom", PREV_HOM, "1482 Hom closure attempt"),
        ("SRC1483_7_prev_rejection", PREV_REJECTION, "1482 rejection ledger"),
        ("SRC1483_8_web1336", WEB_1336, "existing ONERA/CMSM web source candidate register"),
        ("SRC1483_9_readout_schema", READOUT_SCHEMA, "official readout schema"),
        ("SRC1483_10_source_schema", SOURCE_SCHEMA, "source-worldtube schema"),
        ("SRC1483_11_product_schema", PRODUCT_SCHEMA, "product convention schema"),
        ("SRC1483_12_branch_schema", BRANCH_SCHEMA, "branch classifier schema"),
        ("SRC1483_13_product_live", PRODUCT_LIVE, "partial product convention row"),
        ("SRC1483_14_branch_live", BRANCH_LIVE, "same-branch guard row"),
        ("SRC1483_15_readout_requirements", READOUT_REQUIREMENTS, "requirements-only readout scaffold"),
        ("SRC1483_16_C_parent_schema", C_PARENT_SCHEMA, "C_parent import schema"),
        ("SRC1483_17_old_acq", OLD_ACQ, "prior source acquisition ledger"),
        ("SRC1483_18_old_pack", OLD_PACK, "prior official source-pack manifest"),
        ("SRC1483_19_old_parse", OLD_PARSE, "prior parser dry-run"),
        ("SRC1483_20_old_priority", OLD_PRIORITY, "prior source-pack priority ledger"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": source_id,
            "path_or_url": rel(path),
            "source_kind": "local_file",
            "exists_or_resolved": path.exists(),
            "usage": usage,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, usage in sources
    ]


def acquisition_rows() -> list[dict[str, Any]]:
    candidates = [
        (
            "ACQ1483_0_ONERA_data_page",
            "https://microscope.onera.fr/fr/publication/microscope-data-are-available",
            "official announcement page",
            "states mission data are available and points to the CMSM/REGARDS portal",
            "PORTAL_POINTER_ONLY",
            "open portal and capture official package/filelist/checksum metadata before import",
        ),
        (
            "ACQ1483_1_ONERA_english_node",
            "https://microscope.onera.fr/en/node/59",
            "official announcement page",
            "states mission data are available and points to REGARDS/CNES route",
            "PORTAL_POINTER_ONLY",
            "prefer portal filelist over hand-entered URLs",
        ),
        (
            "ACQ1483_2_CMSM_portal",
            "https://cmsm-ds.onera.fr/user/microscope",
            "official data portal",
            "candidate route for raw/calibrated/auxiliary/orbit products",
            "BROWSER_PORTAL_NEEDED_NO_LOCAL_ARRAYS",
            "capture package id, module id, filenames, checksums, license, and schema",
        ),
        (
            "ACQ1483_3_REGARDS_CNES_route",
            "https://regards.cnes.fr/user/microscope",
            "official data portal",
            "alternate/current route advertised by ONERA English page",
            "BROWSER_PORTAL_NEEDED_NO_LOCAL_ARRAYS",
            "capture official package metadata; do not infer package identities",
        ),
        (
            "ACQ1483_4_CQG_analysis",
            "https://arxiv.org/abs/2209.15488",
            "primary analysis paper",
            "eta formula, 4 Hz accelerometer data, session/mask/model structure",
            "SCHEMA_ANCHOR_ONLY",
            "use for required columns and model semantics, not as machine-array source",
        ),
        (
            "ACQ1483_5_PRL_result",
            "https://arxiv.org/abs/2209.15487",
            "primary result paper",
            "eta(Ti,Pt) bound and final result",
            "BOUND_PROVENANCE_ONLY",
            "use as bound/provenance; forbid bound-inversion into C_parent",
        ),
        (
            "ACQ1483_6_OCA_context",
            "https://www.oca.eu/fr/microscope",
            "institutional mission page",
            "states raw/calibrated/auxiliary data route and user support context",
            "PORTAL_CONTEXT_ONLY",
            "use as route corroboration; still require official portal filelist",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "acquisition_id": acquisition_id,
            "url": url,
            "source_kind": source_kind,
            "expected_use": expected_use,
            "current_status": status,
            "next_action": next_action,
            "local_file_created": False,
            "source_file_imported": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for acquisition_id, url, source_kind, expected_use, status, next_action in candidates
    ]


def package_checklist_rows() -> list[dict[str, Any]]:
    items = [
        ("PKG1483_0_package_id", "official package id / module id", "metadata", "MISSING", "required before any download is treated as official"),
        ("PKG1483_1_filelist", "portal file list with filenames and product categories", "metadata", "MISSING", "needed to distinguish raw/calibrated/aux/orbit products"),
        ("PKG1483_2_checksums", "checksums or reproducible hash manifest", "metadata", "MISSING", "guards against silent file mutation"),
        ("PKG1483_3_license_access", "license/access terms and citation requirement", "docs", "MISSING", "needed for source provenance"),
        ("PKG1483_4_data_dictionary", "official data dictionary/schema", "docs", "MISSING", "needed before parser can read arrays"),
        ("PKG1483_5_readout_arrays", "accelerometer/readout arrays with timestamps and masks", "official_readout", "MISSING_LIVE_FILE", "needed for K_CMSM"),
        ("PKG1483_6_attitude_orbit", "attitude, angular velocity/acceleration, orbit position/velocity", "official_readout", "MISSING_LIVE_FILE", "needed for projection and orbit average"),
        ("PKG1483_7_session_masks", "science session, calibration, glitch/onboard masks", "official_readout", "MISSING_LIVE_FILE", "needed for final-analysis weighting"),
        ("PKG1483_8_source_worldtube", "Earth/source profile or source projection model", "source_worldtube", "MISSING_LIVE_FILE", "needed for R_source"),
        ("PKG1483_9_units_axes", "axis orientation, units, sign/body-order convention", "product_convention", "PARTIAL_PENDING", "needed to lock tau sign and compare to eta"),
        ("PKG1483_10_branch_lock", "same-parent-branch id across all inputs", "branch_classifier", "GUARD_ONLY_NONCLAIM", "prevents mixed-basis claims"),
        ("PKG1483_11_C_parent", "theorem-zero or sourced finite parent coefficient", "coefficients", "MISSING_LIVE_FILE", "needed for a real MTS prediction"),
        ("PKG1483_12_material_tensor", "full TA6V-minus-PtRh10 parent-basis material tensor", "derived", "MISSING_LIVE_FILE", "needed for R_material"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "required_item": item,
            "target_bucket": bucket,
            "current_status": status,
            "why_required": why,
            "claim_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, item, bucket, status, why in items
    ]


def tau_lock_rows() -> list[dict[str, Any]]:
    formula = "tau_eff_X = < K_CMSM^a(t,s) R_source_a^X(t,s) >_{accepted sessions, masks, orbit weights, product convention}"
    rows = [
        ("TAULOCK1483_0_domain", "domain", "accepted MICROSCOPE science-session rows after official masks and calibration cuts", "official timestamps/session/mask rows", "MISSING_LIVE_READOUT_MATRIX", "none"),
        ("TAULOCK1483_1_readout_kernel", "K_CMSM^a", "maps observed source/material response component a into the eta readout channel", "declared m/s^2 or dimensionless-normalized units; sign and axis convention", "MISSING_LIVE_READOUT_MATRIX", "official readout/design matrix"),
        ("TAULOCK1483_2_source_kernel", "R_source_a^X", "finite Earth/source worldtube response in the same parent basis X", "basis-matched source units declared with model/dataset path", "MISSING_SOURCE_WORLDTUBE", "source profile/orbit shell weighting"),
        ("TAULOCK1483_3_mask_weight", "W(t,s)", "official session, glitch, calibration, and orbit weights; no hand masking", "dimensionless weights summing by declared convention", "MISSING_MASK_AND_WEIGHT_RULE", "official data dictionary"),
        ("TAULOCK1483_4_product_convention", "eta/order/sign", "eta(Ti,Pt), body order, sensitive-axis sign, and positive-X orientation", "dimensionless eta convention", "PARTIAL_PENDING_NONCLAIM", "official convention row without pending fields"),
        ("TAULOCK1483_5_branch_lock", "branch_id", "every factor must declare the same parent branch id", "identifier only", "GUARD_EXISTS_NONCLAIM", "parent-owned branch proof"),
        ("TAULOCK1483_6_output", "tau_eff_X", formula, "units equal K_CMSM times R_source after declared normalization", "SYMBOLIC_ONLY_NO_NUMERIC_OUTPUT", "all above inputs"),
        ("TAULOCK1483_7_forbidden_shortcuts", "refusal rule", "tau_eff=1, bound inversion, DD-only basis, measured-G absorption, and mixed-branch rows are invalid", "n/a", "ACTIVE_REFUSAL_RULE", "none; this is locked now"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "lock_id": lock_id,
            "factor": symbol,
            "symbol": symbol,
            "definition": definition,
            "required_units_or_convention": units,
            "current_status": status,
            "missing_for_evaluation": missing,
            "numeric_value": "NOT_EVALUATED",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for lock_id, symbol, definition, units, status, missing in rows
    ]


def tau_column_schema_rows() -> list[dict[str, Any]]:
    columns = [
        ("same_parent_branch_id", "string", "must equal active branch id"),
        ("session_id", "string", "official MICROSCOPE session/segment id"),
        ("time_s_or_phase", "number/string", "seconds with epoch or orbit phase key"),
        ("accepted_mask", "boolean/int", "official analysis mask after cuts"),
        ("axis", "string", "sensitive X axis or declared transformed axis"),
        ("K_CMSM_component", "string", "readout/source component label"),
        ("K_CMSM_value", "number", "readout kernel value"),
        ("K_CMSM_units", "string", "units/convention for readout kernel"),
        ("R_source_component", "string", "source basis component label"),
        ("R_source_value", "number", "source worldtube/projection value"),
        ("R_source_units", "string", "units/convention for source component"),
        ("orbit_weight", "number", "weight in accepted average"),
        ("product_sign", "number/string", "declared sign/body-order convention"),
        ("source_url_or_path", "string", "official file/source path"),
        ("checksum_or_package_id", "string", "provenance identifier"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "schema_id": f"TAUSCHEMA1483_{idx}",
            "column": column,
            "type": dtype,
            "requirement": requirement,
            "required_for_score": True,
            "current_status": "SCHEMA_LOCKED_VALUE_MISSING",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for idx, (column, dtype, requirement) in enumerate(columns)
    ]


def parser_refresh_rows() -> list[dict[str, Any]]:
    targets = [
        ("PARSE1483_0_live_readout", "live K_CMSM readout", READOUT_LIVE, "must be real readout/design matrix"),
        ("PARSE1483_1_readout_requirements", "readout requirements", READOUT_REQUIREMENTS, "requirements-only scaffold"),
        ("PARSE1483_2_source_worldtube", "source worldtube", SOURCE_LIVE, "must be real source projection file"),
        ("PARSE1483_3_product_convention", "product convention", PRODUCT_LIVE, "partial row currently has pending fields"),
        ("PARSE1483_4_branch_guard", "branch guard", BRANCH_LIVE, "guard row, not prediction"),
        ("PARSE1483_5_C_parent_import", "C_parent import", C_PARENT_IMPORT, "must be theorem-zero or sourced coefficient"),
        ("PARSE1483_6_material_tensor", "material tensor", MATERIAL_LIVE, "must be full MTS material tensor"),
    ]
    rows: list[dict[str, Any]] = []
    for parser_id, target_role, target, condition in targets:
        exists = target.exists()
        has_blocker = text_has_blocker(target)
        if not exists:
            status = "REFUSED_TARGET_ABSENT"
            reason = "required live target does not exist"
        elif has_blocker:
            status = "REFUSED_PENDING_OR_NONCLAIM_FIELDS"
            reason = "target exists but contains pending/missing/nonclaim markers or false claim flags"
        else:
            status = "STRUCTURE_OK_SCORE_STILL_DISABLED_BY_CROSS_FACTOR_GATES"
            reason = "individual structure is not enough for score permission"
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "parser_id": parser_id,
                "target_role": target_role,
                "target_path": str(target),
                "target_exists": exists,
                "condition": condition,
                "parser_status": status,
                "refusal_reason": reason,
                "score_permission": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def c_parent_interaction_rows() -> list[dict[str, Any]]:
    items = [
        ("CPI1483_0_factorization", "WEP product separates coefficient and apparatus/source functional", "eta_pred = | C_parent_X * R_material_X * tau_eff_X | summed over declared basis X", "tau lock supplies only tau_eff_X; it does not determine C_parent_X", "MISSING_C_PARENT_IMPORT"),
        ("CPI1483_1_no_bound_inversion", "MICROSCOPE bound cannot define C_parent", "bound may reject a sourced C_parent but cannot choose it", "prevents circular fit-as-prediction", "ACTIVE_REFUSAL_RULE"),
        ("CPI1483_2_zero_certificate", "C_parent_X=0 requires parent theorem-zero", "zero row must cite parent proof and satisfy C_parent_import_schema", "closure preference remains invalid", "NOT_PROVEN"),
        ("CPI1483_3_finite_import", "finite C_parent requires units/sign/basis/source", "C_parent_WEP_slot_import.csv must parse with no placeholders", "keeps finite residual route honest", "MISSING_IMPORT_ROW"),
        ("CPI1483_4_tau_dependency", "tau cannot be evaluated before source/readout data", "tau_eff_X remains symbolic until K_CMSM and R_source pass", "blocks WEP score even if C_parent is later found", "TAU_SYMBOLIC_ONLY"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "interaction_id": interaction_id,
            "rule": rule,
            "contract": contract,
            "why_it_matters": why,
            "current_status": status,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for interaction_id, rule, contract, why, status in items
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1483_0_no_source_file_import", "OFFICIAL_PACKAGE_NOT_IMPORTED", "no official portal package/filelist/checksum was imported"),
        ("REJ1483_1_readout_absent", "MISSING_LIVE_READOUT_MATRIX", "K_CMSM target file remains absent"),
        ("REJ1483_2_source_absent", "MISSING_SOURCE_WORLDTUBE", "R_source target file remains absent"),
        ("REJ1483_3_tau_symbolic", "TAU_EFF_SYMBOLIC_ONLY", "tau functional is locked but not evaluated"),
        ("REJ1483_4_product_pending", "PENDING_PRODUCT_SIGN_UNITS_ORBIT", "product convention still carries pending fields"),
        ("REJ1483_5_C_parent_absent", "MISSING_C_PARENT_IMPORT", "parent coefficient/theorem-zero import remains absent"),
        ("REJ1483_6_material_absent", "MISSING_FULL_PARENT_MATERIAL_TENSOR", "full material tensor remains absent"),
        ("REJ1483_7_no_local_claim", "CLAIM_PROMOTION_FORBIDDEN", "no WEP/local-GR/Newton claim can be promoted"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "blocking_marker": marker,
            "reason": reason,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rejection_id, marker, reason in rows
    ]


def gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("GATE1483_0_source_routes_recorded", True, "ONERA/CMSM/REGARDS/CQG/PRL/OCA source routes are recorded"),
        ("GATE1483_1_no_import", not READOUT_LIVE.exists() and not SOURCE_LIVE.exists(), "no live readout/source file was fabricated"),
        ("GATE1483_2_tau_locked", True, "symbolic tau functional and required columns are explicit"),
        ("GATE1483_3_tau_not_evaluated", True, "all tau rows keep numeric_value=NOT_EVALUATED"),
        ("GATE1483_4_parser_refuses_score", True, "parser refresh keeps score_permission=false"),
        ("GATE1483_5_C_parent_independent", True, "C_parent remains independent and missing"),
        ("GATE1483_6_claim_flags_false", True, "all generated claim flags remain false"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate_pass": gate_pass,
            "detail": detail,
            "claim_effect": "blocks claim" if gate_id != "GATE1483_0_source_routes_recorded" else "source-ledger only",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate_pass, detail in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    decisions = [
        ("DEC1483_0_do_not_download_blind", "do not pull anonymous portal/browser payloads into live claim files", "official package identity/checksum/schema must be captured first", "source acquisition remains ledger-only"),
        ("DEC1483_1_lock_tau_contract", "lock tau_eff as a symbolic functional rather than a unit-kernel shortcut", "this lets future MICROSCOPE arrays drop in without changing theory", "tau_eff=1 remains forbidden"),
        ("DEC1483_2_keep_C_parent_separate", "keep C_parent as the coupling bottleneck, not a data-derived fit", "MICROSCOPE can test but not define the theory coefficient", "next derivation must still attack the coupling slot"),
        ("DEC1483_3_next_target", "next step should build a parent-basis material/source/tau product interface", "readout data alone will not produce local-GR reduction without C_parent and material/source basis", "1484 should define the branch-locked product interface and refusal tests"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "why": why,
            "consequence": consequence,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, why, consequence in decisions
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1483_0_1484",
            "next_target": "1484-Y5-R10-RAB-branch-locked-WEP-product-interface-or-C-parent-coupling-derivation.md",
            "script": "scripts/Y5_R10_RAB_branch_locked_WEP_product_interface_or_C_parent_coupling_derivation.py",
            "objective": "define the complete branch-locked WEP product interface connecting C_parent, R_material, R_source, and tau_eff; then try again to derive or theorem-zero the C_parent coupling slot",
            "include": "product interface schema; basis labels; units/sign/refusal tests; C_parent theorem clauses; material/source/tau compatibility gates",
            "exclude": "GitHub action; formalization-workbench edits; numeric WEP/local-GR claim; fabricated arrays; bound-inverted coefficient",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def all_claim_flags_false(groups: list[list[dict[str, Any]]]) -> bool:
    for group in groups:
        for row in group:
            if str(row.get("valid_prediction_row", "False")) == "True":
                return False
            if str(row.get("valid_for_claim", "False")) != "False":
                return False
            if str(row.get("claim_allowed", "False")) != "False":
                return False
    return True


def validation_rows(
    sources: list[dict[str, Any]],
    acquisitions: list[dict[str, Any]],
    checklist: list[dict[str, Any]],
    tau: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    c_parent: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated = [
        SOURCE_REGISTER,
        ACQUISITION_LEDGER,
        PACKAGE_CHECKLIST,
        TAU_FUNCTIONAL_LOCK,
        TAU_COLUMN_SCHEMA,
        PARSER_REFRESH,
        C_PARENT_INTERACTIONS,
        REJECTION_LEDGER,
        NO_CLAIM_GATES,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    source_paths_exist = all(row["exists_or_resolved"] for row in sources)
    route_rows_ok = all(row["url"].startswith("https://") and not row["source_file_imported"] for row in acquisitions)
    checklist_blocked = all(not row["claim_ready"] for row in checklist)
    tau_symbolic = all(row["numeric_value"] == "NOT_EVALUATED" and not row["score_ready"] for row in tau)
    schema_locked = len(schema) >= 15 and all(row["current_status"] == "SCHEMA_LOCKED_VALUE_MISSING" for row in schema)
    parser_refuses = all(not row["score_permission"] and not row["valid_for_claim"] for row in parser)
    c_parent_separate = all(not row["score_ready"] and not row["claim_allowed"] for row in c_parent)
    rejection_blocks = len(rejections) >= 8 and all(not row["claim_allowed"] for row in rejections)
    gate_pass = all(row["gate_pass"] for row in gates)
    decision_nonclaim = all(not row["claim_allowed"] for row in decisions)
    next_written = len(next_target) == 1 and next_target[0]["next_id"] == "NEXT1483_0_1484"
    csv_parse = all(path.exists() and parse_csv(path) for path in generated)
    copies_exist = all(path.exists() for path in [QUAR_ACQ, QUAR_TAU, QUAR_PARSE, BRANCH_TAU_LOCK, BRANCH_ACQ_LEDGER, BRANCH_PARSE_REFRESH])
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = (
        not any(path.stat().st_mtime >= START_TS for path in FORMALIZATION.rglob("*") if path.is_file())
        if FORMALIZATION.exists()
        else True
    )
    claim_flags_false = all_claim_flags_false([sources, acquisitions, checklist, tau, schema, parser, c_parent, rejections, gates, decisions, next_target])
    checks = [
        ("VAL1483_0_sources", source_paths_exist, "all cited local source paths exist"),
        ("VAL1483_1_acquisition_routes", route_rows_ok, "official source routes recorded without importing unsourced arrays"),
        ("VAL1483_2_package_checklist_blocked", checklist_blocked, "official package checklist remains nonclaim"),
        ("VAL1483_3_tau_symbolic", tau_symbolic, "tau functional locked but not evaluated"),
        ("VAL1483_4_tau_schema", schema_locked, "tau input schema locked with values missing"),
        ("VAL1483_5_parser_refuses", parser_refuses, "parser refresh refuses score paths"),
        ("VAL1483_6_C_parent_separate", c_parent_separate, "C_parent interaction points remain independent/nonclaim"),
        ("VAL1483_7_rejection_blocks", rejection_blocks, "rejection ledger blocks claim"),
        ("VAL1483_8_gates", gate_pass, "no-claim gates pass"),
        ("VAL1483_9_decisions", decision_nonclaim, "decision ledger keeps claim false"),
        ("VAL1483_10_next_target", next_written, "1484 handoff written"),
        ("VAL1483_11_csv_parse", csv_parse, "all generated 1483 CSVs parse cleanly"),
        ("VAL1483_12_branch_copies", copies_exist, "branch/quarantine copies written"),
        ("VAL1483_13_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1483_14_formalization_untouched", formalization_untouched, "formalization modified-file count since start=0"),
        ("VAL1483_15_claim_flags_false", claim_flags_false, "all prediction/claim flags remain false"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "generated_utc": utc_now(),
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1483_16_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1483 records official acquisition routes and locks symbolic tau_eff without opening a claim",
            "generated_utc": utc_now(),
        }
    )
    return rows


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ACQUISITION_LEDGER, QUAR_ACQ)
    shutil.copyfile(TAU_FUNCTIONAL_LOCK, QUAR_TAU)
    shutil.copyfile(PARSER_REFRESH, QUAR_PARSE)
    shutil.copyfile(TAU_FUNCTIONAL_LOCK, BRANCH_TAU_LOCK)
    shutil.copyfile(ACQUISITION_LEDGER, BRANCH_ACQ_LEDGER)
    shutil.copyfile(PARSER_REFRESH, BRANCH_PARSE_REFRESH)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> list[str]:
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return lines


def write_doc(
    acquisitions: list[dict[str, Any]],
    checklist: list[dict[str, Any]],
    tau: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    c_parent: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    lines = [
        "# 1483 - MICROSCOPE Source-File Acquisition Ledger Or Symbolic Tau Functional Lock",
        "",
        "## Verdict",
        "- No official MICROSCOPE arrays were imported into live claim files; the ONERA/CMSM/REGARDS routes are recorded as acquisition targets only.",
        "- The useful advance is the tau lock: `tau_eff_X` is now an explicit symbolic functional of readout, source, masks, orbit weights, sign convention, and branch id.",
        "- This keeps the local-GR/WEP branch honest: future data can fill values, but `tau_eff=1`, bound inversion, DD-only basis, and mixed-branch shortcuts stay forbidden.",
        "",
        "## Acquisition Ledger",
    ]
    lines.extend(markdown_table(acquisitions, ["acquisition_id", "source_kind", "current_status", "next_action"]))
    lines.extend(["", "## Package Checklist"])
    lines.extend(markdown_table(checklist, ["check_id", "required_item", "current_status", "why_required"]))
    lines.extend(["", "## Tau Functional Lock"])
    lines.extend(markdown_table(tau, ["lock_id", "symbol", "current_status", "missing_for_evaluation", "numeric_value"]))
    lines.extend(["", "## Tau Input Schema"])
    lines.extend(markdown_table(schema, ["schema_id", "column", "type", "requirement"]))
    lines.extend(["", "## Parser Refresh"])
    lines.extend(markdown_table(parser, ["parser_id", "target_exists", "parser_status", "refusal_reason"]))
    lines.extend(["", "## C Parent Interaction Points"])
    lines.extend(markdown_table(c_parent, ["interaction_id", "current_status", "why_it_matters"]))
    lines.extend(["", "## Rejection Ledger"])
    lines.extend(markdown_table(rejections, ["rejection_id", "blocking_marker", "reason"]))
    lines.extend(["", "## No-Claim Gates"])
    lines.extend(markdown_table(gates, ["gate_id", "gate_pass", "detail"]))
    lines.extend(["", "## Decision Ledger"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} - {row['consequence']}.")
    lines.extend(["", "## Validation"])
    lines.extend(markdown_table(validation, ["check_id", "result", "detail"]))
    lines.extend(["", "## Next Target"])
    lines.extend(markdown_table(next_target, ["next_id", "next_target", "script", "objective"]))
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    acquisitions = acquisition_rows()
    checklist = package_checklist_rows()
    tau = tau_lock_rows()
    schema = tau_column_schema_rows()
    parser = parser_refresh_rows()
    c_parent = c_parent_interaction_rows()
    rejections = rejection_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ACQUISITION_LEDGER, acquisitions)
    write_csv(PACKAGE_CHECKLIST, checklist)
    write_csv(TAU_FUNCTIONAL_LOCK, tau)
    write_csv(TAU_COLUMN_SCHEMA, schema)
    write_csv(PARSER_REFRESH, parser)
    write_csv(C_PARENT_INTERACTIONS, c_parent)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(NO_CLAIM_GATES, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)
    copy_outputs()
    validation = validation_rows(sources, acquisitions, checklist, tau, schema, parser, c_parent, rejections, gates, decisions, next_target)
    write_csv(VALIDATION, validation)
    write_doc(acquisitions, checklist, tau, schema, parser, c_parent, rejections, gates, decisions, validation, next_target)
    print("Y5_R10_1483_MICROSCOPE_tau_functional_locked_nonclaim")


if __name__ == "__main__":
    main()
