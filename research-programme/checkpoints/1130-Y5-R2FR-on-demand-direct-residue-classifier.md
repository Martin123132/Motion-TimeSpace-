# 5114 - on-demand direct-residue classifier

## Motivation

The next failure, `E020__S507614_N0000__A01__primary24`, repeated the same
kind of cross-additive ambiguity. Manually adding a checkpoint for every
future row would only catalogue failures. This checkpoint therefore converts
the 5112 source-separated calculation into a fail-closed on-demand numerical
classifier.

## Classifier contract

The fallback is permitted only when a cross-additive collision has exactly
one owned `direct:g1` or `direct:g2` pole. It evaluates the direct component
alone at 60 decimal digits with 24 relative and 24 global nodes on two locked
radius scales. It may return:

- `EVENT_LOCAL_ARBITRARY_PRECISION_ZERO` below the locked zero gate;
- `STABLE_DIRECT_COMPONENT_NONZERO` when the radius-grid values agree;
- unresolved, which leaves the kernel fail closed.

The classifier cannot infer a symbolic theorem from labels or suppress a
stable contribution.

## Witness and replay

The A01 row has maximum direct-only magnitude
`1.7040731418866509e-25` and is an event-local zero. The registry grows once,
to twelve rows. The existing 5112 outer witness
`31.01294678732344 - 0.254009009904149 i` verifies that the stable-nonzero
branch remains live. The A01 job then converged on replay.

## Status

- cross-additive on-demand classifier: authorized;
- stable-zero and stable-nonzero outcomes: both supported;
- unresolved outcome: fail closed;
- validation: `6/6` passed;
- full MTS claim: not allowed.

## Outputs

- `scripts/Y5_R2FR_5114_on_demand_direct_residue_classifier.py`
- `source-intake/functional_rg/5114/on_demand_direct_residue_classifier_gate.json`
- `source-intake/functional_rg/5114/event_local_direct_zero_registry_v3.json`
- `source-intake/functional_rg/5114/S507614_A01_direct_component_audit.csv`
- `source-intake/mts_residuals/P8_Y5_BRR545_5114_VALIDATION.csv`
