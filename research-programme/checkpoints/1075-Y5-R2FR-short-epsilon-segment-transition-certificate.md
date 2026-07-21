# 5059 - short epsilon-segment transition certificate

Marker: `MTS_5059_SHORT_EPSILON_SEGMENT_TRANSITION_CERTIFICATE`.

An a-priori certificate now tracks every opposite-ownership collision root and
the chamber endpoints only along the short `E040 -> E020` segment. It is
anchored to the saved `E040` endpoint logs and compares 8-, 16-, and 32-step
transition signatures.

Across all 120 pairs, the certificate has zero classification errors and flags
only `S503402_N0000/A06`, where two converged contour transitions occur. All
other rows have a zero transition signature. Maximum root and boundary
projective steps are `0.0251` and `0.0135`, below the locked `0.1` limit. The
production 8/16 certificate costs a mean `0.277 s` per argument.

## Evidence

- Result: `source-intake/functional_rg/5059/short_epsilon_segment_transition_certificate.json`
- Rows: `source-intake/functional_rg/5059/epsilon_segment_certificate_rows.csv`
- Generator: `scripts/Y5_R2FR_5059_short_epsilon_segment_transition_certificate.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5059_VALIDATION.csv`

The full `E020` classes are validation labels only; they are not read by the
certificate construction.
