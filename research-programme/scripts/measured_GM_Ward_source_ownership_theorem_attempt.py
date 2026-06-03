from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "measured-GM-Ward-source-ownership-theorem-attempt"
CHECKPOINT_DOC = "445-measured-GM-Ward-source-ownership-theorem-attempt.md"
STATUS = "measured_GM_Ward_source_ownership_theorem_attempt_written_conditional_identity_bianchi_not_enough_mu_extra_not_parent_derived_no_Newton_PPN_or_local_GR_pass"
CLAIM_CEILING = "Ward_source_ownership_conditional_theorem_only_no_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "446-source-owner-current-parent-action-contract.md"
OWNER_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_Ward_source_owner_identity_CONTRACT.csv")


OWNER_CONTRACT_COLUMNS = [
    "contract_id",
    "required_identity",
    "mathematical_form",
    "affected_components",
    "affected_rows",
    "current_status",
    "evidence_needed",
    "fallback_if_missing",
]


SOURCE_DOCS = [
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "parent-action Ward identity and source-normalized Newtonian limit contract",
    },
    {
        "path": "402-EH-source-normalization-parent-pair.md",
        "role": "mu_obs = G_eff M_eff + mu_extra weak-field chain",
    },
    {
        "path": "403-boundary-domain-flux-nohair-numeric-contract.md",
        "role": "alpha3/Gdot/source-charge flux locks and Ward-owned flux warning",
    },
    {
        "path": "405-same-frame-EH-source-derived-stack-audit.md",
        "role": "Ward flux silence and source-normalized GM listed as open GR stack rungs",
    },
    {
        "path": "419-boundary-exchange-coefficient-retained-evaluator.md",
        "role": "boundary/exchange coefficient retained evaluator",
    },
    {
        "path": "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
        "role": "source-normalization test plan and Ward/Bianchi next move",
    },
    {
        "path": "428-MTS-local-residual-vector-input-contract.md",
        "role": "local residual vector and measured-GM requirements",
    },
    {
        "path": "436-auxiliary-projector-local-Euler-equation-ledger.md",
        "role": "mass-flux projector and auxiliary/source Euler rows",
    },
    {
        "path": "439-EH-only-exterior-parent-premise-ladder.md",
        "role": "P8 constant source-normalization premise",
    },
    {
        "path": "441-extra-sector-nohair-priority-gate.md",
        "role": "source-normalization no-hair contract and priority",
    },
    {
        "path": "444-source-normalization-residual-vector-refinement.md",
        "role": "P8 residual-vector refinement and next target",
    },
    {
        "path": "runs/20260602-044500-boundary-domain-flux-nohair-numeric-contract/results/family_rollup.csv",
        "role": "numeric family locks for flux/source/drift rows",
    },
    {
        "path": "runs/20260602-044500-boundary-domain-flux-nohair-numeric-contract/results/flux_balance_equations.csv",
        "role": "flux balance equations from boundary/domain checkpoint",
    },
    {
        "path": "runs/20260602-044500-boundary-domain-flux-nohair-numeric-contract/results/nohair_mechanism_tests.csv",
        "role": "boundary/domain/flux no-hair mechanism tests",
    },
    {
        "path": "runs/20260602-073500-boundary-exchange-coefficient-retained-evaluator/results/retained_coefficients.csv",
        "role": "retained boundary/exchange coefficient rows",
    },
    {
        "path": "runs/20260602-123000-auxiliary-projector-local-Euler-equation-ledger/results/Euler_ledger_rows.csv",
        "role": "Euler ledger row A7 mass-flux projector source identity",
    },
    {
        "path": "runs/20260602-143000-source-normalization-residual-vector-refinement/results/mu_obs_decomposition.csv",
        "role": "measured-GM decomposition from checkpoint 444",
    },
    {
        "path": "runs/20260602-143000-source-normalization-residual-vector-refinement/results/P8_source_residual_template_rows.csv",
        "role": "P8 residual vector rows from checkpoint 444",
    },
    {
        "path": "runs/20260602-143000-source-normalization-residual-vector-refinement/results/P8_gate_tests.csv",
        "role": "P8 source-normalization gate tests",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv",
        "role": "P8 source residual template",
    },
    {
        "path": "source-intake/mts_residuals/R11_P8_source_normalization_rows_TEMPLATE.csv",
        "role": "P8 source-normalization R11 template",
    },
]


