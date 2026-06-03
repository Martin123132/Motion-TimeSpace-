# 286 - Memory-Stress Normalization Scale No-Go

Private derivation checkpoint. This is not a public field-theory, CMB, or local-GR claim.

## Purpose

Checkpoint 285 kept the fixed no-clock branch empirically alive but mixed. The theory problem is still sharper:

```text
Can the memory stress itself force B_mem = 2/27?
```

This checkpoint attempts that route directly.

Short verdict:

```text
No. The memory-stress, pressure-kernel, and hazard equations are homogeneous in B_mem.
They can preserve the shape and conservation identities for any B_mem.
```

So:

```text
B_mem=2/27 still requires a non-homogeneous parent-owned boundary charge,
or it remains a locked empirical closure amplitude.
```

## Machine Artifact

Script:

```text
scripts/memory_stress_normalization_scale_no_go.py
```

Run:

```text
runs/20260601-000109-memory-stress-normalization-scale-no-go
```

Status:

```text
memory_stress_normalization_scale_no_go_Bmem_requires_boundary_charge_owner
```

Claim ceiling:

```text
amplitude_not_derived_exact_parent_contract_written
```

## Attempted Derivation

Use the current locked memory density shape:

```text
rho_M(N) = rho_Lambda + B_mem A(N)
A(N) = 1 - exp[-(N/u3)^p]
p = 3
u3 = 1/4
```

The conditional pressure kernel is:

```text
p_M + rho_M = B_mem A_N / 3
```

and:

```text
rho_N = B_mem A_N.
```

Therefore:

```text
3(p_M + rho_M) - rho_N = 0.
```

But this identity is linear in `B_mem`. If:

```text
B_mem -> lambda B_mem,
```

then:

```text
rho_N -> lambda rho_N
p_M + rho_M -> lambda(p_M + rho_M)
3(p_M + rho_M) - rho_N -> lambda[3(p_M + rho_M) - rho_N] = 0.
```

So the pressure/stress identity cannot pick `lambda`.

That is the scale no-go.

## Integral Check

The additive-hazard law gives:

```text
integral A_N dN = 1.
```

That fixes the activated fraction, not the total released charge.

Numerically:

| Branch | `B_mem` | `integral A_N dN` | `integral B_mem A_N dN` | `integral (p+rho)dN` |
|---|---:|---:|---:|---:|
| zero memory | 0.0 | 1.0 | 0.0 | 0.0 |
| `1/27` probe | 0.037037037037037035 | 1.0 | 0.037037037037037035 | 0.012345679012345678 |
| locked `2/27` | 0.07407407407407407 | 1.0 | 0.07407407407407407 | 0.024691358024691357 |
| near fitted primary | 0.07453319160061826 | 1.0 | 0.07453319160061826 | 0.02484439720020609 |

All of these obey the same kernel law.

Therefore:

```text
choosing an impulse value chooses B_mem.
```

Unless the parent action fixes that impulse independently, stress-impulse normalization is just a restatement, not a derivation.

## Endpoint Quadratic Reaudit

The exact amplitude target remains:

```text
27R^2 - 12R + 1 = 0.
```

Roots:

```text
R_today = 1/9
R_early = 1/3
DeltaR = 2/9
B_mem = DeltaR/3 = 2/27.
```

This is still the cleanest theorem target.

But the formal potential:

```text
U(R) = 9R^3 - 6R^2 + R
dU/dR = 27R^2 - 12R + 1
```

has:

| Endpoint | `R` | `U''` | Ordinary gradient role |
|---|---:|---:|---|
| today low endpoint | 0.1111111111111111 | -6.0 | unstable |
| early high endpoint | 0.3333333333333333 | 6.0 | stable |

So ordinary down-gradient dynamics do not give the desired arrow:

```text
1/3 -> 1/9.
```

The endpoint equation is useful, but the endpoint arrow is still missing.

## Route Ledger

