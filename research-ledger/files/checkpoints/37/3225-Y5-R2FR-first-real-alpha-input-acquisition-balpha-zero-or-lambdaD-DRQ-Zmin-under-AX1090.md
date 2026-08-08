# 3225 - First Real Alpha Input Acquisition: b_alpha Zero Or lambdaD/DRQ/Zmin under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result.

## Result

3225 tries to acquire the first real MTS alpha input.

The exact input is still not acquired:

```text
b_alpha_m = 0
```

is not source-signed, because `R_Z`, no-extra-`F^2`, strict EM double-zero, and readout closure are still not all owned by the parent action.

The finite standalone input is also not acquired:

```text
C_D := 2 |lambda_D| ||D_m R_Q||^2 / Z_min
|b_alpha_m| <= C_D |Delta m|
```

because `lambda_D`, `D_m R_Q`, `Z_min`, and the EM-attached `Delta m` amplitude are still missing.

But 3225 does get a real nonclaim constraint out of the data anchors:

```text
C_D |Delta m tau_clock_time| <= 2.1e-18 yr^-1       (best clock 1sigma anchor)
C_D |Delta m tau_WEP beta_source_alpha| <= eta_bound / DeltaQ_alpha
```

For the MICROSCOPE alpha/Coulomb row this gives:

```text
C_D |Delta m tau_WEP beta_source_alpha| <= 1.407170e-12
```

This is not an MTS pass. It is the first useful target inequality for the finite coupling branch.

Current verdict: `FIRST_STANDALONE_ALPHA_INPUT_NOT_ACQUIRED_PRODUCT_CONSTRAINTS_DERIVED`.

## Exact b_alpha Zero Acquisition Audit

| audit_id | target_input | required_derivation | status | missing_for_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| BZ3225_0_exact_RZ_zero | b_alpha_m = 0 | R_Z=Z_A-C_P N_Q is parent-owned, Delta Z_A=lambda_D\|\|R_Z\|\|^2, and R_Z=0 on the same local branch | NOT_ACQUIRED | parent R_Z object; same-branch root; no independent lambda_A/f(I)F_Q^2; readout closure | false |
| BZ3225_1_no_extra_F2_route | b_alpha_m = 0 by absence | unique Maxwell subblock plus operator-domain exhaustion forbids independent F_Q^2 coefficients | NOT_ACQUIRED | operator-domain exhaustion/no-hidden-visible hom theorem and radiative/readout closure | false |
| BZ3225_2_double_zero_route | b_alpha_m = 0 by strict double-zero | F_EM(m_*)=F_EM'(m_*)=0 for the EM F_Q^2 coefficient and m=m_* local lock | NOT_ACQUIRED | parent EM source-root owner; Hessian/stress/readout guards | false |
| BZ3225_3_verdict | first exact zero input | one exact-zero route source-signs all clauses | EXACT_ZERO_INPUT_NOT_ACQUIRED | source-signed exact zero theorem | false |

## Finite Input Acquisition Audit

| input_id | quantity | needed_for | current_value | source_status | why_not_acquired | next_source_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FI3225_0_C_D | C_D := 2 \|lambda_D\| \|\|D_m R_Q\|\|^2 / Z_min | \|b_alpha_m\| <= C_D \|Delta m\| | MISSING | not source-backed | lambda_D, D_m R_Q, and Z_min all remain placeholder rows | source R_Z finite coefficient package or exact zero switch | false |
| FI3225_1_Delta_m | Delta m | finite off-root b_alpha_m branch | MISSING | not EM-attached | local amplitude machinery exists elsewhere but not tied to EM R_Q/Z_A branch | tie local lock/amplitude law to same EM branch | false |
| FI3225_2_tau_clock | tau_clock_time | clock product prediction \|b_alpha_m tau_clock_time\| | MISSING | clock product bound exists but tau is not derived | clock rows bound the product only | derive clock readout/local Xhat normalization before standalone b_alpha_m | false |
| FI3225_3_tau_WEP_beta | tau_WEP * beta_source_alpha | WEP alpha/Coulomb product prediction | MISSING | not source-backed | WEP projection ledger names required beta/tau but does not provide MTS value | derive/source material projection and source-test alpha coupling | false |
| FI3225_4_Zmin_shortcut_refusal | Z_min | denominator of finite alpha bound | MISSING | do not set by convention | alpha normalization/gauge norm owner remains unsigned; using observed alpha would be readout fitting unless contracted | source parent gauge norm or keep Z_min as explicit finite input | false |

## Product Constraints From Anchors

