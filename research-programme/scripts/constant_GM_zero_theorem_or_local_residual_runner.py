from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "constant_GM_zero_theorem_or_local_residual_runner_written_conditional_zero_theorem_failed_local_residual_runner_inputs_loaded_no_Newton_or_local_GR_pass"
CLAIM_CEILING = "constant_GM_zero_or_residual_runner_only_no_constant_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "467-mu-extra-zero-owner-or-source-normalization-coefficient-vector.md"

DOC_PATH = Path("466-constant-GM-zero-theorem-or-local-residual-runner.md")
ZERO_THEOREM_PATH = Path("source-intake/mts_residuals/P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv")
RESIDUAL_RUNNER_INPUT_PATH = Path("source-intake/mts_residuals/P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv")
BOUND_MATRIX_PATH = Path("source-intake/mts_residuals/P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_CONSTANT_GM_ZERO_OR_RESIDUAL_DECISION.csv")

DERIVATIVE_GATE_PATH = Path("source-intake/mts_residuals/P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv")
FILL_QUEUE_PATH = Path("source-intake/mts_residuals/P8_CONSTANT_GM_DERIVATIVE_HAIR_FILL_QUEUE.csv")
P8_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv")
LOCAL_RESIDUAL_CONTRACT_PATH = Path("runs/20260602-094500-MTS-local-residual-vector-input-contract/results/residual_components.csv")
R11_DERIVATIVE_VECTOR_PATH = Path("source-intake/mts_residuals/R11_SOURCE_NORMALIZATION_DERIVATIVE_HAIR_VECTOR.csv")


SOURCE_REGISTER = [
    {
        "path": "465-constant-GM-derivative-hair-fill-gate.md",
        "role": "exact D_X ln mu_obs derivative-hair law and CGM channel map",
    },
    {
        "path": str(DERIVATIVE_GATE_PATH),
        "role": "machine-readable derivative-hair rows",
    },
    {
        "path": str(FILL_QUEUE_PATH),
        "role": "minimum fill queue from 465",
    },
    {
        "path": str(P8_TEMPLATE_PATH),
        "role": "P8 source-normalization residual template with bound targets",
    },
    {
        "path": str(LOCAL_RESIDUAL_CONTRACT_PATH),
        "role": "local residual vector contract with source locks for eta, Gdot, R10, R11",
    },
    {
        "path": str(R11_DERIVATIVE_VECTOR_PATH),
        "role": "R11 source-normalization derivative vector from 465",
    },
    {
        "path": "461-PG-residual-input-derive-or-fill-gate.md",
        "role": "P8 rows retained/unfilled before this runner",
    },
    {
        "path": "462-charge-current-equality-direct-derivation-attempt.md",
        "role": "charge-current equality residual decomposition",
    },
    {
        "path": "464-R11-executable-vector-minimum-fill-skeleton.md",
        "role": "source_normalization_operator priority and R10 link requirement",
    },
]


ZERO_THEOREM_COLUMNS = [
    "premise_id",
    "premise",
    "mathematical_form",
    "current_status",
    "evidence_now",
    "failure_if_missing",
    "residual_channel_activated",
    "promotion_effect",
    "next_action",
]


