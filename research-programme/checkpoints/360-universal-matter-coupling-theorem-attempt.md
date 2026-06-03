# 360 - Universal Matter Coupling Theorem Attempt

Private derivation checkpoint. This is not a public WEP, clock, redshift, PPN, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 359 identified the sharpest loaded local pressure:

```text
eta_WEP = 2.8e-15
```

That makes universal matter coupling the next fight.

The question here is:

```text
can MTS make direct WEP/clock/composition residuals exactly absent by action structure,
instead of merely small by tuning?
```

Short answer:

```text
yes, conditionally.
```

If every matter species, photon, clock, ruler, and lab standard couples only to one observed coframe/metric, and no matter action has direct non-geometric MTS arguments, then direct WEP and clock vertices are exactly absent.

But:

```text
the parent principle selecting that observed coframe is still not derived.
```

So this is a real conditional theorem, not a WEP pass.

## 2. Machine Artifact

Script:

```text
scripts/universal_matter_coupling_theorem_attempt.py
```

Run:

```text
runs/20260601-191500-universal-matter-coupling-theorem-attempt
```

Key outputs:

```text
results/source_register.csv
results/pressure_context.csv
results/theorem_axioms.csv
results/matter_action_contract.csv
results/forbidden_vertices.csv
results/variation_results.csv
results/residual_update.csv
results/selector_route_status.csv
results/next_queue.csv
results/gate_results.csv
results/decision.csv
status.json
DONE.txt
```

Status:

```text
universal_matter_coupling_conditional_theorem_sharpened_direct_WEP_clock_vertices_zero_parent_selector_open
```

Claim ceiling:

```text
conditional_universal_coupling_theorem_only_no_WEP_clock_PPN_or_local_GR_pass
```

Source paths missing:

```text
0
```

## 3. The Coupling Contract

The clean matter action is:

```text
S_matter
  = sum_A S_A[Psi_A, ehat, omega[ehat], constants_A].
```

Every matter/clock/ruler/photon sector sees:

```text
ehat^a_mu
```

and:

```text
ghat_munu = eta_ab ehat^a_mu ehat^b_nu.
```

At fixed observed coframe:

```text
delta S_matter / delta Z_I = 0
```

for every non-geometric MTS variable:

```text
Z_I in {X, J_rel, V_def, P_D, Cperp, species charges, ...}.
```

That is the exact version of:

```text
no direct memory-matter force.
```

It is not:

```text
the WEP coupling is tiny.
```

It is:

```text
the direct vertex is not in the action.
```

## 4. Projected Matter Metric

The strongest current local branch is not:

```text
ghat_munu = exp(C) g_munu.
```

That raw metric has the trace-source hazard:

```text
delta S_matter / delta C
  = 1/2 sqrt(-ghat) T_hat.
```

Instead the clean conditional branch is:

```text
ghat_munu = exp(P_D C) g_munu.
```

Then:

```text
delta S_matter / delta Cperp = 0.
```

So the local residual representative `Cperp` does not get sourced by the matter trace.

This is a proper action-level improvement.

But it needs a parent principle:

```text
why does matter see P_D C rather than C?
```

The best candidate answer is:

```text
Cperp is residual gauge / exact representative data,
and matter can depend only on the gauge-invariant quotient representative P_D C.
```

That is not yet parent-derived.

## 5. Axioms And Status

| Axiom | Meaning | Status |
|---|---|---|
| `U1` one observed coframe | one geometry for all observables | contract |
| `U2` no direct MTS matter arguments | no `Z_I` in matter action at fixed `ehat` | conditional action theorem |
| `U3` residual representative invariance | `Cperp` shifts are gauge/exact representative shifts | not parent-derived |
| `U4` projected metric selector | `ghat=exp(P_D C)g` | conditional on `U3` |
| `U5` no species-specific compensation | no species Weyl factors/charges/functions | required selection rule |
| `U6` owned selector stress | projector/domain stresses retained in Ward ledger | conditional from 356-357 |
| `U7` common-mode local silence | `P_D C` has no local clock/redshift drift | open |

This is the honest result:

```text
the direct WEP disaster can be killed exactly,
but the parent selector principle is still open.
```

## 6. Forbidden Vertices

The universal action forbids:

| Vertex | Why forbidden |
|---|---|
| `m_A(Z)` | species-dependent masses create composition dependence |
| `alpha_EM(Z)` or `f_A(Z)F^2` | clocks and spectroscopy become direct MTS probes |
| `q_A X_mu J_A^mu` | species current creates fifth force |
| `lambda_A V_def O_A` | defect/load field directly talks to matter outside geometry |
| species-specific metric `ghat_A` | different species measure different geometries |
| raw `Cperp` matter trace source | local representative becomes matter-sourced |

If any of these are allowed, WEP/clock residuals must stay in the source-locked runner.

## 7. Variation Results

