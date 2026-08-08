from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_Hamiltonian_charge_integrability_reference_and_source_equality_failed_current_claim_first_fill_rows_written"
CLAIM_CEILING = "Hamiltonian_charge_integrability_reference_source_equality_attempt_only_no_BRR545_source_measure_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "555-Y5-radial-closure-Cterm-zero-or-first-Hamiltonian-residual-fill.md"

DOC_PATH = Path("554-Y5-Hamiltonian-charge-integrability-reference-lock-or-source-equality-fill.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_554_SOURCE_REGISTER.csv")
INTEGRABILITY_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_CHARGE_INTEGRABILITY_REFERENCE_ATTEMPT.csv")
SOURCE_EQUALITY_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_EQUALITY_ATTEMPT.csv")
BOUND_FILL_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_INTEGRABILITY_SOURCE_EQUALITY_FILL_ROWS.csv")
EVALUATOR_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_INTEGRABILITY_SOURCE_EQUALITY_EVALUATOR.csv")
OBSTRUCTION_LEDGER_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_554_OBSTRUCTION_LEDGER.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_554_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_554_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_554_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "553-Y5-Hamiltonian-PiM-repair-clause-test-or-bound-fill.md",
        "role": "Hamiltonian PiM repair failure and residual decomposition",
    },
    {
        "source_file": "552-Y5-parent-action-BRR545-zero-theorem-contract-or-first-repair-attempt.md",
        "role": "BRR545 parent-action zero theorem contract",
    },
    {
        "source_file": "541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md",
        "role": "Hamiltonian source-measure contract and residual rows",
    },
    {
        "source_file": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
        "role": "GR-style worldtube source-measure glue reference route",
    },
    {
        "source_file": "504-parent-Hilbert-worldtube-glue-or-external-radial-input-plan.md",
        "role": "parent Noether charge route and C-term closure ledger",
    },
    {
        "source_file": "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
        "role": "Hamiltonian boundary charge attempt and contract",
    },
    {
        "source_file": "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
        "role": "Hamiltonian charge to Poisson/Gauss calibration gate",
    },
    {
        "source_file": "450-Hilbert-source-to-measured-monopole-calibration-gate.md",
        "role": "Hilbert source to measured monopole calibration gate",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_REPAIR_CLAUSE_TEST.csv",
        "role": "553 repair clause tests",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_REPAIR_RESIDUAL_DECOMPOSITION.csv",
        "role": "553 Hamiltonian PiM residual decomposition",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_REPAIR_BOUND_FILL_ROW.csv",
        "role": "553 Hamiltonian PiM repair bound fill row",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_553_VALIDATION.csv",
        "role": "previous validation gate",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "role": "457 Hamiltonian boundary charge contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
        "role": "458 Poisson/Gauss calibration contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Hilbert_monopole_calibration_CONTRACT.csv",
        "role": "450 Hilbert monopole calibration contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
        "role": "504 worldtube glue theorem clauses",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
        "role": "510 worldtube source-measure theorem rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_CLAUSES.csv",
        "role": "510 required worldtube source-measure clauses",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
        "role": "541 Hamiltonian source-measure contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_RESIDUAL_INPUTS.csv",
        "role": "541 Hamiltonian source-measure residual inputs",
    },
    {
        "source_file": "scripts/Y5_Hamiltonian_charge_integrability_reference_lock_or_source_equality_fill.py",
        "role": "this checkpoint generator",
    },
]