| constraint_id | arena | derived_constraint | numeric_bound | units | source_anchor | what_is_real | what_is_missing | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PC3225_0_clock_1sigma | clock | C_D \|Delta m tau_clock_time\| <= product_bound_1sigma | 2.100000e-18 | yr^-1 in the clock-time convention | ACB1052_2 | source-backed clock product bound | C_D, Delta m, tau_clock_time individually | false | false |
| PC3225_1_clock_2sigma | clock | C_D \|Delta m tau_clock_time\| <= product_bound_2sigma | 3.200000e-18 | yr^-1 in the clock-time convention | ACB1052_2 | source-backed clock product bound | C_D, Delta m, tau_clock_time individually | false | false |
| PC3225_2_WEP_alpha | MICROSCOPE_WEP | C_D \|Delta m tau_WEP beta_source_alpha\| <= eta_bound / delta_Q_abs | 1.407170e-12 | dimensionless product in selected WEP projection convention | AWP1052_0_alpha_Coulomb | source-backed eta_bound and alpha/Coulomb delta_Q_abs | C_D, Delta m, tau_WEP, beta_source_alpha | false | false |
| PC3225_3_WEP_unit_source_beta_anchor | MICROSCOPE_WEP | if unit source prediction convention is used, \|beta_source_alpha\| must stay below required_abs_beta_source_max | 4.797781e-05 | dimensionless beta_source_alpha under 1052 convention | AWP1052_0_alpha_Coulomb | source-backed 1052 required beta threshold | MTS beta_source_alpha theorem/prior and tau_WEP | false | false |
| PC3225_4_R10_none | R10 | no numeric product constraint can be derived yet | MISSING_PROMOTED_R10_BOUND_AND_PROJECTIONS | dimensionless alpha(lambda) | RAP1052_0..2 definitions only | projection law language | tau_R10, K_X(lambda), beta_s, beta_t, promoted bound curve | false | false |

## First Real Input Decision