| Variation | Result if axioms hold | Status |
|---|---|---|
| `delta S_matter / delta Z_I` at fixed `ehat` | `0` for every non-geometric MTS variable | conditional exact |
| `delta S_matter / delta Cperp` for `exp(P_D C)g` | `0` | conditional exact |
| `delta S_matter / delta C` for raw `exp(C)g` | `1/2 sqrt(-ghat) T_hat` | hazard if raw metric used |
| matter Ward identity | `nabla_hat_mu T_hat^mu_nu = 0` on matter shell | conditional exact |
| selector/projector/domain variation | retained in parent Ward ledger | conditional open |

This is the mathematical gain of checkpoint 360.

The WEP channel becomes:

```text
zero by absence of vertices
```

provided the observed metric/coframe selector is parent-owned.

## 8. Residual Update

| Residual | After 360 | Still open |
|---|---|---|
| `eta_WEP` | direct species-dependent vertices conditionally zero | parent derivation of selector and no hidden species-specific coupling |
| `alpha_clock_redshift` | direct clock-sector MTS vertices conditionally zero | common-mode `P_D C` drift/local redshift silence |
| `gamma_minus_1` | matter/photon geometry mismatch conditionally removed | trace-free/boundary/operator residuals remain |
| `delta_G_or_fifth_force` | direct species-charge fifth force conditionally forbidden | bulk `X`, radial, and domain fifth-force sectors remain |

So the outcome is not:

```text
local tests passed.
```

It is:

```text
the most dangerous direct matter-coupling channels have an exact conditional kill switch.
```

That is very useful.

## 9. Selector Route Status

| Route | Verdict | Risk |
|---|---|---|
| minimal metric postulate | closure if standalone | not derived from MTS |
| residual gauge invariance | best conditional route | needs parent gauge/cohomology theorem |
| relative cohomology class | supporting route | must show domain projection is constraint-safe |
| boundary-clock normalization | plausible side route | clock/redshift drift remains |
| raw `exp(C)g` metric | rejected as lead | sources `Cperp` |

The next real theorem target is therefore:

```text
Cperp is residual gauge / exact representative data.
```

If that is derived, then:

```text
matter seeing P_D C is not a local-test patch.
It is quotient/gauge invariance.
```

## 10. What Improved

Before this checkpoint:

```text
universal matter coupling was the top empirical pressure debt.
```

Now it has a clean conditional theorem:

```text
one observed coframe + no direct MTS matter arguments
  -> direct WEP/clock vertices vanish.
```

And the projected matter metric has a clean conditional selector route:

```text
residual representative invariance
  -> matter depends only on P_D C
  -> delta S_matter / delta Cperp = 0.
```

This is a meaningful advance toward local GR.

It turns "WEP must be tiny" into:

```text
WEP vertex must be absent by action structure.
```

## 11. What Still Fails

No WEP/clock/PPN/local-GR pass follows.

Still open:

```text
parent derivation of one observed coframe,
parent residual gauge/cohomology principle for Cperp,
proof of no species-specific compensation,
owned selector/projector/domain stress closure,
common-mode P_D C clock/redshift silence,
EH/no-hair/operator/source-normalization gates.
```

The result is exactly conditional:

```text
if the parent action selects the universal projected matter metric,
then direct WEP/clock vertices are zero.
```

But:

```text
the parent action has not yet selected it.
```

## 12. Gate Results

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | all cited source files exist |
| universal action contract written | pass | single observed coframe and forbidden vertices listed |
| direct WEP/clock vertices zero | conditional pass | no direct MTS arguments at fixed `ehat` gives zero variation |
| projected metric `Cperp` source removed | conditional pass | `ghat=exp(P_D C)g` gives `delta S_matter/delta Cperp=0` |
| parent selector principle derived | fail | residual gauge/cohomology principle remains open |
| common-mode clock silence derived | fail | local drift/gradient of `P_D C` not derived |
| universal coupling promoted | fail | core axioms remain contract/open/not parent-derived |
| WEP or clock pass claimed | fail | conditional zero is not observational pass |
| local GR promoted | fail | EH/no-hair/operator/source-normalization gates remain open |
| claim ceiling enforced | pass | no WEP/clock/PPN/local-GR claim |

## 13. Decision

Decision:

```text
universal_matter_coupling_conditional_theorem_sharpened_direct_WEP_clock_vertices_zero_parent_selector_open
```

Meaning:

```text
The local branch now has an exact conditional way to kill direct WEP/clock vertices:
make all matter and standards couple only to one observed coframe,
with no direct non-geometric MTS arguments.
```

But:

```text
the parent selector principle for that coframe is still missing.
```

## 14. Next Target

Next:

```text
361 - Residual Gauge Principle For Projected Matter Metric
```

Pass condition:

```text
derive Cperp as residual gauge / exact representative data,
so P_D C is the unique matter-visible scalar in the coherent limit.
```

Fail condition:

```text
projected matter metric remains an explicit closure,
and WEP/clock residuals stay in the source-locked runner.
```

This is the cleanest route because it tries to make the local-test-safe matter metric a theorem, not a patch.
