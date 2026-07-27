# 4725 - No-Bare-R2 Parent Grammar Proof or cBare Finite Row

Generated: `2026-07-07T22:14:03+00:00`

## Purpose

4725 attacks the bare `R^2/f(R)` component of `c_R2_eff_total`. The aim is not to circle the blocker, but to decide whether the parent action language actually forbids a bare curvature-square slot or whether a finite `c_bare` row must survive.

## What Actually Moved

- The older action documents support an EH-plus-MTS-potential effective action with no explicit direct bare `R^2` term.
- The stronger statement is only candidate-branch safe: the 3890 grammar excludes a direct bare slot, but it is not global corpus adoption.
- Global `c_bare` still survives through `S_R11`/non-EH factorization and possible counterterm/singular-running routes.
- Therefore `c_bare` is now split rather than vaguely missing: `c_bare_global = c_bare_direct + c_R11_curvature_square + c_counterterm`.

## Grammar Audit

- `NBARE4725_0_core_action_shape`: SUPPORTS_NO_DIRECT_BARE_SLOT
- `NBARE4725_1_fundamental_action_shape`: SUPPORTS_NO_DIRECT_BARE_SLOT
- `NBARE4725_2_2485_derivative_grammar`: BLOCKS_GLOBAL_NO_BARE_PROOF
- `NBARE4725_3_3007_minimal_grammar`: GRAMMAR_CONTRACT_NOT_PARENT_SIGNED
- `NBARE4725_4_3890_candidate_action`: CANDIDATE_DIRECT_SLOT_EXCLUDED
- `NBARE4725_5_R11_survivor`: RESIDUAL_CURVATURE_SQUARE_SURVIVES
- `NBARE4725_6_4720_selector`: CONDITIONAL_ZERO_ROUTE
- `NBARE4725_7_1589_hunt`: NO_PARENT_NO_BARE_CLAUSE_FOUND
- `NBARE4725_8_verdict`: DIRECT_ZERO_CANDIDATE_GLOBAL_FINITE_ROW

## cBare Split

- `CBS4725_0_direct_metric_slot`: 0 in the 3890 candidate grammar branch if that branch is adopted
- `CBS4725_1_R11_residual_slot`: MISSING_FACTORISATION_ZERO_OR_NUMERIC_VALUE
- `CBS4725_2_counterterm_slot`: MISSING_NO_COUNTERTERM_PARENT_RULE
- `CBS4725_3_global_cbare`: MISSING_TOTAL_c_bare_ZERO_OR_VALUE

## Finite Rows

- `CBARE4725_0_direct_candidate_zero`: 0_IF_3890_CANDIDATE_GRAMMAR_ADOPTED
- `CBARE4725_1_R11_residual`: MISSING_R11_FACTORISATION_ZERO_OR_NUMERIC_COEFFICIENT
- `CBARE4725_2_counterterm`: MISSING_NO_SINGULAR_COUNTERTERM_RULE_OR_VALUE
- `CBARE4725_3_global_effective`: c_bare_direct + c_R11_curvature_square + c_counterterm

## Gates

- `GATE4725_0_sources_verified`: NONE
- `GATE4725_1_global_no_bare_R2_signed`: GLOBAL_PARENT_GRAMMAR_UNSIGNED
- `GATE4725_2_candidate_direct_slot_zero`: CANDIDATE_ONLY_NOT_CLAIM
- `GATE4725_3_R11_residual_zero`: R11_RESIDUAL_CHANNEL_LIVE
- `GATE4725_4_counterterm_zero`: COUNTERTERM_RULE_MISSING
- `GATE4725_5_cbare_numeric_or_zero`: MISSING_GLOBAL_CBARE_ZERO_OR_VALUE
- `GATE4725_6_local_GR_R2_channel_closed`: CBARE_GLOBAL_RETAINED_NONCLAIM

## Decision

`NO_DIRECT_BARE_R2_SLOT_EXCLUDED_IN_CANDIDATE_GRAMMAR_GLOBAL_CBARE_UNSIGNED_FINITE_ROW_STAGED_NONCLAIM`

## Next Target

`4726-Y5-R2FR-hidden-exchange-BLinvB-zero-or-memory-fibre-vertex-bound.md`
