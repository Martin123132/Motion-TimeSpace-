from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_second_order_PPN_source_stability_contract_written_inputs_unfilled_no_PPN_or_local_GR_promotion"
CLAIM_CEILING = "second_order_PPN_source_stability_or_residual_evaluator_only_no_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "525-Y5-delta-beta-source-expansion-or-R11-input-fill.md"

DOC_PATH = Path("524-Y5-second-order-PPN-source-stability-or-residual-evaluator.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_PPN_SOURCE_STABILITY_SOURCE_REGISTER.csv")
METRIC_EXPANSION_PATH = Path("source-intake/mts_residuals/P8_Y5_PPN_METRIC_EXPANSION_CONTRACT.csv")
STABILITY_GATE_PATH = Path("source-intake/mts_residuals/P8_Y5_PPN_SOURCE_STABILITY_GATES.csv")
RESIDUAL_VECTOR_PATH = Path("source-intake/mts_residuals/P8_Y5_PPN_RESIDUAL_VECTOR.csv")
INPUT_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_Y5_PPN_EVALUATOR_INPUT_TEMPLATE.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_PPN_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_PPN_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_PPN_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
        "role": "declares PPN source stability as the next hard local-GR gate",
    },
    {
        "source_file": "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
        "role": "minimal local-GR fixed-point action contract including metric PPN readout",
    },
    {
        "source_file": "512-match-MTS-symbols-to-local-GR-action-blocks.md",
        "role": "MTS symbol-to-action map and q_loc demotion rule",
    },
    {
        "source_file": "440-metric-only-second-order-sector-reduction-attempt.md",
        "role": "second-order metric-only/R11 sector filter",
    },
    {
        "source_file": "438-R11-nonEH-coefficient-vector-contract.md",
        "role": "R11 operator-vector contract that blocks symbolic EH/local-GR claims",
    },
    {
        "source_file": "439-EH-only-exterior-parent-premise-ladder.md",
        "role": "EH-only parent premise ladder with second-order operator debt",
    },
    {
        "source_file": "179-local-GR-PPN-silence-contract.md",
        "role": "earlier local-GR PPN silence contract and residual vector",
    },
    {
        "source_file": "221-Noether-source-identity-or-compact-PPN-closure-map.md",
        "role": "compact PPN closure map and source identity obstruction",
    },
    {
        "source_file": "227-local-PPN-coefficient-map-or-official-bound-manifest.md",
        "role": "official bound manifest and local PPN coefficient map",
    },
    {
        "source_file": "229-second-order-beta-or-boundary-scalar-owner.md",
        "role": "second-order beta and boundary/scalar owner route",
    },
    {
        "source_file": "303-second-order-beta-response-attempt.md",
        "role": "prior beta-response attempt and guardrails",
    },
    {
        "source_file": "304-epsilon-loc-beta-guard-update.md",
        "role": "epsilon-local beta guard update",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv",
        "role": "523 residual scorecard feeding second-order source stability",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
        "role": "511 fixed-point conditions including metric PPN readout",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_RESIDUAL_VECTOR.csv",
        "role": "511 local-GR residual vector including metric PPN tail",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
        "role": "512 symbol action-placement map",
    },
    {
        "source_file": "source-intake/mts_residuals/R11_EXECUTABLE_VECTOR_STATUS.csv",
        "role": "R11 status showing operator vector rows are template-only/no-claim",
    },
    {
        "source_file": "source-intake/mts_residuals/R11_MTS_MINIMUM_EXECUTABLE_VECTOR_SKELETON.csv",
        "role": "minimum executable R11 vector skeleton with missing coefficients",
    },
    {
        "source_file": "source-intake/mts_residuals/MTS_local_residual_predictions_TEMPLATE.csv",
        "role": "canonical local residual prediction template",
    },
    {
        "source_file": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "local PPN and source-normalization empirical locks",
    },
    {
        "source_file": "scripts/Y5_second_order_PPN_source_stability_or_residual_evaluator.py",
        "role": "this checkpoint generator",
    },
]


