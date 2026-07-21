# 4973 - C3 fixed-point form factor and finite-anchor verdict

Marker: `MTS_4973_C3_FIXED_POINT_FORM_FACTOR_KERNEL`.

Formal marker: `PPC4161_C3_FORM_FACTOR_KERNEL_NO_GO_4973`.

> **Checkpoint 4974 correction:** the `Gamma^(4)` plus
> `Gamma^(3)-Gamma^(3)` topology cited below is the source's second metric
> response for curvature-squared form factors. The `C3` calculation requires
> the third response: `Gamma^(5)`, mixed `Gamma^(3)/Gamma^(4)`, and
> `Gamma^(3)^3`. The characteristic and endpoint-null theorem in this file
> remain valid; only its proposed kernel assembly order is superseded.

Status: private source-executed derivation checkpoint. No GitHub action and no
complete-amplitude, exact-all-operator-GR, or full-MTS claim.

## 1. Decision

Checkpoint 4973 does not repeat the local Wilson flow. It constructs the
momentum-dependent equation that the missing Weyl-cubic form factor must obey,
imposes its ultraviolet and infrared conditions, projects the exact two-loop
remainders directly, and then decides whether the finite anchor can be read
from the information already retained.

The result is two-sided:

1. on the quasi-local ultraviolet branch, the fixed-point `C3` form factor is
   unique once its full momentum kernel is known;
2. the present local beta, physical logarithmic slope, and factor-ten helicity
   identity do not determine that kernel or its finite integral.

This is proved constructively rather than inferred from a missing-file audit.
An explicit family of kernels preserves every currently known endpoint and
helicity condition while shifting `delta_c_fin` by an arbitrary amount.

The finite constant therefore cannot be calculated from the current
zero-momentum parent plus endpoint data. The next valid routes are sharply
limited to:

```text
derive the full parent fluctuation C3 kernel in one declared scheme;
or
retain one explicit matched physical scale lambda.
```

## 2. Canonical C3 flow

Let the dimensionful on-shell Weyl-cubic form factor be
`f_C3,k(s,t,u)`, with `u=-s-t`. Since a cubic curvature operator has mass
dimension six in four dimensions,

```text
[f_C3,k]=-2.
```

Define

```text
x=s/k^2,
y=t/k^2,
F_k(x,y)=k^2 f_C3,k(k^2 x,k^2 y),
H_C3,k(x,y)=k^2 beta_f(k;k^2 x,k^2 y).
```

The chain rule gives the exact dimensionless flow

```text
partial_lnk F_k
  =2F_k+2x partial_x F_k+2y partial_y F_k+H_C3,k.
```

At a fixed point,

```text
(1+x partial_x+y partial_y)F_*(x,y)=-H_*(x,y)/2.
```

This is the cubic analogue of the source-acquired quadratic form-factor PDE,
with the additional `+F_*` term fixed by the `-2` canonical dimension. The
runner verifies the equation symbolically.

## 3. Exact characteristics and ultraviolet boundary

Along a fixed scattering-angle ray

```text
x=rho,
y=z rho,
z=t/s,
```

the fixed-point equation becomes

```text
d[rho F_*(rho,z rho)]/d rho=-H_*(rho,z rho)/2.
```

Its exact general solution is

```text
F_*(rho,z rho)
  =C(z)/rho-[1/(2rho)] integral_0^rho H_*(v,zv) dv.
```

The homogeneous mode has the dimensionful form

```text
f_hom(s,t)=C(t/s)/s.
```

It is therefore an inverse-momentum nonlocal interaction. If the parent
fixed point is required to be quasi-local and `H_*` is finite at the origin,
regularity forces

```text
C(z)=0.
```

Under that explicit condition the form factor is unique once `H_*(x,y)` is
known. If inverse-Laplacian fixed-point modes are admitted, `C(z)` remains a
boundary function and uniqueness is not claimed. This distinction is kept
explicit because the acquired form-factor literature allows nonlocal fixed
points in principle.

## 4. Endpoint-silent kernel family

The current parent supplies the zero-momentum local beta and checkpoint 4972
supplies the physical logarithmic endpoint. To test whether those endpoints
fix the finite integral, set

```text
x=Q^2/k^2,
dlnk=-dx/(2x),
Delta K_a(x)=a x/(1+x)^2.
```

This deformation obeys

```text
Delta K_a(0)=0,
Delta K_a(infinity)=0.
```

It therefore changes neither the local beta nor the asymptotic logarithmic
slope. Nevertheless,

```text
integral_(k=infinity)^(k=0) Delta K_a(Q^2/k^2) dlnk
  =-(a/2) integral_0^infinity dx/(1+x)^2
  =-a/2.
```

Embedding the same deformation as `P_h Delta K_a` in each helicity preserves
the exact `P_pppp/P_mppp=10` C3 identity. Thus even the two-helicity gate does
not remove this finite direction.

Rows `a=-2,-1,0,1,2` are executed in
`C3_kernel_null_deformation.csv`; they shift the finite conversion by
`+1,+1/2,0,-1/2,-1` while leaving both endpoints exactly unchanged. This is
a constructive non-identifiability theorem for the retained data, not an
assumption that the missing kernel is zero.

## 5. Direct two-loop remainder attempt

The stronger alternative was tested before rejecting the finite extraction:
perhaps the exact Abreu two-loop remainders already contain a universal
finite `C3` shift.

