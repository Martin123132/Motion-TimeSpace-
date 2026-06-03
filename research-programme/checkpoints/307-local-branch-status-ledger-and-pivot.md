# 307 - Local Branch Status Ledger and Pivot

Private local-theory checkpoint. This is not a public local-GR, PPN, fifth-force, cosmology, CMB, or parent-field-theory claim.

## Purpose

Checkpoints 298-306 squeezed the local branch hard:

```text
open sector -> selector -> epsilon_loc runner -> coefficient map -> beta -> fifth-force gradient -> trace-source profile
```

This checkpoint asks:

```text
what has actually been derived,
what is merely conditional,
and what exact theorem target remains if we want local GR rather than a closure?
```

Short answer:

```text
we now have a conditional local residual suppression theorem,
but not a parent derivation of local GR.
```

That is real progress, but it is not the belt yet.

## Local Residual Vector

Use the local residual vector:

```text
R_loc =
(
  gamma - 1,
  beta - 1,
  a_5/a_N,
  delta_clock,
  delta_matter,
  nabla_mu Delta T_eff^{mu nu}
).
```

The current branch controls it through:

```text
gamma - 1          ~ c_gamma epsilon_loc
beta - 1           ~ c_beta epsilon_loc
a_5/a_N            ~ epsilon_loc shape_factor L_test/L_profile
delta_clock        ~ c_clock epsilon_loc
delta_matter       ~ c_matter epsilon_loc
conservation leak  ~ nabla_mu Delta T_eff^{mu nu}.
```

From checkpoint 303:

```text
c_beta = b1 - 2a1,
beta_eff = B/A^2.
```

So:

```text
B = A^2
```

is the clean beta-zero condition.

## Conditional Suppression Theorem

The strongest honest theorem currently available is:

```text
If:
1. matter couples universally through g_eff,
2. local leakage is trace-only common mode at leading order,
3. either sigma_D = 0 or the trace source is constant/flat,
4. the second-order response obeys B = A^2,
5. any remaining profile gradient passes the local gradient bound,

then R_loc is zero or bounded in the current local runner.
```

Proof sketch:

```text
universal coupling      -> c_clock = c_matter = 0
trace-only common mode  -> c_gamma = 0
B = A^2                 -> beta_eff = 1
sigma_D = 0             -> epsilon_loc = 0
flat trace source       -> grad s_D = 0
gradient runner         -> any nonzero residual must pass epsilon_loc L_test/L_profile bound
```

This is useful because the local problem is no longer vague.

But it is conditional because the parent theory has not derived the premises.

## Local Stack Status

| Layer | Earned | Blocker |
|---|---|---|
| open boundary sector | `q_r/q_a`, `Gamma_D`, positivity, and scalar trace-source route exist | noise/FDT state, Bianchi identity, and local silence are not parent-owned |
| local silence selector | `sigma_D=0` exactly suppresses local open-sector residuals | parent theory has not selected `sigma_D=0` for local domains |
| epsilon runner | exact silence passes; failure probes fail | thresholds remain proxy/internal |
| gamma/clock/matter | common-mode and universal-coupling contracts suppress leading channels | contracts are not action theorems |
| beta | `beta_eff=B/A^2` and `c_beta=b1-2a1` are derived | `B=A^2` is not parent-derived |
| fifth force | gradient runner catches local gradients | profile scale and official bound are not parent-derived |
| flat profile | Neumann/no-flux plus constant source gives `grad s_D=0` | Neumann/no-source conditions are not parent-derived |

## Promotion Gates

| Gate | Result | Meaning |
|---|---|---|
| source paths exist | pass | local branch ledger is traceable |
| open sector constructed | pass | effective local language exists |
| exact silence condition written | pass | `sigma_D=0` is a clean sufficient condition |
| conditional local suppression theorem | pass | the residual vector now has an exact theorem target |
| local selector parent-derived | fail | no action theorem forces local silence |
| universal metric coupling parent-derived | fail | direct clock/matter channel not officially closed |
| beta parent relation derived | fail | `B=A^2` is still a target |
| fifth-force gradient gate ready | pass | local gradients are no longer hand-waved |
| flat-profile theorem | conditional pass | nonzero leakage can be safe if flat |
| profile parent-derived | fail | flatness cannot be assumed |
| official PPN claim allowed | fail | no public local-GR/PPN claim |
| local GR promoted | fail | branch remains effective closure |
| `B_mem` parent-derived | fail | `2/27` remains empirical closure/theorem target |

## What This Means

This is not grim in the "dead idea" sense.

It is grim only in the useful engineering sense:

```text
the local branch now has named load-bearing parts,
and several of them are not bolted to the parent action yet.
```

That is much better than vague optimism.

It means we know the exact parts that have to hold.

Boxing-score version:

```text
MTS is not getting knocked out locally anymore by a mystery punch.
We can see the punches:
gamma, beta, fifth force, clocks, matter coupling, conservation.
We have defensive moves for each.
But the judges cannot score it as local GR until the footwork is derived from the parent action.
```

## Decision

Decision:

```text
local_branch_strongly_gated_but_unpromoted_empirical_pivot_recommended
```

Claim ceiling:

```text
conditional_local_residual_suppression_theorem_no_local_GR_or_PPN_promotion
```

The local branch should remain:

```text
effective closure / theorem target
```

not:

```text
derived local GR.
```

## Next Step

There are two honest routes.

Recommended route:

```text
pivot back to empirical holdout testing,
because the local branch is now disciplined enough to stop eating tokens without new data pressure.
```

Best theorem route if we keep deriving locally:

```text
derive the selector parent theorem:
local closed/gapped domains -> sigma_D = 0
FLRW open/nontrivial domains -> sigma_D != 0.
```

Reason:

```text
selector silence is the cleanest exact local-GR route.
profile flatness is useful,
but exact silence is stronger.
```

## Machine Artifacts

Script:

```text
scripts/local_branch_status_ledger.py
```

Run:

```text
runs/20260601-000130-local-branch-status-ledger
```

Output files:

```text
runs/20260601-000130-local-branch-status-ledger/results/source_register.csv
runs/20260601-000130-local-branch-status-ledger/results/local_stack_status.csv
runs/20260601-000130-local-branch-status-ledger/results/combined_theorem.csv
runs/20260601-000130-local-branch-status-ledger/results/residual_vector_contract.csv
runs/20260601-000130-local-branch-status-ledger/results/promotion_gates.csv
runs/20260601-000130-local-branch-status-ledger/results/allowed_forbidden_claims.csv
runs/20260601-000130-local-branch-status-ledger/results/next_targets.csv
runs/20260601-000130-local-branch-status-ledger/results/decision.csv
```
