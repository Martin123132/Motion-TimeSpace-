from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_Cextra_bulk_memory_range_positive_operator_zero_failed_Yukawa_bound_fill_written"
CLAIM_CEILING = "bulk_memory_range_Cextra_attempt_only_no_R10_fifth_force_radial_closure_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "558-Y5-R10-alpha-lambda-source-normalized-curve-data-or-no-range-theorem.md"

DOC_PATH = Path("557-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_CEXTRA_BULK_MEMORY_RANGE_557_SOURCE_REGISTER.csv")
POSITIVE_OPERATOR_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_Y5_CEXTRA_BULK_MEMORY_RANGE_POSITIVE_OPERATOR_ATTEMPT.csv")
FORCE_LAW_MAP_PATH = Path("source-intake/mts_residuals/P8_Y5_CEXTRA_BULK_MEMORY_RANGE_FORCE_LAW_MAP.csv")
BOUND_FILL_PATH = Path("source-intake/mts_residuals/P8_Y5_CEXTRA_BULK_MEMORY_RANGE_YUKAWA_FILL_ROW.csv")
R10_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_Y5_CEXTRA_BULK_MEMORY_RANGE_R10_CURVE_CONTRACT.csv")
EVALUATOR_PATH = Path("source-intake/mts_residuals/P8_Y5_CEXTRA_BULK_MEMORY_RANGE_EVALUATOR.csv")
OBSTRUCTION_LEDGER_PATH = Path("source-intake/mts_residuals/P8_Y5_CEXTRA_BULK_MEMORY_RANGE_557_OBSTRUCTION_LEDGER.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_557_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_557_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_557_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "556-Y5-extra-sector-Hamiltonian-charge-silence-or-channel-fill.md",
        "role": "Cextra core channel split selecting bulk/memory/range as next target",
    },
    {
        "source_file": "555-Y5-radial-closure-Cterm-zero-or-first-Hamiltonian-residual-fill.md",
        "role": "radial C-term closure failure retaining C_extra",
    },
    {
        "source_file": "522-Y5-extra-mass-projection-silence-or-channelwise-bound.md",
        "role": "Y5 extra mass projection silence and channelwise bound input",
    },
    {
        "source_file": "506-local-EH-reduction-and-extra-sector-silence-theorem.md",
        "role": "positive source-free operator silence route",
    },
    {
        "source_file": "380-bulk-X-mass-gap-source-normalized-force-law.md",
        "role": "bulk-X mass-gap and source-normalized Yukawa force-law debt",
    },
    {
        "source_file": "437-R10-alpha-lambda-executable-curve-contract.md",
        "role": "R10 alpha(lambda) executable curve contract",
    },
    {
        "source_file": "467-mu-extra-zero-owner-or-source-normalization-coefficient-vector.md",
        "role": "mu_extra source-normalization coefficient vector",
    },
    {
        "source_file": "468-mu-extra-coefficient-vector-to-local-bound-scorecard.md",
        "role": "mu_extra local bound scorecard requiring R10 curve",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_EXTRA_CHARGE_CHANNEL_MAP.csv",
        "role": "556 Cextra channel re-basis map",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_EXTRA_CHARGE_BOUND_FILL_ROW.csv",
        "role": "556 Cextra core bound fill row",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_556_VALIDATION.csv",
        "role": "previous validation gate",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_EXTRA_MASS_CHANNELWISE_BOUND_INPUT.csv",
        "role": "522 channelwise bulk/memory/range input row",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
        "role": "506 positive operator and memory silence identities",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_FIELD_SPECIFIC_SILENCE_ACCEPTANCE_GATES.csv",
        "role": "507 theorem-zero/numeric/demotion gates",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_OWNER_LEDGER.csv",
        "role": "mu_extra owner ledger with bulk_X_Yukawa_tail row",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_BOUND_SUMMARY.csv",
        "role": "mu_extra bound summary with R10 curve requirement",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MU_EXTRA_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv",
        "role": "source-normalized coefficient vector with epsilon_bulk_X row",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv",
        "role": "constant-GM derivative/range hair gate",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_CONSTANT_GM_DERIVATIVE_HAIR_FILL_QUEUE.csv",
        "role": "constant-GM fill queue including R10 alpha(lambda)",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv",
        "role": "mu_extra local bound scorecard rows requiring R10 curve",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MU_EXTRA_SCORECARD_REQUIRED_INPUTS.csv",
        "role": "mu_extra required input artifact list",
    },
    {
        "source_file": "source-intake/mts_residuals/R10_alpha_lambda_curve_TEMPLATE.csv",
        "role": "R10 executable alpha(lambda) curve template",
    },
    {
        "source_file": "source-intake/mts_residuals/R11_R10_LINK_REQUIREMENTS.csv",
        "role": "R11-to-R10 link requirements",
    },
    {
        "source_file": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "local-bound claims table containing symbolic R10 row",
    },
    {
        "source_file": "runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/source_normalized_force_law.csv",
        "role": "380 source-normalized bulk-X Yukawa force-law ledger",
    },
    {
        "source_file": "runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/gate_results.csv",
        "role": "380 gate results showing alpha_X/lambda_X not parent-derived",
    },
    {
        "source_file": "runs/20260602-094500-MTS-local-residual-vector-input-contract/results/residual_components.csv",
        "role": "local residual component contract containing R10",
    },
    {
        "source_file": "runs/20260602-105000-MTS-local-residual-vector-evaluator/results/gate_results.csv",
        "role": "local residual evaluator gate showing missing R10 curve",
    },
    {
        "source_file": "scripts/Y5_Cextra_bulk_memory_range_positive_operator_zero_or_Yukawa_bound_fill.py",
        "role": "this checkpoint generator",
    },
]


