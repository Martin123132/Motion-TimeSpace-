# 3730 - Coupling Source-Norm Derivation Hunt

## Status
- `COUPLING_SOURCE_NORM_CONTRACT_ADVANCED_VALUES_MISSING`
- Main split: `sigma_A` is the parent source-current norm; `beta_A` is the arena observable response norm.
- This is progress over a vague coupling gap: it tells us exactly what must be derived next.

## Core Derivation
- `DER3730_0_parent_current` `DERIVED_DEFINITION`: J_X := delta_X S_parent = delta_X S_matter + delta_X S_boundary + delta_X S_marker + delta_X S_nonH | The source norm sigma_A must come from a parent variation/current, not from a fitted arena knob.
- `DER3730_1_sigma_envelope` `DERIVED_BOUND_CONTRACT`: sigma_A <= ||Pi_A J_X|| + ||tail_A|| <= sum_i ||component_i,A|| | A no-cancellation absolute envelope is the safe finite-coupling route for every local arena.
- `DER3730_2_beta_matrix_norm` `DERIVED_OPERATOR_NORM_CONTRACT`: beta_A=sqrt(lambda_max(B_A^T W_A B_A)) for finite response matrices, or beta_A=||B_A||_{H_to_OA} | The observable response norm is computable from the arena linearized readout map; it is not a new physical constant.
- `DER3730_3_3729_response_link` `DERIVED_LINK_TO_3729`: residual_bound_A=beta_A*sigma_A/(Xi_loc-ell_A)+epsilon_A | The 3729 response law becomes scoreable exactly when Xi_loc, sigma_A, beta_A, ell_A, epsilon_A, and bound_A are owned.
- `DER3730_4_quotient_zero_branch` `CONDITIONAL_ZERO_THEOREM`: If Dq[X]=0, e_obs=Obs_e(q(Phi)), S_matter=Sbar[Psi,e_obs,theta], Lie_X theta=0, and hidden tails vanish, then J_X=0 and sigma_A=0. | The zero-coupling route is real mathematically, but only conditional until the parent action signs all clauses together.
- `DER3730_5_R10_product_law` `DERIVED_PRODUCT_GUARD`: alpha_X(lambda)=K_X^R10(lambda) beta_source(lambda) beta_test(lambda)+epsilon_tail(lambda) | The R10 coupling is a source-test product; universal c_g normally enters as c_g^2 unless one leg is already inside Qbar_XH.
- `DER3730_6_EM_Poynting_source` `ROUTE_OPEN_CONTRACT`: sigma_EM <= ||Pi_EM delta_X(Hodge/constitutive/stress/Poynting balance)|| + ||tail_EM|| | The Poynting route is not discarded: it is converted into a gateable source-current/observable-response problem.

## Route Split
- `ROUTE3730_0_zero_sigma` `CONDITIONAL_NOT_PARENT_SIGNED`: sigma_A=0 | quotient-zero branch
- `ROUTE3730_1_finite_sigma` `SCHEMA_READY_VALUES_MISSING`: sigma_A <= |c_g tau_A|+|b_dis tau_dis,A|+sum|b_marker s_marker,A|+|q_nonH,A|+|Delta_W,A|+|boundary_A| | finite no-cancellation source envelope
- `ROUTE3730_2_beta_matrix` `DERIVED_SCHEMA_VALUES_MISSING`: beta_A=sqrt(lambda_max(B_A^T W_A B_A)) | finite observable response norm
- `ROUTE3730_3_R10_product` `DERIVED_PRODUCT_FORM_NUMERICALLY_BLOCKED`: sigma_R10 or alpha_R10 uses K_X^R10 beta_source beta_test + epsilon_tail | source-test product branch
- `ROUTE3730_4_EM_Poynting` `ROUTE_OPEN_PARENT_INPUTS_MISSING`: sigma_EM from Hodge/constitutive/stress/Poynting variation; beta_EM from D O_Poynting | EM/Poynting branch

## Arena Couplings
- `R10_short_range`: sigma route `sigma_R10 from K_X^R10 beta_source beta_test plus retained tails`; beta route `beta_R10 from alpha/torque readout normalization`
- `PPN_solar_system`: sigma route `sigma_PPN from c_g/b_dis/tail source current projected into weak-field metric equations`; beta route `beta_PPN from PPN response matrix M_PPN`
- `clock_redshift`: sigma route `sigma_clock from marker/constants/time-readout variation`; beta route `beta_clock from frequency/redshift observable derivative`
- `orbital_dynamics`: sigma route `sigma_orbit from source normalization, measured GM calibration, and boundary/support tails`; beta route `beta_orbit from orbit/range/timing response matrix`
- `EM_Poynting_waves`: sigma route `sigma_EM from Hodge/constitutive/Poynting-balance variation`; beta route `beta_EM from Maxwell stress/Poynting observable map`
- `Newton_limit`: sigma route `sigma_Newton from Poisson-source and measured-G normalization residual`; beta route `beta_Newton from acceleration/potential residual map`

## Decisions
- `DEC3730_0_real_progress` `COUPLING_BOTTLENECK_SPLIT_INTO_SIGMA_AND_BETA` | The framework no longer has a vague coupling gap: sigma_A is the parent source-current norm and beta_A is an arena response matrix norm.
- `DEC3730_1_best_route` `ATTACK_PARENT_JX_AND_RESPONSE_MATRICES_NEXT` | The fastest route to local-GR/Newton testing is not another bound table; it is deriving J_X plus B_A/W_A for at least one arena.
- `DEC3730_2_R10_warning` `KEEP_SOURCE_TEST_PRODUCT_LAW` | R10 finite exchange is product-shaped, so linear c_g shortcuts are rejected unless one leg is explicitly packed into the source normalization.
- `DEC3730_3_EM_route` `KEEP_EM_POYNTING_AS_GATEABLE_BRANCH` | Poynting/vector-wave intuition survives as a formal response arena but still needs parent Hodge/constitutive variation.

## Refusals
- `REF3730_0_parent_JX` `J_X`: missing parent-owned source current | fix: derive delta_X S_parent including matter, boundary, marker, and non-Hilbert tails
- `REF3730_1_zero_signature` `sigma_A=0`: zero branch not parent-signed | fix: close q-kernel, observed coframe, matter functor, no-marker, and hidden-tail clauses together
- `REF3730_2_finite_components` `finite sigma_A`: component values missing | fix: source c_g, b_dis, b_A, b_alpha, q_nonH, support and boundary rows with units
- `REF3730_3_beta_matrix` `beta_A`: observable response matrices missing | fix: derive B_A and W_A for each arena, then compute singular/eigenvalue norm
- `REF3730_4_R10_product` `R10 beta_source beta_test`: R10 product inputs missing | fix: derive K_X, Z_X, lambda_X, beta_source, beta_test, profile and tail envelope
- `REF3730_5_EM_Poynting` `EM/Poynting`: Hodge/constitutive variation missing | fix: derive the parent EM observable map and Poynting-balance source current

## Next Target
- `3731-Y5-R2FR-parent-JX-current-and-arena-response-matrix.md`
- Objective: derive parent `J_X` and write finite `B_A/W_A` response-matrix templates, so at least one arena can feed real `sigma_A` and `beta_A` into 3729.