WARD_THEOREM_STATEMENT = [
    {
        "part": "conditional_theorem",
        "statement": "Ward/Bianchi conservation plus explicit source ownership implies measured-GM constancy only if every residual source current is an exact owned divergence with zero boundary flux and no species/range/frame charge.",
        "mathematical_form": "nabla_mu T_tot^{mu nu}=0; q_res^nu=nabla_mu K_owner^{mu nu}; n_i K_owner^{i0}|partialSigma=0; partial_{A,lambda,r} q_res^0=0 => partial_{t,A,lambda,r} mu_obs=0",
        "status": "proved_as_conditional_identity",
    },
    {
        "part": "non_theorem_warning",
        "statement": "Bianchi conservation alone conserves the total stress-energy; it does not prove the observed matter/source monopole is conserved or equal to measured orbital GM.",
        "mathematical_form": "nabla_mu(T_obs^{mu nu}+T_hidden^{mu nu})=0 does not imply nabla_mu T_obs^{mu nu}=0",
        "status": "blocks_parent_promotion",
    },
    {
        "part": "P8_success_condition",
        "statement": "Measured GM is derived only when G_eff is constant, M_eff is a closed calibrated monopole, and mu_extra integrates to zero with no residual source charge.",
        "mathematical_form": "mu_obs=G_eff M_eff + mu_extra = GM_measured; partial_{t,r,A,lambda} mu_obs=0; mu_extra=0",
        "status": "not_parent_derived",
    },
]


PROOF_STEPS = [
    {
        "step": 1,
        "claim": "Diffeomorphism invariance gives on-shell total conservation.",
        "mathematical_step": "nabla_mu T_tot^{mu nu}=0",
        "status": "structural_Ward_identity_available",
        "gap": "total conservation does not select the observed measured-GM source.",
    },
    {
        "step": 2,
        "claim": "Split the total source into observed matter/source plus owned residual sectors.",
        "mathematical_step": "T_tot^{mu nu}=T_obs^{mu nu}+T_owner^{mu nu}+T_unowned^{mu nu}",
        "status": "decomposition_required",
        "gap": "the parent action has not proved T_unowned^{mu nu}=0 or pure owned divergence.",
    },
    {
        "step": 3,
        "claim": "Define the measured-GM residual source as the part of the weak-field source not equal to constant G_eff M_eff.",
        "mathematical_step": "mu_extra = int_Sigma rho_extra d^3x + surface/projector/range/source-charge terms",
        "status": "definition_from_P8_refinement",
        "gap": "rho_extra components are templated, not theorem-zero.",
    },
    {
        "step": 4,
        "claim": "If the residual source density is an exact owned divergence, Gauss/Stokes pushes it to the boundary.",
        "mathematical_step": "rho_extra = partial_i V_owner^i => int_Sigma rho_extra d^3x = int_partialSigma n_i V_owner^i dS",
        "status": "valid_conditional_math",
        "gap": "exact-divergence ownership is not derived for boundary, bulk, domain, projector, or memory sectors.",
    },
    {
        "step": 5,
        "claim": "If boundary flux vanishes or is a universal constant calibration, the residual monopole vanishes or is absorbable.",
        "mathematical_step": "int_partialSigma n_i V_owner^i dS = 0 or constant universal calibration",
        "status": "valid_conditional_math",
        "gap": "prior flux rows show alpha3/Gdot/source locks remain open.",
    },
    {
        "step": 6,
        "claim": "If species, frame, radial, and range derivatives of the residual source vanish, measured GM is universal and range independent.",
        "mathematical_step": "partial_A mu_obs=partial_r mu_obs=partial_lambda mu_obs=0",
        "status": "valid_conditional_math",
        "gap": "no-marker, no-finite-range-charge, and one-frame calibration are not parent-derived.",
    },
    {
        "step": 7,
        "claim": "Then and only then the EH-to-Poisson chain becomes measured Newtonian gravity.",
        "mathematical_step": "nabla^2 Phi=4 pi G_eff rho_eff with mu_obs=GM_measured",
        "status": "conditional_Newton_route",
        "gap": "P8 conditions are open, so no Newton/PPN/local-GR promotion.",
    },
]


