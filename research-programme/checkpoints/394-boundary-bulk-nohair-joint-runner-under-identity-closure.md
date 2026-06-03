# 394 - Boundary/Bulk No-Hair Joint Runner Under Identity Closure

Private boundary/bulk/local-GR checkpoint. This is not a public boundary no-hair, bulk-field, fifth-force, PPN, source-normalization, Einstein-Hilbert, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 393 exposed the Newtonian source-normalization contract:

```text
mu_obs = G_eff M_eff + mu_extra.
```

This checkpoint asks whether `mu_extra` from boundary and bulk sectors can be killed, owned, or honestly retained:

```text
q_BX^nu := P_loc[n_mu B^{mu nu} + F_X^nu + F_boundary^nu].
```

For local GR, this joint force/flux vector must be:

```text
zero,
pure gauge,
constant universal monopole,
Ward-owned exchange,
or explicitly retained as a source-budgeted residual.
```

Current result:

```text
conditional kill switches exist,
but boundary/bulk no-hair is not parent-derived.
```

## 2. Run Manifest

Script:

```text
scripts/boundary_bulk_nohair_joint_runner_under_identity_closure.py
```

Expected run directory:

```text
runs/<timestamp>-boundary-bulk-nohair-joint-runner-under-identity-closure
```

Expected result files:

```text
results/source_register.csv
results/joint_Ward_flux_contract.csv
results/boundary_bulk_channel_ledger.csv
results/joint_nohair_mechanisms.csv
results/joint_residual_amplitude_laws.csv
results/runner_policy_rows.csv
results/no_go_results.csv
results/gate_policy.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

## 3. Joint Ward/Flux Contract

The boundary and bulk channels cannot be treated as separate loopholes. They enter the same local conservation/source problem:

```text
q_BX^nu
  =
  P_loc[
    n_mu B^{mu nu}
    + F_X^nu
    + F_boundary^nu
  ].
```

The local-GR branch needs:

```text
q_BX^nu = 0
```

or a controlled safe substitute:

```text
q_BX^nu = pure gauge,
q_BX^nu = constant universal monopole only,
q_BX^nu + q_owned^nu = 0 by total Ward identity,
or q_BX^nu is retained and source-budgeted.
```

Anything else feeds local residual rows.

## 4. Boundary Channels

| Channel | Safe condition | Current status | Rows |
|---|---|---:|---|
| `B_TF` trace-free shear | class-only boundary action forbids angular reps | not parent-derived | `gamma`, `xi`, slip |
| `B_0i` vector boundary | no marker, normal, vector frame, or patch label | not parent-derived | `alpha1`, `alpha2`, `alpha3` |
| `B_rad` radial trace | only constant universal monopole survives | not parent-derived | `beta`, `delta_G`, fifth force |
| `B_flux` unowned flux | total Ward-owned boundary current | mapped, not proved | `alpha3`, `Gdot/G`, `beta` |
| `B_mono` constant monopole | calibrated universal measured-`GM` rescaling | conditional only | safe only if 393 gates pass |

The useful theorem fragment from checkpoint 379 is:

```text
S_boundary = S_boundary(Q_rel, M_eff, V_scalar, I_top)
  => delta S_boundary/delta B_TF = 0
  => delta S_boundary/delta B_0i = 0.
```

But this requires the parent action to forbid angular/vector boundary data. It does not kill radial hair or flux by itself.

## 5. Bulk-X Channels

| Channel | Safe condition | Current status | Rows |
|---|---|---:|---|
| source-free massive `X` | `(-Delta+m_X^2)X=0`, `m_X^2>0`, regular decaying data | conditional only | none if theorem-zero |
| sourced Yukawa `X` | derive `alpha_X(lambda_X)` and source/test charge | missing | fifth force, WEP-source |
| boundary-resourced `X` | boundary does not resource `X`, or flux is Ward-owned | open | fifth force, `beta`, `Gdot/G`, `alpha3` |
| nonlocal/spectral `X` | kernel silence/screening spectrum derived | unscored | scale-dependent `delta_G`, fifth force |

The useful theorem fragment from checkpoint 380 is:

```text
(-Delta + m_X^2)X = 0,
m_X^2 > 0,
regular decaying boundary data,
no exterior source
  => X = 0.
```

But with a source:

```text
(-Delta + m_X^2)X = q_X rho_source
  => X(r) = Q_X exp(-r/lambda_X)/(4 pi r),
  => a_X/a_GR = alpha_X(1+r/lambda_X)exp(-r/lambda_X).
