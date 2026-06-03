# 393 - Source-Normalized Newtonian Limit Under Identity Closure

Private source-normalization/local-GR checkpoint. This is not a public Newtonian-limit, PPN, Einstein-Hilbert, fifth-force, source-normalization, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 392 made the EH question honest:

```text
identity coframe closure does not select EH by itself.
```

This checkpoint asks the next necessary GR-reduction question:

```text
Even if the exterior is conditionally EH-shaped,
does MTS derive the measured Newtonian source normalization?
```

Short answer:

```text
Not yet.
```

But we can now state the exact contract:

```text
G_eff = kappa_eff c^4/(8 pi)
nabla^2 Phi = 4 pi G_eff rho_eff
mu_obs = G_eff M_eff + mu_extra
```

Only a constant, universal, range-independent `mu_obs` can be absorbed into measured `GM`.

## 2. Run Manifest

Script:

```text
scripts/source_normalized_Newtonian_limit_under_identity_closure.py
```

Expected run directory:

```text
runs/<timestamp>-source-normalized-Newtonian-limit-under-identity-closure
```

Expected result files:

```text
results/source_register.csv
results/weak_field_derivation_steps.csv
results/source_normalization_contract.csv
results/absorption_conditions_under_identity.csv
results/residual_amplitude_laws.csv
results/runner_row_transitions.csv
results/no_go_results.csv
results/gate_policy.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

## 3. Weak-Field Source Algebra

Assume only for this algebra that the conditional EH branch from checkpoint 392 is available:

```text
G_{mu nu} + Lambda g_{mu nu} = kappa_eff T_{mu nu}^{eff}.
```

In the local weak-field, slow-motion limit:

```text
g_00 = -1 - 2 Phi/c^2 + O(c^-4),
T_00^{eff} = rho_eff c^2 + O(c^0),
G_00 = 2 nabla^2 Phi/c^2 + O(c^-4).
```

Therefore:

```text
nabla^2 Phi = (kappa_eff c^4/2) rho_eff
             = 4 pi G_eff rho_eff,
G_eff := kappa_eff c^4/(8 pi).
```

This is the source-normalization hinge. EH-shaped equations are not enough unless `kappa_eff`, `rho_eff`, `M_eff`, and measured `GM` are all fixed.

## 4. Measured GM Contract

Define the observed Kepler parameter:

```text
mu_obs(r,t,A) := r^2 partial_r Phi_A.
```

The MTS source-normalized form is:

```text
mu_obs(r,t,A)
  =
  G_eff(r,t,A) M_eff(r,t)
  + mu_extra(r,t,A).
```

Safe absorption into measured `GM` requires:

```text
partial_r mu_obs = 0,
partial_t mu_obs = 0,
partial_A mu_obs = 0,
mu_extra(r,lambda) = 0 or constant universal.
```

If all of that holds:

```text
mu_obs = GM_measured
```

and a constant universal normalization disappears into the measured source. If any condition fails, it is not calibration. It is a residual.

## 5. Source-Normalization Contract

| Contract item | Required form | Current status |
|---|---|---|
| `kappa -> G_eff` | `G_eff = kappa_eff c^4/(8 pi)` | conditional EH branch only |
| `Pi_M J -> M_eff` | parent-fixed physical source charge | flux conditional, calibration open |
| radial conservation | `partial_r M_eff = 0` | conditional from 244 |
| time constancy | `partial_t ln(G_eff M_eff)=0` | not parent-derived |
| species universality | same source normalization for all matter/clocks/compositions | direct coframe closed only |
| range independence | no finite-range `mu_extra`, or derive `alpha(lambda)` | not derived |
| Ward-owned flux | boundary/bulk/projector/domain flux owned | mapped, not closed |

## 6. Residual Amplitude Laws

The important residuals are now explicit:

| Channel | Amplitude law | Observable row |
|---|---|---|
| source normalization | `delta_mu/mu = delta G_eff/G_eff + delta M_eff/M_eff + mu_extra/(G_eff M_eff)` | `delta_G`, fifth force |
| radial source hair | `partial_r ln mu_obs` | fifth force, `beta-1`, `delta_G` |
| time drift | `Gdot_obs/G_obs = partial_t ln(G_eff M_eff)` | `Gdot/G` |
| finite-range force | `a_extra/a_GR = alpha(lambda)(1+r/lambda)exp(-r/lambda)` | fifth force |
| source-normalization beta | `beta_SN ~ d ln(G_eff M_eff)/d(U/c^2)` plus nonlinear hair | `beta-1` |
| species source charge | `eta_SN ~ Delta_A ln mu_obs` | WEP/composition force |

These are not decorative. They are the exact exits that stop the branch from pretending it has reduced to Newton.

## 7. Under Identity Closure

Identity closure helps here, but only on one side:

```text
matter geometry side:
  ehat = e
  direct nonmetric matter pullback closed by label
