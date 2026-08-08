# 4845 Y5 R2FR Gamma local constancy exchange and SigmaGamma profile bound

**Status:** 4845 constructs the local suppression mechanism that the previous plateau route lacked. The private post-checkpoint candidate uses an exchange-odd response doublet and a positive action. Its Euler equation forces the active Gamma carrier to zero in a source-free closed local collar, while a nonzero source produces a quadratic, executable `Sigma_Gamma` bound. The constant background `Gamma0` is retained explicitly.

**Decision:** `RESPONSE_DOUBLET_POSITIVE_ACTION_CONSTRUCTS_ACTIVE_GAMMA_LOCAL_ZERO_AND_QUADRATIC_SOURCE_BOUND_CONSTANT_BACKGROUND_RETAINED_GLOBAL_ADOPTION_OPEN_NONCLAIM`.

## Candidate action

Use the 4844 normalization repair and define:

```text
Z^A = (R_+^A-R_-^A)/2,                  E: Z^A -> -Z^A
Gamma_eff = Gamma0
          + 1/2 A_AB^mn nabla_m Z^A nabla_n Z^B
          + 1/2 M2_AB Z^A Z^B - J_A Z^A + O(Z^4)
S_Gamma = -(1/kappa) int sqrt(-g) Gamma_eff.
```

Ordinary matter belongs to the exchange-even visible branch established in 4843. Therefore it cannot generate a linear exchange-odd `J_A Z^A` vertex. Odd history, boundary or transition sources are not erased; they are the finite `J_A` branch.

Variation gives:

```text
L_AB Z^B = J_A + O(Z^3),
L_AB = -nabla_m(A_AB^mn nabla_n) + M2_AB.
```

The algebraic auxiliary limit is `A=0`. The dynamic local limit keeps the positive derivative operator.

## Local zero theorem

On a fixed local collar:

```text
<Z,LZ> = ||Z||_L^2 = <Z,J> + B_boundary.
```

If `lambda_gap>0`, `J_loc=0`, the boundary flux vanishes and gauge/zero modes are removed, positivity forces:

```text
Z=0 and nabla Z=0.
```

Exchange evenness and regular same-action metric response then give:

```text
Gamma_active=0,
Pi_active=0,
Sigma_active=Gamma_active-2Pi_active,00-Pi_active=0,
q_Gamma=nabla_m X_Gamma^mn=0.
```

This is an Euler/energy theorem, not an inserted local-vacuum plateau.

## Finite quadratic branch

For nonzero odd source or boundary lift:

```text
||Z||_H1 <= (||J_Z||+B_lift)/lambda_gap,
||Sigma_active|| <= C_Sigma [(||J_Z||+B_lift)/lambda_gap]^2 + R_higher,
epsilon_a <= c^2 r^3 ||Sigma_active||/(3GM).
```

The absence of a linear term is the useful physical payoff: local active gravity is quadratically suppressed in the exchange-odd source. A real prediction still needs sourced `J_Z`, boundary lift, gap, response coefficient and arena data.

## Background and exchange

The split is:

```text
Sigma_total = Gamma0 + Sigma_active.
```

`Gamma0` is not deleted. If constant it has `q=0` but still produces the de-Sitter `r` acceleration scored by the runner.

With `X_Gamma` on the left of `G+X=kappa T`:

```text
nabla_m X_Gamma^mn = kappa nabla_m T_matter^mn = q_Gamma^n.
```

This positive sign matches the parent equation `K_MTS=-X` and `q=nabla K_matter`. The older negative-sign sentence in the repair note is inconsistent with its displayed Einstein equation and is not carried forward.

## Scope guard

This action controls the Gamma carrier. It does not prove that every source, PPN, even-stress, boundary or readout residual is a component of `Z`. In particular, `q_Gamma=0` alone does not imply full local GR.

## Source register

