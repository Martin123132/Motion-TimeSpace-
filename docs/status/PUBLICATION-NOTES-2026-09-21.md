# Publication notes — 21 September 2026

## Boundary

Authorized public update of `Martin123132/Motion-TimeSpace-`, based on main
`bf2448465` and the COMPLETE local seal
`source-intake/navier-stokes/20260914/annular-candidate-horizontal-shift-final-integrity.json`.
No old research file is removed. The working physics tree and protected
`formalization-workbench` are not rewritten by the exporter.

## Exact inventory, not a directory-list approximation

`research-programme/updates/20260921/MANIFEST.csv` inventories every declared
input/output path in that seal, the seal itself, the new dated reader notes
and any statically discoverable local Python import dependencies. Each row
records original source-relative path, public path (if included), bytes,
SHA-256, disposition and reason. Hash-identical earlier public files are
referenced rather than duplicated. Multiple source paths may legitimately
share one public blob.

The exporter checks all declared hashes against local files, including arrays
it does not copy. Included new artifacts are copied byte-for-byte into
hash-sharded folders, with `-text` attributes to prevent newline conversion.
The verifier independently reads committed Git blobs and checks every
included manifest row. New catalogue shards have at most 200 entries and
new payload directories remain below 1,000 entries. GitHub's UI can still
limit a large PR diff; that display is not used as the completeness test.

## Included

- All non-NPZ source artifacts in the declared seal lineage: derivations,
  executable sources, JSON/CSV audit records, immutable resume snapshots,
  logs/markers owned by that lineage, and preserved failed attempts.
- New dated derivation/result notes through September 21.
- Numerical arrays from the independent Ward-source, localized Legendre
  current, horizontal-shift current and finite-step refinement packages.
- Prior artifacts already on main, referenced by exact matching SHA-256.
- An export/restore/committed-blob verifier, bounded navigation catalogue
  and reader-facing status note.

`EXPORT-REPORT.json` gives exact counts and explicitly records historical
syntax failures found during static import scanning. Those scripts remain
unchanged as failed evidence, not advertised as successful entry points.

## Excluded explicitly

Historical numerical NPZ arrays outside the four named current packages
remain local. They constitute most of the roughly 11 GB source closure;
each omission has its own manifest row, byte count and hash. There is no
silent clipping of their bytes and no invented public download location.

The incomplete D4 5515 frontier, mutable top-level resume, unrelated private
repositories, virtual environments, credentials and third-party source/data
caches are not part of this release. The source hierarchy under
`navier-stokes` is an inherited directory name, not an endorsement or
independent confirmation of a claimed Millennium-problem solution.

## Restore and validation limits

Run `python tools/publish_annular_20260921.py --restore NEW_DIRECTORY`
to reconstruct all included source-relative paths. It refuses an existing
destination. Missing historical arrays still prevent some full reruns; the
manifest is authoritative about that. Python packages, mutable resume and
protected sibling paths required by historical sealing scripts are separate
runtime prerequisites. The payload is not advertised as a standalone full
reproduction or a laptop backup.

Run `python tools/publish_annular_20260921.py --verify HEAD` to verify
committed included bytes and navigation. It does not rerun expensive physics.
Scientific failures and their subsequent refinements remain separate records.
The dated source documents' original “private/no GitHub” language describes
their execution time; this later publication is independently authorized.

Work after this snapshot continues locally and is not automatically pushed.
