from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_Hamiltonian_PiM_integrability_source_equality_failed_current_claim_FB554_0_first_residual_fill_staged_nonclaim"
CLAIM_CEILING = "Hamiltonian_PiM_integrability_source_equality_gate_only_no_stable_source_charge_no_Newton_no_PPN_no_R10_no_R11_no_local_GR_claim"
NEXT_TARGET = "665-Y5-R10-fill-or-prove-FB554-0-Hamiltonian-integrability-reference-row.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "664-Y5-R10-Hamiltonian-PiM-integrability-source-equality-or-first-residual-fill.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "663_doc": ROOT / "663-Y5-R10-minimal-parent-action-source-current-Euler-Ward-test-or-residual-input-fill.md",
    "663_validation": RESIDUALS / "P8_Y5_BRR545_663_VALIDATION.csv",
    "663_chain": RESIDUALS / "P8_Y5_R10_663_EULER_WARD_CHAIN_RESULT.csv",
    "663_repair": RESIDUALS / "P8_Y5_R10_663_PIM_REPAIR_OR_DEMOTION.csv",
    "663_priority": RESIDUALS / "P8_Y5_R10_663_RESIDUAL_INPUT_PRIORITY.csv",
    "554_doc": ROOT / "554-Y5-Hamiltonian-charge-integrability-reference-lock-or-source-equality-fill.md",
    "554_validation": RESIDUALS / "P8_Y5_BRR545_554_VALIDATION.csv",
    "554_integrability_attempt": RESIDUALS / "P8_Y5_HAMILTONIAN_CHARGE_INTEGRABILITY_REFERENCE_ATTEMPT.csv",
    "554_source_equality_attempt": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_EQUALITY_ATTEMPT.csv",
    "554_fill_rows": RESIDUALS / "P8_Y5_HAMILTONIAN_INTEGRABILITY_SOURCE_EQUALITY_FILL_ROWS.csv",
    "554_evaluator": RESIDUALS / "P8_Y5_HAMILTONIAN_INTEGRABILITY_SOURCE_EQUALITY_EVALUATOR.csv",
    "554_obstruction_ledger": RESIDUALS / "P8_Y5_HAMILTONIAN_554_OBSTRUCTION_LEDGER.csv",
    "553_doc": ROOT / "553-Y5-Hamiltonian-PiM-repair-clause-test-or-bound-fill.md",
    "553_validation": RESIDUALS / "P8_Y5_BRR545_553_VALIDATION.csv",
    "553_repair_test": RESIDUALS / "P8_Y5_HAMILTONIAN_PIM_REPAIR_CLAUSE_TEST.csv",
    "553_residual_decomposition": RESIDUALS / "P8_Y5_HAMILTONIAN_PIM_REPAIR_RESIDUAL_DECOMPOSITION.csv",
    "553_bound_fill": RESIDUALS / "P8_Y5_HAMILTONIAN_PIM_REPAIR_BOUND_FILL_ROW.csv",
    "553_obstruction": RESIDUALS / "P8_Y5_HAMILTONIAN_PIM_REPAIR_OBSTRUCTION_LEDGER.csv",
    "541_doc": ROOT / "541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md",
    "541_contract": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
    "541_scorecard": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_SCORECARD.csv",
    "541_inputs": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_RESIDUAL_INPUTS.csv",
    "540_residual_activation": RESIDUALS / "P8_Y5_HAMILTONIAN_PIM_RESIDUAL_ACTIVATION.csv",
    "539_branch": RESIDUALS / "P8_Y5_PIM_HAMILTONIAN_BRANCH_DEFINITION.csv",
    "Noether_chain": RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
    "PG_contract": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
    "Hilbert_monopole": RESIDUALS / "P8_Hilbert_monopole_calibration_CONTRACT.csv",
}


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    roles = {
        "663_doc": "fresh Euler/Ward result selecting Hamiltonian PiM integrability/reference as first target",
        "663_validation": "prior 663 validation",
        "663_chain": "Euler/Ward chain with PiM Hamiltonian identification blocker",
        "663_repair": "PiM repair/demotion rows",
        "663_priority": "first residual priority rows selecting Delta_symp/B_zero/H_ref",
        "554_doc": "prior Hamiltonian charge integrability/source equality attempt",
        "554_validation": "prior 554 validation",
        "554_integrability_attempt": "machine integrability/reference attempt rows",
        "554_source_equality_attempt": "machine source-equality attempt rows",
        "554_fill_rows": "first two fill rows FB554_0 and FB554_1",
        "554_evaluator": "nonclaim evaluator for fill rows",
        "554_obstruction_ledger": "integrability/source-equality obstruction ledger",
        "553_doc": "Hamiltonian PiM repair clause failure and total residual envelope",
        "553_validation": "prior 553 validation",
        "553_repair_test": "repair-clause test rows",
        "553_residual_decomposition": "Hamiltonian PiM residual decomposition",
        "553_bound_fill": "total Hamiltonian PiM bound fill row",
        "553_obstruction": "repair obstruction ledger",
        "541_doc": "Hamiltonian PiM source-measure scorecard",
        "541_contract": "source-measure contract rows",
        "541_scorecard": "source-measure scorecard rows",
        "541_inputs": "source-measure residual input rows",
        "540_residual_activation": "residual activation map after Hamiltonian PiM readout test",
        "539_branch": "Hamiltonian PiM branch definition rows",
        "Noether_chain": "parent Noether closure chain",
        "PG_contract": "Poisson/Gauss measured-GM calibration contract",
        "Hilbert_monopole": "Hilbert source to measured monopole calibration contract",
    }
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": bool_text(path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def integrability_attempt_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "attempt_id": "HCI664_0_target",
            "claim": "Q_tau defines a finite integrable Hamiltonian mass functional with fixed reference and fixed observed time generator",
            "mathematical_form": "delta H_tau = int_S(delta Q_tau - i_tau theta); delta^2 H_tau=0; partial_{source,r,t,frame}B_ref=0; delta tau=0",
            "current_result": "target_defined_not_parent_derived",
            "why_not_enough": "a target definition does not supply the MTS parent theta, Q_tau, reference branch, or tau lock",
            "activated_residual": "epsilon_HPiM_integrability_abs",
            "valid_for_claim": "false",
            "source_paths": source_list("554_integrability_attempt", "553_repair_test"),
            "generated_utc": now,
        },
        {
            "attempt_id": "HCI664_1_GR_reference",
            "claim": "EH/covariant-phase-space theory gives a known conditional integrable charge route",
            "mathematical_form": "delta L=E delta phi+dtheta; J_tau=theta(phi,L_tau phi)-i_tau L; on shell J_tau=dQ_tau+C_tau",
            "current_result": "known_conditional_reference",
            "why_not_enough": "MTS has not inherited the EH symplectic charge and fixed boundary conditions sector-by-sector",
            "activated_residual": "R_action;C_projector;C_boundary",
            "valid_for_claim": "false",
            "source_paths": source_list("Noether_chain", "554_integrability_attempt"),
            "generated_utc": now,
        },
        {
            "attempt_id": "HCI664_2_parent_symplectic_current",
            "claim": "current MTS supplies explicit L, theta, Q_tau, and constraint decomposition for all local sectors",
            "mathematical_form": "S_parent[L(g,fields)]; theta_MTS; Q_tau^MTS; C_tau=C_EH+C_extra+C_projector+C_boundary+C_ref",
            "current_result": "not_derived",
            "why_not_enough": "current corpus has contracts and conditional routes, not a fully varied parent Lagrangian with all local sectors",
            "activated_residual": "epsilon_HPiM_integrability_abs;epsilon_HPiM_radial_closure_abs",
            "valid_for_claim": "false",
            "source_paths": source_list("553_residual_decomposition", "663_chain"),
            "generated_utc": now,
        },
        {
            "attempt_id": "HCI664_3_reference_lock",
            "claim": "B_ref/reference subtraction is fixed once and cannot absorb source, radius, time, frame, or readout changes",
            "mathematical_form": "partial_t Delta_ref=partial_r Delta_ref=partial_source Delta_ref=partial_frame Delta_ref=0",
            "current_result": "fail_current_claim",
            "why_not_enough": "reference superselection and boundary/reference rows remain open",
            "activated_residual": "Delta_ref_over_MH;B_zero_flux;H_ref_shift",
            "valid_for_claim": "false",
            "source_paths": source_list("554_obstruction_ledger", "663_priority"),
            "generated_utc": now,
        },
        {
            "attempt_id": "HCI664_4_time_generator_lock",
            "claim": "tau is the same observed time generator in source variation, charge, and readout",
            "mathematical_form": "tau_source=tau_charge=tau_orbit; delta tau=0 inside the local branch",
            "current_result": "open",
            "why_not_enough": "same observed time/coframe branch is not parent-derived for all MTS sectors",
            "activated_residual": "Delta_frame;dln_Geff_dt;source_charge",
            "valid_for_claim": "false",
            "source_paths": source_list("554_integrability_attempt", "541_scorecard"),
            "generated_utc": now,
        },
        {
            "attempt_id": "HCI664_5_symplectic_boundary_flux",
            "claim": "extra symplectic and boundary flux terms vanish or are fixed topological constants",
            "mathematical_form": "int_boundary(delta Q_tau-i_tau theta)_extra=0 or fixed; B_zero_flux=0",
            "current_result": "fail_current_claim",
            "why_not_enough": "Delta_symp and B_zero_flux are retained; boundary no-hair and projector silence are not signed",
            "activated_residual": "Delta_symp;B_zero_flux;projector_variation",
            "valid_for_claim": "false",
            "source_paths": source_list("554_obstruction_ledger", "553_obstruction"),
            "generated_utc": now,
        },
        {
            "attempt_id": "HCI664_6_integrability_verdict",
            "claim": "HSM541_1/HPT553_1 can be signed for current MTS",
            "mathematical_form": "epsilon_HPiM_integrability_abs=0",
            "current_result": "fail_current_claim",
            "why_not_enough": "missing explicit theta/Q_tau/B_ref/tau lock and zero symplectic-boundary flux theorem",
            "activated_residual": "FB554_0_HPiM_integrability_reference_bound",
            "valid_for_claim": "false",
            "source_paths": source_list("554_fill_rows", "554_evaluator"),
            "generated_utc": now,
        },
    ]


