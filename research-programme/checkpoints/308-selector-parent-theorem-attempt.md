# 308 - Selector Parent Theorem Attempt

Private derivation checkpoint. This is not a public local-GR, PPN, cosmology, galaxy, CMB, or parent-field-theory claim.

## Purpose

Checkpoint 307 said the cleanest local-GR route is:

```text
derive the selector parent theorem:
local closed/gapped domains -> sigma_D = 0,
FLRW open/nontrivial domains -> sigma_D != 0.
```

This checkpoint tries to write that theorem without smuggling in:

```text
"because we need local GR."
```

Short answer:

```text
the selector theorem has a clean spectral/topological route,
but the parent action has not closed it yet.
```

That is not a dead end.

It is a sharper shopping list.

## Selector Objects

Define the MTS-projected boundary spectral density:

```text
rho_MTS,D(omega).
```

This must not be generic environmental dissipation.

It has to be:

```text
rho_MTS,D(omega)
= rho[P_MTS B_D, P_MTS B_D](omega),
```

where `P_MTS` projects onto the MTS boundary/memory channel.

Then define:

```text
b_D = lim_{omega -> 0+} rho_MTS,D(omega)/omega,
c_D = ||Pi_rel [J_B]_D||.
```

The hard selector is:

```text
sigma_D = Theta(b_D) Theta(c_D).
```

A smooth runner version is:

```text
sigma_D = b_D c_D / (b_D c_D + mu_*^2).
```

## Conditional Parent Theorem

The theorem we can prove conditionally is:

```text
If a laboratory-local domain is closed/gapped in the MTS-projected boundary channel,
then rho_MTS,D(omega)=0 for 0<omega<omega_gap,
so b_D=0.
```

Also:

```text
If the local relative boundary-current class is exact/trivial,
then Pi_rel[J_B]_D=0,
so c_D=0.
```

Therefore:

```text
sigma_D = Theta(b_D) Theta(c_D) = 0.
```

So:

```text
Gamma_D = N_D = Lambda_D = 0
```

in the selector-controlled open sector.

That gives exact local open-sector silence.

For FLRW:

```text
rho_MTS,FLRW(omega) = eta omega + o(omega), eta > 0
```

implies:

```text
b_FLRW = eta > 0.
```

If:

```text
||Pi_rel[J_B]_FLRW|| > 0,
```

then:

```text
sigma_FLRW != 0.
```

So the selector can, in principle, silence laboratory-local domains while leaving the cosmological branch active.

## What Was Derived

These implications are now clean:

| Premise | Result | Status |
|---|---|---|
| projected local spectral gap | `b_D=0` | proved from premise |
| local relative triviality | `c_D=0` | proved from premise |
| `b_D=0` or `c_D=0` | `sigma_D=0` | proved from selector |
| FLRW Ohmic projected bath | `b_FLRW>0` | proved from premise |
| FLRW nontrivial relative class | `c_FLRW>0` | proved from premise |
| `b_FLRW>0` and `c_FLRW>0` | `sigma_FLRW != 0` | proved from selector |

So the mathematics of the selector is not the weak point.

The weak point is ownership of the premises.

## What Failed

The parent theory has not yet derived:

```text
rho_MTS,D excludes ordinary EM/environmental baths,
local domains are gapped/closed in that projected channel,
local relative boundary-current classes are trivial,
FLRW has an Ohmic/gapless projected boundary bath,
FLRW has a nontrivial relative boundary-current class.
```

Without those, this is still a theorem target.

## No-Go Checks

| Claim | Result | Reason |
|---|---|---|
| generic local dissipation can define `b_D` | fail | warm ordinary labs would activate `sigma_D` |
| bounded systems automatically have `b_D=0` | fail | bound systems can radiate or contain gapless ordinary fields |
| relative triviality alone is enough | partial | it can kill trace activation, but not all bath/noise language alone |
| FLRW activity follows from nonzero `H` alone | fail | expansion is not the same as a boundary spectral density/class |
| black holes and galaxies are covered automatically | fail | horizons and extended bound domains need separate treatment |

