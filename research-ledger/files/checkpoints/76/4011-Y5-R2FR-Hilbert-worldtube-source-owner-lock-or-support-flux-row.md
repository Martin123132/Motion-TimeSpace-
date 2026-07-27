# 4011 - Hilbert Worldtube Source-Owner Lock Or Support-Flux Row

- Timestamp: `2026-07-01T20:38:52+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## Result

The clean theorem route is now explicit:

`W_H[tau] := closure(supp J_H[tau])`.

If `J_H[tau]`, `tau`, and `e_obs` descend through the same reduced branch, and the support is compact/regular, then vertical variation of the support vanishes. In that branch, `R_W=0`; if the shape coordinates are also q-basic and linked surfaces are parent-owned, then `C_shape=0` and `C_domain=0`.

That is a genuine derivation route, not a plateau axiom. But it is only a support/source-domain result; it does not yet prove that the same support carries the measured Newton/PPN mass charge.

## Coupling Lesson

This checkpoint separates two things that were getting glued together too early:

- support ownership: `W_source` must be the Hilbert-current support before readout;
- charge ownership: `Pi_M J_H` must equal the exterior `H_tau`/topological mass charge up to exact zero-flux terms.

In short: support ownership is not yet charge ownership.

4011 can conditionally solve the first. The second is now the next bottleneck.

## Finite Support-Flux Row

If the theorem branch is not adopted, the retained nonclaim vector is

`epsilon_support_4011 <= |R_W|+|C_shape|+|C_domain|+|C_ref|+|C_frame|+|epsilon_support_jump|+|epsilon_EM_once|+|epsilon_boundary_flux|`.

No cancellation between support, shape, reference, frame, EM/Poynting or boundary terms is credited.

## Evaluator Results

- `CASE4011_0_full_lock_signed`: support=`CONDITIONAL_HILBERT_WORLDTUBE_SUPPORT_LOCK`, worldtube=`R_W_C_shape_C_domain_ZERO_IF_SINGLE_BRANCH_SIGNED`, charge=`SAME_CHARGE_ASSUMED_IN_CASE_NOT_PROVEN_GLOBALLY`, next=`move to Pi_M/H_tau source-current commutator and charge equality proof`
- `CASE4011_1_support_selector_open`: support=`SUPPORT_LOCK_BLOCKED`, worldtube=`R_W`, charge=`CHARGE_GLUE_NOT_TESTED_BY_THIS_CASE`, next=`retain R_W as finite nonclaim rows`
- `CASE4011_2_domain_mask_open`: support=`SUPPORT_LOCK_BLOCKED`, worldtube=`C_domain`, charge=`CHARGE_GLUE_NOT_TESTED_BY_THIS_CASE`, next=`retain C_domain as finite nonclaim rows`
- `CASE4011_3_shape_open`: support=`SUPPORT_LOCK_BLOCKED`, worldtube=`C_shape`, charge=`CHARGE_GLUE_NOT_TESTED_BY_THIS_CASE`, next=`retain C_shape as finite nonclaim rows`
- `CASE4011_4_same_charge_open`: support=`SUPPORT_LOCK_CONDITIONAL_BUT_CHARGE_OPEN`, worldtube=`SUPPORT_COMPONENTS_CONDITIONALLY_ZERO`, charge=`epsilon_same_charge`, next=`retain epsilon_same_charge as finite nonclaim rows`
- `CASE4011_5_EM_once_open`: support=`SUPPORT_LOCK_BLOCKED`, worldtube=`epsilon_EM_once`, charge=`CHARGE_GLUE_NOT_TESTED_BY_THIS_CASE`, next=`retain epsilon_EM_once as finite nonclaim rows`
- `CASE4011_6_support_jump_open`: support=`SUPPORT_LOCK_BLOCKED`, worldtube=`epsilon_support_jump`, charge=`CHARGE_GLUE_NOT_TESTED_BY_THIS_CASE`, next=`retain epsilon_support_jump as finite nonclaim rows`
- `CASE4011_7_boundary_flux_open`: support=`SUPPORT_LOCK_BLOCKED`, worldtube=`epsilon_boundary_flux`, charge=`CHARGE_GLUE_NOT_TESTED_BY_THIS_CASE`, next=`retain epsilon_boundary_flux as finite nonclaim rows`
- `CASE4011_8_numeric_pack`: support=`FINITE_SUPPORT_FLUX_PACK_NONCLAIM`, worldtube=`EPSILON_SUPPORT_4011_VECTOR_REQUIRED`, charge=`NO_LOCAL_GR_PROMOTION`, next=`fill numeric/source-backed support, shape, domain, frame, EM-once and boundary-flux rows`

## Verdict

This moves the project forward by turning the worldtube problem into a precise theorem-plus-vector fork. The worldtube selector can be made non-arbitrary, but the theory still has to prove the coupling/charge equality.

## Next Target

- `4012-Y5-R2FR-PiM-Htau-source-current-commutator-lock-or-CM-Ccurl-row.md`
- `scripts/Y5_R2FR_4012_PiM_Htau_source_current_commutator_lock_or_CM_Ccurl_row.py`

## Source Count

- source needles found: `39/39`
