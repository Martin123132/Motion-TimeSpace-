from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "PiM-flux-closure-Ward-or-topological-current-attempt"
CHECKPOINT_DOC = "455-PiM-flux-closure-Ward-or-topological-current-attempt.md"
STATUS = "PiM_flux_closure_Ward_or_topological_current_attempt_written_conditional_mass_current_routes_not_parent_derived_dMeff_radial_hair_retained_no_Newton_or_local_GR_pass"
CLAIM_CEILING = "PiM_flux_closure_attempt_only_no_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "456-PiM-projector-variation-stress-ledger.md"
CONTRACT_PATH = Path("source-intake/mts_residuals/P8_PiM_flux_closure_Ward_topological_CONTRACT.csv")


CONTRACT_COLUMNS = [
    "contract_id",
    "required_identity",
    "mathematical_form",
    "closes_component",
    "affected_rows",
    "current_status",
    "evidence_needed",
    "fallback_if_missing",
]


SOURCE_DOCS = [
    {
        "path": "454-PiM-parent-symplectic-projector-algebra-attempt.md",
        "role": "immediate Pi_M algebra checkpoint and PM6 closure next target",
    },
    {
        "path": "source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        "role": "PM0-PM8 projector algebra and closure contract feeding this attempt",
    },
    {
        "path": "244-Meff-monopole-source-normalization-or-radial-memory-hair.md",
        "role": "conditional Stokes theorem: closed Pi_M flux gives radially conserved M_eff",
    },
    {
        "path": "445-measured-GM-Ward-source-ownership-theorem-attempt.md",
        "role": "Ward source-ownership theorem and Bianchi warning",
    },
    {
        "path": "446-source-owner-current-parent-action-contract.md",
        "role": "parent action terms for K_owner, q_retained, and mass-flux projector closure",
    },
    {
        "path": "449-source-current-Ward-universality-theorem-attempt.md",
        "role": "Hilbert source-current Ward sublemma and measured-GM caveat",
    },
    {
        "path": "451-mass-flux-projector-Euler-calibration-attempt.md",
        "role": "Euler closure attempt and no-ad-hoc multiplier warning",
    },
    {
        "path": "251-N5-boundary-projector-parent-owner-or-modified-exterior-branch.md",
        "role": "topological projector stress-silence route and Hodge projector no-go warning",
    },
    {
        "path": "252-topological-projector-parent-action-skeleton.md",
        "role": "metric-independent topological projector parent skeleton template",
    },
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "minimal parent local action and source-normalized Newtonian limit contract",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_current_Ward_universality_CONTRACT.csv",
        "role": "SC6 closed calibrated mass projector contract",
    },
    {
        "path": "source-intake/mts_residuals/P8_Ward_source_owner_identity_CONTRACT.csv",
        "role": "C3 closed calibrated mass current and owner-current contracts",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
        "role": "A4 mass-flux projector parent-action block",
    },
    {
        "path": "source-intake/mts_residuals/P8_q_retained_zero_conditions_CONTRACT.csv",
        "role": "legal zero routes for retained source/exchange current",
    },
    {
        "path": "runs/20260602-101500-Ward-Bianchi-exchange-owner-for-Poisson-source/results/Ward_identity_chain.csv",
        "role": "Bianchi/Ward chain showing exchange terms and measured-GM limitation",
    },
    {
        "path": "runs/20260602-101500-Ward-Bianchi-exchange-owner-for-Poisson-source/results/source_residual_decomposition.csv",
        "role": "source residual decomposition including non-Hilbert and boundary flux channels",
    },
    {
        "path": "runs/20260602-150000-source-owner-current-parent-action-contract/results/parent_action_blocks.csv",
        "role": "machine A4 mass-flux projector parent-action term",
    },
    {
        "path": "runs/20260602-010500-parent-local-action-minimal-contract/results/action_blocks.csv",
        "role": "minimal action S_source_normalization block",
    },
]


