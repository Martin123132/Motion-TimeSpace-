# 398 - Parent Action Contract v2 After Identity Stack

Private parent-action/local-GR checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, boundary, bulk, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 397 built runner-v3. It did the honest thing:

```text
closure_zero stayed closure_zero,
budget_only stayed budget_only,
contingent_budget stayed contingent,
unscored_parameterized stayed unscored,
retained_residual stayed retained.
```

This checkpoint writes the next parent-action contract:

```text
What must a future parent action derive to turn each runner-v3 row into a theorem row?
```

Answer:

```text
every non-derived runner-v3 state needs a named action block,
variation identity,
Ward owner,
or force-law/source-normalization theorem.
```

The contract is written here. It is not satisfied yet.

## 2. Run Manifest

Script:

```text
scripts/parent_action_contract_v2_after_identity_stack.py
```

Expected run directory:

```text
runs/<timestamp>-parent-action-contract-v2-after-identity-stack
```

Expected result files:

```text
results/source_register.csv
results/parent_action_blocks_v2.csv
results/runner_row_parent_obligations.csv
results/required_variation_identities_v2.csv
results/no_cheat_rules_v2.csv
results/derivation_milestones.csv
results/contract_tests_v2.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

## 3. Parent Action Blocks v2

The future local parent action must pay for these blocks:

| Block | Must vary to | Rows paid |
|---|---|---|
| `S_metric_core` | EH-only local exterior or explicit non-EH coefficients | `gamma`, `beta`, `xi`, fifth force, operator ledger |
| `S_matter_identity_or_selector` | `ehat=e` or no nonmetric matter pullback | direct WEP/coframe row |
| `S_species_blind_constants` | no species source charge or constants drift | WEP-source, clock, composition force |
| `S_source_normalization` | constant universal `kappa/G_eff/M_eff/GM` | `beta`, `Gdot/G`, fifth force, WEP-source |
| `S_boundary_class_flux` | no `B_TF`, no `B_0i`, no radial/flux hair | `gamma`, `beta`, `alpha_i`, `xi`, `Gdot/G` |
| `S_bulk_X` | `X=0` no-hair or `alpha_X(lambda_X)` | fifth force, WEP-source, `gamma`, `beta` |
| `S_projector_domain` | no physical domain/projector vector or retained stress | `alpha_i`, `xi`, `Gdot/G` |
| `S_total_Ward_owner` | every force/flux channel owned, zero, or retained | `alpha3`, `Gdot/G`, source drift |

## 4. Runner Row Obligations

| Runner row | State | Parent obligation |
|---|---:|---|
| `R0 eta_WEP_direct_geometry` | `closure_zero` | derive `ehat=e` from parent variation |
| `R1 eta_WEP_source_charge` | `contingent_budget` | forbid species-dependent source/bulk/boundary charges |
| `R2 alpha_clock` | `budget_only` | fix constants and clock sector against nonmetric/source drift |
| `R3 gamma` | `budget_only` | derive EH-only exterior and remove/budget shear/bulk/domain slip |
| `R4 beta` | `budget_only` | derive nonlinear source-normalized Newtonian limit |
| `R5 alpha1` | `budget_only` | remove boundary/domain/projector vector leakage |
| `R6 alpha2` | `budget_only` | remove anisotropic domain/projector vector residues |
| `R7 alpha3` | `contingent_budget` | own or eliminate momentum/flux nonconservation |
| `R8 xi` | `budget_only` | remove boundary/domain/topology preferred-location anisotropy |
| `R9 Gdot/G` | `contingent_budget` | derive time-independent `G_eff M_eff` and no flux drift |
| `R10 fifth force` | `unscored_parameterized` | derive zero theorem or `alpha(lambda)` profiles |
| `R11 non-EH operators` | `retained_residual` | derive EH operator selection or retain every coefficient |

## 5. Required Variation Identities

The contract needs these identities:

```text
matter identity coframe:
  delta S_matter/delta Z_I|e = 0,
  ehat=e,
  partial_Z theta_A = 0.

species-blind source charge:
  partial_A mu_obs = 0,
  q_X,A/m_A universal or q_X=0.

EH operator selection:
  E_ext^{mu nu} = a G^{mu nu} + b g^{mu nu},
  all non-EH H_i coefficients zero or retained.

