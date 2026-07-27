# 4007 - Cell-Lock Matter/Readout Descent Or J_R Bound Row

- Timestamp: `2026-07-01T20:10:32+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## Result

The descent route is real, but conditional. The exact object is

`J_R := delta_R(S_matter + B_readout + S_eff)`.

Using the 4006 equation,

`lambda_R = -(J_R + delta B_R/delta R_AB + readout_regen)`.

So the cell-lock branch only becomes stress/current silent if `J_R`, boundary hair and readout regeneration all vanish.

## Derivation

If ordinary matter is a source-label-forgetting quotient functor,

`S_matter = Sbar_m[Obs(q(Phi)), psi, theta]`, with `v_R in ker(Dq)`,

then

`delta_R S_matter = (delta Sbar/dObs) DObs(Dq[v_R]) + sum_a (partial Sbar/partial theta_a) delta_R theta_a + marker/readout terms`.

The first term vanishes by the chain rule. The constants term vanishes only if masses, charges, `alpha_EM`, clocks and material standards are q-basic/fixed. The marker/readout terms vanish only if the parent grammar forgets source labels before variation and readout is fixed before variation.

## Countermodel

The surviving legal countermodel is simple:

`S_matter = sum_A w_A(R_AB) S_A`.

Then `J_R = sum_A (partial_R w_A) L_A + ...`. Ward conservation does not remove this because the weight is inserted before variation. This is the coupling leak we have been circling; now it has a name and formula.

## Verdict

- `J_R=0` is derivable, not assumed, under a parent-signed source-label-forgetting matter constructor.
- Current corpus does not yet sign that constructor in one branch.
- Therefore `J_R` remains a finite nonclaim row, with `eta_source_AB=2.8e-15` usable only as a bound scale, not as a theory coefficient.
- This moves the target from vague local-GR failure to one concrete parent-language gate: ban `w_A(R_AB)`/marker source slots or pay their coefficients.

## Evaluator Results

- `CASE4007_0_all_clauses_signed`: `CONDITIONAL_JR_ZERO`, J_R=`J_R_ZERO_IF_PARENT_SIGNED`, lambda=`LAMBDA_R_ZERO_IF_4006_BOUNDARY_GATE_CLOSED`, next=`promote only after parent action adopts the clauses in one branch`
- `CASE4007_1_prefactor_open`: `PREVARIATION_WEIGHT_OPEN`, J_R=`J_R_PREFACTOR_COUNTERTERM_LIVE`, lambda=`LAMBDA_R_NOT_ZERO`, next=`prove source-label-forgetting/no-Hom grammar or bound w_R_source`
- `CASE4007_2_marker_constants_open`: `CONSTANT_MARKER_OPEN`, J_R=`J_R_THETA_COUNTERTERM_LIVE`, lambda=`LAMBDA_R_NOT_ZERO`, next=`prove constant-sector universality or fill b_theta_R`
- `CASE4007_3_readout_open`: `READOUT_REGEN_OPEN`, J_R=`J_R_READOUT_COMPONENT_LIVE`, lambda=`LAMBDA_R_NOT_ZERO`, next=`prove variation-before-readout or fill readout_regen_R`
- `CASE4007_4_boundary_open`: `BOUNDARY_ONLY_OPEN`, J_R=`J_R_ZERO_BULK_ONLY`, lambda=`LAMBDA_R_BLOCKED_BY_BOUNDARY`, next=`separate boundary nohair/B_R pass`
- `CASE4007_5_numeric_bound_pack`: `FINITE_BOUND_PACK_NONCLAIM`, J_R=`J_R_RETAINED_WITH_NUMERIC_TARGETS`, lambda=`LAMBDA_R_FINITE_NONCLAIM`, next=`fill component coefficients and arena projections`
- `CASE4007_6_missing_everything`: `MISSING_PARENT_DESCENT`, J_R=`J_R_NOT_ZEROED`, lambda=`LAMBDA_R_NOT_ZERO`, next=`write the parent matter constructor rather than re-auditing symptoms`

## Next Target

- `4008-Y5-R2FR-source-label-forgetting-parent-functor-or-JR-coefficient-pack.md`
- `scripts/Y5_R2FR_4008_source_label_forgetting_parent_functor_or_JR_coefficient_pack.py`

## Source Count

- source needles found: `28/28`
