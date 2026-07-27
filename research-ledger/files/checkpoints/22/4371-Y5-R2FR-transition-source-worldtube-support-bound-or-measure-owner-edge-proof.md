# 4371: source/worldtube support bound or measure-owner edge proof

Marker: `PPC4161_TRANSITION_SOURCE_WORLDTUBE_SUPPORT_BOUND_OR_MEASURE_OWNER_EDGE_PROOF_4371`

## What changed

- Filled source-backed `R/r` examples for the 4370 `K_N(s)` gate.
- Converted support geometry into immediate `E_perp <= delta_N/K_N(s)` multipliers.
- Proved a conditional measure-owner lemma, but kept it unsigned.
- Kept the branch nonclaim because `E_perp` and `delta_N` remain missing.

## Decision row

| decision_id | decision | summary | next_target |
| --- | --- | --- | --- |
| DEC4371_0 | SOURCE_SUPPORT_GEOMETRY_ANCHORS_FILLED_MEASURE_OWNER_EDGE_CONDITIONAL_EPERP_STILL_UNSOURCED_NONCLAIM | 4371 fills source-backed support geometry examples for the epsilon_Gsrc_perp gate using NASA solar-system size/distance rows. The resulting K_N(s) values show that far-field solar and Earth-Moon source-shape residuals are geometrically suppressed after monopole subtraction. However E_perp and delta_N are still not sourced, so the rows are gate-ready but nonclaim. The measure-owner route is sharpened to a conditional lemma: a q-basic species-blind measure/Jacobian/hbar owner would zero the measure component, but 4361/1606 keep that edge unsigned and it would not alone zero all epsilon_Gsrc_perp components. | 4372-Y5-R2FR-transition-Eperp-envelope-decomposition-or-measure-owner-action-line-proof.md |

## Next target

| next_id | target | question | preferred_route | alternate_zero_route | avoid |
| --- | --- | --- | --- | --- | --- |
| NT4371_0 | 4372-Y5-R2FR-transition-Eperp-envelope-decomposition-or-measure-owner-action-line-proof.md | Can E_perp be decomposed into source-measure, source-mass, transition-hair, Xi and T components, or can the measure-owner action line be proved? | decompose E_perp into component envelopes and try to zero/source the largest pieces | prove the species-blind measure/Jacobian/hbar owner edge from the parent action line | treating average support geometry as an empirical local-GR pass |
