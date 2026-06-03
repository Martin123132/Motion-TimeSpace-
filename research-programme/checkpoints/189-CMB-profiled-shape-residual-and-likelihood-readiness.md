# 189 - CMB Profiled Shape Residual and Likelihood Readiness

Private CMB pipeline checkpoint. This is not a public CMB claim.

## 1. Trigger

Checkpoint 188 found:

```text
theta compensation is not derived,
but H0 profiling can force theta* to match.
```

The next question is not whether we can shout victory. We cannot.

The useful question is:

```text
after theta* is explicitly matched, are the remaining CMB shape residuals small
enough to justify a real matched likelihood stage?
```

This checkpoint extends the profiled spectra comparison to:

```text
lmax = 1000
```

and keeps the claim ceiling bolted down.

## 2. Machine Artifact

Script:

```text
scripts/CMB_profiled_shape_residual_and_likelihood_readiness.py
```

Run:

```text
runs/20260601-000006-CMB-profiled-shape-residual-and-likelihood-readiness
```

Command:

```text
python scripts/CMB_profiled_shape_residual_and_likelihood_readiness.py --timestamp 20260601-000006
```

Status:

```text
CMB_profiled_shape_residuals_quantified_likelihood_readiness_open_no_claim
```

Claim ceiling:

```text
profiled_shape_residual_proxy_only_no_official_likelihood_no_CMB_claim
```

## 3. Derivation Pressure Ledger

Current derivation status:

| object | status | derivable now |
|---|---|---|
| `B_mem=2/27` | empirical locked closure / theorem target | no |
| `p=3,u3=1/4` activation | locked regularized activation closure | partial |
| high-`c_s` perturbation owner | effective scalar branch | partial/effective only |
| theta compensation | not derived; H0 profile quantified | no |
| local GR / PPN silence | screened effective branch, not parent-owned | no |

So the theory status is still:

```text
interesting effective branch with live derivation debts,
not a completed fundamental derivation.
```

## 4. Extended Shape Residuals

The two profiled MTS branches were rerun against their matched LCDM controls to
`lmax=1000`.

### Same-physical-density profile

This is the branch where physical densities are held as in checkpoint 183, and
MTS pays the theta cost by moving to:

```text
H0 = 65.92050790786743
```

Residual summary:

| band | RMS `Delta TT/TT` | RMS `Delta EE/EE` | max `|Delta TT/TT|` |
|---|---:|---:|---:|
| low `ell=2..29` | `0.003774830464393818` | `0.001009441000689574` | `0.013754942713195875` |
| acoustic `ell=30..200` | `0.00013209473870415205` | `0.000013362326004225307` | `0.0006176619509336372` |
| extended `ell=201..1000` | `0.000020920026621696776` | `0.0000596862002261587` | `0.00006815117912010139` |
| all `ell=2..1000` | `0.0006346008821986184` | `0.0001773220832776728` | `0.013754942713195875` |

Readout:

```text
Once theta* is matched, the same-density high-ell shape residual is tiny in
this smoke test.
```

But:

```text
this is not the locked-transfer theorem branch, and it costs a low H0.
```

### Locked-Omega_m profile

This branch keeps the locked matter fraction and profiles:

```text
H0 = 67.53464937210083
```

Residual summary:

| band | RMS `Delta TT/TT` | RMS `Delta EE/EE` | max `|Delta TT/TT|` |
|---|---:|---:|---:|
| low `ell=2..29` | `0.010775307404885186` | `0.013109239148399312` | `0.020175933750619993` |
| acoustic `ell=30..200` | `0.011923194870684443` | `0.0032177675458014902` | `0.013265906390895225` |
| extended `ell=201..1000` | `0.00828858519770164` | `0.01268716766604675` | `0.012262989753960412` |
| all `ell=2..1000` | `0.009088670038048426` | `0.011639985695432386` | `0.020175933750619993` |

Readout:

```text
The locked-Omega_m profile is still a pressure branch: theta can be forced, but
percent-level shape residuals remain.
```

## 5. Likelihood Readiness

Readiness matrix:

| item | status | reason |
|---|---|---|
| same-density profiled branch | ready for mock likelihood | high-ell shape residual is small after theta matching |
| locked-`Omega_m` profiled branch | stress-test only before claim | residuals remain around percent level |
| official likelihood assets | not ready locally | no Planck/ACT/SPT likelihood was invoked |
| derivation-first requirement | open | theta theorem still failed |

The next fair move is therefore:

```text
run a matched mock likelihood first, or build official likelihood readiness,
but do not count H0 profiling as a theory win.
```

## 6. Boxing-Card Read

MTS did not get knocked out here.

Actually, there is a useful split:

```text
same-density profiled branch:
  surprisingly clean CMB shape after theta matching,
  but asks for H0 around 65.92 and is not a derivation.

locked-Omega_m branch:
  closer to declared late-time lock,
  but CMB shape remains rougher.
```

So the best current stance is:

```text
MTS deserves a proper matched CMB likelihood stress test,
but the fundamental theory still owes a derivation of why the theta/H0
compensation should exist.
```

## 7. Claim Gates

| gate | result |
|---|---|
| all cited sources exist | pass |
| extended CAMB branches ran | pass |
| profiled residuals logged | pass |
| theta compensation derived | fail |
| official likelihood run | not run |
| support claim allowed | fail |

## 8. Decision

Decision:

```text
CMB_profiled_shape_residuals_quantified_likelihood_readiness_open_no_claim
```

Meaning:

```text
The same-density profiled CMB branch is clean enough to justify a matched mock
likelihood. The locked-Omega_m branch remains a CMB pressure branch. Neither is
a CMB claim because theta compensation is not derived and no official likelihood
has been run.
```

Next target:

```text
190-CMB-matched-mock-likelihood-or-derivation-pivot.md
```
