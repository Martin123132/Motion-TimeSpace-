# 5191 - O4 FLRW tensor nondegeneracy, order reduction, and cosmological safety

Marker: `MTS_5191_O4_FLRW_TENSOR_NONDEGENERACY_ORDER_REDUCTION`

**Verdict:** `O4=C^2 X` cannot be set to zero, declared redundant, or
resummed as an exact healthy finite higher-derivative theory. The parent flow
predicts a nonzero coefficient and the full operator is an independent
on-shell scalar-gravity interaction. On a homogeneous clock background its
isolated tensor acceleration Hessian has rank two, so it is not degenerate.
If the finite truncation is resummed, its extra tensor pole has the opposite
residue to the GR pole.

The correct low-energy interpretation is nevertheless viable. At first order
in the derivative expansion, the tensor `q^4` term is equation-of-motion
reducible. For a time-dependent FLRW clock, exact reduction of order leaves a
second-order tensor action with background-suppressed kinetic and gradient
corrections. The source-predicted Wilson coefficient gives an enormous
control margin below Planck curvature under an explicit canonical kinetic
density bound.

No GitHub action and no edit to `formalization-workbench` occurred.

## 1. Parent ownership and sign

The assembled local action uses

```text
Gamma contains -u_O4 C_abcd C^abcd X,
X=g^munu partial_mu psi partial_nu psi.
```

Define the signed coefficient multiplying `+C^2 X`:

```text
c_O4=-u_O4,
B(eta)=c_O4 Xbar(eta).
```

The completed Type-II fixed point has

```text
u_O4*=-0.0018050754086485139,
u_O4=0 invariant=False,
O4 adds a relevant direction=False.
```

The four converged infrared endpoints give

```text
-3.3225249561681114 <= W_O4=u_O4/g^2
                             <= -3.3224177636400554.
```

Thus in the canonical scalar coordinate

```text
c_O4=-u_O4/Z=-W_O4 l_P^4>0,
|c_O4| <= 2.267293816536319e-139 m^4.
```

For a homogeneous timelike canonical clock, `X_c<0`, hence `B<0`.

## 2. The full operator is not redundant

Checkpoint 4930 places

```text
O4=C_abcd C^abcd (nabla phi)^2
```

in the independent integration-by-parts/equation-of-motion quotient of the
shift-symmetric six-derivative scalar-gravity EFT. Checkpoint 4959 then
constructs its gauge-complete on-shell projector. The five-projector Gram
matrix is positive definite, with minimum eigenvalue

```text
1.683210889814806e-05.
```

A local field redefinition may move `O4` effects among equivalent operators,
but it cannot delete its full on-shell amplitude. This must be separated from
the narrower fact that its free tensor `q^4` two-point term is perturbatively
reducible.

The external primary basis reference is
`https://arxiv.org/abs/1908.08050`; the reduction-of-order methodology is
cross-checked against `https://arxiv.org/abs/1709.09695`. The newer
six-derivative scalar-tensor amplitude count is recorded at
`https://arxiv.org/abs/2512.13453`.

## 3. Exact time-dependent tensor Weyl density

Use conformal time, spatial momentum along `z`, and either real TT
polarization `gamma(eta) cos(kz)`. Four-dimensional conformal invariance gives

```text
sqrt(-g) C[g]^2=sqrt(-gtilde) C[gtilde]^2.
```

The executed full linearized Riemann/Ricci/Weyl contraction gives the same
spatially averaged density for plus and cross:

```text
(k**2*gamma(eta) - 2*k*Derivative(gamma(eta), eta) - Derivative(gamma(eta), (eta, 2)))*(k**2*gamma(eta) + 2*k*Derivative(gamma(eta), eta) - Derivative(gamma(eta), (eta, 2)))/2.
```

Writing `D gamma=gamma''+k^2 gamma`,

```text
C_1^2
 =1/2(D gamma)^2-2k^2(gamma gamma')'.
```

