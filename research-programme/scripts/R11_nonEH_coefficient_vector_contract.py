from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "R11-nonEH-coefficient-vector-contract"
CHECKPOINT_DOC = "438-R11-nonEH-coefficient-vector-contract.md"
STATUS = "R11_nonEH_coefficient_vector_contract_written_EH_only_or_operator_vector_required_no_R11_pass_no_local_GR_pass"
CLAIM_CEILING = "R11_operator_vector_contract_only_no_EH_PPN_Newton_fifth_force_or_local_GR_pass"
NEXT_TARGET = "439-EH-only-exterior-parent-premise-ladder.md"
TEMPLATE_PATH = Path("source-intake/mts_residuals/R11_nonEH_operator_vector_TEMPLATE.csv")


SOURCE_DOCS = [
    {
        "path": "392-EH-operator-selection-under-identity-closure.md",
        "role": "EH conditional selection and retained non-EH operator ledger",
    },
    {
        "path": "402-EH-source-normalization-parent-pair.md",
        "role": "same-frame EH/source pair and non-EH counterexamples",
    },
    {
        "path": "405-same-frame-EH-source-derived-stack-audit.md",
        "role": "derived-stack audit and no-promotion policy",
    },
    {
        "path": "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
        "role": "canonical retained operator families and affected local rows",
    },
    {
        "path": "428-MTS-local-residual-vector-input-contract.md",
        "role": "R11 residual-vector contract and operator-vector comparison rule",
    },
    {
        "path": "431-MTS-local-residual-vector-evaluator.md",
        "role": "evaluator that blocks symbolic R11 operator placeholders",
    },
    {
        "path": "436-auxiliary-projector-local-Euler-equation-ledger.md",
        "role": "A1/A2/A8 hidden-variable rows feeding R11",
    },
    {
        "path": "437-R10-alpha-lambda-executable-curve-contract.md",
        "role": "sister symbolic-row contract for finite-range force curves",
    },
    {
        "path": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "R11 internal symbolic local-bound row",
    },
    {
        "path": "source-intake/mts_residuals/MTS_local_residual_predictions_TEMPLATE.csv",
        "role": "MTS residual template requiring curve_or_vector_file for R11",
    },
    {
        "path": "runs/20260602-043500-EH-source-normalization-parent-pair/results/same_frame_theorem_pair.csv",
        "role": "same-frame theorem pair and non-EH elimination statement",
    },
    {
        "path": "runs/20260602-043500-EH-source-normalization-parent-pair/results/counterexample_models.csv",
        "role": "counterexamples showing same frame and Bianchi do not imply EH",
    },
    {
        "path": "runs/20260602-085500-EH-operator-retained-ledger-and-source-normalization-test-plan/results/EH_operator_retained_ledger.csv",
        "role": "machine-readable operator family ledger",
    },
    {
        "path": "runs/20260602-085500-EH-operator-retained-ledger-and-source-normalization-test-plan/results/local_bound_test_matrix.csv",
        "role": "R11 symbolic no-pass local-bound test row",
    },
    {
        "path": "runs/20260602-094500-MTS-local-residual-vector-input-contract/results/residual_components.csv",
        "role": "R11 residual component row",
    },
    {
        "path": "runs/20260602-105000-MTS-local-residual-vector-evaluator/results/evaluator_rules.csv",
        "role": "symbolic operator block rule",
    },
    {
        "path": "runs/20260602-123000-auxiliary-projector-local-Euler-equation-ledger/results/Euler_ledger_rows.csv",
        "role": "A1/A2/A8 retained symbolic operator rows",
    },
    {
        "path": "runs/20260602-124500-R10-alpha-lambda-executable-curve-contract/results/gate_results.csv",
        "role": "sister R10 symbolic gate policy",
    },
]


