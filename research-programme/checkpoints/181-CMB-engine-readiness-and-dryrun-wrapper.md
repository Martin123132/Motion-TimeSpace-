# 181 - CMB Engine Readiness and Dry-Run Wrapper

Private execution-readiness checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 180 selected:

```text
CMB engine readiness, then CMB kill-screen.
```

But checkpoint 151 had already warned:

```text
no CLASS/CAMB/Cobaya engine or long-run wrapper was available.
```

So this checkpoint does not run spectra. It builds the dry-run wrapper and makes
the current failure clean, logged, and inspectable.

## 2. Machine Artifact

Checkpoint script:

```text
scripts/CMB_engine_readiness_and_dryrun_wrapper.py
```

New future long-run wrapper:

```text
scripts/cmb_kill_screen_long_run.py
```

Run:

```text
runs/20260531-235959-CMB-engine-readiness-and-dryrun-wrapper
```

Command:

```text
python scripts/CMB_engine_readiness_and_dryrun_wrapper.py --timestamp 20260531-235959
```

Status:

```text
CMB_engine_readiness_wrapper_written_dryruns_fail_clean_missing_engine
```

Claim ceiling:

```text
engine_readiness_and_dryrun_only_no_spectra_no_CMB_claim
```

## 3. What Was Built

The new wrapper:

```text
scripts/cmb_kill_screen_long_run.py
```

now supports:

```text
--config <blueprint.json>
--dry-run
--output-root <runs folder>
--timestamp <stamp>
```

It writes the long-run style artifacts:

```text
run_config.json
log.txt
status.json
engine_version.json
DONE.txt or FAILED.txt
results/engine_readiness.csv
results/blueprint_lock_audit.csv
results/output_contract_audit.csv
results/claim_gate_results.csv
```

It also writes explicit `not_run` placeholders for the future spectra outputs:

```text
baseline_reproduction.csv
background_functions.csv
spectra_TT_TE_EE.csv
lensing_phi_phi.csv
late_ISW_diagnostics.csv
likelihood_scorecard.csv
```

Those placeholders are deliberately labelled:

```text
not_run
```

so nobody can mistake a dry-run for a CMB result.

## 4. Engine Preflight

Current engine state:

| engine/tool | status |
|---|---|
| `camb` Python module | missing |
| `classy` Python module | missing |
| `class` executable | missing |
| `cobaya` Python module | missing |
| `montepython` Python module | missing |

Therefore:

```text
engine_available = false
```

No CMB spectra run was attempted.

## 5. Dry-Run Results

The wrapper dry-ran all three checkpoint-151 blueprints:

| config | status | marker | reason |
|---|---|---|---|
| `LCDM_baseline_reproduction` | `dry_run_blocked_missing_engine_no_spectra_run` | `FAILED.txt` | missing CMB engine |
| `MTS_exact_auxiliary_transfer_locked` | `dry_run_blocked_missing_engine_no_spectra_run` | `FAILED.txt` | missing CMB engine |
| `MTS_high_cs_transfer_locked` | `dry_run_blocked_missing_engine_no_spectra_run` | `FAILED.txt` | missing CMB engine |

This is a successful checkpoint result because the failure is clean:

```text
blueprints valid,
locks valid,
output contract valid,
no spectra run,
no claim.
```

## 6. Lock Audit

The dry-run wrapper enforces the no-rescue locks:

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

All current blueprint lock audits passed.

This matters because the CMB round must not become:

```text
turn knobs until it survives.
```

It must be:

```text
fixed branch versus fair baseline under predeclared rules.
```

## 7. Gate Results

All checkpoint gates passed:

| gate | result |
|---|---|
| all cited sources exist | pass |
| wrapper exists | pass |
| blueprints valid and locked | pass |
| engine readiness known | pass |
| missing engine fails cleanly | pass |
| no spectra run performed | pass |
| claim ceiling preserved | pass |

This checkpoint turns “we cannot run CMB yet” from a vague problem into a
controlled state:

```text
the wrapper works,
the configs are locked,
the dry-runs fail cleanly,
and the missing dependency is explicit.
```

## 8. Decision

Decision:

```text
CMB_engine_readiness_wrapper_written_dryruns_fail_clean_missing_engine
```

Meaning:

```text
The CMB kill-screen is now operationally fenced, but not executable on this
machine until a CLASS/CAMB route is installed or an external engine path is
provided.
```

No support claim is allowed:

```text
no spectra,
no likelihood,
no baseline reproduction,
no CMB pass.
```

Boxing-card readout:

```text
We built the ring inspection checklist. The gloves are locked, the judges'
cards are fixed, and the bout cannot start because the arena lights are not
installed yet. Good: better a clean stoppage than shadowboxing in the dark.
```

## 9. Next Target

Create:

```text
182-CMB-engine-install-or-external-run-plan.md
```

Next task:

```text
Choose a CMB engine route: install/use CAMB locally, install/use CLASS/classy,
or prepare an external-run handoff. Then rerun the dry-run wrapper before any
long spectra execution.
```