METRIC_EXPANSION_ROWS = [
    {
        "term_id": "MEX524_0_first_order_potential_locked",
        "metric_piece": "U",
        "required_form": "U(x)=G_0 int rho_H(x')/|x-x'| d^3x' with the same measured-GM normalization as the first-order Gauss/orbital branch",
        "residual_if_failed": "epsilon_SN;epsilon_charge;epsilon_Gauss;epsilon_mu_extra_total",
        "current_status": "blocked_by_523_scorecard_unfilled",
        "valid_for_claim": "false",
    },
    {
        "term_id": "MEX524_1_g00_quadratic_beta",
        "metric_piece": "g_00",
        "required_form": "g_00=-1+2U/c^2-2(1+delta_beta_total)U^2/c^4+O(c^-6), require delta_beta_total=0",
        "residual_if_failed": "delta_beta_source;delta_beta_operator;delta_beta_readout",
        "current_status": "not_derived",
        "valid_for_claim": "false",
    },
    {
        "term_id": "MEX524_2_spatial_curvature_gamma",
        "metric_piece": "g_ij",
        "required_form": "g_ij=(1+2(1+delta_gamma)U/c^2)delta_ij+O(c^-4), require delta_gamma=0",
        "residual_if_failed": "gamma_minus_1;c_nonEH_operator_vector;scalar_or_tensor_slip",
        "current_status": "not_derived",
        "valid_for_claim": "false",
    },
    {
        "term_id": "MEX524_3_gravitomagnetic_preferred_frame",
        "metric_piece": "g_0i",
        "required_form": "g_0i equals the GR vector-potential structure in the observed frame, with alpha1=alpha2=alpha3=0",
        "residual_if_failed": "alpha1;alpha2;alpha3;frame_or_domain_vector",
        "current_status": "not_derived",
        "valid_for_claim": "false",
    },
    {
        "term_id": "MEX524_4_preferred_location_boundary",
        "metric_piece": "location/domain/boundary terms",
        "required_form": "boundary, domain, projector, and memory terms do not create xi or preferred-location potentials",
        "residual_if_failed": "xi;boundary_domain_projector_stress;nonlocal_memory_kernel",
        "current_status": "not_derived",
        "valid_for_claim": "false",
    },
    {
        "term_id": "MEX524_5_q_loc_second_order_silence",
        "metric_piece": "q_loc residual forcing",
        "required_form": "q_loc^nu=P_loc(nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}) is an on-shell Ward residual with no O(U^2) local force/source contribution",
        "residual_if_failed": "delta_q_loc_PPN;epsilon_loc_beta;source_force_residual",
        "current_status": "not_derived_zero",
        "valid_for_claim": "false",
    },
    {
        "term_id": "MEX524_6_no_cancellation_PPN_envelope",
        "metric_piece": "total PPN residual vector",
        "required_form": "|Delta_PPN| is bounded componentwise; beta/gamma/alpha_i/xi rows cannot cancel by sign tuning",
        "residual_if_failed": "Delta_PPN_envelope",
        "current_status": "policy_written_unscored",
        "valid_for_claim": "false",
    },
]


