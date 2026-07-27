from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2891-Y5-R2FR-no-boundary-charge-source-descent-or-qRhat-row-under-AX1090.md"

SRC_2890_DOC = ROOT / "2890-Y5-R2FR-xU-delta-p-profile-zero-or-source-row-under-AX1090.md"
SRC_2890_NEXT = RESIDUALS / "P8_Y5_R2FR_2890_NEXT_TARGET.csv"
SRC_2890_PROFILE = RESIDUALS / "P8_Y5_R2FR_2890_PROFILE_INPUT_ROW_NONCLAIM.csv"
SRC_2890_KERNEL = RESIDUALS / "P8_Y5_R2FR_2890_COMMON_WEYL_KERNEL_UPDATE.csv"
SRC_2890_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2890_VALIDATION.csv"

SRC_1884_AUDIT = RESIDUALS / "P8_Y5_PARENT_QLOC_1884_NO_BOUNDARY_CHARGE_SOURCE_DESCENT_AUDIT.csv"
SRC_1884_MATRIX = RESIDUALS / "P8_Y5_PARENT_QLOC_1884_SOURCE_DESCENT_PREMISE_MATRIX.csv"
SRC_1884_CONTRACT = RESIDUALS / "P8_Y5_PARENT_QLOC_1884_DELTA_P_QRHAT_INPUT_CONTRACT.csv"
SRC_1240_ZERO = RESIDUALS / "P8_Y5_R10_1240_QR_ZERO_CHARGE_THEOREM_ATTEMPT.csv"
SRC_1246_CLAUSES = RESIDUALS / "P8_Y5_R10_1246_PARENT_QR_ZERO_THEOREM_CLAUSES.csv"
SRC_1254_BOUNDARY = RESIDUALS / "P8_Y5_R10_1254_BOUNDARY_FLUX_CONTRACT.csv"
SRC_2094_ZERO = RESIDUALS / "P8_Y5_PARENT_QLOC_2094_QR_NOCHARGE_THEOREM_ATTEMPT.csv"
SRC_2094_FINITE = RESIDUALS / "P8_Y5_PARENT_QLOC_2094_FIRST_FINITE_QRHAT_INPUT_ROWS.csv"
SRC_2575_ZERO = RESIDUALS / "P8_Y5_QR_ZERO_2575_PARENT_ZERO_SIGNATURE_AUDIT.csv"
SRC_2575_INPUT = RESIDUALS / "P8_Y5_QR_ZERO_2575_LIVE_DELTA_P_QRHAT_COUPLING_INPUT_ROW.csv"
SRC_2833_ZERO = RESIDUALS / "P8_Y5_R2FR_2833_QRHAT_PARENT_ZERO_PROOF_AUDIT.csv"
SRC_2840_CERT = RESIDUALS / "P8_Y5_R2FR_2840_PARENT_ZERO_CERTIFICATE_AUDIT.csv"
SRC_2841_BRIDGE = RESIDUALS / "P8_Y5_R2FR_2841_QREFF_TO_QRHAT_CONDITIONAL_BRIDGE.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2891_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_2891_NO_BOUNDARY_SOURCE_THEOREM_ATTEMPT.csv",
    "integral": RESIDUALS / "P8_Y5_R2FR_2891_SOURCE_NEUTRALITY_INTEGRAL_LAW.csv",
    "qrhat": RESIDUALS / "P8_Y5_R2FR_2891_QRHAT_INPUT_ROW_NONCLAIM.csv",
    "kernel": RESIDUALS / "P8_Y5_R2FR_2891_PROFILE_AND_KERNEL_UPDATE.csv",
    "ppn": RESIDUALS / "P8_Y5_R2FR_2891_FULL_PPN_BLOCKER_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2891_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2891_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2891_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2891_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2891_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2891_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "qrhat_copy": LOCAL_BOUNDS / "RAB_QRHAT_INPUT_ROW_2891_NONCLAIM.csv",
    "theorem_copy": SOURCE_WEIGHT / "RAB_NO_BOUNDARY_SOURCE_THEOREM_2891_NONCLAIM.csv",
    "ppn_copy": BETA_DOCS / "RAB_FULL_PPN_BLOCKER_LEDGER_2891_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2891_parent_action_or_beta_source_NEXT.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2891_0_2890_doc", SRC_2890_DOC, "NEXT2890_0_2891;PROFILE_LAW_DERIVED_VALUE_AND_ZERO_BLOCKED", "2890 handoff"),
        ("SRC2891_1_2890_next", SRC_2890_NEXT, "NEXT2890_0_2891", "explicit 2891 target"),
        ("SRC2891_2_2890_profile", SRC_2890_PROFILE, "PROF2890_0_live_xU_delta_p_qRhat;MISSING_PARENT_ZERO_THEOREM_OR_SOURCE_BACKED_FINITE_QRHAT_ROW", "profile input row"),
        ("SRC2891_3_2890_kernel", SRC_2890_KERNEL, "KUP2890_0_common_weyl_profile_substitution;PROFILE_SUBSTITUTION_READY_VALUES_MISSING_NONCLAIM", "kernel update"),
        ("SRC2891_4_2890_validation", SRC_2890_VALIDATION, "VAL2890_OVERALL", "2890 validation"),
        ("SRC2891_5_1884_audit", SRC_1884_AUDIT, "NBC1884_1_exact_zero_flux_lemma;NO_BOUNDARY_CHARGE_NOT_PARENT_DERIVED", "zero-flux lemma"),
        ("SRC2891_6_1884_matrix", SRC_1884_MATRIX, "SDM1884_1_boundary_charge;SDM1884_2_source_silence", "source descent matrix"),
        ("SRC2891_7_1884_contract", SRC_1884_CONTRACT, "DPQR1884_1_qRhat;DPQR1884_6_descent_statuses", "delta_p/q_R_hat contract"),
        ("SRC2891_8_1240_zero", SRC_1240_ZERO, "ZQR1240_5_verdict;ZERO_CHARGE_THEOREM_NOT_DERIVED", "early Q_R zero audit"),
        ("SRC2891_9_1246_clauses", SRC_1246_CLAUSES, "QZT1246_5_topological;QZT1246_6_first_class", "zero theorem route clauses"),
        ("SRC2891_10_1254_boundary", SRC_1254_BOUNDARY, "BFC1254_1_raw_boundary_flux;BFC1254_2_zero_theorem", "finite/boundary flux contract"),
        ("SRC2891_11_2094_zero", SRC_2094_ZERO, "QZ2094_2_source_neutrality;ZERO_THEOREM_FAIL_CURRENT_CORPUS", "source neutrality attempt"),
        ("SRC2891_12_2094_finite", SRC_2094_FINITE, "QRI2094_4_first_input_verdict;MTS_QRHAT_INPUT_ROW_BLOCKED_EXACT_MISSING_PARENT_INPUTS", "finite q_R_hat input status"),
        ("SRC2891_13_2575_zero", SRC_2575_ZERO, "QRZ2575_6_verdict;QR_PARENT_ZERO_WITH_COUPLING_NOT_DERIVED_CURRENT_CORPUS", "coupling owner audit"),
        ("SRC2891_14_2575_input", SRC_2575_INPUT, "LIVE2575_2_no_live_mts_prediction;NO_LIVE_PREDICTION_ROW_ACCEPTED", "live q_R_hat coupling input"),
        ("SRC2891_15_2833_zero", SRC_2833_ZERO, "PZ2833_5_parent_zero_verdict;NOT_CLOSED", "recent q_R_hat parent zero audit"),
        ("SRC2891_16_2840_cert", SRC_2840_CERT, "PZ2840_5_joint_certificate;NOT_CLOSED", "joint parent-zero certificate audit"),
        ("SRC2891_17_2841_bridge", SRC_2841_BRIDGE, "BRG2841_4_qRhat_map;BRG2841_5_delta_p_map", "q_R_eff bridge"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        found, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "NBT2891_0_exterior_conservation",
            "exterior current equation",
            "partial_r(W_R partial_r C_R)=J_R and J_R=0 outside the compact source imply W_R partial_r C_R=Q_R",
            "DERIVED_CONDITIONAL",
            "conserved exterior charge exists",
            "does not set Q_R=0",
        ),
        (
            "NBT2891_1_integrated_source_charge",
            "source integral law",
            "integrating through the source gives Q_R(out)=Q_R(in)+Integral_source J_R dr; with regular center/no inner edge Q_R(in)=0",
            "EXACT_CONDITIONAL_SOURCE_CHARGE_LAW",
            "Q_R equals the parent reciprocal source charge Pi_R when the radial reduction is legitimate",
            "requires parent-owned J_R density, measure, orientation and boundary class",
        ),
        (
            "NBT2891_2_source_neutrality",
            "ordinary matter carries no reciprocal charge",
            "if S_matter=Sbar[q(Phi),Psi,theta] and v_R is vertical in ker(Dq), then delta_vR S_matter=0 and the ordinary source contribution to J_R vanishes",
            "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "would force Pi_R=0 for the protected ordinary-source class",
            "parent quotient map, vertical generator, and matter/readout descent are unsigned",
        ),
        (
            "NBT2891_3_boundary_charge_zero",
            "zero/proper reciprocal boundary charge",
            "if the reciprocal generator has no physical boundary charge for allowed local sources, Q_R is pure gauge/zero rather than exterior hair",
            "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "would close Q_R=0 together with source neutrality",
            "boundary term and reference subtraction are not parent-derived",
        ),
        (
            "NBT2891_4_coupling_owner",
            "coupling/source normalization ownership",
            "kappa_MTS, ell_J, H_core source equation and measured GM convention must be fixed before readout",
            "REQUIRED_NOT_SIGNED",
            "prevents fitted-GM/coupling rescaling from hiding a finite Q_R",
            "coupling owner remains a hard blocker from 2575",
        ),
        (
            "NBT2891_5_verdict",
            "parent no-boundary-charge/source-descent theorem",
            "current MTS parent signs Q_R=0, therefore q_R_hat=delta_p=x_U_CR=0",
            "NO_BOUNDARY_SOURCE_DESCENT_NOT_PARENT_SIGNED_CURRENT_CORPUS",
            "do not install a zero row",
            "source-neutrality theorem is exact as a contract but not parent-signed",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for theorem_id, target, statement, status, if_closed, blocker in specs:
        rows.append(
            add_common(
                {
                    "theorem_id": theorem_id,
                    "target": target,
                    "statement": statement,
                    "current_status": status,
                    "if_closed": if_closed,
                    "current_blocker": blocker,
                    "conditional_piece_proved": status.startswith("EXACT") or status == "DERIVED_CONDITIONAL",
                    "parent_signed": False,
                    "parent_zero_closed": False,
                    "theorem_zero_adopted": False,
                    "finite_value_present": False,
                    "prediction_source_backed": False,
                    "accepted_for_scoring": False,
                }
            )
        )
    return rows


def integral_law_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SNL2891_0_radial_balance",
            "partial_r(W_R partial_r C_R)=J_R",
            "Q_R(r)=W_R partial_r C_R",
            "partial_r Q_R=J_R",
            "local radial reduction of reciprocal current",
            "DERIVED_CONDITIONAL_BALANCE",
        ),
        (
            "SNL2891_1_source_integral",
            "Q_R(out)-Q_R(in)=Integral_source J_R dr",
            "Q_R(out)=Pi_R if Q_R(in)=0",
            "Pi_R is the total reciprocal source charge",
            "regular center or no inner boundary; parent measure fixed",
            "EXACT_CONDITIONAL_INTEGRAL_LAW",
        ),
        (
            "SNL2891_2_zero_condition",
            "Pi_R=0 and no physical boundary charge",
            "Q_R(out)=0",
            "C_R=0 exterior if C_R(infinity)=0 and W_R>0",
            "ordinary source neutrality plus boundary zero theorem",
            "EXACT_CONDITIONAL_ZERO_CHAIN",
        ),
        (
            "SNL2891_3_ppn_consequence",
            "Q_R=0",
            "q_R_hat=0; delta_p=-q_R_hat/2=0; x_U_CR=-q_R_hat=0",
            "first-order reciprocal PPN profile is killed",
            "requires the same measured GM convention before readout",
            "EXACT_CONDITIONAL_PPN_CONSEQUENCE",
        ),
        (
            "SNL2891_4_current_status",
            "source neutrality and boundary charge are not parent-signed",
            "Q_R(out) remains a live residual",
            "finite q_R_hat or parent zero theorem still required",
            "current corpus lacks parent source density and coupling owner",
            "VALUE_ZERO_BLOCKED",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for law_id, premise, relation, consequence, required_context, status in specs:
        rows.append(
            add_common(
                {
                    "law_id": law_id,
                    "premise": premise,
                    "relation": relation,
                    "consequence": consequence,
                    "required_context": required_context,
                    "current_status": status,
                    "parent_signed": False,
                    "theorem_zero_adopted": False,
                    "finite_value_present": False,
                    "prediction_source_backed": False,
                    "accepted_for_scoring": False,
                }
            )
        )
    return rows


def qrhat_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "input_id": "QR2891_0_live_qRhat_source_row",
                "route_type": "parent_zero_or_finite_qR_hat_required",
                "q_R_hat": "MISSING_PARENT_ZERO_OR_NUMERIC_Q_R_HAT",
                "delta_p": "MISSING_PARENT_ZERO_OR_NUMERIC_DELTA_P",
                "x_U_CR": "MISSING_PARENT_ZERO_OR_NUMERIC_X_U_CR",
                "relations": "x_U_CR=-q_R_hat; delta_p=-q_R_hat/2; C_R=-q_R_hat U/c^2 if exterior C_R=-Q_R/r",
                "units": "dimensionless",
                "GM_convention": "q_R_hat=Q_R c^2/(G M_source), same measured GM as U=GM/r",
                "source_path": "MISSING_PARENT_ZERO_THEOREM_OR_SOURCE_BACKED_FINITE_QRHAT_ROW",
                "source_id": "MISSING_PARENT_SOURCE_OR_FINITE_SOURCE",
                "parent_zero_status": "MISSING_PARENT_NO_BOUNDARY_SOURCE_DESCENT_SIGNATURE",
                "finite_value_status": "MISSING_NUMERIC_Q_R_HAT",
                "coupling_owner_status": "MISSING_PARENT_COUPLING_OWNER_FOR_PREDICTION",
                "boundary_charge_status": "MISSING_BOUNDARY_CHARGE_ZERO_THEOREM",
                "source_descent_status": "MISSING_SOURCE_DESCENT",
                "matter_readout_status": "MISSING_MATTER_READOUT_DESCENT",
                "projection_status": "MISSING_ARENA_PROJECTION",
                "qRhat_abs_guardrail": "4.6e-05_comparator_only_not_prediction",
                "current_status": "QRHAT_SOURCE_ROW_BLOCKED_NONCLAIM",
                "closure_used": False,
                "comparator_only": False,
                "gamma_only": False,
                "cancellation_only": False,
                "full_vector_ready": False,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        ),
        add_common(
            {
                "input_id": "QR2891_1_parent_zero_template",
                "route_type": "parent_zero_theorem_only",
                "q_R_hat": "0_IF_PARENT_SIGNED",
                "delta_p": "0_IF_PARENT_SIGNED",
                "x_U_CR": "0_IF_PARENT_SIGNED",
                "relations": "source neutrality + boundary zero + exterior zero-flux lemma",
                "units": "dimensionless",
                "GM_convention": "not_required_for_zero_theorem_but_required_if_scored",
                "source_path": "MISSING_PARENT_NO_BOUNDARY_SOURCE_DESCENT_THEOREM",
                "source_id": "MISSING_PARENT_ZERO_SOURCE",
                "parent_zero_status": "UNSIGNED_CONDITIONAL_ZERO_ROUTE",
                "finite_value_status": "not_applicable",
                "coupling_owner_status": "MISSING_PARENT_COUPLING_OWNER_FOR_PREDICTION",
                "boundary_charge_status": "MISSING_BOUNDARY_CHARGE_ZERO_THEOREM",
                "source_descent_status": "MISSING_SOURCE_DESCENT",
                "matter_readout_status": "MISSING_MATTER_READOUT_DESCENT",
                "projection_status": "MISSING_ARENA_PROJECTION",
                "qRhat_abs_guardrail": "not_a_finite_row",
                "current_status": "TEMPLATE_ONLY_NOT_A_VALUE_ROW",
                "closure_used": False,
                "comparator_only": False,
                "gamma_only": False,
                "cancellation_only": False,
                "full_vector_ready": False,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        ),
        add_common(
            {
                "input_id": "QR2891_2_finite_qRhat_template",
                "route_type": "finite_qR_hat_prediction_required",
                "q_R_hat": "MISSING_NUMERIC_Q_R_HAT",
                "delta_p": "MISSING_NUMERIC_DELTA_P",
                "x_U_CR": "MISSING_NUMERIC_X_U_CR",
                "relations": "q_R_hat=Q_R c^2/(G M_source); delta_p=-q_R_hat/2; x_U_CR=-q_R_hat",
                "units": "dimensionless",
                "GM_convention": "same measured GM as U=GM/r",
                "source_path": "MISSING_SOURCE_BACKED_Q_R_OR_QRHAT_ROW",
                "source_id": "MISSING_FINITE_QRHAT_SOURCE",
                "parent_zero_status": "not_applicable",
                "finite_value_status": "MISSING_Q_R_VALUE_AND_SOURCE_BODY",
                "coupling_owner_status": "MISSING_PARENT_COUPLING_OWNER_FOR_PREDICTION",
                "boundary_charge_status": "finite_charge_branch_requires_boundary_flux_or_source_body",
                "source_descent_status": "finite_source_body_required",
                "matter_readout_status": "MISSING_MATTER_READOUT_DESCENT",
                "projection_status": "MISSING_ARENA_PROJECTION",
                "qRhat_abs_guardrail": "4.6e-05_comparator_only_not_prediction",
                "current_status": "TEMPLATE_ONLY_NOT_A_VALUE_ROW",
                "closure_used": False,
                "comparator_only": False,
                "gamma_only": False,
                "cancellation_only": False,
                "full_vector_ready": False,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        ),
    ]


def kernel_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "update_id": "PKU2891_0_qRhat_bridge_reaffirmed",
                "parent_update": "KUP2890_0_common_weyl_profile_substitution",
                "profile_relation": "x_U_CR=2delta_p=-q_R_hat",
                "gamma_relation": "gamma_obs-1=(-q_R_hat*(1+4*b_R)/2)/(1+b_R*q_R_hat)",
                "if_parent_zero": "q_R_hat=0 kills the first-order C_R reciprocal profile, but only after parent source-neutrality/boundary zero is signed",
                "if_finite": "finite q_R_hat must be source-normalized and carried through the full PPN vector",
                "current_status": "BRIDGE_READY_VALUE_MISSING_NONCLAIM",
                "missing_for_claim": "MISSING_PARENT_ZERO_OR_FINITE_QRHAT;MISSING_b_R;MISSING_BETA_SOURCE_ENDPOINT_QLOC_CHANNELS",
                "comparison_ready": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
    ]


