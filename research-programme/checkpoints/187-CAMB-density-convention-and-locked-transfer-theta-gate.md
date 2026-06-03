# 187 - CAMB Density Convention and Locked-Transfer Theta Gate

Private CMB pipeline checkpoint. This is not a public CMB claim.

## 1. Trigger

Checkpoint 186 showed:

```text
MTS high-c_s w(a) produces finite CAMB spectra,
but same-density theta* shifts by about 0.459%.
```

The next question was whether the declared locked-transfer stance:

```text
h = 0.6842175693081872
Omega_m0 = 0.3032827426766658
B_mem = 2/27
p = 3
u3 = 1/4
```

reduces that raw acoustic-scale hazard without hidden calibration rescue knobs.

## 2. Machine Artifact

Script:

```text
scripts/CAMB_density_convention_locked_transfer_theta_gate.py
```

Run:

```text
runs/20260601-000004-CAMB-density-convention-and-locked-transfer-theta-gate
```

Command:

```text
python scripts/CAMB_density_convention_locked_transfer_theta_gate.py --timestamp 20260601-000004
```

Status:

```text
CAMB_locked_transfer_theta_gate_ran_theta_hazard_not_reduced_no_likelihood_claim
```

Claim ceiling:

```text
locked_transfer_theta_gate_only_no_official_likelihood_no_CMB_claim
```

## 3. Density Conventions

The gate tests both honest CAMB interpretations of the locked `Omega_m0` input:

| convention | rule | `omch2` | actual CAMB `Omega_m` |
|---|---|---:|---:|
| checkpoint-183 control | fixed baseline vector | `0.12` | `0.31388722429740024` |
| locked, neutrino subtracted | `Omega_m0 h^2 - ombh2 - mnu/93.14` | `0.11896874117701545` | `0.303284184576856` |
| locked, neutrino not subtracted | `Omega_m0 h^2 - ombh2` | `0.11961293271663323` | `0.3046602103653526` |

The neutrino-subtracted convention is the cleaner reading if locked `Omega_m0`
is meant to include massive neutrino matter. The not-subtracted convention is
kept as a sensitivity branch so we cannot fool ourselves with a convention
choice.

## 4. Branches Run

All declared branches ran to `lmax=200`:

| branch | model | purpose |
|---|---|---|
| `LCDM_checkpoint183_control` | LCDM | Planck-like smoke control |
| `MTS_same_density_fluid_control` | CAMB Fluid | checkpoint-186 hazard reference |
| `LCDM_locked_transfer_neutrino_subtracted` | LCDM | locked-transfer control |
| `MTS_locked_transfer_neutrino_subtracted_fluid` | CAMB Fluid | main locked MTS branch |
| `MTS_locked_transfer_neutrino_subtracted_PPF` | CAMB PPF | diagnostic comparator |
| `LCDM_locked_transfer_neutrino_not_subtracted` | LCDM | convention sensitivity control |
| `MTS_locked_transfer_neutrino_not_subtracted_fluid` | CAMB Fluid | convention sensitivity MTS branch |
| `MTS_locked_transfer_neutrino_not_subtracted_PPF` | CAMB PPF | diagnostic comparator |

## 5. Theta Gate

Same-density reference:

| branch | control | fractional `theta*` shift |
|---|---|---:|
| `MTS_same_density_fluid_control` | `LCDM_checkpoint183_control` | `0.004593764101486964` |

Locked-transfer readout:

| branch | control | fractional `theta*` shift | improvement vs same-density |
|---|---|---:|---:|
| `MTS_locked_transfer_neutrino_subtracted_fluid` | `LCDM_locked_transfer_neutrino_subtracted` | `0.004729833346660761` | `-0.000136069245173797` |
| `MTS_locked_transfer_neutrino_not_subtracted_fluid` | `LCDM_locked_transfer_neutrino_not_subtracted` | `0.004711891535075118` | `-0.00011812743358815408` |

So the locked-transfer branch does not reduce the raw `theta*` hazard. It is
slightly worse under both density conventions.

Against the original checkpoint-183 LCDM control, the locked branches are also
farther away:

| branch | fractional shift vs checkpoint-183 LCDM |
|---|---:|
| `MTS_locked_transfer_neutrino_subtracted_fluid` | `0.006336084178604894` |
| `MTS_locked_transfer_neutrino_not_subtracted_fluid` | `0.006970656311523455` |

## 6. Interpretation

This is not a death blow, but it is a real CMB pressure point.

What survived:

```text
MTS remains CAMB-runnable as a high-c_s effective branch.
The locked background does not numerically explode.
The sound horizon itself is not the main moving target.
```

What failed at this gate:

```text
Locked h/Omega_m transfer does not solve the raw acoustic-angle mismatch.
```

The problem is now sharp:

```text
Either derive a theta-compensation mechanism from the theory, or run a matched
profiled CMB fit where MTS and baseline models get the same allowed freedom and
the same parameter-count penalties.
```

No one gets a free haymaker. LCDM/wCDM/CPL must be tested under the same rule
set if we move to profiling.

## 7. Claim Gates

| gate | result |
|---|---|
| all cited sources exist | pass |
| all declared branches ran | pass |
| density conventions declared | pass |
| locked-transfer theta hazard reduced | warning |
| locked-transfer theta warning | warning |
| exact auxiliary spectra | blocked |
| official likelihood | not run |
| support claim allowed | fail |

## 8. Decision

Decision:

```text
CAMB_locked_transfer_theta_gate_ran_theta_hazard_not_reduced_no_likelihood_claim
```

Meaning:

```text
The locked-transfer stance has now had a fair smoke test. It runs, but it does
not reduce the raw theta* hazard. Treat CMB as an open pressure gate, not as
support and not as a clean kill.
```

Next target:

```text
188-CMB-theta-compensation-theorem-or-profiled-fit-gate.md
```
