from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "R10-alpha-lambda-executable-curve-contract"
CHECKPOINT_DOC = "437-R10-alpha-lambda-executable-curve-contract.md"
STATUS = "R10_alpha_lambda_executable_curve_contract_written_theorem_zero_or_curve_required_no_R10_pass_no_local_GR_pass"
CLAIM_CEILING = "R10_alpha_lambda_curve_contract_only_no_fifth_force_PPN_EH_Newton_or_local_GR_pass"
NEXT_TARGET = "438-R11-nonEH-coefficient-vector-contract.md"
TEMPLATE_PATH = Path("source-intake/mts_residuals/R10_alpha_lambda_curve_TEMPLATE.csv")


SOURCE_DOCS = [
    {
        "path": "380-bulk-X-mass-gap-source-normalized-force-law.md",
        "role": "bulk X Yukawa force-law options and alpha_X(lambda_X) debt",
    },
    {
        "path": "403-boundary-domain-flux-nohair-numeric-contract.md",
        "role": "boundary/domain/flux no-hair gates and fifth-force hair branch",
    },
    {
        "path": "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
        "role": "local-bound test matrix requiring verified alpha(lambda) curve for R10",
    },
    {
        "path": "428-MTS-local-residual-vector-input-contract.md",
        "role": "R10 residual vector input contract and symbolic curve comparison rule",
    },
    {
        "path": "431-MTS-local-residual-vector-evaluator.md",
        "role": "local residual evaluator that blocks missing R10 curve files",
    },
    {
        "path": "434-measured-GM-mu-extra-zero-route.md",
        "role": "measured mu decomposition showing finite-range/radial hair channels",
    },
    {
        "path": "435-exterior-extra-source-nohair-owner-gate.md",
        "role": "exterior extra-source owners and bulk X theorem-zero fork",
    },
    {
        "path": "436-auxiliary-projector-local-Euler-equation-ledger.md",
        "role": "C1 Euler ledger routing A0/A6/A7/A8 into R10",
    },
    {
        "path": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "R10 empirical row declaring alpha(lambda) symbolic and unscored",
    },
    {
        "path": "source-intake/mts_residuals/MTS_local_residual_predictions_TEMPLATE.csv",
        "role": "MTS residual template requiring curve_or_vector_file for R10",
    },
    {
        "path": "runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/bulk_X_operator_routes.csv",
        "role": "machine-readable bulk X operator route table",
    },
    {
        "path": "runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/source_normalized_force_law.csv",
        "role": "source-normalized Yukawa alpha/lambda force-law ledger",
    },
    {
        "path": "runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/gate_results.csv",
        "role": "bulk X force-law gates showing alpha(lambda) not parent-derived",
    },
    {
        "path": "runs/20260602-085500-EH-operator-retained-ledger-and-source-normalization-test-plan/results/local_bound_test_matrix.csv",
        "role": "local bound matrix row requiring R10 curve",
    },
    {
        "path": "runs/20260602-094500-MTS-local-residual-vector-input-contract/results/residual_components.csv",
        "role": "R10 residual component contract",
    },
    {
        "path": "runs/20260602-105000-MTS-local-residual-vector-evaluator/results/gate_results.csv",
        "role": "evaluator symbolic-file missing gate for R10",
    },
    {
        "path": "runs/20260602-120000-measured-GM-mu-extra-zero-route/results/mu_extra_decomposition.csv",
        "role": "mu_extra channels that can induce radial/fifth-force residuals",
    },
    {
        "path": "runs/20260602-123000-auxiliary-projector-local-Euler-equation-ledger/results/Euler_ledger_rows.csv",
        "role": "A0/A6/A7/A8 Euler rows feeding R10",
    },
]


