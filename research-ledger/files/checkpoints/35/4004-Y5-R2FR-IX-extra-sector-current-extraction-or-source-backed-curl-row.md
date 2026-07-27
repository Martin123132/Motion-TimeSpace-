# 4004 - I_X Extra-Sector Current Extraction Or Source-Backed Curl Row

- Timestamp: `2026-07-01T19:42:41+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## Result

`I_X` has been reduced to a clean fork, not a foggy missing variable.

`I_X := |d_field alpha_tau^X|/M_H_ref`, where

`alpha_tau^X := int_S(delta Q_tau^X - i_tau Theta_X)`.

## Fork A: Auxiliary Zero

If the extra sector is algebraic/auxiliary, with no `D_mu X`, no derivative boundary term, no matter/source/readout coupling to `X`, and no boundary hair, then:

`Theta_X = 0`, `Q_tau^X = 0/proper`, `alpha_tau^X = 0`, so `I_X = 0`.

This is the low-scrutiny route because it kills the symplectic current structurally rather than tuning it.

The R_AB compatibility block is the clearest current candidate: `S_R=int mu_parent Lambda_R [R_AB-C_AB(q(Phi),theta,top)]`. Current evidence supports this as an exact conditional theorem, not yet a parent necessity theorem.

## Fork B: Derivative Current

If a kinetic/elastic term is legal, then the current is real:

`Theta_X^mu = -Z_X nabla^mu X delta X`,

`Pi_X^n = -Z_X n_mu nabla^mu X`.

That branch needs either a field-specific positive-operator nohair proof or a finite source row with `Z_X`, `M_X^2`, `Q_X_source`, `q_test_X`, `PiM_H_projection`, `boundary_flux`, and `tau_R10`.

## Guard

Even if `Theta_X=0`, local GR is not won unless bulk stress, matter/source descent, boundary/reference, projector, and `Dq` leaks are also zero/bounded. This prevents an auxiliary shortcut from secretly hiding a force in `C_tau_bulk`.

## Evaluator Results

- `CASE4004_0_auxiliary_all_signed`: `CONDITIONAL_AUXILIARY_ZERO`, Theta_X_zero=True, Q_tau_X_zero=True, I_X=`0.0`, claim=False, next=`promote only after parent necessity and remaining 4003 components close`
- `CASE4004_1_auxiliary_matter_missing`: `THETA_ZERO_BUT_BULK_SOURCE_OPEN`, Theta_X_zero=True, Q_tau_X_zero=True, I_X=`I_X_SYMPLECTIC_ZERO_CONDITIONAL_CTAU_OPEN`, claim=False, next=`prove matter descent/bulk stress guard or retain C_tau_bulk/source row`
- `CASE4004_2_derivative_term_present`: `DERIVATIVE_CURRENT_REQUIRES_SOURCE_ROW`, Theta_X_zero=False, Q_tau_X_zero=False, I_X=`MISSING_Z_X_M_X_Q_SOURCE_Q_TEST_BOUNDARY`, claim=False, next=`fill finite coefficient row or prove positive nohair`
- `CASE4004_3_positive_operator_template_only`: `DERIVATIVE_CURRENT_REQUIRES_SOURCE_ROW`, Theta_X_zero=False, Q_tau_X_zero=False, I_X=`MISSING_Z_X_M_X_Q_SOURCE_Q_TEST_BOUNDARY`, claim=False, next=`fill finite coefficient row or prove positive nohair`
- `CASE4004_4_positive_operator_all_signed`: `CONDITIONAL_POSITIVE_OPERATOR_ZERO`, Theta_X_zero=False, Q_tau_X_zero=False, I_X=`0.0`, claim=False, next=`requires actual parent L_X certificate before any claim`
- `CASE4004_5_source_backed_nonclaim_row`: `NONCLAIM_NUMERIC_SOURCE_ROW_ACCEPTED`, Theta_X_zero=False, Q_tau_X_zero=False, I_X=`FINITE_ROW_AVAILABLE_TOTAL_CHAIN_OPEN`, claim=False, next=`score as residual only, do not claim local GR`
- `CASE4004_6_missing_schema`: `BLOCKED_MISSING_SCHEMA`, Theta_X_zero=False, Q_tau_X_zero=False, I_X=`MISSING`, claim=False, next=`repair schema/source rows`

## Verdict

Best route: prove auxiliary necessity/no-derivative protection. If that fails, stop trying to make `I_X` disappear and fill the first real coefficient row.

## Next Target

- `4005-Y5-R2FR-auxiliary-necessity-or-first-real-IX-source-coefficient.md`
- `scripts/Y5_R2FR_4005_auxiliary_necessity_or_first_real_IX_source_coefficient.py`

## Source Count

- source needles found: `21/21`
