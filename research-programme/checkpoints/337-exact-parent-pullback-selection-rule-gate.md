# 337 - Exact Parent-Pullback Selection Rule Gate

Private derivation checkpoint. This is not a public cosmology, CMB, local-GR, PPN, perturbation-theory, or unified-field claim.

## Purpose

Checkpoint 336 found the exact missing move:

```text
projection must be an exact parent readout/quotient,
not a new reduced EFT stage where all residual invariants can be written.
```

This checkpoint asks whether that is enough to mathematically forbid the active counterterm.

Short answer:

```text
yes, conditionally.
```

There is now a real theorem template:

```text
full S27 cell equivalence
+ trace-normalized parent Hamiltonian current
+ exact readout projection
=> epsilon_H = 1
=> q_trace = 2/27
=> no later lambda_mem P_active counterterm.
```

But it is still conditional because the parent MTS action has not yet proved that the reduction is exact readout rather than a Wilsonian reduced EFT.

This is an improvement, not a demotion: the missing assumption is now much sharper.

## Machine Artifact

Script:

```text
scripts/exact_parent_pullback_selection_rule_gate.py
```

Run:

```text
runs/20260601-194500-exact-parent-pullback-selection-rule-gate
```

Status:

```text
exact_parent_pullback_theorem_constructed_parent_action_premise_open
```

Claim ceiling:

```text
conditional_pullback_theorem_no_unconditional_epsilonH_or_Bmem_promotion
```

## The Algebraic Win

Use the full cell-equivalence group:

```text
S27.
```

The verifier uses adjacent transpositions as generators and solves the commutant condition:

```text
H_parent G = G H_parent
```

for all generators.

Result:

```text
constraint rank = 727
operator dimension = 729
commutant dimension = 2
```

So the full parent-invariant current lives in:

```text
span(I_cell, J_cell)
```

where:

```text
I_cell = identity current,
J_cell = coherent all-cell mode.
```

This matters because it is stronger than the earlier hand-wavy "identity only" route. Even if the parent current allows the coherent all-cell invariant `J_cell`, the diagonal readout is still uniform over all cells.

Therefore, once the parent trace is normalized:

```text
Tr(H_parent)/27 = 1,
```

any rank-2 coordinate readout obeys:

```text
Tr(P_active H_parent)/2 = 1.
```

So:

```text
epsilon_H = 1.
```

and:

```text
Tr(P_active H_parent)/27 = 2/27.
```

## Pullback Samples

The verifier tested several full-parent-invariant currents:

| Sample | Parent form | Full trace average | Active average |
|---|---|---:|---:|
| identity only | `I_cell` | 1 | 1 |
| mixed identity/coherent | `0.3 I_cell + 0.7 J_cell` | 1 | 1 |
| opposite identity/coherent | `2 I_cell - J_cell` | 1 | 1 |
| mostly identity | `0.95 I_cell + 0.05 J_cell` | 1 | 1 |

All exact parent readouts give:

```text
epsilon_H = 1,
q_trace = 2/27.
```

The post-projection counterterm:

```text
I_cell + delta P_active
```

with:

```text
delta = 0.0061980866083466
```

gives:

```text
epsilon_H = 1.0061980866083466,
q_trace_effective = 0.07453319160061828.
```

But it is not in the full parent commutant.

That means:

```text
exact parent pullback forbids it;
post-projection residual EFT allows it.
```

## The Fork

There are now two clean branches.

### Branch A - Exact Parent Readout

Rule:

```text
reduced operators must be restrictions/readouts of full S27-invariant parent operators.
```

Then:

```text
lambda_mem P_active is forbidden,
epsilon_H = 1 is conditionally derived,
B_mem = 2/27 follows if H_star = H0 and rank/dim are retained.
```

### Branch B - Wilsonian Reduced EFT

Rule:

```text
after projection, write every S2 x S25 residual-invariant operator.
```

Then:

```text
lambda_mem P_active is allowed,
epsilon_H is a free or fitted coupling,
B_mem = 2/27 remains an empirical closure/theorem target.
```

So the theory cannot dodge this fork.

## Gate Results

| Gate | Result |
|---|---|
| source paths exist | pass |
| full `S27` commutant dimension two | pass |
| full-invariant trace normalization implies `epsilon_H=1` | pass |
| full-invariant trace normalization implies `q_trace=2/27` | pass |
| `P_active` is not full-invariant | pass |
| `P_active` is residual-invariant | pass |
| exact pullback forbids lambda counterterm | pass |
| reduced Wilsonian EFT allows lambda counterterm | pass |
| parent action proves exact readout not EFT | fail |
| `epsilon_H` parent-derived unconditionally | fail |
| `B_mem` parent promotion allowed | fail |

## What We Can Honestly Say Now

This is the strongest amplitude result so far:

```text
If MTS reduction is exact parent readout,
then the no-later-counterterm rule is not arbitrary.
```

It follows from:

```text
full cell equivalence + trace normalization + pullback selection.
```

The remaining weakness is not the algebra. The algebra works.

The remaining weakness is action ownership:

```text
why is MTS projection exact readout rather than reduced EFT?
```

Until that is owned by the parent action, the fair status is:

```text
epsilon_H = 1 is conditionally derived under exact-readout premises,
B_mem = 2/27 remains the locked empirical lead/theorem target,
not an unconditional parent-derived result.
```

## Next Derivation Target

Next:

```text
derive_action_level_exact_readout_or_demote_epsilonH_to_closure.
```

Acceptance rule:

```text
The parent action must make P_active a readout/boundary/quotient map,
not a new dynamical tensor available for reduced counterterms.
```

Possible route:

```text
S_parent is varied before projection.
Projection is applied only to observables/current readout.
No independent reduced action S_reduced[P_active] is introduced.
All effective corrections must be pullbacks of parent-invariant operators.
```

If that route can be stated as an action principle, the amplitude branch becomes genuinely serious.

If it cannot, we should keep the locked branch empirical and stop calling `epsilon_H=1` derived.
