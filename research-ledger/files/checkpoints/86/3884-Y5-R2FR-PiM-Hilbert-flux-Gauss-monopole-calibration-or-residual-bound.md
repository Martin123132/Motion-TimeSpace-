# 3884 - PiM Hilbert Flux and Gauss Monopole Calibration

Generated: `2026-07-01T07:43:35+00:00`

## Result

3884 turns the 3883 same Hilbert source into a first-order Newton candidate:

`Let J_M := Pi_M J_H[tau]. Then dJ_M = (dPi_M)J_H + Pi_M dJ_H. If Pi_M is parent-fixed/covariantly constant, T_H is conserved, tau is Killing or stationary in the local collar, and boundary/radiative fluxes vanish, then d(Pi_M J_H)=0.`

Then:

`From nabla^2 Phi=4*pi*G0*rho_H, integration over a compact source volume gives oint grad Phi.n dA = 4*pi*G0 M_H, where M_H=int rho_H dV = int Pi_M J_H.`

and:

`In the source-free exterior, Phi=-G0 M_H/r + multipoles + residuals; slow test bodies obey a^i=-partial^i Phi, so the monopole gives v^2 r=G0 M_H when range, radial, frame and non-EH residuals vanish.`

So the candidate branch now has the right logical ladder: Hilbert stress -> closed projected mass -> Gauss monopole -> inverse-square orbital readout. It remains nonclaim because parent PiM ownership, boundary/reference silence, extra charge, and second-order PPN/R11 stability are still live gates.

## PiM Hilbert Flux Closure

| flux_id | piece | statement | status | effect |
| --- | --- | --- | --- | --- |
| PFC3884_0_definition | projected mass current | J_M := Pi_M J_H[tau] | DEFINITION_FROM_3883_SOURCE | uses the same Hilbert source before orbital readout |
| PFC3884_1_product_rule | flux identity | Let J_M := Pi_M J_H[tau]. Then dJ_M = (dPi_M)J_H + Pi_M dJ_H. If Pi_M is parent-fixed/covariantly constant, T_H is conserved, tau is Killing or stationary in the local collar, and boundary/radiative fluxes vanish, then d(Pi_M J_H)=0. | EXACT_CONDITIONAL_THEOREM | turns Meff drift/radial hair into explicit failed-premise terms |
| PFC3884_2_stationary_zero | stationary collar zero | If tau is Killing, ell_J fixed, Pi_M covariantly constant, and net boundary/radiative flux vanishes, then d_t M_eff=0 and partial_r M_eff=0 between linked surfaces. | CANDIDATE_FLUX_ZERO | closes time/radial source drift in the candidate branch |
| PFC3884_3_em_flux | EM flux exception | Nonzero Phi_EM_rad changes M_eff by the Poynting energy flux and must stay in the residual vector. | RETAIN_IF_NONZERO | keeps EM flow honest rather than double-counted |
| PFC3884_4_limits | limits | Pi_M parent ownership, projector stress silence, reference terms, domain motion, and non-EH extra charge are not globally signed. | OPEN_RESIDUAL_GUARD | no Newton/local-GR claim yet |

## Gauss Monopole Calibration

| gauss_id | piece | statement | status | effect |
| --- | --- | --- | --- | --- |
| GMC3884_0_Poisson | Poisson source | nabla^2 Phi=4*pi*G0*rho_H from 3882/3883 | INPUT_LOCKED_IN_CANDIDATE | source density is Hilbert density |
| GMC3884_1_Gauss | Gauss theorem | From nabla^2 Phi=4*pi*G0*rho_H, integration over a compact source volume gives oint grad Phi.n dA = 4*pi*G0 M_H, where M_H=int rho_H dV = int Pi_M J_H. | EXACT_CONDITIONAL_GAUSS_BRIDGE | converts source density into a surface monopole |
| GMC3884_2_surface_independence | surface independence | If d(Pi_M J_H)=0 in the exterior annulus, M_H[S2]=M_H[S1] for linked surfaces around the same worldtube. | CANDIDATE_SURFACE_INDEPENDENCE | kills radial source hair from mass-flux drift |
| GMC3884_3_multipoles | multipole guard | Non-spherical compact sources add multipoles but not a different monopole; multipoles are readout/PPN corrections, not GM calibration freedom. | MONOPOLE_ONLY_GUARD | prevents hiding source normalization in shape terms |
| GMC3884_4_residual | if failed | Delta_Gauss = M_eff[Pi_M J_H] - (4*pi*G0)^-1 oint grad Phi.n dA stays as an explicit residual. | RESIDUAL_IF_PREMISES_FAIL | no orbital backfill |

