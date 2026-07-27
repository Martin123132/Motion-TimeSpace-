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
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1735"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1735 - Dq Tau Theta Leak Source Pack Units And Arena Projections"
UTC = datetime.now(timezone.utc).isoformat()


def yesno(value: bool) -> str:
    return "True" if value else "False"


def no() -> str:
    return "False"


SOURCES = [
    {
        "source_id": "SRC1735_0_1734_doc",
        "source_key": "1734_doc",
        "source_path": ROOT / "1734-Y5-R2FR-current-descent-lemma-Dq-tau-projectability-or-theta-leak-row.md",
        "needles": ["NEXT1734_0_primary", "E_Dq_tau"],
    },
    {
        "source_id": "SRC1735_1_1734_next",
        "source_key": "1734_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1734_NEXT_TARGET.csv",
        "needles": ["1735-Y5-R2FR-Dq-tau-theta-leak-source-pack-units-and-arena-projections.md", "selected"],
    },
    {
        "source_id": "SRC1735_2_1734_leak_rows",
        "source_key": "1734_theta_Qtau_leak_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1734_THETA_QTAU_LEAK_ROWS.csv",
        "needles": ["TLR1734_4_total_theta_qtau_leak", "MISSING_COMMON_UNITS"],
    },
    {
        "source_id": "SRC1735_3_1734_validation",
        "source_key": "1734_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1734_VALIDATION.csv",
        "needles": ["VAL1734_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1735_4_1669_doc",
        "source_key": "1669_Dq_projection_precedent",
        "source_path": ROOT / "1669-Y5-R2FR-Dq-leak-bound-source-pack-units-and-arena-projections.md",
        "needles": ["Dq Leak Bound Source Pack Units", "VAL1669_OVERALL"],
    },
    {
        "source_id": "SRC1735_5_1669_arena_matrix",
        "source_key": "1669_arena_matrix",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1669_ARENA_PROJECTION_MATRIX.csv",
        "needles": ["R10_fifth_force", "MISSING_R10_FIELD_MAP_AND_BOUND_CURVE"],
    },
    {
        "source_id": "SRC1735_6_local_bounds",
        "source_key": "local_bound_claims",
        "source_path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "needles": ["R10_fifth_force", "alpha(lambda)"],
    },
    {
        "source_id": "SRC1735_7_1402_shared_tau",
        "source_key": "1402_shared_tau_transfer",
        "source_path": RESIDUALS / "P8_Y5_R10_1402_SHARED_TAU_TRANSFER_THEOREM_AUDIT.csv",
        "needles": ["DTT1402_7_current_verdict", "SHARED_TRANSFER_NOT_DERIVED_ARENA_ISOLATION_REQUIRED"],
    },
    {
        "source_id": "SRC1735_8_1053_tau_projection",
        "source_key": "1053_tau_projection_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_1053_TAU_WEP_R10_PROJECTION_AUDIT.csv",
        "needles": ["TPR1053_4_verdict", "TRANSFER_BLOCKED"],
    },
    {
        "source_id": "SRC1735_9_688_symgrad_tau",
        "source_key": "688_symgrad_tau",
        "source_path": RESIDUALS / "P8_Y5_R10_688_SYMGRAD_TAU_DECOMPOSITION.csv",
        "needles": ["SGT688_8_verdict", "source_input_required_nonclaim"],
    },
    {
        "source_id": "SRC1735_10_1519_coframe_tau",
        "source_key": "1519_coframe_tau_lock",
        "source_path": RESIDUALS / "P8_Y5_PARENT_FRAME_1519_COFRAME_TAU_LOCK_AUDIT.csv",
        "needles": ["OCF1519_7_verdict", "COFRAME_TAU_LOCK_NOT_PROVED"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1735_SOURCE_REGISTER.csv",
    "unit_conventions": RESIDUALS / "P8_Y5_PARENT_QLOC_1735_THETA_LEAK_UNIT_CONVENTIONS.csv",
    "arena_matrix": RESIDUALS / "P8_Y5_PARENT_QLOC_1735_ARENA_PROJECTION_MATRIX.csv",
    "r10_template": RESIDUALS / "P8_Y5_PARENT_QLOC_1735_R10_SOURCE_PACK_TEMPLATE.csv",
    "local_template": RESIDUALS / "P8_Y5_PARENT_QLOC_1735_PPN_WEP_CLOCK_ORBIT_SOURCE_PACK_TEMPLATE.csv",
    "bound_placeholders": RESIDUALS / "P8_Y5_PARENT_QLOC_1735_BOUND_COMPARISON_PLACEHOLDERS.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1735_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1735_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1735_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1735_VALIDATION.csv",
}


COPY_MAP = {
    "unit_conventions": "R2FR_1735_THETA_LEAK_UNIT_CONVENTIONS.csv",
    "arena_matrix": "R2FR_1735_ARENA_PROJECTION_MATRIX.csv",
    "r10_template": "R2FR_1735_R10_SOURCE_PACK_TEMPLATE.csv",
    "local_template": "R2FR_1735_PPN_WEP_CLOCK_ORBIT_SOURCE_PACK_TEMPLATE.csv",
    "bound_placeholders": "R2FR_1735_BOUND_COMPARISON_PLACEHOLDERS.csv",
    "decision": "R2FR_1735_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1735_CLAIM_GATE.csv",
    "next_target": "R2FR_1735_NEXT_TARGET.csv",
}


LEAK_COMPONENTS = [
    {
        "source_row_id": "TLR1734_0_Dq_tau_commutator",
        "component_id": "E_Dq_tau_commutator_norm",
        "symbol": "||Dq([L_tau,v])-[L_tau_red,Dq(v)]||",
        "channel": "tau flow fails to preserve quotient vertical directions",
        "unit_convention": "quotient-norm per observed-time unit, or dimensionless after multiplying by a declared local time scale",
        "required_source_inputs": "q_map;Dq;tangent_norm;vertical_basis;L_tau_on_parent;L_tau_red;local_time_scale;source_path",
        "first_theorem_zero_route": "prove q and tau are projectable and tau preserves ker(Dq)",
        "first_bound_route": "derive finite commutator norm and project it into PPN/tau/R10 current rows",
    },
    {
        "source_row_id": "TLR1734_1_Dq_source_readout",
        "component_id": "Dsource_readout_Dq_tau_leak",
        "symbol": "||D_source/readout[Dq(v)]|| + ||Delta_tau_roles||",
        "channel": "source, clock, orbit, and boundary readout leakage caused by Dq or tau mismatch",
        "unit_convention": "dimensionless source/readout norm after each arena declares its readout functional",
        "required_source_inputs": "source_map;clock_map;orbit_map;boundary_tau;Dq;vertical_basis;arena_readout_norm;source_path",
        "first_theorem_zero_route": "prove source/clock/orbit/boundary functors all descend through q with one tau",
        "first_bound_route": "derive finite arena-specific readout leak rows for WEP, clocks, orbit, and boundary",
    },
    {
        "source_row_id": "TLR1734_2_tau_nonstationary",
        "component_id": "epsilon_nonstationary_tau",
        "symbol": "epsilon_tau",
        "channel": "nonstationary observed-time generator obstruction",
        "unit_convention": "dimensionless after normalizing stress-contracted symgrad(tau) by M_H_ref, or time-gradient units before normalization",
        "required_source_inputs": "trace;shear;lapse_acceleration;shift_extrinsic;boundary_motion;tau_mismatch;stress_envelope;M_H_ref;source_path",
        "first_theorem_zero_route": "prove local observed tau is Killing/stationary with one clock/source/boundary normalization",
        "first_bound_route": "fill SGT688 components with no-cancellation absolute sum",
    },
    {
        "source_row_id": "TLR1734_3_coupling_marker",
        "component_id": "qbar_XT_or_marker_tau_leak",
        "symbol": "qbar_XT_marker_tau",
        "channel": "constants, material labels, hidden frames, projector/boundary source charge",
        "unit_convention": "dimensionless coupling/source coefficient, or force-normalized after arena response map",
        "required_source_inputs": "constant_owner;material_marker_owner;hidden_frame_coefficients;projector_boundary_charge;arena_response_map;source_path",
        "first_theorem_zero_route": "prove constants/material markers and hidden frame data are quotient/topological and tau-silent",
        "first_bound_route": "derive finite qbar/source-weight coefficients for WEP/R10/clock comparison",
    },
    {
        "source_row_id": "TLR1734_4_total_theta_qtau_leak",
        "component_id": "epsilon_theta_Qtau_projectability_abs",
        "symbol": "epsilon_theta_Qtau_projectability_abs",
        "channel": "absolute no-cancellation projectable-current leak envelope",
        "unit_convention": "dimensionless after all subcomponents share M_H_ref or declared local norm; otherwise not scoreable",
        "required_source_inputs": "E_Dq_tau;Dsource_readout_Dq_tau;epsilon_tau;qbar_XT_marker_tau;common_units;normalization_denominator;source_path",
        "first_theorem_zero_route": "prove all four positive subcomponents theorem-zero in the same parent branch",
        "first_bound_route": "sum absolute source-backed subcomponents with no cancellation credit",
    },
]


ARENA_MAP = {
    "R0_identity_coframe_direct": {
        "arena_family": "WEP",
        "leak_components": "Dsource_readout_Dq_tau_leak;E_Dq_tau_commutator_norm;epsilon_theta_Qtau_projectability_abs",
        "projection_needs": "observed coframe/readout derivative plus tau-source lock for differential acceleration",
        "arena_conversion": "eta_geom_AB from same-frame acceleration response with tau/readout mismatch retained",
        "projection_status": "MISSING_COFRAME_TAU_READOUT_PROJECTION",
    },
    "R1_WEP_source_charge": {
        "arena_family": "WEP",
        "leak_components": "qbar_XT_or_marker_tau_leak;Dsource_readout_Dq_tau_leak;epsilon_theta_Qtau_projectability_abs",
        "projection_needs": "material/source tensor, qbar/source-weight map, and tau_WEP normalization",
        "arena_conversion": "eta_source_AB from composition-dependent source charge and tau_WEP response",
        "projection_status": "MISSING_WEP_SOURCE_TAU_PROJECTION",
    },
    "R2_clock_redshift": {
        "arena_family": "clock",
        "leak_components": "epsilon_nonstationary_tau;Dsource_readout_Dq_tau_leak;qbar_XT_or_marker_tau_leak",
        "projection_needs": "clock functor, tau_clock map, marker derivative, and redshift normalization",
        "arena_conversion": "Delta nu/nu = (1 + alpha_clock) Delta U/c^2 plus tau/marker leak",
        "projection_status": "MISSING_CLOCK_TAU_MARKER_MAP",
    },
    "R3_gamma": {
        "arena_family": "PPN_light",
        "leak_components": "E_Dq_tau_commutator_norm;epsilon_nonstationary_tau;Dsource_readout_Dq_tau_leak",
        "projection_needs": "weak-field spatial metric response to projectability/current leak",
        "arena_conversion": "gamma_minus_1 from g_ij response at O(c^-2)",
        "projection_status": "MISSING_GAMMA_PROJECTABLE_CURRENT_RESPONSE",
    },
    "R4_beta": {
        "arena_family": "PPN_orbital",
        "leak_components": "epsilon_nonstationary_tau;epsilon_theta_Qtau_projectability_abs;Dsource_readout_Dq_tau_leak",
        "projection_needs": "second-order temporal metric response, source normalization, and orbital tau map",
        "arena_conversion": "beta_minus_1 from g_00 O(c^-4) after GM/H_tau calibration",
        "projection_status": "MISSING_BETA_ORBITAL_TAU_RESPONSE",
    },
    "R5_alpha1": {
        "arena_family": "PPN_preferred_frame",
        "leak_components": "epsilon_nonstationary_tau;E_Dq_tau_commutator_norm;qbar_XT_or_marker_tau_leak",
        "projection_needs": "vector/preferred-frame response from nonprojectable tau and hidden frame source",
        "arena_conversion": "alpha1 from g_0i/vector weak-field terms",
        "projection_status": "MISSING_ALPHA1_TAU_FRAME_PROJECTION",
    },
    "R6_alpha2": {
        "arena_family": "PPN_preferred_frame",
        "leak_components": "epsilon_nonstationary_tau;E_Dq_tau_commutator_norm;qbar_XT_or_marker_tau_leak",
        "projection_needs": "anisotropic preferred-frame response and spin/tau alignment",
        "arena_conversion": "alpha2 preferred-frame coefficient",
        "projection_status": "MISSING_ALPHA2_TAU_ANISOTROPY_MAP",
    },
    "R7_alpha3": {
        "arena_family": "PPN_momentum",
        "leak_components": "Dsource_readout_Dq_tau_leak;epsilon_nonstationary_tau;qbar_XT_or_marker_tau_leak",
        "projection_needs": "momentum exchange, boundary motion, source readout and marker-current leakage",
        "arena_conversion": "alpha3-equivalent self-acceleration/momentum residual",
        "projection_status": "MISSING_ALPHA3_SOURCE_EXCHANGE_MAP",
    },
    "R8_xi": {
        "arena_family": "PPN_preferred_location",
        "leak_components": "epsilon_nonstationary_tau;qbar_XT_or_marker_tau_leak;epsilon_theta_Qtau_projectability_abs",
        "projection_needs": "domain/preferred-location anisotropy under tau/projectability leak",
        "arena_conversion": "xi from preferred-location/domain coupling",
        "projection_status": "MISSING_XI_DOMAIN_TAU_PROJECTION",
    },
    "R9_Gdot": {
        "arena_family": "orbital_Gdot",
        "leak_components": "epsilon_nonstationary_tau;qbar_XT_or_marker_tau_leak;Dsource_readout_Dq_tau_leak",
        "projection_needs": "time derivative of measured GM/G_eff from tau, marker, and source-readout leakage",
        "arena_conversion": "d ln G_eff/dt or d ln mu_obs/dt in yr^-1",
        "projection_status": "MISSING_GDOT_TAU_MARKER_DERIVATIVE",
    },
    "R10_fifth_force": {
        "arena_family": "R10_short_range",
        "leak_components": "E_Dq_tau_commutator_norm;Dsource_readout_Dq_tau_leak;epsilon_nonstationary_tau;qbar_XT_or_marker_tau_leak;epsilon_theta_Qtau_projectability_abs",
        "projection_needs": "lambda, tau_R10, beta/source/test legs, kinetic normalization, material geometry, and alpha(lambda) curve",
        "arena_conversion": "|sum_a alpha_a tau_R10_a(lambda_i) delta_w_a| <= alpha_bound(lambda_i)",
        "projection_status": "MISSING_R10_THETA_TAU_FIELD_MAP_AND_BOUND_CURVE",
    },
    "R11_EH_operator_ledger": {
        "arena_family": "operator_closure",
        "leak_components": "E_Dq_tau_commutator_norm;epsilon_theta_Qtau_projectability_abs;qbar_XT_or_marker_tau_leak",
        "projection_needs": "non-EH/current-descent operator coefficient vector and same-frame source normalization",
        "arena_conversion": "retained operator coefficients compared to EH-plus-Lambda target",
        "projection_status": "MISSING_CURRENT_DESCENT_OPERATOR_VECTOR",
    },
}


def source_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": yesno(path.exists()),
                "needles": ";".join(source["needles"]),
                "needles_present": yesno(all(needle in text for needle in source["needles"])),
                "checked_utc": UTC,
            }
        )
    return rows


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def unit_convention_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "source_row_id": component["source_row_id"],
            "component_id": component["component_id"],
            "symbol": component["symbol"],
            "channel": component["channel"],
            "unit_convention": component["unit_convention"],
            "status": "UNIT_CONVENTION_STAGED_INPUTS_MISSING",
            "required_source_inputs": component["required_source_inputs"],
            "first_theorem_zero_route": component["first_theorem_zero_route"],
            "first_bound_route": component["first_bound_route"],
            "prediction_source_backed": no(),
            "accepted_for_scoring": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for component in LEAK_COMPONENTS
    ]


