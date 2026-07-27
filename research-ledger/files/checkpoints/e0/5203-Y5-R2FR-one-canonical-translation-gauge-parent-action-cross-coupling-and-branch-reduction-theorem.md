# 5203 - One canonical translation-gauge parent action, cross-coupling and branch-reduction theorem

Marker: `MTS_5203_ONE_CANONICAL_TRANSLATION_PARENT_ACTION_BRANCH_THEOREM`.

Checked: `2026-07-24`.

## Decision

This checkpoint assembles one parent functional rather than continuing to
write separate local, cosmological and collective models.

The common field packet is

```text
X^A;
mathcalB^A_mu;
omega^A_Bmu,inertial;
A_mu;
psi;
Phi_visible;
rho_i.
```

Its coframe and metric are

```text
e^A_mu = D_mu X^A + mathcalB^A_mu,

g_mu_nu = eta_AB e^A_mu e^B_nu.
```

The closed-time-path parent is

```text
Gamma_CTP
 = S_can[e_+,A_+,psi_+,Phi_+]
  -S_can[e_-,A_-,psi_-,Phi_-]
  +Gamma_IF[+,-]
  +Gamma_rho_i[Sigma_i].
```

Through the displayed EFT order, the canonical single-copy action can be
written in translation variables as

```text
S_can
 = integral d^4x e {
    -F_R(psi) T_TEGR/2
    -T^mu partial_mu F_R(psi)
    -U_Lambda

    -Z(psi) X_psi/2
    -V_even(psi)
    +P_ge_2(X_psi)

    -Z_A F_mu_nu F^mu_nu/4

    +c_IR C_mu_nu_rho_sigma F^mu_nu F^rho_sigma
    +G_C3 Tr(C^3)
    -u_O4 C^2 X_psi
   }

   +S_visible[e,omega_LC[e],A,Phi_visible]
   +Gamma_contact
   +Gamma_nonlocal
   +Gamma_p8plus
   +S_matched_boundary.
```

Here

```text
X_psi = g^mu_nu partial_mu psi partial_nu psi.
```

This action contains:

* the 5202 translation-gauge origin of the coframe;
* the exact TEGR local-GR block;
* the 5201 universal coframe source, Maxwell stress and Poynting vector;
* the source-complete even motion function required by checkpoints
  4950-4951;
* the CFF, C3 and O4 higher-gradient corridor;
* one CTP state functional rather than an externally appended occupation
  force.

The decisive qualification is that `F_R`, `V_even`, `Z` and the generated
`X_psi^2` coefficient are not yet solved on one physical MTS trajectory.
They are retained symbolically. Setting them to convenient values without a
flow theorem would be closure smuggling.

The result is therefore:

```text
one canonical parent action assembled                         = yes;
local GR/Newton/PPN/Maxwell reduction from that action         = yes,
                                                                conditionally;
flat-FLRW equations from that action                           = yes;
physical FLRW trajectory completely selected                  = no;
collective galaxy state compatible with that CTP parent        = yes;
collective galaxy preparation/profile derived                  = no;
full MTS unification                                           = no.
```

## 1. Scalar-curvature completion in translation variables

The curvature function is not optional once an interacting even scalar
functional is retained. Start in the curvature representation:

```text
S_F = (1/2) integral d^4x e F_R(psi) R_LC[e].
```

Checkpoint 5202 established

```text
R_LC = -T_TEGR + B_T,

B_T = 2 e^-1 partial_mu(e T^mu).
```

Therefore

```text
e F_R R_LC/2
 = -e F_R T_TEGR/2
   +F_R partial_mu(e T^mu).
```

The exact product rule gives

```text
F_R partial_mu(e T^mu)
 = partial_mu(e F_R T^mu)
   -e T^mu partial_mu F_R.
```

Hence

```text
S_F
 = integral d^4x e [
    -F_R T_TEGR/2
    -T^mu partial_mu F_R
   ]
   +matched boundary.
```

The generator verifies the product-rule residual exactly:

```text
0.
```

The derivative torsion-vector term is compulsory. The shortcut

```text
-F_R(psi) T_TEGR/2
```

without

```text
-T^mu partial_mu F_R
```

is a different scalar-torsion theory whenever `F_R` is nonconstant. It is
not used here as a hidden modification of GR.

