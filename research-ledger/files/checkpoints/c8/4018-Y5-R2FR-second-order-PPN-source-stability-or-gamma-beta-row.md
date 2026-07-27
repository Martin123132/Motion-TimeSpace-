# 4018 - Second-Order PPN Source Stability Or Gamma/Beta Row

- Timestamp: `2026-07-01T21:28:21+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## Result

This checkpoint makes the local-GR gate explicit: Newton/Gauss is first order; local GR needs the second-order PPN vector.

PPN frame:

`g_00=-1+2U/c^2-2 beta U^2/c^4+O(c^-6)`

`g_ij=delta_ij(1+2 gamma U/c^2)+O(c^-4)`.

The non-smuggled beta test is:

`beta_eff = B_source/A_source^2`

`delta_beta_source = B_source/A_source^2 - 1`.

So once `A_source` is fixed by the Newton/Gauss/Hilbert source bridge, the second-order coefficient must obey `B_source=A_source^2`. Otherwise beta fails even if the Newtonian limit looked fine.

## Conditional Local-GR Route

If the local reduced action is EH-only through `O(U^2)`, the 4017 `K_G` packet is same-branch, `Pi_M/H_tau` source equality holds, source prefactors are absent, and R11/q_loc/readout/boundary/projector tails vanish, then the GR PPN vector follows conditionally:

`gamma=1`, `beta=1`, `alpha1=alpha2=alpha3=xi=zeta_i=0`.

## Finite PPN Vector

`epsilon_PPN_2nd_4018 <= |delta_gamma_EH|+|delta_gamma_R11|+|delta_gamma_readout|+|delta_beta_source|+|delta_beta_R11|+|delta_beta_q_loc|+|delta_beta_boundary|+|delta_beta_readout|+|alpha1|+|alpha2|+|alpha3|+|xi|+sum_i|zeta_i|+|Gdot/G|`.

## Evaluator Results

- `CASE4018_0_full_EH_source_PPN_signed`: owner=`CONDITIONAL_LOCAL_GR_PPN_LOCK`, residual=`GAMMA_BETA_ALPHA_XI_ZETA_ZERO_IF_ALL_PARENT_GATES_SIGNED`, claim=`LOCAL_GR_CONDITIONAL_ONLY_NOT_PUBLIC_CLAIM`, next=`next adopt/check EH-only R11 no-extra operator branch against residual scorer`
- `CASE4018_1_gamma_only`: owner=`BETA_SOURCE_STABILITY_BLOCKED`, residual=`delta_beta_source+beta_minus_1`, claim=`NO_BETA_OR_LOCAL_GR_CLAIM`, next=`prove B_source=A_source^2 after source normalization or fill beta residuals`
- `CASE4018_2_beta_square_law_open`: owner=`BETA_SOURCE_STABILITY_BLOCKED`, residual=`delta_beta_source+beta_minus_1`, claim=`NO_BETA_OR_LOCAL_GR_CLAIM`, next=`prove B_source=A_source^2 after source normalization or fill beta residuals`
- `CASE4018_3_R11_operator_tail`: owner=`PPN_EH_ONLY_BLOCKED`, residual=`delta_gamma_R11+delta_beta_R11+delta_beta_q_loc`, claim=`NO_GAMMA_BETA_CLAIM`, next=`derive EH-only/no-extra-operator branch or retain R11/q_loc PPN residuals`
- `CASE4018_4_source_prefactor_open`: owner=`SOURCE_CURRENT_ORIGIN_BLOCKED`, residual=`epsilon_parent_JH_origin+delta_beta_source`, claim=`NO_SOURCE_NORMALIZED_PPN_CLAIM`, next=`close Hilbert source-current origin/no-source-prefactor gate`
- `CASE4018_5_preferred_frame_open`: owner=`FULL_PPN_VECTOR_BLOCKED`, residual=`alpha_i+xi+zeta_i`, claim=`NO_LOCAL_GR_PROMOTION`, next=`close preferred-frame/conservation rows after gamma/beta`
- `CASE4018_6_Newton_overclaim`: owner=`NEWTON_TO_LOCAL_GR_OVERCLAIM_REJECTED`, residual=`gamma_beta_full_PPN_vector_required`, claim=`NO_LOCAL_GR_PROMOTION`, next=`keep Newton/Gauss as first-order only until full PPN vector closes`
- `CASE4018_7_cancellation_attempt`: owner=`PPN_CANCELLATION_REJECTED`, residual=`Delta_PPN_abs_no_cancellation`, claim=`NO_PPN_PASS`, next=`absolute-sum each component; no opposite-sign cancellation`
- `CASE4018_8_numeric_runner_pack`: owner=`PPN_EH_ONLY_BLOCKED`, residual=`delta_gamma_R11+delta_beta_R11+delta_beta_q_loc`, claim=`NO_GAMMA_BETA_CLAIM`, next=`derive EH-only/no-extra-operator branch or retain R11/q_loc PPN residuals`

## Verdict

This is a necessary tightening. We now have a real conditional local-GR route, but also the exact firewall: gamma-only or Newton-only is not enough, and beta cannot be repaired by fitted GM. Current status remains nonclaim until the EH-only/R11/no-extra-operator branch is adopted or all residuals are scored.

## Next Target

- `4019-Y5-R2FR-EH-only-R11-no-extra-operator-adoption-or-PPN-residual-scorer.md`
- `scripts/Y5_R2FR_4019_EH_only_R11_no_extra_operator_adoption_or_PPN_residual_scorer.py`

## Source Count

- source needles found: `32/32`
