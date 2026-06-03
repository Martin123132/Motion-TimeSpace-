# 370 - Common-Mode phi_C Coefficient Map

Private coefficient-map checkpoint. This is not a public WEP, clock, PPN, fifth-force, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 369 built the source-locked local-bound runner.

The runner still had one central missing object:

```text
how does local phi_C feed clock, gamma, beta, and fifth-force rows?
```

This checkpoint writes the weak-field coefficient map for the labelled class-metric branch:

```text
ghat_mn = exp(phi_C) g_mn.
```

Result:

```text
common-mode phi_C is locally dangerous unless it is theorem-zero, absorbed in a very restricted way, or tiny against U_GR.
```

No local pass is claimed.

## 2. Machine Artifact

Script:

```text
scripts/common_mode_phiC_coefficient_map.py
```

Run:

```text
runs/20260601-223000-common-mode-phiC-coefficient-map
```

Outputs:

```text
results/source_register.csv
results/weak_field_map.csv
results/coefficient_budgets.csv
results/zero_theorem_requirements.csv
results/runner_update.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

Status:

```text
phiC_weak_field_coefficient_map_written_common_mode_bounds_require_zero_theorem_or_tiny_gradient_no_pass
```

Claim ceiling:

```text
coefficient_map_and_budget_only_no_clock_PPN_WEP_fifth_force_EH_or_local_GR_pass
```

Source paths missing:

```text
0
```

## 3. Weak-Field Map

Use:

```text
ghat_mn = exp(phi_C) g_mn.
```

For weak-field bookkeeping:

```text
g00 = -1 + 2U + ...
gij = (1 + 2U) deltaij + ...
```

The common conformal factor gives:

```text
U_time  ~= U - phi_C/2
U_space ~= U + phi_C/2
```

So the class scalar can affect:

```text
clock/redshift through Delta phi_C,
gamma through the time/space potential split,
fifth-force pressure through grad phi_C,
beta through second-order phi_C and residual operator terms.
```

Sign conventions are not used for pass/fail here.

Only absolute budget pressure is used.

## 4. Coefficient Budgets

| Residual | Proxy map | Source target | Required phi_C condition if proxy applies |
|---|---|---:|---|
| `alpha_clock_redshift` | `~ 0.5 * |Delta phi_C / Delta U_GR|` | `3.1e-5` | `|Delta phi_C / Delta U_GR| <= 6.2e-5` |
| `gamma_minus_1` | `~ |phi_C / U_GR|` or `r_grad` | `2.3e-5` | `r_grad <= 2.3e-5` |
| `beta_minus_1` | needs `phi_C = s1 U + s2 U^2 + ...` plus EH residual | `7.8e-5` | coefficient still missing |
| `eta_WEP` | species-specific `F_A(C_D)` difference | `2.8e-15` | universal species function required |
| `delta_G` / fifth force | `~ 0.5 * |grad phi_C|/|grad U_GR|` | quarantined | source lock missing |

This is a useful result, but it is harsh:

```text
unless local phi_C is zero/constant, gamma and clock rows demand very small common-mode gradients.
```

## 5. Zero-Theorem Routes

The cleanest ways to survive are:

| Route | Condition | Kills |
|---|---|---|
| strict local class silence | `grad phi_C = 0` and `Delta phi_C = 0` locally | clock, gamma proxy, fifth-force proxy |
| universal species function | same `F(C_D)` for all matter sectors | direct WEP class response |
| EH operator recovery | exterior dynamics reduce to EH | residual operator terms in gamma/beta/slip |
| measured-GM absorption | conserved universal monopole absorbed into measured `GM` | only limited monopole pressure |
| source-locked fifth-force manifest | fifth-force row gets real bound and coefficient | removes quarantine ambiguity |

The first route is the best local safety theorem:

```text
stationary local domains must have locally constant phi_C.
```

Not merely:

```text
small-ish phi_C.
```

## 6. Runner Update

The runner rows now update as:

| Runner row | Update | Claim status |
|---|---|---|
| `alpha_clock_redshift` | proxy `c_clock ~= 1/2`, needs `|Delta phi_C/Delta U| <= 6.2e-5` | budget only |
| `gamma_minus_1` | proxy `c_gamma ~= 1`, needs `r_grad <= 2.3e-5` | budget only |
| `beta_minus_1` | second-order map still missing | blocked |
| `eta_WEP` | common-mode does not solve species universality | hardest ready gate |
| `delta_G` / fifth force | half-gradient proxy identified | quarantined |

So:

```text
phi_C coefficient mapping improves the runner,
but does not pass the runner.
```

## 7. What Still Fails

Still open:

```text
derive grad phi_C = 0 for stationary local domains,
derive universal F(C_D) across species,
derive beta second-order coefficients,
source-lock fifth-force / preferred-frame / xi rows,
derive or bound residual EH operator terms.
```

This checkpoint makes the local branch more testable.

It also makes clear why it is not yet locally safe.

## 8. Decision

Decision:

```text
phiC_weak_field_coefficient_map_written_common_mode_bounds_require_zero_theorem_or_tiny_gradient_no_pass
```

Meaning:

```text
common-mode phi_C now has explicit weak-field budget pressure.
```

But:

```text
no zero theorem,
no beta coefficient,
no WEP species theorem,
no fifth-force source lock,
no EH recovery.
```

No promotion:

```text
clock not passed,
PPN not passed,
WEP not passed,
fifth-force not scored,
local GR not derived.
```

## 9. Next Target

Next:

```text
371 - WEP Species Universality Or Active eta Runner
```

Aim:

```text
prove universal F(C_D) across matter sectors,
or keep eta_WEP as the active hardest ready local gate.
```

Reason:

```text
even perfect common-mode phi_C silence does not save the branch
if different species see different class functions.
```
