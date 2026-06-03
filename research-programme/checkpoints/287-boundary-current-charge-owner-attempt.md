# 287 - Boundary-Current Charge Owner Attempt

Private derivation checkpoint. This is not a public field-theory, CMB, local-GR, or amplitude-prediction claim.

## Purpose

Checkpoint 286 proved a useful no-go:

```text
the memory-stress and hazard equations are homogeneous in B_mem.
```

So the amplitude cannot be derived from the stress kernel alone.

The next possible non-circular route is:

```text
derive a parent-owned relative boundary current J_B,
derive a charge unit Q_*,
and show DeltaR = (Q_early - Q_today)/Q_* = 2/9.
```

This checkpoint asks whether the existing relative-current machinery can do that.

Short verdict:

```text
No promotion yet.
The relative boundary current can support conservation/invariance,
but it does not derive the normalized charge unit or endpoint occupancies.
```

However, the obstruction is now exact:

```text
we need a Ward/index theorem giving effective level k=9,
endpoint occupancies n_today=1 and n_early=3,
endpoint arrow 3 -> 1,
and trace partition B_mem = DeltaR/3.
```

## Machine Artifact

Script:

```text
scripts/boundary_current_charge_owner_attempt.py
```

Run:

```text
runs/20260601-000110-boundary-current-charge-owner-attempt
```

Status:

```text
boundary_current_charge_owner_not_derived_exact_quantization_obstruction_identified
```

Claim ceiling:

```text
relative_current_support_only_no_amplitude_or_local_GR_promotion
```

## What The Current Owns

The formal relative current is:

```text
J_B = (j_3, b_2)
```

with:

```text
d_rel J_B =
(
  d j_3,
  i* j_3 - d_boundary b_2
)
= 0.
```

The relative charge is:

```text
Q_B[D] = integral_D j_3 - integral_boundaryD b_2.
```

For class-preserving boundary variations:

```text
delta_eta Q_B[D] = 0.
```

This is good. It means the boundary-current language is not fluff:

```text
it can own conservation support and admissible-variation invariance.
```

But the normalized charge is:

```text
R = Q_B / Q_*.
```

and neither `Q_*` nor the endpoint values are derived by relative closure.

## Quantization Attempt

If relative periods are integral, then:

```text
R = n/k.
```

The desired endpoints are:

```text
R_today = 1/9
R_early = 1/3
DeltaR = 2/9
B_mem = DeltaR/3 = 2/27.
```

That is equivalent to the minimal integer data:

```text
k = 9
n_today = 1
n_early = 3
delta_n = 2.
```

Multiples also reproduce the same rational endpoints:

| Level | `n_today` | `n_early` | `R_today` | `R_early` | `DeltaR` |
|---:|---:|---:|---:|---:|---:|
| 9 | 1 | 3 | 1/9 | 1/3 | 2/9 |
| 18 | 2 | 6 | 1/9 | 1/3 | 2/9 |
| 27 | 3 | 9 | 1/9 | 1/3 | 2/9 |

So the exact target is not merely a decimal coincidence.

But:

```text
integral-period language does not by itself choose k=9,
does not choose n_today=1,
does not choose n_early=3,
and does not choose the arrow 3 -> 1.
```

It turns the amplitude problem into a level/occupancy theorem.

That is progress, but not promotion.

## Local / FLRW Split

The desired branch behaviour is still clean:

| Branch | Desired current class | Status | Missing parent step |
|---|---|---|---|
| stationary local vacuum | `[J_B]=0` or exact | possible conditional | prove `P_loc J_B=0` from equations |
| coherent FLRW | `[J_B]` nontrivial | possible contract | derive endpoint occupancies and arrow |
| boundary transition | class change or exchange `b_2` | open danger | no PPN wall stress |
| collapse / merger | possible event source | open | source/sink law |

This is the same good/bad split we keep finding:

```text
local silence and FLRW nonzero class are compatible,
but not parent-selected.
```

## Topological Safety Tension

There is a structural tradeoff:

| Route | Advantage | Failure |
|---|---|---|
| pure topological current | metric-independent, no PPN wall stress | inert unless coupled to stress/background equations |
| physical boundary surface stress | can carry amplitude | risks local-GR/PPN failure |
| topological current with Ward trace coupling | could be safe locally and source FLRW globally | Ward identity not derived |
| multiplier-imposed closure | gives `d_rel J_B=0` | does not select representative, level, endpoints, or arrow |

The best live theory route is therefore:

```text
topological current + Ward-fixed trace coupling.
```

That is the only route that could plausibly be:

```text
safe locally,
nonzero cosmologically,
and amplitude-fixing.
```

But it is still a theorem target.

## Gates

| Gate | Result | Meaning |
|---|---|---|
| source paths exist | pass | audit is traceable |
| relative current owner | pass formal | `J_B=(j_3,b_2)` and `d_relJ_B=0` support conservation |
| charge invariance | pass conditional | `Q_B[D]` invariant under class-preserving variations |
| charge unit `Q_*` derived | fail | scale remains free |
| level `k=9` derived | fail | no Ward/index theorem yet |
| endpoint occupancies derived | fail | `n=(1,3)` identified, not selected |
| topological safety vs physical source | open | pure topology safe but inert |
| local silence derived | fail | local trivial class conditional |
| `B_mem` derived | fail | still needs `Q_*`, level, occupancies, arrow, trace partition |

## Decision

Decision:

```text
boundary_current_charge_owner_not_derived_exact_quantization_obstruction_identified
```

Meaning:

```text
relative current machinery is good conservation/support structure,
but not yet a normalized charge owner.
```

What improved:

```text
the missing amplitude theorem is now integer-level precise:
k=9, n_today=1, n_early=3, arrow 3 -> 1, trace partition 1/3.
```

What did not improve:

```text
B_mem=2/27 is not derived.
local GR is not derived.
the parent field theory is not complete.
```

Boxing-score version:

```text
We found the scorecard the judge would need:
rounds 1 and 3 on a 9-point card.
But we have not shown why this fight uses that card.
That missing rulebook is the Ward/index theorem.
```

## Output Files

```text
runs/20260601-000110-boundary-current-charge-owner-attempt/results/source_register.csv
runs/20260601-000110-boundary-current-charge-owner-attempt/results/current_construction_contract.csv
runs/20260601-000110-boundary-current-charge-owner-attempt/results/charge_quantization_attempts.csv
runs/20260601-000110-boundary-current-charge-owner-attempt/results/local_FLRW_branch_tests.csv
runs/20260601-000110-boundary-current-charge-owner-attempt/results/topological_vs_physical_source_tension.csv
runs/20260601-000110-boundary-current-charge-owner-attempt/results/endpoint_integer_level_tests.csv
runs/20260601-000110-boundary-current-charge-owner-attempt/results/gate_results.csv
runs/20260601-000110-boundary-current-charge-owner-attempt/results/decision.csv
```

## Next Step

There are two honest next routes.

### Theory Route

Attempt:

```text
derive the k=9 Ward/index level.
```

Pass condition:

```text
the parent action forces a 9-level relative charge lattice,
selects endpoint occupancies 3 and 1,
and supplies the endpoint arrow.
```

Fail condition:

```text
k=9 is only spatial component counting or post-fit rationalization.
```

### Empirical Route

Run:

```text
no-SH0ES and DESI DR1/DR2 fixed-branch robustness.
```

Recommended:

```text
one k=9 Ward/index attempt next,
then empirical no-SH0ES if the theorem route still fails.
```

Reason:

```text
we now know the exact thing to try deriving; one clean attempt is worth it before returning to data.
```
