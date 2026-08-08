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
CHECKPOINT = "2885"

DOC = ROOT / "2885-Y5-R2FR-DqZ-zero-theorem-or-first-factor-value-fill-under-AX1090.md"

SRC_2884_DOC = ROOT / "2884-Y5-R2FR-Z-physical-lock-map-or-first-DqZ-factor-source-row-under-AX1090.md"
SRC_2884_NEXT = RESIDUALS / "P8_Y5_R2FR_2884_NEXT_TARGET.csv"
SRC_2884_DQZ = RESIDUALS / "P8_Y5_R2FR_2884_FIRST_DQZ_FACTOR_SOURCE_ROW_NONCLAIM.csv"
SRC_2884_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2884_VALIDATION.csv"

SRC_1671_DOC = ROOT / "1671-Y5-R2FR-DqZ-basis-kernel-or-Cobs-operator-norm-input.md"
SRC_1671_QUEUE = RESIDUALS / "P8_Y5_PARENT_QLOC_1671_PRODUCT_FACTOR_QUEUE.csv"
SRC_1673_ATTEMPT = RESIDUALS / "P8_Y5_PARENT_QLOC_1673_DQZ_ZERO_THEOREM_ATTEMPT.csv"
SRC_1673_CONDITIONS = RESIDUALS / "P8_Y5_PARENT_QLOC_1673_DQZ_ZERO_THEOREM_CONDITIONS.csv"
SRC_1673_VALUE = RESIDUALS / "P8_Y5_PARENT_QLOC_1673_DQZ_FACTOR_VALUE_FILL_NONCLAIM.csv"
SRC_1674_MATRIX = RESIDUALS / "P8_Y5_PARENT_QLOC_1674_DQZ_COMPONENT_DERIVATIVE_MATRIX.csv"
SRC_1674_UPDATE = RESIDUALS / "P8_Y5_PARENT_QLOC_1674_DQZ_FACTOR_VALUE_UPDATE_NONCLAIM.csv"
SRC_1675_LEAK = RESIDUALS / "P8_Y5_PARENT_QLOC_1675_SURVIVING_DQZ_LEAK_VECTOR_NONCLAIM.csv"
SRC_1675_UPDATE = RESIDUALS / "P8_Y5_PARENT_QLOC_1675_DQZ_FACTOR_UPDATE_NONCLAIM.csv"

SRC_2213_AUDIT = RESIDUALS / "P8_Y5_PARENT_QLOC_2213_JA_BA_DQZ_CLAUSE_AUDIT.csv"
SRC_2214_DESCENT = RESIDUALS / "P8_Y5_PARENT_QLOC_2214_DQZ_SOURCE_DESCENT_PROOF_ATTEMPT.csv"

