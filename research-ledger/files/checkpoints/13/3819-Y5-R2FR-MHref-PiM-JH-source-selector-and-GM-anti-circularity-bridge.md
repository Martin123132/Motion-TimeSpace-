# 3819 - MHref, PiM JH Source Selector, And GM Anti-Circularity Bridge

## Status

`PASS_NONCLAIM_SOURCE_SELECTOR_ACTIVE_MASS_AND_GM_GUARD_BUILT`

This checkpoint does not claim Newton, local GR, PPN, R10, clock, orbital, or source-normalization closure. It does something narrower and useful: it turns the source-mass problem into an exact contract rather than a vague missing-data complaint.

## Source Selector Theorem

| selector_id | status | statement | derived_form | failure_if_unsigned |
| --- | --- | --- | --- | --- |
| SST3819_0_fixed_arena_first | EXACT_CONDITIONAL_SELECTOR_ORDER | Choose the observed metric/coframe, time generator tau, reference H_ref, source worldtube W_src, and linking surfaces before fitting any orbital mu=GM. | arena=(g_obs,e_obs,tau,H_ref,W_src,[S_link]) fixed first | source normalization can be absorbed into a readout fit |
| SST3819_1_worldtube_from_current_support | EXACT_CONDITIONAL_WORLDTUBE_DEFINITION | The source region is selected by the support of the same-frame Hilbert/Hamiltonian source current, not by a fitted gravitational radius. | W_src=closure(supp J_H[tau,e_obs]) with homology class [S_link] around W_src | mass support and orbital readout can chase each other |
| SST3819_2_dressed_Hamiltonian_source_mass | EXACT_CONDITIONAL_CHARGE_DEFINITION | The mass entering Poisson is the dressed Hamiltonian charge of W_src in the fixed arena, including matter, binding, improvement and boundary/reference terms. | M_H_ref(W)=c^-2*(H_tau[W,S_link]-H_ref) | bare rest mass, boundary energy, and readout mass are silently mixed |
| SST3819_3_positive_mass_condition | DERIVED_CONDITIONAL_POSITIVITY_LAW | M_H_ref is nonnegative if the tau-Hamiltonian density obeys the branch energy condition, H_ref is the fixed vacuum/reference minimum, and boundary/improvement terms do not over-subtract. | M_H_ref>=0, strict if W_src carries nonzero positive Hamiltonian charge | negative denominators or sign flips remain possible |
| SST3819_4_orbital_GM_forbidden_as_input | EXACT_ANTI_CIRCULARITY_RULE | An orbital mu_fit can test the product G_ref*M_H_ref, but cannot define M_H_ref for that same test. | M_H_ref != mu_fit/G_ref for any claim using mu_fit as evidence | Newton recovery becomes tautological |
| SST3819_5_selector_verdict | PARTIAL_ADVANCE_NOT_CLOSED | The selector law is now explicit enough to prevent GM laundering, but parent-signed tau/H_ref/Pi_M/source-current ownership is still required. | selector usable as contract; not a Newton/local-GR claim | retain finite source-normalization residuals |

## Active Mass Law

