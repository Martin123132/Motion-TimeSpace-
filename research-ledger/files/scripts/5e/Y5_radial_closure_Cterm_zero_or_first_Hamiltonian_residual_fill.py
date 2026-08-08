from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_radial_closure_Cterm_zero_failed_current_claim_first_Hamiltonian_radial_residual_fill_written"
CLAIM_CEILING = "radial_closure_Cterm_attempt_only_no_source_measure_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "556-Y5-extra-sector-Hamiltonian-charge-silence-or-channel-fill.md"

DOC_PATH = Path("555-Y5-radial-closure-Cterm-zero-or-first-Hamiltonian-residual-fill.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_555_SOURCE_REGISTER.csv")
RADIAL_CTERM_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_RADIAL_CTERM_THEOREM_ATTEMPT.csv")
RADIAL_CTERM_DECOMP_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_RADIAL_CTERM_DECOMPOSITION.csv")
BOUND_FILL_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_RADIAL_CTERM_BOUND_FILL_ROW.csv")
EVALUATOR_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_RADIAL_CTERM_EVALUATOR.csv")
OBSTRUCTION_LEDGER_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_555_OBSTRUCTION_LEDGER.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_555_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_555_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_555_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "554-Y5-Hamiltonian-charge-integrability-reference-lock-or-source-equality-fill.md",
        "role": "Hamiltonian integrability/source-equality failure and next C-term target",
    },
    {
        "source_file": "553-Y5-Hamiltonian-PiM-repair-clause-test-or-bound-fill.md",
        "role": "Hamiltonian PiM residual decomposition containing epsilon_HPiM_radial_closure_abs",
    },
    {
        "source_file": "541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md",
        "role": "Hamiltonian source-measure contract and residual inputs",
    },
    {
        "source_file": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
        "role": "GR-style worldtube source-measure and annulus charge reference route",
    },
    {
        "source_file": "506-local-EH-reduction-and-extra-sector-silence-theorem.md",
        "role": "local EH reduction and extra-sector silence requirements",
    },
    {
        "source_file": "504-parent-Hilbert-worldtube-glue-or-external-radial-input-plan.md",
        "role": "parent Noether charge route and original C-term decomposition",
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
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_REPAIR_RESIDUAL_DECOMPOSITION.csv",
        "role": "553 Hamiltonian PiM residual decomposition",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_REPAIR_BOUND_FILL_ROW.csv",
        "role": "553 total Hamiltonian PiM bound fill row",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_INTEGRABILITY_SOURCE_EQUALITY_FILL_ROWS.csv",
        "role": "554 first component fill rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_554_OBSTRUCTION_LEDGER.csv",
        "role": "554 C-term and extra-charge obstruction ledger",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_554_VALIDATION.csv",
        "role": "previous validation gate",
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
        "source_file": "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
        "role": "509 M_eff flux theorem attempt",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv",
        "role": "509 M_eff flux closure clauses",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
        "role": "509 M_eff flux residual map",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_LOCAL_ZERO_EXTRA_PREMISE_REQUIREMENTS.csv",
        "role": "extra-sector local-zero requirements",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_FIELD_SPECIFIC_SILENCE_ACCEPTANCE_GATES.csv",
        "role": "field-specific silence gates",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_EXTRA_MASS_CHANNELWISE_BOUND_INPUT.csv",
        "role": "Y5 extra-mass channelwise bound inputs",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv",
        "role": "domain/projector coefficient inputs",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_COMMUTATOR_PROJECTOR_BOUND_FILL_ROW.csv",
        "role": "projector commutator bound fill row",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_BOUNDARY_FLUX_BOUND_FILL_ROW.csv",
        "role": "boundary flux bound fill row",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_FILL_PACK.csv",
        "role": "boundary/reference first residual fill pack",
    },
    {
        "source_file": "scripts/Y5_radial_closure_Cterm_zero_or_first_Hamiltonian_residual_fill.py",
        "role": "this checkpoint generator",
    },
]


