from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "source-owner-current-parent-action-contract"
CHECKPOINT_DOC = "446-source-owner-current-parent-action-contract.md"
STATUS = "source_owner_current_parent_action_contract_written_exact_terms_needed_K_owner_not_parent_derived_q_retained_not_zero_no_measured_GM_Newton_or_local_GR_pass"
CLAIM_CEILING = "source_owner_parent_action_contract_only_no_K_owner_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "447-no-species-source-charge-one-coframe-theorem-attempt.md"
ACTION_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv")
ZERO_CONDITIONS_PATH = Path("source-intake/mts_residuals/P8_q_retained_zero_conditions_CONTRACT.csv")


ACTION_CONTRACT_COLUMNS = [
    "term_id",
    "parent_block",
    "required_action_structure",
    "variation_target",
    "euler_identity_required",
    "produces_or_kills",
    "affected_contracts",
    "affected_rows",
    "current_status",
    "fallback_if_missing",
]


ZERO_CONDITION_COLUMNS = [
    "condition_id",
    "channel",
    "zero_route",
    "required_parent_evidence",
    "forbidden_shortcut",
    "affected_components",
    "affected_rows",
    "current_status",
    "fallback_if_missing",
]


SOURCE_DOCS = [
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "minimal parent action blocks and required Ward/source variation identities",
    },
    {
        "path": "402-EH-source-normalization-parent-pair.md",
        "role": "EH/source weak-field chain and measured-GM obstruction",
    },
    {
        "path": "403-boundary-domain-flux-nohair-numeric-contract.md",
        "role": "boundary/domain/flux no-hair numeric locks",
    },
    {
        "path": "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
        "role": "source-normalization test plan and no symbolic pass policy",
    },
    {
        "path": "436-auxiliary-projector-local-Euler-equation-ledger.md",
        "role": "hidden-variable Euler ledger including A7 mass-flux projector",
    },
    {
        "path": "444-source-normalization-residual-vector-refinement.md",
        "role": "P8 source residual components",
    },
    {
        "path": "445-measured-GM-Ward-source-ownership-theorem-attempt.md",
        "role": "conditional Ward source-ownership theorem and owner contract",
    },
    {
        "path": "runs/20260602-044500-boundary-domain-flux-nohair-numeric-contract/results/family_rollup.csv",
        "role": "flux/source/drift family lock rollup",
    },
    {
        "path": "runs/20260602-073500-boundary-exchange-coefficient-retained-evaluator/results/retained_coefficients.csv",
        "role": "retained boundary/exchange coefficient map",
    },
    {
        "path": "runs/20260602-123000-auxiliary-projector-local-Euler-equation-ledger/results/Euler_ledger_rows.csv",
        "role": "Euler ledger row A7 and hidden-variable zero conditions",
    },
    {
        "path": "runs/20260602-143000-source-normalization-residual-vector-refinement/results/P8_source_residual_template_rows.csv",
        "role": "P8 residual rows activated if source ownership fails",
    },
    {
        "path": "runs/20260602-144500-measured-GM-Ward-source-ownership-theorem-attempt/results/owner_identity_contract.csv",
        "role": "C0-C7 Ward source-owner identity contract",
    },
    {
        "path": "runs/20260602-144500-measured-GM-Ward-source-ownership-theorem-attempt/results/residual_current_ledger.csv",
        "role": "residual source/exchange current ledger",
    },
    {
        "path": "source-intake/mts_residuals/P8_Ward_source_owner_identity_CONTRACT.csv",
        "role": "checkpoint 445 source-owner contract",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv",
        "role": "P8 residual vector fallback",
    },
    {
        "path": "source-intake/mts_residuals/R11_P8_source_normalization_rows_TEMPLATE.csv",
        "role": "P8 R11 source-normalization fallback",
    },
]


