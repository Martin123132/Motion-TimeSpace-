# 358 - Local EH Exterior Operator From Ward-Closed Action

Private derivation checkpoint. This is not a public local-GR, PPN, WEP, redshift, fifth-force, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 357 left the right next question:

```text
if the Ward-force ledger closes,
does the local exterior automatically become Einstein-Hilbert/GR?
```

Short answer:

```text
no, not automatically.
```

Ward closure is necessary.

But it is not sufficient by itself, because a conserved metric equation can still contain:

```text
higher curvature,
scalar-tensor pieces,
vector/preferred-frame pieces,
torsion/nonmetricity,
or nonlocal/memory kernels.
```

So this checkpoint sharpens the exact sufficiency theorem:

```text
Ward closure + no-hair + universal coupling + metric-only local second-order exterior
  -> Einstein-Hilbert exterior
  -> Newton/PPN GR baseline.
```

The new obstruction is:

```text
the second-order metric-only operator is still an axiom/target,
not parent-derived.
```

## 2. Machine Artifact

Script:

```text
scripts/local_EH_exterior_operator_from_Ward_closed_action.py
```

Run:

```text
runs/20260601-184500-local-EH-exterior-operator-from-Ward-closed-action
```

Key outputs:

```text
results/source_register.csv
results/EH_sufficiency_assumptions.csv
results/operator_basis_audit.csv
results/EH_operator_theorem_steps.csv
results/operator_obstruction_ledger.csv
results/weak_field_limit_map.csv
results/next_queue.csv
results/gate_results.csv
results/decision.csv
status.json
DONE.txt
```

Status:

```text
EH_exterior_operator_sufficiency_sharpened_Ward_closure_not_enough_operator_axioms_open_no_local_GR_promotion
```

Claim ceiling:

```text
conditional_EH_operator_sufficiency_only_no_parent_EH_derivation_no_local_GR_or_PPN_pass
```

Source paths missing:

```text
0
```

## 3. Sufficiency Stack

The local EH route now needs these assumptions.

| Assumption | Statement | Status after 357 |
|---|---|---|
| `A0` compact local exterior | outside ordinary matter support; source appears as conserved monopole/boundary data | definition plus monopole condition |
| `A1` single physical metric/coframe | all matter, clocks, rulers, photons, lab standards see one `g/e` | not derived hard open |
| `A2` Ward force closure | `F_X + F_P + F_boundary + F_domain + F_matter_nonmetric = 0` or absent through PPN order | mapped, not proved |
| `A3` no local MTS hair | `E_MTS_munu` is zero, pure gauge, or conserved monopole boundary renormalization | candidate mechanisms only |
| `A4` metric-only exterior variables | only the metric/coframe propagates locally | not derived |
| `A5` local diffeomorphism-invariant action | remaining exterior action is local and covariant | structural target |
| `A6` second-order metric equations | no higher than second derivatives in the surviving metric equation | not parent-derived |
| `A7` four-dimensional low-energy exterior | local tested scales are effectively 4D | assumed for local tests |

If all of these hold, the exterior action has the conditional form:

```text
S_ext[g]
  = (16 pi G_eff)^-1 int_E sqrt(-g)(R - 2 Lambda_eff)
  + boundary.
```

Then:

```text
G_munu + Lambda_eff g_munu = 0
```

in local vacuum, and:

```text
G_munu = 0
```

to compact Solar-System PPN order.

## 4. Operator Basis Audit

The dangerous part is not conservation anymore.

The dangerous part is the operator basis.

| Operator family | Example | Local effect | Status |
|---|---|---|---|
| Einstein-Hilbert plus `Lambda` | `sqrt(-g)(R - 2 Lambda)` | GR exterior baseline | target operator |
| boundary/topological terms | GHY/topological boundary pieces | no bulk PPN effect if owned | allowed if owned |
| higher curvature | `R^2`, `R_munu R^munu`, `Weyl^2` | extra massive scalar/spin-2 or higher-derivative corrections | must forbid or bound |
| scalar-tensor/auxiliary metric coupling | `phi R`, `(nabla phi)^2`, `V(phi)` | `gamma`, `beta`, WEP, fifth-force residuals | must no-hair or retain |
| vector/preferred-frame terms | `u^mu u^nu R_munu`, domain normal operators | `alpha1`, `alpha2`, preferred-frame residuals | quarantined unless silent |
| torsion/nonmetricity | `T^2`, `Q^2`, independent connection couplings | spin/WEP/clock/light-cone residuals | must forbid or bound |
| nonlocal/memory kernel | `R Box^-1 R`, history/domain kernels | scale-dependent fifth force or secular drift | must no-hair or bound |

This is the main correction to a too-fast GR argument:

```text
conserved != Einstein.
```

A non-EH operator can still be conserved.

So MTS must either:

```text
derive the EH operator selection,
or retain/bound the extra operator corrections.
```

## 5. Conditional EH Operator Theorem

The sharpened theorem is:

```text
If:
  1. the Ward force ledger closes,
  2. local no-hair removes MTS bulk/boundary residuals,
  3. matter universally couples to one metric/coframe,
  4. only the metric/coframe propagates in the exterior,
  5. the exterior action is local, diffeomorphism invariant, 4D, and second-order,

then:
  the local exterior bulk action is Einstein-Hilbert plus Lambda,
  up to boundary/topological pieces.
```

