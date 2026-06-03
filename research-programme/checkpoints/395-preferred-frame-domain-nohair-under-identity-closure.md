# 395 - Preferred-Frame Domain No-Hair Under Identity Closure

Private preferred-frame/domain/local-GR checkpoint. This is not a public PPN, preferred-frame, domain-projector, WEP, Einstein-Hilbert, source-normalization, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 394 joined boundary and bulk into one local force/flux runner. The next local-GR gate is:

```text
Can the remaining preferred-frame/domain/projector residues be killed,
or must alpha1, alpha2, alpha3, xi, and Gdot/G stay in the runner?
```

Identity closure helps, but only in one place:

```text
ehat = e
  => direct coframe vector slip is closure-zero inside this branch.
```

It does not kill:

```text
domain vectors,
projector representative leakage,
boundary vector B_0i,
domain anisotropy,
H1/H2 topology-cycle memory,
or unowned domain/projector/boundary flux.
```

Current result:

```text
coframe slip closed by label;
domain/projector preferred-frame no-hair not parent-derived;
alpha1, alpha2, alpha3, xi, and Gdot/G stay retained.
```

## 2. Run Manifest

Script:

```text
scripts/preferred_frame_domain_nohair_under_identity_closure.py
```

Expected run directory:

```text
runs/<timestamp>-preferred-frame-domain-nohair-under-identity-closure
```

Expected result files:

```text
results/source_register.csv
results/identity_branch_vector_split.csv
results/domain_projector_nohair_contract.csv
results/preferred_frame_coefficient_map_under_identity.csv
results/domain_to_observable_ledger.csv
results/nohair_or_budget_decision_tree.csv
results/runner_policy_rows.csv
results/no_go_results.csv
results/gate_policy.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

## 3. Identity-Branch Vector Split

The dangerous vector/preferred-frame set is:

```text
V_vec = {
  coframe_slip,
  B_0i,
  domain_vector,
  projector_vector,
  domain_anisotropy,
  unowned_flux
}.
```

Under identity closure:

```text
coframe_slip := ehat - e = 0
```

but only as:

```text
closure_zero_not_derived_zero.
```

Everything else remains:

| Channel | State | Rows |
|---|---:|---|
| coframe slip | closure-zero by identity label | `alpha1`, clock, WEP closed only in branch |
| `B_0i` boundary vector | retained | `alpha1`, `alpha2`, `alpha3` |
| domain vector/normal | retained | `alpha1`, `alpha2`, `xi` |
| projector vector leakage | retained | `alpha1`, `alpha2`, `xi`, gamma-if-stress |
| domain anisotropy/cycles | retained | `xi`, gamma, slip |
| unowned flux | retained | `alpha3`, `Gdot/G`, secular drift |

This is the fair split: we do not double-count the coframe channel, but we do not let domain/projector hair hide behind it either.

## 4. Domain/Projector No-Hair Contract

The preferred-frame/domain theorem would need:

| Premise | Would kill | Current status |
|---|---|---:|
| scalar/topological domain selector | `eps_domain_vec`, `eps_domain_aniso` | not parent-derived |
| metric-independent projector or retained stress | fake Bianchi/projector vector force | conditional formal action only |
| representative invariance | representative vector leakage | open |
| topology-cycle silence | H1/H2 vector/cavity modes | not parent-derived |
| free-boundary Euler without vector normal | normal-frame/patch-marker residues | physical selection open |
| Ward-owned domain flux | `alpha3`, `Gdot/G`, secular drift | mapped, not proved |

So the theorem shape is good, but the parent action has not earned it.

## 5. Coefficient Map Under Identity

The updated source-locked maps are:

| Residual | Map after identity closure | State |
|---|---|---:|
| `alpha1` | `C1B eps_B0i + C1D eps_domain_vec + C1P eps_P_vector + C1M eps_marker` | budget-only |
| `alpha2` | `C2B eps_B0i + C2D eps_domain_vec + C2A eps_domain_aniso + C2P eps_P_vector` | budget-only |
| `alpha3` | `C3F eps_unowned_flux + C3D eps_domain_momentum_drift + C3B eps_boundary_flux` | contingent budget-only |
| `xi` | `CxiTF eps_B_TF_l>=2 + CxiD eps_domain_aniso + CxiExt eps_external_domain_aniso + CxiTopo eps_H1H2_cycle` | budget-only |
| `Gdot/G` | `CGF eps_unowned_flux_dot + CGD eps_domain_scale_dot + CGM eps_Meff_dot + CGK eps_memory_kernel_drift` | contingent budget-only |

The old coframe-slip term is not used as an active retained term inside this branch, because identity closure removes it by label.

## 6. Domain-to-Observable Ledger

| Domain/projector piece | Status | Local risk | Rows |
|---|---:|---|---|
| fixed-domain coherent projection | mathematically sharpened | physical selector still absent | `xi/gamma` only if anisotropy leaks |
| physical domain selector | not parent-derived | preferred frame/normal or tuned scale | `alpha1`, `alpha2`, `xi` |
| domain boundary Euler | conditional admissibility only | normal/patch marker physical | `alpha1`, `alpha2`, `alpha3`, `xi` |
| H1/H2 cycles or cavity modes | not parent-forbidden | vector/cycle memory | `xi`, `alpha1`, `alpha2` |
| dropped projector stress | forbidden shortcut | fake Bianchi closure | `alpha3`, `Gdot/G`, `beta` |
| representative-dependent matter action | open outside identity branch | clock/WEP/preferred-frame reopening | clock, WEP, `alpha1` |

## 7. Decision Tree

| Condition | Decision | Forbidden inference |
|---|---|---|
| coframe vector slip only | closure-zero inside identity branch | parent-derived vector no-hair |
| domain/projector vector pure gauge/topological | derived-zero if parent proves gauge status | covariance alone proves it |
| domain/projector stress retained | budget-only | dropping stress after using projector |
| unowned flux/momentum nonconservation | contingent `alpha3/Gdot` budget | erase without Ward owner |
| domain anisotropy/topology cycles survive | budget `xi` and related slip | fold `xi` into gamma only |

## 8. Runner Policy

| Row | State after 395 |
|---|---|
| `alpha1` | retained budget-only |
| `alpha2` | retained budget-only |
| `alpha3` | retained contingent budget |
| `xi` | retained budget-only |
| `Gdot/G` | retained contingent budget |
| local-GR reduction | fail promotion |

## 9. No-Go Results

| No-go | Consequence |
|---|---|
| covariance does not kill physical domain vectors | gauge/topological status must be derived |
| identity coframe does not kill domain anisotropy | `alpha_i` and `xi` remain active |
| formal projector Bianchi is not physical selector | domain selector/scale debts remain |
| `xi` is not gamma | preferred-location row stays separate |
| `alpha3` is contingent, not optional | score only if channel exists, but do not erase unowned flux |

## 10. Gate Results

| Gate | Status | Evidence |
|---|---:|---|
| source paths exist | pass | all cited source paths exist |
| identity coframe slip closed by label | closure pass | `eps_coframe_slip` removed only inside identity branch |
| domain/projector no-hair parent-derived | fail | selector, gauge status, topology, Euler, and flux premises open |
| preferred-frame coefficient map updated | pass | identity-closed and retained terms separated |
| Ward flux owned | fail | domain/projector/boundary flux mapped, not owned |
| `xi` kept separate | pass | domain anisotropy/topology cycles kept in `xi` row |
| preferred-frame/PPN promoted | fail | coefficients missing or contingent |
| local-GR promoted | fail | conditional/retained only |
| claim ceiling enforced | pass | no preferred-frame/PPN/domain/local-GR pass |

## 11. Decision

Decision:

```text
preferred_frame_domain_nohair_under_identity_written_coframe_slip_closed_by_label_domain_projector_vector_residues_retained_no_PPN_or_local_GR_pass
```

Interpretation:

```text
Identity closure removes direct coframe vector slip in this branch.
It does not derive preferred-frame/domain no-hair.
Domain selector vectors, projector vector leakage, boundary B_0i,
domain anisotropy, topology-cycle memory, and unowned flux remain retained.
alpha1, alpha2, alpha3, xi, and Gdot/G stay in the runner.
```

Claim ceiling:

```text
preferred_frame_domain_nohair_under_identity_only_no_preferred_frame_PPN_domain_projector_or_local_GR_pass
```

## 12. Next Target

396 - Local-GR Reduction Sufficiency Stack Audit

Task:

```text
roll up identity, EH, source, boundary, bulk, preferred-frame,
and domain gates into one local-GR sufficiency audit.
```

Pass condition:

```text
every local-GR premise is classified as derived,
closure-only,
conditional,
retained,
failed,
or ready for runner-v3.
```
