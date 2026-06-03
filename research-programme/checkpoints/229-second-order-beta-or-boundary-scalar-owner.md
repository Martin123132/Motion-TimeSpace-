# 229 - Second-Order Beta or Boundary Scalar Owner

Private local-derivation checkpoint. This is not a public local-GR, PPN,
clock, WEP, or field-theory completion claim.

## 1. Trigger

Checkpoint 228 made the local no-slip branch sharper:

```text
delta Phi = delta Psi
```

is sufficient if compact-shell boundary stress is scalar/isotropic.

But two things remained open:

```text
derive the scalar boundary owner,
or derive the second-order beta response.
```

This checkpoint attacks the scalar boundary owner first, because it is the
cleanest route to making the checkpoint-228 no-slip condition less axiomatic.

## 2. Machine Artifact

Script:

```text
scripts/second_order_beta_or_boundary_scalar_owner.py
```

Run:

```text
runs/20260601-000046-second-order-beta-or-boundary-scalar-owner
```

Command:

```text
python scripts/second_order_beta_or_boundary_scalar_owner.py --timestamp 20260601-000046
```

Status:

```text
scalar_boundary_symmetry_owner_derived_sufficient_beta_reduced_to_vacuum_Einstein_gate_no_PPN_promotion
```

Claim ceiling:

```text
scalar_boundary_sufficient_owner_plus_beta_reduction_no_parent_local_GR_or_PPN_promotion
```

## 3. Scalar Boundary Owner

Let the compact local collar have induced boundary metric:

```text
gamma_AB.
```

The allowed boundary data are scalar shell objects:

```text
Y_boundary =
{N_D, C_coh, I_M, K, R_boundary, n^mu partial_mu phi_A, scalar memory}.
```

The sufficient boundary action is:

```text
S_boundary =
int_boundary sqrt(|gamma|) F(Y_boundary).
```

Crucial restriction:

```text
F has no tangential vector,
no tangential tensor,
no trace-free shell curvature,
no tangential J_rel shear,
no hidden angular harmonic label.
```

Then the boundary stress is:

```text
tau_AB =
-(2/sqrt(|gamma|)) delta S_boundary / delta gamma^AB.
```

On a stationary compact isotropic collar, the tangent little group permits only:

```text
tau_AB = tau gamma_AB.
```

Therefore:

```text
tau_TF_AB = 0.
```

This is the scalar-boundary owner we needed for checkpoint 228:

```text
D_AB(Phi - Psi) = 8 pi G tau_TF_AB = 0.
```

After compact matching removes homogeneous `l >= 2` slip modes:

```text
Phi - Psi = 0.
```

So the no-slip/common-mode condition is no longer just:

```text
assume delta Phi = delta Psi.
```

It is now:

```text
derive tau_TF_AB = 0 from scalar-only compact boundary symmetry.
```

That is a real improvement.

## 4. Allowed and Forbidden Boundary Terms

| term | status | local effect |
|---|---|---|
| `N_D` | allowed | trace pressure from coherent volume |
| `C_coh` / `I_M` | allowed | scalar exposure/common mode |
| `K` trace and `R_boundary` scalar | allowed | isotropic shell stress |
| `K_TF_AB` | forbidden for no-slip | can source `Phi - Psi` |
| tangential `J_rel_A` / memory shear | forbidden for no-slip | creates `l >= 2` boundary data |
| direct matter/clock coupling | forbidden for local universality | creates WEP/clock residuals |

This makes the boundary problem precise.

The programme must not merely say:

```text
the boundary is scalar.
```

It must prove:

```text
the parent field variables leave no allowed tangential shear channel on compact
stationary collars.
```

## 5. Beta Reduction

This checkpoint does not derive `beta = 1`.

It reduces the beta problem to a sharper exact gate.

For a compact spherical local system, `beta = 1` follows if:

