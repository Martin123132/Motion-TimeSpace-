# Publication Notes - 2026-07-21

## Scope

This update publishes the compact research record created after the checkpoint-516 public merge.

| Item | Count | Size |
|---|---:|---:|
| Checkpoint Markdown documents | 658 | 7.480 MiB |
| Python scripts | 851 | 22.938 MiB |
| Compact residual CSV/JSON artifacts | 5,404 | 15.466 MiB |
| Total copied research artifacts | 6,913 | 45.884 MiB |

The source range is private checkpoint `4501` through `5175`. Public checkpoint filenames subtract the established offset `3984`, producing public checkpoint `517` through `1191`. Document titles, script names, row IDs, and residual filenames retain the original private checkpoint numbers for provenance.

Seventeen checkpoint numbers in the source interval have no Markdown checkpoint file. Their corresponding public numbers remain absent rather than being fabricated or silently renumbered.

## Included

- checkpoint derivations, failed routes, red-team gates, and decision ledgers;
- source Python scripts associated with the interval;
- compact CSV/JSON residuals, validation tables, and source registers;
- updated public status, claim ceiling, gate map, and reading order;
- a reusable allowlisted synchronization script that refuses to run on `main` or `master`.

## Excluded

- the local `functional_rg` tree (`15,701` files, approximately `815.787 MiB` for this interval), which contains source caches, third-party bundles, PDFs, logs, arrays, and large generated products;
- raw run directories, virtual environments, notebooks, caches, and compiled Python files;
- large `NPZ`, `NPY`, HDF5, FITS, database, and pickle products;
- any Git history rewriting or direct update to the protected default branch.

Some historical documents contain absolute local paths. They are retained as provenance records and are not portable execution instructions.

## Integrity

The publication script performs a dry run before copying, applies an extension and size allowlist, checks destination collisions, and verifies every copied artifact against its source with SHA-256. The applied snapshot verified all `6,913` copied files.

The publication remains a work-in-progress research snapshot. Generated rows marked `nonclaim`, `conditional`, `blocked`, or `valid_for_claim=false` retain those meanings after publication.