def ppn_rows() -> list[dict[str, Any]]:
    specs = [
        ("PPNB2891_0_qRhat", "q_R_hat;delta_p;x_U_CR", "gamma_minus_1;local_GR_Newton", "SOURCE_NEUTRALITY_THEOREM_UNSIGNED_VALUE_MISSING", "MISSING_PARENT_SOURCE_NEUTRALITY_OR_FINITE_QRHAT"),
        ("PPNB2891_1_bR", "b_R", "gamma_minus_1;clock_common_mode", "MISSING_b_R_VALUE_OR_ZERO", "MISSING_NO_WEYL_SLOT_THEOREM_OR_SOURCE_COEFFICIENT"),
        ("PPNB2891_2_beta", "Delta_beta_total_abs", "beta_minus_1;orbital_timing", "MISSING_BETA_RESPONSE_KERNEL_AND_SOURCE_NORMALIZED_VECTOR", "MISSING_SECOND_ORDER_FIELD_EQUATION"),
        ("PPNB2891_3_source_coupling", "kappa_MTS;ell_J;H_core;w_R", "source_normalization;Newton_GM;WEP", "MISSING_PARENT_COUPLING_OWNER", "MISSING_HCORE_SOURCE_EQUATION_AND_COUPLING_OWNER"),
        ("PPNB2891_4_preferred_endpoint", "d_R;epsilon_endpoint_R;alpha_readout", "preferred_frame;light_time;clock", "MISSING_PROJECTION_SILENCE_OR_FINITE_KERNEL", "MISSING_DISFORMAL_ENDPOINT_READOUT_MAP"),
        ("PPNB2891_5_q_loc_Khat", "q_loc^nu;Khat^{mu nu}", "beta;clock;orbital;local_GR_Newton", "MISSING_QLOC_WARD_ZERO_PROFILE_OR_FINITE_KERNEL", "MISSING_WARD_ZERO_THROUGH_OU2"),
        ("PPNB2891_6_total_abs", "Delta_PPN_abs", "all_PPN;local_GR_Newton", "SCHEMA_READY_VALUES_MISSING", "MISSING_ALL_COMPONENT_VALUES_OR_THEOREM_ZEROS"),
    ]
    return [
        add_common(
            {
                "blocker_id": blocker_id,
                "symbols": symbols,
                "observable_targets": targets,
                "current_status": status,
                "missing_for_claim": missing,
                "no_cancellation_policy": "active",
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for blocker_id, symbols, targets, status, missing in specs
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2891_0_integral_law", "Q_R source integral law is derived", "PASS_NONCLAIM", "Q_R(out)=Integral_source J_R under regular/no-inner-boundary conditions"),
        ("GATE2891_1_source_neutrality", "ordinary matter source neutrality is parent-signed", "FAIL", "S_matter quotient descent and vertical generator are unsigned"),
        ("GATE2891_2_boundary_zero", "reciprocal boundary charge is zero/proper", "FAIL", "boundary charge theorem and reference subtraction are unsigned"),
        ("GATE2891_3_coupling_owner", "coupling/source normalization is parent-owned", "FAIL", "kappa_MTS, ell_J and H_core source equation remain missing"),
        ("GATE2891_4_qrhat_row", "live q_R_hat row is zero or numeric/source-backed", "FAIL", "no parent zero theorem or finite q_R_hat prediction row exists"),
        ("GATE2891_5_local_gr", "local GR/Newton limit follows", "FAIL", "full PPN vector and beta/source/readout channels remain open"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": False,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for gate_id, criterion, result, reason in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2891_0_qRhat_parent_zero_or_finite_row_runner",
                "status": "REFUSED_QRHAT_ZERO_AND_NUMERIC_ROW_MISSING",
                "accepted_zero_theorems": 0,
                "accepted_finite_rows": 0,
                "accepted_predictions": 0,
                "reason": "source-neutrality integral law is conditional; parent source descent, boundary zero, coupling owner and finite q_R_hat value remain missing",
                "runner_ready": False,
                "claim_unlocked": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2891_0_integral", "KEEP_SOURCE_NEUTRALITY_INTEGRAL_LAW", "it identifies the exact missing theorem: Q_R is the integrated reciprocal source charge, not just an arbitrary mystery coefficient", "use Pi_R=0 as the parent action/source-neutrality target"),
        ("DEC2891_1_zero", "DO_NOT_INSTALL_QRHAT_ZERO_ROW", "source neutrality, boundary charge and coupling owner are not signed in one parent package", "keep q_R_hat, delta_p and x_U_CR missing/nonclaim"),
        ("DEC2891_2_finite", "DO_NOT_USE_COMPARATOR_AS_FINITE_PREDICTION", "Cassini-style q_R_hat ceiling is a guardrail only, not an MTS source value", "finite route still needs Q_R or q_R_hat from parent coefficients/source body"),
        ("DEC2891_3_next", "SELECT_PARENT_ACTION_SOURCE_NEUTRALITY_CONSTRUCTION_NEXT", "another audit will not close this; the next leap is to build or reject the parent action/generator clause that makes ordinary sources neutral", "attempt a minimal parent action/source-neutrality generator in 2892"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
                "accepted_for_scoring": False,
            }
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2891_0_2892",
                "status": "selected_primary",
                "target_doc": "2892-Y5-R2FR-parent-action-source-neutrality-generator-or-closure-demotion-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_parent_action_source_neutrality_generator_or_closure_demotion_under_AX1090_2892.py",
                "mission": "construct the minimal parent action/quotient-generator package that signs ordinary-source neutrality, zero reciprocal boundary charge and coupling ownership; if it fails, demote q_R_hat=0 to closure-only and move finite rows/beta forward",
                "forbidden_shortcuts": "no lambda_R by hand; no GR AB=1 import; no comparator-as-prediction; no gamma-only local-GR claim; no cancellation; no GitHub action",
                "selected": True,
                "accepted_for_scoring": False,
            }
        ),
        add_common(
            {
                "next_id": "NEXT2891_1_held_beta",
                "status": "held_secondary",
                "target_doc": "2892b-Y5-R2FR-beta-source-normalized-second-order-kernel-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_beta_source_normalized_second_order_kernel_under_AX1090_2892b.py",
                "mission": "attack beta/source normalization if parent source-neutrality is demoted to closure-only",
                "forbidden_shortcuts": "do not infer beta=1 from q_R_hat or gamma",
                "selected": False,
                "accepted_for_scoring": False,
            }
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("BR2891_0_qrhat_copy", OUTPUTS["qrhat"], BRANCH_OUTPUTS["qrhat_copy"], "local-bounds copy of q_R_hat input row"),
        ("BR2891_1_theorem_copy", OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_copy"], "source-weight copy of no-boundary/source theorem attempt"),
        ("BR2891_2_ppn_copy", OUTPUTS["ppn"], BRANCH_OUTPUTS["ppn_copy"], "beta-source docs copy of full PPN blocker ledger"),
        ("BR2891_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue next target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in copy_specs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source),
                    "copy_path": str(destination),
                    "purpose": purpose,
                    "exists": destination.exists(),
                }
            )
        )
    return rows


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                return False
    return True


def generated_under_root(paths: list[Path]) -> bool:
    root_resolved = ROOT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root_resolved)
        except ValueError:
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "parent_signed",
        "parent_zero_closed",
        "theorem_zero_adopted",
        "finite_value_present",
        "prediction_source_backed",
        "accepted_for_scoring",
        "gate_passed",
        "runner_ready",
        "claim_unlocked",
        "comparison_ready",
        "full_vector_ready",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    theorem = rows_by_name["theorem"]
    integral = rows_by_name["integral"]
    qrhat = rows_by_name["qrhat"]
    kernel = rows_by_name["kernel"]
    ppn = rows_by_name["ppn"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    checks = [
        ("VAL2891_0_sources_exist", all(row["path_exists"] for row in sources), "all registered source paths exist"),
        ("VAL2891_1_source_anchors", all(row["anchors_found"] for row in sources), "all registered source anchors were found"),
        ("VAL2891_2_integral_law", any(row["current_status"] == "EXACT_CONDITIONAL_SOURCE_CHARGE_LAW" for row in theorem), "source integral law is recorded"),
        ("VAL2891_3_zero_not_adopted", any(row["current_status"] == "NO_BOUNDARY_SOURCE_DESCENT_NOT_PARENT_SIGNED_CURRENT_CORPUS" for row in theorem) and all(row["theorem_zero_adopted"] is False for row in theorem), "Q_R zero theorem is not adopted"),
        ("VAL2891_4_source_chain", any(row["current_status"] == "EXACT_CONDITIONAL_ZERO_CHAIN" for row in integral), "conditional source-neutrality zero chain is explicit"),
        ("VAL2891_5_qrhat_row_nonclaim", qrhat[0]["current_status"] == "QRHAT_SOURCE_ROW_BLOCKED_NONCLAIM" and "MISSING" in qrhat[0]["q_R_hat"], "live q_R_hat row remains missing/nonclaim"),
        ("VAL2891_6_kernel_nonclaim", kernel[0]["current_status"] == "BRIDGE_READY_VALUE_MISSING_NONCLAIM" and kernel[0]["comparison_ready"] is False, "profile/kernel bridge remains nonclaim"),
        ("VAL2891_7_full_ppn_blockers", len(ppn) == 7 and any(row["blocker_id"] == "PPNB2891_6_total_abs" for row in ppn), "full PPN blocker ledger remains active"),
        ("VAL2891_8_gates_fail_closed", all(row["gate_passed"] is False for row in gates), "acceptance gates fail closed"),
        ("VAL2891_9_runner_refused", runner[0]["status"] == "REFUSED_QRHAT_ZERO_AND_NUMERIC_ROW_MISSING" and runner[0]["runner_ready"] is False, "runner remains refused"),
        ("VAL2891_10_next_target_2892", next_target[0]["next_id"] == "NEXT2891_0_2892" and next_target[0]["selected"] is True, "2892 parent action/source-neutrality construction selected"),
        ("VAL2891_11_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2891_12_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2891_13_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2891_14_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2891_15_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2891_16_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2891_17_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2891_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2891 derived the conditional source-neutrality integral contract Q_R(out)=Integral J_R, refused q_R_hat=0 without parent source/boundary/coupling signatures, kept finite q_R_hat missing, and selected parent action/source-neutrality construction for 2892.",
            "timestamp_utc": now(),
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    text = f"""# 2891 - Y5 R2FR No-Boundary-Charge Source Descent Or qRhat Row Under AX1090

Status: `Y5_R2FR_2891_source_neutrality_integral_law_derived_qRhat_zero_unsigned_2892_next`

## Private Verdict

2891 gets a useful exact contract, but not the parent-signed zero theorem.

The local reciprocal charge is now pinned to a source-neutrality condition:

`partial_r(W_R partial_r C_R)=J_R`, so with `Q_R(r)=W_R partial_r C_R`, `partial_r Q_R=J_R`.

Integrating through a compact source gives `Q_R(out)-Q_R(in)=Integral_source J_R dr`. With regular center/no inner reciprocal edge, `Q_R(in)=0`, hence the exterior hair is the total reciprocal source charge `Pi_R`.

So the clean derivation route is now exact: if ordinary matter is neutral under the reciprocal generator, and the reciprocal boundary charge is zero/proper, then `Pi_R=Q_R=0`, hence `q_R_hat=delta_p=x_U_CR=0`.

But current corpus still does not parent-sign the needed quotient map, vertical generator, source neutrality, boundary charge, matter/readout descent, projection silence, or coupling owner. Therefore no local-GR, PPN, or q_R_hat zero claim is allowed.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## No-Boundary Source Theorem Attempt

{md_table(rows_by_name["theorem"], ["theorem_id", "target", "current_status", "if_closed", "current_blocker", "valid_for_claim"])}

## Source Neutrality Integral Law

{md_table(rows_by_name["integral"], ["law_id", "premise", "relation", "consequence", "current_status", "valid_for_claim"])}

## qRhat Input Row

{md_table(rows_by_name["qrhat"], ["input_id", "route_type", "q_R_hat", "delta_p", "x_U_CR", "relations", "current_status", "valid_for_claim"])}

## Profile And Kernel Update

{md_table(rows_by_name["kernel"], ["update_id", "profile_relation", "gamma_relation", "if_parent_zero", "current_status", "valid_for_claim"])}

## Full PPN Blocker Ledger

{md_table(rows_by_name["ppn"], ["blocker_id", "symbols", "observable_targets", "current_status", "missing_for_claim", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "accepted_zero_theorems", "accepted_finite_rows", "reason", "runner_ready", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    remove_pycache()
    rows_by_name = {
        "sources": source_register_rows(),
        "theorem": theorem_rows(),
        "integral": integral_law_rows(),
        "qrhat": qrhat_rows(),
        "kernel": kernel_rows(),
        "ppn": ppn_rows(),
        "gates": gate_rows(),
        "runner": runner_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], branch_rows)
    rows_by_name["branches"] = branch_rows
    remove_pycache()
    validation = validation_rows(rows_by_name, branch_rows)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(rows_by_name, branch_rows, validation)
    remove_pycache()
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation if row["validation_id"] == "VAL2891_OVERALL")
    print(f"VAL2891_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
