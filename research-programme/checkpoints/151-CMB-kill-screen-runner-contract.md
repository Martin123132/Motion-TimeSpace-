# 151 - CMB Kill-Screen Runner Contract

Private run-contract checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 150 gave the MTS memory branch a Boltzmann interface:

```text
rho_mem(a), w_mem(a), closure modes, and CMB background safety are defined.
```

The next danger is obvious:

```text
if we rush into CMB spectra, we can accidentally turn the test into another rescue fit.
```

This checkpoint prevents that. It writes the future CMB spectra kill-screen contract before any long CLASS/CAMB-style computation is attempted.

Short answer:

```text
The CMB kill-screen rulebook is now written.
The actual spectra run is not ready because no CLASS/CAMB engine or long-run wrapper is present.
```

## 2. Machine Artifact

Script:

```text
research-programme\scripts\CMB_kill_screen_runner_contract.py
```

Run:

```text
research-programme\runs\20260531-235950-CMB-kill-screen-runner-contract
```

Generated:

```text
source_register.csv
environment_preflight.csv
parameter_lock_manifest.csv
kill_screen_run_matrix.csv
config_blueprint_register.csv
output_artifact_contract.csv
score_band_policy.csv
failure_decision_tree.csv
long_run_workflow.csv
gate_results.csv
decision.csv
launch_commands.ps1
configs/*.blueprint.json
log.txt
DONE.txt
status.json
```

Status:

```text
CMB_kill_screen_runner_contract_written_no_spectra_run
```

Claim ceiling:

```text
CMB_kill_screen_runner_contract_no_spectra_run_no_support_claim
```

## 3. Environment Preflight

The current machine state is:

| Item | Status | Meaning |
|---|---|---|
| `camb` Python module | missing | no CAMB spectra runner available in the active Python environment |
| `classy` Python module | missing | no CLASS Python wrapper available |
| `class` executable | missing | no standalone CLASS executable on `PATH` |
| `cobaya` | missing | no likelihood plumbing package available |
| `montepython` | missing | no CLASS likelihood wrapper available |
| future runner script | missing | `scripts\cmb_kill_screen_long_run.py` does not exist yet |

So the contract is ready, but execution is blocked until an engine/wrapper exists.

That is a good block, not a bad block: it stops us from pretending compressed-distance work is a real CMB spectra test.

## 4. Parameter Locks

These cannot move inside the kill-screen:

| Parameter | Value | Rule |
|---|---:|---|
| `B_mem` | `0.07407407407407407` | frozen; no CMB refit |
| `p` | `3.0` | frozen activation exponent |
| `u3` | `0.25` | frozen activation scale |
| `c_s_eff^2` | `1` for high-sound-speed route | fixed closure, not fitted |
| `sigma_mem` | `0` | no fitted slip/lensing rescue |

Calibration branches must be labelled separately:

```text
late-transfer locked,
joint calibration diagnostic,
CMB-only control.
```

No branch can quietly reset `Omega_m0`, `h`, `r_d`, BAO alpha, or SN offset and then call itself a unified prediction.

## 5. Run Matrix

The future kill-screen must run at least these branches:

| Run | Purpose | Interpretation |
|---|---|---|
| `LCDM_baseline_reproduction` | prove the pipeline reproduces baseline spectra/likelihood | required before reading MTS |
| `MTS_exact_auxiliary_transfer_locked` | strict no-clustering memory kill-screen | kill-screen only |
| `MTS_high_cs_transfer_locked` | test `c_s_eff^2=1` effective memory | kill-screen only |
| `MTS_exact_auxiliary_joint_calibration` | test spectra under joint calibration stress | diagnostic only |
| `MTS_high_cs_joint_calibration` | same but high-sound-speed closure | diagnostic only |
| `MTS_CMB_only_control` | separate spectra compatibility from late-transfer failure | control only |

This is the baseline-parity point again: MTS does not get tortured alone, but it also does not get private rescue knobs.

## 6. Required Outputs

The future long run must write:

```text
run_config.json
log.txt
status.json
DONE.txt or FAILED.txt
engine_version.json
baseline_reproduction.csv
background_functions.csv
spectra_TT_TE_EE.csv
lensing_phi_phi.csv
late_ISW_diagnostics.csv
likelihood_scorecard.csv
claim_gate_results.csv
```

Codex should not sit watching the terminal. The runner must write `status.json` and a completion marker, then we inspect the run after it finishes.

## 7. Score Bands

Predeclared score bands:

| Metric | Band | Decision |
|---|---|---|
| baseline reproduction | required first | otherwise pipeline fail |
| total `Delta chi2 <= 2` | competitive draw | survives kill-screen only |
| `2 < Delta chi2 <= 6` | mild tension | inspect sector residuals |
| `6 < Delta chi2 <= 10` | serious tension | repair or demote branch |
| `Delta chi2 > 10` | hard fail | CMB rejects that closure/calibration branch |
| any sector degradation `> 6` | hard sector fail | do not hide sector failure in total score |
| any lock/refit violation | invalid | discard run |

Even a good CMB kill-screen result would not finish the theory. It would only say:

```text
the current MTS closure survived spectra-level pressure.
```

Parent action, local GR, amplitude, and domain selector still remain.

## 8. Workflow

Future VS Code pattern:

```text
1. implement scripts\cmb_kill_screen_long_run.py
2. run the generated dry-run command first
3. if dry-run passes, launch from VS Code terminal
4. stop spending tokens while it runs
5. return with: inspect run <run-folder>
```

Generated launch file:

```text
research-programme\runs\20260531-235950-CMB-kill-screen-runner-contract\launch_commands.ps1
```

Generated config blueprints:

```text
configs\LCDM_baseline_reproduction.blueprint.json
configs\MTS_exact_auxiliary_transfer_locked.blueprint.json
configs\MTS_high_cs_transfer_locked.blueprint.json
```

## 9. Decision

Current fair status:

```text
CMB kill-screen contract written.
Spectra execution blocked by missing engine/wrapper.
No CMB support claim.
```

Next fork:

```text
implement the CMB long-run wrapper,
or return to the calibration theorem before spending time on spectra.
```

My preference: do one more theory move first unless you specifically want the CMB tooling built next. The calibration bridge is already known to be the live problem; spectra tooling without the bridge may only tell us which punch hurts.