| law_id | status | formula | meaning | scope |
| --- | --- | --- | --- | --- |
| AML3819_0_Komar_Tolman_stationary_selector | EXACT_CONDITIONAL_STATIONARY_ACTIVE_MASS_FORM | M_tau=(2/c^2)*int_Sigma (T_mn-0.5*T*g_mn)n^m tau^n dSigma + M_boundary_reference | For a stationary branch this is the active source charge associated with tau, not an arbitrary fitted mass. | requires stationary/asymptotic or finite-domain tau, boundary reference, and same-frame total Hilbert stress |
| AML3819_1_slow_weak_limit | EXACT_CONDITIONAL_LIMIT | M_tau=int rho_rest d^3x + O(v^2/c^2,p/c^2,binding/c^2,boundary/c^2,nonEH) | The Newtonian mass follows as the slow weak limit only after pressure, kinetic, binding, boundary and non-EH terms are retained or bounded. | ordinary cold sources may make corrections tiny; compact/relativistic sources cannot drop them |
| AML3819_2_Poisson_density_refinement | SOURCE_DENSITY_REFINEMENT | rho_H in nabla^2 Phi=4*pi*G_ref*rho_H must mean the selected active Hamiltonian/Tolman density, not whichever density best fits mu | 3818's Poisson algebra is preserved, but the source symbol is now sharpened. | if rho_H is taken as T_00/c^2, pressure/binding residual R_pressure_binding must be retained |
| AML3819_3_passive_inertial_link | CARRIED_EXACT_CONDITIONAL_FROM_3772 | same descended matter action => m_passive/m_inertial=1 + retained residuals | This keeps Newton's inertial/passive side connected to the same source branch. | still depends on source action descent and theta/coupling silence |
| AML3819_4_active_mass_verdict | DERIVED_CONDITIONAL_NOT_NUMERICALLY_CLOSED | M_active=M_H_ref if stationary active charge, boundary reference, and slow-limit residuals are signed | The active-mass route is viable and sharper than a placeholder, but not yet claim-grade. | feeds 3820 Komar/Tolman and independent-source ledger |

## PiM JH Closure Audit

| audit_id | status | condition | result | residual_symbol |
| --- | --- | --- | --- | --- |
| PIM3819_0_exact_product_identity | EXACT_OBSTRUCTION_IDENTITY | d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H | Flux closure is not a vibe-check: it fails only through current nonconservation, projector commutator, boundary flux, anomaly, or readout-dependence terms. | R_PiM_commutator |
| PIM3819_1_current_conservation_feed | CONDITIONAL_FROM_3817 | nabla_mu T_total^mu_nu=0 and same tau/coframe source current | Pi_M dJ_H can vanish if the 3817 Ward/Bianchi total-current contract is parent-signed. | C_Bianchi_total |
| PIM3819_2_projector_fixedness | OPEN_REQUIRED_ZERO | [d,Pi_M]J_H=0 | This is the main unsolved technical zero: Pi_M must be a fixed parent charge map, not a radius/readout-dependent mask. | R_PiM_commutator |
| PIM3819_3_compact_exterior_flux | OPEN_REQUIRED_ZERO_OR_BOUND | int_annulus d(Pi_M J_H)=0 or finite epsilon_radial_Meff | Radiation, non-EH, boundary and frame tails must be absent or bounded before inverse-square mass closure is claimed. | R_flux_leak |
| PIM3819_4_closure_verdict | NOT_CLOSED_BUT_NOW_EXACTLY_LOCALIZED | PIM3819_1 through PIM3819_3 all signed | Pi_M closure remains blocked; the next proof should target projector fixedness plus active-mass source density, not re-list generic missing data. | R_PiM_JH_flux |

## GM Anti-Circularity Contract

| contract_id | status | rule | acceptance | blocked_action |
| --- | --- | --- | --- | --- |
| GM3819_0_observable_split | EXACT_DEGENERACY_LAW | mu_fit=G_ref*M_H_ref*(1+delta_readout+delta_boundary+delta_range+delta_nonEH+delta_orbit) | a test must split the product or state that only mu is tested | do not infer M_H_ref=mu_fit/G_ref and then claim Newton source recovery |
| GM3819_1_independent_mass_inputs | SOURCE_LEDGER_REQUIRED | claim-grade M_H_ref needs non-orbital source evidence: lab mass/calorimetry/composition/density-volume or a parent Hamiltonian charge calculation | source path, units, uncertainty, frame, tau/reference and no orbital-mu reuse | do not use ephemeris GM as the mass denominator for the same arena |
| GM3819_2_allowed_orbital_use | SAFE_USE_RULE | orbital data may constrain residuals in mu_fit, range dependence, PPN/readout tails, or ratios once source normalization is separately fixed | the row labels orbital evidence as product evidence, not source-mass evidence | do not mark local GR/Newton passed from orbital agreement alone |
| GM3819_3_dimensionless_cross_arena_use | PREFERRED_NEXT_TEST_ROUTE | use WEP, R10, clock, PPN and orbital ratios as cross-arena constraints on the same source-normalization vector | one shared residual vector; no per-arena refitting | do not tune G_eff or source mass separately in each arena |
| GM3819_4_verdict | PASS_GUARD_NOT_PHYSICS_CLAIM | GM circularity is now guarded explicitly; the physics claim remains blocked until M_H_ref/Pi_M are independently owned | 3820 builds the active-mass/source-ledger route | do not publish Newton/local-GR pass from this checkpoint |

