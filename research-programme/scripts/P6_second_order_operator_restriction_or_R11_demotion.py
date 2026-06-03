from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "P6-second-order-operator-restriction-or-R11-demotion"
CHECKPOINT_DOC = "442-P6-second-order-operator-restriction-or-R11-demotion.md"
STATUS = "P6_second_order_operator_restriction_attempt_written_Lovelock_conditional_parent_restriction_not_derived_P6_demoted_to_R11_no_EH_Newton_PPN_or_local_GR_pass"
CLAIM_CEILING = "P6_second_order_operator_restriction_only_no_EH_Newton_PPN_R10_R11_or_local_GR_pass"
NEXT_TARGET = "443-metric-compatibility-Levi-Civita-or-R11-connection-row.md"
P6_TEMPLATE_PATH = Path("source-intake/mts_residuals/R11_P6_metric_operator_rows_TEMPLATE.csv")


R11_VECTOR_COLUMNS = [
    "model_id",
    "branch_id",
    "vector_id",
    "operator_family",
    "coefficient_symbol",
    "coefficient_value",
    "coefficient_units",
    "normalization",
    "operator_form",
    "weak_field_map",
    "affected_rows",
    "induced_observable",
    "predicted_residual_or_bound_source",
    "derivation_status",
    "formula_reference",
    "source_file",
    "assumptions",
    "valid_for_claim",
    "notes",
]


SOURCE_DOCS = [
    {
        "path": "358-local-EH-exterior-operator-from-Ward-closed-action.md",
        "role": "Lovelock-style EH sufficiency and operator obstruction",
    },
    {
        "path": "375-EH-exterior-operator-or-residual-modified-gravity-ledger.md",
        "role": "operator-or-residual modified-gravity ledger",
    },
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "minimal parent action and EH exterior identity contract",
    },
    {
        "path": "392-EH-operator-selection-under-identity-closure.md",
        "role": "same-frame identity does not imply EH and non-EH operators retained",
    },
    {
        "path": "438-R11-nonEH-coefficient-vector-contract.md",
        "role": "R11 operator vector schema and theorem-zero route",
    },
    {
        "path": "439-EH-only-exterior-parent-premise-ladder.md",
        "role": "P6 second-order rung in the EH-only premise ladder",
    },
    {
        "path": "440-metric-only-second-order-sector-reduction-attempt.md",
        "role": "sector reduction matrix and second-order operator filter",
    },
    {
        "path": "441-extra-sector-nohair-priority-gate.md",
        "role": "P6 selected as highest-priority next theorem attack",
    },
    {
        "path": "runs/20260601-184500-local-EH-exterior-operator-from-Ward-closed-action/results/EH_operator_theorem_steps.csv",
        "role": "machine-readable conditional EH theorem steps",
    },
    {
        "path": "runs/20260601-184500-local-EH-exterior-operator-from-Ward-closed-action/results/operator_basis_audit.csv",
        "role": "operator basis audit showing higher-curvature/nonlocal obstructions",
    },
    {
        "path": "runs/20260601-235000-EH-exterior-operator-or-residual-modified-gravity-ledger/results/coefficient_to_observable_map.csv",
        "role": "coefficient-to-observable map for modified-gravity operators",
    },
    {
        "path": "runs/20260602-130000-R11-nonEH-coefficient-vector-contract/results/coefficient_vector_schema.csv",
        "role": "canonical R11 coefficient-vector schema",
    },
    {
        "path": "runs/20260602-130000-R11-nonEH-coefficient-vector-contract/results/operator_families.csv",
        "role": "canonical R11 operator families",
    },
    {
        "path": "runs/20260602-133000-metric-only-second-order-sector-reduction-attempt/results/second_order_operator_filter.csv",
        "role": "P6 operator-family filter",
    },
    {
        "path": "runs/20260602-134500-extra-sector-nohair-priority-gate/results/sector_priority_matrix.csv",
        "role": "P6 priority ranking",
    },
    {
        "path": "source-intake/mts_residuals/R11_nonEH_operator_vector_TEMPLATE.csv",
        "role": "full R11 vector template",
    },
]


