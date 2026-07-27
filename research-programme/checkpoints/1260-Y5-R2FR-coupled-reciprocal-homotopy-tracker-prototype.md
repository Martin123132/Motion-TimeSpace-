# 5244 — Coupled reciprocal homotopy tracker prototype

## Derivation

The matched component owns a reciprocal root pair, so representative and reciprocal roots are not independent branches. At every homotopy node this prototype selects the joint candidate pair that first minimizes `|r_rep r_rec - 1|` and then minimizes projective continuation distance. This enforces the exact component constraint during transport rather than checking it only after two independent tracks have been chosen.

## Reference set

`10` cases: five 5242 high-resolution controls plus one interior representative for every distinct Q03 cached winding state.

## Results

- Reference states reproduced: `9/10`.
- Maximum coupled/reference step fraction: `2`.
- Maximum reciprocal residual: `7.90134180417e-12`.
- Maximum collision-pair projective step: `0.176356302165`.
- Maximum chamber-boundary projective step: `0.999999997009`.
- Runtime: `106.835 s`.

## Decision

`HOLD_COLLISION_PAIR_REPAIR__DERIVE_RECIPROCAL_PROJECTIVE_BOUNDARY_TRACKER`

## Claim boundary

This audits collision and boundary transport at a bounded reference set. It does not yet rebuild Q03/Q05, integrate the two-angle slice, derive local GR, or validate full MTS.

## Interpretation

Joint collision-root selection repairs reciprocal identity to about 1e-11, but it is not sufficient. The physical chamber endpoint can still make an almost unit projective jump, and one cached winding state is not reproduced. The remaining ambiguity belongs to endpoint sheet exchange, not to the reciprocal collision pair.

## Next exact target

Track each physical chamber endpoint as its reciprocal projective pair through the homotopy, allowing endpoint sheet exchange without a logarithmic jump. Re-run this same ten-case reference set before returning to 5243.
