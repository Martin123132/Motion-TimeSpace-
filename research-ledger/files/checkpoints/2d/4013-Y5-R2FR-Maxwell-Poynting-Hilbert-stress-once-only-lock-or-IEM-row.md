# 4013 - Maxwell/Poynting Hilbert Stress Once-Only Lock Or I_EM Row

- Timestamp: `2026-07-01T20:52:44+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## Result

The Poynting route is now disciplined instead of mystical:

`J_H_total = J_matter + J_EM + J_binding + J_apparatus + dB_zero`.

Minimal Maxwell variation gives the EM Hilbert stress, and the Lorentz force exchange cancels only in the total matter+EM stress. Bound/local EM field energy belongs inside `J_H_total` once. Net radiative/background Poynting flux crossing the worldtube boundary is not deleted; it becomes `Phi_EM_rad`.

So the rule is: count EM stress once, not zero times and not twice.

## Branch Law

Stationary isolated branches may set the time-averaged boundary Poynting flux to zero using

`dU_EM/dt + int_boundary S_Poynting.n dA = -int_W J.E dV`.

Radiating or externally driven branches must retain the flux row. Internal Poynting circulation is allowed; only net boundary flux matters for source-mass drift.

## Finite EM Vector

`epsilon_EM_once_4013 <= |Delta_Hodge_EM|+|w_EM-1|+|C_XF2|+|C_JQ|+|Phi_EM_rad|/(G_ref M_H)+|C_EM_readout|+|Delta_J_total|+|epsilon_binding_once|+|C_Poynting_units|`.

This is still not an EM unification claim: it does not derive charge, alpha, Coulomb law or Maxwell emergence.

## Evaluator Results

- `CASE4013_0_full_once_only_signed`: EM=`CONDITIONAL_MAXWELL_POYNTING_ONCE_ONLY_LOCK`, source=`BOUND_EM_INSIDE_JH_TOTAL_AND_PHI_EM_ZERO_ON_STATIONARY_BRANCH`, claim=`SOURCE_ACCOUNTING_LOCK_NOT_EM_UNIFICATION_OR_FULL_LOCAL_GR`, next=`move to observed Hodge/Maxwell normalization owner or Newton/Gauss bridge`
- `CASE4013_1_Hodge_open`: EM=`EM_ONCE_ONLY_LOCK_BLOCKED`, source=`Delta_Hodge_EM`, claim=`NO_NEWTON_LOCAL_GR_MAXWELL_PROMOTION`, next=`retain Delta_Hodge_EM as finite nonclaim rows`
- `CASE4013_2_Maxwell_norm_open`: EM=`EM_ONCE_ONLY_LOCK_BLOCKED`, source=`w_EM+C_JQ`, claim=`NO_NEWTON_LOCAL_GR_MAXWELL_PROMOTION`, next=`retain w_EM+C_JQ as finite nonclaim rows`
- `CASE4013_3_current_owner_open`: EM=`EM_ONCE_ONLY_LOCK_BLOCKED`, source=`epsilon_internal_exchange`, claim=`NO_NEWTON_LOCAL_GR_MAXWELL_PROMOTION`, next=`retain epsilon_internal_exchange as finite nonclaim rows`
- `CASE4013_4_total_variation_open`: EM=`EM_ONCE_ONLY_LOCK_BLOCKED`, source=`Delta_J_total`, claim=`NO_NEWTON_LOCAL_GR_MAXWELL_PROMOTION`, next=`retain Delta_J_total as finite nonclaim rows`
- `CASE4013_5_Poynting_flux_open`: EM=`EM_ONCE_ONLY_LOCK_BLOCKED`, source=`Phi_EM_rad`, claim=`NO_NEWTON_LOCAL_GR_MAXWELL_PROMOTION`, next=`retain Phi_EM_rad as finite nonclaim rows`
- `CASE4013_6_hidden_F2_open`: EM=`EM_ONCE_ONLY_LOCK_BLOCKED`, source=`C_XF2`, claim=`NO_NEWTON_LOCAL_GR_MAXWELL_PROMOTION`, next=`retain C_XF2 as finite nonclaim rows`
- `CASE4013_7_readout_binding_units_open`: EM=`EM_ONCE_ONLY_LOCK_BLOCKED`, source=`C_EM_readout+epsilon_binding_once+C_Poynting_units`, claim=`NO_NEWTON_LOCAL_GR_MAXWELL_PROMOTION`, next=`retain C_EM_readout+epsilon_binding_once+C_Poynting_units as finite nonclaim rows`
- `CASE4013_8_numeric_pack`: EM=`FINITE_EM_ONCE_ONLY_PACK_NONCLAIM`, source=`DELTA_HODGE+wEM+CJQ+CXF2+PHI_EM+CEM_READOUT+BINDING+UNITS_VECTOR_REQUIRED`, claim=`NO_NEWTON_LOCAL_GR_MAXWELL_PROMOTION`, next=`fill source-backed EM/Hodge/normalization/Poynting/binding rows or prove them zero`

## Verdict

This is a real forward step: Poynting is no longer a loose intuition. It is either already inside total Hilbert stress or it is a boundary-flux residual. The next mathematical throat is observed Hodge/Maxwell normalization ownership.

## Next Target

- `4014-Y5-R2FR-observed-Hodge-Maxwell-normalization-owner-or-CXF2-row.md`
- `scripts/Y5_R2FR_4014_observed_Hodge_Maxwell_normalization_owner_or_CXF2_row.py`

## Source Count

- source needles found: `55/55`
