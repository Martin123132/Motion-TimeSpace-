# 385 - Observed-Coframe Selector Pullback Cancellation Theorem

Private parent-action/WEP/local-GR checkpoint. This is not a public WEP, PPN, clock, Einstein-Hilbert, fifth-force, source-normalization, boundary, bulk-field, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 384 found the first unowned parent-variation term:

```text
Pi_I^matter =
  (delta S_matter / delta ehat^a_mu)
  (partial ehat^a_mu / partial Z_I).
```

The question now is:

```text
can Pi_I^matter be cancelled or forbidden?
```

Answer:

```text
only under strict conditions.
```

The legal fates are:

```text
identity coframe,
pure gauge pullback,
constant universal normalization,
species symmetry/common F plus common-mode silence,
Ward-owned selector counterstress,
or explicit closure/residual retention.
```

None of these is parent-derived in the current branch.

So the result is:

```text
cancellation routes classified,
Pi_I^matter not cancelled,
eta_WEP remains active,
no local-GR promotion.
```

That is not a loss.

It is a sharper map of where the punch has to land.

## 2. Machine Artifact

Script:

```text
scripts/observed_coframe_selector_pullback_cancellation_theorem.py
```

Run:

```text
runs/20260602-013500-observed-coframe-selector-pullback-cancellation-theorem
```

Outputs:

