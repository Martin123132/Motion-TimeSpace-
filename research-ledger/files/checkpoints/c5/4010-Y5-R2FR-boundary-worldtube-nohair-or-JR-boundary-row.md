# 4010 - Boundary/Worldtube Nohair Or J_R Boundary Row

- Timestamp: `2026-07-01T20:29:10+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## Result

The boundary/worldtube obstruction is now decomposed instead of waved away:

`J_R_boundary := Pi_R^n + delta_R B_R + delta_R W_source + delta_R Pi_loc + nonHilbert_boundary_tail`.

The zero route is exact but conditional. `J_R_boundary=0` requires no derivative boundary momentum, proper/scalar/topological boundary action, parent-owned Hilbert worldtube support, fixed local projection, and zero-flux non-Hilbert improvements.

## Boundary Lemma

The scalar stationary boundary lemma is real: if the boundary stress is a pure tangential trace, then `n_mu P_loc_nu tau^{mu nu}=0`, so the preferred-momentum/alpha3 boundary channel vanishes.

But the corpus does not yet parent-own those premises, and the numeric product `W_boundary_alpha3 epsilon_boundary_flux` is still missing.

## Finite Row

If the nohair theorem fails, the retained row is

`|J_R_boundary| <= |Pi_R^n| + |delta_R B_R| + |delta_R W_source| + |[D_R,Pi_loc]B| + |nonHilbert_boundary_tail|`.

No cancellation between components is credited.

## Evaluator Results

- `CASE4010_0_full_gate_signed`: boundary=`CONDITIONAL_BOUNDARY_WORLDTUBE_ZERO`, J_R=`J_R_BOUNDARY_ZERO_IF_SINGLE_BRANCH_SIGNED`, next=`assemble with 4006/4008/4009 branch and move to source-current normalization`
- `CASE4010_1_boundary_action_open`: boundary=`BOUNDARY_ACTION_OPEN`, J_R=`DELTA_R_B_R_LIVE`, next=`derive proper/scalar/topological boundary owner or fill B_R`
- `CASE4010_2_worldtube_open`: boundary=`WORLDTUBE_SUPPORT_OPEN`, J_R=`DELTA_R_W_SOURCE_LIVE`, next=`derive Hilbert worldtube source owner lock`
- `CASE4010_3_projection_open`: boundary=`PROJECTION_BOUNDARY_OPEN`, J_R=`PILOC_COMMUTATOR_TAIL_LIVE`, next=`prove projector/source support commutation or retain C_domain`
- `CASE4010_4_nonhilbert_open`: boundary=`NONHILBERT_BOUNDARY_OPEN`, J_R=`NONHILBERT_BOUNDARY_TAIL_LIVE`, next=`prove exact improvement zero-flux or retain nonHilbert row`
- `CASE4010_5_derivative_boundary_open`: boundary=`DERIVATIVE_BOUNDARY_MOMENTUM_OPEN`, J_R=`PI_R_N_LIVE`, next=`adopt no-derivative grammar or fill Pi_R^n`
- `CASE4010_6_numeric_pack`: boundary=`FINITE_BOUNDARY_PACK_NONCLAIM`, J_R=`J_R_BOUNDARY_COMPONENT_ENVELOPE`, next=`fill numeric source paths, units and arena projections`

## Verdict

This is a useful narrowing: the boundary problem is no longer a fog bank. It is a finite list of gates, and the hardest one is now the Hilbert worldtube source-owner lock.

## Next Target

- `4011-Y5-R2FR-Hilbert-worldtube-source-owner-lock-or-support-flux-row.md`
- `scripts/Y5_R2FR_4011_Hilbert_worldtube_source_owner_lock_or_support_flux_row.py`

## Source Count

- source needles found: `36/36`
