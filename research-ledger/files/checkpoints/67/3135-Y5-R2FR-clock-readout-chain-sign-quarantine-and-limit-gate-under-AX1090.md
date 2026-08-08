# 3135 - Clock Readout Chain, Sign Quarantine, and Limit Gate under AX1090

Private checkpoint. This is a response to the time/flow fork: do not reject a branch merely because an internal time-like variable seems to run with the "wrong" sign relative to GR. First derive the observable clock readout.

## Result

3135 converts the intuition into a precise gate:

```text
internal flow variable -> quotient/readout map -> clock observable -> tested limit
```

The useful theorem is conditional but real:

```text
tau_clk[path] = R_clock(q(Phi), path, clock_species)
```

If the internal flow variable only appears through `q(Phi)` and the observable clock functional `R_clock`, then a sign inversion in the internal flow variable is not by itself a physical contradiction. The branch fails only if the wrong sign survives into the measured observable:

```text
d tau_clk / d t_obs,
Delta nu / nu,
Gdot/G,
PPN gamma,
EM/Poynting stress flux.
```

## What Actually Closes

The following algebraic/readout facts are accepted as conditional lemmas:

| item | conditional result |
|---|---|
| variable separation | `tau_flow` is not automatically `tau_clk` |
| SR clock limit | if `R_clock` is observed metric proper time, `d tau_clk/dt_obs = sqrt(1-v_obs^2/c^2)` |
| GR redshift | if `g00_obs = -(1+2 Phi/c^2)`, then `Delta nu/nu = (Phi_A-Phi_B)/c^2` |
| null photons | `d tau_clk=0` follows from `g_obs(k,k)=0`, not necessarily from literal internal time stoppage |
| direct flow leakage | any direct flow effect becomes a bounded residual, not a hidden pass |

That is genuine progress: the "time runs opposite" worry is now a readout-chain problem, not a vibes problem.

## What Does Not Close

No local-GR, Newton, Maxwell, or clock claim is promoted.

The missing parent-owned pieces are still:

```text
q object,
observed coframe/metric readout,
R_clock ownership,
q-basic matter action,
same tau for clock/source/charge/orbit/boundary,
Maxwell/EM stress inheritance,
no direct internal-flow coupling to constants or source weights.
```

So the safe status is:

```text
sign_quarantine = conditional_pass
local_GR_claim = false
Newton_claim = false
Maxwell_claim = false
clock_claim = false
```

## Loaded Empirical Bounds

3135 loads already-existing source-backed local bounds into the residual vector:

| residual | loaded bound/input | meaning |
|---|---:|---|
| `epsilon_clock_alpha_product` | `2.1e-18 yr^-1` | strongest loaded alpha-sensitive clock product row |
| `epsilon_GR_redshift` | `2.48e-05` | Galileo eccentric-satellite redshift/LPI row |
| `epsilon_Gdot_source_time` | `9.6e-15 yr^-1` | LLR `Gdot/G` row |
| `epsilon_PPN_gamma_readout` | `2.3e-05` | Cassini gamma row |
| `epsilon_tau_role` | `MISSING_SAME_TAU_NORMALIZATION_THEOREM` | tau roles still not unified |
| `epsilon_clock_readout_direct` | `MISSING_C_Obs_e_AND_C_shadow_abs_ZERO_OR_BOUND` | direct readout leakage still open |
| `epsilon_EM_flow` | `MISSING_EM_PARENT_MAXWELL_INHERITANCE_OR_BOUND` | Poynting/background-flow channel now explicit |

## Poynting Vector Channel

Your Poynting-vector instinct lands in a useful place:

```text
S_EM = -1/4 integral sqrt(-g_obs) F_{mu nu}F^{mu nu}
```

If EM is inherited through the observed coframe, then the Poynting vector is part of the observed Maxwell stress tensor. If a background-flow channel carries extra energy flux not represented by that stress tensor, it is not free; it becomes:

```text
epsilon_EM_flow.
```

That is the right way to test the idea without cheating.

## Claim Gate

| gate | result |
|---|---|
| internal-flow sign quarantine | `formal_pass_conditional` |
| SR/GR limits after readout | `conditional_not_parent_signed` |
| real clock bounds loaded | `source_bounds_loaded_no_MTS_product` |
| same tau for charge/clock/source/orbit/boundary | `fail_for_claim` |
| EM/Poynting readout channel | `new_residual_channel_defined_no_claim` |
| total local-GR/Newton/Maxwell claim | `not_claim_ready` |

## Runner Artifacts

| artifact | path |
|---|---|
| input ledger | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3135_CLOCK_READOUT_INPUTS.csv` |
| readout lemma | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3135_READOUT_CHAIN_LEMMA.csv` |
| SR/GR limit expansion | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3135_SR_GR_LIMIT_EXPANSION.csv` |
| residual vector | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3135_TIME_SIGN_RESIDUAL_VECTOR.csv` |
| gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3135_GATE.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3135_VALIDATION.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3135_clock_readout_chain_limit_gate.py` |

## Next Target

3136 should attack one of two concrete doors:

```text
preferred:
derive the observed-coframe clock functional R_clock from the parent q/readout map.
```

or:

```text
if EM is the better path:
derive Maxwell/Poynting stress inheritance through g_obs, or keep epsilon_EM_flow as a finite bound row.
```

The preferred route is the clock functional because it directly controls SR, redshift, Newtonian time, and the tau-role mismatch.

