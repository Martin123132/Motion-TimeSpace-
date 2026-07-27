from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1736"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1736 - Dq Tau Commutator Zero Or First Finite Bound Row"
UTC = datetime.now(timezone.utc).isoformat()


def yesno(value: bool) -> str:
    return "True" if value else "False"


def no() -> str:
    return "False"


SOURCES = [
    {
        "source_id": "SRC1736_0_1735_doc",
        "source_key": "1735_handoff_doc",
        "source_path": ROOT / "1735-Y5-R2FR-Dq-tau-theta-leak-source-pack-units-and-arena-projections.md",
        "needles": ["NEXT1735_0_primary", "VAL1735_OVERALL"],
    },
    {
        "source_id": "SRC1736_1_1735_units",
        "source_key": "1735_unit_conventions",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1735_THETA_LEAK_UNIT_CONVENTIONS.csv",
        "needles": ["E_Dq_tau_commutator_norm", "q_map;Dq;tangent_norm"],
    },
    {
        "source_id": "SRC1736_2_1734_projectability",
        "source_key": "1734_Dq_tau_projectability_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1734_DQ_TAU_PROJECTABILITY_AUDIT.csv",
        "needles": ["DTP1734_3_vertical_distribution_invariant", "MISSING_DQ_TAU_COMMUTATOR"],
    },
    {
        "source_id": "SRC1736_3_1734_theorem",
        "source_key": "1734_projectable_current_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1734_PROJECTABLE_CURRENT_THEOREM.csv",
        "needles": ["PCT1734_1_tau_commutator_law", "OBSTRUCTION_DEFINED_NOT_ZEROED"],
    },
    {
        "source_id": "SRC1736_4_1505_Dq_verticality",
        "source_key": "1505_Dq_verticality_tests",
        "source_path": RESIDUALS / "P8_Y5_R10_1505_DQ_VERTICALITY_TESTS.csv",
        "needles": ["DQT1505_8_acceptance", "BLOCKED"],
    },
    {
        "source_id": "SRC1736_5_1667_q_audit",
        "source_key": "1667_quotient_map_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1667_QUOTIENT_MAP_AUDIT.csv",
        "needles": ["QMA1667_6_verdict", "Q_NOT_COMPUTABLE_CURRENT_CORPUS"],
    },
    {
        "source_id": "SRC1736_6_1667_Dq_tests",
        "source_key": "1667_Dq_on_Zphi_tests",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv",
        "needles": ["DQT1667_6_verdict", "DQ_ZPHI_NOT_CLOSED_RETAIN_LEAK"],
    },
    {
        "source_id": "SRC1736_7_684_tau_audit",
        "source_key": "684_tau_generator_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_684_TAU_GENERATOR_AUDIT.csv",
        "needles": ["TGA684_6_total", "NO_PARENT_SIGNED_TAU_LOCK"],
    },
    {
        "source_id": "SRC1736_8_688_symgrad_tau",
        "source_key": "688_symgrad_tau",
        "source_path": RESIDUALS / "P8_Y5_R10_688_SYMGRAD_TAU_DECOMPOSITION.csv",
        "needles": ["SGT688_8_verdict", "source_input_required_nonclaim"],
    },
    {
        "source_id": "SRC1736_9_1519_coframe_tau",
        "source_key": "1519_coframe_tau_lock",
        "source_path": RESIDUALS / "P8_Y5_PARENT_FRAME_1519_COFRAME_TAU_LOCK_AUDIT.csv",
        "needles": ["OCF1519_7_verdict", "COFRAME_TAU_LOCK_NOT_PROVED"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1736_SOURCE_REGISTER.csv",
    "proof_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1736_COMMUTATOR_PROOF_AUDIT.csv",
    "theorem_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1736_COMMUTATOR_THEOREM_ATTEMPT.csv",
    "finite_bound_schema": RESIDUALS / "P8_Y5_PARENT_QLOC_1736_FIRST_FINITE_BOUND_ROW_SCHEMA.csv",
    "arena_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1736_ARENA_IMPACT_ROWS.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1736_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1736_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1736_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1736_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1736_VALIDATION.csv",
}


COPY_MAP = {
    "proof_audit": "R2FR_1736_COMMUTATOR_PROOF_AUDIT.csv",
    "theorem_attempt": "R2FR_1736_COMMUTATOR_THEOREM_ATTEMPT.csv",
    "finite_bound_schema": "R2FR_1736_FIRST_FINITE_BOUND_ROW_SCHEMA.csv",
    "arena_impact": "R2FR_1736_ARENA_IMPACT_ROWS.csv",
    "runner_refusal": "R2FR_1736_RUNNER_REFUSAL.csv",
    "decision": "R2FR_1736_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1736_CLAIM_GATE.csv",
    "next_target": "R2FR_1736_NEXT_TARGET.csv",
}


PROOF_CLAUSES = [
    {
        "clause_id": "DTC1736_0_q_explicit",
        "clause": "computable parent quotient q",
        "required_statement": "q maps the parent field chart to observed quotient data before matter, clock, source, boundary and orbit readout.",
        "mathematical_test": "q: Phi_parent -> Q_obs exists and Dq is a computable differential on the retained tangent directions.",
        "current_status": "Q_NOT_COMPUTABLE_CURRENT_CORPUS",
        "blocker": "1667 records q as a partial contract rather than a parent-signed computable map.",
    },
    {
        "clause_id": "DTC1736_1_vertical_basis",
        "clause": "vertical basis and Dq kernel",
        "required_statement": "each tested v is explicitly in ker(Dq), not just called gauge or vertical by analogy.",
        "mathematical_test": "Dq[v_a]=0 for every retained vertical generator v_a.",
        "current_status": "DQ_KERNEL_UNSIGNED",
        "blocker": "1505/1667 keep the unified X/Z/phi/RAB basis and Dq computation missing.",
    },
    {
        "clause_id": "DTC1736_2_tau_projectable",
        "clause": "tau projects through q",
        "required_statement": "the observed-time generator descends to a reduced generator on Q_obs.",
        "mathematical_test": "Dq(L_tau Phi)=L_tau_red q(Phi), with one tau for source, charge, clock, orbit and boundary.",
        "current_status": "NO_PARENT_SIGNED_TAU_LOCK",
        "blocker": "684/685/742 leave tau roles split and not parent-owned.",
    },
    {
        "clause_id": "DTC1736_3_vertical_invariance",
        "clause": "tau preserves vertical equivalence",
        "required_statement": "if v is vertical then the tau bracket with v is also vertical.",
        "mathematical_test": "[L_tau,v] in ker(Dq), equivalently Dq([L_tau,v])=0 when Dq(v)=0.",
        "current_status": "COMMUTATOR_NOT_COMPUTABLE",
        "blocker": "q, Dq, vertical basis, tau action and bracket action are not all sourced.",
    },
    {
        "clause_id": "DTC1736_4_reduced_bracket",
        "clause": "reduced bracket owner",
        "required_statement": "L_tau_red is the pushforward of L_tau rather than a separately fitted observed-time flow.",
        "mathematical_test": "[L_tau_red,Dq(v)] is defined in the same quotient tangent norm as Dq([L_tau,v]).",
        "current_status": "REDUCED_GENERATOR_NOT_OWNED",
        "blocker": "tau_red is not constructed from a parent q-pushforward.",
    },
    {
        "clause_id": "DTC1736_5_norm_units",
        "clause": "norm and local time scale",
        "required_statement": "the commutator magnitude has a declared quotient norm and observed-time unit.",
        "mathematical_test": "||E_Dq_tau|| has quotient_norm/time units or is made dimensionless by an explicit local time scale.",
        "current_status": "NORM_CONVENTION_STAGED_INPUTS_MISSING",
        "blocker": "1735 declared units but no tangent norm or local time scale is sourced.",
    },
    {
        "clause_id": "DTC1736_6_source_readout_guard",
        "clause": "source/readout reopening guard",
        "required_statement": "source, matter, clock, orbit and boundary readouts cannot reintroduce the killed direction.",
        "mathematical_test": "D_source/readout[Dq(v)]=0 and no marker/source charge survives the quotient.",
        "current_status": "READOUT_REOPENING_NOT_EXCLUDED",
        "blocker": "1023/1519/1734 keep matter coupling, markers, hidden frames, source and boundary channels open.",
    },
    {
        "clause_id": "DTC1736_7_verdict",
        "clause": "commutator theorem-zero verdict",
        "required_statement": "DTC1736_0 through DTC1736_6 all pass in the same parent branch.",
        "mathematical_test": "E_Dq_tau[v]=Dq([L_tau,v])-[L_tau_red,Dq(v)]=0 for all retained vertical v.",
        "current_status": "THEOREM_ZERO_NOT_SIGNED",
        "blocker": "the exact conditional theorem is valid, but the parent instantiation is missing q/Dq/tau/vertical/norm/readout inputs.",
    },
]


ARENA_ROWS = [
    {
        "arena_row_id": "R0_identity_coframe_direct",
        "arena_family": "WEP",
        "observable": "eta_WEP_direct_geometry",
        "bound_reference": "local_bound_claims.csv",
        "commutator_role": "nonprojectable tau can make direct coframe acceleration frame-dependent",
        "projection_requirement": "same observed coframe plus tau/source/readout lock",
        "predicted_residual": "MISSING_NUMERIC_OR_THEOREM_ZERO",
        "blocker": "MISSING_COFRAME_TAU_READOUT_PROJECTION",
    },
    {
        "arena_row_id": "R3_gamma",
        "arena_family": "PPN_light",
        "observable": "gamma_minus_1",
        "bound_reference": "local_bound_claims.csv",
        "commutator_role": "Dq/tau leak can feed weak-field spatial metric response",
        "projection_requirement": "projectable current response into g_ij at O(c^-2)",
        "predicted_residual": "MISSING_NUMERIC_OR_THEOREM_ZERO",
        "blocker": "MISSING_GAMMA_PROJECTABLE_CURRENT_RESPONSE",
    },
    {
        "arena_row_id": "R5_alpha1",
        "arena_family": "PPN_preferred_frame",
        "observable": "alpha1",
        "bound_reference": "local_bound_claims.csv",
        "commutator_role": "tau nonprojectability can act like preferred-frame vector leakage",
        "projection_requirement": "vector response from parent tau and hidden frame source",
        "predicted_residual": "MISSING_NUMERIC_OR_THEOREM_ZERO",
        "blocker": "MISSING_ALPHA1_TAU_FRAME_PROJECTION",
    },
    {
        "arena_row_id": "R6_alpha2",
        "arena_family": "PPN_preferred_frame",
        "observable": "alpha2",
        "bound_reference": "local_bound_claims.csv",
        "commutator_role": "anisotropic tau leak can seed preferred-frame/spin alignment residual",
        "projection_requirement": "anisotropic response map and spin/tau alignment",
        "predicted_residual": "MISSING_NUMERIC_OR_THEOREM_ZERO",
        "blocker": "MISSING_ALPHA2_TAU_ANISOTROPY_MAP",
    },
    {
        "arena_row_id": "R9_Gdot",
        "arena_family": "orbital_Gdot",
        "observable": "dlnG_eff_dt",
        "bound_reference": "local_bound_claims.csv",
        "commutator_role": "nonprojectable tau can make measured GM drift with readout choice",
        "projection_requirement": "tau/orbit/source derivative map in yr^-1",
        "predicted_residual": "MISSING_NUMERIC_OR_THEOREM_ZERO",
        "blocker": "MISSING_GDOT_TAU_MARKER_DERIVATIVE",
    },
    {
        "arena_row_id": "R10_fifth_force",
        "arena_family": "R10_short_range",
        "observable": "alpha(lambda)",
        "bound_reference": "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "commutator_role": "finite E_Dq_tau can become a short-range source/test response coefficient",
        "projection_requirement": "lambda, tau_R10, beta/source/test legs, material geometry and alpha(lambda) curve",
        "predicted_residual": "MISSING_NUMERIC_OR_THEOREM_ZERO",
        "blocker": "MISSING_R10_THETA_TAU_FIELD_MAP_AND_BOUND_CURVE",
    },
    {
        "arena_row_id": "R11_EH_operator_ledger",
        "arena_family": "operator_closure",
        "observable": "non_EH_operator_coefficients",
        "bound_reference": "symbolic_operator_closure",
        "commutator_role": "if not zero, the leak is a non-Einstein-Hilbert operator source rather than local GR",
        "projection_requirement": "operator basis and current-descent coefficient vector",
        "predicted_residual": "MISSING_NUMERIC_OR_THEOREM_ZERO",
        "blocker": "MISSING_CURRENT_DESCENT_OPERATOR_VECTOR",
    },
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def source_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": yesno(exists),
                "needles": ";".join(needles),
                "needles_present": yesno(exists and all(needle in text for needle in needles)),
                "checked_utc": UTC,
            }
        )
    return rows


def proof_audit_rows() -> list[dict[str, Any]]:
    rows = []
    for clause in PROOF_CLAUSES:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                **clause,
                "parent_signed": no(),
                "theorem_zero_available": no(),
                "finite_row_required": "True",
                "valid_for_claim": no(),
                "claim_allowed": no(),
            }
        )
    return rows


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "THM1736_0_exact_conditional",
            "statement": "If q is a smooth parent quotient, tau is q-projectable, and the vertical distribution is tau-invariant, then the Dq/tau commutator vanishes on vertical directions.",
            "mathematical_form": "for v in ker(Dq): E_Dq_tau[v]=Dq([L_tau,v])-[L_tau_red,Dq(v)]=0",
            "proof_step": "projectability gives Dq(L_tau)=L_tau_red(q); vertical invariance gives [L_tau,v] in ker(Dq); Dq(v)=0 makes the reduced bracket term vanish.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_current_claim": "MISSING_Q_MAP;MISSING_DQ;MISSING_VERTICAL_BASIS;MISSING_TAU_ACTION;MISSING_TAU_PROJECTABILITY;MISSING_NORM;MISSING_READOUT_GUARD",
            "theorem_zero_if_clauses_signed": "True",
            "current_claim_status": "FAIL_CURRENT_CLAIM",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "THM1736_1_naturality_identity",
            "statement": "The desired zero is a naturality/projectability identity, not a fitted cancellation.",
            "mathematical_form": "Dq_*[T,V]=[Dq_*T,Dq_*V] when T is q-related to T_red and V is vertical",
            "proof_step": "because Dq_*V=0, the quotient bracket is [T_red,0]=0; the parent bracket must remain vertical.",
            "proof_status": "ROUTE_IDENTIFIED_NOT_PARENT_INSTANTIATED",
            "missing_for_current_claim": "MISSING_PARENT_Q_RELATED_TAU_AND_VERTICAL_DISTRIBUTION",
            "theorem_zero_if_clauses_signed": "True",
            "current_claim_status": "CONDITIONAL_ONLY",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "THM1736_2_current_instantiation",
            "statement": "Current MTS signs the theorem-zero for E_Dq_tau.",
            "mathematical_form": "DTC1736_0..DTC1736_6 all parent-signed in one branch",
            "proof_step": "not satisfied: q/Dq/tau/vertical/norm/readout clauses all remain unsigned or staged.",
            "proof_status": "THEOREM_ZERO_NOT_SIGNED",
            "missing_for_current_claim": "DTC1736_0_TO_DTC1736_6_UNSIGNED",
            "theorem_zero_if_clauses_signed": no(),
            "current_claim_status": "FAIL_CURRENT_CLAIM",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "THM1736_3_finite_fallback",
            "statement": "If any theorem-zero clause remains unsigned, E_Dq_tau must be retained as a finite source row.",
            "mathematical_form": "epsilon_E_Dq_tau := ||Dq([L_tau,v])-[L_tau_red,Dq(v)]||",
            "proof_step": "the retained row is nonclaim until numeric source inputs or a zero theorem are provided.",
            "proof_status": "FINITE_ROW_REQUIRED_NONCLAIM",
            "missing_for_current_claim": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "theorem_zero_if_clauses_signed": no(),
            "current_claim_status": "SOURCE_ROW_STAGED_ONLY",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def finite_bound_schema_rows() -> list[dict[str, Any]]:
    base = {
        "branch_id": BRANCH_ID,
        "system_id": "local_exterior_or_R10_test_system_MISSING",
        "q_map_id": "MISSING_Q_MAP",
        "vertical_basis_id": "MISSING_VERTICAL_BASIS",
        "tau_id": "MISSING_PARENT_TAU",
        "Dq_matrix": "MISSING_DQ_MATRIX",
        "Lt_parent_action": "MISSING_LTAU_PARENT_ACTION",
        "Lt_reduced_action": "MISSING_LTAU_REDUCED_ACTION",
        "commutator_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
        "norm": "MISSING_QUOTIENT_TANGENT_NORM",
        "local_time_scale": "MISSING_LOCAL_TIME_SCALE",
        "units": "quotient_norm_per_time_or_dimensionless_MISSING",
        "source_path": "MISSING_SOURCE_PATH",
        "prediction_source_backed": no(),
        "accepted_for_scoring": no(),
        "score_ready": no(),
        "valid_prediction_row": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    }
    rows = [
        {
            **base,
            "row_id": "EDT1736_0_total_commutator_norm",
            "component_id": "E_Dq_tau_commutator_norm",
            "formula": "||Dq([L_tau,v])-[L_tau_red,Dq(v)]||",
            "status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "projection_targets": "R0_WEP;R3_gamma;R5_alpha1;R6_alpha2;R9_Gdot;R10_fifth_force;R11_operator_closure",
        },
        {
            **base,
            "row_id": "EDT1736_1_q_map_source",
            "component_id": "q_map",
            "formula": "q(Phi_parent)->Q_obs",
            "status": "MISSING_Q_MAP",
            "projection_targets": "all_local_arenas",
        },
        {
            **base,
            "row_id": "EDT1736_2_Dq_kernel_source",
            "component_id": "Dq_kernel",
            "formula": "Dq[v_a]=0 or finite value",
            "status": "MISSING_DQ_AND_VERTICAL_BASIS",
            "projection_targets": "all_local_arenas",
        },
        {
            **base,
            "row_id": "EDT1736_3_tau_projectability_source",
            "component_id": "tau_projectability",
            "formula": "Dq(L_tau Phi)-L_tau_red q(Phi)",
            "status": "MISSING_PARENT_TAU_LOCK",
            "projection_targets": "WEP;clock;orbital;PPN;R10",
        },
        {
            **base,
            "row_id": "EDT1736_4_vertical_invariance_source",
            "component_id": "vertical_distribution_invariance",
            "formula": "Dq([L_tau,v_a])",
            "status": "MISSING_COMMUTATOR_ACTION",
            "projection_targets": "PPN;R10;operator_closure",
        },
        {
            **base,
            "row_id": "EDT1736_5_norm_units_source",
            "component_id": "quotient_norm_and_units",
            "formula": "||E_Dq_tau|| * t_local or ||E_Dq_tau||/norm_ref",
            "status": "MISSING_NORM_AND_LOCAL_TIME_SCALE",
            "projection_targets": "all_numeric_comparisons",
        },
    ]
    return rows


