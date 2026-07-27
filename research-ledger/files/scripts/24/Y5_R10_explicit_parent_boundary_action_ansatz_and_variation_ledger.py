from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_explicit_parent_boundary_action_ansatz_written_variation_ledger_conditional_no_FB5540_zero_nonclaim"
CLAIM_CEILING = "explicit_parent_boundary_action_ansatz_and_variation_ledger_only_no_stable_Hamiltonian_source_charge_no_Newton_no_PPN_no_R10_no_R11_no_local_GR_claim"
NEXT_TARGET = "668-Y5-R10-sector-Lagrangian-owner-and-boundary-condition-lock.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "667-Y5-R10-explicit-parent-boundary-action-ansatz-and-variation-ledger.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "666_doc": ROOT / "666-Y5-R10-parent-boundary-reference-lock-or-FB554-0-source-value-hunt.md",
    "666_validation": RESIDUALS / "P8_Y5_BRR545_666_VALIDATION.csv",
    "666_parent_lock": RESIDUALS / "P8_Y5_R10_666_PARENT_LOCK_ATTEMPT.csv",
    "666_clause_test": RESIDUALS / "P8_Y5_R10_666_BOUNDARY_REFERENCE_CLAUSE_TEST.csv",
    "666_source_hunt": RESIDUALS / "P8_Y5_R10_666_FB5540_SOURCE_VALUE_HUNT_LEDGER.csv",
    "665_validation": RESIDUALS / "P8_Y5_BRR545_665_VALIDATION.csv",
    "665_theorem_zero": RESIDUALS / "P8_Y5_R10_665_THEOREM_ZERO_ATTEMPT.csv",
    "664_validation": RESIDUALS / "P8_Y5_BRR545_664_VALIDATION.csv",
    "664_integrability_attempt": RESIDUALS / "P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv",
    "554_validation": RESIDUALS / "P8_Y5_BRR545_554_VALIDATION.csv",
    "554_fill_rows": RESIDUALS / "P8_Y5_HAMILTONIAN_INTEGRABILITY_SOURCE_EQUALITY_FILL_ROWS.csv",
    "553_validation": RESIDUALS / "P8_Y5_BRR545_553_VALIDATION.csv",
    "553_doc": ROOT / "553-Y5-Hamiltonian-PiM-repair-clause-test-or-bound-fill.md",
    "552_validation": RESIDUALS / "P8_Y5_BRR545_552_VALIDATION.csv",
    "552_zero_contract": RESIDUALS / "P8_Y5_BRR545_PARENT_ACTION_ZERO_THEOREM_CONTRACT.csv",
    "552_repair_attempt": RESIDUALS / "P8_Y5_BRR545_FIRST_REPAIR_ATTEMPT.csv",
    "550_validation": RESIDUALS / "P8_Y5_BRR545_550_VALIDATION.csv",
    "550_doc": ROOT / "550-Y5-projector-symplectic-silence-certificate-or-commutator-bound-fill.md",
    "549_validation": RESIDUALS / "P8_Y5_BRR545_549_VALIDATION.csv",
    "549_doc": ROOT / "549-Y5-boundary-cohomology-nohair-certificate-or-boundary-flux-bound-fill.md",
    "548_validation": RESIDUALS / "P8_Y5_BRR545_548_VALIDATION.csv",
    "548_doc": ROOT / "548-Y5-boundary-reference-theorem-certificate-attempt-or-first-numeric-bound-fill.md",
    "545_contract": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv",
    "545_ownership": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_PARENT_OWNERSHIP_AUDIT.csv",
    "510_doc": ROOT / "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
    "505_doc": ROOT / "505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md",
    "457_doc": ROOT / "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
    "hamiltonian_contract": RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
    "noether_chain": RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
    "worldtube_clauses": RESIDUALS / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
}


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


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


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    roles = {
        "666_doc": "immediate predecessor requesting explicit parent boundary action ansatz",
        "666_validation": "prior 666 validation",
        "666_parent_lock": "parent lock attempt rows",
        "666_clause_test": "clause gaps that the action ansatz must address",
        "666_source_hunt": "source-value fallback rows",
        "665_validation": "prior 665 validation",
        "665_theorem_zero": "FB554_0 theorem-zero attempt",
        "664_validation": "prior 664 validation",
        "664_integrability_attempt": "Hamiltonian integrability attempt",
        "554_validation": "prior 554 validation",
        "554_fill_rows": "original FB554_0 unfilled row",
        "553_validation": "prior 553 validation",
        "553_doc": "Hamiltonian PiM repair failure",
        "552_validation": "prior 552 validation",
        "552_zero_contract": "BRR545 parent-action zero-theorem contract",
        "552_repair_attempt": "Hamiltonian PiM first repair candidate",
        "550_validation": "prior 550 validation",
        "550_doc": "projector symplectic silence failure",
        "549_validation": "prior 549 validation",
        "549_doc": "boundary cohomology/no-hair failure",
        "548_validation": "prior 548 validation",
        "548_doc": "reference-lock failure",
        "545_contract": "minimal parent boundary/reference clauses",
        "545_ownership": "parent ownership audit",
        "510_doc": "worldtube source-measure glue reference",
        "505_doc": "conditional Noether mass charge closure",
        "457_doc": "Hamiltonian boundary charge attempt",
        "hamiltonian_contract": "Hamiltonian charge contract rows",
        "noether_chain": "parent Noether closure derivation chain",
        "worldtube_clauses": "parent worldtube glue clauses",
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


def action_ansatz_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "ansatz_id": "PBA667_0_field_bundle",
            "object": "Phi=(g_mu_nu,psi_matter,X_MTS,chi_B,C_top,tau)",
            "mathematical_form": "fields include observed metric/coframe, matter, retained MTS extra fields X_MTS, boundary markers chi_B, relative/topological class C_top, and local time generator tau",
            "purpose": "make every possible leakage channel a varied parent object rather than a post-readout knob",
            "derived_now": "definition_level_ansatz",
            "gap": "field content and sector dynamics are not yet uniquely fixed by the corpus",
            "valid_for_claim": "false",
            "source_paths": source_list("666_clause_test", "545_contract"),
            "generated_utc": now,
        },
        {
            "ansatz_id": "PBA667_1_bulk_action",
            "object": "L_parent",
            "mathematical_form": "L_parent=(16*pi*G_ref)^-1(R-2*Lambda_loc)*epsilon + L_matter[g_obs,psi] + L_X[g,X_MTS,nabla X_MTS] + dB_top + L_residual",
            "purpose": "separate EH local operator, observed matter coupling, MTS extra sectors, exact/topological terms, and residual debts",
            "derived_now": "conditional_ansatz_written",
            "gap": "L_X and L_residual are not yet specified well enough to compute Theta_X, Q_X, or positivity/silence",
            "valid_for_claim": "false",
            "source_paths": source_list("505_doc", "552_zero_contract", "noether_chain"),
            "generated_utc": now,
        },
        {
            "ansatz_id": "PBA667_2_boundary_action",
            "object": "B_total",
            "mathematical_form": "B_total=B_GHY[g;G_ref]+B_ref[gamma_ref,tau_ref,C_top]+B_class[chi_B,C_top]+B_ct[fixed branch]",
            "purpose": "put the reference subtraction and boundary class into the action before source/readout fitting",
            "derived_now": "conditional_ansatz_written",
            "gap": "B_ref and B_class are named but not parent-selected or varied from a unique MTS principle",
            "valid_for_claim": "false",
            "source_paths": source_list("548_doc", "549_doc", "545_contract"),
            "generated_utc": now,
        },
        {
            "ansatz_id": "PBA667_3_charge_definition",
            "object": "Q_tau^MTS",
            "mathematical_form": "J_tau=Theta(Phi,L_tau Phi)-i_tau L_parent; J_tau=dQ_tau^MTS+C_tau; Q_tau^MTS=Q_EH+Q_X+Q_top+Q_boundary",
            "purpose": "replace independent Pi_M proof credit with the parent Noether/Hamiltonian charge",
            "derived_now": "formal_Noether_shape_available",
            "gap": "Q_X, C_tau, and equality to the same-frame Hilbert/source mass are not computed",
            "valid_for_claim": "false",
            "source_paths": source_list("510_doc", "553_doc", "552_repair_attempt"),
            "generated_utc": now,
        },
        {
            "ansatz_id": "PBA667_4_reference_rule",
            "object": "H_ref and Delta_ref",
            "mathematical_form": "H_ref[S,tau]=int_S B_ref; Delta_ref=H_ref[S,tau]-H_ref[fixed branch]",
            "purpose": "make reference shifts auditable instead of letting them absorb source calibration",
            "derived_now": "ledger_definition_written",
            "gap": "partial_source,r,t,frame,lambda Delta_ref=0 remains an imposed clause, not derived",
            "valid_for_claim": "false",
            "source_paths": source_list("548_doc", "666_parent_lock"),
            "generated_utc": now,
        },
        {
            "ansatz_id": "PBA667_5_denominator_rule",
            "object": "M_H_ref",
            "mathematical_form": "M_H_ref=G_ref^-1 int_S Q_tau^MTS with same tau and same observed frame; GM_orbit=G_ref*M_H_ref only after Gauss/readout",
            "purpose": "prevent orbital GM or reference-only mass from becoming a circular denominator",
            "derived_now": "guardrail_definition_written",
            "gap": "worldtube source equality and Poisson/Gauss/orbital readout remain downstream",
            "valid_for_claim": "false",
            "source_paths": source_list("510_doc", "hamiltonian_contract", "worldtube_clauses"),
            "generated_utc": now,
        },
    ]


