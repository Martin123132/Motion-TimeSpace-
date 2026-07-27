from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_R10_alpha_lambda_no_range_theorem_failed_source_normalized_curve_placeholder_written"
CLAIM_CEILING = "R10_alpha_lambda_data_or_no_range_attempt_only_no_fifth_force_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "559-Y5-R10-bound-curve-digitization-and-MTS-alpha-prediction-runner.md"

DOC_PATH = Path("558-Y5-R10-alpha-lambda-source-normalized-curve-data-or-no-range-theorem.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_558_SOURCE_REGISTER.csv")
NO_RANGE_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_NO_RANGE_THEOREM_ATTEMPT.csv")
CURVE_DATA_AUDIT_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_CURVE_DATA_AUDIT.csv")
MTS_CURVE_INPUT_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_MTS_CURVE_INPUT_CONTRACT.csv")
R10_PLACEHOLDER_REJECTION_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAMBDA_PLACEHOLDER_REJECTION.csv")
R10_MTS_CURVE_PATH = Path("source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv")
EVALUATOR_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_558_EVALUATOR.csv")
OBSTRUCTION_LEDGER_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_558_OBSTRUCTION_LEDGER.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_558_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_558_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_558_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "557-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill.md",
        "role": "bulk/memory/range no-hair miss and R10/Yukawa fill contract",
    },
    {
        "source_file": "556-Y5-extra-sector-Hamiltonian-charge-silence-or-channel-fill.md",
        "role": "Cextra core channel split",
    },
    {
        "source_file": "437-R10-alpha-lambda-executable-curve-contract.md",
        "role": "R10 executable alpha(lambda) curve contract",
    },
    {
        "source_file": "380-bulk-X-mass-gap-source-normalized-force-law.md",
        "role": "bulk-X source-normalized Yukawa force-law debt",
    },
    {
        "source_file": "428-MTS-local-residual-vector-input-contract.md",
        "role": "local residual vector R10 symbolic curve requirement",
    },
    {
        "source_file": "431-MTS-local-residual-vector-evaluator.md",
        "role": "evaluator refusal of missing symbolic R10 curve",
    },
    {
        "source_file": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "local bound manifest with symbolic R10 fifth-force row",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_CEXTRA_BULK_MEMORY_RANGE_R10_CURVE_CONTRACT.csv",
        "role": "557 R10 curve/theorem-zero contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_CEXTRA_BULK_MEMORY_RANGE_YUKAWA_FILL_ROW.csv",
        "role": "557 Yukawa fill row",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_557_VALIDATION.csv",
        "role": "previous validation gate",
    },
    {
        "source_file": "source-intake/mts_residuals/R10_alpha_lambda_curve_TEMPLATE.csv",
        "role": "generic R10 alpha(lambda) curve template",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv",
        "role": "mu_extra local scorecard requiring R10 curve rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MU_EXTRA_SCORECARD_REQUIRED_INPUTS.csv",
        "role": "required R10 curve input artifact row",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv",
        "role": "range derivative hair gate",
    },
    {
        "source_file": "runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/source_normalized_force_law.csv",
        "role": "380 source-normalized bulk-X force law ledger",
    },
    {
        "source_file": "runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/gate_results.csv",
        "role": "380 gate results showing alpha/lambda not parent-derived",
    },
    {
        "source_file": "scripts/Y5_R10_alpha_lambda_source_normalized_curve_data_or_no_range_theorem.py",
        "role": "this checkpoint generator",
    },
]


