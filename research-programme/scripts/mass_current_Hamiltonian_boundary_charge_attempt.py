from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "mass-current-Hamiltonian-boundary-charge-attempt"
CHECKPOINT_DOC = "457-mass-current-Hamiltonian-boundary-charge-attempt.md"
STATUS = "mass_current_Hamiltonian_boundary_charge_attempt_written_conditional_GR_like_charge_route_downstream_of_EH_boundary_calibration_not_parent_derived_no_Newton_or_local_GR_pass"
CLAIM_CEILING = "Hamiltonian_boundary_charge_attempt_only_no_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md"
CONTRACT_PATH = Path("source-intake/mts_residuals/P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv")


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
        "path": "456-PiM-projector-variation-stress-ledger.md",
        "role": "immediate projector-variation stress gate feeding the Hamiltonian charge route",
    },
    {
        "path": "455-PiM-flux-closure-Ward-or-topological-current-attempt.md",
        "role": "mass-flux closure route table and Hamiltonian/asymptotic charge candidate",
    },
    {
        "path": "454-PiM-parent-symplectic-projector-algebra-attempt.md",
        "role": "Pi_M algebra and mass-channel projector identity",
    },
    {
        "path": "source-intake/mts_residuals/P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
        "role": "FC rows requiring mass-current closure and calibration",
    },
    {
        "path": "source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv",
        "role": "PV rows requiring projector variation ownership before charge promotion",
    },
    {
        "path": "450-Hilbert-source-to-measured-monopole-calibration-gate.md",
        "role": "Hilbert current to measured orbital monopole calibration blocker",
    },
    {
        "path": "source-intake/mts_residuals/P8_Hilbert_monopole_calibration_CONTRACT.csv",
        "role": "HM rows for absolute measured-GM calibration",
    },
    {
        "path": "452-constant-universal-Geff-kappa-identity-attempt.md",
        "role": "constant universal G_eff/kappa requirement",
    },
    {
        "path": "source-intake/mts_residuals/P8_constant_universal_Geff_kappa_CONTRACT.csv",
        "role": "CU rows for coupling constancy and no source/range drift",
    },
    {
        "path": "402-EH-source-normalization-parent-pair.md",
        "role": "same-frame EH/source weak-field chain",
    },
    {
        "path": "424-same-frame-EH-source-Poisson-reduction-gate.md",
        "role": "Poisson bridge and measured-GM requirements",
    },
    {
        "path": "439-EH-only-exterior-parent-premise-ladder.md",
        "role": "EH-only parent-premise ladder and Lovelock-style conditional route",
    },
    {
        "path": "247-local-EH-exterior-sufficiency-stack-no-promotion.md",
        "role": "conditional EH exterior sufficiency stack",
    },
    {
        "path": "230-exterior-vacuum-Einstein-branch-or-Jrel-representative.md",
        "role": "Schwarzschild exterior contract and ordinary mass vs J_rel separation",
    },
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "minimal parent action blocks including source normalization and boundary identities",
    },
    {
        "path": "375-EH-exterior-operator-or-residual-modified-gravity-ledger.md",
        "role": "EH operator or retained modified-gravity residual fork",
    },
    {
        "path": "244-Meff-monopole-source-normalization-or-radial-memory-hair.md",
        "role": "Stokes/Meff monopole source-normalization route",
    },
    {
        "path": "451-mass-flux-projector-Euler-calibration-attempt.md",
        "role": "mass-flux projector Euler/calibration warning",
    },
    {
        "path": "runs/20260602-084000-same-frame-EH-source-Poisson-reduction-gate/results/Poisson_chain.csv",
        "role": "machine weak-field EH-to-Poisson chain",
    },
    {
        "path": "runs/20260602-131500-EH-only-exterior-parent-premise-ladder/results/Lovelock_selection_contract.csv",
        "role": "machine EH-only Lovelock-style conditional selection contract",
    },
    {
        "path": "runs/20260602-160000-Hilbert-source-to-measured-monopole-calibration-gate/results/calibration_chain.csv",
        "role": "machine Hilbert current to measured-GM calibration chain",
    },
]


