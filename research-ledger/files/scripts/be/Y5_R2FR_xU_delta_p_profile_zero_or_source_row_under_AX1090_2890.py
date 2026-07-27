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

DOC = ROOT / "2890-Y5-R2FR-xU-delta-p-profile-zero-or-source-row-under-AX1090.md"

SRC_2889_DOC = ROOT / "2889-Y5-R2FR-common-frame-bR-zero-or-first-PPN-kernel-row-under-AX1090.md"
SRC_2889_NEXT = RESIDUALS / "P8_Y5_R2FR_2889_NEXT_TARGET.csv"
SRC_2889_KERNEL = RESIDUALS / "P8_Y5_R2FR_2889_COMMON_WEYL_PPN_KERNEL_ROW_NONCLAIM.csv"
SRC_2889_INPUTS = RESIDUALS / "P8_Y5_R2FR_2889_KERNEL_INPUT_REQUIREMENTS.csv"
SRC_2889_PPN = RESIDUALS / "P8_Y5_R2FR_2889_FULL_PPN_GUARD_LEDGER.csv"
SRC_2889_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2889_VALIDATION.csv"

SRC_1882_DOC = ROOT / "1882-Y5-R2FR-sigmaR-profile-coefficient-from-CR-source-normalization-or-no-shadow-action-contract.md"
SRC_1882_IDENTITY = RESIDUALS / "P8_Y5_PARENT_QLOC_1882_CR_WEAK_FIELD_IDENTITY.csv"
SRC_1882_COMBO = RESIDUALS / "P8_Y5_PARENT_QLOC_1882_PPN_COMBINATION_BOUND.csv"
SRC_1883_BRIDGE = RESIDUALS / "P8_Y5_PARENT_QLOC_1883_DELTA_P_QRHAT_BRIDGE.csv"
SRC_1884_DOC = ROOT / "1884-Y5-R2FR-no-boundary-charge-source-descent-or-delta-p-input-contract.md"
SRC_1884_AUDIT = RESIDUALS / "P8_Y5_PARENT_QLOC_1884_NO_BOUNDARY_CHARGE_SOURCE_DESCENT_AUDIT.csv"
SRC_1884_CONTRACT = RESIDUALS / "P8_Y5_PARENT_QLOC_1884_DELTA_P_QRHAT_INPUT_CONTRACT.csv"
SRC_1884_TEMPLATE = RESIDUALS / "P8_Y5_PARENT_QLOC_1884_DELTA_P_QRHAT_CANDIDATE_TEMPLATE_NONCLAIM.csv"
SRC_2631_VECTOR = RESIDUALS / "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_FULL_PPN_VECTOR_LEDGER.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2890_SOURCE_REGISTER.csv",
    "profile_law": RESIDUALS / "P8_Y5_R2FR_2890_XU_DELTA_P_PROFILE_LAW.csv",
    "profile_input": RESIDUALS / "P8_Y5_R2FR_2890_PROFILE_INPUT_ROW_NONCLAIM.csv",
    "kernel_update": RESIDUALS / "P8_Y5_R2FR_2890_COMMON_WEYL_KERNEL_UPDATE.csv",
    "ppn_blockers": RESIDUALS / "P8_Y5_R2FR_2890_FULL_PPN_BLOCKER_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2890_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2890_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2890_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2890_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2890_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2890_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "profile_copy": LOCAL_BOUNDS / "RAB_XU_DELTA_P_PROFILE_INPUT_2890_NONCLAIM.csv",
    "kernel_copy": SOURCE_WEIGHT / "RAB_COMMON_WEYL_KERNEL_UPDATE_2890_NONCLAIM.csv",
    "ppn_copy": BETA_DOCS / "RAB_FULL_PPN_BLOCKER_LEDGER_2890_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2890_delta_p_qRhat_or_beta_channel_NEXT.csv",
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
        ("SRC2890_0_2889_doc", SRC_2889_DOC, "NEXT2889_0_2890;MISSING_x_U_PROFILE_OR_DELTA_P", "2889 handoff"),
        ("SRC2890_1_2889_next", SRC_2889_NEXT, "NEXT2889_0_2890", "explicit 2890 target"),
        ("SRC2890_2_2889_kernel", SRC_2889_KERNEL, "PPNK2889_0_common_weyl_gamma;PPNK2889_1_CR_delta_p_combo", "common-Weyl kernel input"),
        ("SRC2890_3_2889_inputs", SRC_2889_INPUTS, "REQ2889_1_xU;MISSING_x_U_PROFILE_OR_DELTA_P", "x_U requirement"),
        ("SRC2890_4_2889_ppn", SRC_2889_PPN, "PPNG2889_0_gamma;PPNG2889_5_total_abs", "full PPN guard"),
        ("SRC2890_5_2889_validation", SRC_2889_VALIDATION, "VAL2889_OVERALL", "2889 validation"),
        ("SRC2890_6_1882_doc", SRC_1882_DOC, "x_U_CR = dC_R/du|0 = 2(p-1);FREE_PROFILE_ROUTE_REJECTED_FOR_CR_CHANNEL", "profile identity source"),
        ("SRC2890_7_1882_identity", SRC_1882_IDENTITY, "CRID1882_0_definitions;CRID1882_2_nonGR_residual", "C_R weak-field identity table"),
        ("SRC2890_8_1882_combo", SRC_1882_COMBO, "PCB1882_0_exact_combo;NO_CANCELLATION_GUARD_ACTIVE", "no-circularity combo guard"),
        ("SRC2890_9_1883_bridge", SRC_1883_BRIDGE, "DPB1883_1_QR_delta_p;delta_p=-q_R_hat/2", "delta_p/q_R_hat bridge"),
        ("SRC2890_10_1884_doc", SRC_1884_DOC, "NO_BOUNDARY_CHARGE_NOT_PARENT_DERIVED;delta_p=q_R_hat=0", "zero-flux checkpoint"),
        ("SRC2890_11_1884_audit", SRC_1884_AUDIT, "NBC1884_1_exact_zero_flux_lemma;NO_BOUNDARY_CHARGE_NOT_PARENT_DERIVED", "no-boundary audit"),
        ("SRC2890_12_1884_contract", SRC_1884_CONTRACT, "DPQR1884_1_qRhat;DPQR1884_6_descent_statuses", "delta_p/q_R_hat input contract"),
        ("SRC2890_13_1884_template", SRC_1884_TEMPLATE, "DPQR1884_TEMPLATE_FINITE_QRHAT;MISSING_NUMERIC_Q_R_HAT", "nonclaim input template"),
        ("SRC2890_14_2631_vector", SRC_2631_VECTOR, "PPNV2631_0_delta_p_qR;PPNV2631_8_total_abs", "full local PPN vector"),
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