RADIAL_CTERM_ATTEMPT_ROWS = [
    {
        "step_id": "RCT555_0_target",
        "claim": "the Hamiltonian mass charge is radially closed between two linking spheres in a compact source-free annulus",
        "mathematical_form": "Delta_H_tau(S1,S2)=int_S2 Q_tau-int_S1 Q_tau=int_A dQ_tau=0",
        "current_result": "target_defined",
        "why_not_enough": "target definition is not a zero theorem for current MTS",
        "valid_for_claim": "false",
    },
    {
        "step_id": "RCT555_1_EH_reference",
        "claim": "EH/covariant-phase-space gravity gives a conditional reference route for annulus charge closure",
        "mathematical_form": "on shell J_tau=dQ_tau plus constraints; source-free stationary exterior and controlled boundary flux imply Delta_H_tau=0",
        "current_result": "known_conditional_reference",
        "why_not_enough": "MTS has not inherited the EH fixed point, symplectic current, and boundary/reference locks sector-by-sector",
        "valid_for_claim": "false",
    },
    {
        "step_id": "RCT555_2_C_EH_zero",
        "claim": "the EH constraint contribution vanishes in the local exterior",
        "mathematical_form": "C_EH[E_g,kappa,Delta_Lambda]=0",
        "current_result": "conditional_not_signed",
        "why_not_enough": "constant kappa, EH operator reduction, and subtraction/reference handling remain open for current MTS",
        "valid_for_claim": "false",
    },
    {
        "step_id": "RCT555_3_C_extra_zero",
        "claim": "non-EH/domain/memory/range/motion sectors carry no Hamiltonian mass charge through the annulus",
        "mathematical_form": "C_extra=sum_i C_i^extra=0",
        "current_result": "fail_current_claim",
        "why_not_enough": "extra-sector silence has gates and coefficient skeletons, not a parent theorem-zero certificate",
        "valid_for_claim": "false",
    },
    {
        "step_id": "RCT555_4_C_projector_zero",
        "claim": "the Hamiltonian mass projector is fixed through the annulus and does not generate commutator hair",
        "mathematical_form": "C_projector=[d,Pi_M^H]J_H + delta_domain(Pi_M^H)=0",
        "current_result": "fail_current_claim",
        "why_not_enough": "projector symplectic silence and Hamiltonian PiM equality remain residual/bound rows",
        "valid_for_claim": "false",
    },
    {
        "step_id": "RCT555_5_C_boundary_ref_zero",
        "claim": "boundary, side-flux, reference, and subtraction terms are fixed or vanish",
        "mathematical_form": "C_boundary+C_ref=0 with partial_r,t,source,frame B_ref=0",
        "current_result": "fail_current_claim",
        "why_not_enough": "boundary cohomology/no-hair and fixed-reference locks failed current claim",
        "valid_for_claim": "false",
    },
    {
        "step_id": "RCT555_6_verdict",
        "claim": "HPRD553_2 can be signed for current MTS",
        "mathematical_form": "epsilon_HPiM_radial_closure_abs=abs(int_A(C_EH+C_extra+C_projector+C_boundary+C_ref))/M_H_ref=0",
        "current_result": "fail_current_claim",
        "why_not_enough": "at least C_EH, C_extra, C_projector, C_boundary, and C_ref remain unzeroed or unbounded",
        "valid_for_claim": "false",
    },
]