| source_id | exists | needle_found | role |
| --- | --- | --- | --- |
| SRC4845_00_resume | True | True | 4845 resume and handoff |
| SRC4845_01_4844 | True | True | corrected action normalization and trace-reversed source |
| SRC4845_02_candidate | True | True | existing response-doublet Gamma owner candidate |
| SRC4845_03_quadratic | True | True | positive quadratic action and energy identity |
| SRC4845_04_contract | True | True | exchange-even action contract |
| SRC4845_05_variation | True | True | Euler and positive theorem |
| SRC4845_06_metric | True | True | same-action metric-response fixed point |
| SRC4845_07_sources | True | True | counterexample ledger preventing overclaim |
| SRC4845_08_positive | True | True | general positive-operator silence identity |
| SRC4845_09_parent_eq | True | True | parent exchange-current sign and response pair |
| SRC4845_10_consistency | True | True | older sign statement to reconcile |
| SRC4845_11_matter | True | True | ordinary matter source-prefactor zero on private branch |
| SRC4845_12_lock | True | True | scope guard: Gamma carrier does not prove all physical residuals |
| SRC4845_13_runner | True | True | 4845 suppression runner |
| SRC4845_14_generator | True | True | 4845 generator and validator |

## Action construction

| construction_id | object | formula | meaning |
| --- | --- | --- | --- |
| RDA4845_0_fields | response doublet | R_+^A,R_-^A; Z^A=(R_+^A-R_-^A)/2 | Z is the exchange-odd Gamma carrier only |
| RDA4845_1_symmetry | exchange symmetry | E:R_+^A<->R_-^A; Z^A->-Z^A | ordinary visible matter is exchange-even on the 4843 branch |
| RDA4845_2_density | corrected Gamma density | Gamma_eff=Gamma0+1/2 A_AB^mn nabla_m Z^A nabla_n Z^B+1/2 M2_AB Z^A Z^B-J_A Z^A+O(Z^4) | uses a_Gamma=1 from 4844 |
| RDA4845_3_action | post-checkpoint candidate action | S_Gamma=-(1/kappa) int sqrt(-g) Gamma_eff | same action owns Gamma and Pi_Gamma/Khat response |
| RDA4845_4_Euler | Z Euler equation | L_AB Z^B=J_A+O(Z^3); L=-nabla(A nabla)+M2 | active operator remains nondegenerate at the local origin |
| RDA4845_5_auxiliary | algebraic auxiliary limit | A_AB=0; M2_AB Z^B=J_A | J=0 and positive M2 force Z=0 without a plateau axiom |
| RDA4845_6_dynamic | positive dynamic limit | A>=0, M2>0 after gauge/zero-mode removal | energy identity gives zero or finite response bound |
| RDA4845_7_scope | candidate adoption scope | private post-checkpoint Gamma-carrier branch | not a unique global derivation from all original MTS primitives |

## Suppression theorem

| theorem_id | object | formula | consequence |
| --- | --- | --- | --- |
| LST4845_0_energy | energy identity | <Z,LZ>=\|\|Z\|\|_L^2=<Z,J>+B_boundary | exact on the candidate action |
| LST4845_1_zero | active local zero | J_loc=0, B_boundary=0, lambda_gap>0 => Z=0 | Gamma_act=Pi_act=Sigma_act=q_Gamma=0 |
| LST4845_2_bound | finite carrier bound | \|\|Z\|\|_H1 <= (\|\|J\|\|+B_lift)/lambda_gap | source and boundary deviations remain measurable |
| LST4845_3_quadratic | quadratic gravitational suppression | \|\|Sigma_act\|\| <= C_Sigma[(\|\|J\|\|+B_lift)/lambda_gap]^2+R_higher | no linear ordinary-matter Gamma force |
| LST4845_4_acceleration | local acceleration bound | epsilon_a <= c^2 r^3 \|\|Sigma_act\|\|/(3GM) | direct Newton/orbital comparator |
| LST4845_5_background | constant Gamma0 | Sigma_total=Gamma0+Sigma_act | Gamma0 is retained as de-Sitter background and never silently subtracted |
| LST4845_6_qscope | q_loc scope | q_Gamma=0 does not imply every PPN/source/even-stress residual is zero | prevents the old full-rank overclaim |
| LST4845_7_cosmology | cosmological activation | nonzero J_cos/history/boundary can drive Z away from zero | must be derived next rather than inserted as an environment switch |

