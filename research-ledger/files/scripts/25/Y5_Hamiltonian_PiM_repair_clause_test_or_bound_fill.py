from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_Hamiltonian_PiM_repair_clause_failed_current_claim_residual_decomposition_and_bound_row_written"
CLAIM_CEILING = "Hamiltonian_PiM_repair_clause_test_and_bound_row_only_no_BRR545_source_measure_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "554-Y5-Hamiltonian-charge-integrability-reference-lock-or-source-equality-fill.md"

DOC_PATH = Path("553-Y5-Hamiltonian-PiM-repair-clause-test-or-bound-fill.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_553_SOURCE_REGISTER.csv")
REPAIR_TEST_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_REPAIR_CLAUSE_TEST.csv")
RESIDUAL_DECOMPOSITION_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_REPAIR_RESIDUAL_DECOMPOSITION.csv")
BOUND_FILL_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_REPAIR_BOUND_FILL_ROW.csv")
EVALUATOR_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_REPAIR_EVALUATOR.csv")
OBSTRUCTION_LEDGER_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_REPAIR_OBSTRUCTION_LEDGER.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_553_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_553_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_553_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "552-Y5-parent-action-BRR545-zero-theorem-contract-or-first-repair-attempt.md",
        "role": "BRR545 parent-action zero theorem contract and selected Hamiltonian PiM repair candidate",
    },
    {
        "source_file": "541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md",
        "role": "Hamiltonian PiM source-measure scorecard and residual input rows",
    },
    {
        "source_file": "540-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test.md",
        "role": "Hamiltonian PiM source-measure and PPN readout tests",
    },
    {
        "source_file": "539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md",
        "role": "Hamiltonian PiM branch definition and topological PiM demotion",
    },
    {
        "source_file": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
        "role": "GR-style Hamiltonian/Noether source-measure glue and M_eff residual runner",
    },
    {
        "source_file": "504-parent-Hilbert-worldtube-glue-or-external-radial-input-plan.md",
        "role": "parent Noether mass-charge route and radial closure C-term ledger",
    },
    {
        "source_file": "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
        "role": "Hamiltonian charge to Poisson/Gauss calibration contract",
    },
    {
        "source_file": "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
        "role": "Hamiltonian boundary charge contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_PARENT_ACTION_ZERO_THEOREM_CONTRACT.csv",
        "role": "552 BRR545 parent-action zero theorem contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_FIRST_REPAIR_ATTEMPT.csv",
        "role": "552 first repair attempt rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_552_VALIDATION.csv",
        "role": "previous validation gate",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PIM_HAMILTONIAN_BRANCH_DEFINITION.csv",
        "role": "539 Hamiltonian PiM branch definition rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PIM_HAMILTONIAN_GATE_RESULTS.csv",
        "role": "539 Hamiltonian PiM gate results",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
        "role": "541 source-measure contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_SCORECARD.csv",
        "role": "541 source-measure scorecard",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_RESIDUAL_INPUTS.csv",
        "role": "541 residual input rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_RESIDUAL_ACTIVATION.csv",
        "role": "540 residual activation map",
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
        "source_file": "source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
        "role": "504 worldtube glue theorem clauses",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_COMMUTATOR_PROJECTOR_BOUND_FILL_ROW.csv",
        "role": "550 commutator/projector bound fill row",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_RESIDUAL_ENVELOPE.csv",
        "role": "551 strict BRR545 residual envelope",
    },
    {
        "source_file": "scripts/Y5_Hamiltonian_PiM_repair_clause_test_or_bound_fill.py",
        "role": "this checkpoint generator",
    },
]


