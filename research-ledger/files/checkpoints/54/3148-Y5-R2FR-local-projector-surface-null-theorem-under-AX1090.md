# 3148 - Local Projector Surface-Null Theorem under AX1090

Private checkpoint. This follows the 3147 fork:

```text
try to prove Pi_local P_surface = 0
or K_source = K_cal
from Hilbert/worldtube geometry.
```

3148 derives the exact theorem shape and checks what the score becomes if the theorem closes.

## Result

The local source-GM projection from 3145 is:

```text
Pi_local[P]
:= (1/M_H,S) Int_W xi_nu P^{mu nu} dSigma_mu
```

with source/calibration subtraction understood.

For the surface/profile channel, a clean silence theorem exists:

```text
P_surface = d_S Lambda,
partial W is empty or common-calibrated,
xi.Lambda|partial W = 0
=> Pi_local P_surface = 0.
```

Equivalent common-worldtube form:

```text
K_surface[S;W] - K_surface[cal;W] = 0.
```

So the surface/profile channel can be killed by geometry, not by a numerical fiddle, if the boundary/worldtube hypotheses are parent-signed.

## Score Consequence

The active absolute fallback remains:

```text
|DeltaK_C| + |DeltaK_surface|
= 4.382882115828398e-03,
```

which is above:

```text
3.979617773650001e-03.
```

But if the local projector annihilates the surface/profile channel, the score becomes Coulomb-only:

```text
|DeltaK_C|
= 3.382521373501744e-03.
```

At the current `delta_J` smoke envelope:

```text
eta_C = 2.379891834968431e-15,
eta_bound = 2.8e-15.
```

So the theorem would pass this pressure gate.

That is a real advance: the local branch does not need broad tuning. It needs a very specific surface-null/common-worldtube theorem.

## Why It Is Not Claimed

The theorem is exact but not signed. These gates remain live:

| gate | status | blocker |
|---|---|---|
| surface exactness | `fail_for_claim` | parent does not yet prove `P_surface=d_S Lambda` with no harmonic/nonexact/corner residue |
| same worldtube | `fail_for_claim` | source and calibration worldtube functional not locked |
| Poynting/static flux | `fail_for_claim` | unresolved flux cannot be swallowed by static ADM mass |
| reference/readout re-entry | `fail_for_claim` | `rho_reference_counterterm` and `rho_projector_readout` remain in allocator |
| `J_direct` / `J_spurion` | `fail_for_claim` | 3134 still carries finite leakage heads |

Therefore:

```text
Pi_local P_surface = 0
```

is a theorem target, not a result.

## Proof Contract

To promote the theorem, 3149 or later must sign:

1. `P_surface=d_S Lambda` plus zero harmonic/nonexact/corner terms;
2. weighted Stokes closedness on the compact/common-calibrated worldtube;
3. stationary/no unresolved Poynting flux, or a separated dynamic flux channel;
4. no reference/readout counterterm re-entry;
5. no `J_direct` or `J_spurion` source re-entry.

If these fail, the fallback is still:

```text
rho_profile <= 0.04926870396835468
```

using a real profile/worldtube row, not the two-layer smoke profile.

## Runner Artifacts

| artifact | path |
|---|---|
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3148_INPUTS.csv` |
| theorem | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3148_LOCAL_PROJECTOR_SURFACE_NULL_THEOREM.csv` |
| gates | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3148_GATE_STATUS.csv` |
| scorecard | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3148_SURFACE_NULL_SCORECARD.csv` |
| proof contract | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3148_PROOF_CONTRACT.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3148_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3148_VALIDATION.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3148_local_projector_surface_null_theorem.py` |

## Decision

3148 establishes:

```text
surface-null theorem shape is strong enough to rescue the pressure row,
but not yet signed.
```

The active branch remains:

```text
absolute no-cancellation pressure retained.
```

Next target:

```text
3149:
attack one proof clause directly,
preferably Poynting/static-flux separation or weighted-Stokes exactness.
```

If that fails, switch to the data-facing route:

```text
import/source a real PREM/shell/worldtube profile
and test rho_profile <= 0.04926870396835468.
```
