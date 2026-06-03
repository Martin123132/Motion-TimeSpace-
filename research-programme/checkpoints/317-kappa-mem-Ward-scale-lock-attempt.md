# 317 - Kappa Mem Ward Scale-Lock Attempt

Private derivation checkpoint. This is not a public field-theory, cosmology, CMB, local-GR, or amplitude-prediction claim.

## Purpose

Checkpoint 316 reduced the FLRW amplitude problem to one number:

```text
kappa_mem.
```

This checkpoint asks the hardest version:

```text
Can a Ward identity or metric variation force kappa_mem = 1?
```

Short answer:

```text
No, not from the currently available Ward/conservation machinery.
```

But the no-go is now stronger and cleaner:

```text
diffeomorphism Ward identities and FLRW continuity are homogeneous under
S_mem -> lambda S_mem.
```

So they preserve the stress form for any `lambda`. They cannot pick `lambda=1`.

## Rescaling Proof

Take the reduced memory action family:

```text
S_mem[lambda] = -lambda rho_* integral sqrt(-g) q F(N).
```

Here:

```text
q = Tr(P_active)/dim(V_cell).
```

Metric variation gives:

```text
T_mem^munu[lambda] = lambda T_mem^munu[1].
```

So:

```text
rho_mem -> lambda rho_mem,
p_mem -> lambda p_mem,
S_mem_source -> lambda S_mem_source.
```

The FLRW continuity identity:

```text
rho_N = 3(rho+p)
```

becomes:

```text
lambda rho_N = 3(lambda rho + lambda p).
```

Therefore, if the identity holds for `lambda=1`, it holds for every constant `lambda`.

That proves:

```text
Bianchi/continuity cannot derive kappa_mem.
```

## Ward Identity Result

A diffeomorphism Ward identity can enforce:

```text
nabla_mu T_mem^munu = field equation terms + boundary terms.
```

But it is also linear in the action coefficient.

So the transformation:

```text
S_mem -> lambda S_mem
```

preserves the Ward identity.

This kills the shortcut:

```text
Ward identity exists, therefore kappa_mem = 1.
```

False.

The honest statement is:

```text
Ward identity can own conservation.
Ward identity does not own normalization unless it is a nonhomogeneous scale/anomaly/index identity.
```

## Route Audit

| Route | Can Set `kappa_mem`? | Verdict |
|---|---:|---|
| insert `rho_c0` | yes formally | calibration insertion, not parent derivation |
| geometric EH scale-lock | only if `H_star=H0` | reduces to an unproved scale theorem |
| diffeomorphism Ward identity | no | homogeneous rescaling no-go |
| trace/Weyl anomaly | possible | no anomaly/operator/level derived |
| boundary charge quantization | sets `q`, not `kappa` | still needs stress coupling |
| endpoint quadratic | sets `DeltaR` target only | endpoint coefficients/arrow not owned |

So the only live promotion route is:

```text
trace Ward / anomaly / index scale-lock
plus
boundary charge unit
plus
local silence.
```

That is a much narrower target than “derive the amplitude”.

## What Is Still Good

The empirical alignment remains interesting:

| Branch | `B_mem` | implied `kappa_mem` |
|---|---:|---:|
| DESI DR2 full-cov no-SH0ES fitted shape | 0.074533 | 1.006198 |
| DESI DR1 full-cov no-SH0ES fitted shape | 0.073418 | 0.991149 |
| DR2 kappa-free short smoke | 0.074533 | 1.006198 |

This says:

```text
kappa_mem = 1 is empirically well aligned.
```

It does not say:

```text
kappa_mem = 1 is derived.
```

That distinction is now locked.

## Required Future Theorem

To promote the amplitude, a future parent action must supply a nonhomogeneous scale-lock:

| Condition | Must Prove |
|---|---|
| `N1` | parent equation fixes `rho_*/rho_c0=1` and is not invariant under `rho_* -> lambda rho_*` |
| `N2` | real operator/complex/anomaly gives the level or stress coefficient before fitting |
| `N3` | boundary charge unit `Q_*` and endpoint occupancies are parent-selected |
| `N4` | trace partition sends one third of `DeltaR` into the background memory channel |
| `N5` | same coupling is null or volume-suppressed in local PPN domains |

Without `N1` or `N2`, the amplitude stays closure-only.

## Decision

Decision:

```text
kappa_mem_Ward_scale_lock_not_derived_rescaling_no_go_strengthened
```

Claim ceiling:

```text
kappa_mem_closure_only_until_nonhomogeneous_scale_lock_or_index_anomaly
```

Meaning:

```text
we can derive the stress form and conservation,
but not the unit normalization.
```

Boxing translation:

```text
The punch mechanics are real.
The glove weight is still not fixed by the rules.
To fix the glove weight, we need a weigh-in theorem: anomaly, index, or scale-lock.
```

## Next Target

The theory branch has now narrowed to:

```text
construct an explicit trace-anomaly/index operator that fixes kappa_mem,
or stop trying to promote kappa_mem for now.
```

The empirical branch should now test the actual lead closure:

```text
fully-fixed B_mem=2/27,
full-cov no-SH0ES,
DESI DR2 and DR1,
same LCDM/wCDM/CPL baselines,
same nuisance and covariance policy.
```

That is the cleanest next move because the derivation has identified exactly what is missing.

## Machine Artifacts

Script:

```text
scripts/kappa_mem_Ward_scale_lock_attempt.py
```

Run:

```text
runs/20260601-000144-kappa-mem-Ward-scale-lock-attempt
```

Output files:

```text
runs/20260601-000144-kappa-mem-Ward-scale-lock-attempt/results/source_register.csv
runs/20260601-000144-kappa-mem-Ward-scale-lock-attempt/results/ward_rescaling_proof.csv
runs/20260601-000144-kappa-mem-Ward-scale-lock-attempt/results/scale_lock_routes.csv
runs/20260601-000144-kappa-mem-Ward-scale-lock-attempt/results/necessary_conditions.csv
runs/20260601-000144-kappa-mem-Ward-scale-lock-attempt/results/empirical_kappa_readout.csv
runs/20260601-000144-kappa-mem-Ward-scale-lock-attempt/results/gate_results.csv
runs/20260601-000144-kappa-mem-Ward-scale-lock-attempt/results/decision.csv
```
