from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from R10_alpha_lambda_bound_prediction_runner import run_runner


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_R10_ZX_lambda_prefactor_range_conditionally_derived_theorem_zero_not_signed_bound_curve_missing"
CLAIM_CEILING = "R10_prefactor_range_gate_only_no_fifth_force_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md"

DOC_PATH = Path("562-Y5-R10-ZX-lambda-mass-gap-and-bound-curve-fill-or-theorem-zero.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_562_SOURCE_REGISTER.csv")
PREF_RANGE_FORMULA_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_ZX_LAMBDA_PREFACtOR_FORMULA_REGISTER.csv")
MASS_GAP_GATE_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_MASS_GAP_THEOREM_ZERO_GATE.csv")
NOHAIR_IDENTITY_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_POSITIVE_OPERATOR_NOHAIR_ATTEMPT.csv")
BOUND_CURVE_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_BOUND_CURVE_REAL_DATA_CONTRACT.csv")
ALPHA_ROW_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_ZX_LAMBDA_ALPHA_ROW_TEMPLATE.csv")
EVALUATOR_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_562_EVALUATOR.csv")
OBSTRUCTION_LEDGER_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_562_OBSTRUCTION_LEDGER.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_562_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_562_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_562_ROUTE_UPDATE.csv")

MTS_CURVE_PATH = Path("source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv")
BOUND_CURVE_PATH = Path("source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv")


SOURCE_REGISTER = [
    {
        "source_file": "561-Y5-R10-source-test-charge-and-PiM-projection-zero-or-coefficient-fill.md",
        "role": "R10 numerator factorization and coefficient fallback",
    },
    {
        "source_file": "560-Y5-R10-source-normalized-alpha-law-from-parent-or-runner-real-data-fill.md",
        "role": "conditional alpha law requiring Z_X and lambda_X",
    },
    {
        "source_file": "559-Y5-R10-bound-curve-digitization-and-MTS-alpha-prediction-runner.md",
        "role": "R10 runner and placeholder rejection",
    },
    {
        "source_file": "557-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill.md",
        "role": "mass-gap-alone guardrail and bulk/memory/range route",
    },
    {
        "source_file": "437-R10-alpha-lambda-executable-curve-contract.md",
        "role": "accepted R10 alpha(lambda) curve convention",
    },
    {
        "source_file": "380-bulk-X-mass-gap-source-normalized-force-law.md",
        "role": "bulk-X mass-gap/source-normalized force-law debt",
    },
    {
        "source_file": "runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/bulk_X_operator_routes.csv",
        "role": "operator route ledger",
    },
    {
        "source_file": "runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/source_normalized_force_law.csv",
        "role": "source-normalized force-law quantity ledger",
    },
    {
        "source_file": "runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/gate_results.csv",
        "role": "bulk-X gate results showing alpha/lambda not parent-derived",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_NUMERATOR_COEFFICIENT_VECTOR.csv",
        "role": "561 numerator coefficient vector",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_NUMERATOR_ALPHA_FILL_TEMPLATE.csv",
        "role": "561 alpha row template with K_X",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAW_FORMULA_REGISTER.csv",
        "role": "560 alpha formula register",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAW_PARENT_INPUTS.csv",
        "role": "560 parent input debts",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_BOUND_CURVE_DIGITIZATION_CONTRACT.csv",
        "role": "559 bound curve digitization contract",
    },
    {
        "source_file": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "symbolic R10 local-bound manifest",
    },
    {
        "source_file": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv",
        "role": "current MTS-side placeholder curve retained unchanged",
    },
    {
        "source_file": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "role": "current bound-side placeholder curve retained unchanged",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_561_VALIDATION.csv",
        "role": "previous validation gate",
    },
    {
        "source_file": "scripts/R10_alpha_lambda_bound_prediction_runner.py",
        "role": "reusable R10 curve comparator",
    },
    {
        "source_file": "scripts/Y5_R10_ZX_lambda_mass_gap_and_bound_curve_fill_or_theorem_zero.py",
        "role": "this checkpoint generator",
    },
]


