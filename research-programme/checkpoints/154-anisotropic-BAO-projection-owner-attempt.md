# 154 - Anisotropic BAO Projection Owner Attempt

Private bridge-owner checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 153 rejected a pure `H(z)` repair as a complete owner:

```text
DH wants lower H,
but most DM rows also want lower transverse distance.
```

That sign pattern cannot be fixed by simply nudging the FLRW expansion curve. This checkpoint tests the cleaner projection idea:

```text
Can an observer/projection map separate radial and transverse BAO response
without invoking Q^nu matter-memory exchange?
```

Short answer:

```text
The projection route is still live.
A scalar redshift/clock remap has the right qualitative sign structure.
But no parent observer-map owner has been derived yet.
```

## 2. Machine Artifact

Script:

```text
research-programme\scripts\anisotropic_BAO_projection_owner_attempt.py
```

Run:

```text
research-programme\runs\20260531-235959-anisotropic-BAO-projection-owner-attempt
```

Generated:

```text
source_register.csv
projection_target_rows.csv
radial_transverse_projection_factors.csv
scalar_redshift_remap_consistency.csv
projection_model_audit.csv
owner_contract.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
anisotropic_projection_route_live_redshift_map_plausible_parent_owner_missing
```

Claim ceiling:

```text
anisotropic_BAO_projection_owner_attempt_no_bridge_promotion
```

## 3. Projection Target

The required projection amplitude is small:

```text
max required BAO projection factor = 0.015182831800200747
```

That is about a percent-level shape/projection effect, not a giant deformation.

The independent projection closure would be:

```text
D_M -> (1 + Pi_perp) D_M
D_H -> (1 + Pi_parallel) D_H
```

This can fit the target by construction, but by itself it is just a ruler patch. It only becomes physics if `Pi_perp` and `Pi_parallel` come from a parent observer/projection tensor.

## 4. Redshift/Clock Remap Test

A less ugly route is a scalar redshift map:

```text
z_true = z_obs + zeta(z)
D_M_obs = D_M(z_true)
D_H_obs = D_H(z_true) dz_true/dz_obs
```

This naturally separates transverse and radial BAO response:

```text
D_M depends on the shifted distance integral,
D_H depends on both H(z_true) and dz_true/dz_obs.
```

That means a scalar clock/redshift map can look anisotropic in BAO space without making spacetime itself anisotropic.

Machine result:

```text
4/6 paired redshifts require opposed radial/transverse signs.
scalar redshift remap max derivative mismatch = 0.005100250386681451.
```

Readout:

```text
not exact,
not derived,
but not dead.
```

This is the first bridge route that has the right kind of footwork: it can lower transverse distance while increasing radial distance through the derivative term.

## 5. Model Audit

| Model | Result | Promotion status |
|---|---|---|
| independent radial/transverse projector | exact by construction | empirical closure only |
| scalar redshift remapping | qualitative sign success | live theorem target |
| pure single-metric `H(z)` change | fails complete owner | rejected |
| `Q^nu` exchange map | possible but dangerous | deferred |

The important thing is that `Q^nu` is still not forced. The projection route has not collapsed.

## 6. Owner Contract

A real projection theorem must derive:

```text
Pi_perp(z), Pi_parallel(z)
```

or:

```text
zeta(z)
```

from a parent observer map, clock map, coframe, or projection tensor.

It must satisfy:

```text
B_mem -> 0 implies Pi_perp = Pi_parallel = zeta = 0.
```

It must predict together:

```text
D_M/r_d,
D_H/r_d,
D_V/r_d,
SN distance redshifts,
cosmic chronometer H(z),
and local/PPN silence.
```

If it only fixes BAO while breaking SN or H(z), it is not a bridge. It is a patch.

## 7. Decision

Current fair status:

```text
anisotropic/projective BAO route live;
parent owner missing;
Q^nu still deferred.
```

Next checkpoint:

```text
155-redshift-projection-clock-map-owner.md
```

Target:

```text
derive zeta(z) from the MTS clock/observer map,
or demote projection to closure-only and return to Q^nu / full Boltzmann inference.
```

This is the neat route if it works: win the bridge round with footwork, not with a haymaker that risks knocking out local GR.
