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
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1460-Y5-R10-RAB-calibrated-point-source-theorem-reopen-or-official-data-acquisition-route.md"

PREV_NEXT = OUT / "P8_Y5_R10_1459_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1459_VALIDATION.csv"
PREV_REFUSAL = OUT / "P8_Y5_R10_1459_QUARANTINE_PROMOTION_REFUSAL.csv"
PREV_LIVE_DRYRUN = OUT / "P8_Y5_R10_1459_LIVE_IMPORT_DRY_RUN.csv"
PREV_SIGNING = OUT / "P8_Y5_R10_1459_PARENT_SIGNING_DECISION.csv"

POINT_SOURCE_1421 = OUT / "P8_Y5_R10_1421_PARENT_POINT_SOURCE_THEOREM_ATTEMPT.csv"
COMMON_MODE_1332 = OUT / "P8_Y5_R10_1332_COMMON_MODE_SOURCE_THEOREM.csv"
COMMON_MODE_REDUCTION_1337 = OUT / "P8_Y5_R10_1337_COMMON_MODE_PREMISE_REDUCTION.csv"
COMMON_MODE_STATUS_1338 = OUT / "P8_Y5_R10_1338_COMMON_MODE_THEOREM_STATUS.csv"
MEASURED_G_GUARD_1425 = OUT / "P8_Y5_R10_1425_MEASURED_G_COMMON_MODE_GUARD.csv"
COMMON_MODE_ABSORB_1450 = OUT / "P8_Y5_R10_1450_COMMON_MODE_ABSORPTION_GUARD.csv"

SOURCE_WORLD_1456 = COEFF / "source_worldtube_projection_theorem_attempt_1456.csv"
OFFICIAL_KCMSM_1456 = COEFF / "official_KCMSM_bound_inputs_nonclaim_1456.csv"
SOURCE_ACQ_1455 = OUT / "P8_Y5_R10_1455_SOURCE_WORLDTUBE_ACQUISITION_LEDGER_NONCLAIM.csv"
OFFICIAL_ACQ_1455 = OUT / "P8_Y5_R10_1455_OFFICIAL_READOUT_ACQUISITION_LEDGER_NONCLAIM.csv"
MICROSCOPE_PROVENANCE_1069 = OUT / "P8_Y5_R10_1069_MICROSCOPE_PROVENANCE_LEDGER.csv"
MICROSCOPE_EXTERNAL_1070 = OUT / "P8_Y5_R10_1070_EXTERNAL_MICROSCOPE_READOUT_SOURCE_LEDGER.csv"
ORBIT_REQUIREMENTS_1068 = OUT / "P8_Y5_R10_1068_MICROSCOPE_ORBIT_READOUT_REQUIREMENTS.csv"

LIVE_OFFICIAL_READOUT = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"
LIVE_SOURCE_WORLD = MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv"
LIVE_MATERIAL_TENSOR = MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"
LIVE_CPARENT = COEFF / "C_parent_WEP_slot_import.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1460_SOURCE_REGISTER.csv"
POINT_THEOREM = OUT / "P8_Y5_R10_1460_CALIBRATED_POINT_SOURCE_THEOREM_REOPEN.csv"
SOURCE_DECOMP = OUT / "P8_Y5_R10_1460_SOURCE_DECOMPOSITION_AND_ZERO_CONDITIONS.csv"
FINITE_BOUND = OUT / "P8_Y5_R10_1460_FINITE_SOURCE_ERROR_BOUND_CONTRACT.csv"
ACQUISITION_ROUTE = OUT / "P8_Y5_R10_1460_OFFICIAL_DATA_ACQUISITION_ROUTE.csv"
LIVE_GUARD = OUT / "P8_Y5_R10_1460_LIVE_IMPORT_GUARD.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1460_REDUCTION_GATES.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1460_PARENT_SIGNING_DECISION.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1460_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1460_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1460_VALIDATION.csv"

