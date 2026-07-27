# 3739 - Parent 2PN Beta Map and G_N Normalization

## Status
- `PARENT_2PN_AND_GN_MAP_DERIVED_PARENT_COEFFICIENTS_MISSING`
- The local-GR problem is now reduced to parent coefficient gates rather than a vague missing-coupling complaint.
- No local-GR, PPN, or Newton-constant claim is made until the parent coefficients are extracted or explicitly calibrated.

## Weak-Field Parent Expansion
- `EXP3739_0_metric_00` `effective_matter_metric`: g00_eff = -1 + 2*A1*X - 2*A2*X^2 + O(X^3) | A1 is the Newtonian potential normalization; A2 is the second-order lapse coefficient.
- `EXP3739_1_spatial_metric` `effective_matter_metric`: gij_eff = (1 + 2*G1*X)*delta_ij + O(X^2) | G1/A1 is the PPN gamma ratio after first-order normalization.
- `EXP3739_2_parent_field_equation` `parent_field_equation`: L_X X = kappa_X*rho_eff; quasi-static local limit nabla^2 X = kappa_X*rho_eff | kappa_X is the source response fixed by the parent kinetic/coupling normalization.
- `EXP3739_3_newton_potential_match` `newtonian_limit`: U = A1*X; nabla^2 U = A1*kappa_X*rho_eff | The first-order metric coefficient maps the parent potential X to the Newtonian potential U.

## 2PN Beta Map
- `BETA3739_0_ppn_compare` `DERIVED_ALGEBRAIC_MAP`: beta_MTS = A2/A1^2 | Compare g00_eff=-1+2*A1*X-2*A2*X^2 with PPN g00=-1+2*U-2*beta*U^2 using U=A1*X.
- `BETA3739_1_residual` `DERIVED_RESIDUAL_CONDITION`: beta_MTS - 1 = (A2-A1^2)/A1^2 | The local-GR beta residual is exactly the failure of the parent second-order coefficient to equal the square of the first-order coefficient.
- `BETA3739_2_fill_C_beta_2PN` `SYMBOLIC_FILL_VALUES_MISSING`: C_beta_2PN = abs(A2/A1^2 - 1) | This is the 3738 beta-row coefficient if A1 and A2 are finite and source-owned.
- `BETA3739_3_zero_condition` `ZERO_THEOREM_TARGET`: C_beta_2PN = 0 iff A2=A1^2 | The non-smuggled local-GR route is a parent theorem forcing A2=A1^2, not a fitted beta row.

## Newton Constant Normalization
- `GN3739_0_first_order_match` `DERIVED_ALGEBRAIC_MAP`: 4*pi*G_N_eff = A1*kappa_X | From U=A1*X and nabla^2 X=kappa_X*rho_eff, the Newtonian Poisson equation gives nabla^2 U=A1*kappa_X*rho_eff.
- `GN3739_1_action_coupling_form` `CONDITIONAL_PARENT_ACTION_MAP`: G_N_eff = A1*K_m/(4*pi*Z_X) times unit_factor_CG | If the parent local quadratic action gives Z_X*L_X X = K_m*rho_eff, then kappa_X=K_m/Z_X up to the unit/sign convention.
- `GN3739_2_derivation_vs_calibration` `ANTI_OVERCLAIM`: G_N is derived only if A1, K_m, Z_X, and unit_factor_CG are fixed by the parent; otherwise G_N is a calibrated closure constant. | This mirrors GR's coupling constant discipline: calibration is allowed for a model fit, but it is not a derivation.
- `GN3739_3_positive_attraction_gate` `SIGN_GATE_VALUES_MISSING`: A1*kappa_X > 0 | Attractive Newtonian gravity requires the first-order metric/source product to have the observed sign.

