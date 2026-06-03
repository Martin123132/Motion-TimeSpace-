# Fresh Holdout or Official Likelihood Roadmap

## 1. Purpose

This file follows:

```text
39-calibrated-background-backreaction-guardrail.md
```

The question is:

```text
After the frozen CMB-calibrated closure row passes growth and late-background
guardrails, what is the next genuinely stronger test?
```

Short answer:

```text
the immediate local next test is a calibrated H(z) covariance guardrail. The
stronger route is official CMB spectra/lensing, but that is not locally ready
and needs a perturbation/early-sector contract before it can be honest.
```

## 2. Machine Run

Implemented:

```text
scripts/fresh_holdout_or_official_likelihood_roadmap.py
```

Successful run:

```text
runs/20260531-010340-fresh-holdout-or-official-likelihood-roadmap/status.json
```

Readout:

```text
fresh_holdout_roadmap_selects_Hz_guardrail_official_CMB_not_ready
```

## 3. Current State

The frozen CMB-calibrated row now has:

```text
compressed CMB distance fixed;
growth still near locked C0;
late-background SN/BAO not catastrophically worsened.
```

Still missing:

```text
fresh independent holdout;
official CMB likelihood;
parent H0/Omega_m0/b_mem map;
parent perturbation contract.
```

So the branch status remains:

```text
frozen closure candidate, not evidence.
```

## 4. Local Data Inventory

Local and usable as guardrail:

```text
cosmic_chronometers_covariance_branch
cosmic_chronometers_full_Hz
```

Already consumed in this post-checkpoint chain:

```text
Planck 2018 compressed distance prior;
SDSS/eBOSS BAO-plus growth;
SDSS/eBOSS full-shape growth;
Pantheon+/DESI late-background guardrail.
```

Not configured locally:

```text
official CMB spectra/lensing likelihood;
fresh external growth/RSD holdout.
```

## 5. Route Scorecard

Selected immediate route:

```text
calibrated_Hz_covariance_guardrail
```

Why:

```text
it is local, row-locked, covariance-aware, and was not used to train the frozen
CMB-calibrated row.
```

Caveat:

```text
H(z) was already studied in the main path, so this cannot become support. It is
only a guardrail on the new frozen calibrated row.
```

Strongest route:

```text
official_CMB_spectra_lensing_fixed_params
```

Caveat:

```text
not ready until the theory supplies a perturbation/early-sector contract, or we
explicitly label the run as a fixed-background stress test with no support claim.
```

## 6. Official Likelihood References

The official-likelihood route should be built from primary/tooling sources:

```text
Planck Legacy Archive CMB spectrum and likelihood code;
Cobaya cosmological theory/likelihood framework;
NASA LAMBDA ACT DR6 lensing likelihood data;
ACT DR6 data products.
```

No official-likelihood run is allowed until:

```text
the frozen background row is fixed;
baseline treatment is identical;
perturbation freedoms are locked or parent-derived;
the run writes a separate setup manifest.
```

## 7. Gate Result

Passed:

```text
source 39 complete;
local H(z) covariance guardrail exists;
next route selected.
```

Failed by design:

```text
official CMB likelihood ready now;
fresh external growth ready now;
support claim.
```

## 8. Decision

Next immediate target:

```text
41-calibrated-Hz-covariance-guardrail.md
```

Purpose:

```text
run the frozen native CMB-calibrated row against the local row-locked H(z)
covariance branch with no parameter rescue and equal baseline treatment.
```

Allowed language if it passes:

```text
the calibrated closure row also survives direct-H(z) guardrail.
```

Forbidden language:

```text
H(z) supports MTS;
the calibrated row is independently validated;
the official CMB problem is solved.
```
