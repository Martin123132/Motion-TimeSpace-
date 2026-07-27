# 5236 - Stratified causal multi-slice A00 pool validation

## Decision

`ADOPT_STRATIFIED_CAUSAL_POOL_METHOD_AND_PREPARE_BOUNDED_MULTI_EVENT_RUN`.

The 5235 root scanner and subtraction were not left as a one-event success.
This checkpoint adds an independent direct family and an endpoint-owned
negative control:

- `AF01_soft_energy`: owner `direct_five_point`, geometric/active/inactive roots `1/1/0`, subtracted patches `1`.
- `AF02_decay_cosine`: owner `direct_five_point`, geometric/active/inactive roots `3/2/1`, subtracted patches `2`.
- `AF04_endpoint_decay_cosine`: owner `endpoint_subtraction`, geometric/active/inactive roots `1/0/1`, subtracted patches `0`.

## Independent direct slice

For `AF01_C01`, all atlas surfaces were scanned over
`soft_energy in [0.005,0.995]`.  The scan found
one left-`s24` pole,

```text
q_* = +0.722986913699
      +7.86644933412e-05 i,
```

with causal windings
`(-1,1)`.  Its order-32
subtracted patch error is
`8.03766812e-05`, compared
with raw error `0.752596855`.

## Endpoint-owned control

The endpoint `AF04_C01` slice contains the geometric
`endpoint:shared:soft:s23` zero at
`+0.500209418095`.  Its windings are
`(0,0)`, not the inherited active
pair.  It is therefore recorded but deliberately not subtracted.

This confirms that the same filter works on both summand owners: it accepts a
direct physical pole when the residue family is live and rejects an endpoint
factorization zero when that family has left the causal cycle.

## Pooled convergence

The three accepted patches from the two direct slices were pooled only after
individual causal classification and subtraction.  Relative to the pooled
order-1024 subtracted reference:

- raw order-32 error: `0.76161425`;
- subtracted order-32 error:
  `2.60065135e-05`;
- improvement: `29285.5191x`;
- order-1024 raw crosscheck error:
  `2.99203588e-05`.

The stabilization is therefore not specific to one pole, one coordinate, or
one event.

## Scope and next target

This is a stratified conditional pool, not the full multidimensional A00
coefficient.  It validates the method needed for that computation without
making a UV, local-GR, or full-MTS claim.

The next implementation should package this scanner, winding gate, residue
fit and cache into a bounded multi-event runner, dry-run its job manifest, and
only then authorize a larger A00 calculation.