| decision_id | candidate_first_input | result | why | usable_progress | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| FIRST3225_0_exact_input | exact b_alpha_m=0 | not_acquired | no exact zero route is source-signed | keeps exact route as R_Z source target | try source-sign R_Z or abandon exact-zero for finite bound acquisition | false |
| FIRST3225_1_finite_input | finite C_D and Delta m | not_acquired | lambda_D, D_m R_Q, Z_min, and EM-attached Delta m remain missing | defines C_D := 2\|lambda_D\|\|\|D_mR_Q\|\|^2/Z_min as the first compact coefficient target | source C_D package or source one constituent with units | false |
| FIRST3225_2_product_constraint | real anchor-derived product constraints | acquired_as_nonclaim_constraint | clock and WEP source anchors yield numeric constraints on combined MTS products | C_D\|Delta m tau_clock\| <= 2.1e-18 yr^-1 and C_D\|Delta m tau_WEP beta_alpha\| <= eta/deltaQ | use these as target inequalities when sourcing C_D, Delta m, tau_clock, tau_WEP, beta_source_alpha | false |
| FIRST3225_3_next_target | 3226-Y5-R2FR-CD-coefficient-package-or-clock-product-saturation-bound-under-AX1090 | next | the first productive acquisition target is now C_D or a bounded product involving C_D | turn missing lambda_D/DRQ/Zmin into a single coefficient package with source/units gates | derive/source C_D directly or set explicit prior-width targets from clock/WEP products | false |

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3225_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3225_BALPHA_ZERO_ACQUISITION_AUDIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3225_FINITE_INPUT_ACQUISITION_AUDIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3225_PRODUCT_CONSTRAINTS_FROM_ANCHORS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3225_FIRST_REAL_INPUT_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3225_VALIDATION.csv`

## Source Register

| input_id | relative_path | exists | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC3225_00_3224_doc | 3224-Y5-R2FR-finite-alpha-bound-propagator-clock-WEP-R10-under-AX1090.md | true | 3224 handoff and first-input blocker | L27:or finite lambda_D, \|\|D_m R_Q\|\|, Delta m, Z_min. \| L38:\| PROP3224_0_acceptance_rule \| all \| accept prediction only if every required MTS input is numeric, finite, sourced, and valid_for_claim=true \| b_alpha_m theorem-zero switch OR finite lambda_D, \\\|\\\|D_ \| L42:\| PROP3224_4_hessian_stress_guard \| all \| G_eff >= G_mem - eta_D - eta_stress - eta_readout > 0 \| G_mem, lambda_D, \\\|\\\|D_m R_Q\\\|\\\|, \\\|\\\|F_Q^2\\\|\\\|, stress/readout bounds \| 3219/3223 Hessian guards \| al \| L63:\| SMOKE3223_1_lambda_D \| lambda_D \| MISSING_NUMERIC_OR_THEOREM_FIXED \| MISSING_OR_PLACEHOLDER \| false \| false \| false \| SCHEMA_ONLY_OR_MISSING_SOURCE \| | false |
| SRC3225_01_3224_mts | P8_Y5_R2FR_3224_MTS_ALPHA_INPUT_READINESS.csv | true | MTS alpha input readiness | L2:SMOKE3223_0_balpha_zero_switch,b_alpha_m,0,0.0,dimensionless vertical slope,MISSING_SOURCE_SIGNED_RQ,false,false,false,SCHEMA_ONLY_OR_MISSING_SOURCE,2026-06-26T21:54:04.737064+00:00 \| L3:SMOKE3223_1_lambda_D,lambda_D,MISSING_NUMERIC_OR_THEOREM_FIXED,MISSING_OR_PLACEHOLDER,Z_A per \|\|R_Q\|\|^2,MISSING_PARENT_ACTION_TERM,false,false,false,SCHEMA_ONLY_OR_MISSING_SOURCE,2026-06-26T21:54:04.7 \| L4:SMOKE3223_2_DRQ_norm,\|\|D_m R_Q\|\|,MISSING_OPERATOR_NORM,MISSING_OR_PLACEHOLDER,R_Q per m,MISSING_LINEARIZED_DEFECT_MAP,false,false,false,SCHEMA_ONLY_OR_MISSING_SOURCE,2026-06-26T21:54:04.737064+00:00 \| L5:SMOKE3223_3_delta_m,Delta m,MISSING_LOCAL_AMPLITUDE,MISSING_OR_PLACEHOLDER,m units,MISSING_SAME_BRANCH_LOCAL_LOCK_BOUND,false,false,false,SCHEMA_ONLY_OR_MISSING_SOURCE,2026-06-26T21:54:04.737064+00:00 | false |
| SRC3225_02_3224_blockers | P8_Y5_R2FR_3224_FIRST_REAL_INPUT_BLOCKERS.csv | true | first real input blockers | L2:BLK3224_0_first_MTS_scalar,one of: exact b_alpha_m=0 theorem switch OR finite b_alpha_m bound,without this the propagator has no MTS prediction to send into any arena,R_Z parent residual or finite lam \| L3:BLK3224_1_clock_projection,tau_clock_time,"clock rows bound b_alpha*tau, not b_alpha alone",clock readout/local Xhat normalization row,MISSING,do not divide the clock bound by an assumed tau,false,202 \| L4:BLK3224_2_WEP_projection,tau_WEP and beta_source_alpha,WEP alpha/Coulomb test needs source/test material projection,material sensitivity/source label theorem or finite prior row,MISSING,fill beta_sour | false |
| SRC3225_03_3224_anchors | P8_Y5_R2FR_3224_IMPORTED_BOUND_ANCHORS.csv | true | imported clock/WEP/R10 anchor rows | L4:ACB1052_2,clock,P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv,171Yb+ E3 / 171Yb+ E2,2.1e-18,3.2e-18,yr^-1,bounds b_alpha*tau_clock_time only; H0-normalized value is diagnostic unless tau_clock_t \| L5:AWP1052_0_alpha_Coulomb,MICROSCOPE_WEP,P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv,alpha/Coulomb composition channel,2.8e-15,,dimensionless eta,required_abs_beta_source_max=4.797780522732e-05,false \| L8:RAP1052_0_product_law,R10_short_range,P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv,alpha_X(lambda)=K_X^R10(lambda) beta_s(lambda) beta_t(lambda)+epsilon_tail(lambda),MISSING_PROMOTED_R10_BOUND_OR_PR | false |
| SRC3225_04_3218 | 3218-Y5-R2FR-EM-F2-vertex-owner-for-memory-slope-zero-or-balpha-m-source-row-under-AX1090.md | true | b_alpha formula and zero routes | L1:# 3218 - EM F2 Vertex Owner For Memory Slope Zero Or b_alpha_m Source Row under AX1090 \| L3:Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result. \| L10:S_EM = -1/4 int Z_A(m,q,readout) F_Q^2 \| L12:b_alpha_m := partial_m ln Z_A \| m_* | false |
| SRC3225_05_3223_formula | P8_Y5_R2FR_3223_FINITE_ALPHA_BOUND_FORMULA.csv | true | finite b_alpha formulas | L3:FORM3223_1_offroot_bound,finite off-root b_alpha_m,\|b_alpha_m\| <= 2 \|lambda_D\| \|\|D_m R_Q\|\|^2 \|Delta m\| / Z_min + O(Delta m^2),"lambda_D, \|\|D_m R_Q\|\|, Delta m, Z_min, units, source paths",FINITE_BOUND_ \| L4:FORM3223_2_alpha_residual,finite alpha residual,\|Delta alpha/alpha\| <= \|lambda_D\| \|\|D_m R_Q\|\|^2 Delta m^2 / Z_min + O(Delta m^3),same finite inputs plus readout/radiative correction bound,FINITE_BOUND \| L5:FORM3223_3_hessian_guard,defect-norm Hessian correction,G_eff >= G_mem - eta_D - eta_stress - eta_readout > 0,"G_mem, lambda_D, \|\|D_m R_Q\|\|, \|\|F_Q^2\|\| support norm, stress/readout bounds",FINITE_BOUND | false |
| SRC3225_06_1057 | P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv | true | unique Maxwell subblock status | L4:UMS1057_2_no_independent_F2,independent lambda_A F_Q^2 is inadmissible,Allowed[S_vis] contains no scalar-density operator DeltaS=-lambda_A/4 int F_Q^2 outside parent curvature norm,NOT_DERIVED_CURRENT \| L7:UMS1057_5_verdict,no-independent-F2 theorem,UMS1057_1..4 all signed => alpha_EM parent-owned by unique Maxwell subblock,FAIL_CURRENT_CLAIM_OPERATOR_DOMAIN_EXHAUSTION_REQUIRED,"current corpus has contr | false |
| SRC3225_07_1058 | P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv | true | operator-domain exhaustion status | L5:VOE1058_3_no_hidden_visible_hom,no hidden-to-visible coefficient morphisms,"Hom(C_hid,Coeff(O_vis)) = Const or absent",BLOCKED_BY_SCALAR_OBSTRUCTION,one surviving invariant scalar I_hid permits c=c0+e \| L7:VOE1058_5_verdict,visible operator-domain exhaustion theorem,VOE1058_1 through VOE1058_4 signed => no independent alpha counterterm,REJECT_CURRENT_CLAIM_RETAIN_COUNTERTERM_PRIOR,"current corpus has co | false |
| SRC3225_08_clock | P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv | true | clock alpha product bound | L1:bound_id,row_type,clock_pair,delta_K_alpha,product_bound_1sigma_yr_inv,product_bound_2sigma_yr_inv,H0_normalized_diagnostic,interpretation,standalone_balpha_ready,valid_for_claim,generated_utc \| L3:ACB1052_1,imported_clock_pair,171Yb+ E3 / 171Yb+ E2,-6.95,2.1e-18,3.2e-18,2.93296e-08,bounds b_alpha*tau_clock_time only; H0-normalized value is diagnostic unless tau_clock_time=H0*dchi_X/dN is derive \| L4:ACB1052_2,best_current,171Yb+ E3 / 171Yb+ E2,-6.95,2.1e-18,3.2e-18,2.93296e-08,bounds b_alpha*tau_clock_time only; H0-normalized value is diagnostic unless tau_clock_time=H0*dchi_X/dN is derived,false | false |
| SRC3225_09_WEP | P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv | true | WEP alpha projection bound | L1:projection_id,arena,channel,source_row,delta_Q_abs,eta_bound,unit_source_eta_prediction,overshoot_factor,required_abs_beta_source_max,missing_for_claim,score_ready,valid_for_claim,generated_utc \| L2:AWP1052_0_alpha_Coulomb,MICROSCOPE_WEP,alpha/Coulomb composition channel,WEP988_WAS651_0_alpha_Coulomb,1.989808886825e-03,2.8e-15,5.836031862511e-11,2.084297e+04,4.797780522732e-05,beta_source_alpha t | false |

## Validation

| check_id | pass | detail |
| --- | --- | --- |
| VAL3225_00_inputs_exist | true | inputs=10 |
| VAL3225_01_exact_zero_not_claimed | true | exact_claims=0 |
| VAL3225_02_finite_inputs_not_claimed | true | finite_claims=0 |
| VAL3225_03_product_constraints_numeric | true | numeric_constraints=4 |
| VAL3225_04_product_constraints_nonclaim | true | product_claims=0 |
| VAL3225_05_progress_row_written | true | anchor-derived product constraints acquired as nonclaim constraints |
| VAL3225_06_claims_blocked | true | claim_rows_true=0 |
| VAL3225_07_no_formalization_workbench_edit | true | no formalization-workbench paths are output targets |
| VAL3225_08_csv_parse | true | P8_Y5_R2FR_3225_INPUTS.csv;P8_Y5_R2FR_3225_BALPHA_ZERO_ACQUISITION_AUDIT.csv;P8_Y5_R2FR_3225_FINITE_INPUT_ACQUISITION_AUDIT.csv;P8_Y5_R2FR_3225_PRODUCT_CONSTRAINTS_FROM_ANCHORS.csv;P8_Y5_R2FR_3225_FIRST_REAL_INPUT_DECISION.csv |
| VAL3225_09_next_target | true | 3226-Y5-R2FR-CD-coefficient-package-or-clock-product-saturation-bound-under-AX1090 |

All generated rows remain `valid_for_claim=false`.