THEOREM_STATEMENT = [
    {
        "part": "conditional_mass_flux_closure_theorem",
        "statement": "If the parent action supplies a same-frame Hilbert mass-channel current J_M=Pi_M J_H, a local stationarity/Hamiltonian or topological conservation identity gives dJ_M=0 in the compact exterior, projector variation is owned, and all non-Hilbert/boundary exchange fluxes have zero mass-channel projection, then M_eff is radially and temporally conserved.",
        "mathematical_form": "J_M=Pi_M J_H; dJ_M=0; int_boundary K_owner^M=0 => M_eff(r2)-M_eff(r1)=int_{S2xI} dJ_M=0",
        "status": "valid_conditional_route",
    },
    {
        "part": "Ward_limit",
        "statement": "Diffeomorphism Ward conservation of total stress is not enough. It gives source bookkeeping, but mass-flux closure requires a separately conserved mass-channel current or a proof that all exchange terms have zero Pi_M projection.",
        "mathematical_form": "nabla_mu T_tot^{mu nu}=0 does not imply d(Pi_M J_H)=0 if F_X,F_P,F_B,F_D,F_nm,delta kappa survive",
        "status": "blocks_overclaim",
    },
    {
        "part": "Killing_Hamiltonian_route",
        "statement": "A GR-like route can close the current if the compact exterior has an observed stationary time generator xi, the same-frame Hilbert stress is separately conserved, and j_M^mu=T_H^{mu nu}xi_nu has zero exchange and boundary flux. This is promising but depends on local stationarity/EH-asymptotic structure that is not yet parent-derived.",
        "mathematical_form": "nabla_mu j_M^mu=T_H^{mu nu}nabla_(mu xi_nu)+xi_nu nabla_mu T_H^{mu nu}; xi Killing and nabla T_H=0 => d(*j_M)=0",
        "status": "conditional_not_parent_derived",
    },
    {
        "part": "topological_current_route",
        "statement": "A topological route can close the mass channel if a parent BF/closed-form sector supplies a metric-independent mass current J_M^top with dJ_M^top=0 and an on-shell identity J_M^top=Pi_M J_H. The closure is then real only if that sector is independently motivated and variation-owned.",
        "mathematical_form": "dJ_M^top=0; J_M^top=Pi_M J_H on shell => d(Pi_M J_H)=0",
        "status": "promising_future_route_not_in_corpus",
    },
    {
        "part": "Euler_multiplier_limit",
        "statement": "An Euler equation E_lambdaM=d(Pi_M J_H)=0 is sufficient as mathematics, but it is not a derivation if lambda_M is added only to repair Newtonian GM. The multiplier must be gauge, topological, Ward, or source-normalization owned.",
        "mathematical_form": "delta_{lambda_M} S=0 => d(Pi_M J_H)=0; legal only if lambda_M has independent parent origin",
        "status": "closure_only_unless_owned",
    },
    {
        "part": "current_corpus_status",
        "statement": "The corpus has all the right conditional ingredients, but it has not derived a mass-channel Ward current, a topological closed mass current, zero boundary/non-Hilbert flux, projector variation silence, absolute calibration, or second-order source stability.",
        "mathematical_form": "FC0-FC8 remain contract rows; dM_eff/radial hair residuals retained",
        "status": "not_parent_derived",
    },
]


CLOSURE_ROUTES = [
    {
        "route_id": "R0_Ward_Killing_mass_current",
        "mechanism": "use a stationary observed time generator to turn Hilbert stress conservation into a conserved mass current",
        "mathematical_form": "j_M^mu=T_H^{mu nu}xi_nu; xi Killing; nabla_mu T_H^{mu nu}=0 => d(*j_M)=0",
        "would_close": "d(Pi_M J_H)=0 if Pi_M J_H=*j_M and exchange flux is zero",
        "required_extra_premise": "same-frame Hilbert stress, local stationarity/asymptotic time, no hidden exchange, zero boundary flux",
        "current_status": "conditional_not_parent_derived",
    },
    {
        "route_id": "R1_Hamiltonian_boundary_charge",
        "mechanism": "derive mass as the conserved Hamiltonian/asymptotic boundary charge of the local EH exterior branch",
        "mathematical_form": "dH_xi/dt=0 and delta H_xi = int_S2 Pi_M J_H after constraints",
        "would_close": "constant M_eff and calibration bridge if EH exterior and source matching are already derived",
        "required_extra_premise": "EH-only exterior operator, boundary conditions, asymptotic/compact Hamiltonian map",
        "current_status": "conditional_but_downstream_of_EH_gate",
    },
    {
        "route_id": "R2_topological_closed_mass_current",
        "mechanism": "introduce a metric-independent closed mass-current sector whose on-shell representative equals Pi_M J_H",
        "mathematical_form": "J_M^top=dB_M or dJ_M^top=0; J_M^top=Pi_M J_H",
        "would_close": "d(Pi_M J_H)=0 without Hodge metric stress if equality is parent-derived",
        "required_extra_premise": "BF/closed-form sector with independent reason and no local stress/source charge",
        "current_status": "promising_future_route_not_in_corpus",
    },
    {
        "route_id": "R3_source_owner_zero_projection",
        "mechanism": "use the Ward owner ledger to show every retained exchange current has zero Pi_M projection through the annulus",
        "mathematical_form": "Pi_M(q_retained + dK_owner)=0 and int_boundary Pi_M K_owner=0",
        "would_close": "mass channel even if other non-mass sectors remain",
        "required_extra_premise": "formula-level K_owner, q_retained zero or orthogonal, boundary no-flux",
        "current_status": "not_parent_derived",
    },
    {
        "route_id": "R4_Euler_source_normalization_constraint",
        "mechanism": "vary a source-normalization multiplier to impose closed projected mass flux",
        "mathematical_form": "S_M=int lambda_M wedge d(Pi_M J_H); E_lambdaM=0",
        "would_close": "d(Pi_M J_H)=0 directly",
        "required_extra_premise": "lambda_M is gauge/topological/Ward-owned, not an ad hoc Newton repair",
        "current_status": "sufficient_math_closure_only_without_origin",
    },
    {
        "route_id": "R5_retained_residual_branch",
        "mechanism": "do not close the current; make d(Pi_M J_H) executable as source-normalization residual data",
        "mathematical_form": "d(Pi_M J_H) -> dln_Meff_dt, partial_r ln mu_obs, mu_extra/(GM)",
        "would_close": "nothing; keeps the branch testable",
        "required_extra_premise": "units, normalization, coefficient/curve source, local bounds",
        "current_status": "fallback_required_if_R0_R4_fail",
    },
]


