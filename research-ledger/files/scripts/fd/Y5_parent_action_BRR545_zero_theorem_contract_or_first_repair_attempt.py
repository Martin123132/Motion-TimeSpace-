from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_parent_action_BRR545_zero_theorem_contract_written_Hamiltonian_PiM_repair_candidate_selected_not_promoted"
CLAIM_CEILING = "parent_action_BRR545_zero_theorem_contract_and_repair_candidate_only_no_BRR545_source_measure_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "553-Y5-Hamiltonian-PiM-repair-clause-test-or-bound-fill.md"

DOC_PATH = Path("552-Y5-parent-action-BRR545-zero-theorem-contract-or-first-repair-attempt.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_552_SOURCE_REGISTER.csv")
ZERO_THEOREM_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_PARENT_ACTION_ZERO_THEOREM_CONTRACT.csv")
CLAUSE_TESTS_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_PARENT_ACTION_CLAUSE_TESTS.csv")
FIRST_REPAIR_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_FIRST_REPAIR_ATTEMPT.csv")
OBSTRUCTION_LEDGER_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_REPAIR_OBSTRUCTION_LEDGER.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_552_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_552_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_552_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "551-Y5-BRR545-residual-envelope-and-first-local-lock-fill-or-demotion.md",
        "role": "BRR545 residual envelope and closure-only demotion",
    },
    {
        "source_file": "550-Y5-projector-symplectic-silence-certificate-or-commutator-bound-fill.md",
        "role": "projector silence failure and commutator/projector bound row",
    },
    {
        "source_file": "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
        "role": "minimal local-GR fixed-point parent-action ansatz",
    },
    {
        "source_file": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
        "role": "GR-style Hamiltonian/Noether worldtube source-measure glue route",
    },
    {
        "source_file": "506-local-EH-reduction-and-extra-sector-silence-theorem.md",
        "role": "positive source-free operator silence theorem shape",
    },
    {
        "source_file": "504-parent-Hilbert-worldtube-glue-or-external-radial-input-plan.md",
        "role": "parent Noether mass charge and radial closure theorem clauses",
    },
    {
        "source_file": "446-source-owner-current-parent-action-contract.md",
        "role": "source-owner current parent-action terms",
    },
    {
        "source_file": "382-parent-local-action-minimal-contract.md",
        "role": "earlier minimal parent local action contract",
    },
    {
        "source_file": "539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md",
        "role": "Hamiltonian Pi_M candidate and topological demotion warning",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_RESIDUAL_ENVELOPE.csv",
        "role": "551 strict BRR545 residual envelope",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_LOCAL_LOCK_PREFLIGHT.csv",
        "role": "551 local lock preflight rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_CLOSURE_DEMOTION_DECISION.csv",
        "role": "551 closure demotion decision",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv",
        "role": "545 boundary/reference minimal action clauses",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        "role": "511 minimal parent local-GR action blocks",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
        "role": "511 fixed-point conditions",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_DERIVED_CHAIN.csv",
        "role": "511 conditional derived chain",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
        "role": "446 source-owner parent action term contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
        "role": "504 worldtube glue theorem clauses",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        "role": "Pi_M parent symplectic projector algebra contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv",
        "role": "Pi_M variation stress contract",
    },
    {
        "source_file": "scripts/Y5_parent_action_BRR545_zero_theorem_contract_or_first_repair_attempt.py",
        "role": "this checkpoint generator",
    },
]