THEOREM_STATEMENT = [
    {
        "part": "conditional_Hamiltonian_boundary_charge_theorem",
        "statement": "If the local branch has a same-frame EH-only exterior, an observed stationary/asymptotic time generator xi, a differentiable integrable Hamiltonian H_xi, vanishing bulk constraints, no extra sector charge, constant universal coupling, and Poisson/Gauss/orbital calibration, then the conserved Hamiltonian boundary charge can be identified with M_eff and the Pi_M mass channel is closed.",
        "mathematical_form": "H_xi = integral_Sigma (xi_perp C_perp + xi^i C_i) + B_xi; C=0 and dH_xi/dt=0; B_xi = G_eff M_eff after calibration; d(Pi_M J_H)=0",
        "status": "valid_conditional_GR_like_route",
    },
    {
        "part": "boundary_charge_not_automatic_mass",
        "statement": "A conserved Hamiltonian charge is not automatically the measured Newtonian monopole. It may include boundary, projector, non-EH, memory, domain, or coupling pieces unless the parent action proves those pieces absent, harmless, or separately retained.",
        "mathematical_form": "H_xi = H_Hilbert_mass + H_boundary + H_projector + H_nonEH + H_domain + H_delta_kappa",
        "status": "blocks_overclaim",
    },
    {
        "part": "constraints_to_surface_charge_route",
        "statement": "In a GR-like Hamiltonian formulation, the bulk constraints vanish on shell and the physical generator is the boundary term. This is the cleanest route to mass conservation, but it is downstream of deriving the EH constraint algebra and boundary conditions.",
        "mathematical_form": "delta H_xi = delta integral_Sigma C_xi + delta B_xi; on shell C_xi=0, so delta H_xi=delta B_xi",
        "status": "conditional_downstream_of_EH",
    },
    {
        "part": "ADM_Komar_Noether_dictionary",
        "statement": "ADM, Komar, Brown-York, and covariant Noether/Iyer-Wald charges can all play the mass role only in their proper regimes: asymptotically flat, stationary Killing, quasilocal boundary with subtraction, or integrable exact-symmetry phase space.",
        "mathematical_form": "M_ADM, M_Komar[xi], E_BY[S], Q_xi^IW are equal only after field equations, boundary conditions, and normalization are matched",
        "status": "route_dictionary_not_independent_proof",
    },
    {
        "part": "Poisson_Gauss_bridge",
        "statement": "The weak-field measured-GM bridge is a Gauss-law calibration: the surface charge must reduce to the same coefficient that sources nabla^2 Phi=4 pi G rho and orbital acceleration. Without this, the charge is conserved but misnormalised.",
        "mathematical_form": "M_Gauss = (4 pi G_eff)^-1 surface_integral grad Phi dot dS; mu_obs=G_eff M_Gauss",
        "status": "next_calibration_gate",
    },
    {
        "part": "current_corpus_status",
        "statement": "The corpus has the conditional EH/Poisson/monopole ingredients, but it has not parent-derived EH-only exterior constraints, Hamiltonian boundary integrability, charge equality to Pi_M J_H, no extra charge, or measured-GM calibration.",
        "mathematical_form": "HC0-HC9 remain contract rows; no measured-GM/Newton/PPN/local-GR promotion",
        "status": "not_parent_derived",
    },
]


CHARGE_ROUTES = [
    {
        "route_id": "R0_Hamiltonian_constraint_boundary_charge",
        "mechanism": "derive mass from the differentiable Hamiltonian generator of observed time translations",
        "mathematical_form": "H[xi]=integral_Sigma C_xi + B_xi; C_xi=0 on shell; dH[xi]/dt=0 for symmetry xi",
        "would_close": "constant surface mass charge if B_xi equals Pi_M Hilbert mass",
        "required_extra_premise": "same-frame EH constraint algebra, integrable boundary term, and exact symmetry",
        "current_status": "conditional_downstream_of_EH_gate",
    },
    {
        "route_id": "R1_ADM_asymptotic_mass",
        "mechanism": "use asymptotically flat spatial infinity to define the conserved mass",
        "mathematical_form": "M_ADM proportional to surface_integral (partial_j h_ij - partial_i h_jj) dS_i",
        "would_close": "global asymptotic mass for isolated systems",
        "required_extra_premise": "asymptotic flatness/falloff, same observed metric, and no non-EH asymptotic charge",
        "current_status": "conditional_not_compact_or_parent_derived",
    },
    {
        "route_id": "R2_Komar_stationary_mass",
        "mechanism": "use a stationary Killing vector to convert geometry into a surface mass charge",
        "mathematical_form": "M_Komar proportional to surface_integral nabla^mu xi^nu dS_munu",
        "would_close": "stationary mass in an EH branch after correct normalization/stress terms",
        "required_extra_premise": "Killing xi, EH equations, stress/factor normalization, and stationary local branch",
        "current_status": "conditional_not_parent_derived",
    },
    {
        "route_id": "R3_covariant_Noether_Iyer_Wald_charge",
        "mechanism": "use diffeomorphism Noether charge in covariant phase space",
        "mathematical_form": "delta H_xi = integral_S (delta Q_xi - xi dot theta); exact symmetry and integrability give H_xi",
        "would_close": "charge conservation and variation matching if the phase-space one-form is integrable",
        "required_extra_premise": "parent Lagrangian, symplectic current, integrability, and no extra charge leakage",
        "current_status": "conditional_powerful_but_requires_parent_action",
    },
    {
        "route_id": "R4_Poisson_Gauss_orbital_bridge",
        "mechanism": "calibrate the boundary charge to the weak-field Gauss-law source measured by orbits",
        "mathematical_form": "surface_integral grad Phi dot dS = 4 pi G_eff M; a=-grad Phi",
        "would_close": "measured GM if G_eff is constant and no hidden charge exists",
        "required_extra_premise": "EH-to-Poisson reduction, constant G_eff, zero mu_extra, slow-particle geodesic limit",
        "current_status": "next_required_gate",
    },
    {
        "route_id": "R5_retained_modified_charge_branch",
        "mechanism": "keep the Hamiltonian charge but admit it contains non-EH/projector/boundary pieces",
        "mathematical_form": "H_xi = G_eff M_eff + sum_a c_a Q_a; c_a Q_a mapped to R3-R11 residuals",
        "would_close": "nothing; makes the branch testable rather than falsely GR",
        "required_extra_premise": "coefficient/profile map, units, local bounds, and source paths",
        "current_status": "fallback_if_R0_R4_fail",
    },
]


