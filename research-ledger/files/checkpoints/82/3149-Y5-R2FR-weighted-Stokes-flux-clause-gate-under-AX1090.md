# 3149 - Weighted-Stokes / Flux Clause Gate under AX1090

Private checkpoint. This follows 3148:

```text
Pi_local P_surface = 0
```

would rescue the active source-GM pressure row, but only if the boundary/projector proof is real.

3149 attacks the exact clause.

## Result

The surface/profile term must be decomposed before projection:

```text
P_surface = d_S Lambda + h_surface + r_surface.
```

Weighted Stokes gives:

```text
Int_S W d_S Lambda
= Int_partialS W Lambda
  - Int_S d_S(W) wedge Lambda.
```

So ordinary exactness is not enough.

The local projector kills the surface channel only if:

```text
partialS = 0 or corner terms are bounded,
h_surface = 0,
r_surface = 0,
d_S(W) = 0,
Poynting/static flux = 0 or separated,
reference/readout counterterms = 0.
```

Then:

```text
Pi_local P_surface = 0.
```

## Score Impact

Current active fallback:

```text
|DeltaK_C| + |DeltaK_surface|
= 4.382882115828398e-03,
```

above:

```text
3.979617773650001e-03.
```

If every weighted-Stokes/flux clause closes, the surface term is removed and the score becomes:

```text
|DeltaK_C| = 3.382521373501744e-03,
```

which is below threshold.

So the rescue path is exact, but it is clause-heavy.

## Flux Separation

Poynting flux is not forbidden. It just cannot be smuggled into static `GM`.

Allowed split:

```text
DeltaK_static = Hilbert stationary source term,
DeltaK_flux = Int_partialW S_EM . dA dt / M_H.
```

If the flux branch exists, it becomes a separate dynamic/radiative coefficient. It does not silently cancel a static source-mass coefficient.

This matters because EM/Poynting intuition can still be physically useful, but it must live in the right channel.

## Bound If Unsigned

If any clause is unsigned, the honest fallback is:

```text
|Q_surface|
<= C_corner
 + ||d_S W|| ||Lambda||
 + |<W,h_surface>|
 + |<W,r_surface>|
 + |Phi_Poynting|
 + |C_ref|
 + |C_readout|.
```

3149 stages each term as a nonclaim row:

| term | status |
|---|---|
| `C_corner` | missing zero theorem or numeric bound |
| `||d_S W|| ||Lambda||` | missing closed-weight theorem or derivative norm |
| `harmonic_surface_abs` | missing cohomology zero or bound |
| `residual_surface_abs` | missing residual zero or bound |
| `poynting_flux_abs` | missing stationary zero or dynamic flux bound |
| `reference_readout_abs` | missing reference/readout silence or bound |

## Gates

| gate | status |
|---|---|
| `P_surface=d_S Lambda` primitive | `fail_for_claim` |
| corner-free or corner-bounded | `fail_for_claim` |
| closed weight `d_S(W)=0` or derivative bound | `fail_for_claim` |
| harmonic/residual zero or bound | `fail_for_claim` |
| Poynting flux zero or separated dynamic branch | `fail_for_claim` |
| reference/readout silence | `fail_for_claim` |
| `Pi_local P_surface=0` | `not_claim_ready` |

## Runner Artifacts

| artifact | path |
|---|---|
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3149_INPUTS.csv` |
| theorem | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3149_WEIGHTED_STOKES_FLUX_THEOREM.csv` |
| gates | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3149_CLAUSE_GATES.csv` |
| bound schema | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3149_STOKES_FLUX_BOUND_SCHEMA.csv` |
| score impact | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3149_SCORE_IMPACT.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3149_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3149_VALIDATION.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3149_weighted_stokes_flux_clause_gate.py` |

## Decision

3149 proves the local clause shape:

```text
weighted Stokes + closed weight + no flux/re-entry
=> Pi_local P_surface = 0.
```

But it does not promote the zero theorem.

The active status remains:

```text
absolute no-cancellation pressure row retained.
```

Next target:

```text
3150:
derive d_S(W)=0 from parent/source boundary class,
or fill the first finite bound term:
||d_S W|| ||Lambda|| or poynting_flux_abs.
```

That is now the shortest honest route: close one clause, or put a number/bound on it.
