from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "Hamiltonian-charge-to-Poisson-Gauss-calibration-gate"
CHECKPOINT_DOC = "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md"
STATUS = "Hamiltonian_charge_to_Poisson_Gauss_calibration_gate_written_exact_measured_GM_bridge_conditions_not_parent_derived_residual_rows_retained_no_Newton_or_local_GR_pass"
CLAIM_CEILING = "Poisson_Gauss_calibration_gate_only_no_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "459-PG-calibration-residual-mapper.md"
CONTRACT_PATH = Path("source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv")


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
        "path": "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
        "role": "immediate Hamiltonian boundary-charge checkpoint and HC8 next target",
    },
    {
        "path": "source-intake/mts_residuals/P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "role": "HC0-HC9 Hamiltonian charge premises feeding this calibration gate",
    },
    {
        "path": "424-same-frame-EH-source-Poisson-reduction-gate.md",
        "role": "same-frame EH-to-Poisson algebra and no-promotion policy",
    },
    {
        "path": "402-EH-source-normalization-parent-pair.md",
        "role": "weak-field chain G_eff=kappa_eff c^4/(8 pi) and mu_obs decomposition",
    },
    {
        "path": "450-Hilbert-source-to-measured-monopole-calibration-gate.md",
        "role": "Hilbert current to measured orbital monopole blocker",
    },
    {
        "path": "source-intake/mts_residuals/P8_Hilbert_monopole_calibration_CONTRACT.csv",
        "role": "HM rows for mass projector, absolute calibration, zero mu_extra, and derivative silence",
    },
    {
        "path": "451-mass-flux-projector-Euler-calibration-attempt.md",
        "role": "mass-flux projector Euler closure and no-ad-hoc multiplier warning",
    },
    {
        "path": "source-intake/mts_residuals/P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
        "role": "MF rows for Pi_M closure and absolute calibration",
    },
    {
        "path": "452-constant-universal-Geff-kappa-identity-attempt.md",
        "role": "constant universal coupling route and retained drift/source/range rows",
    },
    {
        "path": "source-intake/mts_residuals/P8_constant_universal_Geff_kappa_CONTRACT.csv",
        "role": "CU rows for G_eff/kappa derivative silence",
    },
    {
        "path": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "role": "GM absorption theorem attempt and constant-monopole policy",
    },
    {
        "path": "244-Meff-monopole-source-normalization-or-radial-memory-hair.md",
        "role": "conditional closed Pi_M flux implies radially conserved M_eff",
    },
    {
        "path": "439-EH-only-exterior-parent-premise-ladder.md",
        "role": "EH-only parent-premise ladder controlling Poisson validity",
    },
    {
        "path": "230-exterior-vacuum-Einstein-branch-or-Jrel-representative.md",
        "role": "ordinary mass flux separated from local relative memory exchange",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv",
        "role": "P8 measured-GM residual fallback rows",
    },
    {
        "path": "runs/20260602-084000-same-frame-EH-source-Poisson-reduction-gate/results/Poisson_chain.csv",
        "role": "machine EH-to-Poisson chain",
    },
    {
        "path": "runs/20260602-143000-source-normalization-residual-vector-refinement/results/mu_obs_decomposition.csv",
        "role": "machine mu_obs decomposition into drift, source charge, flux, range, radial, and frame channels",
    },
    {
        "path": "runs/20260602-160000-Hilbert-source-to-measured-monopole-calibration-gate/results/calibration_chain.csv",
        "role": "machine Hilbert-to-measured-monopole calibration chain",
    },
]


