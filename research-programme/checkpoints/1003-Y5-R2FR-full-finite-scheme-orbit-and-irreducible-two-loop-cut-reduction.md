# 4987 - Full finite-scheme orbit and irreducible two-loop cut reduction

Date: 2026-07-14

Marker: `MTS_4987_FULL_FINITE_SCHEME_ORBIT_IRREDUCIBLE_CUT_REDUCTION`.

> **4990 amplitude-scheme correction.** The finite-orbit theorem survives,
> but its amplitude-scheme coefficient is `beta_C=203/10`, not the
> unbridged Type-I/Litim value `16`. The active invariant is therefore
> `K_mu=3S-(203/10)rho+(18/pi)r4`. `K_ang` and the double-rational-free
> reduction are unchanged. The original `3S-16rho+(18/pi)r4` expression is
> retained only as correction history.

Status: private analytic, primary-source-locked, generated and independently
validated checkpoint. This checkpoint corrects the scope of the 4986
two-loop invariant, derives the full finite `X^2/O2` coordinate orbit, and
reduces the two-loop Einstein-scalar state sum to four genuinely surviving
cut classes. It does not yet integrate those four classes or assign numerical
values to the two physical single-log coefficients.

## 1. Why the target needed one more scheme coordinate

Checkpoint 4986 correctly proved invariance under the resonant
six-derivative redefinition

```text
w'=w+alpha g c.
```

That result was explicitly in a fixed common four-derivative scheme. The
general one-loop finite renormalization also permits

```text
C'=C+beta,
```

where `C=c/g^2`. The renormalized pure-minimal one-loop four-scalar amplitude
therefore needs its local rational coordinate `r4`, defined in the same
normalized `X^2` tree basis:

```text
R4=C P4+H4,log+r4 P4,
P4=s^2+t^2+u^2  (up to the declared X2 normalization).
```

Amplitude invariance gives

```text
r4'=r4-beta,
C+r4=scheme invariant.
```

Thus `I_2L` and `J_2L` from 4986 are physical coordinates after the p4
scheme has been fixed, but are not invariants of the larger finite orbit.
This is a scope refinement rather than a failure of the 4986 RG algebra.

## 2. Exact local-polynomial orbit theorem

For four identical massless scalars, impose crossing symmetry and
`s+t+u=0`. A general homogeneous polynomial after eliminating `u` is tested
under the two generators

```text
(s,t) -> (t,s),
(s,t) -> (s,-s-t).
```

Exact nullspace reduction gives

```text
degree 2: dimension 1, vector (1,1,1),
          q2=s^2+st+t^2=(s^2+t^2+u^2)/2;

degree 3: dimension 1, vector (0,1,1,0),
          q3=s^2t+st^2=-stu.
```

Therefore the local crossing-symmetric rational ambiguity is exactly one
dimensional at both p4 and p6. A finite `X^2` counterterm spans the first;
the finite `O2` coordinate spans the second. No additional local
four-scalar polynomial is hidden at either order.

## 3. Full affine finite-scheme orbit

Use the 4986 reduced amplitude

```text
R6=-3W stu+C F1+F2,

F1=f_A L_A+f_B L_B+rho stu,
f_A=46/(15pi),
f_B=-1/(15pi),

F2,single=A L_A+B L_B+eta stu,

dC/dlnmu=A_c=203/10,
dW/dlnmu=B_gc C+S,
B_gc=-6/pi.
```

The most general finite affine change needed at this order is

```text
C'=C+beta,
W'=W+alpha C+delta.
```

Exact amplitude and beta-flow invariance require

```text
r4'=r4-beta,
rho'=rho+3alpha,

S'=S+(203/10)alpha-B_gc beta,
A'=A-beta f_A,
B'=B-beta f_B,
eta'=eta-beta rho+3(delta-alpha beta).
```

Substitution into `R6` gives `R6'-R6=0` identically. The old combinations
transform as

```text
I=3S-(203/10)rho -> I'=I-3B_gc beta,
J=A-B            -> J'=J-beta(f_A-f_B).
```

Since

```text
f_A+f_B=3/pi=-B_gc/2,
f_A-f_B=47/(15pi),
```

the full finite-scheme invariants are

```text
K_mu =I-3B_gc r4
     =3S-(203/10)rho+(18/pi)r4,

K_ang=J-(f_A-f_B)r4
     =A-B-[47/(15pi)]r4.
```

All twelve symbolic orbit identities have exact zero residual. An
independent validator then reproduces the invariants on `96` exact rational
scheme transformations.

## 4. Double rational-free common scheme

The one-dimensional orbit theorem guarantees that the finite choices

```text
beta=r4,
alpha=-rho/3
```

set

```text
r4_rf=0,
rho_rf=0.
```

In this declared scheme,

```text
K_mu=3S_rf,
K_ang=J_rf,

A_rf=A-f_A r4,
B_rf=B-f_B r4,

K_mu=-6(A_rf+B_rf),
K_ang=A_rf-B_rf.
```

This does not set the two-loop answer to zero. It removes only the two local
one-loop rational coordinates, so the surviving cut calculation returns the
physical invariants directly rather than a scheme-labelled `S` or `J`.

## 5. Exact two-particle state reduction

Each side of the s-channel cut contains two external scalars. Reflection
symmetry requires an even number of internal scalar legs on each tree or
one-loop amplitude. Hence

```text
phi-h intermediate state = exact zero.
```

The two-particle state sum initially reduces to `phi-phi` and `h-h`.
Dunbar-Norridge further give

