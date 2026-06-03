# 377 - Fifth-Force Range Coupling Map

Private fifth-force/local-bound checkpoint. This is not a public fifth-force, PPN, WEP, Einstein-Hilbert, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 374 made the fifth-force problem honest:

```text
delta_G_or_fifth_force is not one scalar number.
```

Checkpoint 376 then cleaned up the preferred-frame fog.

So the remaining foggiest local row is:

```text
delta_G_or_fifth_force_yukawa.
```

This checkpoint asks:

```text
can MTS derive alpha_Y(lambda_Y),
or another source-normalized force residual?
```

Answer:

```text
not yet.
```

But the contract is now exact:

```text
either theorem-zero,
or universal monopole absorbed by a source-normalization theorem,
or range/coupling derived and scored,
or explicitly unscored.
```

Current status:

```text
range/coupling contract written,
alpha_Y(lambda_Y) not parent-derived,
fifth-force row remains parameterized and unscored.
```

This is not a retreat.

It is moving the monster from fog into a labelled cage.

## 2. Machine Artifact

Script:

```text
scripts/fifth_force_range_coupling_map.py
```

Run:

```text
runs/20260602-001500-fifth-force-range-coupling-map
```

Outputs:

```text
results/source_register.csv
results/force_law_contract.csv
results/MTS_channel_force_map.csv
results/scoring_decision_tree.csv
results/absorption_tests.csv
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
fifth_force_range_coupling_contract_written_alphaY_lambdaY_not_parent_derived_row_remains_parameterized_unscored
```

Claim ceiling:

```text
fifth_force_range_coupling_map_only_no_fifth_force_PPN_EH_WEP_or_local_GR_pass
```

Source paths missing:

```text
0
```

## 3. Force-Law Contract

The standard scoring object is:

```text
V(r) = -G m1 m2 / r * [1 + alpha_Y exp(-r/lambda_Y)].
```

The corresponding acceleration residual is:

```text
a_extra/a_GR = alpha_Y (1 + r/lambda_Y) exp(-r/lambda_Y).
```

Therefore MTS must derive:

```text
alpha_Y,
lambda_Y,
source coupling,
screening/composition,
and source normalization.
```

A gradient proxy alone is not enough.

For the class metric:

```text
a_phi/a_GR ~= 0.5 |grad phi_C| / |grad U_GR|.
```

This becomes a Yukawa-like score only if MTS derives something like:

```text
phi_C(r) = 2 alpha_phi U_GR(r) exp(-r/lambda_phi).
```

Then:

```text
a_phi/a_GR ~= alpha_phi (1 + r/lambda_phi) exp(-r/lambda_phi).
```

Only then can one say:

```text
alpha_Y = alpha_phi,
lambda_Y = lambda_phi.
```

That profile has not been parent-derived.

## 4. MTS Channel Map

| MTS channel | Candidate profile | Needs | Current status |
|---|---|---|---|
| common-mode `phi_C` gradient | `phi_C = 2 alpha_phi U_GR exp(-r/lambda_phi)` | `alpha_phi`, `lambda_phi`, source law | profile not derived |
| bulk `X` scalar/auxiliary | `(-Delta + m_X^2)X = q_X rho_source` | `m_X`, `q_X`, source charge | operator/sign/source missing |
| radial boundary hair | `B_rad = A_B exp(-r/L_B)/r` | `A_B`, `L_B`, universality | no radial no-hair theorem |
| nonlocal memory kernel | spectral superposition of Yukawa modes | kernel spectrum and weights | not locally derived |
| class-changing domain wall | surface/transition force | wall thickness, tension, event law | not Yukawa |
| species-specific class response | composition-dependent mediator | range law plus `Delta F_AB` | WEP closure active |

This is useful because it prevents one sloppy move:

```text
fifth force = 0 because local phi_C should be small.
```

No.

Either:

```text
grad(phi_C)=0 by theorem,
```

or:

```text
derive the force profile and score it.
```

## 5. Scoring Decision Tree

The fifth-force row now obeys:

| Condition | Decision |
|---|---|
| `grad(phi_C)=0` and no bulk/radial/nonlocal channel | theorem-zero, conditional until parent-derived |
| only universal constant monopole survives | absorb into measured `GM` only if source-normalization theorem holds |
| single finite-range scalar profile derived | score against `alpha_Y(lambda_Y)` source curve |
| nonlocal/multi-range kernel derived | score as spectral force kernel, not one Yukawa point |
| domain-wall/class-transition force derived | score as transition stress/surface force, not Yukawa |
| range/coupling missing | remain parameterized and unscored |

Current branch lands in the last row:

```text
range/coupling missing.
```

So:

```text
fifth-force row remains active debt.
```

## 6. GM Absorption Tests

Some fifth-force-looking terms can be harmless if they are just measured mass normalization.

But absorption into `GM` requires all of:

| Test | Required | If failed |
|---|---|---|
| universal | same response for all matter/clocks | WEP/composition force |
| constant/unresolved range | indistinguishable from `GM` rescaling | range-dependent fifth force |
| time-independent | no secular `G_eff` or `M_eff` drift | `Gdot/G` row active |
| source-normalized | parent fixes `kappa`, `G_eff`, `M_eff`, measured `GM` | `delta_G` ambiguity |
| Ward-owned | monopole conserved and flux-balanced | beta/alpha3/secular drift |

These are not details.

They are the difference between:

```text
safe mass renormalization
```

and:

```text
hidden fifth force.
```

The next checkpoint should attack this directly.

## 7. Runner Update

| Runner row | After 377 | Claim status |
|---|---|---|
| `delta_G_or_fifth_force_yukawa` | force-law contract written; `alpha_Y(lambda_Y)` required | unscored |
| common-mode `phi_C` force proxy | maps to Yukawa only if `phi_C(r)` profile derived | conditional/unscored |
| bulk `X` scalar force | requires `m_X`, `q_X`, source charge | unscored |
| radial boundary hair | requires `A_B`, `L_B`, universality | unscored |
| universal monopole `delta_G` | requires source-normalization / `GM` absorption theorem | next target |

This is the compact result:

```text
the fifth-force row is no longer vague,
but it is still not passed.
```

## 8. Failure Modes

The traps are now explicit:

| Failure | Consequence |
|---|---|
| one-number fifth-force bound | fake precision; wrong range comparison |
| treating `r_grad` as `alpha_Y` | invalid score without radial profile |
| absorbing `GM` without source theorem | hides `delta_G`, `Gdot`, WEP, or beta residuals |
| double-counting composition force | confused WEP/fifth-force accounting |
| calling domain-wall force Yukawa | wrong source geometry |

This matters because the local branch is trying to reduce to GR.

If we cheat the fifth-force row, the local-GR claim becomes decorative.

## 9. Gate Results

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | all cited source paths exist |
| Yukawa force-law contract written | pass | `V(r)` and `a_extra/a_GR` relation written |
| MTS channels mapped to range/coupling | pass | six channels mapped |
| `phi_C` proxy limited | pass | not treated as `alpha_Y` without profile |
| `GM` absorption tests written | pass | universality/range/time/source/Ward tests recorded |
| `alpha_Y(lambda_Y)` parent-derived | fail | no channel has derived range and coupling |
| fifth-force scalar scored | fail | row remains parameterized/unscored |
| local-GR or PPN pass claimed | fail | force-law contract only |
| claim ceiling enforced | pass | no fifth-force/local-GR claim |

## 10. Decision

Decision:

```text
fifth_force_range_coupling_contract_written_alphaY_lambdaY_not_parent_derived_row_remains_parameterized_unscored
```

Meaning:

```text
the fifth-force row now has the right mathematical contract,
but MTS has not derived the required range/coupling law.
```

Therefore:

```text
delta_G_or_fifth_force_yukawa
remains active,
parameterized,
and unscored.
```

No promotion:

```text
fifth-force not passed,
PPN not passed,
EH not derived,
local GR not derived.
```

## 11. Next Target

Next:

```text
378 - Source Normalization Geff Meff GM Absorption Theorem
```

Aim:

```text
derive kappa,
G_eff,
M_eff,
and measured-GM absorption,
or keep delta_G/Gdot rows active.
```

Pass condition:

```text
Newtonian source normalization is parent-derived,
or source-bounded.
```

Why this next:

```text
the only safe way for a universal monopole residual to disappear
is measured-GM absorption.
```

That needs a theorem.
