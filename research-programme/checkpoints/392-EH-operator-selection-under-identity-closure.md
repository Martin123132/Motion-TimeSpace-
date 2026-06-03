# 392 - EH Operator Selection Under Identity Closure

Private local-GR/EH checkpoint. This is not a public Einstein-Hilbert, PPN, source-normalization, fifth-force, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 391 left us in the cleanest local branch so far:

```text
identity coframe closure:
  ehat = e
  S_matter = sum_A S_A[Psi_A, e, omega[e], theta_A]
```

That closes the direct matter/coframe pullback obstruction by label. The question here is narrower and harder:

```text
Does identity closure force the exterior gravitational operator to be Einstein-Hilbert?
```

Short answer:

```text
No, not by itself.
```

Better answer:

```text
identity closure
+ metric-only local 4D second-order exterior
+ source-normalized compact exterior
+ Ward closure
+ boundary/bulk/vector/nonlocal no-hair
  => EH + Lambda + harmless boundary/topological terms.
```

That is a real conditional route. But the extra premises are not yet parent-derived, so EH is not promoted.

## 2. Run Manifest

Script:

```text
scripts/EH_operator_selection_under_identity_closure.py
```

Expected run directory:

```text
runs/<timestamp>-EH-operator-selection-under-identity-closure
```

Expected result files:

```text
results/source_register.csv
results/operator_selection_premises.csv
results/selection_attempts.csv
results/EH_sufficiency_ladder.csv
results/nonEH_operator_ledger_under_identity.csv
results/runner_transition_under_identity.csv
results/no_go_results.csv
results/gate_policy.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

## 3. EH Selection Question

Write the exterior equations schematically as

```text
E_total^{mu nu}
  =
  E_EH^{mu nu}
  + sum_i c_i H_i^{mu nu}
  + E_boundary^{mu nu}
  + E_bulk/vector/nonlocal^{mu nu}
  =
  kappa T^{mu nu}.
```

Identity closure controls the matter side:

```text
T^{mu nu} = T^{mu nu}[Psi_A, e]
```

It does not automatically set

```text
c_i = 0.
```

So the real EH theorem has to be an operator-selection theorem, not a WEP theorem.

## 4. Conditional EH Theorem Shape

The viable theorem shape is:

```text
If:
  1. matter sees one coframe e;
  2. exterior ordinary matter support is compact;
  3. all Ward force channels are closed or retained;
  4. all MTS bulk/boundary/vector/domain/projector hair is zero, pure gauge, constant monopole, or source-budgeted;
  5. the surviving exterior is metric-only;
  6. the surviving local 4D metric equations are second order;
  7. boundary/topological terms are harmless or Ward-owned;
  8. kappa, G_eff, M_eff, and measured GM are source-normalized;
then:
  E_ext^{mu nu} = a G^{mu nu} + b g^{mu nu}