MASS_CHANNEL_DECOMPOSITION = [
    {
        "term": "Hilbert_matter_mass_current",
        "symbolic_form": "Pi_M J_H",
        "closure_condition": "same-frame Hilbert stress has a conserved mass/energy current in the observed local branch",
        "if_nonzero_or_open_rows": "R1;R4;R9;R11",
        "current_status": "conditional_from_source_Ward_not_mass_closed",
    },
    {
        "term": "projector_variation_flux",
        "symbolic_form": "(d Pi_M) J_H or (delta Pi_M)J_H",
        "closure_condition": "Pi_M is metric-independent/topological or variation stress is theorem-zero",
        "if_nonzero_or_open_rows": "R3;R4;R7;R8;R10;R11",
        "current_status": "not_parent_derived",
    },
    {
        "term": "boundary_owner_flux",
        "symbolic_form": "int_boundary Pi_M K_owner",
        "closure_condition": "compact-boundary mass flux vanishes or is universal constant calibration",
        "if_nonzero_or_open_rows": "R3;R4;R7;R8;R9;R11",
        "current_status": "fail_open",
    },
    {
        "term": "hidden_exchange_mass_projection",
        "symbolic_form": "Pi_M(F_X + F_P + F_D + F_nm)",
        "closure_condition": "exchange owners are zero, exact with zero boundary flux, or orthogonal to Pi_M",
        "if_nonzero_or_open_rows": "R0;R3;R4;R7;R8;R9;R10;R11",
        "current_status": "not_parent_derived",
    },
    {
        "term": "coupling_source_drift",
        "symbolic_form": "Pi_M[T_obs d kappa_eff]",
        "closure_condition": "kappa_eff/G_eff is constant and universal",
        "if_nonzero_or_open_rows": "R1;R4;R9;R10;R11",
        "current_status": "conditional_from_453_not_parent_derived",
    },
    {
        "term": "finite_range_or_radial_source_hair",
        "symbolic_form": "partial_r mu_obs or partial_lambda mu_obs",
        "closure_condition": "no radial/range source charge or executable alpha(lambda) below locks",
        "if_nonzero_or_open_rows": "R3;R4;R10;R11",
        "current_status": "not_derived_symbolic",
    },
]


