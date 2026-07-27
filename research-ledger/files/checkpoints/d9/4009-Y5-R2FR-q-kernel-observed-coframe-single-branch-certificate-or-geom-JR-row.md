# 4009 - q-Kernel Observed-Coframe Single-Branch Certificate Or Geometric J_R Row

- Timestamp: `2026-07-01T20:23:12+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## Result

The direct quotient route is rejected for the current observer map.

If the public readout sees `A=T^2` and `B=S`, then `R_AB=ln(AB)` is not vertical: clocks, radial rulers, light bending and the matter coframe can all see it.

The clean route is different: parent-signed constraint-first elimination.

`E_Lambda: Omega_tr=Omega_ref -> T sqrt(S)=1 -> R_AB=0`.

After that reduction, there is no independent `v_R` tangent to public readout. This is not a gauge claim; it is auxiliary elimination before readout.

## Geometric Source Term

If the constraint-first route is not adopted, the honest residual is

`J_R_geom = int tau_a^mu D_R e_mu^a dmu_obs = 1/2 int sqrt(-g) T^{mu nu} D_R g_{mu nu}`.

So the geometry leak is now explicit: either eliminated by the cell-lock branch, or carried as a finite coefficient row.

## Single-Branch Conditions

- 4006 cell-lock action adopted before `q` and readout.
- no independent derivative/kinetic `R_AB` grammar.
- one observed coframe feeds EH, matter, clocks, rods and source normalization.
- 4008 source-label-forgetting matter constructor adopted in the same branch.
- boundary/worldtube reciprocal flux closed or bounded.

## Evaluator Results

- `CASE4009_0_direct_full_metric`: q=`DIRECT_VERTICALITY_FAILS`, J_R_geom=`J_R_GEOM_LIVE`, next=`do not call R_AB vertical; use constraint-first route or finite geometry row`
- `CASE4009_1_class_quotient`: q=`CLASS_QUOTIENT_CIRCULAR`, J_R_geom=`J_R_GEOM_NOT_ZEROED`, next=`derive primitive equivalence before readout or reject`
- `CASE4009_2_constraint_first_bulk`: q=`CONDITIONAL_CONSTRAINT_FIRST_BULK_PASS`, J_R_geom=`J_R_GEOM_BULK_ZERO_CONDITIONAL`, next=`assemble single-branch adoption and attack boundary/source-normalization gates`
- `CASE4009_3_constraint_hidden_coframe`: q=`CONSTRAINT_FIRST_HIDDEN_COFRAME_OPEN`, J_R_geom=`C_HIDDEN_COFRAME_R_LIVE`, next=`prove one observed coframe/no hidden metric leakage`
- `CASE4009_4_constraint_matter_packet_open`: q=`CONSTRAINT_FIRST_MATTER_PACKET_OPEN`, J_R_geom=`SOURCE_LABEL_OR_CONSTANT_TERMS_LIVE`, next=`adopt 4008 constructor in same branch or keep coefficient pack`
- `CASE4009_5_constraint_boundary_open`: q=`BULK_GEOMETRY_ZERO_BOUNDARY_OPEN`, J_R_geom=`J_R_BOUNDARY_WORLD_TUBE_OPEN`, next=`derive boundary/worldtube nohair or finite boundary row`

## Verdict

This is stricter and cleaner than claiming `R_AB` is gauge. Direct verticality fails; constraint-first elimination remains viable. The next live term is boundary/worldtube flux.

## Next Target

- `4010-Y5-R2FR-boundary-worldtube-nohair-or-JR-boundary-row.md`
- `scripts/Y5_R2FR_4010_boundary_worldtube_nohair_or_JR_boundary_row.py`

## Source Count

- source needles found: `31/31`