P6_PROBLEM_STATEMENT = [
    {
        "item": "P6_target",
        "statement": "derive that the surviving local exterior metric equations are at most second order through local tested scales",
        "mathematical_form": "E_ext^{mu nu}=E_ext^{mu nu}(g, partial g, partial^2 g)",
        "current_status": "central_blocker_not_parent_derived",
    },
    {
        "item": "why_it_matters",
        "statement": "without P6, Lovelock/EH selection does not start and R2/fR/Ricci/Weyl/nonlocal operators remain legal",
        "mathematical_form": "E_ext^{mu nu}=aG^{mu nu}+bg^{mu nu}+sum_i c_i H_i^{mu nu}",
        "current_status": "R11_retained",
    },
    {
        "item": "legal_success",
        "statement": "parent action forbids, topologizes, or exactly decouples every higher-derivative/nonlocal metric operator",
        "mathematical_form": "c_R2=c_fR=c_Ricci=c_Weyl=c_nonlocal=0 or topological/harmless",
        "current_status": "not_derived",
    },
    {
        "item": "legal_failure",
        "statement": "if any coefficient survives, P6 is demoted to R11 coefficient-vector data",
        "mathematical_form": "R11_P6_metric_operator_rows_TEMPLATE.csv",
        "current_status": "template_written_by_this_checkpoint",
    },
]


P6_THEOREM_ROUTES = [
    {
        "route_id": "P6_R0_Lovelock_if_assumed",
        "route_claim": "local 4D metric-only diffeomorphic second-order equations select EH plus Lambda",
        "required_parent_evidence": "P1-P7 already derived, especially metric-only and second-order",
        "result": "conditional_EH_theorem_shape",
        "status": "pass_conditional_not_parent_derivation",
        "why_not_enough": "this assumes P6; it does not derive P6",
    },
    {
        "route_id": "P6_R1_parent_derivative_order",
        "route_claim": "the parent metric core contains no local higher-derivative metric invariants",
        "required_parent_evidence": "configuration/symmetry/minimality principle restricting S_metric to EH plus Lambda plus harmless boundary/topological terms",
        "result": "would_derive_P6",
        "status": "not_supplied",
        "why_not_enough": "current corpus lists the action blocks but does not provide the excluding symmetry/principle",
    },
    {
        "route_id": "P6_R2_ghost_regularitiy_no_extra_modes",
        "route_claim": "regularity/unitarity/no-extra-local-propagating-mode principle forbids higher-derivative metric modes",
        "required_parent_evidence": "explicit theorem that MTS parent configuration admits no Ostrogradsky/spin-2/scalar ghost or auxiliary metric mode in local branch",
        "result": "could_reduce_higher_curvature",
        "status": "not_derived",
        "why_not_enough": "ghost avoidance is a design pressure; EFT or degenerate theories can still retain controlled higher operators",
    },
    {
        "route_id": "P6_R3_topological_combination_only",
        "route_claim": "all quadratic curvature terms combine into 4D topological/boundary terms",
        "required_parent_evidence": "coefficients fixed to Gauss-Bonnet/topological combination and boundary no-hair is derived",
        "result": "conditional_boundary_harmless",
        "status": "not_derived",
        "why_not_enough": "coefficient relation and boundary/class no-hair are both open",
    },
    {
        "route_id": "P6_R4_auxiliary_degenerate_second_order",
        "route_claim": "higher-curvature-looking sector is rewritten with auxiliaries that have second-order equations",
        "required_parent_evidence": "auxiliary variables are absent/gauge/no-haired and do not add scalar/vector/source residuals",
        "result": "not_metric_only_unless_auxiliaries_harmless",
        "status": "fails_as_EH_route_currently",
        "why_not_enough": "degenerate or auxiliary reformulations can still be modified gravity, not EH",
    },
    {
        "route_id": "P6_R5_low_energy_EFT_suppression",
        "route_claim": "higher-curvature/nonlocal terms are suppressed below local bounds",
        "required_parent_evidence": "numeric coefficient scales and weak-field maps below source-locked residual limits",
        "result": "empirical_retained_branch_only",
        "status": "R11_demotion",
        "why_not_enough": "small is testable, not theorem-zero local GR",
    },
    {
        "route_id": "P6_R6_nonlocal_kernel_silence",
        "route_claim": "nonlocal/memory kernels vanish or become constant universal calibration in compact ordinary exterior",
        "required_parent_evidence": "compact-local kernel support/screening theorem with no Gdot/alpha3/R10 leakage",
        "result": "could_clear_nonlocal_part_of_P6",
        "status": "not_derived",
        "why_not_enough": "cosmological memory activity does not imply local kernel silence",
    },
]


