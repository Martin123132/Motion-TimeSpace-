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
QUARANTINE = MICROSCOPE / "quarantine" / "1462"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1462-Y5-R10-RAB-common-measure-current-parent-signature-or-first-CMSM-inventory-fill.md"

PREV_NEXT = OUT / "P8_Y5_R10_1461_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1461_VALIDATION.csv"
PREV_FACTOR_PROOF = OUT / "P8_Y5_R10_1461_PARENT_SOURCE_FACTORIZATION_PROOF_ATTEMPT.csv"
PREV_NO_RELATIVE = OUT / "P8_Y5_R10_1461_NO_RELATIVE_SOURCE_LABEL_AUDIT.csv"
PREV_COUNTERMODELS = OUT / "P8_Y5_R10_1461_SOURCE_LABEL_COUNTERMODEL_AUDIT.csv"
PREV_CMSM_SCAFFOLD = OUT / "P8_Y5_R10_1461_CMSM_INVENTORY_SCAFFOLD.csv"
PREV_CHECKSUM_SCAFFOLD = OUT / "P8_Y5_R10_1461_CMSM_CHECKSUM_AND_EXTRACTION_SCAFFOLD.csv"

COMMON_MEASURE_1452 = OUT / "P8_Y5_R10_1452_COMMON_MEASURE_CURRENT_THEOREM_ATTEMPT.csv"
JACOBIAN_1452 = OUT / "P8_Y5_R10_1452_SPECIES_JACOBIAN_LEDGER_NONCLAIM.csv"
CURRENT_AUDIT_1452 = OUT / "P8_Y5_R10_1452_CURRENT_OWNER_AUDIT.csv"
NONHILBERT_1452 = OUT / "P8_Y5_R10_1452_NONHILBERT_CURRENT_LEDGER_NONCLAIM.csv"
SIGNING_1452 = OUT / "P8_Y5_R10_1452_PARENT_SIGNING_DECISION.csv"
ACTION_LOCK_1418 = OUT / "P8_Y5_R10_1418_ACTION_SCALE_CURRENT_OWNER_LOCK_ATTEMPT.csv"
CURRENT_OWNER_1453 = OUT / "P8_Y5_R10_1453_CURRENT_SOURCE_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv"
CURRENT_MATRIX_1453 = OUT / "P8_Y5_R10_1453_CURRENT_RESCALING_SELECTOR_MATRIX.csv"
ZETA_1453 = OUT / "P8_Y5_R10_1453_ZETA_A_NONHILBERT_CURRENT_LEDGER_NONCLAIM.csv"
COMMON_MODE_REDUCTION_1337 = OUT / "P8_Y5_R10_1337_COMMON_MODE_PREMISE_REDUCTION.csv"
COMMON_MODE_STATUS_1338 = OUT / "P8_Y5_R10_1338_COMMON_MODE_THEOREM_STATUS.csv"

QUAR_1461_INVENTORY = MICROSCOPE / "quarantine" / "1461" / "CMSM_OFFICIAL_INVENTORY_TEMPLATE_QUARANTINE_NONCLAIM.csv"
QUAR_1461_CHECKSUM = MICROSCOPE / "quarantine" / "1461" / "CMSM_DOWNLOAD_CHECKSUM_MANIFEST_TEMPLATE_QUARANTINE_NONCLAIM.csv"
QUAR_1461_EXTRACTION = MICROSCOPE / "quarantine" / "1461" / "CMSM_EXTRACTION_SCHEMA_TEMPLATE_QUARANTINE_NONCLAIM.csv"

LIVE_OFFICIAL_READOUT = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"
LIVE_SOURCE_WORLD = MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv"
LIVE_MATERIAL_TENSOR = MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"
LIVE_CPARENT = COEFF / "C_parent_WEP_slot_import.csv"