ZERO_THEOREM_ROWS = [
    {
        "premise_id": "Z0_decomposition_identity",
        "premise": "measured source decomposition exists",
        "mathematical_form": "mu_obs = G_eff M_eff + mu_extra = G_eff M_eff(1+epsilon_mu)",
        "current_status": "pass_identity",
        "evidence_now": "465 derives epsilon_mu and D_X ln mu_obs law",
        "failure_if_missing": "no source-normalized GM language",
        "residual_channel_activated": "none",
        "promotion_effect": "identity credit only",
        "next_action": "use the identity as the runner backbone",
    },
    {
        "premise_id": "Z1_global_coupling_superselection",
        "premise": "G_eff is parent-fixed and derivative-silent",
        "mathematical_form": "D_X ln G_eff = 0 for X=t,r,A,lambda,frame,domain",
        "current_status": "open_not_parent_derived",
        "evidence_now": "constant-coupling contracts exist but 461 retains dln_Geff_dt",
        "failure_if_missing": "local Gdot or source/range/frame coupling drift",
        "residual_channel_activated": "P8_Geff_time_drift",
        "promotion_effect": "blocks constant GM and local GR",
        "next_action": "derive superselection or fill drift/source/range residual rows",
    },
    {
        "premise_id": "Z2_calibrated_PiM_flux_conservation",
        "premise": "M_eff is a conserved calibrated source charge",
        "mathematical_form": "D_X ln M_eff = 0 and d(Pi_M J_H)=0 in compact exterior",
        "current_status": "open_not_parent_derived",
        "evidence_now": "Pi_M/charge-current route is conditional; 462 leaves Delta_flux and Delta_PiM active",
        "failure_if_missing": "mass flux, memory exchange, or beta/Gdot source drift",
        "residual_channel_activated": "P8_Meff_conservation",
        "promotion_effect": "blocks measured source mass",
        "next_action": "derive calibrated Pi_M Ward flux closure or fill dln_Meff_dt",
    },
    {
        "premise_id": "Z3_mu_extra_zero_or_universal_constant",
        "premise": "epsilon_mu has no active derivative hair",
        "mathematical_form": "epsilon_mu=0, or epsilon_mu=constant universal calibration and D_X epsilon_mu=0",
        "current_status": "failed_missing_coefficient_vector",
        "evidence_now": "465 R11 vector still has MISSING_ markers for epsilon_mu and mu_extra",
        "failure_if_missing": "hidden boundary/bulk/domain/memory/non-EH measured-GM contribution",
        "residual_channel_activated": "P8_boundary_bulk_domain_mu_extra;R11_source_normalization_operator",
        "promotion_effect": "blocks Newton source normalization",
        "next_action": "try mu_extra owner theorem; otherwise fill coefficient vector",
    },
    {
        "premise_id": "Z4_species_blind_source_action",
        "premise": "source charge is species/material blind",
        "mathematical_form": "Delta_AB ln mu_obs = 0 or eta_source_AB = 0",
        "current_status": "open_not_parent_derived",
        "evidence_now": "461 keeps direct WEP separate from source-charge WEP",
        "failure_if_missing": "composition-dependent gravitational source charge",
        "residual_channel_activated": "P8_species_source_charge",
        "promotion_effect": "blocks full WEP/source-normalized Newton",
        "next_action": "derive selector-blind source action or fill eta_source_AB row",
    },
    {
        "premise_id": "Z5_no_radial_or_range_hair",
        "premise": "no radial/range-dependent measured-GM profile",
        "mathematical_form": "partial_r ln mu_obs = 0 and alpha(lambda)=0, or executable curves remain below bounds",
        "current_status": "open_not_parent_derived",
        "evidence_now": "R10 link required but missing; radial profile not loaded",
        "failure_if_missing": "radius/range-dependent Newton constant or fifth force",
        "residual_channel_activated": "P8_radial_source_hair;P8_range_dependence",
        "promotion_effect": "blocks inverse-square Newton claim",
        "next_action": "derive no-range/no-radial theorem or build alpha(lambda)/radial profile inputs",
    },
    {
        "premise_id": "Z6_same_frame_source_pullback",
        "premise": "source variation and matter readout use one parent-selected observed frame",
        "mathematical_form": "Delta_frame ln mu_obs = 0",
        "current_status": "partial_conditional_only",
        "evidence_now": "same-frame matter route exists conditionally, but source variation is not parent-derived",
        "failure_if_missing": "frame/source calibration split",
        "residual_channel_activated": "P8_frame_calibration_split",
        "promotion_effect": "blocks same-frame Newton",
        "next_action": "attach frame theorem to source variation, not only geodesic readout",
    },
    {
        "premise_id": "Z7_parent_identity_cancellation",
        "premise": "any cancellation among derivative terms is a parent identity",
        "mathematical_form": "D_X ln G_eff + D_X ln M_eff + D_X ln(1+epsilon_mu) == 0 as an identity",
        "current_status": "not_supplied",
        "evidence_now": "465 explicitly forbids tuned cancellation",
        "failure_if_missing": "post-hoc cancellation treated as derivation",
        "residual_channel_activated": "all_nonzero_channels",
        "promotion_effect": "no cancellation credit",
        "next_action": "do not allow tuned cancellation in runner scoring",
    },
    {
        "premise_id": "Z8_second_order_source_stability",
        "premise": "first-order source normalization survives PPN second order",
        "mathematical_form": "delta_beta_source=0 and gamma-1=0 after measured-GM normalization",
        "current_status": "deferred_until_first_order_rows_scored",
        "evidence_now": "461 and 465 defer beta/gamma source-normalized vector",
        "failure_if_missing": "Newton-only branch cannot become local GR",
        "residual_channel_activated": "P8_nonlinear_beta_source_residue",
        "promotion_effect": "blocks local GR promotion",
        "next_action": "run second-order PPN source vector after Z1-Z7 are scored",
    },
]


