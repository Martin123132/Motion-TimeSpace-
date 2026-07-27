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
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2884-Y5-R2FR-Z-physical-lock-map-or-first-DqZ-factor-source-row-under-AX1090.md"

SRC_2883_DOC = ROOT / "2883-Y5-R2FR-constraint-first-q-construction-or-Dq-leak-source-pack-under-AX1090.md"
SRC_2883_NEXT = RESIDUALS / "P8_Y5_R2FR_2883_NEXT_TARGET.csv"
SRC_2883_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2883_VALIDATION.csv"
SRC_2883_QUEUE = RESIDUALS / "P8_Y5_R2FR_2883_CQM_DQZ_PRODUCT_BOUND_QUEUE.csv"
SRC_2883_PACK = RESIDUALS / "P8_Y5_R2FR_2883_DQ_LEAK_ARENA_SOURCE_PACK.csv"

SRC_1672_DOC = ROOT / "1672-Y5-R2FR-Z-physical-lock-map-or-first-DqZ-factor-source-row.md"
SRC_1672_LOCK = RESIDUALS / "P8_Y5_PARENT_QLOC_1672_Z_TO_RPHYS_LOCK_MAP_ATTEMPT.csv"
SRC_1672_RANK = RESIDUALS / "P8_Y5_PARENT_QLOC_1672_FULL_RANK_COERCIVITY_GATE.csv"
SRC_1672_NULLSPACE = RESIDUALS / "P8_Y5_PARENT_QLOC_1672_PHYSICAL_NULLSPACE_LEDGER.csv"
SRC_1672_DQZ_ROW = RESIDUALS / "P8_Y5_PARENT_QLOC_1672_FIRST_DQZ_FACTOR_SOURCE_ROW_NONCLAIM.csv"
SRC_1672_ARENA = RESIDUALS / "P8_Y5_PARENT_QLOC_1672_DQZ_ARENA_LINKS_NONCLAIM.csv"
SRC_1672_NEXT = RESIDUALS / "P8_Y5_PARENT_QLOC_1672_NEXT_TARGET.csv"
SRC_1672_VALIDATION = RESIDUALS / "P8_Y5_BRR545_1672_VALIDATION.csv"

