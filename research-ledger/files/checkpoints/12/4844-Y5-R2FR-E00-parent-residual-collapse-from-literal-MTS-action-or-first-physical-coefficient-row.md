# 4844 Y5 R2FR E00 parent residual collapse from literal MTS action or first physical coefficient row

**Status:** 4844 derives the metric-side `Gamma_G` contribution directly from the literal MTS action. It finds a correctable factor-two normalization error in the existing core text and replaces the generic raw-`E_00` Newton shortcut with the correct trace-reversed source `Sigma_Gamma`. No core document is changed at this checkpoint.

**Decision:** `LITERAL_ACTION_FACTOR_TWO_GAMMA_NORMALIZATION_MISMATCH_AND_TRACE_REVERSED_NEWTON_SOURCE_DERIVED_CORRECTED_ACTION_CANDIDATE_STAGED_NONCLAIM`.

## Exact action variation

Parameterize the vacuum/exchange term as:

```text
S_Gamma = -(a_Gamma/kappa) int sqrt(-g) Gamma_G
Pi_Gamma_mn := delta Gamma_G / delta g^mn
```

Using `delta sqrt(-g)=-1/2 sqrt(-g) g_mn delta g^mn` and the standard Hilbert definition of `T_mn` gives:

```text
G_mn + a_Gamma Gamma_G g_mn - 2 a_Gamma Pi_Gamma_mn = kappa T_mn.
```

The literal core action writes `L_LambdaKappa=2 Gamma_G/kappa` and subtracts it, so `a_Gamma=2`. If `Pi_Gamma_mn=0`, that action yields:

```text
G_mn + 2 Gamma_G g_mn = kappa T_mn,
```

not the claimed unit-coefficient equation. The minimal correction is:

```text
L_LambdaKappa = Gamma_G/kappa,
```

equivalently `a_Gamma=1`. If `Gamma_G` depends on the metric, memory, or fields, the `Pi_Gamma_mn` term is mandatory even after this normalization repair.

## Trace-reversed Newton source

Define:

```text
X_mn = a_Gamma (Gamma_G g_mn - 2 Pi_Gamma_mn)
Xbar_mn = X_mn - 1/2 g_mn X.
```

For `g_00~-1`:

```text
Sigma_Gamma := Xbar_00
             = a_Gamma (Gamma_G - 2 Pi_Gamma_00 - Pi_Gamma).
```

The Newton equation is therefore:

```text
nabla^2 Phi = 4 pi G rho - c^2 Sigma_Gamma
              + other trace-reversed residuals.
```

For a constant spherical `Sigma_Gamma`:

```text
Delta Phi = -(c^2 Sigma_Gamma/6) r^2
Delta a_r = +(c^2 Sigma_Gamma/3) r
|Delta a|/(GM/r^2) = c^2 |Sigma_Gamma| r^3/(3GM).
```

This also shows why a raw Einstein-form `E_00` is not enough for a generic residual: its trace/spatial equations decide the force potential.

## Bianchi gate

If matter is separately conserved:

```text
nabla^m X_mn = 0.
```

For `Pi_Gamma_mn=0`, this forces `partial_n Gamma_G=0` in the local branch. A varying `Gamma_G` therefore requires a dynamic response tensor and its field equation, or an explicit matter-exchange current; it cannot be varied as a constant and interpreted as dynamical afterward.

## Source register

| source_id | exists | needle_found | role |
| --- | --- | --- | --- |
| SRC4844_00_resume | True | True | 4843 selected the literal-action E00 target |
| SRC4844_01_core_action | True | True | literal action and claimed Gamma field term |
| SRC4844_02_core_equation | True | True | claimed extended Einstein equation |
| SRC4844_03_fundamental_action | True | True | second statement of Gamma action normalization |
| SRC4844_04_weak_trace | True | True | correct Newtonian curvature projection |
| SRC4844_05_weak_MTS | True | True | trace-reversed MTS source precedent |
| SRC4844_06_consistency | True | True | Bianchi/exchange-current guard |
| SRC4844_07_equation_redflag | True | True | metric-dependence variation warning |
| SRC4844_08_poisson_4719 | True | True | raw E00 Poisson map to correct |
| SRC4844_09_eh_4720 | True | True | local vacuum residual family |
| SRC4844_10_reconcile_4843 | True | True | source-prefactor handoff |
| SRC4844_11_runner | True | True | 4844 action/trace-reverse runner |
| SRC4844_12_generator | True | True | 4844 generator and validator |