PREF_RANGE_FORMULA_ROWS = [
    {
        "formula_id": "PR562_0_static_quadratic_energy",
        "object": "stable local X branch",
        "expression": "E_X=1/2 int d^3x [Z_X |grad X|^2 + M_X^2 X^2] - int d^3x J_X X",
        "derived_relation": "parent must supply Z_X and M_X^2 before lambda or no-hair is legal",
        "required_parent_inputs": "Z_X;M_X_squared;J_X;boundary_conditions;sign_convention",
        "status": "conditional_form_written",
        "valid_for_claim": "false",
    },
    {
        "formula_id": "PR562_1_static_operator",
        "object": "Euler operator",
        "expression": "(-Z_X Delta + M_X^2)X=J_X",
        "derived_relation": "divide by Z_X only if Z_X != 0 and sign is healthy",
        "required_parent_inputs": "Z_X positive;M_X_squared sign;source split",
        "status": "conditional_operator_written",
        "valid_for_claim": "false",
    },
    {
        "formula_id": "PR562_2_canonical_mass_and_range",
        "object": "canonical finite range",
        "expression": "mu_X^2=M_X^2/Z_X; lambda_X=1/mu_X=sqrt(Z_X/M_X^2)",
        "derived_relation": "finite real lambda requires Z_X>0 and M_X^2>0 in the same branch",
        "required_parent_inputs": "Z_X;M_X_squared",
        "status": "conditional_exact_relation_derived",
        "valid_for_claim": "false",
    },
    {
        "formula_id": "PR562_3_green_profile",
        "object": "source-normalized exterior field",
        "expression": "X(r)=Q_X^H(lambda_X) exp(-r/lambda_X)/(4*pi*Z_X*r)",
        "derived_relation": "Z_X appears both in the range through canonicalization and in the source amplitude denominator",
        "required_parent_inputs": "Q_X^H(lambda_X);Z_X;lambda_X",
        "status": "conditional_profile_derived",
        "valid_for_claim": "false",
    },
    {
        "formula_id": "PR562_4_prefactor",
        "object": "R10 alpha prefactor",
        "expression": "K_X=s_X/(4*pi*Z_X*G_obs); alpha_X(lambda)=K_X Qbar_XH(lambda) qbar_XT",
        "derived_relation": "sign and Z_X fix the prefactor once numerator coefficients are filled",
        "required_parent_inputs": "s_X;Z_X;G_obs;Qbar_XH;qbar_XT",
        "status": "conditional_prefactor_derived",
        "valid_for_claim": "false",
    },
    {
        "formula_id": "PR562_5_positive_operator_identity",
        "object": "source-free no-hair identity",
        "expression": "int_A [Z_X|grad X|^2+M_X^2 X^2] = int_boundary Z_X X n.gradX + int_A X J_X",
        "derived_relation": "if Z_X>0, M_X^2>0, J_X=0, and boundary term=0 then X=0",
        "required_parent_inputs": "positive operator;zero source;zero boundary flux;regularity;decay",
        "status": "conditional_nohair_identity_written",
        "valid_for_claim": "false",
    },
    {
        "formula_id": "PR562_6_spectral_generalization",
        "object": "memory/nonlocal kernel",
        "expression": "delta a/a_GR=int dlnlambda alpha(lambda)(1+r/lambda)exp(-r/lambda)",
        "derived_relation": "nonlocal memory needs a positive spectral measure or conservative envelope, not a scalar lambda",
        "required_parent_inputs": "spectral density;source normalization;positivity;no-cancellation policy",
        "status": "conditional_extension_only",
        "valid_for_claim": "false",
    },
]