DERIVATION_STEPS = [
    {
        "step": 1,
        "claim": "The 454 algebra reduces the closure equation to constancy of the mass-channel charge.",
        "mathematical_step": "Pi_M J_H=ell_M(J_H) omega_M and d omega_M=0, so d(Pi_M J_H)=d ell_M(J_H) wedge omega_M",
        "status": "algebra_imported",
        "gap": "does not show d ell_M(J_H)=0",
    },
    {
        "step": 2,
        "claim": "Stokes makes the physical meaning exact.",
        "mathematical_step": "M_eff(r2)-M_eff(r1) proportional to int_{S2xI} d(Pi_M J_H)",
        "status": "conditional_from_244",
        "gap": "the integrand is not theorem-zero",
    },
    {
        "step": 3,
        "claim": "Ward can conserve a mass current only after a time generator/current is specified.",
        "mathematical_step": "nabla_mu(T_H^{mu nu}xi_nu)=T_H^{mu nu}nabla_(mu xi_nu)+xi_nu nabla_mu T_H^{mu nu}",
        "status": "conditional_GR_style_route",
        "gap": "xi/stationarity and separate Hilbert conservation are not parent-derived",
    },
    {
        "step": 4,
        "claim": "Total Ward conservation still allows exchange with hidden sectors.",
        "mathematical_step": "nabla T_H = -F_X-F_P-F_B-F_D-F_nm + retained terms",
        "status": "blocks_overclaim",
        "gap": "must prove zero Pi_M projection of every exchange owner",
    },
    {
        "step": 5,
        "claim": "Topology can close a current only if the mass current itself is the topological object.",
        "mathematical_step": "dJ_M^top=0 and J_M^top=Pi_M J_H on shell",
        "status": "promising_future_route",
        "gap": "current corpus has topological projector templates, not a topological mass current identity",
    },
    {
        "step": 6,
        "claim": "A multiplier equation is sufficient but not explanatory unless independently owned.",
        "mathematical_step": "delta_lambdaM S=0 => d(Pi_M J_H)=0",
        "status": "closure_only_without_origin",
        "gap": "no independent lambda_M origin supplied",
    },
    {
        "step": 7,
        "claim": "Therefore flux closure remains a sharp parent-action target or retained residual.",
        "mathematical_step": "FC0-FC8 fail/open => dM_eff and radial-hair rows active",
        "status": "no_promotion",
        "gap": "measured GM/Newton/local GR remain unpromoted",
    },
]


CONTRACT = [
    {
        "contract_id": "FC0_same_frame_Hilbert_mass_current",
        "required_identity": "the mass-channel current is the same-frame Hilbert/Ward matter source projected by Pi_M before readout",
        "mathematical_form": "J_M=Pi_M J_H[e_obs]",
        "closes_component": "readout/fitted mass-current ambiguity",
        "affected_rows": "R0;R1;R4;R9;R11",
        "current_status": "conditional_from_source_current_contract",
        "evidence_needed": "same observed coframe, Hilbert source definition, and parent-defined Pi_M",
        "fallback_if_missing": "source current remains fitted/calibration-only",
    },
    {
        "contract_id": "FC1_stationary_or_Hamiltonian_time_generator",
        "required_identity": "the compact local branch supplies an observed stationary time/Hamiltonian generator for mass conservation",
        "mathematical_form": "j_M^mu=T_H^{mu nu}xi_nu with L_xi g_obs=0 or Hamiltonian boundary charge H_xi",
        "closes_component": "stress conservation to mass-current conservation bridge",
        "affected_rows": "R4;R9;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "stationary/asymptotic local branch or Hamiltonian charge theorem",
        "fallback_if_missing": "Ward conservation cannot be counted as d(Pi_M J_H)=0",
    },
    {
        "contract_id": "FC2_closed_mass_current_equation",
        "required_identity": "the parent action derives d(Pi_M J_H)=0 from Ward, topology, or Euler identity",
        "mathematical_form": "dJ_M=0 where J_M=Pi_M J_H",
        "closes_component": "M_eff radial/time drift",
        "affected_rows": "R4;R7;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "Ward_M, topological mass current, or independently owned E_lambdaM equation",
        "fallback_if_missing": "dln_Meff_dt and partial_r ln mu_obs remain active",
    },
    {
        "contract_id": "FC3_no_exchange_projection",
        "required_identity": "hidden, projector, domain, boundary, nonmetric, coupling, and memory exchange currents have zero Pi_M projection",
        "mathematical_form": "Pi_M(F_X+F_P+F_B+F_D+F_nm+T d kappa)=0",
        "closes_component": "mu_extra entering the mass channel",
        "affected_rows": "R0;R1;R3;R4;R7;R8;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "K_owner formula, q_retained zero proof, constant coupling, and no-hair/exchange theorem",
        "fallback_if_missing": "P8_boundary_bulk_domain_mu_extra and Gdot/range rows remain active",
    },
    {
        "contract_id": "FC4_zero_compact_boundary_mass_flux",
        "required_identity": "owned divergence terms carry no compact-boundary mass flux except universal constant calibration",
        "mathematical_form": "int_boundary Pi_M K_owner=0 or constant_global with partial_{t,r,A,lambda}=0",
        "closes_component": "boundary/improvement monopole shift",
        "affected_rows": "R3;R4;R7;R8;R9;R11",
        "current_status": "fail_open",
        "evidence_needed": "class-only/topological boundary no-flux theorem",
        "fallback_if_missing": "boundary/exchange coefficient vector blocks Newton claim",
    },
    {
        "contract_id": "FC5_topological_mass_current_origin",
        "required_identity": "if using topology, the topological object is the absolute mass current itself and equals Pi_M J_H on shell",
        "mathematical_form": "dJ_M^top=0 and J_M^top=Pi_M J_H",
        "closes_component": "non-ad-hoc closure of mass channel",
        "affected_rows": "R4;R7;R9;R11",
        "current_status": "promising_future_route_not_in_corpus",
        "evidence_needed": "BF/closed-form mass-current parent sector with no local stress/source-charge leakage",
        "fallback_if_missing": "topological projector templates cannot close the absolute mass flux",
    },
    {
        "contract_id": "FC6_no_ad_hoc_lambdaM",
        "required_identity": "lambda_M closure multiplier has independent gauge, topological, Ward, or source-normalization reason",
        "mathematical_form": "S_M=int lambda_M d(Pi_M J_H) legal only if lambda_M is parent-owned",
        "closes_component": "fake Euler derivation",
        "affected_rows": "R1;R4;R9;R11",
        "current_status": "not_satisfied",
        "evidence_needed": "independent origin and variation ledger for lambda_M",
        "fallback_if_missing": "closure counted as explicit assumption only",
    },
    {
        "contract_id": "FC7_absolute_calibration_after_closure",
        "required_identity": "the closed mass current is calibrated to the measured orbital/asymptotic monopole",
        "mathematical_form": "M_eff=(4 pi G_ref)^-1 int_S2 J_M and mu_obs=G_eff M_eff",
        "closes_component": "conserved but misnormalized mass charge",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "EH/Poisson/asymptotic/orbital matching plus constant universal G_eff",
        "fallback_if_missing": "d(Pi_M J_H)=0 is not yet measured Newtonian GM",
    },
    {
        "contract_id": "FC8_retained_residual_fallback",
        "required_identity": "any nonzero or unproved mass-channel flux is converted into executable residual data",
        "mathematical_form": "d(Pi_M J_H) -> dln_Meff_dt, partial_r ln mu_obs, mu_extra/(GM), alpha(lambda)",
        "closes_component": "nothing; preserves falsifiability",
        "affected_rows": "R1;R3;R4;R7;R8;R9;R10;R11",
        "current_status": "template_policy_only",
        "evidence_needed": "coefficient/curve, units, normalization, source path, and local-bound mapping",
        "fallback_if_missing": "no measured-GM/Newton/PPN/local-GR claim",
    },
]