def variation_ledger_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "step_id": "VL667_0_total_variation",
            "variation_statement": "delta S_parent=int_M E_A delta Phi^A + int_boundary(Theta_EH+Theta_X+delta B_total)",
            "derived_piece": "covariant phase-space form for the ansatz",
            "required_zero_or_lock": "well-defined variational principle with boundary conditions fixed before readout",
            "current_result": "conditional_formal_step",
            "retained_residual_if_fail": "undefined_Theta_or_boundary_variation",
            "valid_for_claim": "false",
            "source_paths": source_list("545_contract", "505_doc"),
            "generated_utc": now,
        },
        {
            "step_id": "VL667_1_Noether_current",
            "variation_statement": "J_tau=Theta(Phi,L_tau Phi)-i_tau L_parent; dJ_tau=-E_A L_tau Phi",
            "derived_piece": "diffeomorphism Noether current if the parent action is covariant",
            "required_zero_or_lock": "all retained fields varied and E_A=0 in the compact exterior",
            "current_result": "conditional_formal_step",
            "retained_residual_if_fail": "C_extra;C_projector;C_boundary;C_ref",
            "valid_for_claim": "false",
            "source_paths": source_list("noether_chain", "worldtube_clauses"),
            "generated_utc": now,
        },
        {
            "step_id": "VL667_2_charge_decomposition",
            "variation_statement": "J_tau=dQ_tau^MTS+C_tau; C_tau=C_EH+C_X+C_projector+C_boundary+C_ref",
            "derived_piece": "surface charge plus constraints/leakage decomposition",
            "required_zero_or_lock": "C_X=C_projector=C_boundary=C_ref=0 or source-backed bounds",
            "current_result": "conditional_with_retained_terms",
            "retained_residual_if_fail": "radial_closure_over_MH;symplectic_boundary_flux_over_MH;Delta_ref_over_MH",
            "valid_for_claim": "false",
            "source_paths": source_list("505_doc", "553_doc", "666_source_hunt"),
            "generated_utc": now,
        },
        {
            "step_id": "VL667_3_Hamiltonian_variation",
            "variation_statement": "delta H_tau[S]=int_S(delta Q_tau^MTS-i_tau Theta_total)-delta H_ref[S]",
            "derived_piece": "candidate Hamiltonian charge variation",
            "required_zero_or_lock": "finite integrable delta H_tau, fixed tau, and fixed H_ref",
            "current_result": "candidate_not_integrability_proof",
            "retained_residual_if_fail": "delta_H_tau_nonintegrable_over_MH;Delta_ref_over_MH",
            "valid_for_claim": "false",
            "source_paths": source_list("664_integrability_attempt", "554_fill_rows"),
            "generated_utc": now,
        },
        {
            "step_id": "VL667_4_integrability_curl",
            "variation_statement": "I_tau(delta1,delta2)=delta1 delta2 H_tau-delta2 delta1 H_tau=int_S i_tau omega_total + curl(delta H_ref)",
            "derived_piece": "exact obstruction to path-independent Hamiltonian mass",
            "required_zero_or_lock": "omega_X, boundary/reference curl, tau variation, and projector/domain variation vanish or are bounded",
            "current_result": "obstruction_identified_not_zeroed",
            "retained_residual_if_fail": "delta_H_tau_nonintegrable_over_MH",
            "valid_for_claim": "false",
            "source_paths": source_list("665_theorem_zero", "666_parent_lock"),
            "generated_utc": now,
        },
        {
            "step_id": "VL667_5_reference_derivative",
            "variation_statement": "Delta_ref derivative = partial_{source,r,t,frame,lambda} H_ref[S,tau]",
            "derived_piece": "reference-lock test expression",
            "required_zero_or_lock": "H_ref depends only on fixed branch data and C_top",
            "current_result": "test_written_not_passed",
            "retained_residual_if_fail": "Delta_ref_over_MH",
            "valid_for_claim": "false",
            "source_paths": source_list("548_doc", "666_clause_test"),
            "generated_utc": now,
        },
        {
            "step_id": "VL667_6_boundary_flux",
            "variation_statement": "Phi_boundary=int_boundary(delta Q_tau^extra-i_tau Theta_extra)+int_boundary delta B_class",
            "derived_piece": "boundary/projector/non-EH symplectic leakage channel",
            "required_zero_or_lock": "relative cohomology triviality, no vector/tensor hair, projector silence",
            "current_result": "test_written_not_passed",
            "retained_residual_if_fail": "symplectic_boundary_flux_over_MH;B_zero_flux_over_MH;Delta_symp_over_MH",
            "valid_for_claim": "false",
            "source_paths": source_list("549_doc", "550_doc", "545_ownership"),
            "generated_utc": now,
        },
        {
            "step_id": "VL667_7_source_readout",
            "variation_statement": "M_source[W]=G_ref^-1 int_S Q_tau^MTS and a_r=-G_ref*M_source/r^2 only after source-measure and Gauss readout",
            "derived_piece": "denominator/readout guardrail",
            "required_zero_or_lock": "same-frame worldtube source equality and weak-field Poisson/Gauss limit",
            "current_result": "not_reached",
            "retained_residual_if_fail": "M_H_ref;Delta_cal;PPN_vector",
            "valid_for_claim": "false",
            "source_paths": source_list("510_doc", "hamiltonian_contract", "worldtube_clauses"),
            "generated_utc": now,
        },
    ]


