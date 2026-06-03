# 168 - Pair Half-Kernel Parent Ownership Gate

Private derivation gate. This is not a public claim.

## 1. Trigger

Checkpoint 167 locked the lane rule:

```text
no-clock MTS is the empirical lead;
pair-ruler half-kernel is a sidecar only if the action owns the 1/2 factor.
```

The exact question here is:

```text
does the normal-ordered pair action derive the half-kernel source law before
BAO residual scoring?
```

Short answer:

```text
not yet.
```

The `1/2` in the action is real, but by itself it is not enough. In the most
ordinary symmetric variational counting, it is only the bookkeeping factor that
removes double-counting of ordered pairs.

## 2. Machine Artifact

Script:

```text
scripts/pair_half_kernel_parent_ownership_gate.py
```

Run:

```text
runs/20260531-235959-pair-half-kernel-parent-ownership-gate
```

Generated:

```text
source_register.csv
variational_counting_table.csv
ownership_conditions.csv
exact_parent_contract.csv
branch_verdict_matrix.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
half_kernel_contract_constructed_parent_ownership_not_proven
```

Claim ceiling:

```text
pair_half_kernel_parent_ownership_gate_no_sidecar_promotion
```

## 3. The Counting Problem

The live pair action from checkpoint 163 was:

```text
S_pair ~ 1/2 integral dmu_x dmu_y
         :delta_g(x)delta_g(y):
         ell_A K_c^A_B ell^B.
```

The tempting move was:

```text
there is a 1/2 in the action,
therefore T_D and S_D should be halved.
```

That does not automatically follow.

For a symmetric ordered-pair integral:

```text
1/2 integral_DxD [pair(x,y)]
```

the `1/2` usually just cancels the double counting:

```text
(x,y) and (y,x)
```

or cancels the two endpoint/order contributions in the variation.

So the default variational source factor is:

```text
action prefactor 1/2 x endpoint/order multiplicity 2 = 1.
```

That means:

```text
the written action prefactor does not by itself own the half-kernel law.
```

## 4. When the Half Factor Could Be Real

The half-kernel can still be real, but only under a stricter source contract.

| route | net source factor | verdict |
|---|---:|---|
| ordered-pair double-count factor only | `1` | fails to own half-kernel |
| unordered pair measure | `1` | fails to own half-kernel |
| single-pair auxiliary `K_c` equation | `1/2` | conditional |
| normal-ordered connected pair current | `1/2` | conditional |
| post-hoc BAO repair factor | `1/2` | rejected |

So the possible derivation route is not:

```text
there is a 1/2 in S_pair.
```

It must be:

```text
the parent varies a single connected unordered-pair source/current once per
physical pair, and that source equation normalizes K_c with a genuine 1/2.
```

That equation has not been derived yet.

## 5. Exact Parent Contract

For the half-kernel to be promoted, a future parent action must satisfy all of:

| step | condition | required content |
|---:|---|---|
| 1 | domain | pair space is `(D x D - diagonal)/Z2` or an ordered integral with explicit quotient |
| 2 | kernel symmetry | `K_c(x,y)` is well-defined under endpoint swap |
| 3 | zero marginal | `integral dmu_y W_D K_c(x,y)=0` and the swapped condition |
| 4 | single-pair source equation | `delta S / delta K_c = 0` gives `K_c proportional to 1/2 J_pair`, not endpoint source |
| 5 | normalization link | checkpoint-161 `B/4`, `B/6` laws are shown to be ordered-pair laws before quotienting |
| 6 | conservation safety | pair stress/current satisfies Bianchi-compatible conservation or explicit exchange |
| 7 | observable safety | growth/RSD, lensing/slip, and CMB-ruler responses are derived or bounded |

The decisive missing step is:

```text
single-pair source equation.
```

Without that, the half factor is a good clue, not a derivation.

## 6. Current Gate Results

| gate | status | readout |
|---|---|---|
| written action prefactor exists | pass limited | checkpoint 163 writes `S_pair` with `1/2` |
| bookkeeping half is enough | fail | endpoint/order multiplicity cancels it |
| single-pair source equation | fail open | no varied `K_c` equation or conserved pair current |
| zero marginal survives halving | pass conditional | linear rescaling preserves the compensated-kernel identity |
| pre-data parent ownership | fail open | half-kernel was tested after row-pressure diagnosis |
| sidecar promotion | fail | no promotion from this gate |

That is a narrow but important result:

```text
the half-kernel is not dead;
the half-kernel is not owned.
```

## 7. Branch Verdict

| branch | empirical status | ownership status | verdict |
|---|---|---|---|
| base 161 pair-ruler | `DeltaBIC_vs_no_clock=+1.5020119090340813` | source law inserted | live reference, not lead |
| half-kernel pair-ruler | `DeltaBIC_vs_no_clock=+0.5114297958095904` | contract exists, parent ownership missing | best sidecar candidate, closure-only |
| no-clock lead | lead lane from 167 | unaffected by half-kernel gap | empirical lead remains |

The half-kernel score is still useful:

```text
it improved the pair branch without a fitted projection amplitude.
```

But its legal status is now:

```text
closure-only sidecar until the pair current/source equation is derived.
```

## 8. Decision

Decision:

```text
half_kernel_contract_constructed_parent_ownership_not_proven
```

Meaning:

```text
The action prefactor is a real structural clue.
But the ordinary variational count cancels it.
To own the half-kernel, MTS needs a single-pair auxiliary K_c equation or a
conserved connected pair current whose normalization gives the 1/2 before data
scoring.
```

So we do not promote:

```text
MTS_pair_ruler_half_kernel
```

We keep:

```text
MTS_2over27_no_clock_u3quarter
```

as the empirical lead.

Boxing-card readout:

```text
The half-kernel had a nice counterpunch, but the replay shows the 1/2 may just
be referee bookkeeping unless we derive the pair current.
No knockdown. No disgrace. It stays in the gym.
```

## 9. Next Target

Create:

```text
169-no-clock-lead-official-likelihood-refresh-plan.md
```

Task:

```text
move the main empirical work back onto the no-clock lead branch while keeping
the pair-ruler half-kernel frozen as a closure-only sidecar.
```

Pass condition:

```text
future tests score MTS, LCDM, wCDM, and CPL symmetrically with source manifests,
covariance checks, nuisance rules, jackknifes, and edge flags.
```

Fail condition:

```text
the sidecar half-kernel is used as if parent-owned, or baselines are not put
through the same stress tests as MTS.
```
