# 147 - ELG Grid Likelihood Holdout

Private empirical checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 146 passed the source-locked SDSS/eBOSS Gaussian growth covariance holdout, but it still excluded the ELG grid likelihood because ELG is not well approximated by a simple Gaussian covariance file.

This checkpoint closes that obvious gap:

```text
parse the eBOSS DR16 ELG non-Gaussian grid likelihood.
```

Question:

```text
Does frozen B_mem = 2/27 survive the ELG grid likelihood?
```

Short answer:

```text
yes, as a clean competitive draw.
```

It neither wins nor loses the ELG round by itself. That is still useful, because it means the missing non-Gaussian ELG branch does not reverse the growth scorecard.

## 2. Machine Artifact

Script:

```text
research-programme\scripts\ELG_grid_likelihood_holdout.py
```

Run:

```text
research-programme\runs\20260531-231500-ELG-grid-likelihood-holdout
```

Fetched source intake:

```text
research-programme\source-intake\sdss_eboss_dr16_elg_grid\20260531-231500
```

Generated:

```text
source_register.csv
fetch_hash_lock.csv
grid_schema.csv
fit_summary.csv
baseline_comparisons.csv
control_reproduction.csv
nearest_grid_offsets.csv
combined_gaussian_plus_ELG_diagnostic.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
ELG_grid_primary_competitive_draw
```

Claim ceiling:

```text
ELG_grid_likelihood_holdout_no_perturbation_or_CMB_promotion
```

## 3. Source Lock

Fetched files:

```text
README.txt
sdss_DR16_ELG_FSBAO_DMDHfs8gridlikelihood.txt
```

Source root:

```text
https://svn.sdss.org/public/data/eboss/DR16cosmo/tags/v1_0_1/likelihoods/
```

Hash lock:

```text
fetched files = 2
failures = 0
```

The ELG grid file is:

```text
60,331,968 bytes
```

and matches both the local source manifest and the local formalization-workbench copy.

## 4. Grid Schema

The ELG likelihood is a relative-probability grid over:

```text
D_M(z_eff)/r_d
D_H(z_eff)/r_d
f sigma_8(z_eff)
```

The SDSS README states that the ELG likelihood is not well approximated as Gaussian, so a grid of relative probability is used.

The effective redshift used here is:

```text
z_eff = 0.85
```

This matches the eBOSS DR16 ELG BAO/RSD literature for the ELG sample.

Grid:

| Quantity | Value |
|---|---:|
| rows | `1000000` |
| shape | `100 x 100 x 100` |
| `D_M/r_d` range | `[10.4408648, 35.5453295]` |
| `D_H/r_d` range | `[7.59609571, 33.5029314]` |
| `fσ8` range | `[0.0160668366, 0.731336079]` |
| max probability | `1.0` |
| positive rows | `897452` |
| zero-probability rows | `102548` |

Best grid point:

```text
D_M/r_d = 19.5697611
D_H/r_d = 20.1569858
fσ8 = 0.268939801
```

## 5. Fairness Contract

Same as the previous growth gates:

```text
fixed no-CMB late-time backgrounds
frozen B_mem = 2/27
shared fitted sigma8_0 only
same test applied to LCDM, wCDM, CPL, MTS locked, and MTS Bmem-zero
```

The grid likelihood is interpolated in log-probability space.

Zero-probability cells are floored only for numerical stability:

```text
probability floor = 1e-300
```

All model predictions landed inside the grid.

## 6. Primary ELG Result

DR2 no-CMB primary background:

| Model | `D_M/r_d` | `D_H/r_d` | `sigma8_0` | `fσ8` | Grid chi2 |
|---|---:|---:|---:|---:|---:|
| LCDM | `20.176158769910483` | `18.358305029487767` | `0.6459980807316362` | `0.35563911953416777` | `0.6557588375955071` |
| wCDM | `20.178563868408656` | `18.254340866161794` | `0.6703674151772693` | `0.36286401285836983` | `0.7311754653368334` |
| CPL | `20.153525093532142` | `18.267604507486794` | `0.6395899844036588` | `0.35563920254935544` | `0.6970077815097433` |
| MTS locked 2/27 | `20.17112838757099` | `18.29099073762001` | `0.6506390913511579` | `0.3556392725840205` | `0.6932606383399861` |
| MTS Bmem-zero | `20.176158769910483` | `18.358305029487767` | `0.6459980807316362` | `0.35563911953416777` | `0.6557588375955071` |

MTS locked vs LCDM:

```text
Delta chi2 = +0.03750180074447895
```

Readout:

```text
competitive draw
```

MTS locked vs wCDM:

```text
Delta chi2 = -0.03791482699684734
```

MTS locked vs CPL:

```text
Delta chi2 = -0.0037471431697572166
```

So the ELG grid does not pick a winner among these branches at meaningful strength.

## 7. Diagnostic Combination

Adding the ELG grid delta to the previous Gaussian BAO-plus all-row delta gives:

| Background | Gaussian Delta vs LCDM | ELG Delta vs LCDM | Sum | Readout |
|---|---:|---:|---:|---|
| DR2 primary | `-2.3035702803557125` | `0.03750180074447895` | `-2.2660684796112336` | locked preferred |
| DR1 release sensitivity | `-2.5501137065853374` | `0.047092508755774865` | `-2.5030211978295624` | locked preferred |

Important:

```text
this is a diagnostic sum only.
```

It is not an official joint likelihood wrapper. It is still useful because it tells us the ELG grid does not erase the previous Gaussian growth preference/draw card.

## 8. Gates

| Gate | Status | Evidence |
|---|---|---|
| source fetch hash lock | pass | 2 files |
| grid schema | pass | `100 x 100 x 100`, 1,000,000 rows |
| prediction inside grid | pass | 10 fit rows |
| frozen `B_mem` no refit | pass | only `sigma8_0` profiled for every model |
| negative control | pass | Bmem-zero reproduces LCDM |
| primary ELG not disfavored | pass | competitive draw |
| official joint claim | fail | diagnostic sum only |
| theory promotion | fail | no perturbation action, local GR, or CMB theorem |

## 9. Judge's Card

Boxing version:

```text
ELG is a quiet round.
Nobody lands a decisive shot.
MTS does not lose it.
```

That matters because ELG was the missing non-Gaussian growth/geometry branch. If this had blown up, the previous growth card would have looked suspiciously Gaussian-only.

Instead:

```text
ELG preserves the late-time survival story.
```

The honest statement is:

```text
the frozen branch survives the source-locked non-Gaussian ELG grid likelihood as a draw.
```

The stronger internal statement is:

```text
the late-time empirical branch has now survived SN+BAO, BAO-only, BAO+H(z), source-locked H(z), Gaussian SDSS/eBOSS growth covariance, jackknifes, and the non-Gaussian ELG grid.
```

Still forbidden:

```text
MTS derives perturbations.
MTS passes CMB.
MTS derives local GR.
MTS is a completed unified theory.
```

## 10. Next Target

The obvious empirical gaps are now higher-level:

```text
official_likelihood_wrapper_or_CMB_perturbation_contract
```

Two clean routes:

1. build a wrapper that reproduces the current late-time stack from official likelihood modules/configs;
2. return to theory and write the CMB/perturbation contract needed before any serious CMB claim.

My read:

```text
one more empirical integration checkpoint is useful, but the real title fight is now perturbations/CMB/local-GR derivation.
```
