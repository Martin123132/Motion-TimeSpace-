# 5087 - finer removable-limit rejection

Marker: `MTS_5087_FINER_REMOVABLE_LIMIT_CERTIFICATE`.

The blocked `E020__S507603_N0000__A07__primary24` row was given exactly one
additional predeclared symmetric approach level, `3.90625e-6`. The existing
`1e-7` acceptance threshold was not changed.

The four-level result still fails: maximum directional convergence is
`1.3519152718372752e-7`, direction spread is
`1.0423781952676258e-7`, and the new level does not contract both old
diagnostics. The numerical removable-extension route is therefore rejected
for this row. No fifth level and no tolerance relaxation are authorized.

## Evidence

- Certificate: `source-intake/functional_rg/5087/finer_removable_limit_certificate.json`
- Failed gate: `source-intake/functional_rg/5087/E020_A07_primary24_finer_limit_gate.json`
- Generator: `scripts/Y5_R2FR_5087_finer_removable_limit_certificate.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5087_VALIDATION.csv`

The required successor is an algebraic local collision classification, not a
longer numerical limit ladder.