SRC_757_BASIS = RESIDUALS / "P8_Y5_R10_757_RESIDUAL_VECTOR_BASIS.csv"
SRC_757_CONTRACT = RESIDUALS / "P8_Y5_R10_757_PHYSICAL_LOCK_CONTRACT.csv"
SRC_777_LOCK = RESIDUALS / "P8_Y5_R10_777_PHYSICAL_RESIDUAL_LOCK_MAP.csv"
SRC_778_RANK = RESIDUALS / "P8_Y5_R10_778_PHYSICAL_LOCK_RANK_PROOF_ATTEMPT.csv"
SRC_1282_MAP = RESIDUALS / "P8_Y5_R10_1282_RESPONSE_DOUBLET_COMPONENT_MAP_AUDIT.csv"
SRC_1282_VALIDATION = RESIDUALS / "P8_Y5_BRR545_1282_VALIDATION.csv"
SRC_1671_DQZ = RESIDUALS / "P8_Y5_PARENT_QLOC_1671_DQZ_FACTOR_INPUT_ROWS.csv"
SRC_1671_COBS = RESIDUALS / "P8_Y5_PARENT_QLOC_1671_COBS_FACTOR_INPUT_ROWS.csv"
SRC_1671_QUEUE = RESIDUALS / "P8_Y5_PARENT_QLOC_1671_PRODUCT_FACTOR_QUEUE.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2884_SOURCE_REGISTER.csv",
    "lock": RESIDUALS / "P8_Y5_R2FR_2884_Z_TO_RPHYS_LOCK_MAP_ATTEMPT.csv",
    "rank": RESIDUALS / "P8_Y5_R2FR_2884_FULL_RANK_COERCIVITY_GATE.csv",
    "nullspace": RESIDUALS / "P8_Y5_R2FR_2884_PHYSICAL_NULLSPACE_LEDGER.csv",
    "dqz_row": RESIDUALS / "P8_Y5_R2FR_2884_FIRST_DQZ_FACTOR_SOURCE_ROW_NONCLAIM.csv",
    "arena": RESIDUALS / "P8_Y5_R2FR_2884_DQZ_ARENA_LINKS_NONCLAIM.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2884_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2884_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2884_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2884_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2884_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2884_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "lock_copy": LOCAL_BOUNDS / "RAB_Z_TO_RPHYS_LOCK_MAP_2884_NONCLAIM.csv",
    "dqz_copy": SOURCE_WEIGHT / "RAB_FIRST_DQZ_FACTOR_SOURCE_ROW_2884_NONCLAIM.csv",
    "arena_copy": BETA_DOCS / "RAB_DQZ_ARENA_LINKS_2884_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2884_DqZ_zero_or_first_factor_value_NEXT.csv",
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
        ("SRC2884_0_2883_doc", SRC_2883_DOC, "Status: `Y5_R2FR_2883_constraint_first_not_derived_Dq_pack_retained_Zlock_2884_next`;full-rank/coercive `Z` physical lock", "2883 handoff"),
        ("SRC2884_1_2883_next", SRC_2883_NEXT, "NEXT2883_0_2884", "explicit 2884 target"),
        ("SRC2884_2_2883_validation", SRC_2883_VALIDATION, "VAL2883_OVERALL", "2883 validation"),
        ("SRC2884_3_2883_queue", SRC_2883_QUEUE, "PQ2883_0_Z_physical_lock;PQ2883_3_product_bound", "2883 product-bound queue"),
        ("SRC2884_4_2883_pack", SRC_2883_PACK, "DSP2883_0_Dq_Z;DSP2883_3_Cqm", "2883 Dq leak arena pack"),
        ("SRC2884_5_1672_doc", SRC_1672_DOC, "PHYSICAL_LOCK_NOT_PROVED;Dq_Z_norm", "prior physical-lock checkpoint"),
        ("SRC2884_6_1672_lock", SRC_1672_LOCK, "LOCK1672_0_q_loc;LOCK1672_6_verdict", "Z to R_phys lock attempt"),
        ("SRC2884_7_1672_rank", SRC_1672_RANK, "RG1672_0_define_L;RG1672_5_verdict", "full-rank/coercivity gate"),
        ("SRC2884_8_1672_nullspace", SRC_1672_NULLSPACE, "NS1672_0_q_loc_only;NS1672_5_readout_coupling", "physical nullspace ledger"),
        ("SRC2884_9_1672_dqz", SRC_1672_DQZ_ROW, "DQZ1672_0_first_factor_row;SOURCE_READY_TEMPLATE_VALUE_MISSING", "first Dq_Z factor row"),
        ("SRC2884_10_1672_arena", SRC_1672_ARENA, "R0_identity_coframe_direct;R10_fifth_force", "Dq_Z arena links"),
        ("SRC2884_11_1672_next", SRC_1672_NEXT, "1673-Y5-R2FR-DqZ-zero-theorem-or-first-factor-value-fill.md", "1672 next target"),
        ("SRC2884_12_1672_validation", SRC_1672_VALIDATION, "VAL1672_OVERALL", "1672 validation"),
        ("SRC2884_13_757_basis", SRC_757_BASIS, "RVB757_0_q_loc_vector;RVB757_5_matter_coupling", "physical residual basis"),
        ("SRC2884_14_757_contract", SRC_757_CONTRACT, "PLC757_1_lock_map;PLC757_5_zero_theorem", "physical lock contract"),
        ("SRC2884_15_777_lock", SRC_777_LOCK, "PRL777_0_q_loc_vector;PRL777_6_verdict", "residual lock map"),
        ("SRC2884_16_778_rank", SRC_778_RANK, "RPA778_0_block_form;RPA778_4_verdict", "rank proof attempt"),
        ("SRC2884_17_1282_map", SRC_1282_MAP, "RCM1282_1_q_loc_vector_lock;RCM1282_6_verdict", "response-doublet component map audit"),
        ("SRC2884_18_1282_validation", SRC_1282_VALIDATION, "VAL1282_10_overall", "1282 validation"),
        ("SRC2884_19_1671_dqz", SRC_1671_DQZ, "DQZ1671_0_basis;DQZ1671_2_derivative", "Dq_Z factor input rows"),
        ("SRC2884_20_1671_cobs", SRC_1671_COBS, "COBS1671_0_operator_norm;COBS1671_2_shadow_frame_guard", "C_Obs_e factor rows"),
        ("SRC2884_21_1671_queue", SRC_1671_QUEUE, "PFQ1671_0_clean_kill;PFQ1671_3_physical_lock", "product factor queue"),
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


