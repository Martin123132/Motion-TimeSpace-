# 4959 - Gauge-complete `O2/O3/O4` six-scalar projectors and invariant rate bound

Date: 2026-07-13

Marker: `MTS_CURVATURE_SIXPOINT_PROJECTOR_DECISION_4959`.

Status: private analytic, source-locked and numerically executed checkpoint.
This checkpoint performs the tensor calculation requested by 4958. It derives
the three missing external-scalar projectors, combines them with the essential
`X2/X3` trajectory, and obtains a coefficient-independent lower bound against
an arbitrary `O2` cancellation. It does not derive the parent `O2` Wilson
coefficient, a galaxy formation rate, or full MTS.

## 1. Conventions and complete amplitude

Use all-incoming massless momenta and

```text
eta=diag(+---),  sum_i k_i=0,  k_i^2=0,
kappa=16 pi g,
u_X2=4a2,  v_X3=8a3.
```

For a scalar pair `(i,j)`, define

```text
q_ij=k_i+k_j,
H_mn^(ij)=[k_i,m k_j,n+k_j,m k_i,n]/q_ij^2,
C^(ij)=Weyl_linear[q_ij,H^(ij)].
```

The physical six-derivative tree amplitude in the selected reflection-even
parent is

```text
M6 = u_X2^2 P_X2 + v_X3 P_X3
   + kappa w_O2 P_O2
   + kappa^3 h_C3 P_O3
   + kappa^2 u_O4 P_O4,

P_O5=0.
```

Thus the five nonzero projector structures are now explicit. `w_O2` remains
an unevaluated parent coefficient, not an omitted operator.

## 2. Gauge-complete `O2` projector

For the source-basis operator

```text
O2=(nabla phi)^2(nabla_rho nabla_sigma phi)^2,
```

the flat four-scalar vertex is

```text
V4_O2(k1,k2,k3,k4)
 =-sum_(a,b,c,d in S4)(k_a.k_b)(k_c.k_d)^2
 =-3 s t u.
```

The one-metric contact is obtained by varying the measure, all three inverse
metrics, and both Levi-Civita connections. It is not gauge invariant alone.
Let `l_r=q+k_r` and

```text
V_h2(k,p;h)=k.h.p-(tr h)(k.p)/2.
```

The amputated gauge-complete four-scalar/one-metric form factor is

```text
A_O2^(4h)(q,h;k1,...,k4)
 =V_O2,contact^(4h)
  -sum_r [V_h2(k_r,-l_r;h)/l_r^2]
          V4_O2(l_r,{k_s:s!=r}).
```

The six-scalar projector is

```text
P_O2=sum_(i<j) A_O2^(4h)(q_ij,H^(ij);remaining four momenta).
```

The relative minus sign is fixed by the Ward identity. The contact-only
piece is nonzero for a pure-gauge metric; contact plus all four scalar-leg
attachments gives

```text
A_O2^(4h)(q,q_(m xi_n)+q_(n xi_m);k1,...,k4)=0,
```

with executed residual `2.39e-18`.

## 3. Weyl projectors `O3` and `O4`

Represent each Weyl tensor as a six-dimensional bivector matrix `M` and let

```text
S=diag(-1,-1,-1,+1,+1,+1),
A=M S.
```

Direct four-index contraction gives

```text
C1.C2=4 Tr(A1 A2),
C1_mn^rs C2^mnab C3_abrs=8 Tr(A1 A3 A2).
```

After the operator and scalar-pair permutations,

```text
P_O3=24 sum_matchings
 [Tr(A1 A2 A3)+Tr(A1 A3 A2)],

P_O4=4 sum_matchings sum_explicit_pair
 (k_i.k_j)(C_a.C_b)
 =16 sum_matchings sum_explicit_pair
 (k_i.k_j)Tr(A_a A_b).
```

The linear Weyl tensor is exactly silent for a pure-gauge metric in the
implemented algebra. Weyl trace, pair exchange, antisymmetry, full scalar
permutation and degree-six homogeneity checks pass at floating residuals
between `0` and `2.22e-16` on the analytic test events.

## 4. Exact no-cancellation witness

Two rational planar `2->4` configurations give the projector vectors

```text
E_x=E_y=1/4:
  (P_X2,P_X3,P_O2,P_O3,P_O4)
  =(-39/128,21/128,21/1024,7/96,-1/32),

E_x=1/6, E_y=1/3:
  (P_X2,P_X3,P_O2,P_O3,P_O4)
  =(-13/54,7/54,163/3888,14/243,-2/81).
```

The `X3/O2` two-event determinant is

```text
P_X3^(1)P_O2^(2)-P_O2^(1)P_X3^(2)=175/41472 != 0.
```

Therefore `P_X3` and `P_O2` are not proportional functions on phase space.
No constant value of `w_O2` can cancel the gravity-forced `X3` amplitude
identically. By continuity, the squared-amplitude Gram determinant is
strictly positive on any phase-space measure containing neighborhoods of
these events.

## 5. Integrated five-projector Gram matrix