POSITIVE_OPERATOR_ATTEMPT_ROWS = [
    {
        "step_id": "BMR557_0_target",
        "claim": "bulk, memory, and finite-range extra sectors have zero Hamiltonian mass-charge leakage in the compact source-free annulus",
        "mathematical_form": "epsilon_bulk_memory_range_over_MH = M_H^-1 int_A(C_bulk+C_memory+C_range)=0",
        "current_result": "target_defined",
        "why_not_enough": "target definition is not a parent action or no-hair proof",
        "valid_for_claim": "false",
    },
    {
        "step_id": "BMR557_1_massive_positive_operator",
        "claim": "a positive massive elliptic operator forces the bulk field to vanish outside the source",
        "mathematical_form": "(-Delta_A+m_X^2)X=0; m_X^2>0; int_A(|grad X|^2+m_X^2 X^2)=boundary_flux",
        "current_result": "conditional_reference",
        "why_not_enough": "MTS has not supplied field-specific operator sign, m_X, source charge, and zero boundary flux for the bulk/memory/range sector",
        "valid_for_claim": "false",
    },
    {
        "step_id": "BMR557_2_source_charge_zero",
        "claim": "ordinary compact local matter has no bulk/memory/range source charge in the annulus",
        "mathematical_form": "rho_X=0 in A and Q_X[source]=0 or Pi_M^H Q_X=0",
        "current_result": "not_derived",
        "why_not_enough": "source-normalized charge Q_X, q_test, and Pi_M projection are not parent-owned",
        "valid_for_claim": "false",
    },
    {
        "step_id": "BMR557_3_memory_kernel_silence",
        "claim": "memory/history response is local, stable, and derivative-silent in compact local systems",
        "mathematical_form": "K_mem local positive/stable; no boundary/history injection; D_t epsilon_mem=D_r epsilon_mem=D_lambda epsilon_mem=0",
        "current_result": "not_derived",
        "why_not_enough": "memory double-zero/local kernel premises are not signed for this Hamiltonian charge channel",
        "valid_for_claim": "false",
    },
    {
        "step_id": "BMR557_4_Yukawa_force_law_route",
        "claim": "if a finite-range field survives, it must be represented as a source-normalized Yukawa curve",
        "mathematical_form": "a_X/a_GR = alpha_X(lambda_X)(1+r/lambda_X)exp(-r/lambda_X)",
        "current_result": "contract_available",
        "why_not_enough": "380/437 provide the convention and template, but alpha_X(lambda_X), lambda_X, source/test charges, and bound curve rows are missing",
        "valid_for_claim": "false",
    },
    {
        "step_id": "BMR557_5_mass_gap_not_enough",
        "claim": "a positive mass gap alone removes the fifth-force channel",
        "mathematical_form": "m_X^2>0 => alpha_X=0",
        "current_result": "invalid_shortcut",
        "why_not_enough": "mass gap sets lambda_X but not alpha_X; source/test coupling and measured-G normalization determine fifth-force strength",
        "valid_for_claim": "false",
    },
    {
        "step_id": "BMR557_6_no_cancellation",
        "claim": "bulk/memory/range leakage can cancel against other Cextra channels",
        "mathematical_form": "C_bulk+C_memory+C_range+C_nonEH+...=0 by fitted cancellation",
        "current_result": "forbidden",
        "why_not_enough": "Cextra uses strict absolute channel bounds; only parent Ward identity can remove a channel",
        "valid_for_claim": "false",
    },
    {
        "step_id": "BMR557_7_verdict",
        "claim": "epsilon_bulk_memory_range_over_MH can be filled as zero in FB556_0",
        "mathematical_form": "epsilon_bulk_memory_range_over_MH=0",
        "current_result": "fail_current_claim",
        "why_not_enough": "no positive-operator zero certificate and no executable R10 alpha(lambda) curve are available",
        "valid_for_claim": "false",
    },
]


