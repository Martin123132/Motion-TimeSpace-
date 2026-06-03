# 182 - CMB Engine Install or External Run Plan

Private engine-readiness checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 181 produced the right kind of failure:

```text
the CMB dry-run wrapper existed,
the blueprints were locked,
but no CLASS/CAMB engine was available.
```

This checkpoint tries the least-invasive local route:

```text
install/use CAMB in the existing `.venv-score` environment,
then rerun the CMB dry-run wrapper.
```

No spectra are run in this checkpoint.

## 2. Machine Artifact

Script:

```text
scripts/CMB_engine_install_or_external_run_plan.py
```

Run:

```text
runs/20260531-235959-CMB-engine-install-or-external-run-plan
```

Command:

```text
python scripts/CMB_engine_install_or_external_run_plan.py --timestamp 20260531-235959
```

Status:

```text
CMB_CAMB_engine_installed_dryruns_ready_no_spectra_run
```

Claim ceiling:

```text
CMB_engine_install_readiness_no_spectra_no_CMB_claim
```

## 3. Engine Route

Local CAMB installed successfully:

```text
python -m pip install camb
```

Detected engine:

| route | status |
|---|---|
| CAMB Python | installed, selected |
| `camb` version | `1.6.6` |
| CLASS / `classy` | not selected |
| CLASS executable | not selected |
| external handoff | not needed now |

The active engine path is:

```text
.venv-score\Lib\site-packages\camb\__init__.py
```

## 4. Dry-Run Results

All three checkpoint-151 blueprints now dry-run cleanly:

| config | status | marker | reason |
|---|---|---|---|
| `LCDM_baseline_reproduction` | `dry_run_ready_engine_available_no_spectra_run` | `DONE.txt` | dry run only |
| `MTS_exact_auxiliary_transfer_locked` | `dry_run_ready_engine_available_no_spectra_run` | `DONE.txt` | dry run only |
| `MTS_high_cs_transfer_locked` | `dry_run_ready_engine_available_no_spectra_run` | `DONE.txt` | dry run only |

This means:

```text
the arena lights are installed,
but the fight has not started.
```

## 5. Lock Audit

The dry-runs preserved the locks:

```text
B_mem = 2/27
p = 3
u3 = 1/4
do_not_refit_B_mem
do_not_refit_p_or_u3
do_not_fit_c_s_eff
do_not_fit_sigma_mem_or_slip
log_calibration_branch_separately
```

There were:

```text
bad_locks = 0
dry_run_failures = 0
spectra_runs = 0
```

So the next CMB work can move from engine setup to baseline reproduction.

## 6. Gate Results

All checkpoint gates passed:

| gate | result |
|---|---|
| all cited sources exist | pass |
| CAMB engine available | pass |
| all blueprint dry-runs ready | pass |
| locks preserved | pass |
| no spectra run performed | pass |
| claim ceiling preserved | pass |

## 7. What This Does Not Mean

This does not mean:

```text
MTS passes CMB.
LCDM baseline has been reproduced.
TT/TE/EE/lensing spectra have been scored.
the calibration bridge is solved.
the parent theory is promoted.
```

It only means:

```text
CAMB is importable,
the CMB kill-screen wrapper can see an engine,
and the fixed blueprints pass dry-run readiness.
```

## 8. Decision

Decision:

```text
CMB_CAMB_engine_installed_dryruns_ready_no_spectra_run
```

Meaning:

```text
The local CAMB route is now available. The next move is a tiny LCDM baseline
reproduction smoke, still with no MTS interpretation.
```

Boxing-card readout:

```text
The arena lights are on. The judges are seated. The MTS fighter still stays in
the corner until the baseline fighter throws the first legal punch and proves
the ring itself works.
```

## 9. Next Target

Create:

```text
183-LCDM-baseline-reproduction-dry-run.md
```

Next task:

```text
Use CAMB for a tiny LCDM baseline spectra smoke. Write status/log/results.
Do not read or interpret MTS CMB branches until the LCDM baseline smoke passes.
```