| Route | Result | Reason |
|---|---|---|
| Bianchi / continuity | no-go | fixes `p+rho=rho_N/3`, but homogeneous in `B_mem` |
| additive hazard | no-go for amplitude | fixes `A=1-exp(-I_M)`, not total charge |
| stress impulse | conditional restatement | `integral(p+rho)dN=B_mem/3` |
| endpoint quadratic | formal theorem target | gives `DeltaR=2/9`, but not parent-owned |
| normalized boundary charge | only viable contract | could fix `DeltaR=2/9` before data |

## Exact Parent Contract

To derive:

```text
B_mem = 2/27
```

instead of fitting or freezing it, a future parent action must satisfy all clauses:

| Clause | Must prove | Why needed |
|---|---|---|
| boundary current owner | parent variables define a conserved relative boundary current `J_B` before FLRW reduction | no current, no charge |
| charge unit | dimensionless `Q_*` fixed by action/Ward identity, not data | `DeltaR=Q_B/Q_*` needs a real unit |
| endpoint equations | stationarity gives `27R^2-12R+1=0` with fixed coefficients | source of `1/3` and `1/9` |
| endpoint arrow | dynamics select `1/3 -> 1/9` | formal potential arrow is not enough |
| trace partition | background density receives one third of `DeltaR` | needed for `B_mem=DeltaR/3` |
| local silence | same current vanishes/projects out in local vacuum/PPN domains | cosmology amplitude must not break local GR |
| Bianchi closure | metric variation gives covariantly conserved stress | field theory needs conservation |

This is the contract. No clause can be skipped without turning the amplitude back into closure.

## Gates

| Gate | Result | Meaning |
|---|---|---|
| source paths exist | pass | derivation audit is traceable |
| pressure kernel selects amplitude | fail | kernel is homogeneous in `B_mem` |
| hazard integral selects amplitude | fail | unit activation fraction only |
| scale-symmetry no-go | pass | homogeneous stress equations cannot derive `B_mem` |
| endpoint quadratic exact target | pass formal | `DeltaR=2/9`, `B=2/27` retained |
| endpoint arrow derived | fail | formal potential points the wrong way |
| parent contract written | pass | exact future derivation target stated |
| `B_mem` derived now | fail | needs parent-owned boundary charge |

## Decision

Decision:

```text
memory_stress_normalization_scale_no_go_Bmem_requires_boundary_charge_owner
```

Meaning:

```text
The current stress/hazard machinery can derive shape-like behaviour,
but it cannot derive the amplitude because it has a scale symmetry in B_mem.
```

What improved:

```text
we now know exactly what kind of object must be added/derived:
a conserved normalized boundary charge with DeltaR=2/9 and trace partition 1/3.
```

What did not improve:

```text
B_mem=2/27 is still not derived.
```

Boxing-score version:

```text
We tried to get the power punch from the shoulder mechanics.
The mechanics are real, but they do not set the glove weight.
The glove weight has to come from the weigh-in: the boundary charge normalization.
```

## Output Files

```text
runs/20260601-000109-memory-stress-normalization-scale-no-go/results/source_register.csv
runs/20260601-000109-memory-stress-normalization-scale-no-go/results/normalization_integrals.csv
runs/20260601-000109-memory-stress-normalization-scale-no-go/results/scale_symmetry_no_go.csv
runs/20260601-000109-memory-stress-normalization-scale-no-go/results/endpoint_quadratic_reaudit.csv
runs/20260601-000109-memory-stress-normalization-scale-no-go/results/amplitude_route_ledger.csv
runs/20260601-000109-memory-stress-normalization-scale-no-go/results/parent_contract.csv
runs/20260601-000109-memory-stress-normalization-scale-no-go/results/gate_results.csv
runs/20260601-000109-memory-stress-normalization-scale-no-go/results/decision.csv
```

## Next Step

The next derivation target is now precise:

```text
derive the boundary-current owner J_B and charge unit Q_*,
or keep B_mem=2/27 as locked empirical closure.
```

Best next attempt:

```text
construct a relative boundary-current action whose FLRW reduction gives
DeltaR = Q_B/Q_* = 2/9,
while the same current is locally silent under the PPN/vacuum projector.
```
