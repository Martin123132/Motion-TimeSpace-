# 382 - Parent Local Action Minimal Contract

Private parent-action/local-GR checkpoint. This is not a public WEP, PPN, Einstein-Hilbert, fifth-force, boundary no-hair, bulk-field, source-normalization, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 381 said the local-GR route is:

```text
coherent,
finite,
not promoted.
```

The reason is now clear:

```text
the remaining blockers are action-level blockers.
```

Not one missing fit.

Not one nicer phrase.

Not one more hand-picked local silence assumption.

The branch needs a parent local action whose variation forces the right things:

```text
one observed coframe,
owned selector/class/projector/domain variables,
Ward force closure,
EH-only exterior operator,
source normalization,
class-only/Ward-owned boundary terms,
bulk-X no-hair or source-normalized force law,
and explicit residual fallbacks when any premise fails.
```

This checkpoint writes that contract.

It does not satisfy it.

That distinction is the whole discipline.

Current result:

```text
minimal parent local action contract written,
required variations and fallbacks explicit,
contract not satisfied,
no local-GR promotion.
```

## 2. Machine Artifact

Script:

```text
scripts/parent_local_action_minimal_contract.py
```

Run:

```text
runs/20260602-010500-parent-local-action-minimal-contract
```

Outputs:

```text
results/source_register.csv
results/action_blocks.csv
results/variation_identities.csv
results/local_GR_sufficiency_stack.csv
results/residual_fallback_rows.csv
results/contract_tests.csv
results/claim_policy.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

Status:

```text
parent_local_action_minimal_contract_written_required_variations_and_fallbacks_explicit_not_satisfied_no_local_GR_promotion
```

Claim ceiling:

```text
parent_action_contract_only_no_WEP_PPN_EH_boundary_bulk_fifth_force_source_or_local_GR_pass
```

Source paths missing:

```text
0
```

## 3. Minimal Action Skeleton

The contract form is:

```text
S_parent =
  S_EH_or_metric_core[g/e]
  + S_matter[Psi_A, ehat]
  + S_selector_liftedC_class[g/e, C, P_D, class data]
  + S_projector[P_D, relative chains, boundary data]
  + S_X[g/e, X, P, J_eff]
  + S_boundary[g/e|partialD, Q_rel, M_eff, X, P_D, Y_partialD]
  + S_domain[chi_D, n_mu, L_cg, class/domain data]
  + S_source_norm[kappa, G_eff, M_eff, Pi_M J].
```

This is not proposed as a final beautiful action.

It is the minimum list of sectors that cannot be hidden.

If a future action leaves one out, it must explain why that sector is absent by symmetry, gauge, topology, or low-energy theorem.

If it cannot, the missing sector becomes a residual.

## 4. Action Blocks

| Block | Must vary to | If failed |
|---|---|---|
| `S_EH_or_metric_core` | EH as only surviving local exterior operator | modified-gravity operator ledger |
| `S_matter_one_coframe` | no direct MTS matter vertices; matter Ward identity on one `ehat` | WEP, clock, nonmetric light/species charge |
| `S_selector_lifted_C_class` | quotient/class metric selected without raw `Cperp` trace source | projected-metric closure / `phi_C` residual |
| `S_projector_P_D` | `F_P_bulk=0` or retained conserved projector stress | gamma, xi, preferred-frame, conservation residual |
| `S_X_auxiliary_or_mass_gap` | `F_X=0` by constraint/no-hair or `alpha_X(lambda_X)` if sourced | bulk residual, fifth-force, gamma/beta |
| `S_boundary_class_only` | no `B_TF`, no `B_0i`, Ward-owned flux | boundary coefficients |
| `S_domain_covariant_selector` | no fixed preferred normal/domain vector leakage | `alpha1`, `alpha2`, `xi` |
| `S_source_normalization` | `kappa`, `G_eff`, `M_eff`, measured `GM` fixed | `delta_G`, `Gdot/G`, beta, fifth-force, WEP |

This is the tight version of the local-GR bill.

No line can be paid by vibes.

Each has to be paid by variation, theorem, or retained residual.

## 5. Required Variation Identities

The future parent action must produce at least these identities.

### Ward identity

```text
nabla_mu(T_matter^munu + kappa^-1 E_MTS^munu)
  + F_X^nu
  + F_P^nu
  + F_boundary^nu
  + F_domain^nu
  + F_matter_nonmetric^nu
  = 0.