```

`alpha_X(lambda_X)` is not derived, so this remains unscored.

## 6. Joint Residual Amplitude Laws

| Row | Amplitude law | Current policy |
|---|---|---|
| `gamma-1` | `c_TF eps_B_TF + c_rad eps_B_rad + c_X eps_bulk_X + c_slip eps_nonEH` | retained budget-only |
| `beta-1` | `c_rad eps_B_rad + c_flux eps_B_flux + c_X2 eps_bulk_X^2 + c_SN beta_SN` | retained budget-only |
| `alpha1/alpha2` | `c_vec eps_B0i + c_marker eps_marker + c_domain eps_domain` | retained budget-only |
| `alpha3` | `c_flux eps_B_flux + c_Xflux eps_X_flux` | contingent budget-only |
| `xi` | `c_xi eps_B_TF_l>=2 + c_domain eps_external_domain` | retained budget-only |
| fifth force | `alpha_X(lambda_X)` / `alpha_B(lambda_B)` Yukawa plus radial boundary gradient | parameterized unscored |
| `Gdot/G` | `partial_t ln[GM + mu_extra_BX]` | contingent budget-only |
| WEP-source | `Delta_A ln[mu_obs_A] + Delta_A q_X/q_m` | direct coframe closed; source charge open |

This is the honest shape of the problem. If boundary or bulk hair survives, it must be either derived harmless or carried into these rows.

## 7. Mechanism Verdicts

| Mechanism | Helps with | Does not solve | Verdict |
|---|---|---|---:|
| class-only boundary | angular/vector boundary sources | radial hair, flux, bulk `X` | conditional only |
| positive source-free bulk mass gap | regular decaying source-free `X` | sourced/boundary-resourced/nonlocal `X` | conditional only |
| constant universal monopole | measured-`GM` absorption | radial/time/species/range dependence | conditional only |
| Ward-owned flux | fake Bianchi/source drift | unowned flux | mapped, not closed |
| source-budget exit | honest testability | theorem-zero | available fallback |

## 8. Runner Policy

| Runner row | State after 394 |
|---|---|
| boundary no-hair | conditional only |
| bulk-X no-hair | conditional only |
| constant monopole absorption | conditional only |
| fifth force | retained, parameterized, unscored |
| preferred-frame and `xi` | retained budget-only |
| source normalization | retained |
| local-GR reduction | fail promotion |

So this is progress, but not a local-GR pass. We have caged the monsters; we have not killed them.

## 9. No-Go Results

| No-go | Consequence |
|---|---|
| class-only boundary is not full boundary no-hair | `eps_B_rad` and `eps_B_flux` remain |
| bulk mass gap needs source-free conditions | bulk-X residual remains unless every premise is derived |
| `GM` absorption cannot hide flux | `alpha3`, `Gdot/G`, `beta`, source rows stay active |
| fifth force needs range and coupling | no scalar fifth-force score without `alpha(lambda)` |
| identity closure is not source-charge universality | WEP-source/composition guards remain |

## 10. Gate Results

| Gate | Status | Evidence |
|---|---:|---|
| source paths exist | pass | all cited source paths exist |
| joint boundary/bulk contract written | pass | `q_BX^nu` contract and residual ledger written |
| boundary no-hair parent-derived | fail | class-only/no-marker/radial/flux premises open |
| bulk-X no-hair parent-derived | fail | positive source-free mass-gap and harmless boundary data not derived |
| joint Ward flux owned | fail | boundary/bulk flux mapped, not owned |
| fifth force scored | fail | `alpha_X(lambda_X)` or `alpha_B(lambda_B)` missing |
| residual runner rows retained | pass | observable amplitude rows retained |
| local-GR/PPN promoted | fail | conditional only |
| claim ceiling enforced | pass | no boundary/bulk/PPN/fifth-force/source/local-GR pass |

## 11. Decision

Decision:

```text
boundary_bulk_nohair_joint_runner_under_identity_written_conditional_kill_switches_not_parent_derived_boundary_bulk_residuals_retained_no_local_GR_pass
```

Interpretation:

```text
Boundary and bulk residues now sit in one joint runner.
Class-only boundary dependence is a useful conditional kill switch.
Positive source-free bulk-X mass gap is a useful conditional kill switch.
Neither is parent-derived.
Constant universal monopole absorption is allowed only if source-normalization gates pass.
Radial hair, unowned flux, sourced X, boundary-resourced X,
nonlocal kernels, and source-charge dependence remain retained residuals.
```

Claim ceiling:

```text
boundary_bulk_nohair_joint_runner_under_identity_only_no_boundary_bulk_PPN_fifth_force_source_or_local_GR_pass
```

## 12. Next Target

395 - Preferred-Frame/Domain No-Hair Under Identity Closure

Task:

```text
derive or budget preferred-frame/domain/projector residues after identity and boundary-bulk gates.
```

Pass condition:

```text
alpha1, alpha2, alpha3, and xi are theorem-zero,
pure gauge,
source-budgeted,
or coefficient-mapped.
```