## Bianchi exchange map

| exchange_id | identity | meaning |
| --- | --- | --- |
| BEX4845_0_field | G_mn+X_mn=kappa T_mn | X_mn=Gamma_eff g_mn-2 Pi_Gamma_mn |
| BEX4845_1_Bianchi | nabla^m X_mn=kappa nabla^m T_mn | the sign is positive when X is written on the left |
| BEX4845_2_parent_q | q_n:=nabla^m K_matter_mn=nabla^m X_mn | matches 36 with K_MTS=-X and q=nabla Gamma-div Khat |
| BEX4845_3_external | Pi=0 => q_n=partial_n Gamma_G | a varying external Gamma exchanges with matter and is not separately conservative |
| BEX4845_4_variational | candidate Z on shell and matter Z-blind => nabla X=0 | diffeomorphism Noether identity closes total conservation |
| BEX4845_5_sign_repair | older negative-sign line is inconsistent with G+Gamma g=kappa T | use the positive-sign identity above in future post-checkpoint work |

## Runner output

| row_id | runner_status | Z_H1_bound | Sigma_active_bound_m2 | fractional_acceleration_bound | background_fractional_acceleration | exchange_balance_residual_m3 | missing_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RUN4845_0_live_global_zero_missing | BLOCKED_GAMMA_ACTIVE_LOCAL_ZERO | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_candidate_action_adopted_private_signed;MISSING_response_doublet_parent_owned_signed;MISSING_exchange_symmetry_signed;MISSING_ordinary_matter_exchange_even_signed;MISSING_no_linear_even_Z_source_signed;MISSING_positive_operator_gap_signed;MISSING_local_odd_source_zero_signed;MISSING_boundary_flux_zero_signed;MISSING_zero_mode_removed_signed;MISSING_on_shell_Euler_signed;MISSING_Gamma0_local_constant_signed;MISSING_same_action_metric_response_signed;MISSING_coefficients_regular_at_origin_signed;MISSING_no_direct_Z_readout_signed;MISSING_background_force_retained_or_bounded_signed |
| RUN4845_1_private_candidate_active_zero_pass | GAMMA_ACTIVE_LOCAL_ZERO_PASS_PRIVATE_NONCLAIM | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | RETAINED_SEPARATELY | 0.000000000000000e+00 |  |
| RUN4845_2_odd_source_reactivation_control | BLOCKED_GAMMA_ACTIVE_LOCAL_ZERO | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_local_odd_source_zero_signed |
| RUN4845_3_live_quadratic_bound_missing | BLOCKED_GAMMA_QUADRATIC_SUPPRESSION_BOUND | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_J_Z_norm_m2;MISSING_boundary_lift_norm_m2;MISSING_lambda_gap_m2;MISSING_C_Sigma_quad_m2;MISSING_R_higher_m2;MISSING_radius_m;MISSING_GM_m3_s2 |
| RUN4845_4_quadratic_bound_smoke_pass | GAMMA_QUADRATIC_SUPPRESSION_BOUND_PASS_NONCLAIM | 3.000000000000000e-10 | 9.100000000000001e-52 | 2.726224042168347e-22 | RETAINED_SEPARATELY | SEPARATE_GATE_REQUIRED |  |
| RUN4845_5_constant_background_smoke_pass | GAMMA0_BACKGROUND_PROFILE_PASS_NONCLAIM | NOT_THIS_ROUTE | NOT_THIS_ROUTE | NOT_THIS_ROUTE | 2.995850595789392e-23 | 0_IF_GAMMA0_CONSTANT |  |
| RUN4845_6_positive_exchange_sign_pass | GAMMA_EXCHANGE_BALANCE_PASS_NONCLAIM | NOT_THIS_ROUTE | NOT_THIS_ROUTE | NOT_THIS_ROUTE | NOT_THIS_ROUTE | 0.000000000000000e+00 |  |
| RUN4845_7_negative_exchange_sign_control_fails | BLOCKED_GAMMA_EXCHANGE_BALANCE | NOT_THIS_ROUTE | NOT_THIS_ROUTE | NOT_THIS_ROUTE | NOT_THIS_ROUTE | 4.000000000000000e-60 | EXCHANGE_SIGN_OR_MAGNITUDE_MISMATCH |
| RUN4845_8_forbidden_qloc_to_full_sigma | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4845_9_forbidden_background_drop | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4845_10_forbidden_even_stress_erasure | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4845_11_forbidden_bound_as_source | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4845_12_forbidden_measured_GM_source | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |

## Validation

| check_id | status | detail |
| --- | --- | --- |
| VAL4845_00_sources_exist | PASS | all cited source paths exist |
| VAL4845_01_needles_found | PASS | all cited source needles found |
| VAL4845_02_runner_compiles | PASS | runner compiles |
| VAL4845_03_generator_compiles | PASS | generator compiles |
| VAL4845_04_output_count | PASS | outputs=13 inputs=13 |
| VAL4845_05_claims_false | PASS | all rows remain nonclaim |
| VAL4845_06_live_zero_blocked | PASS | MISSING_candidate_action_adopted_private_signed;MISSING_response_doublet_parent_owned_signed;MISSING_exchange_symmetry_signed;MISSING_ordinary_matter_exchange_even_signed;MISSING_no_linear_even_Z_source_signed;MISSING_positive_operator_gap_signed;MISSING_local_odd_source_zero_signed;MISSING_boundary_flux_zero_signed;MISSING_zero_mode_removed_signed;MISSING_on_shell_Euler_signed;MISSING_Gamma0_local_constant_signed;MISSING_same_action_metric_response_signed;MISSING_coefficients_regular_at_origin_signed;MISSING_no_direct_Z_readout_signed;MISSING_background_force_retained_or_bounded_signed |
| VAL4845_07_candidate_zero | PASS | candidate active Gamma zero propagates |
| VAL4845_08_reactivation | PASS | odd source reopens finite route |
| VAL4845_09_live_bound_blocked | PASS | MISSING_J_Z_norm_m2;MISSING_boundary_lift_norm_m2;MISSING_lambda_gap_m2;MISSING_C_Sigma_quad_m2;MISSING_R_higher_m2;MISSING_radius_m;MISSING_GM_m3_s2 |
| VAL4845_10_bound_smoke | PASS | quadratic suppression arithmetic passes |
| VAL4845_11_background | PASS | constant background remains explicitly scored |
| VAL4845_12_exchange_sign | PASS | positive Bianchi sign passes and negative control fails |
| VAL4845_13_forbidden | PASS | all qloc/background/even-stress/bound/source shortcuts fail |
| VAL4845_14_resume | PASS | resume records theorem and next activation target |
| VAL4845_15_no_pycache | PASS | scripts __pycache__ removed |

## What changed

- The local Gamma route now has a concrete parent-action candidate and a proof, not a plateau declaration.
- Exact local active silence and finite quadratic suppression are two branches of the same Euler equation.
- The Bianchi exchange sign is reconciled with the parent tensor split.
- Cosmological activation and the first physical local profile row are now the next real tests.

## Next target

`4846-Y5-R2FR-response-doublet-cosmology-local-source-split-or-first-real-SigmaGamma-arena-row.md`
