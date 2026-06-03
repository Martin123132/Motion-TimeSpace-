# 274 - Lifted C-Sector Form / Holonomy Route

Private derivation checkpoint. This is not a public local-GR, CMB, BAO, or unified-field claim.

## Purpose

Checkpoint 273 showed that the current scalar `Cperp` branch does not inherit the `J_rel` relative-exactness theorem:

```text
scalar Cperp exactness is not derived.
```

This checkpoint tries the harder route before giving up on derivation:

```text
lift the C-sector from a scalar residual into a form / connection / holonomy / boundary-class sector.
```

The aim is not to rescue the scalar branch by words. The aim is to identify whether there is a real parent-action route where local residuals become gauge/exact while the FLRW domain memory survives as a genuine nonzero class.

## Machine Artifact

Script:

```text
scripts/lifted_C_sector_form_holonomy_route.py
```

Run:

```text
runs/20260601-000092-lifted-C-sector-form-holonomy-route
```

Status:

```text
lifted_C_sector_3form_boundary_route_identified_not_parent_derived_projected_metric_remains_closure
```

Claim ceiling:

```text
lifted_C_sector_theorem_target_only_no_local_GR_or_unification_promotion
```

## Main Result

The scalar `C` branch is still not repaired.

However, the lifted route is not dead. The best current theorem target is:

```text
three-form domain memory current / boundary-class route
```

schematically:

```text
C_D[D] = N_D^{-1} integral_D J_C
```

or equivalently by a boundary potential:

```text
J_C = dB_C + J_C^{top}
```

where the local exact part can be killed by a stationary local boundary condition, while the coherent FLRW domain class can remain nonzero.

This is the first route that has the right shape:

```text
local exact residuals vanish by Stokes / presymplectic degeneracy
FLRW memory survives as a domain H^3 class
matter sees only the class scalar C_D, not arbitrary Cperp profiles
```

But it is still a theorem target, not a completed derivation.

## Route Comparison

| Route | Local residuals | FLRW memory | Verdict |
|---|---|---|---|
| scalar `Cperp` | not killed | closure only | rejected as derivation |
| 1-form connection holonomy | possible if zero-period exact shifts | possible via cycle/endpoint period | side route |
| 2-form boundary flux | possible on closed/stationary boundary | possible via boundary flux | side route |
| 3-form domain current | best match to local exactness + FLRW volume class | natural `H^3(D, partial D)` route | best current target |
| 4-form global flux | very clean local silence | possible but too rigid | possible but probably over-global |

The three-form route fits the existing corpus best because it connects to:

```text
J_M / J_rel style current language
relative cohomology boundary contract
FLRW coherent domain load
det(Q) / spatial volume exposure
```

## Conditional Theorem Shape

The possible theorem would be:

```text
Let J_C be a domain 3-form memory current on a spatial domain D with boundary partial D.
Let local residual changes satisfy delta J_C = dB_C, with B_C carrying zero primitive on stationary local boundaries.
Then delta C_D = N_D^{-1} integral_D dB_C
              = N_D^{-1} integral_partialD B_C
              = 0
for local stationary domains.
```

But in FLRW:

```text
integral_D J_C^{top} != 0
```

can survive as a coherent domain class.

That is exactly the kind of structure needed:

```text
local no-hair / PPN silence
cosmological memory response
same-domain BAO cancellation
endpoint CMB contrast possibility
```

## What Is Still Missing

The route does not yet derive the theory. It defines the contract a future parent action must satisfy:

| Missing piece | Why it matters |
|---|---|
| derive `J_C` from `Q^i_j`, coframe, or `det(Q)` | otherwise the 3-form is just a named repair field |
| derive the boundary primitive condition | otherwise local residuals may still leak into PPN |
| derive universal matter coupling to `C_D[D]` | otherwise `exp(P_D C)g` remains inserted |
| vary the domain/boundary/projector consistently | otherwise Bianchi/conservation may be hidden |
| derive `B_mem=2/27` | amplitude still closure/theorem target |
| derive `Hstar=H0` | scale lock still closure/theorem target |

## Matter-Metric Consequence

Checkpoint 267 showed:

```text
bar_g = exp(P_D C) g
```

decouples `Cperp` if it is assumed.

Checkpoint 273 showed the scalar `Cperp` sector does not derive that assumption.

This checkpoint refines the status:

```text
bar_g = exp(C_D[D]) g
```

could be derivable if `C_D[D]` is a genuine class observable of a lifted 3-form sector.

But today:

```text
projected matter metric = explicit effective closure
```

not parent-derived physics.

## Decision

The local route should not be abandoned, but the scalar route is demoted.

The live derivation target is now:

```text
derive a domain 3-form memory current J_C from the existing MTS load geometry.
```

The boss-fight condition is sharp:

```text
If J_C follows from Q^i_j / det(Q) / coframe load variation,
then the local-silence route can be promoted to a serious theorem attempt.

If J_C has to be added by hand,
then this branch remains an effective closure and must be tested empirically as such.
```

## Output Files

```text
runs/20260601-000092-lifted-C-sector-form-holonomy-route/results/source_register.csv
runs/20260601-000092-lifted-C-sector-form-holonomy-route/results/candidate_routes.csv
runs/20260601-000092-lifted-C-sector-form-holonomy-route/results/exactness_gates.csv
runs/20260601-000092-lifted-C-sector-form-holonomy-route/results/three_form_contract.csv
runs/20260601-000092-lifted-C-sector-form-holonomy-route/results/decision_gates.csv
runs/20260601-000092-lifted-C-sector-form-holonomy-route/results/route_policy.csv
runs/20260601-000092-lifted-C-sector-form-holonomy-route/results/numeric_bounds.csv
runs/20260601-000092-lifted-C-sector-form-holonomy-route/results/decision.csv
```

## Next Step

Next target:

```text
275 - J_C Three-Form Memory Current from Q / Coframe Load
```

Attempt:

```text
J_C = normalized spatial volume / load 3-form derived from Q^i_j
```

and test whether:

```text
delta J_C = dB_C
```

is a true local residual identity rather than a new closure axiom.