def source_equality_attempt_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "attempt_id": "HSE664_0_target",
            "claim": "worldtube source measure equals the same observed-frame Hamiltonian charge before orbital fitting",
            "mathematical_form": "M_source[W]=G_ref^-1 int_S Q_tau; W_source=supp(J_H[e_obs]); source_frame=readout_frame",
            "current_result": "target_defined_not_theorem",
            "why_not_enough": "target definition is not a source-measure theorem",
            "activated_residual": "epsilon_HPiM_source_equality_abs",
            "valid_for_claim": "false",
            "source_paths": source_list("554_source_equality_attempt", "541_contract"),
            "generated_utc": now,
        },
        {
            "attempt_id": "HSE664_1_dressed_source_guardrail",
            "claim": "M_source must be dressed Hamiltonian/Noether charge, not bare rest matter",
            "mathematical_form": "M_source[W] := H_tau[S_outer]-H_ref; M_bare is not generally equal",
            "current_result": "guardrail_pass_not_theorem",
            "why_not_enough": "guardrail prevents a false proof but does not prove current MTS source equality",
            "activated_residual": "Delta_cal;Delta_frame",
            "valid_for_claim": "false",
            "source_paths": source_list("541_doc", "Hilbert_monopole"),
            "generated_utc": now,
        },
        {
            "attempt_id": "HSE664_2_same_observed_matter_coupling",
            "claim": "matter source, clocks, rods, and orbital readout all couple to the same observed metric/coframe",
            "mathematical_form": "S_matter[psi,g_obs]; J_H[e_obs]; g_readout=g_obs at local branch",
            "current_result": "open",
            "why_not_enough": "same-frame/coframe theorem is still a contract, not a completed parent derivation",
            "activated_residual": "Delta_frame;R1_WEP_source_charge",
            "valid_for_claim": "false",
            "source_paths": source_list("554_source_equality_attempt", "541_scorecard"),
            "generated_utc": now,
        },
        {
            "attempt_id": "HSE664_3_worldtube_linking_surfaces",
            "claim": "inner worldtube and outer linking surface read the same charge with no extra boundary or frame terms",
            "mathematical_form": "int_S Q_tau - M_source[W] = Delta_frame + Delta_cal + Delta_boundary + Delta_extra = 0",
            "current_result": "fail_current_claim",
            "why_not_enough": "Delta_frame, Delta_cal, Delta_boundary, and extra-sector charge rows remain open",
            "activated_residual": "Delta_frame;Delta_cal;Delta_boundary;Delta_extra",
            "valid_for_claim": "false",
            "source_paths": source_list("554_obstruction_ledger", "540_residual_activation"),
            "generated_utc": now,
        },
        {
            "attempt_id": "HSE664_4_Hilbert_current_equality",
            "claim": "Hamiltonian charge equals the parent Hilbert/source current mass channel",
            "mathematical_form": "G_ref^-1 int_S Q_tau = M_eff[Pi_M^H J_H] and delta H_tau=delta int_S Pi_M^H J_H",
            "current_result": "not_derived",
            "why_not_enough": "Hamiltonian PiM is a candidate definition, but same-frame Hilbert equality and old/new PiM residuals remain unproved",
            "activated_residual": "R_Htop;I_commutator;R_eq",
            "valid_for_claim": "false",
            "source_paths": source_list("539_branch", "663_repair"),
            "generated_utc": now,
        },
        {
            "attempt_id": "HSE664_5_orbital_denominator_policy",
            "claim": "orbital GM cannot substitute for source equality before Gauss/readout theorem",
            "mathematical_form": "GM_orbit=G_ref M_source only after Poisson/Gauss/orbital readout",
            "current_result": "policy_pass",
            "why_not_enough": "policy blocks circular calibration; it does not fill Delta_cal",
            "activated_residual": "Delta_cal;alpha_lambda;partial_r_ln_mu_obs",
            "valid_for_claim": "false",
            "source_paths": source_list("PG_contract", "554_source_equality_attempt"),
            "generated_utc": now,
        },
        {
            "attempt_id": "HSE664_6_source_equality_verdict",
            "claim": "HSM541_2/HPT553_2 can be signed for current MTS",
            "mathematical_form": "epsilon_HPiM_source_equality_abs=0",
            "current_result": "fail_current_claim",
            "why_not_enough": "same observed frame, source worldtube glue, and denominator calibration are not derived",
            "activated_residual": "FB554_1_HPiM_source_equality_bound",
            "valid_for_claim": "false",
            "source_paths": source_list("554_fill_rows", "554_evaluator"),
            "generated_utc": now,
        },
    ]