def profile_law_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "XDP2890_0_CR_identity",
            "C_R/R_AB first-order profile",
            "C_R=ln(T^2 S), u=U/c^2, T^2=1-2u+O(u^2), S=1+2p u+O(u^2)",
            "C_R=2(p-1)u+O(u^2)",
            "x_U_CR=dC_R/du|0=2delta_p",
            "DERIVED_SYMBOLIC_PROFILE_LAW_NONCLAIM",
            "delta_p value/theorem-zero; source-normalized PPN gauge; full-vector closure",
        ),
        (
            "XDP2890_1_QR_bridge",
            "finite exterior reciprocal charge",
            "if C_R=-Q_R/r and q_R_hat=Q_R c^2/(GM_source) with same measured GM as U=GM/r",
            "C_R=-q_R_hat U/c^2",
            "x_U_CR=-q_R_hat and delta_p=-q_R_hat/2",
            "DERIVED_CONDITIONAL_QRHAT_PROFILE_BRIDGE_NONCLAIM",
            "Q_R value or no-boundary-charge zero theorem; GM convention; source body",
        ),
        (
            "XDP2890_2_zero_route",
            "local-GR reciprocal-lock route",
            "if Q_R=0, W>0, exterior J_R=0 and C_R(infinity)=0, then C_R=0",
            "C_R=0 through first PPN order",
            "x_U_CR=delta_p=q_R_hat=0",
            "EXACT_CONDITIONAL_ZERO_ROUTE_NOT_PARENT_SIGNED",
            "parent no-boundary-charge/source-descent signature",
        ),
        (
            "XDP2890_3_free_xU_rejection",
            "free x_U profile fit",
            "treat x_U as an independent fit coefficient while also using C_R=ln(T^2S)",
            "rejected for the C_R channel",
            "x_U_CR is tied to delta_p; it is not an independent escape hatch",
            "FREE_XU_ROUTE_REJECTED_FOR_CR_CHANNEL",
            "none for rejection; future q_loc tails must stay separate from C_R first-order profile",
        ),
        (
            "XDP2890_4_verdict",
            "x_U/delta_p/q_R_hat profile zero or value",
            "combine 1882 identity, 1883 bridge and 1884 zero-flux lemma",
            "profile law exists but zero/value is not parent-signed",
            "x_U_CR=2delta_p=-q_R_hat conditionally; numeric/source-backed row still missing",
            "PROFILE_LAW_DERIVED_VALUE_AND_ZERO_BLOCKED",
            "MISSING_PARENT_NO_BOUNDARY_CHARGE_OR_NUMERIC_QRHAT;MISSING_FULL_PPN_VECTOR",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for law_id, target, assumptions, derived_relation, profile_result, status, missing in specs:
        rows.append(
            add_common(
                {
                    "law_id": law_id,
                    "target": target,
                    "assumptions": assumptions,
                    "derived_relation": derived_relation,
                    "profile_result": profile_result,
                    "current_status": status,
                    "missing_for_claim": missing,
                    "parent_signed": False,
                    "theorem_zero_adopted": False,
                    "finite_value_present": False,
                    "prediction_source_backed": False,
                    "accepted_for_scoring": False,
                }
            )
        )
    return rows


def profile_input_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "profile_id": "PROF2890_0_live_xU_delta_p_qRhat",
                "route_type": "finite_or_parent_zero_profile_input",
                "symbols": "x_U_CR;delta_p;q_R_hat",
                "units": "dimensionless",
                "definition": "first-order coefficient of C_R=ln(T^2S) relative to u=U/c^2",
                "profile_law": "x_U_CR=2*delta_p; if exterior C_R=-Q_R/r and q_R_hat=Q_R c^2/(GM_source), then x_U_CR=-q_R_hat",
                "candidate_x_U_CR": "MISSING_NUMERIC_OR_PARENT_ZERO",
                "candidate_delta_p": "MISSING_NUMERIC_OR_PARENT_ZERO",
                "candidate_q_R_hat": "MISSING_NUMERIC_OR_PARENT_ZERO",
                "source_convention": "U=GM/r, u=U/c^2, same measured GM as q_R_hat=Q_R c^2/(G M_source)",
                "source_path": "MISSING_PARENT_ZERO_THEOREM_OR_SOURCE_BACKED_FINITE_QRHAT_ROW",
                "source_id": "MISSING_PARENT_SOURCE_OR_FINITE_SOURCE",
                "zero_theorem_status": "MISSING_PARENT_NO_BOUNDARY_CHARGE_SOURCE_DESCENT",
                "boundary_charge_status": "MISSING_BOUNDARY_CHARGE_ZERO_THEOREM",
                "source_descent_status": "MISSING_SOURCE_DESCENT",
                "matter_descent_status": "MISSING_MATTER_READOUT_DESCENT",
                "projection_status": "MISSING_ARENA_PROJECTION",
                "full_vector_status": "MISSING_BETA_BR_SOURCE_ENDPOINT_QLOC_CHANNELS",
                "current_status": "PROFILE_LAW_DERIVED_VALUE_MISSING_NONCLAIM",
                "closure_used": False,
                "comparator_only": False,
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
                "profile_id": "PROF2890_1_parent_zero_template",
                "route_type": "parent_zero_theorem_required",
                "symbols": "x_U_CR;delta_p;q_R_hat",
                "units": "dimensionless",
                "definition": "zero row allowed only when Q_R=0/source descent is parent-signed",
                "profile_law": "Q_R=0 plus exterior zero-flux lemma implies C_R=0, so x_U_CR=delta_p=q_R_hat=0",
                "candidate_x_U_CR": "0_IF_PARENT_SIGNED",
                "candidate_delta_p": "0_IF_PARENT_SIGNED",
                "candidate_q_R_hat": "0_IF_PARENT_SIGNED",
                "source_convention": "parent theorem route; measured GM still needed if scored",
                "source_path": "MISSING_PARENT_NO_BOUNDARY_CHARGE_SOURCE_DESCENT_THEOREM",
                "source_id": "MISSING_PARENT_ZERO_SOURCE",
                "zero_theorem_status": "UNSIGNED_CONDITIONAL_ZERO_ROUTE",
                "boundary_charge_status": "MISSING_BOUNDARY_CHARGE_ZERO_THEOREM",
                "source_descent_status": "MISSING_SOURCE_DESCENT",
                "matter_descent_status": "MISSING_MATTER_READOUT_DESCENT",
                "projection_status": "MISSING_ARENA_PROJECTION",
                "full_vector_status": "MISSING_FULL_VECTOR_CLOSURE",
                "current_status": "TEMPLATE_ONLY_NOT_A_VALUE_ROW",
                "closure_used": False,
                "comparator_only": False,
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
                "profile_id": "PROF2890_2_finite_qrhat_template",
                "route_type": "finite_qR_hat_required",
                "symbols": "x_U_CR;delta_p;q_R_hat",
                "units": "dimensionless",
                "definition": "finite charge row allowed only with real Q_R/GM source normalization",
                "profile_law": "x_U_CR=-q_R_hat and delta_p=-q_R_hat/2",
                "candidate_x_U_CR": "MISSING_NUMERIC_X_U_CR",
                "candidate_delta_p": "MISSING_NUMERIC_DELTA_P",
                "candidate_q_R_hat": "MISSING_NUMERIC_Q_R_HAT",
                "source_convention": "q_R_hat=Q_R c^2/(G M_source); M_source must match U=GM/r in PPN comparator",
                "source_path": "MISSING_SOURCE_BACKED_FINITE_QRHAT_ROW",
                "source_id": "MISSING_FINITE_QRHAT_SOURCE",
                "zero_theorem_status": "not_applicable",
                "boundary_charge_status": "finite_charge_branch_requires_Q_R_source",
                "source_descent_status": "finite_source_body_required",
                "matter_descent_status": "MISSING_MATTER_READOUT_DESCENT",
                "projection_status": "MISSING_ARENA_PROJECTION",
                "full_vector_status": "MISSING_FULL_VECTOR_CLOSURE",
                "current_status": "TEMPLATE_ONLY_NOT_A_VALUE_ROW",
                "closure_used": False,
                "comparator_only": False,
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


def kernel_update_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "update_id": "KUP2890_0_common_weyl_profile_substitution",
                "parent_kernel": "PPNK2889_0_common_weyl_gamma",
                "observable": "gamma_minus_1",
                "old_missing": "MISSING_x_U_PROFILE_OR_DELTA_P",
                "new_information": "x_U_CR is not free for the C_R channel: x_U_CR=2delta_p=-q_R_hat conditionally",
                "updated_shadow_formula": "s_R=b_R*x_U_CR=2*b_R*delta_p=-b_R*q_R_hat",
                "pure_shadow_gamma_formula": "gamma_minus_1=2*b_R*x_U_CR/(1-b_R*x_U_CR)",
                "combined_baseline_formula": "gamma_obs-1=(delta_p+4*b_R*delta_p)/(1-2*b_R*delta_p)=(-q_R_hat*(1+4*b_R)/2)/(1+b_R*q_R_hat)",
                "current_status": "PROFILE_SUBSTITUTION_READY_VALUES_MISSING_NONCLAIM",
                "missing_for_claim": "MISSING_b_R_VALUE_OR_ZERO;MISSING_delta_p_OR_q_R_hat_VALUE_OR_ZERO;MISSING_BETA_CHANNEL;MISSING_FULL_PPN_VECTOR",
                "comparison_ready": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        ),
        add_common(
            {
                "update_id": "KUP2890_1_no_free_bR_bound",
                "parent_kernel": "PPNK2889_1_CR_delta_p_combo",
                "observable": "gamma_obs_minus_1",
                "old_missing": "MISSING_delta_p_ZERO_OR_VALUE",
                "new_information": "Cassini constrains only the combined delta_p/q_R_hat and b_R expression; it does not bound b_R alone",
                "updated_shadow_formula": "leading gamma residual = delta_p*(1+4*b_R) = -q_R_hat*(1+4*b_R)/2",
                "pure_shadow_gamma_formula": "not enough for local GR because baseline p and beta/source channels remain open",
                "combined_baseline_formula": "score only after each PPN channel is theorem-zero or finite/source-backed",
                "current_status": "NO_CASSINI_AS_MTS_PREDICTION_NONCLAIM",
                "missing_for_claim": "MISSING_NO_CANCELLATION_IDENTITY;MISSING_FULL_VECTOR_VALUES",
                "comparison_ready": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        ),
    ]