At

```text
psi=0,
F_R(0)=M_R^2,
partial_mu F_R=0,
```

the block reduces exactly to

```text
-M_R^2 T_TEGR/2,
```

which is Einstein-Hilbert gravity plus the matched boundary term.

## 2. Translation variation and independent equations

Because

```text
e^A_mu=D_mu X^A+mathcalB^A_mu,
```

variation with respect to the translation connection gives

```text
delta Gamma/delta mathcalB^A_mu
 = delta Gamma/delta e^A_mu
 = E_A^mu.
```

Variation with respect to the relational fields gives

```text
delta Gamma/delta X^A
 = -D_mu E_A^mu.
```

The generator checks the corresponding finite-dimensional adjoint chain
rule with an exact zero residual matrix. Thus the `X^A` equation is a Ward
consequence of the coframe equation. The four relational labels do not add
four propagating scalar equations.

In curvature notation, the symmetric metric equation has the structure

```text
F_R G_mu_nu
 +(g_mu_nu Box-nabla_mu nabla_nu)F_R
 +U_Lambda g_mu_nu
 +DeltaE_C3_mu_nu
 +DeltaE_CFF_mu_nu
 +DeltaE_O4_mu_nu
 +DeltaE_completion_mu_nu

 =T_visible_mu_nu
  +T_EM_mu_nu
  +T_psi_mu_nu
  +T_state_mu_nu.
```

The `U(1)` equation is

```text
Z_A nabla_mu F^mu_nu
 -4c_IR nabla_mu(
   C^mu_nu_rho_sigma F^rho_sigma
  )
 =J^nu,

nabla_mu J^mu=0.
```

The motion equation is

```text
nabla_mu[
 (Z-2P_X+2u_O4 C^2)nabla^mu psi
]

+F_R'(psi)R/2
-Z'(psi)X_psi/2
-V_even'(psi)
=0.
```

Local Lorentz, diagonal diffeomorphism and `U(1)` invariance give the same
improved Hilbert and current Ward identities as checkpoint 5201. On all
bulk and state equations,

```text
nabla_mu(
 T_bulk^mu_nu+T_state^mu_nu
)=0.
```

No independent Newton, lensing, orbital, wave, photon-energy or Poynting
source coefficient appears.

## 3. Analytic `Z2` double-zero theorem

Write the most general local even expansions needed for the branch test:

```text
F_R(psi)
 =M_R^2+xi_2 psi^2/2+f_4 psi^4/4!+...,

Z_A(psi)
 =Z_A0+Z_A2 psi^2/2+...,

A_matter(psi)
 =1+a_m2 psi^2/2+...,

V_even(psi)
 =V_0+M_psi^2 psi^2/2+lambda_4 psi^4/4!+....
```

Analytic reflection symmetry gives

```text
F_R'(0)=0,
Z_A'(0)=0,
A_matter'(0)=0,
V_even'(0)=0.
```

The algebraic scalar source from these functions is

```text
S_psi,alg
 =F_R' R/2
  -Z_A' F^2/4
  +A_matter' L_matter
  -V_even'.
```

The generator returns

```text
S_psi,alg|psi=0 = 0.
```

It also returns exact zero for all local quadratic cross-block coefficients:

```text
Gamma_hpsi       proportional F_R'(0)       =0;
Gamma_Apsi       proportional Z_A'(0) Abar =0;
Gamma_matter,psi proportional A_matter'(0) =0.
```

This proves that analytic even couplings cannot create:

* an additive local scalar source;
* linear scalar-metric mixing;
* linear scalar-photon mixing;
* a species-dependent linear matter charge;
* a second Newton or Maxwell normalization

on the `psi=0` branch.

It does **not** prove local stability. The second variation is
coefficient-dependent. The executed algebraic slope is

```text
-Z_A2 F^2/4
+a_m2 L_matter
-M_psi^2
+xi_2 R/2.
```

Together with the kinetic operator, this enters `K_psi_psi`. The physical
local branch requires

```text
spectrum(K_psi_psi)>0
```

on the selected domain. Thus:

```text
psi=0 stationary                            = exact;
psi=0 automatically stable                  = false;
psi=0 dynamically selected by current parent= false.
```