FORCE_LAW_MAP_ROWS = [
    {
        "map_id": "BMRF557_0_static_bulk_operator",
        "branch": "massive_bulk_X",
        "operator_or_law": "(-Delta+m_X^2)X=q_X rho_source",
        "needed_for_zero": "m_X^2>0; q_X rho_source=0 in A; zero boundary flux; no source/test charge projection",
        "needed_for_bound": "m_X;lambda_X=1/m_X;q_source;q_test;Q_X;measured_G_normalization",
        "current_status": "operator_and_charges_not_parent_derived",
        "R10_artifact": "R10_alpha_lambda_curve_MTS_source_normalization.csv",
        "valid_for_claim": "false",
    },
    {
        "map_id": "BMRF557_1_memory_kernel_tail",
        "branch": "memory_history_kernel",
        "operator_or_law": "X_mem(t,r)=int K_mem(t-t',r,r')J(t',r')",
        "needed_for_zero": "local stable positive kernel; no history/boundary injection; derivative-silent universal constant only",
        "needed_for_bound": "conservative alpha_envelope(lambda) mapping the nonlocal tail to R10 convention",
        "current_status": "kernel_locality_and_tail_not_derived",
        "R10_artifact": "R10_alpha_lambda_curve_MTS_source_normalization.csv or theorem-zero source",
        "valid_for_claim": "false",
    },
    {
        "map_id": "BMRF557_2_range_scan",
        "branch": "finite_range_profile",
        "operator_or_law": "delta a/a_GR = alpha(lambda)(1+r/lambda)exp(-r/lambda)",
        "needed_for_zero": "alpha(lambda)=0 for every local lambda by parent absence/gauge/topology/no-hair",
        "needed_for_bound": "sampled lambda rows with alpha_predicted and alpha_bound in the same convention",
        "current_status": "curve_template_only",
        "R10_artifact": "source-intake/mts_residuals/R10_alpha_lambda_curve_TEMPLATE.csv -> real branch curve required",
        "valid_for_claim": "false",
    },
    {
        "map_id": "BMRF557_3_Hamiltonian_projection",
        "branch": "PiM_H_projection_of_bulk_charge",
        "operator_or_law": "epsilon_bulk_memory_range_over_MH = M_H^-1 int_A Pi_M^H dJ_bulk/memory/range",
        "needed_for_zero": "Pi_M^H projection of surviving bulk/memory/range charge is zero by parent identity",
        "needed_for_bound": "projection coefficient from bulk charge to alpha(lambda) or source-normalized mass residual",
        "current_status": "PiM_projection_not_derived",
        "R10_artifact": "R10 curve plus Hamiltonian projection normalization",
        "valid_for_claim": "false",
    },
    {
        "map_id": "BMRF557_4_constant_monopole_guardrail",
        "branch": "constant_universal_calibration",
        "operator_or_law": "epsilon_bulk_X=constant universal",
        "needed_for_zero": "constant is parent-fixed, species/range/time/radius/frame independent, and not a fifth-force tail",
        "needed_for_bound": "derivative rows D_t,D_r,D_lambda all zero or bounded",
        "current_status": "not_parent_fixed",
        "R10_artifact": "not R10 if truly universal; otherwise R10/time/radial rows required",
        "valid_for_claim": "false",
    },
]


