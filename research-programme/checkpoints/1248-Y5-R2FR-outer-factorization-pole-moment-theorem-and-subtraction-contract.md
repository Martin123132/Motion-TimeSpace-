# 5232 - Outer factorization-pole moment theorem and subtraction contract

## Result

Decision: `ADOPT_ANALYTIC_OUTER_POLE_SUBTRACTION_BEFORE_ANY_NEW_A00_POOLING`.

Checkpoint 5231's local double-residue law was correct, but it did not yet
identify the outer source of the large A00 events.  Two independent extreme
families now show the same mechanism.  A third, ordinary KLT propagator

```text
D_h4 = (k_h + p_4)^2
```

vanishes transversely while the collision winding remains active.  The local
tail is therefore

```text
T(q, epsilon) = R / (q - q_*(epsilon)) + O(1),
```

not a numerical quadrature failure and not a higher global-azimuth pole.

## Located poles

- `fresh_g1_decay_pole` `E040`: `q_*=-0.839588430801-0.000108798207757 i`, `|D'|=1.42656735`.
- `fresh_g1_decay_pole` `E020`: `q_*=-0.839588768222-5.43998016249e-05 i`, `|D'|=1.4265661`.
- `old_g2_soft_energy_pole` `E040`: `q_*=+0.722986424026+0.00015732681797 i`, `|D'|=1.65564921`.
- `old_g2_soft_energy_pole` `E020`: `q_*=+0.72298691369+7.86644942107e-05 i`, `|D'|=1.6556483`.

The fresh positive tail uses `q=decay_cosine`, `h=g1`; the old negative tail
uses `q=soft_energy`, `h=g2`.  In both cases `D_h4` equals its complementary
three-particle channel to the recorded tolerance.  Its derivative is nonzero.
The imaginary displacement of `q_*` halves from E040 to E020, as required by
the inherited regulator.

## Scaling test

- `fresh_g1_decay_pole` `E040`: negative slope `-0.991817672`, positive slope `-0.989551111`.
- `fresh_g1_decay_pole` `E020`: negative slope `-0.998768923`, positive slope `-0.996502303`.
- `old_g2_soft_energy_pole` `E040`: negative slope `-0.966239462`, positive slope `-0.995872122`.
- `old_g2_soft_energy_pole` `E020`: negative slope `-0.980347019`, positive slope `-1.00999994`.

Multiplying the correction by `D_h4` leaves a locally regular numerator:
the one-sided relative spreads are below
`0.02`.  The covariant KLT replay agrees with the
spinor implementation at relative residual
`1.56065651e-10`.  The tail is therefore a
physical factorization pole of the current cut integrand, not a spinor-chart
conditioning artefact.

## Physical topology

At the real part of both located poles, E040 and E020 targeted homotopies keep
the stored reciprocal winding:

- fresh `g1/g3`: `W_u=+1`, `W_v=-1`;
- old `g2/g3`: `W_u=-1`, `W_v=+1`.

The previously suspected joint angular corner is different.  At
`soft_cosine=0.99`, `decay_cosine=0.98`, a 49152-step
single-family track resolves two crossings of each reciprocal root with
opposite signs.  Both net windings are zero.  The frozen-winding corner
divergence is rejected.

## Moment theorem

If an active contribution behaves as `rho^(-s)` near a codimension-`k`
singular set, its `p`th absolute moment exists exactly when

```text
p s < k.
```

Equality gives a logarithmic divergence.  Here `k=1` and `s=1`.  Consequently
the zero-regulator random variable has no absolute first moment and no second
moment.  Its complex integral is still defined as the Feynman boundary value,
but it is not the ordinary expectation estimated by a raw Monte Carlo mean.
This explains why ordinary pooling, jackknifes and median-of-means could not
stabilize the A00 tranches.

## Required subtraction

For each active outer pole, compute

```text
R = lim_(q -> q_*) (q-q_*) T(q)
  = lim_(q -> q_*) D(q) T(q) / D'(q_*).
```

Then use

```text
integral T dq
  = integral [T - R/(q-q_*)] dq
    + R [Log_F(q_max-q_*) - Log_F(q_min-q_*)].
```

The first term is the regular numerical remainder.  The second is analytic
and retains the causal branch; at zero regulator it supplies the
principal-value and signed `i*pi R` terms.  Randomized QMC is admissible only
for the subtracted remainder.

## Claim boundary

This checkpoint does not establish the numeric UV coefficient, local GR, or
the full MTS theory.  It replaces an invalid statistical question with the
correct causal integration contract.

## Next target

Build the complete active-family outer-pole atlas, derive every `q_*` and
outer residue, apply the subtraction family by family, and rerun the fresh
A00 replication on the regular remainder.