MASS_GAP_GATE_ROWS = [
    {
        "gate_id": "MG562_0_Z_positive",
        "target": "no ghost / elliptic positivity",
        "required_condition": "Z_X>0",
        "derivation_attempt": "read from quadratic parent residue of X kinetic/gradient term",
        "current_status": "not_parent_derived",
        "consequence_if_pass": "operator can be elliptic and canonicalized",
        "consequence_if_fail": "wrong-sign branch rejected for local GR",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "MG562_1_mass_positive",
        "target": "finite stable range",
        "required_condition": "M_X^2>0",
        "derivation_attempt": "read from parent Hessian/potential around local vacuum branch",
        "current_status": "not_parent_derived",
        "consequence_if_pass": "lambda_X=sqrt(Z_X/M_X^2)",
        "consequence_if_fail": "massless/tachyonic branch remains dangerous or rejected",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "MG562_2_source_free",
        "target": "theorem-zero no-hair source premise",
        "required_condition": "J_X=0 and Q_X^H(lambda)=0",
        "derivation_attempt": "use 561 source/test/projection zero gate",
        "current_status": "failed_current_claim",
        "consequence_if_pass": "positive operator can force X=0 with zero boundary flux",
        "consequence_if_fail": "finite-range Yukawa curve is retained",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "MG562_3_boundary_flux_zero",
        "target": "no inner/outer boundary charge",
        "required_condition": "int_boundary Z_X X n.gradX=0",
        "derivation_attempt": "regular compact source, decaying infinity, and zero class/domain/projector flux",
        "current_status": "not_parent_derived",
        "consequence_if_pass": "energy identity can close source-free no-hair",
        "consequence_if_fail": "boundary charge contributes to Q_X^H(lambda)",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "MG562_4_canonical_lambda",
        "target": "numeric or symbolic lambda row",
        "required_condition": "lambda_X=sqrt(Z_X/M_X^2) with units meters",
        "derivation_attempt": "canonicalize the static operator",
        "current_status": "relation_derived_values_missing",
        "consequence_if_pass": "lambda column can be filled",
        "consequence_if_fail": "R10 curve remains placeholder",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "MG562_5_prefactor_units",
        "target": "dimensionless alpha",
        "required_condition": "K_X Qbar_XH qbar_XT dimensionless",
        "derivation_attempt": "define K_X=s_X/(4*pi*Z_X*G_obs)",
        "current_status": "relation_derived_units_missing",
        "consequence_if_pass": "alpha_predicted can be computed after numerator fill",
        "consequence_if_fail": "alpha row cannot be scored",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "MG562_6_bound_curve",
        "target": "empirical R10 comparison",
        "required_condition": "digitized alpha_bound(lambda) rows in same convention",
        "derivation_attempt": "audit current local bound files",
        "current_status": "missing_real_bound_curve",
        "consequence_if_pass": "runner can compare abs(alpha_predicted)<=alpha_bound",
        "consequence_if_fail": "R10 remains not evaluable even with symbolic MTS formula",
        "valid_for_claim": "false",
    },
]


NOHAIR_IDENTITY_ROWS = [
    {
        "step_id": "NH562_0_start",
        "claim": "positive mass-gap branch alone gives no local fifth force",
        "mathematical_form": "Z_X>0;M_X^2>0",
        "result": "insufficient",
        "reason": "positivity gives a decaying Green function, not zero source charge",
        "repair": "add J_X=0, Q_X=0, boundary_flux=0, and projection/test-charge zero theorem",
        "valid_for_claim": "false",
    },
    {
        "step_id": "NH562_1_energy_identity",
        "claim": "source-free positive operator with zero boundary flux forces X=0",
        "mathematical_form": "int_A[Z_X|gradX|^2+M_X^2X^2]=0",
        "result": "conditional_theorem",
        "reason": "follows only when right-hand source and boundary terms vanish",
        "repair": "parent-sign every premise",
        "valid_for_claim": "false",
    },
    {
        "step_id": "NH562_2_compact_source_inner_boundary",
        "claim": "compact source exterior automatically has zero inner boundary term",
        "mathematical_form": "int_inner Z_X X n.gradX=0",
        "result": "not_derived",
        "reason": "inner boundary encodes Q_X^H(lambda) unless source/projection silence is proved",
        "repair": "derive zero source monopole or include Q_X in alpha curve",
        "valid_for_claim": "false",
    },
    {
        "step_id": "NH562_3_massless_limit",
        "claim": "M_X^2=0 is safe if source is universal",
        "mathematical_form": "-Z_X Delta X=J_X",
        "result": "danger_branch",
        "reason": "gives long-range 1/r force or GM calibration only under stronger derivative-silence theorem",
        "repair": "prove exact gauge/universal constant branch or reject for local GR",
        "valid_for_claim": "false",
    },
    {
        "step_id": "NH562_4_wrong_sign_limit",
        "claim": "Z_X<0 or M_X^2<0 can be screened later",
        "mathematical_form": "(-Z_X Delta + M_X^2) not positive",
        "result": "reject_for_local_branch",
        "reason": "ghost/tachyonic/growing exterior mode is incompatible with the clean local-GR route",
        "repair": "derive healthy sign or demote branch",
        "valid_for_claim": "false",
    },
    {
        "step_id": "NH562_5_verdict",
        "claim": "R10 can be theorem-zero at 562",
        "mathematical_form": "positive operator + zero source + zero boundary + zero numerator",
        "result": "fail_current_claim",
        "reason": "operator signs, parent values, source silence, and boundary flux are not all signed",
        "repair": "retain alpha(lambda) coefficient branch and obtain real bound curve",
        "valid_for_claim": "false",
    },
]