PARENT_ACTION_PROBLEM = [
    {
        "item": "target",
        "statement": "write the exact parent-action structures that would make K_owner and q_retained=0 derivable rather than assumed",
        "mathematical_form": "S_parent must vary to q_res^nu=nabla_mu K_owner^{mu nu} and q_retained^nu=0 or retained mapped",
        "current_status": "contract_needed_not_solution",
    },
    {
        "item": "non_cheat_rule",
        "statement": "a multiplier that simply sets every dangerous residual to zero is not a derivation unless the constraint is fixed by parent symmetry, topology, gauge, or an already-defined physical conservation law",
        "mathematical_form": "lambda_nu q_retained^nu is closure-only unless q_retained=0 is a parent configuration constraint",
        "current_status": "enforced_by_this_checkpoint",
    },
    {
        "item": "legal_success",
        "statement": "every exchange/source channel is either absent, gauge/topological, exact-owned with zero boundary flux, positive source-free no-haired, or explicitly retained as residual data",
        "mathematical_form": "q_res^nu=nabla_mu K_owner^{mu nu}; int_boundary K_owner=0; q_retained^nu=0 or vector_row",
        "current_status": "not_parent_derived",
    },
    {
        "item": "legal_failure",
        "statement": "if any action block lacks the variation identity, the linked P8 residual row remains active",
        "mathematical_form": "P8_source_owner_parent_action_terms_CONTRACT.csv plus P8_q_retained_zero_conditions_CONTRACT.csv",
        "current_status": "contracts_written_by_this_checkpoint",
    },
]


