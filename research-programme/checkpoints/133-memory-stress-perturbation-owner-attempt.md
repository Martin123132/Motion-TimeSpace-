# 133 - Memory Stress Perturbation Owner Attempt

Private theorem attempt. This is not a public claim.

## 1. Trigger

Checkpoint 132 found a useful first-order cancellation:

```text
delta C_coh^(1) = 0
```

around the FLRW bulk branch.

That made smooth memory a serious theorem target rather than a plateau axiom.

But checkpoint 132 also left the central question open:

```text
Can a real stress tensor own this smoothness?
```

This checkpoint tests the stress-owner options.

## 2. Machine Artifact

Script:

```text
research-programme\scripts\memory_stress_perturbation_owner_attempt.py
```

Run:

```text
research-programme\runs\20260531-185800-memory-stress-perturbation-owner-attempt
```

Generated:

```text
source_register.csv
stress_owner_candidates.csv
conservation_obstruction.csv
subhorizon_suppression_estimate.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
perfect_fluid_exact_smooth_memory_rejected_subhorizon_route_open
```

Claim ceiling:

```text
memory_stress_owner_attempt_no_growth_promotion
```

## 3. Main Result

The exact smooth-memory theorem fails if memory is modeled as a separately conserved perfect fluid.

Reason:

```text
w_mem != -1 during the activation transition.
```

For a separately conserved perfect fluid, setting:

```text
delta_mem = 0
theta_mem = 0
delta p_mem = 0
pi_mem = 0
```

does not solve the linear conservation equations unless special conditions hold.

The obstruction is:

| Equation | Silent substitution | Obstruction | Exact silence condition |
|---|---|---|---|
| background continuity | `rho'_N = 3(rho+p)` | none | defines `w_mem(N)` |
| linear energy conservation | `delta_mem=theta_mem=delta_p_mem=0` | `3(1+w_mem) Phi_prime` | `w_mem=-1`, `Phi_prime=0`, or non-perfect-fluid counterterm |
| linear momentum conservation | `theta_mem=delta_p_mem=pi_mem=0` | `(1+w_mem) k^2 Psi` | `w_mem=-1`, `Psi=0`, or constrained/geometric counterstress |
| Poisson source | `delta_rho_mem=0` | none if a true constraint removes physical `delta_rho_mem` | gauge-invariant constraint |
| anisotropic stress | `pi_mem=0` | depends on `S_stress` variation | no linear shear response |

This is the hard point:

```text
exactly smooth + separately conserved + perfect fluid + w != -1
```

does not work.

## 4. What Remains Viable

Candidate stress owners:

| Candidate | Verdict | Meaning |
|---|---|---|
| pure cosmological constant | rejected | smooth exactly, but cannot reproduce locked `A(a)` transition |
| separately conserved perfect fluid | rejected as exact theorem | conservation sources perturbations when `w_mem != -1` |
| high-sound-speed scalar/k-essence-like sector | viable approximation if derived | perturbations are subhorizon-suppressed, not zero |
| auxiliary constrained memory | best exact route, not derived | memory perturbation could be a constraint, not a propagating fluid mode |
| geometric counterstress | viable if parent identity exists | can evade Euler obstruction only if divergence-free on shell |
| controlled exchange `Q^nu` | dangerous last resort | can cancel sources but risks becoming a fitted force |

So the clean route is not:

```text
ordinary smooth perfect fluid.
```

The clean route is either:

```text
1. non-propagating auxiliary/geometric memory;
2. high-sound-speed subhorizon-suppressed memory;
3. controlled exchange, only if parent-derived and locally silent.
```

## 5. Why This Does Not Kill The Growth Result

The SDSS/eBOSS growth gate in checkpoint 130 is late-time and subhorizon.

If the memory stress behaves like a high-sound-speed dark sector, a rough perturbation scaling is:

```text
delta_mem / delta_m ~ (1+w_mem) (aH / ck)^2
```

On the sampled SDSS/eBOSS linear modes:

```text
k >= 0.02 h/Mpc
```

the largest rough bound in the audit was:

```text
2.70506e-05
```

This maximum occurs near:

```text
z = 0.15
k = 0.02 h/Mpc
```

Representative largest rows:

| z | k `[h/Mpc]` | `|1+w_mem|` | `(aH/ck)^2` | rough bound |
|---:|---:|---:|---:|---:|
| `0.15` | `0.02` | `0.10988899605472524` | `0.00024616335283758514` | `2.705064370878733e-05` |
| `0.38` | `0.02` | `0.0761499313281584` | `0.00022796390260442943` | `1.735943552862629e-05` |
| `0.15` | `0.05` | `0.10988899605472524` | `3.938613645401362e-05` | `4.328102993405973e-06` |
| `0.51` | `0.02` | `0.011873951116018855` | `0.0002216122251948732` | `2.631412728676087e-06` |

Interpretation:

```text
exact smoothness fails for a perfect fluid,
but subhorizon smoothness can be an extremely good approximation if the parent
stress derives high sound speed or non-propagating memory.
```

That means checkpoint 130 is not killed.

It remains:

```text
conditionally plausible, not promoted.
```

## 6. Gates

Gate results:

| Gate | Status | Evidence |
|---|---|---|
| background stress reproduction | pass effective | `w_mem(N)` can be defined from `rho_mem(N)` |
| exact smooth perfect fluid | fail | linear energy/momentum conservation sources perturbations when `w_mem != -1` |
| subhorizon suppression viable | pass conditional | rough `(1+w)(aH/ck)^2` suppression is tiny on tested SDSS/eBOSS modes |
| exact auxiliary/geometric owner | open | would evade perfect-fluid obstruction, but `S_stress` / Bianchi identity is not derived |
| checkpoint-130 growth proxy promoted | fail | proxy remains conditional until stress owner derives smoothness or controlled growth |
| support claim allowed | fail | internal theorem audit only |

## 7. Interpretation

This is a useful correction to the theory route.

The phrase:

```text
smooth memory
```

must now be split into two different claims:

### Exact Smooth Memory

Requires:

```text
auxiliary constrained memory
or geometric counterstress
or a true non-propagating parent sector
```

because a perfect fluid cannot be exactly silent through the activation transition.

### Approximate Subhorizon Smooth Memory

Requires:

```text
c_s^2 ~ 1 or stronger smoothing mechanism
```

and is likely enough for:

```text
SDSS/eBOSS growth gate
late-time subhorizon f_sigma8
checkpoint-130 proxy accuracy
```

but it is not a fundamental derivation unless the sound speed or constraint is derived.

Boxing-score version:

```text
The perfect-fluid route got countered clean.
But MTS slipped the bigger punch: on the actual growth scales, the correction
can be tiny if the parent stress has high sound speed or is constrained.
```

## 8. Consequence For The Framework

This checkpoint improves the framework because it removes a bad hidden assumption.

Before:

```text
maybe memory is exactly smooth.
```

After:

```text
memory cannot be exactly smooth as an ordinary separately conserved perfect
fluid unless w=-1.
```

Therefore a serious parent theory must pick one:

```text
1. derive a non-propagating auxiliary/geometric memory stress;
2. derive a high-sound-speed stress and quantify residual perturbations;
3. derive controlled exchange Q^nu;
4. demote growth to empirical closure-only.
```

This is the correct narrowing.

## 9. Decision

Decision:

```text
memory_stress_owner_status =
perfect_fluid_exact_smooth_memory_rejected_subhorizon_route_open
```

Meaning:

```text
the exact perfect-fluid smooth theorem is rejected;
the growth branch is not killed;
the viable path is high-sound-speed suppression or non-propagating auxiliary /
geometric memory.
```

Do not promote checkpoint 130 as derived growth.

Do not demote checkpoint 130.

Use it as:

```text
a conditional growth benchmark whose theoretical owner is now sharply defined.
```

## 10. Next Target

Create:

```text
134-subhorizon-suppressed-growth-correction-gate.md
```

Purpose:

```text
quantify how large a high-sound-speed memory perturbation correction could be
before checkpoint 130 changes materially.
```

Pass condition:

```text
show that the rough memory perturbation correction is far below the current
growth data sensitivity for k >= 0.02 h/Mpc, or identify the scale/redshift
where it stops being safe.
```

If it passes:

```text
checkpoint 130 becomes a robust late-time subhorizon approximation target.
```

If it fails:

```text
derive auxiliary/geometric counterstress next or demote the smooth-growth route.
```