THEOREM_STATEMENT = [
    {
        "part": "conditional_Poisson_Gauss_calibration_theorem",
        "statement": "If the Hamiltonian boundary charge is already well-defined, same-frame, EH-only, and equal to the projected Hilbert mass current, and if the weak-field equation reduces to Poisson with constant universal G_eff and zero residual source channels, then the charge is calibrated to measured orbital GM.",
        "mathematical_form": "B_xi = G_eff M_H; nabla^2 Phi = 4 pi G_eff rho_H; surface_integral grad Phi dot dS = 4 pi G_eff M_H; a = -grad Phi",
        "status": "valid_conditional_measured_GM_bridge",
    },
    {
        "part": "Gauss_law_algebra",
        "statement": "The Gauss bridge is exact only when the Poisson source has no residual terms. Any source_residual or mu_extra term becomes a real measured-GM correction, not a harmless relabel.",
        "mathematical_form": "nabla^2 Phi = 4 pi G_eff rho_H + S_res; M_Gauss = (4 pi G_eff)^-1 surface_integral grad Phi dot dS = M_H + (4 pi G_eff)^-1 integral S_res dV",
        "status": "exact_residual_exposure",
    },
    {
        "part": "orbital_readout_condition",
        "statement": "Orbital GM is the coefficient of the inverse-square acceleration in the observed matter frame. The Hamiltonian/Gauss charge equals it only when the potential is pure monopole plus allowed constant calibration, with no finite-range, radial, frame, or species charge.",
        "mathematical_form": "a_r = -partial_r Phi = -mu_obs/r^2; mu_obs = G_eff M_Gauss iff Phi = -G_eff M_Gauss/r + constant",
        "status": "measured_readout_gate",
    },
    {
        "part": "constant_offset_policy",
        "statement": "A global constant normalization can be absorbed into measured G after all derivatives and source labels vanish. Time, radial, range, species, frame, or domain dependence is physics and must be derived zero or retained.",
        "mathematical_form": "delta_mu/mu = constant_global allowed; partial_t,r,A,lambda,frame delta_mu = 0 required",
        "status": "calibration_policy_not_parent_normalization",
    },
    {
        "part": "first_order_limit",
        "statement": "Poisson/Gauss calibration is a Newtonian source gate, not a full local-GR gate. Gamma, beta, preferred-frame, Gdot, and fifth-force rows remain active until the same branch passes PPN order.",
        "mathematical_form": "Poisson pass does not imply gamma=1, beta=1, alpha_i=0, xi_PPN=0, Gdot=0",
        "status": "blocks_local_GR_overclaim",
    },
    {
        "part": "current_corpus_status",
        "statement": "The algebraic bridge is clean, but the current corpus has not parent-derived charge equality to Pi_M J_H, zero mu_extra/source_residuals, constant universal G_eff, pure inverse-square readout, or second-order PPN source stability.",
        "mathematical_form": "PG0-PG10 remain contract rows; no measured-GM/Newton/PPN/local-GR promotion",
        "status": "not_parent_derived",
    },
]


CALIBRATION_CHAIN = [
    {
        "step": 1,
        "stage": "Hamiltonian_boundary_charge",
        "mathematical_form": "H_xi = B_xi on shell",
        "needed_for": "conserved candidate source charge",
        "current_status": "conditional_from_457_not_parent_derived",
    },
    {
        "step": 2,
        "stage": "charge_to_projected_Hilbert_mass",
        "mathematical_form": "B_xi/G_eff = M_eff[Pi_M J_H]",
        "needed_for": "same mass source as the parent matter current",
        "current_status": "not_parent_derived",
    },
    {
        "step": 3,
        "stage": "same_frame_weak_field_metric",
        "mathematical_form": "g_00 = -1 + 2 Phi/c^2 + O(c^-4)",
        "needed_for": "observed matter acceleration reads the same Phi",
        "current_status": "conditional_not_parent_derived",
    },
    {
        "step": 4,
        "stage": "Poisson_coefficient",
        "mathematical_form": "nabla^2 Phi = (kappa_eff c^4/2) rho_H = 4 pi G_eff rho_H",
        "needed_for": "G_eff identification",
        "current_status": "algebra_pass_if_424_premises_hold",
    },
    {
        "step": 5,
        "stage": "Gauss_surface_integral",
        "mathematical_form": "surface_integral grad Phi dot dS = 4 pi G_eff M_H",
        "needed_for": "surface charge equals enclosed source",
        "current_status": "conditional_if_source_residuals_zero",
    },
    {
        "step": 6,
        "stage": "orbital_inverse_square_readout",
        "mathematical_form": "a_r = -G_eff M_H/r^2",
        "needed_for": "measured mu_obs = G_eff M_H",
        "current_status": "conditional_if_no_extra_force",
    },
    {
        "step": 7,
        "stage": "derivative_silence",
        "mathematical_form": "partial_t,r,A,lambda mu_obs = 0",
        "needed_for": "no Gdot, source-charge, radial, or fifth-force row",
        "current_status": "not_parent_derived",
    },
    {
        "step": 8,
        "stage": "PPN_source_stability",
        "mathematical_form": "delta_beta_source=0 after the same measured-GM normalization",
        "needed_for": "local-GR/source completion",
        "current_status": "not_derived",
    },
]