INTEGRABILITY_ATTEMPT_ROWS = [
    {
        "step_id": "HCI554_0_target",
        "claim": "Q_tau defines a finite integrable Hamiltonian mass functional with fixed reference and fixed observed time generator",
        "mathematical_form": "delta H_tau = int_S(delta Q_tau - i_tau theta); delta^2 H_tau=0; partial_source,r,t,frame B_ref=0; delta tau=0",
        "current_result": "target_defined",
        "why_not_enough": "target definition is not a parent-action derivation",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HCI554_1_GR_reference_route",
        "claim": "EH/covariant-phase-space theory has a known conditional integrable charge route",
        "mathematical_form": "delta L=E delta phi+dtheta; J_tau=theta(phi,L_tau phi)-i_tau L; on shell J_tau=dQ_tau plus constraints",
        "current_result": "known_conditional_reference",
        "why_not_enough": "MTS has not inherited the EH symplectic charge and fixed boundary conditions sector-by-sector",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HCI554_2_parent_Lagrangian_theta_Q",
        "claim": "current MTS supplies explicit L, theta, Q_tau, and constraint decomposition for all BRR545-relevant fields",
        "mathematical_form": "S_parent[L(g,fields)]; theta_MTS; Q_tau^MTS; C_tau=C_EH+C_extra+C_projector+C_boundary+C_ref",
        "current_result": "not_derived",
        "why_not_enough": "the corpus has contracts and conditional routes, not a fully varied parent Lagrangian with all local sectors",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HCI554_3_reference_lock",
        "claim": "B_ref/reference subtraction is fixed once and cannot absorb source, radius, time, frame, or readout changes",
        "mathematical_form": "partial_t Delta_ref=partial_r Delta_ref=partial_source Delta_ref=partial_frame Delta_ref=0",
        "current_result": "fail_current_claim",
        "why_not_enough": "reference superselection was previously attempted and failed for current MTS; boundary/reference rows remain open",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HCI554_4_time_generator_lock",
        "claim": "tau is the same observed stationary/asymptotic/quasilocal time generator in source variation, charge, and readout",
        "mathematical_form": "tau_source=tau_charge=tau_orbit; delta tau=0 inside the local branch",
        "current_result": "open",
        "why_not_enough": "same observed time/coframe branch is not parent-derived for all MTS sectors",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HCI554_5_symplectic_boundary_flux",
        "claim": "extra symplectic and boundary flux terms vanish or are fixed topological constants",
        "mathematical_form": "int_boundary(delta Q_tau-i_tau theta)_extra=0 or fixed; B_zero_flux=0",
        "current_result": "fail_current_claim",
        "why_not_enough": "Delta_symp and B_zero_flux were retained in BRR545; boundary cohomology/no-hair and projector silence failed current claim",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HCI554_6_integrability_verdict",
        "claim": "HSM541_1 / HPT553_1 can be signed for current MTS",
        "mathematical_form": "epsilon_HPiM_integrability_abs=0",
        "current_result": "fail_current_claim",
        "why_not_enough": "missing explicit theta/Q_tau/B_ref/tau lock and zero symplectic-boundary flux theorem",
        "valid_for_claim": "false",
    },
]


SOURCE_EQUALITY_ATTEMPT_ROWS = [
    {
        "step_id": "HSE554_0_target",
        "claim": "worldtube source measure equals the same observed-frame Hamiltonian charge before orbital fitting",
        "mathematical_form": "M_source[W]=G_ref^-1 int_S Q_tau; W_source=supp(J_H[e_obs]); source_frame=readout_frame",
        "current_result": "target_defined",
        "why_not_enough": "target definition is not a source-measure theorem",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HSE554_1_dressed_source_guardrail",
        "claim": "M_source must be dressed Hamiltonian/Noether charge, not bare rest matter",
        "mathematical_form": "M_source[W]:=H_tau[S_outer]-H_ref; M_bare not equal by default",
        "current_result": "guardrail_pass",
        "why_not_enough": "guardrail prevents a false proof but does not prove current MTS source equality",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HSE554_2_same_observed_matter_coupling",
        "claim": "matter source, clocks, and orbital readout all couple to the same observed metric/coframe",
        "mathematical_form": "S_matter[psi,g_obs]; J_H[e_obs]; g_readout=g_obs at local branch",
        "current_result": "open",
        "why_not_enough": "same-frame/coframe theorem is still a contract, not a completed parent derivation",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HSE554_3_worldtube_linking_surfaces",
        "claim": "inner worldtube and outer linking surface read the same charge with no extra boundary or frame terms",
        "mathematical_form": "int_S Q_tau - M_source[W] = Delta_frame+Delta_cal+Delta_boundary+Delta_extra = 0",
        "current_result": "fail_current_claim",
        "why_not_enough": "Delta_frame, Delta_cal, Delta_boundary, and extra-sector charge rows remain open",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HSE554_4_Hilbert_current_equality",
        "claim": "Hamiltonian charge equals the parent Hilbert/source current mass channel",
        "mathematical_form": "G_ref^-1 int_S Q_tau = M_eff[Pi_M^H J_H] and delta H_tau=delta int_S Pi_M^H J_H",
        "current_result": "not_derived",
        "why_not_enough": "Hamiltonian PiM is a candidate definition, but same-frame Hilbert equality and old/new PiM residuals remain unproved",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HSE554_5_orbital_denominator_not_substitute",
        "claim": "orbital GM cannot be used as evidence for source equality before Gauss/readout theorem",
        "mathematical_form": "GM_orbit=G_ref M_source only after Poisson/Gauss/orbital readout",
        "current_result": "policy_pass",
        "why_not_enough": "policy blocks circular calibration; it does not fill Delta_cal",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HSE554_6_source_equality_verdict",
        "claim": "HSM541_2 / HPT553_2 can be signed for current MTS",
        "mathematical_form": "epsilon_HPiM_source_equality_abs=0",
        "current_result": "fail_current_claim",
        "why_not_enough": "same observed frame, source worldtube glue, and denominator calibration are not derived",
        "valid_for_claim": "false",
    },
]


