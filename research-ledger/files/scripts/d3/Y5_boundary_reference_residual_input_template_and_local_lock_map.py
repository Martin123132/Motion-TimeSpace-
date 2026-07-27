from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_BRR545_residual_input_template_and_local_lock_map_written_no_values_filled"
CLAIM_CEILING = "BRR545_input_template_and_lock_map_only_no_source_measure_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "548-Y5-boundary-reference-theorem-certificate-attempt-or-first-numeric-bound-fill.md"

DOC_PATH = Path("547-Y5-boundary-reference-residual-input-template-and-local-lock-map.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_SOURCE_REGISTER.csv")
INPUT_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_INPUT_TEMPLATE.csv")
THEOREM_CERTIFICATE_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_THEOREM_CERTIFICATE_TEMPLATE.csv")
LOCAL_LOCK_MAP_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_LOCAL_LOCK_MAP.csv")
EVALUATOR_DRYRUN_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_EVALUATOR_DRYRUN.csv")
ACCEPTANCE_GATES_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_ACCEPTANCE_GATES.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "546-Y5-parent-action-boundary-reference-clause-search-or-residual-score.md",
        "role": "MAC545 ownership search and BRR545 scorecard",
    },
    {
        "source_file": "545-Y5-boundary-reference-minimal-action-clause-or-residual-row.md",
        "role": "minimal sufficient contract and retained BRR545 row",
    },
    {
        "source_file": "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
        "role": "source-normalization and Gauss/orbital calibration gate",
    },
    {
        "source_file": "524-Y5-second-order-PPN-source-stability-or-residual-evaluator.md",
        "role": "second-order PPN source-stability residual evaluator",
    },
    {
        "source_file": "530-Y5-R11-beta-component-vector-or-EH-nohair-theorem.md",
        "role": "R11/beta component vector and boundary/projector component locks",
    },
    {
        "source_file": "531-Y5-source-normalized-Newton-and-beta-residual-envelope.md",
        "role": "source-normalized Newton precondition gate",
    },
    {
        "source_file": "532-Y5-measured-GM-source-current-closure-or-first-input-fill.md",
        "role": "measured-GM source-current closure attempt",
    },
    {
        "source_file": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "local empirical lock rows used only as gates, not pass evidence",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_RESIDUAL_SCORECARD.csv",
        "role": "546 BRR545 scorecard",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_SOURCE_NEWTON_PRECONDITION_GATE.csv",
        "role": "Newton/source precondition gate",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PPN_RESIDUAL_VECTOR.csv",
        "role": "PPN residual vector",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_BOUND_REGISTER.csv",
        "role": "local GR residual bound register",
    },
    {
        "source_file": "scripts/Y5_boundary_reference_residual_input_template_and_local_lock_map.py",
        "role": "this checkpoint generator",
    },
]