HAMILTONIAN_REQUIREMENTS = [
    {
        "requirement": "same_frame_EH_exterior",
        "mathematical_form": "E_ext^{mu nu}=a G^{mu nu}+b g^{mu nu} in the observed frame",
        "needed_for": "GR Hamiltonian constraint algebra and standard boundary charge",
        "current_status": "conditional_not_parent_derived",
    },
    {
        "requirement": "observed_time_generator",
        "mathematical_form": "xi is asymptotic time translation, stationary Killing field, or admissible quasilocal lapse/shift",
        "needed_for": "mass rather than arbitrary diffeomorphism charge",
        "current_status": "not_parent_derived",
    },
    {
        "requirement": "differentiable_integrable_Hxi",
        "mathematical_form": "delta H_xi has a finite boundary term B_xi and path-independent phase-space integral",
        "needed_for": "well-defined conserved charge",
        "current_status": "not_parent_derived",
    },
    {
        "requirement": "constraints_on_shell",
        "mathematical_form": "C_perp=0 and C_i=0 after hidden/projector/domain variables are varied or retained",
        "needed_for": "bulk generator reduces to boundary charge",
        "current_status": "not_parent_derived",
    },
    {
        "requirement": "no_extra_sector_charge",
        "mathematical_form": "Q_nonEH=Q_projector=Q_boundary_hair=Q_domain=Q_delta_kappa=0 or retained",
        "needed_for": "H_xi equals Hilbert mass rather than total hidden charge",
        "current_status": "fail_open",
    },
    {
        "requirement": "charge_equals_PiM_Hilbert_current",
        "mathematical_form": "delta B_xi = delta integral_S Pi_M J_H with Pi_M variation owned",
        "needed_for": "d(Pi_M J_H)=0 and M_eff closure",
        "current_status": "not_parent_derived",
    },
    {
        "requirement": "constant_universal_Geff",
        "mathematical_form": "G_eff=kappa_eff c^4/(8 pi); partial_t,r,A,lambda G_eff=0",
        "needed_for": "measured Newtonian source normalization",
        "current_status": "conditional_not_parent_derived",
    },
    {
        "requirement": "Poisson_Gauss_orbital_calibration",
        "mathematical_form": "M_charge=(4 pi G_eff)^-1 surface_integral grad Phi dot dS and mu_obs=G_eff M_charge",
        "needed_for": "orbital GM instead of arbitrary conserved charge",
        "current_status": "not_parent_derived",
    },
    {
        "requirement": "PPN_second_order_completion",
        "mathematical_form": "gamma=1, beta=1, alpha_i=0, xi_PPN=0, Gdot=0 after charge calibration",
        "needed_for": "local-GR claim rather than first-order Newton bridge",
        "current_status": "not_promoted",
    },
]


