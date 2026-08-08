# 5305 — Topology-safe regulator-ladder preflight

## Result

Four fixed-decay energy nodes now cover the narrow two-branch region, the
angular-cutoff event, the validated 5302 witness, and the upper INNER branch.
The lower `g1` activation edge and the later `g2` cancellation edge were
checked directly against the transported `MC04+MC12` sign orbit. Above the
`g2` edge the newly active `MC12(-,+)` term cancels `MC04(-,-)` exactly.

The full `MC04+MC12` four-sign orbit reproduces the single `MC04(-,-)` edge
component at the selected support probes with maximum relative error
`2.14130718488e-16`. This licenses
the cheaper one-component integrand for the next selected-node ladders only.

- selected energy nodes: `4`;
- mask probes: `27`;
- sign-orbit probes: `40`;
- E0025 peak-scan rows: `1143`;
- planned angular panels: `1803`;
- widest panel: `0.00894531320368`;
- widest peak-core panel: `2.00000000006e-06`.

Decision: **TOPOLOGY_SAFE_NODES_SYMMETRY_AND_PEAK_PANELS_RESOLVED__RUN_FIVE_REGULATOR_LADDERS**.

Validation: **PASS**.

## Claim boundary

This is a topology, symmetry, peak-localization, and panel-construction
preflight. It is not a finite-regulator integral, regulator-zero result,
energy-angle cubature, phase-space coefficient, local-GR result, or full-MTS
claim.