BOUND_CURVE_CONTRACT_ROWS = [
    {
        "contract_id": "BC562_0_current_manifest",
        "artifact": "source-intake/local_bounds/local_bound_claims.csv",
        "required_content": "R10 bound source names and convention",
        "current_status": "symbolic_alpha_lambda_only",
        "repair": "digitize/source machine-readable lambda, alpha_bound rows",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "BC562_1_bound_curve_file",
        "artifact": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "required_content": "positive numeric lambda_value, lambda_units, alpha_bound, source, method, claim flag",
        "current_status": "placeholder_rows_only",
        "repair": "replace placeholders with sourced rows and conservative interpolation policy",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "BC562_2_MTS_curve_file",
        "artifact": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv",
        "required_content": "lambda_X, alpha_predicted, source file, assumptions, valid_for_claim after derivation",
        "current_status": "placeholder_rows_only",
        "repair": "fill from K_X Qbar_XH qbar_XT once parent values exist",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "BC562_3_comparison_rule",
        "artifact": "scripts/R10_alpha_lambda_bound_prediction_runner.py",
        "required_content": "abs(alpha_predicted(lambda)) <= alpha_bound(lambda)",
        "current_status": "runner_available_and_blocks_placeholders",
        "repair": "rerun after both curve files have valid rows",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "BC562_4_no_online_claim",
        "artifact": "future data acquisition",
        "required_content": "source URL/DOI, extraction/digitization method, units, interpolation, date, uncertainty/caveat",
        "current_status": "not_attempted_in_derivation_checkpoint",
        "repair": "perform a separate real-data acquisition pass before any R10 scoring",
        "valid_for_claim": "false",
    },
]


ALPHA_ROW_TEMPLATE = [
    {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "R10_ZX_lambda_prefactor_branch",
        "curve_id": "R10_alpha_lambda_curve_MTS_source_normalization",
        "lambda_value": "MISSING_lambda_X=sqrt(Z_X/M_X_squared)",
        "lambda_units": "m",
        "alpha_predicted": "s_X*Qbar_XH(lambda_X)*qbar_XT/(4*pi*Z_X*G_obs)",
        "alpha_bound": "MISSING_DIGITIZED_ALPHA_BOUND",
        "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "force_law_form": "Yukawa_potential_and_acceleration_ratio",
        "derivation_status": "prefactor_range_template_not_numeric",
        "formula_reference": "562-Y5-R10-ZX-lambda-mass-gap-and-bound-curve-fill-or-theorem-zero.md",
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_ZX_LAMBDA_PREFACtOR_FORMULA_REGISTER.csv",
        "assumptions": "Z_X>0;M_X_squared>0;same-frame G_obs;no cancellation;bound convention matches R10 runner",
        "valid_for_claim": "false",
        "notes": "template only; requires parent-derived Z_X, M_X_squared, numerator coefficients, and real bound rows",
    }
]


