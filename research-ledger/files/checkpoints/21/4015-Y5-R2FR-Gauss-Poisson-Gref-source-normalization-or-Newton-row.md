# 4015 - Gauss/Poisson/G_ref Source Normalization Or Newton Row

- Timestamp: `2026-07-01T21:09:24+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## Result

This checkpoint turns the Newton side into an actual bridge rather than another missing-coupling fog bank.

Definitions are now fixed before orbital readout:

`kappa_ref := 8*pi*G_ref/c^4`

`g_00=-(1+2*Phi/c^2)+O(c^-4)`

`T_00^H=rho_H*c^2+O(v^2/c^2)`

`M_H_ref=int rho_H dV_obs`

If the reduced EH 00 operator, same-frame nonrelativistic source limit, 4012 charge lock, Gauss boundary closure, and slow-geodesic matter readout are all signed, then

`nabla^2 Phi=4*pi*G_ref*rho_H`

`int_S grad(Phi).dS=4*pi*G_ref*M_H_ref`

`Phi=-G_ref*M_H_ref/r` and `v^2*r=G_ref*M_H_ref` in the clean monopole slow-orbit branch.

That is the right reduction target: `GM_orb` tests `G_ref*M_H_ref`; it does not define either side.

## Newton Constant Policy

This does not claim the numerical value of Newton's constant is derived. GR itself fixes how one universal `G` couples geometry to stress; it does not derive the number from Newtonian mechanics. The MTS target is therefore: one parent-owned, source-blind `G_ref` used by the EH operator, Hamiltonian charge, Poisson law, Gauss law, and orbital readout. A deeper derivation of `G_ref` is a later superselection/normalization target, not something to smuggle in here.

## Finite Bridge Vector

`epsilon_Newton_bridge_4015 <= |Delta_EH00|+|Delta_NR_source|+|C_PiM_H|+|C_Gref_kappa|+|C_frame|+|C_units|+|C_Gauss_boundary|+|C_multipole|+|C_orbital_readout|+|mu_extra|/(G_ref*M_H_ref)+|epsilon_EM_once|+|epsilon_G_run|+|epsilon_range|+|epsilon_PPN_2nd|`.

## Evaluator Results

- `CASE4015_0_full_Newton_bridge_signed`: owner=`CONDITIONAL_NEWTON_GAUSS_POISSON_LOCK`, residual=`DELTA_EH00_CPiMH_GAUSS_ORBITAL_ZERO_IF_PARENT_SIGNED`, claim=`NEWTON_LIMIT_CONDITIONAL_ONLY_LOCAL_GR_NOT_CLAIMED`, next=`move to G_ref superselection and then PPN second-order source stability`
- `CASE4015_1_EH_operator_open`: owner=`NEWTON_BRIDGE_BLOCKED`, residual=`Delta_EH00+Delta_NR_source`, claim=`NO_POISSON_COEFFICIENT_CLAIM`, next=`prove reduced EH 00 operator or keep operator residual rows`
- `CASE4015_2_charge_lock_open`: owner=`NEWTON_BRIDGE_BLOCKED`, residual=`C_PiM_H`, claim=`NO_SOURCE_MASS_CLAIM`, next=`close Pi_M/H_tau/Hilbert charge equality before using Newton mass`
- `CASE4015_3_Gref_kappa_open`: owner=`GREF_CALIBRATION_BLOCKED`, residual=`C_Gref_kappa+epsilon_G_run+epsilon_range`, claim=`NO_CONSTANT_UNIVERSAL_G_CLAIM`, next=`derive global coupling superselection or source Gdot/range/source residual rows`
- `CASE4015_4_Gauss_boundary_open`: owner=`GAUSS_SURFACE_BLOCKED`, residual=`C_Gauss_boundary+C_multipole+mu_extra_over_GM`, claim=`NO_INVERSE_SQUARE_SURFACE_CLAIM`, next=`close boundary/worldtube/nohair and mu_extra rows`
- `CASE4015_5_geodesic_readout_open`: owner=`ORBITAL_READOUT_BLOCKED`, residual=`C_orbital_readout+fifth_force_readout`, claim=`NO_ORBITAL_GM_CLAIM`, next=`derive slow-particle same-frame geodesic limit`
- `CASE4015_6_EM_once_open`: owner=`SOURCE_STRESS_BOOKKEEPING_BLOCKED`, residual=`epsilon_EM_once`, claim=`NO_ACTIVE_SOURCE_CLAIM`, next=`close Maxwell/Poynting once-only owner`
- `CASE4015_7_PPN_overclaim`: owner=`NEWTON_ONLY_NOT_LOCAL_GR`, residual=`epsilon_PPN_2nd`, claim=`NO_LOCAL_GR_PROMOTION`, next=`run second-order PPN source-stability after first-order coupling is locked`
- `CASE4015_8_orbital_laundering_attempt`: owner=`ORBITAL_GM_LAUNDERING_REJECTED`, residual=`C_PiM_H_UNOWNED_AND_IMPORT_FORBIDDEN`, claim=`NO_NEWTON_SOURCE_CLAIM`, next=`derive M_H_ref from parent charge or keep orbital GM as output-only comparison`
- `CASE4015_9_numeric_nonclaim_pack`: owner=`NEWTON_BRIDGE_BLOCKED`, residual=`Delta_EH00+Delta_NR_source`, claim=`NO_POISSON_COEFFICIENT_CLAIM`, next=`prove reduced EH 00 operator or keep operator residual rows`

## Verdict

This is a real forward step. The Newton limit is now expressed as a conditional derivation chain with an anti-circularity guard. The grim bit is still honest: without G_ref superselection and second-order PPN stability, this is not local GR yet. The good bit is that the target is now narrow enough to attack.

## Next Target

- `4016-Y5-R2FR-Gref-superselection-universal-calibration-or-Gdot-range-row.md`
- `scripts/Y5_R2FR_4016_Gref_superselection_universal_calibration_or_Gdot_range_row.py`

## Source Count

- source needles found: `43/43`
