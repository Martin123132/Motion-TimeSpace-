# 5069 - canonical-path signed-winding composition law

Marker: `MTS_5069_SIGNED_SEGMENT_WINDING_COMPOSITION_LAW`.

The missing transition law is the canonical path difference, not a naive
top-edge winding sum:

`W(target) = path-transport[W(source)] + W(reverse source vertical + regulator-floor horizontal + target vertical)`.

Pathwise labelled-root transport handles finite crossings, monodromy, and
projective infinity. The law certifies all 232 available cases: 120 epsilon
segments and 112 adjacent argument segments, including all 46 transition
cases. There are zero composition failures, zero endpoint-log error, and zero
source-representation spread.

## Evidence

- Result: `source-intake/functional_rg/5069/signed_segment_winding_composition_law.json`
- Rows: `source-intake/functional_rg/5069/winding_composition_rows.csv`
- Generator: `scripts/Y5_R2FR_5069_signed_segment_winding_composition_law.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5069_VALIDATION.csv`

This closes the topology-composition obstruction; it does not itself evaluate a
fresh physical observable.
