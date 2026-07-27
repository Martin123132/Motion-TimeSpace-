from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_Hilbert_worldtube_parent_action_contract_written_not_yet_Euler_Ward_derived"
CLAIM_CEILING = "parent_action_contract_only_no_Hilbert_worldtube_glue_epsilon_charge_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "538-Y5-minimal-parent-action-Euler-Ward-test-or-closure-demotion.md"

DOC_PATH = Path("537-Y5-Hilbert-worldtube-parent-action-contract-or-PiM-input-fill.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_PARENT_ACTION_CONTRACT_SOURCE_REGISTER.csv")
PARENT_ACTION_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv")
CLAUSE_MAP_PATH = Path("source-intake/mts_residuals/P8_Y5_PARENT_ACTION_TO_HWT536_CLAUSE_MAP.csv")
DERIVATION_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_Y5_PARENT_ACTION_DERIVATION_ATTEMPT.csv")
PIM_INPUT_FILL_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_PARENT_ACTION_CONTRACT_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_PARENT_ACTION_CONTRACT_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_PARENT_ACTION_CONTRACT_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "536-Y5-Hilbert-worldtube-glue-theorem-or-PiM-input-audit.md",
        "role": "exact Hilbert-worldtube theorem target and Pi_M input audit",
    },
    {
        "source_file": "535-Y5-PiM-commutator-bound-runner-or-Hilbert-worldtube-glue.md",
        "role": "Pi_M runner and original Hilbert-worldtube certificate rows",
    },
    {
        "source_file": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
        "role": "EH-style worldtube/source-measure reference route and residual decomposition",
    },
    {
        "source_file": "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
        "role": "minimal local parent-action fixed-point ansatz",
    },
    {
        "source_file": "512-match-MTS-symbols-to-local-GR-action-blocks.md",
        "role": "MTS symbol-to-local-GR action block matching",
    },
    {
        "source_file": "506-local-EH-reduction-and-extra-sector-silence-theorem.md",
        "role": "local EH reduction and extra-sector silence theorem attempt",
    },
    {
        "source_file": "509-source-measure-Meff-flux-closure-after-kappa-gate.md",
        "role": "source-measure flux closure theorem target",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
        "role": "536 HWT theorem rows to be mapped by the parent-action contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PIM_NUMERIC_INPUT_AUDIT.csv",
        "role": "536 Pi_M numeric input audit showing no claim-valid rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_VALIDATION.csv",
        "role": "536 validation gates",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv",
        "role": "source-measure flux required clauses",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
        "role": "source-measure residual fallback map",
    },
    {
        "source_file": "scripts/Y5_Hilbert_worldtube_parent_action_contract_or_PiM_input_fill.py",
        "role": "this checkpoint generator",
    },
]


