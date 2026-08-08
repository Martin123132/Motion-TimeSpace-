# 4086 - Parent EH Operator Signature Or Non-EH R11 Projection

- Timestamp: `2026-07-02T03:58:24+00:00`
- Status: `private_nonclaim_checkpoint`
- Decision: `PARENT_EH_SIGNATURE_REDUCED_TO_EXACT_LADDER_ELSE_NON_EH_R11_PPN_PROJECTION_VECTOR_SELECTED`
- Public local-GR/EH-only claim: `false`
- GitHub action: `false`

## Result

4086 turns the 4085 handoff into a hard fork:

```text
Route A: parent signs the EH/EC operator ladder.
Route B: every unsigned escape channel becomes a non-EH/R11 PPN projection residual.
```

No more fog. If the parent branch is truly local, 4D, diffeomorphism-invariant, metric/coframe-only, Levi-Civita, second-order through PPN order, boundary-silent and same-source, then the observed field equation is forced into:

```text
E_obs^{mu nu} = A_* G^{mu nu}[g_obs] + B_* g_obs^{mu nu}
```

That is the EH signature route.

## What Was Derived

The operator theorem is exact conditional:

```text
P1 observed metric/coframe owner
P2 local product chart
P3 Ward/Bianchi identity
P4 Levi-Civita connection
P5 no independent extra fields
P6 no higher-derivative/nonlocal metric operators through 2PN
P7 boundary/topological/projector silence
P8 same Hilbert source and constant kappa/G

P1...P8 => EH/EC local operator
EH/EC + 4085 => gamma=beta=1, alpha_i=xi=zeta_i=0, Gdot/G=0
```

This is not claimed for MTS yet because the parent has not signed every rung.

## Double-Zero Mechanism

4086 also writes the useful decoupling lemma:

```text
C_i(X0)=0
partial_A C_i(X0)=0
H_AB(X0)>0
linear readout/projector coupling = 0
```

then the auxiliary/non-EH operator has no linear local PPN source. A single zero is not enough; the first derivative and readout must vanish too, or the operator goes into the residual vector.

## Non-EH Projection Vector

If the EH ladder fails at any rung:

```text
DeltaE_nonEH^{mu nu}
  = sum_i c_i E_i^{mu nu}
  + E_q^{mu nu}
  + E_projector^{mu nu}
  + E_boundary^{mu nu}
  + E_readout^{mu nu}
```

The projections are now fixed:

```text
delta_gamma_nonEH ~ -(kappa_ref/(C_TF U)) nabla^{-2} P_TF[DeltaE_nonEH_ij]
delta_beta_nonEH  := Pi_beta[DeltaE_nonEH_00 at 2PN]
alpha_i, xi       := Pi_alpha_i/Pi_xi[vector/domain/coframe/projector markers]
zeta_i            := Pi_zeta_i[nabla_mu DeltaE_nonEH^{mu nu} - kappa_ref DeltaJ_source^nu]
Gdot/G            := partial_t kappa_eff/kappa_eff
alpha(lambda)     := finite-range tail if an extra mode survives
```

That is the forward path: not circling, but forcing the extra pieces to either disappear by theorem or pay a bound.

## Route Selection

The broad EH-only parent assertion is too expensive to claim right now. The better route is:

```text
first fill one live non-EH projection row
compare it against 4085 gamma/beta bounds
then repeat family-by-family
```

The first target is the tracefree spatial/gamma-beta projection because 3918 already derived the gamma map and 4085 has real bounds.

## Decision

```text
EH signature theorem = exact conditional
auxiliary double-zero decoupling = exact conditional
non-EH/R11 PPN projection formulas = selected
local GR claim = still false
next gate = first non-EH R11 projection fill against gamma/beta
```

## Sources

- David Lovelock, *The Einstein Tensor and Its Generalizations*, Journal of Mathematical Physics 12, 498 (1971).
- 4085 source-stable PPN theorem and bound table.
- 3906/4019/4042 R11 and EH-selector corpus checkpoints.

## Next

```text
4087-Y5-R2FR-first-nonEH-R11-projection-fill-gamma-beta-bound.md
```

This is the clean Mayweather route: do not need a knockout claim; make each escape channel step into the ring and score it fairly.
