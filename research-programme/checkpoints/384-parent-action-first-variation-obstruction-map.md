# 384 - Parent Action First Variation Obstruction Map

Private parent-action/local-GR checkpoint. This is not a public WEP, PPN, Einstein-Hilbert, fifth-force, boundary, bulk-field, source-normalization, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 382 wrote the minimal parent local action contract.

Checkpoint 383 made the residual runner honest.

This checkpoint starts doing the thing the contract demands:

```text
vary the parent action.
```

Not fully.

Not beautifully.

But enough to ask:

```text
where does the first unavoidable unowned term appear?
```

Answer:

```text
the observed-coframe selector pullback.
```

The earlier conditional WEP theorem said:

```text
delta S_matter / delta Z_I | ehat = 0.
```

That is true if matter has no direct non-geometric MTS arguments at fixed observed coframe.

But the parent action must also vary the fields that define:

```text
ehat.
```

If:

```text
ehat = ehat(g, C, P_D, X, boundary, domain, ...)
```

then the total variation contains:

```text
(delta S_matter / delta ehat^a_mu)
  (partial ehat^a_mu / partial Z_I).
```

This is not killed by:

```text
delta S_matter / delta Z_I | ehat = 0.
```

That is the first obstruction.

It is the chain rule walking into the ring with steel-toe boots.

## 2. Machine Artifact

Script:

```text
scripts/parent_action_first_variation_obstruction_map.py
```

Run:

```text
runs/20260602-012500-parent-action-first-variation-obstruction-map
```

Outputs:

```text
results/source_register.csv
results/variation_chain.csv
results/obstruction_candidates.csv
results/coframe_pullback_terms.csv
results/ownership_routes.csv
results/residual_impact.csv
results/contract_update.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

Status:

```text
parent_action_first_variation_obstruction_map_written_first_unowned_term_is_observed_coframe_selector_pullback_no_local_GR_promotion
```

Claim ceiling:

```text
first_variation_obstruction_map_only_no_WEP_PPN_EH_boundary_bulk_source_or_local_GR_pass
```

Source paths missing:

```text
0
```

## 3. Variation Chain

The first variation starts as:

| Step | Variation | Result | Status |
|---:|---|---|---|
| 1 | `delta_psi S_parent` | matter equations | owned on matter shell |
| 2 | `delta_e/g S_parent` | metric equation with matter plus MTS stresses | needs EH/source gates later |
| 3 | `delta_Z S_matter` at fixed `ehat` | direct MTS matter vertex zero | conditional pass |
| 4 | total `delta_Z S_matter` when `ehat=ehat(Z)` | coframe selector pullback | first unowned term |
| 5 | `delta_Z S_selector` plus pullback | selector equation sourced by matter stress | needs owner/counterstress |
| 6 | boundary/domain/X/projector variations | secondary source terms | serious but later |

The first obstruction is step 4.

Not because WEP is impossible.

Because the previous WEP kill switch was a fixed-`ehat` theorem.

The parent variation cannot keep `ehat` fixed if `ehat` is selected by MTS fields.

## 4. The Obstruction

Let:

```text
Z_I in {C_D, P_D, Cperp, X, boundary data, domain data, source-normalization data, ...}.
```

The fixed-coframe theorem gives:

```text
delta S_matter / delta Z_I | ehat = 0.
```

But the total variation is:

```text
dS_matter/dZ_I
  = delta S_matter / delta Z_I | ehat
    + (delta S_matter / delta ehat^a_mu)
      (partial ehat^a_mu / partial Z_I).
```

Therefore:

```text
dS_matter/dZ_I
  = (delta S_matter / delta ehat^a_mu)
    (partial ehat^a_mu / partial Z_I)
