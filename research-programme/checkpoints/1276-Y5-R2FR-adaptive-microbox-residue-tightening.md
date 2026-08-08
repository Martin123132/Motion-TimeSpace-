# 5260 — Adaptive microbox residue tightening

## Purpose

Checkpoint 5258 closed the existence problem: every active transition bracket
has a finite continuous interval residue envelope. Checkpoint 5259 then showed
that the first enclosure was too loose to use efficiently. Its certified
envelopes were 48–133 times the earlier sampled scale and implied 11–13 more
outer bisections.

Checkpoint 5260 addresses that measured dependency inflation. It does not add
a new physical assumption and it does not promote a local-GR claim.

## Partition theorem

Let \(B_j=[x_j^-,x_j^+]\) be one of the 976 certified leaf boxes from
checkpoint 5258. Partition it into 16 closed microboxes,

\[
B_{jk}
=
\left[
x_j^-+\frac{k}{16}(x_j^+-x_j^-),
x_j^-+\frac{k+1}{16}(x_j^+-x_j^-)
\right],
\qquad k=0,\ldots,15.
\]

Because

\[
B_j=\bigcup_{k=0}^{15}B_{jk},
\]

and the checkpoint-5258 interval evaluator encloses the residue on every
microbox,

\[
\sup_{x\in B_j}|R_\epsilon(x)|
\leq
\max_k \widehat R_{\epsilon,jk}.
\]

Taking the maximum over all parent boxes therefore preserves the continuous
certificate:

\[
\widehat R_\epsilon
=
\max_{j,k}\widehat R_{\epsilon,jk}.
\]

The half-residue triangle envelope and boundary-location error remain

\[
E_C
=0.016\left(2\widehat R_{20}+\widehat R_{40}\right),
\qquad
\delta_C
=\frac14\,\Delta x\,E_C.
\]

No sampling claim enters these inequalities. Sampled rows are used only to
measure how conservative the certified bound remains.

## Why 16 pieces

A convergence pilot split the former maximum box for each transition by
\(1,2,4,8,\) and \(16\). At 16 pieces, the new upper bound on every tested
worst box was within approximately \(1.27\)–\(1.36\) of its thin-midpoint
interval value. No split produced a singular failure.

Sixteen is therefore the first tested power-of-two depth that removes most of
the dependency explosion without rewriting the amplitude evaluator or adding
thousands of unnecessary topology generations.

## Certified result

The full run contains 15,616 microboxes and covers all 976 checkpoint-5258
parents exactly. Every interval denominator remains separated and every
analytic-disk root gate remains valid.

| transition | tightened envelope | reduction from 5258 | certified / sampled | error / budget | further bisections |
|---|---:|---:|---:|---:|---:|
| I01_T00 | 6,447.489 | 71.932 | 1.542 | 35.902 | 6 |
| I01_T01 | 13,290.827 | 25.553 | 1.893 | 74.007 | 7 |
| I06_T00 | 30,305.457 | 45.103 | 2.958 | 168.750 | 8 |
| I06_T01 | 6,447.489 | 71.932 | 1.542 | 35.902 | 6 |

The maximum certified-to-sampled ratio is now \(2.9582\), down from
\(133.4185\). The maximum fixed-envelope bisection count is now eight, down
from thirteen.

## Reflection handling

The raw I01_T00/I06_T01 envelopes differ by
\(1.5539\times10^{-5}\) relatively after independent floating-point
subdivision. Rather than average them or assert exact numerical equality, the
certificate assigns both members the componentwise maximum of their two
independent \(R_{20}\) and \(R_{40}\) upper bounds. This is a safe union bound:
it can only enlarge either enclosure. The final paired envelopes are therefore
identical without weakening coverage.

## Decision

`USE_TIGHTENED_CERTIFICATE_FOR_TARGETED_TOPOLOGY_BISECTION`

The interval-representation problem is now controlled well enough to return
to the physical outer boundary search. The next calculation should:

1. bisect only the four active topology brackets;
2. use the certified 5260 envelope in the stopping law;
3. prioritise I06_T00, then I01_T01, then the reflected pair;
4. stop each transition independently when its boundary error is below
   \(0.6052369604865984\);
5. rerun the outer coefficient and GR-linked handoff gate only after all four
   stopping conditions close.

## Claim scope

- Continuous boundary residue certificate: **true**.
- Certified enclosure sufficiently close to sampled scale for targeted
  bisection: **true**.
- Current boundary-error budget: **not met**.
- Numeric UV coefficient: **not yet claimable**.
- Local GR: **not yet claimable**.
- Full MTS field theory: **not yet claimable**.

## Machine-readable evidence

- `scripts/Y5_R2FR_5260_adaptive_microbox_residue_tightening.py`
- `source-intake/functional_rg/5260/microbox_run_config.json`
- `source-intake/functional_rg/5260/status.json`
- `source-intake/functional_rg/5260/tightened_interval_residue_boxes.csv`
- `source-intake/functional_rg/5260/tightened_transition_envelopes.csv`
- `source-intake/functional_rg/5260/microbox_residue_validation.csv`
- `source-intake/functional_rg/5260/microbox_residue_result.json`
