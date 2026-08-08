# 5115 - general on-demand owned-direct residue classifier

## New collision class

`E020__S507615_N0000__A01__primary24` failed on the same-source,
opposite-ownership pair `direct:g2:minus_v` / `direct:g2:plus_v` in physical
chamber 1. It was outside checkpoint 5114's cross-additive scope. The existing
double-precision outward-contour repair did not converge and was not relaxed.

## Direct-component result

The chamber-owned direct component was evaluated at 60 decimal digits on
three relative radii and two global radii. The result is the stable nonzero

`-19.942056041962328 + 0.4064000175315503 i`,

with maximum absolute spread `1.0515297056590613e-9`, approximately
`5.27e-11` relative to its magnitude. The contribution is therefore retained;
it is not converted to zero.

## Generalized numerical scope

The on-demand classifier now covers only two explicitly derived scopes:

1. cross-additive rows with exactly one owned direct `g1/g2` pole;
2. same-source direct `g1/g2` `minus_u/plus_u` or `minus_v/plus_v` pairs with
   opposite ownership, evaluated in the physical owning chamber.

All calculations remain source separated and event local. Unknown collision
classes, unstable values and failed precision tests still fail closed. The
blocked job converged after replay while preserving the nonzero residue.

## Status

- same-source stable nonzero: derived numerically and retained;
- contour tolerances: unchanged;
- broad holomorphy theorem: still rejected;
- validation: `5/5` passed;
- full MTS claim: not allowed.

## Outputs

- `scripts/Y5_R2FR_5115_general_on_demand_owned_direct_residue_classifier.py`
- `source-intake/functional_rg/5115/general_on_demand_owned_direct_classifier_gate.json`
- `source-intake/functional_rg/5115/S507615_A01_same_source_direct_audit.csv`
- `source-intake/mts_residuals/P8_Y5_BRR545_5115_VALIDATION.csv`
