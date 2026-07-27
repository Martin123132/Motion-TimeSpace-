# 3322 - C_i projection and composite/contact-tail gate for epsilon_grad under AX1090

Run UTC: `2026-06-27T20:10:04.594743+00:00`

## Verdict

3322 turns the previous `C_i` placeholder into an actual operator contract.

Start from the public metric readout

`g_pub[psi] = eta + S[grad psi grad psi]`.

For `psi = psi_bar + pi`, the split is

`delta g_pub = 2 S[grad psi_bar sym grad pi] + S[grad pi grad pi]`.

The first term gives the tree-level single-`pi` local residue. For an arena projection/window `Pi_i W_i` and band-limited propagator `H_pi(lambda)`, Cauchy-Schwarz gives

`|B_i_tree(lambda)| <= ||Pi_i W_i||^2 ||D S_ell H_pi(lambda) S_ell^dagger D^dagger|| epsilon_grad(lambda)^2`.

So

`C_i(lambda,S,H_pi)=||Pi_i W_i||^2 ||D S_ell H_pi(lambda) S_ell^dagger D^dagger|| x source_normalization_i`.

This is real progress: the local branch no longer has a nameless coupling fog. The remaining coupling problem is sharply isolated into projection norm, propagator normalization, and source/Newton normalization.

The second term, `S[grad pi grad pi]`, is the dangerous composite tail. It does not create a single-`pi` tree pole if the parent vacuum has no tadpole/mixing, but it can still create two-particle, contact, boundary, or anisotropic residuals. Therefore the safe no-cancellation bound is

`|R_i^MTS(lambda)| <= C_i(lambda) [epsilon_bg T_grad(lambda)+epsilon_boundary+epsilon_kernel_aniso]^2 + epsilon_composite_i(lambda)`.

No local-GR/R10/WEP/clock/orbital claim follows yet. The branch has improved from unknown to bounded-contract form.

## Source Register