RUNNER_INPUT_COLUMNS = [
    "model_id",
    "branch_id",
    "component_id",
    "symbol",
    "derivative_channel",
    "observable_link",
    "predicted_value",
    "prediction_units",
    "bound_or_target",
    "bound_source",
    "formula_reference",
    "input_source_file",
    "derivation_status",
    "runner_state",
    "valid_for_claim",
    "notes",
]


RUNNER_INPUT_ROWS = [
    {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "constant_GM_zero_or_residual_runner",
        "component_id": "P8_boundary_bulk_domain_mu_extra",
        "symbol": "epsilon_mu = mu_extra/(G_eff M_eff)",
        "derivative_channel": "amplitude;D_t;D_r;D_A;D_lambda;Delta_frame",
        "observable_link": "gamma;beta;alpha3;xi;Gdot;operator_ledger",
        "predicted_value": "MISSING_NUMERIC_OR_DERIVED_ZERO_EPSILON_MU_VECTOR",
        "prediction_units": "dimensionless",
        "bound_or_target": "zero owned exchange or coefficient residuals below row locks",
        "bound_source": str(P8_TEMPLATE_PATH),
        "formula_reference": "epsilon_mu := mu_extra/(G_eff M_eff)",
        "input_source_file": str(R11_DERIVATIVE_VECTOR_PATH),
        "derivation_status": "retained_unfilled",
        "runner_state": "not_scoreable_prediction_missing",
        "valid_for_claim": "false",
        "notes": "highest priority; constant universal calibration may be absorbed, derivative hair may not",
    },
    {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "constant_GM_zero_or_residual_runner",
        "component_id": "P8_Geff_time_drift",
        "symbol": "dln_Geff_dt",
        "derivative_channel": "D_t",
        "observable_link": "Gdot_over_G",
        "predicted_value": "MISSING_NUMERIC_OR_DERIVED_ZERO_DRIFT",
        "prediction_units": "yr^-1",
        "bound_or_target": "9.6e-15 yr^-1 or derived zero",
        "bound_source": str(P8_TEMPLATE_PATH),
        "formula_reference": "d ln mu_obs/dt = d ln G_eff/dt + d ln M_eff/dt + d ln(1+epsilon_mu)/dt",
        "input_source_file": str(DERIVATIVE_GATE_PATH),
        "derivation_status": "retained_unfilled",
        "runner_state": "not_scoreable_prediction_missing",
        "valid_for_claim": "false",
        "notes": "must be separated from dln_Meff_dt and epsilon_mu drift",
    },
    {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "constant_GM_zero_or_residual_runner",
        "component_id": "P8_Meff_conservation",
        "symbol": "dln_Meff_dt",
        "derivative_channel": "D_t;flux",
        "observable_link": "beta_minus_1;Gdot_over_G",
        "predicted_value": "MISSING_NUMERIC_OR_DERIVED_ZERO_MASS_FLUX",
        "prediction_units": "yr^-1",
        "bound_or_target": "beta/Gdot locks or derived conservation",
        "bound_source": str(P8_TEMPLATE_PATH),
        "formula_reference": "D_X ln mu_obs identity plus Pi_M flux closure",
        "input_source_file": str(DERIVATIVE_GATE_PATH),
        "derivation_status": "retained_unfilled",
        "runner_state": "not_scoreable_prediction_missing",
        "valid_for_claim": "false",
        "notes": "mass conservation has to be owned by Pi_M/Ward flux, not assumed",
    },
    {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "constant_GM_zero_or_residual_runner",
        "component_id": "P8_species_source_charge",
        "symbol": "eta_source_AB",
        "derivative_channel": "D_A;Delta_AB",
        "observable_link": "eta_WEP_source_charge",
        "predicted_value": "MISSING_NUMERIC_OR_DERIVED_ZERO_SOURCE_CHARGE",
        "prediction_units": "dimensionless",
        "bound_or_target": "2.8e-15 or derived universal source charge",
        "bound_source": str(P8_TEMPLATE_PATH),
        "formula_reference": "Delta_AB ln mu_obs = 0",
        "input_source_file": str(DERIVATIVE_GATE_PATH),
        "derivation_status": "retained_unfilled",
        "runner_state": "not_scoreable_prediction_missing",
        "valid_for_claim": "false",
        "notes": "direct coframe WEP cannot automatically fill source-charge WEP",
    },
    {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "constant_GM_zero_or_residual_runner",
        "component_id": "P8_radial_source_hair",
        "symbol": "partial_r_ln_mu_obs",
        "derivative_channel": "D_r",
        "observable_link": "gamma_minus_1;beta_minus_1;alpha(lambda)",
        "predicted_value": "MISSING_RADIAL_PROFILE_OR_DERIVED_ZERO",
        "prediction_units": "inverse_length_or_dimensionless_envelope",
        "bound_or_target": "zero radial hair or mapped PPN/fifth-force residuals",
        "bound_source": str(P8_TEMPLATE_PATH),
        "formula_reference": "partial_r ln mu_obs = partial_r ln G_eff + partial_r ln M_eff + partial_r ln(1+epsilon_mu)",
        "input_source_file": str(DERIVATIVE_GATE_PATH),
        "derivation_status": "retained_unfilled",
        "runner_state": "not_scoreable_prediction_missing",
        "valid_for_claim": "false",
        "notes": "single-radius calibration does not clear this row",
    },
    {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "constant_GM_zero_or_residual_runner",
        "component_id": "P8_range_dependence",
        "symbol": "alpha(lambda)",
        "derivative_channel": "D_lambda;finite_range",
        "observable_link": "delta_G_or_fifth_force_yukawa",
        "predicted_value": "MISSING_EXECUTABLE_ALPHA_LAMBDA_CURVE_OR_ZERO_THEOREM",
        "prediction_units": "range-dependent",
        "bound_or_target": "verified alpha(lambda) bound curve or derived zero",
        "bound_source": str(P8_TEMPLATE_PATH),
        "formula_reference": "finite-range source hair maps to alpha(lambda)",
        "input_source_file": str(DERIVATIVE_GATE_PATH),
        "derivation_status": "retained_unfilled",
        "runner_state": "not_scoreable_curve_missing",
        "valid_for_claim": "false",
        "notes": "this remains curve-required; symbolic R10 text cannot score",
    },
    {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "constant_GM_zero_or_residual_runner",
        "component_id": "P8_frame_calibration_split",
        "symbol": "delta_frame_source",
        "derivative_channel": "Delta_frame;D_domain",
        "observable_link": "eta_WEP_direct_geometry;clock_redshift;operator_ledger",
        "predicted_value": "MISSING_NUMERIC_OR_DERIVED_ZERO_FRAME_SPLIT",
        "prediction_units": "dimensionless",
        "bound_or_target": "one observed frame or explicit residual below row locks",
        "bound_source": str(P8_TEMPLATE_PATH),
        "formula_reference": "Delta_frame ln mu_obs = 0",
        "input_source_file": str(DERIVATIVE_GATE_PATH),
        "derivation_status": "retained_unfilled",
        "runner_state": "not_scoreable_prediction_missing",
        "valid_for_claim": "false",
        "notes": "same-frame theorem must apply to source variation and matter readout",
    },
    {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "constant_GM_zero_or_residual_runner",
        "component_id": "P8_nonlinear_beta_source_residue",
        "symbol": "delta_beta_source",
        "derivative_channel": "second_order",
        "observable_link": "beta_minus_1",
        "predicted_value": "MISSING_SECOND_ORDER_PPN_SOURCE_VECTOR",
        "prediction_units": "dimensionless",
        "bound_or_target": "7.8e-05 or derived second-order source closure",
        "bound_source": str(P8_TEMPLATE_PATH),
        "formula_reference": "PPN beta after measured-GM normalization",
        "input_source_file": str(DERIVATIVE_GATE_PATH),
        "derivation_status": "deferred_retained_unfilled",
        "runner_state": "deferred_until_first_order_rows_score",
        "valid_for_claim": "false",
        "notes": "first-order Newton cannot be promoted to local GR without this",
    },
]