and the action is EH + Lambda + harmless boundary/topological terms.
```

This is exactly the right GR-facing ladder. The problem is not the theorem shape. The problem is that MTS still has to derive the premises from the parent action.

## 5. Why Identity Closure Is Not Enough

Identity closure removes one dangerous route:

```text
delta S_matter / delta Z_I | ehat=e = 0
```

But it does not remove conserved non-EH exterior tensors. Diffeomorphism covariance and Bianchi-style conservation are necessary; they are not uniqueness.

Allowed if not excluded:

- `R^2` / `f(R)` scalar curvature corrections;
- `R_{mu nu}R^{mu nu}` or Weyl/shear corrections;
- scalar-tensor or class-metric gravity-sector residues;
- vector/domain/projector preferred-frame operators;
- torsion/nonmetricity if the parent connection is not forced to Levi-Civita;
- bulk-X force-law terms;
- nonlocal/memory kernels;
- source-normalization operators.

That means the current branch is not dead, but it is not a GR reduction yet. It is a disciplined modified-gravity ledger unless the EH premises are derived.

## 6. Selection Attempt Results

| Attempt | Result | Reason |
|---|---:|---|
| identity closure only | fail | matter sees one coframe, but pure gravity operators remain open |
| Bianchi/Ward only | fail | conserved non-EH tensors exist |
| metric-only without second-order | fail | higher-curvature and nonlocal curvature terms survive |
| low-energy EFT truncation | conditional budget | small is testable, but not exact local-GR derivation |
| local 4D metric second-order | conditional pass | selects EH + Lambda if the premise is parent-derived |
| no-hair/source/boundary stack | open | source, boundary, bulk, preferred-frame, and fifth-force debts remain |

## 7. Non-EH Operator Ledger Under Identity

| Family | Observable risk | Policy |
|---|---|---|
| EH + Lambda | Newtonian/PPN baseline | target only if full stack holds |
| boundary/topological | `gamma`, `beta`, `alpha3`, `xi` | retain unless class-only/topological/Ward-owned |
| `R^2` / `f(R)` | `gamma`, `beta`, fifth force | derive zero or map mass/range/coupling |
| Ricci/Weyl squared | `gamma`, `xi`, slip/wave sector | retain coefficient ledger |
| scalar-tensor/class metric | `gamma`, `beta`, clock, fifth force, `Gdot/G` | separate modified-gravity/counterstress branch |
| vector/preferred-frame | `alpha1`, `alpha2`, `alpha3`, `xi` | retain until vector/domain no-hair |
| torsion/nonmetricity | WEP/clock/spin/light-cone risks | forbid by compatibility theorem or retain |
| bulk-X | fifth force, `gamma`, `beta`, `delta_G` | derive theorem-zero or `alpha_X(lambda_X)` |
| nonlocal/memory | `Gdot/G`, `delta_G`, fifth force | derive local kernel silence/screening |
| source normalization | `delta_G`, `Gdot/G`, `beta`, fifth force | next target |

## 8. Runner Transition

The identity branch changes the local runner policy like this:

| Row | New policy |
|---|---|
| `eta_WEP` | closure-zero only inside identity branch |
| `alpha_clock` | direct matter spurion closed, source/nonlocal residues still tracked |
| `gamma-1` | retained |
| `beta-1` | retained |
| `alpha_i`, `xi` | retained |
| fifth-force Yukawa row | retained and still range/coupling parameterized |
| `Gdot/G` | retained through source-normalization/memory risk |

So this is not a knockout. It is the Mayweather version: remove one opening, keep the footwork clean, make every remaining punch visible.

## 9. No-Go Results

| No-go | Consequence |
|---|---|
| identity closure does not select EH | EH operator selection remains separate |
| Bianchi identity is not uniqueness | conserved non-EH tensors remain |
| metric-only is not enough | second-order/locality or coefficient control is mandatory |
| EFT suppression is not exact reduction | suppressed residues are testable, not theorem-zero |
| EH without source normalization is not Newton | source-normalized Newtonian limit is next |

## 10. Gate Results

| Gate | Status | Evidence |
|---|---:|---|
| source paths exist | pass | all cited source paths exist |
| identity closure retained as label | pass | closure-zero, not parent-derived WEP |
| EH conditional selection theorem written | pass | metric-only local 4D second-order exterior selects EH if assumed |
| EH parent-derived | fail | core premises remain open |
| non-EH operator ledger retained | pass | all operator families stay explicit |
| source-normalized Newtonian limit derived | fail | next target |
| PPN/local-GR promoted | fail | no promotion allowed |
| claim ceiling enforced | pass | no EH/PPN/source/boundary/bulk/fifth-force/local-GR pass |

## 11. Decision

Decision:

```text
EH_operator_selection_under_identity_closure_attempt_written_EH_conditional_not_parent_derived_nonEH_operators_retained_no_local_GR_pass
```

Interpretation:

```text
Identity closure is useful.
It removes the matter/coframe pullback ambiguity in the GR-facing branch.
But it does not derive Einstein-Hilbert.
EH is selected only if the extra operator premises are also derived:
  metric-only,
  local,
  4D,
  second-order,
  source-normalized,
  boundary/bulk/vector/nonlocal no-hair.
Those premises remain open.
Therefore all non-EH operators stay in the ledger.
```

Claim ceiling:

```text
EH_operator_selection_under_identity_closure_only_no_EH_PPN_source_boundary_bulk_fifth_force_or_local_GR_pass
```

## 12. Next Target

393 - Source-Normalized Newtonian Limit Under Identity Closure

Task:

```text
derive kappa, G_eff, M_eff, and measured-GM absorption under identity closure,
or keep delta_G, Gdot/G, beta, and fifth-force rows active.
```

Pass condition:

```text
constant universal source normalization is parent-derived,
or source-normalization residues remain explicit and budgeted.
```
