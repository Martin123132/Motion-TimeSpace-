# 5048 - integrated restricted fourth-scramble repair

Marker: `MTS_5048_INTEGRATE_RESTRICTED_FOURTH_SCRAMBLE_AND_REAUDIT`.

All 45 contaminated fourth-scramble jobs and all 45 kernel files were backed up
and hash-verified before the restricted scratch replacements were applied. The
live 5040 matrix is now `378/378`, with zero failed and zero unconverged jobs.

The corrected nested/sample-0 SD ratios are
`(0.935,0.657,0.632,0.759,0.673)`. The nested/equal-cost-independent halfwidth
ratios are `(1.780,1.251,1.203,1.445,1.281)`, so the original design decision
to prefer additional independent scrambles remains, now for a stronger reason.
Target and imaginary equivalence remain open `5/5`; contraction is supported
for `3/5`. This is matrix repair, not production precision.

## Evidence

- Integration: `source-intake/functional_rg/5048/restricted_fourth_scramble_integration.json`
- Manifest: `source-intake/functional_rg/5048/staged_replacement_manifest.json`
- Backup: `source-intake/functional_rg/5048/live_backup_before_restricted_recompute`
- Generator: `scripts/Y5_R2FR_5048_integrate_restricted_fourth_scramble_and_reaudit.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5048_VALIDATION.csv`