REPAIR_TEST_ROWS = [
    {
        "test_id": "HPT553_0_definition_level_repair",
        "repair_clause": "replace independent Pi_M with Hamiltonian charge representative",
        "mathematical_form": "ell_H[S,tau]=int_S Q_tau; Pi_M^H J_H=ell_H[J_H;tau,S] omega_M^H",
        "current_result": "allowed_as_candidate_definition",
        "why_not_claim": "definition-level repair does not prove integrability, source equality, radial closure, or readout",
        "residual_if_fail": "R_Htop;R_eq;I_commutator",
        "valid_for_claim": "false",
    },
    {
        "test_id": "HPT553_1_integrable_charge",
        "repair_clause": "Q_tau gives a finite integrable Hamiltonian with fixed reference and time generator",
        "mathematical_form": "delta H_tau=int_S(delta Q_tau-i_tau theta) with path-independent integral and fixed B_ref,tau",
        "current_result": "fail_current_claim",
        "why_not_claim": "current MTS has no fully explicit parent Lagrangian, theta, Q_tau, reference subtraction, and integrability proof",
        "residual_if_fail": "epsilon_HPiM_integrability_abs;epsilon_Delta_symp_abs",
        "valid_for_claim": "false",
    },
    {
        "test_id": "HPT553_2_same_frame_source",
        "repair_clause": "Hamiltonian charge reads the same observed Hilbert/worldtube source current before orbital fitting",
        "mathematical_form": "W_source=supp(J_H[e_obs]); M_source[W]=G_ref^-1 int_S Q_tau",
        "current_result": "fail_current_claim",
        "why_not_claim": "same-frame worldtube source-measure glue is known as a GR-style route but not inherited for current MTS",
        "residual_if_fail": "epsilon_HPiM_source_equality_abs;Delta_frame;Delta_cal",
        "valid_for_claim": "false",
    },
    {
        "test_id": "HPT553_3_radial_closure",
        "repair_clause": "Hamiltonian mass charge is closed in compact source-free exterior",
        "mathematical_form": "int_S2 Q_tau-int_S1 Q_tau=int_A(C_EH+C_extra+C_projector+C_boundary+C_ref)=0",
        "current_result": "fail_current_claim",
        "why_not_claim": "C_extra, C_projector, C_boundary, and reference terms are not field-specific zeroed",
        "residual_if_fail": "epsilon_HPiM_radial_closure_abs;epsilon_radial_Meff;dln_Meff",
        "valid_for_claim": "false",
    },
    {
        "test_id": "HPT553_4_projector_variation_removed",
        "repair_clause": "independent Hodge/topological Pi_M variation is eliminated or demoted",
        "mathematical_form": "old Pi_M is absent from S_parent or Pi_M^old J_H=Pi_M^H J_H+dB_zero+R_Htop",
        "current_result": "partial_repair_policy_only",
        "why_not_claim": "old Pi_M can be demoted, but old-new equality and zero boundary flux are not proved",
        "residual_if_fail": "epsilon_HPiM_old_PiM_equivalence_abs;epsilon_projector_variation",
        "valid_for_claim": "false",
    },
    {
        "test_id": "HPT553_5_no_extra_charge",
        "repair_clause": "extra MTS sectors carry no independent Hamiltonian mass charge",
        "mathematical_form": "Delta_nonEH=Delta_extra=Delta_frame=Delta_boundary=Delta_projector=0 or individually bounded",
        "current_result": "fail_current_claim",
        "why_not_claim": "field-specific silence/source-charge proofs remain open",
        "residual_if_fail": "mu_extra;Delta_nonEH;Delta_extra;Delta_projector",
        "valid_for_claim": "false",
    },
    {
        "test_id": "HPT553_6_denominator_and_Gauss_readout",
        "repair_clause": "same charge is the positive M_H_ref denominator and the orbital inverse-square source",
        "mathematical_form": "M_H_ref=G_ref^-1 int_S Q_tau; GM_orbit=G_ref M_H_ref; a_r=-G_ref M_H_ref/r^2",
        "current_result": "fail_current_claim",
        "why_not_claim": "Poisson/Gauss/orbital readout and PPN followthrough are not derived",
        "residual_if_fail": "epsilon_MHref_calibration_abs;Delta_cal;alpha_lambda;PPN_vector",
        "valid_for_claim": "false",
    },
    {
        "test_id": "HPT553_7_repair_verdict",
        "repair_clause": "Hamiltonian PiM repair closes BZTC552_4 for current MTS",
        "mathematical_form": "HPT553_0..HPT553_6 all pass componentwise",
        "current_result": "fail_current_claim",
        "why_not_claim": "repair is conceptually right but currently shifts the proof debt into integrability, source-measure, closure, and readout",
        "residual_if_fail": "epsilon_HPiM_total_abs",
        "valid_for_claim": "false",
    },
]


