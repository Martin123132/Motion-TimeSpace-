# 278 - Admissible Domain Class / Boundary Current Owner

Private derivation checkpoint. This is not a public local-GR, CMB, BAO, or unified-field claim.

## Purpose

Checkpoint 277 derived the free-boundary Euler equation for `C_coh[D]`, but found a degeneracy:

```text
FLRW domains are stationary but not unique.
stationary local domains are silent but not selected.
```

This checkpoint asks whether the degeneracy can be restricted without adding:

```text
a fitted smoothing length
a surface-tension wall stress
a quiet-domain hand choice
```

The attempted route is:

```text
admissible boundary variations are those preserving a relative memory class.
```

## Machine Artifact

Script:

```text
scripts/admissible_domain_class_boundary_current_owner.py
```

Run:

```text
runs/20260601-000096-admissible-domain-class-boundary-current-owner
```

Status:

```text
relative_current_restricts_admissible_variations_but_does_not_select_physical_domain_class
```

Claim ceiling:

```text
admissible_variation_contract_sharpened_no_domain_selection_or_local_GR_promotion
```

## Relative Current Setup

Use the relative pair:

```text
J_rel = (j_3, b_2)
```

with relative closure:

```text
d_rel J_rel =
(
  d j_3,
  i* j_3 - d_boundary b_2
)
= 0.
```

Define the relative memory charge:

```text
Q_rel[D] =
integral_D j_3
- integral_boundaryD b_2.
```

The admissibility rule is:

```text
delta_eta Q_rel[D] = 0.
```

Meaning:

```text
boundary motions are gauge/admissible only if they preserve the relative memory class.
```

## What This Fixes

Checkpoint 277 allowed arbitrary boundary displacement `eta`.

That was too broad. It made the Euler condition degenerate because many boundaries were stationary.

The relative-current rule narrows the variation space:

```text
not every eta is admissible;
only class-preserving eta are gauge-like.
```

Equivalently, a moving-boundary flux must be absorbed by boundary exchange:

```text
i_eta j_3 =
delta_eta b_2 + d_boundary gamma_1
```

on `boundary D`.

This is a real improvement:

```text
the degeneracy is no longer arbitrary boundary calculus.
```

It becomes:

```text
which relative class / representative does the parent theory select?
```

## Branch Readout

| Branch | Relative class | Status |
|---|---|---|
| stationary local | `Q_rel = 0` | conditional silence, not selection |
| FLRW | nonzero expansion class | conditional nonzero branch |
| tracefree shear | no scalar class change if purely tracefree | conditional |
| collapse / merger | possible class-changing event | open |
| galaxy empirical pillar | kept separate from scalar local silence | open |

The rule keeps the good split:

```text
local stationary class trivial
FLRW expansion class nontrivial
```

but still does not derive why those are the physical classes.

## What Still Fails

The action can formally impose:

```text
d_rel J_rel = 0
```

using a multiplier.

But that does not select:

```text
the physical representative b_2
the initial relative class Q_rel
the event source law for class changes
the normalization of the FLRW expansion class
u3
B_mem
the matter coupling
```

So the result is:

```text
closure/admissibility can be owned formally;
representative selection is still not derived.
```

## Decision

This is a useful narrowing, but not a promotion.

The route has improved from:

```text
choose a quiet domain
```

to:

```text
allow only relative-class-preserving boundary variations
```

That is much more respectable. It is not a fitted smoothing rule and it does not add a surface wall.

But it does not yet answer:

```text
why this local system carries the trivial class
why this FLRW domain carries the nonzero class
why the representative is the one used by matter
```

So:

```text
the Euler degeneracy is restricted, not solved.
```

## Output Files

```text
runs/20260601-000096-admissible-domain-class-boundary-current-owner/results/source_register.csv
runs/20260601-000096-admissible-domain-class-boundary-current-owner/results/relative_current_objects.csv
runs/20260601-000096-admissible-domain-class-boundary-current-owner/results/admissibility_conditions.csv
runs/20260601-000096-admissible-domain-class-boundary-current-owner/results/degeneracy_tests.csv
runs/20260601-000096-admissible-domain-class-boundary-current-owner/results/branch_readout.csv
runs/20260601-000096-admissible-domain-class-boundary-current-owner/results/gate_results.csv
runs/20260601-000096-admissible-domain-class-boundary-current-owner/results/decision.csv
```

## Next Step

Next target:

```text
279 - Representative Selection / Boundary Polarization No-Go
```

Attempt:

```text
test whether a boundary polarization Pi(C_coh) can select the local-zero / FLRW-nonzero representative
without becoming a new arbitrary selector function.
```

Acceptance condition:

```text
Pi(C_coh) must be forced by the parent action or symmetry.
```

If not:

```text
the local branch should be ledgered as a disciplined effective closure and moved toward empirical/local-bound tests.
```