R10_CONTRACT_CHAIN = [
    {
        "step": 1,
        "contract": "R10 is a range-dependent inverse-square/fifth-force test, not a scalar local residual.",
        "required_object": "alpha(lambda) curve or theorem-zero derivation",
        "current_status": "symbolic_curve_required",
        "failure_if_missing": "no_R10_pass",
    },
    {
        "step": 2,
        "contract": "The accepted Yukawa convention must be explicit before comparison.",
        "required_object": "V(r)=-G m1 m2/r [1+alpha(lambda) exp(-r/lambda)]",
        "current_status": "convention_written",
        "failure_if_missing": "formula_ambiguous",
    },
    {
        "step": 3,
        "contract": "The acceleration residual must use the same convention as the bound curve.",
        "required_object": "a_extra/a_GR = alpha(lambda) (1+r/lambda) exp(-r/lambda)",
        "current_status": "convention_written",
        "failure_if_missing": "curve_not_comparable",
    },
    {
        "step": 4,
        "contract": "A non-Yukawa retained force must be conservatively mapped to a Yukawa-equivalent envelope.",
        "required_object": "alpha_envelope(lambda) over the declared comparison range",
        "current_status": "contract_only_no_envelope_supplied",
        "failure_if_missing": "non_yukawa_symbolic_block",
    },
    {
        "step": 5,
        "contract": "Theorem-zero can replace a curve only if the finite-range source is absent, gauge/topological, screened, or no-haired by a parent proof.",
        "required_object": "source-free positive operator/gauge identity/screening/no-hair derivation",
        "current_status": "not_derived",
        "failure_if_missing": "theorem_zero_not_available",
    },
    {
        "step": 6,
        "contract": "A constant universal monopole may be absorbed into measured GM only if it is range/species/time independent.",
        "required_object": "source-normalized calibration proof",
        "current_status": "conditional_not_supplied",
        "failure_if_missing": "GM_absorption_not_allowed",
    },
    {
        "step": 7,
        "contract": "Every curve row must carry derivation status, source path, formula reference, assumptions, and valid_for_claim flag.",
        "required_object": "executable CSV with declared columns",
        "current_status": "template_written_only",
        "failure_if_missing": "curve_file_invalid",
    },
    {
        "step": 8,
        "contract": "Until a theorem-zero proof or real curve exists, R10 remains symbolic and blocks fifth-force/local-GR promotion.",
        "required_object": "no promotion from placeholders",
        "current_status": "enforced",
        "failure_if_missing": "false_local_GR_pass",
    },
]


FORCE_LAW_FORMS = [
    {
        "form_id": "Yukawa_potential",
        "mathematical_form": "V(r) = -G m1 m2/r [1 + alpha(lambda) exp(-r/lambda)]",
        "alpha_meaning": "dimensionless strength relative to Newtonian gravity at the same source/test normalization",
        "lambda_meaning": "finite interaction range",
        "accepted_for_R10": True,
        "notes": "directly comparable when alpha_bound(lambda) uses the same convention",
    },
    {
        "form_id": "Yukawa_acceleration_ratio",
        "mathematical_form": "a_extra/a_GR = alpha(lambda) (1 + r/lambda) exp(-r/lambda)",
        "alpha_meaning": "same alpha as potential convention",
        "lambda_meaning": "finite interaction range",
        "accepted_for_R10": True,
        "notes": "needed when MTS branch predicts acceleration rather than potential",
    },
    {
        "form_id": "bulk_X_static_green_function",
        "mathematical_form": "(-Delta + m_X^2) X = q_X rho_source; X(r)=Q_X exp(-r/lambda_X)/(4 pi r); lambda_X=1/m_X",
        "alpha_meaning": "source-normalized product of source and test charges relative to measured G",
        "lambda_meaning": "inverse positive mass gap",
        "accepted_for_R10": True,
        "notes": "accepted only if q_X, Q_X, test charge, sign, and normalization are derived",
    },
    {
        "form_id": "non_yukawa_envelope",
        "mathematical_form": "alpha_envelope(lambda) >= max_range |a_extra/a_GR mapped to Yukawa-equivalent bound convention|",
        "alpha_meaning": "conservative executable envelope",
        "lambda_meaning": "comparison scale used by external alpha(lambda) bound",
        "accepted_for_R10": True,
        "notes": "allowed only as an explicit conservative map; symbolic text does not pass",
    },
]


