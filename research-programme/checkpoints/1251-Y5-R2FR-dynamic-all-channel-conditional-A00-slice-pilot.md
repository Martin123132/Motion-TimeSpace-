# 5235 - Dynamic all-channel conditional A00 slice pilot

## Decision

`ADOPT_CAUSAL_DYNAMIC_ROOT_FILTER_AND_SCALE_TO_MULTI_EVENT_PILOT`.

Checkpoint 5234's atlas is now used as an executable root catalogue rather
than a list of future targets.  On the representative `AF02_C01`
`g1+/g3-` component, all `13` unconsumed direct
surfaces were scanned over the full conditional
`decay_cosine in [-0.995,0.995]`.  No pole coordinate was
hardcoded.

## Geometry is not enough

The scan found three geometric zeros:

- `direct:L:s14`: `q_*=-0.839588768226-5.43998014841e-05 i`, windings `(1,-1)`, active `True`.
- `direct:shared:s13`: `q_*=-0.324372188378-0.000164952671701 i`, windings `(1,-1)`, active `True`.
- `direct:L:s01`: `q_*=+0.643968231761-0.000107900624961 i`, windings `(0,0)`, active `False`.

The shared `s13` and left `s14` zeros retain the inherited reciprocal winding
and are genuine poles of this residue family.  The left `s01` channel is also
a real factorization zero, but both collision windings have switched off by
that point.  It is therefore not part of the active family correction and was
not subtracted.

This is the first concrete use of the distinction

```text
physical denominator zero != active causal residue-family pole.
```

It prevents both missed poles and spurious subtraction.

## Active residues

- `DP01` `direct:L:s14`: slopes `-0.998763873` and `-0.996507333`, numerator-fit residual `1.05470401e-07`.
- `DP02` `direct:shared:s13`: slopes `-1.00552439` and `-0.954674438`, numerator-fit residual `3.25275846e-09`.

Both active roots have simple `1/(q-q_*)` scaling and a regular fitted
numerator `D*T`.  The inactive root is absent from the residue-fit table.

## Two-patch pilot

The two accepted patches were integrated as

```text
integral T dq
  = integral [T - R/(q-q_*)] dq
    + R [Log_F(q_max-q_*) - Log_F(q_min-q_*)].
```

Their combined order-32 raw relative error is
`0.75949135`.  The combined order-32
subtracted error is
`1.3535319e-07`, an improvement of
`5611181.74x`.  The independent
order-1024 raw result differs from the subtracted reference by
`2.26287621e-05`.

## Scope

This closes one complete conditional slice: every atlas channel was scanned,
every geometric root was causally classified, and every active pole was
subtracted.  It is not yet the full multidimensional A00 coefficient and does
not establish the UV coefficient, local GR, or full MTS.

## Next target

Run the same causal root filter on a stratified set spanning direct and
endpoint-owned families, cache the accepted roots and residues, and compare
the raw versus fully subtracted event pools before authorizing a full run.
