# 380 - Bulk-X Mass-Gap Source-Normalized Force Law

Private local-GR/fifth-force checkpoint. This is not a public bulk-field, fifth-force, PPN, WEP, Einstein-Hilbert, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 379 left the boundary sector honest:

```text
boundary hair is retained unless class-only / Ward-owned restrictions are parent-derived.
```

The other local force monster is:

```text
bulk X.
```

Checkpoint 357 already named the possible route:

```text
positive massive source-free local operator
  -> no bulk hair or screened bulk hair.
```

Checkpoint 377 then said a fifth-force score needs:

```text
alpha_X(lambda_X).
```

This checkpoint asks:

```text
can we derive the bulk-X mass gap and source-normalized force law?
```

Answer:

```text
not yet.
```

But the contract is now sharp:

```text
bulk X must be theorem-zero,
Yukawa-scored with derived m_X and q_X,
or explicitly retained as an unscored residual.
```

Current status:

```text
mass-gap / force-law contract written,
alpha_X(lambda_X) not parent-derived,
bulk-X residual retained.
```

So the ghost is not dead.

But it is now wearing a name tag.

## 2. Machine Artifact

Script:

```text
scripts/bulk_X_mass_gap_source_normalized_force_law.py
```

Run:

```text
runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law
```

Outputs:

```text
results/source_register.csv
results/bulk_X_operator_routes.csv
results/mass_gap_conditions.csv
results/nohair_steps.csv
results/source_normalized_force_law.csv
results/observable_impact_map.csv
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
bulk_X_mass_gap_and_source_normalized_force_law_not_parent_derived_alphaX_lambdaX_missing_residual_retained
```

Claim ceiling:

```text
bulk_X_force_law_contract_only_no_fifth_force_PPN_EH_WEP_or_local_GR_pass
```

Source paths missing:

```text
0
```

## 3. Bulk-X Operator Routes

The possible local fates of `X` are now split:

| Route | Equation | Verdict |
|---|---|---|
| source-free massive no-hair | `(-Delta + m_X^2) X = 0`, `m_X^2 > 0` | conditional theorem target |
| source-normalized Yukawa | `(-Delta + m_X^2) X = q_X rho_source` | force-law contract only |
| first-order constraint `X` | `S_X = int sqrt(-g)[P nabla X + J_eff X] + S_boundary` | rank-zero route, not mass gap |
| massless `X` | `-Delta X = q_X rho_source` | long-range danger unless charge/gauge vanishes |
| tachyonic/wrong-sign `X` | `(-Delta - |m_X|^2)X = q_X rho_source` | reject for local-GR branch |
| nonlocal/spectral `X` | superposition of Yukawa kernels | modified-gravity residual, unscored |

The important split:

```text
rank-zero first-order X
```

is not the same as:

```text
positive massive source-free X.
```

That matters.

Checkpoint 222 made the first-order route attractive because it avoids a regular propagating vector kinetic term.

But first-order rank zero does not by itself give:

```text
m_X^2 > 0,
lambda_X = 1/m_X,
Q_X,
q_test,
alpha_X.
```

So it cannot yet pass the fifth-force or local-GR gate.

## 4. No-Hair Identity

The useful conditional proof is standard and clean.

Assume:

```text
L_X X = 0,
L_X = -Delta + m_X^2,
m_X^2 > 0.
```

Multiply by `X` and integrate over the local exterior domain:

```text
int_D X L_X X
  = int_D (|grad X|^2 + m_X^2 X^2)
    - int_boundary X n.grad X.
```

If:

```text
J_X = 0,
boundary term = 0,
m_X^2 > 0,
regular decaying exterior data,
```

then:

```text
int_D (|grad X|^2 + m_X^2 X^2) = 0.
```

Therefore:

```text
X = 0,
grad X = 0.
```

That would kill the local bulk-X force.

This is a real theorem shape.

But it is conditional because MTS has not derived the needed parent conditions.

## 5. Source-Normalized Force Law

If a compact source remains, the result is not no-hair.

It is a finite-range force:

```text
(-Delta + m_X^2) X = q_X rho_source.
```

For a monopole source, the exterior profile is:

```text
X(r) = Q_X exp(-r/lambda_X) / (4 pi r),
lambda_X = 1 / m_X.
```

The local force row needs:

```text
a_X/a_GR = alpha_X (1 + r/lambda_X) exp(-r/lambda_X).
```

But:

```text
alpha_X
```

is not a free decoration.

It needs a parent-normalized charge product:

```text
alpha_X proportional to Q_X q_test / (G_measured M_source m_test).
```

So the parent action must derive:

```text
m_X,
q_X,
Q_X,
q_test,
G_eff,
M_eff,
measured GM normalization.
```

Those are not currently derived.

Therefore:

```text
bulk X cannot be fifth-force scored yet.
```

## 6. Conditions Still Missing

The no-hair / Yukawa pass requires:

