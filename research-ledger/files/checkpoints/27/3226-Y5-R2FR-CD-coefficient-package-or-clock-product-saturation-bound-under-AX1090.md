# 3226 - C_D Coefficient Package Or Clock Product Saturation Bound under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result.

## Result

3226 packages the finite alpha branch into one coefficient:

```text
C_D := 2 |lambda_D| ||D_m R_Q||^2 / Z_min
|b_alpha_m| <= C_D |Delta m|.
```

Then the real data anchors become saturation conditions:

```text
C_D <= B_clock / Pi_clock
Pi_clock := |Delta m tau_clock_time|

C_D <= B_WEP / Pi_WEP
Pi_WEP := |Delta m tau_WEP beta_source_alpha|.
```

No projection product is assumed to be one. The saturation tables are diagnostic target curves only.

The key practical readout:

```text
If Pi_clock = 1e-6, then C_D must be <= 2.1e-12 in the clock 1sigma convention.
If Pi_WEP = 1e-6, then C_D must be <= 1.407170e-6 in the MICROSCOPE alpha/Coulomb convention.
```

So the clock product is the sharper first pressure test unless `Pi_clock` is extremely suppressed relative to `Pi_WEP`.

Current verdict: `CD_PACKAGE_DEFINED_SATURATION_BOUNDS_DERIVED_NO_COEFFICIENT_CLAIM`.

## C_D Coefficient Package

| package_id | quantity | definition | units | role | source_status | missing_for_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CD3226_0_definition | C_D | C_D := 2 \|lambda_D\| \|\|D_m R_Q\|\|^2 / Z_min | 1/[m] after chosen memory normalization, or inverse of Delta m units | compact finite coefficient controlling \|b_alpha_m\| <= C_D \|Delta m\| | definition_exact_inputs_missing | lambda_D; D_m R_Q norm; Z_min; units; source paths | false |
| CD3226_1_clock_product | Pi_clock := \|Delta m tau_clock_time\| | clock product projection multiplying C_D in \|dot alpha/alpha\| <= C_D Pi_clock | clock-time convention units | projection factor that must not be set to one | not_derived | EM-attached Delta m and tau_clock_time | false |
| CD3226_2_WEP_product | Pi_WEP := \|Delta m tau_WEP beta_source_alpha\| | WEP projection factor multiplying C_D in the alpha/Coulomb channel | selected WEP projection convention | source/test projection factor that must not inherit clock tau | not_derived | EM-attached Delta m, tau_WEP, beta_source_alpha | false |
| CD3226_3_hessian | eta_D | defect-norm Hessian correction tied to C_D plus field/support norms | memory operator correction units | keeps alpha finite branch from smuggling local-GR/Maxwell stress safety | not_derived | G_mem floor, \|\|F_Q^2\|\| support norm, stress/readout bounds | false |

## Product Saturation Bounds