RESIDUAL_DECOMPOSITION_ROWS = [
    {
        "residual_id": "HPRD553_0_integrability",
        "symbol": "epsilon_HPiM_integrability_abs",
        "definition": "failure of Q_tau to define an integrable fixed-reference Hamiltonian mass functional",
        "formula": "abs(delta_H_tau_nonintegrable_over_MH)+abs(Delta_ref_over_MH)",
        "mapped_locks": "R3_gamma;R9_Gdot;R10_fifth_force;R11_EH_operator_ledger",
        "required_input": "delta_H_tau_nonintegrable_over_MH;Delta_ref_over_MH;source_file;assumptions",
        "current_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "HPRD553_1_source_equality",
        "symbol": "epsilon_HPiM_source_equality_abs",
        "definition": "worldtube source measure differs from the Hamiltonian charge in the observed source frame",
        "formula": "abs(M_source_W-G_ref^-1 int_S Q_tau)/M_H_ref",
        "mapped_locks": "R1_WEP_source_charge;R9_Gdot;R11_EH_operator_ledger",
        "required_input": "source_frame;readout_frame;source_charge_mismatch_over_MH;Delta_frame;Delta_cal",
        "current_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "HPRD553_2_radial_closure",
        "symbol": "epsilon_HPiM_radial_closure_abs",
        "definition": "finite annulus Hamiltonian mass charge is not closed",
        "formula": "abs(int_A(C_EH+C_extra+C_projector+C_boundary+C_ref))/M_H_ref",
        "mapped_locks": "R4_beta;R7_alpha3;R8_xi;R9_Gdot;R10_fifth_force;R11_EH_operator_ledger",
        "required_input": "C_EH_over_MH;C_extra_over_MH;C_projector_over_MH;C_boundary_over_MH;C_ref_over_MH",
        "current_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "HPRD553_3_old_PiM_equivalence",
        "symbol": "epsilon_HPiM_old_PiM_equivalence_abs",
        "definition": "old/topological/Hodge Pi_M differs from Hamiltonian Pi_M representative",
        "formula": "abs(int_S(Pi_M_old J_H-Pi_M^H J_H-dB_zero))/M_H_ref",
        "mapped_locks": "R3_gamma;R4_beta;R7_alpha3;R8_xi;R11_EH_operator_ledger",
        "required_input": "old_new_PiM_mismatch_over_MH;B_zero_flux_over_MH;projector_variation_over_MH",
        "current_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "HPRD553_4_extra_charge",
        "symbol": "epsilon_HPiM_extra_charge_abs",
        "definition": "non-EH/domain/memory/range/frame/boundary/projector sectors carry independent Hamiltonian mass charge",
        "formula": "sum_i abs(Delta_i_over_MH)",
        "mapped_locks": "R1_WEP_source_charge;R4_beta;R7_alpha3;R8_xi;R9_Gdot;R10_fifth_force;R11_EH_operator_ledger",
        "required_input": "channel;Delta_charge_over_MH;coefficient_to_lock;source_file",
        "current_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "HPRD553_5_denominator_readout",
        "symbol": "epsilon_HPiM_denominator_readout_abs",
        "definition": "Hamiltonian charge does not calibrate to the positive same-frame orbital measured-GM denominator",
        "formula": "abs(G_ref*M_H_ref/GM_orbit-1)+readout_residuals",
        "mapped_locks": "R1_WEP_source_charge;R3_gamma;R4_beta;R9_Gdot;R10_fifth_force;R11_EH_operator_ledger",
        "required_input": "GM_orbit;M_H_ref;Delta_cal;alpha_lambda;partial_r_ln_mu_obs;PPN_vector",
        "current_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "HPRD553_6_total_no_cancellation",
        "symbol": "epsilon_HPiM_total_abs",
        "definition": "strict absolute envelope for the Hamiltonian PiM repair branch",
        "formula": "sum_abs(HPRD553_0..HPRD553_5)",
        "mapped_locks": "R1_WEP_source_charge;R3_gamma;R4_beta;R7_alpha3;R8_xi;R9_Gdot;R10_fifth_force;R11_EH_operator_ledger",
        "required_input": "all component rows theorem-zero or source-backed; no cancellation credit",
        "current_status": "not_computable",
        "valid_for_claim": "false",
    },
]


