# 5380 - D4 complexified event-neighborhood certificate

## Decision

`D4_COMMON_CLOSED_COMPLEX_EVENT_NEIGHBORHOOD_CERTIFIED__ENCLOSE_PARENT_RESIDUE`

## Construction

The real component equations certified in checkpoint 5379 are complexified as analytic algebraic equations. Branch deaths use three complex unknowns. Support contacts use five, with `s^2+c^2=1` replacing the soft-angle square root. This avoids an unsupported complex interval square-root branch.

Each real regulator bin is thickened to `|Im epsilon| <= 1e-06` and tested by a complex rectangular Krawczyk operator. Failed faces are enlarged only by their measured inclusion deficit, with safety factor `1.5`, and the complete operator is recomputed for at most `8` steps.

- certified boxes: `64/64`;
- maximum contraction bound: `0.004464108856732533`;
- minimum strict real/imaginary inclusion margin: `6.986543461817707e-11`.

## Scope

This certifies the analytic event branches on a common closed complex epsilon neighborhood. It does not yet interval-enclose the parent residue and its amplitude denominators there, so the strict endpoint-C theorem, H3, W3, D4 outer limit and broader claims remain open.
