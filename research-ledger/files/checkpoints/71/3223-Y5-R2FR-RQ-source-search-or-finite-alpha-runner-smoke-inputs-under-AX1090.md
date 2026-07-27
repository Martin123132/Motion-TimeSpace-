# 3223 - RQ Source Search Or Finite Alpha Runner Smoke Inputs under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result.

## Result

3223 performs a bounded source search over the files that actually matter for the `R_Q` defect-norm route.

Result:

```text
No candidate R_Q is source-signed yet.
```

But the search is informative rather than empty:

```text
R_Z = Z_A - C_P N_Q
```

is still the best alpha/coupling owner target because it attaches directly to the EM kinetic coefficient. `R_W` and `R_H` are better treated as second-lane guards for current/stress/readout safety. `R_theta` supports the charge/conservation route but does not own the Maxwell kinetic coefficient.

Since no exact `R_Q` source row exists, 3223 stages the finite branch instead:

```text
|b_alpha_m| <= 2 |lambda_D| ||D_m R_Q||^2 |Delta m| / Z_min + O(Delta m^2).
```

The smoke runner deliberately refuses claims because all needed finite inputs remain placeholder/nonclaim.

Current verdict: `NO_RQ_SOURCE_SIGNED_FINITE_ALPHA_SMOKE_RUNNER_STAGED`.

## RQ Source Search

| search_id | candidate | positive_hits | blocking_hits | result | source_signed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRCSEARCH3223_RZ | R_Z = Z_A - C_P N_Q or unique Maxwell-subblock projection residual | Z_A decomposition; EM owner contract; Maxwell kinetic inheritance; unique subblock target | unique F2/operator-domain/readout clauses remain not derived; scalar f(I)F_Q^2 countermodel survives | RZ_TEMPLATE_FOUND_NOT_PARENT_SIGNED | false | false |
| SRCSEARCH3223_RW | R_W^nu = nabla_mu(Z_*F_Q^{mu nu}) - J_Q^nu | Maxwell equation closure and current conservation support exist | current owner/source normalization and alpha kinetic coefficient are unsigned | RW_CURRENT_SUPPORT_NOT_KINETIC_OWNER | false | false |
| SRCSEARCH3223_RH | R_H = Hodge/coframe/readout descent residual | readout/Hodge channel is named and guarded | observed Hodge/readout descent remains not parent-signed; Poynting channel remains separate | RH_STRESS_READOUT_GUARD_FOUND_NOT_DERIVED | false | false |
| SRCSEARCH3223_RTHETA | R_theta = d_rel J_B or nabla_mu J_Q^mu | relative/phase-current conservation support exists | charge unit/level and Maxwell kinetic coefficient ownership are not derived | RTHETA_CONSERVATION_SUPPORT_NOT_ALPHA_OWNER | false | false |
| SRCSEARCH3223_VERDICT | promote a source-signed R_Q | several templates and conditional contracts exist | no row supplies parent object + EM coefficient attachment + same-branch root + Hessian/stress/readout closure | NO_RQ_SOURCE_SIGNED_BUILD_FINITE_ALPHA_SMOKE_INPUTS | false | false |

## RQ Candidate Scorecard

| candidate_id | candidate | parent_object | coefficient_attachment | same_branch_root | hessian_bound | stress_readout | overall | next_use | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SCORE3223_RZ | R_Z coefficient residual | partial | best | missing | missing | missing | best_alpha_owner_target_not_signed | first target if one more source hunt is attempted | false |
| SCORE3223_RW | R_W Ward-current mismatch | partial | weak | conditional | missing | partial_current_only | use_as_Maxwell_current_guard_not_alpha_owner | second-lane guard after R_Z | false |
| SCORE3223_RH | R_H Hodge/readout residual | missing | readout_only | missing | missing | best_stress_guard_target | needed_for_Poynting_not_alpha_zero | stress/readout residual lane | false |
| SCORE3223_RTHETA | R_theta phase-current conservation | partial | missing | conditional_conservation | missing | not_enough | charge_route_support_not_coupling_owner | charge/conservation branch, not immediate b_alpha zero | false |

