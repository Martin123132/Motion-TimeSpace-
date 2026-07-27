# 5238 - Endpoint-owned residue and combined bounded A00 runner

## Decision

`ADOPT_ENDPOINT_OWNED_RESIDUE_AND_COMBINED_BOUNDED_A00_METHOD`.

The endpoint contribution is now isolated from the parent finite-plus
integrand rather than inferred from an ownership label.  At a local
collision its coefficient is

```text
C_endpoint = lim_(delta->0)
             [-endpoint_value / soft_energy] delta^2,

R_endpoint = (Delta w) sigma C_endpoint
             / (r_* z_* J_collision).
```

The symbols are the same reciprocal winding difference, chamber orientation,
relative root, global root and collision Jacobian already fixed by the direct
residue theorem.  No new closure coefficient is introduced.

## Ownership identity

- Audited endpoint component-coordinate jobs:
  `24`.
- Minimum endpoint coefficient fraction:
  `0.999997211971`.
- Maximum split-to-full closure residual:
  `5.8194450871e-16`.

Thus the isolated direct and endpoint coefficients reconstruct the original
finite-plus family residue before any outer-pole fit.

## Bounded endpoint run

- Families: `4`.
- Family/tranche strata: `8`.
- Reciprocal components: `8`.
- Component-coordinate jobs: `24`.
- Passed jobs: `24/24`.
- Geometric/active/inactive roots:
  `16/`
  `5/`
  `11`.

Relative to the endpoint order-512 subtracted
reference, order-32 subtraction changes the error from
`0.0306061261245` to
`4.99819806741e-11`.

## Combined method pool

The cached direct and endpoint patch unions were combined order by order.
This is a method-convergence pool, not yet the physical multidimensional
A00 coefficient.

- Raw order-32 error:
  `0.159683098568`.
- Subtracted order-32 error:
  `9.78831907869e-07`.
- Subtracted order-128 error:
  `2.14679489212e-07`.
- Order-32 improvement:
  `163136.384587x`.

## Failed jobs

- None.

## Scope

The complete active direct and endpoint residue families now have a common
branch-aware causal subtraction method.  This does not yet supply the
remaining regular-domain integration or regulator extrapolation needed for a
physical A00 coefficient, and it makes no UV, local-GR or full-MTS claim.

## Next target

Construct one matched event-level A00 integral that combines all active
component patches with the regular complement, then perform the E040/E020
regulator extrapolation before scaling to the 48-event source pool.