CHARGE_DICTIONARY = [
    {
        "charge": "ADM_mass",
        "regime": "asymptotically flat isolated exterior",
        "helps_with": "global mass conservation and weak-field normalization",
        "hidden_debt": "compact local systems and non-EH asymptotic charges are not automatically covered",
        "current_use": "conditional_calibration_template",
    },
    {
        "charge": "Komar_mass",
        "regime": "stationary spacetime with a normalized timelike Killing vector",
        "helps_with": "turns stationary geometry into a surface integral",
        "hidden_debt": "requires EH equations/factors and stationary generator",
        "current_use": "conditional_Killing_branch",
    },
    {
        "charge": "Brown_York_quasilocal_energy",
        "regime": "finite timelike boundary with reference subtraction",
        "helps_with": "compact boundary accounting",
        "hidden_debt": "reference choice/boundary stress can become source hair",
        "current_use": "retained_boundary_audit_route",
    },
    {
        "charge": "Iyer_Wald_Noether_charge",
        "regime": "covariant phase space for a parent Lagrangian and exact/asymptotic symmetry",
        "helps_with": "parent-action-compatible charge variation",
        "hidden_debt": "integrability and extra-sector symplectic terms must be owned",
        "current_use": "best_formal_future_route",
    },
    {
        "charge": "Poisson_Gauss_mass",
        "regime": "weak-field static Newtonian limit",
        "helps_with": "direct measured-GM/orbital bridge",
        "hidden_debt": "downstream of EH/source normalization and no fifth-force/radial hair",
        "current_use": "next_gate",
    },
]


DERIVATION_CHAIN = [
    {
        "step": 1,
        "claim": "Start with a Hamiltonian generator for an observed time flow.",
        "mathematical_step": "H_xi = integral_Sigma C_xi + B_xi",
        "status": "standard_conditional_form",
        "gap": "MTS parent has not derived the EH constraint algebra",
    },
    {
        "step": 2,
        "claim": "On shell, the bulk constraints vanish and the charge lives on the boundary.",
        "mathematical_step": "C_xi=0 => H_xi=B_xi",
        "status": "conditional_on_full_Euler_ownership",
        "gap": "hidden/projector/domain/source variables may leave nonzero constraints or charges",
    },
    {
        "step": 3,
        "claim": "A symmetry or boundary stationarity makes the charge conserved.",
        "mathematical_step": "dH_xi/dt={H_xi,H_xi}=0 or L_xi fields=0",
        "status": "conditional",
        "gap": "observed xi/stationary/asymptotic branch is not parent-derived",
    },
    {
        "step": 4,
        "claim": "To close the Pi_M current, the boundary variation must equal the projected Hilbert mass current.",
        "mathematical_step": "delta B_xi = delta integral_S Pi_M J_H",
        "status": "not_derived",
        "gap": "projector variation and source-current calibration remain open",
    },
    {
        "step": 5,
        "claim": "To make Newtonian GM, the conserved charge must reduce to Poisson/Gauss mass.",
        "mathematical_step": "B_xi = G_eff M_Gauss and surface_integral grad Phi = 4 pi G_eff M",
        "status": "next_gate",
        "gap": "absolute orbital calibration and constant G_eff remain unproved",
    },
    {
        "step": 6,
        "claim": "If any extra charge survives, the route is modified gravity/source-normalization, not local GR.",
        "mathematical_step": "H_xi = G_eff M + sum_a c_a Q_a",
        "status": "retained_fallback",
        "gap": "needs coefficient/profile mapping into R3-R11 local residuals",
    },
]


