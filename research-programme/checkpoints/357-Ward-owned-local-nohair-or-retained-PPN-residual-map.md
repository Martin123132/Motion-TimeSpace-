# 357 - Ward-Owned Local No-Hair Or Retained PPN Residual Map

Private derivation checkpoint. This is not a public local-GR, PPN, WEP, redshift, fifth-force, CMB, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 356 made the conservation problem honest:

```text
nabla_mu(T_matter^munu + kappa^-1 E_MTS^munu)
  + F_X^nu
  + F_P^nu
  + F_boundary^nu
  + F_domain^nu
  + F_matter_nonmetric^nu
  = 0.
```

This checkpoint asks the next unavoidable question:

```text
what happens to each F term locally?
```

Every Ward-force channel now has only three legal fates:

```text
1. vanish by theorem,
2. become boundary-only with no local PPN support,
3. remain as an explicit retained residual.
```

The banned option is:

```text
set it to zero because local GR needs it gone.
```

That is the whole point of this checkpoint.

## 2. Machine Artifact

Script:

```text
scripts/Ward_owned_local_nohair_or_retained_PPN_residual_map.py
```

Run:

```text
runs/20260601-183000-Ward-owned-local-nohair-or-retained-PPN-residual-map
```

Key outputs:

```text
results/source_register.csv
results/force_fate_map.csv
results/nohair_mechanism_candidates.csv
results/retained_residual_vector.csv
results/source_locked_residual_join.csv
results/theorem_or_retain_decisions.csv
results/next_queue.csv
results/gate_results.csv
results/decision.csv
status.json
DONE.txt
```

Status:

```text
Ward_force_channels_mapped_to_nohair_conditions_or_retained_PPN_residuals_no_local_GR_promotion
```

Claim ceiling:

```text
force_channel_map_and_symbolic_bound_contract_only_no_local_GR_no_PPN_pass_no_nohair_theorem
```

Source paths missing:

```text
0
```

## 3. Force Fate Map

| Force | Best theorem-zero route | If still open | Current verdict |
|---|---|---|---|
| `F_X^nu` | positive elliptic/massive local operator with no exterior source | `epsilon_bulk`, `epsilon_rad` | retained until local `X` operator/source terms are derived |
| `F_P^nu` | metric-independent covariant topological `P_D` with owned constraint | `epsilon_TF`, `epsilon_vec`, `epsilon_P_bulk` | conditional bulk-zero only; boundary and parent selection open |
| `F_boundary^nu` | class-only boundary action leaves conserved monopole only | `epsilon_rad`, `epsilon_TF`, `epsilon_vec`, clock/WEP boundary terms | monopole safe condition known; no-hair not derived |
| `F_domain^nu` | covariant/dynamical domain selector with no preferred frame/location | domain vector/anisotropy/`L_cg` gradient residuals | retained and quarantined |
| `F_matter_nonmetric^nu` | universal single metric/coframe matter coupling | `epsilon_clock`, `epsilon_WEP`, nonmetric light/ruler residuals | hard open until universal coupling theorem |

This is progress because each force channel is now either:

```text
a theorem target,
or a residual target.
```

No channel is allowed to be rhetorically erased.

## 4. Candidate No-Hair Mechanisms

The plausible proof routes are now explicit.

| Mechanism | Applies to | Would prove | Current status |
|---|---|---|---|
| maximum-principle mass gap | `F_X^nu` / nonprojector bulk residual | local scalar/bulk residual vanishes or is exponentially screened | candidate, not derived |
| topological relative-chain exactness | `F_P^nu` | no bulk projector force/stress | conditional from N5, parent selection open |
| class-only boundary action | `F_boundary^nu` | only conserved monopole trace survives | not derived |
| covariant domain selector | `F_domain^nu` | no preferred-frame/location force | not derived |
| universal matter coupling | `F_matter_nonmetric^nu` | WEP/clock/nonmetric residuals vanish at action level | not derived |

The most useful new mathematical route is the first one:

```text
(-Delta + m_eff^2) phi = 0,
m_eff^2 > 0,
regular local exterior data,
asymptotic/local boundary decay
  -> phi = 0 or screened.
```

If MTS can derive that form for the local auxiliary/bulk sector, `F_X^nu` becomes controllable.

But right now:

```text
m_eff^2 > 0,
the no-source exterior equation,
and the exact boundary conditions
```

are not derived.

So this is a theorem target, not a theorem.

## 5. Retained PPN Residual Vector

The retained vector now connects the Ward forces to local test sectors.

| Residual | Symbolic formula | Force sources | Source-lock status |
|---|---|---|---|
| `gamma_minus_1` | `C_TF epsilon_TF + C_rad epsilon_rad + C_bulk epsilon_bulk + C_nonmetric epsilon_nonmetric_light` | `F_P`, `F_boundary`, `F_X`, nonmetric matter | source-locked |
| `beta_minus_1` | `C_rad2 epsilon_rad + C_nl epsilon_boundary_nonlinear + C_bulk2 epsilon_bulk` | `F_boundary`, `F_X` | source-locked |
| `eta_WEP` | `C_WEP epsilon_WEP + C_comp epsilon_species_charge + C_boundary epsilon_WEP_boundary` | nonmetric matter, boundary | source-locked |
| `alpha_clock_redshift` | `C_clock epsilon_clock + C_nonmetric epsilon_clock_metric_mismatch` | nonmetric matter, boundary | source-locked |
| `preferred_frame_alpha1_alpha2` | `C_vec epsilon_vec + C_domain epsilon_domain_vec + C_P epsilon_P_vector` | domain, projector, boundary | quarantined |
| `xi_preferred_location_anisotropy` | `C_TF2 epsilon_TF_lge2 + C_domain2 epsilon_domain_aniso + C_ext epsilon_external_aniso` | domain, projector, boundary | quarantined |
| `delta_G_or_fifth_force` | `C_bulkG epsilon_bulk + C_radG epsilon_rad + C_L epsilon_Lcg_grad` | `F_X`, boundary, domain | quarantined |

