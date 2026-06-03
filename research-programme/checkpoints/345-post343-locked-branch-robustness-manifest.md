# 345 - Post-343 Locked-Branch Robustness Manifest

Private empirical/theory-discipline checkpoint. This is not a public cosmology, CMB, local-GR, PPN, perturbation-theory, or unified-field claim.

## Purpose

Checkpoint 343 made the hard but clean decision:

```text
B_mem = 2/27 is an explicit locked closure value and theorem target,
not a parent-derived amplitude.
```

Checkpoint 344 updated the claim ledger so the programme does not drift back into overclaiming.

This checkpoint now does the empirical bookkeeping that follows from that decision.

The question is not:

```text
have we derived the amplitude?
```

The question is:

```text
with the amplitude now honestly labelled as closure,
does the locked branch remain live enough to keep deriving around it?
```

Short answer:

```text
yes, as a late-time closure-performance branch only.
```

## Machine Artifact

Script:

```text
scripts/post343_locked_branch_robustness_manifest.py
```

Run:

```text
runs/20260601-214500-post343-locked-branch-robustness-manifest
```

Key outputs:

```text
results/source_register.csv
results/empirical_evidence_register.csv
results/post343_robustness_matrix.csv
results/next_run_manifest.csv
results/claim_ceiling_table.csv
results/gate_results.csv
results/decision.csv
status.json
DONE.txt
```

Status:

```text
post343_locked_closure_robustness_manifest_written_no_public_claim
```

Claim ceiling:

```text
empirical_closure_manifest_only_no_parent_derivation_or_stable_evidence_claim
```

## Source Coverage

The manifest source register contains 25 rows:

```text
source_paths_missing = 0
```

It ties together:

- the pre-343 SN+BAO robustness scorecards,
- the frozen-branch holdout scorecards,
- the source-locked H(z), growth, and ELG holdouts,
- the official wrapper DR1/DR2 locked no-SH0ES runs,
- the 343/344 post-derivation claim-control checkpoints.

Important source split:

| Source class | Role | Post-343 use |
|---|---|---|
| `100`-`106` | pre-343 robustness context | retained, but fitted-amplitude rows are not closure proof |
| `144`-`147` | frozen/holdout survivability | retained as empirical pressure tests |
| `330` | official wrapper DR1/DR2 locked branch | primary post-343 background evidence |
| `343`-`344` | claim discipline | controls all interpretation |

## Post-343 Locked SN+BAO Matrix

Primary branch:

```text
MTS_fixed_2over27_no_clock
B_mem = 2/27
u3 = 1/4
p = 3
no SH0ES
full Pantheon+ covariance
DESI BAO full covariance
```

### DR2

Run:

```text
runs/20260601-174000-DR2-locked2over27-fullcov-noSH0ES-cosmo-SN-BAO-short-smoke
```

| Reference | Delta chi2 | Delta AIC | Delta BIC |
|---|---:|---:|---:|
| `LCDM` | -5.259466877750583 | -5.259466877750583 | -5.259466877750583 |
| `wCDM` | -0.16900927232632057 | -2.1690092723263206 | -7.569629849697321 |
| `CPL` | +0.1677276035882187 | -3.8322723964117813 | -14.63351355115401 |

Diagnostics:

```text
locked branch edge flag = false
all parsed prior edges = 0
zero-memory control max delta vs LCDM = 0.0
fitted diagnostic B_mem = 0.07453319160061826
locked B_mem = 0.07407407407407407
relative shift = +0.6198086608346595 percent
```

### DR1

Run:

```text
runs/20260601-174500-DR1-locked2over27-fullcov-noSH0ES-cosmo-SN-BAO-short-smoke
```

| Reference | Delta chi2 | Delta AIC | Delta BIC |
|---|---:|---:|---:|
| `LCDM` | -3.6187583484374954 | -3.6187583484374954 | -3.6187583484374954 |
| `wCDM` | -0.38142370168634443 | -2.3814237016863444 | -7.781433218849088 |
| `CPL` | +0.38253685994436637 | -3.6174631400556336 | -14.41748217438112 |

Diagnostics:

```text
locked branch edge flag = false
all parsed prior edges = 0
zero-memory control max delta vs LCDM = 0.0
fitted diagnostic B_mem = 0.07341846186321792
locked B_mem = 0.07407407407407407
relative shift = -0.885076484655805 percent
```

## Gate Results

All manifest gates passed:

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | all sources present |
| run CSVs parse | pass | DR1 and DR2 run CSVs parsed |
| locked branch edge-clean | pass | no locked prior-edge flags |
| no prior-edge dependency in matrix | pass | all parsed prior-edge rows clean |
| zero-memory control reproduces LCDM | pass | tolerance `1e-9` |
| fair baseline comparisons | pass | same data, nuisance, calibration |
| DR1/DR2 release split present | pass | both releases present |
| locked vs LCDM BIC not disfavored | pass | DR2 `-5.259466877750583`; DR1 `-3.6187583484374954` |
| fitted diagnostic near locked value | pass | within one percent in both releases |
| post-343 claim ceiling enforced | pass | no parent-derivation or stable-evidence claim |
| CMB/growth/local-GR not promoted | pass | late-time evidence stays separated |

## Judge's Card

This is a good round for the locked branch.

It is not a knockout and it is not a derivation.

But after the amplitude was demoted to explicit closure, the thing we needed to check was whether the empirical branch still deserved oxygen. On the current post-343 manifest, it does:

```text
DR2: edge-clean, same-k better than LCDM, better BIC than LCDM/wCDM/CPL.
DR1: edge-clean, same-k better than LCDM, better BIC than LCDM/wCDM/CPL.
zero-memory: exactly reproduces LCDM.
fitted diagnostic amplitude: lands within about one percent of 2/27 in both releases.
```

That is not random noise-level nonsense. It is a live late-time closure signal.

But the ceiling stays strict:

```text
No parent amplitude derivation.
No stable cosmology evidence claim.
No CMB pass.
No perturbation theory pass.
No local GR/PPN pass.
No completed unified theory claim.
```

## What This Means For The Theory Route

The programme now has two clean lanes instead of one muddled lane.

Lane A:

```text
empirical locked closure branch
```

This lane is alive.

Lane B:

```text
parent derivation of the closure factors
```

This lane is incomplete.

The key factorization remains:

```text
B_mem = q_trace * epsilon_H * (H_star/H0)^2.
```

Post-343 status:

| Factor | Status |
|---|---|
| `q_trace=2/27` | conditional if rank/dim assumed |
| `epsilon_H=1` | closure or conditional exact-readout theorem target |
| `H_star=H0` | independent calibration closure/theorem target |
| `B_mem=2/27` | explicit closure, empirically interesting |

So the next derivation work should not try to smuggle `2/27` back in through a side door.

The next honest derivation target is:

```text
derive H_star = H0,
or prove why it must remain a calibration closure.
```

Reason:

```text
q_trace and epsilon_H have already been battered through several routes.
H_star/H0 is the remaining multiplicative factor that has not received the same focused gate.
```

## Next Run Manifest

The manifest writes five next-run/theory options.

Priority order:

| Priority | Next target | Why |
|---:|---|---|
| 1 | post-343 relabel dry-run | embed closure labels directly in official wrapper outputs |
| 2 | strict baseline ladder | keep the boxing card fair against fitted LCDM/wCDM/CPL |
| 3 | independent late-time holdout refresh | keep testing without amplitude refit |
| 4 | CMB/growth kill-screen | prevent late-time success becoming a fake CMB claim |
| 5 | `H_star=H0` calibration theory gate | next derivation target |

My recommendation:

```text
do H_star=H0 next.
```

Not because the empirical branch is weak.

Because the empirical branch is now strong enough to justify a serious derivation attempt, and `H_star/H0` is the least-worked factor left in the amplitude product.

## Bottom Line

Post-343, the locked branch is cleaner than before:

```text
less overclaimed,
more testable,
still empirically alive,
and better positioned for real derivation work.
```

That is a good place to be.

Next checkpoint should attempt:

```text
346 - H_star/H0 Calibration Theorem Gate
```

with a hard rule:

```text
derive H_star = H0 from the parent action / observer normalization,
or demote it explicitly to closure like B_mem.
```