source-normalized Newtonian limit:
  G_eff = kappa_eff c^4/(8 pi),
  mu_obs = G_eff M_eff,
  partial_r,t,A mu_obs = 0.

boundary class/flux no-hair:
  delta S_boundary/delta B_TF = 0,
  delta S_boundary/delta B_0i = 0,
  B_rad = 0,
  n_mu B^{mu nu}+F_owned^nu = 0.

bulk-X no-hair or force law:
  (-Delta+m_X^2)X=0 -> X=0,
  or (-Delta+m_X^2)X=q_X rho -> alpha_X(lambda_X).

domain/projector no-hair:
  P_D topological/gauge or T_P,T_D retained,
  domain selector scalar/topological,
  no H1/H2 vector cycles.

total Ward force closure:
  F_X + F_P + F_boundary + F_domain + F_source + F_matter_nonmetric = 0
  or retained.
```

## 6. No-Cheat Rules

| Rule | Forbids |
|---|---|
| closure is not derivation | calling `ehat=e` parent-derived without variation proof |
| field redefinition is not GR | renaming `ehat` while EH/source debts remain |
| Bianchi is not uniqueness | deleting non-EH operators by conservation alone |
| `GM` absorption only constant universal | hiding radial/time/species/range dependence in mass |
| boundary effect is not a bucket | hiding shear/vector/radial/flux pieces |
| `alpha3` is contingent, not optional | ignoring unowned flux or scoring it when absent |
| fifth force needs profile | scalar-scoring without `alpha(lambda)` |
| projector stress not droppable | using projector/domain action while dropping stress |

## 7. Derivation Milestones

| Milestone | Success condition |
|---|---|
| identity matter selector | `R0` moves from `closure_zero` to `derived_zero`; `R1` charges forbidden/universal |
| EH operator selection | `R11` coefficients theorem-zero or explicit retained EFT coefficients |
| source normalization | `R4/R9/R10` source exits close except true force-law rows |
| boundary/bulk Ward no-hair | boundary/bulk coefficients zero or `alpha(lambda)`-scored |
| domain/projector theorem | `alpha_i/xi/Gdot` domain/projector channels close or coefficient-map quantitatively |
| PPN coefficient derivation | `gamma=beta=1`, `alpha_i=xi=0`, no fifth force, no `Gdot/G` from parent action |

## 8. Contract Tests

| Test | Current result |
|---|---:|
| every runner-v3 row has parent obligation | pass contract written |
| identity branch not mislabeled | pass policy |
| non-EH operators not deleted | pass policy |
| source/boundary/bulk/domain flux owned | fail open |
| `alpha(lambda)` force law derived | fail open |
| local-GR claim allowed | fail open |

## 9. Gate Results

| Gate | Status | Evidence |
|---|---:|---|
| source paths exist | pass | all cited source paths exist |
| parent action blocks v2 written | pass | action blocks specified |
| runner rows mapped to obligations | pass | runner-v3 row obligations written |
| variation identities written | pass | required variation identities written |
| no-cheat rules written | pass | no-cheat rules recorded |
| contract satisfied | fail | obligations are written but not parent-derived |
| all runner rows promotable | fail | rows remain closure/contingent/budget/unscored/retained |
| local-GR promoted | fail | contract unsatisfied |
| claim ceiling enforced | pass | no WEP/EH/Newton/PPN/fifth-force/boundary/bulk/domain/local-GR pass |

## 10. Decision

Decision:

```text
parent_action_contract_v2_after_identity_stack_written_runner_v3_nonderived_rows_mapped_to_parent_obligations_contract_not_satisfied_no_local_GR_pass
```

Interpretation:

```text
Every runner-v3 non-derived row now has a parent-action obligation.
The contract is sharper than the old skeleton.
It names the exact variations, source-normalization identities,
Ward owners, no-hair theorems, and force-law profiles needed.
The contract is written, not satisfied.
No local-GR claim is allowed.
```

Claim ceiling:

```text
parent_action_contract_v2_only_no_WEP_EH_Newton_PPN_fifth_force_boundary_bulk_domain_or_local_GR_pass
```

## 11. Next Target

399 - Local-GR Status For Human Review

Task:

```text
write a concise private status memo for human review:
what is strong,
what is open,
what to test next,
and where the main files are.
```

Pass condition:

```text
clear project overview with no public overclaim
and direct pointers to runner-v3 / contract artifacts.
```
