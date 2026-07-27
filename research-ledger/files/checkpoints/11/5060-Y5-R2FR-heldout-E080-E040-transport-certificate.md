# 5060 - held-out E080-to-E040 transport certificate

Marker: `MTS_5060_HELDOUT_E080_TO_E040_TRANSPORT_CERTIFICATE`.

The 5059 rule was tested on a different epsilon interval and additional event
rows that were not used to select the `E040 -> E020` result. The held-out matrix
contains 84 pairs across six events.

It independently contains one topology change,
`S503403_N0000/A06`. The certificate detects that transition and sends it to
fallback. All other 83 rows are transported, and all 83 reproduce the full
`E040` numerical signature exactly. There are no false negatives, conservative
fallbacks, failed transports, or unconverged transition signatures.

## Evidence

- Result: `source-intake/functional_rg/5060/heldout_e080_to_e040_transport_certificate.json`
- Rows: `source-intake/functional_rg/5060/heldout_e080_to_e040_rows.csv`
- Generator: `scripts/Y5_R2FR_5060_heldout_e080_to_e040_transport_certificate.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5060_VALIDATION.csv`

This validates the transport/fallback decision rule outside its initial epsilon
interval; it does not validate MTS physics.