BIANCHI_INSUFFICIENCY_ROWS = [
    {
        "temptation": "total conservation implies source conservation",
        "why_false": "hidden sectors can exchange energy-momentum with observed matter while total T remains conserved",
        "required_fix": "derive separate observed-source current conservation or prove exchange is owned and boundary-silent",
        "affected_components": "P8_Meff_conservation;P8_boundary_bulk_domain_mu_extra",
    },
    {
        "temptation": "divergence terms do not affect monopoles",
        "why_false": "a divergence integrates to a boundary flux, and boundary flux is exactly one of the dangerous retained channels",
        "required_fix": "prove the surface integral vanishes or is a constant universal calibration",
        "affected_components": "P8_boundary_bulk_domain_mu_extra;P8_radial_source_hair",
    },
    {
        "temptation": "constant calibration can absorb all source differences",
        "why_false": "time, species, radial, and range dependence are observables, not unit choices",
        "required_fix": "prove partial_{t,A,r,lambda} mu_obs=0 before absorbing GM",
        "affected_components": "P8_Geff_time_drift;P8_species_source_charge;P8_range_dependence;P8_radial_source_hair",
    },
    {
        "temptation": "direct WEP row clears source charge",
        "why_false": "direct geometry WEP is not the full source-normalization composite; hidden source/test charges can survive",
        "required_fix": "derive species/source universality in the parent matter/source action",
        "affected_components": "P8_species_source_charge",
    },
    {
        "temptation": "source-free exterior means no fifth force",
        "why_false": "finite-range fields can be sourced by the compact body and live in the exterior",
        "required_fix": "derive zero source charge/screening or provide an executable alpha(lambda) curve",
        "affected_components": "P8_range_dependence",
    },
    {
        "temptation": "cosmological memory success implies local memory silence",
        "why_false": "a cosmological kernel can still produce local Gdot, flux, or source drift unless compact-local silence is derived",
        "required_fix": "derive local kernel silence or map Gdot/alpha3/R10 residuals",
        "affected_components": "P8_Geff_time_drift;P8_boundary_bulk_domain_mu_extra;P8_range_dependence",
    },
]


