from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1672"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1672-Y5-R2FR-Z-physical-lock-map-or-first-DqZ-factor-source-row.md"

SOURCE_FILES = {
    "1671_doc": ROOT / "1671-Y5-R2FR-DqZ-basis-kernel-or-Cobs-operator-norm-input.md",
    "1671_validation": OUT / "P8_Y5_BRR545_1671_VALIDATION.csv",
    "1671_dqz_rows": OUT / "P8_Y5_PARENT_QLOC_1671_DQZ_FACTOR_INPUT_ROWS.csv",
    "1671_cobs_rows": OUT / "P8_Y5_PARENT_QLOC_1671_COBS_FACTOR_INPUT_ROWS.csv",
    "757_basis": OUT / "P8_Y5_R10_757_RESIDUAL_VECTOR_BASIS.csv",
    "757_contract": OUT / "P8_Y5_R10_757_PHYSICAL_LOCK_CONTRACT.csv",
    "757_attempt": OUT / "P8_Y5_R10_757_PHYSICAL_LOCK_ATTEMPT.csv",
    "777_lock_map": OUT / "P8_Y5_R10_777_PHYSICAL_RESIDUAL_LOCK_MAP.csv",
    "777_rank_gate": OUT / "P8_Y5_R10_777_LOCK_RANK_AND_NULLSPACE_GATE.csv",
    "778_rank_attempt": OUT / "P8_Y5_R10_778_PHYSICAL_LOCK_RANK_PROOF_ATTEMPT.csv",
    "778_readout_candidate": OUT / "P8_Y5_R10_778_EM_CLOCK_ORBIT_READOUT_INPUT_CANDIDATE.csv",
    "1282_component_map": OUT / "P8_Y5_R10_1282_RESPONSE_DOUBLET_COMPONENT_MAP_AUDIT.csv",
    "1282_validation": OUT / "P8_Y5_BRR545_1282_VALIDATION.csv",
    "1667_dq_tests": OUT / "P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv",
    "1665_signature": OUT / "P8_Y5_PARENT_QLOC_1665_PARENT_SIGNATURE_CLAUSE_AUDIT.csv",
}

