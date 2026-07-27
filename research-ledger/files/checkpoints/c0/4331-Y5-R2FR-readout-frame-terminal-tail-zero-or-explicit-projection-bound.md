# 4331 Y5-R2FR readout-frame terminal tail zero or explicit projection bound

Marker: `PPC4161_READOUT_FRAME_TERMINAL_TAIL_ZERO_OR_PROJECTION_BOUND_4331`

Decision: `QUOTIENT_NATURAL_PURE_READOUT_ZERO_IMPORTED_TERMINAL_SHORTCUT_REJECTED_REDUCED_GEOMETRY_CORE_HANDS_TO_XI_NONCLAIM`

## Result

`epsilon_readout_frame` and `epsilon_terminal` are now branch-resolved. The zero route is quotient-natural readout plus action-domain ownership, not terminal-object rhetoric.

## Reduced Geometry Core

| formula_id | formula | status |
| --- | --- | --- |
| F4331_0_readout_zero | R_obs(Phi)=Rbar(q(Phi)) and Hperp in ker(Dq) => D_Hperp R_obs = DRbar[Dq(Hperp)] = 0 | CONDITIONAL_ZERO_DERIVED |
| F4331_1_pure_postprocessing_guard | readout_after_variation and no readout slot in S_parent/S_eff => epsilon_readout_frame=0 | CONDITIONAL_ZERO_DERIVED |
| F4331_2_terminal_reject | terminal e_pub exists does not imply no A_g/B_dis/h_perp/readout frame slot in S_matter or S_EM | REJECTED_SHORTCUT |
| F4331_3_terminal_action_domain_zero | e_obs=e_bar(q) used in the action domain and no separate terminal-to-matter frame map => epsilon_terminal=0 | CONDITIONAL_ZERO_DERIVED_NOT_SHORTCUT |
| F4331_4_projection_bound | epsilon_projection_open <= \|R_post_action_reentry\| + \|R_terminal_shortcut\| + \|R_projector_fit\| + \|R_source_readout_reentry\| + sum_a \|Pi_a R_a\| | BOUND_RETAINED_OUTSIDE_BRANCH |
| F4331_5_geometry_core_update | epsilon_geom_core <= C_EMopen epsilon_EM_open_boundary + C_coeff_open epsilon_coeff_open + C_proj epsilon_projection_open + tail_guard_sum | REDUCED_BUT_OPEN |
| F4331_6_source_readout_update | epsilon_source_readout <= (L_T L_mg + L_g) epsilon_geom_core_after_projection + Xi_src_hidden | NONCLAIM_HANDOFF_TO_XI |

## Remaining Projection Tails

| tail_id | symbol | observable_links | status |
| --- | --- | --- | --- |
| TAIL4331_0_post_action_reentry | R_post_action_reentry | PPN; clocks; source readout; R10; orbital | RETAINED_OUTSIDE_BRANCH |
| TAIL4331_1_terminal_shortcut | R_terminal_shortcut | common frame coupling; PPN gamma; WEP; clocks | REJECTED_AS_ZERO_RETAINED_AS_BOUND_IF_USED |
| TAIL4331_2_projector_fit | R_projector_fit | PPN; R10; clock; orbital scoring | RETAINED_OUTSIDE_BRANCH |
| TAIL4331_3_source_readout_reentry | R_source_readout_reentry | Newtonian mass; WEP; orbital GM; clock/source coupling | RETAINED_OUTSIDE_BRANCH |
| TAIL4331_4_arena_projection | Pi_arena_tail | R10; PPN; clocks; orbital systems | RETAINED_FOR_LOCAL_TEST_RUNNERS |

## Next

| next_target | target_question | preferred_route |
| --- | --- | --- |
| 4332-Y5-R2FR-Xi-src-hidden-zero-or-source-label-tail-bound.md | Can Xi_src_hidden be zeroed by source-label forgetting, Hilbert source ownership and no hidden source-prefactor slots, or must it become a finite multi-arena source-label tail? | prove no hidden source weights, no source normalization reentry, no direct matter-X vertex and no environment/source-label selector in the parent/effective action |
