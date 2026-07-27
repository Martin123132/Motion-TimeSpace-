# 5070 - canonical argument-chain constructor gate

Marker: `MTS_5070_CANONICAL_ARGUMENT_CHAIN_CONSTRUCTOR_GATE`.

Using one full `A00` anchor per event and the 5069 composition law, all 112
remaining `E040` argument topologies are recursively constructed across eight
events. The maximum depth is 14; 45 edges carry nonzero transition data; none
fails the reduced/rootwise kernel contract.

Eighteen documents differ from saved full topologies only in cancelling raw
path-history rows. The physical quotient is the rootwise net winding, not that
redundant history. Saved target documents are used only for validation.

## Evidence

- Result: `source-intake/functional_rg/5070/canonical_argument_chain_constructor_gate.json`
- Rows: `source-intake/functional_rg/5070/canonical_argument_chain_rows.csv`
- Generator: `scripts/Y5_R2FR_5070_canonical_argument_chain_constructor_gate.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5070_VALIDATION.csv`

Kernel equivalence, rather than raw-history equality, remains the next gate.