NO_RANGE_ATTEMPT_ROWS = [
    {
        "step_id": "NR558_0_target",
        "claim": "the R10 finite-range channel is absent or theorem-zero for the local branch",
        "mathematical_form": "alpha(lambda)=0 for every lambda in the local test range",
        "current_result": "target_defined",
        "why_not_enough": "target definition is not a no-range theorem",
        "valid_for_claim": "false",
    },
    {
        "step_id": "NR558_1_absent_coupling",
        "claim": "bulk/memory/range source and test charges are exactly absent",
        "mathematical_form": "Q_X=q_test=0 or q_X rho_source=0 and Pi_M^H Q_X=0",
        "current_result": "not_derived",
        "why_not_enough": "source/test charge normalization remains missing from the parent action",
        "valid_for_claim": "false",
    },
    {
        "step_id": "NR558_2_positive_operator_nohair",
        "claim": "a positive source-free no-hair theorem removes the finite-range field",
        "mathematical_form": "(-Delta+m_X^2)X=0, m_X^2>0, boundary_flux=0 => X=0",
        "current_result": "conditional_not_signed",
        "why_not_enough": "operator sign, boundary flux, source charge, and Hamiltonian projection are not all supplied",
        "valid_for_claim": "false",
    },
    {
        "step_id": "NR558_3_gauge_topological_absence",
        "claim": "the finite-range-looking variable is pure gauge/topological and has no local stress or matter charge",
        "mathematical_form": "X=dLambda or delta_g S_X=delta_m S_X=0 in A",
        "current_result": "not_derived",
        "why_not_enough": "no gauge/topological proof exists for the active bulk/memory/range channel",
        "valid_for_claim": "false",
    },
    {
        "step_id": "NR558_4_screened_branch",
        "claim": "a screened local branch suppresses alpha(lambda) below all R10 bounds",
        "mathematical_form": "alpha_predicted(lambda) <= alpha_bound(lambda) with screening source and no WEP/time/range leakage",
        "current_result": "not_supplied",
        "why_not_enough": "screening law and sampled alpha(lambda) curve are missing",
        "valid_for_claim": "false",
    },
    {
        "step_id": "NR558_5_universal_calibration",
        "claim": "the surviving monopole is a constant universal calibration, not a finite-range force",
        "mathematical_form": "D_t epsilon=D_r epsilon=D_lambda epsilon=D_species epsilon=0",
        "current_result": "not_parent_fixed",
        "why_not_enough": "range/species/time/radius derivative silence is not parent-derived",
        "valid_for_claim": "false",
    },
    {
        "step_id": "NR558_6_executable_curve_fallback",
        "claim": "if no theorem-zero exists, the branch supplies an executable alpha(lambda) curve",
        "mathematical_form": "CSV rows: lambda_i, alpha_predicted_i, alpha_bound_i, sources, valid_for_claim=true after validation",
        "current_result": "template_only",
        "why_not_enough": "the curve file written here is intentionally invalid until real MTS prediction and bound rows replace placeholders",
        "valid_for_claim": "false",
    },
    {
        "step_id": "NR558_7_verdict",
        "claim": "R10/fifth-force can pass or be removed",
        "mathematical_form": "R10_pass=true or alpha(lambda)=0 theorem",
        "current_result": "fail_current_claim",
        "why_not_enough": "no no-range theorem and no executable source-normalized alpha(lambda) data exist yet",
        "valid_for_claim": "false",
    },
]


CURVE_DATA_AUDIT_ROWS = [
    {
        "audit_id": "R10A558_0_bound_manifest_symbolic",
        "artifact": "source-intake/local_bounds/local_bound_claims.csv",
        "what_exists": "R10 row names Adelberger_Heckel_Nelson_2003_ISL_curve and reference URL/DOI",
        "what_is_missing": "digitized lambda/alpha_bound rows in a machine-readable curve file",
        "claim_status": "bound_source_named_not_evaluable",
        "valid_for_claim": "false",
    },
    {
        "audit_id": "R10A558_1_MTS_prediction_missing",
        "artifact": "P8_Y5_CEXTRA_BULK_MEMORY_RANGE_YUKAWA_FILL_ROW.csv",
        "what_exists": "required symbols for m_X, lambda_X, alpha_X(lambda), source/test charges, and PiM projection",
        "what_is_missing": "numeric or theorem-zero values for every MTS-side field",
        "claim_status": "MTS_prediction_missing",
        "valid_for_claim": "false",
    },
    {
        "audit_id": "R10A558_2_template_exists",
        "artifact": "R10_alpha_lambda_curve_TEMPLATE.csv",
        "what_exists": "generic executable curve schema",
        "what_is_missing": "branch-specific rows with real alpha_predicted and alpha_bound",
        "claim_status": "template_only",
        "valid_for_claim": "false",
    },
    {
        "audit_id": "R10A558_3_branch_placeholder_written",
        "artifact": "R10_alpha_lambda_curve_MTS_source_normalization.csv",
        "what_exists": "expected branch file name and schema-compatible placeholder rows",
        "what_is_missing": "all claim-bearing numeric data and theorem-zero certificate",
        "claim_status": "placeholder_rejected",
        "valid_for_claim": "false",
    },
    {
        "audit_id": "R10A558_4_next_data_task",
        "artifact": "future R10 bound/prediction runner",
        "what_exists": "contract for comparing alpha_predicted(lambda) to alpha_bound(lambda)",
        "what_is_missing": "external bound digitization/source plus MTS alpha(lambda) prediction",
        "claim_status": "next_target",
        "valid_for_claim": "false",
    },
]