PARENT_ACTION_CONTRACT_ROWS = [
    {
        "contract_id": "PAC537_0_covariant_parent_action",
        "action_clause": "write an explicit diffeomorphism-covariant parent action with symplectic potential",
        "mathematical_form": "S_parent = int_M L(phi,dphi) + int_boundary B; delta L = E_A delta phi^A + dTheta(phi,delta phi)",
        "derives_hwt536_step": "HWT536_0;HWT536_2",
        "required_output": "Noether current J_tau and Hamiltonian variation are defined before fitting",
        "current_status": "contract_only_no_full_Lagrangian",
        "failure_mode": "worldtube charge is postulated rather than derived",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "PAC537_1_single_observed_source_frame",
        "action_clause": "matter couples to one observed metric/coframe used by source, clocks, and orbital readout",
        "mathematical_form": "S_matter = S_matter[e_obs,psi_m]; J_H[tau] = delta S_matter/delta e_obs contracted with tau",
        "derives_hwt536_step": "HWT536_1",
        "required_output": "same-frame Hilbert source current",
        "current_status": "not_yet_derived",
        "failure_mode": "source mass and orbital mass can differ by frame choice",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "PAC537_2_parent_fixed_worldtube",
        "action_clause": "compact source support and linking surfaces are selected by the source current/support, not by fit residuals",
        "mathematical_form": "W_source = supp(J_H); S1,S2 link the same W_source; A = ext(W_source) between S1 and S2",
        "derives_hwt536_step": "HWT536_0",
        "required_output": "worldtube fixed before local readout",
        "current_status": "not_yet_derived",
        "failure_mode": "mass channel can be retuned per radius/system",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "PAC537_3_local_EH_symplectic_fixed_point",
        "action_clause": "local exterior reduces to EH at the equation and covariant-phase-space charge level",
        "mathematical_form": "Q_MTS_tau = Q_EH_tau + Delta_nonEH + Delta_symp + Delta_extra + Delta_frame + Delta_PiM",
        "derives_hwt536_step": "HWT536_2;HWT536_7;HWT536_8",
        "required_output": "all Delta terms are zero or explicitly bounded before promotion",
        "current_status": "not_derived_for_current_MTS",
        "failure_mode": "equation-shape GR can hide non-GR charge hair",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "PAC537_4_action_owned_PiM_projector",
        "action_clause": "Pi_M is fixed by parent algebra and covariantly constant on the local exterior source-current space",
        "mathematical_form": "Pi_M^2=Pi_M; nabla Pi_M=0 on A; [d,Pi_M]J_H=0",
        "derives_hwt536_step": "HWT536_3;HWT536_6",
        "required_output": "Pi_M cannot be tuned as an empirical mass selector",
        "current_status": "not_derived",
        "failure_mode": "projector commutator/stress becomes source hair",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "PAC537_5_Hilbert_topological_charge_equality",
        "action_clause": "topological representative equals the Hilbert worldtube charge, not merely a conserved abstract current",
        "mathematical_form": "Pi_M J_H = J_M_top + dB_zero + R_eq with R_eq=0 or bounded",
        "derives_hwt536_step": "HWT536_3;HWT536_4;HWT536_5",
        "required_output": "conserved object is the measured source charge",
        "current_status": "not_derived",
        "failure_mode": "topology conserves the wrong object",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "PAC537_6_reference_and_boundary_zero",
        "action_clause": "reference background and exact/boundary improvement terms are fixed with zero compact exterior flux",
        "mathematical_form": "int_boundary dB_zero=0; Delta_symp=0; H_tau[reference] fixed once",
        "derives_hwt536_step": "HWT536_5",
        "required_output": "surface charge equality is not shifted by bookkeeping",
        "current_status": "missing_certificate_or_bound",
        "failure_mode": "mass equality gains arbitrary boundary offset",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "PAC537_7_extra_sector_mass_charge_silence",
        "action_clause": "motion, time, domain, memory, range, connection, and boundary sectors carry no independent local mass charge",
        "mathematical_form": "delta H_tau^extra = 0 in A, or channelwise residual below local locks",
        "derives_hwt536_step": "HWT536_7",
        "required_output": "no hidden local fifth-force/PPN source channel",
        "current_status": "field_specific_queue_open",
        "failure_mode": "extra sectors can repair fits while breaking local GR",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "PAC537_8_dressed_source_Gauss_readout",
        "action_clause": "dressed Hamiltonian source charge normalizes to the weak-field inverse-square coefficient",
        "mathematical_form": "M_source[W]=H_tau[S]-H_ref; g_00=-1+2G_ref M_source/r+O(r^-2)",
        "derives_hwt536_step": "HWT536_2;HWT536_8",
        "required_output": "measured GM and Newtonian limit are derived from the same charge",
        "current_status": "not_reached",
        "failure_mode": "Newtonian recovery remains an orbital calibration ledger",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "PAC537_9_second_order_PPN_stability",
        "action_clause": "the source charge remains stable through second order and preferred-frame/conservation PPN channels",
        "mathematical_form": "Delta_PPN={gamma-1,beta-1,alpha_i,zeta_i,xi} from parent expansion and below locks",
        "derives_hwt536_step": "HWT536_8",
        "required_output": "local GR, not just local Newton, is tested at the correct order",
        "current_status": "not_reached",
        "failure_mode": "leading-order pass can still fail local GR",
        "valid_for_claim": "false",
    },
]


