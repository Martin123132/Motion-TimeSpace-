# 3228 - Xi-clock Product Row Or Clock-tau Owner under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result.

## Result

3228 does make a mathematical move. It does not merely list a missing row.

If the observed EM kinetic coefficient owns the fine-structure readout,

```text
S_EM = -1/4 int sqrt(-g_obs) Z_A(Phi) F_obs^2,
alpha_EM proportional to Z_A^-1,
```

then the clock observable is controlled by the logarithmic derivative:

```text
|d ln alpha_EM / d tau_obs| = |d ln Z_A / d tau_obs|.
```

For the defect-norm route

```text
Z_A = Z_* + lambda_D <R_Q,R_Q>_P,
```

the chain rule gives

```text
|D_tau ln Z_A| <= 2 |lambda_D| ||R_Q|| ||D_tau R_Q|| / Z_min.
```

Near the same local root branch this becomes

```text
||R_Q|| <= ||D_m R_Q|| |Delta m| + O(Delta m^2),
||D_tau R_Q|| <= ||D_m R_Q|| |tau_clock_time| + E_transport,
```

so the direct clock product is exactly the right target:

```text
Xi_clock := C_D |Delta m tau_clock_time|
C_D := 2 |lambda_D| ||D_m R_Q||^2 / Z_min
|d ln alpha_EM / d tau_obs| <= Xi_clock + E_HO + E_transport.
```

The data side is ready:

```text
Xi_clock + E_HO + E_transport <= 2.1e-18 yr^-1   (1sigma)
Xi_clock + E_HO + E_transport <= 3.2e-18 yr^-1   (2sigma)
```

The parent-side product law is derived conditionally, but not claimable. The core missing owner is now precise:

```text
D_tau R_Q = D_m R_Q tau_clock_time + E_transport.
```

If the exact same local branch has `R_Q=0` and no linear/readout leakage, the defect-norm alpha channel is clock-silent without setting `tau_clock_time` by hand. That is a real possible route, but it is still unsigned.

Current verdict: `XI_CLOCK_PRODUCT_LAW_DERIVED_CONDITIONALLY_PARENT_OWNER_NOT_SIGNED`.

## Xi-clock Product Derivation

| step_id | claim_piece | formula | derivation_status | required_clauses | result_if_signed | failure_mode | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| XID3228_0_observable_quantity | clock observable alpha drift | \|d ln alpha_EM / d tau_obs\| | TARGET_DEFINED | observed clock time tau_obs; EM fine-structure readout alpha_EM | clock data compare directly to parent-side alpha drift | using internal flow time instead of observed clock time gives an unscored quantity | false |
| XID3228_1_EM_kinetic_owner | alpha owner | S_EM=-1/4 int sqrt(-g_obs) Z_A(Phi) F_obs^2; alpha_EM proportional to Z_A^-1 after fixed charge normalization | CONDITIONAL_EXACT | observed Maxwell subblock; fixed charge normalization; no hidden representative Weyl/disformal coefficient | d ln alpha_EM/dtau_obs = - d ln Z_A/dtau_obs | if charge normalization or Hodge/readout carries another coefficient, Xi_clock is not complete | false |
| XID3228_2_defect_norm_chain_rule | defect-norm derivative | Z_A=Z_*+lambda_D <R_Q,R_Q>_P gives \|D_tau ln Z_A\| <= 2\|lambda_D\| \|\|R_Q\|\| \|\|D_tau R_Q\|\| / Z_min | DERIVED_FROM_3222_CONTRACT_CONDITIONAL | R_Q parent object; positive Z_min; parent inner product and observed derivative domain | alpha drift is controlled by a product of residual amplitude and residual clock derivative | no parent-signed R_Q/Z_A contract means this remains a contract, not a live theorem | false |
| XID3228_3_root_taylor_product | near-root product law | \|\|R_Q\|\| <= \|\|D_m R_Q\|\| \|Delta m\| + O(Delta m^2); \|\|D_tau R_Q\|\| <= \|\|D_m R_Q\|\| \|tau_clock_time\| + transport error | DERIVED_CONDITIONALLY | same branch coordinate m; same operator norm; finite Hessian; transport identity D_tau R_Q = D_m R_Q tau_clock_time + E_transport | \|d ln alpha_EM/dtau_obs\| <= C_D \|Delta m tau_clock_time\| + E_HO + E_transport | if tau_clock_time is not the branch velocity in the same R_Q direction, the Xi reduction is not valid | false |
| XID3228_4_xi_clock_identity | direct product target | Xi_clock := C_D \|Delta m tau_clock_time\| with C_D=2\|lambda_D\|\|\|D_mR_Q\|\|^2/Z_min | PRODUCT_LAW_DERIVED_WITH_UNSIGNED_CLAUSES | XID3228_1 through XID3228_3 plus controlled higher-order/error terms | Xi_clock is the parent-side row compared to the clock bound | do not split or fit C_D/Pi_clock unless the parent action supplies the split | false |
| XID3228_5_exact_root_silence | local exact-root clock silence | R_Q=0 and D_tau R_Q finite imply D_tau ln Z_A=0 for the pure defect-norm term | EXACT_CONDITIONAL_ZERO | same local branch really satisfies R_Q=0; no linear Z_A term; no readout/Hodge coefficient leakage | the defect-norm alpha channel is locally clock-silent without setting tau_clock_time by hand | linear kinetic owner, representative leakage, or nonzero R_Q reopens the clock bound | false |

