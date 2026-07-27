# 5234 - Complete active-family physical-channel and pole-order atlas

## Decision

`ADOPT_COMPLETE_PHYSICAL_CHANNEL_ATLAS_AND_BUILD_DYNAMIC_ROOT_ENUMERATOR`.

This checkpoint replaces the phrase “the A00 tails have more missing poles”
with a finite, source-backed atlas.  The 5231 pool contains exactly ten
nonzero canonical families and twelve reciprocal components.  The two extra
components are the second collision branches of the `g1/g2` families.

## The summand owner is now measured

The finite-plus integrand is the difference of a direct five-point KLT term
and its endpoint subtraction.  Their local double coefficients were separated
before taking the family residue:

```text
C_total = lim_(delta->0) delta^2 (T_direct - T_endpoint) / e
        = C_direct + C_endpoint.
```

The result is not an assumption:

- `AF01_C01` `direct:g2:plus/direct:g3:minus`: `direct_five_point` at owner fraction `0.999999999504`.
- `AF02_C01` `direct:g1:plus/direct:g3:minus`: `direct_five_point` at owner fraction `0.999999998814`.
- `AF03_C01` `direct:g2:minus/direct:g3:plus`: `direct_five_point` at owner fraction `0.999998494423`.
- `AF04_C01` `direct:g3:plus/subtraction:decay:plus`: `endpoint_subtraction` at owner fraction `0.999997211971`.
- `AF05_C01` `direct:g3:plus/subtraction:decay:minus`: `endpoint_subtraction` at owner fraction `0.999999866337`.
- `AF06_C01` `direct:g3:minus/subtraction:decay:plus`: `endpoint_subtraction` at owner fraction `0.999999999976`.
- `AF07_C01` `direct:g1:minus/direct:g3:plus`: `direct_five_point` at owner fraction `0.999999669907`.
- `AF08_C01` `direct:g3:minus/subtraction:decay:minus`: `endpoint_subtraction` at owner fraction `0.999999998595`.
- `AF09_C01` `direct:g1:minus/direct:g2:plus`: `direct_five_point` at owner fraction `0.999999963612`.
- `AF09_C02` `direct:g1:minus/direct:g2:plus`: `direct_five_point` at owner fraction `0.99999984278`.
- `AF10_C01` `direct:g1:plus/direct:g2:minus`: `direct_five_point` at owner fraction `0.999999995573`.
- `AF10_C02` `direct:g1:plus/direct:g2:minus`: `direct_five_point` at owner fraction `0.999999995701`.

All direct/direct families are direct-five-point owned.  Every
`g3/subtraction:decay` family is endpoint owned because `direct:g3` is the
same direction as the endpoint soft leg, while `subtraction:decay` supplies
the hard four-point factor.  The minimum measured owner fraction is
`0.999997211971`.

## Exact channel equations

Write `e=E_3` and `C=n_s.d` for the soft energy and soft/decay relative
cosine.  Momentum conservation gives the three shared internal invariants
without fitting:

```text
s12 = 4(1-e),
s13 = 2 e (1-C),
s23 = 2 e (1+C).
```

For either hard or soft internal leg `i`, the scalar channels are

```text
left:  s0i=-2 E_i(1-h_i),      si4=-2 E_i(1+h_i),
right: s0i=-2 E_i(1-o.n_i),    si4=-2 E_i(1+o.n_i).
```

The scalar-pair/complement channel is fixed: `s04=s123=4`.  In the endpoint
subtraction the hard aliases are `s01=s24`, `s02=s14`, and `s12=s04=4`;
the soft-factor channels are `s03,s13,s23,s34`.  The implementation exposes
the full ten-pair orbit after these complement aliases are expanded.

Across `136` independent direct and endpoint checks, the largest
relative equation residual is
`1.17151329e-14`.
Every source label in every reciprocal component also lands on its stated
right-cut physical channel; the largest relative zero residual is
`1.01543705e-13`.

## Pole-order theorem

An isolated tree factorization divisor has

```text
M_5 = sum_h M_L M_R / D + O(1).
```

It is therefore at most simple.  Checkpoint 5138 proves this explicitly for
one scalar-graviton KLT representative, including cancellation of the apparent
Parke-Taylor double denominator.  Graviton permutation and scalar crossing
cover the six scalar-graviton channels.  Checkpoint 5127 supplies the existing
full-amplitude graviton-graviton witness; the fresh active-family `s13`
witness here has slopes
`-1.00552439` and
`-0.954674438`, regular `D*T`, vanishing
`D^2*T`, and retained windings
`(1,-1)`.

Taking the local collision residue is linear.  If the already-consumed
collision factors are `A(z,q)B(z,q)` and a third transverse channel is
`D(q)`, then

```text
Res_z^[A,B] C/[A B D] = C_eff(q)/D(q).
```

The collision residue cannot raise the third-channel order.  At genuine
intersections the code must inspect the full multivariate residue; the atlas
explicitly forbids multiplying one-dimensional pole orders by hand.

## What is and is not closed

All `172` owner-surface rows are classified as:

1. already consumed by the local double-collision residue;
2. fixed and nonzero; or
3. a simple candidate whose root must be enumerated and causally subtracted
   if it intersects the integration domain.

This is a complete structural pole atlas, not yet the completed A00 integral.
It does not establish the UV coefficient, local GR, or the full MTS theory.

## Next target

Build the dynamic root enumerator from these exact equations, retain only
roots on the inherited Feynman sheet with active winding, subtract each
certified simple pole analytically, and run a small all-channel A00 pilot.