R11_CONTRACT_CHAIN = [
    {
        "step": 1,
        "contract": "R11 is the non-EH operator-family ledger, not a scalar modified-gravity flag.",
        "required_object": "EH-only theorem-zero proof or full c_nonEH operator vector",
        "current_status": "retained_symbolic",
        "failure_if_missing": "no_R11_pass",
    },
    {
        "step": 2,
        "contract": "Same-frame matter closure does not set non-EH coefficients to zero.",
        "required_object": "separate operator-selection proof",
        "current_status": "known_counterexample_guard",
        "failure_if_missing": "false_EH_selection",
    },
    {
        "step": 3,
        "contract": "Bianchi/Ward conservation does not make a conserved non-EH tensor vanish.",
        "required_object": "metric-only local 4D second-order premise or retained coefficients",
        "current_status": "known_counterexample_guard",
        "failure_if_missing": "conservation_used_as_uniqueness",
    },
    {
        "step": 4,
        "contract": "The EH-only route must derive metric-only, local, four-dimensional, second-order exterior dynamics in the observed matter frame.",
        "required_object": "parent-derived Lovelock-style premise stack",
        "current_status": "conditional_not_parent_derived",
        "failure_if_missing": "EH_only_not_available",
    },
    {
        "step": 5,
        "contract": "If EH-only is not derived, every retained family needs a coefficient, units, normalization, operator form, and weak-field map.",
        "required_object": "executable coefficient-vector CSV",
        "current_status": "template_written_only",
        "failure_if_missing": "operator_vector_missing",
    },
    {
        "step": 6,
        "contract": "A nonzero coefficient must map into affected rows R0-R11 before it can be scored or called safe.",
        "required_object": "affected_rows plus induced residual prediction or bound source",
        "current_status": "contract_only_no_real_vector",
        "failure_if_missing": "operator_unmapped",
    },
    {
        "step": 7,
        "contract": "Boundary/topological, torsion, nonmetricity, scalar, vector, bulk, nonlocal, and source-normalization operators each need their own zero/safe condition.",
        "required_object": "family-specific theorem or coefficient row",
        "current_status": "retained",
        "failure_if_missing": "operator_family_hidden",
    },
    {
        "step": 8,
        "contract": "Until theorem-zero or a real coefficient vector exists, R11 blocks EH/local-GR promotion.",
        "required_object": "no promotion from symbolic operator ledgers",
        "current_status": "enforced",
        "failure_if_missing": "false_local_GR_pass",
    },
]