BOUND_MATRIX_COLUMNS = [
    "component_id",
    "observable",
    "target_type",
    "target_value",
    "units",
    "source",
    "evaluation_rule",
    "scoreable_now",
    "reason_not_scoreable",
]


BOUND_MATRIX_ROWS = [
    {
        "component_id": "P8_boundary_bulk_domain_mu_extra",
        "observable": "epsilon_mu_vector",
        "target_type": "zero_or_component_locks",
        "target_value": "zero owned exchange or row-by-row coefficient bounds",
        "units": "dimensionless",
        "source": str(P8_TEMPLATE_PATH),
        "evaluation_rule": "score only if epsilon_mu coefficient vector has numeric values or theorem-zero source",
        "scoreable_now": "false",
        "reason_not_scoreable": "epsilon_mu vector missing",
    },
    {
        "component_id": "P8_Geff_time_drift",
        "observable": "Gdot_over_G",
        "target_type": "upper_bound_or_zero",
        "target_value": "9.6e-15",
        "units": "yr^-1",
        "source": str(P8_TEMPLATE_PATH),
        "evaluation_rule": "abs(predicted dln_Geff_dt) <= 9.6e-15 yr^-1 or derived_zero",
        "scoreable_now": "false",
        "reason_not_scoreable": "predicted dln_Geff_dt missing",
    },
    {
        "component_id": "P8_Meff_conservation",
        "observable": "dln_Meff_dt",
        "target_type": "derived_conservation_or_decomposed_bound",
        "target_value": "Gdot/beta locks after decomposition",
        "units": "yr^-1",
        "source": str(P8_TEMPLATE_PATH),
        "evaluation_rule": "score only after separating mass flux from G_eff and epsilon_mu drift",
        "scoreable_now": "false",
        "reason_not_scoreable": "mass flux residual missing",
    },
    {
        "component_id": "P8_species_source_charge",
        "observable": "eta_source_AB",
        "target_type": "upper_bound_or_zero",
        "target_value": "2.8e-15",
        "units": "dimensionless",
        "source": str(P8_TEMPLATE_PATH),
        "evaluation_rule": "abs(predicted eta_source_AB) <= 2.8e-15 or derived universal source charge",
        "scoreable_now": "false",
        "reason_not_scoreable": "source-charge prediction missing",
    },
    {
        "component_id": "P8_radial_source_hair",
        "observable": "partial_r_ln_mu_obs",
        "target_type": "zero_or_mapped_bound",
        "target_value": "zero radial hair or mapped PPN/fifth-force residuals",
        "units": "inverse_length_or_dimensionless_envelope",
        "source": str(P8_TEMPLATE_PATH),
        "evaluation_rule": "score only with radial profile/theorem or explicit mapping to PPN/R10",
        "scoreable_now": "false",
        "reason_not_scoreable": "radial profile missing",
    },
    {
        "component_id": "P8_range_dependence",
        "observable": "alpha(lambda)",
        "target_type": "curve_bound_or_zero",
        "target_value": "verified alpha(lambda) bound curve",
        "units": "range-dependent",
        "source": str(P8_TEMPLATE_PATH),
        "evaluation_rule": "score only against executable alpha(lambda) curve with lambda and alpha_predicted columns",
        "scoreable_now": "false",
        "reason_not_scoreable": "alpha(lambda) curve missing",
    },
    {
        "component_id": "P8_frame_calibration_split",
        "observable": "delta_frame_source",
        "target_type": "zero_or_row_locks",
        "target_value": "one observed frame or residual below WEP/clock locks",
        "units": "dimensionless",
        "source": str(P8_TEMPLATE_PATH),
        "evaluation_rule": "score only with parent frame theorem or numeric split residual",
        "scoreable_now": "false",
        "reason_not_scoreable": "frame/source split residual missing",
    },
    {
        "component_id": "P8_nonlinear_beta_source_residue",
        "observable": "delta_beta_source",
        "target_type": "upper_bound_or_zero",
        "target_value": "7.8e-05",
        "units": "dimensionless",
        "source": str(P8_TEMPLATE_PATH),
        "evaluation_rule": "abs(predicted delta_beta_source) <= 7.8e-05 or second-order theorem-zero",
        "scoreable_now": "false",
        "reason_not_scoreable": "deferred until first-order rows score",
    },
]


