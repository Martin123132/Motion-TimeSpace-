# Annular Spatial-Clock-Energy Reproducibility Capsule

This capsule is a byte-preserving source-root slice for the sealed
`annular-spatial-clock-energy` result. It contains every path named by the
seal's `inputs` and `outputs` maps, plus the seal and its immutable resume
snapshot. The role-level mapping is in `CAPSULE-MANIFEST.csv`; repeated paths
are retained there when an artifact is both an input and an output.

## Restore contract

Treat this directory as the original `post-checkpoint-work` root. Keep the
relative layout unchanged: scripts remain under `scripts/`, source-intake
artifacts remain under `source-intake/`, and root derivation notes remain at
the capsule root. Inspect a copied script from this directory, for example:

```powershell
Set-Location C:\path\to\20260909
python -B scripts\derive_annular_spatial_clock_energy_20260909.py --help
```

The capsule is intended for inspection and rerun preparation, not an automatic
re-execution of the sealed jobs. The derive command is for a fresh output
workspace; an existing sealed output folder intentionally makes its creation
fail with `exist_ok=False`. Do not delete or overwrite saved evidence to rerun
it. Install the required compatible Python runtime packages separately; they
are not part of this source closure. The seal's own results are conditional
finite-dimensional evidence. The paired
interface/Gram-residual estimate, equivalence to the older `H` norm, uniform
spatial evolution, stability, and black-hole/horizon completion remain open.

## Integrity

The seal declares `1,256` input entries and `415` output entries. They resolve
to `1,409` unique local source paths and `154,538,343` bytes when role
duplicates are counted. No included source file exceeds 5 MiB. The capsule
manifest records declared and observed SHA-256 values; the publication
verification report separately checks the committed Git blobs and pushed ref.