OPERATOR_FAMILIES = [
    {
        "operator_family": "EH_plus_Lambda_baseline",
        "role": "target baseline",
        "operator_form": "sqrt(-g) (R - 2 Lambda)",
        "affected_rows": "R0;R2;R3;R4;R5;R6;R7;R8;R9;R10;R11",
        "zero_or_safe_condition": "baseline only after same-frame, source-normalization, no-hair, and EH-selection premises are parent-derived",
        "current_status": "target_only_not_parent_derived",
    },
    {
        "operator_family": "boundary_topological_terms",
        "role": "possible harmless boundary/topological sector",
        "operator_form": "boundary/class/topological functionals and induced boundary stress",
        "affected_rows": "R3;R4;R7;R8;R11",
        "zero_or_safe_condition": "pure boundary/topological/class-only with no local stress, exchange, shear, radial, or preferred-location hair",
        "current_status": "retained",
    },
    {
        "operator_family": "R2_fR_scalar_mode",
        "role": "higher-curvature scalar mode",
        "operator_form": "sqrt(-g) (c_R2 R^2 + c_fR f_extra(R))",
        "affected_rows": "R3;R4;R10;R11",
        "zero_or_safe_condition": "c_R2/c_fR zero, infinite scalar mass, zero matter coupling, or mapped alpha(lambda)/PPN residual below bounds",
        "current_status": "retained_symbolic",
    },
    {
        "operator_family": "Ricci_Weyl_squared",
        "role": "quadratic tensor/slip sector",
        "operator_form": "sqrt(-g) (c_Ricci R_mn R^mn + c_Weyl C_mnrs C^mnrs)",
        "affected_rows": "R3;R8;R11",
        "zero_or_safe_condition": "coefficient zero, pure topological combination, or weak-field slip/location residual below bounds",
        "current_status": "retained_symbolic",
    },
    {
        "operator_family": "scalar_tensor_class_metric",
        "role": "scalar/class metric modified-gravity sector",
        "operator_form": "sqrt(-g) [F(phi,C) R - 1/2 (nabla phi)^2 - V(phi,C)]",
        "affected_rows": "R2;R3;R4;R9;R10;R11",
        "zero_or_safe_condition": "scalar/class field locally silent or source-normalized residuals mapped below clock, PPN, Gdot, and fifth-force locks",
        "current_status": "retained",
    },
    {
        "operator_family": "vector_preferred_frame",
        "role": "vector/domain/projector preferred-frame sector",
        "operator_form": "c_V V_mu V_nu, projector/domain vector stress, or aether-like terms",
        "affected_rows": "R5;R6;R7;R8;R11",
        "zero_or_safe_condition": "vector is absent, pure gauge, dynamically aligned, or mapped below alpha1/alpha2/alpha3/xi bounds",
        "current_status": "retained",
    },
    {
        "operator_family": "torsion_nonmetricity",
        "role": "connection compatibility sector",
        "operator_form": "c_T T^2 + c_Q Q^2 + matter spin/light-cone connection couplings",
        "affected_rows": "R0;R1;R2;R11",
        "zero_or_safe_condition": "Levi-Civita compatibility theorem or source/light-cone residual map below WEP/clock locks",
        "current_status": "retained_symbolic",
    },
    {
        "operator_family": "bulk_X_force_law",
        "role": "bulk/memory/load auxiliary force-law sector",
        "operator_form": "(-Delta + m_X^2) X = q_X rho_source plus metric/source stress",
        "affected_rows": "R1;R3;R4;R10;R11",
        "zero_or_safe_condition": "positive source-free no-hair or alpha_X(lambda_X) plus PPN/source map below bounds",
        "current_status": "retained",
    },
    {
        "operator_family": "nonlocal_memory_kernel",
        "role": "nonlocal/time-memory kernel sector",
        "operator_form": "integral K(x,x_prime) I[g,fields](x_prime) dV_prime",
        "affected_rows": "R7;R9;R10;R11",
        "zero_or_safe_condition": "local kernel silence/screening or mapped alpha3/Gdot/fifth-force residual below bounds",
        "current_status": "retained",
    },
    {
        "operator_family": "source_normalization_operator",
        "role": "hidden source-charge/G_eff/M_eff operator sector",
        "operator_form": "mu_obs = G_eff M_eff + mu_extra with operator corrections",
        "affected_rows": "R1;R4;R9;R10;R11",
        "zero_or_safe_condition": "constant, conserved, universal, range-independent measured GM or explicit residual map",
        "current_status": "retained_core_blocker",
    },
    {
        "operator_family": "projector_domain_stress",
        "role": "projector/domain/readout stress sector",
        "operator_form": "delta_g P_D, delta_g chi_D, lambda_P constraint stress, or readout-mask backreaction",
        "affected_rows": "R5;R6;R7;R8;R11",
        "zero_or_safe_condition": "covariant topological projector/domain theorem or explicit preferred-frame/location residual map",
        "current_status": "retained_symbolic",
    },
]