## Fill Rows for 3738
- `FILL3739_0_C_beta_2PN` `C_beta_2PN` -> `abs(A2/A1^2 - 1)` | ready only after A1 and A2 are source-owned in a fixed weak-field gauge
- `FILL3739_1_GN_eff` `G_N_eff` -> `A1*kappa_X/(4*pi)` | derivable only if parent fixes A1 and kappa_X; otherwise calibrated closure
- `FILL3739_2_rho_eff_norm` `rho_eff_norm` -> `rho_eff normalization entering kappa_X and measured-G calibration` | requires matter/source normalization and lab-G convention
- `FILL3739_3_gamma_condition` `Phi0_inv/gamma row support` -> `gamma_MTS=G1/A1; gamma residual vanishes iff G1=A1` | A1 and G1 must be extracted before gamma row can be closed

## Parent Input Ledger
- `A1` `P0`: first-order g00 parent coefficient | next: extract from parent matter metric/lapse expansion
- `A2` `P0`: second-order g00 parent coefficient | next: derive from 2PN parent metric expansion
- `G1` `P1`: first-order spatial metric coefficient | next: extract alongside A1 from spatial metric expansion
- `kappa_X` `P0`: quasi-static source response of parent potential | next: derive from parent field equation or calibrated Poisson closure
- `Z_X` `P1`: parent kinetic normalization for X | next: extract from quadratic parent action
- `K_m` `P1`: matter/source coupling to X | next: extract from matter coupling/current term
- `unit_factor_CG` `P1`: unit conversion between parent variables and SI/PPN Poisson form | next: state c/unit powers before numeric G_N comparison
- `weak_field_gauge` `P0`: coordinate/gauge convention for PPN comparison | next: derive gauge map rather than comparing raw coordinates

## Theorem Rows
- `THM3739_0_beta_map` `DERIVED_ALGEBRAIC_MAP`: For g00_eff=-1+2*A1*X-2*A2*X^2 and U=A1*X, the PPN beta parameter is beta=A2/A1^2. | This turns the vague 2PN beta blocker into a concrete parent-coefficient equality.
- `THM3739_1_beta_zero` `ZERO_THEOREM_TARGET`: Local GR beta recovery follows if the parent action or quotient geometry proves A2=A1^2 in the local weak-field gauge. | This is the clean no-fit route for the beta row.
- `THM3739_2_gn_map` `DERIVED_ALGEBRAIC_MAP`: The effective Newton constant obeys 4*pi*G_N_eff=A1*kappa_X in the matched Poisson limit. | MTS can only claim to derive G_N if the parent fixes both factors rather than calibrating them.
- `THM3739_3_gr_reduction_conditions` `LOCAL_GR_CONDITION_SET`: A minimal local-GR gate is A1 nonzero, G1=A1, A2=A1^2, positive A1*kappa_X, no preferred-frame leakage, and controlled boundary/tail terms. | This is a compact target list for actual derivation, not an empirical handwave.
- `THM3739_4_claim_gate` `ANTI_OVERCLAIM`: This checkpoint derives the algebraic gates but does not source the parent coefficients. | No local-GR, PPN, or Newton-constant pass is claimed.

## Decisions
- `DEC3739_0_progress` `LOCAL_GR_GATE_REDUCED_TO_PARENT_COEFFICIENTS` | The beta and Newton-G problems are now concrete coefficient equalities: A2=A1^2 and 4*pi*G_N=A1*kappa_X.
- `DEC3739_1_GN_stance` `G_N_DERIVATION_REQUIRES_PARENT_FIXING` | If the parent does not fix A1 and kappa_X, MTS may still calibrate G_N like GR, but must not call that a derivation.
- `DEC3739_2_next` `NEXT_EXTRACT_PARENT_ACTION_COEFFICIENTS` | The best next move is to hunt the corpus/action notes for the actual A1, A2, G1, kappa_X, Z_X, and K_m coefficients.

## Next Target
- `3740-Y5-R2FR-parent-action-coefficient-extraction-A1-A2-G1-kappa.md`
- Objective: search and extract the parent action/effective metric coefficients A1, A2, G1, kappa_X, Z_X, and K_m from the corpus or mark them as calibrated closure inputs