## Parent Xi-clock Contract

| clause_id | required_parent_clause | mathematical_need | current_evidence | status | why_it_matters | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| XIC3228_0_parent_EM_block | observed EM kinetic block descends as Z_A(Phi) F_obs^2 | S_EM=-1/4 int sqrt(-g_obs) Z_A F_obs^2 | 3222 contract writes the defect-norm EM block but does not source-sign it | CONTRACT_WRITTEN_NOT_PARENT_SIGNED | owns alpha rather than treating alpha as an external fitted parameter | false |
| XIC3228_1_alpha_normalization | fixed charge/readout normalization | alpha_EM proportional to Z_A^-1, with no extra clock/species coefficient | 1052/1809 warn that clock rows bound products only | UNSIGNED_NORMALIZATION | prevents hiding drift in units, charge convention, or clock species | false |
| XIC3228_2_clock_generator | observed clock time generator | D_tau is derivative with respect to tau_obs measured by the descended clock matter | 3136 gives conditional observed-coframe clock theorem | CONDITIONAL_CLOCK_THEOREM_NOT_PARENT_SIGNED | clock data score observed time, not an internal flow coordinate | false |
| XIC3228_3_same_branch_transport | same-branch transport identity | D_tau R_Q = D_m R_Q tau_clock_time + E_transport | not found as a parent row; 3227 only defines tau_clock_time product maps | MISSING_CORE_OWNER | this is the exact bridge from defect-norm alpha to clock drift | false |
| XIC3228_4_finite_remainder | finite Taylor/Hessian remainder | E_HO + E_transport bounded below the clock residual budget | 3223/3226 name finite Hessian guards but do not source coefficients | BOUND_TEMPLATE_ONLY | keeps Xi_clock from being a first-order mirage with uncontrolled second-order debt | false |
| XIC3228_5_data_comparison | clock-bound comparison row | Xi_clock + E_HO + E_transport <= B_clock | B_clock is real: 2.100000e-18 yr^-1 at 1sigma and 3.200000e-18 yr^-1 at 2sigma | DATA_SIDE_READY_PARENT_SIDE_MISSING | turns the derivation into a falsifiable local coupling bound | false |

## Xi-clock Bound Interface

