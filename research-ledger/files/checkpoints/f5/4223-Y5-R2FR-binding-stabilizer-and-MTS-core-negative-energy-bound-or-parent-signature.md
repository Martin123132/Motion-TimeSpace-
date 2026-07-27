# 4223 - Binding/Stabilizer And MTS-Core Negative Energy Bound Or Parent Signature

**Status:** `BINDING_AND_MTS_CORE_SIGN_REDUCED_TO_CANONICAL_ACTION_BOUND_GAMMA_BOUNDARY_OR_BATH_AND_BINDING_FRACTION_ROWS_NONCLAIM`.

## Main move

This checkpoint does not just say "binding and core signs are missing." It derives the exact sign gate:

```text
H_psi = (1/2c^2) psi_dot^2 + (1/2)|grad psi|^2 + (lambda/n)|psi|^n + H_gamma_boundary.
```

`gamma psi psi_dot` is boundary-like for fixed `gamma`; if it is intended as physical damping, it is an open-system/bath row.

## Bound rows staged

- `E_MTS_core_neg_abs <= (max(0,-lambda)/n) int |psi|^n + E_gamma_bath_or_open_abs + E_signature_mismatch_abs`
- `E_binding_stabilizer_neg_abs <= beta_bind E_visible_rest + E_stab_neg_abs`

## Decision

No local-GR/Newton claim is made. The route is sharper, but the source rows for `lambda`, `gamma`, `beta_bind`, and stabilizer/core mismatch values are still missing.

Next: `4224-Y5-R2FR-lambda-gamma-core-action-sign-and-binding-bound-source-row.md`.