## Orbital Newton Readout

| orbital_id | piece | statement | status | effect |
| --- | --- | --- | --- | --- |
| ORB3884_0_exterior | exterior potential | In the source-free exterior, Phi=-G0 M_H/r + multipoles + residuals; slow test bodies obey a^i=-partial^i Phi, so the monopole gives v^2 r=G0 M_H when range, radial, frame and non-EH residuals vanish. | EXACT_CONDITIONAL_READOUT | links Poisson/Gauss monopole to measured Kepler GM |
| ORB3884_1_no_range | range/radial guard | No finite-range alpha(lambda), radial source hair, frame split, or non-EH force may be absorbed into the monopole. | NO_CALIBRATION_CHEAT | keeps SPARC/orbital style fits from defining the source |
| ORB3884_2_slow_geodesic | slow-particle readout | For minimally coupled slow matter, d^2x^i/dt^2=-partial_i Phi+O(v^2/c^2,PPN). | CANDIDATE_NEWTON_READOUT | first-order Newton mechanics branch |
| ORB3884_3_not_GR | not local GR | Newtonian inverse-square readout does not prove gamma=1, beta=1, alpha_i=0, xi=0 or R11 non-EH operator silence. | NO_LOCAL_GR_PROMOTION | next gate is second-order PPN/R11 |

## Residual Bound Rows

| residual_id | component_id | symbol | formula_or_bound | current_status |
| --- | --- | --- | --- | --- |
| MGR3884_0_Meff_time | P8_Meff_conservation | dln_Meff_dt | \|d_t ln M_eff\| <= \|b_tau_strain\| + \|b_PiM_comm\| + \|Phi_EM_rad\|/(M_eff*c^2) + \|b_boundary_ref\| + \|b_extra_charge\| | OPEN_UNLESS_FLUX_THEOREM_PARENT_SIGNED |
| MGR3884_1_radial | P8_radial_source_hair | partial_r_ln_mu_obs | \|partial_r ln M_eff\| <= \|b_PiM_comm\|+\|b_boundary\|+\|b_extra_charge\|+\|b_range\| | OPEN_UNLESS_GAUSS_SURFACE_INDEPENDENCE_SIGNED |
| MGR3884_2_Gauss | P8_Gauss_calibration | Delta_Gauss | M_eff[Pi_M J_H] - (4*pi*G0)^-1 oint grad Phi.n dA | OPEN_GLOBAL_CLAIM |
| MGR3884_3_PiM | P8_PiM_projector_stress | Delta_PiM_metric | M_eff[delta Pi_M J_H]+M_eff[Pi_M J_H-J_M_parent] | OPEN_PROJECTOR_PARENT_OWNERSHIP |
| MGR3884_4_flux | P8_boundary_radiative_flux | Phi_EM_rad | dM_eff/dt includes -Phi_EM_rad/c^2 | OPEN_IF_RADIATING |
| MGR3884_5_orbital | P8_orbital_readout_residual | delta_a_r | a_r + G0*M_eff/r^2 | OPEN_UNTIL_READOUT_SIGNED |
| MGR3884_6_PPN | P8_nonlinear_beta_source_residue | delta_beta_source;gamma_minus_1 | second-order source-normalized PPN residual vector | DEFERRED_NEXT |

## Runner Update

| update_id | runner_field | rule | status |
| --- | --- | --- | --- |
| RUNU3884_0_flux | b_MHref_lock | b_MHref_lock := b_PiM_flux+b_Gauss+b_orbital+b_PiM_stress+b_boundary_ref+b_flux+b_PPN_source | MASS_LOCK_REFINED |
| RUNU3884_1_candidate | candidate zeros | b_PiM_flux=0 and b_Gauss=0 in the stationary candidate if PiM is parent-fixed and Gauss/readout premises hold | CANDIDATE_ONLY |
| RUNU3884_2_residual | fallback rows | if any premise fails, use MGR3884 residual rows for dln_Meff_dt, radial hair, Delta_Gauss, Delta_PiM, Phi_EM_rad and delta_a_r | RESIDUAL_BOUND_READY |
| RUNU3884_3_Newton | Newton branch | nabla^2 Phi=4*pi*G0 rho_H; oint gradPhi.n dA=4*pi*G0 M_eff; a=-gradPhi | FIRST_ORDER_NEWTON_CANDIDATE |
| RUNU3884_4_no_GR | local_GR | no promotion beyond first-order Newton until PPN/R11 source-stability vector is derived or bounded | NO_LOCAL_GR_PROMOTION |

