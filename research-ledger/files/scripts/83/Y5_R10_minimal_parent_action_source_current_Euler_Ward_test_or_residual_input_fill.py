from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_minimal_parent_action_Euler_Ward_chain_conditional_PiM_Hamiltonian_identification_still_unsigned_first_residual_fill_selected_nonclaim"
CLAIM_CEILING = "minimal_parent_Euler_Ward_gate_only_no_Hilbert_worldtube_glue_no_source_normalized_Newton_no_PPN_no_R10_no_R11_no_local_GR_claim"
NEXT_TARGET = "664-Y5-R10-Hamiltonian-PiM-integrability-source-equality-or-first-residual-fill.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "663-Y5-R10-minimal-parent-action-source-current-Euler-Ward-test-or-residual-input-fill.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "662_doc": ROOT / "662-Y5-R10-Hilbert-worldtube-source-measure-glue-or-equality-residual-bound.md",
    "662_validation": RESIDUALS / "P8_Y5_BRR545_662_VALIDATION.csv",
    "662_proof_chain": RESIDUALS / "P8_Y5_R10_662_PROOF_CHAIN.csv",
    "662_parent_clause_audit": RESIDUALS / "P8_Y5_R10_662_PARENT_CLAUSE_AUDIT.csv",
    "662_residual_decomposition": RESIDUALS / "P8_Y5_R10_662_RESIDUAL_DECOMPOSITION.csv",
    "662_bound_template": RESIDUALS / "P8_Y5_R10_662_BOUND_INPUT_TEMPLATE.csv",
    "661_obstruction_audit": RESIDUALS / "P8_Y5_R10_661_EQUALITY_OBSTRUCTION_AUDIT.csv",
    "538_doc": ROOT / "538-Y5-minimal-parent-action-Euler-Ward-test-or-closure-demotion.md",
    "538_validation": RESIDUALS / "P8_Y5_EULER_WARD_VALIDATION.csv",
    "538_chain": RESIDUALS / "P8_Y5_EULER_WARD_CHAIN_TEST.csv",
    "538_decision": RESIDUALS / "P8_Y5_EULER_WARD_DECISION.csv",
    "539_doc": ROOT / "539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md",
    "539_branch": RESIDUALS / "P8_Y5_PIM_HAMILTONIAN_BRANCH_DEFINITION.csv",
    "539_gates": RESIDUALS / "P8_Y5_PIM_HAMILTONIAN_GATE_RESULTS.csv",
    "539_demotion": RESIDUALS / "P8_Y5_TOPOLOGICAL_PIM_DEMOTION_LEDGER.csv",
    "540_doc": ROOT / "540-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test.md",
    "540_source_measure": RESIDUALS / "P8_Y5_HAMILTONIAN_PIM_SOURCE_MEASURE_TEST.csv",
    "540_gauss_ppn": RESIDUALS / "P8_Y5_HAMILTONIAN_PIM_GAUSS_PPN_TEST.csv",
    "540_residual_activation": RESIDUALS / "P8_Y5_HAMILTONIAN_PIM_RESIDUAL_ACTIVATION.csv",
    "541_doc": ROOT / "541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md",
    "541_gate_update": RESIDUALS / "P8_Y5_SOURCE_MEASURE_HSM541_GATE_UPDATE.csv",
    "PAC537_contract": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
    "HWT536_attempt": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
    "PIF537_template": RESIDUALS / "P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv",
    "Noether_chain": RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
    "first_variation_gates": RESIDUALS / "P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv",
    "Hilbert_monopole": RESIDUALS / "P8_Hilbert_monopole_calibration_CONTRACT.csv",
    "PG_contract": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
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
        "662_doc": "fresh conditional worldtube glue theorem and R_glue residual target",
        "662_validation": "prior R10/Y5 checkpoint validation",
        "662_proof_chain": "parent variation through residual branch proof-chain rows",
        "662_parent_clause_audit": "unsigned parent clauses feeding Euler/Ward test",
        "662_residual_decomposition": "R_glue component split",
        "662_bound_template": "bound-input scaffold if Euler/Ward repair fails",
        "661_obstruction_audit": "prior equality obstruction audit including multiplier/topological wrong-object guard",
        "538_doc": "older minimal parent Euler/Ward test identifying DAT537_4 blocker",
        "538_validation": "older Euler/Ward validation",
        "538_chain": "machine Euler/Ward chain test rows",
        "538_decision": "older decision selecting PiM-as-Hamiltonian repair",
        "539_doc": "PiM as Hamiltonian charge-map candidate and topological demotion",
        "539_branch": "machine Hamiltonian PiM candidate rows",
        "539_gates": "machine Hamiltonian PiM gate rows",
        "539_demotion": "old topological PiM demotion ledger",
        "540_doc": "Hamiltonian PiM source-measure and PPN readout gate",
        "540_source_measure": "Hamiltonian PiM source-measure tests",
        "540_gauss_ppn": "Gauss/PPN readout tests",
        "540_residual_activation": "residual activation map after Hamiltonian PiM gate",
        "541_doc": "Hamiltonian PiM source-measure scorecard",
        "541_gate_update": "source-measure gate update",
        "PAC537_contract": "parent-action clauses required for HWT536",
        "HWT536_attempt": "Hilbert worldtube theorem attempt rows",
        "PIF537_template": "PiM residual input template",
        "Noether_chain": "parent Noether closure derivation chain",
        "first_variation_gates": "first-variation gates including Pi_M and local source current",
        "Hilbert_monopole": "Hilbert-to-measured-monopole calibration contract",
        "PG_contract": "Poisson/Gauss calibration contract",
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


