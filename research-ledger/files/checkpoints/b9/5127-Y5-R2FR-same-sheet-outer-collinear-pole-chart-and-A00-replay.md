# 5127 - same-sheet outer-collinear pole chart and A00 replay

## What the failed integration was actually seeing

The endpoint-adjacent direct-`g1` collisions are removable double-zero
collisions, but they were not the dominant A00 error. Two symmetric interior
intervals contain four genuine outer simple poles that checkpoint 5030 could
not catalogue because it searched only opposite-ownership global-root
collisions.

The missing roots are derived before replay from

```text
C(q)=c_s c_d+s_s s_d(q+q^-1)/2.
```

The beam-spinor family satisfies `p_1^-=E_1-p_1z=0`. The hard-soft family
satisfies

```text
s_13 = 2 e A (1+beta) (1-C) = 0.
```

Each condition is a quadratic in `q` with reciprocal roots. No root, event,
seed or fit parameter was inferred from the desired integral value.

## Guarded numerical continuation

For each isolated root `z0=log(q0)`, the integrated global cycle is written

```text
F(z) = R/(z-z0) + H(z).
```

`R` is measured on an isolated high-precision Cauchy boundary. The absence of
a material second principal coefficient checks the simple-pole order. The
regular part `H` is reconstructed by Cauchy's formula only inside 65% of that
boundary radius; outside it the original evaluator is used. The pole is
subtracted in the adaptive integrand and integrated analytically. No principal
value or half residue is inserted.

- `beam_spinor:small`: `q=(0.12666165152262066+0j)`, `Res=(5.754987326726801-0.05183427890224275j)`, path distance `0.000184594`.
- `hard_soft_invariant:small`: `q=(0.33192806900481986+0j)`, `Res=(-16.369687781612072+0.1457293425852153j)`, path distance `9.85258e-05`.
- `hard_soft_invariant:large`: `q=(3.0127009234204865+0j)`, `Res=(16.36968791904939-0.14572930429311445j)`, path distance `9.85258e-05`.
- `beam_spinor:large`: `q=(7.895049432711758+0j)`, `Res=(-5.75484490653906+0.05194832630209567j)`, path distance `0.000184594`.

## Exact replay

The locked A00 row changes from `COMPLETED_UNCONVERGED` to
`COMPLETED_CONVERGED`. Its interval count changes from
`4112` to
`69`, and the maximum chamber error
changes from `0.003319880181794845` to
`1.8630336285107402e-05` under the unchanged
`5e-5` tolerance and 4096-interval cap.

The new causally corrected value is
`(4759.048142980555-2596.8478131853926j)`. It remains private nonclaim pilot
data. Checkpoint 5127 repairs a missing analytic stratum in the numerical
contour map; it does not establish the UV coefficient, source coupling,
local GR/Newton, Maxwell, galactic dynamics or full MTS.

The machine/cog condition is unchanged: one parent theory must preserve the
tested local GR/Newton cogs while deriving galactic activation without a
manual regime switch.