ALPHA_LAMBDA_CURVE_SCHEMA = [
    {
        "column": "model_id",
        "meaning": "MTS model/family label",
        "required": True,
        "example": "MTS_branch_name",
    },
    {
        "column": "branch_id",
        "meaning": "specific derivation or parameter branch",
        "required": True,
        "example": "fill_branch_id",
    },
    {
        "column": "curve_id",
        "meaning": "unique curve identifier for R10",
        "required": True,
        "example": "R10_alpha_lambda_curve",
    },
    {
        "column": "lambda_value",
        "meaning": "interaction range value",
        "required": True,
        "example": "fill_numeric_lambda",
    },
    {
        "column": "lambda_units",
        "meaning": "units for lambda_value",
        "required": True,
        "example": "m",
    },
    {
        "column": "alpha_predicted",
        "meaning": "dimensionless predicted or envelope fifth-force strength",
        "required": True,
        "example": "fill_numeric_alpha_predicted",
    },
    {
        "column": "alpha_bound",
        "meaning": "dimensionless external upper bound at matching lambda",
        "required": True,
        "example": "fill_numeric_alpha_bound",
    },
    {
        "column": "alpha_bound_source",
        "meaning": "reference path or URL for bound curve",
        "required": True,
        "example": "Adelberger_Heckel_Nelson_2003_ISL_curve",
    },
    {
        "column": "force_law_form",
        "meaning": "Yukawa_potential, Yukawa_acceleration_ratio, bulk_X_static_green_function, or non_yukawa_envelope",
        "required": True,
        "example": "Yukawa_potential",
    },
    {
        "column": "derivation_status",
        "meaning": "derived_zero, derived_bound, fitted, phenomenological, closure_assumed, or speculative",
        "required": True,
        "example": "fill_derivation_status",
    },
    {
        "column": "formula_reference",
        "meaning": "file or equation source for alpha_predicted(lambda)",
        "required": True,
        "example": "fill_formula_reference",
    },
    {
        "column": "source_file",
        "meaning": "source derivation or run artifact supplying the row",
        "required": True,
        "example": "fill_source_file",
    },
    {
        "column": "assumptions",
        "meaning": "source normalization, exterior, matter-frame, and range assumptions",
        "required": True,
        "example": "fill_assumptions",
    },
    {
        "column": "valid_for_claim",
        "meaning": "true only after the row is real data, not a placeholder",
        "required": True,
        "example": "false",
    },
    {
        "column": "notes",
        "meaning": "comparison caveats and interpolation notes",
        "required": False,
        "example": "no scalar placeholder pass",
    },
]


CURVE_COMPARISON_RULES = [
    {
        "rule_id": "C10_1_units",
        "rule": "Convert every lambda_value into the bound-curve units before interpolation.",
        "pass_condition": "lambda units declared and conversion unambiguous",
        "current_status": "template_only",
    },
    {
        "rule_id": "C10_2_bound_match",
        "rule": "Compare alpha_predicted(lambda) against alpha_bound(lambda) at every supplied row.",
        "pass_condition": "abs(alpha_predicted) <= alpha_bound for all rows unless signed bounds are explicitly supplied",
        "current_status": "no_real_curve_supplied",
    },
    {
        "rule_id": "C10_3_interpolation",
        "rule": "Use conservative interpolation or a denser supplied curve across the declared lambda range.",
        "pass_condition": "no unsampled peak can exceed the bound between rows",
        "current_status": "not_yet_applicable",
    },
    {
        "rule_id": "C10_4_non_yukawa",
        "rule": "For non-Yukawa forces, compare only after a conservative alpha_envelope(lambda) map is supplied.",
        "pass_condition": "envelope is executable and source-normalized",
        "current_status": "not_supplied",
    },
    {
        "rule_id": "C10_5_claim_flag",
        "rule": "Rows with valid_for_claim=false are documentation templates only.",
        "pass_condition": "scorer ignores templates and placeholders",
        "current_status": "enforced",
    },
]