ZERO_THEOREM_CONTRACT_ROWS = [
    {
        "clause_id": "BZTC552_0_covariant_phase_space_parent",
        "parent_action_clause": "single diffeomorphism-covariant parent action with covariant symplectic potential and Hamiltonian/Noether charge",
        "mathematical_form": "S_parent=int_M L[phi]+int_dM B_ref; delta L=E_A delta phi^A+dTheta; J_tau=Theta(phi,L_tau phi)-i_tau L; J_tau=dQ_tau+C_tau",
        "zeros_or_owns": "defines Delta_symp, B_zero_flux, M_H_ref, and charge leakage as derived terms instead of readout names",
        "required_evidence": "explicit local parent Lagrangian, boundary term, Theta, Q_tau, and constraint decomposition in MTS variables",
        "current_status": "template_available_not_current_MTS_derived",
        "accepted_for_claim": "false",
    },
    {
        "clause_id": "BZTC552_1_local_EH_fixed_point",
        "parent_action_clause": "compact local exterior has an EH fixed point with silent non-EH sectors",
        "mathematical_form": "Phi=Phi0; C_i(Phi0)=0; partial_A C_i(Phi0)=0; L_AB delta Phi^B=0 with positive source-free operator and zero boundary/source flux",
        "zeros_or_owns": "kills non-EH charge shifts, fifth-force leakage, gamma/beta/operator tails at first order",
        "required_evidence": "field-specific operators, signs, masses, source-charge laws, and boundary conditions for Gamma_eff, K_hat, q_loc, chi_D, Qcoh, memory, and domain fields",
        "current_status": "minimal_ansatz_exists_but_symbols_not_fully_matched",
        "accepted_for_claim": "false",
    },
    {
        "clause_id": "BZTC552_2_reference_superselection",
        "parent_action_clause": "Hamiltonian reference subtraction is fixed by the parent branch and cannot depend on source, radius, frame, or post-fit readout",
        "mathematical_form": "partial_t Delta_ref=partial_r Delta_ref=partial_source Delta_ref=partial_frame Delta_ref=0",
        "zeros_or_owns": "zeros epsilon_Delta_symp_abs reference drift and its R3/R9/R10/R11 leakage",
        "required_evidence": "reference background/surface rule generated by action, topology, or asymptotic/local stationarity; no fitted subtraction",
        "current_status": "reference_lock_certificate_failed_current_claim",
        "accepted_for_claim": "false",
    },
    {
        "clause_id": "BZTC552_3_boundary_relative_nohair",
        "parent_action_clause": "boundary/exact/improvement sector is relative-cohomology trivial or class-only scalar with no vector/tensor/derivative hair",
        "mathematical_form": "B_imp=dC and int_A dB_imp=0; n_mu P_loc_nu T_B^{mu nu}=0; T_B^TF=T_B^vector=0; partial_t,r,frame T_B=0",
        "zeros_or_owns": "zeros epsilon_B_flux_abs and its R7/R8/R4/R9/R11 leakage",
        "required_evidence": "parent-selected relative class, boundary Euler equation, no-hair theorem, or source-backed boundary flux coefficients",
        "current_status": "boundary_cohomology_nohair_certificate_failed_current_claim",
        "accepted_for_claim": "false",
    },
    {
        "clause_id": "BZTC552_4_Hamiltonian_mass_projector",
        "parent_action_clause": "replace independent/topological Pi_M credit with a Hamiltonian mass-charge map fixed by Q_tau",
        "mathematical_form": "ell_H[S,tau]=int_S Q_tau; Pi_M^H J_H:=ell_H[J_H;tau,S] omega_M^H with int_S omega_M^H=1 and delta Pi_M^H=0 at fixed charge branch",
        "zeros_or_owns": "targets epsilon_commutator and epsilon_projector_variation by making the mass channel a charge definition, not a readout projector",
        "required_evidence": "charge integrability, fixed S/tau/reference, equality to Hilbert/source current, and proof that no Hodge/domain projector variation remains",
        "current_status": "best_first_repair_candidate_not_promoted",
        "accepted_for_claim": "false",
    },
    {
        "clause_id": "BZTC552_5_worldtube_denominator_glue",
        "parent_action_clause": "M_H_ref is the dressed Hamiltonian/Noether source charge and the same quantity that calibrates orbital GM",
        "mathematical_form": "M_H_ref=(G_ref)^-1 int_S Q_tau = M_source[W]; GM_orbit=G_ref M_H_ref in the same observed frame",
        "zeros_or_owns": "zeros epsilon_MHref_calibration_abs and R1/R9/R11 denominator leakage",
        "required_evidence": "worldtube source-measure glue, one observed coframe, constant G_ref, Poisson/Gauss/orbital readout theorem",
        "current_status": "worldtube_glue_route_known_GR_style_but_not_inherited_for_current_MTS",
        "accepted_for_claim": "false",
    },
    {
        "clause_id": "BZTC552_6_extra_sector_no_charge",
        "parent_action_clause": "all motion/time/domain/memory/range/boundary/projector extra sectors carry no independent local exterior mass charge or are retained as scored residuals",
        "mathematical_form": "Delta_nonEH=Delta_extra=Delta_frame=0 by gauge/topology/positive no-source theorem, otherwise explicit coefficient vector",
        "zeros_or_owns": "prevents BRR545 repair from hiding charge in a different local residual channel",
        "required_evidence": "sector-by-sector silence theorem or executable coefficient/profile residual rows",
        "current_status": "sector_queue_open",
        "accepted_for_claim": "false",
    },
    {
        "clause_id": "BZTC552_7_no_cancellation_envelope_identity",
        "parent_action_clause": "BRR545 zero theorem must be componentwise or absolute-envelope bounded, never cancellation-based",
        "mathematical_form": "epsilon_BRR545_abs = |epsilon_Delta_symp|+|epsilon_B_flux|+|epsilon_commutator|+|epsilon_projector_variation|+|epsilon_MHref|",
        "zeros_or_owns": "converts all failed clauses into explicit local locks instead of allowing a net-zero bookkeeping trick",
        "required_evidence": "componentwise theorem-zero certificates or source-backed numeric/profile rows for every mapped lock",
        "current_status": "envelope_written_unfilled",
        "accepted_for_claim": "false",
    },
    {
        "clause_id": "BZTC552_8_PPN_readout_after_BRR545",
        "parent_action_clause": "after BRR545, the same charge must generate the weak-field metric and PPN coefficients",
        "mathematical_form": "g_00=-1+2G_ref M_H_ref/r+O(r^-2); gamma-1=0; beta-1=0; alpha_i=xi=zeta_i=0 or bounded residual vector",
        "zeros_or_owns": "prevents a Newton-looking mass theorem from being mislabelled as local GR",
        "required_evidence": "weak-field expansion from the same parent action through PPN order",
        "current_status": "not_reached",
        "accepted_for_claim": "false",
    },
]


