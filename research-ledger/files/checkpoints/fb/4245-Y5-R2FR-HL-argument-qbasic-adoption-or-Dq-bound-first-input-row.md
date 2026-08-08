# 4245 - H_L argument q-basic adoption or Dq-bound first input row

**Status:** `HL_QBASIC_SUBPROFILE_ADOPTED_EXACTLY_DQ_RESIDUAL_REDUCED_TO_HPERP_FIRST_GEOM_BOUND_ROW_STAGED_NONCLAIM`.

## What changed

4245 proves the useful part of the `H_L` adoption:

```text
H_L = H_q + Hperp,
Dq_i[H_q]=0,
Dq_i[H_L]=Dq_i[Hperp].
```

So the q-basic piece is no longer part of the obstruction. The whole Dq burden is now on `Hperp`.

## First concrete row

The first component-bound row is:

```text
epsilon_geom >= ||Dq_geom[Hperp]||
```

with envelope:

```text
epsilon_geom <= epsilon_Oloc + epsilon_coframe + epsilon_projector + epsilon_wall + epsilon_Hodge_geom.
```

## Next target

`4246-Y5-R2FR-Hperp-geometry-zero-certificate-or-epsilon-geom-profile-fill.md`
