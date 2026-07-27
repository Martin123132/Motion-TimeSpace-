# 4055 - Hilbert Owner, D_GK Zero, and Trace/Background Subtraction

- Timestamp: `2026-07-02T00:59:14+00:00`
- Status: `private_nonclaim_checkpoint`
- Formalization modified: `false`
- Public local-GR claim: `false`

## What Actually Moved

4053 left `D_GK=0` and trace/background subtraction as the sharp remaining `q_loc` blockers. 4055 turns them into a parent-action contract.

Define the renormalized local density:

```text
Gamma_ren := Gamma_eff - Gamma_0 - Gamma_ref,
Gamma_ren(Phi0)=0,    d Gamma_ren|Phi0=0.
```

Then define the parent sector:

```text
S_GK[g,Y] := - int sqrt|g| Gamma_ren(g,Y,nablaY,D) + B_GK[g,Y],
T_Hilbert_GK^{mu nu}:=(-2/sqrt|g|) delta S_GK/delta g_{mu nu},
K_Gamma^{mu nu}:=Gamma_ren g^{mu nu}-T_Hilbert_GK^{mu nu}.
```

If the live local branch adopts

```text
Khat^{mu nu}:=K_Gamma^{mu nu},
```

then the mismatch is algebraically zero:

```text
D_GK^{mu nu}
= Gamma_ren g^{mu nu}-Khat^{mu nu}-T_Hilbert_GK^{mu nu}
= 0.
```

That means the Helmholtz/integrability issue is not a handwave: inside this candidate packet, `T_GK` is a Hilbert stress by construction.

## Trace Rule

The constant piece `Gamma_0` is fixed background/Lambda/reference data:

```text
nabla Gamma_0 = 0,
delta_local Gamma_0 = 0,
D_source Gamma_0 = D_range Gamma_0 = D_readout Gamma_0 = 0.
```

So it cannot be used as compact local mass, radial `G`, or a source-dependent prefactor. The only local `q_loc` carrier is `Gamma_ren`, and the quadratic/fixed-point rule makes its first variation vanish.

## Honest Status

This is a real derivation path, not another missing-list. But it is still conditional: 4055 defines the exact parent adoption contract. It does not prove the older live `Khat` symbols were already `K_Gamma`.

If adoption is rejected, the fallback is now exact:

```text
Delta_K^{mu nu}:=K_Gamma^{mu nu}-Khat^{mu nu},
|q_loc| <= ||P_loc|| |nabla_mu Delta_K^{mu nu}| + Euler/boundary/source terms.
```

## Next Target

Build the integrated local parent packet: EH + same-source matter/EM + `Gamma_ren/K_Gamma` + no-source-boundary/projector clauses. If the packet cannot be adopted cleanly, run the `Delta_K` bound branch.