CLAUSE_TEST_ROWS = [
    {
        "test_id": "CT552_0_reference_symplectic",
        "BRR545_component": "epsilon_Delta_symp_abs",
        "required_clauses": "BZTC552_0;BZTC552_2;BZTC552_7",
        "current_result": "fail_current_claim",
        "missing": "fixed parent reference subtraction and Delta_symp theorem-zero/source-backed value",
        "accepted_for_claim": "false",
    },
    {
        "test_id": "CT552_1_boundary_flux",
        "BRR545_component": "epsilon_B_flux_abs",
        "required_clauses": "BZTC552_0;BZTC552_3;BZTC552_7",
        "current_result": "fail_current_claim",
        "missing": "relative cohomology/nohair boundary theorem or boundary flux coefficients/profiles",
        "accepted_for_claim": "false",
    },
    {
        "test_id": "CT552_2_projector_commutator",
        "BRR545_component": "epsilon_commutator",
        "required_clauses": "BZTC552_0;BZTC552_4;BZTC552_5;BZTC552_7",
        "current_result": "repair_candidate_open",
        "missing": "Hamiltonian Pi_M charge integrability and equality to same-frame Hilbert/source current",
        "accepted_for_claim": "false",
    },
    {
        "test_id": "CT552_3_projector_variation",
        "BRR545_component": "epsilon_projector_variation",
        "required_clauses": "BZTC552_4;BZTC552_7",
        "current_result": "repair_candidate_open",
        "missing": "proof that no Hodge/domain/source-space projector variation survives",
        "accepted_for_claim": "false",
    },
    {
        "test_id": "CT552_4_denominator_reference",
        "BRR545_component": "epsilon_MHref_calibration_abs",
        "required_clauses": "BZTC552_5;BZTC552_8",
        "current_result": "fail_current_claim",
        "missing": "same-frame measured-GM denominator, worldtube source-measure glue, and Gauss/orbital readout",
        "accepted_for_claim": "false",
    },
    {
        "test_id": "CT552_5_extra_sector_leak_check",
        "BRR545_component": "all_components",
        "required_clauses": "BZTC552_1;BZTC552_6",
        "current_result": "fail_current_claim",
        "missing": "field-specific silence/source-charge proofs for all extra sectors",
        "accepted_for_claim": "false",
    },
    {
        "test_id": "CT552_6_first_local_lock_R7_alpha3",
        "BRR545_component": "R7_alpha3",
        "required_clauses": "BZTC552_3;BZTC552_4;BZTC552_7",
        "current_result": "cannot_fill",
        "missing": "boundary alpha3 coefficient/theorem-zero and projector alpha3 coefficient/theorem-zero",
        "accepted_for_claim": "false",
    },
    {
        "test_id": "CT552_7_no_cheat_policy",
        "BRR545_component": "all_components",
        "required_clauses": "BZTC552_7",
        "current_result": "pass_policy",
        "missing": "none for policy; values/theorems still missing",
        "accepted_for_claim": "false",
    },
]