COEFFICIENT_VECTOR_SCHEMA = [
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
        "column": "vector_id",
        "meaning": "unique R11 operator-vector identifier",
        "required": True,
        "example": "R11_nonEH_operator_vector",
    },
    {
        "column": "operator_family",
        "meaning": "family name matching the operator-family ledger",
        "required": True,
        "example": "R2_fR_scalar_mode",
    },
    {
        "column": "coefficient_symbol",
        "meaning": "symbol used in the parent/effective action",
        "required": True,
        "example": "c_R2",
    },
    {
        "column": "coefficient_value",
        "meaning": "numeric value, zero with theorem source, or bounded envelope value",
        "required": True,
        "example": "fill_numeric_or_zero",
    },
    {
        "column": "coefficient_units",
        "meaning": "units after declared normalization",
        "required": True,
        "example": "dimensionless_or_length_power",
    },
    {
        "column": "normalization",
        "meaning": "how coefficient is normalized relative to EH, measured G, cutoff, or source units",
        "required": True,
        "example": "relative_to_EH_local_action",
    },
    {
        "column": "operator_form",
        "meaning": "action/equation operator represented by this row",
        "required": True,
        "example": "sqrt(-g) c_R2 R^2",
    },
    {
        "column": "weak_field_map",
        "meaning": "formula or artifact mapping coefficient into local residual rows",
        "required": True,
        "example": "fill_gamma_beta_alpha_lambda_map",
    },
    {
        "column": "affected_rows",
        "meaning": "semicolon-separated R rows affected if this coefficient is not theorem-zero",
        "required": True,
        "example": "R3;R4;R10;R11",
    },
    {
        "column": "induced_observable",
        "meaning": "observable residual, curve, or vector generated by the operator",
        "required": True,
        "example": "gamma_minus_1;beta_minus_1;alpha(lambda)",
    },
    {
        "column": "predicted_residual_or_bound_source",
        "meaning": "numeric residual, bound source, curve file, or downstream map artifact",
        "required": True,
        "example": "fill_residual_or_map_path",
    },
    {
        "column": "derivation_status",
        "meaning": "derived_zero, derived_bound, fitted, phenomenological, closure_assumed, or speculative",
        "required": True,
        "example": "fill_derivation_status",
    },
    {
        "column": "formula_reference",
        "meaning": "file/equation source for coefficient and weak-field map",
        "required": True,
        "example": "fill_formula_reference",
    },
    {
        "column": "source_file",
        "meaning": "source derivation or run artifact supplying this row",
        "required": True,
        "example": "fill_derivation_or_run_path",
    },
    {
        "column": "assumptions",
        "meaning": "frame, locality, source-normalization, boundary, and range assumptions",
        "required": True,
        "example": "fill_operator_assumptions",
    },
    {
        "column": "valid_for_claim",
        "meaning": "true only after row is real data, not a placeholder",
        "required": True,
        "example": "false",
    },
    {
        "column": "notes",
        "meaning": "comparison caveats and unresolved derivation debts",
        "required": False,
        "example": "symbolic operator row cannot pass",
    },
]


VECTOR_COMPARISON_RULES = [
    {
        "rule_id": "C11_1_family_completeness",
        "rule": "The vector must include every retained operator family or a sourced reason why the family is absent.",
        "pass_condition": "all required families are present, theorem-zero, or explicitly not in branch",
        "current_status": "template_only",
    },
    {
        "rule_id": "C11_2_zero_credit",
        "rule": "coefficient_value=0 earns theorem credit only with derivation_status=derived_zero and a real formula/source path.",
        "pass_condition": "zero is derived, not typed as a wish",
        "current_status": "no_theorem_zero_sources_supplied",
    },
    {
        "rule_id": "C11_3_nonzero_mapping",
        "rule": "Every nonzero coefficient must map to affected residual rows before being called safe.",
        "pass_condition": "weak_field_map and predicted_residual_or_bound_source are executable",
        "current_status": "no_real_vector_supplied",
    },
    {
        "rule_id": "C11_4_R10_coupling",
        "rule": "Operators inducing finite-range forces must also supply or reference the R10 alpha(lambda) curve.",
        "pass_condition": "R10 curve exists for all fifth-force inducing families",
        "current_status": "R10_template_only",
    },
    {
        "rule_id": "C11_5_claim_flag",
        "rule": "Rows with valid_for_claim=false are scaffolding only.",
        "pass_condition": "scorer ignores templates and placeholders",
        "current_status": "enforced",
    },
    {
        "rule_id": "C11_6_all_or_retained",
        "rule": "Derived local GR requires all non-EH families theorem-zero or scored below their induced local locks.",
        "pass_condition": "no symbolic operator family remains",
        "current_status": "not_satisfied",
    },
]


