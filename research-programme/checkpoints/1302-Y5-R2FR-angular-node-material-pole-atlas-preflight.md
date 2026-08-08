# 5286 — Angular-node material-pole atlas preflight

## Purpose

The fixed-angle source result cannot simply be copied across the angular
domain. This checkpoint rebuilds the energy-channel geometry at each
order-two angular Gauss node, scans for interior channel zeros, refines
each detected complex pole, and builds the exact-mask energy-panel
contract required by an inner integrator.

## Pole-presence patterns

- `A02_S01_D01`: `['MC12']`
- `A02_S01_D02`: `['MC04']`
- `A02_S02_D01`: `[]`
- `A02_S02_D02`: `[]`

- present material poles:
  `4`;
- absent material channels:
  `12`;
- unresolved near-zero channels:
  `0`;
- maximum channel-root residual:
  `2.2204492918e-16`;
- maximum E040/E020 real-pole separation:
  `7.27717981541e-07`.

Decision:
`ACCEPT_ORDER2_ANGULAR_POLE_ATLAS__RUN_INNER_ENERGY_SMOKE`.

Validation: **PASS**.

## Claim boundary

This is a working pole atlas and panel preflight. It does not yet claim
angular convergence or a full phase-space coefficient.
