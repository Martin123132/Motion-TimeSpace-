# 4941 - Natural Type-II direct O4 zero proof and minimal parent completion

Marker: `MTS_NATURAL_TYPEII_DIRECT_O4_ZERO_MINIMAL_PARENT_COMPLETION_4941`.

Date: `2026-07-12`.

Status: private analytic and source-executed checkpoint. The explicit
right-hand-side metric-scalar trace left open by 4940 is now derived in the
unchanged parent's natural Type-II/Litim source scheme. It vanishes exactly.
This does not restore `u_O4=0`: the parent metric-kernel contribution remains
nonzero. Consequently the 4940 six-coordinate point and 45-run family are now
the completed minimal `C3-CFF-F4+motion-O4` result, not merely a known-source
diagnostic. The full five-operator motion quotient, visible-matter completion
and local observable projection remain open.

## 1. Source scheme and Hessian

The scalar-gravity source supplies the exact kinetic Hessian vertices

```text
V_X,hh;

B_hpsi
 =1/2 g_mn q.D-q_(m D_n);

B_psih=B_hpsi^dagger,

q_m=nabla_m psi.
```

The pure-gravity source uses the harmonic-gauge Einstein-Hilbert operator

```text
Delta_EH=-nabla^2+E_C+Ricci terms,

E_C=-2 C_(m|r|n)s
```

and defines the regulator Laplacian with endomorphism parameter
`beta_endo`. The declared parent calculation fixes

```text
beta_endo=1,
```

for which the regulator Laplacian equals the Einstein-Hilbert Laplacian. The
unabsorbed Weyl endomorphism in the regulated inverse is therefore

```text
E_C,residual=(1-beta_endo)E_C=0.
```

This source choice is essential: the corresponding Type-I calculation at
`beta_endo=0` is not zero.

## 2. Complete direct-channel classification

At order

```text
C^2 X,
```

the minimally coupled Hessian has only two source classes:

1. one `V_X,hh` insertion with two curvature orders supplied by the
   heat-kernel density, bundle curvature or residual Weyl endomorphisms;
2. two mixed `B` insertions with two curvature orders supplied by the same
   three routes.

The lower essential scalar interaction is `X^2`; it is quartic in the scalar,
so its second field variation at `psi=0` cannot add a two-scalar O4 source.
The higher `O1`, `O2` and `O5` operators also have field degree greater than
two. The neutral photon trace has no scalar legs. Thus this list is complete
for the additive two-scalar O4 source in the declared minimal truncation.

## 3. Four-dimensional tensor zeros

A generic Euclidean four-dimensional Weyl tensor was represented by two
independent symmetric trace-free `3x3` self-dual blocks, carrying all ten
Weyl components. Exact symbolic contraction proves

```text
C_mabc C_n^abc=(1/4)g_mn C^2,

tr(K V_X)=0,

sum_perm tr(K E_C K E_C K V_X)=0,

tr(K V_X Omega_mn Omega^mn)=0.
```

The first identity is the four-dimensional Lanczos identity. The remaining
three remove the identity-density, endomorphism-squared and bundle-curvature
parts of the one-`V_X` trace. They were simplified to the exact symbolic zero,
not estimated numerically.

## 4. Mixed-vertex identity

The two exact kinetic mixed vertices obey

```text
B^dagger K B=(1/2)X(-nabla^2).
```

Therefore the curvature-squared heat-kernel density without a residual
endomorphism is proportional to

```text
Q_0[z W(z)]=(zW)(0)=0.
```

This is an exact optimized-threshold zero. Terms containing one residual
Weyl endomorphism carry `1-beta_endo`; terms containing two carry
`(1-beta_endo)^2`. Both vanish at the natural Type-II point.

As an independent normalization check, the principal algebraic
`B-C-C-B` trace gives

```text
h-regulator angular/radial coefficient      =(3/16)C^2,

scalar-regulator angular/radial coefficient =(1/16)C^2.
```

For a general endomorphism parameter its dimensionless source is

```text
S_O4,direct^principal(beta_endo,D)
 =(1-beta_endo)^2
   g(D+3)/(8pi D^4),
```

where `D` is the graviton threshold denominator. At `D=1` and the 4940
Newton coordinate, the Type-I comparator is

```text
S_O4,direct(beta_endo=0)=0.0208299023069.
```

The parent result is instead

```text
S_O4,direct(beta_endo=1)=0.
```

The zero is therefore a derived consequence of the source-owned natural
endomorphism, not a generic declaration that mixed gravity-scalar traces
vanish.

## 5. Lower four-derivative quotient

The source comparator tracks

```text
c X^2,

ctilde R_mn X^mn,

d R X.
```

At leading order for one canonical massless scalar,

```text
R_mn=8pi G X_mn,

R=8pi G X,

X_mn X^mn=X^2.
```

Hence the essential coordinate is

```text
c_ess=c+8pi g(ctilde+d).
```

Evaluating the source beta functions at
`c=ctilde=d=eta_s=eta_N=lambda=0` gives

```text
beta_c|0       =20g^2,

beta_ctilde|0  =-g/(6pi),

beta_d|0       =-g/(3pi),

beta_c,ess|0   =16g^2.
```

This closes the lower-order EOM quotient rather than silently dropping the
known `R X` and `R_mn X_mn` sources. The retained `X^2` interaction does not
alter the additive O4 two-point source at zero scalar background.

## 6. Completed minimal O4 point

Combining the direct result with the 4940 metric-kernel term gives

```text
beta_uO4
 =4u_O4-gamma_C2/2,

S_O4,direct=0.
```

The direct zero is not the value required to cancel the kernel source:

```text
S_direct required for u_O4=0
 =-0.00721281432165.
```

Therefore `u_O4=0` is not invariant. Since the newly calculated term is
exactly zero, the completed minimal point is identically the 4940 point,

```text
(g,g_plus,g_minus,g_CFF,h_C3,u_O4)_*
 =(0.130878136124880,
   0.371466079910460,
   3.45320848803473,
   0.00409533354414041,
   3.91680160559022e-6,
  -0.00180507540864851),

||beta||_infinity=1.42490481635e-13.
```

Its six-coordinate block has one relevant direction; adding the universal
motion gap gives two. The O4 mode remains irrelevant, and all 45 trajectories
already integrated in 4940 remain the completed minimal O4 family.

## 7. Claim boundary

```text
curved metric-scalar Hessian                    = reconstructed from source;
generic ten-component Weyl identities           = exact symbolic pass;
direct RHS O4 trace in natural Type-II scheme   = derived exact zero;
metric-kernel O4 source                         = derived nonzero;
u_O4=0 invariant surface                        = false;
minimal O4 parent point and family              = completed;
O4 adds a relevant UV datum                     = false;
all five scalar six-derivative beta functions   = open;
full visible-matter motion fixed point          = false;
physical PPN/clock/fifth-force projection       = open;
full MTS fixed point                            = false;
local GR/Newton/Maxwell promotion               = false.
```

## 8. Next target

`4942-Y5-R2FR-O4-completed-endpoint-local-vacuum-homogeneous-motion-branch-and-C3-CFF-PPN-residual-gate.md`

Use the completed O4 endpoint action to derive the local homogeneous
`psi=0` branch, its scalar characteristic and stress variation. Then combine
the already calculated `C3`, `CFF`, threshold and O4 endpoint coefficients in
one weak-field local residual vector. This can test whether the completed
motion portal preserves the GR/Newton/Maxwell branch without waiting for
higher scalar operators that vanish at quadratic order around `psi=0`.