```text
M_tree(phi,phi,h+,h+)=0,
M_tree(phi,phi,h-,h-)=0,
M_tree(phi,phi,h+,h-) != 0.
```

Therefore only

```text
C2_phiphi:
  Re A_4phi^(1) x A_4phi^(0) plus loop-placement swap;

C2_hh:
  Re A_2phi2h^(1,+-) x A_2phi2h^(0,+-)
  plus loop-placement swap
```

survive. Same-helicity graviton cuts and every scalar-graviton cut vanish
before integration.

## 6. Exact three-particle state reduction

The same reflection count permits only zero or two internal scalars:

```text
phi-h-h   = exact zero,
phi-phi-phi = exact zero,
h-h-h     = parity allowed,
phi-phi-h = parity allowed.
```

The Forde-Kosower all-plus scalar-gluon tree contains a positive power
`(-m_phi^2)^j` in every term. It therefore vanishes in the massless limit;
all-minus follows by spinor conjugation. Bjerrum-Bohr et al. construct the
two-scalar gravity tree by KLT squaring, so

```text
M_tree(phi,phi,h+,h+,h+)=0,
M_tree(phi,phi,h-,h-,h-)=0.
```

The surviving three-particle classes are consequently

```text
C3_hhh(mixed helicity):
  A_2phi3h^(0) x A_2phi3h^(0);

C3_phiphih:
  A_4phi1h^(0) x A_4phi1h^(0).
```

The complete nonzero state census is now four classes, not an unrestricted
sum over every scalar/graviton assignment.

## 7. Renormalized master projection

The source-locked real two-loop on-shell identity is

```text
D1 ReF1+D2 F0=-(1/pi)[Re(M)Re(F)]^(2).
```

After the common stress-tensor/soft subtraction, define

```text
C2_ren = C2_phiphi
       + C2_hh(+-)
       + C3_hhh(mixed)
       + C3_phiphih
       - C_IR.
```

In the double rational-free scheme, the MTS `stu` projection is exactly

```text
Pi_stu[-C2_ren/pi-D1 ReF1]=-K_mu stu.
```

This equation is the correct numerical target for the scale coefficient.
It includes the known one-loop beta action and does not promote a raw
two-loop pole, an evanescent counterterm coefficient, or `S` alone.

## 8. Independent angular projector

For physical s-channel kinematics

```text
t=-s(1-z)/2,
u=-s(1+z)/2,
stu=s^3(1-z^2)/4.
```

After subtracting the forced double logarithm,

```text
Disc_s F2,single/(-2pi i s^3)
 =A_rf+(B_rf/4)(1-z^2)
 =d0+d2 P2(z),

d0=A_rf+B_rf/6,
d2=-B_rf/6.
```

The inverse map is

```text
A_rf=d0+d2,
B_rf=-6d2,
K_mu=-6(d0-5d2),
K_ang=d0+7d2.
```

Equivalently two nonsingular angles suffice:

```text
A_rf=D(1),
B_rf=4[D(0)-D(1)].
```

Sixty-four exact rational controls reconstruct both coefficients with zero
residual. Scale running fixes only `K_mu`; the angular discontinuity is still
required for `K_ang`.

## 9. Physics decision

```text
crossing-local p4 rational dimension       = one, proved;
crossing-local p6 rational dimension       = one, proved;
full finite X2/O2 affine orbit             = derived exactly;
4986 I/J fixed-p4-scheme scope             = corrected;
fully invariant K_mu and K_ang             = derived exactly;
double rational-free scheme                = constructed;
mixed phi-h two-cut                        = exact zero;
same-helicity h-h two-cut                  = exact zero;
odd-scalar three-cuts                      = exact zero;
all-equal-helicity h-h-h three-cut         = exact zero;
surviving cut classes                      = four;
numeric K_mu                               = open;
numeric K_ang                              = open;
finite trajectory datum C_w                = open;
exact all-operator local GR                = false;
full MTS                                   = false.
```

The live runner records `13` closed and `4` explicit open/nonclaim gates.
The independent validator passes `233/233` checks.

## 10. Artifacts

- `post-checkpoint-work/scripts/Y5_R2FR_4987_full_finite_scheme_orbit_and_cut_reduction.py`
- `post-checkpoint-work/scripts/Y5_R2FR_4987_full_finite_scheme_orbit_and_cut_reduction_validation.py`
- `post-checkpoint-work/source-intake/functional_rg/4987/crossing_local_polynomial_basis.csv`
- `post-checkpoint-work/source-intake/functional_rg/4987/full_finite_scheme_orbit.csv`
- `post-checkpoint-work/source-intake/functional_rg/4987/two_loop_cut_state_census.csv`
- `post-checkpoint-work/source-intake/functional_rg/4987/rational_free_master_projection.csv`
- `post-checkpoint-work/source-intake/functional_rg/4987/single_log_angular_projector_checks.csv`
- `post-checkpoint-work/source-intake/functional_rg/4987/two_loop_cut_reduction_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4987/full_finite_scheme_orbit_and_cut_reduction_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4987/PROVENANCE.md`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4987_VALIDATION.csv`

## Next target

Checkpoint 4988 should calculate the first surviving term rather than reopen
the census: insert the archived renormalized Dunbar-Norridge four-scalar
amplitude into `C2_phiphi`, perform the universal gravity soft subtraction in
the same rational-free scheme, and project its exact contribution onto
`d0,d2`. Only then proceed to the opposite-helicity `2phi2h` cut and the two
surviving three-particle trees.