```

Required:

```text
every force channel is varied, owned, zero-derived, boundary-only harmless,
or retained.
```

Current status:

```text
structural identity written,
not closed.
```

### Matter/coframe identity

```text
delta S_matter / delta Z_I | ehat = 0
```

for:

```text
Z_I in {X, J_rel, V_def, P_D, Cperp, species charges, ...}.
```

Required:

```text
one ehat for all matter, clocks, photons, rulers, standards,
and no species-dependent F_A(C_D).
```

Current status:

```text
conditional if one coframe is assumed,
not parent-derived.
```

### EH exterior identity

```text
Ward closure
+ no-hair
+ universal coupling
+ metric-only local 4D second-order diffeo exterior
  -> S_ext = S_EH + boundary.
```

Required:

```text
operator basis is EH-only through local PPN order.
```

Current status:

```text
conditional sufficiency theorem,
not parent-derived.
```

### Source-normalized Newtonian limit

```text
M_eff = (4 pi G_ref)^-1 int_S2 Pi_M J,
d(Pi_M J) = 0,
mu_obs = G_eff M_eff.
```

Required:

```text
constant universal measured-GM absorption only,
no drift,
no species dependence,
no range leakage.
```

Current status:

```text
M_eff conditional,
GM absorption open.
```

### Boundary identity

```text
delta S_boundary / delta B_TF = 0,
delta S_boundary / delta B_0i = 0,
n_mu B^{mu nu} + F_boundary_owned^nu = 0.
```

Required:

```text
class-only boundary action,
no angular representatives,
no marker normals,
no radial hair,
Ward-owned flux.
```

Current status:

```text
conditional no-angular theorem,
flux/radial/class-only proof open.
```

### Bulk-X identity

Either:

```text
(-Delta + m_X^2) X = 0,
m_X^2 > 0
  -> X = 0
```

or:

```text
(-Delta + m_X^2) X = q_X rho_source
  -> alpha_X(lambda_X).
