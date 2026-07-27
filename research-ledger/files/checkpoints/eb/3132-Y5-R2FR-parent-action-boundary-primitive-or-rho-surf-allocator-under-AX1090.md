# 3132 - Parent-Action Boundary Primitive or rho_surf Allocator under AX1090

Private checkpoint. This follows 3131 by taking the hard route first:

```text
derive B_surf = d_boundary Lambda with zero compact boundary integral
```

or, if that does not close:

```text
make rho_surf executable instead of leaving it as fog.
```

## Parent-Action Attempt

The current best boundary formula shape is:

```text
B_surf^nu := sigma n_mu P_X^{mu nu} + B_ct^nu + B_ref^nu + B_exact^nu.
```

The clean exactness route would require:

```text
B_surf = d_S Lambda + h + r,
```

with:

```text
h = 0,
r = 0,
partial S = empty or corner charges included,
d_S(F epsilon) = 0,
reference fixed before readout,
source and calibration using the same boundary class.
```

That would give:

```text
DeltaC_Scal,surf = 0
rho_surf = 0.
```

## Verdict

The formula shape is real progress, but the parent primitive is not derived yet.

The blockers are not generic anymore:

```text
parent L_X is not selected,
Theta_X is not parent-owned,
P_X is not parent-owned,
counterterm/reference class is not signed,
boundary/cohomology/kernel/corner terms are not zeroed,
source/calibration boundary class is not locked.
```

So 3132 keeps:

```text
zero_promoted = false
claim_allowed = false
valid_for_claim = false
```

## Best Derivation Routes

The least-scrutiny route is:

```text
absent/nonprimitive quotient route:
X or the surface/binding variable is not an independent parent field,
so Theta_X = P_X = B_surf = 0 before readout.
```

The second-best route is:

```text
first-class vertical constraint:
Omega_flat(v_X)=delta C_X,
with Q_X = K_boundary = 0 on proper compact transformations,
while observed ADM/time/Newton charges are not killed.
```

Both routes remain conditional until the parent map is actually written.

## Executable rho_surf Allocator

Because the zero proof is not signed, 3132 converts the fallback into a strict allocator:

```text
rho_surf = sum_i rho_i
```

and:

```text
sum_i |rho_i| <= 0.3283734585378189.
```

No cancellation between unknown components is allowed.

The equal split is only a diagnostic budget:

```text
|rho_i| <= 0.04104668231722736
```

for each of eight retained components:

```text
rho_nonexact_residual,
rho_corner_joint,
rho_harmonic_cohomology,
rho_kernel_derivative,
rho_reference_counterterm,
rho_projector_readout,
rho_flux_poynting,
rho_profile_worldtube.
```

The corresponding equal-split coefficient budget is:

```text
DeltaC_i <= 0.0004974522217062501.
```

and the predicted WEP-scale eta contribution at the current delta_J bound is:

```text
eta_i <= 3.5e-16.
```

Again, equal split is not a claim. The actual rule is the sum-absolute inequality.

## Runner Artifacts

| artifact | path |
|---|---|
| input rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3132_PARENT_BOUNDARY_PRIMITIVE_INPUTS.csv` |
| proof output | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3132_PARENT_BOUNDARY_PRIMITIVE_OUTPUT.csv` |
| rho allocator | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3132_RHO_SURF_ALLOCATOR.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3132_VALIDATION.csv` |
| gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3132_PARENT_BOUNDARY_PRIMITIVE_GATE.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3132_parent_boundary_primitive_or_rho_surf_allocator.py` |

## Next Target

3133 should take one of two routes:

```text
try the absent/nonprimitive quotient proof for the surface/binding variable,
```

or:

```text
fill the first allocator component with a theorem-zero or sourced numeric value.
```

The best first allocator target is:

```text
rho_profile_worldtube,
```

because it directly answers whether the raw bulk Earth surface/binding row is even the right source profile for local WEP/orbital readout.