CONTRACT = [
    {
        "contract_id": "HC0_same_frame_EH_exterior",
        "required_identity": "the compact observed local exterior has the EH-only metric constraint algebra",
        "mathematical_form": "S_ext -> S_EH + boundary; C_perp=C_i=0 in the observed frame",
        "closes_component": "non-EH Hamiltonian generator ambiguity",
        "affected_rows": "R3;R4;R5;R6;R8;R10;R11",
        "current_status": "conditional_not_parent_derived",
        "evidence_needed": "P1-P7 EH-only parent-premise ladder or equivalent parent action proof",
        "fallback_if_missing": "R11 non-EH coefficient vector remains active",
    },
    {
        "contract_id": "HC1_observed_time_generator",
        "required_identity": "the mass charge is generated by an observed stationary/asymptotic time flow",
        "mathematical_form": "xi = partial_t at infinity or Killing/quasilocal admissible generator with fixed normalization",
        "closes_component": "arbitrary diffeomorphism charge/readout ambiguity",
        "affected_rows": "R2;R4;R5;R6;R8;R9;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "stationary local branch or asymptotic/quasilocal boundary theorem",
        "fallback_if_missing": "Hamiltonian charge cannot be identified as mass",
    },
    {
        "contract_id": "HC2_differentiable_integrable_Hxi",
        "required_identity": "the Hamiltonian has a finite integrable boundary term",
        "mathematical_form": "delta H_xi = finite delta B_xi and integral_phase_space delta B_xi is path independent",
        "closes_component": "ill-defined or reference-dependent boundary energy",
        "affected_rows": "R3;R4;R7;R8;R9;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "explicit parent symplectic current, boundary conditions, and reference/subtraction rule",
        "fallback_if_missing": "boundary charge is retained as calibration/reference ambiguity",
    },
    {
        "contract_id": "HC3_constraints_and_boundary_conditions",
        "required_identity": "all bulk constraints vanish after every hidden/source/projector/domain variable is varied or retained",
        "mathematical_form": "C_xi=0 including E_X, E_P, E_D, E_boundary, and source-normalization equations",
        "closes_component": "bulk-to-boundary reduction",
        "affected_rows": "R3;R4;R7;R8;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "complete parent Euler/Ward ledger with no unowned force channel",
        "fallback_if_missing": "H_xi includes retained bulk/exchange residuals",
    },
    {
        "contract_id": "HC4_charge_equals_PiM_Hilbert_mass",
        "required_identity": "the Hamiltonian surface charge equals the parent-defined projected Hilbert mass current",
        "mathematical_form": "B_xi/G_eff = M_eff[Pi_M J_H] and delta B_xi = delta integral_S Pi_M J_H",
        "closes_component": "d(Pi_M J_H)=0 and measured mass-source identity",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "source-current Ward identity, Pi_M variation ownership, and calibration theorem",
        "fallback_if_missing": "conserved charge is not the Hilbert/Newton source",
    },
    {
        "contract_id": "HC5_no_extra_hidden_charge",
        "required_identity": "non-EH, projector, boundary, domain, memory, range, and coupling sectors carry no unowned mass charge",
        "mathematical_form": "Q_nonEH+Q_PiM+Q_boundary+Q_domain+Q_memory+Q_range+Q_delta_kappa=0 or retained",
        "closes_component": "mu_extra and boundary/source hair",
        "affected_rows": "R1;R3;R4;R7;R8;R9;R10;R11",
        "current_status": "fail_open",
        "evidence_needed": "no-hair/topological/Ward-owned theorem or executable coefficient vector",
        "fallback_if_missing": "P8 mu_extra and R11/R10 residuals remain active",
    },
    {
        "contract_id": "HC6_projector_variation_boundary_safe",
        "required_identity": "Pi_M and boundary/projector terms are varied before readout and contribute no hidden stress or are retained",
        "mathematical_form": "delta(Pi_M J_H)=Pi_M delta J_H+(delta Pi_M)J_H with delta Pi_M theorem-zero or mapped",
        "closes_component": "projector stress leak inside the charge",
        "affected_rows": "R3;R4;R7;R8;R10;R11",
        "current_status": "conditional_from_456_not_parent_derived",
        "evidence_needed": "PV1/PV3 closure or PV6 retained coefficient/profile map",
        "fallback_if_missing": "Hamiltonian charge contains projector-domain stress",
    },
    {
        "contract_id": "HC7_constant_universal_Geff",
        "required_identity": "the charge normalization uses a constant universal G_eff/kappa_eff",
        "mathematical_form": "G_eff=kappa_eff c^4/(8 pi); partial_t,r,A,lambda G_eff=0",
        "closes_component": "Gdot/source/range normalization drift",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_status": "conditional_not_parent_derived",
        "evidence_needed": "global-coupling/superselection theorem or explicit retained residual bounds",
        "fallback_if_missing": "Hamiltonian mass is not stable measured GM",
    },
    {
        "contract_id": "HC8_Poisson_Gauss_orbital_calibration",
        "required_identity": "the surface charge reduces to the Poisson/Gauss source and orbital acceleration",
        "mathematical_form": "M=(4 pi G_eff)^-1 surface_integral grad Phi dot dS and a=-grad Phi",
        "closes_component": "absolute measured-GM calibration",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "weak-field EH/source reduction plus no hidden force/range/source hair",
        "fallback_if_missing": "conserved charge remains calibration-only",
    },
    {
        "contract_id": "HC9_retained_residual_fallback",
        "required_identity": "any failed charge premise emits executable residual terms rather than a local-GR claim",
        "mathematical_form": "delta H_xi residuals -> gamma,beta,alpha_i,xi,Gdot,alpha(lambda),mu_extra,dM_eff rows",
        "closes_component": "claim leakage",
        "affected_rows": "R1;R3;R4;R5;R6;R7;R8;R9;R10;R11",
        "current_status": "template_policy_only",
        "evidence_needed": "map HC0-HC8 failures into local residual evaluator",
        "fallback_if_missing": "manual no-promotion discipline remains required",
    },
]


