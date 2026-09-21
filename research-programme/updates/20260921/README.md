# September 21: currents from the retained action

Source snapshots are byte-exact. Dates and “private/no GitHub” statements inside them describe their original runs, not this later authorized publication.

## Read first

- [source-intake/navier-stokes/20260914/annular-candidate-horizontal-shift-final-integrity.json](../../../research-programme/updates/20260921/files/4b/4b2da0883b59ee83-annular-candidate-horizontal-shift-final-integrity.json)
- [RESULTS-20260921-candidate-horizontal-shift-and-localized-current.md](../../../research-programme/updates/20260921/files/db/dbd5bdf65b3181f3-RESULTS-20260921-candidate-horizontal-shift-and-localized-current.md)
- [DERIVATION-20260921-candidate-horizontal-shift-and-localized-current.md](../../../research-programme/updates/20260921/files/be/bea3be2f432c0c21-DERIVATION-20260921-candidate-horizontal-shift-and-localized-current.md)
- [DERIVATION-20260921-horizontal-shift-step-size-refinement.md](../../../research-programme/updates/20260921/files/9a/9a0bbb95e3a6c497-DERIVATION-20260921-horizontal-shift-step-size-refinement.md)
- [DERIVATION-20260921-moving-source-localized-Legendre-current.md](../../../research-programme/updates/20260921/files/54/54f88d7ebf75b7cd-DERIVATION-20260921-moving-source-localized-Legendre-current.md)

## Complete inventory

[Bounded source catalogue](catalogue/README.md). [Machine-readable mapping](MANIFEST.csv). [Export counts](EXPORT-REPORT.json).

All declared seal paths are inventoried, including excluded historical raw arrays. Source scripts, derivations, JSON/CSV audit records and four recent numerical packages are published. This is not an all-data standalone rerun capsule: omitted arrays must be restored locally. Six original coarse failures and their separate successful refinement remain distinct.

Restore included source paths into a NEW directory with `python tools/publish_annular_20260921.py --restore DESTINATION`. Do not use the public hash-sharded directory as a runnable source tree. Local import dependencies are included; Python packages, omitted raw arrays, mutable resume and protected sibling seal dependencies are not supplied.

Verify committed bytes with `python tools/publish_annular_20260921.py --verify HEAD`. This checks Git blobs, all manifest entries, bounded directory counts, and local catalogue targets; it does not rerun the physics.
