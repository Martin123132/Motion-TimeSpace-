# 4942 - Completed O4 endpoint local branch and C3-CFF residual gate

Marker: `MTS_O4_COMPLETED_ENDPOINT_LOCAL_BRANCH_C3_CFF_RESIDUAL_4942`.

Date: `2026-07-12`.

Status: private analytic and source-executed checkpoint. The completed
`C3-CFF-F4+motion-O4` family now has an exact source-free local
`psi=0` branch. The nonzero O4 coefficient changes the scalar kinetic
normalization but not its characteristic cone, and its complete tree stress
vanishes on that branch. The same 45 trajectories have been reconstructed
with their C3, CFF and O4 Wilson coordinates and projected into one local
residual vector. Standard constant PPN `gamma` and `beta` are unchanged
in the declared vacuum branch; nonzero higher-gradient C3 and curved-photon
CFF residuals remain, but the endpoint values make them extraordinarily
small. This is a real local-vacuum advance, not full local-GR promotion:
matter-interior continuation and complete visible-threshold matching remain
open.

## 1. Completed local scalar action

Use the Lorentzian quadratic motion sector

```text
S_psi
 = integral sqrt(-g)
   [-Z_psi X/2
    -u_O4 C_abcd C^abcd X
    -m_psi^2 psi^2/2],

X=g^mn nabla_m psi nabla_n psi.
```

The exact scalar equation is

```text
nabla_m[(Z_psi+2u_O4 C^2)nabla^m psi]-m_psi^2 psi=0.
```

It is homogeneous. Therefore

```text
psi=0,
nabla_m psi=0
```

is an exact local solution for arbitrary `m_psi^2`, curvature and universal
`J_gap`. No local value of the independent motion gap was fitted or
retuned.

Every metric variation of the canonical scalar, mass and O4 terms contains
`psi` or at least two derivatives of `psi`. Consequently

```text
T_mn^(psi)|psi=0=0,
T_mn^(O4)|psi=0=0.
```

The O4 fixed-point value is nonzero, but the portal is classically silent on
the homogeneous branch.

## 2. Scalar characteristic and positivity

The principal symbol is

```text
P^mn_psi=(Z_psi+2u_O4 C^2)g^mn
        =Z_eff g^mn.
```

Gradients of `C^2` are lower derivative and do not enter the characteristic.
Thus O4 conformally rescales the scalar principal symbol and leaves its null
cone equal to the public metric cone whenever

```text
Z_eff>0.
```

At a Gaussian endpoint,

```text
g=k^2 G_N,
utilde_O4=k^4 u_O4/Z_psi,
W_O4=utilde_O4/g^2,

u_O4/Z_psi=W_O4 l_P^4.
```

For Schwarzschild,

```text
C^2=48 M_geom^2/r^6,

Z_eff/Z_psi
 =1+96 W_O4 l_P^4 M_geom^2/r^6.
```

The complete family has

```text
-3.31918184977 <= W_O4 <= -3.31843917692.
```

Using its worst magnitude, the largest sampled kinetic correction is
`3.12e-155` at the 1.4-solar-mass, 12-km benchmark; the ten-solar-mass
horizon value is `7.15e-156`. The formal zero-crossing radii are
`2.7e-24` to `4.1e-22 m`, deep outside the domain where the retained EFT
would be extrapolated as a standalone classical action. Every actual
benchmark has `Z_eff/Z_psi>0` by more than 154 decimal orders.

## 3. Same-family Wilson reconstruction

The 4940 equations were rerun rather than mixing the older 4939 endpoint with
the O4-backreacted family. All 45 trajectories reach `g=1e-10`. Their
envelopes are

```text
W_C:
  0.000600014864845 to 0.000603365145951;

A_C3:
 -2.20044195542e-5 to -2.19231661105e-5;

W_O4:
 -3.31918184977 to -3.31843917692;

J_gap:
  0 to 0.239905067582.
```

The reconstructed O4 rows agree with the hash-locked 4940 family to better
than `5e-10`. The dimensionful worst-envelope coefficients are

```text
|u_O4/Z_psi| =2.26501247792e-139 m^4,

|G_C3|       =5.74817118019e-75 m^2,

|a_+|        =7.54778158500e-143 m^4,

|c_gamma^parent|
              =7.92263868782e-72 m^2,
```

where

```text
G_C3=A_C3 l_P^2,
a_+=16pi A_C3 l_P^4,
c_gamma^parent=16pi W_C l_P^2.
```

The free-lepton threshold comparator
`|c_gamma^leptons|=9.62179442357e-31 m^2` is about `1.21e41` larger than
the parent CFF value. This does not complete QCD, electroweak spin-1 or
hadronic matching.

