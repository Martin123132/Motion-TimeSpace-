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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1739"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1739 - Parent Coframe Ownership Or Common Frame Log Derivative Row"
UTC = datetime.now(timezone.utc).isoformat()


def yesno(value: bool) -> str:
    return "True" if value else "False"


def no() -> str:
    return "False"


SOURCES = [
    {
        "source_id": "SRC1739_0_1738_doc",
        "source_key": "1738_handoff_doc",
        "source_path": ROOT / "1738-Y5-R2FR-observed-coframe-kernel-zero-or-first-finite-DObs-e-row.md",
        "needles": ["NEXT1738_0_primary", "VAL1738_OVERALL"],
    },
    {
        "source_id": "SRC1739_1_1738_theorem",
        "source_key": "1738_kernel_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1738_KERNEL_THEOREM_ATTEMPT.csv",
        "needles": ["DOK1738_1_same_coframe_not_enough", "COUNTERMODEL_SURVIVES"],
    },
    {
        "source_id": "SRC1739_2_1738_finite_rows",
        "source_key": "1738_finite_DObs_e_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1738_FINITE_DOBS_E_SOURCE_ROWS.csv",
        "needles": ["DBG1738_0_common_frame_log_derivative", "RETAINED_NONCLAIM_COMMON_FRAME_ROW"],
    },
    {
        "source_id": "SRC1739_3_1045_matter_functor",
        "source_key": "1045_parent_matter_functor_signature",
        "source_path": RESIDUALS / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "needles": ["MFS1045_6_verdict", "FAIL_CURRENT_CLAIM_PARENT_MATTER_FUNCTOR_NOT_SIGNED"],
    },
    {
        "source_id": "SRC1739_4_1720_matter_signature",
        "source_key": "1720_matter_functor_signature",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "needles": ["MFS1720_8_verdict", "MATTER_FUNCTOR_SIGNATURE_NOT_PARENT_SIGNED"],
    },
    {
        "source_id": "SRC1739_5_785_metric_coframe",
        "source_key": "785_metric_coframe_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_785_PSI_METRIC_COFRAME_CONTRACT.csv",
        "needles": ["PMC785_6_parent_action_metric_ownership", "not_derived"],
    },
    {
        "source_id": "SRC1739_6_943_coframe_coupling",
        "source_key": "943_coframe_coupling_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
        "needles": ["CFC943_7_contract_verdict", "contract_exact_but_unsigned"],
    },
    {
        "source_id": "SRC1739_7_1504_independence",
        "source_key": "1504_observed_coframe_independence",
        "source_path": RESIDUALS / "P8_Y5_R10_1504_OBSERVED_COFRAME_INDEPENDENCE_AUDIT.csv",
        "needles": ["OC1504_3_universal_conformal_countermodel", "COUNTERMODEL_SURVIVES"],
    },
    {
        "source_id": "SRC1739_8_623_functor",
        "source_key": "623_coframe_functor_theorem",
        "source_path": RESIDUALS / "P8_Y5_R10_623_COFRAME_FUNCTOR_THEOREM_ATTEMPT.csv",
        "needles": ["OCF623_4_bg_verdict", "not_closed"],
    },
    {
        "source_id": "SRC1739_9_862_pullback",
        "source_key": "862_pullback_closure",
        "source_path": RESIDUALS / "P8_Y5_R10_862_COFRAME_PULLBACK_CLOSURE_AUDIT.csv",
        "needles": ["CC862_1_strict_identity_coframe", "cleanest_route_but_not_parent_derived"],
    },
    {
        "source_id": "SRC1739_10_1229_source_coupling",
        "source_key": "1229_source_coupling_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_1229_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv",
        "needles": ["THM1229_2_countermodel", "OBSTRUCTION_ACTIVE"],
    },
    {
        "source_id": "SRC1739_11_1635_matter_descent",
        "source_key": "1635_matter_descent_signature_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1635_MATTER_DESCENT_SIGNATURE_GATE.csv",
        "needles": ["MDSG1635_7_all_clauses", "PIR_ZERO_STACK_NOT_CLOSED_CURRENT_CORPUS"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1739_SOURCE_REGISTER.csv",
    "ownership_clause_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1739_PARENT_COFRAME_OWNERSHIP_CLAUSE_GATE.csv",
    "ownership_theorem_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1739_PARENT_COFRAME_OWNERSHIP_THEOREM_ATTEMPT.csv",
    "common_frame_derivative_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1739_COMMON_FRAME_LOG_DERIVATIVE_ROWS.csv",
    "shadow_frame_countermodel_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1739_SHADOW_FRAME_COUNTERMODEL_GATE.csv",
    "local_bound_projection_schema": RESIDUALS / "P8_Y5_PARENT_QLOC_1739_BG_LOCAL_BOUND_PROJECTION_SCHEMA.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1739_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1739_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1739_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1739_VALIDATION.csv",
}


COPY_MAP = {
    "ownership_clause_gate": "R2FR_1739_PARENT_COFRAME_OWNERSHIP_CLAUSE_GATE.csv",
    "ownership_theorem_attempt": "R2FR_1739_PARENT_COFRAME_OWNERSHIP_THEOREM_ATTEMPT.csv",
    "common_frame_derivative_rows": "R2FR_1739_COMMON_FRAME_LOG_DERIVATIVE_ROWS.csv",
    "shadow_frame_countermodel_gate": "R2FR_1739_SHADOW_FRAME_COUNTERMODEL_GATE.csv",
    "local_bound_projection_schema": "R2FR_1739_BG_LOCAL_BOUND_PROJECTION_SCHEMA.csv",
    "decision": "R2FR_1739_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1739_CLAIM_GATE.csv",
    "next_target": "R2FR_1739_NEXT_TARGET.csv",
}


OWNERSHIP_CLAUSES = [
    {
        "clause_id": "PCO1739_0_parent_q",
        "clause": "parent quotient object",
        "required_statement": "q: Phi_parent -> Q_vis exists before matter, clock, source, boundary and orbital readout.",
        "mathematical_test": "Dq is computable and candidate residual directions are either in ker(Dq) or retained.",
        "current_status": "CONDITIONAL_SUPPORT_NOT_PARENT_COMPLETE",
        "blocker": "1045/1720/1738 keep q as a support condition rather than a parent construction.",
    },
    {
        "clause_id": "PCO1739_1_metric_coframe_owner",
        "clause": "observed coframe owned by parent action",
        "required_statement": "e_obs is derived as E(Q_vis), by constraint, Euler equation, or induced metric mechanism.",
        "mathematical_test": "e_obs(Phi)=E(q(Phi)) and no direct X, Z, phi, R_AB/Jq, boundary or marker argument appears.",
        "current_status": "PARENT_ACTION_METRIC_OWNERSHIP_NOT_DERIVED",
        "blocker": "785 says metric/coframe ownership is the next hard theorem, not closed.",
    },
    {
        "clause_id": "PCO1739_2_no_common_frame_derivative",
        "clause": "common-frame residual derivative vanishes",
        "required_statement": "universal Weyl/disformal/common-frame dependence on residual directions is theorem-zero.",
        "mathematical_test": "b_g,X := ||e_obs^-1 DObs_e[partial_X]|| = 0 for every local residual X.",
        "current_status": "COMMON_FRAME_COUNTERMODEL_SURVIVES",
        "blocker": "1504/623 keep e_obs=exp(b_g X)e0 and similar common-frame countermodels legal.",
    },
    {
        "clause_id": "PCO1739_3_connection_lock",
        "clause": "connection and derivative stack owned by e_obs",
        "required_statement": "omega_matter=omega[e_obs] or torsion/nonmetricity/independent connection residuals are explicitly zeroed or retained.",
        "mathematical_test": "Domega_m[X]=Domega[e_obs](DObs_e[X]) with no independent connection force channel.",
        "current_status": "CONNECTION_LOCK_UNSIGNED",
        "blocker": "785/943 leave connection and hidden frame clauses conditional.",
    },
    {
        "clause_id": "PCO1739_4_matter_functor",
        "clause": "ordinary matter functor uses the owned coframe",
        "required_statement": "S_ord=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_A] with an owned vertical lift.",
        "mathematical_test": "delta_X S_ord at fixed Q_vis has no direct matter-frame derivative except retained rows.",
        "current_status": "MATTER_FUNCTOR_SIGNATURE_NOT_PARENT_SIGNED",
        "blocker": "1045/1720 keep ordinary matter functor and vertical lift unsigned.",
    },
    {
        "clause_id": "PCO1739_5_constants_superselection",
        "clause": "material constants are not residual fields",
        "required_statement": "masses, charges, alpha_EM, clock constants and material labels are quotient-owned or retained explicitly.",
        "mathematical_test": "Lie_X theta_A=0 and Lie_X m_A=0, or b_A/b_alpha rows are finite.",
        "current_status": "CONSTANT_SUPERSELECTION_UNSIGNED",
        "blocker": "1045/1720/1635 keep constants and material marker clauses unsigned.",
    },
    {
        "clause_id": "PCO1739_6_no_source_prefactor",
        "clause": "no hidden source-only matter prefactor",
        "required_statement": "S_ord cannot contain w_A(X)S_A or source-only action weights unless they are universal or retained.",
        "mathematical_test": "delta w_A=0, w_A=w_*, or P_loc nabla_mu[sum_A delta w_A T_A^munu] is bounded.",
        "current_status": "SOURCE_PREFACTOR_COUNTERMODEL_SURVIVES",
        "blocker": "1229 countermodel shows source weights can leave equations looking unchanged while changing Hilbert source.",
    },
    {
        "clause_id": "PCO1739_7_boundary_endpoint_silence",
        "clause": "boundary and endpoint data do not move the local coframe",
        "required_statement": "P_loc partial_Q_endpoint e_obs=0 and boundary/projector coframe leakage is exact, zero-flux, or retained.",
        "mathematical_test": "P_loc DObs_e[v_boundary]=0 with no clock/WEP/PPN endpoint leakage.",
        "current_status": "BOUNDARY_ENDPOINT_SILENCE_OPEN",
        "blocker": "862/1738 keep endpoint and boundary silence open.",
    },
    {
        "clause_id": "PCO1739_8_tau_source_normal_lock",
        "clause": "tau/source normal lock",
        "required_statement": "J_H[tau] and rho_H=T_obs(n,tau) use the same observed frame and tau before calibration.",
        "mathematical_test": "tau, n, source support, clock time and orbit readout all descend through Q_vis.",
        "current_status": "TAU_SOURCE_NORMAL_LOCK_UNSIGNED",
        "blocker": "1720 keeps tau/source normal lock unsigned.",
    },
    {
        "clause_id": "PCO1739_9_verdict",
        "clause": "parent coframe ownership verdict",
        "required_statement": "PCO1739_0 through PCO1739_8 all pass in one parent branch.",
        "mathematical_test": "e_obs=E(Q_vis), b_g=0, connection/matter/source/readout cannot reopen the local residual.",
        "current_status": "PARENT_COFRAME_OWNERSHIP_NOT_SIGNED",
        "blocker": "the theorem form is clear but ownership, no-shadow-frame, source prefactor, boundary and tau clauses are unsigned.",
    },
]


BG_ROWS = [
    {
        "row_id": "BG1739_0_generic",
        "symbol": "b_g,X",
        "direction": "generic coframe-relevant residual X",
        "definition": "common-frame log derivative of the observed coframe",
        "formula": "b_g,X := ||e_obs^-1 DObs_e[partial_X]||",
        "units": "dimensionless_per_declared_X_unit_or_component_norm_MISSING",
        "source_anchor": "DBG1738_0_common_frame_log_derivative",
    },
    {
        "row_id": "BG1739_1_Z",
        "symbol": "b_g,Z",
        "direction": "Z response-doublet residual",
        "definition": "common-frame derivative along v_Z",
        "formula": "||e_obs^-1 DObs_e[v_Z]||",
        "units": "dimensionless_per_Z_unit_or_component_norm_MISSING",
        "source_anchor": "DOE1738_0_vZ",
    },
    {
        "row_id": "BG1739_2_phi",
        "symbol": "b_g,phi",
        "direction": "trace-free improvement auxiliary",
        "definition": "common-frame derivative along v_phi",
        "formula": "||e_obs^-1 DObs_e[v_phi]||",
        "units": "dimensionless_per_phi_unit_or_component_norm_MISSING",
        "source_anchor": "DOE1738_1_vphi",
    },
    {
        "row_id": "BG1739_3_RAB_Jq",
        "symbol": "b_g,RAB",
        "direction": "R_AB/J_q cell or radial response",
        "definition": "common-frame derivative along v_RAB/Jq",
        "formula": "||e_obs^-1 DObs_e[v_RAB/Jq]||",
        "units": "dimensionless_per_RAB_unit_or_component_norm_MISSING",
        "source_anchor": "DOE1738_2_vRAB_Jq",
    },
    {
        "row_id": "BG1739_4_boundary",
        "symbol": "b_g,boundary",
        "direction": "boundary/projector endpoint",
        "definition": "local projection of boundary-induced coframe derivative",
        "formula": "||e_obs^-1 P_loc DObs_e[v_boundary]||",
        "units": "dimensionless_boundary_projection_norm_MISSING",
        "source_anchor": "DOE1738_3_vboundary",
    },
    {
        "row_id": "BG1739_5_total_abs",
        "symbol": "epsilon_bg_abs",
        "direction": "all coframe-relevant residuals",
        "definition": "absolute no-cancellation envelope for common-frame coframe leakage",
        "formula": "|b_g,Z|+|b_g,phi|+|b_g,RAB|+|b_g,boundary|+other sourced b_g rows",
        "units": "common_dimensionless_norm_MISSING",
        "source_anchor": "DOE1738_4_total_coframe_kernel_envelope",
    },
]


SHADOW_GATES = [
    {
        "gate_id": "SFC1739_0_Weyl",
        "countermodel": "e_obs=exp(b_g X)e0",
        "survives_because": "a single coframe can still be X-dependent and locally physical",
        "zero_or_bound_required": "b_g,X=0 theorem or finite b_g bound",
    },
    {
        "gate_id": "SFC1739_1_disformal",
        "countermodel": "g_obs=C(X)g0+D(X)u_mu u_nu",
        "survives_because": "universal disformal dependence can create PPN/clock/preferred-frame residuals",
        "zero_or_bound_required": "C_X=D_X=0 theorem or finite PPN/clock rows",
    },
    {
        "gate_id": "SFC1739_2_source_prefactor",
        "countermodel": "S_ord=sum_A w_A(X)S_A",
        "survives_because": "source weights can alter Hilbert stress even when matter equations look unchanged",
        "zero_or_bound_required": "w_A quotient-equivalent/null-projected or source residual bound",
    },
    {
        "gate_id": "SFC1739_3_boundary_endpoint",
        "countermodel": "e_obs=E(Q_vis,Q_endpoint) with local endpoint derivative",
        "survives_because": "boundary/cosmological memory can leak into local coframe without projection silence",
        "zero_or_bound_required": "P_loc partial_Q_endpoint e_obs=0 or finite endpoint row",
    },
]


BOUND_SCHEMAS = [
    {
        "projection_id": "BGP1739_0_WEP",
        "arena": "WEP",
        "observable": "eta_AB",
        "mapping_need": "composition/source/readout response to common-frame derivative and marker rows",
        "bound_source": "local_bound_claims.csv",
    },
    {
        "projection_id": "BGP1739_1_PPN_gamma_beta",
        "arena": "PPN",
        "observable": "gamma_minus_1;beta_minus_1",
        "mapping_need": "weak-field metric response from b_g and source normalization",
        "bound_source": "local_bound_claims.csv",
    },
    {
        "projection_id": "BGP1739_2_PPN_preferred_frame",
        "arena": "PPN_preferred_frame",
        "observable": "alpha1;alpha2;alpha3;xi",
        "mapping_need": "disformal/vector/tau-frame response tied to common-frame derivative",
        "bound_source": "local_bound_claims.csv",
    },
    {
        "projection_id": "BGP1739_3_clock",
        "arena": "clock",
        "observable": "Delta nu/nu;alpha_clock",
        "mapping_need": "clock standards response to b_g, constants and tau mismatch",
        "bound_source": "local_bound_claims.csv",
    },
    {
        "projection_id": "BGP1739_4_R10",
        "arena": "R10_short_range",
        "observable": "alpha(lambda)",
        "mapping_need": "range, material geometry, source/test legs and b_g-induced Yukawa coefficient",
        "bound_source": "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
    },
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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


def ownership_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            **clause,
            "parent_signed": no(),
            "ownership_theorem_closed": no(),
            "finite_row_required": "True",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for clause in OWNERSHIP_CLAUSES
    ]


def ownership_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PCO1739_THM0_chain_rule_bg_zero",
            "statement": "If the parent action owns e_obs=E(Q_vis) and X is excluded from Q_vis or lies in ker(Dq), then b_g,X=0.",
            "mathematical_form": "b_g,X=||e_obs^-1 DE[Dq(partial_X)]||=0",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_current_claim": "MISSING_PARENT_Q;MISSING_PARENT_COFRAME_OWNERSHIP;MISSING_DQ_KERNEL;MISSING_NO_SHADOW_FRAME_RULE",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PCO1739_THM1_parent_ownership_current",
            "statement": "Current MTS signs parent coframe ownership and common-frame derivative zero.",
            "mathematical_form": "PCO1739_0..PCO1739_8 all pass and BG1739_i=0",
            "proof_status": "PARENT_COFRAME_OWNERSHIP_NOT_SIGNED",
            "missing_for_current_claim": "OWNERSHIP_STACK_UNSIGNED;COMMON_FRAME_COUNTERMODELS_SURVIVE;SOURCE_PREFACTOR_SURVIVES",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PCO1739_THM2_finite_fallback",
            "statement": "If parent coframe ownership is unsigned, b_g must be retained as a finite local residual.",
            "mathematical_form": "epsilon_bg_abs=sum_i |b_g,i| with no cancellation credit",
            "proof_status": "FINITE_BG_ROW_REQUIRED_NONCLAIM",
            "missing_for_current_claim": "MISSING_NUMERIC_OR_THEOREM_ZERO_AND_ARENA_MAPS",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def bg_rows() -> list[dict[str, Any]]:
    rows = []
    for row in BG_ROWS:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                **row,
                "value_or_formula": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "source_path": "MISSING_SOURCE_PATH",
                "status": "RETAINED_NONCLAIM_BG_ROW",
                "accepted_for_scoring": no(),
                "score_ready": no(),
                "valid_prediction_row": no(),
                "valid_for_claim": no(),
                "claim_allowed": no(),
            }
        )
    return rows


