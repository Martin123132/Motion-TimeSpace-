# 311 - Sector Label `S_D` Origin Attempt

Private derivation checkpoint. This is not a public local-GR, PPN, cosmology, galaxy, CMB, or parent-field-theory claim.

## Purpose

Checkpoint 310 reduced the ordinary/MTS split to:

```text
derive S_D,
derive [K_boundary,S_D]=0.
```

This checkpoint asks:

```text
can S_D appear naturally as a spectral-support label,
rather than as a hand-added sector switch?
```

Short answer:

```text
yes, conditionally:
S_D can be built as the support projector of a positive MTS boundary-activity operator.
```

But:

```text
the activity operator and commuting boundary kernel are still not parent-derived.
```

## Activity Operator

Let:

```text
H_B(D)
```

be the boundary data space with inner product:

```text
<.,.>_D.
```

Define the MTS boundary activity map:

```text
C_D = P_rel P_IR P_coh.
```

Meaning:

```text
P_coh  keeps coherent scalar/isotropic domain content,
P_IR   keeps the low-frequency MTS boundary channel,
P_rel  keeps non-exact relative boundary-current memory content.
```

Then define:

```text
A_D = C_D^† C_D.
```

So:

```text
<B,A_D B>_D = ||C_D B||_D^2 >= 0.
```

Therefore `A_D` is positive if `C_D` and the boundary inner product are parent-owned.

## Spectral Support Label

Define:

```text
S_D = 1_(0,infinity)(A_D).
```

This is the projector onto the support/range of MTS boundary activity.

Then:

```text
C_D B_ord = 0
```

implies:

```text
A_D B_ord = 0,
S_D B_ord = 0.
```

And:

```text
C_D B_FLRW != 0
```

implies:

```text
S_D B_FLRW != 0.
```

This removes an arbitrary threshold.

The split is:

```text
H_ord = Ker(A_D),
H_MTS = support(A_D).
```

## Block Kernel Condition

The block kernel follows if:

```text
[K_boundary,A_D] = 0
```

or equivalently:

```text
[K_boundary,S_D] = 0.
```

Then:

```text
<H_ord,K_boundary H_MTS> = 0.
```

So:

```text
K_cross = 0.
```

That would derive the ordinary/MTS sector split.

## What Was Gained

| Item | Result |
|---|---|
| `S_D` can be written without a fitted threshold | conditional pass |
| ordinary zero-activity data lies in `Ker(A_D)` | conditional pass |
| FLRW active data lies in `support(A_D)` | conditional pass |
| `S_D^2=S_D` and `S_D^†=S_D` | conditional pass |
| block split follows from `[K,A_D]=0` | conditional pass |

This is the cleanest `S_D` form so far.

## What Failed

The parent action has not derived:

```text
C_D = P_rel P_IR P_coh,
the boundary inner product <.,.>_D,
A_D as a real constraint/charge operator,
[K_boundary,A_D]=0,
exact C_D B_ord=0 for ordinary coherent stress.
```

So:

```text
S_D remains a conditional spectral label,
not a parent-owned sector theorem.
```

## No-Go Checks

| Claim | Result | Reason |
|---|---|---|
| `S_D=support(A_D)` derives local GR by itself | fail | `A_D` depends on underived parent projectors |
| spectral support removes all closure | partial | it removes thresholds, not parent-action ownership |
| ordinary coherent stress is automatically in `Ker(A_D)` | fail | scalar/coherent ordinary stress can leak unless `C_D` is MTS-specific |
| `K_cross=0` follows without an action statement | fail | generic `K_boundary` can mix kernel and support |
| hard support handles small leakage gently | fail | any nonzero activity activates the hard projector |

## Promotion Gates

| Gate | Result | Meaning |
|---|---|---|
| source paths exist | pass | attempt traceable |
| activity operator constructed | conditional pass | `A_D=C_D^†C_D` gives a real theorem target |
| threshold-free sector label constructed | conditional pass | `S_D=1_(0,infinity)(A_D)` |
| ordinary kernel silence condition written | conditional pass | `C_D B_ord=0 -> S_D B_ord=0` |
| FLRW retention condition written | conditional pass | `C_D B_FLRW !=0 -> S_D B_FLRW !=0` |
| activity operator parent-derived | fail | `C_D` and `<.,.>_D` remain contracts |
| kernel commutation parent-derived | fail | `[K_boundary,A_D]=0` not action-owned |
| ordinary coherent counterexample closed | fail | generic bath problem not fully closed |
| hard support regularized | fail | exact zero or smooth bounded runner needed |
| selector parent-derived | fail | `sigma_D` remains conditional |
| local GR promoted | fail | no PPN/local-GR promotion |
| empirical pivot recommended | pass | local derivation route is now narrow enough to park |

## Decision

Decision:

```text
SD_spectral_support_label_constructed_block_kernel_parent_origin_still_missing
```

Claim ceiling:

```text
conditional_SD_label_no_block_kernel_selector_local_GR_or_Bmem_promotion
```

Meaning:

```text
we found the cleanest non-arbitrary S_D definition,
but it still needs parent ownership of A_D and K commutation.
```

Boxing-score version:

```text
We found the judges' rulebook:
only modes with actual MTS boundary activity enter the MTS weight class.
But the promoter still has to prove this rulebook belongs to the sport,
not just to our corner.
```

## Next Step

This is where I would stop squeezing the local branch for now.

Recommended next:

```text
pivot back to empirical holdout testing.
```

Reason:

```text
the remaining local theorem is now very narrow:
derive C_D and [K_boundary,A_D]=0 from the parent action.
```

That is a real future theorem target, but further local work right now risks circling the same closure.

Empirical pivot should keep the claim ceiling:

```text
local branch = conditional theorem target / effective closure,
not derived local GR.
```

## Machine Artifacts

Script:

```text
scripts/sector_label_SD_origin_attempt.py
```

Run:

```text
runs/20260601-000134-sector-label-SD-origin-attempt
```

Output files:

```text
runs/20260601-000134-sector-label-SD-origin-attempt/results/source_register.csv
runs/20260601-000134-sector-label-SD-origin-attempt/results/activity_operator.csv
runs/20260601-000134-sector-label-SD-origin-attempt/results/spectral_label_proof.csv
runs/20260601-000134-sector-label-SD-origin-attempt/results/block_kernel_origin.csv
runs/20260601-000134-sector-label-SD-origin-attempt/results/branch_tests.csv
runs/20260601-000134-sector-label-SD-origin-attempt/results/no_go_tests.csv
runs/20260601-000134-sector-label-SD-origin-attempt/results/promotion_gates.csv
runs/20260601-000134-sector-label-SD-origin-attempt/results/next_targets.csv
runs/20260601-000134-sector-label-SD-origin-attempt/results/decision.csv
```
