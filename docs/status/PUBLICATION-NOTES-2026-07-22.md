# Publication Notes - 2026-07-22

## Purpose

This small follow-up publicly timestamps the frozen paired MTS/CDM ensemble before confirmatory seeds 2-12 are inspected. It is a preregistration and audit update, not a model-preference claim.

## Scope

Private checkpoint `5176` maps to public checkpoint `1192` under the established offset of `3984`.

| Item | Count | Size |
|---|---:|---:|
| Checkpoint Markdown documents | 1 | 0.003 MiB |
| Checkpoint Python scripts | 2 | 0.047 MiB |
| Compact validation CSV files | 1 | 0.006 MiB |
| Curated protocol and seed-1 machine-readable files | 14 | 0.021 MiB |
| Protocol snapshot README | 1 | less than 0.002 MiB |
| Portable snapshot verifier | 1 | less than 0.004 MiB |
| Total research artifacts | 20 | approximately 0.083 MiB |

The update also refreshes the README, project map, claim ceiling, and dated status documents.

## Included

- the frozen 12-seed schedule and symmetric decision rule;
- the seed-1 nonclaim result and explicit pilot exclusion;
- the ensemble runner and independent freeze verifier;
- compact validation output showing all current checkpoint gates pass.
- a curated machine-readable snapshot of the protocol, seed schedule, freeze record, source hashes, aggregate tables, and seed-1 outputs.
- a standard-library verifier for the compact public snapshot.

## Excluded

- phase caches, arrays, logs, and approximately 73 MiB of generated seed-1 run products;
- the remainder of the local `functional_rg` source/cache tree;
- third-party source bundles and datasets;
- any statement of MTS or CDM preference.

## Integrity

The publication helper copied four allowlisted checkpoint artifacts and verified all four destination files against their private sources with SHA-256. Fourteen additional compact protocol/result files were copied byte-for-byte and independently hash-checked. The checkpoint records the protocol and runner hashes, all rows remain `valid_for_claim=false`, and the protected formalization-workbench digest remains `b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.

The remaining confirmatory sequence must be run without changing the frozen protocol, runner, seed order, estimands, or inference rule.
