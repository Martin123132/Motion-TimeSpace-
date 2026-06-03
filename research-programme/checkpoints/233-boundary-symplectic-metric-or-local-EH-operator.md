# 233 - Boundary Symplectic Metric or Local EH Operator

Private local-derivation checkpoint. This is not a public local-GR, PPN,
clock, WEP, or field-theory completion claim.

## 1. Trigger

Checkpoint 232 made `P_mem` less arbitrary:

```text
P_mem = 1 - Pi_M - Pi_TF - Pi_matter.
```

But the hard row remained:

```text
what metric makes those projectors canonical?
```

This checkpoint writes the best current boundary metric candidate and the
parallel local Einstein-Hilbert exterior gate.

## 2. Machine Artifact

Script:

```text
scripts/boundary_symplectic_metric_or_local_EH_operator.py
```

Run:

```text
runs/20260601-000050-boundary-symplectic-metric-or-local-EH-operator
```

Command:

```text
python scripts/boundary_symplectic_metric_or_local_EH_operator.py --timestamp 20260601-000050
```

Status:

```text
boundary_Hodge_DeWitt_metric_candidate_projectors_orthogonal_Lovelock_EH_gate_written_no_promotion
```

Claim ceiling:

```text
boundary_metric_candidate_and_EH_gate_no_parent_local_GR_or_PPN_promotion
```

## 3. Boundary Metric Candidate

The best current candidate is a Hodge/DeWitt boundary metric:

```text
<delta J_1, delta J_2>_boundary
= <harmonic flux>_Hodge
+ <trace-free shell stress>_DeWitt
+ <matter/clock direct coupling block>
+ <relative memory exchange>_Hodge-relative.
```

This gives:

| block | projector | meaning |
|---|---|---|
| harmonic absolute `H^2` flux | `Pi_M` | mass/charge monopole stored as `M_eff` |
| trace-free shell tensor | `Pi_TF` | anisotropic shear/slip source |
| direct matter/clock vertex | `Pi_matter` | WEP/redshift-danger coupling |
| relative memory exchange | `P_mem` | exact cohomology channel |

Then:

```text
P_mem
```

is not a magic eraser.

It is the orthogonal complement to:

```text
Pi_M,
Pi_TF,
Pi_matter.
```

under the candidate boundary metric.

## 4. Why This Helps

The Hodge part separates:

```text
harmonic absolute S^2 flux
```

from:

```text
relative exact memory flux.
```

So ordinary mass is preserved:

```text
Pi_M J -> M_eff.
```

The DeWitt/SO(3) part separates:

```text
scalar trace
```

from:

```text
trace-free l >= 2 shear.
```

So no-slip safety is not obtained by deleting arbitrary information.

It is obtained by assigning the dangerous shear block to:

```text
Pi_TF.
```

The matter/clock block is not projected away after fitting. It is forbidden by
the universal-coupling contract:

```text
Pi_matter = 0
```

only if the parent matter action has no direct memory-sector vertex.

## 5. Local EH Operator Gate

The parallel beta route is:

```text
if the compact exterior metric sector is four-dimensional,
diffeomorphism invariant,
metric-only,
second-order,
and carries no exterior X/J_rel/V_def hair,
```

then the local exterior operator is forced into the Einstein-Hilbert/Lovelock
class:

```text
G_mu_nu + Lambda g_mu_nu = 0.
```

For a compact Solar-System exterior, the constant `Lambda`-like term is not the
PPN beta issue, and the local branch reduces to:

```text
G_mu_nu = 0
```

to PPN order around the source.

Then the exterior is Schwarzschild and:

```text
beta = 1.
```

This is not a derivation from MTS yet.

It is the exact gate the parent action must pass.

## 6. What Still Fails

Still missing:

```text
derive the boundary Hodge/DeWitt metric from the parent action,
vary the boundary metric blocks into Bianchi-safe stress,
derive no-hair for X/J_rel/V_def,
derive the local metric-only Einstein-Hilbert exterior operator,
derive universal matter/clock coupling.
```

So:

```text
P_mem is better owned but not parent-owned;
beta is better gated but not derived;
local GR remains unpromoted.
```

## 7. Gate Results

| gate | result |
|---|---|
| all cited local sources exist | pass |
| boundary Hodge/DeWitt metric candidate written | pass |
| `P_mem` orthogonal-complement route written | pass |
| local EH/Lovelock sufficient gate written | pass |
| parent boundary metric derived | fail |
| local EH exterior operator parent-derived | fail |
| local GR or PPN promoted | fail |

The pass rows are useful.

The fail rows are still decisive.

## 8. Decision

Decision:

```text
boundary_Hodge_DeWitt_metric_candidate_projectors_orthogonal_Lovelock_EH_gate_written_no_promotion
```

Meaning:

```text
the parent-projector route is improved by a concrete boundary Hodge/DeWitt
metric candidate: harmonic H^2 flux defines Pi_M and M_eff, trace-free shell
tensors define Pi_TF, direct matter/clock vertices define Pi_matter, and P_mem
is their orthogonal complement in the relative memory sector.
```

Main gain:

```text
P_mem can now be judged against a concrete orthogonality contract.
```

Main failure:

```text
the boundary metric and local EH exterior operator are candidates, not parent
theorems.
```

## 9. Next Target

Create:

```text
234-boundary-metric-variation-and-Bianchi-ledger.md
```

Purpose:

```text
vary the candidate boundary metric blocks into stress/Bianchi accounting.
```

Pass condition:

```text
Pi_M,
Pi_TF,
Pi_matter,
P_mem
```

produce a conserved total stress ledger without hidden local PPN hair.

Fail condition:

```text
the projector metric is treated as harmless without varying its stress.
```
