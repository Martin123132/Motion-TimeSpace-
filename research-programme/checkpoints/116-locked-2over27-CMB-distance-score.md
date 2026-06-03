# 116 - Locked 2/27 CMB Distance Score

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 115 declared the fair CMB parameter-map contract:

```text
h and Omega_m0 fitted symmetrically for every branch;
Omega_b h2 and n_s fixed to each compressed prior table mean;
scale-factor sound-horizon quadrature only;
wCDM and LCDM compressed prior tables both required.
```

This checkpoint implements and runs the guarded score.

## 2. Short Verdict

```text
CMB_distance_score_status =
locked_2over27_CMB_distance_score_competitive_or_better_vs_LCDM
```

```text
theory_promotion_allowed =
false
```

```text
CMB_public_claim_allowed =
false
```

Plain English:

```text
The locked B_mem=2/27 branch is not killed by the compressed CMB distance prior
when h and Omega_m0 are fitted fairly for every model.
```

But the important caveat is:

```text
this score is nearly non-discriminating.
```

All simple branches can fit the compressed distance-prior observables almost exactly once `h` and `Omega_m0` are free.

So this is a survival result, not a support result.

Boxing-score version:

```text
MTS stayed on its feet and did not lose the round, but the round was mostly
about calibration footwork rather than heavy punches.
```

## 3. Machine Artifact

Script:

```text
research-programme\scripts\locked_2over27_CMB_distance_score.py
```

Dry-run:

```text
research-programme\runs\20260531-160859-locked-2over27-CMB-distance-score-dryrun
```

Score run:

```text
research-programme\runs\20260531-161215-locked-2over27-CMB-distance-score
```

Generated:

```text
source_register.csv
prior_table_register.csv
model_register.csv
parameter_map_register.csv
fit_summary.csv
prior_edge_table.csv
distance_prior_residuals.csv
baseline_comparisons.csv
scorecard_gates.csv
decision.csv
status.json
```

## 4. Score Contract

Primary prior tables:

```text
wCDM
LCDM
```

Score modes:

```text
strict_full4 = R, l_A, Omega_b_h2, n_s
marginal_R_lA = R, l_A
```

Models:

```text
LCDM
wCDM
CPL
MTS_locked_2over27
MTS_Bmem_zero
```

Locked branch:

```text
p = 3
u3 = 1/4
DeltaR = 2/9
B_mem = 2/27
```

No CMB-specific retuning was allowed.

## 5. Locked Branch Fits

| Prior table | Score mode | chi2 | Omega_m0 | h | Edge flag |
|---|---|---:|---:|---:|---|
| `wCDM` | `strict_full4` | 1.9856415095050835e-09 | 0.3295740146787432 | 0.6671371381879377 | false |
| `wCDM` | `marginal_R_lA` | 1.3218987894658261e-09 | 0.32957399350906025 | 0.6671371660320761 | false |
| `LCDM` | `strict_full4` | 1.5635293638699566e-09 | 0.331286732138333 | 0.6659279626767358 | false |
| `LCDM` | `marginal_R_lA` | 2.1248054813659225e-09 | 0.3312867941619584 | 0.6659279085720234 | false |

Interpretation:

```text
the CMB-only fitted locked branch prefers Omega_m0 about 0.330-0.331 and
h about 0.666-0.667.
```

These are not edge solutions.

## 6. LCDM Comparisons

| Prior table | Score mode | Delta chi2 vs LCDM | Delta AIC vs LCDM | Delta BIC vs LCDM | Scorecard |
|---|---|---:|---:|---:|---|
| `wCDM` | `strict_full4` | 4.433844434692235e-10 | 4.433848843632404e-10 | 4.433844434692235e-10 | competitive draw |
| `wCDM` | `marginal_R_lA` | -2.3411718256042797e-09 | -2.3411717009480526e-09 | -2.3411718256042797e-09 | competitive draw |
| `LCDM` | `strict_full4` | 1.1981717887141212e-09 | 1.1981722281007023e-09 | 1.1981717887141212e-09 | competitive draw |
| `LCDM` | `marginal_R_lA` | -6.525917953746776e-10 | -6.525917584099261e-10 | -6.525917953746776e-10 | competitive draw |

