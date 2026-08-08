# 3131 - Boundary Exactness/Common-Worldtube Proof or rho_surf Retention under AX1090

Private checkpoint. This follows 3130 and tries the clean route first:

```text
surface/binding term is boundary-exact and same-worldtube calibrated
=> rho_surf = 0.
```

## Result

The zero route is now written as a theorem target, but it is not promoted.

The required clauses are:

```text
1. B_surf is exact or cohomologically silent on the compact boundary partition.
2. Source and calibration use the same fixed Hilbert-stress worldtube functional.
3. Reference zero, boundary orientation, and normalization are shared before readout.
4. Poynting/radiative flux is zero, averaged, or explicitly separated from static ADM mass.
5. Hidden/domain/non-EH channels carry no independent mass-channel exchange.
6. Profile/readout/source labels do not re-enter after common-mode calibration.
```

Current corpus support is useful, but conditional. The proof is blocked by unsigned boundary exactness, unsigned same-worldtube calibration, live source-label/species-slot residuals, Poynting/radiative closure guards, hidden exchange obstructions, and missing profile/readout weighting.

## Conditional Theorem

If all six clauses are parent-signed, then:

```text
C_surf[B] = integral_{partial W_B} B_surf
```

and:

```text
DeltaC_Scal,surf = C_surf[S] - C_surf[cal] = 0.
```

Equivalently:

```text
rho_surf = 0.
```

This would be the cleanest route because it does not ask a finite profile factor to hide the binding surface term.

## Why It Is Not Claimed

The best older ingredients are:

```text
Hilbert EM measure,
Poynting flux guard,
worldtube source measure clauses,
parent worldtube glue clauses,
source-measure flux clauses,
topological-Hilbert equality obstructions,
source descent/common-mode guard.
```

But they do not yet prove the exact boundary/common-worldtube cancellation. They say what must be true.

The sharp obstruction remains:

```text
boundary exactness/common-worldtube calibration is not parent-signed.
```

and:

```text
NoSourceOnlySpeciesSlot/source-label forgetting remains missing.
```

So 3131 keeps:

```text
zero_promoted = false
claim_allowed = false
valid_for_claim = false
```

## Retained Finite Bound

Because the zero route is not signed, the finite 3130 cap remains the live bound:

```text
|rho_surf| <= 0.3283734585378189.
```

The required suppression is:

```text
suppression >= 0.6716265414621811.
```

This is not impossibly tiny, but it has to be derived from profile/worldtube/calibration geometry or scored as a real residual.

## Method Note

Martin's fork heuristic is now carried as a private discipline rule:

```text
Do not reject a branch only because its internal time/flow language looks opposite to GR.
First map the observed clock/metric limit and decide whether the difference is a real observable residual,
or just a different variable-language that reduces to GR in the calibrated local limit.
```

This is not evidence and it cannot promote a claim. It is a guard against killing a potentially useful derivation route too early.

## Runner Artifacts

| artifact | path |
|---|---|
| input rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3131_BOUNDARY_EXACTNESS_INPUTS.csv` |
| output rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3131_BOUNDARY_EXACTNESS_OUTPUT.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3131_VALIDATION.csv` |
| gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3131_BOUNDARY_EXACTNESS_GATE.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3131_boundary_exactness_common_worldtube.py` |

## Next Target

3132 should try the parent-action clause:

```text
derive B_surf = d_boundary Lambda with zero compact boundary integral,
and prove the source/calibration worldtube functional is the same object before readout.
```

If that cannot be signed, switch to an executable profile/worldtube allocator:

```text
rho_surf = P_profile[source worldtube, orbit, shell, calibration] acting on Q_surface_binding_Earth
```

and require:

```text
rho_surf <= 0.3283734585378189.
```
