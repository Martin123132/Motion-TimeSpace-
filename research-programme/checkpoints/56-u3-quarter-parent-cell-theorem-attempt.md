# u3 Quarter Parent-Cell Theorem Attempt

## 1. Purpose

This file follows:

```text
55-u3-quarter-lock-smoke.md
```

The previous checkpoint showed that:

```text
u_3 = 1/4
```

survives the no-refit internal smoke guardrails. This checkpoint asks:

```text
Can u_3 = 1/4 be motivated by a parent 3+1 coherence-cell theorem rather than
kept as a numerically cute near-lock?
```

Short answer:

```text
there is a clean conditional route: a coherent 3+1 observer cell gives
X_FLRW = 4N, hence u_3 = 1/4. But the cell is not yet parent-action-derived.
```

So we have a theorem-shaped doorway, not the finished theorem. Still, doorway
beats wallpaper.

## 2. Machine Run

Implemented:

```text
scripts/u3_quarter_parent_cell_theorem_attempt.py
```

Successful run:

```text
runs/20260531-104327-u3-quarter-parent-cell-theorem-attempt/status.json
```

Readout:

```text
u3_quarter_has_conditional_3plus1_cell_route_not_parent_derivation
```

Generated:

```text
runs/20260531-104327-u3-quarter-parent-cell-theorem-attempt/results/source_checkpoint_register.csv
runs/20260531-104327-u3-quarter-parent-cell-theorem-attempt/results/u3_quarter_theorem_chain.csv
runs/20260531-104327-u3-quarter-parent-cell-theorem-attempt/results/candidate_cell_routes.csv
runs/20260531-104327-u3-quarter-parent-cell-theorem-attempt/results/noncircularity_tests.csv
runs/20260531-104327-u3-quarter-parent-cell-theorem-attempt/results/gate_results.csv
runs/20260531-104327-u3-quarter-parent-cell-theorem-attempt/results/decision.csv
```

## 3. Conditional Theorem Chain

Use a parent coherent 3+1 observer cell:

```text
C_4 = theta^0 wedge theta^1 wedge theta^2 wedge theta^3.
```

In a coherent FLRW/conformal branch, all four legs carry the same log expansion
load:

```text
d ln C_4/dtau = 4H.
```

Integrating from epoch to today gives:

```text
L_4 = integral_t^t0 4H dt = 4 ln(a0/a) = 4N.
```

Therefore the quarter-locked scalar load is:

```text
X_FLRW = 4N = N/u_3.
```

So:

```text
u_3 = 1/4.
```

Then the existing spatial determinant route remains:

```text
Q^i_j = X_FLRW delta^i_j
I_M = det(Q) = X_FLRW^3 = (4N)^3
F = 1 - exp[-(4N)^3].
```

This reproduces exactly:

```text
F = 1 - exp[-(N/(1/4))^3].
```

## 4. What Was Earned

This makes the quarter value less arbitrary:

```text
p = 3 comes from the three spatial coherent load eigen-directions;
u_3 = 1/4 comes from the four legs of the coherent observer cell;
the quarter-locked branch already survived checkpoint 55's no-refit smoke.
```

The key separation is:

```text
spatial determinant gives the cubic exposure;
3+1 cell normalization gives the quarter scale.
```

That is the most coherent story so far for why the branch wants both `3` and
`1/4`.

## 5. What Still Fails

Gate result:

```text
u3_quarter_cell_route_written                   pass
u3_quarter_parent_derived                       fail
time_leg_origin_derived                         fail
spatial_determinant_and_4D_cell_reconciled      open
quarter_lock_empirical_smoke_survived           pass
support_claim_allowed                           fail
```

The hard missing theorem is:

```text
why the parent memory sector normalizes the FLRW load by the 3+1 observer cell
while the exposure determinant remains spatial/coherent-load cubic.
```

That is not a trivial paperwork gap. A critic can fairly ask:

```text
why not a 4D determinant giving p=4?
why not a spatial-only normalization giving u_3=1/3?
why is the clock leg equal to one Hubble leg?
```

Those questions need an action/current owner.

## 6. Non-Circularity Status

Passed or partially passed:

```text
the observer-cell language predates the quarter smoke;
the quarter value is not being promoted from score alone;
the 3+1 route is structurally tied to MTS's motion-time-space framing.
```

Failed or open:

```text
the fourth/clock leg is not yet parent-derived;
the spatial determinant plus 4D normalization split is not yet action-owned;
the local observer-cell branch and cosmology memory-cell branch are not yet one
shared theorem.
```

So the route is nontrivial, but not complete.

## 7. Decision

Decision:

```text
u3_quarter_parent_cell_status =
conditional_cell_theorem_candidate_not_parent_derivation
```

Meaning:

```text
u_3=1/4 now has a conditional 3+1 coherence-cell route;
that route matches the less-free smoke-surviving branch;
the route is not a parent derivation until an action/current owns it.
```

Allowed wording:

```text
The quarter-lock scale has a plausible 3+1 coherence-cell origin candidate.
```

Forbidden wording:

```text
MTS derives u_3=1/4.
```

Not yet. The little beastie has a collar, not a passport.

## 8. Next Target

Create:

```text
57-memory-action-owner-contract.md
```

Purpose:

```text
write the minimal parent action/current contract that would have to own:
p = 3;
u_3 = 1/4;
the coherent domain D;
Bianchi/conservation bookkeeping;
b_mem amplitude;
perturbation/lensing response.
```

Pass condition:

```text
one parent memory/action owner can explain why the activation is a spatial
determinant normalized by a 3+1 coherence cell, while remaining locally silent.
```

Fail condition:

```text
the branch remains a chain of individually plausible closure rules without a
single parent owner.
```
