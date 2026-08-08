# 4247 - motion-frame no-shadow signature or epsilon_geom numeric fill

**Status:** `MOTION_FRAME_NOSHADOW_NOT_PARENT_SIGNED_EPSILON_GEOM_NUMERIC_FILL_CONTRACT_READY_NONCLAIM`.

## Result

No-shadow is not adopted. The source-backed reasons are:

```text
A_MF_PARENT_SIGNATURE_NOT_FOUND,
Palatini_EH_forced_by_A_MF_alone = false,
selector_assumptions_parent_derived = false,
bulk owner-connection route failed at the solder map.
```

## What improved

`epsilon_geom` is now a numeric-fill contract, not just a symbol:

```text
epsilon_geom_L1
= epsilon_Oloc
+ epsilon_coframe
+ epsilon_projector
+ epsilon_wall
+ epsilon_Hodge_geom.
```

The template rows are intentionally `valid_for_claim=false`.

## Next target

`4248-Y5-R2FR-epsilon-geom-profile-sampler-or-coframe-shadow-bound-first-row.md`
