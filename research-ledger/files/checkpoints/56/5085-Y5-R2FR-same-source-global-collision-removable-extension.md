# 5085 - same-source global-collision removable extension

Marker: `MTS_5085_SAME_SOURCE_GLOBAL_COLLISION_REMOVABLE_EXTENSION`.

The next fresh-pilot obstruction occurs at `S507603_N0000`, `E040_A11`,
chamber 1, where opposite-ownership `direct:g2:plus_u` and
`direct:g2:plus_v` global poles coalesce. Their equality is not accidental:

`plus_u = plus_v  iff  e^2 = h hbar  iff  n_z = z`.

A symmetric three-direction approach and Richardson extrapolation were
evaluated at 24, 32, and 48 global nodes. The directional spread is at most
`1.82e-9`, the node-ladder spread is `3.26e-10`, and the common finite limit
is

`6654.904194418538 + 293.6848357474912 i`.

The recomputed `A11` kernel converges and invokes the extension 13 times. The
runner permits the extension only for opposite-ownership `u/v` coalescences
within `direct:g1` or `direct:g2`; every invocation must independently pass
the multidirection limit. The later pilot failure at `E020/A07` demonstrates
that this is a fail-closed row-level gate, not a blanket removable-pole axiom.

## Evidence

- Gate: `source-intake/functional_rg/5085/same_source_global_collision_removable_extension.json`
- Recomputed kernel gate: `source-intake/functional_rg/5085/A11_primary24_extension_gate.json`
- Generator: `scripts/Y5_R2FR_5085_same_source_global_collision_removable_extension.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5085_VALIDATION.csv`

This certifies the stated local extension and no wider physical claim.