def lock_rows() -> list[dict[str, Any]]:
    specs = [
        ("LOCK2884_0_q_loc", "q_loc vector", "Z_q^nu -> q_loc^nu/q_*", "q_loc^nu/q_* = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})/q_*", "NOT_CLOSED", "MISSING_GAMMA_EFF_KHAT_PLOC_OWNER_AND_COMPONENT_DATA", "alpha3;PPN;R10;compact-orbit", "theorem-zero q_loc or sourced q_loc component profile"),
        ("LOCK2884_1_Y5", "Y5 measured-GM/source normalization", "Z_mu -> epsilon_mu", "epsilon_mu = Delta(GM)_measured/(GM)_GR or equivalent source-current residual", "FAILS_CURRENT_ROUTE_EXCHANGE_EVEN_SCALAR", "MISSING_SOURCE_CURRENT_CLOSURE_AND_GAUSS_ORBITAL_CALIBRATION", "Newton limit;WEP/source universality;orbits;clocks", "parent-signed Y5 source-current descent or finite epsilon_mu bound"),
        ("LOCK2884_2_Y6", "Y6 extra stress/local exterior metric", "Z_T -> DeltaT_extra/T_*", "DeltaT_extra^{mu nu}/T_* and induced weak-field metric response", "NOT_CLOSED", "EXCHANGE_EVEN_CONSERVED_STRESS_CAN_LIVE_IN_QLOC_KERNEL", "PPN beta/gamma;lensing;local exterior metric", "stress decomposition plus metric-response matrix"),
        ("LOCK2884_3_PPN", "full PPN residual vector", "Z_PPN -> DeltaPPN_I", "DeltaPPN_I={gamma-1,beta-1,alpha_i,xi,zeta_i,Gdot,R11}", "NOT_CLOSED", "MISSING_PPN_RESPONSE_OPERATOR_AND_GAUGE_FRAME_CERTIFICATE", "solar-system PPN;pulsars;preferred-frame;time drift", "PPN response matrix W^I_A with gauge/frame source conditions"),
        ("LOCK2884_4_boundary", "boundary/harmonic flux", "Z_H -> B_obs_boundary/M_H and harmonic/projector leakage", "q_H and P_flux P_Hodge q_loc", "NOT_CLOSED", "MISSING_HODGE_FLUX_BOUNDARY_OPERATOR_AND_PROJECTOR_DESCENT", "alpha3;local force;compact-shell leakage", "boundary operator/no-flux theorem or sourced B_obs component row"),
        ("LOCK2884_5_coupling", "matter/source/readout coupling", "Z_coupling -> DeltaCoupling_A and B_obs_source_measure/M_H", "species/frame/source/photon/clock/orbit pullback residuals", "PARTIAL_ONLY_NOT_CLOSED", "MISSING_QUOTIENT_MATTER_SOURCE_READOUT_DESCENT", "WEP;clocks;EM/charge;source normalization;orbit readout", "coupling descent input pack or finite source-measure coefficient bound"),
        ("LOCK2884_6_verdict", "full physical residual vector", "Z^A = N^A_I R_phys^I + O(R_phys^2), rank/coercive after gauge quotient", "R_phys={q_loc,Y5,Y6,DeltaPPN,q_H,DeltaCoupling}", "PHYSICAL_LOCK_NOT_PROVED", "all channel rows above remain unsigned or incomplete", "all local-GR recovery gates", "Dq_Z zero theorem or first source-backed Dq_Z factor value"),
    ]
    return [
        add_common(
            {
                "lock_id": lock_id,
                "physical_channel": channel,
                "candidate_lock": candidate,
                "physical_residual": residual,
                "current_status": status,
                "blocker": blocker,
                "test_arenas": arenas,
                "next_input": next_input,
                "parent_signed": False,
                "full_rank_component": False,
                "coercive_norm_component": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for lock_id, channel, candidate, residual, status, blocker, arenas, next_input in specs
    ]


def rank_rows() -> list[dict[str, Any]]:
    specs = [
        ("RG2884_0_define_L", "Define L^I_A = partial R_phys^I / partial Z^A around the local-GR background", "MISSING_SOURCE_BACKED_RESPONSE_OPERATOR", "no single sourced L matrix exists for q_loc/Y5/Y6/PPN/boundary/coupling"),
        ("RG2884_1_full_rank", "rank(L)=dim(R_phys) after gauge quotient", "NOT_SATISFIED", "q_loc-only or PPN-only rank would leave source/boundary/coupling nullspace"),
        ("RG2884_2_kernel", "ker(L) contains only gauge/quotient directions, not physical local residuals", "OPEN_KERNEL_RISK", "Y5, Y6, PPN, boundary, or readout couplings can survive formal Z silence"),
        ("RG2884_3_coercivity", "c_-||R_phys||^2 <= <Z,MZ> <= c_+||R_phys||^2 with c_->0", "MISSING_COERCIVE_PHYSICAL_LOCK", "positive auxiliary norm is not proven to control measured residuals"),
        ("RG2884_4_no_linear_work", "J_I=B_I=0 for all physical residual channels in compact local vacuum", "SOURCE_BOUNDARY_WORK_NOT_ZERO", "source-current, boundary, and readout leakage can drive residuals"),
        ("RG2884_5_verdict", "physical-lock theorem closes", "FULL_RANK_COERCIVITY_NOT_PROVED", "do not promote response-doublet to GR/Newton reduction"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "current_status": status,
                "failure_mode": failure,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for gate_id, criterion, status, failure in specs
    ]


def nullspace_rows() -> list[dict[str, Any]]:
    specs = [
        ("NS2884_0_q_loc_only", "q_loc zero but Y5/Y6/PPN/coupling survive", "q_loc-only lock can miss measured-GM shifts, conserved stress, and readout leakage"),
        ("NS2884_1_even_scalar", "exchange-odd Z cannot erase exchange-even source normalization by parity alone", "Y5 measured source strength is an observed even scalar unless separately parent-owned"),
        ("NS2884_2_conserved_stress", "Bianchi-silent extra stress survives auxiliary Z zero", "Y6 can change beta/gamma/exterior metric while remaining conserved"),
        ("NS2884_3_PPN_operator", "PPN vector response missing", "without W^I_A, gamma/beta/alpha_i/xi/Gdot/R11 can sit outside Z"),
        ("NS2884_4_boundary_harmonic", "boundary/Hodge/projector flux survives", "compact collar and harmonic modes can re-enter alpha3/source-measure channels"),
        ("NS2884_5_readout_coupling", "clock/photon/orbit/EM/source readout hidden maps survive", "same-coframe wording is not a full quotient-invariant matter/readout theorem"),
    ]
    return [
        add_common(
            {
                "nullspace_id": row_id,
                "nullspace_risk": risk,
                "why_it_matters": why,
                "status": "ACTIVE_GUARD",
                "parent_signed_absence_theorem": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for row_id, risk, why in specs
    ]


def dqz_row_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "row_id": "DQZ2884_0_first_factor_row",
                "symbol": "Dq_Z_norm",
                "definition": "||Dq[partial_Z]||_q after parent q, Z basis, and q/Z norms are declared",
                "units": "dimensionless after q/Z normalization",
                "candidate_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "current_status": "SOURCE_READY_TEMPLATE_VALUE_MISSING",
                "source_paths": f"{SRC_1671_DQZ}; {SRC_1672_LOCK}; {SRC_1282_MAP}",
                "required_source_inputs": "parent q(Phi); unified Z basis; Dq[partial_Z]; q norm; Z norm; quotient/constraint sort; physical-lock or no-claim label",
                "priority_arenas": "R0_identity_coframe_direct;R3_gamma;R4_beta;R10_fifth_force;R11_EH_operator_ledger",
                "projection_formula": "C_qm_Z <= C_Obs_e * Dq_Z_norm * N_Z",
                "derivation_status": "NONCLAIM_FACTOR_TEMPLATE",
                "promotion_rule": "valid only if candidate_value is numeric/source-backed or theorem-zero, units are fixed, and no MISSING_* markers remain",
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
    ]


def arena_rows() -> list[dict[str, Any]]:
    specs = [
        ("R0_identity_coframe_direct", "eta_WEP_direct_geometry", "eta_geom_AB <= Pi_R0*C_Obs_e*Dq_Z_norm*N_Z + source/readout terms", "MISSING_PI_R0_COBS_DQZ_NZ", "Dq_Z_norm; C_Obs_e; N_Z; Pi_R0; source/readout/boundary guards"),
        ("R3_gamma", "gamma_minus_1", "|gamma-1| <= Pi_gamma*C_Obs_e*Dq_Z_norm*N_Z + calibration/RAB terms", "MISSING_WEAK_FIELD_METRIC_RESPONSE", "Dq_Z_norm; C_Obs_e; N_Z; Pi_gamma; weak-field metric response"),
        ("R4_beta", "beta_minus_1", "|beta-1| <= Pi_beta*C_Obs_e*Dq_Z_norm*N_Z + S_cg/source-normalization terms", "MISSING_POST_NEWTONIAN_RESPONSE", "Dq_Z_norm; C_Obs_e; N_Z; Pi_beta; source-normalization response"),
        ("R10_fifth_force", "delta_G_or_fifth_force_yukawa", "|alpha_pred(lambda)| <= Pi_R10(lambda)*C_Obs_e*Dq_Z_norm*N_Z plus 1503 coefficient chain", "MISSING_R10_FIELD_MAP_AND_BOUND_CURVE", "Dq_Z_norm; C_Obs_e; N_Z; Pi_R10(lambda); alpha(lambda) bound curve"),
        ("R11_EH_operator_ledger", "non_EH_operator_coefficients", "non-EH operator residual includes any Dq_Z-induced visible operator coefficient", "MISSING_OPERATOR_COEFFICIENT_VECTOR", "Dq_Z_norm; C_Obs_e; N_Z; operator coefficient vector"),
    ]
    return [
        add_common(
            {
                "arena_row_id": row_id,
                "observable": observable,
                "projection_formula": formula,
                "current_status": status,
                "required_inputs": inputs,
                "predicted_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "comparison_ready": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for row_id, observable, formula, status, inputs in specs
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2884_0_channels", "q_loc/Y5/Y6/PPN/boundary/coupling channels audited", "PASS_CONTROL_ONLY", "all required channels are named but unsigned", False),
        ("GATE2884_1_lock", "Z is full-rank/coercive over R_phys", "FAIL", "no sourced response matrix L or coercive norm exists", False),
        ("GATE2884_2_nullspace", "no physical nullspace survives formal Z silence", "FAIL", "Y5/Y6/PPN/boundary/coupling nullspaces remain active", False),
        ("GATE2884_3_source_work", "J_I=B_I=0 for compact local vacuum", "FAIL", "source-current, boundary and readout leakage remain open", False),
        ("GATE2884_4_dqz_factor", "Dq_Z_norm factor is source-backed", "FAIL", "candidate value remains MISSING_NUMERIC_OR_THEOREM_ZERO", False),
        ("GATE2884_5_arena_score", "R0/R3/R4/R10/R11 comparisons are score-ready", "FAIL", "C_Obs_e, N_Z, Pi_arena and Dq_Z value are missing", False),
        ("GATE2884_6_local_GR_Newton", "response-doublet double-zero derives local GR/Newton", "FAIL_CLOSED", "formal auxiliary silence is not yet measured residual silence", False),
    ]
    return [
        add_common({"gate_id": gate_id, "criterion": criterion, "result": result, "reason": reason, "gate_passed": passed})
        for gate_id, criterion, result, reason, passed in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2884_0_Zlock_or_DqZ_import",
                "status": "REFUSED_Z_LOCK_AND_DQZ_FACTOR_NOT_LIVE",
                "accepted_physical_lock_maps": 0,
                "accepted_dqz_factor_rows": 0,
                "accepted_arena_links": 0,
                "reason": "Z-to-R_phys full-rank/coercive lock is unsigned and Dq_Z_norm has no numeric/theorem-zero value",
                "runner_ready": False,
                "claim_unlocked": False,
                "score_allowed": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2884_0_lock", "PHYSICAL_LOCK_NOT_PROVED", "six-channel R_phys map exists as a requirement set but no parent-signed full-rank/coercive operator exists", "do not promote response-doublet double-zero"),
        ("DEC2884_1_factor", "DQZ_FACTOR_ROW_STAGED_NONCLAIM", "Dq_Z_norm is the first concrete factor row with units/source requirements and arena links", "fill only with theorem-zero or source-backed numeric/interval value"),
        ("DEC2884_2_best_next", "TARGET_DQZ_ZERO_OR_NUMERIC_FIRST", "Dq_Z=0 is still cleaner than bounding C_Obs_e because it kills the product at the earliest factor", "attempt q/Z basis plus Dq derivative extraction before C_Obs_e numeric work"),
        ("DEC2884_3_safety", "NO_GR_NEWTON_CLAIM", "physical-lock failure plus missing product factor cannot derive local GR/Newton", "keep all claim gates false"),
    ]
    return [add_common({"decision_id": row_id, "decision": decision, "because": because, "next_action": next_action}) for row_id, decision, because, next_action in specs]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2884_0_2885",
                "status": "selected_primary",
                "target_doc": "2885-Y5-R2FR-DqZ-zero-theorem-or-first-factor-value-fill-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_DqZ_zero_theorem_or_first_factor_value_fill_under_AX1090_2885.py",
                "mission": "try to close Dq_Z_norm=0 from q/Z basis and quotient/constraint independence; if it fails, fill Dq_Z_norm with a source-backed nonclaim numeric/interval row or a blocker ledger",
                "forbidden_shortcuts": "no invented Dq_Z value; no formal-Z-to-physical-residual leap; no cancellation; no local-GR/R10/PPN/WEP claim",
                "selected": True,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    pairs = [
        ("COPY2884_0_lock", OUTPUTS["lock"], BRANCH_OUTPUTS["lock_copy"], "Z to R_phys lock map nonclaim copy"),
        ("COPY2884_1_dqz", OUTPUTS["dqz_row"], BRANCH_OUTPUTS["dqz_copy"], "first Dq_Z factor row nonclaim copy"),
        ("COPY2884_2_arena", OUTPUTS["arena"], BRANCH_OUTPUTS["arena_copy"], "Dq_Z arena links nonclaim copy"),
        ("COPY2884_3_next", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to Dq_Z zero/value target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in pairs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(add_common({"copy_id": copy_id, "source_table": str(source), "copy_path": str(destination), "purpose": purpose, "exists": destination.exists()}))
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
        "full_rank_component",
        "coercive_norm_component",
        "theorem_zero_adopted",
        "finite_value_present",
        "prediction_source_backed",
        "accepted_for_scoring",
        "parent_signed_absence_theorem",
        "comparison_ready",
        "gate_passed",
        "runner_ready",
        "claim_unlocked",
        "score_allowed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    lock = rows_by_name["lock"]
    rank = rows_by_name["rank"]
    nullspace = rows_by_name["nullspace"]
    dqz_row = rows_by_name["dqz_row"]
    arena = rows_by_name["arena"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    checks = [
        ("VAL2884_0_sources_exist", all(row["path_exists"] for row in sources), "all registered source paths exist"),
        ("VAL2884_1_source_anchors", all(row["anchors_found"] for row in sources), "all registered source anchors were found"),
        ("VAL2884_2_all_channels_present", len(lock) == 7 and any(row["lock_id"] == "LOCK2884_6_verdict" for row in lock), "q_loc/Y5/Y6/PPN/boundary/coupling channels are audited"),
        ("VAL2884_3_lock_failed", any(row["current_status"] == "PHYSICAL_LOCK_NOT_PROVED" for row in lock), "physical Z-to-R_phys lock is not promoted"),
        ("VAL2884_4_rank_failed", any(row["gate_id"] == "RG2884_5_verdict" and row["current_status"] == "FULL_RANK_COERCIVITY_NOT_PROVED" for row in rank), "full-rank/coercivity theorem remains not proved"),
        ("VAL2884_5_nullspace_guards", len(nullspace) >= 6 and all(row["status"] == "ACTIVE_GUARD" for row in nullspace), "physical nullspace guards remain active"),
        ("VAL2884_6_dqz_row_staged", dqz_row[0]["symbol"] == "Dq_Z_norm" and dqz_row[0]["candidate_value"] == "MISSING_NUMERIC_OR_THEOREM_ZERO", "first Dq_Z factor row is staged as nonclaim"),
        ("VAL2884_7_arena_links", len(arena) >= 5 and any(row["arena_row_id"] == "R10_fifth_force" for row in arena), "Dq_Z factor row links to R0/R3/R4/R10/R11 arenas"),
        ("VAL2884_8_gates_fail_closed", all(row["gate_passed"] is False for row in gates), "all claim gates fail closed"),
        ("VAL2884_9_runner_refused", runner[0]["status"] == "REFUSED_Z_LOCK_AND_DQZ_FACTOR_NOT_LIVE" and runner[0]["runner_ready"] is False, "runner remains refused"),
        ("VAL2884_10_next_target_2885", next_target[0]["next_id"] == "NEXT2884_0_2885" and next_target[0]["selected"] is True, "2885 target selected"),
        ("VAL2884_11_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2884_12_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2884_13_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2884_14_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2884_15_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2884_16_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2884_17_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2884_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2884 audited the Z-to-R_phys physical-lock map, refused response-doublet promotion, staged the first Dq_Z factor row, and selected Dq_Z zero theorem or first factor value fill for 2885.",
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
    text = f"""# 2884 - Y5 R2FR Z Physical-Lock Map Or First DqZ Factor Source Row Under AX1090

Status: `Y5_R2FR_2884_Z_physical_lock_not_proved_DqZ_factor_staged_2885_next`

## Private Verdict

2884 hits the response-doublet route at the exact weak point.

The theorem we would want is sharp:

`Z^A = N^A_I R_phys^I + O(R_phys^2)`, `rank(N)=dim(R_phys)` after gauge quotient, and `c_-||R_phys||^2 <= <Z,MZ> <= c_+||R_phys||^2`, with no compact-local linear source or boundary work.

That would let formal `Z=0` become measured local silence: `q_loc=Y5=Y6=DeltaPPN=q_H=DeltaCoupling=0`.

Current verdict: not proved. The six physical channels are now audited, but no parent-signed full-rank/coercive response operator exists. So the response-doublet remains a serious derivation target, not a local-GR/Newton result.

The concrete fallback is now staged: `Dq_Z_norm` is the first nonclaim product factor in `C_qm_Z <= C_Obs_e * Dq_Z_norm * N_Z`.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Z To Rphys Lock Map Attempt

{md_table(rows_by_name["lock"], ["lock_id", "physical_channel", "candidate_lock", "current_status", "blocker", "test_arenas", "valid_for_claim"])}

## Full-Rank Coercivity Gate

{md_table(rows_by_name["rank"], ["gate_id", "criterion", "current_status", "failure_mode", "valid_for_claim"])}

## Physical Nullspace Ledger

{md_table(rows_by_name["nullspace"], ["nullspace_id", "nullspace_risk", "why_it_matters", "status", "valid_for_claim"])}

## First DqZ Factor Source Row

{md_table(rows_by_name["dqz_row"], ["row_id", "symbol", "definition", "units", "candidate_value", "current_status", "projection_formula", "valid_for_claim"])}

## DqZ Arena Links

{md_table(rows_by_name["arena"], ["arena_row_id", "observable", "projection_formula", "current_status", "predicted_value", "comparison_ready", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "accepted_physical_lock_maps", "accepted_dqz_factor_rows", "reason", "runner_ready", "valid_for_claim"])}

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
        "lock": lock_rows(),
        "rank": rank_rows(),
        "nullspace": nullspace_rows(),
        "dqz_row": dqz_row_rows(),
        "arena": arena_rows(),
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
    overall = next(row for row in validation if row["validation_id"] == "VAL2884_OVERALL")
    print(f"VAL2884_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
