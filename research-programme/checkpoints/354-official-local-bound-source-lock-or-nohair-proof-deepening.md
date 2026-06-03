# 354 - Official Local-Bound Source Lock Or No-Hair Proof Deepening

Private derivation checkpoint. This is not a public local-GR, PPN, WEP, clock, Cassini, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 353 left two paths:

```text
deepen the no-hair proof,
or source-lock the local-bound numbers before using the runner.
```

This checkpoint does both, but with a strict claim ceiling.

The source-lock result is:

```text
gamma, beta, WEP, and clock/redshift targets now have explicit source URLs.
```

The no-hair result is:

```text
A3-A7 are sharpened,
but not derived.
```

So the runner becomes less handwavy, but still not an official PPN pass.

## 2. Run Ledger

Script:

```text
scripts/official_local_bound_source_lock_or_nohair_proof_deepening.py
```

Run directory:

```text
runs/20260601-234500-official-local-bound-source-lock-or-nohair-proof-deepening
```

Command:

```text
python scripts/official_local_bound_source_lock_or_nohair_proof_deepening.py --timestamp 20260601-234500
```

Status:

```text
local_bound_source_lock_partial_gamma_beta_WEP_redshift_locked_nohair_deepened_no_local_GR_promotion
```

Claim ceiling:

```text
source_locked_targets_for_internal_runner_only_no_official_PPN_or_local_GR_pass_claim
```

Outputs:

```text
results/source_register.csv
results/external_source_lock.csv
results/source_locked_bound_manifest.csv
results/proxy_to_source_locked_delta.csv
results/nohair_proof_deepening.csv
results/runner_readiness_after_source_lock.csv
results/gate_results.csv
results/decision.csv
```

## 3. External Source Lock

The old runner in 353 used proxy scales.

This checkpoint records four external sources:

| Source | Use |
|---|---|
| Will, Living Reviews 2014 | PPN `gamma`, `beta`, Nordtvedt, preferred-frame sector map |
| PDG 2018 gravity-tests review | compact cross-check of `gamma`, `beta`, WEP, redshift, metric coupling |
| MICROSCOPE final result 2022 | WEP / Eotvos parameter for Ti-Pt |
| Galileo redshift PRL 2018 | clock/redshift violation parameter |

These source-locks are for internal runner targets only.
They are not a public pass/fail claim.

## 4. Source-Locked Target Scales

The source-locked internal target manifest is now:

| Residual | Internal target scale | Source status | Runner status |
|---|---:|---|---|
| `gamma - 1` | `2.3e-5` | Cassini / review locked | ready internal |
| `beta - 1` | `7.8e-5` | Mercury/Messenger / review locked | ready internal |
| `eta_WEP` | `2.8e-15` | MICROSCOPE final locked | ready internal |
| `alpha_clock_redshift` | `3.1e-5` | Galileo redshift locked | ready internal |
| preferred-frame `alpha1/alpha2` | not numeric locked here | sector identified only | quarantined |
| preferred-location / anisotropy `xi` | not numeric locked here | sector identified only | quarantined |
| fifth-force / `delta_G` | not numeric locked here | needs dedicated source | quarantined |

This improves the runner because:

```text
gamma/beta/WEP/clock are no longer arbitrary proxy rows.
```

But it also tightens discipline:

```text
preferred-frame, anisotropy, and fifth-force rows cannot be scored yet.
```

## 5. Proxy Replacement Audit

The previous proxy values compare as:

| Residual | Old proxy | Source-locked scale | Update |
|---|---:|---:|---|
| `gamma - 1` | `2.3e-5` | `2.3e-5` | matches |
| `beta - 1` | `8.0e-5` | `7.8e-5` | matches |
| `eta_WEP` | `1.0e-14` | `2.8e-15` | proxy too loose |
| `alpha_clock_redshift` | `1.0e-6` | `3.1e-5` | proxy was not a sourced redshift scale |
| preferred-frame | `4.0e-7` | none | quarantined |
| anisotropy | `1.0e-3` | none | quarantined |
| fifth force | `1.0e-10` | none | quarantined |

