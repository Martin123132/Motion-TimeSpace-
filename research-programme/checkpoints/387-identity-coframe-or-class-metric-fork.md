# 387 - Identity Coframe Or Class-Metric Fork

Private local-GR/WEP branch checkpoint. This is not a public WEP, PPN, preferred-frame, fifth-force, Einstein-Hilbert, source-normalization, boundary, bulk-field, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 386 made the local budget pressure explicit:

```text
order-one retained pullback couplings fail every numeric local row.
```

So the next move cannot be:

```text
maybe it is small.
```

The next move has to be structural.

Checkpoint 385 already gave the legal fates of:

```text
Pi_I^matter =
  (delta S_matter / delta ehat)
  (partial ehat / partial Z_I).
```

This checkpoint turns that into the unavoidable fork:

```text
Branch A: local matter sees the identity/metric coframe.
Branch B/C/D: local matter sees a class-metric pullback, retained as closure/counterstress unless derived.
```

This is not narrowing the whole theory to GR.

It is protecting the local-GR reduction target from being muddled with a different modified-gravity branch.

## 2. Machine Artifact

Script:

```text
scripts/identity_coframe_or_class_metric_fork.py
```

Run:

```text
runs/20260602-015500-identity-coframe-or-class-metric-fork
```

Outputs:

