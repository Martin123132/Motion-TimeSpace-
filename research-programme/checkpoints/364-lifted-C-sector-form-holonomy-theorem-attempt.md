# 364 - Lifted C Sector Form Holonomy Theorem Attempt

Private derivation checkpoint. This is not a public WEP, clock, PPN, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 363 set the right target:

```text
do not smuggle in exp(P_D C)g as a local-GR proof.
try to derive the lifted C route.
```

This checkpoint attempts that derivation directly.

The question is:

```text
can local Cperp become exact/null representative data,
while global P_D C survives as cosmological memory?
```

Short answer:

```text
yes conditionally, by a lifted 3-form/domain-class construction;
no as a completed parent-action theorem yet.
```

That is progress, but not promotion.

## 2. Machine Artifact

Script:

```text
scripts/lifted_C_sector_form_holonomy_theorem_attempt.py
```

Run:

```text
runs/20260601-203000-lifted-C-sector-form-holonomy-theorem-attempt
```

Outputs:

```text
results/source_register.csv
results/theorem_assumptions.csv
results/degree_audit.csv
results/local_null_derivation.csv
results/FLRW_survival.csv
results/matter_metric_implications.csv
results/failure_modes.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

Status:

```text
lifted_C_three_form_local_residual_nullness_conditionally_derived_parent_action_boundary_domain_missing
```

Claim ceiling:

```text
conditional_lifted_C_theorem_shape_only_no_parent_selector_EH_WEP_clock_PPN_or_local_GR_promotion
```

Source paths missing:

```text
0
```

## 3. Exact Theorem Attempt

Do not model `C` as an ordinary scalar profile.

Instead define a lifted domain observable:

```text
C_D[D] = N_D^{-1} int_D J_C
```

where:

```text
J_C is a 3-form domain memory current.
```

Local representative shifts are required to act as:

```text
delta J_C = d B_perp
```

Then:

```text
delta C_D
= N_D^{-1} int_D delta J_C
= N_D^{-1} int_D d B_perp
= N_D^{-1} int_partialD B_perp.
```

So if the parent action supplies the stationary local boundary condition:

```text
int_partialD B_perp = 0,
```

then:

```text
delta_Cperp C_D = 0.
```

That is the clean mathematical mechanism.

Local `Cperp` is not made harmless by pretending scalar exactness worked.

It is made harmless only if it is no longer a scalar field:

```text
Cperp = exact/null representative motion of a lifted class object.
```

## 4. What Was Actually Derived

The Stokes step is real:

```text
delta J_C = dB_perp
implies
delta C_D = boundary primitive.
```

Therefore, boundary-null representative shifts are invisible to `C_D`.

If matter sees only:

```text
exp(C_D) g_mn
```

then local representative shifts do not create direct matter vertices:

```text
delta_Cperp S_m[psi, exp(C_D)g] = 0.
```

This is stronger than the scalar route.

But the decisive boundary condition:

```text
int_partialD B_perp = 0
```

is still not parent-derived.

So the theorem is conditional.

## 5. Degree Audit

The degree bookkeeping is important.

| Object | Degree | Result |
|---|---|---|
| scalar `Cperp` | 0-form | failed; scalar exactness does not follow |
| `J_rel` memory flux | 2-form/current-like | conditional cohomology success on shell |
| `J_C` domain memory current | 3-form | local residual variations can be boundary-null |
| `B_perp` primitive | 2-form | missing boundary Euler condition |
| `C_D` class observable | domain integral/class scalar | invariant if boundary primitive vanishes |

This avoids the old mistake:

```text
J_rel exactness does not transfer to scalar Cperp.
```

Instead:

```text
Cperp must be reinterpreted as representative motion inside a lifted current/class sector.
```

One warning:

```text
a spatial 3-form can carry a domain/orientation volume class.
```

So topology alone does not force the whole 3-form to vanish locally.

The derived thing is narrower:

```text
exact local residual variations are invisible if their boundary primitive vanishes.
```

That distinction matters.

## 6. FLRW Survival

Checkpoint 275 and 276 give the bridge:

```text
P_coh[Q]^i_j = (1/3)<Tr Q>_D delta^i_j
```

for fixed physical `D`.

Then:

```text
J_C = det(P_coh Q) Omega_D / V_D
```

and:

```text
int_D J_C = det(Q_coh).
```

For FLRW:

```text
Q_coh = (N/u3) I,
```

so:

```text
int_D J_C = (N/u3)^3.
```

This means the lifted route can preserve cosmological memory while local residual shifts quotient away.

But only if:

```text
D, P_D, P_coh, and the boundary primitive are parent-owned.
```

That is the unresolved derivation burden.

## 7. Matter Metric Consequence

If the lifted theorem is completed, then the projected metric route becomes:

```text
matter sees the class observable C_D or P_D C,
not arbitrary local representative data.
```

Then:

```text
ghat_mn = exp(P_D C) g_mn
```

could be upgraded from closure to theorem.

Current status:

| Claim | Status |
|---|---|
| local representative shifts invisible to `C_D` | conditional pass |
| boundary primitive derived | fail |
| FLRW memory survives | conditional pass |
| domain/projector parent-owned | fail |
| matter metric parent-derived | fail |
| local GR promoted | fail |

So this is a promising derivation shape, not a finished derivation.

## 8. Failure Modes

The route fails back to closure if any of these happen:

| Failure | Meaning |
|---|---|
| boundary primitive imposed | `int_partialD B_perp=0` is just a no-leak axiom |
| domain selector imposed | `D/P_D/P_coh` is a convenient smoothing choice |
| matter sees representative | fifth-force/WEP/clock risks return |
| `J_C` added by hand | the 3-form is a repair field, not MTS geometry |
| FLRW class killed | local quotient erases the cosmological signal |

This is the useful pressure map.

It tells us exactly what has to be derived next.

## 9. Decision

Decision:

```text
lifted_C_three_form_local_residual_nullness_conditionally_derived_parent_action_boundary_domain_missing
```

Meaning:

```text
the lifted 3-form/class route gives a real conditional mechanism:
local residual exactness reduces to a boundary primitive by Stokes.
```

But:

```text
the boundary primitive condition,
the domain/projector ownership,
and the representative-invariant matter action
are not derived yet.
```

No promotion:

```text
projected metric remains closure/theorem target,
WEP/clock/PPN not passed,
Einstein-Hilbert exterior not derived,
local GR not derived.
```

## 10. Next Target

Next:

```text
365 - Lifted C Boundary Primitive And Domain Euler Equation
```

Aim:

```text
derive or reject int_partialD B_perp = 0
from a parent variational boundary/domain equation.
```

This is the next real bottleneck.

If we can derive that, the local-GR route gets much less grim.

If we cannot, the lifted `C` route stays as a disciplined closure branch.