```text
q_loc^nu = 0 outside the compact collar,
the exterior field equations reduce to Einstein vacuum,
the boundary contributes only a monopole mass renormalization,
and no X/J_rel/V_def memory hair propagates outside.
```

Then the exterior metric is Schwarzschild up to the effective mass:

```text
g_00 = -1 + 2U - 2U^2 + O(U^3),
```

so:

```text
beta = 1.
```

The important point:

```text
scalar/isotropic boundary stress is enough for first-order gamma/slip,
but beta needs the exterior vacuum-Einstein branch.
```

So beta is no longer a shapeless mystery coefficient.

It is now the same hard local theorem in sharper clothes:

```text
derive exterior q_loc = 0 and no exterior memory hair.
```

## 6. Coefficient Status After This Checkpoint

| residual | checkpoint 229 status |
|---|---|
| `gamma - 1` | stronger sufficient owner via scalar boundary symmetry |
| `Phi - Psi` | stronger sufficient owner via `tau_TF_AB = 0` |
| `G_eff/G - 1` | monopole/common-mode only; source normalization open |
| `alpha_clock` | unchanged universal metric coupling contract |
| `epsilon_matter` | unchanged universal metric coupling contract |
| `beta - 1` | reduced to exterior vacuum-Einstein/no-hair gate |

The safe local route is therefore:

```text
scalar boundary symmetry -> no slip/gamma residual;
exterior vacuum Einstein -> beta = 1;
universal metric coupling -> clock/WEP safety.
```

Only the first arrow improved in this checkpoint.

The second and third arrows are still theorem targets.

## 7. Gate Results

| gate | result |
|---|---|
| all cited local sources exist | pass |
| scalar boundary symmetry gives trace-only stress | pass |
| gamma/slip coefficient owner strengthened | pass |
| beta reduced to exact vacuum-Einstein gate | pass |
| parent scalar boundary action derived | fail |
| exterior vacuum Einstein branch derived | fail |
| local GR or PPN promoted | fail |

The pass rows are not public claims.

The fail rows are the remaining wall.

## 8. Decision

Decision:

```text
scalar_boundary_symmetry_owner_derived_sufficient_beta_reduced_to_vacuum_Einstein_gate_no_PPN_promotion
```

Meaning:

```text
the scalar-only compact boundary owner is now derived as a sufficient symmetry
theorem. If the boundary action uses only scalar shell data and no tangential
memory shear, its compact isotropic stress is trace-only, so the checkpoint-228
no-slip condition is owned at the symmetry level.
```

But:

```text
the parent theory still has to derive F(Y_boundary),
the J_rel representative,
q_loc = 0 outside the compact collar,
and the exterior vacuum-Einstein/no-hair branch.
```

Current status:

```text
local gamma/slip route improved;
beta route sharpened but not solved;
local GR still unpromoted;
PPN still unpromoted.
```

## 9. Why This Is Actually Good

This is not a knockout.

It is a clean counterpunch.

Before:

```text
common-mode leakage was a rescue assumption.
```

Now:

```text
common-mode leakage follows from scalar-only compact boundary symmetry.
```

That is exactly the kind of “make it derivable” move this programme needs.

The next remaining villain is no longer vague:

```text
prove the exterior branch is vacuum Einstein,
or prove the J_rel/local representative makes q_loc vanish outside compact
collars.
```

## 10. Next Target

Create:

```text
230-exterior-vacuum-Einstein-branch-or-Jrel-representative.md
```

Purpose:

```text
derive the exterior vacuum-Einstein/no-hair branch from q_loc = 0 and the
J_rel representative, or explicitly demote beta to a screened closure row.
```

Pass condition:

```text
r > R_shell:
q_loc^nu = 0,
T_memory^TF = 0,
T_memory^trace = 0 or pure mass renormalization,
G_mu_nu = 0,
g_00 = -1 + 2U - 2U^2 + O(U^3).
```

Fail condition:

```text
beta is treated as safe merely because gamma/slip are safe.
```
