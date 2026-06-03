# 269 - Metric Selector Principle Attempt

Private derivation checkpoint. This is not a public local-GR, CMB, BAO, or unified-field claim.

## Purpose

Checkpoint 268 showed:

```text
S_matter[psi, exp(P_D C)g]
```

can be written as an action skeleton and gives:

```text
delta S_matter / delta Cperp = 0.
```

But it left the principle open:

```text
why should matter see P_D C instead of C?
```

This checkpoint attempts the selector principle.

## Machine Artifact

Script:

```text
scripts/metric_selector_principle_attempt.py
```

Run:

```text
runs/20260601-000087-metric-selector-principle-attempt
```

Status:

```text
metric_selector_conditionally_derived_from_residual_gauge_redundancy_parent_gauge_principle_open
```

Claim ceiling:

```text
metric_selector_internal_theorem_target_no_local_GR_or_unification_promotion
```

## Main Result

There is now a clean conditional selector theorem:

```text
if Cperp is a residual gauge / exact representative,
and matter must be invariant under residual representative shifts,
then matter can only depend on P_D C.
```

Write the matter metric as:

```text
bar_g_munu = exp(F[C]) g_munu.
```

Residual shift:

```text
C -> C + eta_perp,
P_D eta_perp = 0.
```

Matter invariance requires:

```text
F[C + eta_perp] = F[C].
```

Therefore:

```text
F[C] = f(P_D C).
```

The coherent limit requires:

```text
f(C_D) = C_D.
```

So:

```text
F[C] = P_D C
```

and:

```text
bar_g_munu = exp(P_D C) g_munu.
```

Then:

```text
delta S_matter / delta Cperp = 0.
```

This is the first proper selector-principle form for the projected matter metric.

## What Is Actually Derived

The metric selector is conditionally derived from these assumptions:

| Axiom | Status |
|---|---|
| `Cperp` shifts are residual gauge / representative changes | not parent-derived |
| all late matter couples to one universal metric | contract |
| matter is invariant under residual shifts | conditional on gauge principle |
| coherent limit recovers `exp(C_D)g` | required |
| no species-specific Weyl compensation | required |
| Bianchi/domain stresses retained | previous conditional pass |

So the result is:

```text
conditional selector theorem,
not parent promotion.
```

## Why This Helps

Before this checkpoint:

```text
exp(P_D C)g
```

was action-writeable but looked like a helpful nonlocal choice.

Now it has a possible principle:

```text
matter couples only to the gauge-invariant quotient representative.
```

This is better than:

```text
choose the projected metric because it passes local tests.
```

The selector is not empirical rescue if the residual gauge principle is derived before scoring.

## What Still Fails

The big missing theorem is now precise:

```text
derive Cperp -> Cperp + eta_perp
```

as a parent first-class constraint, quotient redundancy, or relative-exact cohomology representative.

Without that:

```text
the projected matter metric must be demoted to explicit closure.
```

Other open burdens:

| Obstruction | Status |
|---|---|
| residual gauge principle | main open burden |
| projector parent origin | open |
| domain scale selector | open |
| local microcausality | open |
| late drift saturation | open |
| `B_mem = 2/27`, `Hstar = H0` | not derived |

## Route Comparison

| Route | Verdict |
|---|---|
| quotient/gauge representative | best conditional route |
| relative cohomology class | supporting route |
| boundary-clock normalization | plausible side route |
| ordinary local `exp(C)g` | rejected as lead |
| hard projected-metric closure | allowed only if labelled |

The ordinary local metric stays rejected because it:

```text
breaks residual representative invariance
and sources Cperp.
```

If any residual `Cperp` matter leak remains, the local q-like gate demands:

```text
epsilon < 0.0003105.
```

So the route strongly prefers exact decoupling.

## Decision

Decision:

```text
metric_selector_conditionally_derived_from_residual_gauge_redundancy_parent_gauge_principle_open
```

Meaning:

```text
The projected matter metric is conditionally derivable from a clean selector
principle: if Cperp is a residual gauge/exact representative and matter must be
invariant under residual shifts, then the unique coherent-limit conformal
metric is exp(P_D C)g.
```

But:

```text
the residual gauge/cohomology principle itself is not parent-derived.
```

## Current Theory Status

This is progress.

The local-silence chain is now:

```text
1. ordinary exp(C)g fails as lead;
2. exp(P_D C)g removes Cperp matter source;
3. exp(P_D C)g is action-writeable;
4. exp(P_D C)g is conditionally selected by residual gauge invariance;
5. residual gauge invariance is the next parent theorem target.
```

So the question is no longer:

```text
can we hide Cperp?
```

It is:

```text
is Cperp physically a gauge/exact representative?
```

That is exactly the right kind of field-theory burden.

## Next Target

Next derivation:

```text
derive_Cperp_residual_shift_first_class_constraint_or_demote_metric_selector_to_closure
```

Pass route:

```text
Cperp has a first-class constraint or relative-exact redundancy,
so matter observables must live on the quotient class P_D C.
```

Fail route:

```text
projected matter metric becomes an explicit effective closure rule.
```

## Claim Gates

| Gate | Result |
|---|---|
| conditional selector uniqueness | pass if M1-M6 hold |
| residual gauge principle | not derived |
| cohomology support | partial |
| ordinary local metric | rejected as lead |
| residual `Cperp` leak tolerance | strict |
| local-GR/unification promotion | forbidden |

## Validation

- Script compiles in `.venv-score`.
- Run completed and wrote `DONE.txt`.
- CSV outputs parse cleanly.
- Cited source paths exist.
- No changes were made to `formalization-workbench`.
- Claim ceiling remains internal only; no local-GR or unification promotion is allowed.