FAILURE_CHANNELS = [
    {
        "channel": "charge_normalization_factor",
        "symbolic_form": "B_xi = zeta G_eff M rather than G_eff M",
        "why_dangerous": "a conserved charge can have wrong factors, subtraction, or units",
        "residual_rows": "R4;R9;R11",
        "required_repair": "route-specific ADM/Komar/Noether/Brown-York normalization matched to Poisson",
    },
    {
        "channel": "source_residual_volume_term",
        "symbolic_form": "nabla^2 Phi = 4 pi G_eff rho + S_res",
        "why_dangerous": "Gauss mass picks up integral S_res over the exterior/source region",
        "residual_rows": "R3;R4;R7;R8;R9;R10;R11",
        "required_repair": "derive S_res=0 or map it into P8/R11 residuals",
    },
    {
        "channel": "boundary_reference_shift",
        "symbolic_form": "B_xi -> B_xi + B_ref + B_hair",
        "why_dangerous": "boundary subtraction or hair can shift measured monopole",
        "residual_rows": "R3;R4;R7;R8;R9;R11",
        "required_repair": "class-only reference and zero boundary hair theorem",
    },
    {
        "channel": "variable_Geff",
        "symbolic_form": "G_eff=G_eff(t,r,A,lambda,frame)",
        "why_dangerous": "the same conserved mass charge gives drifting or source-dependent GM",
        "residual_rows": "R1;R4;R9;R10;R11",
        "required_repair": "constant universal coupling/superselection theorem",
    },
    {
        "channel": "finite_range_or_radial_hair",
        "symbolic_form": "Phi=-GM/r(1+alpha exp(-r/lambda)) or partial_r mu_obs != 0",
        "why_dangerous": "the orbital coefficient is not a pure enclosed monopole",
        "residual_rows": "R3;R4;R10;R11",
        "required_repair": "alpha(lambda)=0 theorem or executable fifth-force curve below bounds",
    },
    {
        "channel": "frame_or_species_split",
        "symbolic_form": "mu_obs[A,frame] != G_eff M_H",
        "why_dangerous": "matter or source composition reads a different charge than the metric equation",
        "residual_rows": "R0;R1;R2;R11",
        "required_repair": "same observed frame plus source-current universality",
    },
    {
        "channel": "Poisson_only_second_order_failure",
        "symbolic_form": "nabla^2 Phi passes but beta/gamma/source nonlinear piece fails",
        "why_dangerous": "Newtonian source success is not local GR",
        "residual_rows": "R3;R4;R11",
        "required_repair": "second-order PPN source/operator calculation",
    },
]


