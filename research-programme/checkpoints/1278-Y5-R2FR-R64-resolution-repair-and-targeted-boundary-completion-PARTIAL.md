# 5262 — R64 resolution repair and targeted boundary completion

## Status

`PAUSED_AT_GENERATION_7_RESOURCE_CHECKPOINT`

The controller was stopped deliberately after approximately the agreed
overnight work window. No MTS-owned Python process remains active. All
completed nodes and the current boundary state are restart-safe.

## Resolution repair

Generation 5 produced one failed acceptance row at `G05_I06_T01`:

\[
\epsilon_{32\rightarrow512}=0.00562483826169
>0.005.
\]

This was not a topology, integrity, pole-fit, closure, coverage, or high-order
failure. The existing mid-order comparison was

\[
\epsilon_{128\rightarrow512}
=2.11168301374\times10^{-8}.
\]

The low diagnostic was escalated from order 32 to order 64 without changing
the acceptance tolerance:

\[
\epsilon_{64\rightarrow512}
=5.47681778614\times10^{-5}
<0.005.
\]

The order-128 and order-512 physical values are exactly unchanged at the
stored precision. Generation 5 therefore closes through an explicit
resolution repair, not by weakening or deleting the failed gate.

## Completed boundary work

- Completed generations: 3 through 7.
- Completed scheduled nodes: 20 of 27.
- Third or ambiguous topology signatures: 0.
- Every completed node passes integrity and its effective acceptance contract.
- All future nodes use the declared order ladder `(64, 128, 512)`.

| transition | current width | certified target | width / target | completed bisections | remaining |
|---|---:|---:|---:|---:|---:|
| I01_T00 | \(4.21267358532\times10^{-4}\) | \(3.75486935804\times10^{-4}\) | 1.122 | 5 | 1 |
| I01_T01 | \(4.21267358531\times10^{-4}\) | \(1.82151788608\times10^{-4}\) | 2.313 | 5 | 2 |
| I06_T00 | \(4.21267358531\times10^{-4}\) | \(7.98848804525\times10^{-5}\) | 5.273 | 5 | 3 |
| I06_T01 | \(4.21267358532\times10^{-4}\) | \(3.75486935804\times10^{-4}\) | 1.122 | 5 | 1 |

Seven classified midpoint nodes remain:

1. generation 8: all four transitions;
2. generation 9: I01_T01 and I06_T00;
3. generation 10: I06_T00.

`G08_I01_T00` already has six of twelve topology jobs cached, so resumption
does not discard the partial calculation.

## Resume contract

Resume the existing script without changing its inputs:

`scripts/Y5_R2FR_5262_R64_resolution_repair_and_targeted_boundary_completion.py`

The controller must:

- retain one Python process and single-thread numerical libraries;
- load `source-intake/functional_rg/5262/boundary_state.json`;
- reuse completed node results and the partial `G08_I01_T00` state cache;
- stop only when all four certified width and boundary-error gates pass;
- leave numeric UV, local-GR, and full-MTS claims false until outer
  coefficient reassembly is separately validated.

## Current claim scope

- Continuous residue envelope: **certified**.
- R64 repair of the isolated low-order diagnostic: **validated**.
- Topology remains binary through generation 7: **validated**.
- Final boundary stopping gate: **not yet complete**.
- Numeric outer coefficient: **not yet claimable**.
- Local GR: **not yet claimable**.
- Full MTS: **not yet claimable**.

## Evidence

- `source-intake/functional_rg/5262/G05_I06_T01_R64_repair/resolution_repair_result.json`
- `source-intake/functional_rg/5262/G05_I06_T01_R64_repair/resolution_repair_validation.csv`
- `source-intake/functional_rg/5261/generation_05/result.json`
- `source-intake/functional_rg/5262/boundary_state.json`
- `source-intake/functional_rg/5262/generation_06/`
- `source-intake/functional_rg/5262/generation_07/`
- `source-intake/functional_rg/5262/nodes/G08_I01_T00/state_cache.json`