BOUND_FILL_ROWS = [
    {
        "fill_id": "FB557_0_bulk_memory_range_zero_or_Yukawa_bound",
        "parent_fill_id": "FB556_0_HPiM_Cextra_core_channel_bound",
        "residual_component": "epsilon_bulk_memory_range_over_MH",
        "formula": "min(theorem_zero_certificate, executable_R10_curve_bound); if neither exists => not_claimable",
        "m_X_squared": "MISSING_POSITIVE_MASS_GAP_OR_OPERATOR_SIGN",
        "lambda_X": "MISSING_LAMBDA_OR_NO_RANGE_THEOREM",
        "alpha_X_lambda": "MISSING_SOURCE_NORMALIZED_ALPHA_LAMBDA_CURVE",
        "Q_X_source_charge": "MISSING_SOURCE_CHARGE_ZERO_OR_VALUE",
        "q_test_bulk_charge": "MISSING_TEST_CHARGE_ZERO_OR_VALUE",
        "PiM_H_projection": "MISSING_HAMILTONIAN_PROJECTION_ZERO_OR_COEFFICIENT",
        "boundary_flux": "MISSING_ZERO_BOUNDARY_FLUX_OR_BOUND",
        "memory_kernel_tail": "MISSING_LOCAL_STABLE_MEMORY_KERNEL_ZERO_OR_ENVELOPE",
        "R10_required_artifact": "R10_alpha_lambda_curve_MTS_source_normalization.csv",
        "mapped_lock_rows": "R10_fifth_force;R4_beta;R9_Gdot;R11_EH_operator_ledger",
        "bound_rule": "theorem-zero needs operator sign, zero source, zero boundary flux, and zero Hamiltonian projection; otherwise every lambda row needs alpha_predicted<=alpha_bound with source path",
        "source_file": "MISSING_SOURCE_FILE",
        "derivation_status": "unfilled_after_bulk_memory_range_positive_operator_failure",
        "valid_for_claim": "false",
    },
]