COUNTEREXAMPLES = [
    {
        "counterexample": "conserved_total_charge_not_Hilbert_mass",
        "construction": "H_xi is conserved but includes hidden/projector/domain boundary charge",
        "why_it_fails": "Newton measures the matter-source monopole, not an arbitrary total charge split",
        "required_repair": "HC4 and HC5",
        "affected_contracts": "HC4;HC5",
    },
    {
        "counterexample": "no_stationary_or_asymptotic_time",
        "construction": "a compact branch has no normalized xi or no stationary/asymptotic time translation",
        "why_it_fails": "there is no unique mass Hamiltonian",
        "required_repair": "observed stationary/asymptotic/quasilocal generator theorem",
        "affected_contracts": "HC1;HC2",
    },
    {
        "counterexample": "Komar_factor_or_pressure_mismatch",
        "construction": "Komar-like charge is used where stress terms, factors, or stationarity assumptions differ",
        "why_it_fails": "the surface integral is not equal to orbital mass without field-equation calibration",
        "required_repair": "route-specific normalization and EH/source equation",
        "affected_contracts": "HC0;HC4;HC8",
    },
    {
        "counterexample": "ADM_exists_but_compact_boundary_not_calibrated",
        "construction": "an ADM mass exists at infinity but local compact boundary/orbital GM is shifted by boundary hair",
        "why_it_fails": "asymptotic charge does not automatically fix local measured source strength",
        "required_repair": "boundary no-hair and Poisson/Gauss calibration",
        "affected_contracts": "HC2;HC5;HC8",
    },
    {
        "counterexample": "nonEH_boundary_term_shifts_charge",
        "construction": "an f(R), Weyl, projector, or topological boundary term changes B_xi",
        "why_it_fails": "the charge is conserved but not pure EH/Hilbert mass",
        "required_repair": "EH-only theorem-zero or retained coefficient vector",
        "affected_contracts": "HC0;HC5;HC9",
    },
    {
        "counterexample": "variable_G_charge_normalization",
        "construction": "B_xi is constant while G_eff or kappa_eff drifts with time/range/source",
        "why_it_fails": "measured GM is not constant even if the geometric charge is",
        "required_repair": "constant universal coupling theorem",
        "affected_contracts": "HC7;HC8",
    },
    {
        "counterexample": "Poisson_first_order_only",
        "construction": "the charge matches first-order Poisson but gamma, beta, alpha_i, or xi_PPN remain non-GR",
        "why_it_fails": "Newtonian source calibration is not full local GR",
        "required_repair": "PPN second-order completion",
        "affected_contracts": "HC8;HC9",
    },
]


GATE_TESTS = [
    {
        "gate": "conditional_Hamiltonian_charge_route_written",
        "pass_condition": "Hamiltonian/ADM/Komar/Noether/Gauss routes are separated and status-labelled",
        "current_result": "pass_conditional",
        "evidence": "charge routes and dictionary recorded",
    },
    {
        "gate": "charge_not_overclaimed_as_measured_GM",
        "pass_condition": "conserved boundary charge is not treated as measured orbital monopole without calibration",
        "current_result": "pass",
        "evidence": "boundary_charge_not_automatic_mass theorem and counterexamples",
    },
    {
        "gate": "downstream_EH_dependency_visible",
        "pass_condition": "the Hamiltonian charge route explicitly depends on EH exterior and boundary conditions",
        "current_result": "pass",
        "evidence": "HC0-HC3",
    },
    {
        "gate": "Poisson_Gauss_next_gate_identified",
        "pass_condition": "absolute measured-GM bridge is identified as the next calibration gate",
        "current_result": "pass",
        "evidence": "HC8 and next target",
    },
    {
        "gate": "Hamiltonian_charge_parent_derived",
        "pass_condition": "the current corpus derives H_xi boundary charge and equality to Pi_M J_H",
        "current_result": "fail",
        "evidence": "HC0-HC4 remain conditional/not parent-derived",
    },
    {
        "gate": "extra_hidden_charge_zero_derived",
        "pass_condition": "all non-EH/projector/boundary/domain/coupling charge pieces vanish or are executable",
        "current_result": "fail",
        "evidence": "HC5-HC6 remain fail_open/conditional",
    },
    {
        "gate": "measured_GM_parent_derived",
        "pass_condition": "charge equals Poisson/Gauss/orbital mass with constant G_eff",
        "current_result": "fail",
        "evidence": "HC7-HC8 remain not parent-derived",
    },
    {
        "gate": "Newton_or_local_GR_promoted",
        "pass_condition": "P8 source normalization and PPN rows are all theorem-zero or scored",
        "current_result": "fail",
        "evidence": "Hamiltonian boundary-charge attempt only",
    },
]


