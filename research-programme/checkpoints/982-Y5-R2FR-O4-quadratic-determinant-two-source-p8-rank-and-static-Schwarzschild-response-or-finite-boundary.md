# 4966 - O4 quadratic determinant, p8 source rank and static response

Marker: `MTS_4966_O4_P8_RANK_STATIC_RESPONSE`.

Formal marker: `PPC4161_O4_P8_RANK_STATIC_RESPONSE_4966`.

Date: `2026-07-13`.

Status: private analytic, source-locked and executable checkpoint. This is a
direct continuation of 4965. It derives the first `O4` contribution to the
complete two-coordinate Ricci-flat `p8` target, proves that the two known
motion-sector source directions have rank two, and calculates the two static
spherical response weights rather than setting them to unity. The result
closes a structural source-rank problem but not the independent finite `p8`
matching boundary. Exact all-operator compact GR and full MTS remain false.

## 1. The physical O4 normalization

The source-locked scalar action and Hessian are

```text
S_psi = integral sqrt(-g)
  [-Z_psi (nabla psi)^2/2-u_O4 Q (nabla psi)^2-m_raw^2 psi^2/2],

Q=C_mnrs C^mnrs,

Delta_O4=-nabla_mu[(Z_psi+2u_O4 Q)nabla^mu]+m_raw^2.
```

After `phi=sqrt(Z_psi) psi`, define

```text
w_O4=u_O4/Z_psi,
m_psi^2=m_raw^2/Z_psi,

Delta_O4=-nabla_mu[(1+2w_O4 Q)nabla^mu]+m_psi^2.
```

The functional trajectory uses

```text
utilde_O4=k^4 w_O4,
g=k^2 G_N.
```

Consequently the Planck-normalized physical portal is the ratio

```text
U4 = w_O4/l_P^4
   = utilde_O4/g^2
   = W_O4,
```

not the fixed-point coordinate `utilde_O4*` by itself. The converged `N=8`
GR-connected endpoints are

```text
dynamic eta_N:    U4=-3.3225249561681114,
reference eta_N0: U4=-3.3224177636400554.
```

Both schemes therefore give a finite nonzero `U4`. Their relative spread is
about `3.23e-5`. This locks the coefficient used below without converting the
UV fixed-point number into a dimensionful Wilson coefficient by hand.

## 2. Linear O4 does not source the derivative-free p8 basis

On a locally covariantly constant `Q` patch, let

```text
z=1+2w_O4 Q,
Delta_z=-z Box+m_psi^2.
```

The exact constant-`z` heat-kernel scaling is

```text
Tr exp(-s Delta_z)
 =(4pi s)^-2 exp(-s m_psi^2)
   sum_n s^n z^(n-2) a_n.
```

The only linear `O4` route to a derivative-free `p8` term is `Q a_2`. Its
weight is `z^0`, so its derivative with respect to `w_O4 Q` vanishes exactly.
Checkpoint 4965 proves that the complete parity-even derivative-free target
is `{Q^2,Y^2}`, with `Y=C.Ctilde`, and that derivative pure-gravity
coordinates begin above `p8`. The scalar `a_2` coefficient is parity even and
quadratic in curvature, so one `Q` insertion can only address `Q^2`; it cannot
generate `Y^2`. Hence

```text
Delta B_C at O(w_O4) and p8 = 0,
Delta B_t at O(w_O4) and p8 = 0.
```

There is a separate linear `p4` threshold proportional to
`w_O4 m_psi^4 Q`. It belongs to the four-derivative quotient treated at 4964
and is not silently reclassified as a `p8` source.

## 3. Quadratic O4 determinant source

At second order in `w_O4`, the Euclidean determinant gives

```text
Gamma_psi=1/2 Tr ln[p^2+m_psi^2+2w_O4 Q p^2],

Gamma_psi|Q2
 =-w_O4^2 Q^2
   integral d^d p/(2pi)^d p^4/(p^2+m_psi^2)^2.
```

Using

