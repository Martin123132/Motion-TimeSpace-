# 5437: external01 endpoint zero and pole-order gate

## Decision

**POINTWISE FINITE ENDPOINT DETECTED; PHYSICAL-POLE ROUTE REJECTED.**

At both representative broad-chart centres, `s01`, `[01]`, and `<01> = s01/[01]` approach finite nonzero constants as `t -> 0`. Their fitted log orders are zero. The 5436 zero enclosure is therefore an interval-width dependency, not evidence for a physical collinear pole. The next route is a finer endpoint `t` subcover.

## Pointwise order table

| target | |[01](0)| | |s01(0)| | |<01>(0)| | ord(s01) | ord(<01>) | ord([01]) |
|---|---:|---:|---:|---:|---:|---:|
| LR | 0.229636799617 | 0.00265603726888 | 0.0115662527666 | 0.00002123 | 0.00001987 | 0.00000136 |
| R | 0.230460558058 | 0.00258942918892 | 0.0112358887383 | 0.00002127 | 0.00001988 | 0.00000140 |

## Scope

- This is a reproducible pointwise order diagnostic at the LR/R broad-chart centres and the regulator midpoint.
- It distinguishes a finite endpoint from a simple endpoint zero before any full-cover calculation.
- It does not prove the order uniformly in `x`, regulator, displacement, or chart selector.
- All parent, right-connector, UV, and local-GR claim flags remain false.

## Next derivation

Build the anisotropic endpoint `t` negative-real subcover before any v48 parent edit.