The second term cannot simply be discarded when `B(eta)` varies. The exact
weighted identity is

```text
B C_1^2
 =B(D gamma)^2/2-k^2 B'' gamma^2+J',

J=k^2[B' gamma^2-2B gamma gamma'].
```

Both symbolic residuals are exactly zero.

## 4. Nondegeneracy and the resummed pole

In the 5189 normalization,

```text
A=M_R^2/4,
K_TT(q^2)=q^2(A+Bq^2),
q^2=omega^2-k_phys^2.
```

The highest-time-derivative quadratic Lagrangian is

```text
L_high=B[(gamma_plus'')^2+(gamma_cross'')^2]/2.
```

Therefore

```text
d^2 L_high/d gamma_A'' d gamma_B''=B delta_AB,
rank=2 when B!=0,
det=B^2.
```

TT is an independent FLRW irrep. The scalar, lapse and shift constraints
cannot null this block, `P(X)` has zero TT acceleration Hessian, `C^3` starts
at cubic order on `Cbar=0`, and `CFF` has no pure tensor quadratic term on
`Fbar=0`. No explicitly resolved operator in the selected six-derivative
block supplies a cancellation. The unresolved `Gamma_p8plus/nonlocal` tower
could alter the all-scale spectrum, which is precisely why the finite
truncation is retained only as an EFT; it cannot be used as an unproved
exact cancellation.

The exact extra root and pole decomposition are

```text
q_extra^2=-A/B,

1/[q^2(A+Bq^2)]
 =1/A[1/q^2-1/(q^2-q_extra^2)].
```

The residues are

```text
GR=1/A,
extra=-1/A.
```

For the predicted timelike branch `B<0`, the extra root has positive `q^2`
but negative residue. It is a heavy ghost if the finite polynomial is
incorrectly treated as exact. For `B>0`, the root also has tachyonic sign.
This is not a valid all-scale two-mode theory.

## 5. Why the low-energy EFT still survives

For constant `B`, the first-order local field redefinition

```text
gamma=[1-B D/(2A)] gamma_R
```

removes the linear `B q^4` tensor term. The executed transformed kernel has
linear-`B` coefficient

```text
0.
```

The full `O4` interaction remains physical; only the free two-point
equation-of-motion-squared term is being reduced.

On FLRW, define the leading Einstein equation

```text
E0=gamma''+2 Hc gamma'+k^2 gamma=0,
Hc=a'/a.
```

Since `D gamma=E0-2Hc gamma'`, terms proportional to `E0` are removed by the
same first-order equivalence transformation. Including the exact `B''`
piece from the weighted Weyl density gives

```text
S_T,red=1/2 int d eta [
  Q_T gamma'^2-F_T k^2 gamma^2
]+O(B^2),

Q_T=A a^2+4B Hc^2,
F_T=A a^2+2B''.
```

This equation is second order. In cosmic time,

```text
delta_Q=Q_T/(Aa^2)-1=4B H^2/A,
delta_F=F_T/(Aa^2)-1
       =2[ddot(B)+H dot(B)]/A,
c_T^2=(1+delta_F)/(1+delta_Q)+O(B^2).
```

The finite low-energy gates are `1+delta_Q>0`,
`1+delta_F>0`, and physical frequencies/background derivatives below the
parent cutoff. Any field redefinition must also be applied to the source and
readout map; it is not permission to change frames selectively.

For a homogeneous shift-symmetric `P(X)` clock, the background current gives
an additional exact reduction:

```text
a^3 P_X dot(psi)=constant,
c_s^2=P_X/(P_X+2X P_XX),
d ln|B|/d ln a=d ln|X|/d ln a=-6c_s^2.
```

Therefore

```text
s_B=[ddot(B)+H dot(B)]/(B H^2)
   =36c_s^4-6c_s^2(1+dot(H)/H^2)
    -6 d(c_s^2)/d ln a.
```