| bound_id | quantity | required_bound | units | source | interpretation | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| XIB3228_0_clock_1sigma | Xi_clock + E_HO + E_transport | <= 2.100000e-18 | yr^-1 | PC3225_0_clock_1sigma / ACB1052_2 | best current 1sigma clock pressure gate | false | false |
| XIB3228_1_clock_2sigma | Xi_clock + E_HO + E_transport | <= 3.200000e-18 | yr^-1 | PC3225_1_clock_2sigma / ACB1052_2 | best current 2sigma clock pressure gate | false | false |
| XIB3228_2_exact_root_branch | defect-norm contribution to Xi_clock | 0 if R_Q=0 and no leakage | yr^-1 | derived from chain rule for lambda_D<R_Q,R_Q> | possible local silence mechanism; not active until same-branch root and no-leakage clauses are signed | false | false |
| XIB3228_3_offroot_branch | Xi_clock | C_D \|Delta m tau_clock_time\| <= B_clock - E_HO - E_transport | yr^-1 | 3226 package plus 3228 chain-rule derivation | finite branch score equation; needs parent value/bound for the left side | false | false |

## Owner Obstruction Ledger

| obstruction_id | object | what_was_derived | what_is_still_unsigned | best_next_attack | severity | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| OBS3228_0_not_just_missing | Xi_clock | the product law follows from a logarithmic derivative of Z_A and the defect-norm chain rule | parent-signed EM block, alpha normalization, clock generator, same-branch transport | derive D_tau R_Q = D_m R_Q tau_clock_time + E_transport | CORE | false |
| OBS3228_1_clock_tau_owner | tau_clock_time | observed clocks measure proper time if observed-coframe matter descent is parent-signed | the parent action has not signed the observed-coframe matter functor for clock species | promote the 3136 conditional theorem into a parent action clause or demote to closure | HIGH | false |
| OBS3228_2_alpha_owner | Z_A/alpha_EM | if alpha_EM is owned by Z_A then drift is -D_tau ln Z_A | charge normalization and no hidden Hodge/readout coefficient | write exact Maxwell-subblock readout/no-leakage clause | HIGH | false |
| OBS3228_3_data_side | clock bound | data side already supplies a numeric 2.1e-18 yr^-1 pressure gate | none on the bound itself; only theory-side product row | compare only after Xi_clock or its upper bound is parent-derived | LOW_DATA_READY | false |

## Decision