def local_bound_rows() -> list[dict[str, str]]:
    return read_csv(LOCAL_BOUNDS / "local_bound_claims.csv")


def arena_projection_rows(bounds: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for bound in bounds:
        row_id = bound["row_id"]
        spec = ARENA_MAP[row_id]
        symbolic_bound = bound["upper_bound"] in {"alpha(lambda)", "symbolic"} or bound["upper_bound"] == ""
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "arena_row_id": row_id,
                "arena_family": spec["arena_family"],
                "test_arena": bound["test_arena"],
                "observable": bound["observable"],
                "empirical_upper_bound": bound["upper_bound"],
                "empirical_units": bound["units"],
                "bound_reference": bound["reference_path_or_url"],
                "symbolic_bound_or_curve_required": yesno(symbolic_bound),
                "leak_components": spec["leak_components"],
                "projection_needs": spec["projection_needs"],
                "arena_conversion": spec["arena_conversion"],
                "projection_status": spec["projection_status"],
                "predicted_residual": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "comparison_status": "BLOCKED_PENDING_SOURCE_INPUTS",
                "arena_ready": no(),
                "prediction_source_backed": no(),
                "accepted_for_scoring": no(),
                "score_ready": no(),
                "valid_prediction_row": no(),
                "valid_for_claim": no(),
                "claim_allowed": no(),
            }
        )
    return rows