STABILITY_GATE_ROWS = [
    {
        "gate_id": "PSG524_0_first_order_GM_chain",
        "pass_condition": "523 first-order measured-GM/Gauss/orbital chain is derived or scored below locks",
        "current_result": "fail_precondition_523_scorecard_unfilled",
        "blocks": "PPN_source_stability;local_GR",
    },
    {
        "gate_id": "PSG524_1_metric_expansion_to_second_order",
        "pass_condition": "parent action is expanded to O(U^2) in the observed metric/readout frame",
        "current_result": "contract_written_not_computed",
        "blocks": "beta;gamma;local_GR",
    },
    {
        "gate_id": "PSG524_2_source_normalization_frozen_at_second_order",
        "pass_condition": "the same G0*M_H used at first order remains fixed inside beta/gamma terms",
        "current_result": "fail_not_derived",
        "blocks": "delta_beta_source;source_normalized_Newton_to_GR_bridge",
    },
    {
        "gate_id": "PSG524_3_EH_only_or_R11_vector",
        "pass_condition": "EH-only theorem lands or every non-EH operator family has executable coefficient/vector data",
        "current_result": "fail_R11_template_only",
        "blocks": "gamma;beta;R11;local_GR",
    },
    {
        "gate_id": "PSG524_4_gamma_slip_zero",
        "pass_condition": "spatial curvature coefficient satisfies gamma-1=0 or is scored below the Cassini lock",
        "current_result": "not_derived_not_scored",
        "blocks": "local_GR",
    },
    {
        "gate_id": "PSG524_5_beta_source_zero",
        "pass_condition": "quadratic g00 source coefficient satisfies beta-1=0 after measured-GM normalization",
        "current_result": "not_derived_not_scored",
        "blocks": "local_GR",
    },
    {
        "gate_id": "PSG524_6_preferred_frame_location_zero",
        "pass_condition": "alpha1, alpha2, alpha3, and xi vanish or are scored below official locks",
        "current_result": "not_derived_not_scored",
        "blocks": "local_GR;domain_projector;boundary_flux",
    },
    {
        "gate_id": "PSG524_7_q_loc_second_order_silent",
        "pass_condition": "q_loc is generated by parent variation and has no O(U^2) source-force residual",
        "current_result": "not_derived_zero",
        "blocks": "local_GR;plateau_axiom_forbidden",
    },
    {
        "gate_id": "PSG524_8_boundary_domain_projector_stress_zero",
        "pass_condition": "boundary, domain, projector, memory, and Pi_M variations produce no second-order stress/source leak",
        "current_result": "not_derived_not_scored",
        "blocks": "alpha_i;xi;beta;R11",
    },
    {
        "gate_id": "PSG524_9_no_overclaim",
        "pass_condition": "no PPN/local-GR promotion occurs until every gate is derived-zero or scored",
        "current_result": "pass_policy_enforced",
        "blocks": "false_claims",
    },
]


RESIDUAL_VECTOR_ROWS = [
    {
        "residual_id": "PPN524_0_gamma_operator_slip",
        "symbol": "delta_gamma_operator",
        "definition": "spatial-curvature slip induced by non-EH operator or source-normalization leakage",
        "maps_to": "R3_gamma;R11_EH_operator_ledger",
        "bound_or_target": "gamma_minus_1<=2.3e-5 or derived zero",
        "current_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "PPN524_1_beta_source_quadratic",
        "symbol": "delta_beta_source",
        "definition": "quadratic g00 source-normalization residue after first-order measured-GM calibration",
        "maps_to": "R4_beta;P8_nonlinear_beta_source_residue;SRC523_10",
        "bound_or_target": "beta_minus_1<=7.8e-5 or derived zero",
        "current_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "PPN524_2_beta_operator_quadratic",
        "symbol": "delta_beta_operator",
        "definition": "quadratic g00 residue from higher-curvature/scalar/vector/nonlocal operator families",
        "maps_to": "R4_beta;R11_EH_operator_ledger",
        "bound_or_target": "operator vector scored below beta lock or EH-only theorem",
        "current_status": "unfilled_R11_template_only",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "PPN524_3_alpha1_frame",
        "symbol": "alpha1",
        "definition": "preferred-frame residual from vector/domain/frame split in g0i or matter readout",
        "maps_to": "R5_alpha1;P8_frame_calibration_split",
        "bound_or_target": "alpha1<=1e-4 or derived zero",
        "current_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "PPN524_4_alpha2_domain_vector",
        "symbol": "alpha2",
        "definition": "domain/vector anisotropy residual in second-order local metric",
        "maps_to": "R6_alpha2;domain_projector_stress;R11",
        "bound_or_target": "alpha2<=2e-9 or derived zero",
        "current_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "PPN524_5_alpha3_flux",
        "symbol": "alpha3",
        "definition": "momentum-flux/nonconservation residual from boundary, projector, memory, or source exchange",
        "maps_to": "R7_alpha3;boundary_flux;mu_extra",
        "bound_or_target": "alpha3<=4e-20 or derived zero",
        "current_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "PPN524_6_xi_preferred_location",
        "symbol": "xi",
        "definition": "preferred-location/local anisotropy residual from boundary/domain/nonlocal memory or projector terms",
        "maps_to": "R8_xi;R11;boundary_domain_projector_stress",
        "bound_or_target": "xi<=4e-9 or derived zero",
        "current_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "PPN524_7_q_loc_second_order_force",
        "symbol": "delta_q_loc_PPN",
        "definition": "O(U^2) force/source residual from P_loc(nabla Gamma_eff - div K_hat)",
        "maps_to": "q_loc;Gamma_eff;K_hat;epsilon_loc_beta;R11",
        "bound_or_target": "derived Ward-zero or mapped into beta/gamma/alpha_i/xi bounds",
        "current_status": "not_derived_zero",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "PPN524_8_readout_metric_mismatch",
        "symbol": "delta_metric_readout_2PN",
        "definition": "second-order mismatch between g_obs, g_readout, clock metric, and orbital metric",
        "maps_to": "R0;R2;R3;R4;P8_frame_calibration_split",
        "bound_or_target": "same metric/coframe theorem or clock/WEP/PPN residuals below locks",
        "current_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "PPN524_9_source_normalization_cross_terms",
        "symbol": "epsilon_SN_U2_cross",
        "definition": "cross-terms where first-order source-normalization residuals re-enter O(U^2) metric coefficients",
        "maps_to": "SRC523_0..SRC523_11;R4;R9;R10;R11",
        "bound_or_target": "523 scorecard zero/below-bound before PPN promotion",
        "current_status": "blocked_by_523_unfilled",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "PPN524_10_R11_total_operator_vector",
        "symbol": "c_nonEH_operator_vector",
        "definition": "full non-EH operator-family vector contributing to second-order weak-field coefficients",
        "maps_to": "R11;R3;R4;R5;R6;R7;R8;R10",
        "bound_or_target": "actual coefficient vector or EH-only theorem",
        "current_status": "template_only_no_claim",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "PPN524_11_total_PPN_envelope",
        "symbol": "Delta_PPN_envelope",
        "definition": "componentwise no-cancellation envelope over gamma, beta, alpha_i, xi, q_loc, readout, and R11 rows",
        "maps_to": "all_PPN524_rows",
        "bound_or_target": "all components theorem-zero or below their local locks",
        "current_status": "not_run_inputs_unfilled",
        "valid_for_claim": "false",
    },
]