PARENT_ACTION_BLOCKS = [
    {
        "term_id": "A0_total_covariant_parent",
        "parent_block": "S_core + S_matter + S_source_norm + S_X + S_projector + S_boundary + S_domain + S_memory",
        "required_action_structure": "single diffeomorphic parent action; all local fields varied before readout/scoring",
        "variation_target": "g/e and every Z_I",
        "euler_identity_required": "nabla_mu T_tot^{mu nu}=0 on shell with no unvaried hidden force channel",
        "produces_or_kills": "legal basis for Ward accounting, not separate measured-GM conservation",
        "affected_contracts": "C0_on_shell_total_Ward",
        "affected_rows": "R0-R11",
        "current_status": "structural_available_not_sufficient",
        "fallback_if_missing": "reject branch or retain all affected residual rows",
    },
    {
        "term_id": "A1_source_owner_decomposition",
        "parent_block": "S_owner_current",
        "required_action_structure": "parent-derived Noether/source current decomposition, not a fitted readout split",
        "variation_target": "K_owner^{mu nu}, q_res^nu, q_retained^nu, or equivalent current variables",
        "euler_identity_required": "q_res^nu = nabla_mu K_owner^{mu nu} + q_retained^nu",
        "produces_or_kills": "defines the exact owner current and exposes retained leakage",
        "affected_contracts": "C1_exact_owner_decomposition",
        "affected_rows": "R4;R7;R9;R11",
        "current_status": "not_parent_derived",
        "fallback_if_missing": "P8_boundary_bulk_domain_mu_extra and R11 source rows remain active",
    },
    {
        "term_id": "A2_no_retained_source_constraint",
        "parent_block": "S_owner_current or parent configuration space",
        "required_action_structure": "q_retained is absent by symmetry/topology/gauge, or has a source-free positive operator forcing zero",
        "variation_target": "q_retained^nu",
        "euler_identity_required": "q_retained^nu=0 from legal zero route, not by ad hoc multiplier",
        "produces_or_kills": "kills unowned residual source current",
        "affected_contracts": "C1_exact_owner_decomposition;C2_zero_owner_flux",
        "affected_rows": "R4;R7;R9;R11",
        "current_status": "not_parent_derived",
        "fallback_if_missing": "retain q_retained vector with alpha3/Gdot/source locks",
    },
    {
        "term_id": "A3_boundary_class_topological",
        "parent_block": "S_boundary[g/e|partialD, class data]",
        "required_action_structure": "class-only/topological boundary action with no B_TF, B_0i, radial hair, or local flux",
        "variation_target": "boundary variables and induced boundary data",
        "euler_identity_required": "int_partialSigma n_i K_owner^{i0} dS=0 and no shear/vector/radial boundary source",
        "produces_or_kills": "kills boundary contribution to mu_extra and alpha3/Gdot leakage",
        "affected_contracts": "C2_zero_owner_flux;C6_no_range_or_radial_source_hair",
        "affected_rows": "R3;R4;R7;R8;R9;R11",
        "current_status": "conditional_noangular_radial_flux_open",
        "fallback_if_missing": "boundary/exchange coefficient vector",
    },
    {
        "term_id": "A4_mass_flux_projector",
        "parent_block": "S_source_norm[kappa,G_eff,M_eff,Pi_M J]",
        "required_action_structure": "closed calibrated mass-flux projector, defined before fitting/readout",
        "variation_target": "Pi_M J, M_eff, source-normalization multipliers",
        "euler_identity_required": "d(Pi_M J)=0 and M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J",
        "produces_or_kills": "gives the measured source monopole and kills M_eff drift/radial leakage",
        "affected_contracts": "C3_closed_calibrated_mass_current",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_status": "conditional_flux_calibration_open",
        "fallback_if_missing": "P8_Meff_conservation and P8_radial_source_hair remain active",
    },
    {
        "term_id": "A5_constant_universal_coupling",
        "parent_block": "S_source_norm[kappa,G_eff]",
        "required_action_structure": "G_eff/kappa_eff is a global constant, parent-selected coupling or derived constant local branch",
        "variation_target": "G_eff, kappa_eff, calibration standards",
        "euler_identity_required": "partial_t G_eff=partial_r G_eff=partial_A G_eff=0",
        "produces_or_kills": "kills Gdot and species/radial coupling drift",
        "affected_contracts": "C4_constant_universal_coupling",
        "affected_rows": "R1;R2;R9;R11",
        "current_status": "not_parent_derived",
        "fallback_if_missing": "Gdot/source/clock residual rows",
    },
    {
        "term_id": "A6_selector_blind_source_action",
        "parent_block": "S_matter + S_source_norm",
        "required_action_structure": "no material marker, species spurion, readout mask, torsion/projective source charge, or class label in active gravitational source",
        "variation_target": "species/source labels and matter-source couplings",
        "euler_identity_required": "partial_A mu_obs=0",
        "produces_or_kills": "kills source-charge WEP component",
        "affected_contracts": "C5_no_species_or_marker_source_charge",
        "affected_rows": "R1;R11",
        "current_status": "not_parent_derived",
        "fallback_if_missing": "P8_species_source_charge",
    },
    {
        "term_id": "A7_bulk_X_nohair_or_curve",
        "parent_block": "S_X[g/e, X, P, J_eff]",
        "required_action_structure": "bulk/memory/load fields are source-free positive no-hair in compact exterior, or become executable alpha_X(lambda_X)",
        "variation_target": "X_A",
        "euler_identity_required": "(-Delta + m_X^2)X=0 with m_X^2>0 and regular boundary, or mapped sourced force law",
        "produces_or_kills": "kills or maps finite-range/source hair",
        "affected_contracts": "C6_no_range_or_radial_source_hair",
        "affected_rows": "R1;R3;R4;R9;R10;R11",
        "current_status": "operator_and_sources_not_parent_derived",
        "fallback_if_missing": "R10 alpha(lambda) curve and P8 range/radial rows",
    },
    {
        "term_id": "A8_projector_domain_topological",
        "parent_block": "S_projector + S_domain",
        "required_action_structure": "projector/domain selectors are covariant, first-class/topological, or metric-independent with no local stress/flux",
        "variation_target": "P_D, lambda_P, chi_D, n_mu, L_cg",
        "euler_identity_required": "F_P^nu+F_domain^nu=0 or exact-owned zero-flux divergence",
        "produces_or_kills": "kills domain/projector contribution to mu_extra and preferred-frame leakage",
        "affected_contracts": "C1_exact_owner_decomposition;C2_zero_owner_flux",
        "affected_rows": "R5;R6;R7;R8;R9;R10;R11",
        "current_status": "retained_symbolic",
        "fallback_if_missing": "projector/domain stress residual vector",
    },
    {
        "term_id": "A9_memory_kernel_local_silence",
        "parent_block": "S_memory or nonlocal kernel sector",
        "required_action_structure": "compact-local memory kernel is silent, screened, or constant universal calibration",
        "variation_target": "memory kernel/history variables",
        "euler_identity_required": "partial_t mu_obs from memory = 0 and no local alpha3/R10 leakage",
        "produces_or_kills": "kills memory Gdot/source drift",
        "affected_contracts": "C4_constant_universal_coupling;C6_no_range_or_radial_source_hair",
        "affected_rows": "R7;R9;R10;R11",
        "current_status": "retained",
        "fallback_if_missing": "Gdot/alpha3/R10 memory residual map",
    },
    {
        "term_id": "A10_second_order_source_closure",
        "parent_block": "weak-field solution of S_parent through PPN order",
        "required_action_structure": "same source-normalization identities survive the second-order weak-field expansion",
        "variation_target": "second-order metric/source perturbations",
        "euler_identity_required": "delta_beta_source=0 after measured-GM normalization",
        "produces_or_kills": "kills beta/source nonlinear residue",
        "affected_contracts": "C7_second_order_source_closure",
        "affected_rows": "R4;R11",
        "current_status": "not_derived",
        "fallback_if_missing": "P8_nonlinear_beta_source_residue",
    },
]


