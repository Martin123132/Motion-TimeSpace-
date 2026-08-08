# 5311 — Material-pole-aligned energy preflight

## Result

The 5310 rectangular refinement failure is not an unexplained numerical
instability.  Exact continuation of the parent collision geometry places a
material energy pole inside the worst failed leaf of each affected topology
contract (`3`, `8`, and `29`).  The same scans also identify removable
zero-residue poles rather than treating every geometric collision as singular.

For each witness, the material Laurent term is fitted twice, subtracted before
quadrature, and restored analytically as
`R[log(E_hi-p)-log(E_lo-p)]`.  The remaining energy integral is evaluated on
panels aligned to the pole centers and regulator widths.

- failed-leaf witnesses: `3`;
- geometric poles scanned: `10`;
- material simple poles: `5`;
- removable zero-residue poles: `3`;
- unresolved poles: `0`;
- aligned energy panels: `168`;
- maximum corrected Q4/Q8 change:
  `7.2226626092e-09`;
- maximum corrected Q8/Q12 change:
  `1.21064805848e-09`;
- unaligned direct Q4/Q8 control change:
  `1.62160291219`.

Decision: **MATERIAL_POLE_CAUSE_PROVED_AND_SUBTRACTION_PREFLIGHT_PASSES__BUILD_RESUMABLE_OUTER_SOFT_INTEGRAL**.

Validation: **PASS**.

## Claim boundary

This proves the cause and subtraction route at three representative failed
soft coordinates.  It does not yet perform the continuous outer soft-angle
integral, the decay-angle integral, a full phase-space coefficient, local GR,
or the full MTS theory.