```text
results/source_register.csv
results/branch_fork_table.csv
results/fork_theorems.csv
results/local_GR_requirements.csv
results/runner_impact.csv
results/branch_demotion_rules.csv
results/parent_selector_contract.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

Status:

```text
identity_coframe_local_GR_branch_prioritized_class_metric_pullback_demoted_to_closure_or_counterstress_no_local_GR_pass
```

Claim ceiling:

```text
branch_fork_contract_only_no_WEP_PPN_fifth_force_EH_source_boundary_bulk_or_local_GR_pass
```

Source paths missing:

```text
0
```

## 3. The Fork

Four local coupling branches are now separated:

| Branch | Matter coupling | Local-GR status |
|---|---|---|
| `A_identity_metric_coframe` | `S_matter[psi_A, e, omega[e], constants_A]` | viable candidate, not parent-derived |
| `B_universal_class_metric` | `S_matter[psi_A, exp(F(C_D)) e, ...]` | closure/counterstress unless common mode is killed |
| `C_species_class_metric` | `sum_A S_A[psi_A, exp(F_A(C_D))e, ...]` | fails WEP unless `F_A=F` is derived |
| `D_Ward_owned_class_pullback` | class pullback retained with `E_selector,I + Pi_I^matter=0` | honest modified-gravity fallback |

The important distinction:

```text
identity coframe removes the matter pullback.
class metric must own or budget the pullback.
```

That is the fork.

## 4. Branch A: Identity/Metric Coframe

Branch A says:

```text
ehat_A^a_mu = e^a_mu
```

for every matter species.

The matter action is:

```text
S_matter = sum_A S_A[psi_A, e, omega[e], constants_A].
```

Then for nonmetric MTS selector variables:

```text
Z_I in {C_D, Cperp, P_D, X, boundary, domain, source-normalization data, ...}
```

we have:

```text
partial e / partial Z_I = 0.
```

Therefore:

```text
Pi_I^matter = 0.
```

This is mathematically clean.

It is the best local-GR candidate because the matter sector no longer carries a hidden class-metric force.

But:

```text
the parent action has not yet derived why matter must see e rather than ehat(C_D).
```

So the status is:

```text
conditional theorem target,
not local-GR pass.
```

## 5. Branch B: Universal Class Metric

Branch B says:

```text
ehat^a_mu = exp(F(C_D)) e^a_mu
```

with one common `F(C_D)` for all species.

This can avoid direct species splitting if `F` is genuinely common.

But the pullback remains:

```text
Pi_C^matter ~ T_hat partial_C F.
```

So Branch B still owes one of:

```text
F'(C_D)=0 locally,
pure gauge pullback,
constant universal source/GM absorption,
or Ward-owned no-hair counterstress.
```

Without that, Branch B is not a local-GR derivation.

It is:

```text
common-mode residual branch.
```

That means clock, gamma, fifth-force, and `Gdot/G` rows remain active.

## 6. Branch C: Species Class Metric

Branch C says:

```text
ehat_A^a_mu = exp(F_A(C_D)) e^a_mu.
```

This is the danger branch.

Representative invariance does not kill it because:

```text
C_D
```

is already a class observable.

So:

```text
F_A(C_D)
```

can be representative-invariant and still species-dependent.

The active WEP split is:

```text
Delta F_AB = F_A(C_D) - F_B(C_D).
```

Therefore:

```text
eta_WEP
```

stays active unless a parent species symmetry/common-F selector derives:

```text
F_A(C_D)=F(C_D)
```

for all species.

This branch is not dead as a mathematical possibility.

But for local GR it is demoted unless the common-F theorem is supplied.

## 7. Branch D: Ward-Owned Class Pullback

Branch D does not pretend the pullback vanishes.

It keeps:

```text
E_selector,I + Pi_I^matter = 0.
```

This is honest because the selector stress is in the Ward ledger.

But it is not automatically GR.

It becomes:

```text
modified-gravity/counterstress branch.
```

To become locally safe, the retained stress must be:

```text
no-hair,
boundary-only harmless,
source-normalized,
or below source-locked local budgets.
```

Otherwise it lands back in:

```text
eta_WEP,
clock,
gamma/beta,
preferred-frame,
Gdot,
or fifth-force rows.
```

## 8. Fork Theorems

The theorem-level state is:

| Theorem | Result | Status |
|---|---|---|
| identity coframe pullback zero | `Pi_I^matter=0` for nonmetric `Z_I` | mathematically sufficient given premises |
| universal class metric common mode | common species split can vanish, but `T partial_C F` remains | obstruction |
| species class metric WEP no-go | representative invariance does not force `F_A=F_B` | no-go |
| counterstress not GR by itself | owning stress preserves conservation but not PPN safety | fallback only |

The key clean theorem is:

```text
if ehat=e and matter constants do not depend on Z_I,
then dS_matter/dZ_I=0 for nonmetric selector variables.
```

The missing step is not algebra.

The missing step is parent selection:

```text
why must ehat=e?
```

## 9. Local-GR Requirements

The local-GR route now requires:

| Requirement | Identity branch | Class-metric branch |
|---|---|---|
| universal metric matter | clean if parent-selected | common only if `F_A=F` |
| no selector pullback force | clean for nonmetric `Z_I` | fails unless silence/gauge/source-normalization/counterstress |
| matter Ward identity | ordinary Ward identity on `e` | needs selector stress in total Ward ledger |
| Newton/GR limit | can target EH/source/operator stack next | cannot promote until pullback rows are no-hair/budgeted |
| empirical local budget | avoids matter-pullback budgets | must meet 386 budgets |

So Branch A is not a victory yet.

It is the clean route to try.

Branch B/C/D are still valuable, but not as derived local GR until their extra debts are paid.

## 10. Runner Impact

| Observable | Identity branch | Class/counterstress branch |
|---|---|---|
| `eta_WEP` | theorem-zero if identity/common-F is parent-selected | active unless species symmetry/common-F/no composition charge |
| `alpha_clock_redshift` | ordinary metric clock if constants independent | common `F(C_D)` can be clock-visible |
| `gamma/beta` | pressure moves to EH/operator/source stack | scalar/common-mode/counterstress remains |
| `alpha1/alpha2/xi` | projector/domain absent from matter coframe | selector/domain leakage can remain |
| `Gdot/fifth_force` | only source/bulk/boundary channels remain | common radial/time pullback can source force/drift |

This is why the project should not blur the branches.

The identity branch can still aim at:

```text
GR reduces to Newton
```

style local recovery.

The class-metric branch is closer to:

```text
modified gravity with retained residual stress
```

unless a deeper parent theorem collapses it to Branch A.

## 11. Demotion Rules

The rules are now explicit:

| Condition | Allowed label | Forbidden label |
|---|---|---|
| identity coframe assumed but not parent-derived | local WEP closure branch | derived local GR |
| common class metric with `F'` not zero | common-mode residual branch | local GR reduction |
| species class functions allowed | active WEP residual branch | WEP-safe branch |
| selector counterstress invoked | modified-gravity counterstress branch | GR unless no-hair/source-budget is derived |