INPUT_TEMPLATE_ROWS = [
    {
        "input_id": "BRI547_0_total_boundary_reference",
        "system_id": "MTS_Hamiltonian_PiM_local_branch",
        "surface_pair": "S_inner_to_S_outer",
        "residual_component": "epsilon_boundary_reference_abs",
        "formula": "abs(B_zero_flux_over_MH)+abs(Delta_symp_over_MH)",
        "B_zero_flux_over_MH": "MISSING_NUMERIC_OR_THEOREM_ZERO",
        "Delta_symp_over_MH": "MISSING_NUMERIC_OR_THEOREM_ZERO",
        "M_H_ref_status": "MISSING_SAME_FRAME_MEASURED_GM_DENOMINATOR",
        "theorem_zero_certificate_id": "MISSING_CERTIFICATE",
        "source_file": "MISSING_SOURCE_FILE",
        "units": "dimensionless",
        "normalization": "all numerator terms divided by same positive M_H_ref",
        "assumptions": "MISSING_REFERENCE_LOCK_BOUNDARY_COHOMOLOGY_NOHAIR_PROJECTOR_SILENCE_MEASURED_DENOMINATOR",
        "numeric_input_status": "not_loaded",
        "valid_for_claim": "false",
    },
    {
        "input_id": "BRI547_1_boundary_flux",
        "system_id": "MTS_Hamiltonian_PiM_local_branch",
        "surface_pair": "S_inner_to_S_outer",
        "residual_component": "epsilon_B_flux_abs",
        "formula": "abs(B_zero_flux_over_MH)",
        "B_zero_flux_over_MH": "MISSING_NUMERIC_OR_THEOREM_ZERO",
        "Delta_symp_over_MH": "",
        "M_H_ref_status": "MISSING_SHARED_DENOMINATOR",
        "theorem_zero_certificate_id": "MISSING_B_ZERO_FLUX_CERTIFICATE",
        "source_file": "MISSING_SOURCE_FILE",
        "units": "dimensionless",
        "normalization": "B_zero_flux/M_H_ref",
        "assumptions": "MISSING_BOUNDARY_EXACT_COHOMOLOGY_ZERO_AND_NO_VECTOR_TENSOR_HAIR",
        "numeric_input_status": "not_loaded",
        "valid_for_claim": "false",
    },
    {
        "input_id": "BRI547_2_reference_symplectic",
        "system_id": "MTS_Hamiltonian_PiM_local_branch",
        "surface_pair": "S_inner_to_S_outer",
        "residual_component": "epsilon_Delta_symp_abs",
        "formula": "abs(Delta_symp_over_MH)",
        "B_zero_flux_over_MH": "",
        "Delta_symp_over_MH": "MISSING_NUMERIC_OR_THEOREM_ZERO",
        "M_H_ref_status": "MISSING_SHARED_DENOMINATOR",
        "theorem_zero_certificate_id": "MISSING_DELTA_SYMP_CERTIFICATE",
        "source_file": "MISSING_SOURCE_FILE",
        "units": "dimensionless",
        "normalization": "Delta_symp/M_H_ref",
        "assumptions": "MISSING_REFERENCE_LOCK_AND_PROJECTOR_SYMPLECTIC_SILENCE",
        "numeric_input_status": "not_loaded",
        "valid_for_claim": "false",
    },
    {
        "input_id": "BRI547_3_denominator",
        "system_id": "MTS_Hamiltonian_PiM_local_branch",
        "surface_pair": "S_inner_to_S_outer",
        "residual_component": "M_H_ref_calibration",
        "formula": "M_H_ref>0 and GM_orbit=G*M_H_ref in same observed frame",
        "B_zero_flux_over_MH": "",
        "Delta_symp_over_MH": "",
        "M_H_ref_status": "MISSING_POSITIVE_SAME_FRAME_GM_CERTIFICATE",
        "theorem_zero_certificate_id": "MISSING_GM_DENOMINATOR_CERTIFICATE",
        "source_file": "MISSING_SOURCE_FILE",
        "units": "mass_or_GM_declared",
        "normalization": "same-frame Hilbert/source denominator tied to orbital GM",
        "assumptions": "MISSING_POISSON_GAUSS_ORBITAL_SOURCE_CALIBRATION",
        "numeric_input_status": "not_loaded",
        "valid_for_claim": "false",
    },
]