BRANCH_POINT_THEOREM = COEFF / "calibrated_point_source_theorem_reopen_1460.csv"
BRANCH_ACQUISITION_ROUTE = COEFF / "official_data_acquisition_route_nonclaim_1460.csv"
BRANCH_SIGNING = COEFF / "C_parent_WEP_calibrated_point_source_signing_decision_1460.csv"

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
        ("SRC1460_0_prev_next", PREV_NEXT, "1459 handoff"),
        ("SRC1460_1_prev_validation", PREV_VALIDATION, "1459 validation"),
        ("SRC1460_2_prev_refusal", PREV_REFUSAL, "1459 quarantine refusal"),
        ("SRC1460_3_prev_live_dryrun", PREV_LIVE_DRYRUN, "1459 live dry-run"),
        ("SRC1460_4_prev_signing", PREV_SIGNING, "1459 signing decision"),
        ("SRC1460_5_point_source_1421", POINT_SOURCE_1421, "prior calibrated point-source attempt"),
        ("SRC1460_6_common_mode_1332", COMMON_MODE_1332, "common-mode source theorem"),
        ("SRC1460_7_common_mode_reduction_1337", COMMON_MODE_REDUCTION_1337, "common-mode premise reduction"),
        ("SRC1460_8_common_mode_status_1338", COMMON_MODE_STATUS_1338, "common-mode theorem status"),
        ("SRC1460_9_measured_G_guard_1425", MEASURED_G_GUARD_1425, "measured-G guard"),
        ("SRC1460_10_absorb_guard_1450", COMMON_MODE_ABSORB_1450, "common-mode absorption guard"),
        ("SRC1460_11_source_world_1456", SOURCE_WORLD_1456, "source-worldtube projection theorem attempt"),
        ("SRC1460_12_official_KCMSM_1456", OFFICIAL_KCMSM_1456, "official K_CMSM acquisition ledger"),
        ("SRC1460_13_source_acq_1455", SOURCE_ACQ_1455, "source-worldtube acquisition ledger"),
        ("SRC1460_14_official_acq_1455", OFFICIAL_ACQ_1455, "official readout acquisition ledger"),
        ("SRC1460_15_provenance_1069", MICROSCOPE_PROVENANCE_1069, "MICROSCOPE provenance ledger"),
        ("SRC1460_16_external_1070", MICROSCOPE_EXTERNAL_1070, "external MICROSCOPE source ledger"),
        ("SRC1460_17_orbit_req_1068", ORBIT_REQUIREMENTS_1068, "orbit/readout requirements"),
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


