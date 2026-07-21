# 4983 - Box-squared essential quotient, running frame, and local profile theorem

Formal marker: `PPC4161_BOX2_ESSENTIAL_LOCAL_PROFILE_4983`.

## Decision

Checkpoint 4983 resolves the local analytic four-derivative scalar bilinear
left open at 4982. The result is stronger than merely assigning it an
unknown coefficient:

```text
I_Box=(1/2) integral sqrt(g)(Box psi)^2
```

is an off-shell two-point form-factor coordinate, but it is not an
independent on-shell Wilson direction in the massless shift-symmetric local
EFT. A scalar derivative redefinition removes it order by order. Together
with the already derived disformal/conformal metric quotient, the complete
four-derivative scalar-gravity packet has one essential direction, `X^2`,
whose source remains

```text
beta_c,ess=16g^2.
```

The selected integrated-`H` ordinary-matter branch has `J_psi=0`, a
reflection-even state, and zero scalar boundary data. The new operator
therefore leaves `psi=0`, its stress, scalar charge, and classical
one-scalar fifth force exactly zero. This closes the local analytic
`(Box psi)^2` obstruction on that branch.

It does **not** calculate the numeric off-shell `beta_bBox`, a complete
nonanalytic form factor `Z(-Box)`, or a nonperturbatively resummed heavy
fourth-order mode. Those remain separate from the order-reduced local EFT.

The runner passes `27/27` gates; the independent validator passes
`105/105`. No GitHub action was performed.

## 1. Operator-name correction

Two distinct operators had acquired the shorthand `O2` in different parts
of the corpus. They must not be merged:

```text
four-derivative two-point bilinear:
  O_Box2^(4)=(Box psi)^2,
  derivative order 4, scalar field degree 2;

six-derivative amplitude operator:
  O2^(6)=X(nabla_rho nabla_sigma psi)^2,
  derivative order 6, scalar field degree 4.
```

The latter already has the gauge-complete amplitude projector constructed at
checkpoint 4959. Checkpoint 4983 concerns only `O_Box2^(4)`. This distinction
is recorded in
`source-intake/functional_rg/4983/box2_operator_notation_and_source_scope.csv`.

## 2. Source status

The acquired scalar-gravity source `2110.09566` explicitly states that a
complete off-shell four-derivative truncation should contain
`(D^2 phi)^2`, interprets it as the first momentum-dependent term in
`Z_k(-D^2)`, and leaves it to future work.

The acquired nonredundant gravity-EFT source `1908.08050` supplies the
essential-basis rule: operators proportional to the leading free equations
of motion are removable by perturbative field redefinitions that preserve
the S-matrix. Its shift-symmetric scalar module imposes `Box phi=0` before
enumerating the essential basis. Consequently, the absence of `(Box phi)^2`
from that essential basis is derived redundancy, not evidence that its raw
off-shell coefficient is numerically zero.

## 3. Covariant variation and Hessian

Define

```text
S_Box2=(b_Box/2) integral sqrt(g)Y^2,
Y=Box psi.
```

For a scalar variation,

```text
delta S_Box2
 =b_Box integral sqrt(g) delta_psi Box^2 psi
 +b_Box surface integral n^mu[
     Y nabla_mu delta_psi
    -delta_psi nabla_mu Y].
```

Thus

```text
E_Box2=b_Box Box^2 psi,

delta_chi delta_xi S_Box2
 =b_Box integral sqrt(g)(Box chi)(Box xi),

H_psipsi^Box2=b_Box Box^2.
```

For `delta g_mn=h_mn`, define `D_h f:=delta_h(Box f)`. The exact first
metric variation of the scalar Laplacian is

```text
D_h f=delta_h(Box f)
 =-h^mn nabla_mn f
  -[nabla_m h^(m lambda)-(1/2)nabla^lambda h]nabla_lambda f.
```

The mixed block follows without freezing the connection:

```text
delta_h delta_chi S_Box2
 =b_Box integral sqrt(g)[
   (h/2)Y Box chi
   +(D_h psi)Box chi
   +Y(D_h chi)].
```

At the zero-motion background,

```text
H_hh^Box2|psi=0=0,
H_hpsi^Box2|psi=0=0,
H_psipsi^Box2|psi=0=b_Box Box^2.
```

The covariant formula was independently differentiated at a normal-coordinate
point while retaining arbitrary `h_mn`, `partial_lambda h_mn`, scalar
gradients, and scalar Hessians. Thirty-two local-jet controls give

```text
maximum relative residual =2.80411309254e-15,
maximum absolute residual =8.88178419700e-16.
```

The flat two-point projector is therefore