Nonanalytic functions with a cusp or singular Hessian at zero do not inherit
this theorem. They must be rederived rather than admitted by calling them
even.

## 4. Motion-functional RG closure

The common motion block must include

```text
V_even(psi);
F_R(psi);
Z(psi);
c_X2 X_psi^2.
```

Checkpoint 4950 reconstructed the curved-space one-loop comparator

```text
beta_lambda
 =3lambda_4^2/(4pi)^2,

beta_xi
 =lambda_4(xi-1/6)/(4pi)^2.
```

The 5203 generator executes

```text
beta_xi|xi=0
 =-lambda_4/(96pi^2).
```

Therefore

```text
xi=0
```

is not an invariant surface in that comparator when `lambda_4` is nonzero.
The number `1/6` is not promoted to an MTS prediction; the structural result
is that an interacting curved scalar calculation must retain `F_R`.

Checkpoint 4951 separately proved the exact shift-symmetric surface

```text
M_psi^2=lambda_4=xi=z_2=0,
```

with generated `X_psi^2` allowed, is RG invariant for a shift-preserving
parent regulator. But the physical MTS trajectory contains the relevant
finite pole-mass deformation, so that exact massless surface is not the
complete physical trajectory.

The current status is:

```text
M_psi^2/Z_psi physical pole ratio = defined;
numerical universal J_gap         = not predicted;
F_R,V_even,Z joint trajectory     = not solved;
c_X2 parent-scheme value          = not solved;
motion functional fully RG closed = false.
```

The nonminimal curvature function is retained because closure requires it.
It is **not** reopened as a galaxy scalarization mechanism: checkpoint 4950
found the common galaxy/local activation window empty.

## 5. Cross-coupling classification

The generator classifies the branch-relevant parity-even
scalar-curvature-gauge-matter basis through canonical dimension eight. It is
not represented as the complete SMEFT basis.

### 5.1 Forbidden by exact symmetries

```text
psi R;
psi F^2;
explicit X^A representative dependence;
explicit mathcalB^A representative dependence.
```

The first two are odd under `psi -> -psi`. The latter two violate local
translation invariance unless they occur through `e`, torsion or a
gauge-covariant field strength.

### 5.2 Retained in the motion functional

```text
psi^2 R;
psi^4;
psi^2 X_psi;
X_psi^2.
```

Their values may be zero on a particular trajectory, but none is erased by
calling it inconvenient. `psi^2 R` changes the scalar Hessian but has a local
double zero. `psi^4`, `psi^2 X` and `X^2` begin beyond the local linear
onset.

### 5.3 Direct hidden-visible portals

The symmetry-allowed representatives

```text
psi^2 H^dagger H;
psi^2 F^2;
psi^2 bar f_L H f_R+h.c.
```

are absent from the active parent by the checkpoint-4919 fixed-metric
hidden-visible factorization theorem. Graviton-mediated contact or nonlocal
effects remain in the explicit completion block; they are not relabelled
direct tree portals.

An operator written as

```text
psi^2 T_visible
```

does not acquire an independent coefficient when it is merely the metric
field-redefinition image of `F_R(psi)R`.

The ordinary curved-visible operator

```text
R H^dagger H
```

remains inside `S_visible`. It is not a direct MTS portal and retains only the
physical Higgs pole in the locked 4919 analysis.

### 5.4 Retained mixed EFT operators

```text
C F F;
Tr(C^3);
C^2 X_psi.
```

These are the sourced CFF, C3 and O4 corridor. They share the same
coefficients in every arena.

### 5.5 Explicitly different theories

The minimum parent excludes:

```text
-F_R T_TEGR/2 without -T^mu partial_mu F_R;
independent torsion-vector/axial-current matter couplings;
generic f(T);
generic non-TEGR quadratic torsion coefficients.
```

These are not algebraic rewritings of the current GR-connected parent. They
would require new mode, WEP, spin and source analyses.

### 5.6 State/action separation

A prescribed spacetime function

```text
n(x)
```

is not admitted as a bulk coefficient. It must descend from
`Gamma_rho_i`, a preparation history and a state Euler equation.

All symmetry-allowed rows in the declared basis are therefore:

```text
retained;
forbidden by a locked parent theorem;
identified as a basis-correlated coefficient;
or rejected as a different theory.
```