THEOREM_ZERO_ROUTES = [
    {
        "route_id": "R10_Z0_absent_source",
        "required_derivation": "show the finite-range field/source coupling is exactly absent in compact ordinary local exteriors",
        "allowed_result": "alpha(lambda)=0",
        "current_status": "not_derived",
    },
    {
        "route_id": "R10_Z1_positive_mass_gap_nohair",
        "required_derivation": "positive elliptic massive operator with source-free exterior, regular boundary data, and decaying solution",
        "allowed_result": "no local Yukawa tail outside calibrated source",
        "current_status": "operator_sign_and_sources_open",
    },
    {
        "route_id": "R10_Z2_gauge_topological",
        "required_derivation": "finite-range-looking variable is pure gauge/topological and has no local stress or matter charge",
        "allowed_result": "no physical fifth-force residual",
        "current_status": "not_derived",
    },
    {
        "route_id": "R10_Z3_screened_local_branch",
        "required_derivation": "screening solution with no composition/time/range leakage and no hidden preferred frame",
        "allowed_result": "alpha(lambda) below bound across the local test range",
        "current_status": "not_supplied",
    },
    {
        "route_id": "R10_Z4_universal_GM_calibration",
        "required_derivation": "constant universal source-normalized monopole independent of range, species, and time",
        "allowed_result": "absorbed into measured GM, not counted as finite-range R10",
        "current_status": "conditional_not_proven",
    },
]


INVALID_R10_INPUTS = [
    {
        "input_type": "single_delta_G_scalar",
        "why_invalid": "R10 is range-dependent; a scalar cannot represent alpha(lambda)",
        "required_repair": "supply curve rows over lambda or theorem-zero proof",
    },
    {
        "input_type": "symbolic_alpha_lambda_text",
        "why_invalid": "a formula without numeric/evaluable rows cannot be scored against a bound curve",
        "required_repair": "emit executable curve or dense sampled envelope",
    },
    {
        "input_type": "mass_gap_without_source_normalization",
        "why_invalid": "lambda alone does not set alpha; source/test charges and measured-G normalization are required",
        "required_repair": "derive q_source, q_test, Q_X, sign, and alpha normalization",
    },
    {
        "input_type": "negative_or_tachyonic_operator_called_screened",
        "why_invalid": "tachyonic or wrong-sign operators do not give the accepted local no-hair route",
        "required_repair": "derive stable positive operator or retain explicit curve",
    },
    {
        "input_type": "boundary_or_domain_hair_absorbed_into_GM",
        "why_invalid": "radial/range/time/species dependent hair is not a constant universal calibration",
        "required_repair": "prove constant universality or score as alpha(lambda)",
    },
    {
        "input_type": "template_row_valid_for_claim",
        "why_invalid": "placeholder rows are scaffolding, not evidence",
        "required_repair": "replace placeholders and set valid_for_claim only after validation",
    },
]


TEMPLATE_ROWS = [
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "curve_id": "R10_alpha_lambda_curve",
        "lambda_value": "fill_numeric_lambda",
        "lambda_units": "m",
        "alpha_predicted": "fill_numeric_alpha_predicted",
        "alpha_bound": "fill_numeric_alpha_bound",
        "alpha_bound_source": "fill_bound_curve_reference_or_file",
        "force_law_form": "Yukawa_potential",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "fill_formula_reference",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_same_frame_source_normalization_exterior_matter_range_assumptions",
        "valid_for_claim": "false",
        "notes": "template row only; no scalar placeholder pass",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "curve_id": "R10_alpha_lambda_curve",
        "lambda_value": "fill_numeric_lambda",
        "lambda_units": "m",
        "alpha_predicted": "fill_numeric_alpha_predicted",
        "alpha_bound": "fill_numeric_alpha_bound",
        "alpha_bound_source": "fill_bound_curve_reference_or_file",
        "force_law_form": "non_yukawa_envelope",
        "derivation_status": "fill: derived_bound/phenomenological/closure_assumed/speculative",
        "formula_reference": "fill_envelope_mapping_reference",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_conservative_envelope_range_and_normalization_assumptions",
        "valid_for_claim": "false",
        "notes": "use only after non-Yukawa force is mapped to executable alpha_envelope(lambda)",
    },
]


