# 127 - Radial Pressure Decision Gate

Private checkpoint. This is not a public claim.

## 1. Trigger

The last two empirical gates gave a clean but incomplete picture:

```text
124: the joint BAO penalty is mostly radial, dominated by DH/rs.
126: independent H(z) data tolerate locked MTS at LCDM-draw level.
```

So the decision is whether to:

```text
derive immediately,
test more without CMB,
move to growth,
or return to local-GR/PPN.
```

## 2. Evidence Summary

From checkpoint 124:

```text
failed joint gate BAO delta vs T7 = 4.84109052998793
dominant observable = DH_over_rs
dominant redshift group = z = 0.934
```

From checkpoint 126:

```text
MTS_locked_2over27 vs LCDM on primary H(z):
Delta BIC = +0.33256956910347313
```

Interpretation:

```text
H(z) does not prove the BAO radial-pressure story,
but it does not reject it either.
```

## 3. Route Options

| Route | Status | Decision |
|---|---|---|
| radial `D_H/H(z)` theorem now | premature | needs sharper no-CMB evidence first |
| BAO+H(z) diagnostic without CMB | ready | run next |
| growth / `f\sigma_8` | important | queue after no-CMB radial diagnostic |
| local-GR/PPN derivation | mandatory | keep parallel, but not the answer to this residual |

## 4. Decision

Run:

```text
BAO + H(z), no CMB.
```

Rules:

```text
DESI DR2 BAO shape + cosmic chronometer H(z)
BAO alpha profiled as a nuisance
no CMB priors
no MTS-only BAO-shape correction
no fitted Omega map
same data and covariance for baselines and MTS
```

This tests whether the locked branch remains competitive when the two radial
datasets are combined without letting compressed CMB priors act as referee.

## 5. Acceptance Gates

1. Score:

```text
LCDM, wCDM, CPL, MTS_locked_2over27, MTS_Bmem_zero.
```

2. Count BAO alpha as a nuisance parameter.

3. Report:

```text
BAO chi2
H(z) chi2
total chi2
AIC
BIC
edge flags
```

4. Primary branch:

```text
DESI DR2 BAO + CC15 suggested covariance.
```

5. Sensitivities:

```text
CC15 covariance variants
CC32 diagonal-only
```

6. Promotion is forbidden.

## 6. Next Target

Next checkpoint:

```text
128-BAO-Hz-noCMB-diagnostic.md
```

Script:

```text
scripts\BAO_Hz_noCMB_diagnostic.py
```

Claim ceiling:

```text
no-CMB radial diagnostic only.
```

