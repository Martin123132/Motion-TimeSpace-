# 5113 - S507614 A00 event-local recoil resolution

## Failure examined

The `E020__S507614_N0000__A00__primary24` control job exposed two unstable
cross-additive recoil rows. They could not inherit a zero from the rejected
5084 family theorem, so each direct component was recomputed independently at
60 decimal digits on the locked relative/global radius grid.

## Result

The two rows were:

- `direct:g1:plus_u` / `subtraction:decay:plus_v`, maximum direct-only
  magnitude `2.520250968345786e-30`;
- `direct:g2:minus_v` / `subtraction:decay:plus_v`, maximum direct-only
  magnitude `1.0005805172591163e-32`.

Both are event-local numerical zeros under the existing `1e-20` gate. They
are not promoted into a symbolic family theorem. The exact registry grows
from nine to eleven rows and remains keyed by job, event, argument, pair,
ownership, chamber and root.

The blocked job was replayed using only these exact certificates and
converged. Stable nonzero rows remained untouched.

## Status

- exact rows resolved: `2/2`;
- generalized recoil-zero theorem: still rejected;
- event-local registry version: `v2`, eleven rows;
- validation: `7/7` passed;
- full control matrix and MTS claim: not complete and not allowed.

## Outputs

- `scripts/Y5_R2FR_5113_S507614_A00_event_local_recoil_resolution.py`
- `source-intake/functional_rg/5113/S507614_A00_event_local_recoil_resolution.json`
- `source-intake/functional_rg/5113/event_local_direct_zero_registry_v2.json`
- `source-intake/functional_rg/5113/S507614_A00_direct_component_audit.csv`
- `source-intake/mts_residuals/P8_Y5_BRR545_5113_VALIDATION.csv`