EVALUATOR_ROWS = [
    {
        "gate_id": "E562_0_lambda_relation",
        "gate": "derive lambda from quadratic operator",
        "result": "conditional_pass",
        "detail": "lambda_X=sqrt(Z_X/M_X^2) after canonicalizing (-Z_X Delta+M_X^2)X=J_X",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "E562_1_prefactor_relation",
        "gate": "derive alpha prefactor",
        "result": "conditional_pass",
        "detail": "K_X=s_X/(4*pi*Z_X*G_obs) and alpha=K_X Qbar_XH qbar_XT",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "E562_2_ZX_value",
        "gate": "parent-derived Z_X",
        "result": "fail_current_claim",
        "detail": "kinetic/operator residue is not parent-owned as a numeric/signed value",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "E562_3_mass_gap_value",
        "gate": "parent-derived M_X^2 and lambda_X",
        "result": "fail_current_claim",
        "detail": "mass gap/range is not parent-owned as a numeric/signed value",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "E562_4_theorem_zero",
        "gate": "positive-operator no-hair theorem-zero",
        "result": "fail_current_claim",
        "detail": "zero source, zero boundary flux, and numerator zero premises are not signed",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "E562_5_bound_curve",
        "gate": "real alpha_bound(lambda) rows",
        "result": "fail_current_claim",
        "detail": "bound curve remains placeholder/symbolic",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "E562_6_R10_status",
        "gate": "R10/fifth-force pass",
        "result": "fail_current_claim",
        "detail": "runner still blocks placeholders; no numeric MTS or bound rows",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "E562_7_local_GR_status",
        "gate": "Newton/PPN/local-GR promotion",
        "result": "fail_current_claim",
        "detail": "R10 plus Cextra/radial/source-measure gates remain open",
        "valid_for_claim": "false",
    },
]