BOUND_FILL_ROWS = [
    {
        "fill_id": "FB553_0_Hamiltonian_PiM_repair_bound",
        "residual_component": "epsilon_HPiM_total_abs",
        "formula": "abs(delta_H_tau_nonintegrable_over_MH)+abs(source_charge_mismatch_over_MH)+abs(radial_closure_over_MH)+abs(old_new_PiM_mismatch_over_MH)+sum_abs(extra_charge_over_MH)+abs(denominator_readout_over_MH)",
        "delta_H_tau_nonintegrable_over_MH": "MISSING_INTEGRABILITY_NUMERIC_OR_THEOREM_ZERO",
        "source_charge_mismatch_over_MH": "MISSING_SOURCE_EQUALITY_NUMERIC_OR_THEOREM_ZERO",
        "radial_closure_over_MH": "MISSING_RADIAL_CTERM_NUMERIC_OR_THEOREM_ZERO",
        "old_new_PiM_mismatch_over_MH": "MISSING_OLD_NEW_PIM_EQUIVALENCE_NUMERIC_OR_THEOREM_ZERO",
        "extra_charge_over_MH": "MISSING_EXTRA_CHANNEL_VECTOR_OR_THEOREM_ZERO",
        "denominator_readout_over_MH": "MISSING_GAUSS_ORBITAL_DENOMINATOR_NUMERIC_OR_THEOREM_ZERO",
        "mapped_lock_rows": "R1_WEP_source_charge;R3_gamma;R4_beta;R7_alpha3;R8_xi;R9_Gdot;R10_fifth_force;R11_EH_operator_ledger",
        "bound_rule": "every component must pass individually or theorem-zero; no cancellation credit and no bare-mass/orbital-GM substitution",
        "source_file": "MISSING_SOURCE_FILE",
        "derivation_status": "unfilled_after_Hamiltonian_PiM_repair_clause_failure",
        "valid_for_claim": "false",
    }
]