OWNER_CONDITION_AUDIT = [
    {
        "condition_id": "W0_all_sectors_varied",
        "required_identity": "all parent sectors are varied before any source residual is dropped",
        "mathematical_form": "delta S_parent/delta Z_I=0 for X, P_D, boundary, domain, Pi_M J, nonmetric/source variables",
        "current_status": "ledger_available_not_solved",
        "evidence": "A0-A9 Euler ledger rows exist, but most zero conditions are not derived",
        "fallback": "retain affected P8/R11 residual rows",
    },
    {
        "condition_id": "W1_total_to_owned_split",
        "required_identity": "Ward identity decomposes every force channel into owned zero/boundary/retained pieces",
        "mathematical_form": "F_X^nu+F_P^nu+F_boundary^nu+F_domain^nu+F_nonmetric^nu = nabla_mu K_owner^{mu nu}+q_retained^nu",
        "current_status": "not_parent_derived",
        "evidence": "structural Ward identity written but not closed",
        "fallback": "q_retained feeds P8_boundary_bulk_domain_mu_extra and R7/R9/R11",
    },
    {
        "condition_id": "W2_zero_boundary_flux",
        "required_identity": "owned divergence has zero flux through the compact local boundary",
        "mathematical_form": "int_partialSigma n_i K_owner^{i0} dS = 0",
        "current_status": "fail_open",
        "evidence": "alpha3_flux and Gdot_drift families remain not_parent_derived",
        "fallback": "retain flux coefficients against alpha3/Gdot locks",
    },
    {
        "condition_id": "W3_closed_mass_flux_projector",
        "required_identity": "mass-flux projector gives a closed calibrated source monopole",
        "mathematical_form": "d(Pi_M J)=0; M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J",
        "current_status": "conditional_flux_calibration_open",
        "evidence": "A7 mass_flux_projector row remains open",
        "fallback": "P8_Meff_conservation and P8_radial_source_hair remain active",
    },
    {
        "condition_id": "W4_constant_coupling",
        "required_identity": "G_eff/kappa_eff is constant and universal in the observed local branch",
        "mathematical_form": "partial_t G_eff=partial_r G_eff=partial_A G_eff=0",
        "current_status": "not_parent_derived",
        "evidence": "constant_kappa_to_Geff gate fails open",
        "fallback": "P8_Geff_time_drift and source-normalization R11 rows",
    },
    {
        "condition_id": "W5_species_universality",
        "required_identity": "no material marker, source charge, or species spurion enters the active gravitational source",
        "mathematical_form": "partial_A mu_obs=0",
        "current_status": "not_parent_derived",
        "evidence": "source_charge_WEP row remains retained",
        "fallback": "P8_species_source_charge",
    },
    {
        "condition_id": "W6_no_range_or_radial_hair",
        "required_identity": "source strength has no radial/range dependence after monopole extraction",
        "mathematical_form": "partial_r mu_obs=partial_lambda mu_obs=0",
        "current_status": "not_derived_symbolic",
        "evidence": "R10 remains symbolic and radial/boundary hair is retained",
        "fallback": "P8_range_dependence and P8_radial_source_hair",
    },
    {
        "condition_id": "W7_same_frame_source_calibration",
        "required_identity": "matter/source/clocks/metric use the same observed coframe and source calibration",
        "mathematical_form": "e_source=e_matter=e_metric plus universal standards",
        "current_status": "conditional_not_parent_derived",
        "evidence": "one-coframe and source calibration gates remain conditional",
        "fallback": "P8_frame_calibration_split",
    },
    {
        "condition_id": "W8_second_order_source_closure",
        "required_identity": "source normalization remains closed at second post-Newtonian order",
        "mathematical_form": "delta_beta_source=0 after measured-GM normalization",
        "current_status": "not_derived",
        "evidence": "first-order Poisson chain is conditional and does not clear beta",
        "fallback": "P8_nonlinear_beta_source_residue",
    },
]


RESIDUAL_CURRENT_LEDGER = [
    {
        "current_or_channel": "bulk_X_source_exchange",
        "symbolic_form": "F_X^nu or q_X rho_source",
        "owner_success_condition": "positive source-free no-hair or mapped alpha_X(lambda_X) with source charge zero/below curve",
        "if_unowned_rows": "R1;R3;R4;R9;R10;R11",
        "current_status": "operator_and_sources_not_parent_derived",
    },
    {
        "current_or_channel": "projector_domain_exchange",
        "symbolic_form": "F_P^nu + F_domain^nu",
        "owner_success_condition": "projector/domain variables are topological/gauge or their stress is coefficient-mapped",
        "if_unowned_rows": "R5;R6;R7;R8;R9;R10;R11",
        "current_status": "retained_symbolic",
    },
    {
        "current_or_channel": "boundary_flux",
        "symbolic_form": "F_boundary^nu or n_i K_owner^{i nu}",
        "owner_success_condition": "class-only boundary with zero local flux/radial/shear/vector hair",
        "if_unowned_rows": "R3;R4;R7;R8;R9;R11",
        "current_status": "conditional_noangular_radial_flux_open",
    },
    {
        "current_or_channel": "nonmetric_or_connection_source_exchange",
        "symbolic_form": "F_matter_nonmetric^nu plus torsion/projective source charge",
        "owner_success_condition": "Levi-Civita/same-frame matter connection theorem or explicit P4/P8 rows below bounds",
        "if_unowned_rows": "R0;R1;R2;R11",
        "current_status": "P4_demoted_to_R11",
    },
    {
        "current_or_channel": "mass_flux_projector",
        "symbolic_form": "d(Pi_M J)",
        "owner_success_condition": "closed calibrated source monopole with no radial/time/species leakage",
        "if_unowned_rows": "R1;R4;R9;R10;R11",
        "current_status": "conditional_flux_calibration_open",
    },
    {
        "current_or_channel": "memory_kernel_drift",
        "symbolic_form": "partial_t K_memory or local history kernel contribution",
        "owner_success_condition": "compact-local kernel silence or explicit Gdot/alpha3/R10 residual map",
        "if_unowned_rows": "R7;R9;R10;R11",
        "current_status": "retained",
    },
    {
        "current_or_channel": "species_source_charge",
        "symbolic_form": "partial_A mu_obs",
        "owner_success_condition": "no material marker/species spurion/source charge in parent source action",
        "if_unowned_rows": "R1;R11",
        "current_status": "not_parent_derived",
    },
    {
        "current_or_channel": "finite_range_source_charge",
        "symbolic_form": "partial_lambda mu_obs or alpha(lambda)",
        "owner_success_condition": "no finite-range source charge, exact screening, or executable alpha(lambda) curve below bounds",
        "if_unowned_rows": "R10;R11",
        "current_status": "not_derived_symbolic",
    },
]


