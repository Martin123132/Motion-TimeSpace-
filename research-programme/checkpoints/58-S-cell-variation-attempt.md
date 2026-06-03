# S Cell Variation Attempt

## 1. Purpose

This file follows:

```text
57-memory-action-owner-contract.md
```

The previous checkpoint identified the central missing owner:

```text
S_cell[e,u,Q,lambda_cell].
```

This checkpoint asks:

```text
Can a direct variational S_cell derive spatial determinant exposure and 3+1
normalization without inserting p=3 or u_3=1/4 by hand?
```

Short answer:

```text
not yet. Direct multiplier variations can impose the desired structure, but
they do not derive it.
```

Tiny cape removed. Still useful, but not magic.

## 2. Machine Run

Implemented:

```text
scripts/S_cell_variation_attempt.py
```

Successful run:

```text
runs/20260531-105020-S-cell-variation-attempt/status.json
```

Readout:

```text
S_cell_direct_variation_fails_as_derivation_topological_owner_next
```

Generated:

```text
runs/20260531-105020-S-cell-variation-attempt/results/source_checkpoint_register.csv
runs/20260531-105020-S-cell-variation-attempt/results/variation_candidate_ledger.csv
runs/20260531-105020-S-cell-variation-attempt/results/euler_lagrange_contract.csv
runs/20260531-105020-S-cell-variation-attempt/results/no_smuggling_tests.csv
runs/20260531-105020-S-cell-variation-attempt/results/gate_results.csv
runs/20260531-105020-S-cell-variation-attempt/results/decision.csv
```

## 3. Direct Multiplier Attempt

The obvious local term is:

```text
S_cell = integral sqrt(-g) [
  lambda_I (I_M - det Q)
  + lambda_X (X - 4N)
].
```

Variation gives:

```text
delta lambda_I -> I_M = det Q
delta lambda_X -> X = 4N
```

That reproduces:

```text
p = 3
u_3 = 1/4
```

but only because those targets were put into the action.

Verdict:

```text
valid closure contract;
not a parent derivation.
```

## 4. First-Order Q Improvement

A less bad version is:

```text
S_cell = integral sqrt(-g) [
  lambda_Q (D_tau Q - P_coh[Theta]/u_3)
  + lambda_I (I_M - det Q)
].
```

This at least makes `Q` a field with a local first-order equation:

```text
D_tau Q^i_j = (1/u_3) P_coh[Theta]^i_j.
```

That is better than a post-processed integral:

```text
Q = integral P_coh[Theta] d tau / u_3.
```

But it still assumes:

```text
u_3 = 1/4;
P_coh;
determinant exposure.
```

So it improves the contract but does not close the theorem.

## 5. Rejected Routes

Rejected:

```text
soft potential lock:
adds arbitrary stiffness terms and permits deviations/hair.

direct multiplier lock:
imposes the desired answer.

arbitrary X=4N rescaling:
same smuggling problem in different trousers.
```

Interesting but underdefined:

```text
coframe volume-ratio action:
may relate spatial determinant to 3+1 cell but needs a precise invariant.
```

Best next route:

```text
topological BF / closed-form / no-charge cell owner.
```

Why?

```text
ordinary current conservation permits nonzero charge/hair;
direct multipliers impose the answer;
a nonpropagating or topological owner is the remaining route that might select
the cell structure without local hair.
```

## 6. Gate Verdict

Gate result:

```text
direct_variation_attempted                   pass
S_cell_derives_p3_without_imposition          fail
S_cell_derives_u3_quarter_without_imposition  fail
first_order_Q_field_equation_available        pass_partial
ordinary_current_sufficient                   fail
topological_owner_needed                      pass
support_claim_allowed                         fail
```

So:

```text
S_cell can be written as a disciplined closure/action contract;
S_cell does not yet derive the branch.
```

## 7. Decision

Decision:

```text
S_cell_variation_status = direct_variation_fails_as_derivation
```

Meaning:

```text
the direct action can impose p=3 and u_3=1/4;
it cannot yet select them;
the quarter branch stays retained as a less-free closure candidate, not a
derived field-theory result.
```

The important thing is that this failed cleanly. We now know the next live
route is not another scalar multiplier.

## 8. Next Target

Create:

```text
59-topological-cell-current-owner-attempt.md
```

Purpose:

```text
try a topological/nonpropagating cell-current owner that can select or protect
the memory cell structure without allowing ordinary conserved-current hair.
```

Pass condition:

```text
a BF/closed-form/no-charge mechanism produces the spatial determinant and 3+1
normalization as protected constraints, not inserted answers.
```

Fail condition:

```text
the topological route also reduces to direct multipliers or permits cell charge
hair.
```