def ppn_blocker_rows() -> list[dict[str, Any]]:
    specs = [
        ("PPNB2890_0_delta_p_qRhat", "delta_p;q_R_hat;x_U_CR", "gamma_minus_1;local_GR_Newton", "PROFILE_LAW_READY_VALUE_MISSING", "MISSING_PARENT_NO_BOUNDARY_CHARGE_OR_NUMERIC_QRHAT"),
        ("PPNB2890_1_bR", "b_R", "gamma_minus_1;clock_common_mode", "MISSING_b_R_VALUE_OR_ZERO", "MISSING_NO_WEYL_SLOT_THEOREM_OR_SOURCE_COEFFICIENT"),
        ("PPNB2890_2_beta", "Delta_beta_total_abs", "beta_minus_1;orbital_timing", "MISSING_BETA_RESPONSE_KERNEL_AND_SOURCE_NORMALIZED_VECTOR", "MISSING_SECOND_ORDER_FIELD_EQUATION"),
        ("PPNB2890_3_preferred_frame", "d_R;alpha_i;xi", "preferred_frame;preferred_location", "MISSING_DISFORMAL_PREFERRED_FRAME_PROJECTION", "MISSING_DISFORMAL_RESPONSE_MATRIX"),
        ("PPNB2890_4_source", "w_R;Delta_w", "measured_GM;WEP;source_normalization", "MISSING_SOURCE_PREFACTOR_ZERO_OR_FINITE_VECTOR", "MISSING_SOURCE_DESCENT_AND_COMPONENT_BASIS"),
        ("PPNB2890_5_endpoint_readout", "epsilon_endpoint_R;alpha_readout;delta_GM", "light_time;clock;orbital", "MISSING_ENDPOINT_READOUT_GAUGE_NORMALIZATION", "MISSING_ENDPOINT_SILENCE_AND_GM_MAP"),
        ("PPNB2890_6_q_loc_Khat", "q_loc^nu;Khat^{mu nu}", "beta;clock;orbital;local_GR_Newton", "MISSING_QLOC_WARD_ZERO_PROFILE_OR_FINITE_KERNEL", "MISSING_WARD_ZERO_THROUGH_OU2"),
        ("PPNB2890_7_total_abs", "Delta_PPN_abs", "all_PPN;local_GR_Newton", "SCHEMA_READY_VALUES_MISSING", "MISSING_ALL_COMPONENT_VALUES_OR_THEOREM_ZEROS"),
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
        ("GATE2890_0_profile_law", "x_U_CR profile relation is derived", "PASS_NONCLAIM", "x_U_CR=2delta_p and x_U_CR=-q_R_hat conditionally"),
        ("GATE2890_1_profile_value", "x_U/delta_p/q_R_hat has a parent zero or finite value", "FAIL", "no parent no-boundary-charge theorem or finite q_R_hat row exists"),
        ("GATE2890_2_no_free_fit", "x_U is treated as an independent fitted knob", "FAIL_AS_ROUTE", "free x_U is rejected for the C_R channel"),
        ("GATE2890_3_prediction", "MTS gamma prediction is numeric/source-backed", "FAIL", "b_R and delta_p/q_R_hat remain missing"),
        ("GATE2890_4_full_ppn", "full PPN vector is closed", "FAIL", "beta, source, preferred-frame, endpoint, readout and q_loc channels remain open"),
        ("GATE2890_5_claim", "local GR/Newton limit is claimed", "FAIL", "profile law alone is not a local-GR derivation"),
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
                "runner_id": "RUN2890_0_profile_kernel_runner",
                "status": "REFUSED_PROFILE_VALUES_AND_FULL_PPN_MISSING",
                "accepted_zero_theorems": 0,
                "accepted_profile_rows": 0,
                "accepted_predictions": 0,
                "reason": "profile law is symbolic/nonclaim; no numeric or parent-zero delta_p/q_R_hat row, no b_R row, and no full PPN vector closure",
                "runner_ready": False,
                "claim_unlocked": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2890_0_profile", "INSTALL_XU_DELTA_P_QRHAT_PROFILE_LAW_NONCLAIM", "x_U_CR=2delta_p=-q_R_hat conditionally follows from existing weak-field and exterior-charge bridges", "use this as the only C_R first-order profile interface"),
        ("DEC2890_1_reject_free_xU", "REJECT_FREE_XU_FITTING_ROUTE", "free x_U would double-count the same delta_p/reciprocal-lock failure that the PPN gamma channel measures", "keep q_loc screened-tail route separate from C_R profile route"),
        ("DEC2890_2_value", "DO_NOT_SCORE_PROFILE_YET", "zero theorem and finite q_R_hat row are both missing", "leave all profile rows nonclaim"),
        ("DEC2890_3_next", "SELECT_QRHAT_ZERO_OR_SOURCE_ROW_NEXT", "the next leap is not another gamma algebra pass; it is Q_R ownership/source value or the beta/source channel", "derive no-boundary-charge/source descent or fill a real q_R_hat row next"),
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
                "next_id": "NEXT2890_0_2891",
                "status": "selected_primary",
                "target_doc": "2891-Y5-R2FR-no-boundary-charge-source-descent-or-qRhat-row-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_no_boundary_charge_source_descent_or_qRhat_row_under_AX1090_2891.py",
                "mission": "try to parent-sign Q_R=0/source descent for q_R_hat=delta_p=x_U_CR=0; if it fails, fill a real source-normalized finite q_R_hat row or keep the local branch blocked",
                "forbidden_shortcuts": "no free x_U fit; no Cassini-as-prediction; no closure zero; no gamma-only local-GR claim; no cancellation; no GitHub action",
                "selected": True,
                "accepted_for_scoring": False,
            }
        ),
        add_common(
            {
                "next_id": "NEXT2890_1_held_beta",
                "status": "held_secondary",
                "target_doc": "2891b-Y5-R2FR-beta-source-normalized-second-order-kernel-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_beta_source_normalized_second_order_kernel_under_AX1090_2891b.py",
                "mission": "attack beta/source normalization once the q_R_hat route is either parent-zero or explicitly nonclaim",
                "forbidden_shortcuts": "do not infer beta=1 from gamma algebra",
                "selected": False,
                "accepted_for_scoring": False,
            }
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("BR2890_0_profile_copy", OUTPUTS["profile_input"], BRANCH_OUTPUTS["profile_copy"], "local-bounds copy of x_U/delta_p/q_R_hat profile input row"),
        ("BR2890_1_kernel_copy", OUTPUTS["kernel_update"], BRANCH_OUTPUTS["kernel_copy"], "source-weight copy of common-Weyl kernel update"),
        ("BR2890_2_ppn_copy", OUTPUTS["ppn_blockers"], BRANCH_OUTPUTS["ppn_copy"], "beta-source docs copy of full PPN blocker ledger"),
        ("BR2890_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue next target"),
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
        "theorem_zero_adopted",
        "finite_value_present",
        "prediction_source_backed",
        "accepted_for_scoring",
        "gate_passed",
        "runner_ready",
        "claim_unlocked",
        "comparison_ready",
        "full_vector_ready",
        "selected_claim_path",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    profile_law = rows_by_name["profile_law"]
    profile_input = rows_by_name["profile_input"]
    kernel_update = rows_by_name["kernel_update"]
    ppn_blockers = rows_by_name["ppn_blockers"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    checks = [
        ("VAL2890_0_sources_exist", all(row["path_exists"] for row in sources), "all registered source paths exist"),
        ("VAL2890_1_source_anchors", all(row["anchors_found"] for row in sources), "all registered source anchors were found"),
        ("VAL2890_2_profile_law", any(row["current_status"] == "PROFILE_LAW_DERIVED_VALUE_AND_ZERO_BLOCKED" for row in profile_law), "x_U/delta_p/q_R_hat profile law is derived but value/zero remains blocked"),
        ("VAL2890_3_free_xU_rejected", any(row["current_status"] == "FREE_XU_ROUTE_REJECTED_FOR_CR_CHANNEL" for row in profile_law), "free x_U route is rejected for C_R"),
        ("VAL2890_4_profile_row_nonclaim", profile_input[0]["current_status"] == "PROFILE_LAW_DERIVED_VALUE_MISSING_NONCLAIM" and "MISSING" in profile_input[0]["candidate_q_R_hat"], "live profile row remains missing/nonclaim"),
        ("VAL2890_5_kernel_update", all(row["comparison_ready"] is False for row in kernel_update) and "2*b_R*delta_p" in kernel_update[0]["updated_shadow_formula"] and "q_R_hat" in kernel_update[0]["updated_shadow_formula"], "kernel update substitutes x_U_CR=2delta_p=-q_R_hat but cannot score"),
        ("VAL2890_6_full_ppn_blockers", len(ppn_blockers) == 8 and any(row["blocker_id"] == "PPNB2890_7_total_abs" for row in ppn_blockers), "full PPN blocker ledger remains active"),
        ("VAL2890_7_gates_fail_closed", all(row["gate_passed"] is False for row in gates), "acceptance gates fail closed"),
        ("VAL2890_8_runner_refused", runner[0]["status"] == "REFUSED_PROFILE_VALUES_AND_FULL_PPN_MISSING" and runner[0]["runner_ready"] is False, "runner remains refused"),
        ("VAL2890_9_next_target_2891", next_target[0]["next_id"] == "NEXT2890_0_2891" and next_target[0]["selected"] is True, "2891 q_R_hat/no-boundary route selected"),
        ("VAL2890_10_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2890_11_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2890_12_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2890_13_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2890_14_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2890_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2890_16_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2890_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2890 derived the C_R first-order profile law x_U_CR=2delta_p=-q_R_hat conditionally, rejected free x_U fitting, kept all local-GR/PPN claims blocked, and selected q_R_hat no-boundary/source descent for 2891.",
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
    text = f"""# 2890 - Y5 R2FR xU Delta-p Profile Zero Or Source Row Under AX1090

Status: `Y5_R2FR_2890_xU_profile_law_derived_value_blocked_qRhat_2891_next`

## Private Verdict

2890 is a useful tightening pass, not a local-GR win.

The `C_R` first-order profile is no longer allowed to float as an independent escape knob. From the existing weak-field identity,

`C_R=ln(T^2S)`, `u=U/c^2`, `T^2=1-2u+O(u^2)`, `S=1+2p u+O(u^2)`, so `C_R=2(p-1)u+O(u^2)`.

Therefore `x_U_CR=dC_R/du|0=2delta_p`. Combining the finite exterior charge bridge gives `delta_p=-q_R_hat/2`, hence `x_U_CR=-q_R_hat` when `C_R=-Q_R/r` and `q_R_hat=Q_R c^2/(GM_source)`.

That is the good news: the profile law is sharper. The hard news is the same health bar: `delta_p/q_R_hat` is not zero or numeric until the parent no-boundary-charge/source-descent theorem is signed, or a real source-normalized finite `q_R_hat` row exists. No Cassini/local-GR/PPN claim is allowed.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## xU Delta-p Profile Law

{md_table(rows_by_name["profile_law"], ["law_id", "target", "derived_relation", "profile_result", "current_status", "missing_for_claim", "valid_for_claim"])}

## Profile Input Row

{md_table(rows_by_name["profile_input"], ["profile_id", "route_type", "symbols", "units", "profile_law", "candidate_x_U_CR", "candidate_delta_p", "candidate_q_R_hat", "current_status", "valid_for_claim"])}

## Common-Weyl Kernel Update

{md_table(rows_by_name["kernel_update"], ["update_id", "parent_kernel", "new_information", "updated_shadow_formula", "combined_baseline_formula", "current_status", "valid_for_claim"])}

## Full PPN Blocker Ledger

{md_table(rows_by_name["ppn_blockers"], ["blocker_id", "symbols", "observable_targets", "current_status", "missing_for_claim", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "accepted_zero_theorems", "accepted_profile_rows", "reason", "runner_ready", "valid_for_claim"])}

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
        "profile_law": profile_law_rows(),
        "profile_input": profile_input_rows(),
        "kernel_update": kernel_update_rows(),
        "ppn_blockers": ppn_blocker_rows(),
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
    overall = next(row for row in validation if row["validation_id"] == "VAL2890_OVERALL")
    print(f"VAL2890_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
