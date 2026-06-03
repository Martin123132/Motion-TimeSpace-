# Calibrated H(z) Covariance Guardrail

## 1. Purpose

This file follows:

```text
40-fresh-holdout-or-official-likelihood-roadmap.md
```

The question is:

```text
Does the frozen native CMB-calibrated C0 row survive the local row-locked H(z)
covariance branch without parameter rescue?
```

Short answer:

```text
yes as a guardrail, not as support. The frozen calibrated row is better than
the locked C0 row across all four covariance variants, and is essentially tied
with LCDM under the suggested covariance.
```

## 2. Machine Run

Implemented:

```text
scripts/calibrated_Hz_covariance_guardrail.py
```

Successful run:

```text
runs/20260531-010754-calibrated-Hz-covariance-guardrail/status.json
```

Readout:

```text
calibrated_Hz_covariance_guardrail_passes_not_support
```

## 3. Suggested Covariance Result

Suggested covariance:

```text
LCDM chi2 = 6.222197692674048
locked C0 chi2 = 6.487301338819241
frozen native CMB-calibrated C0 chi2 = 6.227876470664499
```

Frozen native CMB-calibrated C0:

```text
delta chi2 vs locked C0 = -0.25942486815474197
delta chi2 vs best baseline = +0.005678777990450357
```

So the frozen CMB-calibrated row is:

```text
better than locked C0;
nearly tied with LCDM under the suggested covariance.
```

## 4. Covariance Variants

Frozen native CMB-calibrated C0 delta versus locked C0:

```text
diagonal_total_error = -0.3330771661876426
suggested = -0.25942486815474197
conservative = -0.26488499568152246
extra_conservative = -0.24985441921630347
```

This passes the no-rescue H(z) guardrail.

## 5. Why This Still Is Not Support

This H(z) branch was already used in the main corpus to show:

```text
direct H(z) does not independently support the original fixed-shape M6 branch.
```

The new result is narrower:

```text
the CMB-calibrated frozen row does not fail the same H(z) covariance guardrail.
```

Allowed:

```text
H(z) does not kill the frozen calibrated closure row.
```

Forbidden:

```text
H(z) supports MTS;
the calibrated row is independently validated;
the official CMB problem is solved.
```

## 6. Gate Result

Passed:

```text
source 40 complete;
frozen native row evaluated across all covariance variants;
suggested covariance not worse than locked C0 by 2;
all covariance variants not worse than locked C0 by 3;
native calibrated row beats locked C0 in all four variants.
```

Failed by design:

```text
support claim;
official CMB problem solved.
```

## 7. Current Closure Ledger

The frozen native CMB-calibrated C0 row now has:

```text
compressed CMB distance fixed;
growth near locked C0;
late-background SN/BAO backreaction pass;
direct H(z) covariance guardrail pass.
```

Still missing:

```text
fresh independent holdout;
official spectra/lensing likelihood;
parent H0/Omega_m0/b_mem map;
parent perturbation contract.
```

## 8. Next Target

Create:

```text
42-calibrated-closure-candidate-ledger.md
```

Purpose:

```text
package the closure candidate status honestly: what has survived, what remains
unproven, and what exact gates must pass before evidence language is permitted.
```