CLAUSE_MAP_ROWS = [
    {
        "hwt536_step": "HWT536_0_parent_worldtube_fixed",
        "contract_clause": "PAC537_0_covariant_parent_action;PAC537_2_parent_fixed_worldtube",
        "parent_action_output_needed": "W_source and linking surfaces fixed before readout",
        "current_status": "not_derived",
        "valid_for_claim": "false",
    },
    {
        "hwt536_step": "HWT536_1_observed_Hilbert_measure_owned",
        "contract_clause": "PAC537_1_single_observed_source_frame",
        "parent_action_output_needed": "same-frame Hilbert source current",
        "current_status": "not_derived",
        "valid_for_claim": "false",
    },
    {
        "hwt536_step": "HWT536_2_dressed_mass_charge_definition",
        "contract_clause": "PAC537_0_covariant_parent_action;PAC537_8_dressed_source_Gauss_readout",
        "parent_action_output_needed": "dressed Hamiltonian/Noether source charge",
        "current_status": "definition_guardrail_only",
        "valid_for_claim": "false",
    },
    {
        "hwt536_step": "HWT536_3_Hilbert_to_PiM_charge_map",
        "contract_clause": "PAC537_4_action_owned_PiM_projector;PAC537_5_Hilbert_topological_charge_equality",
        "parent_action_output_needed": "Pi_M J_H equals the charge form used by M_source",
        "current_status": "not_derived",
        "valid_for_claim": "false",
    },
    {
        "hwt536_step": "HWT536_4_topological_boundary_match",
        "contract_clause": "PAC537_5_Hilbert_topological_charge_equality",
        "parent_action_output_needed": "topological representative matches same worldtube boundary class",
        "current_status": "not_derived",
        "valid_for_claim": "false",
    },
    {
        "hwt536_step": "HWT536_5_exact_and_reference_terms_zero",
        "contract_clause": "PAC537_6_reference_and_boundary_zero",
        "parent_action_output_needed": "zero exact/reference/boundary improvement flux",
        "current_status": "missing_certificate_or_bound",
        "valid_for_claim": "false",
    },
    {
        "hwt536_step": "HWT536_6_PiM_commutator_and_projector_stress_zero",
        "contract_clause": "PAC537_4_action_owned_PiM_projector",
        "parent_action_output_needed": "commutator and projector-stress silence",
        "current_status": "missing_certificate_or_bound",
        "valid_for_claim": "false",
    },
    {
        "hwt536_step": "HWT536_7_extra_sector_charge_silence",
        "contract_clause": "PAC537_3_local_EH_symplectic_fixed_point;PAC537_7_extra_sector_mass_charge_silence",
        "parent_action_output_needed": "zero non-EH/extra/frame mass charge in local exterior",
        "current_status": "field_specific_queue_open",
        "valid_for_claim": "false",
    },
    {
        "hwt536_step": "HWT536_8_weak_field_readout_after_charge_glue",
        "contract_clause": "PAC537_8_dressed_source_Gauss_readout;PAC537_9_second_order_PPN_stability",
        "parent_action_output_needed": "weak-field metric and PPN vector derived after charge glue",
        "current_status": "not_reached",
        "valid_for_claim": "false",
    },
]