SRC_2643_GATE = RESIDUALS / "P8_Y5_COMMON_DESCENT_DQZ_2643_PARENT_SIGNATURE_THEOREM_GATE.csv"
SRC_2643_LEAK = RESIDUALS / "P8_Y5_COMMON_DESCENT_DQZ_2643_DQZ_JH_LEAK_BOUND_ROWS.csv"
SRC_2643_ARENA = RESIDUALS / "P8_Y5_COMMON_DESCENT_DQZ_2643_ARENA_LEAK_MAP.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2885_SOURCE_REGISTER.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_2885_DQZ_ZERO_THEOREM_CONTRACT.csv",
    "attempt": RESIDUALS / "P8_Y5_R2FR_2885_DQZ_ZERO_PROOF_ATTEMPT.csv",
    "factor": RESIDUALS / "P8_Y5_R2FR_2885_DQZ_FACTOR_VALUE_OR_BLOCKER_LEDGER.csv",
    "leaks": RESIDUALS / "P8_Y5_R2FR_2885_SURVIVING_LEAK_ACQUISITION_ROWS.csv",
    "arena": RESIDUALS / "P8_Y5_R2FR_2885_ARENA_PROJECTION_MAP_NONCLAIM.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2885_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2885_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2885_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2885_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2885_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2885_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "factor_copy": SOURCE_WEIGHT / "RAB_DQZ_ZERO_OR_FACTOR_BLOCKER_LEDGER_2885_NONCLAIM.csv",
    "leak_copy": LOCAL_BOUNDS / "RAB_DQZ_SURVIVING_LEAK_ACQUISITION_2885_NONCLAIM.csv",
    "arena_copy": BETA_DOCS / "RAB_DQZ_ARENA_PROJECTION_MAP_2885_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2885_Qvis_signature_or_finite_DqZ_component_NEXT.csv",
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
        ("SRC2885_0_2884_doc", SRC_2884_DOC, "Status: `Y5_R2FR_2884_Z_physical_lock_not_proved_DqZ_factor_staged_2885_next`;## Next Target", "2884 handoff"),
        ("SRC2885_1_2884_next", SRC_2884_NEXT, "NEXT2884_0_2885", "explicit 2885 target"),
        ("SRC2885_2_2884_dqz", SRC_2884_DQZ, "DQZ2884_0_first_factor_row;Dq_Z_norm", "staged Dq_Z factor row"),
        ("SRC2885_3_2884_validation", SRC_2884_VALIDATION, "VAL2884_OVERALL", "2884 validation"),
        ("SRC2885_4_1671_doc", SRC_1671_DOC, "Dq_Z=0;C_qm_Z <=", "1671 Dq_Z theorem and product split"),
        ("SRC2885_5_1671_queue", SRC_1671_QUEUE, "PFQ1671_0_clean_kill;PFQ1671_2_finite_product", "1671 product factor queue"),
        ("SRC2885_6_1673_attempt", SRC_1673_ATTEMPT, "ZTA1673_0_kernel_route;ZTA1673_3_verdict", "1673 Dq_Z zero proof attempt"),
        ("SRC2885_7_1673_conditions", SRC_1673_CONDITIONS, "ZC1673_0_parent_chart;ZC1673_6_norms", "1673 theorem conditions"),
        ("SRC2885_8_1673_value", SRC_1673_VALUE, "DQZVAL1673_0_first_factor_value;MISSING_SOURCE_BACKED_UPPER_BOUND", "1673 value fill blocker"),
        ("SRC2885_9_1674_matrix", SRC_1674_MATRIX, "DQM1674_0_coframe_metric;DQM1674_5_operator_norm", "1674 component derivative matrix"),
        ("SRC2885_10_1674_update", SRC_1674_UPDATE, "DQZVAL1674_0_update;STRUCTURE_CLARIFIED_VALUE_STILL_MISSING", "1674 value update"),
        ("SRC2885_11_1675_leak", SRC_1675_LEAK, "LEAK1675_0_coframe;LEAK1675_5_residual_lock", "1675 surviving Dq_Z leak vector"),
        ("SRC2885_12_1675_update", SRC_1675_UPDATE, "DQZ1675_0_factor_status;DESCENT_ROUTE_FAILED_SURVIVING_LEAK_VECTOR_EMITTED", "1675 Dq_Z factor update"),
        ("SRC2885_13_2213_audit", SRC_2213_AUDIT, "JBD2213_3_DqZ_zero;JBD2213_6_verdict", "2213 rank-zero silence clause audit"),
        ("SRC2885_14_2214_descent", SRC_2214_DESCENT, "DSD2214_0_exact_chain_rule;DSD2214_5_verdict", "2214 Dq_Z source descent proof attempt"),
        ("SRC2885_15_2643_gate", SRC_2643_GATE, "QVIS2643_2_kernel_membership;QVIS2643_6_verdict", "2643 Q_vis parent signature gate"),
        ("SRC2885_16_2643_leak", SRC_2643_LEAK, "LEAK2643_1_Dq_Z_norm;LEAK2643_6_master_policy", "2643 Dq_Z/J_H leak rows"),
        ("SRC2885_17_2643_arena", SRC_2643_ARENA, "AM2643_0_Newton;AM2643_4_clock_EM", "2643 arena leak map"),
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