```

It does not automatically prove:

```text
source charge universality,
G_eff constancy,
M_eff calibration,
no boundary/bulk flux,
no finite-range extra force.
```

So the WEP/coframe side is cleaner, but the source side is still alive.

## 8. Runner Transitions

| Row | State after 393 | Reason |
|---|---|---|
| Newtonian limit | conditional theorem, not promoted | algebra written, parent calibration open |
| `delta_G` / fifth force | retained, unscored/parameterized | range or constant-monopole theorem missing |
| `Gdot/G` | retained contingent budget | no time-constancy theorem |
| `beta-1` | retained budget-only | nonlinear source-hair coefficient missing |
| `eta_WEP` | direct coframe closure only | source-charge universality still open |
| `gamma-1` | unchanged retained | source normalization does not close operator/boundary/bulk slip |

## 9. No-Go Results

| No-go | Consequence |
|---|---|
| EH shape is not Newtonian source normalization | no Newtonian pass from EH shape alone |
| `M_eff` conservation is not `GM` absorption | `delta_G/Gdot/fifth-force` rows remain |
| identity coframe is not source-charge universality | WEP closes only on direct geometry side |
| constant monopole is the only safe absorption case | radial/time/species/range pieces must be retained |
| source normalization cannot hide boundary/bulk flux | boundary/bulk no-hair remains next target |

## 10. Gate Results

| Gate | Status | Evidence |
|---|---:|---|
| source paths exist | pass | all cited source paths exist |
| conditional Newtonian algebra written | pass | `kappa_eff -> G_eff -> Poisson -> mu_obs` recorded |
| `M_eff` flux conservation imported | conditional pass | checkpoint 244, under closed `Pi_M` flux premises |
| `kappa -> G_eff` parent-calibrated | fail | only conditional EH branch |
| measured-`GM` absorption parent-derived | fail | constant universal `G_eff M_eff = GM_measured` not derived |
| range/time/species independence derived | fail | all exits remain open |
| `delta_G/Gdot/fifth-force` rows retained | pass | no hidden promotion |
| Newtonian/local-GR promoted | fail | conditional only |
| claim ceiling enforced | pass | no Newton/PPN/EH/source/fifth-force/local-GR pass |

## 11. Decision

Decision:

```text
source_normalized_Newtonian_limit_under_identity_attempt_written_constant_GM_absorption_conditional_not_parent_derived_deltaG_Gdot_fifth_force_rows_retained_no_local_GR_pass
```

Interpretation:

```text
The weak-field source-normalization algebra is now explicit.
If the EH branch is assumed,
  G_eff = kappa_eff c^4/(8 pi)
  and mu_obs = G_eff M_eff + mu_extra.
Only constant universal mu_obs can be absorbed into measured GM.
MTS has not yet derived:
  kappa calibration,
  G_eff constancy,
  M_eff calibration,
  source-charge universality,
  no finite-range residue,
  Ward-owned boundary/bulk flux.
Therefore Newtonian reduction is conditional only.
```

Claim ceiling:

```text
source_normalized_Newtonian_limit_under_identity_only_no_Newton_PPN_EH_source_fifth_force_or_local_GR_pass
```

## 12. Next Target

394 - Boundary/Bulk No-Hair Joint Runner Under Identity Closure

Task:

```text
derive or budget boundary and bulk Ward-owned flux/no-hair under identity closure.
```

Pass condition:

```text
boundary/bulk flux is theorem-zero, pure gauge, constant monopole,
source-budgeted, or explicitly retained.
```