```text
Gamma_psipsi^(2)(p)=Zp^2+b_Box p^4+O(p^6),
b_Box=(1/2)d^2 Gamma_psipsi^(2)/d(p^2)^2|p^2=0.
```

No numeric value is assigned to `b_Box`.

## 4. Complete local four-derivative quotient

Before EOM and IBP reduction, use

```text
I_Box=(Box psi)^2,
I_Hessian=(nabla_mn psi)(nabla^mn psi),
I_RicciX=R_mn nabla^m psi nabla^n psi,
I_RX=RX,
I_X2=X^2.
```

The exact Bochner/commutator identity is

```text
integral[I_Box-I_Hessian-I_RicciX]=boundary.
```

This lowers the raw dimension from five to four. For the leading massless
scalar action

```text
S_0=(Z/2) integral sqrt(g)X,
```

the perturbative scalar redefinition

```text
psi_old=chi+s Box chi,
s=b_Box/(2Z)
```

changes

```text
b_Box,new=b_Box-2Zs=0.
```

The finite disformal and conformal transformations already derived at 4958
remove `RicciX` and `RX`. In the post-IBP coordinate basis

```text
(b_Box,ctilde,d,c),
```

the three redundant tangent directions have rank three and annihilate the
single invariant covector

```text
dc_ess=dc+8pi g(dctilde+dd).
```

Hence

```text
raw operator dimension          =5,
IBP identities                  =1,
post-IBP coordinate dimension   =4,
field-redefinition rank         =3,
essential dimension             =1,
essential coordinate            =c_ess.
```

At the source-owned origin,

```text
beta_c=20g^2,
beta_ctilde=-g/(6pi),
beta_d=-g/(3pi),
beta_c,ess=16g^2.
```

The omitted local bilinear therefore does not add a second physical
four-derivative coupling or a new relevant direction to this essential
packet.

## 5. Running essential frame

The raw off-shell flow may generate `b_Box`. Maintaining the essential frame
`b_Box=0` requires a scale-dependent field coordinate,

```text
partial_t psi=gamma_Box Box psi,
gamma_Box=beta_bBox/(2Z).
```

This is a derived frame law, not a numeric value for `beta_bBox`. The latter
is needed to reconstruct the off-shell form factor, but it is not an
independent essential Wilson coordinate.

A sufficient perturbative invertibility condition on the local momentum
domain is

```text
epsilon_Box=|b_Box|p_max^2/(2Z)<1.
```

If the motion gap is retained, the same redefinition removes `Box2` but
shifts the lower kinetic coefficient before pole mass and residue matching:

```text
Z -> Z-b_Box m_gap^2.
```

Thus a finite mass does not make the operator essential; it requires the
lower two-point coordinates to be rematched.

The transformation also moves strength into six-derivative operators. Its
effect on `O2^(6)` and the complete six-point quotient belongs to the next
flow calculation and must not be inferred from the four-derivative result.

## 6. Compact-source response

For a hypothetical massless scalar source in flat Euclidean space,

```text
psi(p)=J(p)/[Zp^2+b_Box p^4]
      =J(p)/(Zp^2)-b_Box J(p)/Z^2+O(b_Box^2 p^2).
```

The first order-reduced correction has the support of `J`. Therefore, for a
smooth compact source,

```text
delta psi_Box2(r>R_source)=0 at O(b_Box).
```

The `p=0` pole residue remains `1/Z`, so `b_Box` changes neither the Gauss
charge nor the coefficient of the long-range `1/r` field.

As a control only, if `b_Box/Z>0` is resummed exactly,

```text
1/[p^2(Z+b_Box p^2)]
 =(1/Z)[1/p^2-1/(p^2+m_Box^2)],
m_Box^2=Z/b_Box.
```

For a normalized compact spherical profile and `r>R`, the Yukawa potential
and force fractions are

```text
delta psi/psi_0=-F(mR)e^(-mr),
delta a/a_0=-F(mR)(1+mr)e^(-mr),

F(mR)=
 [integral_0^R dr' r' J(r')sinh(mr')]
 /[m integral_0^R dr' r'^2J(r')].
```

Fifteen dimensionless rows test `ell/R={0.1,0.3,1}` and
`r/R={1.25,1.5,2,5,10}`. The source normalization residual is
`2.22e-16`, the massless residue is exactly unchanged, and every
order-reduced exterior correction is zero. These rows are not MTS
predictions because no physical `b_Box`, range, or scalar charge is inserted.

## 7. Selected ordinary-matter profiles

Checkpoint 4943 already derives, in the selected integrated-`H` parent,

```text
Args(S_SM)={H,Phi_SM,theta_SM},
J_psi=delta S_SM/delta psi=0,
Gamma_eff[H,psi,Phi_SM]=Gamma_eff[H,-psi,Phi_SM],
psi_boundary=0,
Q_psi=0.
```