RADIAL_CTERM_DECOMPOSITION_ROWS = [
    {
        "cterm_id": "CTD555_0_C_EH",
        "term": "C_EH_over_MH",
        "definition": "EH/constraint mismatch contribution to radial Hamiltonian charge closure",
        "zero_condition": "local exterior satisfies EH constraints with fixed kappa and allowed subtraction already locked",
        "current_status": "conditional_not_signed",
        "activated_residual": "epsilon_HPiM_radial_closure_abs;R11_EH_operator_ledger;R9_Gdot",
        "valid_for_claim": "false",
    },
    {
        "cterm_id": "CTD555_1_C_extra",
        "term": "C_extra_over_MH",
        "definition": "sum of non-EH/domain/memory/range/motion-sector Hamiltonian charge leakage through the annulus",
        "zero_condition": "each extra sector has theorem-zero silence or a source-backed channel coefficient bound",
        "current_status": "open_not_zero",
        "activated_residual": "epsilon_HPiM_extra_charge_abs;mu_extra;R10_fifth_force;R11_EH_operator_ledger",
        "valid_for_claim": "false",
    },
    {
        "cterm_id": "CTD555_2_C_projector",
        "term": "C_projector_over_MH",
        "definition": "variation/commutator leakage from Pi_M or Pi_M^H changing across radius, domain, or source frame",
        "zero_condition": "Pi_M^H is parent-owned, covariantly fixed, and equal to the source/readout mass map",
        "current_status": "open_not_zero",
        "activated_residual": "epsilon_projector_symplectic_abs;epsilon_HPiM_old_new_equivalence_abs",
        "valid_for_claim": "false",
    },
    {
        "cterm_id": "CTD555_3_C_boundary",
        "term": "C_boundary_over_MH",
        "definition": "side flux, inner/outer boundary, symplectic-boundary, or no-hair leakage",
        "zero_condition": "boundary/cohomology/nohair and zero side-flux theorem holds for the local branch",
        "current_status": "open_not_zero",
        "activated_residual": "epsilon_B_flux_abs;epsilon_Delta_symp_abs;R7_alpha3;R8_xi",
        "valid_for_claim": "false",
    },
    {
        "cterm_id": "CTD555_4_C_ref",
        "term": "C_ref_over_MH",
        "definition": "reference subtraction or background/Lambda subtraction dependence across source, radius, time, or frame",
        "zero_condition": "B_ref and subtraction branch are fixed/superselected and do not absorb source or readout changes",
        "current_status": "open_not_zero",
        "activated_residual": "epsilon_HPiM_integrability_abs;epsilon_Delta_symp_abs",
        "valid_for_claim": "false",
    },
    {
        "cterm_id": "CTD555_5_total",
        "term": "epsilon_HPiM_radial_closure_abs",
        "definition": "strict absolute radial Hamiltonian closure envelope",
        "zero_condition": "all component C terms are individually theorem-zero or source-backed below the relevant tolerance",
        "current_status": "unfilled",
        "activated_residual": "HPRD553_2_radial_closure",
        "valid_for_claim": "false",
    },
]


BOUND_FILL_ROWS = [
    {
        "fill_id": "FB555_0_HPiM_radial_Cterm_bound",
        "residual_component": "epsilon_HPiM_radial_closure_abs",
        "formula": "abs(C_EH_over_MH)+abs(C_extra_over_MH)+abs(C_projector_over_MH)+abs(C_boundary_over_MH)+abs(C_ref_over_MH)",
        "C_EH_over_MH": "MISSING_EH_CONSTRAINT_ZERO_OR_SOURCE_BACKED_BOUND",
        "C_extra_over_MH": "MISSING_EXTRA_SECTOR_ZERO_OR_CHANNEL_VECTOR",
        "C_projector_over_MH": "MISSING_PROJECTOR_COMMUTATOR_ZERO_OR_BOUND",
        "C_boundary_over_MH": "MISSING_BOUNDARY_NOFLUX_ZERO_OR_BOUND",
        "C_ref_over_MH": "MISSING_REFERENCE_SUBTRACTION_ZERO_OR_BOUND",
        "dln_Meff_dt": "MISSING_TIME_DRIFT_ZERO_OR_BOUND",
        "dln_Meff_dlnr": "MISSING_RADIAL_PROFILE_ZERO_OR_BOUND",
        "mapped_lock_rows": "R4_beta;R7_alpha3;R8_xi;R9_Gdot;R10_fifth_force;R11_EH_operator_ledger",
        "bound_rule": "each C-term must pass individually or theorem-zero; no cancellation credit between sectors",
        "source_file": "MISSING_SOURCE_FILE",
        "derivation_status": "unfilled_after_radial_Cterm_zero_failure",
        "valid_for_claim": "false",
    },
]


