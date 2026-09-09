# 5432: path-correlated first-spinor subcover gate

## Decision

**COMMON-FAMILY ROUTE REJECTED; FINITE OUTER CHART COVER RETAINED.**

The stronger constructor certifies LLU, but LR and R cross between the plus and minus projective families. A single spinor gauge cannot cover those broad boxes, so wiring this fallback into the parent would be an invalid partial fix. This is a chart transition, not a zero-momentum result.

## Result

- Probe rows: `20`.
- Old direct no-pivot rows: `16`.
- Path-correlated subcover passes: `4`.
- Minimum certified pivot: `0.070109840755822023`.
- Maximum subdivision count required: `2`.

## Next integration

Use the existing adaptive x/t partition to produce a finite chart cover of LR and R, then freeze the committed union.

## Claim boundary

This is a chart-existence certificate, not right-connector completion and not a W3, UV, local-GR, or full-MTS claim.