BOUND_FILL_ROWS = [
    {
        "fill_id": "FB554_0_HPiM_integrability_reference_bound",
        "residual_component": "epsilon_HPiM_integrability_abs",
        "formula": "abs(delta_H_tau_nonintegrable_over_MH)+abs(Delta_ref_over_MH)+abs(symplectic_boundary_flux_over_MH)",
        "delta_H_tau_nonintegrable_over_MH": "MISSING_INTEGRABILITY_NUMERIC_OR_THEOREM_ZERO",
        "Delta_ref_over_MH": "MISSING_REFERENCE_NUMERIC_OR_THEOREM_ZERO",
        "symplectic_boundary_flux_over_MH": "MISSING_SYMPLECTIC_BOUNDARY_NUMERIC_OR_THEOREM_ZERO",
        "time_generator_lock": "MISSING_TAU_LOCK_CERTIFICATE",
        "mapped_lock_rows": "R3_gamma;R9_Gdot;R10_fifth_force;R11_EH_operator_ledger",
        "bound_rule": "integrability, reference, symplectic-boundary, and tau-lock terms must each pass or theorem-zero; no cancellation credit",
        "source_file": "MISSING_SOURCE_FILE",
        "derivation_status": "unfilled_after_integrability_reference_certificate_failure",
        "valid_for_claim": "false",
    },
    {
        "fill_id": "FB554_1_HPiM_source_equality_bound",
        "residual_component": "epsilon_HPiM_source_equality_abs",
        "formula": "abs(source_charge_mismatch_over_MH)+abs(Delta_frame_over_MH)+abs(Delta_cal_over_MH)",
        "source_charge_mismatch_over_MH": "MISSING_SOURCE_EQUALITY_NUMERIC_OR_THEOREM_ZERO",
        "Delta_frame_over_MH": "MISSING_FRAME_NUMERIC_OR_THEOREM_ZERO",
        "Delta_cal_over_MH": "MISSING_CALIBRATION_NUMERIC_OR_THEOREM_ZERO",
        "same_observed_frame_certificate": "MISSING_SAME_FRAME_CERTIFICATE",
        "mapped_lock_rows": "R1_WEP_source_charge;R9_Gdot;R11_EH_operator_ledger",
        "bound_rule": "source equality, frame, and calibration terms must each pass or theorem-zero; orbital GM cannot substitute for source equality",
        "source_file": "MISSING_SOURCE_FILE",
        "derivation_status": "unfilled_after_source_equality_certificate_failure",
        "valid_for_claim": "false",
    },
]