THEOREM_STATUS = [
    {
        "claim": "conditional Hamiltonian boundary-charge route written",
        "status": "pass_conditional",
        "evidence": "Hamiltonian constraint, ADM, Komar, Noether, and Gauss routes distinguished",
    },
    {
        "claim": "mass-charge overclaim blocked",
        "status": "pass",
        "evidence": "conserved charge separated from Pi_M Hilbert mass and measured orbital GM",
    },
    {
        "claim": "GR-like route identified",
        "status": "pass_conditional",
        "evidence": "if EH exterior plus boundary integrability plus calibration hold, M_eff closure follows",
    },
    {
        "claim": "Hamiltonian charge parent-derived",
        "status": "fail",
        "evidence": "no completed parent EH constraint algebra or boundary symplectic theorem",
    },
    {
        "claim": "charge equals Pi_M Hilbert mass derived",
        "status": "fail",
        "evidence": "source-current calibration and projector variation remain open",
    },
    {
        "claim": "measured GM/Newton/local GR promoted",
        "status": "fail",
        "evidence": "constant G_eff, Poisson/Gauss calibration, extra-charge silence, and PPN completion remain open",
    },
]


DECISION = [
    {
        "decision": "The Hamiltonian boundary-charge route is the cleanest GR-like way to make the mass channel non-magical: if the parent action really lands on the same-frame EH constraint algebra and supplies an integrable observed-time boundary generator, then the mass can be a conserved surface charge rather than an inserted lambda_M closure. But in the current corpus this route is downstream, not derived. The boundary charge has not been proved equal to Pi_M J_H, extra non-EH/projector/domain/coupling charges are not theorem-zero, and the charge has not been calibrated to Poisson/Gauss/orbital GM. Therefore this is a strong next route, not a Newton/local-GR pass.",
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
        "why_next": "the Hamiltonian route only becomes measured GM when its surface charge reduces to the Poisson/Gauss/orbital monopole",
    },
    {
        "rank": 2,
        "target": "map HC0-HC9 into P8/R11 residual evaluator",
        "why_next": "failed Hamiltonian-charge premises should activate source-normalization, boundary, operator, Gdot, and fifth-force rows automatically",
    },
    {
        "rank": 3,
        "target": "parent covariant phase-space charge skeleton",
        "why_next": "the Iyer-Wald style route can keep the future parent action and symplectic boundary terms honest",
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
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": "all cited source paths exist" if not missing_sources else "; ".join(missing_sources),
        },
        {
            "gate": "contract_schema_matches",
            "status": "pass" if list(CONTRACT[0].keys()) == CONTRACT_COLUMNS else "fail",
            "evidence": "Hamiltonian boundary-charge contract columns match schema",
        },
        {
            "gate": "theorem_statement_written",
            "status": "pass" if len(THEOREM_STATEMENT) == 6 else "fail",
            "evidence": f"{len(THEOREM_STATEMENT)} theorem rows",
        },
        {
            "gate": "charge_routes_written",
            "status": "pass" if len(CHARGE_ROUTES) == 6 else "fail",
            "evidence": f"{len(CHARGE_ROUTES)} charge routes",
        },
        {
            "gate": "Hamiltonian_requirements_written",
            "status": "pass" if len(HAMILTONIAN_REQUIREMENTS) == 9 else "fail",
            "evidence": f"{len(HAMILTONIAN_REQUIREMENTS)} requirements",
        },
        {
            "gate": "charge_dictionary_written",
            "status": "pass" if len(CHARGE_DICTIONARY) == 5 else "fail",
            "evidence": f"{len(CHARGE_DICTIONARY)} charge dictionary entries",
        },
        {
            "gate": "derivation_chain_written",
            "status": "pass" if len(DERIVATION_CHAIN) == 6 else "fail",
            "evidence": f"{len(DERIVATION_CHAIN)} derivation steps",
        },
        {
            "gate": "contract_written",
            "status": "pass" if len(CONTRACT) == 10 else "fail",
            "evidence": str(CONTRACT_PATH),
        },
        {
            "gate": "charge_not_overclaimed_as_measured_GM",
            "status": "pass",
            "evidence": "conserved boundary charge is separated from measured orbital monopole",
        },
        {
            "gate": "downstream_EH_dependency_visible",
            "status": "pass",
            "evidence": "HC0-HC3 make EH exterior and boundary conditions explicit",
        },
        {
            "gate": "Hamiltonian_charge_parent_derived",
            "status": "fail",
            "evidence": "no completed parent EH constraint algebra or boundary charge theorem",
        },
        {
            "gate": "charge_equals_PiM_Hilbert_mass_derived",
            "status": "fail",
            "evidence": "HC4 remains not_parent_derived",
        },
        {
            "gate": "extra_hidden_charge_zero_derived",
            "status": "fail",
            "evidence": "HC5 remains fail_open",
        },
        {
            "gate": "constant_Geff_and_Gauss_calibration_derived",
            "status": "fail",
            "evidence": "HC7-HC8 remain not_parent_derived",
        },
        {
            "gate": "Newtonian_reduction_promoted",
            "status": "fail",
            "evidence": "Hamiltonian charge attempt only",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "PPN and P8 rows remain retained",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def render_doc(run_dir: Path, source_register: list[dict[str, Any]], gate_results: list[dict[str, str]]) -> str:
    return f"""# 457 - Mass Current Hamiltonian Boundary Charge Attempt

Private P8/R1/R3/R4/R7/R8/R9/R10/R11 Hamiltonian-charge checkpoint. This is not a public WEP, Einstein-Hilbert, measured-GM, Newtonian-limit, PPN, fifth-force, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 456 made projector variation stress explicit. This checkpoint asks whether the mass-channel closure can be earned the GR way: as a conserved Hamiltonian/asymptotic/quasilocal boundary charge, rather than by inserting `d(Pi_M J_H)=0` as a closure axiom.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/mass_current_Hamiltonian_boundary_charge_attempt.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Contract | `{CONTRACT_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_register)}

## 4. Theorem Statement

{markdown_table(THEOREM_STATEMENT)}

## 5. Charge Routes

{markdown_table(CHARGE_ROUTES)}

## 6. Hamiltonian Requirements

{markdown_table(HAMILTONIAN_REQUIREMENTS)}

## 7. Charge Dictionary

{markdown_table(CHARGE_DICTIONARY)}

## 8. Derivation Chain

{markdown_table(DERIVATION_CHAIN)}

## 9. Hamiltonian Boundary-Charge Contract

The Hamiltonian boundary-charge contract has been written to `{CONTRACT_PATH}`.

{markdown_table(CONTRACT, CONTRACT_COLUMNS)}

## 10. Counterexamples

{markdown_table(COUNTEREXAMPLES)}

## 11. Gate Tests

{markdown_table(GATE_TESTS)}

## 12. Theorem Status

{markdown_table(THEOREM_STATUS)}

## 13. Gate Results

{markdown_table(gate_results)}

## 14. Decision

{DECISION[0]["decision"]}

Practical read: this is the Mayweather route, not the haymaker. If MTS can stand in the ring with GR locally, the neatest way is to make mass a real surface charge of the local EH-like branch. But the belt is not awarded for naming ADM/Komar/Hamiltonian charges; the charge still has to be the same charge that appears in `Pi_M J_H`, Poisson/Gauss, and orbital `GM`, with no hidden sector sneaking onto the scorecard.

## 15. Next Queue

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
    write_csv(results_dir / "charge_routes.csv", CHARGE_ROUTES)
    write_csv(results_dir / "Hamiltonian_requirements.csv", HAMILTONIAN_REQUIREMENTS)
    write_csv(results_dir / "charge_dictionary.csv", CHARGE_DICTIONARY)
    write_csv(results_dir / "derivation_chain.csv", DERIVATION_CHAIN)
    write_csv(results_dir / "Hamiltonian_boundary_charge_contract.csv", CONTRACT, CONTRACT_COLUMNS)
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
        "conditional_Hamiltonian_charge_route_written": True,
        "charge_not_overclaimed_as_measured_GM": True,
        "downstream_EH_dependency_visible": True,
        "Poisson_Gauss_next_gate_identified": True,
        "Hamiltonian_charge_parent_derived": False,
        "charge_equals_PiM_Hilbert_mass_derived": False,
        "extra_hidden_charge_zero_derived": False,
        "constant_Geff_and_Gauss_calibration_derived": False,
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
    parser = argparse.ArgumentParser(description="Write the MTS mass-current Hamiltonian boundary-charge attempt.")
    parser.add_argument(
        "--timestamp",
        default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix, e.g. 20260602-174500.",
    )
    parsed_args = parser.parse_args()
    run_dir = write_run(parsed_args.timestamp)
    status_payload = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()
