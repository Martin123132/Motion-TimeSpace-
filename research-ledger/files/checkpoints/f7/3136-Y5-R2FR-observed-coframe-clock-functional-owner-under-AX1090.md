# 3136 - Observed-Coframe Clock Functional Owner under AX1090

Private checkpoint. This follows 3135 by trying to derive the clock readout functional instead of merely declaring that it is missing.

## Result

3136 proves the clean conditional clock theorem:

```text
ordinary clock matter descends to the observed coframe
=> observed clocks measure observed metric proper time.
```

In formula form:

```text
S_pp = -m_A c^2 integral d tau_clk
d tau_clk = sqrt(-g_obs_mu_nu dx^mu dx^nu)/c
```

or equivalently in the eikonal/WKB clock phase limit:

```text
g_obs^{mu nu} partial_mu S partial_nu S + m_A(theta)^2 c^2 = 0.
```

This means the time/flow sign issue is sharper now:

```text
an internal flow variable can run with a strange sign
without being physical clock time,
provided it does not leak into e_obs or material constants.
```

## What Actually Closes

The following conditional derivation is valid:

| step | result |
|---|---|
| `e_obs=Obs_e(q(Phi))`, `Dq(v)=0` | representative/internal variations do not change the observed coframe |
| `S_matter=S_matter[e_obs,psi_A,theta_A]` | clock matter sees the observed coframe |
| WKB/localized matter limit | phase obeys the observed Hamilton-Jacobi equation |
| point-particle/eikonal limit | clock elapsed time is observed proper time |
| redshift/frequency comparison | measured frequency ratios are phase-rate ratios in `tau_clk` |

So the clock functional is not arbitrary. If the parent action signs the observed-coframe matter functor, `R_clock` is forced.

## What Still Does Not Close

This does not yet prove local GR, Newton, or clocks, because the parent has not signed:

```text
q: Phi -> Q_obs,
e_obs = Obs_e(q(Phi)),
ordinary matter functor over e_obs,
constant/mass/charge superselection,
absence of nonminimal clock-flow couplings,
same tau for clock/source/charge/orbit/boundary.
```

The current verdict remains:

```text
R_clock theorem = formal_pass_conditional
parent ownership = fail_for_claim
clock/SR/GR claim = not_claim_ready
```

## Residuals If The Theorem Fails

If the parent cannot sign the matter-clock route, the following residuals must be retained:

| residual | meaning |
|---|---|
| `b_clock` | internal/representative derivative of material clock transition |
| `b_mass` | derivative of mass standard |
| `b_alpha` | derivative of `alpha_EM` or EM transition coupling |
| `delta_e_clock` | direct leakage into observed coframe clock functional |
| `epsilon_nonminimal_clock` | nonminimal curvature/flow clock coupling |
| `epsilon_tau_role` | mismatch between clock/source/charge/orbit/boundary time |

No cancellation between these is allowed unless a parent theorem or sourced bound says so.

## Why This Matters

3135 only said:

```text
internal flow sign is not automatically observable.
```

3136 adds:

```text
the observable clock functional is forced by ordinary observed-coframe matter,
if the parent descent clauses are signed.
```

That is a real step toward GR reduction: SR time dilation, GR redshift, null-photon no-proper-time, and Newtonian slow-motion time all become readouts of the same `g_obs` object rather than separate patches.

## Runner Artifacts

| artifact | path |
|---|---|
| input ledger | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3136_CLOCK_OWNER_INPUTS.csv` |
| theorem rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3136_OBSERVED_CLOCK_FUNCTIONAL_THEOREM.csv` |
| derivation chain | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3136_CLOCK_MATTER_DERIVATION_CHAIN.csv` |
| residuals | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3136_CLOCK_OWNER_RESIDUALS.csv` |
| gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3136_GATE.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3136_VALIDATION.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3136_observed_clock_functional_owner.py` |

## Next Target

The next best route is no longer vague:

```text
3137:
try to parent-sign quotient ownership of material constants/clock standards,
or construct the explicit q -> Obs_e map tightly enough that R_clock is owned.
```

If that fails, stop trying to make clocks disappear and fill the first finite residual row, most likely:

```text
b_clock
```

or:

```text
b_alpha
```