## Domain Consequences

| Domain | Selector Result | Status |
|---|---|---|
| stationary laboratory-local domain | `sigma_D=0` if projected gap/trivial class hold | conditional silence |
| ordinary warm lab with EM bath | safe only if EM bath is projected out | projector required |
| time-dependent radiating local system | hard selector safe if `c_D=0`; smooth selector needs runner | edge/local-bound case |
| black-hole or local horizon domain | may activate | separate horizon branch |
| galaxy/cluster extended bound domain | must not be erased | empirical/domain branch |
| FLRW coherent domain | active if Ohmic bath and nontrivial class hold | conditional cosmology activity |

## Promotion Gates

| Gate | Result | Meaning |
|---|---|---|
| source paths exist | pass | attempt traceable |
| selector objects defined | pass | theorem target is well-posed |
| conditional local silence proved | conditional pass | gap/trivial class imply `sigma_D=0` |
| conditional FLRW activity proved | conditional pass | Ohmic bath/nontrivial class imply `sigma_FLRW != 0` |
| generic bath problem closed | fail | need `P_MTS` projector theorem |
| local gap parent-derived | fail | no action proof of projected local gap |
| local relative triviality parent-derived | fail | no action proof of local trivial class |
| FLRW Ohmic bath parent-derived | fail | cosmology activity remains contract |
| FLRW relative class parent-derived | fail | memory activation remains contract |
| edge cases closed | fail | horizons/galaxies/time-dependent local systems remain separate |
| local GR promoted | fail | selector theorem is not parent-closed |
| `B_mem` parent-derived | fail | `2/27` remains empirical closure/theorem target |

## Decision

Decision:

```text
selector_parent_theorem_conditional_spectral_topological_route_not_parent_closed
```

Claim ceiling:

```text
conditional_selector_theorem_no_local_GR_or_PPN_promotion
```

Meaning:

```text
we can now say exactly what would derive local silence,
but we cannot yet say the parent action actually forces it.
```

Boxing-score version:

```text
We found the footwork pattern.
If MTS can prove its local boundary channel is gapped/trivial,
the local punch misses cleanly.
But the trainer still has to prove the fighter actually moves that way,
not just that the move would work.
```

## Next Step

The next theorem target is:

```text
define and derive the MTS boundary projector P_MTS.
```

Reason:

```text
without P_MTS,
ordinary local EM/environmental baths can fake the boundary bath
and accidentally activate the selector.
```

So the next exact contract is:

```text
rho_MTS,D = rho[P_MTS B_D, P_MTS B_D],
P_MTS kills ordinary local EM/matter bath channels,
P_MTS keeps the coherent cosmological memory boundary channel.
```

If this cannot be derived, the selector route remains closure-only and the better move is empirical holdout testing.

## Machine Artifacts

Script:

```text
scripts/selector_parent_theorem_attempt.py
```

Run:

```text
runs/20260601-000131-selector-parent-theorem-attempt
```

Output files:

```text
runs/20260601-000131-selector-parent-theorem-attempt/results/source_register.csv
runs/20260601-000131-selector-parent-theorem-attempt/results/theorem_definitions.csv
runs/20260601-000131-selector-parent-theorem-attempt/results/parent_contracts.csv
runs/20260601-000131-selector-parent-theorem-attempt/results/conditional_proof.csv
runs/20260601-000131-selector-parent-theorem-attempt/results/domain_tests.csv
runs/20260601-000131-selector-parent-theorem-attempt/results/no_go_tests.csv
runs/20260601-000131-selector-parent-theorem-attempt/results/promotion_gates.csv
runs/20260601-000131-selector-parent-theorem-attempt/results/next_targets.csv
runs/20260601-000131-selector-parent-theorem-attempt/results/decision.csv
```