## Finite Alpha Bound Formula

| formula_id | quantity | formula | inputs_required | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| FORM3223_0_exact_root | b_alpha_m at exact defect root | b_alpha_m = partial_m ln Z_A = 0 if Delta Z_A=lambda_D \|\|R_Q\|\|^2 and R_Q=0 exactly | source-signed R_Q, no linear defect, no independent coefficient, readout closure | THEOREM_SHAPE_ONLY | false |
| FORM3223_1_offroot_bound | finite off-root b_alpha_m | \|b_alpha_m\| <= 2 \|lambda_D\| \|\|D_m R_Q\|\|^2 \|Delta m\| / Z_min + O(Delta m^2) | lambda_D, \|\|D_m R_Q\|\|, Delta m, Z_min, units, source paths | FINITE_BOUND_READY_FOR_INPUTS | false |
| FORM3223_2_alpha_residual | finite alpha residual | \|Delta alpha/alpha\| <= \|lambda_D\| \|\|D_m R_Q\|\|^2 Delta m^2 / Z_min + O(Delta m^3) | same finite inputs plus readout/radiative correction bound | FINITE_BOUND_READY_FOR_INPUTS | false |
| FORM3223_3_hessian_guard | defect-norm Hessian correction | G_eff >= G_mem - eta_D - eta_stress - eta_readout > 0 | G_mem, lambda_D, \|\|D_m R_Q\|\|, \|\|F_Q^2\|\| support norm, stress/readout bounds | FINITE_BOUND_READY_FOR_INPUTS | false |

## Finite Alpha Smoke Inputs

| input_id | quantity | value | units | source_path | activation | schema_valid | numeric_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SMOKE3223_0_balpha_zero_switch | b_alpha_m | 0 | dimensionless vertical slope | MISSING_SOURCE_SIGNED_RQ | requires source-signed exact defect root | true | false | false |
| SMOKE3223_1_lambda_D | lambda_D | MISSING_NUMERIC_OR_THEOREM_FIXED | Z_A per \|\|R_Q\|\|^2 | MISSING_PARENT_ACTION_TERM | finite off-root branch | true | false | false |
| SMOKE3223_2_DRQ_norm | \|\|D_m R_Q\|\| | MISSING_OPERATOR_NORM | R_Q per m | MISSING_LINEARIZED_DEFECT_MAP | finite off-root and Hessian branch | true | false | false |
| SMOKE3223_3_delta_m | Delta m | MISSING_LOCAL_AMPLITUDE | m units | MISSING_SAME_BRANCH_LOCAL_LOCK_BOUND | finite off-root branch | true | false | false |
| SMOKE3223_4_Z_min | Z_min | MISSING_POSITIVE_DENOMINATOR | EM kinetic normalization | MISSING_ALPHA_DENOMINATOR_OWNER | finite off-root branch | true | false | false |
| SMOKE3223_5_tau_clock | tau_clock | MISSING_CLOCK_PROJECTION_FACTOR | time/projection units | P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv | clock comparison | true | false | false |
| SMOKE3223_6_tau_WEP_beta | tau_WEP and beta_source_alpha | MISSING_WEP_SOURCE_TEST_PROJECTION | dimensionless/projection units | P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv | WEP comparison | true | false | false |
| SMOKE3223_7_tau_R10 | tau_R10 | MISSING_R10_SOURCE_TEST_PROJECTION | length/projection units | P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv | R10 comparison | true | false | false |
| SMOKE3223_8_eta_stress_readout | eta_stress + eta_readout | MISSING_STRESS_READOUT_BOUND | operator/alpha correction units | MISSING_HODGE_STRESS_READOUT_SOURCE | Maxwell stress and observed alpha guard | true | false | false |

## Alpha Smoke Runner Results

| run_id | input_rows | schema_valid_rows | numeric_ready_rows | claim_ready_rows | comparison_status | claim_allowed | reason | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN3223_0_schema | 9 | 9 | 0 | 0 | schema_smoke_only | false | finite alpha runner inputs are structurally staged but numeric/source-backed values are missing | false |
| RUN3223_1_zero_switch | 1 | 1 | 0 | 0 | inactive | false | R_Q exact root is not source-signed | false |

