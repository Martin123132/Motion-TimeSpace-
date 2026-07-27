# 3339 - Parent source-coupling decomposition under AX1090

Run UTC: `2026-06-28T02:04:06.019132+00:00`

## Verdict

3339 attacks the coupling directly.

The local-GR source route is now reduced to the decomposition:

`J^{mu nu} = kappa_* T^{mu nu} + Delta J^{mu nu}`

where `kappa_* T^{mu nu}` is the universal Hilbert-stress common mode and `Delta J^{mu nu}` is everything that cannot be hidden inside measured `G_N`.

Measured `G_N` can absorb one universal common coefficient. It cannot absorb species-relative weights, different temporal/spatial tensor ratios, hidden EM/Hodge/current coefficients, spin/clock couplings, or boundary/source-worldtube drift.

The exact local-GR zero route is therefore:

`Delta J^{mu nu} = nabla_lambda B^{lambda mu nu} + O((ell_c/L)^p)`

with zero exterior readout of the boundary/improvement term, universal metric contact absorbed into measured constants, and scale-suppressed derivative contact below the PPN budget.

The important improvement is that `ell_c` now has an owner route: ultralocal Hilbert coupling gives residual `ell_c=0`; a centered finite kernel gives `p_contact=2`; second-moment silence gives `p_contact=4`.

No local-GR/PPN/Maxwell claim is made, because the parent action still has to sign the Hilbert source clause and the EM/current/Hodge owner.

## Source Register