| sat_id | arena | bound_source | assumed_projection_product | saturation_formula | C_D_max | units | interpretation | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SAT3226_clock1_pi_1e+00 | clock | ACB1052_2_1sigma | 1.0e+00 | C_D_max = clock_bound_1sigma / Pi_clock | 2.100000e-18 | yr^-1 divided by Pi_clock units | diagnostic target curve only; Pi_clock is not assumed | false | false |
| SAT3226_clock2_pi_1e+00 | clock | ACB1052_2_2sigma | 1.0e+00 | C_D_max = clock_bound_2sigma / Pi_clock | 3.200000e-18 | yr^-1 divided by Pi_clock units | diagnostic target curve only; Pi_clock is not assumed | false | false |
| SAT3226_WEP_pi_1e+00 | MICROSCOPE_WEP | AWP1052_0_alpha_Coulomb | 1.0e+00 | C_D_max = (eta_bound/delta_Q_alpha) / Pi_WEP | 1.407170e-12 | dimensionless divided by Pi_WEP units | diagnostic target curve only; Pi_WEP is not assumed | false | false |
| SAT3226_clock1_pi_1e-03 | clock | ACB1052_2_1sigma | 1.0e-03 | C_D_max = clock_bound_1sigma / Pi_clock | 2.100000e-15 | yr^-1 divided by Pi_clock units | diagnostic target curve only; Pi_clock is not assumed | false | false |
| SAT3226_clock2_pi_1e-03 | clock | ACB1052_2_2sigma | 1.0e-03 | C_D_max = clock_bound_2sigma / Pi_clock | 3.200000e-15 | yr^-1 divided by Pi_clock units | diagnostic target curve only; Pi_clock is not assumed | false | false |
| SAT3226_WEP_pi_1e-03 | MICROSCOPE_WEP | AWP1052_0_alpha_Coulomb | 1.0e-03 | C_D_max = (eta_bound/delta_Q_alpha) / Pi_WEP | 1.407170e-09 | dimensionless divided by Pi_WEP units | diagnostic target curve only; Pi_WEP is not assumed | false | false |
| SAT3226_clock1_pi_1e-06 | clock | ACB1052_2_1sigma | 1.0e-06 | C_D_max = clock_bound_1sigma / Pi_clock | 2.100000e-12 | yr^-1 divided by Pi_clock units | diagnostic target curve only; Pi_clock is not assumed | false | false |
| SAT3226_clock2_pi_1e-06 | clock | ACB1052_2_2sigma | 1.0e-06 | C_D_max = clock_bound_2sigma / Pi_clock | 3.200000e-12 | yr^-1 divided by Pi_clock units | diagnostic target curve only; Pi_clock is not assumed | false | false |
| SAT3226_WEP_pi_1e-06 | MICROSCOPE_WEP | AWP1052_0_alpha_Coulomb | 1.0e-06 | C_D_max = (eta_bound/delta_Q_alpha) / Pi_WEP | 1.407170e-06 | dimensionless divided by Pi_WEP units | diagnostic target curve only; Pi_WEP is not assumed | false | false |
| SAT3226_clock1_pi_1e-09 | clock | ACB1052_2_1sigma | 1.0e-09 | C_D_max = clock_bound_1sigma / Pi_clock | 2.100000e-09 | yr^-1 divided by Pi_clock units | diagnostic target curve only; Pi_clock is not assumed | false | false |
| SAT3226_clock2_pi_1e-09 | clock | ACB1052_2_2sigma | 1.0e-09 | C_D_max = clock_bound_2sigma / Pi_clock | 3.200000e-09 | yr^-1 divided by Pi_clock units | diagnostic target curve only; Pi_clock is not assumed | false | false |
| SAT3226_WEP_pi_1e-09 | MICROSCOPE_WEP | AWP1052_0_alpha_Coulomb | 1.0e-09 | C_D_max = (eta_bound/delta_Q_alpha) / Pi_WEP | 1.407170e-03 | dimensionless divided by Pi_WEP units | diagnostic target curve only; Pi_WEP is not assumed | false | false |
| SAT3226_clock1_pi_1e-12 | clock | ACB1052_2_1sigma | 1.0e-12 | C_D_max = clock_bound_1sigma / Pi_clock | 2.100000e-06 | yr^-1 divided by Pi_clock units | diagnostic target curve only; Pi_clock is not assumed | false | false |
| SAT3226_clock2_pi_1e-12 | clock | ACB1052_2_2sigma | 1.0e-12 | C_D_max = clock_bound_2sigma / Pi_clock | 3.200000e-06 | yr^-1 divided by Pi_clock units | diagnostic target curve only; Pi_clock is not assumed | false | false |
| SAT3226_WEP_pi_1e-12 | MICROSCOPE_WEP | AWP1052_0_alpha_Coulomb | 1.0e-12 | C_D_max = (eta_bound/delta_Q_alpha) / Pi_WEP | 1.407170e+00 | dimensionless divided by Pi_WEP units | diagnostic target curve only; Pi_WEP is not assumed | false | false |
| SAT3226_clock1_pi_1e-15 | clock | ACB1052_2_1sigma | 1.0e-15 | C_D_max = clock_bound_1sigma / Pi_clock | 2.100000e-03 | yr^-1 divided by Pi_clock units | diagnostic target curve only; Pi_clock is not assumed | false | false |
| SAT3226_clock2_pi_1e-15 | clock | ACB1052_2_2sigma | 1.0e-15 | C_D_max = clock_bound_2sigma / Pi_clock | 3.200000e-03 | yr^-1 divided by Pi_clock units | diagnostic target curve only; Pi_clock is not assumed | false | false |
| SAT3226_WEP_pi_1e-15 | MICROSCOPE_WEP | AWP1052_0_alpha_Coulomb | 1.0e-15 | C_D_max = (eta_bound/delta_Q_alpha) / Pi_WEP | 1.407170e+03 | dimensionless divided by Pi_WEP units | diagnostic target curve only; Pi_WEP is not assumed | false | false |

## Projection Inversion Table