OBSTRUCTION_ROWS = [
    {
        "obstruction_id": "O562_0_ZX_missing",
        "blocked_object": "K_X and operator positivity",
        "reason": "Z_X sign/value not derived from parent quadratic action",
        "repair": "derive parent Hessian/kinetic residue for X",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "O562_1_MX_missing",
        "blocked_object": "lambda_X",
        "reason": "M_X^2 sign/value not derived from parent local vacuum",
        "repair": "derive second variation/potential curvature or spectral range",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "O562_2_nohair_premises_open",
        "blocked_object": "theorem-zero R10 branch",
        "reason": "source, boundary, and numerator zero premises remain unproved",
        "repair": "prove J_X=0, boundary_flux=0, q_test/projection zero, or retain curve",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "O562_3_bound_curve_missing",
        "blocked_object": "empirical R10 score",
        "reason": "alpha_bound(lambda) file is still placeholder data",
        "repair": "separate real-data acquisition/digitization pass",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "O562_4_MTS_curve_missing",
        "blocked_object": "alpha_predicted(lambda)",
        "reason": "numerator, Z_X, and lambda_X are not numeric/source-backed",
        "repair": "fill coefficient rows or theorem-zero certificate",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D562_0_lambda_relation_derived",
        "decision": "lambda_relation_written",
        "meaning": "for a stable local quadratic branch lambda_X=sqrt(Z_X/M_X^2)",
        "status": "conditional_progress",
        "next_target": NEXT_TARGET,
    },
    {
        "decision_id": "D562_1_prefactor_relation_derived",
        "decision": "prefactor_relation_written",
        "meaning": "K_X=s_X/(4*pi*Z_X*G_obs), so alpha=K_X Qbar_XH qbar_XT",
        "status": "conditional_progress",
        "next_target": NEXT_TARGET,
    },
    {
        "decision_id": "D562_2_nohair_not_signed",
        "decision": "positive_operator_nohair_failed_current_claim",
        "meaning": "mass gap alone does not zero R10 without zero source and boundary premises",
        "status": "R10_retained",
        "next_target": NEXT_TARGET,
    },
    {
        "decision_id": "D562_3_bound_curve_missing",
        "decision": "real_bound_curve_still_required",
        "meaning": "even a derived MTS alpha needs digitized external alpha_bound(lambda) rows",
        "status": "data_required",
        "next_target": NEXT_TARGET,
    },
    {
        "decision_id": "D562_4_private_no_push",
        "decision": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "status": "safe_private_work",
        "next_target": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "RU562_0_allowed",
        "allowed_after_562": "MTS may cite lambda_X=sqrt(Z_X/M_X^2) and K_X=s_X/(4*pi*Z_X*G_obs) as conditional derivations",
        "forbidden_after_562": "MTS may not claim numeric lambda, theorem-zero, or R10 pass from symbolic Z_X/M_X^2",
        "next_action": NEXT_TARGET,
    },
    {
        "route_id": "RU562_1_allowed",
        "allowed_after_562": "MTS may proceed to real bound-curve acquisition or parent Hessian derivation",
        "forbidden_after_562": "MTS may not compare against symbolic alpha(lambda) bounds",
        "next_action": NEXT_TARGET,
    },
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = list(rows[0].keys()) if rows else []
    for row in rows[1:]:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_shape(path: Path) -> dict[str, Any]:
    rows = read_csv(path)
    columns = list(rows[0].keys()) if rows else []
    return {"path": rel(ROOT / path), "rows": len(rows), "columns": columns}


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in SOURCE_REGISTER:
        source_path = ROOT / row["source_file"]
        rows.append({**row, "exists": source_path.exists()})
    return rows


def count_claim_rows(row_groups: list[list[dict[str, Any]]]) -> int:
    return sum(1 for rows in row_groups for row in rows if str(row.get("valid_for_claim", "")).lower() == "true")


def validation_rows(
    sources: list[dict[str, Any]],
    runner_result: dict[str, Any],
) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    prior_validation = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_561_VALIDATION.csv"))
    prior_fails = [row for row in prior_validation if row.get("result") == "fail"]
    operator_routes = read_csv(Path("runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/bulk_X_operator_routes.csv"))
    source_law = read_csv(Path("runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/source_normalized_force_law.csv"))
    mts_curve = read_csv(MTS_CURVE_PATH)
    bound_curve = read_csv(BOUND_CURVE_PATH)
    runner_status = runner_result["status"]
    claim_rows = count_claim_rows(
        [
            PREF_RANGE_FORMULA_ROWS,
            MASS_GAP_GATE_ROWS,
            NOHAIR_IDENTITY_ROWS,
            BOUND_CURVE_CONTRACT_ROWS,
            ALPHA_ROW_TEMPLATE,
            EVALUATOR_ROWS,
            OBSTRUCTION_ROWS,
        ]
    )

    return [
        {
            "check_id": "V562_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V562_1_prior_561_clean",
            "result": "pass" if len(prior_validation) == 9 and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_validation)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V562_2_operator_routes_loaded",
            "result": "pass" if len(operator_routes) == 6 and len(source_law) == 5 else "fail",
            "detail": f"operator_routes={len(operator_routes)};source_law={len(source_law)}",
        },
        {
            "check_id": "V562_3_lambda_prefactor_relations_written",
            "result": "pass"
            if any(row["formula_id"] == "PR562_2_canonical_mass_and_range" for row in PREF_RANGE_FORMULA_ROWS)
            and any(row["formula_id"] == "PR562_4_prefactor" for row in PREF_RANGE_FORMULA_ROWS)
            else "fail",
            "detail": "lambda_X=sqrt(Z_X/M_X^2);K_X=s_X/(4*pi*Z_X*G_obs)",
        },
        {
            "check_id": "V562_4_nohair_not_overclaimed",
            "result": "pass" if len(NOHAIR_IDENTITY_ROWS) == 6 and all(row["valid_for_claim"] == "false" for row in NOHAIR_IDENTITY_ROWS) else "fail",
            "detail": f"nohair_rows={len(NOHAIR_IDENTITY_ROWS)};claim_rows={sum(row['valid_for_claim']=='true' for row in NOHAIR_IDENTITY_ROWS)}",
        },
        {
            "check_id": "V562_5_bound_contract_written",
            "result": "pass" if len(BOUND_CURVE_CONTRACT_ROWS) == 5 else "fail",
            "detail": f"bound_contract_rows={len(BOUND_CURVE_CONTRACT_ROWS)}",
        },
        {
            "check_id": "V562_6_existing_placeholders_unchanged_as_blockers",
            "result": "pass" if len(mts_curve) == 2 and len(bound_curve) == 2 else "fail",
            "detail": f"mts_curve_rows={len(mts_curve)};bound_curve_rows={len(bound_curve)}",
        },
        {
            "check_id": "V562_7_runner_still_blocks_placeholders",
            "result": "pass" if runner_status.get("valid_mts_rows") == 0 and runner_status.get("valid_bound_rows") == 0 and runner_status.get("R10_pass_for_claim") is False else "fail",
            "detail": f"valid_mts={runner_status.get('valid_mts_rows')};valid_bound={runner_status.get('valid_bound_rows')};R10_pass={runner_status.get('R10_pass_for_claim')}",
        },
        {
            "check_id": "V562_8_no_claim_rows",
            "result": "pass" if claim_rows == 0 else "fail",
            "detail": f"claim_rows={claim_rows}",
        },
        {
            "check_id": "V562_9_no_overclaim",
            "result": "pass",
            "detail": "Z_X_numeric=false;lambda_numeric=false;theorem_zero=false;R10_pass=false;Newton=false;PPN=false;local_GR=false",
        },
    ]


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    for row in rows[1:]:
        for key in row:
            if key not in headers:
                headers.append(key)
    header_line = "| " + " | ".join(headers) + " |"
    separator = "| " + " | ".join(["---"] * len(headers)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(header, "")).replace("|", "\\|") for header in headers) + " |")
    return "\n".join([header_line, separator, *body])