THEOREM_ZERO_ROUTES = [
    {
        "route_id": "R11_Z0_Lovelock_metric_only",
        "required_derivation": "parent derives local, four-dimensional, metric-only, second-order exterior equations in the observed matter frame",
        "allowed_result": "EH_plus_Lambda plus harmless boundary/topological terms",
        "current_status": "conditional_not_parent_derived",
    },
    {
        "route_id": "R11_Z1_no_extra_fields",
        "required_derivation": "scalar, vector, bulk, projector, domain, torsion, nonmetricity, and nonlocal variables are absent, pure gauge, or locally source-free no-hair",
        "allowed_result": "corresponding operator coefficients zero or harmless",
        "current_status": "not_derived",
    },
    {
        "route_id": "R11_Z2_topological_boundary_only",
        "required_derivation": "boundary/class terms are topological or pure boundary with no local stress, exchange, radial hair, or preferred-location signal",
        "allowed_result": "boundary/topological rows removed from local residual vector",
        "current_status": "not_derived",
    },
    {
        "route_id": "R11_Z3_metric_compatibility",
        "required_derivation": "local observed connection is Levi-Civita and all matter/light/spin couplings use it universally",
        "allowed_result": "torsion/nonmetricity coefficients zero",
        "current_status": "not_parent_derived",
    },
    {
        "route_id": "R11_Z4_source_normalization_constant",
        "required_derivation": "measured GM is constant, conserved, universal, and range independent with mu_extra=0",
        "allowed_result": "source-normalization operator harmless",
        "current_status": "conditional_not_proven",
    },
    {
        "route_id": "R11_Z5_coefficient_vector_empirical",
        "required_derivation": "not a theorem-zero route: supply executable coefficient vector and induced residual maps below bounds",
        "allowed_result": "empirical retained-branch viability only, not derived local GR",
        "current_status": "template_only",
    },
]


INVALID_R11_INPUTS = [
    {
        "input_type": "single_nonEH_scalar",
        "why_invalid": "R11 is an operator-family vector; one scalar cannot represent all non-EH channels",
        "required_repair": "supply full family vector or theorem-zero proof",
    },
    {
        "input_type": "Bianchi_conserved_means_EH",
        "why_invalid": "conserved non-EH tensors exist, so conservation is not uniqueness",
        "required_repair": "derive metric-only local 4D second-order exterior or retain coefficients",
    },
    {
        "input_type": "same_frame_matter_means_EH",
        "why_invalid": "same matter frame can still be scalar-tensor, f(R), vector, or nonlocal gravity",
        "required_repair": "separate same-frame theorem from operator-selection theorem",
    },
    {
        "input_type": "EFT_small_without_scale_or_map",
        "why_invalid": "small-looking coefficients need units, cutoff/normalization, and local residual maps",
        "required_repair": "declare normalization and compute induced R rows",
    },
    {
        "input_type": "boundary_topological_assumed_harmless",
        "why_invalid": "boundary terms can leave local radial/shear/exchange hair unless proven harmless",
        "required_repair": "prove class-only/topological no-hair or retain coefficients",
    },
    {
        "input_type": "torsion_nonmetricity_ignored",
        "why_invalid": "connection residues can affect WEP, clocks, spin, and light cones",
        "required_repair": "derive Levi-Civita compatibility or include rows",
    },
    {
        "input_type": "R10_inducing_operator_without_curve",
        "why_invalid": "R2/f(R), scalar, bulk, source, and nonlocal families can induce finite-range forces",
        "required_repair": "reference a valid R10 alpha(lambda) curve or theorem-zero proof",
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
        "vector_id": "R11_nonEH_operator_vector",
        "operator_family": family["operator_family"],
        "coefficient_symbol": f"fill_coefficient_for_{family['operator_family']}",
        "coefficient_value": "fill_numeric_or_zero",
        "coefficient_units": "fill_units_after_normalization",
        "normalization": "fill_relative_to_EH_measured_G_cutoff_or_source_units",
        "operator_form": family["operator_form"],
        "weak_field_map": "fill_formula_or_run_artifact_mapping_to_R_rows",
        "affected_rows": family["affected_rows"],
        "induced_observable": "fill_observable_residuals_or_curve_names",
        "predicted_residual_or_bound_source": "fill_numeric_residual_bound_or_map_path",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "fill_formula_reference",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_same_frame_locality_boundary_source_normalization_range_assumptions",
        "valid_for_claim": "false",
        "notes": f"template only; {family['current_status']}; {family['zero_or_safe_condition']}",
    }
    for family in OPERATOR_FAMILIES
    if family["operator_family"] != "EH_plus_Lambda_baseline"
]