| inv_id | arena | assumed_C_D | max_projection_product | formula | units | interpretation | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INV3226_clock1_CD_1e+00 | clock | 1.0e+00 | 2.100000e-18 | Pi_clock_max = clock_bound_1sigma / C_D | Pi_clock units | if C_D is this large, Pi_clock must be no larger than this target | false | false |
| INV3226_WEP_CD_1e+00 | MICROSCOPE_WEP | 1.0e+00 | 1.407170e-12 | Pi_WEP_max = (eta_bound/delta_Q_alpha) / C_D | Pi_WEP units | if C_D is this large, Pi_WEP must be no larger than this target | false | false |
| INV3226_clock1_CD_1e-03 | clock | 1.0e-03 | 2.100000e-15 | Pi_clock_max = clock_bound_1sigma / C_D | Pi_clock units | if C_D is this large, Pi_clock must be no larger than this target | false | false |
| INV3226_WEP_CD_1e-03 | MICROSCOPE_WEP | 1.0e-03 | 1.407170e-09 | Pi_WEP_max = (eta_bound/delta_Q_alpha) / C_D | Pi_WEP units | if C_D is this large, Pi_WEP must be no larger than this target | false | false |
| INV3226_clock1_CD_1e-06 | clock | 1.0e-06 | 2.100000e-12 | Pi_clock_max = clock_bound_1sigma / C_D | Pi_clock units | if C_D is this large, Pi_clock must be no larger than this target | false | false |
| INV3226_WEP_CD_1e-06 | MICROSCOPE_WEP | 1.0e-06 | 1.407170e-06 | Pi_WEP_max = (eta_bound/delta_Q_alpha) / C_D | Pi_WEP units | if C_D is this large, Pi_WEP must be no larger than this target | false | false |
| INV3226_clock1_CD_1e-09 | clock | 1.0e-09 | 2.100000e-09 | Pi_clock_max = clock_bound_1sigma / C_D | Pi_clock units | if C_D is this large, Pi_clock must be no larger than this target | false | false |
| INV3226_WEP_CD_1e-09 | MICROSCOPE_WEP | 1.0e-09 | 1.407170e-03 | Pi_WEP_max = (eta_bound/delta_Q_alpha) / C_D | Pi_WEP units | if C_D is this large, Pi_WEP must be no larger than this target | false | false |
| INV3226_clock1_CD_1e-12 | clock | 1.0e-12 | 2.100000e-06 | Pi_clock_max = clock_bound_1sigma / C_D | Pi_clock units | if C_D is this large, Pi_clock must be no larger than this target | false | false |
| INV3226_WEP_CD_1e-12 | MICROSCOPE_WEP | 1.0e-12 | 1.407170e+00 | Pi_WEP_max = (eta_bound/delta_Q_alpha) / C_D | Pi_WEP units | if C_D is this large, Pi_WEP must be no larger than this target | false | false |
| INV3226_clock1_CD_1e-15 | clock | 1.0e-15 | 2.100000e-03 | Pi_clock_max = clock_bound_1sigma / C_D | Pi_clock units | if C_D is this large, Pi_clock must be no larger than this target | false | false |
| INV3226_WEP_CD_1e-15 | MICROSCOPE_WEP | 1.0e-15 | 1.407170e+03 | Pi_WEP_max = (eta_bound/delta_Q_alpha) / C_D | Pi_WEP units | if C_D is this large, Pi_WEP must be no larger than this target | false | false |

## C_D Acquisition Targets

| target_id | target | required_row | why_first | current_status | claim_gate | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACQ3226_0_direct_CD | direct C_D package | C_D numeric value with units and source path | one compact row can feed clock/WEP/R10 propagators once projection products are available | MISSING | valid_for_claim remains false until C_D and at least one projection product are source-backed | derive/source lambda_D, D_m R_Q, Z_min or source C_D directly | false |
| ACQ3226_1_clock_projection | Pi_clock = \|Delta m tau_clock_time\| | clock projection product with units/source | clock gives the tightest numeric product anchor | MISSING | do not set Pi_clock to unity | derive clock readout/local memory normalization | false |
| ACQ3226_2_WEP_projection | Pi_WEP = \|Delta m tau_WEP beta_source_alpha\| | WEP source/test projection product with units/source | WEP provides an independent alpha/Coulomb material-channel target | MISSING | do not transfer clock tau into WEP | derive/source beta_source_alpha and tau_WEP | false |
| ACQ3226_3_unit_source_beta | beta_source_alpha under unit-source convention | \|beta_source_alpha\| <= 4.797781e-05 if the 1052 unit-source convention is used | gives a concrete beta target, but only under the named convention | NUMERIC_TARGET_NONCLAIM | requires tau_WEP and convention match before use | decide whether 1052 unit-source convention is the live WEP projection convention | false |