DECISION_COLUMNS = ["decision_item", "status", "evidence", "next_action"]


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in SOURCE_REGISTER:
        rows.append(
            {
                "path": item["path"],
                "exists": str((ROOT / item["path"]).exists()),
                "role": item["role"],
            }
        )
    return rows


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with (ROOT / path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def count_token(rows: list[dict[str, Any]], token: str) -> int:
    return sum(str(value).count(token) for row in rows for value in row.values())


def decision_rows(source_paths_missing: int, derivative_rows_loaded: int, p8_template_rows_loaded: int) -> list[dict[str, str]]:
    missing_predictions = sum(1 for row in RUNNER_INPUT_ROWS if "MISSING_" in row["predicted_value"])
    zero_failures = sum(1 for row in ZERO_THEOREM_ROWS if row["current_status"] not in {"pass_identity"})
    return [
        {
            "decision_item": "source_paths",
            "status": "pass" if source_paths_missing == 0 else "fail",
            "evidence": f"missing source paths = {source_paths_missing}",
            "next_action": "continue only with existing source paths",
        },
        {
            "decision_item": "derivative_gate_loaded",
            "status": "pass" if derivative_rows_loaded == 8 else "fail",
            "evidence": f"derivative rows loaded = {derivative_rows_loaded}",
            "next_action": "use CGM rows as local runner backbone",
        },
        {
            "decision_item": "P8_template_loaded",
            "status": "pass" if p8_template_rows_loaded == 8 else "fail",
            "evidence": f"P8 source-normalization template rows loaded = {p8_template_rows_loaded}",
            "next_action": "copy bound targets into runner input",
        },
        {
            "decision_item": "zero_theorem_currently_closes",
            "status": "fail",
            "evidence": f"non-identity theorem premises still open/failed/deferred = {zero_failures}",
            "next_action": "do not promote constant GM; use residual runner",
        },
        {
            "decision_item": "runner_predictions_scoreable",
            "status": "fail",
            "evidence": f"runner rows with missing predictions = {missing_predictions}",
            "next_action": "fill theorem-zero or numeric prediction source for each row",
        },
        {
            "decision_item": "constant_GM_promoted",
            "status": "fail",
            "evidence": "Z1-Z7 do not all pass and runner rows are not numerically scoreable",
            "next_action": NEXT_TARGET,
        },
        {
            "decision_item": "local_GR_promoted",
            "status": "fail",
            "evidence": "constant GM not promoted and second-order beta/gamma row deferred",
            "next_action": "wait for first-order rows plus PPN vector",
        },
    ]


def render_doc(
    run_dir: Path,
    source_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    derivative_rows_loaded: int,
    p8_template_rows_loaded: int,
    missing_prediction_rows: int,
) -> str:
    return f"""# 466 - Constant-GM Zero Theorem or Local Residual Runner

Private source-normalization checkpoint. This is not a public measured-GM, Newtonian-limit, PPN, local-GR, cosmology, EM, or unified-field claim.

## 1. Question

Checkpoint 465 gave the exact law

```text
D_X ln mu_obs
  = D_X ln G_eff
  + D_X ln M_eff
  + D_X ln(1 + epsilon_mu).
```

This checkpoint asks whether the zero theorem closes now. If it does not, the same terms must become local residual rows with bound targets.

## 2. Run Metadata

| Field | Value |
| --- | --- |
| Script | `scripts/constant_GM_zero_theorem_or_local_residual_runner.py` |
| Run directory | `{run_dir}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Zero theorem CSV | `{ZERO_THEOREM_PATH}` |
| Local runner input CSV | `{RESIDUAL_RUNNER_INPUT_PATH}` |
| Bound matrix CSV | `{BOUND_MATRIX_PATH}` |
| Decision CSV | `{DECISION_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{md_table(source_rows, ["path", "exists", "role"])}

## 4. Conditional Zero Theorem

The theorem shape is now exact:

```text
If
  D_X ln G_eff = 0,
  D_X ln M_eff = 0,
  D_X epsilon_mu = 0
for every local channel X,
then
  D_X ln mu_obs = 0
for every local channel X.
```

This is a useful conditional theorem, but it is not a proof of the premises.

{md_table(ZERO_THEOREM_ROWS, ZERO_THEOREM_COLUMNS)}

## 5. Local Residual Runner Input

The local runner input has been written to `{RESIDUAL_RUNNER_INPUT_PATH}`.

{md_table(RUNNER_INPUT_ROWS, RUNNER_INPUT_COLUMNS)}

## 6. Bound Matrix

The bound matrix has been written to `{BOUND_MATRIX_PATH}`.

{md_table(BOUND_MATRIX_ROWS, BOUND_MATRIX_COLUMNS)}

## 7. Decision

{md_table(decisions, DECISION_COLUMNS)}

## 8. Result

The zero theorem does not close yet. It fails for the right reason: not because the algebra is broken, but because the parent theory has not yet supplied the silence of `G_eff`, `M_eff`, and `epsilon_mu`.

The useful progress is that the failure is now executable. The runner loaded `{derivative_rows_loaded}` derivative rows and `{p8_template_rows_loaded}` P8 bound-template rows, then produced `{len(RUNNER_INPUT_ROWS)}` local residual input rows. `{missing_prediction_rows}` rows still have missing MTS predictions or theorem-zero sources, so nothing is claimable yet.

Practical read: we have stopped letting `GM` be a magic pocket. If it is constant, the parent action has to prove it. If it is not proven, every bit of derivative hair has a row, a target, and a place to get punched by data.

## 9. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | highest blocker is `epsilon_mu = mu_extra/(G_eff M_eff)` because it controls hidden measured-GM contribution |
| 2 | `R10_alpha_lambda_curve_MTS_source_normalization.csv` | range dependence cannot be scored without an executable curve or theorem-zero |
| 3 | `P8_time_drift_residual_or_zero.csv` | local Gdot row is one of the cleanest early quantitative locks |
"""


def write_run(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-constant-GM-zero-theorem-or-local-residual-runner"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    source_paths_missing = sum(1 for row in source_rows if row["exists"] != "True")
    derivative_rows = read_csv_rows(DERIVATIVE_GATE_PATH)
    p8_template_rows = read_csv_rows(P8_TEMPLATE_PATH)
    r11_rows = read_csv_rows(R11_DERIVATIVE_VECTOR_PATH)

    missing_prediction_rows = sum(1 for row in RUNNER_INPUT_ROWS if "MISSING_" in row["predicted_value"])
    missing_markers_in_runner = count_token(RUNNER_INPUT_ROWS, "MISSING_")
    missing_markers_in_r11 = count_token(r11_rows, "MISSING_")
    generic_fill_tokens = count_token(RUNNER_INPUT_ROWS, "fill_") + count_token(ZERO_THEOREM_ROWS, "fill_") + count_token(BOUND_MATRIX_ROWS, "fill_")
    decisions = decision_rows(source_paths_missing, len(derivative_rows), len(p8_template_rows))

    write_csv(ROOT / ZERO_THEOREM_PATH, ZERO_THEOREM_ROWS, ZERO_THEOREM_COLUMNS)
    write_csv(ROOT / RESIDUAL_RUNNER_INPUT_PATH, RUNNER_INPUT_ROWS, RUNNER_INPUT_COLUMNS)
    write_csv(ROOT / BOUND_MATRIX_PATH, BOUND_MATRIX_ROWS, BOUND_MATRIX_COLUMNS)
    write_csv(ROOT / DECISION_PATH, decisions, DECISION_COLUMNS)

    write_csv(results_dir / "constant_GM_zero_theorem_attempt.csv", ZERO_THEOREM_ROWS, ZERO_THEOREM_COLUMNS)
    write_csv(results_dir / "constant_GM_local_residual_runner_input.csv", RUNNER_INPUT_ROWS, RUNNER_INPUT_COLUMNS)
    write_csv(results_dir / "constant_GM_residual_bound_matrix.csv", BOUND_MATRIX_ROWS, BOUND_MATRIX_COLUMNS)
    write_csv(results_dir / "decision.csv", decisions, DECISION_COLUMNS)
    write_csv(results_dir / "source_register.csv", source_rows, ["path", "exists", "role"])

    doc = render_doc(
        run_dir=Path("runs") / f"{timestamp}-constant-GM-zero-theorem-or-local-residual-runner",
        source_rows=source_rows,
        decisions=decisions,
        derivative_rows_loaded=len(derivative_rows),
        p8_template_rows_loaded=len(p8_template_rows),
        missing_prediction_rows=missing_prediction_rows,
    )
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    status = {
        "timestamp": timestamp,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "source_paths_missing": source_paths_missing,
        "derivative_rows_loaded": len(derivative_rows),
        "p8_source_normalization_template_rows_loaded": len(p8_template_rows),
        "r11_derivative_vector_rows_loaded": len(r11_rows),
        "zero_theorem_premise_rows": len(ZERO_THEOREM_ROWS),
        "local_residual_runner_input_rows": len(RUNNER_INPUT_ROWS),
        "bound_matrix_rows": len(BOUND_MATRIX_ROWS),
        "decision_rows": len(decisions),
        "conditional_zero_theorem_written": True,
        "zero_theorem_currently_closes": False,
        "local_residual_runner_inputs_loaded": True,
        "runner_rows_with_missing_predictions": missing_prediction_rows,
        "missing_markers_in_runner_inputs": missing_markers_in_runner,
        "missing_markers_in_R11_derivative_vector_loaded": missing_markers_in_r11,
        "generic_fill_placeholder_tokens_in_outputs": generic_fill_tokens,
        "numeric_predictions_loaded": False,
        "constant_GM_promoted": False,
        "Newtonian_reduction_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    write_json(run_dir / "status.json", status)
    return status


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default="20260602-213000")
    arguments = parser.parse_args()
    print(json.dumps(write_run(arguments.timestamp), indent=2))


if __name__ == "__main__":
    main()