OWNER_IDENTITY_CONTRACT = [
    {
        "contract_id": "C0_on_shell_total_Ward",
        "required_identity": "parent action yields total on-shell Ward conservation after all variables are varied",
        "mathematical_form": "nabla_mu T_tot^{mu nu}=0",
        "affected_components": "all_P8_components",
        "affected_rows": "R0-R11",
        "current_status": "structural_available_not_sufficient",
        "evidence_needed": "explicit parent variation with every sector included",
        "fallback_if_missing": "no source-ownership theorem; retain residual vector",
    },
    {
        "contract_id": "C1_exact_owner_decomposition",
        "required_identity": "all residual force/source terms are exact owned divergences plus retained mapped rows",
        "mathematical_form": "q_res^nu = nabla_mu K_owner^{mu nu} + q_retained^nu",
        "affected_components": "P8_boundary_bulk_domain_mu_extra;P8_Meff_conservation",
        "affected_rows": "R4;R7;R9;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "formula for K_owner and proof q_retained=0 or mapped",
        "fallback_if_missing": "retain mu_extra and alpha3/Gdot source residual rows",
    },
    {
        "contract_id": "C2_zero_owner_flux",
        "required_identity": "owned divergence has no compact exterior boundary flux",
        "mathematical_form": "int_partialSigma n_i K_owner^{i0} dS = 0",
        "affected_components": "P8_boundary_bulk_domain_mu_extra;P8_radial_source_hair",
        "affected_rows": "R3;R4;R7;R8;R9;R11",
        "current_status": "fail_open",
        "evidence_needed": "class-only/topological boundary theorem with no radial/shear/vector/flux hair",
        "fallback_if_missing": "boundary/exchange coefficient vector",
    },
    {
        "contract_id": "C3_closed_calibrated_mass_current",
        "required_identity": "mass-flux projector is closed and absolutely calibrated to the measured source monopole",
        "mathematical_form": "d(Pi_M J)=0 and M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J",
        "affected_components": "P8_Meff_conservation;P8_radial_source_hair",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_status": "conditional_flux_calibration_open",
        "evidence_needed": "Euler equation for Pi_M J plus calibration proof",
        "fallback_if_missing": "source-normalization residual vector",
    },
    {
        "contract_id": "C4_constant_universal_coupling",
        "required_identity": "G_eff/kappa_eff carries no time/radius/species/frame dependence",
        "mathematical_form": "partial_t G_eff=partial_r G_eff=partial_A G_eff=0",
        "affected_components": "P8_Geff_time_drift;P8_species_source_charge;P8_frame_calibration_split",
        "affected_rows": "R1;R2;R9;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "constant-coupling parent identity or numeric residuals",
        "fallback_if_missing": "Gdot/source/clock residual rows",
    },
    {
        "contract_id": "C5_no_species_or_marker_source_charge",
        "required_identity": "active source has no material-marker or species spurion",
        "mathematical_form": "partial_A mu_obs=0",
        "affected_components": "P8_species_source_charge",
        "affected_rows": "R1;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "selector-blind source action theorem",
        "fallback_if_missing": "eta_source residual row",
    },
    {
        "contract_id": "C6_no_range_or_radial_source_hair",
        "required_identity": "active source has no radial or finite-range dependence beyond the constant monopole",
        "mathematical_form": "partial_r mu_obs=partial_lambda mu_obs=0",
        "affected_components": "P8_range_dependence;P8_radial_source_hair",
        "affected_rows": "R3;R4;R10;R11",
        "current_status": "not_derived_symbolic",
        "evidence_needed": "no-hair theorem or executable alpha(lambda)/radial residual",
        "fallback_if_missing": "R10 curve and P8 radial source row",
    },
    {
        "contract_id": "C7_second_order_source_closure",
        "required_identity": "first-order measured-GM normalization remains valid at beta/PPN order",
        "mathematical_form": "delta_beta_source=0",
        "affected_components": "P8_nonlinear_beta_source_residue",
        "affected_rows": "R4;R11",
        "current_status": "not_derived",
        "evidence_needed": "second-order weak-field source solution in observed frame",
        "fallback_if_missing": "beta source residual row",
    },
]


