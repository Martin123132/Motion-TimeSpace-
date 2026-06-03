# 186 - CAMB High-cs W-table Spectra Smoke

Private CMB pipeline checkpoint. This is not a public CMB claim.

## 1. Trigger

Checkpoint 185 found that installed CAMB can accept the locked no-clock MTS
memory background as a tabulated dark-energy equation of state:

```text
DarkEnergyFluid.set_w_a_table(a,w_mem), cs2 = 1
```

The legal next move was therefore a tiny spectra smoke:

```text
same physical-density baseline,
same CAMB engine,
LCDM control rerun,
MTS high-cs fluid branch,
MTS PPF comparator branch.
```

No official likelihood is run.

No CMB support claim is allowed.

## 2. Machine Artifact

Script:

```text
scripts/CAMB_high_cs_wtable_spectra_smoke.py
```

Run:

```text
runs/20260601-000003-CAMB-high-cs-wtable-spectra-smoke
```

Command:

```text
python scripts/CAMB_high_cs_wtable_spectra_smoke.py --timestamp 20260601-000003
```

Status:

```text
CAMB_high_cs_wtable_spectra_smoke_ran_no_likelihood_theta_shift_flagged
```

Claim ceiling:

```text
tiny_CAMB_spectra_smoke_only_no_official_likelihood_no_CMB_claim
```

## 3. Branches Run

All three tiny CAMB branches ran successfully to `lmax=200`:

| branch | CAMB dark-energy model | status | runtime |
|---|---|---|---:|
| `LCDM_baseline_recomputed` | `lcdm` | pass | `0.730154 s` |
| `MTS_high_cs_fluid_density_isolation` | `fluid` | pass | `1.171792 s` |
| `MTS_high_cs_PPF_density_isolation` | `ppf` | pass | `1.086672 s` |

The fair-comparison rule here is narrow but clean:

```text
use checkpoint-183 H0, ombh2, omch2, tau, As, ns, mnu, omk for all branches;
change only the dark-energy w(a) shape for MTS.
```

That means this is a same-ring pipeline test, not the final locked-transfer
MTS cosmology fit.

## 4. First Result

Good news:

```text
The locked high-c_s MTS w(a) table produces finite CAMB TT/TE/EE spectra.
```

Bad / serious news:

```text
The raw acoustic scale shifts by about 0.459% under the same-density smoke.
```

That is too large to wave away in precision CMB work. It does not kill the
branch by itself because no parameter fit or locked-transfer branch has been
run, but it absolutely blocks any CMB support claim.

## 5. Acoustic-Scale Readout

For the high-cs fluid branch:

| quantity | LCDM | MTS high-cs fluid | fractional shift |
|---|---:|---:|---:|
| `thetastar` | `1.0415969851026594` | `1.046381835941041` | `0.004593764101486964` |
| `DAstar` | `13.867212878935597` | `13.803796491246283` | `-0.004573117052644635` |
| `rdrag` | `147.10139220381296` | `147.10122955697344` | `-1.1056784513767072e-06` |
| `age` | `13.78435583509` | `13.663830724950895` | `-0.008743615703266462` |

Interpretation:

```text
The early sound horizon barely moves. The main raw effect is the late-distance
projection to last scattering.
```

So the immediate hazard is not recombination physics blowing up. It is the
distance/acoustic-angle fit.

## 6. Spectra Residual Summary

Against the recomputed LCDM control:

| branch | max `|Delta TT/TT|` | RMS `Delta TT/TT` | max `|Delta EE/EE|` | RMS `Delta EE/EE` | theta warning |
|---|---:|---:|---:|---:|---|
| `MTS_high_cs_fluid_density_isolation` | `0.019454041701553453` | `0.005663957966212873` | `0.016549318063957163` | `0.010297919233828346` | yes |
| `MTS_high_cs_PPF_density_isolation` | `0.0270954556992222` | `0.006224938044252074` | `0.01654925561701868` | `0.010297891258279172` | yes |

Fluid and PPF are close for the main background/acoustic readout, as expected
for this non-phantom high-cs table. The low-ell differences are not an evidence
claim; they are smoke-test diagnostics.

## 7. Claim Gates

| gate | result |
|---|---|
| all cited sources exist | pass |
| LCDM baseline recomputed | pass |
| MTS high-cs fluid spectra run | pass |
| MTS PPF comparator spectra run | pass |
| raw `thetastar` shift | warning |
| exact auxiliary spectra | blocked |
| official likelihood | not run |
| support claim allowed | fail |

So the score is:

```text
pipeline survives,
CMB support not established,
acoustic-scale hazard now identified cleanly.
```

This is useful because it turns the CMB problem from a vague fear into a specific
target:

```text
Can the locked-transfer branch, with declared density conventions and no rescue
knobs, reduce the theta* hazard without breaking the rest of the theory?
```

## 8. Decision

Decision:

```text
CAMB_high_cs_wtable_spectra_smoke_ran_no_likelihood_theta_shift_flagged
```

Meaning:

```text
The locked MTS high-cs background is CAMB-runnable and does not immediately
explode as spectra, but the same-density smoke produces a precision-CMB
acoustic-scale warning. Treat this as a pressure point, not a win or a kill.
```

Next target:

```text
187-CAMB-density-convention-and-locked-transfer-theta-gate.md
```
