# 5020 — two-loop amplitude cut object and normalization closure

## Concrete verdict

The suspected amplitude/form-factor swap is **not** the missing hhh factor. The Bern--Parra-Martinez--Sawyer identity is genuinely an amplitude-times-form-factor equation, so checkpoint 4987 cited it too broadly. But the object being calculated here is the two-loop four-scalar **scattering amplitude**. The direct gravity-amplitude source at `post-checkpoint-work/source-intake/functional_rg/4985/sources/bern/gr_simp.tex` uses ordinary amplitude unitarity: its three-particle contribution is tree amplitude times tree amplitude. Therefore

```text
C3_hhh      = A_2phi3h^(0) x A_2phi3h^(0),
C3_phiphih  = A_4phi1h^(0) x A_4phi1h^(0)
```

is retained. The `D1 F1` term is the Callan--Symanzik action on the reduced amplitude, not evidence that one five-point tree must be replaced by an operator form factor.

## Exact normalization chain

With `kappa^2=32 pi G`, each five-point tree carries `(kappa/2)^3`, so

```text
[(kappa/2)^3]^2 = kappa^6/64,
kappa^6/G^3     = 32768 pi^3.
```

The sequential three-body measure and normalized angular average give, at `s=4`,

```text
U3_plus/(kappa^6 s^3) = E[H]/(8192 pi^3),
D3/G^3                = -2 E[H]/pi.
```

The same derivation reproduces the independently inherited two-particle weights

```text
D_phiphi/G^3 = -32/pi,
D_hh/G^3     = -64/pi.
```

The real master contains `2D=-U/(pi s^3)`. The hhh `1/3!` is the identical-state completeness factor; there is no extra one-loop placement factor on a tree-times-tree three-particle cut. Every algebraic residual in `post-checkpoint-work/source-intake/functional_rg/5020/coupled_cut_normalization_chain.csv` is zero.

## What the factor-like pattern means

The checkpoint-5017 raw nonlocal hhh vector and the checkpoint-5018 required vector have correlation `0.994601923` and least-squares diagnostic scale `58.848835043`. After that best scale, the relative L2 residual is `0.102070`.

That is useful: the raw calculation has found the broad nonlocal shape. It is **not** permission to multiply it by `64`. The exact coupling/measure chain already gives `-2/pi`, and the raw real-sphere crossed integral was proved in checkpoint 5019 to use the wrong contour. The apparent scale remains a contour/continuation diagnostic until pole residues are included.

## Status

- Three-particle cut object: **settled as amplitude times amplitude**.
- Common `G^3` normalization through two- and three-particle cuts: **derived exactly**.
- Hypothesized missing overall factor `64`: **rejected**.
- Raw/target shape alignment: **recorded but not fitted**.
- Finite-`x` crossed hhh pole completion, coupled locality, UV coefficient, local GR and full MTS: **open**.

Next: reduce one global phase-space azimuth to a unit-circle contour, track the finite-`x` external--internal poles from the physical sheet, and integrate the pole-corrected azimuth before the remaining phase-space variables.