FIRST_REPAIR_ROWS = [
    {
        "repair_id": "HPR552_0_replace_independent_PiM",
        "repair_move": "define the local mass channel from the parent Hamiltonian/Noether charge rather than an independent topological or Hodge Pi_M selector",
        "mathematical_form": "ell_H[S,tau]=int_S Q_tau; M_H_ref=G_ref^-1 ell_H; Pi_M^H is only a representative of this charge map",
        "what_it_repairs": "wrong conserved object risk; post-readout projector risk; part of commutator/projector variation risk",
        "remaining_debt": "charge integrability, reference subtraction, same Hilbert source equality, and no extra charge sectors",
        "current_result": "best_first_repair_candidate",
        "accepted_for_claim": "false",
    },
    {
        "repair_id": "HPR552_1_reference_boundary_pairing",
        "repair_move": "tie Q_tau to the same B_ref/GHY/topological boundary pair used for both inner worldtube and outer linking surface",
        "mathematical_form": "Delta_H[S2,S1]=int_A dQ_tau + int_boundary(delta Q_tau - tau dot Theta) with fixed B_ref and zero extra boundary flux",
        "what_it_repairs": "reference drift and boundary flux terms inside BRR545",
        "remaining_debt": "B_ref superselection and relative boundary nohair theorem are not yet derived",
        "current_result": "required_partner_clause",
        "accepted_for_claim": "false",
    },
    {
        "repair_id": "HPR552_2_same_frame_denominator",
        "repair_move": "make the denominator the same dressed source charge used by the orbital inverse-square readout",
        "mathematical_form": "M_source[W]=G_ref^-1 int_S Q_tau and a_r=-G_ref M_source/r^2+controlled PPN terms",
        "what_it_repairs": "M_H_ref calibration and WEP/source-charge denominator leakage",
        "remaining_debt": "one observed coframe, Poisson/Gauss theorem, and PPN expansion are not yet proved",
        "current_result": "required_partner_clause",
        "accepted_for_claim": "false",
    },
    {
        "repair_id": "HPR552_3_BRR545_zero_condition",
        "repair_move": "state the conditional theorem explicitly",
        "mathematical_form": "if BZTC552_0..BZTC552_8 pass componentwise, then epsilon_BRR545_abs=0 and first local locks may be attempted as theorem-zero rows",
        "what_it_repairs": "turns the closure-only branch into a finite parent-action proof target",
        "remaining_debt": "all current clauses are open or conditional; no theorem is signed",
        "current_result": "conditional_theorem_target_only",
        "accepted_for_claim": "false",
    },
    {
        "repair_id": "HPR552_4_no_numeric_shortcut",
        "repair_move": "do not fill R7_alpha3 or any local lock until the parent-action repair supplies theorem-zero rows or source-backed coefficients",
        "mathematical_form": "no coefficient, no amplitude, no theorem-zero => no local lock pass",
        "what_it_repairs": "prevents the local-GR route from being promoted on placeholder data",
        "remaining_debt": "the next checkpoint must test HPR552_0 directly",
        "current_result": "policy_pass",
        "accepted_for_claim": "false",
    },
]


