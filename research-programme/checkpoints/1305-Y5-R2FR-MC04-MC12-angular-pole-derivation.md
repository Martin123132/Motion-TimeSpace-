# 5289 — MC04/MC12 angular-pole derivation

## Why this checkpoint exists

The 5288 stored-node replay removed the newly derived `MC03/MC08` poles,
but the `A02_S02_D01` and `A02_S02_D02` energy rules remained unstable.
Their paired lower-endpoint coefficients cancel, so the residual could
not honestly be assigned to the endpoint. A fresh geometric scan finds
the omitted `MC04/MC12` angular pole family.

## Result

- owner poles scanned: `4`;
- owner exact-active poles: `4`;
- owner material poles: `2`;
- owner plus mirror material poles:
  `4`;
- maximum pointwise `MC04 + MC12` antisymmetry residual:
  `0`;
- maximum selected residue-fit residual:
  `3.97137615255e-05`;
- validation passed: `True`.

The `MC12` residues are not guessed. They are transported from `MC04`
with sign `-1` only after a pointwise two-regulator antisymmetry audit.

## Decision

`CERTIFY_MC04_MC12_ANGULAR_POLES__RUN_ALL_FAMILY_COMBINED_SUBTRACTION`

This closes the second promoted-pole inventory. It does not yet establish
energy, angular, full phase-space, UV, local-GR, or full-MTS convergence.