def minimal_parent_action_test_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "candidate_id": "MP663_A_EH_observed_silent_parent",
            "candidate": "observed EH exterior plus minimally coupled matter plus topological/silent sectors plus explicit residual sector",
            "action_shape": "S = S_EH[g_obs;G_ref,Lambda] + S_matter[g_obs,psi] + S_top + S_silent + S_boundary + S_residual",
            "Euler_Ward_output": "covariant variation, Noether current, charge decomposition, Stokes equality through linked worldtube surfaces",
            "what_it_closes": "conditional Noether/Stokes chain through worldtube charge if source frame, tau, reference, and C-terms are fixed",
            "what_it_fails": "does not automatically identify current Pi_M/topological current with Hamiltonian source charge",
            "status": "conditional_pass_until_PiM_identification",
            "valid_for_claim": "false",
            "source_paths": source_list("538_chain", "Noether_chain", "662_proof_chain"),
            "generated_utc": now,
        },
        {
            "candidate_id": "MP663_B_Hamiltonian_PiM_charge_map",
            "candidate": "define Pi_M on the local branch as the Hamiltonian/covariant-phase-space source charge map",
            "action_shape": "Pi_M := Pi_M^H; Pi_M^H J_H := ell_H[J_H;tau,S] omega_M^H",
            "Euler_Ward_output": "DAT537_4 becomes a charge-map definition if integrability, fixed reference, and same-source frame are signed",
            "what_it_closes": "wrong-conserved-object risk at charge/integral level",
            "what_it_fails": "not adopted/proved for current MTS; old topological Pi_M equivalence, commutator silence, source-measure glue, and PPN readout remain open",
            "status": "best_repair_candidate_not_promotion",
            "valid_for_claim": "false",
            "source_paths": source_list("539_doc", "539_branch", "540_source_measure"),
            "generated_utc": now,
        },
        {
            "candidate_id": "MP663_C_topological_constraint_parent",
            "candidate": "add a parent topological constraint forcing Pi_M J_H to equal J_M_top plus zero-boundary exact terms",
            "action_shape": "S_constraint = int Lambda_eq wedge (Pi_M J_H - J_M_top - dB_zero)",
            "Euler_Ward_output": "formal equality if constraint is independently owned and stressless",
            "what_it_closes": "keeps old topological-current language only if origin is non-ad-hoc",
            "what_it_fails": "high closure-smuggling risk unless gauge/topological origin, zero stress, and boundary/reference compatibility are separately derived",
            "status": "closure_only_until_independent_origin",
            "valid_for_claim": "false",
            "source_paths": source_list("661_obstruction_audit", "662_parent_clause_audit", "538_chain"),
            "generated_utc": now,
        },
        {
            "candidate_id": "MP663_D_residual_input_branch",
            "candidate": "accept unsigned PiM/source-current identification and fill residual rows instead of claiming derivation",
            "action_shape": "R_glue and Delta_charge terms remain explicit source-backed inputs",
            "Euler_Ward_output": "no theorem closure; creates a testable residual branch",
            "what_it_closes": "prevents hidden calibration and lets R10/R11/local locks evaluate real coefficients later",
            "what_it_fails": "does not derive local GR or Newton; needs sourced rows",
            "status": "fallback_ready_first_fill_selected",
            "valid_for_claim": "false",
            "source_paths": source_list("662_bound_template", "PIF537_template", "540_residual_activation"),
            "generated_utc": now,
        },
    ]