def shadow_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            **gate,
            "excluded_by_current_parent": no(),
            "finite_row_required": "True",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for gate in SHADOW_GATES
    ]


def bound_projection_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            **schema,
            "required_bg_inputs": "BG1739_0_generic;BG1739_5_total_abs;arena_response_map;source_path",
            "predicted_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "comparison_status": "BLOCKED_PENDING_BG_AND_ARENA_MAP",
            "comparison_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for schema in BOUND_SCHEMAS
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1739_0_exact_theorem",
            "decision": "PARENT_COFRAME_OWNERSHIP_WOULD_KILL_BG",
            "reason": "if e_obs factorizes through Q_vis and the residual is vertical/excluded, b_g=0 follows by chain rule",
            "next_action": "keep deriving parent coframe ownership; this remains the cleanest local-GR route",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1739_1_current_verdict",
            "decision": "PARENT_COFRAME_OWNERSHIP_NOT_SIGNED",
            "reason": "metric ownership, no-shadow-frame, matter functor, constants, source prefactor, boundary and tau clauses remain unsigned",
            "next_action": "retain b_g/common-frame rows as finite nonclaim local residuals",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1739_2_testing_bridge",
            "decision": "BG_ROW_IS_THE_TESTABLE_INTERFACE",
            "reason": "if b_g is finite, it projects into WEP, PPN, clocks, R10 and orbital arenas",
            "next_action": "do not score until b_g values and arena response maps are source-backed",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1739_3_best_next_domino",
            "decision": "TARGET_NO_SHADOW_FRAME_ZERO_OR_BG_BOUND_MAP",
            "reason": "the surviving countermodels are Weyl/disformal/source-prefactor routes; they must be zeroed or bounded",
            "next_action": "attempt no-shadow-frame theorem or build b_g bound projection rows",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1739_0_parent_coframe",
            "claim": "parent action owns e_obs=E(Q_vis)",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "PARENT_COFRAME_OWNERSHIP_NOT_SIGNED",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1739_1_bg_zero",
            "claim": "b_g,X=0 for coframe-relevant residuals",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "COMMON_FRAME_COUNTERMODEL_SURVIVES",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1739_2_bg_bound_score",
            "claim": "finite b_g rows can be scored",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "MISSING_BG_VALUES_AND_ARENA_RESPONSE_MAPS",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1739_3_local_GR",
            "claim": "local GR/Newton follows from parent coframe ownership",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "NO_EINSTEIN_REDUCTION_NO_SOURCE_NORMALIZATION_NO_BIANCHI_GATE",
            "claim_allowed": no(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1739_0_primary",
            "next_target": "1740-Y5-R2FR-no-shadow-frame-zero-or-bg-bound-projection-map.md",
            "script": "scripts/Y5_R2FR_no_shadow_frame_zero_or_bg_bound_projection_map.py",
            "objective": "try to prove common Weyl/disformal/source-prefactor routes are forbidden by parent matter/coframe ownership, or build b_g bound projection maps",
            "success_condition": "no-shadow-frame theorem-zero or source-backed nonclaim b_g-to-WEP/PPN/R10 projection schema",
            "selection_status": "selected",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1739_1_parallel_readout_marker",
            "next_target": "1740b-Y5-R2FR-source-readout-marker-Dq-zero-or-finite-row.md",
            "script": "scripts/Y5_R2FR_source_readout_marker_Dq_zero_or_finite_row.py",
            "objective": "prove source/readout and marker functors descend through q, or keep finite leak rows",
            "success_condition": "source/readout and marker rows source-backed with units and nonclaim comparisons",
            "selection_status": "held_parallel",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1739_2_later_tau",
            "next_target": "1741-Y5-R2FR-tau-pushforward-on-qvis-or-finite-Dtau-row.md",
            "script": "scripts/Y5_R2FR_tau_pushforward_on_qvis_or_finite_Dtau_row.py",
            "objective": "prove the observed-time generator is the pushforward of one parent tau on Q_vis",
            "success_condition": "tau pushforward theorem or finite Dtau row for commutator and PPN gates",
            "selection_status": "later",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "ownership_clause_gate": ownership_clause_rows(),
        "ownership_theorem_attempt": ownership_theorem_rows(),
        "common_frame_derivative_rows": bg_rows(),
        "shadow_frame_countermodel_gate": shadow_gate_rows(),
        "local_bound_projection_schema": bound_projection_rows(),
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
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1739_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1739_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {
        "accepted_for_scoring",
        "claim_allowed",
        "comparison_ready",
        "excluded_by_current_parent",
        "gate_pass",
        "ownership_theorem_closed",
        "parent_signed",
        "score_allowed",
        "score_ready",
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
        "claim_allowed",
        "comparison_ready",
        "excluded_by_current_parent",
        "gate_pass",
        "ownership_theorem_closed",
        "parent_signed",
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
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1739_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1739_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1739*"):
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
    clauses = rows_map["ownership_clause_gate"]
    theorem_rows = rows_map["ownership_theorem_attempt"]
    bg = rows_map["common_frame_derivative_rows"]
    shadow = rows_map["shadow_frame_countermodel_gate"]
    projection = rows_map["local_bound_projection_schema"]
    decision = rows_map["decision"]
    claim_rows = rows_map["claim_gate"]
    next_rows = rows_map["next_target"]

    validation = [
        check("VAL1739_0_sources_exist", all(row["exists"] == "True" for row in source_register), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1739_1_needles_present", all(row["needles_present"] == "True" for row in source_register), "required source needles are present", "one or more required source needles missing"),
        check("VAL1739_2_ownership_clauses_complete", {row["clause_id"] for row in clauses} == {row["clause_id"] for row in OWNERSHIP_CLAUSES}, "parent coframe ownership gate covers all required clauses", "ownership gate missing clause"),
        check("VAL1739_3_ownership_not_signed", all(row["parent_signed"] == "False" and row["claim_allowed"] == "False" for row in clauses), "no parent coframe ownership clause is signed for claim", "an ownership clause opened claim"),
        check("VAL1739_4_exact_theorem_recorded", any(row["theorem_id"] == "PCO1739_THM0_chain_rule_bg_zero" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem_rows), "exact conditional b_g zero theorem is recorded", "conditional b_g zero theorem missing"),
        check("VAL1739_5_current_theorem_blocked", any(row["theorem_id"] == "PCO1739_THM1_parent_ownership_current" and row["proof_status"] == "PARENT_COFRAME_OWNERSHIP_NOT_SIGNED" for row in theorem_rows), "current parent coframe ownership claim is blocked", "blocked parent ownership theorem row missing"),
        check("VAL1739_6_bg_rows_nonclaim", all(row["status"] == "RETAINED_NONCLAIM_BG_ROW" and row["score_ready"] == "False" for row in bg), "b_g/common-frame rows are retained nonclaim and not score-ready", "b_g row became score-ready or claim-ready"),
        check("VAL1739_7_shadow_countermodels_active", all(row["excluded_by_current_parent"] == "False" for row in shadow), "shadow-frame/source-prefactor countermodels remain active", "a countermodel was incorrectly excluded"),
        check("VAL1739_8_projection_schema_blocked", all(row["comparison_ready"] == "False" and row["claim_allowed"] == "False" for row in projection), "b_g local-bound projection schema remains blocked nonclaim", "projection schema opened comparison/claim"),
        check("VAL1739_9_decision_next_domino", any(row["decision_id"] == "DEC1739_3_best_next_domino" and row["decision"] == "TARGET_NO_SHADOW_FRAME_ZERO_OR_BG_BOUND_MAP" for row in decision), "decision selects no-shadow-frame zero or b_g bound map as next domino", "decision ledger did not select no-shadow-frame/bg route"),
        check("VAL1739_10_claim_gates_safe", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claim_rows), "all claim gates keep local claims false", "one or more claim gates opened"),
        check("VAL1739_11_no_claim_flags", no_claim_flags(rows_map), "all generated rows keep claim/no-score flags false", "one or more generated flags enabled a claim"),
        check("VAL1739_12_missing_not_ready", missing_rows_not_ready(rows_map), "no row containing MISSING_* is marked source-backed, claim-ready, or score-ready", "a missing row is marked ready"),
        check("VAL1739_13_next_selected", any(row["route_id"] == "NEXT1739_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selects no-shadow-frame zero or b_g bound projection map", "next target missing selected primary route"),
        check("VAL1739_14_csv_parse", parsed_ok, "all generated 1739 CSVs parse", "one or more generated 1739 CSVs failed to parse"),
        check("VAL1739_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1739_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1739_17_formalization_untouched", formalization_untouched(), "no 1739 outputs found under formalization-workbench", "1739 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1739_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1739 parent coframe ownership or common-frame log-derivative row validation" if overall else "one or more 1739 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- Parent coframe ownership would kill the common-frame derivative cleanly: `e_obs=E(Q_vis)` plus vertical/excluded residuals gives `b_g=0` by the chain rule.",
        "- Current MTS does not yet sign that ownership stack: parent `q`, metric/coframe ownership, no-shadow-frame, matter functor, constants, source-prefactor, boundary, and tau/source-normal clauses remain unsigned.",
        "- Therefore `b_g` is now the correct finite nonclaim local metric residual, not a vague worry.",
        "- If `b_g` is derived zero, the local-GR route gets much cleaner; if finite, it must be mapped to WEP/PPN/clock/R10 bounds.",
        "- No local-GR, Newton, WEP, PPN, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Parent Coframe Ownership Gate",
        markdown_table(rows_map["ownership_clause_gate"], ["clause_id", "clause", "mathematical_test", "current_status", "blocker"]),
        "",
        "## Ownership Theorem Attempt",
        markdown_table(rows_map["ownership_theorem_attempt"], ["theorem_id", "statement", "mathematical_form", "proof_status", "missing_for_current_claim"]),
        "",
        "## Common Frame Log Derivative Rows",
        markdown_table(rows_map["common_frame_derivative_rows"], ["row_id", "symbol", "direction", "formula", "value_or_formula", "status"]),
        "",
        "## Shadow Frame Countermodel Gate",
        markdown_table(rows_map["shadow_frame_countermodel_gate"], ["gate_id", "countermodel", "survives_because", "zero_or_bound_required"]),
        "",
        "## Local Bound Projection Schema",
        markdown_table(rows_map["local_bound_projection_schema"], ["projection_id", "arena", "observable", "mapping_need", "predicted_value", "comparison_status"]),
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
        "This is now a proper field-theory fork. Either the parent action owns the observed coframe and forbids shadow common-frame/source-prefactor routes, or MTS carries a finite `b_g` residual that must survive the local bound gauntlet. That is the right kind of hard problem.",
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
    doc_path = ROOT / "1739-Y5-R2FR-parent-coframe-ownership-or-common-frame-log-derivative-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1739_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1739 validation FAIL")
    print("1739 validation PASS")


if __name__ == "__main__":
    main()