## Source Register

Resolved `48/48` source rows.

| source_id | path | needle_found | role |
| --- | --- | --- | --- |
| SRC3884_00_next | source-intake\mts_residuals\P8_Y5_R2FR_3883_NEXT_TARGET.csv | True | 3883 selected PiM/Gauss target |
| SRC3884_01_same_source | source-intake\mts_residuals\P8_Y5_R2FR_3883_SAME_HILBERT_SOURCE_LOCK.csv | True | same Hilbert source lock |
| SRC3884_02_conservation | source-intake\mts_residuals\P8_Y5_R2FR_3883_SAME_HILBERT_SOURCE_LOCK.csv | True | total stress conservation |
| SRC3884_03_density | source-intake\mts_residuals\P8_Y5_R2FR_3883_NEWTON_SOURCE_DENSITY_BRIDGE.csv | True | Hilbert density bridge |
| SRC3884_04_poisson | source-intake\mts_residuals\P8_Y5_R2FR_3883_NEWTON_SOURCE_DENSITY_BRIDGE.csv | True | Poisson source bridge |
| SRC3884_05_PiM_resid | source-intake\mts_residuals\P8_Y5_R2FR_3883_MATTER_EM_RESIDUAL_VECTOR.csv | True | PiM residual |
| SRC3884_06_Gauss_resid | source-intake\mts_residuals\P8_Y5_R2FR_3883_MATTER_EM_RESIDUAL_VECTOR.csv | True | Gauss residual |
| SRC3884_07_runner | source-intake\mts_residuals\P8_Y5_R2FR_3883_RUNNER_UPDATE.csv | True | b_MHref decomposition |
| SRC3884_08_valid | source-intake\mts_residuals\P8_Y5_BRR545_3883_VALIDATION.csv | True | 3883 validation |
| SRC3884_09_SN4 | source-intake\mts_residuals\P8_source_normalized_Newton_branch_STACK.csv | True | closed Meff flux |
| SRC3884_10_SN8 | source-intake\mts_residuals\P8_source_normalized_Newton_branch_STACK.csv | True | Gauss surface integral |
| SRC3884_11_SN9 | source-intake\mts_residuals\P8_source_normalized_Newton_branch_STACK.csv | True | orbital readout |
| SRC3884_12_SN11 | source-intake\mts_residuals\P8_source_normalized_Newton_branch_STACK.csv | True | PPN source stability |
| SRC3884_13_Y5O4 | source-intake\mts_residuals\P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv | True | flux closure owner |
| SRC3884_14_Y5O6 | source-intake\mts_residuals\P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv | True | Gauss orbital calibration |
| SRC3884_15_Y5O7 | source-intake\mts_residuals\P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv | True | PPN stability |
| SRC3884_16_PG4 | source-intake\mts_residuals\P8_PG_calibration_residual_MAP.csv | True | Gauss residual map |
| SRC3884_17_PG5 | source-intake\mts_residuals\P8_PG_calibration_residual_MAP.csv | True | orbital readout residual map |
| SRC3884_18_PG8 | source-intake\mts_residuals\P8_PG_calibration_residual_MAP.csv | True | derivative hair map |
| SRC3884_19_bound_Meff | source-intake\mts_residuals\P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv | True | Meff bound matrix |
| SRC3884_20_bound_radial | source-intake\mts_residuals\P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv | True | radial source bound matrix |
| SRC3884_21_HM2 | source-intake\mts_residuals\P8_Hilbert_monopole_calibration_CONTRACT.csv | True | mass flux closure contract |
| SRC3884_22_HM3 | source-intake\mts_residuals\P8_Hilbert_monopole_calibration_CONTRACT.csv | True | monopole calibration contract |
| SRC3884_23_HM6 | source-intake\mts_residuals\P8_Hilbert_monopole_calibration_CONTRACT.csv | True | no derivative source hair |
| SRC3884_24_HC4 | source-intake\mts_residuals\P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv | True | surface charge equals PiM Hilbert mass |
| SRC3884_25_HC8 | source-intake\mts_residuals\P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv | True | Poisson/Gauss/orbital calibration |
| SRC3884_26_CC3 | source-intake\mts_residuals\P8_charge_current_equality_DIRECT_ATTEMPT.csv | True | projected mass current |
| SRC3884_27_CC7 | source-intake\mts_residuals\P8_charge_current_equality_DIRECT_ATTEMPT.csv | True | closed flux and Gauss calibration |
| SRC3884_28_CC8 | source-intake\mts_residuals\P8_charge_current_equality_DIRECT_ATTEMPT.csv | True | PPN second order guard |
| SRC3884_29_Delta_PiM | source-intake\mts_residuals\P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv | True | PiM residual decomposition |
| SRC3884_30_Delta_flux | source-intake\mts_residuals\P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv | True | flux residual decomposition |
| SRC3884_31_Delta_cal | source-intake\mts_residuals\P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv | True | calibration residual decomposition |
| SRC3884_32_DIV2 | source-intake\mts_residuals\P8_Y5_HILBERT_CURRENT_2467_DIVERGENCE_IDENTITY.csv | True | matter-shell divergence |
| SRC3884_33_DIV4 | source-intake\mts_residuals\P8_Y5_HILBERT_CURRENT_2467_DIVERGENCE_IDENTITY.csv | True | Killing clock closure |
| SRC3884_34_EXC3 | source-intake\mts_residuals\P8_Y5_HILBERT_CURRENT_2467_EXCHANGE_CURRENT_IDENTITY.csv | True | local stationary escape |
| SRC3884_35_HWT3 | source-intake\mts_residuals\P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv | True | Hilbert to PiM map |
| SRC3884_36_HWT8 | source-intake\mts_residuals\P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv | True | weak-field readout after glue |
| SRC3884_37_PAC537_4 | source-intake\mts_residuals\P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv | True | action-owned PiM projector |
| SRC3884_38_PAC537_8 | source-intake\mts_residuals\P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv | True | dressed source Gauss readout |
| SRC3884_39_HWG4 | source-intake\mts_residuals\P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv | True | PiM commutator certificate |
| SRC3884_40_HWG5 | source-intake\mts_residuals\P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv | True | no projector stress certificate |
| SRC3884_41_PV1 | source-intake\mts_residuals\P8_PiM_projector_variation_stress_CONTRACT.csv | True | topological absolute charge route |
| SRC3884_42_PV6 | source-intake\mts_residuals\P8_PiM_projector_variation_stress_CONTRACT.csv | True | projector residual map |
| SRC3884_43_EH501_2 | source-intake\mts_residuals\P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv | True | Ward current route |
| SRC3884_44_EH501_4 | source-intake\mts_residuals\P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv | True | Hamiltonian charge route |
| SRC3884_45_D501 | source-intake\mts_residuals\P8_TOPOLOGICAL_HILBERT_EQUALITY_DECISION.csv | True | topological-Hilbert best route |
| SRC3884_46_EM_flux | source-intake\mts_residuals\P8_EM_Poynting_source_flux_or_cross_term_vector.csv | True | radiative EM flux |
| SRC3884_47_frame | source-intake\mts_residuals\P8_frame_source_split_residual_or_zero.csv | True | frame split residual |

