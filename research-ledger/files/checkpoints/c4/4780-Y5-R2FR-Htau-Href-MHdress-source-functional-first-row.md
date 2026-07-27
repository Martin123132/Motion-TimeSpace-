# 4780 — Htau/Href/MHdress Source-Functional First Row

Generated: `2026-07-08T04:17:57+00:00`

## Result

4780 adds the source-functional runner:

```text
D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Htau_Href_MHdress_source_runner.py
```

It computes only:

```text
M_H^dress = H_tau[S_link;tau,e_obs] - H_ref[Sigma_ref;tau,e_obs].
```

It does **not** define `M_H^dress` from observed `GM/G_cal`.

## Source Contract

| contract_id | contract_statement | status |
| --- | --- | --- |
| HC4780_0_definition | M_H^dress := H_tau[S_link;tau,e_obs] - H_ref[Sigma_ref;tau,e_obs] | definition ready; values missing |
| HC4780_1_no_GM_backfill | M_GM_cal=mu_ref/G_cal is comparator only | enforced by runner |
| HC4780_2_Htau_input | H_tau[S_link;tau,e_obs] | missing parent/numeric evaluation |
| HC4780_3_Href_input | H_ref[Sigma_ref;tau,e_obs] | missing parent/numeric evaluation |
| HC4780_4_downstream | M_H^dress feeds MHdress_E00_open_arena_runner.py | wired in 4780 |

## Htau/Href Source Runner Output

| source_id | M_H_dress_kg | Delta_MH_rel | runner_status |
| --- | --- | --- | --- |
| private_selector_missing_Htau_Href | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | BLOCKED_MISSING_HTAU_OR_HREF |
| private_selector_counterfactual_Htau_minus_Href_equals_comparator | 1.988409870698051e+30 | 0.000000000000000e+00 | MHDRESS_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM |

## Downstream Newton/Orbital Evaluator Output

| arena_id | M_GM_cal_kg | Delta_MH_rel | eta_E00_abs | runner_status |
| --- | --- | --- | --- | --- |
| private_selector_missing_Htau_Href | 1.988409870698051e+30 | MISSING_NUMERIC_VALUE | 0.000000000000000e+00 | BLOCKED_MISSING_MHDRESS |
| private_selector_counterfactual_Htau_minus_Href_equals_comparator | 1.988409870698051e+30 | 0.000000000000000e+00 | 0.000000000000000e+00 | RUNNER_SMOKE_PASS_NONCLAIM |

## Score Gate Update

| source_id | M_H_dress_kg | source_runner_status | open_runner_status |
| --- | --- | --- | --- |
| private_selector_missing_Htau_Href | MISSING_NUMERIC_VALUE | BLOCKED_MISSING_HTAU_OR_HREF | BLOCKED_MISSING_MHDRESS |
| private_selector_counterfactual_Htau_minus_Href_equals_comparator | 1.988409870698051e+30 | MHDRESS_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | RUNNER_SMOKE_PASS_NONCLAIM |

## Anti-Circularity Audit

| audit_id | rule | status |
| --- | --- | --- |
| AC4780_0 | source runner computes M_H^dress only from H_tau-H_ref, never from GM/G_cal | PASS_HTAU_HREF_ONLY |
| AC4780_1 | missing physical H_tau/H_ref row blocks instead of importing comparator mass | PASS_MISSING_BLOCKS |
| AC4780_2 | counterfactual Htau/Href row is smoke-only and claim_allowed=false | PASS_SMOKE_FIREWALL |
| AC4780_3 | downstream open runner receives M_H only from source-runner output | PASS_CHAINED_SOURCE_DISCIPLINE |

## Route Selection

| route_id | route | selection_status |
| --- | --- | --- |
| RT4780_0_Htau | evaluate H_tau[S_link;tau,e_obs] from parent local packet charge | SELECTED_NEXT |
| RT4780_1_Href | evaluate or bound H_ref[Sigma_ref;tau,e_obs] with fixed source-blind reference | SELECTED_NEXT_PARALLEL |

## Decision

`HTAU_HREF_MHDRESS_SOURCE_FUNCTIONAL_RUNNER_IMPLEMENTED_MISSING_PARENT_CHARGE_BLOCKS_COUNTERFACTUAL_SMOKE_PASSES_NONCLAIM`

## Next Target

`4781-Y5-R2FR-Htau-Href-parent-charge-evaluation-or-reference-bound.md`