VARIATION_IDENTITY_REQUIREMENTS = [
    {
        "variation_id": "V0_metric_diffeomorphism",
        "vary": "g/e plus all dynamical sectors",
        "identity": "nabla_mu T_tot^{mu nu}=0 on shell",
        "must_show": "no unvaried readout/mask/projector/source variable is contributing a hidden force",
        "status": "structural_available_not_sufficient",
    },
    {
        "variation_id": "V1_owner_current",
        "vary": "owner current variables or derive Noether current from existing sectors",
        "identity": "q_res^nu=nabla_mu K_owner^{mu nu}+q_retained^nu",
        "must_show": "K_owner is formula-level, covariant, and not chosen after the residual is known",
        "status": "not_parent_derived",
    },
    {
        "variation_id": "V2_retained_current_zero",
        "vary": "q_retained or its underlying sector",
        "identity": "q_retained^nu=0",
        "must_show": "zero follows by absence, gauge/topological identity, first-class constraint, or positive source-free no-hair",
        "status": "not_parent_derived",
    },
    {
        "variation_id": "V3_boundary_flux",
        "vary": "boundary class variables",
        "identity": "int_partialSigma n_i K_owner^{i0} dS=0",
        "must_show": "no B_TF, B_0i, radial hair, or exchange flux survives",
        "status": "conditional_noangular_radial_flux_open",
    },
    {
        "variation_id": "V4_mass_flux_projector",
        "vary": "Pi_M J and M_eff",
        "identity": "d(Pi_M J)=0 and calibrated M_eff integral",
        "must_show": "absolute calibration and no radial/time/species leakage",
        "status": "conditional_flux_calibration_open",
    },
    {
        "variation_id": "V5_coupling_constant",
        "vary": "G_eff/kappa_eff or prove they are global constants not fields",
        "identity": "partial_t G_eff=partial_r G_eff=partial_A G_eff=0",
        "must_show": "not a local field absorbing residual physics",
        "status": "not_parent_derived",
    },
    {
        "variation_id": "V6_species_blindness",
        "vary": "matter/source species labels or prove absent",
        "identity": "partial_A mu_obs=0",
        "must_show": "no material marker or source charge enters active gravitational source",
        "status": "not_parent_derived",
    },
    {
        "variation_id": "V7_range_radial_nohair",
        "vary": "bulk/range/radial source sectors",
        "identity": "partial_r mu_obs=partial_lambda mu_obs=0",
        "must_show": "finite-range field is zero/screened or executable as alpha(lambda)",
        "status": "not_derived_symbolic",
    },
    {
        "variation_id": "V8_second_order_source",
        "vary": "second-order source and metric perturbations",
        "identity": "delta_beta_source=0",
        "must_show": "first-order source normalization is stable at PPN beta order",
        "status": "not_derived",
    },
]