These are machine-zero differences.

Readout:

```text
MTS_locked_2over27 and LCDM are indistinguishable under this compressed
CMB-distance-only calibration score.
```

That is not a win by data separation.

It is a useful survival/draw result.

## 7. Flexible Baseline Comparisons

Against `wCDM`:

| Prior table | Score mode | Delta chi2 | Delta AIC | Delta BIC | Scorecard |
|---|---|---:|---:|---:|---|
| `wCDM` | `strict_full4` | 1.9845678585379213e-09 | -1.999999998015432 | -1.3862943591353221 | points win |
| `wCDM` | `marginal_R_lA` | 1.2911278500829164e-09 | -1.999999998708872 | -0.6931471792688173 | points win |
| `LCDM` | `strict_full4` | 1.535950717832583e-09 | -1.999999998464049 | -1.3862943595839394 | points win |
| `LCDM` | `marginal_R_lA` | 2.100064993132123e-09 | -1.999999997899935 | -0.6931471784598804 | points win |

Against `CPL`:

| Prior table | Score mode | Delta chi2 | Delta AIC | Delta BIC | Scorecard |
|---|---|---:|---:|---:|---|
| `wCDM` | `strict_full4` | 1.9798625838907707e-09 | -3.9999999980201366 | -2.772588720259918 | clean win |
| `wCDM` | `marginal_R_lA` | 1.2764023056516898e-09 | -3.999999998723597 | -1.3862943598434882 | points win |
| `LCDM` | `strict_full4` | 1.5561694244136539e-09 | -3.9999999984438297 | -2.7725887206836115 | clean win |
| `LCDM` | `marginal_R_lA` | 1.931908534788295e-09 | -3.999999998068091 | -1.386294359187982 | points win |

Reason:

```text
wCDM and CPL can also fit the compressed CMB distance priors, but they spend
extra parameters to do it.
```

This is a parsimony result, not a unique-prediction result.

## 8. Edge Flags

Total edge table rows:

```text
52
```

Edge-hit rows:

```text
0
```

Locked branch edge count:

```text
0
```

This is important:

```text
the survival result is not a prior-edge artifact.
```

## 9. Why This Does Not Contradict the Earlier CMB Tension

Earlier repaired CMB scoring used fixed late-time background rows from the old branch.

That test asked:

```text
does the previous late-time parameter set transfer directly into CMB distance?
```

This checkpoint asks a different question:

```text
can each model fit compressed CMB distance priors when h and Omega_m0 are
fitted symmetrically?
```

Answer:

```text
yes, almost all of them can.
```

Therefore the actual issue has sharpened:

```text
not "can MTS fit compressed CMB distances at all?",
but "can the same MTS parameter map fit late-time SN/BAO and CMB without
changing calibration rules?"
```

## 10. Interpretation

Allowed statement:

```text
The locked B_mem=2/27 branch survives a guarded compressed CMB distance-prior
score when h and Omega_m0 are fitted under the same rules as LCDM/wCDM/CPL.
```

Allowed statement:

```text
The result is essentially a CMB-distance calibration draw against LCDM, with
no edge-hit pathology.
```

Forbidden statement:

```text
MTS passes CMB.
```

Forbidden statement:

```text
MTS predicts CMB distances from first principles.
```

Forbidden statement:

```text
CMB now supports MTS.
```

## 11. Decision

The result is better than the earlier fixed-parameter CMB tension, but weaker than a real CMB victory.

Status:

```text
survives_compressed_CMB_distance_as_non_discriminating_calibration_draw
```

This is strategically good:

```text
the branch is not dead on CMB distance geometry.
```

But it is not enough:

```text
CMB-only h/Omega_m0 freedom makes the test too easy.
```

## 12. Next Target

Create:

```text
117-locked-2over27-late-CMB-transfer-gate.md
```

Purpose:

```text
test whether the CMB-only calibrated values Omega_m0 about 0.330-0.331 and
h about 0.666-0.667 can be connected to the late-time SN/BAO branch without
silently changing the calibration map.
```

The next real discriminator is not another CMB-only fit.

It is:

```text
late-time fit -> CMB transfer,
or joint late+CMB fit with one shared parameter set.
```
