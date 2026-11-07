# Publication notes: November 7, 2026

This is an owner-authorized public update of completed MTS research, prepared
from local completed-stage seals. The previous public main commit is
`fb59a16fb9f33dc6cdfaca87c23ff217a85dd0de` (September 21, 2026).
Existing scientific files and all earlier releases are preserved.

## Scope and evidence standard

- Selected completed-stage seals identify eligible sources. Every included
  payload must match a declared SHA-256 before copying and its committed Git
  blob must match the same length and hash after staging.
- A completed investigation may contain a negative result. Historical failed
  attempts inside sealed work are retained as failures, not relabelled passes.
- Current files that no longer match their selected seal are not published
  from that path. Their omission is explicit in the manifest/exclusion ledger.
- Untested relative-phase perturbation drafts, mutable global resume files,
  environments, rollback duplicates, third-party archives and binaries are
  excluded. No new physics calculations are performed for this release.
- Bulky numerical products stay local and have explicit manifest rows with
  the expected hashes from the scientific seals. Those omitted products are
  not newly rehashed in this publication pass. This is not a complete raw-data
  backup or a fully standalone reproduction archive.

## Protection against truncated listings

GitHub's web directory and diff views are not the source of truth for
completeness. The release uses two-level hash-sharded payload folders,
catalogue pages of at most 160 source rows, and a machine-readable manifest
index with hashed CSV parts of at most 4,000 rows each.
The new directory-entry ceiling is 256. No file is shortened to fit the UI.
Git tree inventories and full included-blob hashes are checked rather than
assuming that a browser listing, recursive API result or PR diff is complete.

The exporter checks that no original tracked path is deleted and that the
only modified pre-existing paths are the root README and `.gitattributes`.
The latter disables newline conversion on copied source bytes. The push is
to a new branch, followed by a checked merge; no force push is used.

## Use and reproduction

Start at the [package README](../../research-programme/updates/20261107/README.md).
Run `python tools/publish_verified_20261107.py --verify HEAD` from a checkout
to check committed payloads and navigation. This is a publication-integrity
test, not a rerun or independent mathematical proof of the research.

`python tools/publish_verified_20261107.py --restore NEW_DIRECTORY` reconstructs
included files under `post/` and `data/` in a fresh directory; it refuses an
existing destination. Research scripts retain their original machine paths
and dependencies. Restoring the snapshot does not make all scripts portable
or supply omitted numerical banks, observational catalogues or compilers.

Source snapshots may say "private" or "no GitHub": those statements describe
the original run, before this later explicit publication authorization. No
new licence or transfer of third-party rights is implied. External packages
and data retain their original licences; excluded dependencies are not
redistributed merely because a research script references them.