```text
p^4/(p^2+m^2)^2
 =1-2m^2/(p^2+m^2)+m^4/(p^2+m^2)^2
```

and dimensional regularization, the scaleless first integral vanishes and

```text
integral p^4/(p^2+m^2)^2
 =3m^4/(16pi^2 epsilon)+finite.
```

After MS-bar subtraction, the fixed logarithmic coefficient is

```text
Delta Gamma_Q2^log
 =[3w_O4^2 m_psi^4/(16pi^2)]
   ln(m_psi^2/mu_R^2) integral sqrt(g) Q^2.
```

In the 4965 MTS normalization

```text
S_8=(16pi G_N)^-1 integral sqrt(-g)[b_C Q^2+b_t Y^2],
B_C=b_C/l_P^6,
B_t=b_t/l_P^6,
mu_psi=m_psi l_P,
```

this becomes

```text
Delta B_C^log
 =(3/pi) U4^2 mu_psi^4 ln(m_psi^2/mu_R^2),

Delta B_t^log=0.
```

The pole/log source direction in helicity coordinates is therefore

```text
[Delta B_minus,Delta B_plus]_O4
 proportional to [1,1].
```

Choosing `mu_R=m_psi` can move the displayed logarithm into the finite
matching coefficient; it cannot erase the pole residue or prove that the
finite boundary is zero.

## 4. The two known motion sources span the p8 target

The 4965 minimal massive motion determinant gives

```text
B_minus^psi=1/(60480 pi mu_psi^4),
B_plus^psi =1/(50400 pi mu_psi^4),

[B_minus,B_plus]_minimal proportional to [1,6/5].
```

Place the minimal and quadratic-`O4` directions in columns:

```text
S_dir = [1    1]
        [6/5  1].
```

Then

```text
det(S_dir)=-1/5,
rank(S_dir)=2.
```

Keeping the exact residues rather than stripping their magnitudes gives

```text
det
 [1/(60480pi mu_psi^4)   3U4^2 mu_psi^4/pi]
 [1/(50400pi mu_psi^4)   3U4^2 mu_psi^4/pi]

 =-U4^2/(100800pi^2).
```

The mass cancels. Since both `N=8` trajectories have `U4!=0`, the known
motion-sector source map has full direction rank throughout the selected
trajectory bracket. This removes the 4965 structural rank deficiency. It
does **not** determine the total finite vector because an independently
addable `p8` boundary, pure-gravity loops, photons/CFF, other thresholds and
nonlocal terms have not all been matched in one subtraction convention.

## 5. Exact static spherical response projector

Use

```text
S=(16pi G_N)^-1 integral sqrt(-g)
  [R+b_C K^2+b_t Y^2],

K=R_mnrs R^mnrs,
Y=R_mnrs Rtilde^mnrs.
```

Every static spherically symmetric parity-even geometry has an
orientation-reversing isometry. Since `Y` is a pseudoscalar,

```text
Y_background=0,
delta(Y^2)=2Y deltaY=0.
```

Thus the `b_t` field equation vanishes exactly at first order. Static
spherical data cannot read the difference channel `B_plus-B_minus`.

For the nonzero `K^2` channel,

```text
P^abcd=partial(K^2)/partial R_abcd=4K R^abcd,

H_mn
 =4K R_mabc R_n^abc
  -8 nabla^a nabla^b(K R_mabn)
  -g_mn K^2/2.
```

The generator constructs the Schwarzschild connection and Riemann tensor
from scratch with signature `(-,+,+,+)` and

```text
R^a_bcd
 =partial_c Gamma^a_bd-partial_d Gamma^a_bc
  +Gamma^a_ce Gamma^e_bd-Gamma^a_de Gamma^e_bc.
```

It independently proves `R_mn=0`,

```text
K=48M^2/r^6,
R_mabc R_n^abc=g_mn K/4,
```

and obtains

```text
H^t_t     = 1152 M^3(32r-67M)/r^12,
H^r_r     = 1152 M^3( 4r-11M)/r^12,
H^theta_theta=H^phi_phi
           =-1152 M^3(18r-41M)/r^12.
```