## Decision

| decision_id | decision | because | claim_status | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3223_0_result | NO_RQ_SOURCE_SIGNED_FINITE_ALPHA_SMOKE_RUNNER_STAGED | bounded source search found templates/support for R_Z, R_W, R_H, and R_theta, but no candidate has parent object + EM coefficient attachment + same-branch root + Hessian/stress/readout closure | NO_BALPHA_M_ZERO_NO_ALPHA_RUNNER_CLAIM_NO_MAXWELL_STRESS_NO_LOCAL_GR_CLAIM | turn finite formulas into a reusable alpha-bound propagator and start filling real values only when source-backed | false |
| DEC3223_1_next_target | 3224-Y5-R2FR-finite-alpha-bound-propagator-clock-WEP-R10-under-AX1090 | the derivation route is now exact but unsigned; practical progress is to make the finite branch executable without claims | PRIVATE_NEXT_TARGET | implement a propagator for b_alpha_m bounds into clock/WEP/R10 products using only claim-valid numeric rows | false |

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3223_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3223_RQ_SOURCE_SEARCH.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3223_RQ_CANDIDATE_SCORECARD.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3223_FINITE_ALPHA_BOUND_FORMULA.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3223_FINITE_ALPHA_SMOKE_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3223_ALPHA_SMOKE_RUNNER_RESULTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3223_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3223_VALIDATION.csv`

## Source Register

| input_id | relative_path | exists | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC3223_00_3222_doc | 3222-Y5-R2FR-defect-norm-parent-action-contract-or-finite-alpha-coefficient-runner-under-AX1090.md | true | 3222 handoff and RQ target list | L33:Current verdict: `DEFECT_NORM_PARENT_ACTION_CONTRACT_EXACT_BUT_NOT_SOURCE_SIGNED`. \| L52:\| RQ3222_0_Ward_current_mismatch \| R_W^nu = nabla_mu(Z_* F_Q^{mu nu}) - J_Q^nu \| on-shell Maxwell/Ward residual root gives \\\|\\\|R_W\\\|\\\|^2 double-zero \| connects directly to Maxwell equation and source- \| L54:\| RQ3222_2_Hodge_descent_defect \| R_H = *_obs(q(Phi)) - *_EM,parent or coframe/Hodge descent residual \| readout/Hodge root can protect alpha readout and part of stress/Poynting channel \| directly atta \| L55:\| RQ3222_3_Maxwell_subblock_residual \| R_Z = Z_A - C_P N_Q or projection residual of unique parent Maxwell subblock \| if unique subblock residual vanishes, independent EM coefficient leakage becomes a \| L56:\| RQ3222_4_selected_target \| two-lane target: R_Z for coefficient ownership plus R_H/R_W for stress-current safety \| R_Z attacks b_alpha_m; R_H/R_W attacks Maxwell stress/Poynting/readout leakage \| av | false |
| SRC3223_01_3222_contract | P8_Y5_R2FR_3222_PARENT_ACTION_DEFECT_NORM_CONTRACT.csv | true | parent-action defect-norm contract clauses | L2:DNC3222_0_parent_object,R_Q is a parent-action object,"R_Q=R_Q[Phi,A_Q,J_Q,*_q,theta_Q] is defined before observed readout and before local scoring",prevents an after-the-fact penalty term from masque \| L3:DNC3222_1_action_term,defect norm enters the EM kinetic coefficient,"S_EM=-1/4 int sqrt(-g_q) [Z_* + lambda_D <R_Q,R_Q>_P] F_Q^2",attaches the double-zero to the EM F_Q^2 vertex rather than a generic  \| L9:DNC3222_7_verdict,promote defect-norm EM source-root owner,DNC3222_0 through DNC3222_6 all source-signed,this is the full no-smuggling contract,CONTRACT_EXACT_NOT_LIVE,parent R_Q source and finite Hes | false |
| SRC3223_02_3222_candidates | P8_Y5_R2FR_3222_RQ_CANDIDATE_ROUTES.csv | true | RQ candidate definitions | L2:RQ3222_0_Ward_current_mismatch,R_W^nu = nabla_mu(Z_* F_Q^{mu nu}) - J_Q^nu,on-shell Maxwell/Ward residual root gives \|\|R_W\|\|^2 double-zero,connects directly to Maxwell equation and source-current norm \| L4:RQ3222_2_Hodge_descent_defect,"R_H = *_obs(q(Phi)) - *_EM,parent or coframe/Hodge descent residual",readout/Hodge root can protect alpha readout and part of stress/Poynting channel,directly attacks th \| L5:RQ3222_3_Maxwell_subblock_residual,R_Z = Z_A - C_P N_Q or projection residual of unique parent Maxwell subblock,"if unique subblock residual vanishes, independent EM coefficient leakage becomes a squa | false |
| SRC3223_03_3222_runner | P8_Y5_R2FR_3222_FINITE_ALPHA_RUNNER_SPEC.csv | true | finite alpha runner handoff | L2:AR3222_0_theorem_zero_switch,b_alpha_m_zero_from_defect_norm,0,DNC3222_0..6 source-signed with no linear defect and finite Hessian/stress/readout guards,INACTIVE_NONCLAIM,use finite b_alpha_m bound,fa \| L7:AR3222_5_arena_projection,"tau_clock, tau_WEP, tau_R10, beta_source_alpha",source-backed projection factors for empirical arenas,finite b_alpha_m or theorem-zero switch is available,MISSING_FOR_CLAIM, | false |
| SRC3223_04_3218_ZA | 3218-Y5-R2FR-EM-F2-vertex-owner-for-memory-slope-zero-or-balpha-m-source-row-under-AX1090.md | true | Z_A decomposition and countermodels | L19:Z_A = \| L20:C_P N_Q \| L21:+ lambda_A \| L22:+ f_m(m) \| L31:[ partial_m(C_P N_Q) | false |
| SRC3223_05_3219_bound | 3219-Y5-R2FR-EM-F2-strict-double-zero-source-root-or-balpha-m-finite-bound-under-AX1090.md | true | off-root b_alpha and Hessian guard | L29:G_eff >= G_mem - eta_EM > 0. \| L49:\| HES3219_1_coercivity_floor \| corrected memory operator remains positive \| G_eff >= G_mem - eta_EM, eta_EM >= (1/4)\\\|lambda_F F''\\\| \\\|\\\|F_Q^2\\\|\\\|_op plus readout/radiative corrections \| MISSING_NUMER \| L52:\| HES3219_4_activation \| strict double-zero EM route activates local memory silence \| DZ3219_1 plus G_eff>0 plus intrinsic/boundary/readout source silence \| FAIL_CURRENT_CLAIM \| parent source-root, lo \| L58:\| ORB3219_0_balpha_offroot \| off-root b_alpha_m \| \\\|b_alpha_m\\\| <= \\\|lambda_F F2_m\\\| \\\|delta_m\\\| / Z_min + O(delta_m^2) \| lambda_F; F2_m=F''(m_*); delta_m amplitude; Z_min; units; source paths \| clock \| L100:\| VAL3219_02_hessian_guard \| true \| G_eff >= G_mem - eta_EM \| | false |
| SRC3223_06_1055_contract | P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv | true | single parent action and EM owner contract | L3:PAC1055_1_EM_owner,observed EM connection and kinetic normalization are owned by fixed representation/topological data,"S_EM = -1/(4 g_*^2(ell_EM)) int sqrt(-g_obs(q)) F_Q^2 + S_int[A_Q,J_Q(theta_A)], \| L7:PAC1055_5_radiative_readout_closure,renormalized/effective/readout maps preserve quotient and constant-sector ownership,"S_vis^eff and clock/readout maps remain in Alg[q_loc,Theta_rep,Level_EM] with n \| L8:PAC1055_6_single_parent_action,"one parent variational object owns geometry, EM, matter, source, and readout","S_parent = S_geom[Phi] + S_hidden[Phi] + S_EM[q(Phi),A_Q,ell_EM] + sum_A S_A[Psi_A,q(Phi) | false |
| SRC3223_07_642_descent | P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv | true | Maxwell descent and current status | L3:MD642_1_Gauss_Ampere,d*F = g_EM^2 *J,variation of assumed Maxwell action,closure_success_not_parent_success,"g_EM, source current normalization, and observed-coframe Hodge star",false \| L4:MD642_2_current_conservation,d*J = 0 or nabla_mu J^mu = 0,Noether/Ward current from compact phase,conditional_support,identification of relative boundary current with EM source current,false \| L6:MD642_4_alpha_constant,alpha_EM = g_EM^2/(4 pi hbar c),demand quotient-invariant or topological g_EM,blocked,"no sourced level, index, anomaly, monopole, or Ward theorem fixes g_EM",false | false |
| SRC3223_08_765_mki | P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv | true | Maxwell kinetic inheritance gates | L3:MKI765_1_norm,Parent norm fixes the T_Q length.,"<T_Q,T_Q>_P=N_Q is fixed by a lattice/metric/symplectic form and invariant under vertical representatives",not_signed,rescale T_Q and compensate with c \| L4:MKI765_2_unique_F2,No independent Maxwell kinetic invariant exists.,there is no allowed Delta S=-lambda_A/4 int F_Q^2 beyond the parent curvature norm,failed_current_corpus,g_EM^{-2}=C_P N_Q + lambda_ \| L6:MKI765_4_readout,The observed Hodge star and hbar/c readout are quotient-fixed.,the dimensionless alpha readout has no residual coframe/clock dependence,not_signed,clock and spectroscopy channels see  \| L7:MKI765_5_total,Maxwell kinetic inheritance can be promoted.,MKI765_0..MKI765_4 pass together,blocked,finite kappa_alpha source fill remains required,false,2026-06-12T00:12:57+00:00 | false |
| SRC3223_09_988_emlock | P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv | true | EM lock/readout theorem gates | L3:EMLOCK988_1_unique_Maxwell_F2,observed F_Q^2 is inherited only from the parent curvature norm,g_EM is fixed by the parent norm instead of an independent alpha source,failed_current_corpus,lambda_A F_Q \| L5:EMLOCK988_3_readout_descent,"Hodge star, coframe, and hbar*c readout are quotient-fixed for dimensionless alpha_EM",clock/spectroscopy alpha drift cannot re-enter through units,not_parent_signed,cofra \| L7:EMLOCK988_5_theorem_verdict,EMLOCK988_0 through EMLOCK988_4 are all parent-signed,b_theta_alpha_EM=0 and both WEP alpha/Coulomb and clock alpha channels close structurally,conditional_exact_but_not_pr | false |
| SRC3223_10_1057_unique | P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv | true | unique Maxwell subblock | L2:UMS1057_0_target,unique observed Maxwell subblock,"S_EM[A_Q] = -C_P N_Q/4 int sqrt(-g_obs) F_Q^2, with no independent lambda_A F_Q^2",TARGET_SHARP,would follow from parent curvature-norm exhaustion pl \| L4:UMS1057_2_no_independent_F2,independent lambda_A F_Q^2 is inadmissible,Allowed[S_vis] contains no scalar-density operator DeltaS=-lambda_A/4 int F_Q^2 outside parent curvature norm,NOT_DERIVED_CURRENT \| L7:UMS1057_5_verdict,no-independent-F2 theorem,UMS1057_1..4 all signed => alpha_EM parent-owned by unique Maxwell subblock,FAIL_CURRENT_CLAIM_OPERATOR_DOMAIN_EXHAUSTION_REQUIRED,"current corpus has contr | false |
| SRC3223_11_1058_domain | P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv | true | operator-domain exhaustion | L2:VOE1058_0_target,visible operator-domain exhaustion,"Allowed[S_vis] = Image(ParentGenerate[q_loc, F_parent, theta_rep, topological levels]) and no additional local visible counterterm algebra is admit \| L5:VOE1058_3_no_hidden_visible_hom,no hidden-to-visible coefficient morphisms,"Hom(C_hid,Coeff(O_vis)) = Const or absent",BLOCKED_BY_SCALAR_OBSTRUCTION,one surviving invariant scalar I_hid permits c=c0+e \| L7:VOE1058_5_verdict,visible operator-domain exhaustion theorem,VOE1058_1 through VOE1058_4 signed => no independent alpha counterterm,REJECT_CURRENT_CLAIM_RETAIN_COUNTERTERM_PRIOR,"current corpus has co | false |
| SRC3223_12_1091_domain | 1091-Y5-R10-parent-operator-domain-no-hidden-visible-hom-theorem-or-MOMS-closure.md | true | scalar obstruction and finite b_alpha route | L25:\| ODH1091_2_scalar_obstruction \| surviving scalar kills the theorem \| if I in O(C_hid)^inv and dI != 0, then c_I=c0+epsilon I defines a nonconstant visible coefficient morphism \| COUNTEREXAMPLE_PROVED \| L29:\| ODH1091_6_verdict \| parent operator-domain no-hidden-visible-hom theorem is derived \| ODH1091_1 plus no scalar obstruction plus product/sequester plus radiative/readout closure \| THEOREM_NOT_DERIVED \| L51:\| FR1091_0_b_alpha \| b_alpha \| source_backed_clock_product_only \| \\\|b_alpha*tau_clock_time\\\| <= 2.1e-18 yr^-1 at 1sigma from 1051 Yb E3/E2 row \| tau_clock_time; Xhat normalization; WEP/R10 source-test \| L71:\| CG1091_0_operator_domain \| no hidden-visible hom theorem \| false \| false \| ODH1091_6_verdict=THEOREM_NOT_DERIVED_CURRENT_CORPUS \| | false |
| SRC3223_13_459B_phase | 459B-Andersen-charge-amplitude-phase-current-gate.md | true | phase-current conservation route | L119:\| PC0_parent_phase_variable \| theta_Q is a compact carrier phase of the motion-time-space state \| charge sign becomes a phase orientation rather than an inserted +/- label \| theta_Q appears in the par \| L120:\| PC1_conserved_current \| nabla_mu J_Q^mu = 0 \| charge conservation \| Noether/Ward identity or topological current from the same parent variables \| not_derived \| positive/negative charge is renamed, n \| L123:\| PC4_Maxwell_limit \| coarse-grained carrier equations reduce to Maxwell equations \| EM field law rather than only Coulomb pair force \| Gauss, no-monopole, Faraday, and Ampere-Maxwell equations in one \| L131:theta_Q compact phase \| L132:J_Q^mu derived current | false |
| SRC3223_14_287_current | 287-boundary-current-charge-owner-attempt.md | true | relative boundary current | L28:No promotion yet. \| L79:d_rel J_B = \| L90:Q_B[D] = integral_D j_3 - integral_boundaryD b_2. \| L96:delta_eta Q_B[D] = 0. \| L108:R = Q_B / Q_*. | false |
| SRC3223_15_288_level | 288-k9-Ward-index-level-attempt.md | true | level/index obstruction | L46:rank is not a Ward identity. \| L52:Q_*, \| L53:integral periods, \| L93:\| BF/Chern-Simons level \| integral periods \| level is free unless anomaly/Ward cancellation fixes `9` \| \| L113:\| integral period structure \| fail \| `Q_*` remains free \| | false |
| SRC3223_16_alpha_clock | P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv | true | clock alpha product source anchor | L1:bound_id,row_type,clock_pair,delta_K_alpha,product_bound_1sigma_yr_inv,product_bound_2sigma_yr_inv,H0_normalized_diagnostic,interpretation,standalone_balpha_ready,valid_for_claim,generated_utc \| L2:ACB1052_0,imported_clock_pair,27Al+ / 199Hg+,2.95,3.9e-17,6.2e-17,5.44693e-07,bounds b_alpha*tau_clock_time only; H0-normalized value is diagnostic unless tau_clock_time=H0*dchi_X/dN is derived,false, \| L3:ACB1052_1,imported_clock_pair,171Yb+ E3 / 171Yb+ E2,-6.95,2.1e-18,3.2e-18,2.93296e-08,bounds b_alpha*tau_clock_time only; H0-normalized value is diagnostic unless tau_clock_time=H0*dchi_X/dN is derive \| L4:ACB1052_2,best_current,171Yb+ E3 / 171Yb+ E2,-6.95,2.1e-18,3.2e-18,2.93296e-08,bounds b_alpha*tau_clock_time only; H0-normalized value is diagnostic unless tau_clock_time=H0*dchi_X/dN is derived,false | false |
| SRC3223_17_alpha_WEP | P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv | true | WEP alpha projection anchor | L2:AWP1052_0_alpha_Coulomb,MICROSCOPE_WEP,alpha/Coulomb composition channel,WEP988_WAS651_0_alpha_Coulomb,1.989808886825e-03,2.8e-15,5.836031862511e-11,2.084297e+04,4.797780522732e-05,beta_source_alpha t \| L3:AWP1052_1_surface_binding,MICROSCOPE_WEP,surface/binding composition channel,WEP988_WAS651_1_surface_binding,3.306456347405e-03,2.8e-15,9.697707515141e-11,3.463467e+04,2.887280314062e-05,binding coeff \| L4:AWP1052_2_clock_screen_warning,cross_arena_policy,clock-screen-only branch,WEP988_WAS651_2_clock_screen_only; JAV988_3_cross_arena_policy,not_applicable,2.8e-15,not_applicable,not_applicable,not_appli | false |
| SRC3223_18_alpha_R10 | P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv | true | R10 alpha projection anchor | L2:RAP1052_0_product_law,R10_short_range,alpha_X(lambda)=K_X^R10(lambda) beta_s(lambda) beta_t(lambda)+epsilon_tail(lambda),BETA1035_0_product_law,review-candidate nonclaim R10 bound curve,lambda_X; Z_X; \| L3:RAP1052_1_tau_R10,R10_short_range,tau_R10 := normalized test-leg/material/readout projection under selected Yukawa profile convention,TAUR1033_2_tau_definition; TAUR1033_6_verdict,definition-only tau_ \| L4:RAP1052_2_clock_to_R10_transfer,clock_to_R10_transfer,clock product bound cannot determine alpha_X(lambda) without beta_s beta_t and tau_R10,1051 claim gate plus 1035/1033 projection rows,\|b_alpha*tau | false |

## Validation

| check_id | pass | detail |
| --- | --- | --- |
| VAL3223_00_inputs_exist | true | inputs=19 |
| VAL3223_01_no_RQ_source_signed | true | source_signed_count=0 |
| VAL3223_02_candidates_scored | true | SCORE3223_RZ;SCORE3223_RW;SCORE3223_RH;SCORE3223_RTHETA |
| VAL3223_03_finite_formula_staged | true | off-root b_alpha_m bound formula written |
| VAL3223_04_smoke_schema_valid | true | smoke_rows=9 |
| VAL3223_05_runner_refuses_claim | true | claim_allowed=false for all runner rows |
| VAL3223_06_claims_blocked | true | claim_rows_true=0 |
| VAL3223_07_no_formalization_workbench_edit | true | no formalization-workbench paths are output targets |
| VAL3223_08_csv_parse | true | P8_Y5_R2FR_3223_INPUTS.csv;P8_Y5_R2FR_3223_RQ_SOURCE_SEARCH.csv;P8_Y5_R2FR_3223_RQ_CANDIDATE_SCORECARD.csv;P8_Y5_R2FR_3223_FINITE_ALPHA_BOUND_FORMULA.csv;P8_Y5_R2FR_3223_FINITE_ALPHA_SMOKE_INPUTS.csv;P8_Y5_R2FR_3223_ALPHA_SMOKE_RUNNER_RESULTS.csv;P8_Y5_R2FR_3223_DECISION.csv |
| VAL3223_09_next_target | true | 3224-Y5-R2FR-finite-alpha-bound-propagator-clock-WEP-R10-under-AX1090 |

All generated rows remain `valid_for_claim=false`.
