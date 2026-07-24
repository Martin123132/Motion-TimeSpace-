# Project Map

## Main Public Entry Points

- `README.md` gives the public overview.
- `CLAIM_CEILING.md` states the current claim boundary.
- `docs/status/STATUS-2026-07-24.md` gives the current status snapshot.
- `docs/status/PUBLICATION-NOTES-2026-07-24.md` records the exact update scope and exclusions.
- `docs/theory-gates/LOCAL-GR-NEWTON-GATES.md` gives the main route from MTS toward GR/Newton.

## Research Programme

- `research-programme/checkpoints/` contains numbered derivation attempts, scorecards, red-team ledgers, and promotion gates. The public sequence currently runs through checkpoint `1230`.
- `research-programme/protocols/1192/` preserves the machine-readable freeze record and now contains the complete compact 12-seed outcome.
- `research-programme/scripts/` contains the scripts used to generate many checkpoint artifacts.
- `research-programme/source-intake/mts_residuals/` contains compact CSV/register artifacts used by the residual and theorem-gate workflow.

## Current Derivation Thread

The July 24 update refreshes checkpoint `1192` and extends the public record
through checkpoint `1230`. The most useful new milestones are:

- `research-programme/checkpoints/1192-Y5-R2FR-predeclared-paired-high-mode-seed-ensemble.md` - completed frozen 12-seed metric-split result.
- `research-programme/checkpoints/1194-Y5-R2FR-exact-2PI-Schur-Ward-Vlasov-subtraction-and-Gaussian-residual-stress-no-go.md` - exact Schur/Ward reduction and Gaussian residual-stress no-go.
- `research-programme/checkpoints/1203-Y5-R2FR-canonical-local-parent-action-Hessian-source-residue-and-scale-setting-theorem.md` - canonical local action and scale-setting theorem.
- `research-programme/checkpoints/1204-Y5-R2FR-relational-clock-scalar-no-go-minimal-coframe-parent-and-Fierz-Pauli-selection-theorem.md` - scalar-clock no-go and minimal coframe route.
- `research-programme/checkpoints/1207-Y5-R2FR-O4-FLRW-tensor-nondegeneracy-order-reduction-and-cosmological-safety-theorem.md` - higher-derivative tensor gate.
- `research-programme/checkpoints/1211-Y5-R2FR-matched-joint-CMB-informed-parent-refit-and-physical-sound-horizon-gate.md` - matched parent-scalar cosmology robustness fit.
- `research-programme/checkpoints/1213-Y5-R2FR-universal-gap-cross-arena-compatibility-and-route-separation-theorem.md` - cosmology/galaxy mass-scale route separation.
- `research-programme/checkpoints/1217-Y5-R2FR-source-complete-coframe-variation-full-PPN-calibration-and-local-state-silence-theorem.md` - source-complete coframe and full PPN result.
- `research-programme/checkpoints/1219-Y5-R2FR-one-canonical-translation-gauge-parent-action-cross-coupling-and-branch-reduction-theorem.md` - one common parent functional.
- `research-programme/checkpoints/1224-Y5-R2FR-common-minimal-motion-trajectory-canonical-Z-quotient-absolute-scale-covariance-and-local-GR-selection.md` - common selected motion trajectory.
- `research-programme/checkpoints/1227-Y5-R2FR-selected-trajectory-exact-GR-Maxwell-consistent-truncation-universal-source-and-matched-GRSM-excess-theorem.md` - exact selected two-derivative GR+SM+Maxwell branch.
- `research-programme/checkpoints/1228-Y5-R2FR-fresh-crossed-hhh-two-stratum-pilot.md` - first fresh nonclaim crossed-`hhh` coefficient pilot.
- `research-programme/checkpoints/1229-Y5-R2FR-source-separated-additive-cluster-Cauchy-zero-theorem.md` - exact guarded residue-zero theorem.
- `research-programme/checkpoints/1230-Y5-R2FR-A00-identical-graviton-permutation-control-variate.md` - current coefficient-free variance-control theorem.

Public checkpoint filenames use an offset sequence; document titles and
generated artifact names retain their original private IDs. The established
offset is `3984`, so private `5176-5214` maps to public `1192-1230`.

## Data Policy

- Large raw datasets are not committed.
- Generated run folders are not committed.
- The local `functional_rg` source/cache tree is not committed.
- Virtual environments are not committed.
- Reproducibility notes, scripts, compact source-intake ledgers, and validation CSVs are kept where they help audit the logic.

## Archive

Older repository material is preserved under:

```text
archive/legacy-pre-formalization-2026-06/
```

This archive is kept for provenance. It should not be read as the current claim state of the project.
