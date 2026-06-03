# 361 - Residual Gauge Principle For Projected Matter Metric

Private derivation checkpoint. This is not a public WEP, clock, PPN, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 360 made the universal-coupling route sharp:

```text
if matter sees one observed metric/coframe
and has no direct non-geometric MTS arguments,
then direct WEP/clock vertices vanish.
```

But the matter metric that best protects the local branch is:

```text
ghat_munu = exp(P_D C) g_munu,
```

not:

```text
ghat_munu = exp(C) g_munu.
```

So the question is:

```text
is Cperp genuinely residual gauge / exact representative data,
or is exp(P_D C)g just an imposed projected-metric closure?
```

Short answer:

```text
the selector theorem is conditionally clean,
but Cperp exactness is still not parent-derived.
```

So the projected metric is not promoted.

It is also not dead yet.

It remains a precise theorem target.

## 2. Machine Artifact

Script:

```text
scripts/residual_gauge_principle_for_projected_matter_metric.py
```

Run:

```text
runs/20260601-193000-residual-gauge-principle-for-projected-matter-metric
```

Key outputs:

```text
results/source_register.csv
results/axiom_context.csv
results/gauge_selector_derivation.csv
results/C_exactness_requirements.csv
results/fork_table.csv
results/residual_impact.csv
results/decision_matrix.csv
results/next_queue.csv
results/gate_results.csv
results/decision.csv
status.json
DONE.txt
```

Status:

```text
residual_gauge_selector_theorem_conditional_Cperp_exactness_still_open_projected_metric_not_promoted
```

Claim ceiling:

```text
conditional_residual_gauge_selector_only_no_universal_coupling_WEP_or_local_GR_promotion
```

Source paths missing:

```text
0
```

## 3. Selector Derivation

Decompose:

```text
C = C_D + Cperp,
P_D Cperp = 0,
C_D = P_D C.
```

Consider a kernel shift:

```text
C -> C + eta_perp,
P_D eta_perp = 0.
```

If `eta_perp` is a genuine residual gauge / exact representative shift, then physical matter observables must obey:

```text
F[C + eta_perp] = F[C].
```

That means the matter-visible scalar `F[C]` must descend to the quotient:

```text
F[C] = f(P_D C).
```

The coherent-limit normalization fixes:

```text
f(C_D) = C_D.
```

So:

```text
F[C] = P_D C,
```

and therefore:

```text
ghat_munu = exp(P_D C) g_munu.
```

This is the clean conditional theorem.

The algebra works.

The missing burden is not the selector algebra.

It is:

```text
prove eta_perp is gauge/exact in the parent theory.
```

## 4. Presymplectic Quotient Route

The best route is inherited from the topological projector work.

If:

```text
Cperp = d_rel alpha
```

or is otherwise relative-trivial, and its local boundary primitive vanishes, then a topological action changes only by a boundary term:

```text
delta_eta S_top = int_D d_rel(...)
              = int_partialD (...).
```

For compact stationary local domains, if that boundary term vanishes:

```text
Theta(eta_perp) = 0 or boundary-only,
Omega(eta_perp, delta) = 0.
```

Then `eta_perp` is a null direction of the presymplectic form.

The physical phase space is:

```text
Phase_phys = ConstraintSurface / ker(Omega),
```

so:

```text
C ~ C + eta_perp,
[C] = C / ker(P_D).
```

Then the projected matter metric is not a patch.

It is quotient invariance.

But the key phrase is:

```text
if Cperp is relative-exact.
```

That theorem is still missing for the `C` sector.

## 5. Cperp Exactness Requirements

| Requirement | Needed statement | Current status |
|---|---|---|
| `C` sector class-valued | `C` is a representative of a topological/relative class, not an ordinary scalar observable | not derived |
| relative-exact kernel | local `Cperp` can be written as `d_rel alpha` or relative-trivial data | analogy to `J_rel`, not proof |
| vanishing local boundary primitive | local compact boundary primitive/charge for `eta_perp` vanishes | contract |
| presymplectic degeneracy | `Omega(eta_perp,delta)=0` on the constraint surface | conditional |
| projector covariance | `P_D` is covariant/dynamical/topological, not fixed externally | conditional |
| no material marker | no boundary marker/species label makes the representative physical | open |
| FLRW class survives | local quotient does not delete cosmological `P_D C` memory | conditional shape only |

This is the exact theorem bill.

Until these are paid, the selector is conditional.

## 6. Fork Table