def first_residual_fill_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "fill_id": "FB554_0_HPiM_integrability_reference_bound",
            "residual_component": "epsilon_HPiM_integrability_abs",
            "formula": "abs(delta_H_tau_nonintegrable_over_MH)+abs(Delta_ref_over_MH)+abs(symplectic_boundary_flux_over_MH)",
            "required_inputs": "delta_H_tau_nonintegrable_over_MH;Delta_ref_over_MH;symplectic_boundary_flux_over_MH;M_H_ref;units;source_file;assumptions;valid_for_claim",
            "mapped_lock_rows": "R3_gamma;R9_Gdot;R10_fifth_force;R11_EH_operator_ledger",
            "bound_rule": "integrability, reference, symplectic-boundary, and tau-lock terms must each pass or theorem-zero; no cancellation credit",
            "current_status": "MISSING_INTEGRABILITY_REFERENCE_NUMERIC_OR_THEOREM_ZERO",
            "selection_status": "selected_first",
            "valid_for_claim": "false",
            "source_paths": source_list("554_fill_rows", "554_evaluator", "663_priority"),
            "generated_utc": now,
        },
        {
            "fill_id": "FB554_1_HPiM_source_equality_bound",
            "residual_component": "epsilon_HPiM_source_equality_abs",
            "formula": "abs(source_charge_mismatch_over_MH)+abs(Delta_frame_over_MH)+abs(Delta_cal_over_MH)",
            "required_inputs": "source_charge_mismatch_over_MH;Delta_frame_over_MH;Delta_cal_over_MH;M_H_ref;units;source_file;assumptions;valid_for_claim",
            "mapped_lock_rows": "R1_WEP_source_charge;R9_Gdot;R11_EH_operator_ledger",
            "bound_rule": "source equality, frame, and calibration terms must each pass or theorem-zero; orbital GM cannot substitute for source equality",
            "current_status": "MISSING_SOURCE_EQUALITY_NUMERIC_OR_THEOREM_ZERO",
            "selection_status": "second_after_FB554_0",
            "valid_for_claim": "false",
            "source_paths": source_list("554_fill_rows", "554_evaluator", "541_inputs"),
            "generated_utc": now,
        },
    ]


