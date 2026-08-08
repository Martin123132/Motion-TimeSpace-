# 4246 - Hperp geometry zero certificate or epsilon_geom profile fill

**Status:** `HPERP_GEOMETRY_ZERO_NOT_PARENT_SIGNED_EPSILON_GEOM_DECOMPOSED_PROFILE_ROW_REQUIRED_NONCLAIM`.

## Result

The geometry zero is not claimed. The reason is precise:

```text
A_MF_PARENT_SIGNATURE_NOT_FOUND
```

means `Hperp` could still carry a representative observed-geometry/coframe shadow.

## What improved

The live geometry residual is now decomposed:

```text
epsilon_geom
<= epsilon_Oloc
 + epsilon_coframe
 + epsilon_projector
 + epsilon_wall
 + epsilon_Hodge_geom.
```

This is the first proper profile row for the Hperp geometry channel.

## Next target

`4247-Y5-R2FR-motion-frame-no-shadow-signature-or-epsilon-geom-numeric-fill.md`