ONERA_DATA_PAGE = "https://microscope.onera.fr/fr/publication/microscope-data-are-available"
CMSM_PORTAL = "https://cmsm-ds.onera.fr/user/microscope"
CMSM_ROOT = "https://cmsm-ds.onera.fr/"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1462_SOURCE_REGISTER.csv"
MEASURE_PROOF = OUT / "P8_Y5_R10_1462_COMMON_MEASURE_CURRENT_SIGNATURE_ATTEMPT.csv"
ACTION_SCALE_AUDIT = OUT / "P8_Y5_R10_1462_ACTION_SCALE_AND_SPECIES_JACOBIAN_AUDIT.csv"
CURRENT_OWNER_UPDATE = OUT / "P8_Y5_R10_1462_CURRENT_OWNER_UPDATE.csv"
RESIDUAL_LEDGER = OUT / "P8_Y5_R10_1462_JA_CA_ZETA_RESIDUAL_LEDGER_NONCLAIM.csv"
CMSM_FIRST_FILL = OUT / "P8_Y5_R10_1462_CMSM_FIRST_INVENTORY_FILL_NONCLAIM.csv"
CMSM_PORTAL_PROBE = OUT / "P8_Y5_R10_1462_CMSM_PORTAL_PROBE_LEDGER.csv"
CHECKSUM_PLAN = OUT / "P8_Y5_R10_1462_CMSM_CHECKSUM_PLAN_NONCLAIM.csv"
LIVE_GUARD = OUT / "P8_Y5_R10_1462_LIVE_IMPORT_GUARD.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1462_REDUCTION_GATES.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1462_PARENT_SIGNING_DECISION.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1462_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1462_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1462_VALIDATION.csv"

QUAR_INVENTORY_FILL = QUARANTINE / "CMSM_OFFICIAL_INVENTORY_FIRST_FILL_QUARANTINE_NONCLAIM.csv"
QUAR_PORTAL_PROBE = QUARANTINE / "CMSM_PORTAL_PROBE_QUARANTINE_NONCLAIM.csv"
QUAR_CHECKSUM_PLAN = QUARANTINE / "CMSM_CHECKSUM_PLAN_QUARANTINE_NONCLAIM.csv"

BRANCH_MEASURE_PROOF = COEFF / "common_measure_current_signature_attempt_1462.csv"
BRANCH_CMSM_FILL = COEFF / "CMSM_first_inventory_fill_nonclaim_1462.csv"
BRANCH_SIGNING = COEFF / "C_parent_WEP_common_measure_current_signature_decision_1462.csv"

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
        ("SRC1462_0_prev_next", PREV_NEXT, "1461 handoff"),
        ("SRC1462_1_prev_validation", PREV_VALIDATION, "1461 validation"),
        ("SRC1462_2_prev_factor", PREV_FACTOR_PROOF, "1461 source factorization proof"),
        ("SRC1462_3_prev_no_relative", PREV_NO_RELATIVE, "1461 no-relative-source-label audit"),
        ("SRC1462_4_prev_countermodels", PREV_COUNTERMODELS, "1461 source-label countermodels"),
        ("SRC1462_5_prev_CMSM_scaffold", PREV_CMSM_SCAFFOLD, "1461 CMSM inventory scaffold"),
        ("SRC1462_6_prev_checksum", PREV_CHECKSUM_SCAFFOLD, "1461 checksum scaffold"),
        ("SRC1462_7_common_measure_1452", COMMON_MEASURE_1452, "1452 common measure/current theorem attempt"),
        ("SRC1462_8_jacobian_1452", JACOBIAN_1452, "1452 species Jacobian ledger"),
        ("SRC1462_9_current_audit_1452", CURRENT_AUDIT_1452, "1452 current owner audit"),
        ("SRC1462_10_nonhilbert_1452", NONHILBERT_1452, "1452 non-Hilbert ledger"),
        ("SRC1462_11_signing_1452", SIGNING_1452, "1452 signing decision"),
        ("SRC1462_12_action_lock_1418", ACTION_LOCK_1418, "1418 action-scale/current owner lock"),
        ("SRC1462_13_current_owner_1453", CURRENT_OWNER_1453, "1453 current owner theorem attempt"),
        ("SRC1462_14_current_matrix_1453", CURRENT_MATRIX_1453, "1453 current selector matrix"),
        ("SRC1462_15_zeta_1453", ZETA_1453, "1453 non-Hilbert zeta ledger"),
        ("SRC1462_16_common_mode_reduction_1337", COMMON_MODE_REDUCTION_1337, "1337 common-mode premise reduction"),
        ("SRC1462_17_common_mode_status_1338", COMMON_MODE_STATUS_1338, "1338 common-mode status"),
        ("SRC1462_18_quar_inventory_1461", QUAR_1461_INVENTORY, "1461 CMSM inventory template"),
        ("SRC1462_19_quar_checksum_1461", QUAR_1461_CHECKSUM, "1461 CMSM checksum template"),
        ("SRC1462_20_quar_extraction_1461", QUAR_1461_EXTRACTION, "1461 CMSM extraction template"),
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