This is exactly why source-locking matters.
Some proxy numbers were fine as rough pressure tests; others were either too loose, too strict, or not attached to the correct observable.

## 6. No-Hair Proof Deepening

The no-hair theorem still has the same hard debts, but they are sharper now.

### A3 - Class-Only Boundary Action

If:

```text
S_boundary = S_boundary(total relative class, total charge, induced scalar volume)
```

and not:

```text
S_boundary = S_boundary(angular representatives, marked patches, local anisotropic frame)
```

then trace-free shear and `l >= 2` multipoles have nowhere to enter.

This would kill:

```text
B_TF,ij.
```

Status:

```text
conditional template, not parent-derived.
```

### A4 - No Marker Fields

If boundary markers, active patch labels, and preferred normals are gauge choices rather than physical fields, then local vector/preferred-frame residuals are forbidden.

This would kill:

```text
B_0i.
```

Status:

```text
open.
```

### A5 - No Radial Scalar Hair

An isolated regular exterior can allow a monopole `1/r` contribution.

That is safe only if it is:

```text
universal,
conserved,
and absorbed into measured GM.
```

If the radial trace term carries independent scalar charge, then it is not safe.

Status:

```text
partly sharpened, not closed.
```

### A6 - Single Metric Coupling

Even if the metric field equation becomes Einstein-Hilbert, local tests fail if clocks, rods, photons, and matter do not see the same physical metric/coframe.

This is now the WEP/clock hinge:

```text
C_clock = 0,
C_WEP = 0.
```

Status:

```text
open hard gate.
```

### A7 - Boundary Ward / Bianchi Closure

Boundary flux must be:

```text
zero,
or exactly balanced by an owned conserved boundary charge.
```

Otherwise the theory has fake conservation.

Status:

```text
open hard gate.
```

## 7. Runner Readiness After 354

| Runner sector | Readiness | Reason |
|---|---:|---|
| `gamma/beta` scalar-metric sector | ready internal | source-locked target scales exist |
| WEP/clock sector | ready internal | MICROSCOPE and Galileo scales locked |
| preferred-frame/anisotropy | not ready | numeric bounds not ingested here |
| fifth-force / inverse-square sector | not ready | needs dedicated source lock |

No MTS residual coefficient has been derived yet.

So even ready sectors are:

```text
internal target scales,
not pass/fail evidence.
```

## 8. Gate Results

| Gate | Result | Meaning |
|---|---:|---|
| local source paths exist | pass | cited checkpoints and script exist |
| external sources recorded | pass | four URLs recorded |
| numeric bounds source-locked | partial pass | four target scales locked, three sectors quarantined |
| proxy values replaced/quarantined | pass | proxy table audited |
| no-hair proof deepened | partial pass | A3-A7 sharpened but not derived |
| official PPN pass allowed | fail | no residual coefficients and incomplete source lock |
| local GR promoted | fail | A3-A7 remain open |
| claim ceiling enforced | pass | no local-GR/PPN claim |

## 9. Decision

```text
local_bound_source_lock_partial_gamma_beta_WEP_redshift_locked_nohair_deepened_no_local_GR_promotion
```

This is good progress, but not glory.

The local branch now has:

```text
better experimental scorecards,
sharper no-hair debts,
and fewer proxy numbers pretending to be official.
```

But it still lacks:

```text
derived residual coefficients,
preferred-frame numeric source lock,
fifth-force source lock,
single-metric coupling proof,
boundary Ward proof,
and no-hair theorem.
```

## 10. Next Target

Next checkpoint:

```text
355-source-locked-local-bound-runner-with-open-sector-quarantine.md
```

Task:

```text
build the local-bound runner using only source-locked sectors,
quarantine preferred-frame / anisotropy / fifth-force rows,
and report what residual amplitudes would be required for gamma, beta, WEP, and clock safety.
```

No pass/fail claim until the MTS residual coefficients are derived or bounded from the parent action.
