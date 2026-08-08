# 4981 - Parent motion-graviton-ghost Hessian and common-scheme two-point completion

Formal marker: `PPC4161_PARENT_HESSIAN_COMMON_SCHEME_4981`.

## Decision

Checkpoint 4981 performs the first transfer from the completed free-scalar
determinant to the declared MTS parent. It reconciles the latest integrated
metric, motion, gauge-fixing, and ghost inputs into one source-locked
quadratic Hessian. On the zero-motion-gradient background the Hessian
factorizes exactly, its signed supertrace has the correct two-graviton plus
one-scalar mode count, and its universal one-loop quadratic-curvature
logarithms are fixed.

This is a real parent result, but it is not the complete parent determinant:

```text
integrated-H parent field content                         = retained;
de Donder Einstein and vector-ghost Hessians              = source locked;
zero-gradient motion Hessian                              = derived;
signed parent supertrace                                  = derived;
Einstein-ghost plus motion universal two-point logs       = derived;
checkpoint-4979/4980 factor-of-two convention             = resolved;
leading interacting P(X) Schur correction                 = derived;
finite massive-motion threshold                           = open;
finite graviton-ghost-motion metric TTT                    = open;
full quantum BRST restoration                             = not proven;
exact all-operator local GR                               = false;
full MTS                                                  = false.
```

The runner passes `18/18` gates and the independent validator passes
`68/68`. No web or GitHub action was performed.

## 1. Parent being calculated

The retained parent is not a scalar-only composite-gravity ansatz. Its field
integral contains an independent nondegenerate densitized inverse metric,

```text
H^(mu nu)=sqrt(-g) g^(mu nu),
g^(mu nu)=H^(mu nu)/sqrt(-det H),
sqrt(-g)=sqrt(-det H),
```

together with motion, visible matter, gauge, gauge-fixing, and ghost fields.
Its leading infrared action has the form

```text
Gamma_IR = (M_R^2/2) integral sqrt(-g)(R-2 Lambda_cal)
           +Gamma_motion[g,psi]
           +S_visible[g,Phi,A]+Gamma_higher.
```

Checkpoint 4961 already established the boundary: an independent metric and
Diff/BRST quotient cannot be derived from the single motion scalar used in
the minimal branch. They therefore remain explicit parent data. This
checkpoint derives consequences of that declared parent rather than
pretending to bootstrap its ontology from a scalar loop.

## 2. Source-locked gauge-fixed Hessian

The acquired gravitational source uses the linear split

```text
g_mn=gbar_mn+h_mn
```

and gauge condition

```text
F_mu=kappa(nabla^a h_a mu-omega_bar nabla_mu h),
alpha=1,
omega_bar=1/2.
```

For the Einstein-Hilbert block the two nonminimal derivative coefficients
are

```text
1-1/alpha=0,
1-2 omega_bar/alpha=0.
```

The ghost nonminimal coefficient is independently

```text
1-2 omega_bar=0.
```

The locked operators are consequently of Laplace type:

```text
Delta_h=2 kappa^2 Z_N[-Box 1_T-2 Lambda+U_EH],
Delta_gh=-Box 1_V+R/d,
Delta_psi=Z_psi[-Box+m_gap^2]                 at x=0.
```

The Einstein kinetic supermetric acts on a symmetric tensor as

```text
K h=(1/2)h-(1/4)g tr(h).
```

Its four-dimensional spectrum is

```text
+1/2 with multiplicity 9,
-1/2 with multiplicity 1.
```

The negative trace eigenvalue is the familiar Euclidean conformal-sign
problem. It is recorded explicitly and is not reinterpreted as a new
physical ghost; a contour prescription remains separate from the
Faddeev-Popov cancellation.

## 3. Exact zero-motion factorization

Checkpoint 4956 derived the flat constant-gradient functional `P(X)` block

```text
H_hh=I_10+32 pi g K[p M0+x p' M1+x^2 p'' M2],
H_hpsi=sqrt(32 pi g) q K sqrt(x)[p' B1+x p'' B2],
H_psipsi=1+q^2[2p'-1+4x p''z^2].
```

The canonical conditions are

```text
p(0)=0,
p'(0)=1/2.
```

Therefore at `x=0`

```text
H_hh=I_10,
H_hpsi=0,
H_psipsi=1,
```

in the normalized regulated variables. This proves, rather than assumes,
the zero-gradient factorization of the metric and motion determinants.

The corresponding one-loop signed determinant is

```text
W_parent^(1)
 = +(1/2) Tr_T log Delta_h
   -       Tr_V log Delta_gh
   +(1/2) Tr_S log Delta_psi.
```

On flat space with `Lambda=0`, the weighted count is

```text
(1/2)(9+1)-4 = 1      [two graviton helicities],
1+(1/2)       = 3/2   [two graviton helicities plus one real motion scalar].
```

This is a signed supertrace identity, not a claim that ten metric
components propagate physically.

## 4. Action versus mixed-response normalization

An apparent factor-of-two difference between checkpoints 4979 and 4980 is
not an inconsistency. For either quadratic curvature invariant `I`,

```text
delta_1 delta_2 integral c I^2 = 2c I_1 I_2
```

on a flat background. Checkpoint 4979 tabulates the mixed two-point response;
checkpoint 4980 writes the action counterterm. Hence

```text
mixed response coefficient = 2 action coefficient.
```

The real minimal scalar contribution to the action is therefore