OBSTRUCTION_ROWS = [
    {
        "obstruction_id": "OBS552_0_no_explicit_MTS_parent_Lagrangian",
        "obstruction": "the current corpus does not yet provide one fully varied parent Lagrangian containing the BRR545-relevant variables",
        "blocks": "BZTC552_0;BZTC552_1",
        "repair": "write or extract the parent action with field list, variations, boundary term, and symplectic potential",
        "accepted_for_claim": "false",
    },
    {
        "obstruction_id": "OBS552_1_boundary_reference_not_superselected",
        "obstruction": "reference subtraction and boundary relative class remain selectable rather than parent-fixed",
        "blocks": "BZTC552_2;BZTC552_3",
        "repair": "derive B_ref and relative boundary class from action/topology/stationarity or retain numeric flux rows",
        "accepted_for_claim": "false",
    },
    {
        "obstruction_id": "OBS552_2_Hamiltonian_PiM_not_integrated",
        "obstruction": "Hamiltonian Pi_M is a good candidate but not yet integrated into source-current equality and denominator calibration",
        "blocks": "BZTC552_4;BZTC552_5",
        "repair": "test whether Pi_M can be eliminated in favour of Q_tau without losing same-frame Hilbert/source equality",
        "accepted_for_claim": "false",
    },
    {
        "obstruction_id": "OBS552_3_extra_sector_silence_open",
        "obstruction": "motion/time/domain/memory/range/projector sectors are not yet all positive source-free/topological in compact local exterior",
        "blocks": "BZTC552_1;BZTC552_6",
        "repair": "field-specific Euler/source/boundary silence proofs or coefficient maps",
        "accepted_for_claim": "false",
    },
    {
        "obstruction_id": "OBS552_4_PPN_readout_not_done",
        "obstruction": "even a BRR545 zero theorem would still need weak-field metric/PPN readout from the same action",
        "blocks": "BZTC552_8",
        "repair": "derive metric readout through gamma, beta, alpha_i, xi, zeta_i or score residuals",
        "accepted_for_claim": "false",
    },
    {
        "obstruction_id": "OBS552_5_transition_scale_unowned",
        "obstruction": "local/cosmology/galaxy coexistence still needs ell_tr/L_cg or activation scale from the same parent operator/source structure",
        "blocks": "unified_field_theory_claim",
        "repair": "derive transition scale from operator spectrum, source measure, or topological sector rather than arena switching",
        "accepted_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D552_0_contract_written",
        "status": "BRR545_parent_action_zero_theorem_contract_written",
        "meaning": "the closure-only branch now has exact action-level clauses that would turn it into a derivation route",
        "claim_status": "contract_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D552_1_first_repair_candidate",
        "status": "Hamiltonian_PiM_repair_candidate_selected",
        "meaning": "the least-cheaty first repair is to make the mass channel a Hamiltonian/Noether charge map rather than an independent projector",
        "claim_status": "candidate_not_promotion",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D552_2_BRR545_status",
        "status": "still_unfilled",
        "meaning": "no BRR545 component is theorem-zero or source-backed yet",
        "claim_status": "BRR545_not_claimable",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D552_3_local_GR_status",
        "status": "local_GR_still_closure_only_until_repaired",
        "meaning": "current local-GR transition route remains closure-only, not derived",
        "claim_status": "local_GR_claim_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D552_4_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "BRR545_PARENT_ACTION_ZERO_THEOREM",
        "previous_status": "closure_only_until_parent_action_zero_theorem_or_numeric_bound_fill",
        "new_status": "zero_theorem_contract_written_not_satisfied",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "HAMILTONIAN_PIM_REPAIR",
        "previous_status": "candidate_definition_not_claim",
        "new_status": "selected_as_first_repair_clause_to_test",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR_TRANSITION_ROUTE",
        "previous_status": "closure_only_until_parent_action_zero_theorem_or_numeric_bound_fill",
        "new_status": "closure_only_but_with_exact_parent_action_contract",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_MEASURE_THEOREM",
        "previous_status": "still_blocked_BRR545_envelope_unfilled_and_denominator_missing",
        "new_status": "still_blocked_until_Hamiltonian_PiM_worldtube_denominator_clause_passes",
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
    prior_validation = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_551_VALIDATION.csv"))
    prior_fails = [row for row in prior_validation if row.get("result") == "fail"]
    envelope_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_RESIDUAL_ENVELOPE.csv"))
    lock_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_LOCAL_LOCK_PREFLIGHT.csv"))
    demotion_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_CLOSURE_DEMOTION_DECISION.csv"))
    boundary_contract = read_csv(Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv"))
    min_blocks = read_csv(Path("source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv"))
    min_fixed = read_csv(Path("source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv"))
    min_chain = read_csv(Path("source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_DERIVED_CHAIN.csv"))
    source_owner = read_csv(Path("source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv"))
    worldtube = read_csv(Path("source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv"))
    pim_algebra = read_csv(Path("source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv"))
    pim_variation = read_csv(Path("source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv"))
    claim_contract_rows = [row for row in ZERO_THEOREM_CONTRACT_ROWS if row["accepted_for_claim"] == "true"]
    claim_test_rows = [row for row in CLAUSE_TEST_ROWS if row["accepted_for_claim"] == "true"]
    claim_repair_rows = [row for row in FIRST_REPAIR_ROWS if row["accepted_for_claim"] == "true"]
    return [
        {
            "check_id": "V552_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V552_1_prior_551_clean",
            "result": "pass" if len(prior_validation) == 8 and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_validation)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V552_2_BRR545_evidence_loaded",
            "result": "pass" if len(envelope_rows) == 6 and len(lock_rows) == 8 and len(demotion_rows) == 5 else "fail",
            "detail": f"envelope={len(envelope_rows)};lock_preflight={len(lock_rows)};demotion={len(demotion_rows)}",
        },
        {
            "check_id": "V552_3_parent_contract_evidence_loaded",
            "result": "pass"
            if len(boundary_contract) == 7
            and len(min_blocks) == 7
            and len(min_fixed) == 9
            and len(min_chain) == 6
            and len(source_owner) >= 10
            and len(worldtube) == 6
            else "fail",
            "detail": f"boundary_contract={len(boundary_contract)};min_blocks={len(min_blocks)};min_fixed={len(min_fixed)};min_chain={len(min_chain)};source_owner={len(source_owner)};worldtube={len(worldtube)}",
        },
        {
            "check_id": "V552_4_PiM_evidence_loaded",
            "result": "pass" if len(pim_algebra) == 9 and len(pim_variation) == 9 else "fail",
            "detail": f"pim_algebra={len(pim_algebra)};pim_variation={len(pim_variation)}",
        },
        {
            "check_id": "V552_5_contract_attempt_complete",
            "result": "pass" if len(ZERO_THEOREM_CONTRACT_ROWS) == 9 and len(CLAUSE_TEST_ROWS) == 8 else "fail",
            "detail": f"contract_rows={len(ZERO_THEOREM_CONTRACT_ROWS)};clause_tests={len(CLAUSE_TEST_ROWS)}",
        },
        {
            "check_id": "V552_6_repair_attempt_complete",
            "result": "pass" if len(FIRST_REPAIR_ROWS) == 5 and len(OBSTRUCTION_ROWS) == 6 else "fail",
            "detail": f"repair_rows={len(FIRST_REPAIR_ROWS)};obstruction_rows={len(OBSTRUCTION_ROWS)}",
        },
        {
            "check_id": "V552_7_no_claim_rows",
            "result": "pass" if not claim_contract_rows and not claim_test_rows and not claim_repair_rows else "fail",
            "detail": f"claim_contract={len(claim_contract_rows)};claim_tests={len(claim_test_rows)};claim_repair={len(claim_repair_rows)}",
        },
        {
            "check_id": "V552_8_no_overclaim",
            "result": "pass" if not claim_contract_rows and not claim_test_rows and not claim_repair_rows else "fail",
            "detail": "BRR545_filled=false; Hamiltonian_PiM_repair_passed=false; source_measure=false; Newton=false; PPN=false; local_GR=false",
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
    return f"""# 552 - Y5 Parent Action BRR545 Zero Theorem Contract or First Repair Attempt

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The local-GR route is still not derived, but the closure-only label is now repairable in a precise way.

The exact parent-action contract is:

```text
diffeomorphic parent action
-> EH/Hamiltonian local fixed point
-> fixed reference + no boundary hair
-> Hamiltonian mass charge replaces independent Pi_M
-> same-frame dressed source denominator
-> no-cancellation BRR545 envelope zero
-> weak-field PPN readout
```

The first repair candidate is therefore not another fitted projector. It is to define the mass channel by the Hamiltonian/Noether charge `Q_tau` and demote independent/topological `Pi_M` credit unless it equals that charge map.

That is promising, but it is not yet a pass. Boundary/reference, source-measure denominator, extra-sector silence, and PPN readout remain open.

## 2. Parent-Action BRR545 Zero-Theorem Contract

{markdown_table(ZERO_THEOREM_CONTRACT_ROWS)}

## 3. Clause Tests Against BRR545

{markdown_table(CLAUSE_TEST_ROWS)}

## 4. First Repair Attempt

{markdown_table(FIRST_REPAIR_ROWS)}

## 5. Obstruction Ledger

{markdown_table(OBSTRUCTION_ROWS)}

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
MTS has a BRR545 parent-action zero-theorem contract.
MTS has selected the Hamiltonian/Noether charge map as the first repair candidate for Pi_M.
MTS has a precise route for turning closure-only local GR into a derivation target.
```

Forbidden:

```text
MTS has passed BRR545.
MTS has proved the Hamiltonian Pi_M repair.
MTS has derived source-measure, measured GM, Newton, PPN, or local GR.
```

## 11. Practical Read

This is progress in the right direction. The branch is not being hammered for failing a finished proof; it is being turned into an engineering spec. The cleanest next move is to test whether `Pi_M` can be eliminated as an independent object and replaced by the parent Hamiltonian mass charge without breaking source equality or denominator calibration.

## 12. Next Target

`{NEXT_TARGET}`

Next: test the Hamiltonian-PiM repair clause directly. If it cannot be made charge-integrable and same-frame, keep the commutator/projector residual row active.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-parent-action-BRR545-zero-theorem-contract-or-first-repair-attempt"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (ZERO_THEOREM_CONTRACT_PATH, ZERO_THEOREM_CONTRACT_ROWS),
        (CLAUSE_TESTS_PATH, CLAUSE_TEST_ROWS),
        (FIRST_REPAIR_ATTEMPT_PATH, FIRST_REPAIR_ROWS),
        (OBSTRUCTION_LEDGER_PATH, OBSTRUCTION_ROWS),
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
        "zero_theorem_contract": str(ROOT / ZERO_THEOREM_CONTRACT_PATH),
        "clause_tests": str(ROOT / CLAUSE_TESTS_PATH),
        "first_repair_attempt": str(ROOT / FIRST_REPAIR_ATTEMPT_PATH),
        "obstruction_ledger": str(ROOT / OBSTRUCTION_LEDGER_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "zero_theorem_contract_rows": len(ZERO_THEOREM_CONTRACT_ROWS),
        "clause_test_rows": len(CLAUSE_TEST_ROWS),
        "first_repair_rows": len(FIRST_REPAIR_ROWS),
        "obstruction_rows": len(OBSTRUCTION_ROWS),
        "BRR545_values_filled": False,
        "Hamiltonian_PiM_repair_passed": False,
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
        "done\nprivate_no_github\nBRR545_parent_action_zero_theorem_contract_written_Hamiltonian_PiM_repair_candidate_selected_not_promoted_no_Newton_PPN_or_local_GR_promotion\n",
        encoding="utf-8",
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