OPERATOR_DEMOTION_ROWS = [
    {
        "operator_family": "R2_fR_scalar_mode",
        "operator_form": "sqrt(-g)(c_R2 R^2 + c_fR f_extra(R))",
        "P6_status": "not_forbidden",
        "induced_rows": "R3;R4;R10;R11",
        "theorem_zero_condition": "c_R2=c_fR=0, infinite scalar mass, zero matter/source coupling, or topological/no local scalar mode",
        "demotion_action": "fill R11 row; if finite-range scalar exists, fill R10 alpha(lambda) curve",
    },
    {
        "operator_family": "Ricci_Weyl_squared",
        "operator_form": "sqrt(-g)(c_Ricci R_mn R^mn + c_Weyl C_mnrs C^mnrs)",
        "P6_status": "not_forbidden",
        "induced_rows": "R3;R8;R11",
        "theorem_zero_condition": "coefficients zero or exactly topological/boundary-harmless combination",
        "demotion_action": "fill R11 row with slip/location/wave-sector weak-field map",
    },
    {
        "operator_family": "Gauss_Bonnet_topological_4D",
        "operator_form": "sqrt(-g)(Riemann^2 - 4 Ricci^2 + R^2)",
        "P6_status": "conditionally_harmless",
        "induced_rows": "R3;R4;R7;R8;R11 if boundary hair remains",
        "theorem_zero_condition": "pure 4D topological term plus boundary/class no-hair",
        "demotion_action": "if boundary no-hair not derived, retain boundary/topological R11 row",
    },
    {
        "operator_family": "nonlocal_memory_kernel",
        "operator_form": "R Box^{-1} R or history/domain kernel",
        "P6_status": "not_local_second_order",
        "induced_rows": "R7;R9;R10;R11",
        "theorem_zero_condition": "compact-local kernel silence/screening or constant universal calibration",
        "demotion_action": "fill R11 nonlocal row and R10/Gdot/alpha3 maps if active",
    },
    {
        "operator_family": "EFT_suppressed_metric_operator",
        "operator_form": "sum_n c_n O_n/Lambda_cut^{n-4}",
        "P6_status": "empirical_not_theorem_zero",
        "induced_rows": "R3;R4;R8;R10;R11 depending on O_n",
        "theorem_zero_condition": "all c_n theorem-zero or topological; otherwise not P6",
        "demotion_action": "fill R11 coefficient rows with units/cutoff/normalization and residual maps",
    },
]


