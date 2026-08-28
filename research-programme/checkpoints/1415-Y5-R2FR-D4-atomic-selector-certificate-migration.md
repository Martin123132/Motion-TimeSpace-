# 5399 — D4 atomic selector-certificate migration

## Purpose

Checkpoint 5398 closes every one of the `5,841` source rows in the `15` completed v39 paths. Checkpoint 5399 installs those staged certificates without discarding the original calculation.

## Transaction

1. Require the 5398 staged-migration gate and primary revision v40.
2. Verify every live path still has its recorded v39 hash.
3. Copy every v39 path into `source-intake/functional_rg/5399/archive_v39_path_parts`.
4. Prepare and hash all staged temporary replacements.
5. Atomically replace each live path, then require its hash to equal the staged hash.
6. Change the run manifest to v40 only after every path replacement succeeds.

The operation is idempotent: an interrupted rerun accepts only a live original hash or its exact staged replacement, and it never overwrites a conflicting archive.

## v40 production rule

Future boxes begin with the complete parent-declared chart set. If interval arithmetic proves a positive representative-unit-modulus margin, the uniquely selected chart owns the closed box. Otherwise the evaluator retains the full finite chart union. Thus no mapped-cell midpoint state is assigned to an entire box.

## Claim boundary

This migration repairs selector ownership for completed regular-away paths and licenses continuation of v40 atlas production. It does not finish the atlas, take the regulator limit, close the event-local term, or establish any UV, local-GR, or full-MTS claim.

## Result

- Original v39 paths archived with matching hashes: `15/15`.
- Live paths matching their staged 5398 hashes: `15/15` (`5,891` rows).
- Primary and run manifest revision: `D4-deformed-contour-regular-away-W3-v40`.
- Downstream claims locked: **PASS**.
- Live selector-certificate migration: **PASS**.
- First bounded v40 resume: `3` accepted, `7` pending, maximum depth `8`, `resume_safe=true`.
