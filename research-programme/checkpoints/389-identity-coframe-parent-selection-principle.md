# 389 - Identity Coframe Parent Selection Principle

Private local-GR/WEP selector checkpoint. This is not a public WEP, PPN, preferred-frame, fifth-force, Einstein-Hilbert, source-normalization, boundary, bulk-field, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 388 found the best species result so far:

```text
common F follows conditionally from species-blind geometry.
```

But common `F` does not remove the common-mode pullback:

```text
Pi_C^matter ~ T_hat partial_C F.
```

So this checkpoint tries the stronger route:

```text
can the parent theory force ehat=e locally?
```

Answer:

```text
mathematically yes, if identity coframe is a parent principle;
currently no, it is not derived from existing MTS variation.
```

The result:

```text
identity coframe is the clean local-GR theorem target,
or a labelled local WEP closure for testing the remaining EH/source/boundary/bulk stack.
```

It is not yet:

```text
derived local GR.
```

## 2. Machine Artifact

Script:

```text
scripts/identity_coframe_parent_selection_principle.py
```

Run:

```text
runs/20260602-021500-identity-coframe-parent-selection-principle
```

Outputs:

```text
results/source_register.csv
results/selection_attempts.csv
results/identity_theorem_contract.csv
results/proof_sketch.csv
results/no_go_results.csv
results/runner_transitions.csv
results/branch_policy.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

Status:

```text
identity_coframe_selection_principle_conditional_clean_local_GR_route_not_parent_derived_closure_label_required
```

Claim ceiling:

```text
identity_coframe_selection_attempt_only_no_WEP_PPN_fifth_force_EH_source_boundary_bulk_or_local_GR_pass
```

Source paths missing:

```text
0
```

## 3. Main Result

The identity branch says:

```text
S_matter = sum_A S_A[Psi_A, e, omega[e], theta_A].
```

Here:

```text
e
```

is the same coframe varied in the local gravitational metric core.

The species data:

```text
theta_A
```

may contain ordinary internal constants:

```text
mass,
charge,
spin,
representation,
Yukawa/internal parameters.
```

But it cannot contain:

```text
C_D,
P_D,
X,
boundary data,
domain data,
source-normalization fields,
or species class spurions.
```

Then for nonmetric MTS selector variables:

```text
Z_I in {C_D, Cperp, P_D, X, boundary, domain, source-normalization, ...}
```

we get:

```text
partial e / partial Z_I = 0,
partial theta_A / partial Z_I = 0.
```

Therefore:

```text
dS_matter/dZ_I = 0
```

including:

```text
Pi_I^matter =
  (delta S_matter / delta e)
  (partial e / partial Z_I)
  = 0.
```

This is the cleanest WEP/coframe-pullback kill switch.

But:

```text
the parent action has not yet derived why matter must use e rather than ehat(C_D).
```

## 4. Selection Attempts

| Attempt | Verdict | Reason |
|---|---|---|
| diffeomorphism/local Lorentz | insufficient | universal `exp(F(C_D))e` is still covariant |
| weak equivalence principle | closure/empirical principle | selects one geometry, not identity with `e` |
| strong equivalence/minimal metric coupling | conditional theorem | works if parent adopts same metric core for matter |
| no local class spurion | conditional theorem | forbids `F(C_D)`, `F_A(C_D)`, selector pullbacks |
| constant universal normalization | conditional support | safe only after source/clock normalization |
| field redefinition `e'=ehat` | not a derivation | moves debts into EH/operator/source frame |
| representative gauge invariance | partial only | kills `Cperp`, not physical `C_D` common mode |

The key failure:

```text
covariance allows a universal class metric.
```

So:

```text
diffeomorphism invariance + local Lorentz invariance
```

does not force:

```text
ehat=e.
```

Something stronger is required.

## 5. Identity Theorem Contract

A real parent theorem must supply:

| Contract item | Required statement | Current status |
|---|---|---|
| metric core is observed geometry | same `e` in metric core and matter/clock/ruler sector | conditional premise |
| no matter geometry spurions | no class/projector/bulk/boundary/source/domain variable in matter geometry | needed selection rule |
| constants class-independent | `partial_Z theta_A=0` for nonmetric selector variables | needed for WEP/clock rows |
| normalization fixed | `ehat=A0 e` only if `A0` is constant, universal, source-normalized | open |
| EH operator in same frame | local exterior is EH-only in the same metric matter sees | open |

If all five hold, the matter pullback problem is gone.

But currently:

```text
only the conditional theorem is written.
```

The parent selection principle is still absent.

## 6. Proof Sketch

The proof is short:

1. Assume:

```text
S_matter = sum_A S_A[Psi_A, e, omega[e], theta_A].
```

2. Require:

```text
partial e / partial Z_I = 0,
partial theta_A / partial Z_I = 0.
```

3. Then:

```text
dS_matter/dZ_I = 0.
```

4. Therefore:

```text
Pi_I^matter = 0.
```

5. If instead:

```text
ehat = exp(F(C_D)) e
```

with:

```text
F'(C_D) != 0,
```

the proof fails and the common-mode pullback returns.

So the condition is exact:

```text
identity coframe or constant universal normalization,
not merely universal matter coupling.
```