`S_Box2` is reflection even and its first variation vanishes at `psi=0`.
Therefore

```text
E_psi=E_PX+b_Box Box^2 psi-J_psi=0
```

is solved by `psi=0` for arbitrary local `b_Box`.

The fourth-order boundary variation gives the finite-action and generalized
flux packet

```text
[psi]_Sigma=0,
[n.nabla psi]_Sigma=0,
[b_Box Box psi]_Sigma=0,
[Z n.nabla psi-b_Box n.nabla Box psi]_Sigma=0.
```

The zero profile satisfies all four conditions. Every metric variation of
`S_Box2` contains `Box psi` or a derivative of `psi`, so

```text
T_Box2,mn|psi=0=0.
```

Diffeomorphism invariance gives

```text
nabla_mu T_Box2^{mu}{}_nu=E_Box2 nabla_nu psi.
```

There is no independent on-shell force current. Eight source-backed rows—
Earth, Sun, a one-solar-mass white dwarf, and a neutron-star proxy at one and
ten times mean density—therefore retain

```text
psi=0,
Q_psi=0,
a_psi/a_N=0
```

without choosing `b_Box`.

## 8. Consequence for checkpoints 4981 and 4982

Checkpoint 4981 used a minimal scalar Laplace block at `X=0`. Checkpoint
4983 now supplies the missing qualification:

```text
minimal scalar block = valid essential-frame representative
                       of the local analytic derivative expansion;
raw off-shell b_Box  = not proved numerically zero.
```

Local field redefinitions can shift local counterterms and their Jacobians,
so finite off-shell determinant contacts still require one common frame.
The universal on-shell packet and selected zero-motion local branch are not
changed. A nonanalytic form factor or a nonperturbatively retained extra pole
would require a new calculation and is not imported into the 4981 result.

## 9. What is established

```text
four- versus six-derivative O2 notation                   = separated;
covariant Box2 variation and Hessian                       = derived;
independent local-jet check                                = passed;
flat p4 scalar two-point projector                         = derived;
Bochner/IBP relation                                       = derived;
scalar EOM field redefinition                              = derived;
complete local four-derivative essential dimension         = one;
essential beta source                                      =16g^2;
running b_Box=0 frame law                                  = derived;
compact-source order-reduced exterior correction           = zero;
selected ordinary-matter Box2 profile                      = zero;
selected scalar charge and one-scalar fifth force          = zero.
```

Not established:

```text
numeric beta_bBox                                          = false;
global invertibility of the derivative field map           = false;
nonperturbative heavy fourth-order mode                     = false;
complete nonlocal Z(-Box) form factor                       = false;
six-derivative spillover of the running scalar frame        = open;
finite interacting parent metric TTT                        = false;
exact all-operator local GR                                 = false;
full MTS                                                    = false.
```

## 10. Next target

Checkpoint 4984 should derive or source the running essential-frame
connection `gamma_Box=beta_bBox/(2Z)` and propagate its induced
six-derivative operator shifts. If that full off-shell coefficient cannot be
closed immediately, the direct local route is to prove that the nonanalytic
motion two-point form factor is source-silent on the selected `J_psi=0`,
zero-boundary branch. Do not resurrect an exact heavy pole from a truncated
EFT or treat `b_Box=0` as a fundamental axiom.

## Outputs

- `post-checkpoint-work/scripts/Y5_R2FR_4983_box2_essential_quotient_and_local_profile.py`
- `post-checkpoint-work/source-intake/functional_rg/4983/box2_operator_notation_and_source_scope.csv`
- `post-checkpoint-work/source-intake/functional_rg/4983/box2_covariant_hessian_contract.csv`
- `post-checkpoint-work/source-intake/functional_rg/4983/box2_local_jet_crosscheck.csv`
- `post-checkpoint-work/source-intake/functional_rg/4983/box2_four_derivative_essential_quotient.csv`
- `post-checkpoint-work/source-intake/functional_rg/4983/box2_running_frame_and_projector.csv`
- `post-checkpoint-work/source-intake/functional_rg/4983/box2_sourced_local_profile_response.csv`
- `post-checkpoint-work/source-intake/functional_rg/4983/box2_junction_and_local_GR_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4983/box2_essential_local_profile_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4983/box2_essential_local_profile_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4983/PROVENANCE.md`
- `post-checkpoint-work/scripts/Y5_R2FR_4983_box2_essential_quotient_and_local_profile_validation.py`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4983_VALIDATION.csv`
- `post-checkpoint-work/source-intake/functional_rg/4983/VALIDATION_PROVENANCE.md`
- `formalization-workbench/999-PPC4161-box2-essential-quotient-and-local-profile.md`
