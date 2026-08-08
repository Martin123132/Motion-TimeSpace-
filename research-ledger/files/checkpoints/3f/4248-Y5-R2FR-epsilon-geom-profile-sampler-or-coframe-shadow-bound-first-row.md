# 4248 - epsilon_geom profile sampler or coframe-shadow bound first row

**Status:** `EPSILON_GEOM_SAMPLER_BUILT_COFRAME_SHADOW_BOUND_FIRST_ROW_READY_NUMERIC_INPUTS_MISSING_NONCLAIM`.

## Result

The `epsilon_geom` numeric-fill route now has an executable sampler and first coframe-shadow bound:

```text
epsilon_coframe
<= C_coframe_hU*h_U_response
 + C_coframe_projector*epsilon_Q_projector
 + C_coframe_eigenchart*epsilon_eigenchart
 + C_coframe_degeneracy*epsilon_eigen_degeneracy
 + C_coframe_selector*epsilon_Pi4_selector.
```

## Current state

No candidate numeric profile exists yet, so the sampler emits `MISSING` rows and keeps `valid_for_claim=false`.

## Next target

`4249-Y5-R2FR-fill-hU-response-or-coframe-transfer-constant-first-source-row.md`