COUNTEREXAMPLES = [
    {
        "counterexample": "total_Ward_conservation_only",
        "construction": "nabla_mu T_tot^{mu nu}=0 while observed matter exchanges mass-channel flux with hidden sectors",
        "why_it_fails": "total conservation does not imply d(Pi_M J_H)=0",
        "required_repair": "separate mass-current Ward identity or zero Pi_M projection of exchange",
        "affected_contracts": "FC2;FC3",
    },
    {
        "counterexample": "no_time_generator",
        "construction": "stress is conserved but no stationary/Killing/Hamiltonian time generator is supplied",
        "why_it_fails": "there is no distinguished mass current j_M^mu=T^{mu nu}xi_nu",
        "required_repair": "stationary local branch or Hamiltonian boundary charge theorem",
        "affected_contracts": "FC1;FC2",
    },
    {
        "counterexample": "topological_projector_not_mass_current",
        "construction": "P_mem/P_D is topological for relative memory, but the absolute Pi_M mass current is not shown closed",
        "why_it_fails": "relative topological silence does not close the ordinary mass flux",
        "required_repair": "topological mass current J_M^top equal to Pi_M J_H",
        "affected_contracts": "FC5",
    },
    {
        "counterexample": "lambdaM_magic_wand",
        "construction": "append lambda_M d(Pi_M J_H) only after identifying source-normalization failure",
        "why_it_fails": "the equation is imposed rather than derived",
        "required_repair": "independent gauge/topological/Ward origin for lambda_M",
        "affected_contracts": "FC6",
    },
    {
        "counterexample": "boundary_improvement_flux",
        "construction": "T_H is locally conserved but T_H -> T_H+dB shifts the compact surface monopole",
        "why_it_fails": "the annulus flux is a boundary term, exactly the retained channel",
        "required_repair": "zero compact-boundary mass flux or universal constant calibration theorem",
        "affected_contracts": "FC3;FC4",
    },
    {
        "counterexample": "projector_variation_mass_leak",
        "construction": "Pi_M changes with metric/domain/source split and (delta Pi_M)J_H is dropped",
        "why_it_fails": "projector variation becomes hidden source-normalization stress",
        "required_repair": "topological Pi_M or variation-owned projector stress ledger",
        "affected_contracts": "FC2;FC3",
    },
    {
        "counterexample": "closed_but_not_calibrated",
        "construction": "d(Pi_M J_H)=0 but M_eff normalization differs from orbital/asymptotic measured GM",
        "why_it_fails": "Newton measures mu_obs, not an arbitrary conserved cohomology charge",
        "required_repair": "absolute calibration plus constant universal G_eff",
        "affected_contracts": "FC7",
    },
]


