# 4368: parent-sign common source normalization or final WEP product quarantine

Marker: `PPC4161_TRANSITION_PARENT_SIGN_COMMON_SOURCE_NORMALIZATION_OR_FINAL_WEP_PRODUCT_QUARANTINE_4368`

## What changed

- Tried to activate the clean common-source route from 4367.
- Rejected activation in the current corpus because the actual 4363 row is still Ti/Pt/source/readout-relative.
- Locked a current-corpus quarantine: `PI4363_WEP_product` is WEP/source-composition only, not a PPN/Newton/local-GR export row.
- Selected the next real route: non-product source coupling (`epsilon_Gsrc_open`, `Xi_open`, `T_open`) or one concrete owner/no-`w_A` parent signature.

## Decision row

| decision_id | decision | summary | next_target |
| --- | --- | --- | --- |
| DEC4368_0 | PARENT_COMMON_SOURCE_NORMALIZATION_NOT_SIGNED_WEP_PRODUCT_FINAL_QUARANTINE_NONPRODUCT_CSRC_ROUTE_SELECTED_NONCLAIM | 4368 attempts to activate the common-source route and rejects it in the current corpus. The theorem from 4367 remains valid conditionally, but the actual 4363 product row is Ti/Pt/source/readout-relative and cannot be exported to PPN/Newton/local-GR without a parent action proof. The WEP product is therefore quarantined as WEP-only, and the next serious local-GR route is non-product source coupling: epsilon_Gsrc_open, Xi_open, T_open, or a concrete owner/no-wA activation proof. | 4369-Y5-R2FR-transition-nonproduct-Csrc-source-normalization-row-or-owner-no-wA-activation.md |

## Next target

| next_id | target | question | preferred_route | alternate_zero_route | avoid |
| --- | --- | --- | --- | --- | --- |
| NT4368_0 | 4369-Y5-R2FR-transition-nonproduct-Csrc-source-normalization-row-or-owner-no-wA-activation.md | Can the local-GR route be advanced through non-product source normalization or by activating one concrete owner/no-wA parent signature? | derive/project epsilon_Gsrc_open into Newton/PPN/source-normalization before trying to score local GR | parent-sign a specific ordinary-matter graph/measure/no-reentry edge that kills Xi_open or Delta_w_component_vector | re-exporting the quarantined WEP product to PPN/Newton/local-GR |