## 7. No-Go Results

| No-go | Consequence |
|---|---|
| WEP universality does not select identity | one observed `ehat` can still differ from `e` |
| covariance allows class metric | `S_matter[psi, exp(F(C_D))e]` remains legal |
| field redefinition is not free | debts move into gravitational/MTS operator frame |
| constant scale is not automatic | source-normalization and clock drift gates remain |
| identity closure is not derivation | `ehat=e` can be used only as labelled closure unless parent-derived |

The field-redefinition warning matters.

One might say:

```text
just call ehat the metric.
```

But then the question becomes:

```text
is the EH/operator/source/boundary/bulk stack EH-only in that renamed metric?
```

If not, the local residuals simply moved location.

They did not disappear.

## 8. Runner Transitions

If identity coframe is parent-derived:

| Runner row | Transition | Remaining debt |
|---|---|---|
| `eta_WEP` | matter coframe/species geometry split becomes derived-zero | parent selector proof |
| `alpha_clock_redshift` | direct class-metric clock pullback removed | constants/no-drift/source-normalization |
| `gamma/beta` | matter pullback contribution removed | EH-only exterior, boundary/bulk no-hair |
| `alpha1/alpha2/xi` | domain/projector coframe slip removed | covariant domain/projector, boundary no-hair |
| `Gdot/fifth_force` | class-metric common-mode force removed | source normalization and bulk/boundary force laws |

This is why identity coframe is worth trying.

It does not solve every local-GR debt.

But it removes the first matter-pullback obstruction and lets the next debts be attacked cleanly.

## 9. Branch Policy

The branch policy is now:

| Branch | Allowed claim | Forbidden claim |
|---|---|---|
| identity coframe as parent principle | conditional WEP/coframe-pullback zero theorem | derived local GR before EH/source/boundary/bulk stack closes |
| identity coframe as closure | test remaining EH/source/boundary/bulk debts with WEP pullback closed by axiom | MTS has derived equivalence principle |
| class metric retained | retain pullback with no-hair/source-budget contract | local GR without counterstress/no-hair proof |

So we can still make progress in two honest ways:

```text
use ehat=e as a labelled local closure to test the rest of the GR stack,
```

or:

```text
retain class metric and demand a counterstress/no-hair/source-budget contract.
```

Both are legitimate.

Only one is a derived local-GR claim, and that one is not available yet.

## 10. What Improved

Before this checkpoint, identity coframe was a good phrase.

Now it is an exact theorem contract:

```text
matter uses metric-core e,
no nonmetric class spurions enter geometry/constants,
constant scale is source-normalized,
EH operator lives in same frame.
```

That tells us exactly what a parent action has to do.

It also tells us what not to do:

```text
do not claim WEP/local-GR from universal ehat alone.
```

Universal `ehat` is not enough if:

```text
ehat=exp(F(C_D))e
```

with active `F'`.

## 11. What Still Fails

Still missing:

```text
parent derivation of ehat=e,
no local class-spurion principle,
constant/source-normalized scale theorem,
class metric counterstress no-hair contract,
EH-only exterior operator in the matter frame,
source normalization,
boundary no-hair,
bulk-X no-hair or force law.
```

So:

```text
WEP is not promoted,
PPN is not promoted,
local GR is not promoted.
```

The useful status is:

```text
identity coframe is now the clean closure/theorem target.
```

## 12. Gate Results

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | all cited source paths exist |
| selection attempts written | pass | seven identity-selection routes audited |
| identity coframe mathematically sufficient | conditional pass | `Pi_I^matter=0` if `ehat=e` and nonmetric `Z_I` do not enter matter constants |
| identity parent principle derived | fail | no MTS variation currently forbids universal class metric or local class spurions |
| field redefinition rejected as proof | pass | renaming `ehat` shifts debts into EH/operator/source stack |
| identity closure label required | pass | `ehat=e` can be used only as explicit WEP closure unless parent-derived |
| WEP/PPN/local GR promoted | fail | EH/source/boundary/bulk debts remain |
| claim ceiling enforced | pass | no WEP/PPN/fifth-force/EH/source/boundary/bulk/local-GR pass |

## 13. Decision

Decision:

```text
identity_coframe_selection_principle_conditional_clean_local_GR_route_not_parent_derived_closure_label_required
```

Meaning:

```text
identity coframe is mathematically sufficient
but not parent-derived.
```

It can be used as:

```text
explicit local WEP closure
```

for testing the remaining GR stack.

It cannot be advertised as:

```text
MTS has derived local GR.
```

The recommended branch is:

```text
use identity coframe as labelled closure when testing the EH stack.
```

The fallback branch is:

```text
class-metric counterstress/no-hair contract.
```

## 14. Next Target

Next:

```text
390 - Class-Metric Counterstress No-Hair Contract
```

Aim:

```text
write the exact no-hair/source-budget contract for the retained class-metric pullback branch.
```

Pass condition:

```text
class metric pullback is no-hair,
source-budgeted,
or demoted as modified gravity.
```

Why this next:

```text
identity coframe is clean but not parent-derived.
```

So the honest alternative branch must be made equally explicit:

```text
if class metric survives,
what exactly must its counterstress satisfy?
```