def fb5540_term_map_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "map_id": "TM667_0_delta_H_tau",
            "FB5540_quantity": "delta_H_tau_nonintegrable_over_MH",
            "ansatz_expression": "M_H_ref^-1 * |int_S i_tau omega_total + curl(delta H_ref)|",
            "EH_status": "zero_under_standard_stationary_EH_boundary_conditions",
            "MTS_extra_status": "retained_until_L_X_and_B_total_are_varied",
            "needed_next": "compute omega_X, boundary/reference curl, and tau/domain variation from explicit sector Lagrangians",
            "valid_for_claim": "false",
            "source_paths": source_list("664_integrability_attempt", "666_source_hunt"),
            "generated_utc": now,
        },
        {
            "map_id": "TM667_1_Delta_ref",
            "FB5540_quantity": "Delta_ref_over_MH",
            "ansatz_expression": "M_H_ref^-1 * |H_ref[S,tau]-H_ref[fixed branch]|",
            "EH_status": "zero_or_constant_only_if_reference branch and boundary conditions are fixed",
            "MTS_extra_status": "retained_until_B_ref_is_parent_selected",
            "needed_next": "specify B_ref and prove derivative silence with respect to source, surface, frame, time, and range",
            "valid_for_claim": "false",
            "source_paths": source_list("548_doc", "666_source_hunt"),
            "generated_utc": now,
        },
        {
            "map_id": "TM667_2_symplectic_boundary_flux",
            "FB5540_quantity": "symplectic_boundary_flux_over_MH",
            "ansatz_expression": "M_H_ref^-1 * |int_boundary(delta Q_tau^extra-i_tau Theta_extra)+delta B_class+projector/domain terms|",
            "EH_status": "zero only under fixed EH boundary conditions with no extra flux",
            "MTS_extra_status": "retained_until_boundary_class_nohair_and_projector_silence_are_parent_owned",
            "needed_next": "derive relative boundary class, no vector/tensor hair, and projector silence from sector action",
            "valid_for_claim": "false",
            "source_paths": source_list("549_doc", "550_doc", "666_source_hunt"),
            "generated_utc": now,
        },
        {
            "map_id": "TM667_3_tau_lock",
            "FB5540_quantity": "time_generator_lock",
            "ansatz_expression": "tau_source=tau_charge=tau_clock=tau_readout and delta tau=0",
            "EH_status": "standard only after a fixed stationary/asymptotic/quasilocal generator is selected",
            "MTS_extra_status": "retained_until_observed_coframe_matter_functor_selects_tau",
            "needed_next": "derive observed time generator from matter/coframe coupling",
            "valid_for_claim": "false",
            "source_paths": source_list("666_clause_test", "hamiltonian_contract"),
            "generated_utc": now,
        },
        {
            "map_id": "TM667_4_M_H_ref",
            "FB5540_quantity": "M_H_ref",
            "ansatz_expression": "G_ref^-1 int_S Q_tau^MTS in the same observed frame",
            "EH_status": "positive for ordinary isolated-source branch after source matching",
            "MTS_extra_status": "retained_until_worldtube_source_and_Gauss_readout_are_derived",
            "needed_next": "derive source-measure equality and Poisson/Gauss/orbital readout",
            "valid_for_claim": "false",
            "source_paths": source_list("510_doc", "worldtube_clauses", "hamiltonian_contract"),
            "generated_utc": now,
        },
    ]