def build_doc(
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, Any]],
    runner_summary: list[dict[str, Any]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 562 - Y5 R10 Z_X, Lambda, Mass-Gap and Bound-Curve Fill or Theorem-Zero

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The next stage does derive something exact, but still conditional:

```text
(-Z_X Delta + M_X^2) X = J_X
mu_X^2 = M_X^2/Z_X
lambda_X = 1/mu_X = sqrt(Z_X/M_X^2)
K_X = s_X/(4*pi*Z_X*G_obs)
alpha_X(lambda_X)=K_X Qbar_XH(lambda_X) qbar_XT.
```

This is the clean prefactor/range law. It tells us exactly how to turn the 561 numerator into an R10 curve if the parent action supplies `Z_X`, `M_X^2`, the numerator coefficients, and a real bound curve.

The attempted theorem-zero route is only conditional:

```text
Z_X>0, M_X^2>0, J_X=0, zero boundary flux
=> X=0.
```

Current corpus status: `Z_X`, `M_X^2`, zero source, zero boundary flux, and real `alpha_bound(lambda)` rows are not all supplied. So mass gap remains a range relation, not a local-GR pass.

## 2. Prefactor / Range Formula Register

{markdown_table(PREF_RANGE_FORMULA_ROWS)}

## 3. Mass-Gap Theorem-Zero Gate

{markdown_table(MASS_GAP_GATE_ROWS)}

## 4. Positive-Operator No-Hair Attempt

{markdown_table(NOHAIR_IDENTITY_ROWS)}

## 5. Real Bound-Curve Contract

{markdown_table(BOUND_CURVE_CONTRACT_ROWS)}

## 6. Alpha Row Template

{markdown_table(ALPHA_ROW_TEMPLATE)}

## 7. Runner Dry-Run Recheck

{markdown_table(runner_summary)}

## 8. Evaluator

{markdown_table(EVALUATOR_ROWS)}

## 9. Obstruction Ledger

{markdown_table(OBSTRUCTION_ROWS)}

## 10. Decision

{markdown_table(DECISION_ROWS)}

## 11. Source Register

{markdown_table(sources)}

## 12. Validation

{markdown_table(validations)}

## 13. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 14. Claim Ceiling

Allowed:

```text
MTS has conditionally derived lambda_X=sqrt(Z_X/M_X^2).
MTS has conditionally derived K_X=s_X/(4*pi*Z_X*G_obs).
MTS has written the positive-operator no-hair identity and its missing premises.
```

Forbidden:

```text
MTS has a numeric lambda_X.
MTS has proved theorem-zero.
MTS has digitized real R10 bound data.
MTS has passed R10/fifth-force, Newton, PPN, Cextra, radial closure, or local GR.
```

## 15. Practical Read

This is not grim; it is the algebra finally becoming engineering. The R10 branch has been reduced to a short checklist:

```text
Z_X,
M_X^2,
Qbar_XH(lambda),
qbar_XT,
alpha_bound(lambda).
```

If source/boundary/numerator zero lands, the branch dies cleanly. If not, the curve is now mechanical:

```text
lambda_X=sqrt(Z_X/M_X^2),
alpha_X=K_X Qbar_XH qbar_XT.
```

The only honest next move is data/action ownership: either derive the parent Hessian values, or acquire real bound rows and run a non-claim smoke comparison.

## 16. Next Target

`{NEXT_TARGET}`

Next: acquire/digitize real `alpha_bound(lambda)` rows and/or fill a first non-claim `alpha_predicted(lambda)` smoke row from any sourced parent coefficient values. If no values exist, the branch remains retained but executable.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-R10-ZX-lambda-mass-gap-and-bound-curve-fill-or-theorem-zero"
    results_dir = run_dir / "results"
    runner_results_dir = results_dir / "runner"
    results_dir.mkdir(parents=True, exist_ok=True)

    runner_result = run_runner(ROOT / MTS_CURVE_PATH, ROOT / BOUND_CURVE_PATH, runner_results_dir)
    runner_status = runner_result["status"]
    runner_summary = [
        {
            "summary_id": "R10_RUNNER_562_RECHECK",
            "runner_results_dir": rel(runner_results_dir),
            "mts_rows": runner_status["mts_rows"],
            "valid_mts_rows": runner_status["valid_mts_rows"],
            "bound_rows": runner_status["bound_rows"],
            "valid_bound_rows": runner_status["valid_bound_rows"],
            "comparison_rows": runner_status["comparison_rows"],
            "passed_rows": runner_status["passed_rows"],
            "blocked_or_failed_rows": runner_status["blocked_or_failed_rows"],
            "R10_pass_for_claim": runner_status["R10_pass_for_claim"],
            "claim_allowed": False,
        }
    ]

    sources = source_rows()
    validations = validation_rows(sources, runner_result)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (PREF_RANGE_FORMULA_PATH, PREF_RANGE_FORMULA_ROWS),
        (MASS_GAP_GATE_PATH, MASS_GAP_GATE_ROWS),
        (NOHAIR_IDENTITY_PATH, NOHAIR_IDENTITY_ROWS),
        (BOUND_CURVE_CONTRACT_PATH, BOUND_CURVE_CONTRACT_ROWS),
        (ALPHA_ROW_TEMPLATE_PATH, ALPHA_ROW_TEMPLATE),
        (EVALUATOR_PATH, EVALUATOR_ROWS),
        (OBSTRUCTION_LEDGER_PATH, OBSTRUCTION_ROWS),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(ROOT / path, rows)
        write_csv(results_dir / path.name, rows)

    doc = build_doc(generated_at_utc, run_dir, sources, runner_summary, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    failed_validations = [row for row in validations if row["result"] == "fail"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "document": str(ROOT / DOC_PATH),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "prefactor_range_formula_register": str(ROOT / PREF_RANGE_FORMULA_PATH),
        "mass_gap_gate": str(ROOT / MASS_GAP_GATE_PATH),
        "nohair_attempt": str(ROOT / NOHAIR_IDENTITY_PATH),
        "bound_curve_contract": str(ROOT / BOUND_CURVE_CONTRACT_PATH),
        "alpha_row_template": str(ROOT / ALPHA_ROW_TEMPLATE_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "failed_validations": failed_validations,
        "lambda_relation_conditionally_derived": True,
        "prefactor_relation_conditionally_derived": True,
        "Z_X_numeric_or_signed": False,
        "M_X_squared_numeric_or_signed": False,
        "lambda_X_numeric": False,
        "positive_operator_nohair_signed": False,
        "real_bound_curve_loaded": False,
        "R10_fifth_force_passed": False,
        "alpha_curve_valid_for_claim": False,
        "Newton_limit_signed": False,
        "PPN_passed": False,
        "local_GR_promoted": False,
        "csv_shapes": [csv_shape(path) for path, _rows in csv_outputs],
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        f"{STATUS}\nfailed_validations={len(failed_validations)}\nnext={NEXT_TARGET}\n",
        encoding="utf-8",
    )
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