```

unless:

```text
partial ehat / partial Z_I = 0,
pure gauge,
constant universal and absorbed,
or cancelled by a Ward-owned selector equation.
```

This term is:

```text
Pi_I^matter.
```

It is currently not parent-owned.

## 5. Why This Comes First

The EH operator problem is deep.

Boundary no-hair is deep.

Bulk `X` is deep.

But the matter pullback appears before all of those in the variation chain.

If the parent action says:

```text
matter sees ehat
```

and then says:

```text
ehat is selected from MTS/class/projector/domain data,
```

then the selector fields feel matter stress through:

```text
Pi_I^matter.
```

That is exactly the thing WEP/local-GR cannot ignore.

This is why:

```text
eta_WEP
```

stays the hardest always-relevant local row.

## 6. Pullback Terms

| Term | Schematic form | Dangerous row |
|---|---|---|
| universal common-mode pullback | `T_hat partial[exp(F(C_D))g]/partial C_D` | clock, gamma, fifth-force, `Gdot` |
| species class pullback | `T_A partial[exp(F_A(C_D))g]/partial C_D` | `eta_WEP`, composition force |
| projector selector pullback | `T_hat partial[P_D C]/partial P_D` | gamma, `xi`, alpha rows |
| boundary coframe pullback | `T_hat partial ehat/partial B_partialD` | gamma, beta, alpha rows, WEP boundary |
| bulk-X matter pullback | `T_hat partial ehat/partial X` or `q_test X.J` | fifth-force, WEP if charged |

This shows the trap:

```text
even a universal matter action can source selector equations
if the observed coframe is a nontrivial function of selector fields.
```

Universal is necessary.

It is not sufficient unless the pullback is owned.

## 7. Ownership Routes

The obstruction has five legal fates:

| Route | Would do | Status |
|---|---|---|
| strict identity coframe | matter stress goes only into ordinary metric equation | clean but closure unless parent-derived |
| parent species symmetry | forces `ehat_A=ehat` and `F_A=F` | future theorem target |
| quotient gauge selector | kills raw `Cperp` trace source | conditional support only |
| Ward-owned selector counterstress | cancels pullback honestly | open modified-gravity route |
| closure axiom | labels one coframe/common `F` as assumed | allowed only if labelled |

The best exact route is:

```text
a parent species/coframe symmetry
```

or:

```text
an identity-coframe theorem.
```

The most honest fallback route is:

```text
selector counterstress retained and source-budgeted.
```

The forbidden route is:

```text
drop Pi_I^matter because local GR needs it gone.
```

No conservation cosplay.

We already banned that.

## 8. Residual Impact

If the pullback is not owned:

| Residual | Source lock | Pullback source |
|---|---:|---|
| `eta_WEP` | `2.8e-15` | species class pullback or species test charge |
| `alpha_clock_redshift` | `3.1e-5` | clock metric mismatch/common-mode drift |
| `gamma_minus_1` | `2.3e-5` | nonmetric light, scalar/boundary/bulk stress |
| `beta_minus_1` | `7.8e-5` | radial/nonlinear/source terms |
| `alpha1/alpha2/xi` | source-locked | domain/projector/boundary anisotropic pullback |
| `Gdot/G` | contingent | time-varying source/common mode |
| fifth-force | `alpha(lambda)` | radial common mode, bulk `X`, boundary radial hair |

So this obstruction is not merely philosophical.

It lands straight inside the runner.

## 9. Contract Update

Checkpoint 382 said:

```text
delta S_matter / delta Z_I | ehat = 0.
```

Checkpoint 384 strengthens that to:

```text
Pi_I^matter =
  (delta S_matter / delta ehat^a_mu)
  (partial ehat^a_mu / partial Z_I)
```

must be:

```text
zero,
pure gauge,
constant universal and absorbed,
or Ward-owned and source-budgeted.
```

That is the new exact contract.

This is progress because it blocks a seductive half-proof:

```text
matter has no direct MTS arguments,
therefore WEP is solved.
```

No.

Correct version:

```text
matter has no direct MTS arguments at fixed ehat,
but the parent action must also own the selector pullback of ehat.
```

## 10. Gate Results

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | all cited source paths exist |
| first variation chain written | pass | six variation steps mapped |
| first obstruction identified | pass | observed-coframe selector pullback is first unowned term |
| coframe pullback terms mapped | pass | five pullback term classes mapped |
| ownership routes written | pass | five possible ownership routes classified |
| pullback obstruction solved | fail | no parent identity coframe/species symmetry/counterstress derived |
| WEP or PPN pass claimed | fail | `eta_WEP` and related rows remain active |
| local GR promoted | fail | first variation obstruction mapped, not solved |
| claim ceiling enforced | pass | no WEP/PPN/EH/boundary/bulk/source/local-GR pass |

## 11. Decision

Decision:

```text
parent_action_first_variation_obstruction_map_written_first_unowned_term_is_observed_coframe_selector_pullback_no_local_GR_promotion
```

Meaning:

```text
the first variation exposes the observed-coframe selector pullback as the first unowned term.
```

The branch can still survive.

But it must now prove or retain:

```text
Pi_I^matter =
  (delta S_matter / delta ehat)
  (partial ehat / partial Z_I).
```

No promotion:

```text
WEP not passed,
PPN not passed,
EH not derived,
boundary not closed,
bulk X not closed,
source normalization not derived,
local GR not derived.
```

## 12. Next Target

Next:

```text
385 - Observed-Coframe Selector Pullback Cancellation Theorem
```

Aim:

```text
try to cancel or forbid Pi_I^matter.
```

Allowed routes:

```text
identity coframe,
parent species symmetry,
quotient gauge selector,
Ward-owned selector counterstress,
or explicit closure retention.
```

Pass condition:

```text
Pi_I^matter is derived zero,
pure gauge,
constant universal,
or retained with coefficients.
```

Why this next:

```text
this is now the first obstruction in the parent-action variation.
```

If it cannot be killed or owned, derived local GR cannot start.