This keeps the theory honest.

It also keeps it alive.

Because a branch being demoted is not the same as the whole framework failing.

It just means:

```text
do not make the wrong claim from the right calculation.
```

## 12. Parent Selector Contract

A future parent action must satisfy this exact contract:

| Contract item | Required statement |
|---|---|
| identity/common metric selector | one matter coframe, no species-labelled observed geometries |
| forbid class-dependent constants | no `m_A(C_D)`, `alpha_A(C_D)`, clock, or charge response except universal absorbed units |
| selector pullback ownership | `partial ehat/partial Z_I=0`, pure gauge, constant-normalized, or `E_selector,I + Pi_I^matter=0` |
| runner transition discipline | budget rows become derived-zero only with a theorem source |

The strong local-GR preference is:

```text
ehat = e
```

locally.

Then MTS can still exist, but local matter does not see it as a separate class metric.

MTS effects must move into:

```text
metric equation,
source normalization,
nonlocal/cosmological sector,
boundary/bulk sectors,
or higher operator stack.
```

Those sectors still need work, but they are the correct next debts after the WEP pullback is removed.

## 13. Gate Results

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | all cited source paths exist |
| fork branches written | pass | four local coupling branches classified |
| identity branch mathematically sufficient | conditional pass | `Pi_I^matter` vanishes if matter sees `e` and nonmetric `Z_I` do not enter constants |
| identity branch parent-derived | fail | no parent selector yet forbids class-metric/coframe functions |
| class metric demoted | pass | closure/counterstress unless silence/source-normalization/species symmetry/no-hair is derived |
| `eta_WEP` resolved | fail | species common-F selector remains next target |
| WEP/PPN/local GR promoted | fail | branch fork only; no row moves to derived-zero |
| claim ceiling enforced | pass | no WEP/PPN/fifth-force/EH/source/boundary/bulk/local-GR pass |

## 14. Decision

Decision:

```text
identity_coframe_local_GR_branch_prioritized_class_metric_pullback_demoted_to_closure_or_counterstress_no_local_GR_pass
```

Meaning:

```text
the local-GR route should prioritize identity/metric coframe.
```

That branch is mathematically sufficient to remove:

```text
Pi_I^matter
```

for nonmetric selector variables.

But it is not yet parent-derived.

So the current state is:

```text
identity coframe = primary theorem target,
class metric = closure/counterstress branch,
species class metric = WEP debt unless common-F is derived.
```

This improves the project because it stops one of the biggest hidden ambiguities:

```text
does matter see geometry,
or does matter see MTS class geometry?
```

For local GR, the answer must be:

```text
matter sees geometry,
unless the class pullback is fully owned and locally silent.
```

## 15. Next Target

Next:

```text
388 - WEP Species Symmetry Common-F Parent Selector Attempt
```

Aim:

```text
try to derive F_A(C_D)=F(C_D),
or prove that the identity coframe branch is the only clean local matter-coupling route.
```

Pass condition:

```text
common-F is parent-derived,
or eta_WEP remains explicit closure/budget debt.
```

Why this next:

```text
eta_WEP is still the hardest always-relevant ready row.
```

If we can derive the species symmetry/common-F selector, the local branch gets much stronger.

If we cannot, the theory still survives only by choosing:

```text
identity coframe as a parent principle
```

or accepting:

```text
WEP closure/counterstress.
```