The exact checks are

```text
nabla_mu H^mu_r=0,
H^mu_mu=2K^2,
```

and all `tt`, `rr` and angular linearized field-equation residuals vanish.

Therefore the real-basis and helicity-basis static projectors are

```text
P_static^[B_C,B_t]       =[1,0],
P_static^[B_minus,B_plus]=[1/2,1/2],

rank(P_static)=1.
```

This is an exact symmetry zero for the second response weight, not an
unperformed calculation.

## 6. Fixed-mass Schwarzschild exterior correction

Write

```text
ds^2=-A(r)dt^2+dr^2/B(r)+r^2dOmega^2,
f=1-2M/r,

A=f+b_C p(r),
B=f+b_C q(r).
```

Fixing the ADM mass and asymptotic lapse removes the homogeneous `1/r` and
constant modes. Solving

```text
delta G^mu_nu+H^mu_nu=0
```

gives the unique exterior kernels

```text
p(r)=128 M^3(8r-11M)/r^10,
q(r)=128 M^3(36r-67M)/r^10.
```

Define

```text
x=M/r,
chi=l_P^2 M/r^3.
```

Then

```text
Delta A=128 B_C chi^3(8-11x),
Delta B=128 B_C chi^3(36-67x).
```

Equivalently,

```text
Delta A=64(B_minus+B_plus)chi^3(8-11x),
Delta B=64(B_minus+B_plus)chi^3(36-67x).
```

The weak-field potential and radial acceleration tails are

```text
Delta Phi
 =64 b_C M^3(8r-11M)/r^10,

Delta a_r
 =128 b_C M^3(36r-55M)/r^11.
```

They begin as `r^-9` and `r^-10`, respectively. This converts the abstract
4964 `C8 chi^3` compact envelope into an exact response kernel for the `B_C`
coordinate.

## 7. What closes and what remains open

```text
canonical physical O4 normalization              = derived;
linear O4 derivative-free p8 source               = exact zero;
quadratic O4 p8 pole/log source                    = derived;
known motion-sector p8 source-direction rank       = two;
static spherical p8 response rank                  = one;
exact Schwarzschild B_C response                   = derived;
static B_t response                                = exact zero at first order;
finite total [B_C,B_t]                             = open;
selected static compact GR through p6              = retained;
exact all-operator compact GR                      = false;
full MTS                                           = false.
```

The next verdict-changing target is not another basis audit. Checkpoint 4967
should place the motion, photon/CFF and pure-gravity `p8` thresholds in one
subtraction convention and determine whether the parent supplies a finite
decoupling boundary. If it does not, one bounded physical `B_C` LEC must be
retained for static compact gravity, while `B_t` requires rotating or
four-graviton data.

No GitHub action is authorized by this checkpoint.

## 8. Executable outputs

- `source-intake/functional_rg/4966/O4_p8_determinant_rank_and_static_response_results.json`
- `source-intake/functional_rg/4966/O4_normalization_and_IR_trajectory.csv`
- `source-intake/functional_rg/4966/O4_p8_determinant_source.csv`
- `source-intake/functional_rg/4966/p8_two_source_rank_gate.csv`
- `source-intake/functional_rg/4966/p8_static_response_projector.csv`
- `source-intake/functional_rg/4966/p8_Schwarzschild_metric_response.csv`
- `source-intake/functional_rg/4966/p8_finite_boundary_gate.csv`
- `source-intake/functional_rg/4966/p8_4966_decision.csv`

## 9. Validation

`scripts/Y5_R2FR_4966_O4_p8_determinant_rank_and_static_response_validation.py`
passes `31/31` checks. The validation ledger is
`source-intake/mts_residuals/P8_Y5_BRR545_4966_VALIDATION.csv`, SHA256
`a7963f8a10b4ab9d564da5d10d0acd2029fbbef60dcceb4b12e98f4b610cc759`.
All source hashes, symbolic determinant identities, independent static field
equations, CSV schemas, claim boundaries and formal-register markers pass.
No `__pycache__` directory is retained.