## Decision

| decision_id | decision | because | claim_status | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3226_0_result | CD_PACKAGE_DEFINED_SATURATION_BOUNDS_DERIVED_NO_COEFFICIENT_CLAIM | C_D packages the finite alpha coupling and product anchors define saturation curves, but no C_D or projection product is source-backed | NO_ALPHA_NO_CLOCK_NO_WEP_NO_R10_NO_LOCAL_GR_CLAIM | acquire either direct C_D or the tightest projection product Pi_clock; keep all saturation rows diagnostic | false |
| DEC3226_1_next_target | 3227-Y5-R2FR-Pi-clock-or-CD-source-row-acquisition-under-AX1090 | the product curves show that a C_D claim is impossible without at least one projection product; clock is the tightest first projection target | PRIVATE_NEXT_TARGET | try to derive Pi_clock=\|Delta m tau_clock_time\| from local memory/readout normalization; fallback to direct C_D source row | false |

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3226_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3226_CD_COEFFICIENT_PACKAGE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3226_PRODUCT_SATURATION_BOUNDS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3226_PROJECTION_INVERSION_TABLE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3226_CD_ACQUISITION_TARGETS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3226_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3226_VALIDATION.csv`

## Source Register

| input_id | relative_path | exists | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC3226_00_3225_doc | 3225-Y5-R2FR-first-real-alpha-input-acquisition-balpha-zero-or-lambdaD-DRQ-Zmin-under-AX1090.md | true | 3225 handoff and product constraints | L20:C_D := 2 \|lambda_D\| \|\|D_m R_Q\|\|^2 / Z_min \| L21:\|b_alpha_m\| <= C_D \|Delta m\| \| L29:C_D \|Delta m tau_clock_time\| <= 2.1e-18 yr^-1 (best clock 1sigma anchor) \| L30:C_D \|Delta m tau_WEP beta_source_alpha\| <= eta_bound / DeltaQ_alpha | false |
| SRC3226_01_3225_products | P8_Y5_R2FR_3225_PRODUCT_CONSTRAINTS_FROM_ANCHORS.csv | true | clock/WEP product constraints | L2:PC3225_0_clock_1sigma,clock,C_D \|Delta m tau_clock_time\| <= product_bound_1sigma,2.100000e-18,yr^-1 in the clock-time convention,ACB1052_2,source-backed clock product bound,"C_D, Delta m, tau_clock_ti \| L4:PC3225_2_WEP_alpha,MICROSCOPE_WEP,C_D \|Delta m tau_WEP beta_source_alpha\| <= eta_bound / delta_Q_abs,1.407170e-12,dimensionless product in selected WEP projection convention,AWP1052_0_alpha_Coulomb,so \| L5:PC3225_3_WEP_unit_source_beta_anchor,MICROSCOPE_WEP,"if unit source prediction convention is used, \|beta_source_alpha\| must stay below required_abs_beta_source_max",4.797781e-05,dimensionless beta_sou | false |
| SRC3226_02_3225_finite | P8_Y5_R2FR_3225_FINITE_INPUT_ACQUISITION_AUDIT.csv | true | missing finite input package | L2:FI3225_0_C_D,C_D := 2 \|lambda_D\| \|\|D_m R_Q\|\|^2 / Z_min,\|b_alpha_m\| <= C_D \|Delta m\|,MISSING,not source-backed,"lambda_D, D_m R_Q, and Z_min all remain placeholder rows",source R_Z finite coefficient p \| L3:FI3225_1_Delta_m,Delta m,finite off-root b_alpha_m branch,MISSING,not EM-attached,local amplitude machinery exists elsewhere but not tied to EM R_Q/Z_A branch,tie local lock/amplitude law to same EM b \| L6:FI3225_4_Zmin_shortcut_refusal,Z_min,denominator of finite alpha bound,MISSING,do not set by convention,alpha normalization/gauge norm owner remains unsigned; using observed alpha would be readout fit | false |
| SRC3226_03_3223_formula | P8_Y5_R2FR_3223_FINITE_ALPHA_BOUND_FORMULA.csv | true | finite alpha formula source | L3:FORM3223_1_offroot_bound,finite off-root b_alpha_m,\|b_alpha_m\| <= 2 \|lambda_D\| \|\|D_m R_Q\|\|^2 \|Delta m\| / Z_min + O(Delta m^2),"lambda_D, \|\|D_m R_Q\|\|, Delta m, Z_min, units, source paths",FINITE_BOUND_ \| L5:FORM3223_3_hessian_guard,defect-norm Hessian correction,G_eff >= G_mem - eta_D - eta_stress - eta_readout > 0,"G_mem, lambda_D, \|\|D_m R_Q\|\|, \|\|F_Q^2\|\| support norm, stress/readout bounds",FINITE_BOUND | false |
| SRC3226_04_3224_blockers | P8_Y5_R2FR_3224_FIRST_REAL_INPUT_BLOCKERS.csv | true | projection blockers | L2:BLK3224_0_first_MTS_scalar,one of: exact b_alpha_m=0 theorem switch OR finite b_alpha_m bound,without this the propagator has no MTS prediction to send into any arena,R_Z parent residual or finite lam \| L3:BLK3224_1_clock_projection,tau_clock_time,"clock rows bound b_alpha*tau, not b_alpha alone",clock readout/local Xhat normalization row,MISSING,do not divide the clock bound by an assumed tau,false,202 \| L4:BLK3224_2_WEP_projection,tau_WEP and beta_source_alpha,WEP alpha/Coulomb test needs source/test material projection,material sensitivity/source label theorem or finite prior row,MISSING,fill beta_sour | false |
| SRC3226_05_3210_amp | 3210-Y5-R2FR-scalar-nohair-amplitude-law-and-omega-zero-curl-gate-under-AX1090.md | true | local amplitude law candidate | L10:source/boundary leakage -> X amplitude -> deltaX amplitude -> omega_X curl bound. \| L21:Y_X := sqrt(E_X) \| L25:Y_X <= (a_X + sqrt(a_X^2 + 4 b_X))/2. \| L31:\|\|X\|\|_H1 <= Y_X sqrt(1/m_min^2 + 1/Z_min). | false |
| SRC3226_06_3219_hessian | 3219-Y5-R2FR-EM-F2-strict-double-zero-source-root-or-balpha-m-finite-bound-under-AX1090.md | true | Hessian/coercivity guard | L29:G_eff >= G_mem - eta_EM > 0. \| L49:\| HES3219_1_coercivity_floor \| corrected memory operator remains positive \| G_eff >= G_mem - eta_EM, eta_EM >= (1/4)\\\|lambda_F F''\\\| \\\|\\\|F_Q^2\\\|\\\|_op plus readout/radiative corrections \| MISSING_NUMER \| L52:\| HES3219_4_activation \| strict double-zero EM route activates local memory silence \| DZ3219_1 plus G_eff>0 plus intrinsic/boundary/readout source silence \| FAIL_CURRENT_CLAIM \| parent source-root, lo \| L58:\| ORB3219_0_balpha_offroot \| off-root b_alpha_m \| \\\|b_alpha_m\\\| <= \\\|lambda_F F2_m\\\| \\\|delta_m\\\| / Z_min + O(delta_m^2) \| lambda_F; F2_m=F''(m_*); delta_m amplitude; Z_min; units; source paths \| clock | false |

## Validation

| check_id | pass | detail |
| --- | --- | --- |
| VAL3226_00_inputs_exist | true | inputs=7 |
| VAL3226_01_CD_package_defined | true | C_D := 2\|lambda_D\|\|\|D_mR_Q\|\|^2/Z_min |
| VAL3226_02_saturation_numeric | true | saturation_numeric=18 |
| VAL3226_03_inversion_numeric | true | inversion_numeric=12 |
| VAL3226_04_diagnostic_only | true | claim_allowed_rows=0 |
| VAL3226_05_claims_blocked | true | claim_rows_true=0 |
| VAL3226_06_no_formalization_workbench_edit | true | no formalization-workbench paths are output targets |
| VAL3226_07_csv_parse | true | P8_Y5_R2FR_3226_INPUTS.csv;P8_Y5_R2FR_3226_CD_COEFFICIENT_PACKAGE.csv;P8_Y5_R2FR_3226_PRODUCT_SATURATION_BOUNDS.csv;P8_Y5_R2FR_3226_PROJECTION_INVERSION_TABLE.csv;P8_Y5_R2FR_3226_CD_ACQUISITION_TARGETS.csv;P8_Y5_R2FR_3226_DECISION.csv |
| VAL3226_08_next_target | true | 3227-Y5-R2FR-Pi-clock-or-CD-source-row-acquisition-under-AX1090 |

All generated rows remain `valid_for_claim=false`.