GATE_RESULTS_TEMPLATE = [
    {
        "gate": "R10_contract_chain_written",
        "status": "pass",
        "evidence": "8-step theorem-zero-or-curve chain recorded",
    },
    {
        "gate": "force_law_conventions_written",
        "status": "pass",
        "evidence": "Yukawa potential, acceleration ratio, bulk X Green function, and non-Yukawa envelope conventions recorded",
    },
    {
        "gate": "alpha_lambda_schema_written",
        "status": "pass",
        "evidence": "15-column executable curve schema recorded",
    },
    {
        "gate": "R10_template_written",
        "status": "pass",
        "evidence": str(TEMPLATE_PATH),
    },
    {
        "gate": "actual_alpha_lambda_curve_supplied",
        "status": "fail",
        "evidence": "template only; no real alpha_predicted(lambda) branch data supplied",
    },
    {
        "gate": "R10_theorem_zero_derived",
        "status": "fail",
        "evidence": "no absent-source, positive no-hair, gauge/topological, screened, or universal-GM proof supplied",
    },
    {
        "gate": "scalar_placeholder_allowed",
        "status": "fail",
        "evidence": "single scalar delta_G cannot pass R10",
    },
    {
        "gate": "R10_promoted",
        "status": "fail",
        "evidence": "R10 remains symbolic until theorem-zero or executable curve is supplied",
    },
    {
        "gate": "local_GR_promoted",
        "status": "fail",
        "evidence": "fifth-force gate only; no PPN/EH/Newton/local-GR pass",
    },
    {
        "gate": "claim_ceiling_enforced",
        "status": "pass",
        "evidence": CLAIM_CEILING,
    },
]


DECISION = [
    {
        "decision": "R10 is now converted from a vague symbolic fifth-force debt into an executable contract. A branch may pass R10 only by deriving theorem-zero for every finite-range source, or by supplying an alpha(lambda) curve/envelope with explicit units, force-law convention, source normalization, bound source, assumptions, and valid_for_claim=true after validation. The current state is template-only: no theorem-zero proof and no real curve are supplied, so R10 remains symbolic and blocks fifth-force and local-GR promotion.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "438-R11-nonEH-coefficient-vector-contract.md",
        "why_next": "R11 is the sister symbolic row; non-EH operator families need EH-only theorem-zero or executable coefficient vectors",
    },
    {
        "rank": 2,
        "target": "filled R10 alpha(lambda) curve",
        "why_next": "bulk X, L_cg, flux, or domain branches need real curve data before R10 can be scored",
    },
    {
        "rank": 3,
        "target": "local residual scorer curve mode",
        "why_next": "431 can block missing files; next scorer upgrade should parse and evaluate supplied alpha(lambda) rows",
    },
]


def schema_columns() -> list[str]:
    return [row["column"] for row in ALPHA_LAMBDA_CURVE_SCHEMA]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCE_DOCS:
        source_path = ROOT / source["path"]
        rows.append(
            {
                "source_file": source["path"],
                "exists": source_path.exists(),
                "role": source["role"],
            }
        )
    return rows


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    source_gate = {
        "gate": "source_paths_exist",
        "status": "pass" if not missing_sources else "fail",
        "evidence": "all cited source paths exist" if not missing_sources else ";".join(missing_sources),
    }
    template_columns = list(TEMPLATE_ROWS[0].keys())
    expected_columns = schema_columns()
    schema_gate = {
        "gate": "template_schema_matches_contract",
        "status": "pass" if template_columns == expected_columns else "fail",
        "evidence": "template columns match alpha_lambda_curve_schema"
        if template_columns == expected_columns
        else f"template={template_columns}; expected={expected_columns}",
    }
    return [source_gate, schema_gate, *GATE_RESULTS_TEMPLATE]


