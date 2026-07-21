# 5074 - central-anchor bidirectional-chain gate

Marker: `MTS_5074_CENTRAL_ANCHOR_BIDIRECTIONAL_CHAIN_GATE`.

Measured full-homotopy costs identify `A08` as the fixed central anchor. One
`A08` topology per event is propagated right to `A14` and left to `A00` using
the forward and reverse forms of the 5069 theorem.

Across eight events, all 112 non-anchor documents pass, including 64 reverse
edges and 45 transition edges. Maximum depth falls from 14 to 8. The eight full
anchors average `1.664 s` and never exceed `3.858 s`; all target content used in
the test is validation-only.

## Evidence

- Result: `source-intake/functional_rg/5074/central_anchor_bidirectional_chain_gate.json`
- Rows: `source-intake/functional_rg/5074/central_anchor_bidirectional_chain_rows.csv`
- Generator: `scripts/Y5_R2FR_5074_central_anchor_bidirectional_chain_gate.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5074_VALIDATION.csv`

Nineteen raw-history mismatches remain harmless net-zero quotient differences.