Q_RETAINED_ZERO_CONDITIONS = [
    {
        "condition_id": "Q0_absent_by_configuration",
        "channel": "any residual current",
        "zero_route": "the parent configuration space never contains the residual source channel",
        "required_parent_evidence": "field/source variable absent before variation and not recreated by readout",
        "forbidden_shortcut": "dropping a field after writing it in S_parent",
        "affected_components": "all_P8_components",
        "affected_rows": "R0-R11",
        "current_status": "not_shown_for_all_channels",
        "fallback_if_missing": "retain channel-specific residual row",
    },
    {
        "condition_id": "Q1_gauge_or_topological",
        "channel": "projector/domain/boundary owner current",
        "zero_route": "first-class gauge or topological identity removes local stress/flux",
        "required_parent_evidence": "constraint algebra or topological invariant with zero local variation",
        "forbidden_shortcut": "calling a chosen domain/projector covariant without varying it",
        "affected_components": "P8_boundary_bulk_domain_mu_extra",
        "affected_rows": "R5;R6;R7;R8;R9;R11",
        "current_status": "conditional_open",
        "fallback_if_missing": "projector/domain/boundary residual vector",
    },
    {
        "condition_id": "Q2_exact_owned_zero_flux",
        "channel": "boundary/source exchange",
        "zero_route": "residual is exact divergence and compact-boundary flux vanishes",
        "required_parent_evidence": "K_owner formula plus boundary no-flux theorem",
        "forbidden_shortcut": "using Bianchi to erase a nonzero surface integral",
        "affected_components": "P8_boundary_bulk_domain_mu_extra;P8_radial_source_hair",
        "affected_rows": "R3;R4;R7;R8;R9;R11",
        "current_status": "fail_open",
        "fallback_if_missing": "boundary/exchange coefficient vector",
    },
    {
        "condition_id": "Q3_positive_source_free_nohair",
        "channel": "bulk_X or auxiliary load",
        "zero_route": "positive elliptic/massive source-free equation with regular decay gives zero exterior field",
        "required_parent_evidence": "operator sign, source-free exterior, boundary regularity, and no source charge",
        "forbidden_shortcut": "mass gap without proving q_X=0",
        "affected_components": "P8_range_dependence;P8_radial_source_hair",
        "affected_rows": "R1;R3;R4;R9;R10;R11",
        "current_status": "operator_and_sources_not_parent_derived",
        "fallback_if_missing": "R10 curve and P8 source residual rows",
    },
    {
        "condition_id": "Q4_constant_universal_calibration",
        "channel": "constant source monopole",
        "zero_route": "only a constant universal monopole is absorbed into measured GM",
        "required_parent_evidence": "partial_{t,r,A,lambda} mu_obs=0 and mu_extra constant/universal",
        "forbidden_shortcut": "absorbing time/species/range/radial dependence into GM",
        "affected_components": "P8_Geff_time_drift;P8_species_source_charge;P8_range_dependence;P8_radial_source_hair",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_status": "not_parent_derived",
        "fallback_if_missing": "P8 residual vector",
    },
    {
        "condition_id": "Q5_executable_retained_vector",
        "channel": "any nonzero q_retained",
        "zero_route": "not a zero route; nonzero channel is retained and scored",
        "required_parent_evidence": "coefficient/residual value, units, normalization, source path, and weak-field map",
        "forbidden_shortcut": "symbolic residual counted as pass",
        "affected_components": "all_nonzero_P8_components",
        "affected_rows": "R1;R3;R4;R7;R8;R9;R10;R11",
        "current_status": "template_only",
        "fallback_if_missing": "no measured-GM/Newton/local-GR claim",
    },
]


NO_CHEAT_ACTION_TESTS = [
    {
        "test_id": "N0_no_ad_hoc_multiplier_zero",
        "bad_move": "add lambda_nu q_retained^nu only to force the desired result",
        "legal_if": "q_retained=0 is a parent symmetry/topological/gauge/configuration constraint already required independently",
        "current_result": "not_satisfied",
    },
    {
        "test_id": "N1_no_readout_after_variation_backreaction",
        "bad_move": "use P_read/P_active or fitted masks inside S_parent to cancel source residuals",
        "legal_if": "readout variables enter only after variation and cannot backreact",
        "current_result": "conditional_no_cheat_contract",
    },
    {
        "test_id": "N2_no_Bianchi_monopole_shortcut",
        "bad_move": "claim total conservation makes the measured matter/source monopole constant",
        "legal_if": "observed source current is separately conserved or exchange is exact-owned with zero flux",
        "current_result": "blocked_by_445",
    },
    {
        "test_id": "N3_no_constant_GM_absorbing_physics",
        "bad_move": "absorb radial/time/species/range source effects into measured GM",
        "legal_if": "all derivatives partial_{t,r,A,lambda} mu_obs are theorem-zero",
        "current_result": "not_satisfied",
    },
    {
        "test_id": "N4_no_mass_gap_without_no_charge",
        "bad_move": "use a massive auxiliary as no fifth force while retaining source charge",
        "legal_if": "source charge is zero/screened or alpha(lambda) curve is supplied",
        "current_result": "not_satisfied",
    },
    {
        "test_id": "N5_no_boundary_class_name_only",
        "bad_move": "call boundary data class-only while retaining radial/shear/vector/flux hair",
        "legal_if": "boundary variation proves no local flux, no B_TF, no B_0i, no radial hair",
        "current_result": "not_satisfied",
    },
]