GATE_RESULTS_TEMPLATE = [
    {
        "gate": "R11_contract_chain_written",
        "status": "pass",
        "evidence": "8-step EH-only-or-vector chain recorded",
    },
    {
        "gate": "operator_families_written",
        "status": "pass",
        "evidence": "11 operator families recorded including EH baseline and retained non-EH families",
    },
    {
        "gate": "coefficient_vector_schema_written",
        "status": "pass",
        "evidence": "19-column executable operator-vector schema recorded",
    },
    {
        "gate": "R11_template_written",
        "status": "pass",
        "evidence": str(TEMPLATE_PATH),
    },
    {
        "gate": "actual_operator_vector_supplied",
        "status": "fail",
        "evidence": "template only; no real c_nonEH branch vector supplied",
    },
    {
        "gate": "EH_only_theorem_zero_derived",
        "status": "fail",
        "evidence": "metric-only local 4D second-order exterior remains conditional, not parent-derived",
    },
    {
        "gate": "symbolic_operator_placeholder_allowed",
        "status": "fail",
        "evidence": "symbolic non-EH ledger cannot pass R11",
    },
    {
        "gate": "R11_promoted",
        "status": "fail",
        "evidence": "R11 remains symbolic until EH-only theorem-zero or executable coefficient vector is supplied",
    },
    {
        "gate": "local_GR_promoted",
        "status": "fail",
        "evidence": "operator-vector gate only; no EH/Newton/PPN/fifth-force/local-GR pass",
    },
    {
        "gate": "claim_ceiling_enforced",
        "status": "pass",
        "evidence": CLAIM_CEILING,
    },
]


DECISION = [
    {
        "decision": "R11 is now converted from a symbolic non-EH operator ledger into an executable coefficient-vector contract. A branch may clear R11 only by deriving the EH-only exterior premise stack from the parent action, or by supplying a complete c_nonEH operator-family vector with coefficients, units, normalization, operator forms, weak-field maps, affected residual rows, assumptions, and valid_for_claim=true after validation. The current state is template-only: no EH-only parent theorem and no real coefficient vector are supplied, so R11 remains symbolic and blocks EH/local-GR promotion.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "439-EH-only-exterior-parent-premise-ladder.md",
        "why_next": "R11's theorem-zero route requires deriving metric-only local 4D second-order exterior dynamics rather than assuming them",
    },
    {
        "rank": 2,
        "target": "filled R11 nonEH operator vector",
        "why_next": "if EH-only cannot yet be derived, retained branches need real coefficients and weak-field maps",
    },
    {
        "rank": 3,
        "target": "local residual scorer curve/vector mode",
        "why_next": "431 blocks symbolic files; next scorer upgrade should parse R10 curves and R11 vectors",
    },
]


def schema_columns() -> list[str]:
    return [row["column"] for row in COEFFICIENT_VECTOR_SCHEMA]


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
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
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
        "evidence": "template columns match coefficient_vector_schema"
        if template_columns == expected_columns
        else f"template={template_columns}; expected={expected_columns}",
    }
    family_gate = {
        "gate": "template_covers_retained_nonEH_families",
        "status": "pass" if len(TEMPLATE_ROWS) == len(OPERATOR_FAMILIES) - 1 else "fail",
        "evidence": f"{len(TEMPLATE_ROWS)} retained template rows for {len(OPERATOR_FAMILIES) - 1} non-EH families",
    }
    return [source_gate, schema_gate, family_gate, *GATE_RESULTS_TEMPLATE]


