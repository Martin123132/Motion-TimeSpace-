# 5086 - outward same-source residue-contour gate

Marker: `MTS_5086_OUTWARD_SAME_SOURCE_RESIDUE_CONTOUR_GATE`.

At `S507603_N0000`, `E040_A12`, two isolated same-source residue rows become
less stable when their contours are repeatedly shrunk. They are chamber-0
`direct:g1:minus_u/plus_u` near `16.8768718115` and chamber-2
`direct:g2:minus_v/plus_v` near `-16.6766642636`.

For an isolated finite collision, the contour can instead expand while
remaining below half the nearest-root safe scale. Fractions
`0.25, 0.30, 0.35, 0.40, 0.45` are tested in order. The smallest candidate is
accepted only when the production `32/48` ladder, audit `48/64` ladder, and
their cross-comparison are all below `0.005`.

The `g1` row first passes at fraction `0.30`; the `g2` row passes at `0.25`.
The recomputed `A12` kernel converges with every residue stable. The runner
uses this policy only for unstable same-source, same-chirality minus/plus
pairs in `direct:g1` or `direct:g2` and otherwise fails closed.

## Evidence

- Gate: `source-intake/functional_rg/5086/outward_same_source_residue_contour_gate.json`
- Recomputed kernel gate: `source-intake/functional_rg/5086/A12_primary24_outward_repair_gate.json`
- Generator: `scripts/Y5_R2FR_5086_outward_same_source_residue_contour_gate.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5086_VALIDATION.csv`

This is a numerical contour certificate, not an amplitude or MTS claim.
