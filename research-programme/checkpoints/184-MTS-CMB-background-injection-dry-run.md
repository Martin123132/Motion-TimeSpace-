# 184 - MTS CMB Background Injection Dry Run

Private CMB pipeline checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 183 proved the local CAMB engine can produce sane LCDM spectra:

```text
LCDM baseline smoke passed,
MTS CMB branch not read.
```

This checkpoint lets MTS enter the CMB pipeline for the first time, but only as:

```text
locked background tables,
closure-mode contracts,
blueprint dry-runs.
```

No MTS spectra are run.

No likelihood is run.

No CMB support claim is allowed.

## 2. Machine Artifact

Script:

```text
scripts/MTS_CMB_background_injection_dry_run.py
```

Run:

```text
runs/20260601-000001-MTS-CMB-background-injection-dry-run
```

Command:

```text
python scripts/MTS_CMB_background_injection_dry_run.py --timestamp 20260601-000001
```

Status:

```text
MTS_CMB_background_injection_dry_run_passed_no_spectra
```

Claim ceiling:

```text
MTS_CMB_background_injection_only_no_spectra_no_CMB_claim
```

## 3. Fixed Locks

The injected branch preserves:

| parameter | value | rule |
|---|---:|---|
| `B_mem` | `0.07407407407407407` | fixed no-refit lock |
| `p` | `3.0` | fixed no-refit lock |
| `u3` | `0.25` | fixed no-refit lock |
| `Omega_m0` transfer reference | `0.3032827426766658` | logged calibration input |
| `h` profiled reference | `0.6842175693081872` | logged calibration input |
| `c_s_eff^2` | `1.0` | fixed high-cs closure |
| `sigma_mem` | `0.0` | no fitted slip/lensing rescue |

Lock failures:

```text
0
```

## 4. Background Table

The script writes:

```text
MTS_background_functions.csv
```

using:

```text
rho_mem(a) = 1 - Omega_m0 + B_mem A(N)
A(N) = 1 - exp[-(N/u3)^p]
N = ln(1+z)
1 + w_mem = B_mem A_N / [3 rho_mem].
```

The table includes:

```text
z, a, N, A_mem, dA/dN, rho_mem, w_mem,
E2_no_radiation, E2_with_radiation,
Omega_mem, Omega_m, Omega_r,
c_s_eff^2, sigma_mem.
```

All background rows were finite and positive where required.

## 5. Primary CMB Safety Recheck

The recombination-era memory fractions remain tiny:

| z | `Omega_mem` with radiation | `1+w_mem` | readout |
|---:|---:|---:|---|
| `1059.0` | `1.6266370173279976e-09` | `0.0` | background negligible |
| `1089.9373168180757` | `1.4818565662420977e-09` | `0.0` | background negligible |
| `1091.7904498991018` | `1.4737224055894007e-09` | `0.0` | background negligible |
| `10000.0` | `6.444990236810128e-13` | `0.0` | background negligible |

This says only:

```text
the MTS memory background is not obviously large during primary plasma physics.
```

It does not say:

```text
MTS passes CMB.
```

## 6. Closure Modes

Two closure modes are now injected as contracts:

| mode | status | claim limit |
|---|---|---|
| exact auxiliary smooth memory | dry-run contract only | requires parent auxiliary/Bianchi owner |
| high-sound-speed effective scalar | dry-run contract only | effective EFT owner, not parent promotion |

The high-cs branch carries:

```text
c_s_eff^2 = 1,
sigma_mem = 0.
```

The exact auxiliary branch carries:

```text
delta_mem = theta_mem = delta_p_mem = sigma_mem = 0
```

as a future constraint route, not as a derived theorem.

## 7. CAMB Injection Status

The checkpoint writes:

```text
CAMB_injection_contract.csv
```

Current status:

| pipeline item | injected now |
|---|---|
| background functions | yes, table only |
| closure mode | yes, contract only |
| CAMB custom dark-energy module | no |
| TT/TE/EE/lensing spectra | no |
| likelihood scorecard | no |

So the branch has entered the CMB pipeline as a locked background/closure
payload, but not as a CAMB spectra-producing model.

## 8. Dry-Run Results

Both MTS blueprints dry-run cleanly:

| config | status | marker | spectra |
|---|---|---|---|
| `MTS_exact_auxiliary_transfer_locked` | `dry_run_ready_engine_available_no_spectra_run` | `DONE.txt` | not run |
| `MTS_high_cs_transfer_locked` | `dry_run_ready_engine_available_no_spectra_run` | `DONE.txt` | not run |

## 9. Claim Gates

| gate | result |
|---|---|
| parameter locks preserved | pass |
| background table finite | pass |
| MTS blueprint dry-runs ready | pass |
| MTS spectra run performed | blocked |
| support claim allowed | fail |

Acceptance gates:

| gate | result |
|---|---|
| all cited sources exist | pass |
| parameter locks clean | pass |
| background table written | pass |
| primary CMB background fraction small | pass |
| MTS dry-runs no spectra | pass |
| claim ceiling preserved | pass |

## 10. Decision

Decision:

```text
MTS_CMB_background_injection_dry_run_passed_no_spectra
```

Meaning:

```text
The fixed MTS background and closure modes can now be written into the CMB
pipeline as a locked dry-run payload. The next missing object is the actual
CAMB/PPF/custom-module mapping that turns that payload into spectra without
breaking the no-rescue locks.
```

Boxing-card readout:

```text
MTS has now stepped through the ropes, but only for glove inspection. No punches
were thrown. The next round is building the legal rule that lets CAMB understand
the MTS background without secretly turning knobs.
```

## 11. Next Target

Create:

```text
185-CAMB-MTS-effective-background-module-contract.md
```

Next task:

```text
Define the exact CAMB/PPF/custom-dark-energy mapping needed before MTS spectra
can be run: background interpolation, closure mode, perturbation variables,
baseline parity, and failure gates. No MTS spectra interpretation until that
mapping contract passes.
```
