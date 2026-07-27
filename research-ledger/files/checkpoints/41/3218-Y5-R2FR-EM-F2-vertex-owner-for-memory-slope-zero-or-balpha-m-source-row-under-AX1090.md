# 3218 - EM F2 Vertex Owner For Memory Slope Zero Or b_alpha_m Source Row under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result.

## Result

3218 derives the exact object we needed:

```text
S_EM = -1/4 int Z_A(m,q,readout) F_Q^2

b_alpha_m := partial_m ln Z_A | m_*
           = (partial_m Z_A | m_*) / Z_A(m_*).
```

Using the honest EM coefficient decomposition:

```text
Z_A =
  C_P N_Q
  + lambda_A
  + f_m(m)
  + delta_lambda_rad(m,mu)
  + readout_alpha(m).
```

So:

```text
b_alpha_m =
[ partial_m(C_P N_Q)
  + partial_m lambda_A
  + f_m'(m_*)
  + partial_m delta_lambda_rad
  + partial_m readout_alpha
] / Z_A(m_*).
```

This is progress because it stops the coupling problem being vague. The only honest zero routes are:

```text
1. fixed parent T_Q/gauge norm plus no independent F_Q^2;
2. strict EM double-zero source root f_m=O((m-m_*)^2);
3. radiative/readout closure preserving the same rule.
```

Current verdict: the zero theorem is exact as a conditional, but not parent-signed. The source row for `b_alpha_m` is staged and remains nonclaim.

## Z_A Memory Decomposition

| component_id | term | meaning | memory_derivative | zero_condition | current_status | if_live | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ZA3218_0_parent_norm | C_P N_Q | parent curvature coefficient times fixed gauge-generator norm | partial_m(C_P N_Q) | C_P and N_Q are Q_ONLY/REP_TOPOLOGICAL parent data with Dq[partial_m]=0 | CONDITIONAL_SYMBOLIC_ONLY | contributes to b_alpha_m if parent norm or coefficient depends on memory | false |
| ZA3218_1_lambda_visible | lambda_A | independent visible Maxwell kinetic counterterm | partial_m lambda_A | operator-domain exhaustion forbids independent F_Q^2 or signs lambda_A as fixed Q_ONLY constant | LEGAL_UNLESS_FORBIDDEN | constant lambda shifts alpha; memory-dependent lambda produces b_alpha_m | false |
| ZA3218_2_hidden_scalar | f_m(m) or f(I_hid) | hidden/memory scalar gauge-kinetic coefficient | f_m'(m_*) | typed exclusion, exact even/fixed-point symmetry, or strict double-zero f_m=O((m-m_*)^2) | COUNTERMODEL_ACTIVE | direct EM source J_m includes -1/4 f_m'(m_*) F^2 | false |
| ZA3218_3_radiative_readout | delta_lambda_rad(m,mu)+readout_alpha(m) | effective/readout regeneration of alpha coefficient | partial_m delta_lambda_rad + partial_m readout_alpha | radiative/readout closure preserves the same Q_ONLY/REP_TOPOLOGICAL rule after variation | UNSIGNED | tree-level zero fails to imply observed alpha silence | false |
| ZA3218_4_total | Z_A = C_P N_Q + lambda_A + f_m(m) + delta_lambda_rad + readout_alpha | honest EM kinetic coefficient entering -1/4 Z_A F_Q^2 | b_alpha_m = partial_m ln Z_A = (partial_m Z_A)/Z_A | all nonparent terms absent/stationary and parent piece fixed | FINITE_BRANCH_RETAINED | b_alpha_m must be source-backed or bounded before local tests | false |

## b_alpha_m Zero Theorem Attempt

