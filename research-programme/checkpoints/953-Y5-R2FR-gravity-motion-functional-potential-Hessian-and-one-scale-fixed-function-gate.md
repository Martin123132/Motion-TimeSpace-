# 4937 - Gravity-motion Hessian and one-scale fixed-function gate

Marker: `MTS_GRAVITY_MOTION_FUNCTIONAL_HESSIAN_ONE_SCALE_GATE_4937`.

Date: `2026-07-12`.

Status: private analytic, primary-source-anchored and executable checkpoint.
The unchanged minimally coupled parent does not supply the exact trace
cancellation left open by 4936. Its MES-connected potential branch has a
second relevant motion scale. This rejects one-scale predictivity for the
declared minimal functional block, not the MTS programme. No full-MTS,
local-GR, Newton, Maxwell or galaxy-profile claim is made.

## 1. Parent action and physical variables

The constant-background Euclidean action used in this calculation is

```text
Gamma_k=integral sqrt(g)[-F_k R/2+U_k(psi)+(nabla psi)^2/2].
```

The physical metric fluctuation is decomposed as

```text
f_mn=t_mn+S_hat_mn sigma,

tr S_hat=1,

S_hat_mn S_hat^mn=1/3
```

on flat space. Therefore

```text
sqrt(g)=sqrt(gbar)[1+sigma/2+sigma^2/24+O(f^3)].
```

For an arbitrary off-shell constant `psi`, direct second variation of the
potential gives

```text
delta^2[sqrt(g)U]
 contains U sigma^2/24+(U'/2)sigma delta_psi
          +(U''/2)delta_psi^2.
```

The published physical trace kernel is

```text
K_sigma=(F/2)p^2-U/4.
```

In standard quadratic-form normalization the exact `(sigma,delta_psi)`
Hessian is consequently

```text
H=[[-K_sigma/3, U'/2],
   [U'/2,        p^2+U'']].
```

With the canonical physical trace coordinate

```text
s=sqrt(F/6)sigma,
```

this becomes

```text
H_ss=-(p^2-U/(2F)),

H_spsi=sqrt(3/(2F))U',

H_psipsi=p^2+U''.
```

Thus a constant scalar position does not by itself remove metric-scalar
mixing. The cross block is silent only at a stationary point `U'=0`. The
diagonal source potential flow is recovered in that limit.

## 2. Optimized gravity-motion trace

Define

```text
w=F/(2k^2),

u=U/k^4,

v=u/w,

a=1-v/4,

b=1+u'',

mu^2=3(u')^2/(4w).
```

After the optimized replacement `p^2 -> k^2`, the canonical physical block
is

```text
H/k^2=[[-a,mu],
       [mu, b]],

det(H/k^2)=-(a b+mu^2).
```

For the declared signed diagonal regulator its dimensionless inverse trace is

```text
T_pair=(a+r_sigma b)/[32pi^2(a b+mu^2)].
```

Two normalizations are carried throughout:

```text
r_sigma=1      canonical signed-block robustness convention;

r_sigma=4/3    normalization reproducing the published diagonal
               sigma term 1/[24pi^2(1-v/4)].
```

The second value is a source-calibrated physical-gauge convention, not a
regulator-independent observable.

The full potential equation in this block is

```text
partial_t u
 =-4u+varphi u'
  +5/[24pi^2(1-u/w)]
  -1/(8pi^2)
  +(a+r_sigma b)/[32pi^2(a b+mu^2)].
```

It contains the five TT modes, universal measure term, scalar mode, physical
metric trace and their off-diagonal potential mixing.

## 3. Exact fractional cancellation test

For the 4936 parent realization,

```text
q=|varphi|^(2/3),

u=(3/4)gtilde q^2,

u'=gtilde sqrt(q),

u''=gtilde/(3q),

a=1-3gtilde q^2/(16w),

b=1+gtilde/(3q),

mu^2=3gtilde^2 q/(4w).
```

The pair trace has the exact small-field structure

```text
T_pair
 =r_sigma/(32pi^2)
  +3q/(32pi^2 gtilde)
  +O(q^2),
```

while the difference between the mixed and diagonal pair is

```text
T_pair-T_pair|mu=0
 =-9 r_sigma gtilde q^2/(128pi^2 w)+O(q^3).
```

The TT and physical-trace potential dependence also starts at `q^2`.
Therefore the complete declared block retains

```text
[q]partial_t u=3/(32pi^2 gtilde)
```

for both regulator normalizations. The unchanged minimal parent cannot
cancel the generated `|varphi|^(2/3)` channel. This closes the exact mixed
cancellation escape route of 4936 inside this declared block. It is not a
regulator-independent no-go theorem against an enlarged nonminimal parent.

## 4. Constant fixed-potential roots

The completed 4934/4935 Newton coordinate gives

```text
g*=0.1305603732179711,

w*=1/(16pi g*)=0.15237676942967363.
```

Solving the absolute physical-gauge constant-potential equation gives:

| `r_sigma` | branch | `u0` | `v0=u0/w` | `A` | `theta_mass=2-A` |
|---:|---|---:|---:|---:|---:|
| `1` | low | `0.00383526715875` | `0.0251696316512` | `0.151035530147` | `1.84896446985` |
| `1` | high | `0.146954032461` | `0.964412311738` | `109.389720449` | `-107.389720449` |
| `4/3` | low | `0.00411136018003` | `0.0269815418414` | `0.153338955053` | `1.84666104495` |
| `4/3` | high | `0.146940803251` | `0.964325492668` | `108.860986760` | `-106.860986760` |

Here

```text
A=5/[24pi^2 w(1-v)^2]
  +r_sigma/[128pi^2 w(1-v/4)^2].
```