CONTRACT = [
    {
        "contract_id": "PG0_Hamiltonian_charge_input",
        "required_identity": "the boundary charge B_xi is already well-defined, conserved, and generated by observed time",
        "mathematical_form": "H_xi=B_xi on shell with xi normalized in the observed frame",
        "closes_component": "candidate mass charge existence",
        "affected_rows": "R2;R4;R5;R6;R8;R9;R11",
        "current_status": "conditional_from_457_not_parent_derived",
        "evidence_needed": "HC0-HC3 parent proof or retained charge residuals",
        "fallback_if_missing": "no Poisson/Gauss calibration can be claimed",
    },
    {
        "contract_id": "PG1_charge_equals_projected_Hilbert_source",
        "required_identity": "the Hamiltonian charge equals the parent-defined projected Hilbert mass current",
        "mathematical_form": "B_xi/G_eff = M_eff[Pi_M J_H] and delta B_xi = delta integral_S Pi_M J_H",
        "closes_component": "charge/current split",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "HC4 plus HM/MF source-current calibration and Pi_M variation ownership",
        "fallback_if_missing": "conserved charge is not measured source mass",
    },
    {
        "contract_id": "PG2_same_frame_weak_field_potential",
        "required_identity": "the potential used by matter orbits is the same weak-field potential sourced by the local metric equation",
        "mathematical_form": "g_00=-1+2 Phi/c^2 and a=-grad Phi in the observed matter frame",
        "closes_component": "frame/readout split",
        "affected_rows": "R0;R1;R2;R11",
        "current_status": "conditional_not_parent_derived",
        "evidence_needed": "same-frame matter/metric/coframe theorem",
        "fallback_if_missing": "P8 frame calibration split row remains active",
    },
    {
        "contract_id": "PG3_EH_to_Poisson_coefficient",
        "required_identity": "the same-frame weak-field 00 equation reduces to Poisson with the standard coefficient",
        "mathematical_form": "nabla^2 Phi = (kappa_eff c^4/2) rho_H = 4 pi G_eff rho_H",
        "closes_component": "operator/source coefficient",
        "affected_rows": "R3;R4;R8;R10;R11",
        "current_status": "conditional_from_424",
        "evidence_needed": "EH-only operator selection, nonrelativistic source limit, and no source_residuals",
        "fallback_if_missing": "R11 operator/source residual vector remains active",
    },
    {
        "contract_id": "PG4_Gauss_surface_integral",
        "required_identity": "the Poisson source integrates to the same surface charge over enclosing spheres",
        "mathematical_form": "surface_integral grad Phi dot dS = 4 pi G_eff M_eff with no residual volume/boundary term",
        "closes_component": "absolute monopole surface calibration",
        "affected_rows": "R3;R4;R7;R8;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "closed Pi_M flux, zero boundary/source residuals, and absolute normalization",
        "fallback_if_missing": "P8 radial/source/boundary hair rows remain active",
    },
    {
        "contract_id": "PG5_orbital_inverse_square_readout",
        "required_identity": "test bodies read the Gauss monopole as a pure inverse-square acceleration",
        "mathematical_form": "a_r=-partial_r Phi=-G_eff M_eff/r^2 and v^2 r = G_eff M_eff",
        "closes_component": "measured orbital GM",
        "affected_rows": "R1;R2;R4;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "slow-particle geodesic limit plus no fifth-force, source charge, or radial hair",
        "fallback_if_missing": "orbital GM is a retained empirical readout, not a derived charge",
    },
    {
        "contract_id": "PG6_zero_mu_extra_and_source_residuals",
        "required_identity": "boundary, bulk, domain, projector, memory, range, connection, and non-Hilbert source pieces add no unowned monopole",
        "mathematical_form": "mu_obs=G_eff M_eff + mu_extra with mu_extra=0, and S_res=0",
        "closes_component": "hidden measured-GM correction",
        "affected_rows": "R3;R4;R7;R8;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "Ward/no-hair/topological zero theorem or executable coefficient map",
        "fallback_if_missing": "P8_boundary_bulk_domain_mu_extra remains active",
    },
    {
        "contract_id": "PG7_constant_universal_Geff",
        "required_identity": "G_eff/kappa_eff is constant, universal, source-blind, range-blind, and frame-blind",
        "mathematical_form": "partial_t,r,A,lambda,frame G_eff = 0",
        "closes_component": "Gdot/source/range calibration drift",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_status": "conditional_not_parent_derived",
        "evidence_needed": "CU1-CU7 global-coupling/superselection theorem",
        "fallback_if_missing": "Gdot/source/fifth-force rows remain retained",
    },
    {
        "contract_id": "PG8_no_derivative_hair",
        "required_identity": "the measured source strength has no time, radial, species, range, frame, or domain derivative",
        "mathematical_form": "partial_t mu_obs=partial_r mu_obs=partial_A mu_obs=partial_lambda mu_obs=partial_frame mu_obs=0",
        "closes_component": "measured-GM stability",
        "affected_rows": "R0;R1;R2;R4;R8;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "constant coupling, source universality, radial no-hair, and same-frame calibration",
        "fallback_if_missing": "row-specific P8 residuals remain active",
    },
    {
        "contract_id": "PG9_second_order_source_stability",
        "required_identity": "the same calibration survives beta/gamma/PPN order",
        "mathematical_form": "delta_beta_source=0 and gamma-1=0 after measured-GM normalization",
        "closes_component": "Poisson-only false local-GR pass",
        "affected_rows": "R3;R4;R11",
        "current_status": "not_derived",
        "evidence_needed": "second-order weak-field source/operator calculation in the observed frame",
        "fallback_if_missing": "Newtonian source calibration cannot be promoted to local GR",
    },
    {
        "contract_id": "PG10_retained_residual_fallback",
        "required_identity": "any failed calibration premise becomes executable residual data",
        "mathematical_form": "PG failure -> dln_Geff_dt, dln_Meff_dt, eta_source, alpha(lambda), partial_r ln mu_obs, mu_extra/(GM), delta_beta_source",
        "closes_component": "claim leakage",
        "affected_rows": "R1;R3;R4;R7;R8;R9;R10;R11",
        "current_status": "template_policy_only",
        "evidence_needed": "map PG0-PG9 failures into P8/R11 residual evaluator",
        "fallback_if_missing": "manual no-promotion discipline remains required",
    },
]