OBSTRUCTION_ROWS = [
    {
        "obstruction_id": "HCO554_0_no_parent_symplectic_current",
        "obstruction": "no explicit MTS parent theta/Q_tau/boundary symplectic current is available for all relevant local sectors",
        "activated_residual": "epsilon_HPiM_integrability_abs",
        "repair": "write or extract full parent Lagrangian, theta, Q_tau, and constraint decomposition",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "HCO554_1_reference_not_superselected",
        "obstruction": "reference subtraction can still carry source/radius/time/frame dependence",
        "activated_residual": "epsilon_HPiM_integrability_abs;epsilon_Delta_symp_abs",
        "repair": "derive B_ref from parent branch, topology, or fixed stationarity; otherwise fill Delta_ref row",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "HCO554_2_boundary_symplectic_flux_open",
        "obstruction": "delta Q_tau - i_tau theta can receive boundary/projector/non-EH contributions",
        "activated_residual": "epsilon_HPiM_integrability_abs;epsilon_B_flux_abs;epsilon_projector_variation",
        "repair": "zero boundary/projector symplectic flux or retain coefficients",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "HCO554_3_no_one_frame_theorem",
        "obstruction": "source worldtube, clocks, Hamiltonian charge, and orbital readout are not proven to share one observed frame",
        "activated_residual": "epsilon_HPiM_source_equality_abs;R1_WEP_source_charge",
        "repair": "derive one-observed-coframe matter/source theorem or fill Delta_frame row",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "HCO554_4_source_equality_not_Gauss",
        "obstruction": "source equality is upstream of Poisson/Gauss/orbital calibration and cannot be inferred from fitted GM",
        "activated_residual": "epsilon_HPiM_source_equality_abs;epsilon_HPiM_denominator_readout_abs",
        "repair": "prove worldtube source equality first, then Gauss/readout theorem",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "HCO554_5_Cterm_and_extra_charge_debt",
        "obstruction": "radial C-terms and extra-sector charge silence remain open after integrability/source equality attempt",
        "activated_residual": "epsilon_HPiM_radial_closure_abs;epsilon_HPiM_extra_charge_abs",
        "repair": "next target should attack C-term zero or fill radial/extracharge residuals",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D554_0_integrability_failed",
        "status": "integrability_reference_not_signed",
        "meaning": "current MTS cannot yet provide fixed-reference integrable Hamiltonian mass charge",
        "claim_status": "epsilon_HPiM_integrability_abs_retained",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D554_1_source_equality_failed",
        "status": "same_frame_source_equality_not_signed",
        "meaning": "worldtube source measure and Hamiltonian charge are not yet proved to be the same observed-frame source",
        "claim_status": "epsilon_HPiM_source_equality_abs_retained",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D554_2_fill_rows_written",
        "status": "first_two_HPiM_component_fill_rows_written_unfilled",
        "meaning": "integrability/reference and source-equality failures now have explicit component fill rows",
        "claim_status": "template_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D554_3_local_GR_status",
        "status": "local_GR_still_closure_only",
        "meaning": "no source-measure, measured-GM, Newton, PPN, or local-GR promotion is earned",
        "claim_status": "local_GR_claim_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D554_4_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "HAMILTONIAN_CHARGE_INTEGRABILITY",
        "previous_status": "open_inside_Hamiltonian_PiM_repair",
        "new_status": "attempted_failed_current_claim_integrability_reference_fill_row_written",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "HAMILTONIAN_SOURCE_EQUALITY",
        "previous_status": "open_inside_Hamiltonian_PiM_repair",
        "new_status": "attempted_failed_current_claim_source_equality_fill_row_written",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "HAMILTONIAN_PIM_REPAIR",
        "previous_status": "tested_failed_current_claim_residual_decomposition_written",
        "new_status": "still_failed_first_two_component_rows_written",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_MEASURE_THEOREM",
        "previous_status": "still_blocked_integrability_source_equality_and_denominator_readout_open",
        "new_status": "still_blocked_integrability_reference_and_source_equality_not_signed",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR_TRANSITION_ROUTE",
        "previous_status": "closure_only_Hamiltonian_PiM_repair_not_signed",
        "new_status": "closure_only_integrability_and_source_equality_not_signed",
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
            "notes": "fill only with theorem-zero certificate or source-backed charge/source-frame residual data",
        }
        for row in BOUND_FILL_ROWS
    ]