GATE_TESTS = [
    {
        "gate": "conditional_theorem_written",
        "pass_condition": "Ward ownership theorem is expressed as exact conditional identity",
        "current_result": "pass",
        "evidence": "conditional theorem and proof steps recorded",
    },
    {
        "gate": "Bianchi_not_overclaimed",
        "pass_condition": "total conservation is not used as separate measured-GM conservation",
        "current_result": "pass",
        "evidence": "Bianchi insufficiency rows recorded",
    },
    {
        "gate": "owner_current_derived",
        "pass_condition": "parent action supplies K_owner and proves q_retained=0 or mapped",
        "current_result": "fail",
        "evidence": "no explicit K_owner formula or q_retained zero proof in current corpus",
    },
    {
        "gate": "zero_boundary_flux_derived",
        "pass_condition": "compact exterior boundary flux integral vanishes or is constant universal calibration",
        "current_result": "fail",
        "evidence": "alpha3/Gdot flux families remain not_parent_derived",
    },
    {
        "gate": "closed_mass_current_derived",
        "pass_condition": "d(Pi_M J)=0 and absolute M_eff calibration are parent-derived",
        "current_result": "fail",
        "evidence": "A7 mass-flux projector remains conditional_flux_calibration_open",
    },
    {
        "gate": "species_range_frame_silence_derived",
        "pass_condition": "partial_A mu_obs, partial_lambda mu_obs, and frame split vanish by theorem",
        "current_result": "fail",
        "evidence": "P8 species, range, and frame residual components remain template rows",
    },
    {
        "gate": "measured_GM_promoted",
        "pass_condition": "partial_{t,r,A,lambda} mu_obs=0 and mu_extra=0 are parent-derived",
        "current_result": "fail",
        "evidence": "conditional theorem only; no parent-derived P8",
    },
]


THEOREM_ATTEMPT_STATUS = [
    {
        "claim": "Ward source-ownership conditional theorem written",
        "status": "pass",
        "evidence": "proof steps show Ward + exact owner + zero flux + universality implies P8",
    },
    {
        "claim": "Bianchi-only shortcut rejected",
        "status": "pass",
        "evidence": "total conservation does not imply observed source conservation",
    },
    {
        "claim": "owner identity contract written",
        "status": "pass",
        "evidence": str(OWNER_CONTRACT_PATH),
    },
    {
        "claim": "K_owner/q_retained parent-derived",
        "status": "fail",
        "evidence": "no explicit parent variation closes all exchange/source channels",
    },
    {
        "claim": "mu_extra theorem-zero",
        "status": "fail",
        "evidence": "boundary, bulk, domain, memory, source-charge, and finite-range rows remain legal",
    },
    {
        "claim": "measured GM parent-derived",
        "status": "fail",
        "evidence": "P8 remains conditional, not promoted",
    },
    {
        "claim": "Newton/PPN/local-GR promoted",
        "status": "fail",
        "evidence": "theorem attempt only; no source residual data or PPN solution",
    },
]