- `SRC3322_0_3319_doc`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3319-Y5-R2FR-psi-coarse-graining-no-finite-public-residue-or-Bi-bound-under-AX1090.md` exists=true parse_ok=true role=linear public-readout split and composite-tail caveat
- `SRC3322_1_3320_doc`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3320-Y5-R2FR-local-first-gradient-silence-or-gradient-envelope-under-AX1090.md` exists=true parse_ok=true role=epsilon_grad exact condition and norm-bound fallback
- `SRC3322_2_3321_doc`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3321-Y5-R2FR-smoothing-kernel-scale-separation-bound-for-epsilon-grad-under-AX1090.md` exists=true parse_ok=true role=Gaussian smoothing transfer and threshold handoff
- `SRC3322_3_3321_thresholds`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3321_EPSILON_GRAD_THRESHOLD_ROWS.csv` exists=true parse_ok=true role=arena threshold formulas needing C_i and epsilon_composite
- `SRC3322_4_action_metric`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\action-principle\the-fundamental-action-of-motion-timespace-field-theory.md` exists=true parse_ok=true role=emergent metric from smoothed psi-gradient covariance and matter/EH action
- `SRC3322_5_gravity_ppn`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\gravity\motion-timespace-mts-gravity.md` exists=true parse_ok=true role=solar weak-field PPN margin language
- `SRC3322_6_compact_newton`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\gravity\gravity-as-emergent-mass-geometry-scaling-in-motion-timespace.md` exists=true parse_ok=true role=compact-system Newtonian recovery language

## Operator Bound

- `OP3322_0_public_readout_split`: object=g_pub[psi_bar+pi]; derived_statement=g_pub = eta + S[grad psi_bar grad psi_bar] + 2 S[grad psi_bar sym grad pi] + S[grad pi grad pi]; math_status=IMPORTED_FROM_3319_AND_REWRITTEN_AS_LINEAR_PLUS_COMPOSITE; claim_impact=single-pi finite local residue can only come from the linear term unless a tadpole/mixing converts the composite term into a one-particle pole; valid_for_claim=false
- `OP3322_1_linear_vertex`: object=V_i(lambda); derived_statement=V_i(lambda)=Pi_i W_i S_ell[grad psi_bar sym grad(.)] restricted to the arena band k~1/lambda; math_status=DEFINITION_FROM_PUBLIC_READOUT_AND_ARENA_PROJECTION; claim_impact=the dangerous local coupling is not a free scalar; it is the projected linear vertex of the smoothed metric readout; valid_for_claim=false
- `OP3322_2_cauchy_schwarz_gate`: object=B_i_tree; derived_statement=|B_i_tree(lambda)| <= ||Pi_i W_i||^2 ||D H_pi(lambda) D^dagger|| epsilon_grad(lambda)^2; math_status=DERIVED_OPERATOR_NORM_BOUND; claim_impact=this proves the quadratic epsilon_grad dependence once Pi_i, W_i, and H_pi are bounded operators; valid_for_claim=false
- `OP3322_3_Ci_definition`: object=C_i(lambda,S,H_pi); derived_statement=C_i(lambda,S,H_pi)=||Pi_i W_i||^2 ||D S_ell H_pi(lambda) S_ell^dagger D^dagger|| times source-normalization factors; math_status=DERIVED_RESPONSE_COEFFICIENT_DEFINITION; claim_impact=C_i is now a calculable projection/propagator/source-normalization object, not an unnamed fudge factor; valid_for_claim=false
- `OP3322_4_total_residual_bound`: object=R_i^MTS; derived_statement=|R_i^MTS(lambda)| <= C_i(lambda) [epsilon_bg T_grad(lambda)+epsilon_boundary+epsilon_kernel_aniso]^2 + epsilon_composite_i(lambda); math_status=DERIVED_NO_CANCELLATION_ENVELOPE; claim_impact=local tests can be scored by upper bounds; no favourable cancellation is allowed; valid_for_claim=false

## C_i Response Gate

- `CI3322_0_projection_norm`: quantity=||Pi_i W_i||; needed_for=PPN/R10/WEP/clock arena response; current_state=SYMBOLIC_BOUNDED_OPERATOR; pass_condition=define arena projection and source window, then prove finite norm or source a numeric upper bound; valid_for_claim=false
- `CI3322_1_propagator_norm`: quantity=||D S_ell H_pi S_ell^dagger D^dagger||; needed_for=range-dependent response coefficient; current_state=FORMULA_DERIVED_NUMERIC_VALUE_MISSING; pass_condition=parent action supplies Z_pi and M_pi^2, or a conservative band-limited propagator envelope; valid_for_claim=false
- `CI3322_2_source_normalization`: quantity=source-normalization factors; needed_for=Newton constant / matter coupling calibration; current_state=NOT_PARENT_OWNED_YET; pass_condition=derive kappa=8 pi G/c^4 or match the Poisson/Newtonian limit from psi covariance without re-inserting it silently; valid_for_claim=false
- `CI3322_3_Ci_numeric`: quantity=C_i(lambda); needed_for=claim-ready local bound comparison; current_state=BLOCKED_BY_CI3322_0_TO_CI3322_2; pass_condition=every factor in C_i has a parent source path, unit convention, and numeric or conservative upper bound; valid_for_claim=false

## Composite Tail Gate

- `TAIL3322_0_no_tadpole`: tail=epsilon_tad_i; origin=linearization of S[grad pi grad pi] around a non-stationary or mis-normalized local vacuum; zero_condition=parent vacuum is stationary and the one-point pi tadpole vanishes in the local branch; current_state=NOT_PARENT_SIGNED; claim_effect=if not zero, it can regenerate a single-pi pole and destroy the local branch; valid_for_claim=false
- `TAIL3322_1_two_particle`: tail=epsilon_loop_i; origin=two-pi exchange / loop / composite spectral branch from S[grad pi grad pi]; zero_condition=not generally zero; becomes short-range if H_pi has a mass gap or if arena projection removes the branch; current_state=MASS_GAP_OR_PROJECTION_MISSING; claim_effect=must be bounded separately from the tree epsilon_grad^2 term; valid_for_claim=false
- `TAIL3322_2_contact`: tail=epsilon_contact_i; origin=coincident or finite-size source contact term from the quadratic public readout; zero_condition=vanishes outside source support or is absorbed into calibrated local counterterms with no finite fifth-force residue; current_state=SOURCE_SIZE_COUNTERTERM_RULE_MISSING; claim_effect=R10/lab bounds need this term isolated because contact leakage can mimic a short-range force; valid_for_claim=false
- `TAIL3322_3_boundary`: tail=epsilon_boundary_i; origin=finite kernel support, integration by parts, or local patch boundary leakage; zero_condition=compact support or falloff kills boundary functional for the tested arena; current_state=BOUNDARY_RULE_PARTIAL; claim_effect=kept inside epsilon_eff until the parent local patch construction signs it away; valid_for_claim=false
- `TAIL3322_4_kernel_anisotropy`: tail=epsilon_kernel_aniso_i; origin=non-isotropic smoothing kernel or material/source anisotropy; zero_condition=isotropic kernel and isotropic first moment in the local vacuum; current_state=NOT_NUMERICALLY_BOUNDED; claim_effect=needed for WEP and clock/EM sectors where material orientation can matter; valid_for_claim=false

## Arena Threshold Formulas

- `PPN_local_GR`: residual_bound=|gamma-1|,|beta-1|,|alpha_PF| <= C_PPN epsilon_eff^2 + epsilon_composite_PPN; epsilon_eff=epsilon_bg T_grad(lambda_solar)+epsilon_boundary+epsilon_kernel_aniso; claim_gate=requires C_PPN numeric/source bound and epsilon_composite_PPN below PPN residual limits; valid_for_claim=false
- `R10_short_range`: residual_bound=|alpha_psi(lambda)| <= C_R10(lambda) epsilon_eff(lambda)^2 + epsilon_composite_R10(lambda); epsilon_eff=epsilon_bg T_grad(lambda)+epsilon_boundary+epsilon_kernel_aniso; claim_gate=requires source-backed alpha_bound(lambda), C_R10(lambda), and noncontact finite-range tail split; valid_for_claim=false
- `WEP`: residual_bound=eta_AB <= C_WEP epsilon_eff^2 |Delta q_AB| + epsilon_composite_WEP; epsilon_eff=composition-weighted local gradient leak; claim_gate=requires material response Delta q_AB and anisotropic/composite tail bound; valid_for_claim=false
- `clocks_EM_Poynting`: residual_bound=|delta nu/nu| or EM stress residual <= C_clock epsilon_eff^2 + epsilon_EM_Poynting_tail; epsilon_eff=clock/field projection of the same public metric readout; claim_gate=requires Maxwell stress/Poynting source projection and clock observable normalization; valid_for_claim=false
- `orbital_Newton`: residual_bound=|delta a/a_Newton| <= C_orb epsilon_eff^2 + epsilon_composite_orb; epsilon_eff=compact-system local branch leak; claim_gate=requires Poisson/Newton normalization and compact-source C_orb bound; valid_for_claim=false

## Promotion Gates

- `GATE3322_0_operator_bound`: claim=C_i epsilon_grad^2 tree-residue bound is derived; passed=true; reason=Cauchy/operator-norm bound follows from the linear public readout vertex and bounded arena projection/propagator; valid_for_claim=false
- `GATE3322_1_Ci_numeric`: claim=C_i is numerically/source bounded for local arenas; passed=false; reason=projection norm, propagator normalization, and matter/Newton source normalization are not yet parent-owned; valid_for_claim=false
- `GATE3322_2_composite_zero`: claim=epsilon_composite_i is zero or bounded below local-test limits; passed=false; reason=no-tadpole, mass-gap/projection, contact/counterterm, and boundary clauses remain unsigned; valid_for_claim=false
- `GATE3322_3_local_GR_pass`: claim=local GR/Newton/PPN branch passes; passed=false; reason=the bound form is now sharper, but C_i and epsilon_composite are not claim-grade; valid_for_claim=false

## Decision Ledger

- `DEC3322_0`: question=Did 3322 move beyond saying C_i is missing?; answer=yes; reason=C_i has been decomposed into arena projection, smoothing/propagator norm, and source-normalization factors with an operator-norm proof of the epsilon_grad^2 bound; next_action=derive or source the three C_i factors rather than treating C_i as a fog coefficient; valid_for_claim=false
- `DEC3322_1`: question=What is the main danger left?; answer=the composite tail; reason=S[grad pi grad pi] is harmless for single-pi tree exchange only if no tadpole/mixing appears and its two-particle/contact branch is short-range or bounded; next_action=prove no-tadpole/mass-gap/contact silence or keep epsilon_composite as explicit nuisance; valid_for_claim=false
- `DEC3322_2`: question=Where does the coupling problem now sit?; answer=inside source normalization; reason=GR itself inserts G through kappa; MTS can only claim a deeper route if the psi covariance normalization matches the Poisson/Newton limit without smuggling kappa back in; next_action=attack source normalization/Newton constant matching next; valid_for_claim=false

## Next Target

- `3323-Y5-R2FR-parent-source-normalization-and-composite-no-tadpole-gate-under-AX1090.md`: target_script=scripts/Y5_R2FR_3323_parent_source_normalization_and_composite_no_tadpole_gate.py; objective=derive the parent conditions that fix source normalization/Newton coupling and remove the composite one-particle tail, or force both into explicit nuisance bounds; must_include=Poisson limit; kappa/G normalization; no-tadpole condition; two-pi mass-gap/projection condition; contact/counterterm rule; EM/Poynting stress projection note; fallback_if_failed=local branch remains a bounded closure with explicit C_i and epsilon_composite nuisance parameters; valid_for_claim=false

## Test Notes

- This checkpoint is private and nonclaim.
- Every output row keeps `valid_for_claim=false`.
- The formalization workbench is not modified.
- `C_i` is now a calculable contract, but not yet a sourced number.
- `epsilon_composite_i` remains the main local-GR risk until no-tadpole/contact/mass-gap clauses are parent-signed.