GATE_TESTS = [
    {
        "gate": "conditional_mass_flux_closure_written",
        "pass_condition": "Ward/Killing, Hamiltonian, topological, and Euler closure routes are explicitly distinguished",
        "current_result": "pass_conditional",
        "evidence": "closure routes R0-R5 recorded",
    },
    {
        "gate": "Ward_not_overclaimed",
        "pass_condition": "total Ward conservation is not treated as d(Pi_M J_H)=0",
        "current_result": "pass",
        "evidence": "Ward_limit and total_Ward_conservation_only counterexample",
    },
    {
        "gate": "topological_projector_not_confused_with_mass_closure",
        "pass_condition": "relative P_mem topology does not automatically close absolute Pi_M mass flux",
        "current_result": "pass",
        "evidence": "FC5 and counterexample recorded",
    },
    {
        "gate": "ad_hoc_lambdaM_blocked",
        "pass_condition": "lambda_M closure is not accepted without independent parent origin",
        "current_result": "pass",
        "evidence": "FC6 written",
    },
    {
        "gate": "mass_flux_closure_parent_derived",
        "pass_condition": "current corpus derives d(Pi_M J_H)=0 from Ward, topological, or owned Euler route",
        "current_result": "fail",
        "evidence": "FC2 remains not_parent_derived",
    },
    {
        "gate": "zero_exchange_projection_derived",
        "pass_condition": "all hidden/boundary/projector/coupling exchange currents have zero Pi_M projection",
        "current_result": "fail",
        "evidence": "FC3-FC4 remain not_parent_derived/fail_open",
    },
    {
        "gate": "measured_GM_parent_derived",
        "pass_condition": "closed mass current is absolutely calibrated with constant universal G_eff and zero residuals",
        "current_result": "fail",
        "evidence": "FC7 remains not_parent_derived",
    },
    {
        "gate": "Newton_or_local_GR_promoted",
        "pass_condition": "P8 source-normalization and PPN rows are theorem-zero or empirically scored",
        "current_result": "fail",
        "evidence": "flux-closure theorem attempt only",
    },
]


THEOREM_STATUS = [
    {
        "claim": "exact mass-flux closure routes written",
        "status": "pass_conditional",
        "evidence": "Ward/Killing, Hamiltonian, topological, owner-projection, Euler, and retained routes distinguished",
    },
    {
        "claim": "Stokes/M_eff implication preserved",
        "status": "pass_conditional",
        "evidence": "if d(Pi_M J_H)=0 then M_eff(r2)=M_eff(r1)",
    },
    {
        "claim": "Ward/Bianchi overclaim blocked",
        "status": "pass",
        "evidence": "total conservation separated from mass-channel conservation",
    },
    {
        "claim": "topological route sharpened",
        "status": "pass_conditional",
        "evidence": "topology must close absolute J_M, not merely relative P_mem",
    },
    {
        "claim": "d(Pi_M J_H)=0 parent-derived",
        "status": "fail",
        "evidence": "no completed Ward_M, Hamiltonian, topological mass-current, or owned lambda_M proof",
    },
    {
        "claim": "mass-channel exchange flux theorem-zero",
        "status": "fail",
        "evidence": "boundary, hidden, projector, coupling, and range rows remain open",
    },
    {
        "claim": "measured GM/Newton/local GR promoted",
        "status": "fail",
        "evidence": "absolute calibration, constant G_eff, zero mu_extra, and second-order source stability remain open",
    },
]


