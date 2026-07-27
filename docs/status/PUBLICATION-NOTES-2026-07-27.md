# Publication Notes - 2026-07-27

## Purpose

This update completes the previously unmerged July 24 publication branch and
extends the public research record through checkpoint `1266`. It preserves
successful derivations, failed controls, stopped calculations, topology
corrections, and the current claim ceiling.

## Scope

The established public offset is `3984`. Private checkpoints `5176-5250`
map to public checkpoints `1192-1266`. The new increment in this update is:

| Item | Count | Size |
|---|---:|---:|
| Checkpoint Markdown documents | 36 | 0.088 MiB |
| Checkpoint Python scripts | 37 | 1.363 MiB |
| Compact validation CSV files | 35 | 0.042 MiB |
| Hash-verified new checkpoint artifacts | 108 | 1.493 MiB |

Private checkpoint `5243` was deliberately stopped before integration and has
no compact validation CSV. Its public checkpoint document and source script
are included; the document explicitly blocks a corrected-integral claim.

## Apparent GitHub Truncation

The earlier branch was not missing Git objects. Before this update:

- the recursive GitHub tree contained `8,830` blobs;
- the local tracked-file count was also `8,830`;
- GitHub reported the recursive tree as `truncated=false`;
- the existing verifier passed the complete public range through `1230`.

The confusing part was the presentation layer: GitHub can cap ordinary folder
and pull-request file listings. The repository already had more than 1,000
entries in each of several flat artifact folders, and the pull-request file
view exposed only its first bounded page.

This update adds:

- `research-programme/catalogue/README.md`, with bounded direct-link shards;
- `docs/status/PUBLICATION-INVENTORY-2026-07-27.csv`, containing path, byte
  count, and SHA-256 for every published file except the inventory itself;
- `tools/build_publication_catalogue.py`, which regenerates both;
- `tools/verify_public_update_1266.py`, which verifies the range, source
  mapping, script compilation, validation rows, catalogue, and inventory.

## Included

- public checkpoints `1231-1266`;
- all matching Python scripts selected by the established private-ID rule;
- every available compact CSV/JSON validation artifact in that range;
- the fresh control-pilot failures and exact residue/classification results;
- the physical permutation-chart and outer-pole-subtraction derivations;
- the dynamic active-family atlas and bounded causal integration tests;
- the failed frozen-topology cubature;
- the reciprocal-projective Q03/Q05 topology rebuilds and corrected slices;
- the partial outer-impact calculation and explicit hold decision.

## Excluded

- virtual environments, `__pycache__`, and notebook caches;
- raw run folders, large arrays, logs, and temporary numerical caches;
- the multi-gigabyte local `functional_rg` source/cache tree;
- third-party source bundles and datasets;
- any statement that the partially corrected outer integral is final;
- any completed-`p8`, ultraviolet-completion, or empirical-replacement claim.

## Integrity

The range publisher hash-verified all `108` new copied artifacts. The
publication verifier requires:

- contiguous public checkpoints `1192-1266`;
- exact title mapping back to private checkpoints `5176-5250`;
- all `77` selected Python scripts to compile;
- all `74` compact ledgers to parse, with the deliberately retained failed
  gates confined exactly to private checkpoints `5216`, `5221`, `5240`,
  `5241`, and `5244`;
- only private checkpoint `5243` to lack a compact validation ledger;
- no forbidden runtime artifacts or checkpoint artifact above 5 MiB;
- catalogue shards of at most 250 links;
- an exact path, size, and SHA-256 match against the publication inventory;
- continued verification of the frozen checkpoint-`1192` protocol.

## Public Claim

The selected two-derivative local GR + Standard Model + Maxwell theorem
remains the strongest result. The new work improves the higher-operator
integration method and exposes a material topology correction, but the first
canonical MTS-specific crossed-`hhh` coefficient remains unresolved.