| decision_id | decision | because | claim_status | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3228_0_result | XI_CLOCK_PRODUCT_LAW_DERIVED_CONDITIONALLY_PARENT_OWNER_NOT_SIGNED | the logarithmic derivative of a defect-norm EM kinetic coefficient yields Xi_clock plus explicit higher-order/transport errors, but the parent action has not signed the EM owner, observed clock generator, or same-branch transport identity | NO_ALPHA_NO_CLOCK_NO_WEP_NO_R10_NO_LOCAL_GR_CLAIM | attack the same-branch transport identity D_tau R_Q = D_m R_Q tau_clock_time + E_transport, because that is the core bridge from MTS residual dynamics to the clock bound | false |
| DEC3228_1_next_target | 3229-Y5-R2FR-same-branch-clock-transport-identity-for-DtauRQ-under-AX1090 | without this identity Xi_clock remains a conditional product law; with it, the clock gate becomes a real parent-side bound or an exact-root silence theorem | PRIVATE_NEXT_TARGET | derive or refute D_tau R_Q = D_m R_Q tau_clock_time + E_transport from quotient/readout geometry and the EM residual branch | false |

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3228_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3228_XI_CLOCK_PRODUCT_DERIVATION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3228_PARENT_XI_CLOCK_CONTRACT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3228_XI_CLOCK_BOUND_INTERFACE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3228_OWNER_OBSTRUCTION_LEDGER.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3228_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3228_VALIDATION.csv`

## Source Register

| input_id | relative_path | exists | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC3228_00_3227_doc | 3227-Y5-R2FR-Pi-clock-or-CD-source-row-acquisition-under-AX1090.md | true | 3227 handoff selecting direct Xi_clock product row | L16:\|b_alpha*tau_clock_time\| <= 2.1e-18 yr^-1 (best current 1sigma clock row) \| L30:Xi_clock := C_D Pi_clock = C_D \|Delta m tau_clock_time\| \| L31:Xi_clock <= 2.1e-18 yr^-1 (1sigma diagnostic bound) \| L32:Xi_clock <= 3.2e-18 yr^-1 (2sigma diagnostic bound) | false |
| SRC3228_01_3227_interface | P8_Y5_R2FR_3227_CD_OR_PICLOCK_ACQUISITION_INTERFACE.csv | true | Xi_clock interface and refusal rules | L2:XIC3227_0_definition,Xi_clock,Xi_clock := C_D Pi_clock = C_D \|Delta m tau_clock_time\|,not_applicable,yr^-1 in clock-time convention after source normalization,3225/3226 finite branch plus 1052 clock product anchor,requir \| L5:XIC3227_3_direct_product_acquisition,Xi_clock,derive/source C_D \|Delta m tau_clock_time\| directly from parent clock/EM coupling,MISSING_PARENT_VALUE,yr^-1,none yet,"would avoid arbitrary splitting of C_D, Delta m, and ta \| L7:XIC3227_5_refusal_rule,claim rule,"no pass if Xi_clock is inferred by setting Pi_clock=1, tau_clock_time=H0, or Delta m=1",not_applicable,not_applicable,1052/1809/3226 guardrails,reject assumed-normalization shortcuts,AC | false |
| SRC3228_02_3225_products | P8_Y5_R2FR_3225_PRODUCT_CONSTRAINTS_FROM_ANCHORS.csv | true | real clock product bound | L2:PC3225_0_clock_1sigma,clock,C_D \|Delta m tau_clock_time\| <= product_bound_1sigma,2.100000e-18,yr^-1 in the clock-time convention,ACB1052_2,source-backed clock product bound,"C_D, Delta m, tau_clock_time individually",fal \| L3:PC3225_1_clock_2sigma,clock,C_D \|Delta m tau_clock_time\| <= product_bound_2sigma,3.200000e-18,yr^-1 in the clock-time convention,ACB1052_2,source-backed clock product bound,"C_D, Delta m, tau_clock_time individually",fal | false |
| SRC3228_03_3222_contract | 3222-Y5-R2FR-defect-norm-parent-action-contract-or-finite-alpha-coefficient-runner-under-AX1090.md | true | defect-norm parent action contract | L7:3222 turns the `R_Q` idea into an exact parent-action contract. \| L12:S_EM = -1/4 int sqrt(-g_q) [Z_* + lambda_D <R_Q,R_Q>_P] F_Q^2 \| L13:R_Q(Phi_*) = 0 \| L19:delta_m Delta Z_A \| root = 2 lambda_D <R_Q, delta_m R_Q>_P \| root = 0. | false |
| SRC3228_04_3223_formula | 3223-Y5-R2FR-RQ-source-search-or-finite-alpha-runner-smoke-inputs-under-AX1090.md | true | finite alpha formula and R_Z owner hunt | L3:Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result. \| L18:R_Z = Z_A - C_P N_Q \| L26:\|b_alpha_m\| <= 2 \|lambda_D\| \|\|D_m R_Q\|\|^2 \|Delta m\| / Z_min + O(Delta m^2). \| L37:\| SRCSEARCH3223_RZ \| R_Z = Z_A - C_P N_Q or unique Maxwell-subblock projection residual \| Z_A decomposition; EM owner contract; Maxwell kinetic inheritance; unique subblock target \| unique F2/operator-domain/readout clau | false |
| SRC3228_05_3223_formula_csv | P8_Y5_R2FR_3223_FINITE_ALPHA_BOUND_FORMULA.csv | true | machine finite alpha formula | L3:FORM3223_1_offroot_bound,finite off-root b_alpha_m,\|b_alpha_m\| <= 2 \|lambda_D\| \|\|D_m R_Q\|\|^2 \|Delta m\| / Z_min + O(Delta m^2),"lambda_D, \|\|D_m R_Q\|\|, Delta m, Z_min, units, source paths",FINITE_BOUND_READY_FOR_INPUTS,fal \| L4:FORM3223_2_alpha_residual,finite alpha residual,\|Delta alpha/alpha\| <= \|lambda_D\| \|\|D_m R_Q\|\|^2 Delta m^2 / Z_min + O(Delta m^3),same finite inputs plus readout/radiative correction bound,FINITE_BOUND_READY_FOR_INPUTS,fa \| L5:FORM3223_3_hessian_guard,defect-norm Hessian correction,G_eff >= G_mem - eta_D - eta_stress - eta_readout > 0,"G_mem, lambda_D, \|\|D_m R_Q\|\|, \|\|F_Q^2\|\| support norm, stress/readout bounds",FINITE_BOUND_READY_FOR_INPUTS,fa | false |
| SRC3228_06_3226_package | P8_Y5_R2FR_3226_CD_COEFFICIENT_PACKAGE.csv | true | C_D and Pi_clock package | L2:CD3226_0_definition,C_D,C_D := 2 \|lambda_D\| \|\|D_m R_Q\|\|^2 / Z_min,"1/[m] after chosen memory normalization, or inverse of Delta m units",compact finite coefficient controlling \|b_alpha_m\| <= C_D \|Delta m\|,definition_exac \| L3:CD3226_1_clock_product,Pi_clock := \|Delta m tau_clock_time\|,clock product projection multiplying C_D in \|dot alpha/alpha\| <= C_D Pi_clock,clock-time convention units,projection factor that must not be set to one,not_deri | false |
| SRC3228_07_3136_doc | 3136-Y5-R2FR-observed-coframe-clock-functional-owner-under-AX1090.md | true | conditional clock readout theorem | L11:=> observed clocks measure observed metric proper time. \| L47:So the clock functional is not arbitrary. If the parent action signs the observed-coframe matter functor, `R_clock` is forced. \| L51:This does not yet prove local GR, Newton, or clocks, because the parent has not signed: \| L65:R_clock theorem = formal_pass_conditional | false |
| SRC3228_08_3136_theorem | P8_Y5_R2FR_3136_OBSERVED_CLOCK_FUNCTIONAL_THEOREM.csv | true | machine clock functional theorem | L2:OCF3136_0_target,observed clock functional,R_clock is owned if ordinary clock matter is a local Lorentz matter system over e_obs and quotient-owned material constants.,"R_clock(q(Phi),gamma,A)=integral_gamma sqrt(-g_obs( \| L3:OCF3136_1_WKB_phase,clock phase from matter action,"For minimally coupled localized massive matter, the eikonal phase obeys the observed Hamilton-Jacobi equation.",g_obs^{mu nu} partial_mu S partial_nu S + m_A(theta)^2 c \| L4:OCF3136_2_proper_time,proper-time functional,The worldline action/phase extremal gives the clock elapsed time functional.,S_pp=-m_A c^2 integral d tau_clk; d tau_clk=sqrt(-g_obs_{mu nu} dx^mu dx^nu)/c,formal_pass_conditi \| L5:OCF3136_3_redshift_frequency,redshift from clock phase,"Clock comparison is a ratio of observed proper-time phase rates, not the raw internal flow parameter.","nu_A^obs ~ dS_A/dtau_clk; Delta nu/nu uses e_obs,g_obs and q | false |
| SRC3228_09_2600_doc | 2600-Y5-R2FR-Tobs-delta-tau-norm-owner-or-boundary-clock-action-clause.md | true | Tobs/delta_tau norm owner route | L3:**Status:** private nonclaim derivation checkpoint. The exact source-current response to a moving observed time generator is retained, but the coefficient owner and boundary-clock action clause are not yet parent-signed. \| L5:**Main result:** 2600 gives one real step forward and one hard stop. The real step is the exact law `Delta_JH_delta_tau <= C_Tobs_tau \|\|delta tau_obs\|\|_B`, inherited from the 1729 linear map `L_Tobs^A[delta tau]=star_A(T \| L10:\| SRC2600_00_2599_handoff_doc \| D:\\Users\\ollet\\Desktop\\Turn an intuitive research programme into a formal field-theoretic framework\\Motion-TimeSpace--main\\post-checkpoint-work\\2599-Y5-R2FR-boundary-clock-normalized-tau-o \| L11:\| SRC2600_01_2599_delta_tau_pack \| D:\\Users\\ollet\\Desktop\\Turn an intuitive research programme into a formal field-theoretic framework\\Motion-TimeSpace--main\\post-checkpoint-work\\source-intake\\mts_residuals\\P8_Y5_BOUNDAR | false |
| SRC3228_10_2600_norm | P8_Y5_TOBS_DTAU_2600_NORM_OWNER_ATTEMPT.csv | true | machine norm-owner attempt | L1:timestamp_utc,branch_id,checkpoint_id,attempt_id,object,formula,derivation_status,missing_inputs,owner_signed,score_ready,valid_for_claim,claim_allowed \| L3:2026-06-22T21:06:07.942757+00:00,MTS_R2FR_TOBS_DTAU_NORM_OR_CLOCK_ACTION_2600,2600,TON2600_1_common_domain,domain norm for delta_tau,\|\|delta tau_obs\|\|_B and \|\|tau_obs\|\|_B on the same boundary/collar class used by epsilon \| L4:2026-06-22T21:06:07.942762+00:00,MTS_R2FR_TOBS_DTAU_NORM_OR_CLOCK_ACTION_2600,2600,TON2600_2_common_codomain,codomain current norm,"\|\|star_A(T_obs(delta tau,.))\|\|_{J_A}",NOT_PARENT_OWNED,MISSING_A_EXT;MISSING_VOLUME_FORM \| L5:2026-06-22T21:06:07.942765+00:00,MTS_R2FR_TOBS_DTAU_NORM_OR_CLOCK_ACTION_2600,2600,TON2600_3_stress_envelope,observed stress-energy operator envelope,C_Tobs_tau <= C_star_measure(A_ext) sup_A \|\|T_obs\|\|_op,BOUND_TEMPLATE_ | false |

## Validation

| check_id | pass | detail |
| --- | --- | --- |
| VAL3228_00_inputs_exist | true | inputs=11 |
| VAL3228_01_chain_rule_present | true | D_tau ln Z_A defect-norm chain rule staged |
| VAL3228_02_xi_identity_present | true | Xi_clock identity derived conditionally |
| VAL3228_03_exact_root_zero_present | true | exact-root defect-norm silence clause staged |
| VAL3228_04_transport_core_missing_explicit | true | same-branch transport identity is the core missing owner |
| VAL3228_05_numeric_clock_bounds | true | numeric_clock_bounds=2 |
| VAL3228_06_claims_blocked | true | claim_rows_true=0;claim_allowed=0 |
| VAL3228_07_no_formalization_workbench_edit | true | no formalization-workbench paths are output targets |
| VAL3228_08_csv_parse | true | P8_Y5_R2FR_3228_INPUTS.csv;P8_Y5_R2FR_3228_XI_CLOCK_PRODUCT_DERIVATION.csv;P8_Y5_R2FR_3228_PARENT_XI_CLOCK_CONTRACT.csv;P8_Y5_R2FR_3228_XI_CLOCK_BOUND_INTERFACE.csv;P8_Y5_R2FR_3228_OWNER_OBSTRUCTION_LEDGER.csv;P8_Y5_R2FR_3228_DECISION.csv |
| VAL3228_09_next_target | true | 3229-Y5-R2FR-same-branch-clock-transport-identity-for-DtauRQ-under-AX1090 |

All generated rows remain `valid_for_claim=false`.
