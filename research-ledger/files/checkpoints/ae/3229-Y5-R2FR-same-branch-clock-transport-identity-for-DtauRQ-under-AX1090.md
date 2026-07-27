# 3229 - Same-branch Clock Transport Identity for DtauRQ under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result.

## Result

3229 derives the transport identity as a field-space branch decomposition.

Let the observed clock experiment define a parent configuration path:

```text
gamma: tau_obs -> Phi(tau_obs).
```

For any differentiable residual map `R_Q`,

```text
D_tau R_Q = DR_Q[Phi] . gamma_dot.
```

Choose a local EM residual branch direction `e_m`, a physical transverse piece `v_perp`, and a quotient-vertical piece `v_vert`:

```text
gamma_dot = tau_clock_time e_m + v_perp + v_vert.
```

Then the exact decomposition is:

```text
D_tau R_Q
= D_m R_Q tau_clock_time
  + D_perp R_Q[v_perp]
  + D_vert R_Q[v_vert].
```

So the desired identity is not an axiom. It is exact if:

```text
v_perp = 0,
D_vert R_Q[v_vert] = 0.
```

Otherwise it becomes a finite transport-error problem:

```text
E_transport := ||D_perp R_Q[v_perp]|| + ||D_vert R_Q[v_vert]||.
```

This refines the 3228 clock reduction:

```text
|D_tau ln alpha_EM|
<= C_D |Delta m tau_clock_time| + E_HO + E_clock_transport,

E_clock_transport
:= (2 |lambda_D| / Z_min) ||R_Q|| E_transport.
```

Using the near-root residual bound,

```text
E_clock_transport
<= (2 |lambda_D| / Z_min)
   (||D_m R_Q|| |Delta m| + O(Delta m^2))
   (||D_perp R_Q|| ||v_perp|| + ||D_vert R_Q|| ||v_vert||).
```

Current verdict: `TRANSPORT_IDENTITY_DERIVED_AS_BRANCH_DECOMPOSITION_EXACT_CLOSURE_NOT_SIGNED`.

The next real target is no longer vague clock magic. It is:

```text
prove v_perp=0, or bound ||v_perp|| <= Y_perp,
and prove D_vert R_Q=0 or bound it.
```

## Transport Identity Derivation

| step_id | object | identity | status | derivation | missing_for_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| TR3229_0_field_path | local observed clock path | gamma: tau_obs -> Phi(tau_obs) in parent configuration space | GEOMETRIC_SETUP | Any observed clock experiment selects a path through the parent field configuration space once the observed clock functional is fixed. | parent-signed clock functional and configuration-space domain | false |
| TR3229_1_chain_rule | residual derivative | D_tau R_Q = DR_Q[Phi] . gamma_dot | EXACT_DIFFERENTIAL_IDENTITY | This is the Fréchet chain rule for the residual map R_Q evaluated along gamma(tau_obs). | R_Q parent object and differentiability class | false |
| TR3229_2_tangent_split | clock tangent decomposition | gamma_dot = tau_clock_time e_m + v_perp + v_vert | EXACT_SPLIT_AFTER_BRANCH_CHOICE | Choose e_m as the EM residual branch direction, v_perp as physical transverse drift, and v_vert as representative/quotient-vertical drift. | parent-owned branch coordinate m and projection operators P_m,P_perp,P_vert | false |
| TR3229_3_transport_identity | same-branch transport | D_tau R_Q = D_m R_Q tau_clock_time + D_perp R_Q[v_perp] + D_vert R_Q[v_vert] | DERIVED_EXACT_BRANCH_DECOMPOSITION | Insert the tangent split into the chain rule. No dynamics have been assumed yet. | bounds or zero the transverse and vertical terms | false |
| TR3229_4_vertical_silence | quotient-vertical term | D_vert R_Q[v_vert]=0 if R_Q is quotient-basic or representative-silent | CONDITIONAL_ZERO | If R_Q descends through q(Phi), vertical tangent vectors in ker(Dq) cannot change R_Q. | R_Q=q-basic source row or vertical Ward identity | false |
| TR3229_5_transverse_error | physical transverse drift | E_transport := \|\|D_perp R_Q[v_perp]\|\| + \|\|D_vert R_Q[v_vert]\|\| | BOUND_TARGET_DEFINED | All non-one-dimensional clock-path leakage is isolated into a single normed transport error. | v_perp amplitude bound, D_perpR_Q operator norm, vertical silence or vertical bound | false |
| TR3229_6_exact_closure | one-dimensional same-branch closure | if v_perp=0 and D_vertR_Q[v_vert]=0, then D_tau R_Q = D_m R_Q tau_clock_time exactly | EXACT_CONDITIONAL_THEOREM | The identity follows immediately from the branch decomposition and quotient silence. | parent proof that the clock path stays in the EM residual branch up to vertical gauge | false |

