# Publication Notes - 2026-09-09

## Purpose

This branch extends the public MTS audit from the default branch's private
checkpoint `5417` / public checkpoint `1433` through the latest fully sealed
source boundary at `2026-09-09 23:29:54 BST`. It does not merge or modify the
default branch.

## Included scope

- Available private checkpoint documents `5418-5514`, mapped by the
  established offset `3984` to public documents `1434-1530`.
- Their matching `Y5_R2FR_*.py` scripts and curated validation/residual
  artifacts from `source-intake/functional_rg/`.
- Reader-facing `DERIVATION-*`, `RESULT-*`, and `RESULTS-*` notes dated after
  the previous public upload, plus the D4 overview draft.
- The complete byte-exact own-result package for `annular-second-metric-source`:
  `591/591` checks, `18` saved states, `6` controls.
- The complete byte-exact own-result package for `annular-spatial-clock-energy`:
  `360/360` checks, `18` saved states, `6` controls.
- A reproducibility capsule for the latest spatial-clock-energy seal, preserving
  all `1,256` hashed input entries and `415` hashed output entries under their
  original source-relative paths, with duplicate paths retained in the capsule
  manifest's role map.

## Counts and integrity

The generated `PUBLICATION-MANIFEST-2026-09-09.csv` is the authoritative
source-to-public mapping. Its `source_path` values are relative to the local
post-checkpoint source root recorded in the verification report, or begin with
`GENERATED/` for publication-authored documents. It records every included
file's published path, byte count, and SHA-256 digest. The capsule's role-level
closure map is `research-programme/reproducibility/20260909/CAPSULE-MANIFEST.csv`.
The public post-export report is
`docs/status/PUBLICATION-VERIFICATION-2026-09-09.json`.

The export preserves complete bytes for every included file. Imported artifacts
and the capsule are marked `-text` in `.gitattributes` because this checkout
has `core.autocrlf=true`. Git blobs are verified independently after commit;
the remote branch ref is checked after push. New catalogue and export
directories are bounded below 1,000 entries; preserved legacy flat directories
are not represented as below that threshold.

## Explicit exclusions and omissions

- The paused/incomplete private checkpoint `5515` is excluded;
  no part of its seeded frontier or mutable resume is treated as complete.
- The mutable root `CURRENT_LOCAL_RESUME.md`,
  `LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md`, and
  `REVIEW-20260904-RN-and-maths-transfer.md` are excluded.
- Private backup, galaxy, maths-exploration, RN, and unrelated repositories
  are excluded.
- Functional-RG `work-v1`, `job-cache`, `rung-cache`, and `runs` products,
  logs, files over 5 MiB, and other raw production products are excluded from
  the curated artifact export. The selected compact files are preserved under
  their checkpoint directories; omitted raw products are not silently counted
  as published.
- Virtual environments, bytecode, credentials, tokens, `.env` files,
  personal attachments, third-party datasets, and caches are excluded.

## Reproducibility boundary

The standalone annular folders above are complete byte-exact own-result
packages, but their integrity records refer transitively to a wider source
closure. The capsule closes the latest spatial-clock-energy seal's declared
`1,256` input and `415` output entries: `1,409` unique source paths,
`154,538,343` bytes when role duplicates are counted, and no individual file
over 5 MiB. The capsule also includes the seal, immutable resume snapshot, and
five runtime-dependency files required to import the derive graph, for `1,415`
unique capsule files. All declared closure paths and runtime dependencies were
found locally and matched their declared SHA-256 values before export. The
derive/import closure is therefore present, but the seal phase is not
self-contained: the mutable `CURRENT_LOCAL_RESUME.md` and sibling
`formalization-workbench` path checked by the sealing script are intentionally
omitted. These exact omissions block a standalone seal rerun. The capsule does
not include third-party Python runtime packages or prove the scientific claims;
use its `README.md` for the source-root restore/run contract.

The dated catalogue README and shards are navigation indexes rather than
source artifacts; they are intentionally outside the inventory to avoid a
self-referential catalogue hash. Their links cover every inventory row.

## Claim ceiling

The new annular material is published as conditional derivation and audit
evidence only. Spatially commuted energy without higher clock time derivatives
is a new finding, but its paired interface estimate, equivalence to the older
`H` norm, uniform evolution, stability, and black-hole completion remain
unproved. No unresolved mathematics is presented as established physics.