| Fork | Meaning | Matter metric status | Verdict |
|---|---|---|---|
| residual gauge/exact representative | `Cperp` is a presymplectic null direction | `exp(P_D C)g` conditionally derived | best route |
| ordinary physical scalar `Cperp` | `Cperp` has local kinetic/source support | `exp(P_D C)g` is imposed closure | demote |
| fixed external projector | `P_D` chosen outside parent variation | nonlocal closure with Ward risk | forbidden for promotion |
| material-marker projector | physical marker selects representative | formal covariance hides physical mark | closure/residual |
| relative cohomology local-only | local `Cperp` exact, FLRW class survives | promising if same `P_D` owns both limits | live but unfinished |

This is a useful split.

It tells us what would make the projected metric legitimate, and what would force demotion.

## 7. Residual Impact

If the gauge principle holds:

| Residual | Impact |
|---|---|
| `eta_WEP` | direct `Cperp`/species representative coupling forbidden |
| `alpha_clock_redshift` | direct `Cperp` clock vertex absent; common `P_D C` drift still open |
| `gamma_minus_1` | matter/photon mismatch from local representative removed |
| `delta_G_or_fifth_force` | direct representative fifth force reduced; bulk/radial/domain channels remain |

If it fails:

```text
exp(P_D C)g must be labelled as projected-metric closure,
and WEP/clock/nonmetric residuals stay in the source-locked runner.
```

So this checkpoint does not let us dodge the local tests.

It says exactly what theorem would justify the dodge not being a dodge.

## 8. Decision Matrix

| Claim | Status | Evidence |
|---|---|---|
| matter selector follows from residual gauge invariance | conditional pass | if `eta_perp` is gauge, matter must depend only on `P_D C` |
| `Cperp` is proven gauge/exact in the parent theory | fail | `C`-sector class-valued action and exactness are not derived |
| projected matter metric is parent-derived | fail | selector depends on unproved gauge principle |
| projected metric should be demoted immediately to dead closure | not supported | topological/presymplectic route remains coherent |
| projected metric remains a theorem target | pass | next burden is `Cperp` relative exactness |

This is a fair outcome:

```text
not victory,
not dead,
but sharpened to one missing theorem.
```

## 9. What Improved

Before this checkpoint:

```text
matter seeing P_D C looked like a useful selector principle.
```

Now:

```text
matter seeing P_D C follows if Cperp is a residual gauge/exact representative.
```

That is a cleaner field-theory standard.

The metric selector is no longer just:

```text
choose the projection because local tests demand it.
```

It is:

```text
derive the quotient phase space,
then matter can only see the quotient variable.
```

## 10. What Still Fails

Still not derived:

```text
C-sector topological/class-valued action,
Cperp relative exactness,
vanishing local boundary primitive,
presymplectic null direction,
no material marker,
FLRW/local same-projector compatibility,
common-mode P_D C clock/redshift silence.
```

Therefore:

```text
projected metric not promoted,
WEP/clock pass not claimed,
local GR not claimed.
```

## 11. Gate Results

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | all cited source files exist |
| selector derivation written | pass | seven derivation steps connect residual gauge invariance to `exp(P_D C)g` |
| matter invariance implies projected metric | conditional pass | if `eta_perp` is gauge, matter dependence descends to `P_D C` |
| `Cperp` exactness parent-derived | fail | `C`-sector exactness/topological class status is not derived |
| presymplectic null direction derived | fail | requires exactness and vanishing boundary primitive |
| projected metric promoted | fail | exactness/gauge requirements remain open |
| projected metric demoted to dead closure | fail | route remains live, not dead |
| WEP/clock pass claimed | fail | direct vertices are only conditionally removed |
| local GR promoted | fail | matter selector, no-hair, EH operator, and PPN gates remain open |
| claim ceiling enforced | pass | no universal-coupling, WEP, or local-GR promotion |

## 12. Decision

Decision:

```text
residual_gauge_selector_theorem_conditional_Cperp_exactness_still_open_projected_metric_not_promoted
```

Meaning:

```text
Residual gauge invariance would select exp(P_D C)g.
But Cperp exactness / presymplectic degeneracy is still the missing parent theorem.
```

So:

```text
projected metric = live theorem target,
not derived,
not dead.
```

## 13. Next Target

Next:

```text
362 - Cperp Relative Exactness Or Projected Metric Closure Decision
```

Pass condition:

```text
Cperp is shown to be relative-exact/trivial in the C-sector,
with vanishing local primitive and null presymplectic pairing.
```

Fail condition:

```text
exp(P_D C)g is demoted to explicit projected-metric closure,
and WEP/clock residuals remain in the source-locked runner.
```

This is the fork we have to walk through next.