OBSTRUCTION_ROWS = [
    {
        "obstruction_id": "HRO555_0_EH_fixed_point_not_signed",
        "obstruction": "EH annulus closure is known as a reference route, but current MTS has not signed the EH fixed point and constant-kappa constraints",
        "activated_residual": "C_EH_over_MH;R11_EH_operator_ledger;R9_Gdot",
        "repair": "derive local EH reduction from parent action with fixed kappa/reference subtraction, or retain C_EH coefficient",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "HRO555_1_extra_sector_charge_silence_open",
        "obstruction": "extra fields may carry Hamiltonian mass charge through the source-free annulus",
        "activated_residual": "C_extra_over_MH;epsilon_HPiM_extra_charge_abs",
        "repair": "prove field-specific extra-sector charge silence, or fill channelwise coefficient vector",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "HRO555_2_projector_commutator_open",
        "obstruction": "Pi_M or Pi_M^H can vary with domain, radius, source frame, or symplectic branch",
        "activated_residual": "C_projector_over_MH;epsilon_projector_symplectic_abs;epsilon_HPiM_old_new_equivalence_abs",
        "repair": "derive parent-owned covariantly fixed Hamiltonian projector equality, or keep commutator bound",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "HRO555_3_boundary_reference_open",
        "obstruction": "boundary flux, cohomology, no-hair, and reference subtraction can shift the surface charge",
        "activated_residual": "C_boundary_over_MH;C_ref_over_MH;epsilon_B_flux_abs;epsilon_Delta_symp_abs",
        "repair": "prove no-flux and fixed-reference superselection, or fill boundary/reference residuals",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "HRO555_4_profile_data_missing",
        "obstruction": "no source-backed dln_Meff_dt or dln_Meff_dlnr profile is available as a fallback bound",
        "activated_residual": "dln_Meff_dt;dln_Meff_dlnr;epsilon_radial_Meff",
        "repair": "derive theorem-zero first; if that fails, fill radial/time profile inputs with source-backed data only",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "HRO555_5_local_GR_not_promotable",
        "obstruction": "radial closure is only one component of Hamiltonian PiM repair and does not by itself prove source equality, measured GM, Newton, PPN, or local GR",
        "activated_residual": "epsilon_HPiM_total_abs",
        "repair": "close all Hamiltonian PiM components before promoting local GR branch",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D555_0_radial_Cterm_zero_failed",
        "status": "radial_Cterm_zero_not_signed",
        "meaning": "current MTS cannot yet show the Hamiltonian surface charge is radially closed in the annulus",
        "claim_status": "epsilon_HPiM_radial_closure_abs_retained",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D555_1_reference_route_kept",
        "status": "EH_reference_route_kept_as_benchmark",
        "meaning": "the GR/EH annulus closure route remains the target structure, but MTS has not inherited it yet",
        "claim_status": "conditional_reference_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D555_2_fill_row_written",
        "status": "Hamiltonian_radial_Cterm_fill_row_written_unfilled",
        "meaning": "the radial-closure miss is now a strict component fill row instead of a vague plateau assumption",
        "claim_status": "template_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D555_3_local_GR_status",
        "status": "local_GR_still_closure_only",
        "meaning": "no source-measure, measured-GM, Newton, PPN, or local-GR promotion is earned",
        "claim_status": "local_GR_claim_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D555_4_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "HAMILTONIAN_RADIAL_CLOSURE",
        "previous_status": "open_inside_Hamiltonian_PiM_repair",
        "new_status": "attempted_failed_current_claim_Cterm_fill_row_written",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "HAMILTONIAN_PIM_REPAIR",
        "previous_status": "still_failed_first_two_component_rows_written",
        "new_status": "still_failed_integrability_source_equality_and_radial_Cterm_rows_written",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_MEASURE_THEOREM",
        "previous_status": "still_blocked_integrability_reference_and_source_equality_not_signed",
        "new_status": "still_blocked_radial_closure_also_not_signed",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "EXTRA_SECTOR_CHARGE_SILENCE",
        "previous_status": "open_Cterm_channel",
        "new_status": "next_highest_pressure_radial_Cterm_channel",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR_TRANSITION_ROUTE",
        "previous_status": "closure_only_integrability_and_source_equality_not_signed",
        "new_status": "closure_only_radial_Cterm_zero_not_signed",
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
            "notes": "fill only with theorem-zero C-term certificates or source-backed radial/Hamiltonian residual data",
        }
        for row in BOUND_FILL_ROWS
    ]


