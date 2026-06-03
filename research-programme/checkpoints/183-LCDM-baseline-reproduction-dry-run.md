# 183 - LCDM Baseline Reproduction Dry Run

Private CMB pipeline-smoke checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 182 installed CAMB and made all CMB blueprints dry-run ready:

```text
CAMB available,
blueprints locked,
no spectra run yet.
```

This checkpoint runs the first tiny legal CMB calculation:

```text
LCDM baseline only.
```

No MTS CMB branch is executed or interpreted.

## 2. Machine Artifact

Script:

```text
scripts/LCDM_baseline_reproduction_dry_run.py
```

Run:

```text
runs/20260531-235959-LCDM-baseline-reproduction-dry-run
```

Command:

```text
python scripts/LCDM_baseline_reproduction_dry_run.py --timestamp 20260531-235959
```

Status:

```text
LCDM_CAMB_baseline_smoke_passed_no_MTS_CMB_read
```

Claim ceiling:

```text
LCDM_baseline_smoke_only_no_MTS_CMB_claim
```

## 3. Baseline Vector

The smoke used a fixed vanilla LCDM CAMB vector:

| parameter | value |
|---|---:|
| `H0` | `67.5` |
| `ombh2` | `0.02237` |
| `omch2` | `0.1200` |
| `tau` | `0.0544` |
| `As` | `2.1e-9` |
| `ns` | `0.965` |
| `mnu` | `0.06` |
| `omk` | `0.0` |

This is not an official Planck likelihood reproduction.

It is a CAMB pipeline smoke to prove the local engine can produce sane spectra
before MTS is allowed near the CMB ring.

## 4. Smoke Results

CAMB:

```text
version = 1.6.6
runtime = 0.774418 seconds
lmax = 200
```

All baseline sanity checks passed:

| check | result | value |
|---|---|---:|
| CAMB import | pass | `1.6.6` |
| runtime | pass | `0.774418 s` |
| finite sample spectra | pass | `True` |
| positive sampled `TT` | pass | minimum `819.2138069951296` |
| nonnegative sampled `EE` | pass | minimum `0.0031222663302837837` |
| `zstar` sanity | pass | `1089.9373168180757` |
| `rdrag` sanity | pass | `147.10139220381296` |
| age sanity | pass | `13.78435583509` |

Representative sampled spectra:

| ell | `TT D_ell` | `EE D_ell` | `TE D_ell` |
|---:|---:|---:|---:|
| `2` | `1024.163255581026` | `0.031125095842420812` | `2.634725454617026` |
| `10` | `819.2138069951296` | `0.0031222663302837837` | `0.8522523677071493` |
| `50` | `1422.8908547179165` | `0.11914625021798189` | `0.5570696508779048` |
| `100` | `2699.3503825103053` | `0.7756962002425236` | `-23.208845037636816` |
| `150` | `4381.731811791387` | `1.1026955974117998` | `-46.13710737318073` |
| `200` | `5591.794779151179` | `0.6738615447432365` | `-15.286611593648646` |

## 5. Derived Background Diagnostics

CAMB returned:

| quantity | value |
|---|---:|
| age | `13.78435583509` |
| `zstar` | `1089.9373168180757` |
| `rstar` | `144.44047126476087` |
| `thetastar` | `1.0415969851026594` |
| `DAstar` | `13.867212878935597` |
| `zdrag` | `1059.946808528186` |
| `rdrag` | `147.10139220381296` |
| `zeq` | `3402.8803390689823` |
| `keq` | `0.010384901399096676` |

Again, this is pipeline sanity, not a likelihood score.

## 6. Claim Gates

| gate | result |
|---|---|
| CAMB baseline smoke | pass |
| LCDM baseline before MTS | pass |
| MTS CMB branch read | blocked |
| official likelihood run | not run |
| support claim allowed | fail |

The critical guardrail:

```text
MTS_CMB_branch_executed = false
```

## 7. Decision

Decision:

```text
LCDM_CAMB_baseline_smoke_passed_no_MTS_CMB_read
```

Meaning:

```text
The local CAMB engine can generate sane LCDM spectra and derived background
diagnostics. The CMB pipeline has passed its first baseline smoke. MTS CMB
branches remain blocked until the next controlled dry-run step.
```

Boxing-card readout:

```text
The baseline fighter threw the first legal jab and the ring did not collapse.
Now, and only now, MTS can be brought toward the ropes for a fixed-background
injection dry-run — still no title claim, still no rescue knobs.
```

## 8. Next Target

Create:

```text
184-MTS-CMB-background-injection-dry-run.md
```

Next task:

```text
Inject the fixed MTS background/closure into the CAMB-wrapper pipeline in dry-run
form only. Verify parameter locks, background tables, and claim gates before any
real MTS spectra interpretation.
```