## Claim Gates

| gate_id | status | detail | claim_allowed |
| --- | --- | --- | --- |
| G3884_0_sources | PASS | 48/48 sources resolved | False |
| G3884_1_flux_theorem | PASS | PiM flux product-rule theorem | False |
| G3884_2_flux_zero | PASS | candidate stationary flux zero | False |
| G3884_3_Gauss | PASS | Gauss bridge | False |
| G3884_4_orbital | PASS | slow-particle readout | False |
| G3884_5_residuals | PASS | 7 mass/Gauss residual rows | False |
| G3884_6_no_GR | PASS | PPN/local-GR guard | False |
| G3884_7_no_claim | PASS | candidate first-order Newton only; global adoption and PPN/R11 remain open | False |

## Next Target

| next_id | target_checkpoint | objective | why_next |
| --- | --- | --- | --- |
| NEXT3884_0 | 3885-Y5-R2FR-second-order-PPN-source-stability-or-R11-residual-vector.md | push beyond first-order Newton by deriving gamma=1, beta=1 and preferred-frame/source-stability conditions in the candidate branch, or emit executable R11/PPN residual vector rows | 3884 gives the candidate first-order Newton bridge; the next non-negotiable gate for local GR is second-order PPN and non-EH operator stability |

## Bottom Line

This is a serious Newton bridge in candidate form. If the PiM/topological/projector premises are signed, `M_eff` becomes the closed Hilbert mass and the Gauss monopole gives the measured inverse-square source. The work is not local GR yet; the next hard gate is second-order PPN/R11 stability.
