# 376 - Preferred-Frame Coefficient Map Or Vector No-Hair Theorem

Private preferred-frame/local-GR checkpoint. This is not a public PPN, preferred-frame, WEP, fifth-force, Einstein-Hilbert, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 374 source-locked the preferred-frame and preferred-location rows:

```text
alpha1,
alpha2,
alpha3,
xi.
```

Checkpoint 375 then made the operator issue honest:

```text
vector/preferred-frame operators must be no-haired or coefficient-mapped.
```

This checkpoint asks:

```text
can the parent branch derive vector no-hair,
or must alpha_i / xi coefficients stay active?
```

Answer:

```text
vector no-hair has a clean conditional theorem shape,
but it is not parent-derived.
```

Therefore:

```text
alpha1, alpha2, alpha3, xi, and contingent Gdot/G
remain budget-only coefficient rows.
```

No preferred-frame pass.

No local-GR promotion.

The vector goblin is caged.

It is not slain.

## 2. Machine Artifact

Script:

```text
scripts/preferred_frame_coefficient_map_or_vector_nohair_theorem.py
```

Run:

```text
runs/20260602-000500-preferred-frame-coefficient-map-or-vector-nohair-theorem
```

Outputs:

```text
results/source_register.csv
results/vector_nohair_premises.csv
results/vector_nohair_attempt_steps.csv
results/preferred_frame_coefficient_map.csv
results/epsilon_channels.csv
results/runner_update.csv
results/failure_modes.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

Status:

```text
vector_nohair_conditional_not_parent_derived_preferred_frame_coefficients_mapped_budget_only_no_PPN_pass
```

Claim ceiling:

```text
preferred_frame_coefficient_map_only_no_vector_nohair_PPN_EH_fifth_force_WEP_or_local_GR_pass
```

Source paths missing:

```text
0
```

## 3. Conditional Vector No-Hair Shape

The clean theorem target is:

```text
if marker/domain/projector vectors are gauge,
and the boundary action is class-only,
and any surviving vector obeys a source-free regular exterior equation,
and boundary/domain flux is Ward-owned,
then preferred-frame vector hair vanishes.
```

In symbols, the dangerous vector sector is:

```text
V_vec = {B_0i, u_MTS^i, n_D^i, P_vector^i, flux^i, coframe_slip^i}.
```

The desired no-hair result is:

```text
B_0i = 0,
u_MTS^i = 0,
n_D^i = gauge/bookkeeping only,
P_vector^i = gauge/topological only,
flux^i = Ward-owned,
coframe_slip^i = 0.
```

If that holds:

```text
alpha1 = alpha2 = alpha3 = 0
```

up to the normal GR source motion.

But this is not currently parent-derived.

## 4. Premise Audit

| Premise | Would kill | Current status |
|---|---|---|
| no physical marker vector | marker/projector vector leakage | not parent-derived |
| class-only boundary action | `B_0i` and l=1 vector hair | conditional template |
| covariant domain selector | domain preferred-frame and anisotropy | open |
| regular source-free vector equation | propagating vector preferred-frame mode | operator not derived |
| Ward-owned flux | `alpha3`, `Gdot/G`, secular drift | mapped, not proved |
| single observed coframe | coframe vector matter mismatch | closure axiom required |

So the theorem shape is good.

The derivation status is not.

That means the branch is not allowed to say:

```text
covariance kills preferred frames.
```

Covariance does not by itself kill a physical vector, marker field, domain normal, or aether-like coframe slip.

Those must be absent by parent action, pure gauge, constrained, or bounded.

## 5. Coefficient Map

When no-hair is not derived, the runner must carry:

| Residual | Source lock | Symbolic map | Equal-share ceiling |
|---|---:|---|---:|
| `alpha1` | `1.0e-4` | `C1B eps_B0i + C1D eps_domain_vec + C1P eps_P_vector + C1e eps_coframe_slip` | `2.5e-5` |
| `alpha1` stricter context | `4.0e-5` | same map | `1.0e-5` |
| `alpha2` | `2.0e-9` | `C2B eps_B0i + C2D eps_domain_vec + C2A eps_anisotropic_coframe + C2P eps_P_vector` | `5.0e-10` |
| `alpha3` | `4.0e-20` | `C3F eps_unowned_flux + C3M eps_momentum_nonconserve + C3V eps_vector_frame` | `1.33e-20` |
| `xi` | `4.0e-9` | `CxiTF eps_TF_lge2 + CxiExt eps_external_domain_aniso + CxiD eps_domain_aniso + CxiW eps_Weyl2` | `1.0e-9` |
| `Gdot/G` | `9.6e-15 yr^-1` | `CGk eps_kappa_dot + CGM eps_Meff_dot + CGK eps_memory_kernel_drift` | `3.2e-15 yr^-1` |

These equal-share ceilings are not physics constants.

They are engineering guardrails:

```text
if there are N unknown unit-scale terms,
each term must fit under target/N.
```

The useful bit is that the rows are now loaded and explicit.

The grim bit is that the MTS coefficients are still missing.

## 6. Epsilon Channels

The active preferred-frame channels are:

| Epsilon | Meaning | Observable rows | Current status |
|---|---|---|---|
| `eps_B0i` | boundary vector component surviving locally | `alpha1`, `alpha2` | not zero-derived |
| `eps_domain_vec` | domain selector carries preferred local velocity/frame | `alpha1`, `alpha2`, `xi` | not zero-derived |
| `eps_P_vector` | projector/relative-chain vector representative leaks | `alpha1`, `alpha2` | conditional only |
| `eps_coframe_slip` | observed coframe has vector offset | `alpha1`, clock, WEP | closure axiom required |
| `eps_unowned_flux` | momentum flux not Ward-balanced | `alpha3`, `Gdot/G`, secular drift | Ward ownership open |
| `eps_TF_lge2` | trace-free l>=2 boundary shear | `xi`, gamma, lensing slip | not zero-derived |
| `eps_external_domain_aniso` | external-domain preferred-location anisotropy | `xi` | not zero-derived |

This is where the next derivation attempts must bite.

Especially:

```text
eps_B0i,
eps_domain_vec,
eps_unowned_flux.
```

Those are the local preferred-frame teeth.

## 7. What This Does And Does Not Prove

It proves:

```text
the preferred-frame problem is now finite and source-locked.
```

It does not prove:

```text
preferred-frame safety.
```

The exact no-hair theorem would need:

```text
parent gauge status of marker/domain/projector vectors,
class-only boundary action,
source-free regular vector equation,
Ward-owned flux,
single observed coframe.
```

Those are still theorem targets.

So the status is:

```text
coefficient map written,
no-hair not parent-derived,
budget-only no pass.
```

## 8. Failure Modes

The main traps are:

| Failure | Consequence |
|---|---|
| assuming covariance kills vector hair | false `alpha1/alpha2` pass |
| applying `alpha3` unconditionally | unfair penalty if no such channel exists |
| folding `xi` into `gamma` only | hides preferred-location anisotropy |
| hiding coframe slip inside WEP | reopens clock/WEP/preferred-frame channels |
| erasing flux without Ward ownership | fake Bianchi closure |

This is why the checkpoint keeps both:

```text
conditional theorem shape
```

and:

```text
active coefficient rows.
```

## 9. Gate Results

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | all cited source paths exist |
| source-locked preferred-frame rows loaded | pass | `alpha1`, `alpha2`, `alpha3`, `xi`, contingent `Gdot/G` imported |
| vector no-hair conditional theorem written | conditional pass | premise stack written |
| parent vector no-hair derived | fail | marker/domain/projector gauge status and vector equation open |
| preferred-frame coefficient map written | pass | five residual maps written |
| equal-share budgets written | pass | target/N ceilings recorded |
| PPN or preferred-frame pass claimed | fail | MTS coefficients missing |
| local GR promoted | fail | vector, EH, source, WEP, fifth-force gates open |
| claim ceiling enforced | pass | no PPN/local-GR claim |

## 10. Decision

Decision:

```text
vector_nohair_conditional_not_parent_derived_preferred_frame_coefficients_mapped_budget_only_no_PPN_pass
```

Meaning:

```text
vector no-hair is a sharp theorem target,
but not a completed parent theorem.
```

Therefore:

```text
alpha1,
alpha2,
alpha3,
xi,
and contingent Gdot/G
stay active as budget-only rows.
```

No promotion:

```text
preferred-frame not passed,
PPN not passed,
EH not derived,
local GR not derived.
```

## 11. Next Target

Next:

```text
377 - Fifth-Force Range Coupling Map
```

Aim:

```text
derive alpha_Y(lambda_Y),
or another source-normalized force residual,
for scalar/bulk/phi_C/nonlocal fifth-force channels.
```

Pass condition:

```text
fifth-force row becomes scalar/range scorable,
or remains explicitly unscored.
```

Why this next:

```text
after 376, preferred-frame rows are no longer fog.
```

The remaining foggiest local row is:

```text
delta_G_or_fifth_force_yukawa.
```

It needs a range and a coupling.