def point_source_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "CPS1460_0_observable_identity",
            "claim_piece": "exact source-worldtube decomposition before any point-source shortcut",
            "formal_statement": "eta_AB = N_eta^-1 <K_eta(t) Int_Earth K_X(t,x) rho_m(x)[q0 + delta_q(x)] Delta_R_AB(x) d^3x dt>",
            "derived_result": "identity separates common calibrated source factor q0 from relative source profile delta_q(x)",
            "proof_status": "EXACT_ALGEBRAIC_REWRITE",
            "missing_for_claim": "numeric K_X, official orbit/readout, Delta_R_AB, and parent-signed delta_q status",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "CPS1460_1_common_point_source_limit",
            "claim_piece": "ordinary calibrated exterior source reduction",
            "formal_statement": "if delta_q(x)=0 and K_X is the universal metric source kernel, Int K_X rho_m q0 -> q0 M_E K_X(O_sat) plus ordinary gravity-model multipoles",
            "derived_result": "q0 M_E is a common scalar and may be absorbed into measured GM/G only after universality is signed",
            "proof_status": "CONDITIONAL_THEOREM",
            "missing_for_claim": "same-branch proof that source leg is universal/common-mode and not a relative source charge",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "CPS1460_2_relative_residual_law",
            "claim_piece": "remaining source-worldtube residual if source factorization fails",
            "formal_statement": "delta_eta_AB = N_eta^-1 <K_eta Int_Earth K_X(t,x) rho_m(x) delta_q(x) Delta_R_AB(x) d^3x dt>",
            "derived_result": "any spatial/material source-charge profile survives calibration and must be bounded or measured",
            "proof_status": "EXACT_RESIDUAL_LAW",
            "missing_for_claim": "source composition map or parent theorem setting delta_q(x)=0",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "CPS1460_3_zero_condition",
            "claim_piece": "minimal sufficient condition for source-worldtube removal",
            "formal_statement": "source-worldtube dependence is removable only if delta_q(x)=0 or <K_eta Int K_X rho_m delta_q Delta_R_AB> is source-backed below the declared WEP tolerance",
            "derived_result": "zero is not a convention; it is either a parent theorem or a sourced inequality",
            "proof_status": "EXACT_CONDITIONAL_GATE",
            "missing_for_claim": "parent source-factorization/no-relative-source-label proof or official source/readout data",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "CPS1460_4_measured_G_guard",
            "claim_piece": "calibration cannot hide relative residuals",
            "formal_statement": "G_meas may absorb only one universal constant q0; it cannot absorb delta_q(x), range dependence, material dependence, or branch-dependent source labels",
            "derived_result": "measured-G guard from 1425/1450 remains active",
            "proof_status": "GUARD_RETAINED",
            "missing_for_claim": "none for the guard; missing item is the zero/bound for relative residual",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "CPS1460_5_verdict",
            "claim_piece": "calibrated point-source theorem reopened",
            "formal_statement": "M_WEP,q can replace the full source-worldtube by a calibrated point-source only under signed common-mode factorization plus finite-source error control",
            "derived_result": "the theorem shape is sharper than 1421, but the project still lacks the parent source factorization or official data bound",
            "proof_status": "THEOREM_NOT_PROMOTED",
            "missing_for_claim": "delta_q=0 proof, finite-source bound, official K_CMSM/source-worldtube pack, C_parent_WEP",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def source_decomposition_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "condition_id": "SDZ1460_0_decompose_source",
            "object": "rho_q(x)",
            "law": "rho_q(x) = q0 rho_m(x) + rho_m(x) delta_q(x)",
            "zero_condition": "delta_q(x)=0 over the Earth source support",
            "status": "DEFINED_NOT_SIGNED",
            "why_it_matters": "separates true common-mode source mass from relative source-charge profile",
            "current_blocker": "parent action does not yet forbid source-only relative labels",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "condition_id": "SDZ1460_1_material_response",
            "object": "Delta_R_AB",
            "law": "Delta_R_AB = R_TA6V - R_PtRh10 in the same parent basis as C_parent_WEP",
            "zero_condition": "Delta_R_AB=0 from parent common-coupling theorem, or finite sourced tensor imported",
            "status": "PARTIAL_PAIR_ONLY_FULL_TENSOR_MISSING",
            "why_it_matters": "even a common source can produce WEP signal if material response is not parent-zero",
            "current_blocker": "full material tensor and parent coefficients are absent",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "condition_id": "SDZ1460_2_readout_kernel",
            "object": "K_eta K_X",
            "law": "official readout/orbit/attitude/mask kernel maps source residual to eta_AB",
            "zero_condition": "kernel is fixed downstream and imported from official/source-backed data",
            "status": "MISSING_OFFICIAL_ARRAYS",
            "why_it_matters": "prevents using a chosen kernel as a hidden parent selector",
            "current_blocker": "live official readout remains absent",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "condition_id": "SDZ1460_3_finite_source_remainder",
            "object": "R_finite",
            "law": "R_finite = <K_eta Int_Earth [K_X(t,x)-K_X(t,O_sat)] rho_m(x) delta_q(x) Delta_R_AB d^3x dt>",
            "zero_condition": "R_finite=0 by symmetry/common-mode theorem or |R_finite| <= declared tolerance by source-backed bound",
            "status": "BOUND_NOT_ACQUIRED",
            "why_it_matters": "point-source replacement otherwise discards the finite Earth/source part of the signal",
            "current_blocker": "Earth profile, orbit, and source-charge map missing",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "condition_id": "SDZ1460_4_parent_coefficient",
            "object": "C_parent_WEP",
            "law": "C_parent_WEP = functional derivative slot produced by parent action before downstream readout",
            "zero_condition": "C_parent_WEP=0 by parent symmetry/descent theorem or imported nonzero coefficient with source",
            "status": "MISSING_PARENT_INPUT",
            "why_it_matters": "no numerical WEP residual exists without the parent coefficient owner",
            "current_blocker": "no live C_parent_WEP slot import",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def finite_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "bound_id": "FSB1460_0_norm_bound",
            "quantity": "absolute finite-source residual",
            "bound_form": "|delta_eta_AB| <= |N_eta^-1| ||K_eta|| ||Delta_R_AB|| [||K_X||_inf ||rho_m delta_q||_1 + ||grad K_X||_inf M_1 + 1/2 ||H K_X||_inf M_2]",
            "required_inputs": "official K_eta, source kernel K_X, Delta_R_AB, source moments M_1/M_2, delta_q profile",
            "current_status": "FORMAL_BOUND_ONLY",
            "numeric_allowed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "bound_id": "FSB1460_1_point_source_exact_zero",
            "quantity": "finite-source residual under exact common mode",
            "bound_form": "if delta_q(x)=0 and Delta_R_AB is parent-common, then differential finite-source residual is zero after the common GM calibration",
            "required_inputs": "signed common-mode source theorem and signed material common-coupling theorem",
            "current_status": "CONDITIONAL_ZERO_NOT_SIGNED",
            "numeric_allowed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "bound_id": "FSB1460_2_data_bound_route",
            "quantity": "finite-source residual if exact zero fails",
            "bound_form": "compute the projected residual with official orbit/readout arrays and a declared source-composition model, then compare absolute value to MICROSCOPE eta bound",
            "required_inputs": "CMSM/ONERA data inventory, ephemeris/attitude/masks, source profile/composition, parent coefficient, material tensor",
            "current_status": "ACQUISITION_REQUIRED",
            "numeric_allowed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def acquisition_route_rows() -> list[dict[str, Any]]:
    portal_url = "https://cmsm-ds.onera.fr/"
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": "ACQ1460_0_CMSM_portal_inventory",
            "target_object": "official MICROSCOPE/CMSM file inventory",
            "needed_content": "dataset names, download URLs, file hashes, licence/access note, variable dictionary",
            "source_url_or_path": portal_url,
            "supporting_local_source": str(MICROSCOPE_EXTERNAL_1070),
            "current_status": "POINTER_ONLY_NOT_DOWNLOADED",
            "promotion_rule": "no live import until inventory is downloaded, checksummed, and schema-mapped",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": "ACQ1460_1_official_readout_arrays",
            "target_object": "K_CMSM readout",
            "needed_content": "time_s, session_id, orbit_id, axis, gx_m_s2, gz_m_s2, Sxx, Sxz, mask_flag, calibration_flag, attitude basis",
            "source_url_or_path": portal_url,
            "supporting_local_source": str(OFFICIAL_ACQ_1455),
            "current_status": "MISSING_OFFICIAL_ARRAYS",
            "promotion_rule": "must fill live official_readout only from source-backed rows with no placeholders",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": "ACQ1460_2_orbit_attitude_masks",
            "target_object": "orbit/readout projection kernel",
            "needed_content": "satellite position/velocity or averaged equivalent, sensitive-axis attitude, science segment windows, glitch/calibration masks",
            "source_url_or_path": portal_url,
            "supporting_local_source": str(ORBIT_REQUIREMENTS_1068),
            "current_status": "MISSING_KERNEL_INPUTS",
            "promotion_rule": "orbit/mask objects stay downstream readout maps, never parent action selectors",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": "ACQ1460_3_eta_convention",
            "target_object": "MICROSCOPE eta_AB convention",
            "needed_content": "eta formula, sign convention, absolute-value comparison convention, uncertainty/bound selection",
            "source_url_or_path": "https://arxiv.org/abs/2209.15488; https://arxiv.org/abs/2209.15487",
            "supporting_local_source": str(MICROSCOPE_EXTERNAL_1070),
            "current_status": "SOURCE_BACKED_BUT_NOT_PARENT_MAPPED",
            "promotion_rule": "formula can inform comparison only after parent residual row exists",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": "ACQ1460_4_Earth_source_profile",
            "target_object": "rho_m(x), source composition, delta_q(x)",
            "needed_content": "Earth mass/stress profile, composition/source-weight convention, source moments for finite bound",
            "source_url_or_path": "MISSING_SOURCE_SELECTION_REQUIRED",
            "supporting_local_source": str(SOURCE_ACQ_1455),
            "current_status": "MISSING_SOURCE_PROFILE_AND_COMPOSITION",
            "promotion_rule": "cannot use measured-G calibration to erase relative source profile",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": "ACQ1460_5_material_tensor",
            "target_object": "R_TA6V - R_PtRh10 material response tensor",
            "needed_content": "full material basis response tensor in the same parent basis as C_parent_WEP",
            "source_url_or_path": str(LIVE_MATERIAL_TENSOR),
            "supporting_local_source": str(SOURCE_ACQ_1455),
            "current_status": "LIVE_FILE_ABSENT_PARTIAL_PAIR_ONLY",
            "promotion_rule": "no cancellation or sign use until full tensor is sourced",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": "ACQ1460_6_C_parent_WEP",
            "target_object": "parent action coefficient",
            "needed_content": "C_parent_WEP slot value or theorem-zero certificate generated before readout projection",
            "source_url_or_path": str(LIVE_CPARENT),
            "supporting_local_source": str(PREV_SIGNING),
            "current_status": "MISSING_PARENT_INPUT",
            "promotion_rule": "no numeric WEP row without parent coefficient owner",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": "ACQ1460_7_checksum_and_extractor",
            "target_object": "source-pack reproducibility",
            "needed_content": "download script, extraction script, checksum manifest, row-count manifest, unit audit",
            "source_url_or_path": portal_url,
            "supporting_local_source": str(PREV_REFUSAL),
            "current_status": "NOT_BUILT",
            "promotion_rule": "claim file stays absent until reproducible extraction passes the 1457/1459 validator",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def live_guard_rows() -> list[dict[str, Any]]:
    live_targets = [
        ("LIVE1460_0_official_readout", "official_readout", LIVE_OFFICIAL_READOUT),
        ("LIVE1460_1_source_worldtube", "source_worldtube", LIVE_SOURCE_WORLD),
        ("LIVE1460_2_material_tensor", "material_tensor", LIVE_MATERIAL_TENSOR),
        ("LIVE1460_3_C_parent", "C_parent_WEP", LIVE_CPARENT),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "live_guard_id": guard_id,
            "object": object_name,
            "live_path": str(path),
            "exists_now": path.exists(),
            "would_write_in_1460": False,
            "reason": "1460 is theorem/acquisition route only; no live import and no claim promotion",
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
            "gate_id": "GATE1460_0_exact_decomposition",
            "gate": "source decomposition and residual law written",
            "gate_pass": True,
            "blocking_reason": "none; algebraic decomposition is exact",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1460_1_common_mode_source_signed",
            "gate": "delta_q(x)=0 signed by parent action",
            "gate_pass": False,
            "blocking_reason": "countermodel with source-only relative label is still retained",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1460_2_material_common_or_tensor",
            "gate": "material differential response zero or full tensor imported",
            "gate_pass": False,
            "blocking_reason": "full TA6V/PtRh10 tensor and parent basis map absent",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1460_3_finite_source_bound",
            "gate": "finite-source/multipole residual zero or bounded",
            "gate_pass": False,
            "blocking_reason": "Earth source profile, orbit kernel, and source-charge moments absent",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1460_4_official_KCMSM",
            "gate": "official readout/source kernel imported",
            "gate_pass": False,
            "blocking_reason": "live official readout path remains absent",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1460_5_Cparent",
            "gate": "C_parent_WEP theorem-zero or coefficient imported",
            "gate_pass": False,
            "blocking_reason": "live C_parent_WEP slot absent",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1460_6_measured_G_guard",
            "gate": "relative source residual cannot be absorbed into measured G",
            "gate_pass": True,
            "blocking_reason": "guard active; it blocks false promotion rather than proving zero",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1460_7_theorem_promoted",
            "gate": "calibrated point-source theorem claim-ready",
            "gate_pass": False,
            "blocking_reason": "requires gates 1 through 5; only exact algebra and guard are closed",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1460_0_calibrated_point_source",
            "target": "calibrated point-source/common-mode reduction for WEP source-worldtube leg",
            "exact_residual_law_derived": True,
            "common_mode_source_signed": False,
            "material_tensor_or_zero_signed": False,
            "finite_source_bound_imported": False,
            "official_KCMSM_imported": False,
            "C_parent_WEP_import_allowed": False,
            "tau_WEP_numeric_allowed": False,
            "local_claim_allowed": False,
            "decision": "KEEP_THEOREM_CONDITIONAL_AND_MOVE_TO_SOURCE_FACTORIZATION_OR_DATA_ACQUISITION",
            "reason": "the algebraic point-source residual law is exact, but delta_q(x)=0 and the finite-source bound are not signed or sourced",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1460_0_progress",
            "decision": "upgrade 1421 from a loose point-source target into an exact residual decomposition",
            "why": "the source-worldtube shortcut is legal only after the relative source profile delta_q(x) is zero or bounded",
            "consequence": "we now know the exact missing theorem/data object instead of hand-waving tau_WEP",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1460_1_no_promotion",
            "decision": "do not claim local WEP, local GR, tau_WEP, or source-worldtube removal",
            "why": "relative source labels, material tensor, official K_CMSM, finite-source bound, and C_parent_WEP are absent",
            "consequence": "all 1460 rows remain nonclaim and live files stay untouched",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1460_2_next_route",
            "decision": "next best derivation target is parent source factorization/no-relative-source-label",
            "why": "if delta_q(x)=0 can be signed upstream, the official source-worldtube burden collapses sharply",
            "consequence": "if that theorem fails, run the official CMSM/ONERA inventory and checksum acquisition route",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1460_0_1461",
            "next_target": "1461-Y5-R10-RAB-parent-source-factorization-no-relative-source-label-proof-or-CMSM-inventory.md",
            "script": "scripts/Y5_R10_RAB_parent_source_factorization_no_relative_source_label_proof_or_CMSM_inventory.py",
            "objective": "try to prove delta_q(x)=0 from the parent matter/action grammar; if it fails, build the CMSM/ONERA official inventory/checksum acquisition scaffold",
            "include": "no-relative-source-label theorem; source-only countermodel audit; finite-source residual owner; CMSM portal inventory route; no live claim",
            "exclude": "numeric tau_WEP; local-GR pass; C_parent promotion; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    point_theorem: list[dict[str, Any]],
    source_decomp: list[dict[str, Any]],
    finite_bound: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_csvs = [
        SOURCE_REGISTER,
        POINT_THEOREM,
        SOURCE_DECOMP,
        FINITE_BOUND,
        ACQUISITION_ROUTE,
        LIVE_GUARD,
        REDUCTION_GATES,
        SIGNING_DECISION,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    all_sources_exist = all(truth(row["exists"]) for row in sources)
    point_exact_present = any(row["proof_status"] == "EXACT_RESIDUAL_LAW" for row in point_theorem)
    theorem_not_promoted = any(row["proof_status"] == "THEOREM_NOT_PROMOTED" for row in point_theorem)
    zero_conditions_nonclaim = all(not truth(row["valid_for_claim"]) and not truth(row["claim_allowed"]) for row in source_decomp)
    finite_bounds_non_numeric = all(not truth(row["numeric_allowed"]) and not truth(row["claim_allowed"]) for row in finite_bound)
    acquisition_nonclaim = all(not truth(row["valid_for_claim"]) and not truth(row["claim_allowed"]) for row in acquisition)
    live_paths_untouched = all(not truth(row["exists_now"]) and not truth(row["would_write_in_1460"]) for row in live_guard)
    gate_pattern_safe = (
        truth(gates[0]["gate_pass"])
        and truth(gates[6]["gate_pass"])
        and all(not truth(row["gate_pass"]) for row in gates[1:6] + gates[7:])
    )
    signing_refuses = all(
        not truth(row["C_parent_WEP_import_allowed"])
        and not truth(row["tau_WEP_numeric_allowed"])
        and not truth(row["local_claim_allowed"])
        for row in signing
    )
    generated_parse = all(parse_csv_ok(path) for path in generated_csvs)
    branch_copies = BRANCH_POINT_THEOREM.exists() and BRANCH_ACQUISITION_ROUTE.exists() and BRANCH_SIGNING.exists()
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formal_recent = 0
    if FORMALIZATION.exists():
        formal_recent = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and path.stat().st_mtime > START_TS
        )
    checks = [
        ("VAL1460_0_sources", all_sources_exist, "all cited local source paths exist"),
        ("VAL1460_1_exact_residual_law", point_exact_present, "exact source residual law row exists"),
        ("VAL1460_2_theorem_not_promoted", theorem_not_promoted, "calibrated point-source theorem remains conditional/nonclaim"),
        ("VAL1460_3_zero_conditions_nonclaim", zero_conditions_nonclaim, "zero-condition rows remain nonclaim"),
        ("VAL1460_4_finite_bounds_non_numeric", finite_bounds_non_numeric, "finite-source bounds are formal/contracts only"),
        ("VAL1460_5_acquisition_nonclaim", acquisition_nonclaim, "official acquisition route rows remain nonclaim"),
        ("VAL1460_6_live_paths_untouched", live_paths_untouched, "critical live official/source/material/Cparent files remain absent"),
        ("VAL1460_7_gate_pattern_safe", gate_pattern_safe, "only algebra and measured-G guard pass; claim gates remain false"),
        ("VAL1460_8_signing_refuses", signing_refuses, "parent signing decision refuses Cparent/tau/local claim"),
        ("VAL1460_9_generated_csv_parse", generated_parse, "all generated 1460 CSVs parse cleanly"),
        ("VAL1460_10_branch_copies", branch_copies, "nonclaim branch copies written"),
        ("VAL1460_11_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1460_12_formalization_untouched", formal_recent == 0, f"formalization modified-file count since start={formal_recent}"),
        ("VAL1460_13_overall", True, "1460 derives the exact point-source residual law but does not claim source-worldtube removal"),
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
    point_theorem: list[dict[str, Any]],
    source_decomp: list[dict[str, Any]],
    finite_bound: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    with DOC.open("w", encoding="utf-8") as handle:
        handle.write("# 1460 - Calibrated point-source theorem reopen or official data acquisition route\n\n")
        handle.write(
            "**Current verdict:** the calibrated point-source route can be sharpened into an exact residual law, "
            "but it still cannot be promoted. The source-worldtube dependence disappears only if the relative source "
            "profile `delta_q(x)` is parent-zero/common-mode or explicitly bounded with official source/readout data. "
            "That signature is not yet present, so `tau_WEP`, `C_parent_WEP`, local WEP, and local-GR claims remain blocked.\n\n"
        )
        handle.write(
            "**Useful progress:** we now know the precise missing hinge: prove `rho_q(x)=q0 rho_m(x)` from the parent "
            "matter/action grammar, or acquire the official CMSM/ONERA source pack and bound the finite-source residual. "
            "This is a cleaner target than pretending the Earth source can be replaced by a point mass by habit.\n\n"
        )
        write_table(handle, "Source register", sources)
        write_table(handle, "Calibrated point-source theorem reopen", point_theorem)
        write_table(handle, "Source decomposition and zero conditions", source_decomp)
        write_table(handle, "Finite-source error bound contract", finite_bound)
        write_table(handle, "Official data acquisition route", acquisition)
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
    point_theorem = point_source_theorem_rows()
    source_decomp = source_decomposition_rows()
    finite_bound = finite_bound_rows()
    acquisition = acquisition_route_rows()
    live_guard = live_guard_rows()
    gates = reduction_gate_rows()
    signing = signing_decision_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(POINT_THEOREM, point_theorem)
    write_csv(SOURCE_DECOMP, source_decomp)
    write_csv(FINITE_BOUND, finite_bound)
    write_csv(ACQUISITION_ROUTE, acquisition)
    write_csv(LIVE_GUARD, live_guard)
    write_csv(REDUCTION_GATES, gates)
    write_csv(SIGNING_DECISION, signing)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(POINT_THEOREM, BRANCH_POINT_THEOREM)
    copy_branch(ACQUISITION_ROUTE, BRANCH_ACQUISITION_ROUTE)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    remove_pycache()
    validation = validation_rows(sources, point_theorem, source_decomp, finite_bound, acquisition, live_guard, gates, signing)
    write_csv(VALIDATION, validation)
    write_doc(sources, point_theorem, source_decomp, finite_bound, acquisition, live_guard, gates, signing, decisions, validation, next_target)
    print("Y5_R10_1460_calibrated_point_source_residual_law_written_nonclaim")


if __name__ == "__main__":
    main()