| Condition | Required form | Current status |
|---|---|---|
| positive elliptic operator | `L_X = -Delta + m_X^2`, `m_X^2 > 0` | not parent-derived |
| source-free exterior | no matter/projector/domain/boundary source outside compact matter | not parent-derived |
| regular decaying boundary data | surface term vanishes in no-hair identity | boundary conditions open |
| no boundary/domain re-source | `n.grad X`, class transitions, `L_cg` gradients vanish or are Ward-owned | open after 379 |
| no species charge | all matter sees one coframe and no body-dependent `X` charge | closure required after 373 |
| source-normalized charge | `Q_X` and `q_test` calibrated against measured `GM` | open after 378 |

So the branch cannot say:

```text
X is harmless.
```

The honest statement is:

```text
X has a clean route to harmlessness,
but the parent action has not earned the route.
```

## 7. Observable Impact

The runner rows now update as:

| Observable row | Bulk-X input | Current policy |
|---|---|---|
| `delta_G_or_fifth_force_yukawa` | `alpha_X(lambda_X)` or theorem-zero `X` | parameterized and unscored |
| `gamma_minus_1` | `C_bulk epsilon_bulk` plus scalar/light-cone pieces | budget-only |
| `beta_minus_1` | `C_bulk2 epsilon_bulk` plus nonlinear/radial pieces | budget-only |
| `eta_WEP` | species-dependent `q_test` or body-dependent `Q_X/M` | source-locked if not theorem-zero |
| `Gdot/G` | time-dependent `m_X`, `q_X`, `Q_X`, or source normalization | contingent active |
| preferred-frame / `xi` | vector/tensor or boundary/domain `X` source | route through 376/379 maps |

This checkpoint does not make the local branch worse.

It makes the local branch harder to fool.

## 8. What This Proves

It proves a conditional mathematical statement:

```text
if X has a positive massive source-free local exterior operator,
and if the boundary/domain terms do not re-source it,
then regular decaying X hair vanishes.
```

It also proves the force-law contract:

```text
if X is sourced,
then MTS must derive lambda_X and alpha_X before fifth-force scoring.
```

It does not prove:

```text
positive X operator,
mass gap,
source-free exterior,
source charge,
test charge,
GM normalization,
WEP-safe coupling,
or local GR.
```

Therefore:

```text
bulk-X residual remains active.
```

## 9. Failure Modes

| Failure | Consequence |
|---|---|
| calling rank zero a mass gap | false bulk-X no-hair pass |
| forgetting exterior `X` sources | boundary/domain hair hidden as bulk silence |
| using `alpha_X` without source normalization | fake fifth-force comparison |
| calling massless `X` harmless | long-range fifth force or PPN residual |
| retaining wrong-sign/tachyonic `X` | local instability or growing mode |

These are the shortcuts this checkpoint blocks.

## 10. Gate Results

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | all cited source paths exist |
| mass-gap no-hair identity written | conditional pass | positive source-free massive `X` has zero regular decaying exterior |
| source-normalized force-law contract written | pass | `lambda_X`, `Q_X`, `q_test`, `alpha_X`, and `a_X/a_GR` recorded |
| positive `X` operator parent-derived | fail | parent action has not derived `L_X = -Delta + m_X^2`, `m_X^2 > 0` |
| source-free exterior parent-derived | fail | boundary/projector/domain/matter charges can still re-source `X` |
| `alpha_X(lambda_X)` parent-derived | fail | `m_X`, `q_X`, `Q_X`, `q_test`, and measured-`GM` normalization are missing |
| bulk-X residual retained | pass | `epsilon_bulk` and fifth-force rows remain active |
| fifth-force or PPN pass claimed | fail | contract only; no local bound score |
| local GR promoted | fail | bulk, boundary, source, WEP, EH gates remain open |
| claim ceiling enforced | pass | no local-GR/fifth-force claim |

## 11. Decision

Decision:

```text
bulk_X_mass_gap_and_source_normalized_force_law_not_parent_derived_alphaX_lambdaX_missing_residual_retained
```

Meaning:

```text
a valid bulk-X local pass needs either:
1. a positive source-free mass-gap theorem, or
2. a source-normalized Yukawa force law.
```

The contract is now explicit.

But:

```text
operator sign,
mass gap,
source-free exterior,
X charge,
test coupling,
and alpha_X(lambda_X)
```

are not parent-derived.

Therefore:

```text
bulk X stays as an active retained residual.
```

No promotion:

```text
fifth-force not passed,
PPN not passed,
EH not derived,
WEP not derived,
local GR not derived.
```

## 12. Next Target

Next:

```text
381 - Local-GR Debt Ledger Rollup After 360-380
```

Aim:

```text
roll up the WEP, EH, preferred-frame, fifth-force, source-normalization,
boundary, and bulk-X gates into one compact local-GR debt ledger.
```

Pass condition:

```text
ready rows,
conditional theorem rows,
retained coefficient rows,
failed-open rows,
and unscored rows are separated.
```

Why this next:

```text
we have now caged most of the local-GR monsters one by one.
```

The next useful move is:

```text
show exactly what still blocks derived local GR,
and what can already move toward testing without pretending the derivation is complete.
```
