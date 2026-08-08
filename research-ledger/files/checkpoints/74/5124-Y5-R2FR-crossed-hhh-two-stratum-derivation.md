# 5124 - crossed hhh two-stratum derivation

## Result

This checkpoint takes a forward step on the crossed `hhh` bottleneck. The
existing runner already forms the `s/t/u` cyclic sum at each outer event, so
wrapping the three completed target integrals in another sum cannot change
the random variable or its variance.

The fixed-event contour instead admits the exact split

```text
R = R_naive + R_topological,
R_naive = R_pole_model + R_smooth.
```

Richardson extrapolation, cyclic crossing and the local-shape projection are
all linear, hence the same split survives exactly in the final event-level
coefficient. The maximum numerical closure residual is
`2.478e-11`.

## What cancels and what can be sampled separately

The analytic pole model and regularized smooth remainder have design-matrix
correlations `-0.999978344` (real) and
`-0.999998779` (imaginary). They are large
opposite pieces and **must remain paired**. Separating them would manufacture
variance.

By contrast, `R_topological` and the already-paired `R_naive` have
correlations `0.086813` and
`0.037146`. The topological term carries the
dominant event variance and is an exact independent stratum.

Across `540` completed kernels, all
`8038` crossings form
`4019` reciprocal-root pairs. For the
`3222` isolated safe pairs, reflection of the
relative circle gives `Res(1/r)=-Res(r)`; the largest measured antisymmetry
residual is
`1.916e-09`. The
`797` clustered or mixed `g2/decay` pairs remain
fail-closed and evaluate both residues.

The reciprocal-reduced production replay reproduces the stored topological
correction with relative residual
`2.086e-13` and all
residues stable. It evaluates `11` instead
of `18` crossing rows and costs
`0.562` of the full fixed-event
gate in the recorded benchmark.

The simpler unreduced split was tested first and rejected: its measured cost
fraction was `0.790`, producing
projected speedups `0.851`
(real) and `0.919`
(imaginary), both below unity. The reciprocal theorem—not relabelling the old
estimator—is what makes the revised stratum useful.

## Conditional reciprocal proof

The relative azimuth is represented by `xi` through

```text
c(xi) = (xi + xi^-1)/2,
s(xi) = (xi - xi^-1)/(2 i).
```

Under `I: xi -> xi^-1`, `c` is fixed and `s` changes sign. This is reflection
through the external scattering plane. On an isolated ownership branch the
helicity-summed KLT-plus scalar kernel is reflection-even, so
`F(I xi)=F(xi)`. For the relative contour one-form

```text
omega = F(xi) dxi/xi,
I*omega = F(I xi) d(xi^-1)/(xi^-1) = -omega.
```

Residues of a one-form are invariant under coordinate pullback; therefore
`Res_(1/r)(omega)=-Res_r(omega)`. This proof is deliberately restricted to
one-to-one isolated reciprocal ownership families. Multi-root groups and the
mixed direct-`g2`/subtraction-`decay` family do not yet satisfy that mapping
contract and are the 797 pairs retained fail-closed.

## Derived allocation

For independent topological and full/naive event banks,

```text
Var = sigma_naive^2/N_naive + sigma_top^2/N_top,
Cost = c_full N_naive + c_top N_top,
N_top/N_naive = (sigma_top/sigma_naive) sqrt(c_full/c_top).
```

The 16-event design matrix gives optimal ratios
`5.301` (real) and
`7.520` (imaginary), with
projected cost-normalized speedups `1.104` and
`1.215`. These are design estimates, not an
independent efficiency result; a fresh pilot must confirm them before the UV
coefficient is reconsidered.

## Source-scope correction

The Bern gravity source supplies the exact pure-gravity four-graviton `R^3`
running. It does not supply the two-loop four-scalar `K_mu` coefficient and is
therefore not substituted for this calculation.

## Physics discipline

- No exterior event is deleted or downweighted after inspection.
- No hhh target, locality residual, or desired coefficient is fitted.
- No field equation or coupling is retuned.
- No numeric UV coefficient, local GR/Newton limit, galaxy law, or full MTS is claimed.
- The governing cog condition remains: one parent mechanism must preserve the successful local GR/Newton regime while deriving any large-scale activation without a manual switch.

## Next calculation

Build the restartable reciprocal-reduced topological outer-event runner from
the exact gate proved here, lock fresh seeds and an allocation before seeing
outcomes, then compare its realized cost-variance against the paired high
estimator. The `pole_model+smooth` contour must remain a single full-event
stratum, and unsafe reciprocal families must continue to evaluate both roots.
