# 5273 — Exact Boolean cycle-mask collapse

## Scope

Checkpoint 5272 derived the exact seven boundary surfaces. This checkpoint
uses the paired root structure to remove branch tracking from the interior
volume integral. It is private, leaves the formalization workbench
untouched, and makes no UV, local-GR, or full-MTS claim.

## Derivation

For every sourced surface, the `u` root has margin sign `sign(F)` and the
paired `v` root has margin sign `-sign(F)`. Each component's representative
pair uses the same two surfaces as its reciprocal pair. The product of the
two root-suffix parities, `p_AB`, is also the same in both roles. Therefore
the full representative-plus-reciprocal causal condition reduces to

`cycle_active <=> p_AB F_A F_B < 0`.

Five components have `p_AB=+1`. `MC15` has one `u` and one `v` root per
role, hence `p_AB=-1` and the equivalent inequality `F_A F_B>0`.

The only exception is `F_A F_B=0`, where a root lies on the unit circle.
Those are the codimension-one surfaces already derived in 5272.

## Verification

- Component laws derived: **6**.
- 5269 cycle-atlas rows: **1536**, mismatches **0**.
- 5271 topology-panel rows: **1318**, mismatches **0**.
- Random interior points: **2048**, mismatches **0**.
- Boundary surfaces audited: **7**.
- Proven hard-leg denominator lower bound: `0.0002`.

For hard legs,

`D=1+q^2-s(1-q^2)r >= 2q^2 > 0`,

so the multiplication used to derive `F` introduces no physical
denominator-zero branch in the sourced soft-energy domain.

## Acceptance gates

- `all_5269_cycle_states_match`: **PASS**
- `all_5271_panel_signatures_match`: **PASS**
- `all_component_derivations_close`: **PASS**
- `all_random_interior_root_states_match`: **PASS**
- `boundary_exceptions_are_measure_zero`: **PASS**
- `claims_locked_false`: **PASS**
- `formalization_workbench_unchanged`: **PASS**
- `hard_leg_denominator_proven_positive`: **PASS**
- `parent_5272_accepted`: **PASS**

Validation: **PASS**.

## Consequence

The volume cubature no longer needs nearest-root matching, chamber
continuation, or an interpolated occupation table. It can evaluate the six
exact inequalities pointwise. Boundary-supported distributional terms are
still a separate question and are not silently discarded if the parent
integrand contains derivatives of the mask.

## Next target

Audit the sourced weighted integrand for boundary derivatives. If none are
present, run the first topology-safe joint soft-energy and two-angle
cubature directly with these exact masks. If derivatives are present,
derive their surface-delta contribution before volume integration.