THEOREM_CERTIFICATE_TEMPLATE_ROWS = [
    {
        "certificate_id": "BRC547_0_reference_lock",
        "target_component": "epsilon_Delta_symp_abs",
        "required_statement": "Hamiltonian reference subtraction is source/surface/frame/time/range independent",
        "mathematical_form": "partial_t,r,source,frame,lambda Delta_ref=0",
        "acceptable_source": "parent action variation ledger or fixed background-subtraction theorem",
        "current_status": "missing_certificate",
        "source_file": "MISSING_SOURCE_FILE",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "BRC547_1_boundary_cohomology_zero",
        "target_component": "epsilon_B_flux_abs",
        "required_statement": "exact/improvement boundary form has zero linked-sphere flux in the compact exterior",
        "mathematical_form": "B_imp=dC and int_S2 B_imp-int_S1 B_imp=int_A dB_imp=0",
        "acceptable_source": "relative cohomology theorem or explicit boundary variation proof",
        "current_status": "missing_certificate",
        "source_file": "MISSING_SOURCE_FILE",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "BRC547_2_boundary_no_hair",
        "target_component": "epsilon_B_flux_abs",
        "required_statement": "boundary state has no vector, trace-free tensor, preferred-frame, radial, or time hair",
        "mathematical_form": "T_B^TF=T_B^vector=n_mu P_loc_nu T_B^{mu nu}=partial_t,r,frame T_B=0",
        "acceptable_source": "parent-owned scalar homogeneous marker-free boundary theorem",
        "current_status": "missing_certificate",
        "source_file": "MISSING_SOURCE_FILE",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "BRC547_3_projector_symplectic_silence",
        "target_component": "epsilon_Delta_symp_abs;M_H_ref_calibration",
        "required_statement": "Pi_M is topological/covariantly constant and has no symplectic stress in the exterior",
        "mathematical_form": "nabla Pi_M=0 and delta(Pi_M J_H)=Pi_M delta J_H",
        "acceptable_source": "Pi_M parent charge projector theorem or commutator bound source",
        "current_status": "missing_certificate",
        "source_file": "MISSING_SOURCE_FILE",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "BRC547_4_measured_GM_denominator",
        "target_component": "M_H_ref_calibration",
        "required_statement": "same-frame orbital measured GM equals G times the positive Hilbert/source denominator",
        "mathematical_form": "M_H_ref>0 and GM_orbit=G*M_H_ref",
        "acceptable_source": "Poisson/Gauss/orbital source-calibration theorem",
        "current_status": "missing_certificate",
        "source_file": "MISSING_SOURCE_FILE",
        "valid_for_claim": "false",
    },
]


LOCK_REQUIREMENTS = [
    {
        "map_id": "BRL547_0_boundary_alpha3",
        "residual_component": "epsilon_B_flux_abs",
        "local_row_id": "R7_alpha3",
        "coefficient_needed": "c_B_flux_to_alpha3",
        "pass_rule": "abs(c_B_flux_to_alpha3*epsilon_B_flux_abs) <= upper_bound or theorem-zero",
        "current_status": "coefficient_and_input_missing",
    },
    {
        "map_id": "BRL547_1_boundary_xi",
        "residual_component": "epsilon_B_flux_abs",
        "local_row_id": "R8_xi",
        "coefficient_needed": "c_B_flux_to_xi",
        "pass_rule": "abs(c_B_flux_to_xi*epsilon_B_flux_abs) <= upper_bound or theorem-zero",
        "current_status": "coefficient_and_input_missing",
    },
    {
        "map_id": "BRL547_2_boundary_beta",
        "residual_component": "epsilon_B_flux_abs",
        "local_row_id": "R4_beta",
        "coefficient_needed": "c_B_flux_to_beta",
        "pass_rule": "abs(c_B_flux_to_beta*epsilon_B_flux_abs) <= upper_bound or theorem-zero",
        "current_status": "coefficient_and_input_missing",
    },
    {
        "map_id": "BRL547_3_boundary_Gdot",
        "residual_component": "epsilon_B_flux_abs",
        "local_row_id": "R9_Gdot",
        "coefficient_needed": "partial_t epsilon_B_flux_abs or dln boundary charge/dt",
        "pass_rule": "time derivative maps below Gdot/G lock or theorem derivative-zero",
        "current_status": "time_profile_missing",
    },
    {
        "map_id": "BRL547_4_reference_Gdot",
        "residual_component": "epsilon_Delta_symp_abs",
        "local_row_id": "R9_Gdot",
        "coefficient_needed": "partial_t epsilon_Delta_symp_abs",
        "pass_rule": "time derivative maps below Gdot/G lock or reference derivative-zero",
        "current_status": "time_profile_missing",
    },
    {
        "map_id": "BRL547_5_reference_fifth_force",
        "residual_component": "epsilon_Delta_symp_abs",
        "local_row_id": "R10_fifth_force",
        "coefficient_needed": "radial/range profile alpha_lambda_reference",
        "pass_rule": "range-dependent alpha(lambda) curve required; symbolic row cannot pass without profile",
        "current_status": "range_profile_missing",
    },
    {
        "map_id": "BRL547_6_reference_gamma",
        "residual_component": "epsilon_Delta_symp_abs",
        "local_row_id": "R3_gamma",
        "coefficient_needed": "c_Delta_symp_to_gamma",
        "pass_rule": "abs(c_Delta_symp_to_gamma*epsilon_Delta_symp_abs) <= upper_bound or theorem-zero",
        "current_status": "coefficient_and_input_missing",
    },
    {
        "map_id": "BRL547_7_denominator_WEP",
        "residual_component": "M_H_ref_calibration",
        "local_row_id": "R1_WEP_source_charge",
        "coefficient_needed": "eta_source_from_denominator_mismatch",
        "pass_rule": "source/species dependence maps below WEP source-charge row or same-source theorem",
        "current_status": "same_source_certificate_missing",
    },
    {
        "map_id": "BRL547_8_denominator_Gdot",
        "residual_component": "M_H_ref_calibration",
        "local_row_id": "R9_Gdot",
        "coefficient_needed": "partial_t ln(G*M_H_ref/GM_orbit)",
        "pass_rule": "time drift maps below Gdot/G lock or constant denominator theorem",
        "current_status": "same_frame_time_certificate_missing",
    },
    {
        "map_id": "BRL547_9_denominator_operator",
        "residual_component": "M_H_ref_calibration",
        "local_row_id": "R11_EH_operator_ledger",
        "coefficient_needed": "non_EH_source_normalization_operator_vector",
        "pass_rule": "operator-family source normalization must be theorem-zero or executable below locks",
        "current_status": "operator_vector_missing",
    },
]