```text
Gamma_psi,log^(1)
 =1/[2(4pi)^2] integral sqrt(g)[
   (1/60)  Ricci log(-Box/mu^2) Ricci
  +(1/120) R     log(-Box/mu^2) R].
```

This resolves the normalization before any parent coefficients are added.

## 5. Parent universal quadratic logarithm

The acquired Einstein-plus-ghost proper-time source gives, in action
normalization,

```text
Gamma_EH+gh,log^(1)
 =(4pi)^-2 integral sqrt(g)[
   (7/20)  Ricci log(-Box/mu^2) Ricci
  +(1/120) R     log(-Box/mu^2) R].
```

Adding one real minimally coupled motion scalar on the massless ultraviolet
side of its threshold gives the zero-motion-background parent result

```text
Gamma_parent,log^(1)
 =(4pi)^-2 integral sqrt(g)[
   (43/120) Ricci log(-Box/mu^2) Ricci
  +(1/80)   R     log(-Box/mu^2) R].
```

Equivalently, the mixed two-point response coefficients are `43/60` and
`1/40`. These are universal logarithmic coefficients. The source constants
`c_R(m)` and `c_Ric(m)` remain scheme dependent, and no finite parent
three-point claim follows from the logarithms alone.

If the physical motion pole has nonzero `m_gap`, the displayed scalar term
is its ultraviolet coefficient. For `q^2 << m_gap^2` it decouples into a
mass-dependent analytic expansion. The covariant massive-scalar engine from
checkpoint 4980 supplies the required operator contacts, but the physical
`m_gap` threshold has not yet been evaluated as a parent prediction.

## 6. First interacting-motion correction

Away from `x=0`, write the metric-motion Hessian as

```text
H(x)=[[A0+x A1+..., sqrt(x) B_half+...],
      [sqrt(x) B_half^T+..., C0+x C1+...]].
```

The exact block determinant identity gives

```text
det H=det A det(C-B^T A^-1 B).
```

Consequently

```text
(1/2)Tr log H
 =(1/2)Tr log A0+(1/2)Tr log C0
 +(x/2)Tr[
    A0^-1 A1
   +C0^-1 C1
   -C0^-1 B_half^T A0^-1 B_half]
 +O(x^2).
```

For the checkpoint-4956 normalization,

```text
A1=16 pi g K(M0+M1),
B_half=sqrt(8 pi g) q K B1,
C1=2p''(0)q^2(1+2z^2).
```

The mixing term is already order `x`; separate metric and scalar
determinants are therefore wrong at the first nonzero motion background.
A deterministic block-matrix control verifies the exact Schur identity to
machine precision and the first-order coefficient with relative secant
residual `7.27124851569186e-05` at `x=3e-5`, converging linearly with `x`.

This is the concrete bridge to the next parent calculation: evaluate this
derived Schur kernel covariantly, rather than importing the free-scalar
answer into the interacting branch.

## 7. Covariance and GR scope

Because the locked regulators are functions of background-covariant
Laplace-type operators, the quadratic supertrace is background
diffeomorphism covariant. The acquired proper-time flow is nevertheless a
one-loop-improved approximation and explicitly assumes a non-running ghost
action. It does not by itself prove the full quantum Slavnov-Taylor identity
or restoration of split symmetry.

The result is compatible with the retained local GR/Newton/Maxwell branch:

```text
M_R^2(G_mn+Lambda_cal g_mn)=T_mn,
G_N=1/(8 pi M_R^2),
nabla^2 Phi=4 pi G_N rho.
```

The newly derived logarithms are higher-curvature quantum corrections. They
vanish on a Ricci-flat vacuum at this quadratic order and do not alter the
leading Einstein pole or Newtonian residue. This does not predict the
numerical value of `G_N`, remove the explicit integrated metric from the
parent, or prove exact compact-body GR at every operator order.

## 8. Promotion and next target

Promoted:

```text
parent gauge-fixed quadratic Hessian at x=0             = true;
signed Einstein-ghost-motion supertrace                 = true;
parent universal quadratic-curvature logarithm          = true;
zero-motion scalar contact architecture transfer        = true;
leading nonzero-motion Schur correction                 = true.
```

Not promoted:

```text
physical m_gap finite threshold                         = false;
interacting P(X) finite determinant                     = false;
finite parent metric TTT                                = false;
full quantum BRST identity                              = false;
exact all-operator local GR                             = false;
full MTS                                                = false.
```

The next target is checkpoint 4982: covariantize and project the order-`x`
Schur kernel, including the metric, motion, and ghost regulator insertions,
and fix its two-point subtraction before attempting any finite parent TTT
comparison.

## Outputs

- `post-checkpoint-work/scripts/Y5_R2FR_4981_parent_motion_graviton_ghost_hessian_and_common_scheme.py`
- `post-checkpoint-work/scripts/Y5_R2FR_4981_parent_motion_graviton_ghost_hessian_and_common_scheme_validation.py`
- `post-checkpoint-work/source-intake/functional_rg/4981/parent_gauge_fixed_hessian_contract.csv`
- `post-checkpoint-work/source-intake/functional_rg/4981/parent_supertrace_mode_count.csv`
- `post-checkpoint-work/source-intake/functional_rg/4981/parent_common_scheme_log_coefficients.csv`
- `post-checkpoint-work/source-intake/functional_rg/4981/motion_metric_schur_expansion_crosscheck.csv`
- `post-checkpoint-work/source-intake/functional_rg/4981/parent_contact_transfer_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4981/parent_hessian_common_scheme_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4981/parent_hessian_common_scheme_results.json`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4981_VALIDATION.csv`