RESIDUAL_ACTIVATION_MAP = [
    {
        "failed_action_term": "A1_source_owner_decomposition",
        "activated_component": "P8_boundary_bulk_domain_mu_extra",
        "activated_rows": "R4;R7;R9;R11",
        "runner_action": "load P8/R11 source residual row or keep no-pass",
    },
    {
        "failed_action_term": "A3_boundary_class_topological",
        "activated_component": "P8_boundary_bulk_domain_mu_extra;P8_radial_source_hair",
        "activated_rows": "R3;R4;R7;R8;R9;R11",
        "runner_action": "score boundary/exchange coefficient vector against alpha3/Gdot/xi/gamma/beta locks",
    },
    {
        "failed_action_term": "A4_mass_flux_projector",
        "activated_component": "P8_Meff_conservation;P8_radial_source_hair",
        "activated_rows": "R1;R4;R9;R10;R11",
        "runner_action": "require source-normalization residuals before Newton claim",
    },
    {
        "failed_action_term": "A5_constant_universal_coupling",
        "activated_component": "P8_Geff_time_drift",
        "activated_rows": "R9;R11",
        "runner_action": "score Gdot/G or no-pass if missing",
    },
    {
        "failed_action_term": "A6_selector_blind_source_action",
        "activated_component": "P8_species_source_charge",
        "activated_rows": "R1;R11",
        "runner_action": "report source-charge WEP composite separately from direct WEP",
    },
    {
        "failed_action_term": "A7_bulk_X_nohair_or_curve",
        "activated_component": "P8_range_dependence;P8_radial_source_hair",
        "activated_rows": "R3;R4;R10;R11",
        "runner_action": "require alpha(lambda) curve or theorem-zero source",
    },
    {
        "failed_action_term": "A10_second_order_source_closure",
        "activated_component": "P8_nonlinear_beta_source_residue",
        "activated_rows": "R4;R11",
        "runner_action": "keep beta source residual active",
    },
]


GATE_TESTS = [
    {
        "gate": "parent_action_terms_written",
        "pass_condition": "all needed action blocks and variations are explicit",
        "current_result": "pass",
        "evidence": "11 parent action contract terms recorded",
    },
    {
        "gate": "q_retained_zero_conditions_written",
        "pass_condition": "legal zero routes are distinguished from retained-vector fallback",
        "current_result": "pass",
        "evidence": "6 zero-condition rows recorded",
    },
    {
        "gate": "no_cheat_tests_written",
        "pass_condition": "fake multiplier/readout/Bianchi/GM absorption shortcuts are blocked",
        "current_result": "pass",
        "evidence": "6 no-cheat tests recorded",
    },
    {
        "gate": "K_owner_action_term_derived",
        "pass_condition": "current parent action supplies formula-level K_owner from variation/Noether current",
        "current_result": "fail",
        "evidence": "contract written, not parent-derived",
    },
    {
        "gate": "q_retained_zero_parent_derived",
        "pass_condition": "all q_retained channels are absent/gauge/topological/no-haired or mapped",
        "current_result": "fail",
        "evidence": "multiple channels remain conditional/open/template-only",
    },
    {
        "gate": "measured_GM_promoted",
        "pass_condition": "P8 owner-current contract is satisfied and source residual vector is theorem-zero or evaluated",
        "current_result": "fail",
        "evidence": "parent action contract only",
    },
]


THEOREM_STATUS = [
    {
        "claim": "exact parent-action term contract written",
        "status": "pass",
        "evidence": str(ACTION_CONTRACT_PATH),
    },
    {
        "claim": "q_retained legal-zero conditions written",
        "status": "pass",
        "evidence": str(ZERO_CONDITIONS_PATH),
    },
    {
        "claim": "no-cheat action policy enforced",
        "status": "pass",
        "evidence": "ad hoc multipliers, readout masks, Bianchi shortcuts, and GM absorption shortcuts are blocked",
    },
    {
        "claim": "K_owner parent-derived",
        "status": "fail",
        "evidence": "no formula-level owner current from current parent action",
    },
    {
        "claim": "q_retained zero parent-derived",
        "status": "fail",
        "evidence": "source, boundary, domain, bulk, memory, and range channels remain open or template-only",
    },
    {
        "claim": "measured GM/Newton/local-GR promoted",
        "status": "fail",
        "evidence": "contract only; no P8 proof or residual-data pass",
    },
]