No allowed row is silently set to zero.

## 6. Common-action branch reductions

### 6.1 Local vacuum, GR and Maxwell

Take

```text
psi=0;
nabla_mu psi=0;
rho_i=rho_0 on an open domain;
F_R(0)=M_R^2;
spectrum(K_psi_psi)>0;
one universal coframe.
```

Then the nonconstant part of `F_R`, the motion background stress, O4 and the
state stress vanish. The leading equations are

```text
M_R^2(G_mu_nu+Lambda_cal g_mu_nu)
 =T_visible_mu_nu+T_EM_mu_nu,

nabla_mu F^mu_nu=J^nu
```

with the already bounded C3/CFF/completion residuals retained explicitly.

The weak-field and source results inherited from checkpoint 5201 are

```text
nabla^2 Phi=4pi G_N rho,

G_N=1/(8pi M_R^2),

(gamma,beta,xi_PPN,alpha1,alpha2,alpha3,
 zeta1,zeta2,zeta3,zeta4)

=(1,1,0,0,0,0,0,0,0,0),

T_EM^00=(E^2+B^2)/2,

T_EM^0i=(E cross B)^i.
```

This is exact at leading two-derivative order inside the declared local
branch. It is not an all-operator equality to GR because the finite C3,
CFF, nonlocal and `p8+` corridor remains.

### 6.2 Flat FLRW motion branch

For

```text
e^A_mu=diag(1,a,a,a);
C_mu_nu_rho_sigma=0;
F_mu_nu=0;
psi=psi(t),
```

the background values of

```text
Tr(C^3);
CFF;
C^2 X_psi
```

all vanish. The common parent reduces to the scalar-tensor Friedmann system
defined by

```text
F_R(psi);
V_even(psi);
Z(psi);
P_ge_2(X_psi);
Lambda_cal.
```

The FLRW equations therefore come from the same action. However, their
physical trajectory is not completely selected because the common
functional trajectory and one homogeneous state amplitude remain open.
Previous likelihood fits cannot promote those open inputs into predictions.

### 6.3 Galaxy collective CTP branch

The elementary pole is one universal action coordinate:

```text
m_pole^2=M_psi^2/Z_psi.
```

Checkpoint 5197 proved it cannot simultaneously be the order-`H0`
cosmological pole and the old particle-style galactic mass. The current
galaxy route is instead a collective regulated pair state.

For a pair cell,

```text
P0=|0,0><0,0|;
P1=I-P0;

n=Tr(rho_i P1).
```

The projective relation

```text
n=K_IR/(K_IR+K_UV)
```

and logistic algebra are exact when the two kernel powers and odds law are
provided. But the current parent still lacks:

```text
the preparation functional Gamma_rho_i;
the |k|^(1+q) kernel owner;
q;
s=4;
B=8;
the full Hilbert stress projection.
```

Thus the collective branch uses the same bulk action and a legal CTP state
slot, but it remains a reduced-state closure rather than a derived parent
solution.

### 6.4 Waves

On the local vacuum branch, the parent carries:

```text
two TEGR tensor modes;
two Maxwell modes;
bounded C3/CFF corrections;
no linearly coupled motion scalar.
```

The physical total `c_IR` and higher completion remain explicit EFT inputs
or bounds.

## 7. CTP state stress and conservation

The state stress must be varied from the parent:

```text
T_state^mu_nu
 =(2/e) delta Gamma_rho_i/delta g_mu_nu.
```

For

```text
rho(n)=(1-n)rho_0+n rho_1,
```

the state difference is

```text
DeltaT_state[n]
 =n(T_1-T_0).
```

The exact product rule gives

```text
nabla_mu DeltaT_state^mu_nu
 =(partial_mu n)DeltaT_10^mu_nu
  +n nabla_mu DeltaT_10^mu_nu.
```

The generator returns zero residual for this identity.

Diagonal diffeomorphism invariance gives schematically

```text
nabla_mu T_state^mu_nu
 =-E_n partial_nu n
  +other state Euler terms.
```

Conservation follows when the state equations are solved. It does not follow
from inserting a logistic profile externally.

Exact local silence requires

```text
n=0;
partial_mu n=0
```