def Euler_Ward_chain_result_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "chain_id": "EW663_0_parent_variation",
            "test_equation": "delta L = E_A delta Phi^A + dTheta(Phi,delta Phi)",
            "minimal_parent_result": "conditional_pass_if_explicit_parent_Lagrangian_is_written",
            "current_MTS_result": "contract_only_no_full_current_Lagrangian",
            "blocks_claim": "true",
            "next_requirement": "write explicit local parent action terms or keep R_action residual",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "chain_id": "EW663_1_Noether_current",
            "test_equation": "J_tau = Theta(Phi,L_tau Phi) - i_tau L",
            "minimal_parent_result": "conditional_pass_if_tau_and_source_frame_are_fixed_once",
            "current_MTS_result": "tau_source_readout_lock_still_open",
            "blocks_claim": "true",
            "next_requirement": "derive same observed source/readout time generator",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "chain_id": "EW663_2_source_current_ownership",
            "test_equation": "J_H[tau] = delta S_matter/delta e_obs contracted with tau",
            "minimal_parent_result": "conditional_pass_for_minimally_coupled_observed_matter",
            "current_MTS_result": "same_frame_measure_not_parent_signed",
            "blocks_claim": "true",
            "next_requirement": "prove source, clocks, rods, metric, and orbital readout share e_obs",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "chain_id": "EW663_3_charge_decomposition",
            "test_equation": "J_tau = dQ_tau + C_tau; C_tau=C_EH+C_extra+C_projector+C_boundary",
            "minimal_parent_result": "conditional_pass_for_EH_plus_silent_exterior",
            "current_MTS_result": "C_extra_C_projector_C_boundary_not_zeroed",
            "blocks_claim": "true",
            "next_requirement": "zero or source-bound C_extra, C_projector, and C_boundary",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "chain_id": "EW663_4_worldtube_Stokes_equality",
            "test_equation": "int_S2 Q_tau - int_S1 Q_tau = int_A C_tau + boundary_flux",
            "minimal_parent_result": "mathematical_pass_once_Q_tau_and_W_source_are_defined",
            "current_MTS_result": "conditional_only_worldtube_charge_not_owned",
            "blocks_claim": "true",
            "next_requirement": "fix W_source before readout and control boundary/reference flux",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "chain_id": "EW663_5_PiM_Hamiltonian_identification",
            "test_equation": "(4*pi*G_ref)^-1 int_S Pi_M J_H = int_S Q_tau",
            "minimal_parent_result": "fails_unless_PiM_is_Hamiltonian_charge_map_or_independently_constrained",
            "current_MTS_result": "not_derived_candidate_PiM_H_only",
            "blocks_claim": "true",
            "next_requirement": "derive/adopt Pi_M^H with integrability and source equality, or demote old Pi_M to residual",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "chain_id": "EW663_6_topological_PD_match",
            "test_equation": "Pi_M^top J_H - Pi_M^H J_H = R_Htop + dB_Htop",
            "minimal_parent_result": "optional_repair_only_if_R_Htop_and_boundary_flux_are_zero_or_bounded",
            "current_MTS_result": "old_topological_PiM_demoted_as_independent_proof",
            "blocks_claim": "true",
            "next_requirement": "prove old topological representative equals Hamiltonian charge map or carry R_Htop",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "chain_id": "EW663_7_local_readout_PPN",
            "test_equation": "g_00=-1+2G_ref M_source/r+O(r^-2); Delta_PPN={gamma-1,beta-1,alpha_i,zeta_i,xi}",
            "minimal_parent_result": "not_reached_until_source_charge_equality_closes",
            "current_MTS_result": "not_reached",
            "blocks_claim": "true",
            "next_requirement": "after PiM/source equality, derive Gauss/orbital and second-order PPN readout",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def PiM_repair_or_demotion_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "repair_id": "PR663_0_define_PiM_H",
            "proposal": "make Pi_M the parent Hamiltonian/covariant-phase-space mass charge map on the local branch",
            "mathematical_form": "Pi_M^H J_H := ell_H[J_H;tau,S] omega_M^H; ell_H=(4*pi*G_ref) int_S Q_tau",
            "benefit": "turns DAT537_4 from an equality miracle into a parent charge-map definition",
            "remaining_debt": "charge integrability, fixed reference, same source frame, radial C-term silence, and PPN readout",
            "status": "best_next_derivation_target",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "repair_id": "PR663_1_integrability_reference",
            "proposal": "prove Hamiltonian variation is integrable with fixed reference and boundary convention",
            "mathematical_form": "delta H_tau = int_S(delta Q_tau - i_tau Theta); H_ref fixed once",
            "benefit": "prevents source mass from shifting by reference bookkeeping",
            "remaining_debt": "Delta_symp and B_zero_flux remain if unsigned",
            "status": "not_derived",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "repair_id": "PR663_2_same_source_measure",
            "proposal": "prove worldtube source measure is the same observed Hilbert matter source used by Q_tau",
            "mathematical_form": "W_source=supp(J_H[e_obs]); M_source[W]=H_tau[S]-H_ref before orbital fitting",
            "benefit": "connects dressed parent charge to physical source, not just a surface symbol",
            "remaining_debt": "Delta_frame and Delta_cal remain if source/readout frames split",
            "status": "not_derived",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "repair_id": "PR663_3_demote_old_topological_PiM",
            "proposal": "old Pi_M^top earns no derivation credit unless it equals Pi_M^H up to exact zero-flux terms",
            "mathematical_form": "Pi_M^top J_H = Pi_M^H J_H + dB_Htop + R_Htop",
            "benefit": "kills the conserved-wrong-object loophole",
            "remaining_debt": "R_Htop and boundary flux need theorem-zero or source-backed bound",
            "status": "demoted_unless_equivalent",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "repair_id": "PR663_4_topological_constraint_warning",
            "proposal": "a constraint forcing Pi_M J_H = J_M_top is only a derivation if independently generated",
            "mathematical_form": "S_constraint=int Lambda_eq wedge(Pi_M J_H-J_M_top-dB_zero)",
            "benefit": "possible formal repair if the constraint has real gauge/topological ownership",
            "remaining_debt": "otherwise it is a dressed closure axiom",
            "status": "high_risk_closure_only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "repair_id": "PR663_5_residual_fill",
            "proposal": "if Hamiltonian PiM integrability/source equality does not close, fill first residual rows",
            "mathematical_form": "epsilon_PiM_total_abs = |Delta_symp|+|B_zero_flux|+|R_Htop|+|I_commutator|+|Delta_extra| normalized by M_ref",
            "benefit": "keeps the branch testable without pretending derivation",
            "remaining_debt": "needs source-backed coefficients or theorem-zero rows",
            "status": "fallback_ready",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def residual_input_priority_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "priority_id": "FI663_0_first_target_integrability_reference",
            "quantity": "Delta_symp;B_zero_flux;H_ref_shift",
            "why_first": "without integrability and fixed reference, Hamiltonian PiM is not a stable mass functional",
            "required_columns": "system_id;surface_pair;Delta_symp;B_zero_flux;H_ref_shift;M_ref;units;source_file;assumptions;valid_for_claim",
            "acceptance_rule": "fixed reference theorem or source-backed boundary/symplectic value with uncertainty",
            "current_status": "MISSING_THEOREM_OR_SOURCE_INPUT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "priority_id": "FI663_1_second_target_source_measure_frame",
            "quantity": "Delta_frame;Delta_cal;worldtube_domain_shift",
            "why_first": "source charge and orbital/source measure may otherwise live in different frames or domains",
            "required_columns": "system_id;source_frame;readout_frame;domain_rule;Delta_frame;Delta_cal;Delta_worldtube_domain;source_file;assumptions;valid_for_claim",
            "acceptance_rule": "same-frame/source-worldtube theorem or explicit residual below mapped locks",
            "current_status": "MISSING_THEOREM_OR_SOURCE_INPUT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "priority_id": "FI663_2_third_target_PiM_commutator_projector",
            "quantity": "I_commutator;T_PiM_munu;R_PiM",
            "why_first": "charge-map notation does not automatically silence projector variation or commutator hair",
            "required_columns": "system_id;operator_family;I_commutator;projector_stress_beta_equiv;R_PiM;source_file;assumptions;valid_for_claim",
            "acceptance_rule": "PiM chain-map theorem or source-backed local-bound stress map",
            "current_status": "MISSING_THEOREM_OR_SOURCE_INPUT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "priority_id": "FI663_3_fourth_target_topological_equivalence",
            "quantity": "R_Htop;dB_Htop_flux;R_eq",
            "why_first": "old topological PiM remains demoted unless it equals the Hamiltonian charge representative",
            "required_columns": "system_id;R_Htop;dB_Htop_flux;R_eq_integral;M_ref;source_file;assumptions;valid_for_claim",
            "acceptance_rule": "zero-boundary equality theorem or source-backed residual bound",
            "current_status": "MISSING_THEOREM_OR_SOURCE_INPUT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "priority_id": "FI663_4_fifth_target_extra_C_terms",
            "quantity": "C_extra;C_projector;C_boundary;Delta_extra_vector",
            "why_first": "Noether/Stokes closure depends on these annulus C-terms vanishing or being bounded",
            "required_columns": "system_id;channel;C_term_integral;Delta_charge;M_ref;local_lock;source_file;assumptions;valid_for_claim",
            "acceptance_rule": "field-specific silence theorem or channelwise residual below lock",
            "current_status": "MISSING_THEOREM_OR_SOURCE_INPUT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "priority_id": "FI663_5_later_target_readout_PPN",
            "quantity": "Delta_cal;alpha_lambda;delta_beta_source;gamma_minus_one;alpha_i;zeta_i;xi",
            "why_first": "PPN is not first; it only becomes meaningful after source-charge equality and Newton readout close",
            "required_columns": "system_id;Delta_cal;alpha_lambda;lambda_scale;delta_beta_source;gamma_minus_one;alpha_i_vector;source_file;assumptions;valid_for_claim",
            "acceptance_rule": "Gauss/orbital theorem then second-order PPN envelope against official locks",
            "current_status": "NOT_REACHED_UNTIL_SOURCE_EQUALITY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def scoreability_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "G663_0_Euler_Ward_chain_tested",
            "gate": "minimal parent action Euler/Ward chain is retested",
            "result": "pass",
            "detail": "chain rows cover variation, Noether current, source ownership, charge decomposition, Stokes, PiM identification, topological match, and readout",
            "claim_effect": "no promotion",
            "generated_utc": now,
        },
        {
            "gate_id": "G663_1_Noether_Stokes_conditional",
            "gate": "Noether/Stokes route is structurally available",
            "result": "pass_conditional",
            "detail": "GR-style route is real once Q_tau, W_source, tau, reference, and C-terms are owned",
            "claim_effect": "the route lives but remains conditional",
            "generated_utc": now,
        },
        {
            "gate_id": "G663_2_PiM_identification_blocks",
            "gate": "current PiM/topological current is not derived as the Hamiltonian source charge",
            "result": "blocked_as_expected",
            "detail": "EW663_5 remains the hard blocker; PiM^H is a candidate, not a signed parent output",
            "claim_effect": "blocks Hilbert worldtube glue, source-normalized Newton, and local GR",
            "generated_utc": now,
        },
        {
            "gate_id": "G663_3_topological_PiM_demoted",
            "gate": "old topological PiM is demoted unless equivalent to Hamiltonian PiM",
            "result": "pass",
            "detail": "no conserved-wrong-object credit is allowed",
            "claim_effect": "prevents topology-as-mass overclaim",
            "generated_utc": now,
        },
        {
            "gate_id": "G663_4_residual_fill_selected",
            "gate": "first residual fill target is selected if proof stalls",
            "result": "pass_nonclaim",
            "detail": "integrability/reference rows are first because they decide whether PiM^H is a stable charge functional",
            "claim_effect": "scoreability scaffold only",
            "generated_utc": now,
        },
        {
            "gate_id": "G663_5_inputs_unfilled",
            "gate": "all residual inputs remain unfilled and nonclaim",
            "result": "pass_nonclaim",
            "detail": "FI663 rows require theorem-zero or source-backed inputs before any R10/R11/local use",
            "claim_effect": "no R10/R11/local pass",
            "generated_utc": now,
        },
        {
            "gate_id": "G663_6_PPN_not_reached",
            "gate": "PPN/readout remains downstream",
            "result": "pass",
            "detail": "PPN is not evaluated until source-charge equality and Newton readout close",
            "claim_effect": "blocks local GR overclaim",
            "generated_utc": now,
        },
        {
            "gate_id": "G663_7_claim_guard",
            "gate": "no R10, R11, PPN, Newton, or local-GR claim",
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
            "decision_id": "D663_0_Euler_Ward_route",
            "status": "conditional_Noether_Stokes_chain_survives",
            "meaning": "a minimal GR-style parent can carry the standard Euler/Ward/Noether/Stokes machinery through the worldtube step",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
        {
            "decision_id": "D663_1_hard_blocker",
            "status": "PiM_Hamiltonian_identification_unsigned",
            "meaning": "current MTS still has not derived/adopted PiM as the Hamiltonian charge map with integrability, fixed reference, and same source frame",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
        {
            "decision_id": "D663_2_topological_route",
            "status": "old_topological_PiM_demoted",
            "meaning": "old topological PiM cannot be used as an independent proof of source mass unless equivalent to PiM^H",
            "claim_status": "false",
            "next_action": "prove PiM^top = PiM^H + zero-boundary exact term or keep R_Htop",
            "generated_utc": now,
        },
        {
            "decision_id": "D663_3_first_fill",
            "status": "integrability_reference_first",
            "meaning": "if the derivation stalls, fill Delta_symp/B_zero/H_ref rows before PPN or cosmology-linked claims",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
        {
            "decision_id": "D663_4_local_GR",
            "status": "blocked",
            "meaning": "local GR remains blocked by source-charge equality, residual inputs, Gauss/orbital readout, and PPN followthrough",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows(
    parent_rows: list[dict[str, str]],
    chain_rows: list[dict[str, str]],
    repair_rows: list[dict[str, str]],
    fill_rows: list[dict[str, str]],
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
            "minimal_parent_rows": str(len(parent_rows)),
            "Euler_Ward_chain_rows": str(len(chain_rows)),
            "PiM_repair_rows": str(len(repair_rows)),
            "residual_fill_rows": str(len(fill_rows)),
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
    parent_rows: list[dict[str, str]],
    chain_rows: list[dict[str, str]],
    repair_rows: list[dict[str, str]],
    fill_rows: list[dict[str, str]],
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
    add("V663_0_sources_exist", not missing_sources, "missing=" + ";".join(missing_sources))

    validation_662 = read_csv(SOURCE_PATHS["662_validation"])
    prior_662_failures = [row.get("check_id", "?") for row in validation_662 if row.get("result") != "pass"]
    add("V663_1_prior_662_validation_clean", not prior_662_failures, "prior_662_failures=" + ";".join(prior_662_failures))

    validation_538 = read_csv(SOURCE_PATHS["538_validation"])
    prior_538_failures = [row.get("check_id", "?") for row in validation_538 if row.get("result") != "pass"]
    add("V663_2_prior_538_validation_clean", not prior_538_failures, "prior_538_failures=" + ";".join(prior_538_failures))

    all_valid_flags = [
        row.get("valid_for_claim")
        for row_group in (parent_rows, chain_rows, repair_rows, fill_rows)
        for row in row_group
    ]
    add("V663_3_no_claim_rows", all(flag == "false" for flag in all_valid_flags), "valid_for_claim_flags=" + ";".join(sorted(set(all_valid_flags))))

    candidate_ids = {row["candidate_id"] for row in parent_rows}
    required_candidates = {"MP663_A_EH_observed_silent_parent", "MP663_B_Hamiltonian_PiM_charge_map", "MP663_C_topological_constraint_parent", "MP663_D_residual_input_branch"}
    add("V663_4_minimal_parent_candidates_complete", required_candidates.issubset(candidate_ids), "candidate_ids=" + ";".join(sorted(candidate_ids)))

    chain_ids = {row["chain_id"] for row in chain_rows}
    required_chain = {"EW663_0_parent_variation", "EW663_1_Noether_current", "EW663_2_source_current_ownership", "EW663_3_charge_decomposition", "EW663_4_worldtube_Stokes_equality", "EW663_5_PiM_Hamiltonian_identification", "EW663_6_topological_PD_match", "EW663_7_local_readout_PPN"}
    add("V663_5_Euler_Ward_chain_coverage", required_chain.issubset(chain_ids), "chain_ids=" + ";".join(sorted(chain_ids)))

    hard_block = [
        row
        for row in chain_rows
        if row["chain_id"] == "EW663_5_PiM_Hamiltonian_identification" and row["blocks_claim"] == "true"
    ]
    add("V663_6_PiM_identification_blocks_claim", len(hard_block) == 1, "hard_block_rows=" + str(len(hard_block)))

    repair_ids = {row["repair_id"] for row in repair_rows}
    required_repairs = {"PR663_0_define_PiM_H", "PR663_3_demote_old_topological_PiM", "PR663_5_residual_fill"}
    add("V663_7_repair_and_demotion_coverage", required_repairs.issubset(repair_ids), "repair_ids=" + ";".join(sorted(repair_ids)))

    first_fill = [
        row
        for row in fill_rows
        if row["priority_id"] == "FI663_0_first_target_integrability_reference"
        and row["current_status"] == "MISSING_THEOREM_OR_SOURCE_INPUT"
    ]
    add("V663_8_first_residual_fill_selected", len(first_fill) == 1, "first_fill_rows=" + str(len(first_fill)))

    unfilled = [row["priority_id"] for row in fill_rows if row["current_status"] in {"MISSING_THEOREM_OR_SOURCE_INPUT", "NOT_REACHED_UNTIL_SOURCE_EQUALITY"}]
    add("V663_9_residual_inputs_unfilled_nonclaim", len(unfilled) == len(fill_rows), "fill_rows=" + str(len(fill_rows)))

    blocked_gate = [
        row
        for row in gate_rows
        if row["gate_id"] == "G663_2_PiM_identification_blocks" and row["result"] == "blocked_as_expected"
    ]
    add("V663_10_gate_blocks_claim", len(blocked_gate) == 1, "blocked_gate_rows=" + str(len(blocked_gate)))

    next_target_rows = [row for row in decision if row["next_action"] == NEXT_TARGET]
    add("V663_11_next_target_selected", bool(next_target_rows), NEXT_TARGET)

    changed = formalization_changed_after_cutoff()
    add("V663_12_formalization_workbench_untouched", changed == 0, "formalization_changed_after_cutoff=" + str(changed))

    add("V663_13_status_nonclaim", "no_Hilbert_worldtube_glue" in CLAIM_CEILING and STATUS.endswith("nonclaim"), STATUS)

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
    parent_rows: list[dict[str, str]],
    chain_rows: list[dict[str, str]],
    repair_rows: list[dict[str, str]],
    fill_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    doc = f"""# 663 - Y5 R10 Minimal Parent Action Source-Current Euler-Ward Test Or Residual Input Fill

## Verdict

The Euler/Ward route survives as real mathematics, but it still does not close current MTS. A minimal GR-style parent can supply variation, Noether current, charge decomposition, and Stokes equality. The hard blocker is still the same precise identity:

```text
(4*pi*G_ref)^-1 int_S Pi_M J_H = int_S Q_tau.
```

The clean repair is to make `Pi_M` the parent Hamiltonian charge map `Pi_M^H`, not an independent topological/readout selector. But that repair is not claim-valid until charge integrability, fixed reference, same-frame source measure, old-topological equivalence/demotion, C-term silence, and readout gates are signed.

If the derivation stalls, the first residual fill target is:

```text
Delta_symp, B_zero_flux, H_ref_shift.
```

Those come before PPN because without a stable Hamiltonian charge functional there is no honest source mass to expand to PPN order.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "role"])}

## Minimal Parent Action Test

{markdown_table(parent_rows, ["candidate_id", "candidate", "action_shape", "status", "what_it_fails", "valid_for_claim"])}

## Euler Ward Chain Result

{markdown_table(chain_rows, ["chain_id", "test_equation", "minimal_parent_result", "current_MTS_result", "blocks_claim", "next_requirement", "valid_for_claim"])}

## PiM Repair Or Demotion

{markdown_table(repair_rows, ["repair_id", "proposal", "mathematical_form", "benefit", "remaining_debt", "status", "valid_for_claim"])}

## Residual Input Priority

{markdown_table(fill_rows, ["priority_id", "quantity", "why_first", "required_columns", "current_status", "valid_for_claim"])}

## Scoreability Gates

{markdown_table(gate_rows, ["gate_id", "gate", "result", "detail", "claim_effect"])}

## Decision

{markdown_table(decision, ["decision_id", "status", "meaning", "claim_status", "next_action"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "minimal_parent_rows", "Euler_Ward_chain_rows", "PiM_repair_rows", "residual_fill_rows", "blocked_or_nonclaim_scoreability_gates", "validation_failures", "next_target"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Interpretation

This is the useful kind of no. The action route is not fantasy; it gets us to the exact charge-map boss door. But `Pi_M` cannot be both a free selector and a derived Hamiltonian mass charge. Either it becomes `Pi_M^H` with integrability/source-equality proof, or the old topological route becomes a residual branch.

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    parent_rows = minimal_parent_action_test_rows()
    chain_rows = Euler_Ward_chain_result_rows()
    repair_rows = PiM_repair_or_demotion_rows()
    fill_rows = residual_input_priority_rows()
    gate_rows = scoreability_gate_rows()
    decision = decision_rows()
    validation = validation_rows(source_rows, parent_rows, chain_rows, repair_rows, fill_rows, gate_rows, decision)
    summary_rows = nonclaim_summary_rows(parent_rows, chain_rows, repair_rows, fill_rows, gate_rows, validation)

    write_csv(
        RESIDUALS / "P8_Y5_R10_663_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "source_path", "exists", "role", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_663_MINIMAL_PARENT_ACTION_TEST.csv",
        parent_rows,
        ["candidate_id", "candidate", "action_shape", "Euler_Ward_output", "what_it_closes", "what_it_fails", "status", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_663_EULER_WARD_CHAIN_RESULT.csv",
        chain_rows,
        ["chain_id", "test_equation", "minimal_parent_result", "current_MTS_result", "blocks_claim", "next_requirement", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_663_PIM_REPAIR_OR_DEMOTION.csv",
        repair_rows,
        ["repair_id", "proposal", "mathematical_form", "benefit", "remaining_debt", "status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_663_RESIDUAL_INPUT_PRIORITY.csv",
        fill_rows,
        ["priority_id", "quantity", "why_first", "required_columns", "acceptance_rule", "current_status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_663_SCOREABILITY_GATES.csv",
        gate_rows,
        ["gate_id", "gate", "result", "detail", "claim_effect", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_663_DECISION.csv",
        decision,
        ["decision_id", "status", "meaning", "claim_status", "next_action", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_663_NONCLAIM_SUMMARY.csv",
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "minimal_parent_rows",
            "Euler_Ward_chain_rows",
            "PiM_repair_rows",
            "residual_fill_rows",
            "blocked_or_nonclaim_scoreability_gates",
            "validation_failures",
            "next_target",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_BRR545_663_VALIDATION.csv",
        validation,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_document(source_rows, parent_rows, chain_rows, repair_rows, fill_rows, gate_rows, decision, summary_rows, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"minimal_parent_rows={len(parent_rows)}")
    print(f"Euler_Ward_chain_rows={len(chain_rows)}")
    print(f"PiM_repair_rows={len(repair_rows)}")
    print(f"residual_fill_rows={len(fill_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