def r10_template_rows() -> list[dict[str, Any]]:
    rows = []
    for component in LEAK_COMPONENTS:
        rows.append(
            {
                "schema_version": "R10_THETA_QTAU_PROJECTABILITY_BOUND_1735",
                "branch_id": BRANCH_ID,
                "component_id": component["component_id"],
                "lambda_value": "MISSING_R10_RANGE",
                "lambda_units": "m",
                "projectability_amplitude": "MISSING_COMPONENT_AMPLITUDE_OR_THEOREM_ZERO",
                "Z_a": "MISSING_KINETIC_NORMALIZATION_OR_THEOREM_ZERO",
                "source_leg_s_a": "MISSING_SOURCE_COUPLING_OR_THEOREM_ZERO",
                "test_leg_beta_a": "MISSING_TEST_READOUT_COEFFICIENT_OR_THEOREM_ZERO",
                "tau_R10_a": "MISSING_FINITE_SOURCE_RESPONSE_OR_THEOREM_ZERO",
                "alpha_predicted": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "alpha_bound": "MISSING_DIGITIZED_ALPHA_LAMBDA_CURVE",
                "source_paths": "MISSING_PARENT_INPUTS_AND_R10_BOUND_CURVE",
                "formula_reference": "R10 comparison inherits 1503 alpha law plus 1735 projectability amplitude",
                "current_failure_mode": "R10 cannot score until lambda, tau_R10, beta/s/Z, projectability amplitude, and alpha(lambda) are sourced or theorem-zero",
                "prediction_source_backed": no(),
                "accepted_for_scoring": no(),
                "score_ready": no(),
                "valid_prediction_row": no(),
                "valid_for_claim": no(),
                "claim_allowed": no(),
            }
        )
    return rows