P6_R11_TEMPLATE_ROWS = [
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "vector_id": "R11_P6_metric_operator_rows",
        "operator_family": "R2_fR_scalar_mode",
        "coefficient_symbol": "c_R2_or_c_fR",
        "coefficient_value": "fill_numeric_or_zero",
        "coefficient_units": "fill_length_power_or_dimensionless_after_normalization",
        "normalization": "fill_relative_to_EH_or_cutoff_scale",
        "operator_form": "sqrt(-g)(c_R2 R^2 + c_fR f_extra(R))",
        "weak_field_map": "fill_gamma_beta_scalar_mass_alpha_lambda_map",
        "affected_rows": "R3;R4;R10;R11",
        "induced_observable": "gamma_minus_1;beta_minus_1;alpha(lambda);operator_ledger",
        "predicted_residual_or_bound_source": "fill_numeric_residual_curve_or_map_path",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "fill_formula_reference",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_frame_source_normalization_scalar_mass_coupling_assumptions",
        "valid_for_claim": "false",
        "notes": "P6 template only; finite scalar range also requires R10 curve",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "vector_id": "R11_P6_metric_operator_rows",
        "operator_family": "Ricci_Weyl_squared",
        "coefficient_symbol": "c_Ricci_or_c_Weyl",
        "coefficient_value": "fill_numeric_or_zero",
        "coefficient_units": "fill_length_power_or_dimensionless_after_normalization",
        "normalization": "fill_relative_to_EH_or_cutoff_scale",
        "operator_form": "sqrt(-g)(c_Ricci R_mn R^mn + c_Weyl C_mnrs C^mnrs)",
        "weak_field_map": "fill_gamma_xi_slip_wave_sector_map",
        "affected_rows": "R3;R8;R11",
        "induced_observable": "gamma_minus_1;xi;operator_ledger",
        "predicted_residual_or_bound_source": "fill_numeric_residual_or_map_path",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "fill_formula_reference",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_frame_boundary_topological_wave_sector_assumptions",
        "valid_for_claim": "false",
        "notes": "P6 template only; topological combination needs boundary no-hair source",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "vector_id": "R11_P6_metric_operator_rows",
        "operator_family": "nonlocal_memory_kernel",
        "coefficient_symbol": "c_nonlocal_or_K",
        "coefficient_value": "fill_numeric_kernel_norm_or_zero",
        "coefficient_units": "fill_kernel_units_after_normalization",
        "normalization": "fill_relative_to_local_kernel_or_EH_scale",
        "operator_form": "R Box^-1 R or integral K(x,x_prime) I[g](x_prime)dV_prime",
        "weak_field_map": "fill_alpha3_Gdot_alpha_lambda_kernel_map",
        "affected_rows": "R7;R9;R10;R11",
        "induced_observable": "alpha3;Gdot_over_G;alpha(lambda);operator_ledger",
        "predicted_residual_or_bound_source": "fill_numeric_residual_curve_or_map_path",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "fill_formula_reference",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_compact_local_kernel_silence_or_screening_assumptions",
        "valid_for_claim": "false",
        "notes": "P6 template only; nonlocal success in cosmology is not local silence",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "vector_id": "R11_P6_metric_operator_rows",
        "operator_family": "boundary_topological_terms",
        "coefficient_symbol": "c_GB_or_c_boundary",
        "coefficient_value": "fill_numeric_or_zero",
        "coefficient_units": "fill_units_after_normalization",
        "normalization": "fill_topological_boundary_normalization",
        "operator_form": "Gauss-Bonnet/topological/boundary metric functional",
        "weak_field_map": "fill_boundary_nohair_or_R3_R4_R7_R8_map",
        "affected_rows": "R3;R4;R7;R8;R11",
        "induced_observable": "gamma_minus_1;beta_minus_1;alpha3;xi;operator_ledger",
        "predicted_residual_or_bound_source": "fill_boundary_nohair_source_or_residual_map",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "fill_formula_reference",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_boundary_class_topological_nohair_assumptions",
        "valid_for_claim": "false",
        "notes": "P6 template only; topological term is harmless only if boundary/class hair is also killed",
    },
]


P6_GATE_TESTS = [
    {
        "gate": "locality_gate",
        "pass_condition": "no nonlocal/history/domain kernel contributes to compact local exterior equations",
        "current_result": "fail_open",
        "evidence": "nonlocal_memory_kernel remains retained unless local kernel silence is derived",
    },
    {
        "gate": "higher_derivative_gate",
        "pass_condition": "R2/fR/Ricci/Weyl operators are absent, topological, or exactly decoupled",
        "current_result": "fail_open",
        "evidence": "no parent principle forbids higher-curvature metric operators",
    },
    {
        "gate": "topological_boundary_gate",
        "pass_condition": "topological/boundary combinations leave no local class/boundary hair",
        "current_result": "conditional_open",
        "evidence": "boundary no-hair remains a separate retained gate",
    },
    {
        "gate": "auxiliary_rewrite_gate",
        "pass_condition": "any auxiliary rewrite adds no physical scalar/vector/source operator",
        "current_result": "fail_open",
        "evidence": "auxiliary/projector Euler ledger is not closed",
    },
    {
        "gate": "EFT_suppression_gate",
        "pass_condition": "suppressed operators are either theorem-zero or explicitly coefficient-mapped",
        "current_result": "demote_to_R11",
        "evidence": "small retained coefficients are empirical, not EH theorem",
    },
]