def write_checkpoint_markdown(run_dir: Path, gate_result_rows: list[dict[str, Any]]) -> None:
    source_rows = source_register_rows()
    text = f"""# 438 - R11 Non-EH Coefficient-Vector Contract

Private R11/EH-operator checkpoint. This is not a public Einstein-Hilbert, PPN, Newtonian-limit, fifth-force, cosmology, local-GR, or unified-field claim.

## 1. Purpose

Checkpoint 437 made R10 executable: prove no fifth force or supply an `alpha(lambda)` curve. This checkpoint does the same for R11. The phrase "non-EH operator ledger" is no longer allowed to float around as a symbolic fog bank. Either MTS derives the EH-only exterior premise stack, or it supplies a coefficient vector for every retained non-EH operator family and maps those coefficients into local residual rows.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/R11_nonEH_coefficient_vector_contract.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Template | `{TEMPLATE_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_rows, ["source_file", "exists", "role"])}

## 4. R11 Contract Chain

{markdown_table(R11_CONTRACT_CHAIN, ["step", "contract", "required_object", "current_status", "failure_if_missing"])}

Core rule:

```text
R11 passes only if one of these exists:

1. EH-only theorem-zero:
   the parent action derives a local, 4D, metric-only, second-order exterior
   in the observed matter frame, with all extra fields/hair/source operators
   absent, pure gauge/topological, or harmless;

2. executable coefficient vector:
   every retained non-EH operator family has coefficient, units, normalization,
   operator form, weak-field map, affected rows, source, assumptions,
   and valid_for_claim=true after validation.

Anything else remains symbolic and blocks EH/local-GR promotion.
```

## 5. Operator Families

{markdown_table(OPERATOR_FAMILIES, ["operator_family", "role", "affected_rows", "zero_or_safe_condition", "current_status"])}

## 6. Coefficient-Vector Schema

{markdown_table(COEFFICIENT_VECTOR_SCHEMA, ["column", "meaning", "required", "example"])}

## 7. Vector Comparison Rules

{markdown_table(VECTOR_COMPARISON_RULES, ["rule_id", "rule", "pass_condition", "current_status"])}

## 8. Theorem-Zero Routes

{markdown_table(THEOREM_ZERO_ROUTES, ["route_id", "required_derivation", "allowed_result", "current_status"])}

## 9. Invalid R11 Inputs

{markdown_table(INVALID_R11_INPUTS, ["input_type", "why_invalid", "required_repair"])}

## 10. Template Rows

The reusable template has been written to `{TEMPLATE_PATH}`.

{markdown_table(TEMPLATE_ROWS, schema_columns())}

## 11. Gate Results

{markdown_table(gate_result_rows, ["gate", "status", "evidence"])}

## 12. Decision

{DECISION[0]["decision"]}

Practical read: this is the GR bridge with the lights turned on. If MTS really reduces to GR locally, the non-EH coefficients must disappear for a reason. If they do not disappear, they have to step into the ring as measured residuals. No hidden judges, no symbolic smoke machine.

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
    write_csv(results_dir / "R11_contract_chain.csv", R11_CONTRACT_CHAIN)
    write_csv(results_dir / "operator_families.csv", OPERATOR_FAMILIES)
    write_csv(results_dir / "coefficient_vector_schema.csv", COEFFICIENT_VECTOR_SCHEMA)
    write_csv(results_dir / "vector_comparison_rules.csv", VECTOR_COMPARISON_RULES)
    write_csv(results_dir / "theorem_zero_routes.csv", THEOREM_ZERO_ROUTES)
    write_csv(results_dir / "invalid_R11_inputs.csv", INVALID_R11_INPUTS)
    write_csv(results_dir / "template_rows.csv", TEMPLATE_ROWS, schema_columns())
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)
    write_csv(ROOT / TEMPLATE_PATH, TEMPLATE_ROWS, schema_columns())
    write_csv(results_dir / "R11_nonEH_operator_vector_TEMPLATE.csv", TEMPLATE_ROWS, schema_columns())

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "R11_contract_steps": len(R11_CONTRACT_CHAIN),
        "operator_families": len(OPERATOR_FAMILIES),
        "retained_template_rows": len(TEMPLATE_ROWS),
        "coefficient_vector_schema_columns": len(COEFFICIENT_VECTOR_SCHEMA),
        "vector_comparison_rules": len(VECTOR_COMPARISON_RULES),
        "theorem_zero_routes": len(THEOREM_ZERO_ROUTES),
        "invalid_R11_inputs": len(INVALID_R11_INPUTS),
        "template_path": str(ROOT / TEMPLATE_PATH),
        "R11_vector_template_written": True,
        "actual_R11_vector_supplied": False,
        "EH_only_theorem_zero_derived": False,
        "R11_promoted": False,
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
        description="Write checkpoint 438 R11 non-EH coefficient-vector contract artifacts."
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