COUNTEREXAMPLES = [
    {
        "counterexample": "right_charge_wrong_Phi",
        "construction": "B_xi is conserved, but the matter-frame weak-field potential is sourced by a different coframe or operator",
        "why_it_fails": "orbits do not measure that charge",
        "required_repair": "PG2 same-frame potential theorem",
        "affected_contracts": "PG1;PG2",
    },
    {
        "counterexample": "Poisson_with_residual_source",
        "construction": "nabla^2 Phi = 4 pi G rho + S_res",
        "why_it_fails": "Gauss mass includes the residual volume integral",
        "required_repair": "S_res=0 theorem or retained source residual map",
        "affected_contracts": "PG3;PG4;PG6",
    },
    {
        "counterexample": "boundary_subtraction_hair",
        "construction": "Brown-York/Noether boundary energy has a reference or hair term that shifts B_xi",
        "why_it_fails": "the surface charge is not the enclosed matter monopole",
        "required_repair": "boundary class-only/no-hair theorem",
        "affected_contracts": "PG0;PG4;PG6",
    },
    {
        "counterexample": "Yukawa_or_running_G_fit",
        "construction": "Phi=-GM/r(1+alpha exp(-r/lambda)) or G_eff=G_eff(r,lambda)",
        "why_it_fails": "orbital GM becomes range-dependent",
        "required_repair": "alpha(lambda)=0 theorem or executable R10 curve below bounds",
        "affected_contracts": "PG5;PG7;PG8",
    },
    {
        "counterexample": "species_source_charge",
        "construction": "different source compositions carry different mu_obs despite the same geometric charge",
        "why_it_fails": "measured GM is composition/source-charge dependent",
        "required_repair": "source-current universality and species-blind G_eff",
        "affected_contracts": "PG6;PG7;PG8",
    },
    {
        "counterexample": "constant_offset_called_prediction",
        "construction": "a global constant rescaling of G_eff M_eff is advertised as a predicted G value",
        "why_it_fails": "constant calibration is not a prediction without parent normalization of units/coupling",
        "required_repair": "absolute coupling normalization theorem or no prediction claim",
        "affected_contracts": "PG7;PG8",
    },
    {
        "counterexample": "Poisson_pass_beta_fail",
        "construction": "first-order Poisson/Gauss calibration works, but second-order beta or gamma differs",
        "why_it_fails": "Newtonian source success is not local GR",
        "required_repair": "PPN source/operator completion",
        "affected_contracts": "PG9;PG10",
    },
]


GATE_TESTS = [
    {
        "gate": "conditional_Poisson_Gauss_bridge_written",
        "pass_condition": "Hamiltonian charge, Poisson coefficient, Gauss integral, and orbital readout are linked with conditions",
        "current_result": "pass_conditional",
        "evidence": "theorem statement and calibration chain recorded",
    },
    {
        "gate": "source_residuals_exposed",
        "pass_condition": "nonzero source residuals are shown to enter Gauss mass, not disappear",
        "current_result": "pass",
        "evidence": "Gauss_law_algebra and PG6",
    },
    {
        "gate": "constant_offset_policy_written",
        "pass_condition": "constant calibration is separated from derivative/source/range physics",
        "current_result": "pass",
        "evidence": "constant_offset_policy and PG7-PG8",
    },
    {
        "gate": "Poisson_not_overclaimed_as_local_GR",
        "pass_condition": "first-order calibration does not promote gamma/beta/PPN rows",
        "current_result": "pass",
        "evidence": "first_order_limit and PG9",
    },
    {
        "gate": "charge_to_PiM_Hilbert_mass_derived",
        "pass_condition": "B_xi/G_eff equals M_eff[Pi_M J_H]",
        "current_result": "fail",
        "evidence": "PG1 remains not_parent_derived",
    },
    {
        "gate": "Gauss_orbital_calibration_parent_derived",
        "pass_condition": "surface integral equals orbital GM with no residual channels",
        "current_result": "fail",
        "evidence": "PG4-PG6 remain not_parent_derived",
    },
    {
        "gate": "constant_Geff_derivative_silence_derived",
        "pass_condition": "G_eff and mu_obs have no time/source/range/radial/frame derivatives",
        "current_result": "fail",
        "evidence": "PG7-PG8 remain conditional/not parent-derived",
    },
    {
        "gate": "Newton_or_local_GR_promoted",
        "pass_condition": "measured-GM, P8, and PPN source rows are theorem-zero or scored",
        "current_result": "fail",
        "evidence": "Poisson/Gauss calibration gate only",
    },
]