def arena_impact_rows() -> list[dict[str, Any]]:
    rows = []
    for arena in ARENA_ROWS:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                **arena,
                "input_row": "EDT1736_0_total_commutator_norm",
                "arena_ready": no(),
                "comparison_ready": no(),
                "valid_for_claim": no(),
                "claim_allowed": no(),
            }
        )
    return rows


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUNREF1736_0_commutator_numeric_runner",
            "runner_or_comparison": "E_Dq_tau finite source comparison",
            "required_inputs": "q_map_id;vertical_basis_id;tau_id;Dq_matrix;Lt_parent_action;Lt_reduced_action;commutator_value;norm;local_time_scale;source_path",
            "current_status": "REFUSE_RUN",
            "reason": "all numeric/theorem-zero source fields remain missing",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUNREF1736_1_R10_alpha_runner",
            "runner_or_comparison": "R10 alpha(lambda) projection",
            "required_inputs": "finite E_Dq_tau row;R10 theta/tau field map;source/test couplings;digitized alpha(lambda) curve",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "E_Dq_tau and R10 projection are nonclaim placeholders",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUNREF1736_2_PPN_WEP_clock_orbit",
            "runner_or_comparison": "local PPN/WEP/clock/orbit smoke comparison",
            "required_inputs": "arena projection maps from E_Dq_tau into observables and empirical bounds",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "arena maps remain missing; no local-GR/PPN/Newton pass is allowed",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1736_0_exact_route",
            "decision": "EXACT_CONDITIONAL_THEOREM_IDENTIFIED",
            "reason": "the Dq/tau commutator vanishes if q is explicit, tau is q-projectable, and tau preserves ker(Dq)",
            "next_action": "try to source q, Dq, vertical basis and tau pushforward in one parent chart",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1736_1_current_verdict",
            "decision": "CURRENT_ZERO_PROOF_FAILS_FOR_CLAIM",
            "reason": "q/Dq/vertical/tau/norm/source-readout clauses are unsigned in the current corpus",
            "next_action": "retain E_Dq_tau as finite nonclaim source row",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1736_2_first_finite_row",
            "decision": "FINITE_BOUND_ROW_SCHEMA_STAGED",
            "reason": "a source-backed row now states exactly what numbers or theorem-zero are needed before any comparison",
            "next_action": "do not run claim comparator until row fields are real",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1736_3_best_next_domino",
            "decision": "TARGET_Q_DQ_VERTICAL_BASIS_FIRST",
            "reason": "without q/Dq and vertical basis, every later commutator/coupling/readout proof cycles",
            "next_action": "build q-map/Dq vertical-basis source row or prove a coframe functor zero",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1736_0_q_map",
            "claim": "q is computable for local branch",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "MISSING_Q_MAP",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1736_1_Dq_kernel",
            "claim": "Dq vertical kernel is parent-signed",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "MISSING_DQ_AND_VERTICAL_BASIS",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1736_2_tau_projectable",
            "claim": "tau descends through q",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "NO_PARENT_SIGNED_TAU_LOCK",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1736_3_commutator_zero",
            "claim": "E_Dq_tau_commutator_norm=0",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "THEOREM_ZERO_NOT_SIGNED",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1736_4_finite_bound_score",
            "claim": "finite E_Dq_tau row can be scored against local bounds",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "MISSING_NUMERIC_OR_THEOREM_ZERO_AND_ARENA_PROJECTIONS",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1736_5_local_GR_Newton",
            "claim": "local GR/Newton limit passes from commutator route",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "NO_QLOC_ZERO_NO_PPN_NO_NEWTON_CLAIM",
            "claim_allowed": no(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1736_0_primary",
            "next_target": "1737-Y5-R2FR-q-map-Dq-vertical-basis-source-row-or-coframe-functor-zero.md",
            "script": "scripts/Y5_R2FR_q_map_Dq_vertical_basis_source_row_or_coframe_functor_zero.py",
            "objective": "make q, Dq and the vertical basis explicit enough to compute E_Dq_tau, or prove the observed coframe functor kills the leak",
            "success_condition": "parent-signed q/Dq vertical-basis theorem-zero or finite source-backed Dq rows ready for first arena smoke comparison",
            "selection_status": "selected",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1736_1_parallel_source_readout",
            "next_target": "1736b-Y5-R2FR-source-readout-Dq-tau-leak-first-bound-row.md",
            "script": "scripts/Y5_R2FR_source_readout_Dq_tau_leak_first_bound_row.py",
            "objective": "fill source/readout Dq-tau leak rows if the q/Dq source hunt cannot close",
            "success_condition": "source, clock, orbit and boundary readout maps declared with units and source paths",
            "selection_status": "held_parallel",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1736_2_later_LX",
            "next_target": "1738-Y5-R2FR-vertical-symplectic-silence-LX-QX-proof-attempt.md",
            "script": "scripts/Y5_R2FR_vertical_symplectic_silence_LX_QX_proof_attempt.py",
            "objective": "try deriving Theta_X/Q_X silence from sector L_X after q/Dq and commutator/source-readout rows are staged",
            "success_condition": "Theta_X/Q_X theorem-zero or explicit finite boundary/source residual rows",
            "selection_status": "later",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "proof_audit": proof_audit_rows(),
        "theorem_attempt": theorem_attempt_rows(),
        "finite_bound_schema": finite_bound_schema_rows(),
        "arena_impact": arena_impact_rows(),
        "runner_refusal": runner_refusal_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    def cell(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1736_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1736_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {
        "accepted_for_scoring",
        "arena_ready",
        "claim_allowed",
        "comparison_ready",
        "prediction_source_backed",
        "score_allowed",
        "score_ready",
        "theorem_zero_available",
        "valid_for_claim",
        "valid_prediction_row",
    }
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    readiness = {
        "accepted_for_scoring",
        "arena_ready",
        "claim_allowed",
        "comparison_ready",
        "prediction_source_backed",
        "score_ready",
        "valid_for_claim",
        "valid_prediction_row",
    }
    for rows in rows_map.values():
        for row in rows:
            contains_missing = any("MISSING_" in str(value) for value in row.values())
            if contains_missing and any(str(row.get(flag, "")).lower() == "true" for flag in readiness):
                return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1736_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1736_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1736*"):
        path_text = str(path)
        if "\\.venv\\" in path_text or "\\__pycache__\\" in path_text:
            continue
        if path.is_file():
            return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    source_register = rows_map["source_register"]
    proof_rows = rows_map["proof_audit"]
    theorem_rows = rows_map["theorem_attempt"]
    finite_rows = rows_map["finite_bound_schema"]
    arena_rows = rows_map["arena_impact"]
    runner_rows = rows_map["runner_refusal"]
    decision = rows_map["decision"]
    claim_rows = rows_map["claim_gate"]
    next_rows = rows_map["next_target"]

    required_finite_fields = {
        "system_id",
        "q_map_id",
        "vertical_basis_id",
        "tau_id",
        "Dq_matrix",
        "Lt_parent_action",
        "Lt_reduced_action",
        "commutator_value",
        "norm",
        "local_time_scale",
        "source_path",
    }

    validation = [
        check("VAL1736_0_sources_exist", all(row["exists"] == "True" for row in source_register), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1736_1_needles_present", all(row["needles_present"] == "True" for row in source_register), "required source needles are present", "one or more required source needles missing"),
        check("VAL1736_2_proof_clauses_complete", {row["clause_id"] for row in proof_rows} == {clause["clause_id"] for clause in PROOF_CLAUSES}, "commutator proof audit covers all required clauses", "proof audit missing a clause"),
        check("VAL1736_3_zero_not_signed", all(row["theorem_zero_available"] == "False" and row["claim_allowed"] == "False" for row in proof_rows), "no proof clause signs the zero theorem", "a proof clause opened the zero theorem"),
        check("VAL1736_4_exact_conditional_recorded", any(row["theorem_id"] == "THM1736_0_exact_conditional" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem_rows), "exact conditional commutator theorem is recorded", "exact conditional theorem row missing"),
        check("VAL1736_5_current_claim_fails", any(row["theorem_id"] == "THM1736_2_current_instantiation" and row["proof_status"] == "THEOREM_ZERO_NOT_SIGNED" for row in theorem_rows), "current instantiation explicitly fails for claim", "current theorem failure row missing"),
        check("VAL1736_6_finite_schema_fields", required_finite_fields.issubset(set(finite_rows[0].keys())), "finite source row schema has q/Dq/tau/commutator/norm/source fields", "finite source row schema missing required fields"),
        check("VAL1736_7_finite_rows_nonclaim", all(row["valid_for_claim"] == "False" and row["score_ready"] == "False" for row in finite_rows), "finite commutator rows remain nonclaim and not score-ready", "finite commutator row became claim-ready or score-ready"),
        check("VAL1736_8_arenas_nonclaim", all(row["arena_ready"] == "False" and row["claim_allowed"] == "False" for row in arena_rows), "arena impact rows are blocked nonclaim", "an arena impact row opened a claim flag"),
        check("VAL1736_9_runners_refuse", all(row["current_status"].startswith("REFUSE") and row["claim_allowed"] == "False" for row in runner_rows), "claim runners refuse missing commutator/projection inputs", "a runner refusal row failed to refuse"),
        check("VAL1736_10_decision_next_domino", any(row["decision_id"] == "DEC1736_3_best_next_domino" and row["decision"] == "TARGET_Q_DQ_VERTICAL_BASIS_FIRST" for row in decision), "decision selects q/Dq/vertical basis as next domino", "decision ledger did not select q/Dq/vertical basis"),
        check("VAL1736_11_claim_gates_safe", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claim_rows), "all claim gates keep local claims false", "one or more claim gates opened"),
        check("VAL1736_12_no_claim_flags", no_claim_flags(rows_map), "all generated rows keep claim/no-score flags false", "one or more generated flags enabled a claim"),
        check("VAL1736_13_missing_not_ready", missing_rows_not_ready(rows_map), "no row containing MISSING_* is marked source-backed, claim-ready, or score-ready", "a missing row is marked ready"),
        check("VAL1736_14_next_selected", any(row["route_id"] == "NEXT1736_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selects q-map/Dq/vertical-basis source row or coframe functor zero", "next target missing selected primary route"),
        check("VAL1736_15_csv_parse", parsed_ok, "all generated 1736 CSVs parse", "one or more generated 1736 CSVs failed to parse"),
        check("VAL1736_16_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1736_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1736_18_formalization_untouched", formalization_untouched(), "no 1736 outputs found under formalization-workbench", "1736 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1736_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1736 Dq/tau commutator theorem-zero or first finite bound row validation" if overall else "one or more 1736 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- The exact commutator-zero route exists: if `q` is explicit, `tau` is `q`-projectable, and `tau` preserves `ker(Dq)`, then `E_Dq_tau[v]=0` for vertical `v`.",
        "- Current MTS cannot claim that zero yet because `q`, `Dq`, the vertical basis, the `tau` pushforward, the norm, and the readout guard are not parent-signed.",
        "- Therefore 1736 stages the first finite nonclaim row for `E_Dq_tau_commutator_norm` instead of pretending the local branch has closed.",
        "- No R10, WEP, PPN, clock, orbital, Newton, local-GR, or `q_loc=0` claim is made.",
        "",
        "## Why This Is The Right Pressure Point",
        "This is a clean bit of maths rather than a tuning argument. If the quotient geometry is real, the commutator dies by projectability/naturality. If it does not die, the failure is not vague anymore: it is a measured source row that must be bounded against WEP, PPN, clocks, or R10.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Commutator Proof Audit",
        markdown_table(rows_map["proof_audit"], ["clause_id", "clause", "mathematical_test", "current_status", "blocker", "theorem_zero_available"]),
        "",
        "## Theorem Attempt",
        markdown_table(rows_map["theorem_attempt"], ["theorem_id", "statement", "mathematical_form", "proof_status", "missing_for_current_claim"]),
        "",
        "## First Finite Bound Row Schema",
        markdown_table(rows_map["finite_bound_schema"], ["row_id", "component_id", "formula", "status", "q_map_id", "vertical_basis_id", "tau_id", "commutator_value", "norm", "source_path"]),
        "",
        "## Arena Impact Rows",
        markdown_table(rows_map["arena_impact"], ["arena_row_id", "arena_family", "observable", "commutator_role", "projection_requirement", "predicted_residual", "blocker"]),
        "",
        "## Runner Refusal",
        markdown_table(rows_map["runner_refusal"], ["runner_id", "runner_or_comparison", "current_status", "reason"]),
        "",
        "## Decisions",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "1736 gives us the clean fork. The nice route is not dead: `E_Dq_tau=0` is exactly what a true quotient geometry should give. But the corpus does not yet supply the quotient geometry. So the best attack is now the upstream owner problem: build `q`, `Dq`, and the vertical basis in one parent chart, or accept a finite commutator leak and test it.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1736-Y5-R2FR-Dq-tau-commutator-zero-or-first-finite-bound-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1736_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1736 validation FAIL")
    print("1736 validation PASS")


if __name__ == "__main__":
    main()
