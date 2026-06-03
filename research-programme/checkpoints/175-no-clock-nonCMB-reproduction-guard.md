# 175 - No-Clock Non-CMB Reproduction Guard

Private reproduction checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 174 sorted the non-CMB shelf and found three source-locked lanes
ready for guarded reproduction:

```text
fresh source-locked H(z),
source-locked growth/RSD covariance,
ELG non-Gaussian grid likelihood.
```

This checkpoint re-runs those lanes and compares the new outputs to the locked
reference outputs.

## 2. Machine Artifact

Script:

```text
scripts/no_clock_nonCMB_reproduction_guard.py
```

Run:

```text
runs/20260531-235959-no-clock-nonCMB-reproduction-guard
```

Command:

```text
python scripts/no_clock_nonCMB_reproduction_guard.py --timestamp 20260531-235959 --reference-tolerance 1e-6
```

Status:

```text
no_clock_nonCMB_reproduction_guard_passed
```

Claim ceiling:

```text
non_CMB_guarded_reproduction_no_full_refresh_or_theory_promotion
```

## 3. Reproduction Runs

The guard re-ran:

| lane | reproduction run |
|---|---|
| source-locked H(z) | `runs/20260531-235959-no-clock-nonCMB-reproduction-guard/reproduction-runs/20260531-235959-fresh-CC-Hz-source-locked-holdout` |
| source-locked growth/RSD | `runs/20260531-235959-no-clock-nonCMB-reproduction-guard/reproduction-runs/20260531-235959-source-locked-growth-covariance-holdout` |
| ELG grid likelihood | `runs/20260531-235959-no-clock-nonCMB-reproduction-guard/reproduction-runs/20260531-235959-ELG-grid-likelihood-holdout` |

It did not run:

```text
full official likelihood,
CMB,
SN+BAO refit,
local GR/PPN,
parent action,
pair-ruler sidecar.
```

## 4. Guard Results

All guard gates passed:

| gate | status |
|---|---|
| source files exist | pass |
| reproduction runs completed | pass |
| reproduction artifacts parse | pass |
| source locks pass | pass |
| reference metrics reproduced | pass |
| hard gates clean or non-promotion only | pass |
| sidecar absent | pass |
| full refresh not run | pass |
| promotion blocked by design | pass |
| claim ceiling preserved | pass |

Counts:

```text
reproduction candidates = 3
artifact rows checked = 32
reference metrics checked = 5
bad metrics = 0
hard gate failures = 0
sidecar failures = 0
```

## 5. Reproduced Metrics

All reference metrics reproduced exactly within the `1e-6` tolerance:

| lane | metric | reproduced value | readout |
|---|---|---:|---|
| H(z) | primary `ΔBIC` vs LCDM | 0.33256956910347313 | competitive draw |
| growth/RSD | primary all-row `Δχ²` vs LCDM | -2.3035702803557125 | locked preferred |
| growth/RSD | primary `fσ8`-only `Δχ²` vs LCDM | -0.3346859767476644 | competitive draw |
| ELG grid | primary ELG `Δχ²` vs LCDM | 0.03750180074447895 | competitive draw |
| ELG diagnostic | DR2 Gaussian+ELG diagnostic sum `Δχ²` vs LCDM | -2.2660684796112336 | locked preferred |

Readout:

```text
The source-locked non-CMB card is reproducible: H(z) draws, growth all-row
leans locked, fσ8-only draws, and ELG does not overturn the branch.
```

## 6. Source Locks And Sidecar

All reproduced source locks passed:

| lane | source lock |
|---|---|
| H(z) | pass |
| growth/RSD | pass |
| ELG grid | pass |

Sidecar scan:

```text
pair-ruler / half-kernel hits = 0
```

So this remains the no-clock lead lane, not the pair-ruler sidecar lane.

## 7. Non-Promotion Gates

The only non-pass candidate gates were intentional blockers:

| lane | blocker |
|---|---|
| H(z) | `theory_promotion` |
| growth/RSD | `theory_promotion` |
| ELG grid | `official_joint_claim` |
| ELG grid | `theory_promotion` |

These are allowed blockers, not failures. They say:

```text
do not treat H(z), growth, or ELG reproduction as a parent-action derivation,
CMB bridge, local-GR proof, perturbation theorem, or official joint likelihood.
```

## 8. Decision

Decision:

```text
no_clock_nonCMB_reproduction_guard_passed
```

Meaning:

```text
The locked no-clock branch now has reproducible non-CMB support lanes under the
same disciplined guard framework used for BAO-only and SN+BAO. This strengthens
the empirical case as a field-theory target, but it still does not close the
theory debt.
```

Boxing-card readout:

```text
This was the undercard audit. No fireworks, no cheap knockouts, but all three
fighters made weight, passed the source checks, and reproduced their cards.
The title fight is still parent action plus perturbations.
```

## 9. Next Target

Create:

```text
176-official-refresh-decision-gate.md
```

Next task:

```text
Decide whether to run a broader official-refresh scorecard now, or pause the
empirical expansion and return to the parent-action / perturbation derivation
debt that still blocks real theory promotion.
```
