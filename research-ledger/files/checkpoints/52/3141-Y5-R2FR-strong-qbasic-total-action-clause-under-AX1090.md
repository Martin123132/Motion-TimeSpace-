# 3141 - Strong q-Basic Total Action Clause under AX1090

Private checkpoint. This follows 3140 by attacking the remaining broad parent-action clause:

```text
L_parent = q^*Lbar(Q_obs, Rep(Q_obs), sources) + dB.
```

## Result

3141 reduces the broad problem to a sector gluing theorem.

If every sector of the local parent action is strongly q-basic:

```text
L_s(Phi) = q^* Lbar_s(Q_obs, Rep(Q_obs), J_Q) + dB_s,
```

then the total action is strongly q-basic:

```text
sum_s L_s
= q^*(sum_s Lbar_s) + d(sum_s B_s).
```

So:

```text
L_parent = q^*Lbar_total + dB_total.
```

This is exact. It is just linearity of local n-forms and horizontal exterior derivative.

That means the 3140 theta-descent theorem now has a sector-by-sector construction route:

```text
sector q-basicness
=> total q-basicness
=> theta descent
=> kernel-null up to boundary silence.
```

## What Actually Closes

The useful theorem is:

```text
finite sums of q-basic local n-forms are q-basic.
```

This removes the fog from the phrase:

```text
strong q-basic total action.
```

It is not one magic action clause. It is a checklist of local-form sector signatures.

The total action must be assembled from:

| sector | required q-basic form |
|---|---|
| geometry/EH | `L_geom=q^*Lbar_EH(e_obs,omega_obs,Lambda,G_ref)+dB_geom` |
| projector/domain | `L_proj=q^*Lbar_proj([C]_PD,[J_rel],boundary_class)+dB_proj` |
| EM/Maxwell | `L_EM=q^*(-C_P/4 mu_obs <F_Q T_Q,F_Q T_Q>_P)+dB_EM` |
| ordinary matter | `L_matter=sum_A L_A(Psi_A,Obs_e(Q_obs),A_Q,theta_A)` over `Rep(Q_obs)` |
| source/current | `J_source=delta L_matter/delta e_obs`, then label-forgotten `F_src(T_total)` |
| boundary/no-tail | `B_total=sum_s B_s`, with `int_boundary Xi_v(delta)=0` |

If all six close, the local hidden representative direction becomes gauge/null for the total action route.

## What Still Does Not Close

The gluing theorem is exact, but sector ownership is not signed.

| sector | current status | live residual |
|---|---|---|
| geometry/EH | `conditional_not_parent_signed` | `c_g/b_g`, `A_EH(X)`, PPN residuals |
| projector/domain | `conditional_topological_route_not_total_action_signed` | projector stress, `Delta_W_support`, `q_nonH` |
| EM/Maxwell | `conditional_exact_balpha_zero_not_parent_signed` | `b_alpha`, EM stress/Poynting readout |
| ordinary matter | `conditional_matter_functor_not_parent_signed` | `b_clock`, `b_mass`, `b_alpha` |
| source/current | `conditional_source_functor_not_parent_signed` | `Delta_w_species`, `Delta_kappa_AB`, non-Hilbert current |
| boundary/no-tail | `conditional_boundary_exact_not_zero_charge` | boundary charge, source-support shift |

Therefore:

```text
local GR/Newton/PPN/EM is still not claimed.
```

But the missing work is now structured:

```text
derive or bound the non-q-basic slots sector by sector.
```

## Why EM Now Becomes the Best Tactical Fork

The broad action route is now clean, but too many sectors remain unsigned at once. The best next tactical target is the narrowest sector with the biggest payoff:

```text
EM/Maxwell q-basic sector.
```

Why?

Because if the EM sector closes:

```text
T_Q parent owner
+ fixed charge lattice
+ fixed gauge norm/level
+ no independent F_Q^2
+ same current owner
+ readout/radiative guard
=> b_alpha = 0.
```

That directly hits:

```text
alpha_EM,
Poynting-vector readout,
EM Hilbert stress,
source charge normalization,
WEP alpha branch,
R10 alpha branch.
```

It is also a more test-facing win than another broad local-GR pass.

## What Counts as an EM Sector Win

The EM sector q-basic form must not be merely:

```text
we choose Maxwell.
```

It must show:

```text
L_EM = q^*(-C_P/4 mu_obs <F_Q T_Q,F_Q T_Q>_P) + dB_EM
```

with no legal extra slot:

```text
lambda_A F_Q^2,
f_X(Xhat) F_Q^2,
radiative/readout regenerated F_Q^2.
```

And the same `T_Q` owner must normalize the current:

```text
J_Q = delta L_matter / delta A_Q.
```

If that works, the Poynting vector is not patched in:

```text
T_EM^{mu nu}
```

comes from the Hilbert variation of the owned Maxwell sector, and the observed energy flux is the usual stress-energy flux built from the q-owned EM field.

## Claim Gate

| gate | status |
|---|---|
| q-basic sector gluing theorem | `pass_exact_theorem` |
| all total-action sectors q-basic | `fail_for_claim` |
| EM/Maxwell/Poynting/`b_alpha` claim | `not_claim_ready` |
| calibrated source coupling/Newton claim | `not_claim_ready` |
| local GR/Newton/PPN total-action claim | `not_claim_ready` |

## Why This Matters

This is the first clean total-action architecture after the 3138-3140 chain:

```text
Q_obs construction
-> kernel-null identity
-> theta descent from q-basic action
-> total action as sector q-basic gluing.
```

That is a real spine.

It does not prove the theory. But it tells us how a proof would have to be built without smuggling:

```text
every sector either descends through Q_obs/Rep(Q_obs),
or it is a finite residual to derive, source, and test.
```

No hiding in “the action probably does it.”

## Runner Artifacts

| artifact | path |
|---|---|
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3141_INPUTS.csv` |
| gluing theorem | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3141_QBASIC_GLUING_THEOREM.csv` |
| total action contract | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3141_TOTAL_ACTION_CONTRACT.csv` |
| sector audit | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3141_SECTOR_QBASIC_AUDIT.csv` |
| obstruction fork ledger | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3141_OBSTRUCTION_TO_FORK_LEDGER.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3141_DECISION.csv` |
| gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3141_GATE.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3141_VALIDATION.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3141_strong_qbasic_total_action_clause.py` |

## Next Target

The selected next target is:

```text
3142:
EM/Poynting q-basic sector theorem:
parent T_Q/gauge norm + no independent F_Q^2 + Hilbert stress/current owner.
```

The success condition is not public claim language. It is:

```text
either derive the EM sector q-basic form,
or produce the exact finite EM residual row that must be bounded.
```

This is the best route because it pushes forward on charge, Poynting vector, Maxwell stress, `b_alpha`, and source coupling without trying to swallow the whole GR proof in one bite.
