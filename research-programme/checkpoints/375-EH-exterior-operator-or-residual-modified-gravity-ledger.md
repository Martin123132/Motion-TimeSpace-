# 375 - EH Exterior Operator Or Residual Modified-Gravity Ledger

Private local-GR operator checkpoint. This is not a public Einstein-Hilbert, PPN, WEP, fifth-force, preferred-frame, clock, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 358 gave the key theorem ladder:

```text
Ward closure + no-hair + universal coupling
  + metric-only local 4D second-order diffeo exterior
  -> Einstein-Hilbert plus Lambda.
```

But it also gave the key negative:

```text
Ward closure alone is not enough.
```

Checkpoint 374 then source-locked the preferred-frame and `xi` rows, while keeping fifth force as a range-dependent force-law contract.

This checkpoint asks:

```text
can we now claim the exterior operator is EH,
or must all non-EH pieces be carried as explicit residual operators?
```

Answer:

```text
EH is not parent-derived in the current branch.
```

So the honest local exterior is:

```text
S_ext = S_EH + sum_i c_i O_i + S_boundary/topological.
```

Each coefficient must be:

```text
theorem-zero,
source-bounded,
or explicitly quarantined/unscored.
```

No operator gets deleted because we would like GR to appear.

That is the whole win here.

## 2. Machine Artifact

Script:

```text
scripts/EH_exterior_operator_or_residual_modified_gravity_ledger.py
```

Run:

```text
runs/20260601-235000-EH-exterior-operator-or-residual-modified-gravity-ledger
```

Outputs:

```text
results/source_register.csv
results/EH_route_status.csv
results/derivation_attempt_steps.csv
results/operator_basis_residual_ledger.csv
results/coefficient_to_observable_map.csv
results/source_bound_join.csv
results/modified_gravity_branch_contract.csv
results/promotion_rules.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

Status:

```text
EH_not_parent_derived_residual_operator_ledger_written_modified_gravity_coefficients_retained_no_local_GR_pass
```

Claim ceiling:

```text
EH_operator_or_residual_modified_gravity_ledger_only_no_EH_PPN_WEP_fifth_force_or_local_GR_pass
```

Source paths missing:

```text
0
```

## 3. Current EH Route Status

The EH route is now cleanly split:

| Premise | Required statement | Current status | Failure mode |
|---|---|---|---|
| compact local exterior | source is conserved monopole/boundary data | definition plus monopole condition open | radial scalar or boundary charge |
| single observed metric/coframe | all matter/light/clocks see one geometry | closure axiom, not parent-derived | WEP/clock residuals |
| Ward force closure | parent force terms vanish, cancel, or are owned | mapped, not proved | unowned flux/source drift |
| local no-hair | bulk/boundary/projector/vector hair vanish or reduce to monopole | not derived | gamma, xi, preferred-frame, fifth force |
| metric-only exterior | no independent scalar/vector/torsion/nonlocal kernel propagates locally | not parent-derived | modified-gravity operator ledger |
| local 4D second-order diffeo operator | surviving exterior equations are second-order metric equations | sufficiency condition only | higher-curvature/nonlocal residuals |
| source normalization | `kappa`, `G_eff`, `M_eff`, measured `GM` fixed | open | `delta_G`, `Gdot/G`, fifth-force ambiguity |

So:

```text
the conditional EH theorem is alive,
but the parent EH derivation is not complete.
```

That is not a contradiction.

It is the difference between:

```text
if the ladder holds, GR follows
```

and:

```text
MTS has derived every rung of the ladder.
```

Only the first is true today.

## 4. Operator Basis Residual Ledger

When EH is not parent-derived, the allowed residual families must stay visible:

| Operator family | Local risk | Residual policy |
|---|---|---|
| EH plus `Lambda` | GR baseline if stack holds | target, not standalone proof |
| boundary/topological terms | hidden shear/vector/flux if not owned | retain boundary residuals unless class-only/owned |
| `R^2` / `f(R)` | extra scalar, Yukawa force, gamma/beta shifts | derive zero or map mass/range/coupling |
| `R_mn R^mn` / `Weyl^2` | higher-derivative spin-2/shear/light-bending risk | derive low-energy suppression or bound |
| scalar-tensor/class metric | clock, gamma, fifth force, WEP if species-specific | local zero theorem or residual runner |
| vector/preferred-frame | `alpha1`, `alpha2`, `alpha3`, `xi` | vector no-hair or coefficient map |
| torsion/nonmetricity | spin/WEP/clock/light-cone residuals | metric-compatibility theorem or retain |
| nonlocal/memory kernels | scale-dependent `delta_G`, fifth force, drift | local kernel silence/screening or retain |
| source normalization operators | measured-`GM`, `Gdot/G`, `delta_G` ambiguity | derive `G_eff/M_eff` map or score residuals |

This is the modified-gravity ledger.

It is what stops the theory from making the classic mistake:

```text
we wrote something conserved, therefore it must be GR.
```

No.

Conserved non-EH operators exist.

They must be forbidden, derived away, or bounded.

## 5. Coefficient To Observable Map

The residual coefficients now map into the local runner:

| Coefficient family | Observable rows | Current status |
|---|---|---|
| `c_R2_or_fR` | `gamma`, `beta`, fifth-force/Yukawa | gamma/beta ready; fifth-force parameterized |
| `c_Ricci_or_c_Weyl` | `gamma`, `xi`, lensing slip | gamma/xi ready; wave sector not in this runner |
| `c_scalar_class_phiC` | clock, gamma, fifth force, WEP if species-specific | clock/gamma/WEP ready; fifth force parameterized |
| `c_vector_marker` | `alpha1`, `alpha2`, `alpha3`, `xi` | preferred-frame/xi source-locked, coefficients missing |
| `c_torsion_nonmetricity` | WEP, clock, nonmetric light, spin | WEP/clock ready; other channels not separately locked here |
| `c_nonlocal_memory` | `Gdot/G`, fifth force, secular drift, local-cosmology leakage | `Gdot/G` contingent; fifth force parameterized |
| `c_source_norm` | `delta_G`, `Gdot/G`, Newtonian limit | source normalization open |

This is a better local branch than a yes/no argument.

It says:

```text
if EH is not derived, here is where every leftover operator lands observationally.
```

## 6. Source-Bound Join

The current source-bound join is:

| Residual | Source-lock status | Operator sources |
|---|---|---|
| `gamma_minus_1` | `2.3e-5`, ready budget only | higher curvature, shear, scalar-tensor, nonmetric light |
| `beta_minus_1` | `7.8e-5`, ready budget only | higher curvature, radial scalar hair, nonlinear boundary |
| `eta_WEP` | `2.8e-15`, ready budget only | species metric, nonmetricity, direct class response |
| `alpha_clock_redshift` | `3.1e-5`, ready budget only | clock mismatch, `phi_C`, varying constants |
| `alpha1` | `1.0e-4`, ready budget only | vector marker, domain normal, coframe slip |
| `alpha2` | `2.0e-9`, ready budget only | vector marker, anisotropic coframe |
| `alpha3` | `4.0e-20`, contingent | unowned flux, momentum nonconservation |
| `xi` | `4.0e-9`, ready budget only | trace-free boundary shear, external-domain anisotropy |
| `Gdot/G` | `9.6e-15 yr^-1`, contingent | time-varying `G_eff`, memory kernel, source drift |
| fifth-force/Yukawa | `alpha_Y(lambda_Y)`, not one scalar | scalar hair, bulk `X`, `phi_C`, nonlocal kernel |

Everything is still:

```text
budget-only,
coefficient-missing,
or parameterized.
```

Therefore:

```text
no PPN/preferred-frame/fifth-force pass is claimed.
```

## 7. Modified-Gravity Branch Contract

If the parent action does not derive EH directly, the branch must obey this contract:

| Contract item | Required form | Status |
|---|---|---|
| explicit residual action | `S_ext = S_EH + sum_i c_i O_i + boundary/topological` | written |
| coefficient fate | every `c_i` is theorem-zero, bounded, or quarantined | written |
| range/coupling force map | derive `alpha_Y(lambda_Y)` or `a_extra/a_GR` | missing |
| metric compatibility | no independent scalar/vector/torsion/nonmetricity locally, or coefficients bounded | open |
| source normalization | derive `kappa`, `G_eff`, `M_eff`, measured `GM` absorption | open |
| claim policy | no EH/local-GR promotion until all residual operators controlled | enforced |

This gives us an honest fork:

```text
derive EH,
or become a disciplined modified-gravity residual theory.
```

Both are workable research paths.

Only one is local-GR reduction.

## 8. Promotion Rules

| Promotion | Current result | Allowed? |
|---|---|---|
| conditional EH if full stack assumed | already sharpened | yes, conditional only |
| parent EH operator derived | fail | no |
| modified-gravity residuals made testable | pass | internal ledger only |
| PPN/preferred-frame pass | fail | no |
| fifth-force pass | fail | no |
| local GR pass | fail | no |

This is the boxing card:

```text
we did not win the local-GR round.
```

But we did land a clean technical counter:

```text
we now know exactly what non-EH residues have to answer to.
```

That is progress.

## 9. Gate Results

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | all cited source paths exist |
| conditional EH theorem preserved | pass | full 358 sufficiency stack still gives EH |
| parent EH operator derived | fail | metric-only/second-order/no-hair/source-normalization premises open |
| residual operator ledger written | pass | operator families mapped |
| coefficients joined to observables | pass | coefficient families mapped to source rows |
| fifth-force scalar scored | fail | `alpha_Y(lambda_Y)` missing |
| source normalization derived | fail | `kappa/G_eff/M_eff/GM` map open |
| PPN/preferred-frame pass claimed | fail | source locks exist but MTS coefficients missing |
| local GR promoted | fail | EH not parent-derived |
| claim ceiling enforced | pass | no local-GR/PPN claim |

## 10. Decision

Decision:

```text
EH_not_parent_derived_residual_operator_ledger_written_modified_gravity_coefficients_retained_no_local_GR_pass
```

Meaning:

```text
EH follows only conditionally if the whole sufficiency stack is assumed.
```

But in the actual branch:

```text
metric-only exterior,
second-order operator selection,
local no-hair,
source normalization,
and universal coupling
are not all parent-derived.
```

Therefore:

```text
non-EH operator families remain as explicit modified-gravity residuals.
```

No promotion:

```text
EH not derived,
PPN not passed,
preferred-frame not passed,
fifth-force not passed,
local GR not derived.
```

## 11. Next Target

Next:

```text
376 - Preferred-Frame Coefficient Map Or Vector No-Hair Theorem
```

Aim:

```text
derive vector/marker/domain no-hair,
or map `B_0i` / coframe-vector leakage into `alpha1`, `alpha2`, `alpha3`, and `xi`.
```

Pass condition:

```text
preferred-frame coefficients are theorem-zero,
or budgeted against the source-locked preferred-frame rows.
```

Why this next:

```text
after 374, preferred-frame and xi are no longer vague quarantines.
```

They are loaded local target rows.

So either:

```text
the parent theory kills the vector/marker sector,
```

or:

```text
the branch owes explicit alpha_i coefficients.
```
