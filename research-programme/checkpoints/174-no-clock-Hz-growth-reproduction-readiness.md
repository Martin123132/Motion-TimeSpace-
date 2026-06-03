# 174 - No-Clock H(z)/Growth Reproduction Readiness

Private readiness checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 173 reproduced the SN+BAO locked `2/27` matrix through the
official-refresh guard.

Before expanding again, this checkpoint audits the non-CMB evidence shelf:

```text
H(z),
BAO+H(z),
growth/RSD,
ELG grid likelihood.
```

The purpose is not to score new physics. The purpose is to decide which existing
runs are clean enough to reproduce under the same no-sidecar/no-promotion rules.

## 2. Machine Artifact

Script:

```text
scripts/no_clock_Hz_growth_reproduction_readiness.py
```

Run:

```text
runs/20260531-235959-no-clock-Hz-growth-reproduction-readiness
```

Command:

```text
python scripts/no_clock_Hz_growth_reproduction_readiness.py --timestamp 20260531-235959
```

Status:

```text
no_clock_Hz_growth_reproduction_readiness_passed
```

Claim ceiling:

```text
non_CMB_reproduction_readiness_no_full_refresh_or_theory_promotion
```

## 3. Candidate Shelf

| candidate | arena | current status | readiness |
|---|---|---|---|
| `BAO_Hz_noCMB_robustness` | BAO+H(z) | `noCMB_radial_robustness_stable_draw` | guarded diagnostic reproduction |
| `fresh_CC_Hz_source_locked_holdout` | H(z) | `fresh_CC_source_locked_Hz_holdout_competitive_draw` | guarded reproduction |
| `source_locked_growth_covariance_holdout` | growth/RSD | `growth_covariance_source_locked_primary_preferred_or_draw` | conditional growth reproduction |
| `ELG_grid_likelihood_holdout` | ELG grid growth/RSD | `ELG_grid_primary_competitive_draw` | conditional grid reproduction |

Source-locked ready candidates:

```text
fresh_CC_Hz_source_locked_holdout
source_locked_growth_covariance_holdout
ELG_grid_likelihood_holdout
```

BAO+H(z) robustness is useful context, but it is not promoted above the fresher
source-locked H(z) and growth lanes.

## 4. Readiness Gates

All readiness gates passed:

| gate | status |
|---|---|
| candidate sources exist | pass |
| candidate artifacts parse | pass |
| hard gates clean or non-promotion only | pass |
| source locks pass where required | pass |
| sidecar absent | pass |
| non-CMB reproduction targets identified | pass |
| promotion blocked by design | pass |
| claim ceiling preserved | pass |

Audit counts:

```text
candidate artifacts checked = 45
bad artifacts = 0
hard gate failures = 0
sidecar failures = 0
ready candidates = 4
source-locked ready candidates = 3
```

The allowed failed gates are intentional non-promotion gates, such as:

```text
theory_promotion
official_joint_claim
```

Those failures are not bugs. They are the bouncer doing his job.

## 5. Non-CMB Scorecard

| candidate | metric | value | readout |
|---|---|---:|---|
| BAO+H(z) no-CMB robustness | primary `ΔBIC` vs LCDM | -1.8838579373924915 | competitive draw |
| BAO+H(z) no-CMB robustness | production median `ΔBIC` vs LCDM | -1.2387028598152376 | stable competitive draw |
| fresh source-locked H(z) | primary `ΔBIC` vs LCDM | 0.33256956910347313 | competitive draw |
| source-locked growth covariance | primary all-row `Δχ²` vs LCDM | -2.3035702803557125 | locked preferred |
| source-locked growth covariance | primary `fσ8`-only `Δχ²` vs LCDM | -0.3346859767476644 | competitive draw |
| ELG grid likelihood | primary ELG `Δχ²` vs LCDM | 0.03750180074447895 | competitive draw |
| Gaussian growth + ELG diagnostic | DR2 diagnostic sum `Δχ²` vs LCDM | -2.2660684796112336 | locked preferred |

Readout:

```text
The non-CMB shelf does not give a knockout. It gives survivability plus a few
clean counters: H(z) draws, growth all-row improves, fσ8-only draws, and ELG
does not reverse the card.
```

## 6. Promotion Blockers

The readiness audit explicitly blocks promotion:

| scope | blocker |
|---|---|
| H(z) | survivability is not a derivation |
| growth/RSD | uses conditional GR-proxy perturbations |
| ELG grid | individual grid is useful, but no official joint wrapper yet |
| full programme | CMB bridge, local GR/PPN, and parent action remain unresolved |

So the allowed claim is:

```text
the locked no-clock branch is ready for guarded non-CMB reproduction.
```

The forbidden claim is:

```text
the non-CMB shelf proves the field theory.
```

## 7. Decision

Decision:

```text
no_clock_Hz_growth_reproduction_readiness_passed
```

Meaning:

```text
The next empirical stage is now organized. We know which non-CMB results can be
reproduced under the official guard, which ones are conditional, and why none of
them can substitute for the missing derivations.
```

Boxing-card readout:

```text
This is the corner team sorting the gloves before the next rounds.
H(z) is a draw round, growth lands a couple of counters, ELG does not wobble us,
but none of this wins the title without the parent action and perturbations.
```

## 8. Next Target

Create:

```text
175-no-clock-nonCMB-reproduction-guard.md
```

Next task:

```text
Implement guarded reproduction for the source-locked H(z), conditional
growth/RSD, and ELG grid lanes, while keeping BAO+H(z) robustness as diagnostic
context and preserving the no-promotion ceiling.
```