- `SRC3339_0_3338_doc`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3338-Y5-R2FR-PPN-projector-patch-geometry-source-contract-under-AX1090.md` exists=true parse_ok=true role=3338 handoff for PPN projector, patch scale, and next coupling target
- `SRC3339_1_3338_contact`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3338_CONTACT_UNIVERSALITY_CONTRACT.csv` exists=true parse_ok=true role=contact universality branches
- `SRC3339_2_3338_acquisition`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3338_SOURCE_ACQUISITION_ROWS.csv` exists=true parse_ok=true role=ell_s, ell_c, contact tensor, and spectral-tail missing inputs
- `SRC3339_3_3293_local_gr_coupling`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3293_LOCAL_GR_MATTER_COUPLING_REDUCTION.csv` exists=true parse_ok=true role=prior local-GR matter coupling reduction rows
- `SRC3339_4_2783_wep_owner`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2783_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv` exists=true parse_ok=true role=prior parent WEP coupling owner theorem attempt
- `SRC3339_5_2577_worldtube`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_SOURCE_SELECTOR_COUPLING_2577_WORLDTUBE_HILBERT_COUPLING_SELECTOR_THEOREM.csv` exists=true parse_ok=true role=worldtube/Hilbert source selector and coupling baseline
- `SRC3339_6_2577_implications`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_SOURCE_SELECTOR_COUPLING_2577_NEWTON_GR_IMPLICATIONS.csv` exists=true parse_ok=true role=Newton/local-GR implications of source-selector coupling closure
- `SRC3339_7_3117_em_priority`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3117_EM_COUPLING_OWNER_ALPHA_PRIORITY.csv` exists=true parse_ok=true role=EM alpha/current/Hodge coupling owner split
- `SRC3339_8_3337_contact`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3337_CONTACT_THEOREM.csv` exists=true parse_ok=true role=contact zero/derivative scaling theorem

## Coupling Decomposition Theorem

- `CDEC3339_0_parent_current_definition`: statement=define the parent source current by J_A^{mu nu}:=(2/sqrt(-g_obs)) delta S_matter_A/delta g_obs_{mu nu}, with all ordinary sectors varied against the same observed metric/coframe; derivation=A Hilbert stress/current is the unique object that the local metric perturbation can couple to without adding a post-variation species selector.; zero_condition=all matter sectors use the same g_obs/coframe, action measure, and variation rule; residual_if_failed=species-dependent source selector or non-Hilbert current; valid_for_claim=false
- `CDEC3339_1_common_mode_split`: statement=split the total source current as J^{mu nu}=kappa_* T^{mu nu}+Delta J^{mu nu}; derivation=Choose kappa_* from the Newtonian T00/Poisson slot; the common mode kappa_*T is measured-G calibration, while Delta J is the physical residual source coupling.; zero_condition=Delta J^{mu nu}=0 up to boundary/improvement terms and scale-suppressed derivative contacts; residual_if_failed=PPN/WEP/clock/EM residual channels receive P[Delta J]; valid_for_claim=false
- `CDEC3339_2_irreducible_channel_projection`: statement=project Delta J into trace/common, traceless-metric, species, spin/antisymmetric, EM-Hodge, derivative/contact, and boundary channels; derivation=After the Newtonian common mode is fixed, only non-common tensor structure can affect gamma, beta, WEP, clocks, EM propagation, or orbital residuals.; zero_condition=all non-common projections vanish or are bounded below the arena threshold; residual_if_failed=local-GR branch becomes an explicit residual-vector branch rather than a theorem-zero branch; valid_for_claim=false
- `CDEC3339_3_bianchi_conservation_guard`: statement=the local GR branch requires nabla_mu Delta J^{mu nu}=0 or a signed compensating field equation; derivation=The Einstein/PPN left side is divergence-constrained by the Bianchi identity; an unbalanced source residual is a fifth-force or nonconservation channel, not GR.; zero_condition=parent diffeomorphism invariance plus no external source selector gives nabla_mu T^{mu nu}=0 and no unbalanced Delta J; residual_if_failed=Bianchi/conservation violation must be routed to clock, WEP, orbital, or boundary tests; valid_for_claim=false

## Measured-G Absorption Theorem

- `GABS3339_0_measured_G_absorbs_common_mode`: claim=a single universal common mode kappa_* multiplying the total Hilbert stress is not a PPN anomaly after measured-G calibration; formula=kappa_* T^{00} -> measured G_N rho in the Newtonian Poisson slot; derivation=Local Newtonian experiments fix the product kappa_* times source normalization; a pure common rescaling is the definition of the calibrated Newtonian slot.; claim_gate=allowed only if the same kappa_* multiplies matter, EM stress, pressure/stress, and clock sectors; valid_for_claim=false
- `GABS3339_1_relative_weights_cannot_hide`: claim=species-relative weights w_A cannot be absorbed into one G_N; formula=J^{mu nu}=kappa_* sum_A (1+eta_A)T_A^{mu nu}; eta_A-eta_B survives WEP/source-composition projections; derivation=A single measured G can calibrate one common coefficient, not independent weights for different source/test compositions.; claim_gate=requires eta_A=0 for all ordinary sectors or finite WEP/source-composition bounds; valid_for_claim=false
- `GABS3339_2_tensor_ratio_cannot_hide`: claim=different temporal/spatial/trace couplings cannot be hidden inside Newtonian G; formula=Delta J_TL^{ij}:=J^{ij}-kappa_*T^{ij} and Delta J_tracefree feed gamma/beta/stress residuals; derivation=G_N fixes mostly the slow-motion T00 source; gamma and beta test how the same source curves spatial and nonlinear metric components.; claim_gate=requires tensor-ratio equality or explicit PPN response bound; valid_for_claim=false
- `GABS3339_3_boundary_improvement_silence`: claim=improvement currents can be harmless only if they are exact boundary terms with zero exterior flux/readout; formula=Delta J^{mu nu}=nabla_lambda B^{lambda mu nu}, with P_PPN Delta J=0 on the exterior comparison patch; derivation=Divergence/improvement terms can change local representatives without changing the exterior Hilbert charge only when their boundary projection vanishes.; claim_gate=requires source worldtube, boundary, and readout projector to be fixed before fitting; valid_for_claim=false

## Residual Channel Vector

- `RES3339_0_common_trace`: projection=P_common[Delta J]; zero_route=absorbed into measured G_N if universal across all sectors; observable_risk=none after calibration if exactly common; bound_formula=not scored separately unless Dln(kappa_*) or source normalization varies; status=CONDITIONAL_ZERO_ROUTE; valid_for_claim=false
- `RES3339_1_tensor_anisotropy`: projection=P_TL[Delta J]; zero_route=same Hilbert tensor ratio for T00, Tij, pressure, and stress; observable_risk=PPN gamma/beta and orbital stress residuals; bound_formula=epsilon_tensor <= ||P_PPN G_PPN P_TL Delta J||/||kappa_* T00||; status=PPN_BOUND_REQUIRED_IF_NONZERO; valid_for_claim=false
- `RES3339_2_species_WEP`: projection=P_species[Delta J]; zero_route=one species-blind matter action measure and no source-only weights w_A; observable_risk=WEP, source-composition, clock-composition, R10 material residuals; bound_formula=epsilon_WEP <= max_{A,B}|eta_A-eta_B| after common-mode removal; status=WEP_BOUND_REQUIRED_IF_NONZERO; valid_for_claim=false
- `RES3339_3_spin_clock`: projection=P_spin_or_clock[Delta J]; zero_route=no independent spin/torsion/clock-channel coupling outside the public metric/coframe; observable_risk=clock anisotropy, spin-polarized tests, preferred-frame channels; bound_formula=epsilon_clock <= ||P_clock Delta J||/||kappa_*T||; status=CLOCK_BOUND_REQUIRED_IF_NONZERO; valid_for_claim=false
- `RES3339_4_EM_Hodge_stress`: projection=P_EM[Delta J]; zero_route=Maxwell/Hodge action uses the same public metric/coframe and same kappa_* Hilbert stress owner; observable_risk=light bending, Shapiro delay, EM stress/Poynting, alpha/current/Hodge hidden residuals; bound_formula=epsilon_EM <= |delta_ZA| + |delta_star| + |delta_J| + ||P_EM Delta T_EM||/||T_EM||; status=EM_STRESS_ROUTE_REQUIRED; valid_for_claim=false
- `RES3339_5_derivative_contact`: projection=P_derivative_contact[Delta J]; zero_route=ultralocal Hilbert coupling or universal contact absorbed into measured constants; observable_risk=finite-size PPN/contact floor; bound_formula=epsilon_contact <= C_contact(ell_c/L_PPN)^p_contact; status=CONTACT_SCALE_OWNER_REQUIRED; valid_for_claim=false
- `RES3339_6_boundary_worldtube`: projection=P_boundary[Delta J]; zero_route=fixed worldtube/Hilbert source class and zero exterior boundary flux; observable_risk=source mass drift, orbital GM mismatch, PPN boundary leakage; bound_formula=epsilon_boundary <= ||P_exterior dB||/||kappa_*T||; status=WORLDTUBE_BOUND_REQUIRED_IF_NONZERO; valid_for_claim=false

## Kernel Contact Scale Owner

- `KERN3339_0_ultralocal_Hilbert`: coupling_kernel=K^{mu nu}_{alpha beta}(x,y)=kappa_* delta^{mu nu}_{alpha beta} delta(x-y); derivation=The source current is exactly local Hilbert stress; no finite-width kernel exists after measured-G calibration.; ell_c_owner=ell_c=0 for the residual contact channel; contact_result=epsilon_contact_PPN=0 if tensor universality and boundary silence are also signed; status=BEST_ZERO_ROUTE; valid_for_claim=false
- `KERN3339_1_even_isotropic_finite_kernel`: coupling_kernel=K(z)=delta(z)+m2 nabla^2 delta(z)/2+O(ell_c^4 nabla^4); derivation=A centered even finite-range kernel has no first moment; the first surviving long-wavelength correction is second derivative.; ell_c_owner=ell_c^2 := m2 := integral |z|^2 K(z) dz / integral K(z) dz; contact_result=p_contact=2 unless the second moment is also absorbed or symmetry-forbidden; status=DERIVATIVE_CONTACT_BOUND_ROUTE; valid_for_claim=false
- `KERN3339_2_second_moment_absorbed`: coupling_kernel=K(z)=delta(z)+m4 nabla^4 delta(z)/24+...; derivation=If the zeroth and second-derivative local terms are absorbed by calibration or forbidden by symmetry, the fourth-order term dominates.; ell_c_owner=ell_c^4 := m4 with C_contact carrying tensor/readout constants; contact_result=p_contact=4 route from 3337/3338; status=STRONG_SCALE_SUPPRESSION_ROUTE; valid_for_claim=false
- `KERN3339_3_odd_or_species_kernel`: coupling_kernel=K_A(z) has odd moment or species-dependent coefficient; derivation=Odd moments generate first-derivative/bias terms; species-dependent kernels cannot be absorbed into one G_N.; ell_c_owner=requires finite source-backed kernel moments for each sector; contact_result=retains explicit WEP/contact floor; status=FAIL_OR_BOUND_ROUTE; valid_for_claim=false

## Maxwell/EM Stress Coupling Route

- `EM3339_0_public_Hodge_Maxwell`: condition=S_EM=-lambda_0/4 integral sqrt(-g_obs) F_{mu nu}F^{mu nu} with lambda_0 constant and hidden-independent; consequence=T_EM^{mu nu} is the Hilbert stress of the same observed metric/coframe, so EM stress couples through the same kappa_* common mode; local_residual=no local alpha/Hodge/current residual from lambda_0 alone; alpha number may remain calibrated rather than derived; status=LOCAL_MAXWELL_GR_ROUTE_CONDITIONAL; valid_for_claim=false
- `EM3339_1_hidden_F2_coefficient`: condition=lambda(y)F^2 or hidden-visible coefficient map survives vertical variation; consequence=Lie_v lambda creates b_alpha and EM stress/current residuals; local_residual=clock/WEP/R10/EM propagation channels reopen; status=FAIL_OR_BOUND_ROUTE; valid_for_claim=false
- `EM3339_2_current_owner`: condition=charge/current lattice J_Q is fixed representation/q-basic data; consequence=delta_J=0; source/test charge normalization does not float independently; local_residual=if q_A(y) weights exist then delta_J_A=Lie_v ln q_A and WEP/R10 source legs reopen; status=CURRENT_OWNER_GATE; valid_for_claim=false
- `EM3339_3_poynting_stress_readout`: condition=Poynting flux and radiation stress are read from the same public Hodge metric; consequence=EM energy flow contributes to Hilbert T_EM with the same source coupling as matter; local_residual=private constitutive/background-flow tensor C_constitutive creates birefringence/stress residuals if not zero; status=POYNTING_BACKGROUND_CHECK; valid_for_claim=false

## Parent Signature Requirements

- `REQ3339_0_parent_Hilbert_action`: requirement=one parent matter action varied with respect to the observed metric/coframe; closes=defines T^{mu nu} and J^{mu nu} without post-variation source selectors; current_status=CONDITIONAL_FROM_PRIOR_ROWS_NOT_PARENT_SIGNED; valid_for_claim=false
- `REQ3339_1_common_kappa`: requirement=one universal kappa_* for matter, EM, pressure/stress, and clock sectors; closes=measured-G absorption of common mode; current_status=NOT_PARENT_SIGNED; valid_for_claim=false
- `REQ3339_2_no_species_weights`: requirement=no species-indexed source weights w_A outside representation/gauge data; closes=WEP/source-composition residual zero; current_status=WEP_OWNER_THEOREM_CONDITIONAL_ONLY; valid_for_claim=false
- `REQ3339_3_public_Maxwell_Hodge`: requirement=EM kinetic/Hodge/current owner is public, q-basic, and hidden-independent; closes=Maxwell stress and Poynting couple through Hilbert T_EM; current_status=EM_PRIORITY_SPLIT_EXISTS_NOT_CLOSED; valid_for_claim=false
- `REQ3339_4_kernel_moments`: requirement=ell_c, C_contact, p_contact are derived from the parent coupling kernel or proven ultralocal; closes=3338 contact floor evaluation; current_status=DERIVATION_ROUTE_NOW_DEFINED_BUT_PARENT_INPUT_MISSING; valid_for_claim=false
- `REQ3339_5_bianchi_balance`: requirement=nabla_mu Delta J^{mu nu}=0 or compensator equation is signed; closes=conservation/covariance gate; current_status=NOT_SIGNED_FOR_RESIDUAL_CHANNELS; valid_for_claim=false

## Promotion Gates

- `GATE3339_0_decomposition_theorem`: claim=source coupling can be decomposed into common measured-G mode plus residual channels; passed=true; reason=J=kappa_*T+Delta J with projectors to tensor/species/spin/EM/contact/boundary channels; valid_for_claim=false
- `GATE3339_1_absorption_rule`: claim=measured G absorption is legitimate only for a universal common Hilbert stress coefficient; passed=true; reason=single G_N calibrates one common T00 coefficient and cannot hide species/tensor/EM relative weights; valid_for_claim=false
- `GATE3339_2_kernel_owner_route`: claim=ell_c and p_contact have an owner route through local or finite-range coupling kernels; passed=true; reason=ultralocal Hilbert gives ell_c=0; centered finite kernel gives p=2; second-moment silence gives p=4; valid_for_claim=false
- `GATE3339_3_parent_signature_closed`: claim=parent action signs all zero conditions; passed=false; reason=Hilbert action, common kappa, no species weights, public Maxwell/Hodge, kernel moments, and Bianchi balance are not all parent-signed; valid_for_claim=false
- `GATE3339_4_local_GR_claim`: claim=MTS local-GR/PPN/Maxwell source coupling is claim-ready; passed=false; reason=3339 derives the exact coupling fork but does not yet attach the parent action clauses or numeric residual bounds; valid_for_claim=false

## Decision Ledger

- `DEC3339_0`: question=Did 3339 just circle the missing coupling?; answer=no; reason=it turns coupling into the equation J=kappa_*T+Delta J and identifies exactly which projections are absorbable, zeroable, or empirically boundable; next_action=try to sign J=kappa_*T from the parent action syntax or build finite residual rows for the nonzero projections; valid_for_claim=false
- `DEC3339_1`: question=Can Newton's constant be derived here?; answer=not yet; but its role is clarified; reason=G_N can calibrate the universal common coupling kappa_*, while relative tensor/species/EM weights remain physical and cannot be hidden in G_N; next_action=look for a parent normalization principle for kappa_* separately from local-GR residual silence; valid_for_claim=false
- `DEC3339_2`: question=Does EM/Poynting help the route?; answer=yes, as a coupling discriminator; reason=if EM stress/Poynting comes from the same public Hodge metric, it supports universal Hilbert coupling; hidden F2/Hodge/current maps create measurable residuals; next_action=tie the EM stress owner rows to the parent Hilbert source clause; valid_for_claim=false

## Next Target

- `3340-Y5-R2FR-parent-Hilbert-source-clause-or-finite-residual-vector-under-AX1090.md`: target_script=scripts/Y5_R2FR_3340_parent_Hilbert_source_clause_or_finite_residual_vector.py; objective=search/construct the exact parent action clause that signs J=kappa_*T for matter+EM, or emit finite residual vector rows for tensor/species/spin/EM/contact/boundary channels; must_include=parent action syntax; variation target; common kappa; no species weights; public Maxwell/Hodge; kernel moment owner; Bianchi balance; no local-GR claim unless all zero gates close; fallback_if_failed=promote residual-channel vector to empirical bound acquisition rather than repeating missing-source ledgers; valid_for_claim=false

## Test Notes

- This checkpoint is private and nonclaim.
- It is a derivation/contract checkpoint: it moves the coupling problem into a residual-vector theorem instead of leaving it as a vague missing input.
- It does not derive the numerical value of `G_N` or `alpha`; it separates calibration of common constants from dangerous hidden relative couplings.
- `formalization-workbench` is not modified.