## Action audit

| audit_id | object | formula | result | consequence |
| --- | --- | --- | --- | --- |
| GAV4844_0_parameterization | Gamma action normalization | S_Gamma=-(a_Gamma/kappa) int sqrt(-g) Gamma_G | DEFINITION | core literal action has a_Gamma=2 |
| GAV4844_1_variation | metric variation | G_mn+a_Gamma Gamma_G g_mn-2 a_Gamma Pi_Gamma_mn=kappa T_mn | EXACT_VARIATION | Pi_Gamma_mn:=delta Gamma_G/delta g^mn |
| GAV4844_2_literal_factor | literal core coefficient | a_Gamma=2 | FACTOR_TWO_MISMATCH | metric-independent limit gives G_mn+2 Gamma_G g_mn=kappa T_mn |
| GAV4844_3_corrected_factor | coefficient required by claimed equation | a_Gamma=1 | CORRECTED_ACTION_CANDIDATE | use L_LambdaKappa=Gamma_G/kappa for G_mn+Gamma_G g_mn when Pi=0 |
| GAV4844_4_metric_response | dynamic Gamma response | Pi_Gamma_mn=delta Gamma_G/delta g^mn | MANDATORY_IF_GAMMA_DEPENDS_ON_METRIC_HISTORY | cannot vary Gamma_G as an external constant and later call it dynamical |
| GAV4844_5_Bianchi | local conservation | nabla^m X_mn=kappa nabla^m T_mn | CONSTANT_OR_EXCHANGE_REQUIRED | if Pi=0 and matter is conserved then partial_n Gamma_G=0 locally |
| GAV4844_6_scope | meaning of correction | normalization repair plus exact residual map | CORRECTABLE_NOT_LOCAL_GR_CLAIM | Gamma profile/exchange and all other non-EH residuals remain |

## Trace-reversed map

| map_id | object | formula | meaning |
| --- | --- | --- | --- |
| TRN4844_0_X | Einstein-form residual | X_mn=a_Gamma(Gamma_G g_mn-2 Pi_Gamma_mn) | enters G_mn+X_mn=kappa T_mn |
| TRN4844_1_trace | residual trace | X=a_Gamma(4 Gamma_G-2 Pi_Gamma) | needed before Newton projection |
| TRN4844_2_trace_reverse | trace-reversed residual | Xbar_00=X_00-(1/2)g_00 X | raw E_00 alone is insufficient for generic residuals |
| TRN4844_3_sigma | physical local Gamma source | Sigma_Gamma=a_Gamma[Gamma_G-2 Pi_Gamma_00-Pi_Gamma] for g_00~-1 | units m^-2 |
| TRN4844_4_Poisson | corrected Newton equation | nabla^2 Phi=4 pi G rho-c^2 Sigma_Gamma+other trace-reversed residuals | positive constant Gamma gives de-Sitter outward acceleration |
| TRN4844_5_profile | constant spherical profile | Delta a_r=(c^2/3) Sigma_Gamma r; \|Delta a\|/(GM/r^2)=c^2 \|Sigma_Gamma\| r^3/(3GM) | local profile/arena comparator ready |
| TRN4844_6_threshold | arena threshold | \|Sigma_Gamma\|<=3 tau_a GM/(c^2 r^3) | bound is comparator only and cannot define Gamma_G |
| TRN4844_7_4719_repair | 4719 raw E00 map | replace raw +(c^2/2)E_00 by source-family-specific trace-reversed map | EH harmonic identity remains useful only after spatial/trace equations are controlled |

## Runner output

