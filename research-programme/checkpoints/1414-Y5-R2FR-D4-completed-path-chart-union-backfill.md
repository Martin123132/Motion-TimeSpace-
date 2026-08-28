# 5398 — D4 completed-path chart-union backfill

## Purpose

Checkpoint 5397 proves the finite selector-union inequality and exercises both declared MC04 charts on every observed selector-transition class. The remaining migration debt is concrete: checkpoint 5396 has `15` completed v39 path files, some of whose rows were enclosed with only the midpoint-selected chart.

Checkpoint 5398 recertifies those exact closed boxes by either of two rigorous routes: a closed selector-role margin, or the full finite chart union. It stages replacements under `source-intake/functional_rg/5398/staged_path_parts`; it never edits the live 5396 path files.

## Closed selector-margin route

The 5279 selector is explicit: use the representative chart when `|R_rep|>=1` and the reciprocal chart when `|R_rep|<1`. The representative root is the sourced rational function already evaluated by `expanded_geometry`. On each deformed closed path box, interval arithmetic encloses `|R_rep|`. A positive lower margin

\[
  \delta_B=\begin{cases}
  1-\sup_B|R_{rep}|,&\text{source role reciprocal},\\
  \inf_B|R_{rep}|-1,&\text{source role representative}
  \end{cases}>0
\]

proves the old chart owns the entire box. Such a row needs no second-chart computation. Ambiguous boxes are bisected; any box that still lacks a positive margin falls back to the full chart-union route below.

## Backfill rule

For every old accepted box `B`, retain its already certified v39 chart bound and compute a closed enclosure for every missing parent-declared chart. If `C_old` is the certified source set and `C_new` the missing set, then

\[
  |I_c(p)| \le B_c(B), \qquad p\in B,\quad c\in C_{old}\cup C_{new}.
\]

The runner uses the conservative selector-independent sum

\[
  |I_{\sigma(p)}(p)| \le \max_{c\in C} B_c(B)
  \le \sum_{c\in C} B_c(B),
\]

so no previously certified chart is recomputed or silently weakened. On a bisected old box, its parent supremum remains a valid bound on each child and is rescaled only by the child's exact path-parameter area. If a missing chart does not close, the runner bisects the box and preserves its exact total area.

Terms with only one parent-declared chart are byte-preserving passthroughs. Terms with two charts are evaluated rather than relabelled.

## Gates

- Keep all live 5396 path hashes byte-identical.
- Preserve each path's total parameter area.
- Require every staged row either to contain the complete declared chart set or to carry a positive closed interval selector-role margin for its sole source chart.
- Preserve the existing claim boundary: regular-away deformation and finite-box bounds may remain true, while event-local, full-W3, UV, local-GR, and full-MTS claims remain false.
- Authorize only a later atomic migration after every staged path completes.

## Claim boundary

This is an executable recertification, not a diagnostic inventory. A complete pass repairs the selector-transition ownership issue for the work already computed, but does not itself overwrite 5396, finish the remaining regular-away atlas, remove the regulator, or establish a UV, local-GR, or full-MTS result.

## Result

- Source paths: `15/15`; source rows: `5,841/5,841`.
- Staged rows: `5,891`; every path preserves its source parameter area exactly.
- Closed selector-margin rows: `4,746`, with minimum margin `0.4802908273459625`.
- Explicit two-chart source rows: `290`; two difficult connector rows split into `52` closed children (`50` additional staged rows).
- Single-declared-chart passthrough rows: `805`.
- Live 5396 hashes remained unchanged during staging; all downstream claims remained false.
- Staged migration gate: **PASS**.