DECISION = [
    {
        "decision": "The flux-closure problem is now exact. The best non-cheating routes are: a Ward/Killing or Hamiltonian mass current in a stationary same-frame local branch, a topological closed mass current equal on shell to Pi_M J_H, or an independently owned source-normalization Euler equation. None is currently parent-derived in the corpus. Ward conservation alone is not enough, and the topological P_mem route does not automatically close the absolute mass flux. Therefore d(Pi_M J_H)=0 remains a sharp theorem target; until it is derived, dM_eff, radial source hair, mu_extra, Gdot/source/range residuals remain active and no measured-GM, Newton, PPN, or local-GR promotion is allowed.",
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "456-PiM-projector-variation-stress-ledger.md",
        "why_next": "even the algebraic/topological Pi_M route must own delta Pi_M and boundary metric/projector stress before claiming local closure",
    },
    {
        "rank": 2,
        "target": "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
        "why_next": "the cleanest GR-like derivation of a conserved mass channel is likely a Hamiltonian/asymptotic charge route",
    },
    {
        "rank": 3,
        "target": "map FC0-FC8 into P8 residual evaluator",
        "why_next": "failed closure conditions should activate dM_eff, radial hair, mu_extra, Gdot, and range/source residual rows automatically",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"Cannot write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    csv_fieldnames = fieldnames or list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=csv_fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    table_fieldnames = fieldnames or list(rows[0].keys())
    lines = [
        "| " + " | ".join(table_fieldnames) + " |",
        "| " + " | ".join(["---"] * len(table_fieldnames)) + " |",
    ]
    for item in rows:
        values = []
        for fieldname in table_fieldnames:
            value = str(item.get(fieldname, ""))
            value = value.replace("|", "/")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_source_register() -> list[dict[str, Any]]:
    source_register = []
    for source_doc in SOURCE_DOCS:
        source_path = ROOT / source_doc["path"]
        source_register.append(
            {
                "source_file": source_doc["path"],
                "exists": source_path.exists(),
                "role": source_doc["role"],
            }
        )
    return source_register


def build_gate_results(source_register: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [source_row["source_file"] for source_row in source_register if not source_row["exists"]]
    gate_results = [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": "all cited source paths exist" if not missing_sources else "; ".join(missing_sources),
        },
        {
            "gate": "contract_schema_matches",
            "status": "pass" if list(CONTRACT[0].keys()) == CONTRACT_COLUMNS else "fail",
            "evidence": "Pi_M flux closure contract columns match schema",
        },
        {
            "gate": "theorem_statement_written",
            "status": "pass" if len(THEOREM_STATEMENT) == 6 else "fail",
            "evidence": f"{len(THEOREM_STATEMENT)} theorem rows",
        },
        {
            "gate": "closure_routes_written",
            "status": "pass" if len(CLOSURE_ROUTES) == 6 else "fail",
            "evidence": f"{len(CLOSURE_ROUTES)} closure routes",
        },
        {
            "gate": "mass_channel_decomposition_written",
            "status": "pass" if len(MASS_CHANNEL_DECOMPOSITION) == 6 else "fail",
            "evidence": f"{len(MASS_CHANNEL_DECOMPOSITION)} mass-channel terms",
        },
        {
            "gate": "derivation_steps_written",
            "status": "pass" if len(DERIVATION_STEPS) == 7 else "fail",
            "evidence": f"{len(DERIVATION_STEPS)} derivation steps",
        },
        {
            "gate": "contract_written",
            "status": "pass" if len(CONTRACT) == 9 else "fail",
            "evidence": str(CONTRACT_PATH),
        },
        {
            "gate": "Ward_not_overclaimed",
            "status": "pass",
            "evidence": "total conservation is not treated as d(Pi_M J_H)=0",
        },
        {
            "gate": "topological_projector_not_confused_with_mass_closure",
            "status": "pass",
            "evidence": "relative P_mem topology separated from absolute Pi_M mass-current closure",
        },
        {
            "gate": "ad_hoc_lambdaM_blocked",
            "status": "pass",
            "evidence": "FC6 requires independent lambda_M origin",
        },
        {
            "gate": "mass_flux_closure_parent_derived",
            "status": "fail",
            "evidence": "no completed Ward_M/Hamiltonian/topological/Euler closure proof",
        },
        {
            "gate": "zero_exchange_projection_derived",
            "status": "fail",
            "evidence": "FC3-FC4 remain open/fail_open",
        },
        {
            "gate": "topological_mass_current_parent_derived",
            "status": "fail",
            "evidence": "FC5 is promising_future_route_not_in_corpus",
        },
        {
            "gate": "absolute_calibration_parent_derived",
            "status": "fail",
            "evidence": "FC7 remains not_parent_derived",
        },
        {
            "gate": "measured_GM_parent_derived",
            "status": "fail",
            "evidence": "closure, exchange, calibration, and constant coupling remain open",
        },
        {
            "gate": "Newtonian_reduction_promoted",
            "status": "fail",
            "evidence": "Pi_M flux closure attempt only",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "P8 and PPN source-normalization rows remain retained",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]
    return gate_results


def render_doc(run_dir: Path, source_register: list[dict[str, Any]], gate_results: list[dict[str, str]]) -> str:
    return f"""# 455 - PiM Flux Closure Ward or Topological Current Attempt

Private P8/R1/R4/R7/R9/R10/R11 mass-flux closure checkpoint. This is not a public WEP, Einstein-Hilbert, measured-GM, Newtonian-limit, PPN, fifth-force, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 454 made `Pi_M` algebraically sharp: `Pi_M J=ell_M(J) omega_M` can preserve the mass class.

This checkpoint asks the harder question: can the parent theory derive the differential equation `d(Pi_M J_H)=0`, or is the Newton mass source still an explicit closure/residual branch?

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/PiM_flux_closure_Ward_or_topological_current_attempt.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Contract | `{CONTRACT_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_register)}

## 4. Theorem Statement

{markdown_table(THEOREM_STATEMENT)}

## 5. Closure Routes

{markdown_table(CLOSURE_ROUTES)}

## 6. Mass-Channel Decomposition

{markdown_table(MASS_CHANNEL_DECOMPOSITION)}

## 7. Derivation Steps

{markdown_table(DERIVATION_STEPS)}

## 8. PiM Flux Closure Contract

The Pi_M flux closure Ward/topological contract has been written to `{CONTRACT_PATH}`.

{markdown_table(CONTRACT, CONTRACT_COLUMNS)}

## 9. Counterexamples

{markdown_table(COUNTEREXAMPLES)}

## 10. Gate Tests

{markdown_table(GATE_TESTS)}

## 11. Theorem Status

{markdown_table(THEOREM_STATUS)}

## 12. Gate Results

{markdown_table(gate_results)}

## 13. Decision

{DECISION[0]["decision"]}

Practical read: the route is alive but the punch has to land in the right place. Ward conservation is not enough unless it becomes a conserved mass-channel current. Topology is not enough unless it closes the absolute mass current, not just the relative memory projector. The next engineering brick is projector variation stress, because even a beautiful `Pi_M` can leak through `delta Pi_M` if the parent does not own it.

## 14. Next Queue

{markdown_table(NEXT_QUEUE)}
"""


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_register = build_source_register()
    gate_results = build_gate_results(source_register)
    missing_sources = [source_row["source_file"] for source_row in source_register if not source_row["exists"]]

    write_csv(results_dir / "source_register.csv", source_register)
    write_csv(results_dir / "theorem_statement.csv", THEOREM_STATEMENT)
    write_csv(results_dir / "closure_routes.csv", CLOSURE_ROUTES)
    write_csv(results_dir / "mass_channel_decomposition.csv", MASS_CHANNEL_DECOMPOSITION)
    write_csv(results_dir / "derivation_steps.csv", DERIVATION_STEPS)
    write_csv(results_dir / "PiM_flux_closure_contract.csv", CONTRACT, CONTRACT_COLUMNS)
    write_csv(results_dir / "counterexamples.csv", COUNTEREXAMPLES)
    write_csv(results_dir / "gate_tests.csv", GATE_TESTS)
    write_csv(results_dir / "theorem_status.csv", THEOREM_STATUS)
    write_csv(results_dir / "gate_results.csv", gate_results)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)
    write_csv(ROOT / CONTRACT_PATH, CONTRACT, CONTRACT_COLUMNS)

    doc_text = render_doc(run_dir, source_register, gate_results)
    (ROOT / CHECKPOINT_DOC).write_text(doc_text, encoding="utf-8")

    status_payload = {
        "timestamp": timestamp,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": CHECKPOINT_DOC,
        "run_dir": str(run_dir.relative_to(ROOT)),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "conditional_mass_flux_closure_written": True,
        "Ward_not_overclaimed": True,
        "topological_projector_not_confused_with_mass_closure": True,
        "ad_hoc_lambdaM_blocked": True,
        "mass_flux_closure_parent_derived": False,
        "zero_exchange_projection_derived": False,
        "topological_mass_current_parent_derived": False,
        "absolute_calibration_parent_derived": False,
        "measured_GM_parent_derived": False,
        "Newtonian_reduction_promoted": False,
        "local_GR_claim_allowed": False,
        "counterexamples": len(COUNTEREXAMPLES),
        "contract_rows": len(CONTRACT),
        "failed_gates": [gate_row["gate"] for gate_row in gate_results if gate_row["status"] == "fail"],
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status_payload, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        f"{STATUS}\n{datetime.now(timezone.utc).isoformat()}\n",
        encoding="utf-8",
    )
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Write the MTS Pi_M flux closure Ward/topological current attempt.")
    parser.add_argument(
        "--timestamp",
        default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix, e.g. 20260602-171500.",
    )
    parsed_args = parser.parse_args()
    run_dir = write_run(parsed_args.timestamp)
    status_payload = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()