def contract_rows() -> list[dict[str, Any]]:
    theorem = "If q(Phi)=qbar(Q_vis(Phi)) and every selected v_Z is constraint-tangent or eliminated before Q_vis, with source/readout/boundary/theta silence, then Dq[v_Z]=0 and Dq_Z_norm=0."
    specs = [
        ("DZC2885_0_chain_rule", "exact chain rule", theorem, "delta_Z Obs = DObs[Dq(v_Z)] plus direct theta/source/boundary terms", "EXACT_CONDITIONAL_THEOREM", "2214 and 2643 give the exact conditional formula", "chain rule is usable only after direct terms vanish", True, False),
        ("DZC2885_1_parent_chart", "parent field chart", theorem, "Phi=(Q_vis,Z,gauge,theta,source/readout,boundary) with declared live/eliminated fields", "MISSING_PARENT_FIELD_CHART", "1673 keeps parent chart unsigned", "cannot know what partial_Z means field-by-field", False, False),
        ("DZC2885_2_computable_q", "computable q map", theorem, "q or Q_vis must be explicit enough to differentiate on selected v_Z", "MISSING_COMPUTABLE_Q_MAP", "1673/1674 keep Dq matrix missing", "Dq_Z_norm cannot be evaluated or set to zero", False, False),
        ("DZC2885_3_Z_basis", "unified Z basis", theorem, "Z^A basis must cover local q_loc/Y5/Y6/PPN/boundary/coupling residuals or be eliminated before q", "MISSING_UNIFIED_Z_BASIS", "1671 and 2884 keep component lock open", "formal Z silence can miss a measured residual", False, False),
        ("DZC2885_4_constraint_elimination", "constraint-tangent or pre-q elimination", theorem, "v_Z lies in ker(Dq) by constraint, or Z is solved out before q/matter/readout are formed", "CONSTRAINT_ROUTE_UNSIGNED", "1671/1673 identify this as best route but unsigned", "Z can remain a representative leak direction", False, False),
        ("DZC2885_5_source_readout", "matter/source/readout descent", theorem, "ordinary matter, clocks, photons, source normalization and orbit/PPN readouts depend only on Q_vis", "MISSING_SOURCE_READOUT_DESCENT", "2213/2214/2643 keep J_A/source/readout descent open", "Dq_Z=0 for geometry alone would not kill WEP/clock/GM leaks", False, False),
        ("DZC2885_6_theta_marker", "theta/no-marker silence", theorem, "constants, material markers and EM/clock standards are owned quotient data or superselection labels", "NO_MARKER_THEOREM_NOT_PARENT_SIGNED", "2643 keeps theta/material marker leak active", "clock/EM/WEP residuals can survive as direct terms", False, False),
        ("DZC2885_7_boundary_projector", "boundary/projector no-flux", theorem, "boundary primitive, source worldtube, local projector and corner terms vanish or are separately bounded", "MISSING_BOUNDARY_PROJECTOR_NO_FLUX", "1675/2213/2214 keep boundary/projector terms open", "compact local tests can see edge/projector charge", False, False),
        ("DZC2885_8_norms", "q/Z norm convention", theorem, "declare q norm, Z norm, operator norm and selected tangent normalization", "MISSING_Q_Z_NORMS", "1673 and 1674 keep N_Z and Dq_Z_norm missing", "no numeric theorem-zero or finite interval can be accepted", False, False),
        ("DZC2885_9_verdict", "Dq_Z zero theorem", theorem, "all clauses close in one parent branch", "ZERO_THEOREM_NOT_CLOSED", "only the formal chain-rule theorem is closed; parent signature is not", "Dq_Z_norm remains MISSING_NUMERIC_OR_THEOREM_ZERO", False, False),
    ]
    return [
        add_common(
            {
                "contract_id": contract_id,
                "clause": clause,
                "formal_statement": statement,
                "required_condition": condition,
                "current_status": status,
                "source_evidence": evidence,
                "failure_if_open": failure,
                "conditional_formula_valid": conditional_formula_valid,
                "condition_met": condition_met,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for contract_id, clause, statement, condition, status, evidence, failure, conditional_formula_valid, condition_met in specs
    ]


def attempt_rows() -> list[dict[str, Any]]:
    specs = [
        ("DZA2885_0_vertical_kernel", "prove v_Z in ker(Dq)", "Dq_Z_norm=0 follows if every selected Z tangent is vertical for q", "REJECT_CURRENT_PROOF", "q and Z basis are not parent-signed; Dq cannot be evaluated", "move to parent Q_vis signature or finite component rows"),
        ("DZA2885_1_constraint_first", "eliminate Z before q", "if constraints solve Z=0 before ordinary matter/readout construction, Dq_Z is not a live physical factor", "CONDITIONAL_ONLY", "constraint-first is the least-scrutiny route but the parent action does not yet sign J_Z=B_Z=0 and pre-q elimination", "derive action-level elimination order and no direct source/readout Z slot"),
        ("DZA2885_2_common_descent", "Q_vis common matter descent", "ordinary matter/readouts depend on Phi only through Q_vis; then DObs(v_Z)=DObs Dq(v_Z)", "NOT_PARENT_SIGNED", "theta, source-only weights, readouts, and boundary/projectors remain legal direct terms", "write the object-language exclusion theorem or retain leak rows"),
        ("DZA2885_3_physical_lock", "Z locks physical residual vector", "formal Z silence controls q_loc/Y5/Y6/PPN/boundary/coupling with full rank/coercive norm", "REJECT_CURRENT_PROOF", "2884 keeps Z->R_phys full-rank/coercivity unproved", "do not promote response-doublet to local GR/Newton"),
        ("DZA2885_4_finite_value", "fill Dq_Z_norm finite interval", "score fallback if Dq_Z_norm has a source-backed numeric or interval upper bound", "BLOCKED_NO_VALUE", "no current source provides q/Z norms, Dq matrix, or upper bound", "emit source-ready blocker ledger instead of inventing a number"),
        ("DZA2885_5_verdict", "2885 proof verdict", "derive Dq_Z_norm=0 or fill first factor", "ZERO_PROOF_NOT_CLOSED_FACTOR_VALUE_NOT_FILLED", "theorem clauses are explicit but unsigned; numeric row would be fabricated", "next target must attack Q_vis parent signature or first finite DqZ component row"),
    ]
    return [
        add_common(
            {
                "attempt_id": attempt_id,
                "route": route,
                "candidate_derivation": derivation,
                "current_result": result,
                "blocking_issue": blocker,
                "next_action": next_action,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for attempt_id, route, derivation, result, blocker, next_action in specs
    ]


def factor_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DQZF2885_0_Dq_Z_norm",
            "Dq_Z_norm",
            "operator norm ||Dq[v_Z]||_q / ||v_Z||_Z for selected local response directions",
            "dimensionless after q and Z norm conventions",
            "theorem_zero_or_source_backed_interval_required",
            "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "0",
            "MISSING_SOURCE_BACKED_UPPER_BOUND",
            "q(Phi); Q_vis; selected v_Z basis; q norm; Z norm; source/readout/boundary silence or finite direct terms",
            "C_qm_Z <= C_Obs_e * Dq_Z_norm * N_Z plus additive leak coefficients",
            "BLOCKED_NO_THEOREM_ZERO_OR_FINITE_VALUE",
            "promote only if theorem-zero closes or a source-backed finite interval exists with no MISSING_* markers",
        ),
        (
            "DQZF2885_1_N_Z",
            "N_Z",
            "selected Z tangent normalization ||v_Z||_Z",
            "dimensionless if unit-normalized, otherwise declared local branch units",
            "source_backed_norm_required",
            "MISSING_Z_DIRECTION_NORMALIZATION",
            "0",
            "MISSING_SOURCE_BACKED_UPPER_BOUND",
            "unified Z basis; tangent vector convention; physical channel labels",
            "C_qm_Z <= C_Obs_e * Dq_Z_norm * N_Z",
            "BLOCKED_BASIS_AND_NORM",
            "promote only after selected direction and units are declared",
        ),
        (
            "DQZF2885_2_C_Obs_e",
            "C_Obs_e",
            "observed coframe/readout operator norm ||DObs_e||_{q->e}",
            "dimensionless after q/e norms",
            "operator_norm_or_annihilator_required",
            "MISSING_OBSERVED_COFRAME_FUNCTOR",
            "0",
            "MISSING_SOURCE_BACKED_UPPER_BOUND",
            "Obs_e(Q_vis); no shadow-frame theorem; coframe/measure/connection descent",
            "E_DqZ_A <= C_A_obs * Dq_Z_norm * N_Z + direct tails",
            "BLOCKED_OBS_FUNCTOR_UNSIGNED",
            "promote only after observed-frame functor is parent-owned or finite bounded",
        ),
        (
            "DQZF2885_3_direct_tail_sum",
            "E_direct_Z",
            "sum of theta/source/readout/boundary direct terms not mediated by Dq_Z",
            "arena residual units or source-normalized",
            "component_zero_or_source_bound_required",
            "MISSING_THETA_SOURCE_READOUT_BOUNDARY_TERMS",
            "0",
            "MISSING_SOURCE_BACKED_UPPER_BOUND",
            "theta ownership; no-source-only slot; readout descent; boundary/projector no-flux",
            "eps_JH_Z_abs <= C_matter*Dq_Z_norm + eps_theta + eps_direct + eps_source_weight + eps_boundary",
            "BLOCKED_ADDITIVE_LEAKS_SURVIVE",
            "must be zero/bounded independently; no cancellation policy",
        ),
    ]
    return [
        add_common(
            {
                "row_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "value_type": value_type,
                "candidate_value": candidate,
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
                "required_source_inputs": required_inputs,
                "projection_formula": formula,
                "current_status": status,
                "promotion_rule": promotion_rule,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for row_id, symbol, definition, units, value_type, candidate, lower_bound, upper_bound, required_inputs, formula, status, promotion_rule in specs
    ]


def leak_rows() -> list[dict[str, Any]]:
    specs = [
        ("LEAK2885_0_coframe", "Dq_Z[e_obs,g_obs,mu_m,D_m]", "Pi_coframe*C_Obs_e*Dq_Z_norm*N_Z", "dimensionless or metric/coframe residual units", "MISSING_OBSERVED_COFRAME_FUNCTOR;MISSING_Q_Z_NORMS", "R0_WEP;R3_gamma;R4_beta;R11_operator", "BOUND_FORM_READY_VALUES_MISSING"),
        ("LEAK2885_1_source_weight", "Dq_Z[source normalization/J_H]", "Pi_source*Delta_w_Z + Pi_Gauss*Dq_Z_norm", "dimensionless source-normalized", "MISSING_NO_SOURCE_ONLY_SLOT;MISSING_GAUSS_SOURCE_CURRENT_OWNER", "Newton_limit;WEP;orbits;R10", "COUNTEREXAMPLE_RETAINED"),
        ("LEAK2885_2_theta_marker", "Dq_Z[theta_A, material markers, clock/EM standards]", "Pi_theta*Lie_Z(theta_A)+Pi_marker*qbar_marker_Z", "source-normalized or arena-specific", "NO_MARKER_THEOREM_NOT_PARENT_SIGNED;HIDDEN_FRAME_BAN_UNSIGNED", "clocks;fine_structure;WEP;EM", "BOUND_ROW_REQUIRED"),
        ("LEAK2885_3_readout", "Dq_Z[clock/photon/orbit/EM/PPN readouts]", "Pi_readout*Dq_Z[O_i]", "arena residual units", "MISSING_READOUT_DESCENT", "PPN;orbital;clock;EM", "ARENA_MAP_READY_VALUES_MISSING"),
        ("LEAK2885_4_boundary", "Dq_Z[B_edge,P_loc,Q_X]", "Pi_boundary*B_Z + Pi_QX*Dq_Z[Q_X]", "boundary/projector residual units", "BOUNDARY_PROJECTOR_OPEN", "R10;WEP;compact_orbit;source_measure", "BOUNDARY_ROW_REQUIRED"),
        ("LEAK2885_5_residual_lock", "Dq_Z[R_phys -> observed residuals]", "L^I_A Z^A plus unproved rank/coercive norm", "physical residual vector units", "COMPONENT_MAP_NOT_CLOSED;FULL_RANK_COERCIVITY_NOT_PROVED", "q_loc;PPN;R10;R11", "LOCK_ROW_REQUIRED"),
    ]
    return [
        add_common(
            {
                "leak_id": leak_id,
                "quantity": quantity,
                "symbolic_bound_form": formula,
                "units": units,
                "blockers": blockers,
                "priority_arenas": arenas,
                "status": status,
                "candidate_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for leak_id, quantity, formula, units, blockers, arenas, status in specs
    ]


def arena_rows() -> list[dict[str, Any]]:
    specs = [
        ("ARENA2885_0_Newton", "Newton/GM/orbital", "Delta_GM <= Pi_GM(eps_JH_Z_abs + E_DqZ_GM + source_weight + boundary/readout tails)", "FITTED_GM_GUARD_ACTIVE", "common-mode GM theorem; source map; DqZ norm; orbital projection"),
        ("ARENA2885_1_PPN", "PPN gamma/beta/preferred-frame", "Delta_PPN <= Pi_PPN(eps_JH_Z_abs + E_DqZ_PPN) plus b_g/sigma_X bridge and alpha3 boundary row", "SCHEMA_READY_VALUES_MISSING", "b_g; x_U; no-other-channel proof; PPN vector projection"),
        ("ARENA2885_2_WEP", "WEP/composition", "eta_AB <= Pi_WEP(Delta_w_abs + eps_theta_marker + E_DqZ_WEP + readout marker tail)", "NO_MARKER_AND_NO_SOURCE_SLOT_UNSIGNED", "object-language no-source-slot theorem or finite Delta_w vector; material marker map"),
        ("ARENA2885_3_R10", "R10/contact or source-test branch", "strict branch has no lambda; DqZ/source leak can only feed contact/edge/CDB-reopened finite-range rows", "STRICT_ALPHA_LAMBDA_REJECTED", "finite principal symbol if reopened; source/test charge split; real bound curve; DqZ/contact projection"),
        ("ARENA2885_4_clock_EM", "clock/time/EM", "Delta_clock/alpha_EM <= Pi_theta(eps_theta_marker + E_DqZ_clock/EM + readout standard leak)", "THETA_MARKER_DESCENT_UNSIGNED", "theta ownership; EM/fine-structure readout map; clock standard quotient descent"),
    ]
    return [
        add_common(
            {
                "arena_id": arena_id,
                "arena": arena,
                "leak_path": leak_path,
                "current_status": status,
                "missing_inputs": missing,
                "predicted_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "comparison_ready": False,
                "accepted_for_scoring": False,
            }
        )
        for arena_id, arena, leak_path, status, missing in specs
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2885_0_zero_theorem", "Dq_Z_norm=0 is parent-proved", "FAIL", "parent chart, q map, Z basis, source/readout/boundary silence and norms do not close together"),
        ("GATE2885_1_finite_value", "Dq_Z_norm finite value/interval is source-backed", "FAIL", "no numeric Dq matrix, q/Z norm or source-backed upper bound exists"),
        ("GATE2885_2_no_additive_leaks", "theta/source/readout/boundary tails are zero or bounded", "FAIL", "2643 and 2214 keep additive direct terms alive"),
        ("GATE2885_3_physical_promotion", "formal Dq_Z silence is enough for local-GR/Newton", "FAIL", "2884 keeps Z-to-R_phys physical lock unproved"),
        ("GATE2885_4_runner", "arena runner can compare predictions", "FAIL", "all prediction rows contain MISSING_* markers and claim flags are false"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": False,
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
                "runner_id": "RUN2885_0_dqz_factor_runner",
                "status": "REFUSED_DQZ_ZERO_AND_VALUE_MISSING",
                "accepted_zero_theorems": 0,
                "accepted_factor_rows": 0,
                "accepted_arena_rows": 0,
                "reason": "Dq_Z_norm remains MISSING_NUMERIC_OR_THEOREM_ZERO and additive leak rows are unbounded; no local arena comparison is allowed",
                "runner_ready": False,
                "claim_unlocked": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2885_0_theorem", "DO_NOT_ADOPT_DQZ_ZERO", "only the conditional chain-rule theorem is available; parent Q_vis, q map, Z basis and silence clauses are not signed", "keep theorem as exact contract, not a claim"),
        ("DEC2885_1_value", "DO_NOT_FILL_NUMERIC_DQZ_VALUE", "a number would be fabricated because no source-backed q/Z norm, Dq matrix or interval exists", "retain Dq_Z_norm as source-ready blocker"),
        ("DEC2885_2_route", "BEST_NEXT_ROUTE_QVIS_SIGNATURE", "a parent-owned visible quotient signature can collapse Dq_Z, J_H, theta/source/readout and boundary leaks in one stroke if it exists", "try Q_vis object-language signature before isolated empirical scoring"),
        ("DEC2885_3_fallback", "FINITE_COMPONENT_ROWS_IF_QVIS_FAILS", "if Q_vis cannot be signed, each surviving leak must become an independent finite coefficient row", "stage first finite DqZ/source/readout component acquisition"),
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
                "next_id": "NEXT2885_0_2886",
                "status": "selected_primary",
                "target_doc": "2886-Y5-R2FR-Qvis-parent-signature-or-first-finite-DqZ-component-row-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_Qvis_parent_signature_or_first_finite_DqZ_component_row_under_AX1090_2886.py",
                "mission": "try to parent-sign the visible quotient Q_vis object-language/descent signature that would make Dq_Z, J_H, theta/source/readout and boundary leaks collapse together; if it fails, fill the first finite nonclaim component row from the surviving leak ledger",
                "forbidden_shortcuts": "no Dq_Z=0 without parent q and Q_vis; no numeric Dq_Z value without source-backed matrix/norm; no cancellation; no local-GR/R10/PPN/WEP claim",
                "selected": True,
                "accepted_for_scoring": False,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("BR2885_0_factor_copy", OUTPUTS["factor"], BRANCH_OUTPUTS["factor_copy"], "source-weight copy of Dq_Z factor value/blocker ledger"),
        ("BR2885_1_leak_copy", OUTPUTS["leaks"], BRANCH_OUTPUTS["leak_copy"], "local-bounds copy of surviving Dq_Z leak acquisition rows"),
        ("BR2885_2_arena_copy", OUTPUTS["arena"], BRANCH_OUTPUTS["arena_copy"], "beta-source docs copy of arena projection map"),
        ("BR2885_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue next target"),
    ]
    rows = []
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
        "theorem_zero_adopted",
        "finite_value_present",
        "prediction_source_backed",
        "accepted_for_scoring",
        "condition_met",
        "gate_passed",
        "runner_ready",
        "claim_unlocked",
        "comparison_ready",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    contract = rows_by_name["contract"]
    attempt = rows_by_name["attempt"]
    factor = rows_by_name["factor"]
    leaks = rows_by_name["leaks"]
    arena = rows_by_name["arena"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    checks = [
        ("VAL2885_0_sources_exist", all(row["path_exists"] for row in sources), "all registered source paths exist"),
        ("VAL2885_1_source_anchors", all(row["anchors_found"] for row in sources), "all registered source anchors were found"),
        ("VAL2885_2_contract_written", len(contract) >= 10 and any(row["contract_id"] == "DZC2885_9_verdict" for row in contract), "Dq_Z zero theorem contract is explicit"),
        ("VAL2885_3_zero_not_adopted", any(row["current_status"] == "ZERO_THEOREM_NOT_CLOSED" for row in contract) and all(row["theorem_zero_adopted"] is False for row in contract), "Dq_Z zero is not adopted"),
        ("VAL2885_4_attempt_failed_cleanly", any(row["current_result"] == "ZERO_PROOF_NOT_CLOSED_FACTOR_VALUE_NOT_FILLED" for row in attempt), "proof attempt fails closed"),
        ("VAL2885_5_factor_blocker", factor[0]["symbol"] == "Dq_Z_norm" and factor[0]["candidate_value"] == "MISSING_NUMERIC_OR_THEOREM_ZERO", "Dq_Z_norm remains a source-ready blocker row"),
        ("VAL2885_6_leak_rows", len(leaks) == 6 and all(row["upper_bound"] == "MISSING_SOURCE_BACKED_UPPER_BOUND" for row in leaks), "surviving leak acquisition rows remain nonclaim"),
        ("VAL2885_7_arena_rows", len(arena) == 5 and all(row["comparison_ready"] is False for row in arena), "arena projections are mapped but not scored"),
        ("VAL2885_8_gates_fail_closed", all(row["gate_passed"] is False for row in gates), "acceptance gates fail closed"),
        ("VAL2885_9_runner_refused", runner[0]["status"] == "REFUSED_DQZ_ZERO_AND_VALUE_MISSING" and runner[0]["runner_ready"] is False, "runner remains refused"),
        ("VAL2885_10_next_target_2886", next_target[0]["next_id"] == "NEXT2885_0_2886" and next_target[0]["selected"] is True, "2886 target selected"),
        ("VAL2885_11_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2885_12_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2885_13_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2885_14_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2885_15_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2885_16_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2885_17_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2885_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2885 wrote the exact Dq_Z zero theorem contract, refused to adopt theorem-zero or a fabricated value, emitted source-ready leak/factor blockers, and selected Q_vis parent signature or first finite Dq_Z component row for 2886.",
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
    text = f"""# 2885 - Y5 R2FR DqZ Zero Theorem Or First Factor Value Fill Under AX1090

Status: `Y5_R2FR_2885_DqZ_zero_not_closed_factor_value_blocker_2886_Qvis_next`

## Private Verdict

2885 tries the derivation first.

The clean theorem exists as mathematics:

`q(Phi)=qbar(Q_vis(Phi))` and `v_Z in ker(Dq)` imply `Dq[v_Z]=0`, hence `Dq_Z_norm=0`.

But the current MTS parent branch does not yet sign the needed parent chart, computable `q`, unified `Z` basis, source/readout/theta silence, boundary/projector silence, and q/Z norm convention together. Therefore `Dq_Z_norm=0` is not adopted.

The fallback value route is also blocked: no source-backed matrix, norm, or interval upper bound exists. 2885 therefore emits a source-ready blocker/acquisition ledger rather than inventing a number.

The important progress is that the missing object is now sharper: a parent-owned `Q_vis` object-language/descent signature could collapse `Dq_Z`, `J_H`, theta/source/readout terms, and boundary/projector leaks together. That is the 2886 target.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## DqZ Zero Theorem Contract

{md_table(rows_by_name["contract"], ["contract_id", "clause", "current_status", "source_evidence", "failure_if_open", "condition_met", "valid_for_claim"])}

## DqZ Zero Proof Attempt

{md_table(rows_by_name["attempt"], ["attempt_id", "route", "current_result", "blocking_issue", "next_action", "valid_for_claim"])}

## DqZ Factor Value Or Blocker Ledger

{md_table(rows_by_name["factor"], ["row_id", "symbol", "definition", "units", "candidate_value", "upper_bound", "current_status", "valid_for_claim"])}

## Surviving Leak Acquisition Rows

{md_table(rows_by_name["leaks"], ["leak_id", "quantity", "symbolic_bound_form", "blockers", "priority_arenas", "status", "valid_for_claim"])}

## Arena Projection Map

{md_table(rows_by_name["arena"], ["arena_id", "arena", "leak_path", "current_status", "missing_inputs", "comparison_ready", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "accepted_zero_theorems", "accepted_factor_rows", "reason", "runner_ready", "valid_for_claim"])}

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
        "contract": contract_rows(),
        "attempt": attempt_rows(),
        "factor": factor_rows(),
        "leaks": leak_rows(),
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
    overall = next(row for row in validation if row["validation_id"] == "VAL2885_OVERALL")
    print(f"VAL2885_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