For a canonical clock, `c_s^2=1`, so

```text
s_B=30-6 dot(H)/H^2.
```

On a constant equation-of-state background with `-1<=w<=1`, this is
`s_B=39+9w`, hence `30<=s_B<=48`. The numerical `|s_B|<=100`
envelope below is therefore deliberately wider than the complete canonical
range.

## 6. Source-predicted cosmological envelope

For `phi_c=sqrt(Z)psi`, define

```text
Omega_kin=-X_c/(2 rho_total),
rho_total=3M_R^2 H^2,
M_R^2=1/(8pi l_P^2).
```

On the healthy canonical branch assume

```text
0<=Omega_kin<=1
```

with no large positive kinetic density hidden by a cancelling negative
component. Then

```text
epsilon_bg=|B|H^2/A
          =24|W_O4|Omega_kin(H t_P)^4,

|delta_Q|=4 epsilon_bg,

|delta_F|=2|s_B| epsilon_bg,
s_B=[ddot(B)+H dot(B)]/(B H^2),

|q_extra|/H
 =1/[sqrt(24|W_O4|Omega_kin)(H t_P)^2].
```

At `Omega_kin=1`, `|delta_Q|=1` only at

```text
H=4.389104729428941e+42 s^-1,
```

and the heavy pole reaches `H` only at

```text
H=6.207131435034301e+42 s^-1.
```

Even the illustrative `H=10^40 s^-1` row has

```text
|delta_Q|<=2.694611909530889e-11,
|delta_F|<=1.347305954765445e-09
```

using the deliberately broad derivative-shape envelope `|s_B|<=100`.
This is a conditional theorem for the canonical kinetic-density branch, not
a selection of the actual MTS cosmological initial condition. For a general
shift-symmetric `P(X)` branch, the exact current law above reduces the
remaining input to its sourced `c_s^2(X)` trajectory and one background
state.

## 7. Decision

```text
O4 parent ownership                         = derived;
u_O4=0 invariant surface                    = false;
full O4 operator redundant                  = false;
isolated finite O4 TT truncation degenerate = false;
resummed extra-pole residue                 = opposite to GR;
first-EFT-order q4 two-point term reducible = true;
time-dependent FLRW reduced action          = derived;
local psi=0 tensor protection               = exact;
canonical sub-Planck cosmology              = conditionally controlled;
general P(X) cosmological X(t)               = still required;
all-scale UV two-mode completion             = not established.
```

This resolves the 5189 gate. `O4` does not have to be deleted for MTS to
recover low-energy GR. It has to be treated honestly as an irrelevant EFT
operator. A future fundamental claim must derive the full tower/nonlocal
propagator or another UV completion rather than promote the finite
fourth-order tensor polynomial to an exact spectrum.

## 8. Next target

The next calculation should insert the actual functional MTS `P(X)` into the
homogeneous current/Friedmann system and select its cosmological branch:

```text
Xbar(t), B(t), s_B(t), Omega_kin(t)
```

on the same cosmological branch used by the likelihood work. That turns the
conditional envelope into a branch-specific CMB/GW propagation prediction
without introducing a new coefficient.

## 9. Machine artifacts

- `source-intake/functional_rg/5191/O4_parent_ownership_and_convention.csv`
- `source-intake/functional_rg/5191/FLRW_TT_Weyl_quadratic_identity.csv`
- `source-intake/functional_rg/5191/O4_TT_degeneracy_and_pole.csv`
- `source-intake/functional_rg/5191/O4_redundancy_and_order_reduction.csv`
- `source-intake/functional_rg/5191/O4_cosmology_control_envelope.csv`
- `source-intake/functional_rg/5191/O4_branch_decision.csv`
- `source-intake/functional_rg/5191/source_provenance.csv`
- `source-intake/functional_rg/5191/O4_FLRW_tensor_order_reduction_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5191_VALIDATION.csv`