GATE_RESULTS_TEMPLATE = [
    {
        "gate": "Ward_theorem_statement_written",
        "status": "pass",
        "evidence": "conditional theorem statement recorded",
    },
    {
        "gate": "proof_steps_written",
        "status": "pass",
        "evidence": "7 proof steps recorded",
    },
    {
        "gate": "Bianchi_insufficiency_written",
        "status": "pass",
        "evidence": "6 no-cheat insufficiency rows recorded",
    },
    {
        "gate": "owner_condition_audit_written",
        "status": "pass",
        "evidence": "9 source-owner conditions audited",
    },
    {
        "gate": "residual_current_ledger_written",
        "status": "pass",
        "evidence": "8 residual current/source channels recorded",
    },
    {
        "gate": "owner_identity_contract_written",
        "status": "pass",
        "evidence": str(OWNER_CONTRACT_PATH),
    },
    {
        "gate": "K_owner_parent_derived",
        "status": "fail",
        "evidence": "no explicit K_owner/q_retained identity supplied by parent action",
    },
    {
        "gate": "mu_extra_zero_derived",
        "status": "fail",
        "evidence": "zero boundary flux and source-current closure are not parent-derived",
    },
    {
        "gate": "measured_GM_parent_derived",
        "status": "fail",
        "evidence": "conditional theorem only",
    },
    {
        "gate": "Newtonian_reduction_promoted",
        "status": "fail",
        "evidence": "P8 remains open",
    },
    {
        "gate": "local_GR_promoted",
        "status": "fail",
        "evidence": "Ward/source checkpoint only; no EH/Newton/PPN/local-GR pass",
    },
    {
        "gate": "claim_ceiling_enforced",
        "status": "pass",
        "evidence": CLAIM_CEILING,
    },
]


