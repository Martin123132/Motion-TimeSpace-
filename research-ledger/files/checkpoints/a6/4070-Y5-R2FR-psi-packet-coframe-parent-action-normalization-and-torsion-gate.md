# 4070 - Psi Packet Coframe Parent Action, Normalization, And Torsion Gate

- Timestamp: `2026-07-02T02:08:21+00:00`
- Status: `private_nonclaim_checkpoint`
- Decision: `PURE_GRADIENT_COFRAME_FLATNESS_OBSTRUCTION_FOUND_CARTAN_SOLDER_PARENT_ROUTE_CONSTRUCTED_CONDITIONALLY`
- Public GR/Newton/PPN claim: `false`
- GitHub action: `false`

## The Trap We Caught

The 4069 `psi`-packet coframe fixes the rank/signature problem, but the most obvious version still fails:

```text
e^A = dX^A,   g_obs = eta_AB dX^A dX^B.
```

If `det(dX) != 0`, then `X^A` are local coordinates and `g_obs` is just a pullback of flat internal Minkowski space. That gives `Riemann[g_obs]=0` locally, not curved GR.

So exact scalar gradients alone do **not** derive local GR. That old path is dead.

## Viable Repair

4070 keeps the route alive by making the needed geometry explicit:

```text
X^A = L_* Psi^A
e^A = D_omega X^A + B^A
g_obs = eta_AB e^A e^B
```

Here `B^A` is a translational/solder one-form and `omega^AB` is an internal Lorentz spin connection. This is the minimal Cartan/Palatini-style parent route that can avoid exact-gradient flatness.

## EH Reduction Chain

The conditional route is now:

```text
psi packet + Cartan solder field
-> nondegenerate Lorentzian coframe e^A
-> Einstein-Cartan / Palatini action
-> torsion-free or spinless branch
-> EH[g_obs] + boundary
-> 4063 weak-field Newton/PPN readout
```

This is not a completed MTS derivation yet. The new required derivation is sharper:

```text
derive B^A and omega^AB from MTS motion/flow/memory variables,
or demote them as effective-GR branch inputs.
```

## Hard Claim Limits

- No exact-gradient curved-GR claim.
- No public local-GR/Newton/PPN claim.
- No numerical Newton-G prediction.
- No torsion/extra-mode pass until the Cartan fields are parent-owned and constrained.

## Next

`4071` should attack the origin of the Cartan solder field: can `B^A` and `omega^AB` be derived from MTS flow/memory/transport variables, or are they imported GR infrastructure?