NEEDLES = {
    "1671_doc": ["Dq_Z=0` is not parent-signed", "C_qm_Z <= C_Obs_e * Dq_Z_norm * N_Z"],
    "1671_validation": ["VAL1671_OVERALL", "PASS"],
    "1671_dqz_rows": ["DQZ1671_2_derivative", "MISSING_DQ_DERIVATIVE_OR_THEOREM_ZERO"],
    "1671_cobs_rows": ["COBS1671_0_operator_norm", "MISSING_OBS_E_FUNCTOR_AND_OPERATOR_NORM"],
    "757_basis": ["RVB757_0_q_loc_vector", "RVB757_5_matter_coupling"],
    "757_contract": ["PLC757_1_lock_map", "not_shown"],
    "757_attempt": ["PLA757_6_verdict", "physical_lock_not_proved"],
    "777_lock_map": ["PRL777_6_verdict", "physical_lock_not_proved"],
    "777_rank_gate": ["RNG777_0_full_rank_required", "not_satisfied"],
    "778_rank_attempt": ["RPA778_4_verdict", "rank_proof_not_complete"],
    "778_readout_candidate": ["MISSING_READOUT_FUNCTIONAL", "MISSING_SOURCE_PATH"],
    "1282_component_map": ["RCM1282_6_verdict", "COMPONENT_MAP_NOT_CLOSED"],
    "1282_validation": ["VAL1282_10_overall", "PASS"],
    "1667_dq_tests": ["DQT1667_1_Z_normal_form", "MISSING_UNIFIED_Z_BASIS_AND_COMPONENT_LOCK"],
    "1665_signature": ["PSC1665_7_residual_vector_lock", "PHYSICAL_LOCK_NOT_DERIVED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1672_SOURCE_REGISTER.csv"
LOCK_MAP_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1672_Z_TO_RPHYS_LOCK_MAP_ATTEMPT.csv"
RANK_GATE = OUT / "P8_Y5_PARENT_QLOC_1672_FULL_RANK_COERCIVITY_GATE.csv"
NULLSPACE_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1672_PHYSICAL_NULLSPACE_LEDGER.csv"
DQZ_FIRST_ROW = OUT / "P8_Y5_PARENT_QLOC_1672_FIRST_DQZ_FACTOR_SOURCE_ROW_NONCLAIM.csv"
ARENA_LINKS = OUT / "P8_Y5_PARENT_QLOC_1672_DQZ_ARENA_LINKS_NONCLAIM.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1672_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1672_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1672_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1672_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    LOCK_MAP_ATTEMPT,
    RANK_GATE,
    NULLSPACE_LEDGER,
    DQZ_FIRST_ROW,
    ARENA_LINKS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    LOCK_MAP_ATTEMPT,
    RANK_GATE,
    NULLSPACE_LEDGER,
    DQZ_FIRST_ROW,
    ARENA_LINKS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    LOCK_MAP_ATTEMPT: [
        QUARANTINE / "Z_TO_RPHYS_LOCK_MAP_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_Z_to_Rphys_lock_map_attempt_nonclaim_1672.csv",
        QUEUE / "JR1672_Z_TO_RPHYS_LOCK_MAP_ATTEMPT_NONCLAIM.csv",
    ],
    DQZ_FIRST_ROW: [
        QUARANTINE / "FIRST_DQZ_FACTOR_SOURCE_ROW_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_first_DqZ_factor_source_row_nonclaim_1672.csv",
        QUEUE / "JR1672_FIRST_DQZ_FACTOR_SOURCE_ROW_NONCLAIM.csv",
    ],
    ARENA_LINKS: [
        QUARANTINE / "DQZ_ARENA_LINKS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_DqZ_arena_links_nonclaim_1672.csv",
        QUEUE / "JR1672_DQZ_ARENA_LINKS_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1672.csv",
        QUEUE / "JR1672_NEXT_TARGET_NONCLAIM.csv",
    ],
}

LOCK_CHANNELS = [
    (
        "LOCK1672_0_q_loc",
        "q_loc vector",
        "Z_q^nu -> q_loc^nu/q_*",
        "q_loc^nu/q_* = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})/q_*",
        "MISSING_GAMMA_EFF_KHAT_PLOC_OWNER_AND_COMPONENT_DATA",
        "not_closed",
        "alpha3;PPN;R10;compact-orbit",
        "theorem-zero q_loc or sourced q_loc component profile",
    ),
    (
        "LOCK1672_1_Y5",
        "Y5 measured-GM/source normalization",
        "Z_mu -> epsilon_mu",
        "epsilon_mu = Delta(GM)_measured/(GM)_GR or equivalent source-current residual",
        "MISSING_SOURCE_CURRENT_CLOSURE_AND_GAUSS_ORBITAL_CALIBRATION",
        "fails_current_route_exchange_even_scalar",
        "Newton limit;WEP/source universality;orbits;clocks",
        "parent-signed Y5 source-current descent or finite epsilon_mu bound",
    ),
    (
        "LOCK1672_2_Y6",
        "Y6 extra stress/local exterior metric",
        "Z_T -> DeltaT_extra/T_*",
        "DeltaT_extra^{mu nu}/T_* and induced weak-field metric response",
        "EXCHANGE_EVEN_CONSERVED_STRESS_CAN_LIVE_IN_QLOC_KERNEL",
        "not_closed",
        "PPN beta/gamma;lensing;local exterior metric",
        "stress decomposition plus metric-response matrix",
    ),
    (
        "LOCK1672_3_PPN",
        "full PPN residual vector",
        "Z_PPN -> DeltaPPN_I",
        "DeltaPPN_I={gamma-1,beta-1,alpha_i,xi,zeta_i,Gdot,R11}",
        "MISSING_PPN_RESPONSE_OPERATOR_AND_GAUGE_FRAME_CERTIFICATE",
        "not_closed",
        "solar-system PPN;pulsars;preferred-frame;time drift",
        "PPN response matrix W^I_A with gauge/frame source conditions",
    ),
    (
        "LOCK1672_4_boundary",
        "boundary/harmonic flux",
        "Z_H -> B_obs_boundary/M_H and harmonic/projector leakage",
        "q_H and P_flux P_Hodge q_loc",
        "MISSING_HODGE_FLUX_BOUNDARY_OPERATOR_AND_PROJECTOR_DESCENT",
        "not_closed",
        "alpha3;local force;compact-shell leakage",
        "boundary operator/no-flux theorem or sourced B_obs component row",
    ),
    (
        "LOCK1672_5_coupling",
        "matter/source/readout coupling",
        "Z_coupling -> DeltaCoupling_A and B_obs_source_measure/M_H",
        "species/frame/source/photon/clock/orbit pullback residuals",
        "MISSING_QUOTIENT_MATTER_SOURCE_READOUT_DESCENT",
        "partial_only_not_closed",
        "WEP;clocks;EM/charge;source normalization;orbit readout",
        "coupling descent input pack or finite source-measure coefficient bound",
    ),
]


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_string(value: object) -> str:
    return str(value).strip().lower()


def source_register_rows() -> list[dict[str, object]]:
    rows = []
    for source_id, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[source_id]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1672 Z physical-lock map or first Dq_Z product-factor source-row input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def lock_map_rows() -> list[dict[str, object]]:
    rows = []
    for lock_id, channel, candidate_lock, residual, blocker, status, arenas, next_input in LOCK_CHANNELS:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "lock_id": lock_id,
                "physical_channel": channel,
                "candidate_lock": candidate_lock,
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
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "lock_id": "LOCK1672_6_verdict",
            "physical_channel": "full physical residual vector",
            "candidate_lock": "Z^A = N^A_I R_phys^I + O(R_phys^2), rank/coercive after gauge quotient",
            "physical_residual": "R_phys={q_loc,Y5,Y6,DeltaPPN,q_H,DeltaCoupling}",
            "current_status": "PHYSICAL_LOCK_NOT_PROVED",
            "blocker": "all channel rows above remain unsigned or incomplete",
            "test_arenas": "all local-GR recovery gates",
            "next_input": "first Dq_Z product-factor row plus targeted q_loc/Y5/PPN source rows",
            "parent_signed": False,
            "full_rank_component": False,
            "coercive_norm_component": False,
            "theorem_zero_adopted": False,
            "finite_value_present": False,
            "prediction_source_backed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def rank_gate_rows() -> list[dict[str, object]]:
    rows = [
        (
            "RG1672_0_define_L",
            "Define L^I_A = partial R_phys^I / partial Z^A around the local-GR background",
            "MISSING_SOURCE_BACKED_RESPONSE_OPERATOR",
            "no single sourced L matrix exists for q_loc/Y5/Y6/PPN/boundary/coupling",
        ),
        (
            "RG1672_1_full_rank",
            "rank(L)=dim(R_phys) after gauge quotient",
            "NOT_SATISFIED",
            "q_loc-only or PPN-only rank would leave source/boundary/coupling nullspace",
        ),
        (
            "RG1672_2_kernel",
            "ker(L) contains only gauge/quotient directions, not physical local residuals",
            "OPEN_KERNEL_RISK",
            "Y5, Y6, PPN, boundary, or readout couplings can survive formal Z silence",
        ),
        (
            "RG1672_3_coercivity",
            "c_-||R_phys||^2 <= <Z,MZ> <= c_+||R_phys||^2 with c_->0",
            "MISSING_COERCIVE_PHYSICAL_LOCK",
            "positive auxiliary norm is not proven to control measured residuals",
        ),
        (
            "RG1672_4_no_linear_work",
            "J_I=B_I=0 for all physical residual channels in compact local vacuum",
            "SOURCE_BOUNDARY_WORK_NOT_ZERO",
            "source-current, boundary, and readout leakage can drive residuals",
        ),
        (
            "RG1672_5_verdict",
            "physical-lock theorem closes",
            "FULL_RANK_COERCIVITY_NOT_PROVED",
            "do not promote response-doublet to GR/Newton reduction",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "criterion": criterion,
            "current_status": current_status,
            "failure_mode": failure_mode,
            "parent_signed": False,
            "theorem_zero_adopted": False,
            "finite_value_present": False,
            "prediction_source_backed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, criterion, current_status, failure_mode in rows
    ]


def nullspace_rows() -> list[dict[str, object]]:
    rows = [
        ("NS1672_0_q_loc_only", "q_loc zero but Y5/Y6/PPN/coupling survive", "q_loc-only lock can miss measured-GM shifts, conserved stress, and readout leakage", "ACTIVE_GUARD"),
        ("NS1672_1_even_scalar", "exchange-odd Z cannot erase exchange-even source normalization by parity alone", "Y5 measured source strength is an observed even scalar unless separately parent-owned", "ACTIVE_GUARD"),
        ("NS1672_2_conserved_stress", "Bianchi-silent extra stress survives auxiliary Z zero", "Y6 can change beta/gamma/exterior metric while remaining conserved", "ACTIVE_GUARD"),
        ("NS1672_3_PPN_operator", "PPN vector response missing", "without W^I_A, gamma/beta/alpha_i/xi/Gdot/R11 can sit outside Z", "ACTIVE_GUARD"),
        ("NS1672_4_boundary_harmonic", "boundary/Hodge/projector flux survives", "compact collar and harmonic modes can re-enter alpha3/source-measure channels", "ACTIVE_GUARD"),
        ("NS1672_5_readout_coupling", "clock/photon/orbit/EM/source readout hidden maps survive", "same-coframe wording is not a full quotient-invariant matter/readout theorem", "ACTIVE_GUARD"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "nullspace_id": nullspace_id,
            "nullspace_risk": risk,
            "why_it_matters": why,
            "status": status,
            "parent_signed_absence_theorem": False,
            "theorem_zero_adopted": False,
            "finite_value_present": False,
            "prediction_source_backed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for nullspace_id, risk, why, status in rows
    ]


def dqz_first_row() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQZ1672_0_first_factor_row",
            "symbol": "Dq_Z_norm",
            "definition": "||Dq[partial_Z]||_q after parent q, Z basis, and q/Z norms are declared",
            "units": "dimensionless after q/Z normalization",
            "candidate_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "current_status": "SOURCE_READY_TEMPLATE_VALUE_MISSING",
            "source_paths": "P8_Y5_PARENT_QLOC_1671_DQZ_FACTOR_INPUT_ROWS.csv; P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv; P8_Y5_R10_777_PHYSICAL_RESIDUAL_LOCK_MAP.csv; P8_Y5_R10_1282_RESPONSE_DOUBLET_COMPONENT_MAP_AUDIT.csv",
            "required_source_inputs": "parent q(Phi); unified Z basis; Dq[partial_Z]; q norm; Z norm; quotient/constraint sort; physical-lock or no-claim label",
            "priority_arenas": "R0_identity_coframe_direct;R3_gamma;R4_beta;R10_fifth_force;R11_EH_operator_ledger",
            "projection_formula": "C_qm_Z <= C_Obs_e * Dq_Z_norm * N_Z",
            "derivation_status": "NONCLAIM_FACTOR_TEMPLATE",
            "promotion_rule": "valid only if candidate_value is numeric/source-backed or theorem-zero, units are fixed, and no MISSING_* markers remain",
            "theorem_zero_adopted": False,
            "finite_value_present": False,
            "prediction_source_backed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def arena_link_rows() -> list[dict[str, object]]:
    rows = [
        ("R0_identity_coframe_direct", "eta_WEP_direct_geometry", "eta_geom_AB <= Pi_R0*C_Obs_e*Dq_Z_norm*N_Z + source/readout terms", "MISSING_PI_R0_COBS_DQZ_NZ"),
        ("R3_gamma", "gamma_minus_1", "|gamma-1| <= Pi_gamma*C_Obs_e*Dq_Z_norm*N_Z + calibration/RAB terms", "MISSING_WEAK_FIELD_METRIC_RESPONSE"),
        ("R4_beta", "beta_minus_1", "|beta-1| <= Pi_beta*C_Obs_e*Dq_Z_norm*N_Z + S_cg/source-normalization terms", "MISSING_POST_NEWTONIAN_RESPONSE"),
        ("R10_fifth_force", "delta_G_or_fifth_force_yukawa", "|alpha_pred(lambda)| <= Pi_R10(lambda)*C_Obs_e*Dq_Z_norm*N_Z plus 1503 coefficient chain", "MISSING_R10_FIELD_MAP_AND_BOUND_CURVE"),
        ("R11_EH_operator_ledger", "non_EH_operator_coefficients", "non-EH operator residual includes any Dq_Z-induced visible operator coefficient", "MISSING_OPERATOR_COEFFICIENT_VECTOR"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "arena_row_id": arena_row_id,
            "observable": observable,
            "projection_formula": formula,
            "current_status": status,
            "required_inputs": "Dq_Z_norm; C_Obs_e; N_Z; arena Pi/response matrix; source/readout/boundary guards",
            "predicted_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "comparison_ready": False,
            "prediction_source_backed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for arena_row_id, observable, formula, status in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        ("D1672_0_lock", "PHYSICAL_LOCK_NOT_PROVED", "the six-channel R_phys map exists as a requirement set but no parent-signed full-rank/coercive operator exists", "do not promote response-doublet double-zero"),
        ("D1672_1_first_factor", "DQZ_FACTOR_ROW_STAGED_NONCLAIM", "Dq_Z_norm is now a concrete factor row with units/source requirements and arena links", "fill Dq_Z_norm only with a theorem-zero or source-backed numeric/interval value"),
        ("D1672_2_best_next", "TARGET_DQZ_ZERO_OR_NUMERIC_FIRST", "Dq_Z=0 is still cleaner than bounding C_Obs_e because it kills the product at the earliest factor", "attempt q/Z basis plus Dq derivative extraction before C_Obs_e numeric work"),
        ("D1672_3_safety", "NO_GR_NEWTON_CLAIM", "a physical-lock map failure plus missing product factor cannot derive local GR/Newton", "keep all claim gates false"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def claim_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1672_0_physical_lock", "Z is full-rank/coercive over R_phys", False, "NO_CLAIM", "q_loc/Y5/Y6/PPN/boundary/coupling locks remain unsigned"),
        ("CG1672_1_response_doublet_GR", "response-doublet double-zero derives local GR/Newton", False, "NO_CLAIM", "formal auxiliary zero is not physical residual silence"),
        ("CG1672_2_DqZ_factor", "Dq_Z_norm factor is source-backed", False, "BLOCKED", "candidate value remains MISSING_NUMERIC_OR_THEOREM_ZERO"),
        ("CG1672_3_arena_score", "R0/R3/R4/R10/R11 comparisons are score-ready", False, "BLOCKED", "C_Obs_e, N_Z, arena Pi, and Dq_Z value/theorem-zero missing"),
        ("CG1672_4_public_claim", "public/local claim safe", False, "NO_CLAIM", "private derivation/audit checkpoint only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "status": status,
            "blocker": blocker,
            "local_gr_claim_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, gate_pass, status, blocker in rows
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1673-Y5-R2FR-DqZ-zero-theorem-or-first-factor-value-fill.md",
            "script": "scripts/Y5_R2FR_DqZ_zero_theorem_or_first_factor_value_fill.py",
            "objective": "try to close Dq_Z_norm=0 from q/Z basis and quotient/constraint independence; if it fails, fill Dq_Z_norm with a source-backed nonclaim numeric/interval row or a blocker ledger",
            "success_condition": "Dq_Z_norm is either theorem-zero in the parent branch or has a source-backed finite nonclaim factor value with units, source path, and arena links",
            "forbidden_shortcuts": "no invented Dq_Z value; no formal-Z-to-physical-residual leap; no cancellation; no local-GR/R10/PPN/WEP claim; no GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def all_claim_flags_false(paths: list[Path]) -> bool:
    flag_names = {
        "accepted_for_scoring",
        "claim_allowed",
        "claim_ready",
        "comparison_ready",
        "coercive_norm_component",
        "finite_value_present",
        "full_rank_component",
        "local_gr_claim_allowed",
        "parent_signed",
        "parent_signed_absence_theorem",
        "prediction_source_backed",
        "score_allowed",
        "score_ready",
        "source_backed",
        "theorem_zero_adopted",
        "valid_for_claim",
        "valid_for_mts_claim",
        "valid_prediction_row",
    }
    for path in paths:
        for row in csv_rows(path):
            for flag_name in flag_names.intersection(row):
                if bool_string(row[flag_name]) == "true":
                    return False
    return True


def no_missing_marked_ready(paths: list[Path]) -> bool:
    readiness_flags = {
        "accepted_for_scoring",
        "claim_allowed",
        "comparison_ready",
        "finite_value_present",
        "prediction_source_backed",
        "score_ready",
        "valid_for_claim",
        "valid_prediction_row",
    }
    for path in paths:
        for row in csv_rows(path):
            contains_missing = any("MISSING_" in value for value in row.values())
            if contains_missing and any(bool_string(row.get(flag, False)) == "true" for flag in readiness_flags):
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, object]],
    lock_map: list[dict[str, object]],
    rank_gate: list[dict[str, object]],
    nullspace: list[dict[str, object]],
    dqz: list[dict[str, object]],
    arenas: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim: list[dict[str, object]],
    next_targets: list[dict[str, object]],
) -> list[dict[str, object]]:
    generated_csv_parse = True
    try:
        for generated_path in GENERATED:
            csv_rows(generated_path)
    except Exception:
        generated_csv_parse = False

    formalization_dirty = (
        any("1672" in path.name for path in FORMALIZATION.rglob("*1672*"))
        if FORMALIZATION.exists()
        else False
    )
    sources_ok = all(row["path_exists"] and row["needles_found"] for row in source_rows)
    lock_failed = any(row["lock_id"] == "LOCK1672_6_verdict" and row["current_status"] == "PHYSICAL_LOCK_NOT_PROVED" for row in lock_map)
    all_channels_present = {row["lock_id"] for row in lock_map} >= {f"LOCK1672_{i}_{name}" for i, name in [(0, "q_loc"), (1, "Y5"), (2, "Y6"), (3, "PPN"), (4, "boundary"), (5, "coupling")]}
    rank_failed = any(row["gate_id"] == "RG1672_5_verdict" and row["current_status"] == "FULL_RANK_COERCIVITY_NOT_PROVED" for row in rank_gate)
    nullspace_guarded = all(row["status"] == "ACTIVE_GUARD" for row in nullspace)
    dqz_row_staged = dqz[0]["symbol"] == "Dq_Z_norm" and dqz[0]["candidate_value"] == "MISSING_NUMERIC_OR_THEOREM_ZERO"
    arena_links = {row["arena_row_id"] for row in arenas} >= {"R0_identity_coframe_direct", "R3_gamma", "R4_beta", "R10_fifth_force", "R11_EH_operator_ledger"}
    decision_next = any(row["decision"] == "DQZ_FACTOR_ROW_STAGED_NONCLAIM" for row in decisions)
    claim_gate_safe = all(row["gate_pass"] is False and row["claim_allowed"] is False for row in claim)
    next_target_selected = next_targets[0]["next_target"] == "1673-Y5-R2FR-DqZ-zero-theorem-or-first-factor-value-fill.md"
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target))
    queue_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target))

    checks = [
        ("VAL1672_0_sources_exist", sources_ok, "all cited 1672 source paths exist and needles are present"),
        ("VAL1672_1_lock_failed", lock_failed, "physical Z-to-R_phys lock is not promoted"),
        ("VAL1672_2_all_channels_present", all_channels_present, "q_loc/Y5/Y6/PPN/boundary/coupling channels are audited"),
        ("VAL1672_3_rank_failed", rank_failed, "full-rank/coercivity theorem remains not proved"),
        ("VAL1672_4_nullspace_guards", nullspace_guarded, "physical nullspace guards remain active"),
        ("VAL1672_5_dqz_row_staged", dqz_row_staged, "first Dq_Z factor row is staged as nonclaim"),
        ("VAL1672_6_arena_links", arena_links, "Dq_Z factor row links to R0/R3/R4/R10/R11 arenas"),
        ("VAL1672_7_decision_next", decision_next, "decision records Dq_Z nonclaim factor row"),
        ("VAL1672_8_claim_gate_safe", claim_gate_safe, "all claim gates keep local claims false"),
        ("VAL1672_9_no_mts_claim_flags", all_claim_flags_false(CLAIM_CHECKED), "all 1672 generated rows keep claim/no-score flags false"),
        ("VAL1672_10_missing_not_ready", no_missing_marked_ready(CLAIM_CHECKED), "no row containing MISSING_* is marked source-backed, claim-ready, or score-ready"),
        ("VAL1672_11_next_target_selected", next_target_selected, "next target selects Dq_Z zero theorem or first factor value fill"),
        ("VAL1672_12_csv_parse", generated_csv_parse, "all generated 1672 CSVs parse"),
        ("VAL1672_13_branch_copies", branch_copies, "branch/quarantine copies exist"),
        ("VAL1672_14_queue_copies", queue_copies, "acquisition queue nonclaim copies exist"),
        ("VAL1672_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1672_16_formalization_untouched", not formalization_dirty, "no 1672 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1672_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1672 Z physical-lock map or first Dq_Z factor source-row validation",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[column]).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    source_rows: list[dict[str, object]],
    lock_map: list[dict[str, object]],
    rank_gate: list[dict[str, object]],
    nullspace: list[dict[str, object]],
    dqz: list[dict[str, object]],
    arenas: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 1672 - Z Physical-Lock Map Or First DqZ Factor Source Row

**Private status:** physical-lock theorem attempt plus first nonclaim `Dq_Z_norm` factor row. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, orbital pass, or public claim is made.

## Verdict

The response-doublet route still matters, but it does **not** yet derive local GR/Newton.

The required theorem is:

```text
Z^A = N^A_I R_phys^I + O(R_phys^2)
rank(N)=dim(R_phys) after gauge quotient
c_- ||R_phys||^2 <= <Z,MZ> <= c_+ ||R_phys||^2
J_I = B_I = 0 for compact local vacuum
```

Current result: the six physical channels are named, but the full-rank/coercive map is not parent-signed. Therefore `Z=0` is still formal auxiliary silence, not measured local-GR silence.

The fallback is now concrete:

```text
C_qm_Z <= C_Obs_e * Dq_Z_norm * N_Z
```

`1672` stages `Dq_Z_norm` as the first nonclaim factor row.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Z To Rphys Lock Map Attempt

{markdown_table(lock_map, ["lock_id", "physical_channel", "candidate_lock", "current_status", "blocker", "next_input"])}

## Full-Rank Coercivity Gate

{markdown_table(rank_gate, ["gate_id", "criterion", "current_status", "failure_mode"])}

## Physical Nullspace Ledger

{markdown_table(nullspace, ["nullspace_id", "nullspace_risk", "why_it_matters", "status"])}

## First DqZ Factor Source Row

{markdown_table(dqz, ["row_id", "symbol", "definition", "units", "candidate_value", "current_status", "projection_formula"])}

## DqZ Arena Links

{markdown_table(arenas, ["arena_row_id", "observable", "projection_formula", "current_status", "predicted_value"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Working Interpretation

This is progress in the painful but useful sense: the theory now has a named theorem that would actually matter. If the `Z -> R_phys` map becomes full-rank and coercive, the response-doublet mechanism can become a real local-GR route. If not, `Dq_Z_norm` is the first honest empirical factor to fill. No vibes, no footwork hidden from the judges.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    lock_map = lock_map_rows()
    rank_gate = rank_gate_rows()
    nullspace = nullspace_rows()
    dqz = dqz_first_row()
    arenas = arena_link_rows()
    decisions = decision_rows()
    claim = claim_rows()
    next_targets = next_rows()

    for path, rows in [
        (SOURCE_REGISTER, source_rows),
        (LOCK_MAP_ATTEMPT, lock_map),
        (RANK_GATE, rank_gate),
        (NULLSPACE_LEDGER, nullspace),
        (DQZ_FIRST_ROW, dqz),
        (ARENA_LINKS, arenas),
        (DECISION, decisions),
        (CLAIM_GATE, claim),
        (NEXT_TARGET, next_targets),
    ]:
        write_csv(path, rows)

    copy_outputs()
    validation = validation_rows(source_rows, lock_map, rank_gate, nullspace, dqz, arenas, decisions, claim, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, lock_map, rank_gate, nullspace, dqz, arenas, decisions, claim, next_targets, validation)

    if any(row["result"] == "FAIL" for row in validation):
        raise SystemExit("1672 validation failed; see P8_Y5_BRR545_1672_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print("1672 validation PASS")


if __name__ == "__main__":
    main()