MTS_CURVE_INPUT_CONTRACT_ROWS = [
    {
        "contract_id": "MTSR10_0_bulk_X_static_green_function",
        "branch": "bulk_X_Yukawa_tail",
        "required_MTS_inputs": "m_X;lambda_X;Q_X_source_charge;q_test_bulk_charge;PiM_H_projection;G_measured_normalization",
        "alpha_prediction_rule": "alpha_predicted(lambda_X) from source-normalized Q_X q_test / (G_measured M_source m_test) with declared convention",
        "allowed_status": "derived_zero;derived_bound;source_backed_numeric;template_invalid",
        "current_status": "template_invalid",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "MTSR10_1_memory_tail_envelope",
        "branch": "memory_history_kernel",
        "required_MTS_inputs": "kernel_form;tail_bound;lambda_grid;conservative_alpha_envelope;source_normalization",
        "alpha_prediction_rule": "alpha_envelope(lambda) must bound the full nonlocal tail in the R10 convention",
        "allowed_status": "derived_bound;theorem_zero;template_invalid",
        "current_status": "template_invalid",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "MTSR10_2_no_range_theorem",
        "branch": "no_range_zero",
        "required_MTS_inputs": "operator;source_charge;boundary_flux;Hamiltonian_projection;memory_kernel;range_derivatives;source_file",
        "alpha_prediction_rule": "alpha(lambda)=0 only after all theorem-zero premises are parent-derived",
        "allowed_status": "theorem_zero;template_invalid",
        "current_status": "template_invalid",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "MTSR10_3_bound_curve_data",
        "branch": "external_R10_bound",
        "required_MTS_inputs": "lambda_grid;alpha_bound;alpha_bound_source;interpolation_policy;units",
        "alpha_prediction_rule": "compare abs(alpha_predicted) <= alpha_bound at every sampled lambda with conservative interpolation",
        "allowed_status": "source_backed_numeric;template_invalid",
        "current_status": "template_invalid",
        "valid_for_claim": "false",
    },
]


R10_MTS_CURVE_ROWS = [
    {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "bulk_memory_range_template",
        "curve_id": "R10_alpha_lambda_curve_MTS_source_normalization",
        "lambda_value": "MISSING_NUMERIC_LAMBDA",
        "lambda_units": "m",
        "alpha_predicted": "MISSING_SOURCE_NORMALIZED_ALPHA_PREDICTION",
        "alpha_bound": "MISSING_DIGITIZED_ALPHA_BOUND",
        "alpha_bound_source": "source-intake/local_bounds/local_bound_claims.csv::R10_fifth_force names source only, not digitized curve",
        "force_law_form": "bulk_X_static_green_function",
        "derivation_status": "template_invalid_missing_MTS_prediction_and_bound_curve",
        "formula_reference": "557-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill.md",
        "source_file": "MISSING_SOURCE_FILE",
        "assumptions": "same-frame source normalization; measured-G calibration; no cancellation credit",
        "valid_for_claim": "false",
        "notes": "replace with real sampled lambda/alpha rows before any R10 claim",
    },
    {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "no_range_theorem_zero_template",
        "curve_id": "R10_alpha_lambda_curve_MTS_source_normalization",
        "lambda_value": "ALL_LOCAL_R10_RANGE",
        "lambda_units": "m",
        "alpha_predicted": "MISSING_THEOREM_ZERO_CERTIFICATE",
        "alpha_bound": "not_applicable_until_theorem_zero_signed",
        "alpha_bound_source": "not_applicable_until_theorem_zero_signed",
        "force_law_form": "theorem_zero_candidate",
        "derivation_status": "template_invalid_missing_no_range_theorem",
        "formula_reference": "558-Y5-R10-alpha-lambda-source-normalized-curve-data-or-no-range-theorem.md",
        "source_file": "MISSING_SOURCE_FILE",
        "assumptions": "absent/gauge/topological/screened/nohair source with zero range derivatives",
        "valid_for_claim": "false",
        "notes": "do not count as alpha=0 until theorem-zero premises are source-backed",
    },
]