THEOREM_STATUS = [
    {
        "claim": "Poisson/Gauss measured-GM bridge written",
        "status": "pass_conditional",
        "evidence": "chain from B_xi to Phi to Gauss mass to orbital readout is explicit",
    },
    {
        "claim": "source residual overclaim blocked",
        "status": "pass",
        "evidence": "S_res contributes directly to M_Gauss",
    },
    {
        "claim": "constant calibration policy written",
        "status": "pass",
        "evidence": "global constant offset separated from derivative/source/range dependence",
    },
    {
        "claim": "Hamiltonian charge calibrated to Pi_M Hilbert mass",
        "status": "fail",
        "evidence": "PG1 remains not parent-derived",
    },
    {
        "claim": "measured orbital GM parent-derived",
        "status": "fail",
        "evidence": "PG4-PG8 remain open",
    },
    {
        "claim": "Newton/PPN/local GR promoted",
        "status": "fail",
        "evidence": "PG9/P8/PPN residuals remain active",
    },
]


DECISION = [
    {
        "decision": "The Poisson/Gauss calibration bridge is now exact as a conditional theorem. If the Hamiltonian boundary charge equals the projected Hilbert mass current, the same-frame weak-field equation is EH/Poisson with constant universal G_eff, all source_residual and mu_extra channels vanish, and the potential read by matter is a pure inverse-square monopole, then the conserved charge is measured orbital GM. The current corpus has not derived those premises. Therefore the bridge is clean but not promoted; failed PG rows must become P8/R11 residuals rather than hidden calibration.",
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "459-PG-calibration-residual-mapper.md",
        "why_next": "failed PG0-PG10 rows should directly activate P8/R11 measured-GM, Gdot, fifth-force, and source-normalization residuals",
    },
    {
        "rank": 2,
        "target": "source-normalized Newton branch theorem stack",
        "why_next": "if the residual mapper has theorem-zero inputs, assemble the finite Newton reduction proof stack without overclaiming local GR",
    },
    {
        "rank": 3,
        "target": "second-order PPN source stability attempt",
        "why_next": "Poisson/Gauss is first order; beta/gamma still need the same measured-GM normalization at second order",
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
            "evidence": "Poisson/Gauss calibration contract columns match schema",
        },
        {
            "gate": "theorem_statement_written",
            "status": "pass" if len(THEOREM_STATEMENT) == 6 else "fail",
            "evidence": f"{len(THEOREM_STATEMENT)} theorem rows",
        },
        {
            "gate": "calibration_chain_written",
            "status": "pass" if len(CALIBRATION_CHAIN) == 8 else "fail",
            "evidence": f"{len(CALIBRATION_CHAIN)} calibration stages",
        },
        {
            "gate": "failure_channels_written",
            "status": "pass" if len(FAILURE_CHANNELS) == 7 else "fail",
            "evidence": f"{len(FAILURE_CHANNELS)} failure channels",
        },
        {
            "gate": "contract_written",
            "status": "pass" if len(CONTRACT) == 11 else "fail",
            "evidence": str(CONTRACT_PATH),
        },
        {
            "gate": "source_residuals_exposed",
            "status": "pass",
            "evidence": "Gauss mass includes residual volume term if S_res is nonzero",
        },
        {
            "gate": "constant_offset_policy_written",
            "status": "pass",
            "evidence": "constant-only calibration separated from derivative/source/range physics",
        },
        {
            "gate": "Poisson_not_overclaimed_as_local_GR",
            "status": "pass",
            "evidence": "PG9 keeps second-order PPN rows active",
        },
        {
            "gate": "charge_to_PiM_Hilbert_mass_derived",
            "status": "fail",
            "evidence": "PG1 remains not_parent_derived",
        },
        {
            "gate": "Gauss_orbital_calibration_parent_derived",
            "status": "fail",
            "evidence": "PG4-PG6 remain not_parent_derived",
        },
        {
            "gate": "constant_Geff_derivative_silence_derived",
            "status": "fail",
            "evidence": "PG7-PG8 remain conditional/not parent-derived",
        },
        {
            "gate": "PPN_source_stability_derived",
            "status": "fail",
            "evidence": "PG9 remains not_derived",
        },
        {
            "gate": "measured_GM_parent_derived",
            "status": "fail",
            "evidence": "PG1 and PG4-PG8 are not closed",
        },
        {
            "gate": "Newtonian_reduction_promoted",
            "status": "fail",
            "evidence": "Poisson/Gauss calibration gate only",
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


def render_doc(run_dir: Path, source_register: list[dict[str, Any]], gate_results: list[dict[str, str]]) -> str:
    return f"""# 458 - Hamiltonian Charge to Poisson/Gauss Calibration Gate

Private P8/R1/R3/R4/R7/R8/R9/R10/R11 measured-GM calibration checkpoint. This is not a public WEP, Einstein-Hilbert, measured-GM, Newtonian-limit, PPN, fifth-force, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 457 found the clean GR-like route: mass should be a Hamiltonian/asymptotic/quasilocal boundary charge, not a magic flux closure.

This checkpoint asks the next, stricter question: when does that conserved charge become the `GM` measured by Poisson/Gauss law and orbital acceleration?

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/Hamiltonian_charge_to_Poisson_Gauss_calibration_gate.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Contract | `{CONTRACT_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_register)}

## 4. Theorem Statement

{markdown_table(THEOREM_STATEMENT)}

## 5. Calibration Chain

{markdown_table(CALIBRATION_CHAIN)}

## 6. Failure Channels

{markdown_table(FAILURE_CHANNELS)}

## 7. Poisson/Gauss Calibration Contract

The Poisson/Gauss calibration contract has been written to `{CONTRACT_PATH}`.

{markdown_table(CONTRACT, CONTRACT_COLUMNS)}

## 8. Counterexamples

{markdown_table(COUNTEREXAMPLES)}

## 9. Gate Tests

{markdown_table(GATE_TESTS)}

## 10. Theorem Status

{markdown_table(THEOREM_STATUS)}

## 11. Gate Results

{markdown_table(gate_results)}

## 12. Decision

{DECISION[0]["decision"]}

Practical read: this is where the theory stops being allowed to say "mass" loosely. A Hamiltonian charge, a Gauss flux, and orbital `GM` can be the same object, but only if the same-frame EH/Poisson/source-normalization bills are paid. If any residual survives, it goes on the scorecard as `mu_extra`, `Gdot`, source charge, radial hair, or fifth-force. No pocketing the eight ball.

## 13. Next Queue

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
    write_csv(results_dir / "calibration_chain.csv", CALIBRATION_CHAIN)
    write_csv(results_dir / "failure_channels.csv", FAILURE_CHANNELS)
    write_csv(results_dir / "Poisson_Gauss_calibration_contract.csv", CONTRACT, CONTRACT_COLUMNS)
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
        "conditional_Poisson_Gauss_bridge_written": True,
        "source_residuals_exposed": True,
        "constant_offset_policy_written": True,
        "Poisson_not_overclaimed_as_local_GR": True,
        "charge_to_PiM_Hilbert_mass_derived": False,
        "Gauss_orbital_calibration_parent_derived": False,
        "constant_Geff_derivative_silence_derived": False,
        "PPN_source_stability_derived": False,
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
    parser = argparse.ArgumentParser(description="Write the MTS Hamiltonian charge to Poisson/Gauss calibration gate.")
    parser.add_argument(
        "--timestamp",
        default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix, e.g. 20260602-181500.",
    )
    parsed_args = parser.parse_args()
    run_dir = write_run(parsed_args.timestamp)
    status_payload = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()