THEOREM_ATTEMPT_STATUS = [
    {
        "claim": "P6 theorem routes audited",
        "status": "pass",
        "evidence": "7 candidate routes recorded with required parent evidence",
    },
    {
        "claim": "Lovelock conditional theorem preserved",
        "status": "pass_conditional",
        "evidence": "if P6 is assumed with P1-P7, EH plus Lambda follows",
    },
    {
        "claim": "P6 parent restriction derived",
        "status": "fail",
        "evidence": "no parent symmetry/minimality/regularity theorem forbids higher-curvature or nonlocal metric operators",
    },
    {
        "claim": "higher-curvature/nonlocal operators theorem-zero",
        "status": "fail",
        "evidence": "R2/fR/Ricci/Weyl/nonlocal families remain legal unless coefficients are supplied",
    },
    {
        "claim": "P6 demoted to executable R11 fallback",
        "status": "pass",
        "evidence": str(P6_TEMPLATE_PATH),
    },
    {
        "claim": "EH/Newton/PPN/local-GR promoted",
        "status": "fail",
        "evidence": "P6 demotion only; no R11 data and no local-GR pass",
    },
]


GATE_RESULTS_TEMPLATE = [
    {
        "gate": "P6_problem_statement_written",
        "status": "pass",
        "evidence": "P6 target, success, and failure conditions recorded",
    },
    {
        "gate": "P6_theorem_routes_audited",
        "status": "pass",
        "evidence": "7 routes audited",
    },
    {
        "gate": "operator_demotion_rows_written",
        "status": "pass",
        "evidence": "5 P6 operator demotion rows recorded",
    },
    {
        "gate": "P6_R11_template_written",
        "status": "pass",
        "evidence": str(P6_TEMPLATE_PATH),
    },
    {
        "gate": "P6_parent_restriction_derived",
        "status": "fail",
        "evidence": "no parent principle currently forbids higher-curvature/nonlocal metric operators",
    },
    {
        "gate": "Lovelock_used_without_assumption",
        "status": "fail",
        "evidence": "Lovelock theorem remains conditional and cannot derive its own second-order premise",
    },
    {
        "gate": "P6_promoted",
        "status": "fail",
        "evidence": "P6 is demoted to R11 unless future theorem closes it",
    },
    {
        "gate": "R11_data_supplied",
        "status": "fail",
        "evidence": "template rows only; no numeric coefficients or weak-field maps supplied",
    },
    {
        "gate": "local_GR_promoted",
        "status": "fail",
        "evidence": "P6 audit only; no EH/Newton/PPN/local-GR pass",
    },
    {
        "gate": "claim_ceiling_enforced",
        "status": "pass",
        "evidence": CLAIM_CEILING,
    },
]


DECISION = [
    {
        "decision": "P6 has been attacked directly. The Lovelock/EH theorem remains valid only conditionally: if the parent action has already reduced the compact exterior to local 4D metric-only second-order equations, EH plus Lambda follows. The current corpus does not derive the second-order restriction itself. Ghost/regularity, EFT suppression, auxiliary rewrites, and topological combinations are useful routes but require additional parent evidence that is not supplied. Therefore P6 is not promoted; higher-curvature and nonlocal metric operators are demoted into explicit R11 coefficient rows, with R10 required wherever a finite-range scalar force survives.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "443-metric-compatibility-Levi-Civita-or-R11-connection-row.md",
        "why_next": "P4 is the crisp follow-up: derive Levi-Civita observed branch or retain torsion/nonmetricity R11 rows",
    },
    {
        "rank": 2,
        "target": "fill R11_P6_metric_operator_rows_TEMPLATE.csv",
        "why_next": "if P6 remains demoted, higher-curvature/nonlocal coefficients must become executable data",
    },
    {
        "rank": 3,
        "target": "source-normalization residual vector refinement",
        "why_next": "parallel Newton lane remains necessary even if EH operator route improves",
    },
]


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
    template_schema_gate = {
        "gate": "P6_template_schema_matches_R11",
        "status": "pass" if list(P6_R11_TEMPLATE_ROWS[0].keys()) == R11_VECTOR_COLUMNS else "fail",
        "evidence": "P6 template columns match canonical R11 vector schema"
        if list(P6_R11_TEMPLATE_ROWS[0].keys()) == R11_VECTOR_COLUMNS
        else "P6 template schema mismatch",
    }
    return [source_gate, template_schema_gate, *GATE_RESULTS_TEMPLATE]


