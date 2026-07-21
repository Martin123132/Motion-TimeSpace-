# 5045 - theorem-scope falsification and quarantine

Marker: `MTS_5045_THEOREM_SCOPE_FALSIFICATION_AND_QUARANTINE`.

## Finding

The 5041 exact-zero proof was implemented more broadly than it was proved. Its
independent arbitrary-precision witnesses cover exactly two families:

```text
direct:g1:minus_v / subtraction:decay:minus_u
direct:g1:plus_v  / subtraction:decay:plus_u
```

All eight original third-scramble repairs belong to those families and are
retained. None of the 372 fourth-scramble exact-zero rows belongs to them. The
broad guard also classified stable nonzero `g3` residues, reaching magnitude
`4172.69`, as zero. This is a genuine theorem-scope falsification, not a
tolerance dispute.

## Quarantine

The old fourth-scramble products and dependent 5042-5045 outputs were marked
non-claim pending restricted recomputation. No source data were deleted. The
manifest records paths, hashes, reasons, and replacement status.

## Evidence

- Audit: `source-intake/functional_rg/5045/theorem_scope_audit.json`
- Table: `source-intake/functional_rg/5045/theorem_scope_audit.csv`
- Manifest: `source-intake/functional_rg/5045/quarantine_manifest.csv`
- Generator: `scripts/Y5_R2FR_5045_theorem_scope_falsification_and_quarantine.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5045_SCOPE_VALIDATION.csv`

This checkpoint narrows a numerical lemma; it makes no `hhh`, GR, Newton,
Maxwell, or full-MTS claim.
