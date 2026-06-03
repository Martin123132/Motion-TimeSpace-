# 296 - Positive Coarse-Graining Parent Action Attempt

Private derivation checkpoint. This is not a public cosmology, local-GR, CMB, or parent-field-theory claim.

## Purpose

Checkpoint 295 gave the arrow:

```text
Phi_tau=P_iso+exp(-gamma tau)(I-P_iso),
```

and showed:

```text
gamma>0 gives 3 -> 1.
```

The blocker was:

```text
derive gamma>=0 and identify tau with physical parent time.
```

This checkpoint asks:

```text
can a parent action own positive coarse-graining time?
```

Short answer:

```text
only if the parent includes an open/Onsager/influence sector.
```

A plain reversible action does not do it.

## Reversible Action No-Go

An ordinary conservative parent action gives reversible Euler-Lagrange or Hamiltonian flow.

Such a flow is normally:

```text
invertible,
time-reversal compatible,
phase-volume preserving in Hamiltonian form.
```

But the endpoint arrow needs:

```text
resolved axis information -> scalar trace information,
```

with the asymptotic map:

```text
Phi_infinity=P_iso.
```

That limit loses two anisotropic directions.

So:

```text
a plain reversible action cannot by itself be the fundamental owner
of the irreversible projector arrow.
```

It needs extra structure:

```text
coarse-graining,
boundary/environment modes,
entropy/contact structure,
or doubled influence dynamics.
```

## Onsager Route

Let:

```text
R = R_aniso = I-P_iso.
```

Define a free-energy-like residual:

```text
F(q)=1/2 <q, R q>.
```

An Onsager gradient flow is:

```text
dq/dtau = -gamma R q.
```

Then:

```text
dF/dtau = -gamma ||R q||^2.
```

If:

```text
gamma >= 0,
```

then:

```text
dF/dtau <= 0.
```

The entropy production form is:

```text
sigma = gamma ||R q||^2 >= 0.
```

This exactly supports the checkpoint-295 semigroup:

```text
Phi_tau=P_iso+exp(-gamma tau)R.
```

So the arrow can be made clean:

```text
positive mobility -> positive coarse-graining time -> 3 -> 1.
```

But:

```text
positive mobility is still a parent assumption unless derived.
```

## Influence-Action Route

The strongest field-theory-shaped contract is a doubled/open effective action:

```text
S_eff = int q_a (dot q_r + Gamma R q_r)
      + (i/2) int q_a N q_a.
```

Here:

```text
q_r = resolved axis-load field,
q_a = response/difference field,
N = noise kernel.
```

If:

```text
N >= 0
```

and a fluctuation-dissipation/KMS-like relation holds:

```text
N = 2 T Gamma,
T >= 0,
```

then:

```text
Gamma >= 0.
```

That gives the desired arrow:

```text
dot q_r = -Gamma R q_r.
```

This is the best candidate for parent ownership because it is field-theoretic.

But it requires:

```text
an explicit boundary/environment sector,
a state condition,
and a positivity theorem for the noise kernel.
```

Those are not yet in the MTS parent action.

## Parent Contract

To promote this route, the future parent action must supply:

| Contract item | Required form | Status |
|---|---|---|
| resolved field | `q_r` in axis-load sector | kinematic only |
| response field | `q_a` enforcing `dot q_r + Gamma R q_r=0` | contract only |
| positive noise kernel | `N>=0` | not derived |
| fluctuation-dissipation relation | `N=2T Gamma`, `T>=0` | not derived |
| Ward trace coupling | only `P_iso q_r` sources FLRW stress | not derived |
| local silence filter | local domains have `Gamma=0` or suppressed charge | not derived |

This is a useful contract.

It is not yet a derivation.

## Gates

| Gate | Result | Meaning |
|---|---|---|
| source paths exist | pass | audit traceable |
| ordinary reversible action derives arrow | fail | plain action route rejected |
| Onsager flow derives positive `gamma` | conditional pass | works if positive mobility is parent-owned |
| influence action can parent-own `gamma` | conditional pass | works with positive noise/FDT sector |
| positive mobility parent-derived | fail | not in current parent stack |
| physical time identified | fail | `tau` still coarse-graining time |
| `B_mem` derived | fail | conditional chain only |
| local GR promoted | fail | no `q_loc`/PPN result |

## Decision

Decision:

```text
positive_coarse_graining_time_derivable_only_with_open_onsager_sector
```

Meaning:

```text
the arrow can be parent-owned only if MTS includes an explicit open-boundary,
Onsager, contact, or influence-functional sector.
```

What improved:

```text
we now know exactly what parent-time structure must exist.
```

What did not improve:

```text
the existing parent stack does not yet contain that structure.
```

Therefore:

```text
B_mem=2/27 remains a locked empirical closure/theorem target.
```

Boxing-score version:

```text
The arrow can be thrown cleanly,
but only with an open-system stance.
If we insist on plain reversible footwork,
the punch cannot legally land.
```

## Machine Artifacts

Script:

```text
scripts/positive_coarse_graining_parent_action_attempt.py
```

Run:

```text
runs/20260601-000119-positive-coarse-graining-parent-action-attempt
```

Output files:

```text
runs/20260601-000119-positive-coarse-graining-parent-action-attempt/results/source_register.csv
runs/20260601-000119-positive-coarse-graining-parent-action-attempt/results/parent_routes.csv
runs/20260601-000119-positive-coarse-graining-parent-action-attempt/results/onsager_calculation.csv
runs/20260601-000119-positive-coarse-graining-parent-action-attempt/results/field_theory_contract.csv
runs/20260601-000119-positive-coarse-graining-parent-action-attempt/results/ordinary_action_no_go.csv
runs/20260601-000119-positive-coarse-graining-parent-action-attempt/results/gate_results.csv
runs/20260601-000119-positive-coarse-graining-parent-action-attempt/results/decision.csv
```

## Next Step

There are now two honest paths.

Path A:

```text
construct an explicit open-boundary/influence parent sector
and test whether it can also give Ward trace coupling and local silence.
```

Path B:

```text
formally classify the 2/27 derivation stack as a closure contract:
excellent structure, not parent-derived yet.
```

Recommended next:

```text
write the 2/27 derivation-stack ledger.
```

Reason:

```text
we need a single brutal page showing exactly which pieces are derived,
which are conditional,
and which remain closure.
```