def write_checkpoint_markdown(run_dir: Path, gate_result_rows: list[dict[str, Any]]) -> None:
    source_rows = source_register_rows()
    text = f"""# 442 - P6 Second-Order Operator Restriction Or R11 Demotion

Private EH/operator checkpoint. This is not a public Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, R10/R11, cosmology, local-GR, or unified-field claim.

## 1. Purpose

Checkpoint 441 selected P6 as the next theorem attack. This checkpoint asks whether the current corpus derives the second-order metric-operator restriction needed for Lovelock/EH selection, or whether higher-curvature/nonlocal metric operators must be demoted into R11 coefficient rows.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/P6_second_order_operator_restriction_or_R11_demotion.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| P6 R11 template | `{P6_TEMPLATE_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_rows, ["source_file", "exists", "role"])}

## 4. P6 Problem Statement

{markdown_table(P6_PROBLEM_STATEMENT, ["item", "statement", "mathematical_form", "current_status"])}

## 5. P6 Theorem Routes

{markdown_table(P6_THEOREM_ROUTES, ["route_id", "route_claim", "result", "status", "why_not_enough"])}

## 6. Operator Demotion Rows

{markdown_table(OPERATOR_DEMOTION_ROWS, ["operator_family", "P6_status", "induced_rows", "theorem_zero_condition", "demotion_action"])}

## 7. P6 R11 Template Rows

The P6-specific R11 template has been written to `{P6_TEMPLATE_PATH}`.

{markdown_table(P6_R11_TEMPLATE_ROWS, R11_VECTOR_COLUMNS)}

## 8. P6 Gate Tests

{markdown_table(P6_GATE_TESTS, ["gate", "pass_condition", "current_result", "evidence"])}

## 9. Theorem Attempt Status

{markdown_table(THEOREM_ATTEMPT_STATUS, ["claim", "status", "evidence"])}

## 10. Gate Results

{markdown_table(gate_result_rows, ["gate", "status", "evidence"])}

## 11. Decision

{DECISION[0]["decision"]}

Practical read: P6 did not win the GR belt today. Lovelock is still the right theorem, but only after P6 is earned. Until a parent principle forbids higher-curvature/nonlocal operators, those operators are R11 fighters, not ghosts hidden under the canvas.

## 12. Next Queue

{markdown_table(NEXT_QUEUE, ["rank", "target", "why_next"])}
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    gate_result_rows = gate_rows(source_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "P6_problem_statement.csv", P6_PROBLEM_STATEMENT)
    write_csv(results_dir / "P6_theorem_routes.csv", P6_THEOREM_ROUTES)
    write_csv(results_dir / "operator_demotion_rows.csv", OPERATOR_DEMOTION_ROWS)
    write_csv(results_dir / "P6_R11_template_rows.csv", P6_R11_TEMPLATE_ROWS, R11_VECTOR_COLUMNS)
    write_csv(results_dir / "P6_gate_tests.csv", P6_GATE_TESTS)
    write_csv(results_dir / "theorem_attempt_status.csv", THEOREM_ATTEMPT_STATUS)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)
    write_csv(ROOT / P6_TEMPLATE_PATH, P6_R11_TEMPLATE_ROWS, R11_VECTOR_COLUMNS)
    write_csv(results_dir / "R11_P6_metric_operator_rows_TEMPLATE.csv", P6_R11_TEMPLATE_ROWS, R11_VECTOR_COLUMNS)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "P6_theorem_routes": len(P6_THEOREM_ROUTES),
        "operator_demotion_rows": len(OPERATOR_DEMOTION_ROWS),
        "P6_template_rows": len(P6_R11_TEMPLATE_ROWS),
        "P6_parent_restriction_derived": False,
        "P6_promoted": False,
        "R11_data_supplied": False,
        "EH_promoted": False,
        "Newtonian_reduction_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "P6_template_path": str(ROOT / P6_TEMPLATE_PATH),
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
        description="Write checkpoint 442 P6 second-order operator restriction or R11 demotion artifacts."
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