def pass_fail_clause_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "clause_id": "PF667_0_covariant_form",
            "test": "does the ansatz have a covariant phase-space variation form?",
            "result": "pass_conditional",
            "why": "the formal ansatz supplies delta L=E delta Phi+dTheta and J_tau=Theta-i_tau L",
            "blocks_claim": "explicit L_X and boundary data are still not unique",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "PF667_1_reference_lock",
            "test": "does the ansatz prove Delta_ref=0?",
            "result": "fail_current_claim",
            "why": "B_ref is named but not selected by a current parent principle",
            "blocks_claim": "Delta_ref_over_MH retained",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "PF667_2_integrability",
            "test": "does the ansatz prove delta_H_tau_nonintegrable=0?",
            "result": "fail_current_claim",
            "why": "omega_X, reference curl, tau variation, and domain/projector variation are not computed",
            "blocks_claim": "delta_H_tau_nonintegrable_over_MH retained",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "PF667_3_boundary_flux",
            "test": "does the ansatz prove symplectic_boundary_flux=0?",
            "result": "fail_current_claim",
            "why": "boundary class/nohair and projector silence remain unsigned",
            "blocks_claim": "symplectic_boundary_flux_over_MH retained",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "PF667_4_source_denominator",
            "test": "does the ansatz prove M_H_ref is the measured source mass?",
            "result": "fail_current_claim",
            "why": "worldtube source equality and Poisson/Gauss/orbital readout are not reached",
            "blocks_claim": "M_H_ref and Delta_cal retained",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "PF667_5_FB5540_zero",
            "test": "does the ansatz prove FB554_0=0?",
            "result": "fail_current_claim",
            "why": "at least reference lock, integrability, boundary flux, tau lock, and denominator remain unsigned",
            "blocks_claim": "no stable Hamiltonian source charge",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def residual_fallback_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "fallback_id": "RF667_0_LX_theta_Qtau_owner",
            "missing_object": "L_X;Theta_X;Q_X",
            "exact_need": "sector Lagrangian owner and variation for every retained MTS field",
            "feeds_residual": "delta_H_tau_nonintegrable_over_MH;symplectic_boundary_flux_over_MH;C_extra",
            "fallback_status": "MISSING_SECTOR_LAGRANGIAN_OWNER",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "fallback_id": "RF667_1_Bref_owner",
            "missing_object": "B_ref",
            "exact_need": "reference boundary functional selected before source/readout fitting and derivative-silent",
            "feeds_residual": "Delta_ref_over_MH;Delta_symp_over_MH",
            "fallback_status": "MISSING_PARENT_REFERENCE_FUNCTIONAL",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "fallback_id": "RF667_2_boundary_class_owner",
            "missing_object": "B_class;C_top;chi_B",
            "exact_need": "relative boundary class and no-hair condition derived rather than chosen",
            "feeds_residual": "B_zero_flux_over_MH;symplectic_boundary_flux_over_MH",
            "fallback_status": "MISSING_BOUNDARY_CLASS_SELECTION",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "fallback_id": "RF667_3_tau_owner",
            "missing_object": "tau",
            "exact_need": "same observed time generator selected by matter/coframe coupling",
            "feeds_residual": "time_generator_lock;Delta_frame;Gdot",
            "fallback_status": "MISSING_OBSERVED_TAU_FUNCTOR",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "fallback_id": "RF667_4_source_readout_owner",
            "missing_object": "M_H_ref;GM_orbit relation",
            "exact_need": "worldtube source equality plus Poisson/Gauss/orbital readout",
            "feeds_residual": "M_H_ref;Delta_cal;PPN_vector",
            "fallback_status": "MISSING_SOURCE_MEASURE_AND_GAUSS_READOUT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def evaluator_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "evaluator_id": "EV667_0_ansatz_written",
            "target": "explicit_parent_boundary_action_ansatz",
            "status": "pass_conditional",
            "reason": "a coherent EH-plus-MTS-extra-plus-boundary ansatz and variation ledger now exists",
            "claim_effect": "formal scaffold only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV667_1_FB5540",
            "target": "FB554_0 theorem-zero",
            "status": "not_claimable",
            "reason": "the variation ledger identifies the obstruction but does not zero reference, boundary, tau, or extra-sector terms",
            "claim_effect": "FB554_0 remains blocked",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV667_2_next_route",
            "target": "sector owner and boundary condition lock",
            "status": "derive_first",
            "reason": "the next proof cannot proceed until L_X/B_ref/B_class/tau ownership is fixed or demoted to residual rows",
            "claim_effect": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def scoreability_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "G667_0_sources_exist",
            "gate": "every cited source path exists",
            "result": "pass",
            "detail": "checked by validation",
            "claim_effect": "evidence plumbing only",
            "generated_utc": now,
        },
        {
            "gate_id": "G667_1_prior_validations_clean",
            "gate": "prior 666/665/664/554/553/552/550/549/548 validations are clean",
            "result": "pass",
            "detail": "checked by validation",
            "claim_effect": "checkpoint chain usable",
            "generated_utc": now,
        },
        {
            "gate_id": "G667_2_ansatz_coverage",
            "gate": "field bundle, bulk action, boundary action, charge, reference, and denominator rules are written",
            "result": "pass_conditional",
            "detail": "ansatz is coherent but not current-MTS proof",
            "claim_effect": "formal scaffold only",
            "generated_utc": now,
        },
        {
            "gate_id": "G667_3_variation_ledger_written",
            "gate": "variation ledger maps delta S through FB554_0 components",
            "result": "pass_nonclaim",
            "detail": "obstructions identified explicitly",
            "claim_effect": "no zero theorem",
            "generated_utc": now,
        },
        {
            "gate_id": "G667_4_FB5540_not_zero",
            "gate": "FB554_0 zero theorem remains blocked",
            "result": "blocked_as_expected",
            "detail": "reference, integrability, boundary flux, tau, and denominator clauses fail current claim",
            "claim_effect": "no stable Hamiltonian source charge",
            "generated_utc": now,
        },
        {
            "gate_id": "G667_5_no_claim_rows",
            "gate": "all generated rows remain nonclaim",
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
            "decision_id": "D667_0_ansatz",
            "status": "written_conditional",
            "meaning": "the explicit parent-boundary action ansatz is now on paper, but it is a scaffold rather than a signed MTS derivation",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
        {
            "decision_id": "D667_1_variation",
            "status": "ledger_written",
            "meaning": "delta S, J_tau, Q_tau, delta H_tau, integrability curl, reference derivative, and boundary flux have been mapped",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
        {
            "decision_id": "D667_2_FB5540",
            "status": "not_zero",
            "meaning": "FB554_0 remains open because L_X, B_ref, boundary class, tau, and M_H_ref are not owned",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
    ]


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for path in FORMALIZATION_WORKBENCH.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def prior_validation_failures(source_id: str) -> list[str]:
    rows = read_csv(SOURCE_PATHS[source_id])
    return [row.get("check_id", row.get("validation_id", "?")) for row in rows if row.get("result") != "pass"]


def validation_rows(
    source_rows: list[dict[str, str]],
    ansatz_rows: list[dict[str, str]],
    variation_rows: list[dict[str, str]],
    term_rows: list[dict[str, str]],
    clause_rows: list[dict[str, str]],
    fallback_rows: list[dict[str, str]],
    evaluator_data: list[dict[str, str]],
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
    add("V667_0_sources_exist", not missing_sources, "missing=" + ";".join(missing_sources))

    prior_ids = ["666_validation", "665_validation", "664_validation", "554_validation", "553_validation", "552_validation", "550_validation", "549_validation", "548_validation"]
    flat_prior_failures = [
        f"{source_id}:{failure}"
        for source_id in prior_ids
        for failure in prior_validation_failures(source_id)
    ]
    add("V667_1_prior_validations_clean", not flat_prior_failures, "prior_failures=" + ";".join(flat_prior_failures))

    ansatz_ids = {row["ansatz_id"] for row in ansatz_rows}
    required_ansatz = {"PBA667_0_field_bundle", "PBA667_1_bulk_action", "PBA667_2_boundary_action", "PBA667_3_charge_definition", "PBA667_4_reference_rule", "PBA667_5_denominator_rule"}
    add("V667_2_ansatz_coverage", required_ansatz.issubset(ansatz_ids), "ansatz_ids=" + ";".join(sorted(ansatz_ids)))

    variation_ids = {row["step_id"] for row in variation_rows}
    required_variation = {"VL667_0_total_variation", "VL667_1_Noether_current", "VL667_2_charge_decomposition", "VL667_3_Hamiltonian_variation", "VL667_4_integrability_curl", "VL667_5_reference_derivative", "VL667_6_boundary_flux", "VL667_7_source_readout"}
    add("V667_3_variation_ledger_coverage", required_variation.issubset(variation_ids), "step_ids=" + ";".join(sorted(variation_ids)))

    term_ids = {row["map_id"] for row in term_rows}
    required_terms = {"TM667_0_delta_H_tau", "TM667_1_Delta_ref", "TM667_2_symplectic_boundary_flux", "TM667_3_tau_lock", "TM667_4_M_H_ref"}
    add("V667_4_FB5540_term_map_coverage", required_terms.issubset(term_ids), "term_ids=" + ";".join(sorted(term_ids)))

    clause_ids = {row["clause_id"] for row in clause_rows}
    required_clauses = {"PF667_0_covariant_form", "PF667_1_reference_lock", "PF667_2_integrability", "PF667_3_boundary_flux", "PF667_4_source_denominator", "PF667_5_FB5540_zero"}
    add("V667_5_clause_test_coverage", required_clauses.issubset(clause_ids), "clause_ids=" + ";".join(sorted(clause_ids)))

    fb_zero_fail = [row for row in clause_rows if row["clause_id"] == "PF667_5_FB5540_zero" and row["result"] == "fail_current_claim"]
    add("V667_6_FB5540_not_zero", len(fb_zero_fail) == 1, "fb_zero_fail_rows=" + str(len(fb_zero_fail)))

    fallback_ids = {row["fallback_id"] for row in fallback_rows}
    required_fallback = {"RF667_0_LX_theta_Qtau_owner", "RF667_1_Bref_owner", "RF667_2_boundary_class_owner", "RF667_3_tau_owner", "RF667_4_source_readout_owner"}
    add("V667_7_residual_fallback_coverage", required_fallback.issubset(fallback_ids), "fallback_ids=" + ";".join(sorted(fallback_ids)))

    all_valid_flags = [
        row.get("valid_for_claim")
        for row_group in (ansatz_rows, variation_rows, term_rows, clause_rows, fallback_rows, evaluator_data)
        for row in row_group
    ]
    add("V667_8_no_generated_claim_rows", all(flag == "false" for flag in all_valid_flags), "valid_for_claim_flags=" + ";".join(sorted(set(all_valid_flags))))

    evaluator_claims = [row for row in evaluator_data if row["valid_for_claim"] != "false" or row["status"] not in {"pass_conditional", "not_claimable", "derive_first"}]
    add("V667_9_evaluator_nonclaim", not evaluator_claims, "claimlike_evaluator_rows=" + str(len(evaluator_claims)))

    blocked_gates = {row["gate_id"] for row in gate_rows if row["result"] == "blocked_as_expected"}
    add("V667_10_blocked_gate_present", "G667_4_FB5540_not_zero" in blocked_gates, "blocked_gates=" + ";".join(sorted(blocked_gates)))

    next_target_rows = [row for row in decision if row["next_action"] == NEXT_TARGET]
    add("V667_11_next_target_selected", bool(next_target_rows), NEXT_TARGET)

    changed = formalization_changed_after_cutoff()
    add("V667_12_formalization_workbench_untouched", changed == 0, "formalization_changed_after_cutoff=" + str(changed))

    add("V667_13_status_nonclaim", STATUS.endswith("nonclaim") and "no_stable_Hamiltonian_source_charge" in CLAIM_CEILING, STATUS)

    return rows


def nonclaim_summary_rows(
    ansatz_rows: list[dict[str, str]],
    variation_rows: list[dict[str, str]],
    term_rows: list[dict[str, str]],
    clause_rows: list[dict[str, str]],
    fallback_rows: list[dict[str, str]],
    evaluator_data: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    blocked_gates = [row["gate_id"] for row in gate_rows if row["result"] in {"blocked_as_expected", "pass_nonclaim", "pass_conditional"}]
    failures = [row["check_id"] for row in validation if row["result"] != "pass"]
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "ansatz_rows": str(len(ansatz_rows)),
            "variation_rows": str(len(variation_rows)),
            "FB5540_term_rows": str(len(term_rows)),
            "clause_rows": str(len(clause_rows)),
            "fallback_rows": str(len(fallback_rows)),
            "evaluator_rows": str(len(evaluator_data)),
            "blocked_or_nonclaim_gates": ";".join(blocked_gates),
            "validation_failures": ";".join(failures),
            "next_target": NEXT_TARGET,
            "generated_utc": now,
        }
    ]


def cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, str]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |\n"
    separator = "| " + " | ".join("---" for _ in fields) + " |\n"
    body = "".join("| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |\n" for row in rows)
    return header + separator + body


def write_document(
    source_rows: list[dict[str, str]],
    ansatz_rows: list[dict[str, str]],
    variation_rows: list[dict[str, str]],
    term_rows: list[dict[str, str]],
    clause_rows: list[dict[str, str]],
    fallback_rows: list[dict[str, str]],
    evaluator_data: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    doc = f"""# 667 - Y5 R10 Explicit Parent Boundary Action Ansatz And Variation Ledger

## Verdict

667 writes the parent-boundary machinery explicitly enough to stop hand-waving:

```text
S_parent = int_M L_parent + int_boundary B_total
L_parent = EH + observed matter + MTS-extra sectors + exact/topological terms + residual terms
B_total  = B_GHY + B_ref + B_class + B_ct
delta H_tau[S] = int_S(delta Q_tau^MTS - i_tau Theta_total) - delta H_ref[S]
```

This is real progress as a formal scaffold. It gives `Theta`, `Q_tau`, `B_ref`, the integrability curl, the reference derivative, and the boundary-flux channel a single ledger.

It does **not** yet prove `FB554_0=0`, because the sector Lagrangians, `B_ref`, boundary class/no-hair rule, tau owner, and source/readout denominator are not parent-owned.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "role"])}

## Action Ansatz

{markdown_table(ansatz_rows, ["ansatz_id", "object", "mathematical_form", "purpose", "derived_now", "gap", "valid_for_claim"])}

## Variation Ledger

{markdown_table(variation_rows, ["step_id", "variation_statement", "derived_piece", "required_zero_or_lock", "current_result", "retained_residual_if_fail", "valid_for_claim"])}

## FB5540 Term Map

{markdown_table(term_rows, ["map_id", "FB5540_quantity", "ansatz_expression", "EH_status", "MTS_extra_status", "needed_next", "valid_for_claim"])}

## Pass Fail Clauses

{markdown_table(clause_rows, ["clause_id", "test", "result", "why", "blocks_claim", "valid_for_claim"])}

## Residual Fallback Rows

{markdown_table(fallback_rows, ["fallback_id", "missing_object", "exact_need", "feeds_residual", "fallback_status", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator_data, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim"])}

## Scoreability Gates

{markdown_table(gate_rows, ["gate_id", "gate", "result", "detail", "claim_effect"])}

## Decision

{markdown_table(decision, ["decision_id", "status", "meaning", "claim_status", "next_action"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "ansatz_rows", "variation_rows", "FB5540_term_rows", "clause_rows", "fallback_rows", "evaluator_rows", "blocked_or_nonclaim_gates", "validation_failures", "next_target"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Interpretation

The route has sharpened again. We can now say exactly what a future parent action must supply: a real `L_X`, a real `B_ref`, a parent-selected boundary class, a tau/coframe owner, and a source/readout denominator theorem. Without those, the Hamiltonian charge is still a candidate operator rather than a physical source mass. With those, `FB554_0` becomes a proper theorem target rather than closure fog.

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    ansatz_rows = action_ansatz_rows()
    variation_rows = variation_ledger_rows()
    term_rows = fb5540_term_map_rows()
    clause_rows = pass_fail_clause_rows()
    fallback_rows = residual_fallback_rows()
    evaluator_data = evaluator_rows()
    gate_rows = scoreability_gate_rows()
    decision = decision_rows()
    validation = validation_rows(source_rows, ansatz_rows, variation_rows, term_rows, clause_rows, fallback_rows, evaluator_data, gate_rows, decision)
    summary_rows = nonclaim_summary_rows(ansatz_rows, variation_rows, term_rows, clause_rows, fallback_rows, evaluator_data, gate_rows, validation)

    write_csv(RESIDUALS / "P8_Y5_R10_667_SOURCE_REGISTER.csv", source_rows, ["source_id", "source_path", "exists", "role", "generated_utc"])
    write_csv(
        RESIDUALS / "P8_Y5_R10_667_PARENT_BOUNDARY_ACTION_ANSATZ.csv",
        ansatz_rows,
        ["ansatz_id", "object", "mathematical_form", "purpose", "derived_now", "gap", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_667_VARIATION_LEDGER.csv",
        variation_rows,
        ["step_id", "variation_statement", "derived_piece", "required_zero_or_lock", "current_result", "retained_residual_if_fail", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_667_FB5540_TERM_MAP.csv",
        term_rows,
        ["map_id", "FB5540_quantity", "ansatz_expression", "EH_status", "MTS_extra_status", "needed_next", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_667_PASS_FAIL_CLAUSES.csv",
        clause_rows,
        ["clause_id", "test", "result", "why", "blocks_claim", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_667_RESIDUAL_FALLBACK_ROWS.csv",
        fallback_rows,
        ["fallback_id", "missing_object", "exact_need", "feeds_residual", "fallback_status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_667_EVALUATOR.csv",
        evaluator_data,
        ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_667_SCOREABILITY_GATES.csv",
        gate_rows,
        ["gate_id", "gate", "result", "detail", "claim_effect", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_667_DECISION.csv",
        decision,
        ["decision_id", "status", "meaning", "claim_status", "next_action", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_667_NONCLAIM_SUMMARY.csv",
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "ansatz_rows",
            "variation_rows",
            "FB5540_term_rows",
            "clause_rows",
            "fallback_rows",
            "evaluator_rows",
            "blocked_or_nonclaim_gates",
            "validation_failures",
            "next_target",
            "generated_utc",
        ],
    )
    write_csv(RESIDUALS / "P8_Y5_BRR545_667_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_document(source_rows, ansatz_rows, variation_rows, term_rows, clause_rows, fallback_rows, evaluator_data, gate_rows, decision, summary_rows, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"ansatz_rows={len(ansatz_rows)}")
    print(f"variation_rows={len(variation_rows)}")
    print(f"FB5540_term_rows={len(term_rows)}")
    print(f"clause_rows={len(clause_rows)}")
    print(f"fallback_rows={len(fallback_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
