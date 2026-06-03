# Local Bounds Gate Runner

## 1. Purpose

This file follows:

```text
15-local-observables-data-map.md
```

The question is:

```text
Can the published-bound screening map be turned into a simple pass/fail harness
for candidate local branches?
```

Short answer:

```text
yes. The harness is operational as a conservative screening tool, but it is not
a raw likelihood fit and it cannot create an empirical MTS claim.
```

## 2. Machine Run

Implemented:

```text
scripts/local_bounds_gate_runner.py
```

Successful run:

```text
runs/20260530-232506-local-bounds-gate-runner/status.json
```

Readout:

```text
local_bounds_gate_runner_operational_screening_not_fit
```

Next target:

```text
17-post-checkpoint-promotion-gate-summary.md
```

## 3. Screening Gates

The runner uses the stage-15 gates:

```text
q_R <= 2.3e-5
|delta_beta| <= 7.16e-5
|alpha_clock| <= 2.48e-5
|epsilon_matter| <= 2.745906043549196e-15
Q_R = 0
```

The final gate is a theory gate, not a measured bound:

```text
closure means Q_R must vanish exactly.
```

## 4. Branches Screened

Passed as screening/control branches:

```text
closure_null
qR_at_cassini_gate
beta_at_inpop_gate
clock_at_galileo_gate
mixed_inside_simple_gates
```

Failed:

```text
qR_ten_times_gate
beta_above_gate
matter_above_microscope_gate
kinetic_QR_hair_small_gamma
perihelion_degenerate_but_gamma_fail
```

Important:

```text
closure_null passes only as a control baseline, not as a signal.
```

## 5. Failure Logic

The runner rejects:

```text
gamma leaks:
abs(q_R) > q_R gate.

beta-completion leaks:
abs(delta_beta) > delta_beta gate.

clock/load leaks:
abs(alpha_clock) > alpha_clock gate.

matter-coupling leaks:
abs(epsilon_matter) > epsilon_matter gate.

reciprocal charge hair:
Q_R != 0.
```

It also blocks a trick:

```text
do not hide a failed q_R or beta branch inside a perihelion cancellation.
```

The `perihelion_degenerate_but_gamma_fail` branch exists specifically to catch
that failure mode.

## 6. Outputs

Core outputs:

```text
candidate_local_branches.csv
branch_parameter_gate_results.csv
branch_observable_impacts.csv
candidate_branch_summary.csv
local_bounds_failure_modes.csv
```

These live under:

```text
runs/20260530-232506-local-bounds-gate-runner/results/
```

## 7. Gate Verdict

Passes:

```text
source 15 complete;
candidate branches screened;
pass and fail outcomes both present;
closure null passes as control;
nonzero Q_R fails even when q_R is small.
```

Fails:

```text
empirical claim allowed.
```

Status:

```text
operational screening harness;
not a raw-data fit;
not empirical evidence for MTS.
```

## 8. Next Target

Create:

```text
17-post-checkpoint-promotion-gate-summary.md
```

Purpose:

```text
summarize the full post-checkpoint branch and decide what, if anything, is
eligible for eventual promotion into the main workbench as a closure benchmark,
an open derivation obligation, or a rejected route.
```