This is not a numeric PPN pass.

It is the map needed before a meaningful numeric pass.

The source-locked sectors from checkpoint 354 are:

| Residual | Source-locked scale | Use now |
|---|---:|---|
| `gamma_minus_1` | `2.3e-5` | internal numeric guardrail |
| `beta_minus_1` | `7.8e-5` | internal numeric guardrail |
| `eta_WEP` | `2.8e-15` | internal numeric guardrail |
| `alpha_clock_redshift` | `3.1e-5` | internal numeric guardrail |

Quarantined until numeric source-lock:

```text
preferred_frame_alpha1_alpha2,
xi_preferred_location_anisotropy,
delta_G_or_fifth_force.
```

## 6. Theorem-Or-Retain Decision

| Sector | Best case | Current decision | Why |
|---|---|---|---|
| bulk `X` | mass-gap/no-source theorem | retain symbolic residual | local `X` operator and sign/source terms not derived |
| projector bulk | topological `P_D` gives `F_P_bulk=0` | conditional zero, not promotion | parent selection and boundary closure open |
| boundary multipoles | class-only boundary leaves monopole | retain symbolic residual | no class-only/no-angular theorem yet |
| domain preferred frame | covariant domain selector | retain quarantined residual | preferred-frame and `xi` numeric locks still open |
| matter nonmetricity | universal metric/coframe coupling | retain source-locked residual | WEP/clock theorem not derived |

This is grim in a useful way.

It says exactly where the theory bill remains unpaid.

But it is also much better than vague failure:

```text
we now know what must be proven,
and what must be bounded if it cannot be proven.
```

## 7. What Improved

Before this checkpoint, we had:

```text
a Ward-force ledger.
```

Now we have:

```text
a legal fate map for each Ward-force channel,
a candidate no-hair mechanism list,
a retained PPN residual vector,
and source-lock status for each residual.
```

That means the next local-GR work can no longer drift.

It must either:

```text
derive one of the no-hair mechanisms,
or carry the residual into the PPN runner.
```

## 8. What Still Fails

No local-GR promotion follows.

Failures still standing:

```text
local no-hair theorem not proved,
universal matter coupling not derived,
local EH exterior not derived,
PPN residual coefficients not computed,
preferred-frame/anisotropy/fifth-force sectors not source-locked numerically.
```

The most dangerous single open item is:

```text
F_matter_nonmetric^nu
```

because WEP is brutally tight:

```text
eta_WEP ~ 2.8e-15
```

If universal matter coupling is not derived, this branch becomes extremely expensive to keep alive.

The second dangerous item is:

```text
F_boundary^nu trace-free/vector pieces
```

because they feed `gamma`, lensing slip, preferred-frame terms, and anisotropy.

## 9. Gate Results

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | all cited source files exist |
| Ward forces mapped | pass | five force channels mapped to theorem-zero, boundary-only, or retained residual outcomes |
| no-hair mechanisms identified | pass | five candidate mechanisms written with needed equations and failure modes |
| source-locked bounds joined | pass | four numeric ready sectors; three quarantined sectors |
| retained residuals carried | pass | open sectors retained rather than set to zero by assertion |
| local no-hair theorem proved | fail | key parent equations, signs, and couplings are not derived |
| local GR promoted | fail | force channels remain conditional or retained; EH exterior not yet derived |
| PPN pass claimed | fail | numeric comparison runner deferred until residual coefficients/equations exist |
| claim ceiling enforced | pass | no local-GR, PPN, or no-hair claim |

## 10. Decision

Decision:

```text
Ward_force_channels_mapped_to_nohair_conditions_or_retained_PPN_residuals_no_local_GR_promotion
```

Meaning:

```text
The local-GR route is now more derivable and more falsifiable.
Each Ward-force channel either has a named theorem target
or is retained as an explicit residual that must face source-locked bounds.
```

But:

```text
MTS still does not derive local GR.
```

## 11. Next Target

Next:

```text
358 - Local EH Exterior Operator From Ward-Closed Action
```

Pass condition:

```text
assuming the Ward/no-hair channels close as explicit conditions,
derive that the surviving local weak-field operator is Einstein-Hilbert plus Lambda,
with no extra propagating scalar/vector/tensor local mode.
```

Why this is next:

```text
we need to know whether closing the force ledger is sufficient for GR,
or whether an extra operator-level obstruction remains.
```

If it is sufficient, the project has a clean theorem structure:

```text
Ward closure + no-hair + universal coupling
  -> EH exterior
  -> Newton/PPN.
```

If not, the local branch still has a deeper GR-reduction problem.