## Transport Parent Contract

| clause_id | required_clause | math_need | current_status | why_it_matters | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| TPC3229_0_branch_coordinate | parent-owned EM residual branch coordinate m | e_m and Delta m identify the same local branch used in D_mR_Q | MISSING_PARENT_BRANCH_COORDINATE | without this, tau_clock_time cannot be the velocity along the R_Q branch | false |
| TPC3229_1_clock_path | observed clock path gamma(tau_obs) | gamma_dot is measured with the same tau_obs used by the clock bound | CONDITIONAL_FROM_3136 | prevents using internal flow time as if it were lab clock time | false |
| TPC3229_2_projection_split | tangent projection gamma_dot=tau e_m+v_perp+v_vert | define P_m, P_perp, and vertical kernel consistently | GEOMETRIC_CONTRACT_WRITTEN | turns the vague transport problem into exact pieces that can be bounded | false |
| TPC3229_3_vertical_silence | R_Q is q-basic or vertical-Ward silent | D_vertR_Q[v_vert]=0 for v_vert in ker(Dq) | UNSIGNED | otherwise representative drift can fake alpha/clock drift | false |
| TPC3229_4_transverse_amplitude | v_perp is zero or bounded by local nohair/source leakage | \|\|v_perp\|\| <= Y_perp or v_perp=0 | BOUND_ROUTE_FROM_3210_NOT_ATTACHED_TO_RQ | this is the finite-error route if exact one-dimensional closure fails | false |

## Xi-clock Reduction With Transport Error

| row_id | quantity | formula | status | definition | claim_gate | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| XIR3229_0_corrected_clock_reduction | alpha clock drift | \|D_tau ln alpha_EM\| <= C_D \|Delta m tau_clock_time\| + E_HO + E_clock_transport | REFINED_FROM_3228 | E_clock_transport := (2\|lambda_D\|/Z_min)\|\|R_Q\|\| E_transport, with \|\|R_Q\|\| replaced by its near-root bound when allowed | requires R_Q parent object, Z_min, same branch, and E_transport bound | false |
| XIR3229_1_exact_transport_case | E_clock_transport | E_clock_transport=0 if v_perp=0 and vertical silence holds | EXACT_CONDITIONAL_ZERO | one-dimensional clock path in the EM residual branch | must prove local branch closure, not assume it | false |
| XIR3229_2_finite_transport_case | E_clock_transport | E_clock_transport <= (2\|lambda_D\|/Z_min)(\|\|D_mR_Q\|\| \|Delta m\|+O(Delta m^2)) (\|\|D_perpR_Q\|\| \|\|v_perp\|\| + \|\|D_vertR_Q\|\| \|\|v_vert\|\|) | FINITE_BOUND_FORMULA | finite error budget if exact closure fails | requires transverse amplitude and operator norm inputs | false |

## E_transport Bound Targets

| target_id | target | source_route | required_inputs | result_if_acquired | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| EBT3229_0_transverse_zero | v_perp=0 theorem | 3210 nohair/tangent amplitude collapse | J_perp=0; boundary_perp=0; coercive operator; same branch as R_Q | exact transport identity closes | BEST_ZERO_ROUTE | false |
| EBT3229_1_transverse_bound | \|\|v_perp\|\| <= Y_perp | 3210 amplitude law with source/boundary leakage | source norm; boundary norm; m_min; Z_min; operator domain | finite E_clock_transport bound for the clock gate | BEST_FINITE_ROUTE | false |
| EBT3229_2_vertical_silence | D_vert R_Q=0 | quotient-basic residual or vertical Ward identity | R_Q descends through q(Phi) or explicit vertical annihilation theorem | removes representative drift from alpha/clock channel | NEEDED_FOR_ZERO_AND_FINITE_ROUTES | false |