```

Required:

```text
positive operator/source-free exterior,
or parent-normalized X force law.
```

Current status:

```text
contract written,
not parent-derived.
```

## 6. Local-GR Sufficiency Stack

The local-GR theorem is only legal if the stack closes:

| Rung | Condition | Current status |
|---:|---|---|
| 1 | compact ordinary local exterior | definition plus source conditions open |
| 2 | one observed coframe | closure axiom, not parent-derived |
| 3 | full Ward force closure | mapped, not closed |
| 4 | local no-hair / local silence | conditional mechanisms only |
| 5 | source normalization | not parent-derived |
| 6 | metric-only second-order exterior | central blocker |
| 7 | Newton/PPN reduction | not claimable; coefficients missing |

If this stack closes, the local branch can say:

```text
MTS reduces to GR locally in the same sense GR reduces to Newton in the weak-field limit.
```

If it does not close, the theory is not automatically dead.

It becomes:

```text
a disciplined modified-gravity/residual branch
with explicit local-bound rows.
```

That is the honest fork.

## 7. Residual Fallback Rows

If the contract fails, these rows stay alive:

| Failed contract | Fallback | Runner policy |
|---|---|---|
| one coframe / universal coupling | `eta_WEP`, `alpha_clock` active | source-locked budget only |
| EH operator selection | retain `c_i O_i` modified-gravity coefficients | budget or unscored if range missing |
| boundary class-only / Ward flux | retain `eps_B_TF`, `eps_B0i`, `eps_B_rad`, `eps_B_flux` | no boundary no-hair claim |
| bulk-X no-hair / force law | retain `epsilon_bulk` or derive `alpha_X(lambda_X)` | unscored until charges/range derived |
| source normalization | retain `delta_G`, `Gdot/G`, source ambiguity | only constant universal monopole absorbable |
| preferred-frame/domain covariance | retain vector/domain coefficients | source-locked budget only |

This is important.

The parent action contract does not erase residuals.

It decides which residuals are:

```text
theorem-zero,
closure-zero,
budget-only,
or unscored.
```

## 8. Contract Tests

The contract passes only if all of these are true:

| Test | Pass condition | Current result |
|---|---|---|
| all action blocks varied | every sector varied explicitly | contract written, not performed |
| no hidden force channels | every Ward force zero/boundary/retained | ledger written, not closed |
| single observed coframe forced | `ehat_A=ehat`, `F_A=F` | fail open |
| EH operator forced | non-EH coefficients vanish or are retained | fail open |
| source normalization forced | `kappa`, `G_eff`, `M_eff`, `GM` fixed | fail open |
| boundary/bulk no-hair forced | class-only boundary and positive/source-free `X` | fail open |
| residual fallbacks retained | failed premises feed explicit rows | pass contract |

So the result is:

```text
contract useful,
contract unsatisfied.
```

## 9. What This Improves

This checkpoint prevents a subtle bad move:

```text
solve WEP in one paragraph,
solve boundary in another,
solve X in another,
then pretend the whole parent action exists.
```

No.

The single parent action has to vary consistently.

For example:

```text
one coframe,
class-only boundary,
and no bulk-X matter charge
```

cannot be three unrelated local wishes.

They need one symmetry, constraint, quotient principle, or variational selector.

That is the next serious derivation target.

## 10. What Still Fails

The contract does not yet derive:

```text
one observed coframe,
common species class function,
lifted-C physical class selector,
EH-only exterior operator,
source normalization,
class-only boundary dependence,
Ward-owned boundary flux,
positive source-free bulk-X operator,
alpha_X(lambda_X),
alpha_Y(lambda_Y),
or PPN coefficients.
```

So no public-style local claim follows.

This is not pessimism.

It is the exact target list.

## 11. Gate Results

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | all cited source paths exist |
| action blocks listed | pass | eight minimal action blocks specified |
| variation identities listed | pass | six required variation identities specified |
| local-GR sufficiency stack written | pass | seven sufficiency rungs listed |
| residual fallback rows written | pass | six fallback rows mapped |
| parent action contract satisfied | fail | one-coframe/EH/source/boundary/bulk-X derivations remain open |
| local GR promoted | fail | contract only |
| budget-only testing next allowed | pass | fallback rows can feed local-bound runner v2 |
| claim ceiling enforced | pass | no WEP/PPN/EH/source/boundary/bulk/local-GR pass |

## 12. Decision

Decision:

```text
parent_local_action_minimal_contract_written_required_variations_and_fallbacks_explicit_not_satisfied_no_local_GR_promotion
```

Meaning:

```text
we now have the exact parent local action contract the future theory must satisfy.
```

But:

```text
we have not yet derived that action.
```

So the branch stays:

```text
serious,
coherent,
testable as residuals,
not locally GR-derived.
```

No promotion:

```text
WEP not passed,
PPN not passed,
EH not derived,
source normalization not derived,
boundary no-hair not derived,
bulk-X no-hair not derived,
local GR not derived.
```

## 13. Next Target

Next:

```text
383 - Local-Bound Runner V2 From Retained Residuals
```

Aim:

```text
convert the fallback rows into a no-claim local-bound runner matrix.
```

It must separate:

```text
derived zero,
closure zero,
budget-only,
and unscored parameterized
```

states.

Why this next:

```text
we have the contract.
```

Now the empirical side can test the retained rows without pretending the parent action has already paid the bill.

That is the Mayweather route here:

```text
stay in the round,
score clean counters,
do not throw fake haymakers.
```