DERIVATION_ATTEMPT_ROWS = [
    {
        "attempt_id": "DAT537_0_variation",
        "step": "start from an explicit covariant action",
        "equation": "delta L = E_A delta phi^A + dTheta",
        "derivation_status": "formal_if_action_supplied",
        "current_MTS_status": "full_parent_Lagrangian_not_supplied_here",
        "claim_status": "false",
    },
    {
        "attempt_id": "DAT537_1_Noether_current",
        "step": "define the local time-flow Noether current",
        "equation": "J_tau = Theta(phi,L_tau phi) - i_tau L",
        "derivation_status": "formal_if_tau_and_Theta_fixed",
        "current_MTS_status": "tau/source/readout lock not yet derived",
        "claim_status": "false",
    },
    {
        "attempt_id": "DAT537_2_charge_decomposition",
        "step": "decompose current into surface charge and constraints",
        "equation": "J_tau = dQ_tau + C_tau",
        "derivation_status": "conditional",
        "current_MTS_status": "MTS Q_tau and C_tau not explicitly varied",
        "claim_status": "false",
    },
    {
        "attempt_id": "DAT537_3_worldtube_Stokes_equality",
        "step": "integrate between linked surfaces around the same W_source",
        "equation": "int_S2 Q_tau - int_S1 Q_tau = int_A C_tau + boundary_flux",
        "derivation_status": "mathematical_once_Q_tau_defined",
        "current_MTS_status": "Q_tau/source map not yet owned",
        "claim_status": "false",
    },
    {
        "attempt_id": "DAT537_4_PiM_Hilbert_identification",
        "step": "identify the mass-channel charge with Pi_M projected Hilbert current",
        "equation": "(4*pi*G_ref)^-1 int_S Pi_M J_H = int_S Q_tau",
        "derivation_status": "core_missing_identity",
        "current_MTS_status": "not_derived",
        "claim_status": "false",
    },
    {
        "attempt_id": "DAT537_5_local_readout",
        "step": "derive metric and PPN readout from the same charge",
        "equation": "g_00=-1+2G_ref M_source/r+O(r^-2); Delta_PPN explicit",
        "derivation_status": "not_reached",
        "current_MTS_status": "blocked_by_DAT537_4",
        "claim_status": "false",
    },
]