## Decision

| decision_id | decision | because | claim_status | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3229_0_result | TRANSPORT_IDENTITY_DERIVED_AS_BRANCH_DECOMPOSITION_EXACT_CLOSURE_NOT_SIGNED | D_tau R_Q splits exactly into same-branch, transverse, and vertical pieces; the desired identity is exact when transverse drift vanishes and vertical drift is silent, otherwise the failure is a bounded E_transport term | NO_ALPHA_NO_CLOCK_NO_WEP_NO_R10_NO_LOCAL_GR_CLAIM | derive or bound the transverse branch amplitude v_perp using the 3210 nohair/amplitude machinery, and separately prove vertical silence of R_Q | false |
| DEC3229_1_next_target | 3230-Y5-R2FR-transverse-branch-amplitude-bound-for-Etransport-under-AX1090 | the transport identity no longer needs guessing; only v_perp and vertical silence decide whether Xi_clock is exact or finite-bounded | PRIVATE_NEXT_TARGET | attach the 3210 amplitude law to the R_Q transverse sector and test whether v_perp=0 or \|\|v_perp\|\|<=Y_perp can be parent-signed | false |

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3229_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3229_TRANSPORT_IDENTITY_DERIVATION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3229_TRANSPORT_PARENT_CONTRACT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3229_XI_CLOCK_REDUCTION_WITH_TRANSPORT_ERROR.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3229_ETRANSPORT_BOUND_TARGETS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3229_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3229_VALIDATION.csv`

## Source Register

| input_id | relative_path | exists | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC3229_00_3228_doc | 3228-Y5-R2FR-Xi-clock-product-row-or-clock-tau-owner-under-AX1090.md | true | 3228 handoff selecting same-branch transport identity | L31:\|D_tau ln Z_A\| <= 2 \|lambda_D\| \|\|R_Q\|\| \|\|D_tau R_Q\|\| / Z_min. \| L38:\|\|D_tau R_Q\|\| <= \|\|D_m R_Q\|\| \|tau_clock_time\| + E_transport, \| L44:Xi_clock := C_D \|Delta m tau_clock_time\| \| L46:\|d ln alpha_EM / d tau_obs\| <= Xi_clock + E_HO + E_transport. | false |
| SRC3229_01_3228_derivation | P8_Y5_R2FR_3228_XI_CLOCK_PRODUCT_DERIVATION.csv | true | machine Xi_clock product derivation | L4:XID3228_2_defect_norm_chain_rule,defect-norm derivative,"Z_A=Z_*+lambda_D <R_Q,R_Q>_P gives \|D_tau ln Z_A\| <= 2\|lambda_D\| \|\|R_Q\|\| \|\|D_tau R_Q\|\| / Z_min",DERIVED_FROM_3222_CONTRACT_CONDITIONAL,R_Q parent object; positive  \| L5:XID3228_3_root_taylor_product,near-root product law,\|\|R_Q\|\| <= \|\|D_m R_Q\|\| \|Delta m\| + O(Delta m^2); \|\|D_tau R_Q\|\| <= \|\|D_m R_Q\|\| \|tau_clock_time\| + transport error,DERIVED_CONDITIONALLY,same branch coordinate m; same op \| L7:XID3228_5_exact_root_silence,local exact-root clock silence,R_Q=0 and D_tau R_Q finite imply D_tau ln Z_A=0 for the pure defect-norm term,EXACT_CONDITIONAL_ZERO,same local branch really satisfies R_Q=0; no linear Z_A ter | false |
| SRC3229_02_3228_contract | P8_Y5_R2FR_3228_PARENT_XI_CLOCK_CONTRACT.csv | true | machine parent Xi_clock contract | L5:XIC3228_3_same_branch_transport,same-branch transport identity,D_tau R_Q = D_m R_Q tau_clock_time + E_transport,not found as a parent row; 3227 only defines tau_clock_time product maps,MISSING_CORE_OWNER,this is the exac | false |
| SRC3229_03_3210_doc | 3210-Y5-R2FR-scalar-nohair-amplitude-law-and-omega-zero-curl-gate-under-AX1090.md | true | local amplitude/nohair source for transverse bound route | L10:source/boundary leakage -> X amplitude -> deltaX amplitude -> omega_X curl bound. \| L21:Y_X := sqrt(E_X) \| L25:Y_X <= (a_X + sqrt(a_X^2 + 4 b_X))/2. \| L31:\|\|X\|\|_H1 <= Y_X sqrt(1/m_min^2 + 1/Z_min). | false |
| SRC3229_04_3210_amp | P8_Y5_R2FR_3210_SCALAR_NOHAIR_AMPLITUDE_LAW.csv | true | machine amplitude law | L1:law_id,object,statement,derived_result,status,missing_for_claim,valid_for_claim,generated_utc \| L5:AMP3210_3_profile_amplitude,Y_X_bound,"Let Y_X=sqrt(E_X), a_X=\|\|J_X\|\|_2/m_min, b_X=\|Phi_boundary\|. Then Y_X <= (a_X+sqrt(a_X^2+4 b_X))/2.",from Y_X^2 <= a_X Y_X + b_X; this is the first explicit amplitude law for the loc \| L8:AMP3210_6_tangent_amplitude,delta_X_H1_bound,"For a tangent variation, O_X deltaX = deltaJ_X-(deltaO_X)X plus delta boundary data; the same bound applies with J_delta and Phi_delta.","if X=0, deltaJ_X=0, and deltaPhi_bou | false |
| SRC3229_05_3136_doc | 3136-Y5-R2FR-observed-coframe-clock-functional-owner-under-AX1090.md | true | clock path observed-time source | L11:=> observed clocks measure observed metric proper time. \| L51:This does not yet prove local GR, Newton, or clocks, because the parent has not signed: \| L59:same tau for clock/source/charge/orbit/boundary. | false |
| SRC3229_06_3223_doc | 3223-Y5-R2FR-RQ-source-search-or-finite-alpha-runner-smoke-inputs-under-AX1090.md | true | finite R_Q branch and D_mR_Q source gap | L7:3223 performs a bounded source search over the files that actually matter for the `R_Q` defect-norm route. \| L12:No candidate R_Q is source-signed yet. \| L23:Since no exact `R_Q` source row exists, 3223 stages the finite branch instead: \| L26:\|b_alpha_m\| <= 2 \|lambda_D\| \|\|D_m R_Q\|\|^2 \|Delta m\| / Z_min + O(Delta m^2). | false |

## Validation

| check_id | pass | detail |
| --- | --- | --- |
| VAL3229_00_inputs_exist | true | inputs=7 |
| VAL3229_01_exact_decomposition | true | D_tau R_Q branch decomposition derived |
| VAL3229_02_exact_closure_case | true | one-dimensional same-branch closure staged |
| VAL3229_03_finite_error_formula | true | E_clock_transport finite formula staged |
| VAL3229_04_next_transverse_bound | true | 3230 target tied to transverse amplitude |
| VAL3229_05_claims_blocked | true | claim_rows_true=0 |
| VAL3229_06_no_formalization_workbench_edit | true | no formalization-workbench paths are output targets |
| VAL3229_07_csv_parse | true | P8_Y5_R2FR_3229_INPUTS.csv;P8_Y5_R2FR_3229_TRANSPORT_IDENTITY_DERIVATION.csv;P8_Y5_R2FR_3229_TRANSPORT_PARENT_CONTRACT.csv;P8_Y5_R2FR_3229_XI_CLOCK_REDUCTION_WITH_TRANSPORT_ERROR.csv;P8_Y5_R2FR_3229_ETRANSPORT_BOUND_TARGETS.csv;P8_Y5_R2FR_3229_DECISION.csv |
| VAL3229_08_next_target | true | 3230-Y5-R2FR-transverse-branch-amplitude-bound-for-Etransport-under-AX1090 |

All generated rows remain `valid_for_claim=false`.