| theorem_id | claim_piece | statement | status | what_it_buys | missing_for_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| BAM3218_0_exact_formula | memory slope of alpha coefficient | For S_EM=-1/4 int Z_A(m,q,readout) F_Q^2, b_alpha_m := partial_m ln Z_A\|m_* = [partial_m(C_P N_Q)+partial_m lambda_A+f_m'(m_*)+partial_m delta_lambda_rad+partial_m readout_alpha]/Z_A(m_*). | EXACT_DECOMPOSITION | turns the EM coupling problem into a finite list of derivative owners | zero or source-backed value for every numerator term and positive Z_A denominator | false |
| BAM3218_1_Q_ONLY_zero | typed parent gauge norm kills parent numerator | If C_P, T_Q, N_Q=<T_Q,T_Q>_P, charge lattice, and current owner are fixed parent/representation data and the EM coefficient domain is Q_ONLY/REP_TOPOLOGICAL, then partial_m(C_P N_Q)=0. | EXACT_CONDITIONAL_THEOREM | kills the parent curvature-norm part of b_alpha_m | parent T_Q object, fixed nonrescalable norm/level, same current owner, and no readout drift | false |
| BAM3218_2_no_extra_F2_zero | no-extra-F2 kills lambda/f_m numerator | If the parent visible operator domain forbids independent lambda_A F_Q^2 and f_m(m)F_Q^2 terms, then partial_m lambda_A=f_m'(m_*)=0 by absence. | EXACT_CONDITIONAL_THEOREM | kills the live scalar gauge-kinetic counterterm | operator-domain exhaustion/no-hidden-visible coefficient theorem or product sequester signed for EM | false |
| BAM3218_3_double_zero_subroute | strict double-zero can kill slope without forbidding a memory deformation | If f_m(m)=lambda_m F(m) with F(m_*)=F'(m_*)=0 and m is locally locked to m_*, then f_m'(m_*)=0 even though f_m'' can contribute to the memory Hessian. | EXACT_CONDITIONAL_THEOREM | permits a controlled EM-memory deformation while removing the linear EM source | parent source-root F, same-branch local lock, correction bound, and no singular inverse-zero factors | false |
| BAM3218_4_readout_guard | observed alpha needs effective/readout closure | Even if the bare F_Q^2 coefficient is fixed, b_alpha_m observed is not zero unless S_eff and alpha readout maps preserve the same Q_ONLY/REP_TOPOLOGICAL or double-zero rule. | REQUIRED_GUARD_UNSIGNED | prevents tree-level alpha silence from being overclaimed | radiative/readout closure with source paths | false |
| BAM3218_5_total_verdict | promote b_alpha_m=0 | b_alpha_m=0 follows only if BAM3218_1, BAM3218_2 or BAM3218_3, and BAM3218_4 close on the same parent branch with Z_A(m_*) positive and fixed. | FAIL_CURRENT_CLAIM | states the exact EM F2 win condition | fixed gauge norm, no-extra-F2 or strict double-zero source root, and readout closure are not parent-signed together | false |

## EM F2 Countermodel Ledger

| counter_id | countermodel | why_allowed_now | effect | kills_claim | needed_to_remove | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| CEX3218_0_fm_linear | Z_A(m)=Z_0+epsilon m | m is a scalar and F_Q^2 is gauge/diffeomorphism invariant; no parent object-language theorem forbids it | b_alpha_m=epsilon/Z_0 and J_m contains -epsilon F_Q^2/4 | b_alpha_m_zero | no-extra-F2 theorem, typed exclusion, or strict double-zero/evenness | false |
| CEX3218_1_fixed_norm_plus_lambda | Z_A=C_P N_Q + lambda_A(m) | fixed gauge norm alone does not forbid independent visible F_Q^2 counterterms | parent norm can be fixed while b_alpha_m survives through lambda_A | TQ_owner_implies_alpha_silence | operator-domain exhaustion/no independent F_Q^2 | false |
| CEX3218_2_compact_charge_not_coupling | compact U1 with integer charges and free kinetic coefficient Z_A | charge quantization/labels do not fix the continuous Maxwell kinetic coefficient | relative charge labels can be owned while alpha normalization remains unowned | compact_U1_implies_alpha_fixed | fixed nonrescalable fibre norm/level plus no-extra-F2 | false |
| CEX3218_3_readout_return | bare Z_A fixed, alpha_eff=alpha_0 exp(epsilon m) after readout | radiative/readout closure is unsigned | observed clocks/spectra can see alpha drift even if the bare action is clean | bare_zero_promotes_observed_zero | S_eff/readout functor closure | false |

## b_alpha_m Source Row Template

| row_id | quantity | definition | value | units | memory_normalization | denominator | operator_norm | source_path | equation_ref | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BAMSR3218_0_candidate | b_alpha_m | partial_m ln Z_A at local memory origin m_* | MISSING_NUMERIC_OR_THEOREM_ZERO | 1/[m] or dimensionless if m is normalized | MISSING_m_NORMALIZATION | Z_A(m_*) > 0 | \|\|F_Q^2\|\| on local support | MISSING_SOURCE_PATH | P8_Y5_R2FR_3218_ZA_MEMORY_DECOMPOSITION.csv:ZA3218_4_total | false |
| BAMSR3218_1_zero_switch_refusal | b_alpha_m_zero | theorem-zero switch for b_alpha_m | 0_requested_but_refused | same_as_b_alpha_m | MISSING_m_NORMALIZATION | MISSING_ZA_POSITIVE_OWNER | not_applicable_if_zero_proved | MISSING_PARENT_SIGNED_TQ_NO_EXTRA_F2_READOUT | P8_Y5_R2FR_3218_BALPHA_M_ZERO_THEOREM_ATTEMPT.csv:BAM3218_5_total_verdict | false |
| BAMSR3218_2_double_zero_candidate | b_alpha_m_from_double_zero | f_m'(m_*) if f_m=lambda_m F(m), F(m_*)=F'(m_*)=0 | 0_conditional_on_parent_source_root_and_local_lock | same_as_b_alpha_m | MISSING_m_STAR_AND_LOCAL_LOCK | Z_A(m_*) positive and finite | second-order correction needs \|\|F_Q^2\|\| and f_m'' bound | MISSING_PARENT_SOURCE_ROOT_FOR_EM_F2 | P8_Y5_R2FR_3218_BALPHA_M_ZERO_THEOREM_ATTEMPT.csv:BAM3218_3_double_zero_subroute | false |

## Decision

`BALPHA_M_FORMULA_DERIVED_ZERO_THEOREM_CONDITIONAL_COUNTERMODELS_RETAINED_SOURCE_ROW_STAGED`.

Claim status: `NO_BALPHA_M_ZERO_NO_EM_LOCK_NO_LOCAL_GR_CLAIM`.

Best next route: try the strict double-zero subroute specifically for the EM F2 coefficient, because it may kill b_alpha_m without deriving the full gauge norm value; otherwise source b_alpha_m as a finite residual.

Next target:

```text
3219-Y5-R2FR-EM-F2-strict-double-zero-source-root-or-balpha-m-finite-bound-under-AX1090
```

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3218_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3218_ZA_MEMORY_DECOMPOSITION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3218_BALPHA_M_ZERO_THEOREM_ATTEMPT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3218_EM_F2_COUNTERMODEL_LEDGER.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3218_BALPHA_M_SOURCE_ROW_TEMPLATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3218_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3218_VALIDATION.csv`

## Validation

| check_id | pass | detail |
| --- | --- | --- |
| VAL3218_00_inputs_exist | true | inputs=11 |
| VAL3218_01_decomposition | true | ZA3218_0_parent_norm;ZA3218_1_lambda_visible;ZA3218_2_hidden_scalar;ZA3218_3_radiative_readout;ZA3218_4_total |
| VAL3218_02_exact_formula | true | b_alpha_m=(partial_m Z_A)/Z_A |
| VAL3218_03_zero_claim_blocked | true | fixed norm/no-extra-F2-or-double-zero/readout closure not signed together |
| VAL3218_04_countermodels | true | CEX3218_0_fm_linear;CEX3218_1_fixed_norm_plus_lambda;CEX3218_2_compact_charge_not_coupling;CEX3218_3_readout_return |
| VAL3218_05_source_rows | true | BAMSR3218_0_candidate;BAMSR3218_1_zero_switch_refusal;BAMSR3218_2_double_zero_candidate |
| VAL3218_06_claims_blocked | true | claim_rows_true=0 |
| VAL3218_07_no_formalization_workbench_edit | true | no formalization-workbench paths are output targets |
| VAL3218_08_csv_parse | true | P8_Y5_R2FR_3218_INPUTS.csv;P8_Y5_R2FR_3218_ZA_MEMORY_DECOMPOSITION.csv;P8_Y5_R2FR_3218_BALPHA_M_ZERO_THEOREM_ATTEMPT.csv;P8_Y5_R2FR_3218_EM_F2_COUNTERMODEL_LEDGER.csv;P8_Y5_R2FR_3218_BALPHA_M_SOURCE_ROW_TEMPLATE.csv;P8_Y5_R2FR_3218_DECISION.csv |
| VAL3218_09_next_target | true | 3219-Y5-R2FR-EM-F2-strict-double-zero-source-root-or-balpha-m-finite-bound-under-AX1090 |

All generated rows remain `valid_for_claim=false`.