def validation_rows(sources: list[dict[str, Any]], eval_rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    prior_validation = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_554_VALIDATION.csv"))
    prior_fails = [row for row in prior_validation if row.get("result") == "fail"]
    repair_decomp = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_REPAIR_RESIDUAL_DECOMPOSITION.csv"))
    repair_bound = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_REPAIR_BOUND_FILL_ROW.csv"))
    previous_fill = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_INTEGRABILITY_SOURCE_EQUALITY_FILL_ROWS.csv"))
    previous_obstructions = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_554_OBSTRUCTION_LEDGER.csv"))
    parent_worldtube = read_csv(Path("source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv"))
    worldtube_theorem = read_csv(Path("source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv"))
    worldtube_clauses = read_csv(Path("source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_CLAUSES.csv"))
    meff_theorem = read_csv(Path("source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv"))
    meff_clauses = read_csv(Path("source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv"))
    meff_map = read_csv(Path("source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv"))
    extra_requirements = read_csv(Path("source-intake/mts_residuals/P8_LOCAL_ZERO_EXTRA_PREMISE_REQUIREMENTS.csv"))
    silence_gates = read_csv(Path("source-intake/mts_residuals/P8_FIELD_SPECIFIC_SILENCE_ACCEPTANCE_GATES.csv"))
    extra_inputs = read_csv(Path("source-intake/mts_residuals/P8_Y5_EXTRA_MASS_CHANNELWISE_BOUND_INPUT.csv"))
    domain_projector = read_csv(Path("source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv"))
    boundary_ref = read_csv(Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_FILL_PACK.csv"))
    claim_attempt_rows = [row for row in RADIAL_CTERM_ATTEMPT_ROWS if row["valid_for_claim"] == "true"]
    claim_decomp_rows = [row for row in RADIAL_CTERM_DECOMPOSITION_ROWS if row["valid_for_claim"] == "true"]
    claim_fill_rows = [row for row in BOUND_FILL_ROWS if row["valid_for_claim"] == "true"]
    claim_eval_rows = [row for row in eval_rows if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V555_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V555_1_prior_554_clean",
            "result": "pass" if len(prior_validation) == 10 and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_validation)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V555_2_HPiM_residual_rows_loaded",
            "result": "pass" if len(repair_decomp) == 7 and len(repair_bound) == 1 and len(previous_fill) == 2 and len(previous_obstructions) == 6 else "fail",
            "detail": f"repair_decomp={len(repair_decomp)};repair_bound={len(repair_bound)};previous_fill={len(previous_fill)};previous_obstructions={len(previous_obstructions)}",
        },
        {
            "check_id": "V555_3_worldtube_annulus_evidence_loaded",
            "result": "pass" if len(parent_worldtube) == 6 and len(worldtube_theorem) == 4 and len(worldtube_clauses) == 9 else "fail",
            "detail": f"parent_worldtube={len(parent_worldtube)};worldtube_theorem={len(worldtube_theorem)};worldtube_clauses={len(worldtube_clauses)}",
        },
        {
            "check_id": "V555_4_Meff_flux_evidence_loaded",
            "result": "pass" if len(meff_theorem) == 3 and len(meff_clauses) == 8 and len(meff_map) == 8 else "fail",
            "detail": f"meff_theorem={len(meff_theorem)};meff_clauses={len(meff_clauses)};meff_map={len(meff_map)}",
        },
        {
            "check_id": "V555_5_Cterm_support_loaded",
            "result": "pass" if len(extra_requirements) == 5 and len(silence_gates) == 3 and len(extra_inputs) == 9 and len(domain_projector) == 5 and len(boundary_ref) == 2 else "fail",
            "detail": f"extra_requirements={len(extra_requirements)};silence_gates={len(silence_gates)};extra_inputs={len(extra_inputs)};domain_projector={len(domain_projector)};boundary_ref={len(boundary_ref)}",
        },
        {
            "check_id": "V555_6_radial_attempt_complete",
            "result": "pass" if len(RADIAL_CTERM_ATTEMPT_ROWS) == 7 and len(RADIAL_CTERM_DECOMPOSITION_ROWS) == 6 else "fail",
            "detail": f"attempt_rows={len(RADIAL_CTERM_ATTEMPT_ROWS)};decomposition_rows={len(RADIAL_CTERM_DECOMPOSITION_ROWS)}",
        },
        {
            "check_id": "V555_7_fill_row_written",
            "result": "pass" if len(BOUND_FILL_ROWS) == 1 and len(eval_rows) == 1 else "fail",
            "detail": f"fill_rows={len(BOUND_FILL_ROWS)};evaluator_rows={len(eval_rows)}",
        },
        {
            "check_id": "V555_8_no_claim_rows",
            "result": "pass" if not claim_attempt_rows and not claim_decomp_rows and not claim_fill_rows and not claim_eval_rows else "fail",
            "detail": f"claim_attempt={len(claim_attempt_rows)};claim_decomp={len(claim_decomp_rows)};claim_fill={len(claim_fill_rows)};claim_eval={len(claim_eval_rows)}",
        },
        {
            "check_id": "V555_9_no_overclaim",
            "result": "pass" if not claim_attempt_rows and not claim_decomp_rows and not claim_fill_rows and not claim_eval_rows else "fail",
            "detail": "radial_Cterm_zero_signed=false; source_measure=false; measured_GM=false; Newton=false; PPN=false; local_GR=false",
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
    return f"""# 555 - Y5 Radial Closure C-Term Zero or First Hamiltonian Residual Fill

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The radial Hamiltonian closure gate does not pass yet.

The good news is that this is now a clean mathematical failure, not a vague local-vacuum plateau assumption. The required identity is:

```text
int_S2 Q_tau - int_S1 Q_tau
  = int_A (C_EH + C_extra + C_projector + C_boundary + C_ref).
```

For local GR recovery, the right-hand side must either vanish term-by-term or be bounded by source-backed residual data. Current MTS has neither, so `epsilon_HPiM_radial_closure_abs` remains live.

## 2. Radial C-Term Theorem Attempt

{markdown_table(RADIAL_CTERM_ATTEMPT_ROWS)}

## 3. C-Term Decomposition

{markdown_table(RADIAL_CTERM_DECOMPOSITION_ROWS)}

## 4. First Hamiltonian Radial Fill Row

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
MTS has attempted radial Hamiltonian C-term closure.
MTS has decomposed epsilon_HPiM_radial_closure_abs into C_EH, C_extra, C_projector, C_boundary, and C_ref.
MTS has written the first strict radial C-term fill row.
```

Forbidden:

```text
MTS has proved radial Hamiltonian charge closure.
MTS has derived epsilon_HPiM_radial_closure_abs = 0.
MTS has derived source-measure, measured GM, Newton, PPN, or local GR.
```

## 12. Practical Read

This is not grim in the "dead end" sense. It is grim in the useful engineering sense: the bridge has named missing bolts now. The next highest-pressure bolt is `C_extra`, because even if the EH reference route is imported cleanly, any extra-sector Hamiltonian charge hair kills the local-GR pass.

## 13. Next Target

`{NEXT_TARGET}`

Next: attack extra-sector Hamiltonian charge silence channel-by-channel, or write the first source-backed `C_extra` coefficient vector.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-radial-closure-Cterm-zero-or-first-Hamiltonian-residual-fill"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    eval_rows = evaluator_rows()
    validations = validation_rows(sources, eval_rows)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (RADIAL_CTERM_ATTEMPT_PATH, RADIAL_CTERM_ATTEMPT_ROWS),
        (RADIAL_CTERM_DECOMP_PATH, RADIAL_CTERM_DECOMPOSITION_ROWS),
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
        "radial_Cterm_attempt": str(ROOT / RADIAL_CTERM_ATTEMPT_PATH),
        "radial_Cterm_decomposition": str(ROOT / RADIAL_CTERM_DECOMP_PATH),
        "bound_fill": str(ROOT / BOUND_FILL_PATH),
        "evaluator": str(ROOT / EVALUATOR_PATH),
        "obstruction_ledger": str(ROOT / OBSTRUCTION_LEDGER_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "missing_sources": missing_sources,
        "failed_validations": failed_validations,
        "radial_Cterm_zero_signed": False,
        "epsilon_HPiM_radial_closure_zero_derived": False,
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
