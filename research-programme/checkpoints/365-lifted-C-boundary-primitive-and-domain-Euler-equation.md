# 365 - Lifted C Boundary Primitive And Domain Euler Equation

Private derivation checkpoint. This is not a public WEP, clock, PPN, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 364 found the lifted `C` mechanism:

```text
delta C_D = N_D^-1 int_partialD B_perp.
```

So the decisive missing condition was:

```text
int_partialD B_perp = 0.
```

This checkpoint asks whether that condition can be derived from boundary/domain variation rather than imposed.

Answer:

```text
yes, inside fixed relative-class admissible variations;
no, not yet as a full physical domain/class selection theorem.
```

That is a meaningful improvement.

It is not local-GR promotion.

## 2. Machine Artifact

Script:

```text
scripts/lifted_C_boundary_primitive_and_domain_Euler_equation.py
```

Run:

```text
runs/20260601-205000-lifted-C-boundary-primitive-and-domain-Euler-equation
```

Outputs:

```text
results/source_register.csv
results/target_condition.csv
results/variational_derivation.csv
results/Euler_to_primitive_bridge.csv
results/branch_readout.csv
results/no_overclaim_rules.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

Status:

```text
boundary_primitive_condition_derived_as_fixed_relative_class_admissibility_physical_class_selection_open
```

Claim ceiling:

```text
admissibility_derivation_only_no_physical_domain_selector_matter_metric_EH_PPN_or_local_GR_promotion
```

Source paths missing:

```text
0
```

## 3. The Boundary Primitive Target

From checkpoint 364:

```text
C_D[D] = N_D^-1 int_D J_C
```

and local representative shifts:

```text
delta J_C = d B_perp.
```

Therefore:

```text
delta C_D
= N_D^-1 int_D dB_perp
= N_D^-1 int_partialD B_perp.
```

So local representative invisibility needs:

```text
int_partialD B_perp = 0.
```

If this is merely asserted, the lifted `C` branch is closure.

If it follows from a relative class variational rule, the branch gets stronger.

## 4. Variational Derivation

Use the relative current pair:

```text
J_rel = (j_3, b_2)
```

with relative closure:

```text
d_rel J_rel = (d j_3, i*j_3 - d_boundary b_2) = 0.
```

Define the relative charge/class:

```text
Q_rel[D] = int_D j_3 - int_partialD b_2.
```

Now restrict local representative/domain variations to fixed relative class:

```text
delta Q_rel[D] = 0.
```

For a pure local representative shift:

```text
delta j_3 = dB_perp.
```

Boundary exchange consistency gives:

```text
delta b_2 = B_perp + d_boundary gamma_1.
```

Then:

```text
delta Q_rel
= int_D dB_perp - int_partialD (B_perp + d_boundary gamma_1)
= int_partialD B_perp - int_partialD B_perp
= 0.
```

So within a fixed relative class:

```text
int_partialD B_perp
```

is not a physical leakage of `C_D`.

It is absorbed by the boundary representative.

That is the key result:

```text
the primitive-null condition is derived as class-preserving admissibility,
not as arbitrary silence.
```

## 5. How This Connects To The Domain Euler Equation

Checkpoint 277 derived the free-boundary variation:

```text
delta C_coh
= V_D^-1 int_partialD eta[
  (2a/b)(theta-a) - (a^2/b^2)(R-b)
] dSigma.
```

That Euler equation was real, but degenerate.

It allowed many stationary FLRW and local domains.

Checkpoint 278 improved this by restricting admissible boundary motion:

```text
delta Q_rel[D] = 0.
```

The combined statement is:

```text
Euler stationarity is only tested on relative-class-preserving domain variations.
```

This narrows the degeneracy.

But it does not yet choose the physical class.

So the current result is:

```text
boundary primitive condition: conditionally derived inside a class;
physical domain/class selection: still open.
```

## 6. Branch Readout

| Branch | Class assignment | Primitive status | Promotion status |
|---|---|---|---|
| stationary local vacuum | `Q_rel = 0` | fixed-class representative shifts have no `C_D` leakage | conditional silence, not class selection |
| FLRW coherent domain | `Q_rel != 0` | local exact shifts do not erase global class | conditional memory survival |
| tracefree shear / GW | no scalar coherent volume class if `P_coh` removes tracefree sector | safe only if shear does not source class change | conditional |
| collapse / merger | possible class-changing event | primitive need not vanish | source law open |
| matter coupling | matter should see `C_D/P_D C` only | invisible only if matter action is representative-invariant | next theorem target |

This is a good split.

It says local silence and FLRW memory are compatible in one relative-current language.

But compatibility is not the same as parent selection.

## 7. What Is Still Missing

Still not derived:

| Missing piece | Why it matters |
|---|---|
| physical class selection | parent must select local `Q_rel=0` and FLRW nonzero class |
| representative-invariant matter action | matter must see only `C_D/P_D C`, not `B_perp` or scalar data |
| event source law | collapse/merger class changes need conservation bookkeeping |
| amplitude/normalization | relative current does not derive `u3`, `B_mem`, level, or endpoints |
| EH exterior operator | local GR requires metric-only second-order exterior equations |

So this is not the final GR bridge.

It is a real support beam for it.

## 8. No-Overclaim Rules

| Rule | Meaning |
|---|---|
| primitive null is admissibility | `int_partialD B_perp=0` holds inside fixed relative class variations |
| class selection is open | parent still must choose which relative class is physically realized |
| matter selector is open | WEP/clock/PPN cannot be claimed until matter ignores representatives |
| boundary current is not amplitude owner | invariance does not derive `u3`, `B_mem`, charge level, or endpoints |

This is exactly the sort of thing we want:

```text
derive what can be derived,
label what is still closure,
do not burn the route by overclaiming it.
```

## 9. Decision

Decision:

```text
boundary_primitive_condition_derived_as_fixed_relative_class_admissibility_physical_class_selection_open
```

Meaning:

```text
the boundary primitive condition is no longer a naked axiom
inside fixed relative class sectors.
```

But:

```text
the parent theory still has to select the physical local/FLRW classes,
and matter must be shown to couple only to the class observable.
```

No promotion:

```text
projected metric remains closure/theorem target,
matter selector not derived,
WEP/clock/PPN not passed,
Einstein-Hilbert exterior not derived,
local GR not derived.
```

## 10. Next Target

Next:

```text
366 - Representative-Invariant Matter Action For Lifted C
```

Aim:

```text
prove or reject that matter actions depend only on C_D/P_D C
and not on B_perp, scalar Cperp, or representative data.
```

This is the next best GR-facing gate.

If it works, `exp(P_D C)g` starts moving from closure toward theorem.

If it fails, the branch stays an explicitly labelled effective closure.