## 4. Pure C3 metric residual

The locked pure-`I1=C^3` exterior solution uses

```text
f=1-2M/r
  +24a_+ M^2[9/r^6-49M/(3r^7)],

N=1-108a_+ M^2/r^6,

N^2 f=1-2M/r+40a_+ M^3/r^7.
```

The two `r^-6` terms in `g_tt` cancel. Hence

```text
|Delta Phi/Phi_N|
 =20|a_+|M^2/r^6,

|Delta a/a_N|
 =140|a_+|M^2/r^6.
```

The correction does not alter the coefficients of the standard `U` and
`U^2` PPN terms. Therefore, in this exterior branch,

```text
Delta gamma_PPN=0,
Delta beta_PPN=0
```

at standard constant-PPN order. This is not a declaration that C3 vanishes:
its distinct `r^-7` potential remains. At the ten-solar-mass horizon the
worst-family acceleration fraction is `3.47e-159`; at Earth it is
`3.11e-186`.

## 5. CFF Maxwell residual

For

```text
L_EM=-F_mn F^mn/4+c_gamma C_mnrs F^mn F^rs,
```

variation gives

```text
H^mn=F^mn-4c_gamma C^mnrs F_rs,
nabla_m H^mn=J^n.
```

Antisymmetry retains current conservation. On `F=0), the CFF stress and its
metric PPN contribution vanish exactly. Curved photon propagation is not
zero:

```text
|Delta v_pol|/c
 =12|c_gamma|M_geom/r^3
  +O[(c_gamma M_geom/r^3)^2].
```

The same-family parent envelope gives `5.45e-80` at the ten-solar-mass
horizon and `1.63e-93` at Earth. These are parent-only values. The known
charged-particle thresholds must be added in the identical convention before
a complete physical photon coefficient is claimed.

## 6. Threshold and PPN residual vector

At the executed `g=1e-10` endpoint,

```text
|Delta beta_g/g|
 =g/[6pi(1+w)]
 =g^2/[6pi(g+J_gap)]
 <=5.30516476973e-12.
```

This is an RG-flow residual, not a PPN observable, and tends to zero with
`g`. The local vector is therefore

```text
(Delta gamma_PPN,
 Delta beta_PPN,
 Delta cone_psi,
 T_O4|psi0,
 Delta Phi_C3/Phi_N,
 Delta v_CFF/c,
 Delta beta_g/g)

=(0,
  0,
  0,
  0,
  source-backed r^-6 C3 residual,
  source-backed curvature-polarization residual,
  <=5.3052e-12 at the numerical endpoint).
```

No element of this vector is obtained by choosing a different `J_gap` for
different arenas.

## 7. What is now established

```text
minimal O4 parent point and family             = completed;
source-free local psi=0 branch                 = exact;
O4 tree stress on psi=0                        = exact zero;
O4 scalar characteristic                       = metric cone;
Z_eff positivity on five local benchmarks      = passed;
same-family C3/CFF/O4 Wilson reconstruction    = completed;
standard vacuum PPN gamma and beta shifts      = zero at their defining order;
higher-gradient C3 residual                    = nonzero and calculated;
parent curved-photon CFF residual              = nonzero and calculated;
one universal J_gap without arena retuning     = retained.
```

This is stronger than a closure assumption: the nonzero O4 interaction is
carried all the way to the local equation and shown to be silent on an exact
solution while preserving the characteristic.

## 8. Claim boundary

```text
vacuum/exterior local branch                   = derived;
ordinary-matter interior continuation          = open;
delta S_matter/delta psi source theorem        = open at this checkpoint;
surface/junction stability of psi=0            = open;
QCD/hadronic and EW CFF matching               = open;
all five scalar six-derivative beta functions  = open;
full visible-matter fixed point                = false;
full MTS fixed point                           = false;
local GR/Newton/Maxwell promotion              = false.
```

The small numbers are consequences of the solved Planck-scaled endpoint
coefficients. They do not replace the missing matter-source theorem.

## 9. Next target

`4943-Y5-R2FR-matter-source-interior-psi-zero-continuation-and-junction-or-fifth-force-residual-gate.md`

Vary the unchanged parent matter action with respect to `psi`. If universal
matter is metric-only, prove `delta S_matter/delta psi=0`, derive the
interior and surface junction conditions, and test whether the positive
`Z_eff` zero branch extends through ordinary sources without spontaneous
scalarization. If a source survives, calculate its profile and fifth-force
residual rather than adding a local closure. Keep the C3 and CFF endpoint
coefficients fixed.

No GitHub action is authorized.