PIM_INPUT_FILL_TEMPLATE_ROWS = [
    {
        "input_id": "PIF537_0_R_eq_integral",
        "quantity": "R_eq_integral",
        "definition": "finite-shell integral of Pi_M J_H - J_M_top - dB_zero",
        "required_columns": "system_id;r1;r2;R_eq_integral;M_H_ref;units;normalization;source_file;assumptions;valid_for_claim",
        "acceptance_rule": "source-backed non-placeholder row normalized to M_H_ref",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PIF537_1_I_commutator",
        "quantity": "I_commutator",
        "definition": "finite-annulus integral of [d,Pi_M]J_H",
        "required_columns": "system_id;r1;r2;I_commutator;M_H_ref;units;normalization;source_file;assumptions;valid_for_claim",
        "acceptance_rule": "source-backed Pi_M algebra/profile calculation, not fitted cancellation",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PIF537_2_B_zero_flux",
        "quantity": "B_zero_flux",
        "definition": "exact/reference/boundary improvement flux through compact linked boundary",
        "required_columns": "system_id;r1;r2;B_zero_flux;M_H_ref;reference_choice;source_file;assumptions;valid_for_claim",
        "acceptance_rule": "boundary/reference convention fixed once and source-backed",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PIF537_3_projector_stress_beta_equiv",
        "quantity": "projector_stress_beta_equiv",
        "definition": "weak-field/PPN equivalent of metric stress generated by projector variation",
        "required_columns": "system_id;operator_family;projector_stress_beta_equiv;units;affected_PPN_rows;source_file;assumptions;valid_for_claim",
        "acceptance_rule": "maps to local locks without hiding behind leading-order Newton",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PIF537_4_extra_charge_vector",
        "quantity": "Delta_extra_vector",
        "definition": "non-EH/domain/memory/motion/time/range/frame/source-channel charge residuals",
        "required_columns": "system_id;channel;Delta_charge;M_H_ref;units;local_lock;source_file;assumptions;valid_for_claim",
        "acceptance_rule": "each channel separately zero or bounded; no cancellation-only acceptance",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PIF537_5_Gauss_readout_residual",
        "quantity": "Delta_cal;Delta_PPN",
        "definition": "failure of dressed source charge to control inverse-square coefficient and second-order PPN vector",
        "required_columns": "system_id;Delta_cal;gamma_minus_one;beta_minus_one;alpha_i_vector;source_file;assumptions;valid_for_claim",
        "acceptance_rule": "must compare against local empirical locks and GR baseline conventions",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D537_0_contract_written",
        "status": "parent_action_contract_written",
        "meaning": "future parent action now has exact clauses it must satisfy to derive the Hilbert-worldtube glue",
        "claim_status": "contract_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D537_1_not_yet_Euler_Ward_derived",
        "status": "no_full_action_variation_yet",
        "meaning": "the contract has not been promoted to a real Euler/Ward derivation",
        "claim_status": "no_Hilbert_worldtube_glue_promotion",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D537_2_parallel_input_fill_ready",
        "status": "PiM_fill_template_written",
        "meaning": "if the proof fails, source-backed Pi_M residual rows can be filled without inventing evidence",
        "claim_status": "input_template_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D537_3_no_smuggling_rule",
        "status": "no_plateau_no_bare_mass_no_orbital_fit_shortcut",
        "meaning": "local GR requires derived charge glue and readout, not calibration language",
        "claim_status": "guardrail_retained",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D537_4_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "PARENT_ACTION_CONTRACT",
        "previous_status": "exact_Hilbert_worldtube_contract_written_but_not_derived",
        "new_status": "parent_action_clause_contract_written",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "EULER_WARD_DERIVATION",
        "previous_status": "not_started_after_536",
        "new_status": "next_required_test",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "PIM_INPUT_FILL",
        "previous_status": "audit_no_claim_valid_numeric_rows",
        "new_status": "source_backed_fill_template_written",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "blocked_dressed_source_charge_not_owned",
        "new_status": "still_blocked_until_parent_action_or_input_fill_closes",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "blocked_source_charge_PPN_readout_not_derived",
        "new_status": "still_blocked_until_Euler_Ward_charge_glue_and_PPN_readout",
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


def validation_rows(sources: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    hwt536_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv"))
    hwt536_ids = {row.get("step_id", "") for row in hwt536_rows}
    mapped_hwt_ids = {row["hwt536_step"] for row in CLAUSE_MAP_ROWS}
    unmapped = hwt536_ids - mapped_hwt_ids
    claim_contract_rows = [row for row in PARENT_ACTION_CONTRACT_ROWS if row["valid_for_claim"] == "true"]
    claim_map_rows = [row for row in CLAUSE_MAP_ROWS if row["valid_for_claim"] == "true"]
    claim_fill_rows = [row for row in PIM_INPUT_FILL_TEMPLATE_ROWS if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V537_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V537_1_536_theorem_rows_loaded",
            "result": "pass" if len(hwt536_rows) == 9 else "fail",
            "detail": f"hwt536_rows={len(hwt536_rows)}",
        },
        {
            "check_id": "V537_2_all_HWT536_rows_mapped",
            "result": "pass" if not unmapped and len(mapped_hwt_ids) == 9 else "fail",
            "detail": f"mapped_rows={len(mapped_hwt_ids)};unmapped={len(unmapped)}",
        },
        {
            "check_id": "V537_3_contract_rows_complete",
            "result": "pass" if len(PARENT_ACTION_CONTRACT_ROWS) >= 10 else "fail",
            "detail": f"contract_rows={len(PARENT_ACTION_CONTRACT_ROWS)}",
        },
        {
            "check_id": "V537_4_fill_template_complete",
            "result": "pass" if len(PIM_INPUT_FILL_TEMPLATE_ROWS) >= 6 else "fail",
            "detail": f"fill_template_rows={len(PIM_INPUT_FILL_TEMPLATE_ROWS)}",
        },
        {
            "check_id": "V537_5_no_claim_rows",
            "result": "pass" if not claim_contract_rows and not claim_map_rows and not claim_fill_rows else "fail",
            "detail": f"claim_contract_rows={len(claim_contract_rows)};claim_map_rows={len(claim_map_rows)};claim_fill_rows={len(claim_fill_rows)}",
        },
        {
            "check_id": "V537_6_no_overclaim",
            "result": "pass" if not claim_contract_rows and not claim_map_rows and not claim_fill_rows else "fail",
            "detail": "Euler_Ward_derived=false; Hilbert_worldtube_glue_derived=false; epsilon_charge_filled=false; measured_GM=false; Newton=false; local_GR=false",
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
    validations: list[dict[str, str]],
) -> str:
    return f"""# 537 - Y5 Hilbert Worldtube Parent Action Contract or PiM Input Fill

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The local-GR route now has a precise parent-action contract, not a plateau axiom.

This is still not a proof. The current deliverable is the exact contract a future parent action must satisfy:

```text
explicit covariant action
-> same observed source frame
-> action-owned Pi_M projector
-> Hilbert worldtube source charge equals Pi_M charge
-> boundary/commutator/projector/extra channels vanish or are bounded
-> weak-field and PPN readout follows from the same charge.
```

If the next Euler/Ward variation cannot produce these outputs, the honest branch is residual closure only.

## 2. Parent-Action Contract

{markdown_table(PARENT_ACTION_CONTRACT_ROWS)}

## 3. Clause Map to 536

{markdown_table(CLAUSE_MAP_ROWS)}

## 4. Derivation Attempt Ledger

{markdown_table(DERIVATION_ATTEMPT_ROWS)}

## 5. PiM Input Fill Template

{markdown_table(PIM_INPUT_FILL_TEMPLATE_ROWS)}

## 6. Decision

{markdown_table(DECISION_ROWS)}

## 7. Source Register

{markdown_table(sources)}

## 8. Validation

{markdown_table(validations)}

## 9. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 10. Claim Ceiling

Allowed:

```text
MTS has a parent-action contract for deriving the Hilbert-worldtube glue.
MTS has a parallel source-backed Pi_M input-fill template if the proof does not close.
MTS has not promoted local GR or Newton from this contract.
```

Forbidden:

```text
MTS has derived the Euler/Ward identity for the current parent action.
MTS has proved Hilbert-worldtube glue.
MTS has filled epsilon_charge or measured GM.
MTS has derived source-normalized Newton, beta, PPN, or local GR.
```

## 11. Practical Read

This is the Grossmann move: stop arguing from vibes and write the mathematical machinery the theory must own. The machinery is plausible in shape because it mirrors the GR charge route, but MTS has not yet earned it until the action variation produces the identities.

## 12. Next Target

`{NEXT_TARGET}`

Next: test whether a minimal parent action can actually produce the Euler/Ward chain through `DAT537_4`. If it cannot, demote the local route to explicit residual closure and start filling the Pi_M residual rows.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-Hilbert-worldtube-parent-action-contract-or-PiM-input-fill"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)
    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (PARENT_ACTION_CONTRACT_PATH, PARENT_ACTION_CONTRACT_ROWS),
        (CLAUSE_MAP_PATH, CLAUSE_MAP_ROWS),
        (DERIVATION_ATTEMPT_PATH, DERIVATION_ATTEMPT_ROWS),
        (PIM_INPUT_FILL_TEMPLATE_PATH, PIM_INPUT_FILL_TEMPLATE_ROWS),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(generated_at_utc, run_dir, sources, validations)
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
        "parent_action_contract": str(ROOT / PARENT_ACTION_CONTRACT_PATH),
        "clause_map": str(ROOT / CLAUSE_MAP_PATH),
        "derivation_attempt": str(ROOT / DERIVATION_ATTEMPT_PATH),
        "pim_input_fill_template": str(ROOT / PIM_INPUT_FILL_TEMPLATE_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "parent_action_contract_rows": len(PARENT_ACTION_CONTRACT_ROWS),
        "clause_map_rows": len(CLAUSE_MAP_ROWS),
        "derivation_attempt_rows": len(DERIVATION_ATTEMPT_ROWS),
        "pim_input_fill_template_rows": len(PIM_INPUT_FILL_TEMPLATE_ROWS),
        "Euler_Ward_identity_derived": False,
        "Hilbert_worldtube_glue_derived": False,
        "PiM_bound_computed": False,
        "epsilon_charge_filled": False,
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
        "done\nprivate_no_github\ncontract_only_no_epsilon_charge_measured_GM_Newton_PPN_or_local_GR_promotion\n",
        encoding="utf-8",
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