PLACEHOLDER_REJECTION_ROWS = [
    {
        "rejection_id": "PR558_0_missing_MTS_alpha",
        "row_or_artifact": "R10_alpha_lambda_curve_MTS_source_normalization.csv",
        "reason": "alpha_predicted is missing or nonnumeric",
        "repair": "derive alpha_predicted(lambda) from MTS source-normalized force law",
        "valid_for_claim": "false",
    },
    {
        "rejection_id": "PR558_1_missing_bound_curve",
        "row_or_artifact": "local_bound_claims.csv::R10_fifth_force",
        "reason": "upper_bound is symbolic alpha(lambda), not digitized lambda/alpha rows",
        "repair": "digitize/source an external bound curve with units and provenance",
        "valid_for_claim": "false",
    },
    {
        "rejection_id": "PR558_2_missing_theorem_zero",
        "row_or_artifact": "no_range_theorem_zero_template",
        "reason": "theorem-zero certificate is missing",
        "repair": "derive absent/gauge/topological/screened/nohair branch with zero source, flux, projection, and range derivatives",
        "valid_for_claim": "false",
    },
    {
        "rejection_id": "PR558_3_placeholder_claim_flag",
        "row_or_artifact": "all 558 placeholder rows",
        "reason": "valid_for_claim=false and derivation_status is template_invalid",
        "repair": "replace placeholders with source-backed values and rerun evaluator",
        "valid_for_claim": "false",
    },
]