GATE_RESULTS_TEMPLATE = [
    {
        "gate": "problem_statement_written",
        "status": "pass",
        "evidence": "parent-action source-owner target and non-cheat rule recorded",
    },
    {
        "gate": "parent_action_blocks_written",
        "status": "pass",
        "evidence": "11 action blocks recorded",
    },
    {
        "gate": "variation_identity_requirements_written",
        "status": "pass",
        "evidence": "9 variation identities recorded",
    },
    {
        "gate": "q_retained_zero_conditions_written",
        "status": "pass",
        "evidence": str(ZERO_CONDITIONS_PATH),
    },
    {
        "gate": "no_cheat_action_tests_written",
        "status": "pass",
        "evidence": "6 no-cheat tests recorded",
    },
    {
        "gate": "residual_activation_map_written",
        "status": "pass",
        "evidence": "7 failure-to-row mappings recorded",
    },
    {
        "gate": "K_owner_parent_derived",
        "status": "fail",
        "evidence": "contract specifies required action term but does not derive it from corpus",
    },
    {
        "gate": "q_retained_zero_parent_derived",
        "status": "fail",
        "evidence": "legal zero routes remain unsatisfied for all channels",
    },
    {
        "gate": "measured_GM_parent_derived",
        "status": "fail",
        "evidence": "source-owner contract only",
    },
    {
        "gate": "Newtonian_reduction_promoted",
        "status": "fail",
        "evidence": "P8 remains open",
    },
    {
        "gate": "local_GR_promoted",
        "status": "fail",
        "evidence": "parent-action contract only; no EH/Newton/PPN/local-GR pass",
    },
    {
        "gate": "claim_ceiling_enforced",
        "status": "pass",
        "evidence": CLAIM_CEILING,
    },
]