def local_template_rows(bounds: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for bound in bounds:
        row_id = bound["row_id"]
        if row_id == "R10_fifth_force":
            continue
        spec = ARENA_MAP[row_id]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "arena_row_id": row_id,
                "arena_family": spec["arena_family"],
                "test_arena": bound["test_arena"],
                "observable": bound["observable"],
                "empirical_bound": bound["upper_bound"],
                "units": bound["units"],
                "bound_reference": bound["reference_path_or_url"],
                "required_leak_inputs": spec["leak_components"],
                "required_projection": spec["projection_needs"],
                "predicted_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "prediction_derivation_status": "SOURCE_PACK_TEMPLATE_NONCLAIM",
                "source_file": "MISSING_PARENT_DQ_TAU_THETA_PROJECTION_INPUTS",
                "assumptions": "no-cancellation; same observed frame; compare against GR/null baseline when runnable",
                "comparison_status": "BLOCKED_PENDING_SOURCE_INPUTS",
                "prediction_source_backed": no(),
                "accepted_for_scoring": no(),
                "score_ready": no(),
                "valid_prediction_row": no(),
                "valid_for_claim": no(),
                "claim_allowed": no(),
            }
        )
    return rows


def bound_placeholder_rows(bounds: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for bound in bounds:
        row_id = bound["row_id"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "arena_row_id": row_id,
                "observable": bound["observable"],
                "bound_value": bound["upper_bound"],
                "bound_units": bound["units"],
                "bound_status": "CURVE_REQUIRED" if row_id == "R10_fifth_force" else ("OPERATOR_LEDGER_REQUIRED" if row_id == "R11_EH_operator_ledger" else "BOUND_SOURCE_RECORDED"),
                "predicted_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "prediction_units": bound["units"],
                "comparison_rule": "abs(predicted_value) <= bound_value after same-frame arena projection",
                "comparison_ready": no(),
                "failure_mode_if_used_now": "WOULD_BE_PLACEHOLDER_OR_CLOSURE_CLAIM",
                "prediction_source_backed": no(),
                "accepted_for_scoring": no(),
                "score_ready": no(),
                "valid_prediction_row": no(),
                "valid_for_claim": no(),
                "claim_allowed": no(),
            }
        )
    return rows


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1735_0_source_pack_status",
            "decision": "DQ_TAU_THETA_LEAK_SOURCE_PACK_ARENA_READY_NONCLAIM",
            "reason": "1734 leak symbols now have unit conventions, source requirements, and local arena projection placeholders",
            "next_action": "do not score until parent-signed theorem-zero or numeric source rows exist",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1735_1_R10_status",
            "decision": "R10_REMAINS_CURVE_AND_COEFFICIENT_BLOCKED",
            "reason": "alpha(lambda), tau_R10, lambda, beta/source legs, kinetic normalization, and projectability amplitude are all missing or symbolic",
            "next_action": "use R10 template only as a nonclaim acquisition checklist",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1735_2_best_next_domino",
            "decision": "TARGET_EDQTAU_COMMUTATOR_FIRST",
            "reason": "E_Dq_tau is the exact first obstruction to projectable current descent and feeds all later H_tau/M_H_ref gates",
            "next_action": "try to prove the Dq/tau commutator zero; if it fails, emit first finite nonclaim E_Dq_tau source row",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1735_3_safety",
            "decision": "NO_LOCAL_GR_NEWTON_CLAIM",
            "reason": "a source pack is infrastructure, not a derivation of GR/Newton or an empirical pass",
            "next_action": "keep all local claims false until comparison rows become real and pass gates",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1735_0_component_values", "each theta/Qtau projectability component has numeric source row or theorem-zero", "BLOCKED", "all retained leak rows still contain MISSING_* inputs"),
        ("CG1735_1_arena_projection", "each arena has source-backed projection from projectability leak to observable", "BLOCKED", "R0-R11 projection matrix is schema-only"),
        ("CG1735_2_R10", "R10 alpha(lambda) comparison can be scored", "NO_CLAIM", "R10 bound curve and parent coefficients/projectability amplitudes missing"),
        ("CG1735_3_WEP_PPN_clock_orbit", "WEP/PPN/clock/orbital rows pass", "NO_CLAIM", "predicted residuals are placeholders"),
        ("CG1735_4_Htau_MHref", "H_tau/M_H_ref gates can reopen", "NO_CLAIM", "current-descent projectability and H_tau integrability are not signed"),
        ("CG1735_5_local_GR_Newton", "local GR/Newton reduction follows", "NO_CLAIM", "1735 only prepares leak bounds; it does not prove q_loc=0 or GR reduction"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": no(),
            "status": status,
            "blocker": blocker,
            "local_gr_claim_allowed": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for gate_id, claim, status, blocker in gates
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1735_0_primary",
            "next_target": "1736-Y5-R2FR-Dq-tau-commutator-zero-or-first-finite-bound-row.md",
            "script": "scripts/Y5_R2FR_Dq_tau_commutator_zero_or_first_finite_bound_row.py",
            "objective": "prove E_Dq_tau_commutator_norm=0 from q/tau projectability, or emit first finite nonclaim commutator source row with arena projections",
            "success_condition": "either a parent-signed theorem-zero for E_Dq_tau or a finite source-backed nonclaim row ready for WEP/PPN/R10/orbital smoke comparison",
            "selection_status": "selected",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1735_1_parallel_source_readout",
            "next_target": "1736b-Y5-R2FR-source-readout-Dq-tau-leak-first-bound-row.md",
            "script": "scripts/Y5_R2FR_source_readout_Dq_tau_leak_first_bound_row.py",
            "objective": "fill Dsource_readout_Dq_tau_leak as an arena-specific nonclaim row if the commutator theorem fails",
            "success_condition": "source/clock/orbit/boundary readout maps declared with units and source paths",
            "selection_status": "held_parallel",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1735_2_later_LX",
            "next_target": "1737-Y5-R2FR-vertical-symplectic-silence-LX-QX-proof-attempt.md",
            "script": "scripts/Y5_R2FR_vertical_symplectic_silence_LX_QX_proof_attempt.py",
            "objective": "try deriving Theta_X/Q_X silence from sector L_X after commutator/source readout rows are staged",
            "success_condition": "Theta_X/Q_X theorem-zero or explicit finite boundary/source residual rows",
            "selection_status": "later",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    bounds = local_bound_rows()
    return {
        "source_register": source_rows(),
        "unit_conventions": unit_convention_rows(),
        "arena_matrix": arena_projection_rows(bounds),
        "r10_template": r10_template_rows(),
        "local_template": local_template_rows(bounds),
        "bound_placeholders": bound_placeholder_rows(bounds),
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
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1735_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1735_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {
        "accepted_for_scoring",
        "arena_ready",
        "claim_allowed",
        "comparison_ready",
        "local_gr_claim_allowed",
        "prediction_source_backed",
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
    readiness = {"accepted_for_scoring", "arena_ready", "claim_allowed", "comparison_ready", "prediction_source_backed", "score_ready", "valid_for_claim", "valid_prediction_row"}
    for rows in rows_map.values():
        for row in rows:
            contains_missing = any("MISSING_" in str(value) for value in row.values())
            if contains_missing and any(str(row.get(flag, "")).lower() == "true" for flag in readiness):
                return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1735_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1735_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1735*"):
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
    unit_rows = rows_map["unit_conventions"]
    arena_rows = rows_map["arena_matrix"]
    r10_rows = rows_map["r10_template"]
    local_rows = rows_map["local_template"]
    placeholders = rows_map["bound_placeholders"]
    claim_rows = rows_map["claim_gate"]
    next_rows = rows_map["next_target"]

    validation = [
        check("VAL1735_0_sources_exist", all(row["exists"] == "True" for row in source_register), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1735_1_needles_present", all(row["needles_present"] == "True" for row in source_register), "required source needles are present", "one or more required source needles missing"),
        check("VAL1735_2_unit_conventions_complete", {row["component_id"] for row in unit_rows} == {component["component_id"] for component in LEAK_COMPONENTS}, "all 1734 leak components have unit/source conventions", "unit conventions missing leak component"),
        check("VAL1735_3_all_arenas_mapped", {row["arena_row_id"] for row in arena_rows} == set(ARENA_MAP), "R0-R11 local arenas are mapped to theta/tau leak projection needs", "arena projection matrix missing row"),
        check("VAL1735_4_R10_contract_fields", {"lambda_value", "projectability_amplitude", "Z_a", "source_leg_s_a", "test_leg_beta_a", "tau_R10_a", "alpha_predicted", "alpha_bound"}.issubset(r10_rows[0]), "R10 source-pack template includes projectability/R10 fields", "R10 source-pack template missing required fields"),
        check("VAL1735_5_R10_remains_blocked", all("MISSING_" in row["alpha_predicted"] and row["valid_for_claim"] == "False" for row in r10_rows), "R10 rows remain blocked until parent coefficients and curve are real", "R10 row became scoreable or nonmissing"),
        check("VAL1735_6_local_templates_nonclaim", all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in local_rows), "PPN/WEP/clock/orbit source templates remain nonclaim", "local template row opened claim flag"),
        check("VAL1735_7_bound_placeholders_nonclaim", all(row["comparison_ready"] == "False" and row["claim_allowed"] == "False" for row in placeholders), "bound comparison placeholders are not score-ready", "bound placeholder became comparison-ready"),
        check("VAL1735_8_claim_gates_safe", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claim_rows), "all claim gates keep local claims false", "one or more claim gates opened"),
        check("VAL1735_9_no_claim_flags", no_claim_flags(rows_map), "all generated rows keep claim/no-score flags false", "one or more generated flags enabled a claim"),
        check("VAL1735_10_missing_not_ready", missing_rows_not_ready(rows_map), "no row containing MISSING_* is marked source-backed, claim-ready, or score-ready", "a missing row is marked ready"),
        check("VAL1735_11_next_selected", any(row["route_id"] == "NEXT1735_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selects E_Dq_tau commutator theorem-zero or finite bound row", "next target missing selected primary route"),
        check("VAL1735_12_csv_parse", parsed_ok, "all generated 1735 CSVs parse", "one or more generated 1735 CSVs failed to parse"),
        check("VAL1735_13_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1735_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1735_15_formalization_untouched", formalization_untouched(), "no 1735 outputs found under formalization-workbench", "1735 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1735_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1735 Dq/tau/theta leak source-pack units and arena projections validation" if overall else "one or more 1735 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1735 turns the 1734 `Dq/tau/theta` projectability obstruction into a source-ready, arena-projected nonclaim pack.",
        "- Every leak component now has a unit convention and required source inputs.",
        "- Every local arena row R0-R11 has a projection requirement, but every prediction remains `MISSING_NUMERIC_OR_THEOREM_ZERO`.",
        "- The best next derivation target is the first obstruction: `E_Dq_tau_commutator_norm`.",
        "- No `Theta_total/Q_tau`, `H_tau`, `M_H_ref`, R10, WEP, PPN, clock, orbital, Newton, local-GR, or `q_loc=0` claim is made.",
        "",
        "## Why This Helps",
        "This is the bridge from derivation to testing. If the commutator dies, the current-descent route gets much cleaner. If it does not, the leak now has a declared path into WEP, PPN, clock, orbital, and R10 rows.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Unit Conventions",
        markdown_table(rows_map["unit_conventions"], ["component_id", "symbol", "channel", "unit_convention", "status", "required_source_inputs"]),
        "",
        "## Arena Projection Matrix",
        markdown_table(rows_map["arena_matrix"], ["arena_row_id", "arena_family", "observable", "empirical_upper_bound", "empirical_units", "leak_components", "projection_status", "predicted_residual"]),
        "",
        "## R10 Source Pack Template",
        markdown_table(rows_map["r10_template"], ["component_id", "lambda_value", "projectability_amplitude", "Z_a", "source_leg_s_a", "test_leg_beta_a", "tau_R10_a", "alpha_predicted", "alpha_bound"]),
        "",
        "## PPN WEP Clock Orbit Template",
        markdown_table(rows_map["local_template"], ["arena_row_id", "arena_family", "observable", "empirical_bound", "required_leak_inputs", "predicted_value", "comparison_status"]),
        "",
        "## Bound Placeholders",
        markdown_table(rows_map["bound_placeholders"], ["arena_row_id", "observable", "bound_value", "bound_status", "predicted_value", "comparison_ready", "claim_allowed"]),
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
        "1735 is not a win condition; it is the scorecard before the fight. The first punch should be the commutator theorem: prove `Dq([L_tau,v])-[L_tau_red,Dq(v)]=0`, or write the first finite nonclaim commutator row. That is the cleanest next step toward a derivable GR/Newton limit.",
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
    doc_path = ROOT / "1735-Y5-R2FR-Dq-tau-theta-leak-source-pack-units-and-arena-projections.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1735_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1735 validation FAIL")
    print("1735 validation PASS")


if __name__ == "__main__":
    main()
