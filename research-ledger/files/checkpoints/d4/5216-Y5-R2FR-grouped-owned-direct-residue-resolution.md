# 5216 - Grouped owned-direct residue resolution

## Problem

The transport-repaired `S521509/E040/A00` topology exposed three
unstable direct-only catalog rows. Two rows contain two collision
pairs at one relative root; the old on-demand classifier only
accepted one pair.

## Derived rule

Linearity of the iterated contour integral permits each collision
pair with exactly one chamber-owned direct pole to be evaluated
separately. Their residues are then summed point-by-point on the
same relative/global contour grid. No pole is deleted and no
double-precision tolerance is widened.

## Result

- Resolved grouped rows: `1/3`.
- Event-local replacement rows: `3`.
- Validation: `7/8`.
- Current checkpoint-5215 scale decision: `not allowed`.
- A new fresh run with this classifier predeclared is required.

## Claim boundary

This is an event-local numerical resolution on an outcome-exposed
development event. It does not determine the MTS two-loop
coefficient and does not alter the exact checkpoint-5211
GR+Lambda+SM+Maxwell truncation.

## Evidence

- Precision lock: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5216\grouped_owned_direct_precision_lock.json`
- Extraction: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5216\S521509_E040_A00_catalog_extraction.json`
- Audit: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5216\S521509_E040_A00_grouped_direct_audit.json`
- Replacement registry: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5216\event_local_grouped_direct_replacements.json`
- Validation: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_5216_VALIDATION.csv`