Four independently scrambled Sobol/RAMBO replicas with `32768` events each
were integrated. The scalar `C0/C1/C2` block reproduces the independent 4954
calculation to maximum relative difference `3.01e-4`. Every replica and the
mean five-projector Gram matrix are positive definite; the mean minimum
eigenvalue is `1.68321e-5`.

For the leading `X3/O2` block,

```text
G_X3X3=0.0119994 approximately,
Schur_X3|O2=G_X3X3-G_X3O2^2/G_O2O2
           =0.0103354,

best (kappa w_O2/v_X3)=0.273901,
surviving X3 rate fraction=0.86133.
```

The across-replica standard error of the surviving fraction is about
`0.00133`. Thus even the best possible `O2` coefficient removes only about
`13.9%` of the integrated leading rate. The exact nonproportionality result,
not Monte Carlo sign noise, establishes that the residual is nonzero.

## 6. Normalization correction

Checkpoint 4955 fixed the field convention

```text
X_recent=X_source/2,
u_X2=4a2,
v_X3=8a3,
r3=v_X3/u_X2^2=a3/(2a2^2).
```

The 4957/4958 ratio `r3` is correct, but their absolute scalar rate used
`a2^4` instead of `(4a2)^4`. The exact correction is

```text
K24,scalar,correct=256 K24,scalar,4958.
```

At the `g=10^-10` trajectory endpoint this changes the scalar kernel from
about `5.81182e-64` to `1.48783e-61`. Fixed points, beta functions, relevant
directions, trajectories, ratios and the qualitative decay toward the
Gaussian infrared are unchanged.

## 7. Trajectory bound and `O2` source target

After inserting the known `O3/O4` trajectory coordinates and minimizing over
every real `w_O2`, all four `N=6/N=8` scheme endpoints give

```text
K24,known without O2       about 1.48827e-61,
K24,min over arbitrary O2 about 1.28189e-61,
w_O2,opt/g^2              about 2.84857.
```

The curvature correction relative to the corrected scalar kernel is only
about `3e-4`. The `O3` and `O4` coefficient combinations are respectively
about `1e-11` and `1.6e-9` of the forced `X3` coefficient at this endpoint.

Power counting sharpens the remaining calculation. A Wilsonian four-scalar
one-loop source first occurs at order `G^2`, so the allowed leading flow is

```text
beta_w=6w+S_O2 g^2+...,
w=-(S_O2/2)g^2+C_w g^3.
```

If that analytic `g^2` source is nonzero, `kappa w_O2` is co-leading with
`v_X3~g^3`; if it vanishes, the homogeneous `O2` branch is subleading. The
coefficient producing maximum cancellation would be

```text
S_O2,opt approximately -5.69713,
```

but the rate remains positive even at that value. Consequently the exact
`O2` momentum projection is now needed to predict the rate, not to decide
whether the leading number-changing channel exists.

## 8. Physics decision

```text
flat O2 four-scalar vertex                   = derived exactly;
O2 metric contact plus scalar-leg completion = derived;
O2 Ward identity                             = passed;
O3 and O4 Weyl projectors                     = derived;
complete five-projector p6 amplitude form     = derived;
X3/O2 exact cancellation                      = impossible;
integrated arbitrary-O2 rate lower bound      = derived numerically;
4957/4958 absolute normalization              = corrected by 256;
parent O2 coefficient                         = open momentum projection;
4947 local GR/Newton/Maxwell branch            = retained;
galaxy formation rate                         = not claimed;
full MTS                                      = false.
```

This closes the tensor-projector wall identified at 4958. It leaves one
physical coefficient calculation rather than three unspecified curvature
terms, and that coefficient can no longer erase the forced channel.

## 9. Artifacts

- `post-checkpoint-work/scripts/Y5_R2FR_4959_curvature_sixpoint_projectors.py`
- `post-checkpoint-work/scripts/Y5_R2FR_4959_curvature_sixpoint_projectors_validation.py`
- `post-checkpoint-work/source-intake/functional_rg/4959/PROVENANCE.md`
- `post-checkpoint-work/source-intake/functional_rg/4959/curvature_sixpoint_projector_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4959/sixpoint_projector_identity_checks.csv`
- `post-checkpoint-work/source-intake/functional_rg/4959/sixpoint_projector_QMC_replicates.csv`
- `post-checkpoint-work/source-intake/functional_rg/4959/sixpoint_projector_gram_matrix.csv`
- `post-checkpoint-work/source-intake/functional_rg/4959/trajectory_full_amplitude_bounds.csv`
- `post-checkpoint-work/source-intake/functional_rg/4959/sixpoint_IR_power_counting.csv`
- `post-checkpoint-work/source-intake/functional_rg/4959/sixpoint_projector_decision.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4959_VALIDATION.csv`

## Next target

Return to the priority local-GR/source-coupling route with the scattering
sector no longer ambiguous. Carry the complete amplitude as a bounded
one-parameter family and derive the parent universal source map. The
`O2` momentum-dependent flow is a parallel coefficient calculation; it must
not become another long detour before the same parent action proves universal
metric coupling, PPN silence and Newton/Maxwell source normalization.