OBSTRUCTION_ROWS = [
    {
        "obstruction_id": "HPO553_0_definition_not_theorem",
        "obstruction": "defining Pi_M^H by Q_tau solves naming but not integrability, equality, or readout",
        "activated_residual": "epsilon_HPiM_total_abs",
        "repair": "derive Q_tau from explicit parent action and prove HPT553_1-HPT553_6",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "HPO553_1_reference_boundary_integrability",
        "obstruction": "Hamiltonian charge depends on fixed boundary/reference terms that remain open",
        "activated_residual": "epsilon_HPiM_integrability_abs;epsilon_Delta_symp_abs;epsilon_B_flux_abs",
        "repair": "derive fixed B_ref/tau and zero relative boundary flux or fill source-backed boundary/reference rows",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "HPO553_2_same_source_frame",
        "obstruction": "source worldtube, Hamiltonian charge, clocks, and orbital readout are not yet proven to use one observed frame",
        "activated_residual": "epsilon_HPiM_source_equality_abs;Delta_frame;Delta_cal;R1_WEP_source_charge",
        "repair": "one observed coframe theorem plus dressed source-charge definition",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "HPO553_3_C_terms_not_zero",
        "obstruction": "C_extra/C_projector/C_boundary/C_ref are not all zeroed in the compact source-free exterior",
        "activated_residual": "epsilon_HPiM_radial_closure_abs;mu_extra;Gdot;alpha3;xi",
        "repair": "field-specific silence/nohair/source-free operator proofs or channelwise coefficient vectors",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "HPO553_4_old_PiM_equivalence",
        "obstruction": "old/topological/Hodge Pi_M can be demoted, but equality to Pi_M^H is not proved",
        "activated_residual": "epsilon_HPiM_old_PiM_equivalence_abs;epsilon_projector_variation",
        "repair": "prove old Pi_M absent from parent action or equal to Pi_M^H up to exact zero-flux term",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "HPO553_5_readout_not_reached",
        "obstruction": "even a clean Q_tau would still need Poisson/Gauss/orbital and PPN readout from the same action",
        "activated_residual": "epsilon_HPiM_denominator_readout_abs;PPN_vector",
        "repair": "derive weak-field metric expansion and local PPN vector after source-measure closes",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D553_0_repair_test_failed",
        "status": "Hamiltonian_PiM_repair_not_signed",
        "meaning": "Hamiltonian PiM is still the best repair candidate but does not currently close BZTC552_4",
        "claim_status": "candidate_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D553_1_partial_repair_kept",
        "status": "independent_PiM_demoted_policy_kept",
        "meaning": "old independent/topological/readout PiM earns no proof credit unless equal to PiM^H or bounded",
        "claim_status": "policy_pass_not_theorem",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D553_2_bound_row_written",
        "status": "epsilon_HPiM_total_abs_bound_row_written_unfilled",
        "meaning": "failed repair now has a strict fill row covering integrability, source equality, radial closure, old PiM equivalence, extra charge, and readout",
        "claim_status": "template_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D553_3_local_GR_status",
        "status": "local_GR_still_closure_only",
        "meaning": "no measured-GM, Newton, PPN, or local-GR promotion is earned",
        "claim_status": "local_GR_claim_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D553_4_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "HAMILTONIAN_PIM_REPAIR",
        "previous_status": "selected_as_first_repair_clause_to_test",
        "new_status": "tested_failed_current_claim_residual_decomposition_written",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "BRR545_PROJECTOR_SYMPLECTIC",
        "previous_status": "epsilon_projector_symplectic_abs_retained_with_first_bound_fill_row",
        "new_status": "retained_plus_Hamiltonian_PiM_residual_envelope",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_MEASURE_THEOREM",
        "previous_status": "still_blocked_until_Hamiltonian_PiM_worldtube_denominator_clause_passes",
        "new_status": "still_blocked_integrability_source_equality_and_denominator_readout_open",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR_TRANSITION_ROUTE",
        "previous_status": "closure_only_but_with_exact_parent_action_contract",
        "new_status": "closure_only_Hamiltonian_PiM_repair_not_signed",
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
    rows: list[dict[str, Any]] = []
    for row in BOUND_FILL_ROWS:
        rows.append(
            {
                "fill_id": row["fill_id"],
                "residual_component": row["residual_component"],
                "numeric_status": "not_computed_missing_integrability_source_equality_radial_closure_old_PiM_equivalence_extra_charge_and_readout_values",
                "mapped_lock_rows": row["mapped_lock_rows"],
                "pass_status": "not_claimable",
                "valid_for_claim": "false",
                "notes": "Hamiltonian PiM repair clause failed current claim; fill only with theorem-zero or source-backed charge/readout residual data",
            }
        )
    return rows


def validation_rows(sources: list[dict[str, Any]], eval_rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    prior_validation = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_552_VALIDATION.csv"))
    prior_fails = [row for row in prior_validation if row.get("result") == "fail"]
    zero_contract = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_PARENT_ACTION_ZERO_THEOREM_CONTRACT.csv"))
    first_repair = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_FIRST_REPAIR_ATTEMPT.csv"))
    branch_definition = read_csv(Path("source-intake/mts_residuals/P8_Y5_PIM_HAMILTONIAN_BRANCH_DEFINITION.csv"))
    hamiltonian_gates = read_csv(Path("source-intake/mts_residuals/P8_Y5_PIM_HAMILTONIAN_GATE_RESULTS.csv"))
    source_contract = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv"))
    source_scorecard = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_SCORECARD.csv"))
    source_inputs = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_RESIDUAL_INPUTS.csv"))
    residual_activation = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_RESIDUAL_ACTIVATION.csv"))
    hc_contract = read_csv(Path("source-intake/mts_residuals/P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv"))
    pg_contract = read_csv(Path("source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv"))
    worldtube = read_csv(Path("source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv"))
    brr_bound = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_COMMUTATOR_PROJECTOR_BOUND_FILL_ROW.csv"))
    brr_envelope = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_RESIDUAL_ENVELOPE.csv"))
    claim_test_rows = [row for row in REPAIR_TEST_ROWS if row["valid_for_claim"] == "true"]
    claim_decomp_rows = [row for row in RESIDUAL_DECOMPOSITION_ROWS if row["valid_for_claim"] == "true"]
    claim_bound_rows = [row for row in BOUND_FILL_ROWS if row["valid_for_claim"] == "true"]
    claim_eval_rows = [row for row in eval_rows if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V553_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V553_1_prior_552_clean",
            "result": "pass" if len(prior_validation) == 9 and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_validation)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V553_2_552_contract_loaded",
            "result": "pass" if len(zero_contract) == 9 and len(first_repair) == 5 else "fail",
            "detail": f"zero_contract={len(zero_contract)};first_repair={len(first_repair)}",
        },
        {
            "check_id": "V553_3_Hamiltonian_PiM_evidence_loaded",
            "result": "pass" if len(branch_definition) == 5 and len(hamiltonian_gates) == 7 else "fail",
            "detail": f"branch_definition={len(branch_definition)};hamiltonian_gates={len(hamiltonian_gates)}",
        },
        {
            "check_id": "V553_4_source_measure_evidence_loaded",
            "result": "pass"
            if len(source_contract) == 8
            and len(source_scorecard) == 8
            and len(source_inputs) == 7
            and len(residual_activation) == 7
            else "fail",
            "detail": f"source_contract={len(source_contract)};source_scorecard={len(source_scorecard)};source_inputs={len(source_inputs)};residual_activation={len(residual_activation)}",
        },
        {
            "check_id": "V553_5_Hamiltonian_charge_contracts_loaded",
            "result": "pass" if len(hc_contract) == 10 and len(pg_contract) == 11 and len(worldtube) == 6 else "fail",
            "detail": f"HC={len(hc_contract)};PG={len(pg_contract)};worldtube={len(worldtube)}",
        },
        {
            "check_id": "V553_6_BRR545_fallback_loaded",
            "result": "pass" if len(brr_bound) == 1 and len(brr_envelope) == 6 else "fail",
            "detail": f"commutator_bound={len(brr_bound)};BRR545_envelope={len(brr_envelope)}",
        },
        {
            "check_id": "V553_7_repair_test_complete",
            "result": "pass" if len(REPAIR_TEST_ROWS) == 8 and len(RESIDUAL_DECOMPOSITION_ROWS) == 7 and len(BOUND_FILL_ROWS) == 1 and len(eval_rows) == 1 else "fail",
            "detail": f"repair_tests={len(REPAIR_TEST_ROWS)};residual_decomposition={len(RESIDUAL_DECOMPOSITION_ROWS)};bound_rows={len(BOUND_FILL_ROWS)};evaluator={len(eval_rows)}",
        },
        {
            "check_id": "V553_8_no_claim_rows",
            "result": "pass" if not claim_test_rows and not claim_decomp_rows and not claim_bound_rows and not claim_eval_rows else "fail",
            "detail": f"claim_test={len(claim_test_rows)};claim_decomp={len(claim_decomp_rows)};claim_bound={len(claim_bound_rows)};claim_eval={len(claim_eval_rows)}",
        },
        {
            "check_id": "V553_9_no_overclaim",
            "result": "pass" if not claim_test_rows and not claim_decomp_rows and not claim_bound_rows and not claim_eval_rows else "fail",
            "detail": "Hamiltonian_PiM_repair_passed=false; BRR545_filled=false; source_measure=false; measured_GM=false; Newton=false; PPN=false; local_GR=false",
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
    eval_rows: list[dict[str, Any]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 553 - Y5 Hamiltonian PiM Repair Clause Test or Bound Fill

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The Hamiltonian `Pi_M` repair is the right kind of repair, but it does not close for current MTS.

The useful part survives:

```text
independent/topological/readout Pi_M should not receive proof credit;
the mass channel should be a Hamiltonian/Noether charge map if this branch is used.
```

The missing part is still hard:

```text
Q_tau must be integrable, reference-locked, same-frame,
worldtube-source equal, radially closed, extra-sector silent,
and then read out through Poisson/Gauss/PPN.
```

So the repair stays as a candidate/policy improvement, and `epsilon_HPiM_total_abs` is added as a strict residual envelope.

## 2. Repair Clause Test

{markdown_table(REPAIR_TEST_ROWS)}

## 3. Residual Decomposition

{markdown_table(RESIDUAL_DECOMPOSITION_ROWS)}

## 4. Bound Fill Row

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
MTS has tested the Hamiltonian PiM repair clause.
MTS keeps independent/topological PiM demoted unless it equals the Hamiltonian charge map.
MTS has an explicit residual envelope and fill row for failed Hamiltonian PiM repair.
```

Forbidden:

```text
MTS has proved the Hamiltonian PiM repair.
MTS has filled BRR545.
MTS has derived source-measure, measured GM, Newton, PPN, or local GR.
```

## 12. Practical Read

This is a disciplined miss, not a dead end. We found the clean conceptual move, then refused to pretend it also solves reference subtraction, source equality, radial closure, and readout. The next useful repair is narrower: attack the integrability/reference/source-equality trio directly.

## 13. Next Target

`{NEXT_TARGET}`

Next: try to derive the Hamiltonian charge integrability/reference lock or the same-frame source equality; if neither closes, fill the first `epsilon_HPiM_total_abs` component row.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-Hamiltonian-PiM-repair-clause-test-or-bound-fill"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    eval_rows = evaluator_rows()
    validations = validation_rows(sources, eval_rows)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (REPAIR_TEST_PATH, REPAIR_TEST_ROWS),
        (RESIDUAL_DECOMPOSITION_PATH, RESIDUAL_DECOMPOSITION_ROWS),
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
        "repair_test": str(ROOT / REPAIR_TEST_PATH),
        "residual_decomposition": str(ROOT / RESIDUAL_DECOMPOSITION_PATH),
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
        "repair_test_rows": len(REPAIR_TEST_ROWS),
        "residual_decomposition_rows": len(RESIDUAL_DECOMPOSITION_ROWS),
        "bound_fill_rows": len(BOUND_FILL_ROWS),
        "evaluator_rows": len(eval_rows),
        "Hamiltonian_PiM_repair_passed": False,
        "epsilon_HPiM_total_abs_filled": False,
        "BRR545_values_filled": False,
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
        "done\nprivate_no_github\nHamiltonian_PiM_repair_clause_failed_current_claim_residual_decomposition_and_bound_row_written_no_BRR545_Newton_PPN_or_local_GR_promotion\n",
        encoding="utf-8",
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