At the declared physical point

```text
s=1,
t=u=-1/2,
stu=1/4,
```

the exact local projectors are

```text
P_pppp=-15,
P_mppp=-3/2,
P_pppp=10 P_mppp.
```

After setting `c_R3=c_GB=0`, division of each known Einstein loop remainder
by its local `C3` projector gives

```text
delta_c_app,pppp
  =-117617/1296000+13 ln(2)/3600+i pi/1800
  =-0.088250826539336+0.001745329251994 i,

delta_c_app,mppp
  =-191 ln(2)/40+113 pi^2/69120+1799/1152
   +3709 ln(2)^2/1080-3709 i pi ln(2)/540+1147 i pi/240
  =-0.0820104270873662+0.0574045033625900 i.
```

They are not equal. Equivalently, the coupling-free combination

```text
R_pppp-10 R_mppp
  =0.0936059917795473+0.834887611658935 i
```

is nonzero. The exact remainders therefore contain helicity-dependent
nonlocal cuts and finite functions; they cannot be relabelled as one local
regulator-conversion constant.

This test also protects the known finite `117617` all-plus term from being
mistaken for an MTS Wilson coefficient.

## 6. Exact finite-scheme orbit

Write either helicity amplitude as

```text
A_h=P_h c+L_h.
```

For any finite number `zeta`, the transformation

```text
c -> c+zeta,
L_h -> L_h-P_h zeta
```

leaves every `A_h` unchanged. The runner verifies this identity independently
for `++++` and `-+++`. The physical amplitudes and their beta functions cannot
select a Wilsonian-to-HV finite convention without either calculating both
sides in one common scheme or supplying one matched observable.

The single remaining constant found in checkpoint 4972 is therefore exactly
the expected finite-renormalization orbit; it is not a missing algebraic
manipulation of the known amplitudes.

## 7. Source result

Three primary source packages were acquired and hashed:

- arXiv:2605.29159 derives full momentum-dependent background form factors at
  quadratic curvature order and gives the required `Gamma_k^(3)` plus
  `Gamma_k^(4)` fluctuation-kernel topology, but explicitly leaves the full
  fluctuation form-factor system unsolved;
- arXiv:2210.16072 states that four-field form factors generically have six
  independent arguments and that two-to-two graviton scattering requires the
  effective action through quartic curvature order;
- arXiv:0911.1168 supplies the generic 29-invariant third-order nonlocal
  heat-kernel basis, but not the parent-specific dressed graviton, ghost,
  motion, regulator, and helicity projection needed here.

Consequently the source hunt did not discover a hidden ready-made MTS kernel.
It did identify the exact object that has to be built:

```text
H_C3,k = P_C3 [tadpole(Gamma_k^(4),Gamma_k^(2))
               + bubble(Gamma_k^(3),Gamma_k^(2),Gamma_k^(3))]
```

with the selected parent regulator, gauge, ghost, motion, matter thresholds,
and both physical helicity projectors retained.

## 8. Claim boundary

```text
C3 canonical form-factor flow             = derived;
fixed-angle characteristic solution       = exact;
quasi-local homogeneous-mode removal      = conditional proof;
uniqueness given the full kernel           = conditional proof;
local and logarithmic endpoints            = retained exact;
endpoint-silent finite deformation         = exact counterexample;
direct two-loop finite remainder attempt   = executed and rejected;
finite scheme orbit                        = exact;
delta_c_fin from current local data        = not identifiable;
delta_c_fin=0                              = source prescription only;
leading local GR/Newton/Maxwell branch     = retained;
exact all-operator compact GR              = false;
full MTS                                   = false.
```

## 9. Next calculation

Checkpoint 4974 should not perform another source inventory. It should start
assembling the actual fluctuation kernel from the parent objects already
derived:

1. lock one background split, gauge, ghost operator, and regulator;
2. assemble the complete parent `Gamma_k^(2)` including the motion Hessian;
3. differentiate the retained action to `Gamma_k^(3)` and `Gamma_k^(4)`;
4. project the two loop topologies onto the on-shell `C3` helicity basis;
5. test whether the resulting kernel reproduces both 4972 endpoint slopes;
6. integrate the finite interior only after those tests pass.

If the parent action cannot supply these vertices, retain one explicit
`lambda`; do not manufacture `delta_c_fin=0` as a theorem.

## 10. Outputs

- `post-checkpoint-work/scripts/Y5_R2FR_4973_C3_fixed_point_form_factor_kernel.py`
- `post-checkpoint-work/source-intake/functional_rg/4973/C3_fixed_point_characteristics.csv`
- `post-checkpoint-work/source-intake/functional_rg/4973/C3_kernel_null_deformation.csv`
- `post-checkpoint-work/source-intake/functional_rg/4973/C3_Abreu_finite_remainder_projection.csv`
- `post-checkpoint-work/source-intake/functional_rg/4973/C3_form_factor_source_requirements.csv`
- `post-checkpoint-work/source-intake/functional_rg/4973/C3_fixed_point_form_factor_kernel_results.json`

The calculation passes `23/23` internal checks. The independent checkpoint
validator passes `21/21` checks in
`post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4973_VALIDATION.csv`,
SHA256 `174f0a8964f211825da2bf6a78d25d74b85a6f1996deffb3f90373f7e6bf4d3c`.