DECISION = [
    {
        "decision": "The source-owner current is now expressed as an exact parent-action contract. To earn measured GM, the parent action must produce a formula-level owner current K_owner, prove q_retained=0 by a legal zero route, close the mass-flux projector, fix G_eff as constant/universal, remove species/range/radial/frame source charges, and keep the result through second-order beta. The current corpus does not derive those terms or variations. Therefore this checkpoint sharpens the path but does not promote K_owner, measured GM, Newton, PPN, or local GR.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "447-no-species-source-charge-one-coframe-theorem-attempt.md",
        "why_next": "species/source-charge blindness is the crispest sub-theorem inside the P8 contract",
    },
    {
        "rank": 2,
        "target": "map P8_source_owner_parent_action_terms_CONTRACT.csv into evaluator",
        "why_next": "contract failures should automatically activate P8 residual rows",
    },
    {
        "rank": 3,
        "target": "derive or demote mass-flux projector d(Pi_M J)=0",
        "why_next": "closed calibrated M_eff is the central measured-GM object",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCE_DOCS:
        source_path = ROOT / source["path"]
        rows.append(
            {
                "source_file": source["path"],
                "exists": source_path.exists(),
                "role": source["role"],
            }
        )
    return rows


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    source_gate = {
        "gate": "source_paths_exist",
        "status": "pass" if not missing_sources else "fail",
        "evidence": "all cited source paths exist" if not missing_sources else ";".join(missing_sources),
    }
    action_schema_gate = {
        "gate": "action_contract_schema_matches",
        "status": "pass" if list(PARENT_ACTION_BLOCKS[0].keys()) == ACTION_CONTRACT_COLUMNS else "fail",
        "evidence": "action contract columns match schema"
        if list(PARENT_ACTION_BLOCKS[0].keys()) == ACTION_CONTRACT_COLUMNS
        else "action contract schema mismatch",
    }
    zero_schema_gate = {
        "gate": "zero_conditions_schema_matches",
        "status": "pass" if list(Q_RETAINED_ZERO_CONDITIONS[0].keys()) == ZERO_CONDITION_COLUMNS else "fail",
        "evidence": "q_retained zero-condition columns match schema"
        if list(Q_RETAINED_ZERO_CONDITIONS[0].keys()) == ZERO_CONDITION_COLUMNS
        else "q_retained zero-condition schema mismatch",
    }
    return [source_gate, action_schema_gate, zero_schema_gate, *GATE_RESULTS_TEMPLATE]


def write_checkpoint_markdown(run_dir: Path, gate_result_rows: list[dict[str, Any]]) -> None:
    source_rows = source_register_rows()
    text = f"""# 446 - Source-Owner Current Parent-Action Contract

Private parent-action/source-ownership checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, R10/R11, measured-GM, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 445 proved only a conditional Ward source-ownership theorem. This checkpoint writes the exact parent-action structures and variation identities needed to turn that conditional theorem into a real derivation of `K_owner` and `q_retained=0`.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/source_owner_current_parent_action_contract.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Action contract | `{ACTION_CONTRACT_PATH}` |
| q-retained zero contract | `{ZERO_CONDITIONS_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_rows, ["source_file", "exists", "role"])}

## 4. Parent-Action Problem

{markdown_table(PARENT_ACTION_PROBLEM, ["item", "statement", "mathematical_form", "current_status"])}

## 5. Required Parent-Action Blocks

The parent-action source-owner term contract has been written to `{ACTION_CONTRACT_PATH}`.

{markdown_table(PARENT_ACTION_BLOCKS, ACTION_CONTRACT_COLUMNS)}

## 6. Variation Identity Requirements

{markdown_table(VARIATION_IDENTITY_REQUIREMENTS, ["variation_id", "vary", "identity", "must_show", "status"])}

## 7. q-retained Zero Conditions

The legal zero-condition contract has been written to `{ZERO_CONDITIONS_PATH}`.

{markdown_table(Q_RETAINED_ZERO_CONDITIONS, ZERO_CONDITION_COLUMNS)}

## 8. No-Cheat Action Tests

{markdown_table(NO_CHEAT_ACTION_TESTS, ["test_id", "bad_move", "legal_if", "current_result"])}

## 9. Residual Activation Map

{markdown_table(RESIDUAL_ACTIVATION_MAP, ["failed_action_term", "activated_component", "activated_rows", "runner_action"])}

## 10. Gate Tests

{markdown_table(GATE_TESTS, ["gate", "pass_condition", "current_result", "evidence"])}

## 11. Theorem Status

{markdown_table(THEOREM_STATUS, ["claim", "status", "evidence"])}

## 12. Gate Results

{markdown_table(gate_result_rows, ["gate", "status", "evidence"])}

## 13. Decision

{DECISION[0]["decision"]}

Practical read: this is the engineering drawing for the Ward/source win. It does not win the round yet, but it now says exactly what machine has to exist. No magic multiplier, no readout backreaction, no Bianchi shortcut, no hiding range/species/time dependence in `GM`.

## 14. Next Queue

{markdown_table(NEXT_QUEUE, ["rank", "target", "why_next"])}
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    gate_result_rows = gate_rows(source_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "parent_action_problem.csv", PARENT_ACTION_PROBLEM)
    write_csv(results_dir / "parent_action_blocks.csv", PARENT_ACTION_BLOCKS, ACTION_CONTRACT_COLUMNS)
    write_csv(results_dir / "variation_identity_requirements.csv", VARIATION_IDENTITY_REQUIREMENTS)
    write_csv(results_dir / "q_retained_zero_conditions.csv", Q_RETAINED_ZERO_CONDITIONS, ZERO_CONDITION_COLUMNS)
    write_csv(results_dir / "no_cheat_action_tests.csv", NO_CHEAT_ACTION_TESTS)
    write_csv(results_dir / "residual_activation_map.csv", RESIDUAL_ACTIVATION_MAP)
    write_csv(results_dir / "gate_tests.csv", GATE_TESTS)
    write_csv(results_dir / "theorem_status.csv", THEOREM_STATUS)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)
    write_csv(ROOT / ACTION_CONTRACT_PATH, PARENT_ACTION_BLOCKS, ACTION_CONTRACT_COLUMNS)
    write_csv(ROOT / ZERO_CONDITIONS_PATH, Q_RETAINED_ZERO_CONDITIONS, ZERO_CONDITION_COLUMNS)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "parent_action_terms": len(PARENT_ACTION_BLOCKS),
        "variation_identity_requirements": len(VARIATION_IDENTITY_REQUIREMENTS),
        "q_retained_zero_conditions": len(Q_RETAINED_ZERO_CONDITIONS),
        "no_cheat_tests": len(NO_CHEAT_ACTION_TESTS),
        "residual_activation_rows": len(RESIDUAL_ACTIVATION_MAP),
        "K_owner_parent_derived": False,
        "q_retained_zero_parent_derived": False,
        "measured_GM_parent_derived": False,
        "P8_promoted": False,
        "Newtonian_reduction_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "action_contract_path": str(ROOT / ACTION_CONTRACT_PATH),
        "zero_conditions_path": str(ROOT / ZERO_CONDITIONS_PATH),
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 446 source-owner current parent-action contract artifacts."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()