on an open domain. A pointwise zero or a finite logistic tail is not enough.

## 8. Coefficients, states and closures

The leading logarithmic calibration map is

```text
observables:
  ln G_N;
  ln alpha_EM;
  ln m_pole^2;
  ln Lambda_cal;

coordinates:
  ln M_R^2;
  ln Z_A;
  ln M_psi^2;
  ln Z_psi;
  ln Lambda_cal.
```

Its exact Jacobian is

```text
[[-1, 0, 0, 0, 0],
 [ 0,-1, 0, 0, 0],
 [ 0, 0, 1,-1, 0],
 [ 0, 0, 0, 0, 1]],
```

with

```text
rank=4;
nullity=1.
```

The null direction is the unphysical common normalization of
`M_psi^2` and `Z_psi` at fixed pole ratio.

The classes remain distinct:

```text
action coefficients:
  M_R^2,Z_A,M_psi^2/Z_psi,Lambda_cal,
  F_R,V_even,Z,c_X2,c_IR,G_C3,u_O4,p8plus;

state data:
  homogeneous psi amplitude,rho_i,covariance;

reduced closures:
  q,s=4,B=8 and the current galaxy profile.
```

There are zero arena-specific slots for

```text
G_N;
alpha_EM;
m_pole.
```

## 9. What is now proved

```text
one CTP parent form                                 = assembled;
one translation-gauge coframe                      = retained;
F_R R to complete teleparallel form                = exact;
translation-connection/coframe variation identity = exact;
relational X equation redundancy                   = exact;
analytic Z2 local scalar source                    = zero;
local h-psi, A-psi and matter-psi mixing           = zero;
local scalar stability automatic                   = false;
direct fixed-metric hidden-visible portals         = absent;
all declared symmetry-allowed cross rows           = classified;
local leading GR/Newton/PPN/Maxwell limit           = derived conditionally;
flat-FLRW equations from the same action            = derived;
physical FLRW trajectory                           = incomplete;
galaxy CTP branch compatible                       = yes;
galaxy CTP branch derived                           = no;
all-operator exact GR                               = no;
absolute G_N prediction                            = no;
full MTS unification                               = no.
```

This is progress beyond merely placing old sectors next to one another. The
same coframe and the same variational action now generate their equations,
and the exact locations where action coefficients end and state/closure data
begin are explicit.

## 10. Evidence products

Generator:

```text
scripts/Y5_R2FR_5203_canonical_translation_parent_action_branch_gate.py
```

Evidence directory:

```text
source-intake/functional_rg/5203/
```

Products:

```text
canonical_translation_parent_action.csv
parent_variation_and_Ward_identities.csv
local_Z2_double_zero_theorem.csv
motion_functional_RG_closure.csv
branch_relevant_cross_coupling_basis.csv
common_action_branch_reduction.csv
branch_operator_projection.csv
coefficient_state_closure_ownership.csv
CTP_state_stress_conservation.csv
route_decision.csv
source_provenance.csv
canonical_translation_parent_action_results.json
```

Validation:

```text
source-intake/mts_residuals/P8_Y5_BRR545_5203_VALIDATION.csv
```

The generator locks the relevant 4919, 4950-4951, 5187, 5191-5192,
5196-5197 and 5200-5202 source documents and machine results. It also locks:

```text
formalization-workbench;
checkpoint-5202 output tree;
public worktree;
read-only galaxy repository.
```

## 11. Next derivation

The selected next route is

```text
SOLVE_OR_REJECT_COMMON_F_R_V_Z_X2_MOTION_TRAJECTORY.
```

That calculation must use one parent scheme to determine whether the
reflection-even functional packet

```text
F_R(psi);
V_even(psi);
Z(psi);
c_X2
```

has a GR-connected trajectory with:

```text
F_R(0)>0;
Z(0)>0;
positive local K_psi_psi;
one universal m_pole;
stable homogeneous FLRW evolution;
no reopened galaxy/local scalarization window;
no direct visible portal;
no arena retuning.
```

If such a trajectory cannot be derived, the local GR branch remains valid
as a parent branch, but the claim that the same elementary motion functional
also owns the cosmological sector must be demoted. The collective galaxy
state remains a separate CTP-preparation derivation after that bulk question
is settled.
