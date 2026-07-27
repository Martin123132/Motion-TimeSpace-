# 4724 - Visible-Cell cR2 Zero Signature or R2 Mu Bound Runner

Generated: `2026-07-07T22:06:42+00:00`

## Purpose

4724 takes the best leap-forward route after 4723: try to make `c_R2_eff_total=0` from the visible-cell/no-grain derivation, and if that fails, stage a finite `mu/lambda_R/alpha_eff` runner without claiming local GR.

## What Actually Derived

- `c_R2_cell` has a genuine conditional zero route: the visible quadratic term scales like `ell_cell^2` and vanishes in the gauge-refinement/smooth-response/no-singular-counterterm limit.
- The total coefficient is larger: `c_R2_eff_total = c_R2_cell + c_bare + 1/2 B^T L^-1 B + c_measure + c_boundary`.
- Therefore the local R2 channel is not closed unless the bare, hidden-exchange, measure and boundary pieces are also zero or source-bounded.

## Total Zero Theorem Rows

- `TCZ4724_0_total_law`: DERIVED_BOOKKEEPING_LAW
- `TCZ4724_1_no_cancellation_rule`: DERIVED_NO_SMUGGLING_RULE
- `TCZ4724_2_visible_cell_zero`: CONDITIONAL_DERIVATION_AVAILABLE
- `TCZ4724_3_bare_operator_zero`: UNPROVED_PARENT_GRAMMAR_CLAUSE
- `TCZ4724_4_hidden_exchange_zero`: UNSIGNED_HIDDEN_VERTEX_CLAUSE
- `TCZ4724_5_measure_boundary_zero`: UNSIGNED_MEASURE_BOUNDARY_CLAUSE
- `TCZ4724_6_verdict`: TOTAL_ZERO_NOT_PROVED

## Component Audit

- `CR2COMP4724_0_visible_cell`: CONDITIONAL_ZERO_ONLY
- `CR2COMP4724_1_bare`: MISSING_c_bare_ZERO_OR_VALUE
- `CR2COMP4724_2_hidden_exchange`: MISSING_B_L_MAP_OR_ZERO
- `CR2COMP4724_3_measure`: MISSING_MEASURE_ZERO_OR_VALUE
- `CR2COMP4724_4_boundary`: MISSING_BOUNDARY_ZERO_OR_VALUE
- `CR2COMP4724_5_total`: MISSING_TOTAL_ZERO_CERTIFICATE

## Mu Runner Results

- `MURUN4724_0_missing_total_mu`: BLOCKED_MISSING_PARENT_MU_ALPHA
- `MURUN4724_1_total_zero_if_signed`: BLOCKED_TOTAL_ZERO_UNSIGNED
- `MURUN4724_2_standard_template_bound`: TEMPLATE_ONLY_NOT_MTS_PREDICTION

## Gates

- `GATE4724_0_sources_verified`: NONE
- `GATE4724_1_visible_cell_zero_parent_signed`: REFINEMENT_GAUGE_SIGNATURE_UNSIGNED
- `GATE4724_2_total_cR2eff_zero`: BARE_HIDDEN_MEASURE_BOUNDARY_TERMS_UNSIGNED
- `GATE4724_3_mu_numeric_or_zero`: MISSING_PARENT_MU_OR_TOTAL_ZERO
- `GATE4724_4_alpha_eff_numeric_or_zero`: MISSING_ALPHA_EFF_BODY_CHARGE
- `GATE4724_5_bound_runner_claim_ready`: RUNNER_FAILS_CLOSED_NONCLAIM
- `GATE4724_6_local_GR_R2_channel_closed`: R2_CHANNEL_RETAINED

## Decision

`VISIBLE_CELL_CR2_ZERO_DERIVED_CONDITIONAL_TOTAL_CR2EFF_UNSIGNED_FINITE_MU_BOUND_RUNNER_STAGED_NONCLAIM`

## Next Target

`4725-Y5-R2FR-no-bare-R2-parent-grammar-proof-or-cbare-finite-row.md`
