# 353 - Boundary No-Hair Theorem Attempt Or PPN Bound Runner

Private derivation checkpoint. This is not a public local-GR, PPN, WEP, clock, Cassini, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 352 turned the local GR problem into a finite residual ledger:

```text
bulk,
trace,
trace-free shear,
vector/preferred-frame,
clock/WEP,
conservation flux.
```

This checkpoint does the next honest thing:

```text
try the boundary no-hair theorem first;
if it does not close, prepare a PPN bound runner.
```

Result:

```text
no-hair theorem contract written,
monopole trace safe condition identified,
but no-hair not derived.
```

The useful fallback is:

```text
proxy PPN bound runner scaffold is ready,
but not official-source-locked.
```

## 2. Run Ledger

Script:

```text
scripts/boundary_nohair_theorem_attempt_or_PPN_bound_runner.py
```

Run directory:

```text
runs/20260601-233000-boundary-nohair-theorem-attempt-or-PPN-bound-runner
```

Command:

```text
python scripts/boundary_nohair_theorem_attempt_or_PPN_bound_runner.py --timestamp 20260601-233000
```

Status:

```text
conditional_boundary_nohair_contract_written_proxy_PPN_bound_runner_ready_no_local_GR_promotion
```

Claim ceiling:

```text
conditional_nohair_and_proxy_bounds_only_no_official_PPN_or_local_GR_pass_claim
```

Outputs:

```text
results/source_register.csv
results/nohair_theorem_attempt.csv
results/nohair_sector_verdicts.csv
results/proxy_bound_manifest.csv
results/residual_amplitude_requirements.csv
results/theorem_or_bound_route_decision.csv
results/gate_results.csv
results/decision.csv
```

## 3. Boundary No-Hair Theorem Contract

The theorem we need is not mysterious anymore.
It is:

```text
If:
  A1 local exterior is isolated, stationary, and compact,
  A2 quotient P_D removes projector bulk stress,
  A3 boundary action depends only on total relative class / charge,
  A4 no material boundary marker or preferred frame exists,
  A5 regular asymptotic matching kills radial scalar hair,
  A6 all matter, clocks, rulers, and photons couple to one metric,
  A7 boundary flux obeys an owned Ward/Bianchi identity,

then:
  boundary residual = conserved monopole trace only,
  trace-free shear = 0,
  vector/preferred-frame residual = 0,
  clock/WEP residual = 0,
  non-projector bulk residual = 0,
  local exterior reduces to metric-only EH with measured-mass renormalization.
```

Only A2 currently has a conditional route from earlier work.

The rest are still open.

## 4. The Partial Win

There is one useful theorem-shaped result:

```text
pure conserved boundary monopole trace
```

is locally safe because it can be absorbed into:

```text
measured GM.
```

That is not a new force.
It is just mass calibration, provided it is:

```text
constant,
conserved,
spherically/monopole-only,
and not radius-dependent.
```

So the boundary trace sector is not automatically fatal.

## 5. The Hard Failures

The no-hair theorem does not yet derive:

```text
B_tr^rad(r) = 0,
B_TF,ij = 0,
B_0i = 0,
C_clock = 0,
C_WEP = 0,
E_bulk_nonprojector^MTS = 0,
n_mu B^{mu nu} = 0 or owned.
```

These are exactly the local-GR gatekeepers.

Most dangerous:

```text
B_TF,ij
```

because trace-free/shear boundary stress directly creates anisotropic potentials and lensing slip.

The second most dangerous:

```text
C_WEP
```

because composition-dependent coupling is usually punished brutally by local tests.

## 6. Proxy PPN Bound Runner

Since the theorem did not close, the fallback is an engineering bound runner.

It introduces residual amplitudes:

```text
epsilon_TF,
epsilon_rad,
epsilon_vec,
epsilon_clock,
epsilon_WEP,
epsilon_bulk.
```

Then the symbolic vector from 352 becomes a budget problem:

```text
gamma - 1:
  epsilon_TF + epsilon_rad + epsilon_bulk < proxy_gamma

beta - 1:
  epsilon_rad + epsilon_nl < proxy_beta

preferred-frame:
  epsilon_vec < proxy_alpha

clock:
  epsilon_clock < proxy_clock

WEP:
  epsilon_WEP < proxy_WEP

fifth force:
  epsilon_bulk + epsilon_rad < proxy_fifth_force.
```

The runner emits proxy scales only.

They are not current official bounds.
They are engineering targets until source-locked against official references.

## 7. Proxy Bound Scales

The script uses deliberately labelled proxy scales:

| Residual | Proxy scale | Status |
|---|---:|---|
| `gamma - 1` | `2.3e-5` | proxy only |
| `beta - 1` | `8.0e-5` | proxy only |
| preferred-frame | `4.0e-7` | proxy only |
| anisotropy | `1.0e-3` | proxy only |
| clock | `1.0e-6` | proxy only |
| WEP | `1.0e-14` | proxy only |
| fifth force / `delta_G` | `1.0e-10` | proxy only |

These are not used to claim a pass.
They are used to tell us how small the residual sectors would have to be if their coefficients are order unity.

## 8. Route Decision

| Route | Status | Meaning |
|---|---:|---|
| boundary no-hair theorem | attempted, not closed | A3-A7 still need parent derivations |
| proxy PPN bound runner | ready | usable as engineering scaffold |
| official local-bound pass | not ready | needs source-locked current bounds and model coefficients |
| modified exterior branch | deferred | only if residuals cannot be killed or bounded |

This is a good failure mode:

```text
the obstruction is now finite, named, and testable.
```

## 9. Gate Results

| Gate | Result | Meaning |
|---|---:|---|
| source paths exist | pass | cited local-GR/PPN checkpoints and script exist |
| boundary no-hair theorem attempted | pass | A1-A7 contract written |
| boundary no-hair derived | fail | A3-A7 not parent-derived |
| monopole trace safe condition identified | conditional pass | pure conserved monopole can be measured mass |
| proxy PPN bound runner ready | pass | proxy bounds and amplitude budgets emitted |
| official bound source-locked | fail | numeric rows are proxy scales only |
| local GR or PPN promoted | fail | no theorem and no official pass |
| claim ceiling enforced | pass | no public/local-GR claim |

## 10. What Actually Improved

This did not win the GR belt.

It improved the corner-work:

```text
we now know exactly which no-hair facts must be proved,
which residual sectors would need bounding,
and which local tests are most dangerous.
```

That is what a serious theory-building programme needs.

The route is now:

```text
prove A3-A7,
or source-lock official bounds,
or demote local branch to modified-exterior closure.
```

## 11. Next Target

Next checkpoint:

```text
354-official-local-bound-source-lock-or-nohair-proof-deepening.md
```

There are two sensible next moves:

```text
Option 1:
  deepen the no-hair proof:
  try to derive class-only boundary action, no marker fields, and Ward flux closure.

Option 2:
  source-lock the PPN/local-bound scales:
  replace proxy values with cited official/current bounds before any numeric local test.
```

Default:

```text
do Option 1 first for one more pass,
then source-lock official bounds if the theorem still does not close.
```

## 12. Decision

```text
conditional_boundary_nohair_contract_written_proxy_PPN_bound_runner_ready_no_local_GR_promotion
```

The local GR route is not solved.

But it is no longer foggy.
It is an explicit fight:

```text
class-only boundary action,
no marker fields,
no radial scalar hair,
single metric coupling,
Ward/Bianchi closure,
or bounded residuals.
```

That is exactly the right shape for the next stage.