INPUT_TEMPLATE_ROWS = [
    {
        "model_id": "MTS_local_GR_branch",
        "branch_id": "Y5_second_order_PPN_source_stability",
        "residual_id": row["residual_id"],
        "symbol": row["symbol"],
        "units": "dimensionless_or_operator_units_declared",
        "normalization": row["definition"],
        "required_input": row["bound_or_target"],
        "source_file": "fill_derivation_or_vector_path",
        "derivation_status": "fill: derived_zero/derived_bound/numeric_vector/closure_assumed/speculative",
        "numeric_input_status": "not_loaded",
        "valid_for_claim": "false",
    }
    for row in RESIDUAL_VECTOR_ROWS
]


DECISION_ROWS = [
    {
        "decision_id": "D524_0_PPN_contract_written",
        "status": "second_order_contract_written",
        "meaning": "local GR requires a second-order weak-field expansion after measured-GM normalization, not just a Newton/Poisson pass",
        "claim_status": "conditional_not_satisfied",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D524_1_first_order_precondition_unmet",
        "status": "523_scorecard_unfilled",
        "meaning": "the PPN evaluator cannot promote anything while the first-order measured-GM/source-normalization scorecard is unfilled",
        "claim_status": "blocks_PPN_and_local_GR",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D524_2_R11_still_template_only",
        "status": "operator_vector_missing",
        "meaning": "non-EH operator families remain symbolic/template-only, so gamma/beta/alpha_i/xi cannot be claimed safe",
        "claim_status": "R11_blocks_local_GR",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D524_3_q_loc_not_zero_at_PPN_order",
        "status": "q_loc_second_order_zero_not_derived",
        "meaning": "Gamma_eff/K_hat/q_loc must be a parent-action Ward residual with no O(U^2) local force, or it stays a bounded residual",
        "claim_status": "closure_axiom_forbidden",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D524_4_no_overclaim_private",
        "status": "private_no_push_no_promotion",
        "meaning": "this checkpoint is internal derivation discipline and does not push or publish anything",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "SECOND_ORDER_PPN_SOURCE_STABILITY",
        "previous_status": "hard_next_gate_after_523",
        "new_status": "metric_expansion_contract_and_residual_evaluator_inputs_written_unfilled_no_claim",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "first_order_scorecard_unfilled",
        "new_status": "still_required_before_any_PPN_evaluation_can_promote_local_GR",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "R11_EH_OPERATOR",
        "previous_status": "operator_vector_template_only_or_EH_only_not_derived",
        "new_status": "direct_PPN_blocker_gamma_beta_alpha_xi_vector_missing",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "Q_LOC_GAMMA_KHAT",
        "previous_status": "must_be_derived_or_demoted",
        "new_status": "now_required_to_be_silent_at_O_U2_or_mapped_to_PPN_bounds",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "blocked_by_unfilled_source_normalization_scorecard_and_second_order_PPN_source_vector",
        "new_status": "still_blocked_PPN_vector_inputs_unfilled_and_R11_template_only",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    full_path = ROOT / path
    if not full_path.exists():
        return []
    with full_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in SOURCE_REGISTER:
        full_path = ROOT / item["source_file"]
        rows.append({**item, "exists": full_path.exists()})
    return rows


def validation_rows(sources: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    source_score_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv"))
    fixed_point_rows = read_csv(Path("source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv"))
    local_gr_residual_rows = read_csv(Path("source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_RESIDUAL_VECTOR.csv"))
    r11_status_rows = read_csv(Path("source-intake/mts_residuals/R11_EXECUTABLE_VECTOR_STATUS.csv"))
    r11_claim_rows = [row for row in r11_status_rows if row.get("valid_for_claim", "").lower() == "true"]
    local_bound_rows = read_csv(Path("source-intake/local_bounds/local_bound_claims.csv"))
    local_row_ids = {row.get("row_id", "") for row in local_bound_rows}
    required_local_rows = {
        "R3_gamma",
        "R4_beta",
        "R5_alpha1",
        "R6_alpha2",
        "R7_alpha3",
        "R8_xi",
        "R11_EH_operator_ledger",
    }
    metric_claim_rows = [row for row in METRIC_EXPANSION_ROWS if row["valid_for_claim"] == "true"]
    residual_claim_rows = [row for row in RESIDUAL_VECTOR_ROWS if row["valid_for_claim"] == "true"]
    input_claim_rows = [row for row in INPUT_TEMPLATE_ROWS if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V524_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V524_1_523_scorecard_loaded",
            "result": "pass" if len(source_score_rows) == 12 else "fail",
            "detail": f"source_score_rows={len(source_score_rows)}",
        },
        {
            "check_id": "V524_2_fixed_point_and_local_GR_residuals_loaded",
            "result": "pass" if len(fixed_point_rows) >= 9 and len(local_gr_residual_rows) >= 9 else "fail",
            "detail": f"fixed_point_rows={len(fixed_point_rows)};local_gr_residual_rows={len(local_gr_residual_rows)}",
        },
        {
            "check_id": "V524_3_R11_status_loaded_no_claim",
            "result": "pass" if len(r11_status_rows) >= 10 and not r11_claim_rows else "fail",
            "detail": f"r11_status_rows={len(r11_status_rows)};r11_claim_rows={len(r11_claim_rows)}",
        },
        {
            "check_id": "V524_4_local_PPN_locks_available",
            "result": "pass" if required_local_rows.issubset(local_row_ids) else "fail",
            "detail": f"required_local_rows_present={required_local_rows.issubset(local_row_ids)};local_rows={len(local_bound_rows)}",
        },
        {
            "check_id": "V524_5_metric_expansion_contract_written",
            "result": "pass" if len(METRIC_EXPANSION_ROWS) == 7 and not metric_claim_rows else "fail",
            "detail": f"metric_rows={len(METRIC_EXPANSION_ROWS)};metric_claim_rows={len(metric_claim_rows)}",
        },
        {
            "check_id": "V524_6_PPN_residual_vector_written_unclaimed",
            "result": "pass" if len(RESIDUAL_VECTOR_ROWS) == 12 and not residual_claim_rows and len(INPUT_TEMPLATE_ROWS) == 12 else "fail",
            "detail": f"residual_rows={len(RESIDUAL_VECTOR_ROWS)};input_rows={len(INPUT_TEMPLATE_ROWS)};claim_rows={len(residual_claim_rows) + len(input_claim_rows)}",
        },
        {
            "check_id": "V524_7_no_overclaim",
            "result": "pass" if not metric_claim_rows and not residual_claim_rows and not input_claim_rows and not r11_claim_rows else "fail",
            "detail": "PPN_source_stability_derived=false; PPN_promoted=false; local_GR_claim_allowed=false",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_run_csv(results_dir: Path, filename: str, rows: list[dict[str, Any]]) -> None:
    fieldnames = list(rows[0].keys()) if rows else []
    with (results_dir / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, Any]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 524 - Y5 Second-Order PPN Source Stability or Residual Evaluator

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The local-GR branch cannot be won at first order.

Even if a future checkpoint derives the Newton/Gauss measured-GM chain, local GR still requires the same source normalization to survive the second-order PPN expansion:

```text
g_00 = -1 + 2U/c^2 - 2U^2/c^4 + ...
g_ij = (1 + 2U/c^2) delta_ij + ...
alpha_i = xi = 0.
```

Current MTS has not derived that. This checkpoint writes the contract and the residual evaluator inputs. It does not promote PPN or local GR.

## 2. Metric Expansion Contract

{markdown_table(METRIC_EXPANSION_ROWS)}

## 3. Stability Gates

{markdown_table(STABILITY_GATE_ROWS)}

## 4. PPN Residual Vector

{markdown_table(RESIDUAL_VECTOR_ROWS)}

## 5. Evaluator Input Template

{markdown_table(INPUT_TEMPLATE_ROWS)}

## 6. Decision

{markdown_table(DECISION_ROWS)}

## 7. Source Register

{markdown_table(sources)}

## 8. Validation

{markdown_table(validations)}

## 9. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 10. Claim Ceiling

Allowed:

```text
MTS now has an explicit second-order PPN source-stability contract.
The beta/gamma/alpha_i/xi/q_loc/R11 residual vector is row-addressable.
The evaluator input template is ready for future theorem-zero or numeric/vector fills.
```

Forbidden:

```text
MTS has derived gamma=1 or beta=1.
MTS has derived alpha_i=0, xi=0, or q_loc^nu=0 at PPN order.
MTS has derived EH-only local exterior dynamics or supplied an executable R11 vector.
MTS has promoted Newton, PPN, or local GR.
```

## 11. Next Target

`{NEXT_TARGET}`

The highest-leverage next move is to pick one hard residual and try to actually compute or derive it. The cleanest candidate is `delta_beta_source`: expand the source-normalized metric equation to quadratic order and see whether the source-normalization residual is forced to zero, bounded, or retained.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-second-order-PPN-source-stability-or-residual-evaluator"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)
    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (METRIC_EXPANSION_PATH, METRIC_EXPANSION_ROWS),
        (STABILITY_GATE_PATH, STABILITY_GATE_ROWS),
        (RESIDUAL_VECTOR_PATH, RESIDUAL_VECTOR_ROWS),
        (INPUT_TEMPLATE_PATH, INPUT_TEMPLATE_ROWS),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "metric_expansion_contract": str(ROOT / METRIC_EXPANSION_PATH),
        "source_stability_gates": str(ROOT / STABILITY_GATE_PATH),
        "ppn_residual_vector": str(ROOT / RESIDUAL_VECTOR_PATH),
        "evaluator_input_template": str(ROOT / INPUT_TEMPLATE_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "metric_expansion_rows": len(METRIC_EXPANSION_ROWS),
        "stability_gate_rows": len(STABILITY_GATE_ROWS),
        "ppn_residual_rows": len(RESIDUAL_VECTOR_ROWS),
        "evaluator_input_rows": len(INPUT_TEMPLATE_ROWS),
        "failed_validation_rows": len(failed_validations),
        "PPN_source_stability_contract_written": True,
        "PPN_source_stability_derived": False,
        "PPN_residual_vector_written": True,
        "PPN_residual_vector_scored": False,
        "delta_beta_source_derived": False,
        "gamma_equals_one_derived": False,
        "beta_equals_one_derived": False,
        "alpha_i_xi_zero_derived": False,
        "q_loc_second_order_zero_derived": False,
        "R11_executable_vector_supplied": False,
        "source_normalized_Newton_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "github_push_performed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
