from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1418-Y5-R10-RAB-action-scale-current-owner-lock-or-qbar-source-weight-acquisition-ledger.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1418_SOURCE_REGISTER.csv"
LOCK_ATTEMPT_PATH = SRC_DIR / "P8_Y5_R10_1418_ACTION_SCALE_CURRENT_OWNER_LOCK_ATTEMPT.csv"
GAUGE_TEST_PATH = SRC_DIR / "P8_Y5_R10_1418_GAUGE_QUOTIENT_TEST_MATRIX.csv"
QBAR_ARENA_PATH = SRC_DIR / "P8_Y5_R10_1418_QBAR_SOURCE_WEIGHT_ARENA_ACQUISITION_LEDGER.csv"
PROJECTION_GATE_PATH = SRC_DIR / "P8_Y5_R10_1418_PROJECTION_REQUIREMENT_GATE.csv"
DECISION_PATH = SRC_DIR / "P8_Y5_R10_1418_DECISION_LEDGER.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1418_CLAIM_GATE.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1418_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1418_VALIDATION.csv"

GENERATED_UTC = datetime.now(timezone.utc).isoformat()
STATUS = "Y5_R10_1418_action_scale_current_owner_lock_not_proved_qbar_arena_acquisition_ledger_written_nonclaim"
CLAIM_CEILING = (
    "action_scale_current_owner_lock_attempt_and_qbar_source_weight_acquisition_only_"
    "no_qbar_zero_no_WEP_pass_no_Newton_no_R10_no_PPN_no_local_GR_pass"
)


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def write_csv(relative_path: Path, rows: list[dict[str, Any]]) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {relative_path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def anchor_found(relative_path: str, anchor: str) -> bool:
    path = ROOT / relative_path
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC1418_0_1417_doc",
            "source_path": "1417-Y5-R10-RAB-parent-object-language-constructor-exhaustion-or-qbar-source-acquisition.md",
            "anchor": "NEXT1417_0_1418",
            "role": "prior checkpoint selecting action-scale/current-owner lock",
        },
        {
            "source_id": "SRC1418_1_1417_qbar",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1417_QBAR_SOURCE_WEIGHT_ACQUISITION_ROWS.csv",
            "anchor": "QSA1417_0_qbar_source_weight",
            "role": "qbar_source_weight finite acquisition row",
        },
        {
            "source_id": "SRC1418_2_1067_action_owner",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv",
            "anchor": "ASO1067_5_verdict",
            "role": "action-scale owner conditional not parent-derived",
        },
        {
            "source_id": "SRC1418_3_1067_hbar_measure",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv",
            "anchor": "HMO1067_4_verdict",
            "role": "single hbar/measure/current owner not derived",
        },
        {
            "source_id": "SRC1418_4_1067_consequence",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1067_SOURCE_WEIGHT_CONSEQUENCE_LEDGER.csv",
            "anchor": "SWC1067_4_verdict",
            "role": "relative action-scale branch remains live",
        },
        {
            "source_id": "SRC1418_5_1066_source_scalar",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
            "anchor": "SSE1066_5_verdict",
            "role": "source-scalar exclusion conditional theorem only",
        },
        {
            "source_id": "SRC1418_6_1066_measure_quantum",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv",
            "anchor": "FMQ1066_4_verdict",
            "role": "field/measure/quantum normalization closure not parent-signed",
        },
        {
            "source_id": "SRC1418_7_1415_current",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1415_SOURCE_CURRENT_OWNER_ATTEMPT.csv",
            "anchor": "SCO1415_6_verdict",
            "role": "source-current owner not derived",
        },
        {
            "source_id": "SRC1418_8_1068_tau_pack",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_TAU_WEP_ACQUISITION_PACK.csv",
            "anchor": "TAP1068_6_direct_product_fallback",
            "role": "WEP projection ingredients remain missing",
        },
        {
            "source_id": "SRC1418_9_1068_worldtube",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv",
            "anchor": "SWT1068_5_verdict",
            "role": "source worldtube requirements for finite WEP branch",
        },
        {
            "source_id": "SRC1418_10_1068_force",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_OBSERVED_FRAME_FORCE_MAP.csv",
            "anchor": "FRM1068_5_verdict",
            "role": "observed-frame force/readout map not derived",
        },
        {
            "source_id": "SRC1418_11_local_bounds",
            "source_path": "source-intake/local_bounds/local_bound_claims.csv",
            "anchor": "R1_WEP_source_charge",
            "role": "local WEP source-charge bound anchor",
        },
        {
            "source_id": "SRC1418_12_R10_bound",
            "source_path": "source-intake/local_bounds/local_bound_claims.csv",
            "anchor": "R10_fifth_force",
            "role": "R10 fifth-force symbolic bound anchor",
        },
        {
            "source_id": "SRC1418_13_PPN_gamma",
            "source_path": "source-intake/local_bounds/local_bound_claims.csv",
            "anchor": "R3_gamma",
            "role": "PPN gamma bound anchor",
        },
        {
            "source_id": "SRC1418_14_Gdot",
            "source_path": "source-intake/local_bounds/local_bound_claims.csv",
            "anchor": "R9_Gdot",
            "role": "Newton/orbital Gdot bound anchor",
        },
    ]
    for row in rows:
        row["path_exists"] = (ROOT / row["source_path"]).exists()
        row["anchor_found"] = anchor_found(row["source_path"], row["anchor"])
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def lock_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "lock_id": "ACL1418_0_target_lock",
            "lock_piece": "single action-scale/current-owner lock",
            "required_statement": "one parent hbar/action measure/current owner fixes ordinary matter weights and source currents before readout",
            "formal_effect": "w_A S_A and J_A -> c_A J_A are absent, common-mode only, or gauge/quotient redundant",
            "current_result": "TARGET_EXACT",
            "missing_for_claim": "parent derivation of action measure, hbar/statistical weight, source current, and readout descent",
            "if_signed": "qbar_source_weight and current_rescaling become theorem-zero/common-mode",
            "if_unsigned": "qbar_source_weight acquisition ledger is mandatory",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "lock_id": "ACL1418_1_classical_not_enough",
            "lock_piece": "classical field equations",
            "required_statement": "multiplying S_A by w_A must be redundant for equations, Hilbert source, and quantum measure",
            "formal_effect": "rules out treating w_A as harmless EOM scaling only",
            "current_result": "OBSTRUCTION_EXPLICIT",
            "missing_for_claim": "ASO1067_1 shows delta(w_A S_A)/delta g_obs = w_A T_A",
            "if_signed": "classical redundancy would be upgraded to full source/measure redundancy",
            "if_unsigned": "w_A remains physically active in source sector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "lock_id": "ACL1418_2_hbar_measure_owner",
            "lock_piece": "hbar_parent and Dmu_parent",
            "required_statement": "one action quantum/statistical measure covers all ordinary matter sectors with species-blind Jacobian",
            "formal_effect": "species-dependent effective hbar_A or measure factors cannot mimic source weights",
            "current_result": "OWNER_NOT_DERIVED",
            "missing_for_claim": "HMO1067_0/HMO1067_1/HMO1067_4 remain not_parent_owned",
            "if_signed": "relative action-scale branch collapses to common calibration",
            "if_unsigned": "measure/action-weight residual remains live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "lock_id": "ACL1418_3_current_owner",
            "lock_piece": "Noether/current/source normalization owner",
            "required_statement": "same parent owner fixes matter current, charge labels, and active source normalization",
            "formal_effect": "J_A -> c_A J_A and beta_source,A cannot re-enter as source-only coefficients",
            "current_result": "MISSING_CURRENT_OWNER",
            "missing_for_claim": "SCO1415_3 and HMO1067_2 remain candidate_missing",
            "if_signed": "current_rescaling_residual becomes theorem-owned/common-mode",
            "if_unsigned": "current rescaling remains a finite R_source component",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "lock_id": "ACL1418_4_variation_before_readout",
            "lock_piece": "source variation before projection/readout",
            "required_statement": "T_total is varied from S_matter before material labels, source worldtube, clocks, or instrument readout are applied",
            "formal_effect": "post-variation species/source selectors cannot manufacture kappa_A",
            "current_result": "CONDITIONAL_CLEAN_UNSIGNED",
            "missing_for_claim": "readout/EFT transfer closure and source-worldtube projection remain missing",
            "if_signed": "source labels are forgotten before local tests",
            "if_unsigned": "kappa_A source map remains live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "lock_id": "ACL1418_5_readout_transfer",
            "lock_piece": "readout/EFT preservation of owner lock",
            "required_statement": "effective actions, clocks, WEP/R10/PPN projections preserve the same source/current owner",
            "formal_effect": "a bare action theorem-zero transfers to observables",
            "current_result": "UNSIGNED_TRANSFER_GATE",
            "missing_for_claim": "TAP1068/FRM1068 projection data and radiative/readout closure",
            "if_signed": "local-source branches can use theorem-zero in tests",
            "if_unsigned": "arena-specific finite projections are required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "lock_id": "ACL1418_6_verdict",
            "lock_piece": "action-scale/current-owner lock",
            "required_statement": "ACL1418_1 through ACL1418_5 all close from parent MTS action",
            "formal_effect": "qbar_source_weight=0/current_rescaling=0 by theorem, modulo common calibration",
            "current_result": "LOCK_NOT_PROVED_CURRENT_CORPUS",
            "missing_for_claim": "action measure, hbar, current owner, variation/readout transfer are unsigned",
            "if_signed": "local GR source-side reduction reopens as theorem route",
            "if_unsigned": "write qbar_source_weight arena acquisition ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def gauge_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "test_id": "GQT1418_0_common_weight",
            "candidate_redundancy": "w_A = w_common for all ordinary species",
            "test": "can be absorbed only as universal calibration if measured-G/common-mode guards pass",
            "result": "POSSIBLE_COMMON_MODE_ONLY",
            "residual_if_failed": "none for relative WEP, but common calibration cannot hide relative weights",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "GQT1418_1_relative_weight",
            "candidate_redundancy": "w_A = w_common(1+epsilon_A)",
            "test": "must be removable from Hilbert source, quantum measure, interactions, and readout simultaneously",
            "result": "NOT_GAUGE_PROVED",
            "residual_if_failed": "qbar_source_weight / Delta_w_AB",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "GQT1418_2_field_rescaling",
            "candidate_redundancy": "Psi_A -> Z_A^(1/2) Psi_A",
            "test": "canonical kinetic terms, measured masses/charges, composite material parameters, Hilbert source, and measure remain unchanged",
            "result": "INSUFFICIENT_WITHOUT_CURRENT_MEASURE_OWNER",
            "residual_if_failed": "current_rescaling_residual and qbar_source_weight",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "GQT1418_3_current_rescaling",
            "candidate_redundancy": "J_A -> c_A J_A",
            "test": "same T_Q/Noether owner fixes current normalization before source/readout projection",
            "result": "NOT_GAUGE_PROVED",
            "residual_if_failed": "current_rescaling_residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "GQT1418_4_measure_jacobian",
            "candidate_redundancy": "species-dependent measure/coframe Jacobian",
            "test": "measure and coframe descent are species blind and boundary silent",
            "result": "PARALLEL_OPEN_GATE",
            "residual_if_failed": "measure_source_weight",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "GQT1418_5_verdict",
            "candidate_redundancy": "all source weights are gauge/quotient artifacts",
            "test": "GQT1418_0 through GQT1418_4 close",
            "result": "GAUGE_QUOTIENT_NOT_PROVED",
            "residual_if_failed": "qbar_source_weight arena acquisition remains mandatory",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def qbar_arena_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena_row_id": "QAA1418_0_WEP_source_charge",
            "arena": "WEP_source_charge / MICROSCOPE Ti-Pt",
            "empirical_anchor": "source-intake/local_bounds/local_bound_claims.csv::R1_WEP_source_charge",
            "bound_summary": "|eta_WEP_source_charge| <= 2.8e-15 proxy anchor",
            "prediction_needed": "P_WEP_source = direct parent eta_AB residual OR abs(qbar_source_weight * tau_WEP * material/source contrast)",
            "required_inputs": "qbar_source_weight value/theorem-zero; source worldtube; material tensor; orbit/readout kernel; eta sign convention; no measured-G absorption",
            "current_status": "BOUND_ANCHOR_EXISTS_PROJECTION_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_row_id": "QAA1418_1_Newton_GM_orbital",
            "arena": "Newton_GM / orbital source normalization",
            "empirical_anchor": "source-intake/local_bounds/local_bound_claims.csv::R9_Gdot",
            "bound_summary": "Gdot/G anchor exists; not a direct relative source-weight bound",
            "prediction_needed": "separate universal GM calibration from relative kappa_A/source-weight component in orbital dynamics",
            "required_inputs": "source composition/profile; common-mode calibration proof; time/range dependence of qbar_source_weight; orbital observable projection",
            "current_status": "ANCHOR_EXISTS_DIRECT_QBAR_MAP_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_row_id": "QAA1418_2_R10_fifth_force",
            "arena": "R10 inverse-square / short range",
            "empirical_anchor": "source-intake/local_bounds/local_bound_claims.csv::R10_fifth_force",
            "bound_summary": "alpha(lambda) symbolic curve required",
            "prediction_needed": "alpha_qbar(lambda) from qbar_source_weight, mediator/profile kernel, source/test composition, and range lambda",
            "required_inputs": "real alpha(lambda) curve; lambda convention; K_X kernel; qbar_source coefficient; source/test material map; no tau=1 shortcut",
            "current_status": "BOUND_SYMBOLIC_AND_QBAR_COEFFICIENT_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_row_id": "QAA1418_3_PPN_gamma_beta",
            "arena": "PPN gamma/beta and local metric response",
            "empirical_anchor": "source-intake/local_bounds/local_bound_claims.csv::R3_gamma",
            "bound_summary": "Cassini gamma anchor exists; beta and preferred-frame anchors also exist in local_bound_claims",
            "prediction_needed": "map source-current residual into weak-field metric potentials and PPN residual vector",
            "required_inputs": "parent weak-field equations; source-current owner or finite residual coefficients; projection to gamma,beta,alpha_i,xi; units/signs",
            "current_status": "PPN_PROJECTION_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_row_id": "QAA1418_4_local_GR_limit",
            "arena": "local_GR / Newtonian limit",
            "empirical_anchor": "source-intake/local_bounds/local_bound_claims.csv::R11_EH_operator_ledger",
            "bound_summary": "internal operator-ledger anchor, not empirical pass",
            "prediction_needed": "show qbar_source_weight and current_rescaling vanish or enter retained residual vector below local bounds",
            "required_inputs": "EH reduction; Bianchi/conservation check; source-current theorem; retained residual vector with no-cancellation norm",
            "current_status": "LOCAL_GR_SOURCE_SIDE_REDUCTION_BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_row_id": "QAA1418_5_clock_readout_guard",
            "arena": "clock/readout cross-check",
            "empirical_anchor": "source-intake/local_bounds/local_bound_claims.csv::R2_clock_redshift",
            "bound_summary": "clock/redshift anchor exists but cannot screen WEP/source residual",
            "prediction_needed": "prove readout constants share the same action/current owner or retain separate clock residual",
            "required_inputs": "hbar*c/clock normalization; readout transfer; no using clock agreement as WEP source pass",
            "current_status": "GUARD_ONLY_NOT_SOURCE_PASS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_row_id": "QAA1418_6_verdict",
            "arena": "all qbar_source_weight arenas",
            "empirical_anchor": "QAA1418_0 through QAA1418_5",
            "bound_summary": "anchors exist in several arenas, but no qbar prediction is score-ready",
            "prediction_needed": "theorem-zero from ACL1418_6 or finite sourced coefficient plus arena projections",
            "required_inputs": "value/bound, uncertainty, units, sign, parent basis, source path, arena projection, no-cancellation envelope",
            "current_status": "QBAR_ARENA_LEDGER_SOURCE_READY_BUT_UNSCORED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def projection_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PRG1418_0_theorem_zero_gate",
            "gate": "qbar_source_weight=0 by theorem",
            "opens_if": "ACL1418_6 result becomes LOCK_PROVED and readout transfer signed",
            "current_status": "CLOSED_LOCK_NOT_PROVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PRG1418_1_numeric_gate",
            "gate": "finite qbar_source_weight can be scored",
            "opens_if": "QAA1418 rows have value/bound, uncertainty, units, sign convention, parent basis, source path, and arena projection",
            "current_status": "CLOSED_VALUES_AND_PROJECTIONS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PRG1418_2_no_absorption_gate",
            "gate": "no fake measured-G absorption",
            "opens_if": "common-mode source normalization is separated from relative source weights in Newton/WEP/R10 projections",
            "current_status": "GUARD_ACTIVE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PRG1418_3_no_tau_shortcut",
            "gate": "no tau=1 or cancellation shortcut",
            "opens_if": "direct parent product or sourced projection functional replaces arbitrary tau choices",
            "current_status": "GUARD_ACTIVE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PRG1418_4_overall",
            "gate": "local/source qbar claim gate",
            "opens_if": "PRG1418_0 or PRG1418_1 opens and PRG1418_2/3 guards are satisfied",
            "current_status": "ALL_QBAR_SOURCE_CLAIMS_BLOCKED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1418_0_lock_verdict",
            "decision": "do not promote action-scale/current-owner lock",
            "reason": "single hbar/measure owner, source-current owner, and readout transfer remain unsigned",
            "next_action": "keep lock as exact conditional theorem target",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1418_1_acquisition_verdict",
            "decision": "qbar_source_weight is now arena-ledgered, not just named",
            "reason": "WEP/Newton/R10/PPN/local_GR each need different projection ingredients",
            "next_action": "choose direct parent variation product or build projection matrix",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1418_2_best_next",
            "decision": "target direct source-variation product or qbar projection matrix next",
            "reason": "this avoids arbitrary tau splits and makes the finite branch testable if theorem-zero keeps failing",
            "next_action": "derive P_arena directly from parent variation; if not, write qbar projection matrix rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1418_0_lock_claim",
            "claim": "single parent action-scale/current-owner lock is proved",
            "allowed": False,
            "reason": "ACL1418_6 is LOCK_NOT_PROVED_CURRENT_CORPUS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1418_1_qbar_zero",
            "claim": "qbar_source_weight=0",
            "allowed": False,
            "reason": "the lock and constructor-exhaustion theorem remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1418_2_qbar_bound",
            "claim": "qbar_source_weight is empirically bounded/scored",
            "allowed": False,
            "reason": "arena ledger has anchors but lacks prediction coefficients/projections",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1418_3_local_source_pass",
            "claim": "WEP/Newton/R10/PPN/local-GR source-side pass",
            "allowed": False,
            "reason": CLAIM_CEILING,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1418_0_1419",
            "target_doc": "1419-Y5-R10-RAB-direct-source-variation-product-or-qbar-projection-matrix.md",
            "target_script": "scripts/Y5_R10_RAB_direct_source_variation_product_or_qbar_projection_matrix.py",
            "task": "try to derive direct P_arena source residuals from parent variation, avoiding arbitrary tau splits; if it fails, build the qbar_source_weight projection matrix for WEP/Newton/R10/PPN/local_GR",
            "success_condition": "direct parent variation gives theorem-zero/numeric P_arena, or projection matrix rows specify coefficients, units, signs, anchors, and blocked inputs without claims",
            "do_not_claim": "WEP pass; R10 pass; local-GR pass; qbar_source_weight=0; tau=1 shortcut",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "next_id": "NEXT1418_1_data_parallel",
            "target_doc": "future-local-bound-source-weight-acquisition.md",
            "target_script": "future_source_row_route",
            "task": "acquire source/profile/readout inputs only after the projection matrix says which data are actually needed",
            "success_condition": "every acquired datum has source path, units, sign convention, uncertainty, and arena role",
            "do_not_claim": "source files alone as MTS prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    lock_attempt: list[dict[str, Any]],
    gauge_tests: list[dict[str, Any]],
    qbar_arenas: list[dict[str, Any]],
    projection_gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        LOCK_ATTEMPT_PATH,
        GAUGE_TEST_PATH,
        QBAR_ARENA_PATH,
        PROJECTION_GATE_PATH,
        DECISION_PATH,
        CLAIM_GATE_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "detail": detail,
                "generated_utc": GENERATED_UTC,
            }
        )

    add(
        "VAL1418_0_sources",
        all(row["path_exists"] and row["anchor_found"] for row in sources),
        "all cited local source paths exist and anchors are present",
    )
    add(
        "VAL1418_1_lock_attempt",
        any(row["lock_id"] == "ACL1418_6_verdict" and row["current_result"] == "LOCK_NOT_PROVED_CURRENT_CORPUS" for row in lock_attempt),
        "action-scale/current-owner lock attempt fails honestly",
    )
    add(
        "VAL1418_2_gauge_tests",
        any(row["test_id"] == "GQT1418_5_verdict" and row["result"] == "GAUGE_QUOTIENT_NOT_PROVED" for row in gauge_tests),
        "gauge/quotient route is not promoted",
    )
    add(
        "VAL1418_3_qbar_arena_rows",
        {"QAA1418_0_WEP_source_charge", "QAA1418_1_Newton_GM_orbital", "QAA1418_2_R10_fifth_force", "QAA1418_3_PPN_gamma_beta", "QAA1418_4_local_GR_limit"}.issubset({row["arena_row_id"] for row in qbar_arenas})
        and all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in qbar_arenas),
        "qbar_source_weight arena acquisition rows exist and remain nonclaim",
    )
    add(
        "VAL1418_4_projection_gates",
        any(row["gate_id"] == "PRG1418_4_overall" and row["current_status"] == "ALL_QBAR_SOURCE_CLAIMS_BLOCKED" for row in projection_gates),
        "projection gates keep all qbar source claims blocked",
    )
    add(
        "VAL1418_5_claim_refusal",
        all(row["allowed"] is False and row["claim_allowed"] is False for row in claim_gates),
        "lock, qbar zero, qbar bound, and local-source pass claims are refused",
    )
    add(
        "VAL1418_6_decision",
        any(row["decision_id"] == "DEC1418_2_best_next" and "direct source-variation product" in row["decision"] for row in decisions),
        "decision ledger selects direct source-variation product or projection matrix next",
    )
    add(
        "VAL1418_7_next_target",
        any(row["next_id"] == "NEXT1418_0_1419" for row in next_targets),
        "next target 1419 is staged",
    )
    add(
        "VAL1418_8_scope",
        all((ROOT / path).resolve().is_relative_to(ROOT.resolve()) for path in output_paths),
        "outputs are confined to post-checkpoint-work paths",
    )
    add(
        "VAL1418_9_overall",
        True,
        "1418 fails the action-scale/current-owner lock and writes qbar_source_weight arena acquisition ledger as nonclaim",
    )
    if any(row["status"] == "FAIL" for row in rows):
        for row in rows:
            if row["check_id"] == "VAL1418_9_overall":
                row["status"] = "FAIL"
                row["detail"] = "one or more 1418 validation checks failed"
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    lock_attempt: list[dict[str, Any]],
    gauge_tests: list[dict[str, Any]],
    qbar_arenas: list[dict[str, Any]],
    projection_gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    doc = f"""# 1418 - Action-Scale Current-Owner Lock Or qbar_source_weight Acquisition Ledger

**Current verdict:** the action-scale/current-owner lock is not proved. The conditional theorem is sharp: one parent hbar/action measure/current owner would make `w_A S_A`, `kappa_A`, and `J_A -> c_A J_A` absent or common-mode. The present corpus does not yet derive that owner, so `qbar_source_weight` cannot be set to zero.

**Discipline move:** the finite branch is now arena-ledgered. WEP, Newton/GM, R10, PPN, local-GR, and clock/readout guards each list the exact missing prediction/projection ingredients. Bounds exist in several arenas, but no MTS source-weight prediction is score-ready.

**Status:** `{STATUS}`

## Source Register

{md_table(sources)}

## Action-Scale / Current-Owner Lock Attempt

{md_table(lock_attempt)}

## Gauge / Quotient Test Matrix

{md_table(gauge_tests)}

## qbar_source_weight Arena Acquisition Ledger

{md_table(qbar_arenas)}

## Projection Requirement Gate

{md_table(projection_gates)}

## Decision Ledger

{md_table(decisions)}

## Claim Gate

{md_table(claim_gates)}

## Next Target

{md_table(next_targets)}

## Validation

{md_table(validations)}
"""
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    lock_attempt = lock_attempt_rows()
    gauge_tests = gauge_test_rows()
    qbar_arenas = qbar_arena_rows()
    projection_gates = projection_gate_rows()
    decisions = decision_rows()
    claim_gates = claim_gate_rows()
    next_targets = next_target_rows()
    validations = validation_rows(
        sources,
        lock_attempt,
        gauge_tests,
        qbar_arenas,
        projection_gates,
        decisions,
        claim_gates,
        next_targets,
    )

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(LOCK_ATTEMPT_PATH, lock_attempt)
    write_csv(GAUGE_TEST_PATH, gauge_tests)
    write_csv(QBAR_ARENA_PATH, qbar_arenas)
    write_csv(PROJECTION_GATE_PATH, projection_gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATE_PATH, claim_gates)
    write_csv(NEXT_TARGET_PATH, next_targets)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, lock_attempt, gauge_tests, qbar_arenas, projection_gates, decisions, claim_gates, next_targets, validations)

    if any(row["status"] != "PASS" for row in validations):
        raise SystemExit("1418 validation failed")

    print(STATUS)


if __name__ == "__main__":
    main()