R10_CONTRACT_ROWS = [
    {
        "curve_contract_id": "R10C557_0_required_curve",
        "artifact": "R10_alpha_lambda_curve_MTS_source_normalization.csv",
        "required_columns": "model_id;branch_id;curve_id;lambda_value;lambda_units;alpha_predicted;alpha_bound;alpha_bound_source;force_law_form;derivation_status;formula_reference;source_file;assumptions;valid_for_claim;notes",
        "accepted_forms": "Yukawa_potential;Yukawa_acceleration_ratio;bulk_X_static_green_function;non_yukawa_envelope",
        "claim_rule": "valid_for_claim=true only after real alpha_predicted and alpha_bound rows compare in same convention",
        "current_status": "missing_real_curve",
        "valid_for_claim": "false",
    },
    {
        "curve_contract_id": "R10C557_1_theorem_zero_alternative",
        "artifact": "theorem_zero_certificate",
        "required_columns": "operator;source_charge;boundary_flux;Hamiltonian_projection;memory_kernel;range_derivatives;source_file",
        "accepted_forms": "absent_source;positive_mass_gap_nohair;pure_gauge_topological;screened_local_branch;universal_constant_no_range",
        "claim_rule": "all theorem-zero premises must be parent-derived and source-backed; mass gap alone is not enough",
        "current_status": "missing_zero_certificate",
        "valid_for_claim": "false",
    },
]


OBSTRUCTION_ROWS = [
    {
        "obstruction_id": "BMRO557_0_operator_not_owned",
        "obstruction": "bulk/memory/range field-specific operator, sign, and mass gap are not parent-derived",
        "activated_residual": "epsilon_bulk_memory_range_over_MH;m_X_squared",
        "repair": "derive Euler operator and positive energy identity for the active field",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "BMRO557_1_source_normalization_missing",
        "obstruction": "lambda_X cannot be scored without alpha_X, source charge, test charge, and measured-G normalization",
        "activated_residual": "alpha_X_lambda;Q_X_source_charge;q_test_bulk_charge",
        "repair": "derive source/test charge normalization or emit executable alpha(lambda) curve",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "BMRO557_2_memory_tail_open",
        "obstruction": "memory/history kernel may leave nonlocal tail, time drift, radial hair, or range dependence",
        "activated_residual": "memory_kernel_tail;R9_Gdot;R10_fifth_force",
        "repair": "prove local stable kernel silence or map tail to conservative alpha_envelope(lambda)",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "BMRO557_3_boundary_flux_open",
        "obstruction": "positive operator no-hair requires zero boundary flux or controlled boundary value",
        "activated_residual": "boundary_flux;epsilon_B_flux_abs",
        "repair": "derive zero boundary/linking-sphere flux for the bulk/memory/range field",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "BMRO557_4_projection_open",
        "obstruction": "surviving field may be physically nonzero but Hamiltonian-mass-projection silent; that projection is not proven",
        "activated_residual": "PiM_H_projection;C_extra_over_MH",
        "repair": "derive Pi_M^H projection zero or source-normalized coefficient to R10",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "BMRO557_5_R10_curve_missing",
        "obstruction": "R10 alpha(lambda) curve is a template only, so no fifth-force comparison can be made",
        "activated_residual": "R10_fifth_force;epsilon_bulk_X",
        "repair": "build R10_alpha_lambda_curve_MTS_source_normalization.csv with real MTS prediction rows and bound sources",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D557_0_positive_operator_zero_failed",
        "status": "bulk_memory_range_zero_not_signed",
        "meaning": "current MTS cannot set epsilon_bulk_memory_range_over_MH to zero",
        "claim_status": "epsilon_bulk_memory_range_over_MH_retained",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D557_1_Yukawa_contract_written",
        "status": "R10_curve_or_theorem_zero_contract_written",
        "meaning": "the fallback is an executable alpha(lambda) curve or a full theorem-zero certificate, not a scalar placeholder",
        "claim_status": "template_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D557_2_mass_gap_guardrail",
        "status": "mass_gap_alone_rejected",
        "meaning": "lambda_X without alpha_X and source/test charge normalization cannot pass R10",
        "claim_status": "guardrail_pass_not_theorem",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D557_3_local_GR_status",
        "status": "local_GR_still_closure_only",
        "meaning": "no Cextra, radial closure, fifth-force, Newton, PPN, or local-GR promotion is earned",
        "claim_status": "local_GR_claim_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D557_4_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "CEXTRA_BULK_MEMORY_RANGE",
        "previous_status": "not_derived_not_filled",
        "new_status": "positive_operator_zero_failed_Yukawa_R10_fill_row_written",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "HAMILTONIAN_EXTRA_CHARGE_SILENCE",
        "previous_status": "attempted_failed_current_claim_Cextra_channel_fill_row_written",
        "new_status": "still_failed_bulk_memory_range_not_zero_or_bounded",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "R10_FIFTH_FORCE",
        "previous_status": "alpha_lambda_curve_contract_only",
        "new_status": "bulk_memory_range_requires_real_curve_or_zero_certificate",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "HAMILTONIAN_RADIAL_CLOSURE",
        "previous_status": "still_failed_Cextra_core_not_zero_or_bounded",
        "new_status": "still_failed_bulk_memory_range_component_unfilled",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR_TRANSITION_ROUTE",
        "previous_status": "closure_only_Cextra_not_zero_or_bounded",
        "new_status": "closure_only_R10_bulk_memory_range_not_zero_or_bounded",
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
            "fill_id": row["fill_id"],
            "residual_component": row["residual_component"],
            "numeric_status": "not_computed_missing_theorem_zero_or_source_backed_values",
            "mapped_lock_rows": row["mapped_lock_rows"],
            "pass_status": "not_claimable",
            "valid_for_claim": "false",
            "notes": "mass gap alone is insufficient; fill with full theorem-zero certificate or executable R10 alpha(lambda) curve",
        }
        for row in BOUND_FILL_ROWS
    ]


