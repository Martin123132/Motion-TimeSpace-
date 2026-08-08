# 4333 Y5-R2FR standard branch source-readout rollup or open-tail test pack

Marker: `PPC4161_STANDARD_SOURCE_READOUT_ROLLUP_OR_OPEN_TAIL_TEST_PACK_4333`

Decision: `STANDARD_BRANCH_SOURCE_READOUT_CLOSURE_CONTRACT_DERIVED_OPEN_TAIL_TEST_PACK_RETAINED_NONCLAIM`

## Result

The local source-readout chain now has a clean branch-local closure contract: all standard-zero clauses imply `epsilon_source_readout=0`. The nonstandard route is no longer vague; it is the open-tail test pack below.

## Rollup

| formula_id | formula | status |
| --- | --- | --- |
| F4333_0_reduced_geometry | epsilon_geom_core_after_projection <= C_EMopen epsilon_EM_open_boundary + C_coeff_open epsilon_coeff_open + C_proj epsilon_projection_open + tail_guard_sum | IMPORTED |
| F4333_1_Xi_reduced_source_readout | epsilon_source_readout <= (L_T L_mg + L_g) epsilon_geom_core_after_projection + Xi_open | IMPORTED |
| F4333_2_standard_geometry_zero | epsilon_EM_open_boundary=epsilon_coeff_open=epsilon_projection_open=tail_guard_sum=0 => epsilon_geom_core_after_projection=0 | DERIVED_BRANCH_CONTRACT |
| F4333_3_standard_source_readout_zero | Xi_src_hidden=0 and epsilon_geom_core_after_projection=0 => epsilon_source_readout=0 | DERIVED_BRANCH_CONTRACT |
| F4333_4_open_tail_envelope | epsilon_source_readout_open <= (L_T L_mg + L_g)(C_EMopen epsilon_EM_open_boundary + C_coeff_open epsilon_coeff_open + C_proj epsilon_projection_open + tail_guard_sum) + Xi_open | TEST_PACK_INPUT |
| F4333_5_local_arena_projection | R_arena <= Pi_arena^Xi Xi_open + Pi_arena^EM epsilon_EM_open_boundary + Pi_arena^coeff epsilon_coeff_open + Pi_arena^proj epsilon_projection_open + Pi_arena^guard tail_guard_sum + Pi_arena^tau epsilon_tau_open + Pi_arena^domain epsilon_boundary_projector_open | SOURCE_MATRIX_REQUIRED |
| F4333_6_claim_gate | local claim requires all standard-zero clauses signed, all open tails zero or source-bounded, and all Pi_arena transfer constants fixed before scoring | CLAIM_BLOCKED |

## Test Pack

| arena | tail_inputs | required_sources | projection_contract | status |
| --- | --- | --- | --- | --- |
| R10 short-range fifth-force | Xi_open; epsilon_projection_open; epsilon_coeff_open; tail_guard_sum; epsilon_boundary_projector_open | lambda profile; alpha transfer; lab-composition coupling; boundary/domain support; valid bound curve | Pi_R10 fixed before fit and sourced row-by-row | NOT_READY_FOR_CLAIM |
| PPN/Cassini/local solar tests | epsilon_projection_open; Xi_open; epsilon_coeff_open; tail_guard_sum; epsilon_tau_open | gamma/beta transfer; preferred-frame map; range profile; clock/reference convention | Pi_PPN fixed before scoring, not post-fit | NOT_READY_FOR_CLAIM |
| clock/redshift/atomic standards | epsilon_tau_open; epsilon_coeff_open; Xi_open; epsilon_EM_open_boundary | clock species map; alpha/mass sensitivity; tau reference; EM/radiative collar policy | Pi_clock fixed by metrology source, not by residual minimization | NOT_READY_FOR_CLAIM |
| orbital/ephemeris/binary dynamics | epsilon_tau_open; epsilon_projection_open; Xi_open; tail_guard_sum | GM convention; orbital frame; range/time transfer; source support and no-flux domain | Pi_orbital fixed before using ephemeris residuals | NOT_READY_FOR_CLAIM |
| EM/stress/Poynting/radiation | epsilon_EM_open_boundary; epsilon_coeff_open; Xi_open | open radiation flux; constitutive deformation; source current normalization; Hodge ownership | Pi_EM separates Hilbert EM flux from extra force tail | NOT_READY_FOR_CLAIM |
| WEP/source-composition | Xi_open; epsilon_projection_open; ordinary_matter_shadow_open | composition charge map; source labels; matter action-domain ownership; material selector policy | Pi_WEP source-composition transfer fixed before comparison | NOT_READY_FOR_CLAIM |

## Next

| next_target | target_question | preferred_route |
| --- | --- | --- |
| 4334-Y5-R2FR-local-test-projection-matrix-source-contract-or-R10-PPN-smoke-runner.md | Can the open-tail test pack be converted into source-backed local projection matrices and a first nonclaim R10/PPN smoke runner? | source or define Pi_R10, Pi_PPN, Pi_clock, Pi_orbital and Pi_EM before scoring; keep placeholder rows invalid for claim |