def obstruction_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "obstruction_id": "HO664_0_no_parent_symplectic_current",
            "obstruction": "no explicit MTS parent theta/Q_tau/boundary symplectic current is available for all relevant local sectors",
            "activated_residual": "epsilon_HPiM_integrability_abs",
            "repair": "write or extract full parent Lagrangian, theta, Q_tau, and constraint decomposition",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "HO664_1_reference_not_superselected",
            "obstruction": "reference subtraction can still carry source/radius/time/frame dependence",
            "activated_residual": "Delta_ref_over_MH;H_ref_shift;epsilon_Delta_symp_abs",
            "repair": "derive B_ref from parent branch, topology, or fixed stationarity; otherwise fill Delta_ref row",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "HO664_2_boundary_symplectic_flux_open",
            "obstruction": "delta Q_tau - i_tau theta can receive boundary/projector/non-EH contributions",
            "activated_residual": "B_zero_flux;symplectic_boundary_flux_over_MH;projector_variation",
            "repair": "zero boundary/projector symplectic flux or retain coefficients",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "HO664_3_no_one_frame_theorem",
            "obstruction": "source worldtube, clocks, Hamiltonian charge, and orbital readout are not proven to share one observed frame",
            "activated_residual": "Delta_frame;epsilon_HPiM_source_equality_abs;R1_WEP_source_charge",
            "repair": "derive one-observed-coframe matter/source theorem or fill Delta_frame row",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "HO664_4_source_equality_not_Gauss",
            "obstruction": "source equality is upstream of Poisson/Gauss/orbital calibration and cannot be inferred from fitted GM",
            "activated_residual": "Delta_cal;epsilon_HPiM_denominator_readout_abs",
            "repair": "prove worldtube source equality first, then Gauss/readout theorem",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "HO664_5_next_Cterm_debt",
            "obstruction": "radial C-terms and extra-sector charge silence remain open after integrability/source equality attempt",
            "activated_residual": "epsilon_HPiM_radial_closure_abs;epsilon_HPiM_extra_charge_abs",
            "repair": "attack C-term zero only after FB554_0/1 are theorem-zero or source-backed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def scoreability_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "G664_0_integrability_attempt_complete",
            "gate": "Hamiltonian charge integrability/reference lock attempted",
            "result": "pass",
            "detail": "target, GR reference, parent symplectic current, reference lock, tau lock, boundary flux, and verdict rows written",
            "claim_effect": "no promotion",
            "generated_utc": now,
        },
        {
            "gate_id": "G664_1_integrability_not_signed",
            "gate": "HSM541_1/HPT553_1 remains unsigned",
            "result": "blocked_as_expected",
            "detail": "explicit theta/Q_tau/B_ref/tau lock and zero symplectic-boundary flux theorem are missing",
            "claim_effect": "blocks stable Hamiltonian source charge",
            "generated_utc": now,
        },
        {
            "gate_id": "G664_2_source_equality_attempt_complete",
            "gate": "same-frame source equality attempted",
            "result": "pass",
            "detail": "target, dressed-source guardrail, same-frame matter coupling, worldtube surfaces, Hilbert equality, orbital policy, and verdict rows written",
            "claim_effect": "no promotion",
            "generated_utc": now,
        },
        {
            "gate_id": "G664_3_source_equality_not_signed",
            "gate": "HSM541_2/HPT553_2 remains unsigned",
            "result": "blocked_as_expected",
            "detail": "same observed frame, source worldtube glue, and denominator calibration are not derived",
            "claim_effect": "blocks source-normalized Newton",
            "generated_utc": now,
        },
        {
            "gate_id": "G664_4_FB554_0_selected",
            "gate": "first residual fill row selected",
            "result": "pass_nonclaim",
            "detail": "FB554_0 is selected before source equality, C-terms, Gauss, or PPN because it defines whether the Hamiltonian charge is stable",
            "claim_effect": "scoreability scaffold only",
            "generated_utc": now,
        },
        {
            "gate_id": "G664_5_fill_rows_unfilled",
            "gate": "FB554 rows remain unfilled and nonclaim",
            "result": "pass_nonclaim",
            "detail": "FB554_0/1 require theorem-zero or source-backed inputs before any R10/R11/local use",
            "claim_effect": "no R10/R11/local pass",
            "generated_utc": now,
        },
        {
            "gate_id": "G664_6_no_orbital_circularity",
            "gate": "orbital GM cannot substitute for source equality",
            "result": "pass",
            "detail": "Delta_cal remains a residual until Poisson/Gauss/orbital readout is derived",
            "claim_effect": "prevents circular calibration",
            "generated_utc": now,
        },
        {
            "gate_id": "G664_7_claim_guard",
            "gate": "no R10, R11, Newton, PPN, or local-GR claim",
            "result": "pass",
            "detail": CLAIM_CEILING,
            "claim_effect": "private derivation audit only",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D664_0_integrability",
            "status": "not_signed",
            "meaning": "Hamiltonian PiM still lacks a parent-derived integrable charge with fixed reference, fixed tau, and zero symplectic-boundary flux",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
        {
            "decision_id": "D664_1_source_equality",
            "status": "not_signed",
            "meaning": "same-frame worldtube source equality is not derived and cannot be inferred from orbital GM",
            "claim_status": "false",
            "next_action": "after FB554_0, attempt or fill FB554_1",
            "generated_utc": now,
        },
        {
            "decision_id": "D664_2_first_fill",
            "status": "FB554_0_selected",
            "meaning": "first fill/proof target is delta_H_tau_nonintegrable, Delta_ref, and symplectic_boundary_flux normalized by M_H_ref",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
        {
            "decision_id": "D664_3_downstream",
            "status": "Cterms_Gauss_PPN_deferred",
            "meaning": "radial C-terms, extra-sector charge, Gauss/orbital readout, and PPN remain downstream until stable source charge exists",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows(
    integrability_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    fill_rows: list[dict[str, str]],
    obstruction_data: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    blocked_gates = [row["gate_id"] for row in gate_rows if row["result"] in {"blocked_as_expected", "pass_nonclaim"}]
    failures = [row["check_id"] for row in validation if row["result"] != "pass"]
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "integrability_attempt_rows": str(len(integrability_rows)),
            "source_equality_attempt_rows": str(len(source_rows)),
            "first_fill_rows": str(len(fill_rows)),
            "obstruction_rows": str(len(obstruction_data)),
            "blocked_or_nonclaim_scoreability_gates": ";".join(blocked_gates),
            "validation_failures": ";".join(failures),
            "next_target": NEXT_TARGET,
            "generated_utc": now,
        }
    ]


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for path in FORMALIZATION_WORKBENCH.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def validation_rows(
    source_rows: list[dict[str, str]],
    integrability_rows: list[dict[str, str]],
    source_equality_rows: list[dict[str, str]],
    fill_rows: list[dict[str, str]],
    obstruction_data: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows: list[dict[str, str]] = []

    def add(check_id: str, result: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "result": "pass" if result else "fail",
                "detail": detail,
                "generated_utc": now,
            }
        )

    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    add("V664_0_sources_exist", not missing_sources, "missing=" + ";".join(missing_sources))

    validation_663 = read_csv(SOURCE_PATHS["663_validation"])
    prior_663_failures = [row.get("check_id", "?") for row in validation_663 if row.get("result") != "pass"]
    add("V664_1_prior_663_validation_clean", not prior_663_failures, "prior_663_failures=" + ";".join(prior_663_failures))

    validation_554 = read_csv(SOURCE_PATHS["554_validation"])
    prior_554_failures = [row.get("check_id", "?") for row in validation_554 if row.get("result") != "pass"]
    add("V664_2_prior_554_validation_clean", not prior_554_failures, "prior_554_failures=" + ";".join(prior_554_failures))

    all_valid_flags = [
        row.get("valid_for_claim")
        for row_group in (integrability_rows, source_equality_rows, fill_rows, obstruction_data)
        for row in row_group
    ]
    add("V664_3_no_claim_rows", all(flag == "false" for flag in all_valid_flags), "valid_for_claim_flags=" + ";".join(sorted(set(all_valid_flags))))

    hci_ids = {row["attempt_id"] for row in integrability_rows}
    required_hci = {"HCI664_0_target", "HCI664_1_GR_reference", "HCI664_2_parent_symplectic_current", "HCI664_3_reference_lock", "HCI664_4_time_generator_lock", "HCI664_5_symplectic_boundary_flux", "HCI664_6_integrability_verdict"}
    add("V664_4_integrability_attempt_coverage", required_hci.issubset(hci_ids), "hci_ids=" + ";".join(sorted(hci_ids)))

    hse_ids = {row["attempt_id"] for row in source_equality_rows}
    required_hse = {"HSE664_0_target", "HSE664_1_dressed_source_guardrail", "HSE664_2_same_observed_matter_coupling", "HSE664_3_worldtube_linking_surfaces", "HSE664_4_Hilbert_current_equality", "HSE664_5_orbital_denominator_policy", "HSE664_6_source_equality_verdict"}
    add("V664_5_source_equality_attempt_coverage", required_hse.issubset(hse_ids), "hse_ids=" + ";".join(sorted(hse_ids)))

    selected = [
        row
        for row in fill_rows
        if row["fill_id"] == "FB554_0_HPiM_integrability_reference_bound"
        and row["selection_status"] == "selected_first"
    ]
    add("V664_6_FB554_0_selected_first", len(selected) == 1, "selected_rows=" + str(len(selected)))

    unfilled = [row["fill_id"] for row in fill_rows if "MISSING" in row["current_status"]]
    add("V664_7_fill_rows_unfilled_nonclaim", len(unfilled) == len(fill_rows), "fill_rows=" + str(len(fill_rows)))

    obstruction_ids = {row["obstruction_id"] for row in obstruction_data}
    required_obstructions = {"HO664_0_no_parent_symplectic_current", "HO664_1_reference_not_superselected", "HO664_2_boundary_symplectic_flux_open", "HO664_3_no_one_frame_theorem", "HO664_4_source_equality_not_Gauss", "HO664_5_next_Cterm_debt"}
    add("V664_8_obstruction_coverage", required_obstructions.issubset(obstruction_ids), "obstruction_ids=" + ";".join(sorted(obstruction_ids)))

    blocked_gates = {row["gate_id"] for row in gate_rows if row["result"] == "blocked_as_expected"}
    add("V664_9_blocked_gates_present", {"G664_1_integrability_not_signed", "G664_3_source_equality_not_signed"}.issubset(blocked_gates), "blocked_gates=" + ";".join(sorted(blocked_gates)))

    circularity_gate = [row for row in gate_rows if row["gate_id"] == "G664_6_no_orbital_circularity" and row["result"] == "pass"]
    add("V664_10_orbital_circularity_guard", len(circularity_gate) == 1, "guard_rows=" + str(len(circularity_gate)))

    next_target_rows = [row for row in decision if row["next_action"] == NEXT_TARGET]
    add("V664_11_next_target_selected", bool(next_target_rows), NEXT_TARGET)

    changed = formalization_changed_after_cutoff()
    add("V664_12_formalization_workbench_untouched", changed == 0, "formalization_changed_after_cutoff=" + str(changed))

    add("V664_13_status_nonclaim", "no_stable_source_charge" in CLAIM_CEILING and STATUS.endswith("nonclaim"), STATUS)

    return rows


def cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, str]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |\n"
    separator = "| " + " | ".join("---" for _ in fields) + " |\n"
    body = "".join("| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |\n" for row in rows)
    return header + separator + body


def write_document(
    source_rows: list[dict[str, str]],
    integrability_rows: list[dict[str, str]],
    source_equality_rows: list[dict[str, str]],
    fill_rows: list[dict[str, str]],
    obstruction_data: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    doc = f"""# 664 - Y5 R10 Hamiltonian PiM Integrability Source Equality Or First Residual Fill

## Verdict

The Hamiltonian `Pi_M^H` repair remains the right conceptual move, but 664 does not sign it. The first hard lock is still:

```text
delta H_tau = int_S(delta Q_tau - i_tau theta)
```

with fixed `B_ref`, fixed `tau`, and zero symplectic/boundary leakage. Current MTS does not yet provide the full parent `theta`, `Q_tau`, reference lock, time-generator lock, or zero-flux theorem needed to make that a stable source charge.

The same-frame source equality is also not signed:

```text
M_source[W] = G_ref^-1 int_S Q_tau
```

and orbital `GM` is explicitly forbidden as a shortcut.

So the next exact target is the first fill/proof row:

```text
FB554_0 = abs(delta_H_tau_nonintegrable_over_MH)
        + abs(Delta_ref_over_MH)
        + abs(symplectic_boundary_flux_over_MH).
```

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "role"])}

## Integrability Attempt

{markdown_table(integrability_rows, ["attempt_id", "claim", "mathematical_form", "current_result", "why_not_enough", "activated_residual", "valid_for_claim"])}

## Source Equality Attempt

{markdown_table(source_equality_rows, ["attempt_id", "claim", "mathematical_form", "current_result", "why_not_enough", "activated_residual", "valid_for_claim"])}

## First Residual Fill

{markdown_table(fill_rows, ["fill_id", "residual_component", "formula", "current_status", "selection_status", "valid_for_claim"])}

## Obstruction Ledger

{markdown_table(obstruction_data, ["obstruction_id", "obstruction", "activated_residual", "repair", "valid_for_claim"])}

## Scoreability Gates

{markdown_table(gate_rows, ["gate_id", "gate", "result", "detail", "claim_effect"])}

## Decision

{markdown_table(decision, ["decision_id", "status", "meaning", "claim_status", "next_action"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "integrability_attempt_rows", "source_equality_attempt_rows", "first_fill_rows", "obstruction_rows", "blocked_or_nonclaim_scoreability_gates", "validation_failures", "next_target"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Interpretation

This is a boring but important stop sign. If `H_tau` is not integrable with a fixed reference, then `Pi_M^H` is not yet a physical source-mass operator; it is a candidate notation. The next useful move is to either prove `FB554_0=0` componentwise or fill it with source-backed values. Only after that should source equality, radial C-terms, Gauss readout, and PPN be touched.

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    integrability_rows = integrability_attempt_rows()
    source_equality_rows = source_equality_attempt_rows()
    fill_rows = first_residual_fill_rows()
    obstruction_data = obstruction_rows()
    gate_rows = scoreability_gate_rows()
    decision = decision_rows()
    validation = validation_rows(source_rows, integrability_rows, source_equality_rows, fill_rows, obstruction_data, gate_rows, decision)
    summary_rows = nonclaim_summary_rows(integrability_rows, source_equality_rows, fill_rows, obstruction_data, gate_rows, validation)

    write_csv(
        RESIDUALS / "P8_Y5_R10_664_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "source_path", "exists", "role", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv",
        integrability_rows,
        ["attempt_id", "claim", "mathematical_form", "current_result", "why_not_enough", "activated_residual", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_664_SOURCE_EQUALITY_ATTEMPT.csv",
        source_equality_rows,
        ["attempt_id", "claim", "mathematical_form", "current_result", "why_not_enough", "activated_residual", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_664_FIRST_RESIDUAL_FILL.csv",
        fill_rows,
        ["fill_id", "residual_component", "formula", "required_inputs", "mapped_lock_rows", "bound_rule", "current_status", "selection_status", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_664_OBSTRUCTION_LEDGER.csv",
        obstruction_data,
        ["obstruction_id", "obstruction", "activated_residual", "repair", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_664_SCOREABILITY_GATES.csv",
        gate_rows,
        ["gate_id", "gate", "result", "detail", "claim_effect", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_664_DECISION.csv",
        decision,
        ["decision_id", "status", "meaning", "claim_status", "next_action", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_664_NONCLAIM_SUMMARY.csv",
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "integrability_attempt_rows",
            "source_equality_attempt_rows",
            "first_fill_rows",
            "obstruction_rows",
            "blocked_or_nonclaim_scoreability_gates",
            "validation_failures",
            "next_target",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_BRR545_664_VALIDATION.csv",
        validation,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_document(source_rows, integrability_rows, source_equality_rows, fill_rows, obstruction_data, gate_rows, decision, summary_rows, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"integrability_attempt_rows={len(integrability_rows)}")
    print(f"source_equality_attempt_rows={len(source_equality_rows)}")
    print(f"first_fill_rows={len(fill_rows)}")
    print(f"obstruction_rows={len(obstruction_data)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