ACCEPTANCE_GATE_ROWS = [
    {
        "gate_id": "AG547_0_template_complete",
        "gate": "BRR545 input template has total, boundary-flux, reference-symplectic, and denominator rows",
        "acceptance_rule": "exactly four input rows and all valid_for_claim=false until filled",
        "current_status": "to_validate",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "AG547_1_local_locks_mapped",
        "gate": "each active residual component maps to local empirical/internal lock rows",
        "acceptance_rule": "all external lock row_ids exist in local_bound_claims.csv",
        "current_status": "to_validate",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "AG547_2_no_cancellation_credit",
        "gate": "total envelope uses absolute components, not cancellation",
        "acceptance_rule": "epsilon_total = abs(B/MH)+abs(Delta/MH); no signed cancellation row",
        "current_status": "policy_pass_template_only",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "AG547_3_measured_GM_precondition",
        "gate": "denominator must be same-frame measured GM before Newton/PPN promotion",
        "acceptance_rule": "GM_orbit=G*M_H_ref certificate exists or no measured-GM claim",
        "current_status": "fail_missing_certificate",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "AG547_4_no_public_claim",
        "gate": "private residual template cannot promote local GR",
        "acceptance_rule": "source_measure=false; Newton=false; PPN=false; local_GR=false",
        "current_status": "policy_pass_no_claim",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D547_0_input_template_written",
        "status": "BRR545_input_template_written_unfilled",
        "meaning": "epsilon_B_flux_abs, epsilon_Delta_symp_abs, and M_H_ref now have explicit fill columns",
        "claim_status": "template_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D547_1_lock_map_written",
        "status": "local_lock_map_written_no_pass",
        "meaning": "boundary/reference components are mapped to WEP, gamma, beta, alpha3, xi, Gdot, fifth-force, and R11 locks",
        "claim_status": "no_local_bound_pass_until_coefficients_or_theorem_certificates_exist",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D547_2_next_best_route",
        "status": "theorem_certificate_or_first_numeric_bound_fill",
        "meaning": "try to derive a certificate first; if not, fill one numeric bound row with source-backed coefficient/profile",
        "claim_status": "active_private_research",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D547_3_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "BOUNDARY_REFERENCE_ZERO",
        "previous_status": "MAC545_ownership_search_negative_residual_scorecard_written",
        "new_status": "BRR545_input_template_and_lock_map_written_unfilled",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_MEASURE_THEOREM",
        "previous_status": "blocked_until_BRR545_inputs_or_theorem_zero",
        "new_status": "blocked_until_BRR545_certificate_or_numeric_bound_pass",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "blocked_by_measured_denominator_and_unfilled_boundary_reference_score",
        "new_status": "still_blocked_by_denominator_certificate_and_unfilled_BRR545_values",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "still_blocked_but_gap_is_now_scoreable",
        "new_status": "still_blocked_but_BRR545_is_executable_when_inputs_exist",
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


def parse_float(value: Any) -> float | None:
    try:
        text = str(value).strip()
        if text == "":
            return None
        return float(text)
    except (TypeError, ValueError):
        return None


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in SOURCE_REGISTER:
        full_path = ROOT / item["source_file"]
        rows.append({**item, "exists": full_path.exists()})
    return rows


def local_bound_lookup() -> dict[str, dict[str, str]]:
    rows = read_csv(Path("source-intake/local_bounds/local_bound_claims.csv"))
    return {row["row_id"]: row for row in rows}


def local_lock_map_rows() -> list[dict[str, Any]]:
    bounds = local_bound_lookup()
    rows: list[dict[str, Any]] = []
    for item in LOCK_REQUIREMENTS:
        bound = bounds.get(item["local_row_id"], {})
        rows.append(
            {
                **item,
                "observable": bound.get("observable", "MISSING_LOCAL_BOUND_ROW"),
                "upper_bound": bound.get("upper_bound", ""),
                "units": bound.get("units", ""),
                "test_arena": bound.get("test_arena", ""),
                "reference_path_or_url": bound.get("reference_path_or_url", ""),
                "lock_source_exists": str(bool(bound)).lower(),
                "valid_for_claim": "false",
            }
        )
    return rows


def evaluator_dryrun_rows(input_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    boundary_value = None
    reference_value = None
    for row in input_rows:
        component = row["residual_component"]
        if component == "epsilon_B_flux_abs":
            boundary_value = parse_float(row["B_zero_flux_over_MH"])
        if component == "epsilon_Delta_symp_abs":
            reference_value = parse_float(row["Delta_symp_over_MH"])
    for row in input_rows:
        component = row["residual_component"]
        if component == "epsilon_boundary_reference_abs":
            if boundary_value is not None and reference_value is not None:
                value = abs(boundary_value) + abs(reference_value)
                numeric_status = "computed"
            else:
                value = ""
                numeric_status = "not_computed_missing_component_values"
        elif component == "epsilon_B_flux_abs":
            value_float = parse_float(row["B_zero_flux_over_MH"])
            value = "" if value_float is None else abs(value_float)
            numeric_status = "computed" if value_float is not None else "not_computed_missing_B_zero_flux_over_MH"
        elif component == "epsilon_Delta_symp_abs":
            value_float = parse_float(row["Delta_symp_over_MH"])
            value = "" if value_float is None else abs(value_float)
            numeric_status = "computed" if value_float is not None else "not_computed_missing_Delta_symp_over_MH"
        else:
            value = ""
            numeric_status = "not_computed_missing_GM_denominator_certificate"
        claim_ready = (
            numeric_status == "computed"
            and row["valid_for_claim"] == "true"
            and row["source_file"] != "MISSING_SOURCE_FILE"
        )
        rows.append(
            {
                "input_id": row["input_id"],
                "residual_component": component,
                "dryrun_value": value,
                "numeric_status": numeric_status,
                "source_file": row["source_file"],
                "theorem_zero_certificate_id": row["theorem_zero_certificate_id"],
                "current_status": "claim_ready" if claim_ready else "not_claimable",
                "valid_for_claim": str(claim_ready).lower(),
                "notes": "template row only; fill numeric value or theorem certificate before scoring",
            }
        )
    return rows


def acceptance_gate_rows(local_locks: list[dict[str, Any]], evaluator_rows_out: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_locks = [row for row in local_locks if row["lock_source_exists"] != "true"]
    claim_eval_rows = [row for row in evaluator_rows_out if row["valid_for_claim"] == "true"]
    rows: list[dict[str, Any]] = []
    for gate in ACCEPTANCE_GATE_ROWS:
        current_status = gate["current_status"]
        if gate["gate_id"] == "AG547_0_template_complete":
            current_status = "pass_template_written" if len(INPUT_TEMPLATE_ROWS) == 4 else "fail_template_incomplete"
        elif gate["gate_id"] == "AG547_1_local_locks_mapped":
            current_status = "pass_locks_exist" if not missing_locks and len(local_locks) == len(LOCK_REQUIREMENTS) else "fail_missing_lock_rows"
        elif gate["gate_id"] == "AG547_2_no_cancellation_credit":
            current_status = "pass_policy_enforced"
        elif gate["gate_id"] == "AG547_3_measured_GM_precondition":
            current_status = "fail_missing_certificate"
        elif gate["gate_id"] == "AG547_4_no_public_claim":
            current_status = "pass_policy_no_claim" if not claim_eval_rows else "fail_claim_rows_present"
        rows.append({**gate, "current_status": current_status})
    return rows


def validation_rows(
    sources: list[dict[str, Any]],
    local_locks: list[dict[str, Any]],
    evaluator_rows_out: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    prior_validation = read_csv(Path("source-intake/mts_residuals/P8_Y5_546_VALIDATION.csv"))
    prior_fails = [row for row in prior_validation if row.get("result") == "fail"]
    prior_scorecard = read_csv(Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_RESIDUAL_SCORECARD.csv"))
    ppn_vector = read_csv(Path("source-intake/mts_residuals/P8_Y5_PPN_RESIDUAL_VECTOR.csv"))
    local_bound_rows = read_csv(Path("source-intake/local_bounds/local_bound_claims.csv"))
    missing_locks = [row for row in local_locks if row["lock_source_exists"] != "true"]
    claim_input_rows = [row for row in INPUT_TEMPLATE_ROWS if row["valid_for_claim"] == "true"]
    claim_cert_rows = [row for row in THEOREM_CERTIFICATE_TEMPLATE_ROWS if row["valid_for_claim"] == "true"]
    claim_eval_rows = [row for row in evaluator_rows_out if row["valid_for_claim"] == "true"]
    gate_claim_rows = [row for row in gates if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V547_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V547_1_prior_546_clean",
            "result": "pass" if len(prior_validation) == 8 and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_validation)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V547_2_prior_scorecard_loaded",
            "result": "pass" if len(prior_scorecard) == 4 else "fail",
            "detail": f"prior_scorecard_rows={len(prior_scorecard)}",
        },
        {
            "check_id": "V547_3_local_bound_rows_loaded",
            "result": "pass" if len(local_bound_rows) >= 12 and not missing_locks else "fail",
            "detail": f"local_bound_rows={len(local_bound_rows)};missing_lock_rows={len(missing_locks)}",
        },
        {
            "check_id": "V547_4_templates_complete",
            "result": "pass" if len(INPUT_TEMPLATE_ROWS) == 4 and len(THEOREM_CERTIFICATE_TEMPLATE_ROWS) == 5 else "fail",
            "detail": f"input_rows={len(INPUT_TEMPLATE_ROWS)};certificate_rows={len(THEOREM_CERTIFICATE_TEMPLATE_ROWS)}",
        },
        {
            "check_id": "V547_5_lock_map_and_PPN_context",
            "result": "pass" if len(local_locks) == 10 and len(ppn_vector) >= 10 else "fail",
            "detail": f"lock_rows={len(local_locks)};ppn_vector_rows={len(ppn_vector)}",
        },
        {
            "check_id": "V547_6_dryrun_no_claim_rows",
            "result": "pass" if not claim_input_rows and not claim_cert_rows and not claim_eval_rows and not gate_claim_rows else "fail",
            "detail": f"claim_input={len(claim_input_rows)};claim_cert={len(claim_cert_rows)};claim_eval={len(claim_eval_rows)};claim_gate={len(gate_claim_rows)}",
        },
        {
            "check_id": "V547_7_no_overclaim",
            "result": "pass" if not claim_input_rows and not claim_cert_rows and not claim_eval_rows and not gate_claim_rows else "fail",
            "detail": "BRR545_filled=false; source_measure=false; measured_GM=false; Newton=false; PPN=false; local_GR=false",
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
    local_locks: list[dict[str, Any]],
    evaluator_rows_out: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 547 - Y5 Boundary Reference Residual Input Template and Local Lock Map

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

`BRR545` is now executable once values or theorem certificates exist.

Nothing is filled yet. The important upgrade is that the missing boundary/reference term is no longer just a phrase. It is split into:

```text
epsilon_boundary_reference_abs
= epsilon_B_flux_abs + epsilon_Delta_symp_abs
= |B_zero_flux|/M_H_ref + |Delta_symp|/M_H_ref
```

with a separate `M_H_ref` measured-GM calibration gate. No cancellation credit is allowed.

## 2. Residual Input Template

{markdown_table(INPUT_TEMPLATE_ROWS)}

## 3. Theorem Certificate Template

{markdown_table(THEOREM_CERTIFICATE_TEMPLATE_ROWS)}

## 4. Local Lock Map

{markdown_table(local_locks)}

## 5. Evaluator Dry Run

{markdown_table(evaluator_rows_out)}

## 6. Acceptance Gates

{markdown_table(gates)}

## 7. Decision

{markdown_table(DECISION_ROWS)}

## 8. Source Register

{markdown_table(sources)}

## 9. Validation

{markdown_table(validations)}

## 10. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 11. Claim Ceiling

Allowed:

```text
MTS has an explicit BRR545 input template.
MTS has mapped BRR545 components to local locks.
MTS has a dry-run evaluator showing the rows are not claimable until filled.
```

Forbidden:

```text
MTS has filled BRR545.
MTS passes source-measure, measured GM, Newton, PPN, or local GR.
```

## 12. Practical Read

This is boring engineering in the best possible way. The local-GR branch now has a socket for the missing boundary/reference piece. Next we either plug in theorem certificates, or we plug in conservative numeric/profile bounds.

The first serious attempt should be theorem-first:

```text
reference lock -> boundary cohomology/no-hair -> projector silence -> measured denominator
```

If theorem-first fails, the fallback is not handwaving; it is the `BRI547` input table.

## 13. Next Target

`{NEXT_TARGET}`

Next: attempt the theorem certificates in order, starting with the reference-lock certificate. If that does not close, fill the first numeric/profile bound row rather than hiding the residual.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-boundary-reference-residual-input-template-and-local-lock-map"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    local_locks = local_lock_map_rows()
    evaluator_rows_out = evaluator_dryrun_rows(INPUT_TEMPLATE_ROWS)
    gates = acceptance_gate_rows(local_locks, evaluator_rows_out)
    validations = validation_rows(sources, local_locks, evaluator_rows_out, gates)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (INPUT_TEMPLATE_PATH, INPUT_TEMPLATE_ROWS),
        (THEOREM_CERTIFICATE_TEMPLATE_PATH, THEOREM_CERTIFICATE_TEMPLATE_ROWS),
        (LOCAL_LOCK_MAP_PATH, local_locks),
        (EVALUATOR_DRYRUN_PATH, evaluator_rows_out),
        (ACCEPTANCE_GATES_PATH, gates),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(generated_at_utc, run_dir, sources, local_locks, evaluator_rows_out, gates, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    claim_eval_rows = [row for row in evaluator_rows_out if row["valid_for_claim"] == "true"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "input_template": str(ROOT / INPUT_TEMPLATE_PATH),
        "theorem_certificate_template": str(ROOT / THEOREM_CERTIFICATE_TEMPLATE_PATH),
        "local_lock_map": str(ROOT / LOCAL_LOCK_MAP_PATH),
        "evaluator_dryrun": str(ROOT / EVALUATOR_DRYRUN_PATH),
        "acceptance_gates": str(ROOT / ACCEPTANCE_GATES_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "input_template_rows": len(INPUT_TEMPLATE_ROWS),
        "theorem_certificate_rows": len(THEOREM_CERTIFICATE_TEMPLATE_ROWS),
        "local_lock_rows": len(local_locks),
        "evaluator_rows": len(evaluator_rows_out),
        "claim_eval_rows": len(claim_eval_rows),
        "BRR545_input_template_written": True,
        "BRR545_values_filled": False,
        "BRR545_claim_ready": False,
        "source_measure_theorem_derived": False,
        "measured_GM_derived": False,
        "source_normalized_Newton_derived": False,
        "beta_equals_one_derived": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "github_push_performed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        "done\nprivate_no_github\nBRR545_input_template_and_local_lock_map_written_no_values_filled_no_Newton_PPN_or_local_GR_promotion\n",
        encoding="utf-8",
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
