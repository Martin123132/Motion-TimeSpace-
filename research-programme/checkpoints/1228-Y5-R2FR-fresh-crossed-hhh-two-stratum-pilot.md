# 5212 — fresh crossed-hhh two-stratum pilot

## Result

This checkpoint executes the calculation prescribed by checkpoint 5124 rather
than making another target inventory. It estimates the crossed `hhh`
contribution with two independent outer-event strata:

```text
E[H_crossed] = E[H_naive, full] + E[H_topological, independent].
```

The full stratum keeps `pole_model+smooth` paired. The topological stratum uses
the reciprocal residue theorem only for certified safe pairs and evaluates both
members of every unsafe pair. Fresh seeds and the 2:12 allocation were locked
before outcomes.

The fresh `E040/A10` witness exposed a fixed-grid removable-limit convergence
miss. The repair keeps the original `10^-7` acceptance threshold and collision
scope, but refines the symmetric step and checks successive Richardson limits.
This follows the even expansion of a removable holomorphic collision and still
fails closed if convergence or direction independence is not obtained.

Fresh seed `521213/A00` then exposed four unstable nested residue contours.
Checkpoint 5213 proves that all four are strict cross-additive `D-S` clusters:
the componentwise Cauchy sums are holomorphic in the relative coordinate,
their nearest same-summand singularities lie at least 4660 production contour
radii away, and the historical 601-row stable-nonzero corpus contains no
in-scope counterexample. Only rows passing that complete theorem guard are
replaced by the exact residue zero; same-summand and `g3/soft`-alias rows
remain fail-closed.

Current run state: `COMPLETE`. Completed jobs:
`280/280`.
Complete full events: `2/2`; complete
topological events: `12/12`.

The current independent pilot gives the non-claim candidate `K_mu=352.2131226-54.35401625 i`, with real/imaginary standard errors `1382.35` and `43.8345`. The maximum nonlocal mismatch is `0.898166 sigma`.

At the completed-event count, the realized equal-cost speedups are `0.245397` (real) and `1.62768` (imaginary).

The 12-event topological real mean is `-96.7024` with SE `168.449`, median `-1.49247`, one-event-trimmed mean `-54.8755`, and maximum delete-one shift `0.777695` SE. The ordered half means differ by `1.91848` sigma. The imaginary mean is `1.55265` with SE `1.59641`. The largest real variance occurs at physical cosine `-0.6`.

Blind scaled sampling is not authorized. The selected next route is to derive an analytic control variate for the dominant A00/z=-0.6 topological residue family before buying more events.

Across the completed matrix, the source-separated theorem certified `35` exact zero rows, while the adaptive removable extension was used `4` times. All recorded theorem certificates and gate hashes validate.

## Physics status

- Exact local GR+Maxwell truncation from checkpoint 5211 is unchanged.
- This calculation attacks the finite crossed-`hhh` motion-sector amplitude
  uncertainty that blocks the canonical `K_mu` coefficient.
- A partial or pilot matrix is not promoted to a UV coefficient measurement.
- The pilot does not by itself complete the other surviving cut classes or the
  full MTS parent action.
- Numeric UV, local-GR, galaxy-law and full-MTS claims remain false.

## Decision rule

The locked pilot is complete. Its imaginary component shows an observed
cost-variance gain, but its real component does not, the real mean is not
resolved at two standard errors, and 12 events do not establish tail
convergence. The next derivation target is therefore the dominant
`A00/z=-0.6` topological residue family and an analytic control variate, not
more blind brute-force sampling.
