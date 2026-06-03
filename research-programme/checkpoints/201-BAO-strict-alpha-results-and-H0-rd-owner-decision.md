# 201 - BAO Strict-Alpha Results and H0-r_d Owner Decision

Private theory checkpoint. This is not a public BAO claim.

## 1. Trigger

Checkpoint 200 ran the strict-alpha BAO stress:

```text
2 releases x 5 fixed-alpha candidates x 6 model branches = 60 fits.
```

The result was not just a score. It forced a domain decision:

```text
BAO likes late/readback alpha,
BAO dislikes CMB-profile or half-memory endpoint-jump alpha.
```

This checkpoint converts that into a rule ledger.

## 2. Machine Artifact

Script:

```text
scripts/BAO_strict_alpha_results_and_H0_rd_owner_decision.py
```

Run:

```text
runs/20260601-000018-BAO-strict-alpha-results-and-H0-rd-owner-decision
```

Command:

```text
python scripts/BAO_strict_alpha_results_and_H0_rd_owner_decision.py --timestamp 20260601-000018
```

Status:

```text
BAO_alpha_domain_decision_late_common_mode_candidate_CMB_endpoint_alpha_demoted
```

Claim ceiling:

```text
BAO_alpha_domain_decision_internal_only_parent_H0_rd_owner_missing
```

## 3. Release Consistency

| alpha candidate | worst verdict | max delta chi2 vs shared-alpha locked fit | decision |
|---|---|---:|---|
| DR1 locked-fit readback | `strict_alpha_survives` | `0.18352815632990627` | empirical anchor only |
| DR2 locked-fit readback | `strict_alpha_survives` | `0.0620396325578394` | empirical anchor only |
| late-reference H0 with `rdrag` | `strict_alpha_soft_warning` | `1.3194886763391391` | lead theorem candidate |
| half-memory H0 with `rdrag` | `strict_alpha_pressure` | `15.9641419885347` | demoted for BAO |
| same-density CMB-profile H0 with `rdrag` | `strict_alpha_pressure` | `16.186857530470693` | demoted for BAO |

This gives a clean decision:

```text
BAO alpha should be late common-mode,
not CMB endpoint-jump.
```

## 4. Owner Decisions

| candidate | decision | reason |
|---|---|---|
| DR1/DR2 readbacks | empirical anchors, not parent owners | they survive, but cannot become predictions after seeing BAO |
| late-reference H0 with `rdrag` | lead theorem candidate with warning | survives DR1 and only soft-warns DR2 |
| same-density CMB-profile H0 with `rdrag` | demoted for BAO | strict-alpha pressure in both releases |
| half-memory H0 with `rdrag` | demoted for BAO | strict-alpha pressure in both releases |

The readbacks are useful as calibration targets:

```text
they tell us where BAO wants alpha to live.
```

But they are quarantined:

```text
readback is not prediction.
```

## 5. Endpoint Domain Assignment

The emerging domain map is:

| observable domain | endpoint class | allowed calibration | forbidden calibration |
|---|---|---|---|
| CMB acoustic angle | early-to-late | half-memory clock bridge for theta/H0 profiling | BAO readback as CMB proof |
| BAO ratios | late common-mode ruler calibration | late-reference or parent-derived late `H0-r_d` alpha | CMB-profile/half-memory endpoint-jump alpha |
| SN/local ladder | late local common-mode | late calibration if local/environmental silence holds | unscreened global clock drift |
| growth | path-dependent perturbation history | none from endpoint algebra alone | borrowing background alpha/theta rules |

This is the strongest current version of the endpoint route:

```text
CMB is early-to-late endpoint memory.
BAO is late common-mode ruler calibration.
SN/local is late common-mode if local silence holds.
Growth is not closed by this algebra.
```

## 6. Parent Contract

To promote BAO beyond empirical closure, the parent theory must still derive:

| contract | status |
|---|---|
| late common-mode BAO alpha owner | lead theorem target |
| readback quarantine | guardrail required |
| release-independent alpha prediction | missing |
| local silence consistency | still open |

The next precise theorem target is:

```text
derive why BAO uses the late common-mode H0-r_d owner.
```

If that derivation fails, BAO remains:

```text
empirical closure-only with fair shared alpha.
```

## 7. Claim Gates

| gate | result |
|---|---|
| all cited sources exist | pass |
| CMB/half-memory alpha demoted for BAO | pass |
| late common-mode alpha candidate retained | pass |
| readbacks quarantined | pass |
| parent `H0-r_d` owner derived | fail |
| BAO support claim allowed | fail |

## 8. Decision

Decision:

```text
BAO_alpha_domain_decision_late_common_mode_candidate_CMB_endpoint_alpha_demoted
```

Meaning:

```text
BAO alpha ownership is assigned to the late common-mode theorem route.
CMB-profile and half-memory endpoint-jump alpha are demoted for BAO.
Readbacks remain empirical anchors, not predictions.
```

Current theory status:

```text
BAO no longer looks like a contradiction to the endpoint-clock route;
BAO now enforces a domain distinction;
parent ownership is still missing.
```

Next target:

```text
202-late-common-mode-H0-rd-owner-derivation-attempt.md
```