| row_id | runner_status | field_equation_gamma_coefficient | normalization_mismatch_abs | Sigma_Gamma_m2 | Delta_Poisson_Gamma_s2 | fractional_acceleration_abs | missing_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RUN4844_0_literal_action_factor_two_detected | ACTION_NORMALIZATION_MISMATCH_DETECTED | 2.000000000000000e+00 | 1.000000000000000e+00 | NOT_THIS_ROUTE | NOT_THIS_ROUTE | NOT_THIS_ROUTE |  |
| RUN4844_1_corrected_action_candidate_pass | ACTION_NORMALIZATION_PASS_NONCLAIM | 1.000000000000000e+00 | 0.000000000000000e+00 | NOT_THIS_ROUTE | NOT_THIS_ROUTE | NOT_THIS_ROUTE |  |
| RUN4844_2_live_trace_source_missing | BLOCKED_TRACE_REVERSED_GAMMA_SOURCE | 1.000000000000000e+00 | NOT_THIS_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | NOT_THIS_ROUTE | MISSING_Gamma_G_m2;MISSING_Pi_Gamma_00_m2;MISSING_Pi_Gamma_trace_m2 |
| RUN4844_3_trace_response_smoke_pass | TRACE_REVERSED_GAMMA_SOURCE_PASS_NONCLAIM | 1.000000000000000e+00 | NOT_THIS_ROUTE | 1.300000000000000e-52 | -1.168381732357863e-35 | NOT_THIS_ROUTE |  |
| RUN4844_4_constant_profile_smoke_pass | CONSTANT_GAMMA_PROFILE_PASS_NONCLAIM | 1.000000000000000e+00 | NOT_THIS_ROUTE | 1.000000000000000e-52 | -8.987551787368177e-36 | 2.995850595789392e-23 |  |
| RUN4844_5_local_threshold_smoke_pass | LOCAL_SIGMA_GAMMA_THRESHOLD_PASS_NONCLAIM | NOT_THIS_ROUTE | NOT_THIS_ROUTE | NOT_A_PREDICTION | NOT_THIS_ROUTE | 1.000000000000000e-10 |  |
| RUN4844_6_Bianchi_constant_Gamma_pass | BIANCHI_GAMMA_GATE_PASS_NONCLAIM | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE |  |
| RUN4844_7_Bianchi_variable_external_blocked | BLOCKED_BIANCHI_GAMMA_GATE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_Gamma_constant_or_metric_response_exchange |
| RUN4844_8_forbidden_ignore_factor_two | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4844_9_forbidden_raw_E00 | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4844_10_forbidden_variable_Gamma_no_exchange | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4844_11_forbidden_bound_as_source | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |

## Validation

| check_id | status | detail |
| --- | --- | --- |
| VAL4844_00_sources_exist | PASS | all cited source paths exist |
| VAL4844_01_needles_found | PASS | all cited source needles found |
| VAL4844_02_runner_compiles | PASS | runner compiles |
| VAL4844_03_generator_compiles | PASS | generator compiles |
| VAL4844_04_output_count | PASS | outputs=12 inputs=12 |
| VAL4844_05_claims_false | PASS | all rows remain nonclaim |
| VAL4844_06_literal_mismatch | PASS | literal a_Gamma=2 mismatch detected |
| VAL4844_07_corrected_candidate | PASS | a_Gamma=1 candidate matches claimed coefficient |
| VAL4844_08_live_trace_blocked | PASS | MISSING_Gamma_G_m2;MISSING_Pi_Gamma_00_m2;MISSING_Pi_Gamma_trace_m2 |
| VAL4844_09_trace_smoke | PASS | trace-response Sigma and Poisson source compute |
| VAL4844_10_profile_smoke | PASS | constant spherical profile arithmetic passes |
| VAL4844_11_threshold_smoke | PASS | local comparator threshold arithmetic passes |
| VAL4844_12_Bianchi_controls | PASS | constant branch passes and variable external Gamma blocks |
| VAL4844_13_forbidden_routes | PASS | factor, trace, exchange and bound shortcuts fail |
| VAL4844_14_resume_next | PASS | resume records derivation and next profile target |
| VAL4844_15_no_pycache | PASS | scripts __pycache__ removed |

## What changed

- A real algebraic error is identified and locally repaired: the written potential coefficient is twice the value required by the claimed equation.
- The physically relevant Newton source is now `Sigma_Gamma`, which includes metric response and trace information.
- Constant and varying `Gamma_G` branches are separated by an executable Bianchi gate.
- The next target is no longer a vague `E_00` coefficient: it is a local `Gamma_G/Pi_Gamma` profile or a same-branch constancy/exchange theorem.

## Next target

`4845-Y5-R2FR-Gamma-local-constancy-exchange-and-SigmaGamma-profile-bound.md`