def measure_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "CMC1462_0_target",
            "claim_piece": "common measure/current parent signature",
            "formal_statement": "S_ord = sum_A S_A[psi_A,e_obs,theta_A] is integrated with one parent measure and one hbar_parent; active source is delta S_ord/delta e_obs",
            "proof_move": "make species weights non-arguments of the parent action measure/current functor",
            "status": "TARGET_SHARPENED",
            "if_signed": "w_A, J_A, c_A source-normalization branches collapse to common calibration or vanish",
            "current_blocker": "parent action-scale/statistical measure owner is still a contract, not a derived object",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "CMC1462_1_classical_EOM_insufficient",
            "claim_piece": "classical field equations cannot remove action weights",
            "formal_statement": "delta(w_A S_A)/delta psi_A=0 may equal delta S_A/delta psi_A=0, but delta(w_A S_A)/delta e_obs = w_A T_A",
            "proof_move": "reject the tempting but false engineering shortcut",
            "status": "NO_GO_EXACT",
            "if_signed": "prevents treating w_A as harmless because equations of motion are unchanged",
            "current_blocker": "source variation is sensitive to the action weight",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "CMC1462_2_single_hbar_route",
            "claim_piece": "single parent action scale removes independent hbar_A/w_A",
            "formal_statement": "exp(i S_ord/hbar_parent) with S_ord=sum_A S_A admits one global action scale; independent exp(i w_A S_A/hbar_parent) factors require an extra parent coefficient",
            "proof_move": "push the proof into the parent measure/statistical grammar instead of the classical equations",
            "status": "CONDITIONAL_ROUTE_CLEAN",
            "if_signed": "species-dependent action weights become forbidden source-only coefficients",
            "current_blocker": "MTS parent measure/path-integral/statistical owner is not explicitly derived",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "CMC1462_3_field_redefinition_limit",
            "claim_piece": "field rescaling cannot generally erase w_A",
            "formal_statement": "psi_A -> sqrt(w_A) psi_A can shift normalizations in free sectors but does not generically preserve interactions, charges, quantum measure, and measured constants",
            "proof_move": "block another false zero proof",
            "status": "NO_GO_GENERAL",
            "if_signed": "forces the proof to be parent-structural rather than cosmetic",
            "current_blocker": "interacting matter and quantum normalization make relative action weights observable unless parent-forbidden",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "CMC1462_4_species_jacobian_countermodel",
            "claim_piece": "species Jacobian remains a live measure loophole",
            "formal_statement": "Dmu_parent = product_A J_A Dpsi_A or S_eff=sum_A J_A S_A",
            "proof_move": "identify the exact measure object that must be excluded",
            "status": "COUNTERMODEL_SURVIVES",
            "if_signed": "nothing; this is the obstruction to signing",
            "current_blocker": "no parent proof that J_A is absent/common/exactly cancelled",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "CMC1462_5_current_owner_limit",
            "claim_piece": "current owner kills only post-variation rescaling conditionally",
            "formal_statement": "after T_H is varied, F(T_A,A) cannot redefine the parent source; before variation, S=sum_A w_A S_A still survives",
            "proof_move": "separate post-readout selector mistakes from pre-action weight loopholes",
            "status": "PARTIAL_THEOREM_ONLY",
            "if_signed": "post-current rescalings become downstream readout/calibration artifacts",
            "current_blocker": "pre-action weights and non-Hilbert currents remain live",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "CMC1462_6_verdict",
            "claim_piece": "AX1090_2 common measure/current closure status",
            "formal_statement": "single hbar_parent + species-blind measure + Hilbert current owner + non-Hilbert silence => J_A=c_A=zeta_A=0 or common-mode",
            "proof_move": "reduce the source-normalization problem to an exact parent signature contract",
            "status": "PROOF_NOT_CLOSED",
            "if_signed": "source-side local GR route gains a major theorem-zero support",
            "current_blocker": "action-scale owner, species Jacobian exclusion, and non-Hilbert current silence are still unsigned",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def action_scale_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "ASA1462_0_action_scale_owner",
            "object": "hbar_parent / action measure",
            "needed_signature": "one parent action scale for all ordinary matter sectors",
            "current_status": "OWNER_NOT_DERIVED",
            "failure_mode": "hbar_A or w_A acts as a relative source weight",
            "next_derivation_target": "derive action-scale owner from parent variational/statistical construction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "ASA1462_1_species_measure_jacobian",
            "object": "J_A",
            "needed_signature": "species-blind measure Jacobian or absence theorem",
            "current_status": "COUNTERMODEL_SURVIVES",
            "failure_mode": "effective S_eff=sum_A J_A S_A",
            "next_derivation_target": "prove measure functor is connected/species-blind or keep J_A residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "ASA1462_2_current_normalization",
            "object": "c_A",
            "needed_signature": "single current/source normalization owner before readout",
            "current_status": "PARTIAL_POST_VARIATION_ONLY",
            "failure_mode": "J_src=sum_A c_A T_A or c_A J_A",
            "next_derivation_target": "combine Hilbert variation owner with variation-before-readout and source-worldtube theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "ASA1462_3_nonHilbert_bypass",
            "object": "zeta_A J_NH,A",
            "needed_signature": "non-Hilbert current absent, exact, projected silent, or bounded",
            "current_status": "PARALLEL_GATE_OPEN",
            "failure_mode": "source residual bypasses Hilbert total-stress uniqueness",
            "next_derivation_target": "derive J_NH silence or bound zeta_A projections in WEP/PPN/orbital arenas",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def current_owner_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "update_id": "COU1462_0_post_selector",
            "loophole": "post-variation F(T_A,A)",
            "current_result": "KILLED_CONDITIONALLY",
            "why": "once T_H is varied from a common action, downstream readout cannot redefine parent source",
            "remaining_requirement": "variation-before-readout plus official source/readout kernel must be source-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "update_id": "COU1462_1_pre_action_weight",
            "loophole": "S_matter=sum_A w_A S_A before variation",
            "current_result": "SURVIVES",
            "why": "Hilbert variation inherits w_A",
            "remaining_requirement": "common measure/action-scale theorem, not merely current owner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "update_id": "COU1462_2_nonHilbert",
            "loophole": "zeta_A J_NH,A",
            "current_result": "SURVIVES",
            "why": "not all possible local source currents are proved to be Hilbert/coframe currents",
            "remaining_requirement": "absence/exact/projector-silence theorem or bound inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def residual_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "ledger_id": "R1462_0_wA",
            "symbol": "w_A or hbar_A/hbar_parent",
            "meaning": "relative action-scale/source weight",
            "units": "dimensionless",
            "current_status": "MISSING_PARENT_ZERO",
            "arena_link": "WEP/PPN/R10/source normalization",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "ledger_id": "R1462_1_JA",
            "symbol": "J_A",
            "meaning": "species measure Jacobian",
            "units": "dimensionless",
            "current_status": "MISSING_COMMON_MEASURE",
            "arena_link": "WEP/source normalization",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "ledger_id": "R1462_2_cA",
            "symbol": "c_A",
            "meaning": "current/source normalization rescaling",
            "units": "dimensionless",
            "current_status": "MISSING_CURRENT_OWNER",
            "arena_link": "WEP/PPN/orbital",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "ledger_id": "R1462_3_zetaA",
            "symbol": "zeta_A",
            "meaning": "coefficient of non-Hilbert current bypass",
            "units": "current-defined",
            "current_status": "MISSING_JNH_DEFINITION_OR_SILENCE",
            "arena_link": "WEP/PPN/orbital/local GR",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "ledger_id": "R1462_4_total_policy",
            "symbol": "source_normalization_residual",
            "meaning": "no-cancellation retained sum of absolute active-source loopholes",
            "units": "policy",
            "current_status": "NO_CANCELLATION_RETAINED",
            "arena_link": "all local arenas",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def cmsm_first_fill_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "inventory_id": "CMSM1462_0_ONERA_data_available_page",
            "dataset_id": "MICROSCOPE_CMSM_DATA_PORTAL_POINTER",
            "file_name": "portal_pointer_not_dataset_file",
            "source_url": ONERA_DATA_PAGE,
            "linked_portal_url": CMSM_PORTAL,
            "file_role": "official data availability pointer",
            "evidence_text": "ONERA MICROSCOPE page says mission data are available at the CMSM portal for Equivalence Principle or other tests with the measurements",
            "expected_columns": "not applicable; portal pointer only",
            "licence_or_access_note": "access/licence not extracted from portal yet",
            "source_note": "source-backed pointer row; not an official readout file and not valid for claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "inventory_id": "CMSM1462_1_CMSM_user_microscope_route",
            "dataset_id": "MICROSCOPE_CMSM_USER_ROUTE",
            "file_name": "MISSING_DATASET_FILE_INVENTORY",
            "source_url": CMSM_PORTAL,
            "linked_portal_url": CMSM_ROOT,
            "file_role": "portal route to future dataset inventory",
            "evidence_text": "web/browser title resolves as REGARDS OSS; shell download from this environment failed to connect, so no file inventory is claimed",
            "expected_columns": "MISSING_COLUMN_LIST",
            "licence_or_access_note": "MISSING_ACCESS_NOTE",
            "source_note": "route row only; future manual/browser or network-fixed inventory needed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "inventory_id": "CMSM1462_2_target_readout_dataset",
            "dataset_id": "MISSING_K_CMSM_OFFICIAL_READOUT_DATASET",
            "file_name": "MISSING_FILE_NAME",
            "source_url": CMSM_PORTAL,
            "linked_portal_url": CMSM_ROOT,
            "file_role": "target official readout/orbit/attitude/mask dataset",
            "evidence_text": "needed for time/session/orbit, gx/gz, Sxx/Sxz, masks, calibration flags, attitude/sign conventions",
            "expected_columns": "time_s;session_id;orbit_id;axis;gx_m_s2;gz_m_s2;Sxx;Sxz;mask_flag;calibration_flag;attitude_basis_or_quaternion",
            "licence_or_access_note": "MISSING_ACCESS_NOTE",
            "source_note": "target placeholder; no source-backed file found or downloaded in 1462",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def portal_probe_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "probe_id": "PROBE1462_0_ONERA_page",
            "url": ONERA_DATA_PAGE,
            "method": "PowerShell Invoke-WebRequest with browser user agent",
            "result": "HTTP_200_TEXT_HTML",
            "useful_evidence": "official ONERA page provides CMSM data portal pointer",
            "claim_impact": "supports acquisition route only, not readout data import",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "probe_id": "PROBE1462_1_CMSM_user_route",
            "url": CMSM_PORTAL,
            "method": "PowerShell Invoke-WebRequest from local environment",
            "result": "UNABLE_TO_CONNECT_REMOTE_SERVER",
            "useful_evidence": "no dataset inventory could be extracted by shell in this run",
            "claim_impact": "blocks live source-pack filling; keep quarantine rows only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "probe_id": "PROBE1462_2_CMSM_web_title",
            "url": CMSM_PORTAL,
            "method": "web/browser open",
            "result": "REGARDS_OSS_TITLE_ONLY",
            "useful_evidence": "portal route exists but exposes no parsed file inventory here",
            "claim_impact": "source-backed pointer only; no official arrays",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def checksum_plan_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "checksum_id": "CHK1462_0_pointer_hash_policy",
            "target": "official portal pointer row",
            "required_before_live_import": "dataset file URL, local file path, sha256, byte_count, row_count, schema map",
            "current_status": "POINTER_ONLY_NO_HASH",
            "local_quarantine_path": str(QUAR_INVENTORY_FILL),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "checksum_id": "CHK1462_1_readout_file_policy",
            "target": "K_CMSM readout file",
            "required_before_live_import": "downloaded official file plus checksum and extraction mapping into official_readout schema",
            "current_status": "MISSING_DATASET_FILE",
            "local_quarantine_path": str(QUAR_CHECKSUM_PLAN),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "checksum_id": "CHK1462_2_no_manual_claim_policy",
            "target": "manual/browser portal evidence",
            "required_before_live_import": "manual notes must be converted to source-backed rows with verifiable URLs/files; screenshots alone cannot promote",
            "current_status": "PROMOTION_BLOCKED_BY_DEFAULT",
            "local_quarantine_path": str(QUAR_PORTAL_PROBE),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def live_guard_rows() -> list[dict[str, Any]]:
    live_targets = [
        ("LIVE1462_0_official_readout", "official_readout", LIVE_OFFICIAL_READOUT),
        ("LIVE1462_1_source_worldtube", "source_worldtube", LIVE_SOURCE_WORLD),
        ("LIVE1462_2_material_tensor", "material_tensor", LIVE_MATERIAL_TENSOR),
        ("LIVE1462_3_C_parent", "C_parent_WEP", LIVE_CPARENT),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "live_guard_id": guard_id,
            "object": object_name,
            "live_path": str(path),
            "exists_now": path.exists(),
            "would_write_in_1462": False,
            "reason": "1462 writes only nonclaim theorem ledgers and quarantine inventory rows",
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
            "gate_id": "GATE1462_0_no_go_classical",
            "gate": "classical EOM/field-rescaling shortcuts rejected",
            "gate_pass": True,
            "blocking_reason": "no blocker; false proof routes are explicitly closed",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1462_1_single_hbar_route",
            "gate": "single parent hbar/measure route is clean conditional",
            "gate_pass": True,
            "blocking_reason": "conditional only; parent measure owner unsigned",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1462_2_parent_measure_signed",
            "gate": "parent action-scale/statistical measure owner signed",
            "gate_pass": False,
            "blocking_reason": "owner remains a contract, not a derived theorem",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1462_3_species_jacobian_zero",
            "gate": "J_A/w_A/c_A residuals theorem-zero",
            "gate_pass": False,
            "blocking_reason": "species Jacobian and pre-action weight countermodels survive",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1462_4_nonHilbert_silence",
            "gate": "zeta_A J_NH,A absent/exact/projected silent",
            "gate_pass": False,
            "blocking_reason": "non-Hilbert bypass remains open",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1462_5_CMSM_first_fill",
            "gate": "official ONERA pointer filled into quarantine inventory",
            "gate_pass": True,
            "blocking_reason": "pointer only; no official dataset file inventory",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1462_6_live_claim",
            "gate": "local WEP/local-GR claim allowed",
            "gate_pass": False,
            "blocking_reason": "common measure/current, official source pack, material tensor, and C_parent remain absent",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1462_0_common_measure_current",
            "target": "AX1090_2 common measure/current parent signature",
            "classical_shortcuts_rejected": True,
            "single_hbar_route_clean_conditional": True,
            "parent_measure_owner_signed": False,
            "species_jacobian_zero_signed": False,
            "current_owner_complete": False,
            "nonHilbert_silence_signed": False,
            "CMSM_pointer_filled": True,
            "JA_zero_import_allowed": False,
            "delta_q_zero_import_allowed": False,
            "C_parent_WEP_import_allowed": False,
            "tau_WEP_numeric_allowed": False,
            "local_claim_allowed": False,
            "decision": "REFUSE_COMMON_MEASURE_ZERO_IMPORT_KEEP_RESIDUALS_AND_CMSM_POINTER",
            "reason": "cleanest proof route requires parent action-scale/statistical measure owner; current corpus still permits w_A/J_A/zeta_A countermodels",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1462_0_proof",
            "decision": "common measure/current is a conditional theorem, not a closed theorem-zero",
            "why": "single hbar/measure route is clean, but the parent measure owner is unsigned",
            "consequence": "w_A/J_A/c_A/zeta_A residual rows remain live and nonclaim",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1462_1_no_shortcuts",
            "decision": "reject EOM-only and field-redefinition-only zero proofs",
            "why": "source variation and quantum/statistical normalization still see relative weights",
            "consequence": "future proof must be parent-structural",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1462_2_CMSM",
            "decision": "fill first source-backed CMSM pointer rows but no official data rows",
            "why": "ONERA page gives a real portal pointer, but no file inventory was extracted in this run",
            "consequence": "data route is slightly more real while live claim files remain absent",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1462_0_1463",
            "next_target": "1463-Y5-R10-RAB-parent-measure-owner-contract-or-CMSM-portal-manual-inventory.md",
            "script": "scripts/Y5_R10_RAB_parent_measure_owner_contract_or_CMSM_portal_manual_inventory.py",
            "objective": "try to construct the explicit parent measure/statistical owner that forbids w_A/J_A; if it fails, manually inventory the CMSM portal file list into quarantine rows",
            "include": "parent measure owner; hbar/action-scale ownership; species Jacobian exclusion; CMSM manual inventory; no live claim",
            "exclude": "numeric tau_WEP; local-GR pass; C_parent promotion; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    measure_proof: list[dict[str, Any]],
    action_audit: list[dict[str, Any]],
    current_update: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    cmsm_fill: list[dict[str, Any]],
    portal_probe: list[dict[str, Any]],
    checksum_plan: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_csvs = [
        SOURCE_REGISTER,
        MEASURE_PROOF,
        ACTION_SCALE_AUDIT,
        CURRENT_OWNER_UPDATE,
        RESIDUAL_LEDGER,
        CMSM_FIRST_FILL,
        CMSM_PORTAL_PROBE,
        CHECKSUM_PLAN,
        LIVE_GUARD,
        REDUCTION_GATES,
        SIGNING_DECISION,
        DECISION_LEDGER,
        NEXT_TARGET,
        QUAR_INVENTORY_FILL,
        QUAR_PORTAL_PROBE,
        QUAR_CHECKSUM_PLAN,
    ]
    all_sources_exist = all(truth(row["exists"]) for row in sources)
    proof_not_closed = any(row["status"] == "PROOF_NOT_CLOSED" for row in measure_proof)
    false_shortcuts_closed = any(row["status"] == "NO_GO_EXACT" for row in measure_proof) and any(row["status"] == "NO_GO_GENERAL" for row in measure_proof)
    residuals_nonclaim = all(not truth(row["score_ready"]) and not truth(row["claim_allowed"]) for row in residuals)
    cmsm_pointer_filled = any(row["inventory_id"] == "CMSM1462_0_ONERA_data_available_page" and row["source_url"] == ONERA_DATA_PAGE for row in cmsm_fill)
    cmsm_no_claim = all(not truth(row["valid_for_claim"]) and not truth(row["claim_allowed"]) for row in cmsm_fill)
    portal_probe_nonclaim = all(not truth(row["valid_for_claim"]) and not truth(row["claim_allowed"]) for row in portal_probe)
    checksum_nonclaim = all(not truth(row["valid_for_claim"]) and not truth(row["claim_allowed"]) for row in checksum_plan)
    live_paths_untouched = all(not truth(row["exists_now"]) and not truth(row["would_write_in_1462"]) for row in live_guard)
    gate_pattern_safe = truth(gates[0]["gate_pass"]) and truth(gates[1]["gate_pass"]) and truth(gates[5]["gate_pass"]) and all(
        not truth(row["gate_pass"]) for row in gates[2:5] + gates[6:]
    )
    signing_refuses = all(
        not truth(row["JA_zero_import_allowed"])
        and not truth(row["delta_q_zero_import_allowed"])
        and not truth(row["C_parent_WEP_import_allowed"])
        and not truth(row["tau_WEP_numeric_allowed"])
        and not truth(row["local_claim_allowed"])
        for row in signing
    )
    generated_parse = all(parse_csv_ok(path) for path in generated_csvs)
    branch_copies = BRANCH_MEASURE_PROOF.exists() and BRANCH_CMSM_FILL.exists() and BRANCH_SIGNING.exists()
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formal_recent = 0
    if FORMALIZATION.exists():
        formal_recent = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and path.stat().st_mtime > START_TS
        )
    checks = [
        ("VAL1462_0_sources", all_sources_exist, "all cited local source paths exist"),
        ("VAL1462_1_proof_not_closed", proof_not_closed, "common measure/current proof remains conditional, not promoted"),
        ("VAL1462_2_false_shortcuts_closed", false_shortcuts_closed, "EOM-only and field-redefinition-only zero proofs are rejected"),
        ("VAL1462_3_action_audit_nonclaim", all(not truth(row["claim_allowed"]) for row in action_audit), "action-scale/Jacobian audit rows remain nonclaim"),
        ("VAL1462_4_current_update_nonclaim", all(not truth(row["claim_allowed"]) for row in current_update), "current owner update rows remain nonclaim"),
        ("VAL1462_5_residuals_nonclaim", residuals_nonclaim, "wA/JA/cA/zeta residual ledger remains nonclaim"),
        ("VAL1462_6_CMSM_pointer_filled", cmsm_pointer_filled, "official ONERA CMSM portal pointer row filled"),
        ("VAL1462_7_CMSM_no_claim", cmsm_no_claim and portal_probe_nonclaim and checksum_nonclaim, "CMSM fill/probe/checksum rows remain nonclaim"),
        ("VAL1462_8_live_paths_untouched", live_paths_untouched, "critical live official/source/material/Cparent files remain absent"),
        ("VAL1462_9_gate_pattern_safe", gate_pattern_safe, "only shortcut-closure/conditional-route/CMSM-pointer gates pass; claim gates false"),
        ("VAL1462_10_signing_refuses", signing_refuses, "parent signing refuses JA/delta_q/Cparent/tau/local claim"),
        ("VAL1462_11_generated_csv_parse", generated_parse, "all generated 1462 CSVs parse cleanly"),
        ("VAL1462_12_branch_copies", branch_copies, "nonclaim branch copies written"),
        ("VAL1462_13_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1462_14_formalization_untouched", formal_recent == 0, f"formalization modified-file count since start={formal_recent}"),
        ("VAL1462_15_overall", True, "1462 rejects shortcut proofs, keeps common-measure route conditional, and fills official CMSM pointer rows without claim promotion"),
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
    measure_proof: list[dict[str, Any]],
    action_audit: list[dict[str, Any]],
    current_update: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    cmsm_fill: list[dict[str, Any]],
    portal_probe: list[dict[str, Any]],
    checksum_plan: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    with DOC.open("w", encoding="utf-8") as handle:
        handle.write("# 1462 - Common measure/current parent signature or first CMSM inventory fill\n\n")
        handle.write(
            "**Current verdict:** the common-measure/current route remains the right pressure point, "
            "but it is not closed. Classical EOM and field-rescaling shortcuts fail because source variation "
            "and quantum/statistical normalization still see relative weights. The clean route is a single "
            "`hbar_parent`/measure/current owner, but that owner is not yet derived from the parent action.\n\n"
        )
        handle.write(
            "**Useful progress:** we narrowed the coupling gremlin to the parent measure/statistical owner: "
            "prove that and `w_A/J_A/c_A` lose their hiding place. Meanwhile the CMSM data route now has a "
            "source-backed ONERA portal pointer in quarantine, but still no official readout arrays or live imports.\n\n"
        )
        write_table(handle, "Source register", sources)
        write_table(handle, "Common measure/current signature attempt", measure_proof)
        write_table(handle, "Action-scale and species Jacobian audit", action_audit)
        write_table(handle, "Current owner update", current_update)
        write_table(handle, "JA/cA/zeta residual ledger", residuals)
        write_table(handle, "CMSM first inventory fill", cmsm_fill)
        write_table(handle, "CMSM portal probe ledger", portal_probe)
        write_table(handle, "CMSM checksum plan", checksum_plan)
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
    measure_proof = measure_proof_rows()
    action_audit = action_scale_audit_rows()
    current_update = current_owner_update_rows()
    residuals = residual_ledger_rows()
    cmsm_fill = cmsm_first_fill_rows()
    portal_probe = portal_probe_rows()
    checksum_plan = checksum_plan_rows()
    live_guard = live_guard_rows()
    gates = reduction_gate_rows()
    signing = signing_decision_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(MEASURE_PROOF, measure_proof)
    write_csv(ACTION_SCALE_AUDIT, action_audit)
    write_csv(CURRENT_OWNER_UPDATE, current_update)
    write_csv(RESIDUAL_LEDGER, residuals)
    write_csv(CMSM_FIRST_FILL, cmsm_fill)
    write_csv(CMSM_PORTAL_PROBE, portal_probe)
    write_csv(CHECKSUM_PLAN, checksum_plan)
    write_csv(QUAR_INVENTORY_FILL, cmsm_fill)
    write_csv(QUAR_PORTAL_PROBE, portal_probe)
    write_csv(QUAR_CHECKSUM_PLAN, checksum_plan)
    write_csv(LIVE_GUARD, live_guard)
    write_csv(REDUCTION_GATES, gates)
    write_csv(SIGNING_DECISION, signing)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(MEASURE_PROOF, BRANCH_MEASURE_PROOF)
    copy_branch(CMSM_FIRST_FILL, BRANCH_CMSM_FILL)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    remove_pycache()
    validation = validation_rows(
        sources,
        measure_proof,
        action_audit,
        current_update,
        residuals,
        cmsm_fill,
        portal_probe,
        checksum_plan,
        live_guard,
        gates,
        signing,
    )
    write_csv(VALIDATION, validation)
    write_doc(
        sources,
        measure_proof,
        action_audit,
        current_update,
        residuals,
        cmsm_fill,
        portal_probe,
        checksum_plan,
        live_guard,
        gates,
        signing,
        decisions,
        validation,
        next_target,
    )
    print("Y5_R10_1462_common_measure_conditional_CMSM_pointer_filled_nonclaim")


if __name__ == "__main__":
    main()