Therefore:

```text
local vacuum exterior -> G_munu + Lambda_eff g_munu = 0.
```

With compact local scale:

```text
Lambda_eff is negligible at PPN order.
```

Then the weak-field GR baseline is:

```text
gamma = 1,
beta = 1,
alpha1 = alpha2 = 0,
metric redshift/WEP follows if universal coupling holds.
```

But this is only a conditional theorem.

MTS has not yet derived the full premise stack.

## 6. Operator Obstruction Ledger

| Obstruction | Meaning | Required fix |
|---|---|---|
| Ward closure not enough | a conserved metric equation can be non-EH | derive second-order metric-only operator restriction or bound extra operators |
| second-order axiom not parent-derived | EH uniqueness relies on excluding `R^2`, `f(R)`, nonlocal terms | parent low-energy/regularity theorem or residual bounds |
| universal matter coupling open | EH metric equation is not enough if matter sees another geometry | derive one matter metric/coframe |
| source normalization open | Newtonian limit needs measured `G` and conserved monopole `M_eff` | derive `kappa/G_eff/M_eff` mapping |
| quarantined preferred-frame/fifth-force sectors | not fully source-locked in runner | source-lock or prove zero |

This is an important refinement.

After 357, we knew which forces had to vanish or be retained.

After 358, we know an additional thing:

```text
even after the forces vanish,
the local operator must still be proven to be EH.
```

## 7. Weak-Field Limit Map

| Quantity | EH value if conditions hold | Open parent issue | Residual if failed |
|---|---|---|---|
| Newtonian Poisson limit | `nabla^2 Phi = 4 pi G_eff rho`; vacuum `nabla^2 Phi=0` | `G_eff/kappa/M_eff` normalization | `delta_G_or_fifth_force` |
| `gamma` | `1` | trace-free/shear/operator corrections vanish | `gamma_minus_1` |
| `beta` | `1` | nonlinear scalar/boundary/higher-curvature terms vanish | `beta_minus_1` |
| preferred-frame | `alpha1=alpha2=0` | domain/vector/coframe preferred sectors vanish | preferred-frame residuals |
| clock/WEP | metric redshift and WEP | universal coupling not derived | `alpha_clock_redshift`, `eta_WEP` |

This gives us a cleaner empirical bridge:

```text
operator theorem -> GR baseline,
retained operator/force pieces -> residual vector,
residual vector -> source-locked runner.
```

## 8. What Improved

Before this checkpoint, the route was:

```text
close the Ward/no-hair channels -> hopefully GR.
```

Now it is:

```text
close the Ward/no-hair channels
  -> metric-only exterior
  -> local, diffeo, 4D, second-order operator restriction
  -> EH plus Lambda
  -> Newton/PPN baseline.
```

That is a proper theorem ladder.

It tells us exactly what has to be derived, not merely what has to be true.

## 9. What Still Fails

No local-GR promotion follows.

Still open:

```text
single physical metric/coframe,
Ward force closure,
local no-hair,
metric-only exterior variables,
second-order EH operator selection,
source normalization,
universal matter coupling,
quarantined preferred-frame/fifth-force source locks.
```

The most important result of this checkpoint is:

```text
Ward closure is necessary but not sufficient.
```

If higher-curvature or nonlocal operators remain, MTS becomes:

```text
a modified-gravity branch with residual bounds,
not a derived local-GR branch.
```

## 10. Gate Results

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | all cited source files exist |
| EH sufficiency stack written | pass | eight assumptions and five theorem steps mapped |
| operator basis audited | pass | seven operator families audited; five require forbidding/bounding/quarantine |
| Ward closure sufficient by itself | fail | conserved equations can still include non-EH operators |
| EH operator parent-derived | fail | several sufficiency assumptions remain not derived/not proved |
| weak-field GR baseline conditional | pass | if EH stack holds, Newton/PPN baseline is defined |
| local GR promoted | fail | operator axioms, universal coupling, source normalization, and no-hair remain open |
| PPN pass claimed | fail | no numeric residual comparison performed |
| claim ceiling enforced | pass | no parent EH derivation, local-GR, or PPN pass claim |

## 11. Decision

Decision:

```text
EH_exterior_operator_sufficiency_sharpened_Ward_closure_not_enough_operator_axioms_open_no_local_GR_promotion
```

Meaning:

```text
Closing the Ward/no-hair ledger is necessary but not enough.
The remaining local exterior must also be proven metric-only, local, diffeomorphic, 4D, and second-order.
Only then does the EH exterior follow conditionally.
```

No promotion:

```text
local GR not derived,
PPN not passed,
EH operator not parent-derived.
```

## 12. Next Target

Next:

```text
359 - Source-Locked PPN Residual Runner From Derived Force Ledger
```

Why now:

```text
we have enough structure to build a disciplined runner:
  - GR baseline if EH stack holds,
  - retained force/operator residuals if it does not,
  - source-locked numeric guardrails where available,
  - quarantined sectors where source locks are missing.
```

Pass condition:

```text
numeric-ready sectors compare against locked gamma/beta/WEP/clock scales,
open sectors remain quarantined,
and no residual with missing coefficients is treated as a pass.
```

That runner will not prove GR.

It will tell us which remaining debts are most dangerous empirically.