def validation_rows(sources: list[dict[str, Any]], eval_rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    prior_validation = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_553_VALIDATION.csv"))
    prior_fails = [row for row in prior_validation if row.get("result") == "fail"]
    repair_test = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_REPAIR_CLAUSE_TEST.csv"))
    repair_decomp = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_REPAIR_RESIDUAL_DECOMPOSITION.csv"))
    repair_bound = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_REPAIR_BOUND_FILL_ROW.csv"))
    hc_contract = read_csv(Path("source-intake/mts_residuals/P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv"))
    pg_contract = read_csv(Path("source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv"))
    hm_contract = read_csv(Path("source-intake/mts_residuals/P8_Hilbert_monopole_calibration_CONTRACT.csv"))
    worldtube_theorem = read_csv(Path("source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv"))
    worldtube_clauses = read_csv(Path("source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_CLAUSES.csv"))
    parent_worldtube = read_csv(Path("source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv"))
    hsm_contract = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv"))
    hsm_inputs = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_RESIDUAL_INPUTS.csv"))
    claim_integrability_rows = [row for row in INTEGRABILITY_ATTEMPT_ROWS if row["valid_for_claim"] == "true"]
    claim_source_rows = [row for row in SOURCE_EQUALITY_ATTEMPT_ROWS if row["valid_for_claim"] == "true"]
    claim_fill_rows = [row for row in BOUND_FILL_ROWS if row["valid_for_claim"] == "true"]
    claim_eval_rows = [row for row in eval_rows if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V554_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V554_1_prior_553_clean",
            "result": "pass" if len(prior_validation) == 10 and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_validation)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V554_2_553_repair_rows_loaded",
            "result": "pass" if len(repair_test) == 8 and len(repair_decomp) == 7 and len(repair_bound) == 1 else "fail",
            "detail": f"repair_test={len(repair_test)};repair_decomp={len(repair_decomp)};repair_bound={len(repair_bound)}",
        },
        {
            "check_id": "V554_3_Hamiltonian_contracts_loaded",
            "result": "pass" if len(hc_contract) == 10 and len(pg_contract) == 11 and len(hm_contract) == 9 else "fail",
            "detail": f"HC={len(hc_contract)};PG={len(pg_contract)};HM={len(hm_contract)}",
        },
        {
            "check_id": "V554_4_worldtube_evidence_loaded",
            "result": "pass" if len(worldtube_theorem) == 4 and len(worldtube_clauses) == 9 and len(parent_worldtube) == 6 else "fail",
            "detail": f"worldtube_theorem={len(worldtube_theorem)};worldtube_clauses={len(worldtube_clauses)};parent_worldtube={len(parent_worldtube)}",
        },
        {
            "check_id": "V554_5_source_measure_contract_loaded",
            "result": "pass" if len(hsm_contract) == 8 and len(hsm_inputs) == 7 else "fail",
            "detail": f"hsm_contract={len(hsm_contract)};hsm_inputs={len(hsm_inputs)}",
        },
        {
            "check_id": "V554_6_theorem_attempts_complete",
            "result": "pass" if len(INTEGRABILITY_ATTEMPT_ROWS) == 7 and len(SOURCE_EQUALITY_ATTEMPT_ROWS) == 7 else "fail",
            "detail": f"integrability_rows={len(INTEGRABILITY_ATTEMPT_ROWS)};source_equality_rows={len(SOURCE_EQUALITY_ATTEMPT_ROWS)}",
        },
        {
            "check_id": "V554_7_fill_rows_written",
            "result": "pass" if len(BOUND_FILL_ROWS) == 2 and len(eval_rows) == 2 else "fail",
            "detail": f"fill_rows={len(BOUND_FILL_ROWS)};evaluator_rows={len(eval_rows)}",
        },
        {
            "check_id": "V554_8_no_claim_rows",
            "result": "pass" if not claim_integrability_rows and not claim_source_rows and not claim_fill_rows and not claim_eval_rows else "fail",
            "detail": f"claim_integrability={len(claim_integrability_rows)};claim_source={len(claim_source_rows)};claim_fill={len(claim_fill_rows)};claim_eval={len(claim_eval_rows)}",
        },
        {
            "check_id": "V554_9_no_overclaim",
            "result": "pass" if not claim_integrability_rows and not claim_source_rows and not claim_fill_rows and not claim_eval_rows else "fail",
            "detail": "integrability_reference_signed=false; source_equality_signed=false; source_measure=false; measured_GM=false; Newton=false; PPN=false; local_GR=false",
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
    return f"""# 554 - Y5 Hamiltonian Charge Integrability Reference Lock or Source Equality Fill

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The Hamiltonian charge route still looks like the right GR-shaped road, but current MTS cannot yet drive on it.

Two first gates were tested:

```text
1. fixed-reference integrable Hamiltonian charge;
2. same-frame worldtube source equality.
```

Both fail for current claim. The good news is sharp: the failures are now split into two fill rows rather than one foggy "mass charge" problem.

## 2. Integrability and Reference Attempt

{markdown_table(INTEGRABILITY_ATTEMPT_ROWS)}

## 3. Source Equality Attempt

{markdown_table(SOURCE_EQUALITY_ATTEMPT_ROWS)}

## 4. Fill Rows

{markdown_table(BOUND_FILL_ROWS)}

## 5. Evaluator

{markdown_table(eval_rows)}

## 6. Obstruction Ledger

{markdown_table(OBSTRUCTION_ROWS)}

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
MTS has attempted the Hamiltonian charge integrability/reference gate.
MTS has attempted the same-frame worldtube source-equality gate.
MTS has fill rows for epsilon_HPiM_integrability_abs and epsilon_HPiM_source_equality_abs.
```

Forbidden:

```text
MTS has signed Hamiltonian charge integrability/reference lock.
MTS has signed same-frame source equality.
MTS has derived source-measure, measured GM, Newton, PPN, or local GR.
```

## 12. Practical Read

This is where the boxing match is useful: we did not need a knockout today. We needed clean footwork. The charge route is still alive, but now the judges have two exact scorecards: reference/integrability and source equality. Each must either become a theorem-zero certificate or a source-backed residual.

## 13. Next Target

`{NEXT_TARGET}`

Next: attack radial closure C-terms, because even a clean charge and source equality would still fail if C_extra, C_projector, C_boundary, or C_ref survive in the annulus.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-Hamiltonian-charge-integrability-reference-lock-or-source-equality-fill"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    eval_rows = evaluator_rows()
    validations = validation_rows(sources, eval_rows)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (INTEGRABILITY_ATTEMPT_PATH, INTEGRABILITY_ATTEMPT_ROWS),
        (SOURCE_EQUALITY_ATTEMPT_PATH, SOURCE_EQUALITY_ATTEMPT_ROWS),
        (BOUND_FILL_PATH, BOUND_FILL_ROWS),
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
        "integrability_attempt": str(ROOT / INTEGRABILITY_ATTEMPT_PATH),
        "source_equality_attempt": str(ROOT / SOURCE_EQUALITY_ATTEMPT_PATH),
        "bound_fill": str(ROOT / BOUND_FILL_PATH),
        "evaluator": str(ROOT / EVALUATOR_PATH),
        "obstruction_ledger": str(ROOT / OBSTRUCTION_LEDGER_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "integrability_attempt_rows": len(INTEGRABILITY_ATTEMPT_ROWS),
        "source_equality_attempt_rows": len(SOURCE_EQUALITY_ATTEMPT_ROWS),
        "bound_fill_rows": len(BOUND_FILL_ROWS),
        "evaluator_rows": len(eval_rows),
        "Hamiltonian_integrability_reference_signed": False,
        "Hamiltonian_source_equality_signed": False,
        "epsilon_HPiM_integrability_abs_filled": False,
        "epsilon_HPiM_source_equality_abs_filled": False,
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
        "done\nprivate_no_github\nHamiltonian_charge_integrability_reference_and_source_equality_failed_current_claim_first_fill_rows_written_no_Newton_PPN_or_local_GR_promotion\n",
        encoding="utf-8",
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