## Finite Fallbacks

| residual_id | symbol | definition | bound_formula | current_status |
| --- | --- | --- | --- | --- |
| R3819_0_selector_owner | R_selector_owner | fixed arena/tau/worldtube/source selector residual | norm(delta selector) or Boolean closure failure | TAU_HREF_WORLDTUBE_NOT_PARENT_SIGNED |
| R3819_1_active_mass_density | R_active_density | difference between selected active Hamiltonian/Tolman density and simplified T_00/c^2 density | ||rho_H-rho_active||/rho_ref | PRESSURE_BINDING_BOUNDARY_TERMS_NOT_BOUNDED |
| R3819_2_PiM_commutator | R_PiM_commutator | projector commutator obstruction to d(Pi_M J_H)=0 | ||[d,Pi_M]J_H|| in source annulus | PIM_FIXEDNESS_NOT_PROVED |
| R3819_3_worldtube_boundary | R_worldtube_boundary | boundary/reference/improvement flux across linking surfaces | |int_S delta B_tau|/M_ref | BOUNDARY_REFERENCE_LOCK_OPEN |
| R3819_4_GM_anti_circularity | R_GM_anti_circularity | unresolved split between G_ref, source mass, and observed mu | |delta ln mu-delta ln G_ref-delta ln M_H_ref| | INDEPENDENT_SOURCE_LEDGER_MISSING |
| R3819_5_pressure_binding | R_pressure_binding | pressure, kinetic, internal and binding corrections to Newtonian density | O(v^2/c^2,p/c^2,binding/c^2) | ACTIVE_MASS_LIMIT_NOT_NUMERICALLY_BOUNDED |
| R3819_6_total | R_source_normalization_total | total source-normalization obstruction for Newton/local GR | R_selector_owner+R_active_density+R_PiM_commutator+R_worldtube_boundary+R_GM_anti_circularity+R_pressure_binding | LOCAL_GR_NEWTON_SOURCE_NORMALIZATION_BLOCKED |

## Claim Gates

| gate_id | gate_status | claim_allowed | detail |
| --- | --- | --- | --- |
| GATE3819_0_sources | PASS_NONCLAIM | false | all source paths and needles present |
| GATE3819_1_selector_contract | PASS_NONCLAIM | false | source selector theorem emitted, but parent signatures remain open |
| GATE3819_2_active_mass_law | PASS_NONCLAIM | false | Komar/Tolman active-mass route derived conditionally; pressure/binding/boundary terms retained |
| GATE3819_3_PiM_flux_closure | BLOCKED | false | Pi_M commutator/fixedness and compact exterior flux not proved |
| GATE3819_4_GM_anti_circularity | PASS_GUARD | false | orbital GM laundering forbidden explicitly |
| GATE3819_5_Newton_claim | BLOCKED | false | Newton claim waits on M_H_ref/Pi_M/source-ledger closure |
| GATE3819_6_local_GR_claim | BLOCKED | false | local GR claim waits on source normalization plus PPN/readout residuals |

## Next Target

`3820-Y5-R2FR-Komar-Tolman-active-mass-and-independent-source-ledger.md`

Target: derive or bound the stationary Komar/Tolman active-mass route, pressure/binding corrections, and an independent source ledger so `M_H_ref` is not secretly `mu_fit/G_ref`.

## Machine Outputs

| status | summary |
| --- | --- |
| PASS_NONCLAIM_SOURCE_SELECTOR_ACTIVE_MASS_AND_GM_GUARD_BUILT | 3819 derives the conditional source-selector/active-mass bridge, blocks orbital GM laundering, and selects 3820 Komar/Tolman plus independent source ledger. |