```text
results/source_register.csv
results/cancellation_conditions.csv
results/theorem_attempts.csv
results/no_go_results.csv
results/pullback_classification.csv
results/runner_update.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

Status:

```text
observed_coframe_pullback_cancellation_routes_classified_identity_or_gauge_or_constant_or_counterstress_required_not_parent_derived
```

Claim ceiling:

```text
coframe_pullback_cancellation_theorem_attempt_only_no_WEP_PPN_EH_source_boundary_bulk_or_local_GR_pass
```

Source paths missing:

```text
0
```

## 3. Cancellation Conditions

The pullback can vanish only if one of these holds:

| Condition | Mathematical statement | Current status |
|---|---|---|
| identity coframe | `partial ehat / partial Z_I = 0` | clean but not parent-selected |
| pure gauge pullback | `delta ehat = L_xi ehat + Lorentz rotation` | conditional for representative directions only |
| constant universal normalization | only constant universal scale changes | not parent-derived |
| species symmetry/common `F` | `ehat_A=ehat`, `F_A(C_D)=F(C_D)` | future theorem target |
| Ward-owned counterstress | `E_selector,I + Pi_I^matter = 0` | honest modified-gravity route, open |
| closure retention | labelled closure or retained coefficients | allowed only if explicit |

So the theorem is not:

```text
Pi_I^matter = 0.
```

The theorem is:

```text
Pi_I^matter = 0
```

only under one of the listed structural conditions.

The current parent branch has not supplied one.

## 4. Theorem Attempts

### Identity coframe

If:

```text
ehat = e
```

and:

```text
partial ehat / partial Z_I = 0
```

for all nonmetric MTS variables, then:

```text
Pi_I^matter = 0.
```

This is mathematically sufficient.

Cost:

```text
MTS local effects must live in metric/operator/source sectors,
not in a matter-visible class metric.
```

Current status:

```text
clean route,
not parent-selected.
```

### Species symmetry

If a parent internal symmetry forces:

```text
ehat_A = ehat,
F_A(C_D) = F(C_D),
m_A(C_D) = constant_A,
alpha_A(C_D) = constant_A,
q_A = 0 or common universal,
```

then the species-difference part of the pullback vanishes:

```text
Delta F_AB = 0.
```

This would kill the direct `eta_WEP` class split.

But:

```text
no such parent species symmetry has been supplied.
```

Also:

```text
common-mode F(C_D)
```

still needs local silence or source normalization.

### Quotient gauge selector

If:

```text
Cperp
```

and representative data are exact gauge directions, then pullback along those directions is pure gauge.

This helps.

But it does not prove:

```text
F_A(C_D)=F_B(C_D)
```

because `C_D` is a physical class observable, not merely representative data.

So:

```text
representative invariance kills representative leakage,
not species-specific class response.
```

### Constant common mode

If:

```text
F(C_D) = constant
```

locally, universally, time-independently, and source-normalized, then the pullback can become only:

```text
unit / measured-GM normalization.
```

But this requires:

```text
local phi_C zero theorem,
source normalization,
no drift,
no range dependence,
no species dependence.
```

Those gates are still open.

### Ward-owned counterstress

If:

```text
E_selector,I + Pi_I^matter = 0
```

with selector stress included in the total Ward identity, then the pullback is owned.

This is honest.

But it is not automatically local GR.

It becomes a modified-gravity/residual route unless the counterstress is:

```text
no-hair,
boundary-only harmless,
or source-budgeted below local rows.
```

## 5. No-Go Results

The checkpoint proves several anti-shortcuts:

| No-go | Consequence |
|---|---|
| fixed-`ehat` vertex zero is not total zero | WEP fixed-coframe theorem is necessary but insufficient |
| representative invariance does not force species universality | `eta_WEP` remains active |
| universal common mode is not automatically safe | clock/gamma/fifth-force/`Gdot` rows remain guarded |
| exterior `T=0` does not set source charge zero | source matching and body charge still matter |
| counterstress is not local GR by itself | retained stress must face runner/no-hair gates |

The biggest one:

```text
delta S_matter / delta Z_I | ehat = 0
```

does not imply:

```text
dS_matter/dZ_I = 0.
```

Unless the coframe selector pullback is killed or owned.

## 6. Pullback Classification

| Pullback piece | Classification | Fallback row |
|---|---|---|
| representative `Cperp` | conditional gauge zero | clock/gamma if leakage survives |
| physical common `C_D` | conditional common mode | clock, gamma, fifth-force, `Gdot` |
| species `C_D` response | active WEP residual | `eta_WEP`, composition force |
| projector/domain selector | preferred-frame/aniso residual | `alpha1`, `alpha2`, `xi`, gamma |
| boundary selector | boundary residual | gamma, beta, alpha rows, WEP boundary |
| bulk `X` selector/charge | bulk/fifth-force residual | fifth-force, gamma, beta, WEP if charged |

This tells us which pieces can be handled by gauge language and which cannot.

The crucial split:

```text
Cperp can plausibly be gauge.
C_D species response cannot be made gauge by representative invariance.
```

That is why WEP stays active.

## 7. Runner Update

| Runner row | After 385 | State |
|---|---|---|
| `eta_WEP` | active unless identity coframe or species symmetry is parent-derived | budget-only |
| `alpha_clock_redshift` | common-mode pullback needs silence/normalization | budget-only |
| `gamma`, `beta` | selector/boundary/bulk pullbacks remain coefficient rows | budget-only |
| preferred-frame / `xi` | projector/domain/boundary anisotropic pullbacks remain | budget/contingent |
| fifth-force / `delta_G` | common-mode, boundary, bulk-X pullbacks need range/coupling | unscored parameterized |

So the runner v2 state is unchanged in a useful way:

```text
the reason for the active rows is now sharper.
```

## 8. What Improved

Before 385, we knew:

```text
Pi_I^matter is the first obstruction.
```

Now we know its legal fates:

```text
identity,
gauge,
constant universal,
species symmetry,
counterstress,
or explicit residual.
```

That means the next work cannot drift into vague statements like:

```text
matter couples universally.
```

It has to answer:

```text
does universal mean identity coframe,
common class metric,
or Ward-owned selector stress?
```

Those are different theories.

## 9. What Still Fails

No cancellation is parent-derived.

Still missing:

```text
identity coframe theorem,
parent species symmetry,
common-F selector,
constant local common-mode theorem,
source normalization,
selector counterstress coefficients,
and no-hair for any retained counterstress.
```

Therefore:

```text
Pi_I^matter stays active.
```

And:

```text
eta_WEP remains the hardest always-relevant local row.
```

## 10. Gate Results

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | all cited source paths exist |
| cancellation conditions classified | pass | six legal fates for `Pi_I^matter` classified |
| theorem attempts written | pass | five cancellation routes tested at theorem-contract level |
| no-go results written | pass | five shortcut failures recorded |
| pullback classification written | pass | six pullback pieces classified |
| `Pi_I^matter` cancelled or owned | fail | no identity coframe/species symmetry/constant theorem/counterstress derived |
| WEP or local GR promoted | fail | `eta_WEP` remains active and local-GR stack remains open |
| runner update preserves residuals | pass | pullback-driven residuals retained |
| claim ceiling enforced | pass | no WEP/PPN/EH/source/boundary/bulk/local-GR pass |

## 11. Decision

Decision:

```text
observed_coframe_pullback_cancellation_routes_classified_identity_or_gauge_or_constant_or_counterstress_required_not_parent_derived
```

Meaning:

```text
the pullback obstruction is now mathematically classified,
but not solved.
```

The local route has a clean next fork:

```text
strict identity coframe locally
```

or:

```text
class-metric pullback retained as closure/counterstress.
```

No promotion:

```text
WEP not passed,
clock not passed,
PPN not passed,
fifth-force not scored,
EH not derived,
local GR not derived.
```

## 12. Next Target

Next:

```text
386 - Local-Bound Runner V2 Smoke Matrix
```

Aim:

```text
run a small coefficient-sensitivity smoke for the retained pullback residuals
with GR/null baseline rows.
```

Why next:

```text
385 did not kill Pi_I^matter.
```

So the honest next empirical move is:

```text
test how expensive the retained pullback rows are,
without claiming a pass.
```

The next theory fork after that should be:

```text
identity coframe or class-metric pullback.
```
