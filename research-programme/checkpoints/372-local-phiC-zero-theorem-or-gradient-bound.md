# 372 - Local phi_C Zero Theorem Or Gradient Bound

Private local-bound checkpoint. This is not a public WEP, clock, PPN, fifth-force, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 371 kept WEP active.

This checkpoint returns to the common-mode class metric:

```text
ghat_mn = exp(phi_C) g_mn.
```

The fair question is:

```text
can stationary local domains force grad(phi_C)=0,
or must the branch satisfy clock/gamma gradient budgets?
```

Answer:

```text
grad(phi_C)=0 follows conditionally inside the labelled local-trivial-class / boundary-state branch.
```

But:

```text
the parent theory still has not derived that boundary-state / local-class split.
```

So:

```text
zero theorem: conditional branch result,
gradient bounds: still required fallback,
local pass: not claimed.
```

## 2. Machine Artifact

Script:

```text
scripts/local_phiC_zero_theorem_or_gradient_bound.py
```

Run:

```text
runs/20260601-231000-local-phiC-zero-theorem-or-gradient-bound
```

Outputs:

```text
results/source_register.csv
results/zero_theorem_assumptions.csv
results/zero_theorem_derivation.csv
results/gradient_bound_matrix.csv
results/edge_case_audit.csv
results/runner_update.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

Status:

```text
local_phiC_zero_conditional_on_boundary_state_and_trivial_class_gradient_bounds_remain_if_not_parent_derived
```

Claim ceiling:

```text
conditional_zero_theorem_and_gradient_budget_only_no_clock_gamma_fifth_force_WEP_EH_or_local_GR_pass
```

Source paths missing:

```text
0
```

## 3. Conditional Zero Theorem

Use:

```text
phi_C = lambda C_D.
```

The boundary-state selector target is:

```text
sigma_D = Theta(b_D) Theta(c_D),
```

where:

```text
b_D = IR MTS boundary-bath strength,
c_D = ||[J_B]_D||.
```

For stationary local bound domains, the labelled closure branch assumes:

```text
b_D = 0 and/or c_D = 0,
Q_rel = 0.
```

Then:

```text
C_D|local = 0 or constant.
```

Therefore:

```text
grad(phi_C) = 0,
Delta phi_C = 0.
```

This kills the common-mode class-metric contribution to:

```text
clock drift,
gamma proxy,
class-gradient fifth-force proxy.
```

But only inside that branch.

## 4. Why This Is Not A Local-GR Proof

The needed parent theorem is still missing:

```text
local bound domains are closed/gapped in the MTS bath channel
and/or have trivial relative boundary-current class,
while FLRW domains are open/nontrivial.
```

Checkpoint 300 made this criterion sharp.

It did not derive it.

So this checkpoint proves:

```text
if local trivial class / boundary-state silence holds,
then local phi_C gradients vanish.
```

It does not prove:

```text
local trivial class / boundary-state silence holds in the parent theory.
```

That distinction is the whole game.

## 5. Gradient Fallback Bounds

If the zero theorem is not accepted as parent-derived, the branch must satisfy:

| Residual | Proxy | Required fallback |
|---|---|---|
| `gamma_minus_1` | `~ r_grad` | `r_grad <= 2.3e-5` |
| `alpha_clock_redshift` | `~ 0.5 |Delta phi_C/Delta U|` | `|Delta phi_C/Delta U| <= 6.2e-5` |
| `delta_G` / fifth force | `~ 0.5 r_grad` | quarantined until source-locked |
| `beta_minus_1` | second-order `phi_C` + EH residual | blocked |
| `eta_WEP` | species split, not common-mode gradient | still active |

So the common-mode branch has a clear local rule:

```text
zero it by theorem,
or budget it against clock/gamma.
```

## 6. Edge Cases

Strict local silence is unsafe to overuse.

| Edge case | Risk |
|---|---|
| ordinary environmental bath | ordinary dissipation mimics MTS boundary bath |
| black holes / horizons | local horizon can be gapless/nontrivial |
| galaxies / clusters | bound but not lab-local; do not erase galaxy pillar |
| time-dependent local systems | radiation can make `b_D` nonzero |
| class-changing events | collapse/merger/domain transition changes `Q_rel` |

These are not details.

They are where a local-silence theorem could accidentally murder the empirical pillars.

## 7. Runner Update

| Runner row | If zero theorem holds | If not |
|---|---|---|
| `gamma_minus_1` | class-metric gamma proxy killed | require `r_grad <= 2.3e-5` |
| `alpha_clock_redshift` | class-metric clock drift killed | require `|Delta phi_C/Delta U| <= 6.2e-5` |
| `delta_G` / fifth force | class-gradient force killed | source-lock before scoring |
| `beta_minus_1` | first-order pressure removed | second-order/EH still open |
| `eta_WEP` | unchanged | unchanged and active |

This is a good result, but not glory.

It makes the local runner sharper.

It does not pass it.

## 8. Decision

Decision:

```text
local_phiC_zero_conditional_on_boundary_state_and_trivial_class_gradient_bounds_remain_if_not_parent_derived
```

Meaning:

```text
strict local phi_C silence follows inside the labelled local-trivial-class branch.
```

But:

```text
the parent boundary-state / class-selection theorem is not derived.
```

No promotion:

```text
clock not passed,
gamma not passed,
fifth-force not scored,
WEP still active,
Einstein-Hilbert exterior not derived,
local GR not derived.
```

## 9. Next Target

Next:

```text
373 - One Observed Coframe Parent Selector Or WEP Closure
```

Aim:

```text
attempt a parent selector for one observed coframe / common F(C_D),
separate from representative invariance.
```

Because:

```text
even perfect local phi_C silence does not solve species universality.
```
