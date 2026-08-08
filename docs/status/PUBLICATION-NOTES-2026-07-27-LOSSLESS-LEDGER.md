# Publication Notes - 2026-07-27 Lossless Ledger

## Purpose

This follow-up fixes the practical completeness problem created by a very
large flat research corpus. The earlier curated public sequence was
hash-consistent, but it did not contain every private-sequence artifact, and
GitHub's folder and pull-request views could hide entries beyond their display
limits. A long Windows checkout path could also fail to materialize legacy
files even when their Git objects had downloaded.

The update therefore keeps the readable curated sequence and adds a separate,
byte-exact, physically sharded research ledger.

## Curated Increment

The established offset remains `3984`:

| Private checkpoint | Public checkpoint | Result |
|---:|---:|---|
| `5251` | `1267` | Complete order-5 backbone paired-transport rebuild |
| `5252` | `1268` | Full corrected order-9 cubature; locked outer gates fail |

Both checkpoint documents, both source scripts, and both compact validation
ledgers are copied exactly into the established public locations.

## Lossless Ledger Scope

`research-ledger/` contains:

| Category | Files | Bytes |
|---|---:|---:|
| Top-level checkpoint/support files | 5,239 | 72,285,641 |
| Python/source scripts | 5,578 | 167,703,174 |
| Compact residual/register files | 46,385 | 121,455,576 |
| Selected run evidence (`5250`-`5252`) | 242 | 35,699,500 |
| **Total** | **57,444** | **397,143,891** |

The ordered aggregate manifest digest is:

```text
2f9a19087b892121d7219d885d090cfd69dedf26a448594db6abe3dedd288dc0
```

All `5,577` Python files compile as source. The credential-pattern scan found
zero publish-blocking rows.

## Anti-Truncation Design

- Files are placed in stable two-character hash buckets.
- No physical directory may exceed `500` entries.
- Every catalogue shard has at most `250` direct links.
- Every manifest shard has at most `500` rows.
- Each row records the original source-relative path, published path, byte
  count, and SHA-256 digest.
- `tools/build_lossless_research_ledger.py --verify-only` re-hashes every
  committed ledger file and rejects missing, extra, short, or altered files.
- A second fresh clone with `core.longpaths=true` is required after pushing;
  its commit tree and aggregate ledger digest must match the local branch.

## Exclusions

- virtual environments and bytecode caches;
- the remaining multi-gigabyte `functional_rg` run/cache tree;
- third-party datasets and source bundles outside `post-checkpoint-work`;
- any interpretation that a published historical attempt is thereby promoted.

The root `CLAIM_CEILING.md` remains controlling.

## Current Physics Boundary

All nine order-9 nodes now use the corrected reciprocal-projective transport,
but order `3 -> 5`, order `5 -> 9`, and degree `5-8` tail gates fail. The
update publishes that negative result exactly; it does not claim the first
MTS-specific crossed-`hhh` coefficient.