def write_checkpoint_markdown(run_dir: Path, gate_result_rows: list[dict[str, Any]]) -> None:
    source_rows = source_register_rows()
    text = f"""# 437 - R10 Alpha-Lambda Executable Curve Contract

Private R10/fifth-force checkpoint. This is not a public fifth-force, PPN, Einstein-Hilbert, Newtonian-limit, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 436 routed several retained local branches into R10: bulk X tails, coarse-graining gradients, source-normalization flux, radial hair, boundary/domain hair, and non-EH operator remnants. This checkpoint removes the last loose language around R10: either a branch proves theorem-zero for finite-range forces, or it supplies an executable `alpha(lambda)` curve/envelope that can be compared to the external bound curve.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/R10_alpha_lambda_executable_curve_contract.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Template | `{TEMPLATE_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_rows, ["source_file", "exists", "role"])}

## 4. R10 Contract Chain

{markdown_table(R10_CONTRACT_CHAIN, ["step", "contract", "required_object", "current_status", "failure_if_missing"])}

Core rule:

```text
R10 passes only if one of these exists:

1. theorem-zero:
   alpha(lambda) = 0 by parent-derived absence/gauge/topology/screening/no-hair/calibration proof;

2. executable curve:
   for each lambda_i, supply alpha_predicted(lambda_i), alpha_bound(lambda_i),
   units, force-law convention, source normalization, formula source, assumptions,
   and valid_for_claim=true after validation.

Anything else remains symbolic and blocks R10 promotion.
```

## 5. Accepted Force-Law Forms

{markdown_table(FORCE_LAW_FORMS, ["form_id", "mathematical_form", "alpha_meaning", "lambda_meaning", "accepted_for_R10", "notes"])}

## 6. Alpha-Lambda Curve Schema

{markdown_table(ALPHA_LAMBDA_CURVE_SCHEMA, ["column", "meaning", "required", "example"])}

## 7. Curve Comparison Rules

{markdown_table(CURVE_COMPARISON_RULES, ["rule_id", "rule", "pass_condition", "current_status"])}

## 8. Theorem-Zero Routes

{markdown_table(THEOREM_ZERO_ROUTES, ["route_id", "required_derivation", "allowed_result", "current_status"])}

## 9. Invalid R10 Inputs

{markdown_table(INVALID_R10_INPUTS, ["input_type", "why_invalid", "required_repair"])}

## 10. Template Rows

The reusable template has been written to `{TEMPLATE_PATH}`.

{markdown_table(TEMPLATE_ROWS, schema_columns())}

## 11. Gate Results

{markdown_table(gate_result_rows, ["gate", "status", "evidence"])}

## 12. Decision

{DECISION[0]["decision"]}

Practical read: this is a clean engineering gate. If MTS has no fifth-force locally, prove the no-force theorem. If it has a tiny one, draw the curve. If it cannot draw the curve, it has not beaten the local inverse-square tests yet. No shame, but no free pass.

## 13. Next Queue

{markdown_table(NEXT_QUEUE, ["rank", "target", "why_next"])}
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    gate_result_rows = gate_rows(source_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "R10_contract_chain.csv", R10_CONTRACT_CHAIN)
    write_csv(results_dir / "force_law_forms.csv", FORCE_LAW_FORMS)
    write_csv(results_dir / "alpha_lambda_curve_schema.csv", ALPHA_LAMBDA_CURVE_SCHEMA)
    write_csv(results_dir / "curve_comparison_rules.csv", CURVE_COMPARISON_RULES)
    write_csv(results_dir / "theorem_zero_routes.csv", THEOREM_ZERO_ROUTES)
    write_csv(results_dir / "invalid_R10_inputs.csv", INVALID_R10_INPUTS)
    write_csv(results_dir / "template_rows.csv", TEMPLATE_ROWS, schema_columns())
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)
    write_csv(ROOT / TEMPLATE_PATH, TEMPLATE_ROWS, schema_columns())
    write_csv(results_dir / "R10_alpha_lambda_curve_TEMPLATE.csv", TEMPLATE_ROWS, schema_columns())

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "R10_contract_steps": len(R10_CONTRACT_CHAIN),
        "force_law_forms": len(FORCE_LAW_FORMS),
        "alpha_lambda_schema_columns": len(ALPHA_LAMBDA_CURVE_SCHEMA),
        "curve_comparison_rules": len(CURVE_COMPARISON_RULES),
        "theorem_zero_routes": len(THEOREM_ZERO_ROUTES),
        "invalid_R10_inputs": len(INVALID_R10_INPUTS),
        "template_path": str(ROOT / TEMPLATE_PATH),
        "R10_curve_template_written": True,
        "actual_R10_curve_supplied": False,
        "R10_theorem_zero_derived": False,
        "R10_promoted": False,
        "local_GR_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 437 R10 alpha-lambda executable curve contract artifacts."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()