DECISION = [
    {
        "decision": "The measured-GM Ward route has been attempted. It produces a real conditional theorem: if the parent action derives an exact owned residual current, zero compact boundary flux, a closed calibrated mass-flux projector, constant universal G_eff, no species/range/frame source charge, and second-order source closure, then mu_extra=0 and measured GM is constant. The current corpus does not supply the owner current or the zero-flux/source-universality proofs. Therefore Bianchi/Ward conservation is useful but not sufficient; measured GM is not promoted and P8 remains a residual-vector/parent-contract problem.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "446-source-owner-current-parent-action-contract.md",
        "why_next": "write the exact parent-action terms/variations needed to produce K_owner and q_retained=0",
    },
    {
        "rank": 2,
        "target": "map P8_Ward_source_owner_identity_CONTRACT.csv into P8 residual-vector evaluator",
        "why_next": "if the theorem remains open, the evaluator needs to see which contract failures activate which residual rows",
    },
    {
        "rank": 3,
        "target": "derive no-species/source-charge theorem from one-coframe matter action",
        "why_next": "species universality is the cleanest sub-gate inside P8 after owner-current closure",
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
    owner_contract_schema_gate = {
        "gate": "owner_contract_schema_matches",
        "status": "pass" if list(OWNER_IDENTITY_CONTRACT[0].keys()) == OWNER_CONTRACT_COLUMNS else "fail",
        "evidence": "owner identity contract columns match schema"
        if list(OWNER_IDENTITY_CONTRACT[0].keys()) == OWNER_CONTRACT_COLUMNS
        else "owner identity contract schema mismatch",
    }
    return [source_gate, owner_contract_schema_gate, *GATE_RESULTS_TEMPLATE]


def write_checkpoint_markdown(run_dir: Path, gate_result_rows: list[dict[str, Any]]) -> None:
    source_rows = source_register_rows()
    text = f"""# 445 - Measured-GM Ward Source-Ownership Theorem Attempt

Private Newton/source-ownership theorem checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, R10/R11, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 444 split measured `GM` into exact P8 residual components. This checkpoint attempts the derivation: can Ward/Bianchi ownership force `mu_extra=0` and make measured `GM` constant, or does it only give a conditional theorem with retained source rows?

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/measured_GM_Ward_source_ownership_theorem_attempt.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Owner identity contract | `{OWNER_CONTRACT_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_rows, ["source_file", "exists", "role"])}

## 4. Ward Theorem Statement

{markdown_table(WARD_THEOREM_STATEMENT, ["part", "statement", "mathematical_form", "status"])}

## 5. Conditional Proof Steps

{markdown_table(PROOF_STEPS, ["step", "claim", "mathematical_step", "status", "gap"])}

## 6. Why Bianchi Alone Is Not Enough

{markdown_table(BIANCHI_INSUFFICIENCY_ROWS, ["temptation", "why_false", "required_fix", "affected_components"])}

## 7. Owner Condition Audit

{markdown_table(OWNER_CONDITION_AUDIT, ["condition_id", "required_identity", "mathematical_form", "current_status", "fallback"])}

## 8. Residual Current Ledger

{markdown_table(RESIDUAL_CURRENT_LEDGER, ["current_or_channel", "symbolic_form", "owner_success_condition", "if_unowned_rows", "current_status"])}

## 9. Owner Identity Contract

The source-owner contract has been written to `{OWNER_CONTRACT_PATH}`.

{markdown_table(OWNER_IDENTITY_CONTRACT, OWNER_CONTRACT_COLUMNS)}

## 10. Gate Tests

{markdown_table(GATE_TESTS, ["gate", "pass_condition", "current_result", "evidence"])}

## 11. Theorem Attempt Status

{markdown_table(THEOREM_ATTEMPT_STATUS, ["claim", "status", "evidence"])}

## 12. Gate Results

{markdown_table(gate_result_rows, ["gate", "status", "evidence"])}

## 13. Decision

{DECISION[0]["decision"]}

Practical read: this is a good narrow miss, not a collapse. Ward/Bianchi is the right weapon, but it does not automatically knock out `mu_extra`. It wins only when the parent action shows exactly who owns every exchange current and why the compact boundary carries no source flux. Otherwise the source residual vector stays in the ring.

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
    write_csv(results_dir / "Ward_theorem_statement.csv", WARD_THEOREM_STATEMENT)
    write_csv(results_dir / "proof_steps.csv", PROOF_STEPS)
    write_csv(results_dir / "Bianchi_insufficiency_rows.csv", BIANCHI_INSUFFICIENCY_ROWS)
    write_csv(results_dir / "owner_condition_audit.csv", OWNER_CONDITION_AUDIT)
    write_csv(results_dir / "residual_current_ledger.csv", RESIDUAL_CURRENT_LEDGER)
    write_csv(results_dir / "owner_identity_contract.csv", OWNER_IDENTITY_CONTRACT, OWNER_CONTRACT_COLUMNS)
    write_csv(results_dir / "gate_tests.csv", GATE_TESTS)
    write_csv(results_dir / "theorem_attempt_status.csv", THEOREM_ATTEMPT_STATUS)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)
    write_csv(ROOT / OWNER_CONTRACT_PATH, OWNER_IDENTITY_CONTRACT, OWNER_CONTRACT_COLUMNS)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "Ward_conditional_theorem_written": True,
        "Bianchi_only_shortcut_rejected": True,
        "owner_condition_rows": len(OWNER_CONDITION_AUDIT),
        "residual_current_rows": len(RESIDUAL_CURRENT_LEDGER),
        "owner_contract_rows": len(OWNER_IDENTITY_CONTRACT),
        "K_owner_parent_derived": False,
        "q_retained_zero_derived": False,
        "zero_boundary_flux_derived": False,
        "closed_mass_current_derived": False,
        "mu_extra_zero_derived": False,
        "measured_GM_parent_derived": False,
        "P8_promoted": False,
        "Newtonian_reduction_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "owner_contract_path": str(ROOT / OWNER_CONTRACT_PATH),
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
        description="Write checkpoint 445 measured-GM Ward source-ownership theorem attempt artifacts."
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