def validation_rows(sources: list[dict[str, Any]], eval_rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    prior_validation = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_556_VALIDATION.csv"))
    prior_fails = [row for row in prior_validation if row.get("result") == "fail"]
    cextra_map = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_EXTRA_CHARGE_CHANNEL_MAP.csv"))
    cextra_fill = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_EXTRA_CHARGE_BOUND_FILL_ROW.csv"))
    extra_inputs = read_csv(Path("source-intake/mts_residuals/P8_Y5_EXTRA_MASS_CHANNELWISE_BOUND_INPUT.csv"))
    energy_identity = read_csv(Path("source-intake/mts_residuals/P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv"))
    acceptance_gates = read_csv(Path("source-intake/mts_residuals/P8_FIELD_SPECIFIC_SILENCE_ACCEPTANCE_GATES.csv"))
    owner_ledger = read_csv(Path("source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_OWNER_LEDGER.csv"))
    bound_summary = read_csv(Path("source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_BOUND_SUMMARY.csv"))
    coefficient_vector = read_csv(Path("source-intake/mts_residuals/P8_MU_EXTRA_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv"))
    derivative_gate = read_csv(Path("source-intake/mts_residuals/P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv"))
    fill_queue = read_csv(Path("source-intake/mts_residuals/P8_CONSTANT_GM_DERIVATIVE_HAIR_FILL_QUEUE.csv"))
    scorecard = read_csv(Path("source-intake/mts_residuals/P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv"))
    required_inputs = read_csv(Path("source-intake/mts_residuals/P8_MU_EXTRA_SCORECARD_REQUIRED_INPUTS.csv"))
    r10_template = read_csv(Path("source-intake/mts_residuals/R10_alpha_lambda_curve_TEMPLATE.csv"))
    r11_r10 = read_csv(Path("source-intake/mts_residuals/R11_R10_LINK_REQUIREMENTS.csv"))
    bulk_force_law = read_csv(Path("runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/source_normalized_force_law.csv"))
    bulk_gate_results = read_csv(Path("runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/gate_results.csv"))
    residual_components = read_csv(Path("runs/20260602-094500-MTS-local-residual-vector-input-contract/results/residual_components.csv"))
    evaluator_gates = read_csv(Path("runs/20260602-105000-MTS-local-residual-vector-evaluator/results/gate_results.csv"))
    claim_attempt_rows = [row for row in POSITIVE_OPERATOR_ATTEMPT_ROWS if row["valid_for_claim"] == "true"]
    claim_force_rows = [row for row in FORCE_LAW_MAP_ROWS if row["valid_for_claim"] == "true"]
    claim_fill_rows = [row for row in BOUND_FILL_ROWS if row["valid_for_claim"] == "true"]
    claim_contract_rows = [row for row in R10_CONTRACT_ROWS if row["valid_for_claim"] == "true"]
    claim_eval_rows = [row for row in eval_rows if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V557_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V557_1_prior_556_clean",
            "result": "pass" if len(prior_validation) == 10 and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_validation)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V557_2_Cextra_context_loaded",
            "result": "pass" if len(cextra_map) == 9 and len(cextra_fill) == 1 and len(extra_inputs) == 9 else "fail",
            "detail": f"cextra_map={len(cextra_map)};cextra_fill={len(cextra_fill)};extra_inputs={len(extra_inputs)}",
        },
        {
            "check_id": "V557_3_positive_operator_evidence_loaded",
            "result": "pass" if len(energy_identity) == 4 and len(acceptance_gates) == 3 else "fail",
            "detail": f"energy_identity={len(energy_identity)};acceptance_gates={len(acceptance_gates)}",
        },
        {
            "check_id": "V557_4_mu_extra_bulk_evidence_loaded",
            "result": "pass" if len(owner_ledger) == 8 and len(bound_summary) == 8 and len(coefficient_vector) == 8 and len(derivative_gate) == 8 and len(fill_queue) == 7 else "fail",
            "detail": f"owner_ledger={len(owner_ledger)};bound_summary={len(bound_summary)};coefficient_vector={len(coefficient_vector)};derivative_gate={len(derivative_gate)};fill_queue={len(fill_queue)}",
        },
        {
            "check_id": "V557_5_R10_contract_evidence_loaded",
            "result": "pass" if len(scorecard) >= 20 and len(required_inputs) == 8 and len(r10_template) == 2 and len(r11_r10) >= 6 else "fail",
            "detail": f"scorecard={len(scorecard)};required_inputs={len(required_inputs)};r10_template={len(r10_template)};r11_r10={len(r11_r10)}",
        },
        {
            "check_id": "V557_6_bulk_force_law_prior_loaded",
            "result": "pass" if len(bulk_force_law) == 5 and len(bulk_gate_results) == 10 and len(residual_components) == 12 and len(evaluator_gates) == 10 else "fail",
            "detail": f"bulk_force_law={len(bulk_force_law)};bulk_gates={len(bulk_gate_results)};residual_components={len(residual_components)};evaluator_gates={len(evaluator_gates)}",
        },
        {
            "check_id": "V557_7_attempt_and_contract_complete",
            "result": "pass" if len(POSITIVE_OPERATOR_ATTEMPT_ROWS) == 8 and len(FORCE_LAW_MAP_ROWS) == 5 and len(R10_CONTRACT_ROWS) == 2 else "fail",
            "detail": f"attempt_rows={len(POSITIVE_OPERATOR_ATTEMPT_ROWS)};force_map={len(FORCE_LAW_MAP_ROWS)};r10_contract={len(R10_CONTRACT_ROWS)}",
        },
        {
            "check_id": "V557_8_fill_row_written",
            "result": "pass" if len(BOUND_FILL_ROWS) == 1 and len(eval_rows) == 1 else "fail",
            "detail": f"fill_rows={len(BOUND_FILL_ROWS)};evaluator_rows={len(eval_rows)}",
        },
        {
            "check_id": "V557_9_no_claim_rows",
            "result": "pass" if not claim_attempt_rows and not claim_force_rows and not claim_fill_rows and not claim_contract_rows and not claim_eval_rows else "fail",
            "detail": f"claim_attempt={len(claim_attempt_rows)};claim_force={len(claim_force_rows)};claim_fill={len(claim_fill_rows)};claim_contract={len(claim_contract_rows)};claim_eval={len(claim_eval_rows)}",
        },
        {
            "check_id": "V557_10_no_overclaim",
            "result": "pass" if not claim_attempt_rows and not claim_force_rows and not claim_fill_rows and not claim_contract_rows and not claim_eval_rows else "fail",
            "detail": "bulk_memory_range_zero=false; R10_pass=false; Cextra_zero=false; radial_closure=false; Newton=false; PPN=false; local_GR=false",
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
    return f"""# 557 - Y5 Cextra Bulk/Memory/Range Positive-Operator Zero or Yukawa Bound Fill

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The bulk/memory/range channel cannot be zeroed yet.

The positive-operator route is mathematically legitimate, but current MTS does not yet supply the full certificate:

```text
operator sign + positive mass gap + zero source charge
+ zero boundary flux + zero Hamiltonian mass projection
+ local/stable memory kernel
=> epsilon_bulk_memory_range_over_MH = 0.
```

Mass gap alone is not enough. If a finite-range field survives, it must become an executable `alpha(lambda)` curve in the R10 convention.

## 2. Positive-Operator Zero Attempt

{markdown_table(POSITIVE_OPERATOR_ATTEMPT_ROWS)}

## 3. Force-Law / Projection Map

{markdown_table(FORCE_LAW_MAP_ROWS)}

## 4. Yukawa Fill Row

{markdown_table(BOUND_FILL_ROWS)}

## 5. R10 Curve Contract

{markdown_table(R10_CONTRACT_ROWS)}

## 6. Evaluator

{markdown_table(eval_rows)}

## 7. Obstruction Ledger

{markdown_table(OBSTRUCTION_ROWS)}

## 8. Decision

{markdown_table(DECISION_ROWS)}

## 9. Source Register

{markdown_table(sources)}

## 10. Validation

{markdown_table(validations)}

## 11. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 12. Claim Ceiling

Allowed:

```text
MTS has attempted the bulk/memory/range positive-operator zero route.
MTS has rejected mass-gap-only R10 credit.
MTS has written the Yukawa/R10 fill contract for epsilon_bulk_memory_range_over_MH.
```

Forbidden:

```text
MTS has proved epsilon_bulk_memory_range_over_MH = 0.
MTS has passed R10/fifth-force.
MTS has proved C_extra = 0, radial closure, Newton, PPN, or local GR.
```

## 13. Practical Read

This is a useful miss. The route is now exact: either prove the local no-hair theorem field-by-field, or build the `alpha(lambda)` curve and let the fifth-force data punch it. No scalar placeholder and no "massive therefore safe" shortcut.

## 14. Next Target

`{NEXT_TARGET}`

Next: build or source the actual R10 `alpha(lambda)` branch curve, unless a no-range theorem-zero certificate is available first.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    eval_rows = evaluator_rows()
    validations = validation_rows(sources, eval_rows)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (POSITIVE_OPERATOR_ATTEMPT_PATH, POSITIVE_OPERATOR_ATTEMPT_ROWS),
        (FORCE_LAW_MAP_PATH, FORCE_LAW_MAP_ROWS),
        (BOUND_FILL_PATH, BOUND_FILL_ROWS),
        (R10_CONTRACT_PATH, R10_CONTRACT_ROWS),
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
        "positive_operator_attempt": str(ROOT / POSITIVE_OPERATOR_ATTEMPT_PATH),
        "force_law_map": str(ROOT / FORCE_LAW_MAP_PATH),
        "bound_fill": str(ROOT / BOUND_FILL_PATH),
        "r10_contract": str(ROOT / R10_CONTRACT_PATH),
        "evaluator": str(ROOT / EVALUATOR_PATH),
        "obstruction_ledger": str(ROOT / OBSTRUCTION_LEDGER_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "missing_sources": missing_sources,
        "failed_validations": failed_validations,
        "bulk_memory_range_zero_signed": False,
        "R10_fifth_force_passed": False,
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
