# 4327 - Dq geometry no-shadow or epsilon geom profile reduction

## Verdict

- Rejected full geometry zero because `A_MF/no-shadow` remains unsigned.
- Narrowed source-readout to `epsilon_geom_core + Xi_src_hidden`.
- Reduced geometry to the core conformal/disformal/shadow-frame problem.
- Next target is parent no-extra-frame signature or finite `c_g/b_dis` bound runner.

## Bottleneck Formulas
| formula_id | name | formula | status |
| --- | --- | --- | --- |
| F4327_1_core_frame_bound | core frame-shadow finite bound | epsilon_geom_core <= C_cg sum_s \|c_s\| + C_dis sum_s \|b_dis_s\| + C_shadow sum_s \|\|h_s^perp\|\| + C_readout epsilon_readout_frame + C_terminal epsilon_terminal + epsilon_constitutive_reopen | BOUND_READY_VALUES_MISSING |
| F4327_2_core_zero | no-extra-frame zero | parent no-extra-frame/no-shadow action-domain signature => c_s=b_dis_s=D_Hperp h_s^perp=epsilon_readout_frame=epsilon_terminal=epsilon_constitutive_reopen=0 => epsilon_geom_core=0 | CONDITIONAL_ZERO_ROUTE_NOT_PARENT_SIGNED |
| F4327_3_source_readout_bottleneck | narrowed source-readout bottleneck | epsilon_source_readout <= (L_T L_mg + L_g)epsilon_geom_core + Xi_src_hidden | DERIVED_BOTTLENECK |

## Decision
| decision_id | result | reason | next_action |
| --- | --- | --- | --- |
| DEC4327_0 | GEOMETRY_ZERO_REJECTED_SOURCE_READOUT_NARROWED_TO_CORE_FRAME_SHADOW_PLUS_XI_NONCLAIM | The full geometry/no-shadow zero remains unsigned, but after 4321-4326 the source-readout chain is narrowed to core frame-shadow geometry plus Xi_src_hidden. | 4328-Y5-R2FR-parent-no-extra-frame-signature-or-cg-bdis-bound-runner.md |

## Next Target
| next_target_id | next_target | preferred_route | fallback_route |
| --- | --- | --- | --- |
| NT4327_0 | 4328-Y5-R2FR-parent-no-extra-frame-signature-or-cg-bdis-bound-runner.md | prove parent no-extra-frame/no-shadow action-domain signature for ordinary matter, EM/Hodge and readouts | build finite c_g, b_dis, h_perp, readout-frame and constitutive-tail bound runner with local PPN/R10/clock/orbital projections |