About a constant solution, mixing is quadratic in `u'` and does not enter
the linear operator. The regular potential perturbation obeys

```text
delta beta
 =(-4+A)delta u+varphi delta u'
  -(1/32pi^2)delta u''.
```

The second derivative lowers polynomial degree, so the regular polynomial
matrix is triangular with

```text
lambda_n=-4+A+n,

theta_n=4-A-n.
```

For the `psi -> -psi` even sector, `n=2` is the physical mass direction.
It is relevant on both low roots. The high roots make the scalar directions
irrelevant, but sit only `3.56--3.57 percent` below the TT pole and are far
from the small-`|v|` minimal-essential branch. They cannot be spliced into
the 4935 separatrix as its motion completion.

The formal diagonal value

```text
theta_(4/3)=8/3-A
```

is recorded only as a diagnostic. `|varphi|^(4/3)` is not a regular
eigenoperator of this differential operator because its second derivative
generates `|varphi|^(-2/3)`.

## 5. Minimal-essential sign robustness

The primary minimal-essential source fixes

```text
lambda=3g/(16pi).
```

The action-sign map to the physical-gauge variable is kept two-sided rather
than silently selected:

```text
v=+2lambda=+0.0155844965772:
  A=0.149930471314,
  theta_mass=1.85006952869;

v=-2lambda=-0.0155844965772:
  A=0.141182716526,
  theta_mass=1.85881728347.
```

The motion mass direction is relevant under both sign maps. The conclusion
that the MES-connected branch carries an additional motion datum is therefore
not an artifact of the Euclidean action-sign choice.

## 6. Nonconstant fixed-function shooting

For a regular even solution set

```text
u(0)=u0,

u'(0)=0,

u''(0)=m^2>-1.
```

The origin equation fixes `u0` for each `m^2`. Defining

```text
Y=32pi^2[4u-varphi u'-5/(24pi^2(1-u/w))+1/(8pi^2)],
```

the exact second-order fixed equation is

```text
b=(a-Y mu^2)/(Y a-r_sigma),

u''=b-1.
```

Seventy-two source-reproducible shots cover both roots, both regulator
normalizations and

```text
-0.99 <= m^2 <= 10
```

with explicit sampling around zero. Every nonconstant row terminates before
`varphi=3` through the movable ODE denominator or runaway field/slope. The
only analytic global rows in this scan are the four constant-root
normalization rows. Narrow runaway/denominator termination transitions occur
at finite field; their retained numerator is not zero at the stopping
surface, so they are not promoted to smooth global solutions.

This is a numerical rejection gate in the declared optimized LPA block, not
a theorem excluding every nonconstant solution of every enlarged MTS
functional. No isolated fine-tuned continuation is counted without a smooth
crossing derivation and a large-field boundary condition.

## 7. One-scale decision and exact scale-lock contract

The current result is

```text
MES-connected low branch relevant directions:
  one existing gravity direction
  + one motion mass direction
  = at least two.
```

Thus one-scale predictivity is not obtained from the unchanged minimal
functional block. There is, however, a unique dimensionless scale-lock
candidate:

```text
I_M=gtilde_psi g^(4/3)
   =g_psi G_N^(4/3),

m_gap sqrt(G_N)=c_m I_M^(3/8).
```

Its exact RG contract is

```text
beta_I/I
 =beta_gtilde_psi/gtilde_psi
  +(4/3)beta_g/g.
```

At the Gaussian endpoint, the canonical values

```text
beta_gtilde_psi/gtilde_psi=-8/3,

beta_g/g=2
```

make `beta_I=0` identically. Canonical scaling preserves the ratio but does
not select it. A one-scale theory must derive the value of `I_M` and the
trajectory coefficient `c_m` from the coupled fixed point or a parent
identity. Otherwise the theory is explicitly two-scale.

## 8. O4 and galaxy interface

`O4=C^2(nabla psi)^2` vanishes on the flat constant background used for the
potential equation. It therefore cannot cancel the `q` channel here. This is
not a proof that `beta_uO4=0`; its curved `C^2p^2` projection remains an
independent running coordinate.

The galaxy logistic map remains structurally compatible with a future
motion Hessian, but this checkpoint does not produce its positive amplitude
ratios, radial scale map, numerical exponents or activation stress tensor.
The sibling project should continue to use "metric-dominated lensing with a
negligible bounded CFF correction", not "metric-only lensing".

## 9. Claim boundary

```text
off-shell gravity-motion Hessian                 = derived;
optimized mixed potential trace                  = derived;
fractional q cancellation in unchanged block     = false;
constant potential roots                         = solved;
regular linear scalar spectrum                   = derived;
MES sign-robust motion mass relevance             = derived;
generic nonconstant fixed-function scan pass      = zero;
global nonconstant no-go theorem                  = false;
one-scale unchanged-parent completion             = false;
canonical Newton-motion invariant                 = derived but value unfixed;
O4 beta frozen to zero                            = false;
full MTS fixed point and trajectory               = false;
local GR/Newton/Maxwell promotion                  = false.
```

## 10. Next target

`4938-Y5-R2FR-motion-scale-to-Newton-scale-parent-identity-or-explicit-two-scale-theory-gate.md`

Derive or reject parent ownership of

```text
I_M=gtilde_psi g^(4/3)=g_psi G_N^(4/3)
```

and of `c_m`. The gate must calculate the coupled beta of `I_M`, test whether
the UV critical surface fixes it, and propagate every surviving value down
the 4935 GR separatrix. If no identity or fixed value exists, record the
motion gap as an explicit second essential scale rather than hiding it in a
closure.