OBSTRUCTION_ROWS = [
    {
        "obstruction_id": "R10O558_0_no_range_not_proved",
        "obstruction": "no parent theorem removes finite-range source/test coupling, field profile, or Hamiltonian projection",
        "activated_residual": "R10_fifth_force;epsilon_bulk_memory_range_over_MH",
        "repair": "derive no-range theorem-zero certificate",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "R10O558_1_bound_curve_not_digitized",
        "obstruction": "external R10 bound exists as a reference, not as machine-readable lambda/alpha_bound curve data",
        "activated_residual": "alpha_bound(lambda)",
        "repair": "source/digitize bound curve and record units/interpolation policy",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "R10O558_2_MTS_alpha_missing",
        "obstruction": "MTS alpha_predicted(lambda) is not derived from source-normalized charges or an envelope",
        "activated_residual": "alpha_predicted(lambda);Q_X;q_test;PiM_H_projection",
        "repair": "derive MTS curve or conservative alpha envelope",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "R10O558_3_mass_gap_guardrail_retained",
        "obstruction": "m_X/lambda_X alone cannot score R10 without alpha strength and source/test normalization",
        "activated_residual": "lambda_X;alpha_X_lambda",
        "repair": "derive alpha strength or prove source/test charges vanish",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "R10O558_4_no_local_GR_promotion",
        "obstruction": "R10 is only one component and remains unfilled",
        "activated_residual": "C_extra_over_MH;epsilon_HPiM_radial_closure_abs;local_GR",
        "repair": "close R10 plus remaining Cextra/Cterm/source-measure/PPN rows before promotion",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D558_0_no_range_failed",
        "status": "no_range_theorem_not_signed",
        "meaning": "current MTS cannot set alpha(lambda)=0 for R10",
        "claim_status": "R10_retained",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D558_1_placeholder_curve_written",
        "status": "expected_R10_curve_file_written_invalid",
        "meaning": "the exact required curve file now exists but is explicitly non-claim until real values replace placeholders",
        "claim_status": "template_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D558_2_bound_data_audit",
        "status": "external_bound_source_named_not_digitized",
        "meaning": "the Adelberger-style R10 source is named locally, but machine-readable alpha_bound(lambda) rows are still missing",
        "claim_status": "not_evaluable",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D558_3_local_GR_status",
        "status": "local_GR_still_closure_only",
        "meaning": "no R10/fifth-force, Cextra, radial closure, Newton, PPN, or local-GR promotion is earned",
        "claim_status": "local_GR_claim_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D558_4_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "R10_FIFTH_FORCE",
        "previous_status": "bulk_memory_range_requires_real_curve_or_zero_certificate",
        "new_status": "no_range_failed_expected_curve_file_written_invalid",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "CEXTRA_BULK_MEMORY_RANGE",
        "previous_status": "positive_operator_zero_failed_Yukawa_R10_fill_row_written",
        "new_status": "still_failed_no_range_and_no_alpha_lambda_curve",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_RESIDUAL_VECTOR",
        "previous_status": "R10_symbolic_curve_missing",
        "new_status": "R10_placeholder_file_exists_but_rejected_for_claim",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "HAMILTONIAN_EXTRA_CHARGE_SILENCE",
        "previous_status": "still_failed_bulk_memory_range_not_zero_or_bounded",
        "new_status": "still_failed_R10_bulk_memory_range_data_missing",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR_TRANSITION_ROUTE",
        "previous_status": "closure_only_R10_bulk_memory_range_not_zero_or_bounded",
        "new_status": "closure_only_R10_no_range_or_curve_not_available",
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


def evaluator_rows() -> list[dict[str, Any]]:
    return [
        {
            "evaluator_id": "E558_0_R10_claim_gate",
            "target": "R10_alpha_lambda_curve_MTS_source_normalization.csv",
            "pass_status": "not_claimable",
            "reason": "all rows have valid_for_claim=false and missing numeric/theorem-zero fields",
            "valid_for_claim": "false",
        },
        {
            "evaluator_id": "E558_1_no_range_gate",
            "target": "alpha(lambda)=0 theorem",
            "pass_status": "not_claimable",
            "reason": "no parent-derived absent/gauge/topological/screened/no-hair certificate exists",
            "valid_for_claim": "false",
        },
    ]


def validation_rows(sources: list[dict[str, Any]], eval_rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    prior_validation = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_557_VALIDATION.csv"))
    prior_fails = [row for row in prior_validation if row.get("result") == "fail"]
    local_bounds = read_csv(Path("source-intake/local_bounds/local_bound_claims.csv"))
    r10_local_rows = [row for row in local_bounds if row.get("row_id") == "R10_fifth_force"]
    prior_curve_contract = read_csv(Path("source-intake/mts_residuals/P8_Y5_CEXTRA_BULK_MEMORY_RANGE_R10_CURVE_CONTRACT.csv"))
    prior_yukawa_fill = read_csv(Path("source-intake/mts_residuals/P8_Y5_CEXTRA_BULK_MEMORY_RANGE_YUKAWA_FILL_ROW.csv"))
    generic_template = read_csv(Path("source-intake/mts_residuals/R10_alpha_lambda_curve_TEMPLATE.csv"))
    branch_curve = read_csv(R10_MTS_CURVE_PATH)
    scorecard = read_csv(Path("source-intake/mts_residuals/P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv"))
    required_inputs = read_csv(Path("source-intake/mts_residuals/P8_MU_EXTRA_SCORECARD_REQUIRED_INPUTS.csv"))
    derivative_gate = read_csv(Path("source-intake/mts_residuals/P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv"))
    bulk_force_law = read_csv(Path("runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/source_normalized_force_law.csv"))
    bulk_gate_results = read_csv(Path("runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/gate_results.csv"))
    claim_attempt_rows = [row for row in NO_RANGE_ATTEMPT_ROWS if row["valid_for_claim"] == "true"]
    claim_audit_rows = [row for row in CURVE_DATA_AUDIT_ROWS if row["valid_for_claim"] == "true"]
    claim_contract_rows = [row for row in MTS_CURVE_INPUT_CONTRACT_ROWS if row["valid_for_claim"] == "true"]
    claim_curve_rows = [row for row in branch_curve if row.get("valid_for_claim") == "true"]
    claim_rejection_rows = [row for row in PLACEHOLDER_REJECTION_ROWS if row["valid_for_claim"] == "true"]
    claim_eval_rows = [row for row in eval_rows if row["valid_for_claim"] == "true"]
    placeholder_markers = [
        row
        for row in branch_curve
        if "MISSING" in json.dumps(row) or row.get("valid_for_claim") == "false"
    ]
    return [
        {
            "check_id": "V558_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V558_1_prior_557_clean",
            "result": "pass" if len(prior_validation) == 11 and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_validation)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V558_2_R10_bound_manifest_loaded",
            "result": "pass" if len(local_bounds) == 12 and len(r10_local_rows) == 1 else "fail",
            "detail": f"local_bound_rows={len(local_bounds)};R10_rows={len(r10_local_rows)};R10_upper_bound={r10_local_rows[0].get('upper_bound') if r10_local_rows else 'missing'}",
        },
        {
            "check_id": "V558_3_prior_curve_contract_loaded",
            "result": "pass" if len(prior_curve_contract) == 2 and len(prior_yukawa_fill) == 1 else "fail",
            "detail": f"prior_curve_contract={len(prior_curve_contract)};prior_yukawa_fill={len(prior_yukawa_fill)}",
        },
        {
            "check_id": "V558_4_templates_written",
            "result": "pass" if len(generic_template) == 2 and len(branch_curve) == 2 else "fail",
            "detail": f"generic_template={len(generic_template)};branch_curve={len(branch_curve)}",
        },
        {
            "check_id": "V558_5_scorecard_context_loaded",
            "result": "pass" if len(scorecard) == 21 and len(required_inputs) == 8 and len(derivative_gate) == 8 else "fail",
            "detail": f"scorecard={len(scorecard)};required_inputs={len(required_inputs)};derivative_gate={len(derivative_gate)}",
        },
        {
            "check_id": "V558_6_bulk_force_law_prior_loaded",
            "result": "pass" if len(bulk_force_law) == 5 and len(bulk_gate_results) == 10 else "fail",
            "detail": f"bulk_force_law={len(bulk_force_law)};bulk_gates={len(bulk_gate_results)}",
        },
        {
            "check_id": "V558_7_attempt_and_audit_complete",
            "result": "pass" if len(NO_RANGE_ATTEMPT_ROWS) == 8 and len(CURVE_DATA_AUDIT_ROWS) == 5 and len(MTS_CURVE_INPUT_CONTRACT_ROWS) == 4 and len(PLACEHOLDER_REJECTION_ROWS) == 4 else "fail",
            "detail": f"no_range={len(NO_RANGE_ATTEMPT_ROWS)};audit={len(CURVE_DATA_AUDIT_ROWS)};contract={len(MTS_CURVE_INPUT_CONTRACT_ROWS)};rejections={len(PLACEHOLDER_REJECTION_ROWS)}",
        },
        {
            "check_id": "V558_8_placeholders_rejected",
            "result": "pass" if len(placeholder_markers) == len(branch_curve) and not claim_curve_rows else "fail",
            "detail": f"placeholder_rows={len(placeholder_markers)};branch_curve_rows={len(branch_curve)};claim_curve_rows={len(claim_curve_rows)}",
        },
        {
            "check_id": "V558_9_no_claim_rows",
            "result": "pass" if not claim_attempt_rows and not claim_audit_rows and not claim_contract_rows and not claim_curve_rows and not claim_rejection_rows and not claim_eval_rows else "fail",
            "detail": f"claim_attempt={len(claim_attempt_rows)};claim_audit={len(claim_audit_rows)};claim_contract={len(claim_contract_rows)};claim_curve={len(claim_curve_rows)};claim_rejection={len(claim_rejection_rows)};claim_eval={len(claim_eval_rows)}",
        },
        {
            "check_id": "V558_10_no_overclaim",
            "result": "pass" if not claim_attempt_rows and not claim_audit_rows and not claim_contract_rows and not claim_curve_rows and not claim_rejection_rows and not claim_eval_rows else "fail",
            "detail": "no_range_theorem=false; R10_pass=false; Cextra_zero=false; radial_closure=false; Newton=false; PPN=false; local_GR=false",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row.keys()}) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_run_csv(results_dir: Path, filename: str, rows: list[dict[str, Any]]) -> None:
    fieldnames = sorted({key for row in rows for key in row.keys()}) if rows else []
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
    eval_rows: list[dict[str, Any]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 558 - Y5 R10 Alpha-Lambda Source-Normalized Curve Data or No-Range Theorem

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

R10 still does not pass.

The no-range theorem is not derived, and the data branch is not executable yet. The useful progress is practical: the exact required branch file now exists at `source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv`, but it is intentionally invalid until real values replace the placeholders.

```text
R10 pass requires:
  alpha(lambda)=0 by theorem-zero,
  or sampled rows with alpha_predicted(lambda_i) and alpha_bound(lambda_i).
```

Right now MTS has neither.

## 2. No-Range Theorem Attempt

{markdown_table(NO_RANGE_ATTEMPT_ROWS)}

## 3. Curve Data Audit

{markdown_table(CURVE_DATA_AUDIT_ROWS)}

## 4. MTS Curve Input Contract

{markdown_table(MTS_CURVE_INPUT_CONTRACT_ROWS)}

## 5. Placeholder Curve File

{markdown_table(R10_MTS_CURVE_ROWS)}

## 6. Placeholder Rejection

{markdown_table(PLACEHOLDER_REJECTION_ROWS)}

## 7. Evaluator

{markdown_table(eval_rows)}

## 8. Obstruction Ledger

{markdown_table(OBSTRUCTION_ROWS)}

## 9. Decision

{markdown_table(DECISION_ROWS)}

## 10. Source Register

{markdown_table(sources)}

## 11. Validation

{markdown_table(validations)}

## 12. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 13. Claim Ceiling

Allowed:

```text
MTS has attempted a no-range theorem for R10.
MTS has audited the R10 data gap.
MTS has written the expected R10 branch file as an invalid placeholder.
```

Forbidden:

```text
MTS has passed R10/fifth-force.
MTS has proved alpha(lambda)=0.
MTS has proved C_extra = 0, radial closure, Newton, PPN, or local GR.
```

## 14. Practical Read

This is the first step where the future test is truly mechanical: replace placeholder rows with real `lambda`, `alpha_predicted`, and `alpha_bound`, or prove the no-range theorem. No more scalar R10 vibes. This is either a curve, or it is zero by theorem.

## 15. Next Target

`{NEXT_TARGET}`

Next: acquire/digitize the R10 bound curve and derive or placeholder-test the MTS `alpha_predicted(lambda)` runner without allowing claim credit.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-R10-alpha-lambda-source-normalized-curve-data-or-no-range-theorem"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    eval_rows = evaluator_rows()

    csv_outputs_before_validation: list[tuple[Path, list[dict[str, Any]]]] = [
        (R10_MTS_CURVE_PATH, R10_MTS_CURVE_ROWS),
    ]
    for path, rows in csv_outputs_before_validation:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    validations = validation_rows(sources, eval_rows)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (NO_RANGE_ATTEMPT_PATH, NO_RANGE_ATTEMPT_ROWS),
        (CURVE_DATA_AUDIT_PATH, CURVE_DATA_AUDIT_ROWS),
        (MTS_CURVE_INPUT_CONTRACT_PATH, MTS_CURVE_INPUT_CONTRACT_ROWS),
        (R10_PLACEHOLDER_REJECTION_PATH, PLACEHOLDER_REJECTION_ROWS),
        (EVALUATOR_PATH, eval_rows),
        (OBSTRUCTION_LEDGER_PATH, OBSTRUCTION_ROWS),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(generated_at_utc, run_dir, sources, eval_rows, validations)
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
        "no_range_attempt": str(ROOT / NO_RANGE_ATTEMPT_PATH),
        "curve_data_audit": str(ROOT / CURVE_DATA_AUDIT_PATH),
        "mts_curve_input_contract": str(ROOT / MTS_CURVE_INPUT_CONTRACT_PATH),
        "placeholder_rejection": str(ROOT / R10_PLACEHOLDER_REJECTION_PATH),
        "r10_mts_curve": str(ROOT / R10_MTS_CURVE_PATH),
        "evaluator": str(ROOT / EVALUATOR_PATH),
        "obstruction_ledger": str(ROOT / OBSTRUCTION_LEDGER_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "missing_sources": missing_sources,
        "failed_validations": failed_validations,
        "no_range_theorem_signed": False,
        "R10_fifth_force_passed": False,
        "R10_curve_file_written": True,
        "R10_curve_valid_for_claim": False,
        "Cextra_zero_signed": False,
        "radial_closure_claim_allowed": False,
        "source_measure_claim_allowed": False,
        "measured_GM_claim_allowed": False,
        "Newton_claim_allowed": False,
        "PPN_claim_allowed": False,
        "local_GR_claim_allowed": False,
        "github_push_performed": False,
        "formalization_workbench_modified": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        f"{STATUS}\nfailed_validations={len(failed_validations)}\nnext={NEXT_TARGET}\n",
        encoding="utf-8",
    )
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
