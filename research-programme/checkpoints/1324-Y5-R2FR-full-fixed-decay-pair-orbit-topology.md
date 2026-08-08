# 5308 — Full fixed-decay pair-orbit topology

## Derivation

The earlier moving `g1` edge is not the end of the pair-orbit support.
Both `MC04` and `MC12` obey a product mask with the shared static
`g3` surface `a=+0.3`.  The complete fixed-`|d|` arrangement therefore
contains all signed `g1`, `g2`, and `g3` chambers.  This checkpoint derives
those chambers over the full sourced energy interval rather than extending
the four selected slices by assumption.

- fixed `|d|`: `0.338281138367`;
- surface branch rows: `7826`;
- topology events: `10`;
- topology-stable `|s|` panels: `9`;
- energy chambers: `32`;
- reduction probes: `128`;
- chamber-aligned cubature cells: `32`;
- chambers active above the old `g1` zero crossing:
  `22`;
- maximum surface residual:
  `1.10111919582e-12`;
- maximum pair-reduction change:
  `6.6729254697e-15`;
- full-orbit fallbacks: `6`.

Decision: **FULL_FIXED_DECAY_PAIR_ORBIT_TOPOLOGY_DERIVED__RUN_CHAMBER_ALIGNED_ENERGY_SOFT_CUBATURE**.

Validation: **PASS**.

## Consequence

The next numerical step has an explicit unit-square map for every fixed-decay
energy/soft-angle chamber.  It must integrate finite regulators on those
cells and take the regulator limit after integration.  It must not truncate
the energy domain at the old `g1` zero crossing.

## Claim boundary

This is a complete topology and cubature-coordinate result at one fixed
decay angle.  It is not yet the finite-regulator volume integral, the
decay-angle integral, a full phase-space coefficient, local GR, or the full
MTS theory.
