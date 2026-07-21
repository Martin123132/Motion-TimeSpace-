# 4948 - Parent motion Hessian to galaxy phase-flow and universal-Jgap interface

Marker: `MTS_PARENT_HESSIAN_GALAXY_PHASE_2PI_INTERFACE_4948`.

Date: `2026-07-13`.

Status: private analytic, source-acquired and source-executed checkpoint. The
actual completed parent Hessian is compared to the sibling galaxy phase laws
and to the latest public/local galaxy artifacts without modifying the galaxy
repository. The projective logistic shape is now derived exactly from parent
eigenmode ratios. The direct one-point-field identification nevertheless
fails: the natural spectral-shell map predicts a growing exponent near `1.85`,
not the only locked galaxy exponent `0.77`; the current matter functor has no
linear `psi` source; and the irrelevant `O4` eigenvalue does not by itself
populate a boundary mode or generate its stress. A reflection-even two-point
occupation `G=<psi psi>` is selected as the next parent-derived route because
it can remain nonzero while `<psi>=0` and can be varied through a covariant
2PI action for a conserved metric stress.

## 1. Read-only galaxy source state

The public repository was acquired read-only at

```text
https://github.com/Martin123132/MTS-Galaxy-Lab-
HEAD 5c2fc082adcc67d779cfd99d5b6e9a9c9ac5fcbd
```

The clone at `D:\g4948` was clean before and after this checkpoint. No galaxy
file was edited.

The documented canonical ROTMOD support is

```text
q_locked=0.77,

S_gal(R)
 =Gamma0 L_eff [1-exp(-(R/L_eff)^q_locked)].
```

The local v19 artifacts remain explicitly candidate-level:

- the buffered `Theta` field is labelled `weak but safe` and has fitted
  `beta=1.10`;
- the `Xi` motion source/sink kernel is labelled plausible with a narrow null
  margin;
- the state-derived source normalization is labelled a candidate for a field
  equation.

These are valuable empirical constraints. They are not imported into the
parent as fields or couplings.

## 2. Exact projective eigenmode theorem

Use a covariant spectral shell of physical radius `R`. An angular or radial
shell eigenvalue scales as inverse radius, so write

```text
k(R)=xi/R,
d ln k/d ln R=-1.
```

The constant `xi` is a shell/regulator convention. It changes transition
radii but not logarithmic exponents.

For the relevant motion-mass eigenperturbation with critical exponent
`theta>0`, define the positive amplitude ratio

```text
r_n(R)=C_n (m_gap/k)^theta.
```

Then

```text
d ln r_n/d ln R=theta.
```

The bounded projective coordinate

```text
n=r_n/(1+r_n)
```

therefore obeys identically

```text
dn/d ln R=theta n(1-n).
```

For an irrelevant eigenmode with beta eigenvalue `lambda>0`, define

```text
r_b(R)=C_b (k/m_gap)^lambda,
b=r_b/(1+r_b).
```

It follows identically that

```text
db/d ln R=-lambda b(1-b).
```

The numerical finite-difference residuals are `1.76e-11` for `n` and
`1.32e-10` for `b`. Thus the sibling logistic equations do not need to be
postulated as fundamental nonlinear dynamics: they are projective coordinates
on linearly scaling positive eigenmode weights.

There are two distinct realizations:

1. **One two-state mode:** `b=1-n`. This forces `s=q` and `R_b=R_n`.
2. **Two parent eigenmodes:** `q=theta_n`, `s=lambda_b`; independent source
   amplitudes set independent transition radii.

The sibling law may use the second realization only if both eigenmode
projectors and amplitudes are derived.

## 3. The canonical galaxy support is not the logistic occupation

Let

```text
x=R/L_eff,
f=1-exp(-x^q).
```

Direct differentiation gives

```text
df/d ln R=q x^q exp(-x^q)
          =q(1-f)[-ln(1-f)].
```

This is not

```text
q f(1-f).
```

The executed grid gives a nonzero maximum derivative discrepancy. Therefore
the projective occupation `n` cannot simply be relabelled as the canonical
exponential support. It may eventually source, gate or emerge into that
support, but that map still requires an action and stress derivation.

## 4. Actual parent exponents

The completed seven-coordinate spectrum has two motion-mass variants:

```text
theta_mass=1.84969344551166  for v=+2lambda,
theta_mass=1.85848385394298  for v=-2lambda.
```

The only motion-tagged irrelevant direction in this completed block is the
`O4=C^2(nabla psi)^2` mode,

```text
lambda_O4=3.99602545229438.
```

Under `k=xi/R`, the direct two-mode projective prediction is therefore

```text
q_parent in [1.84969,1.85848],
s_parent=3.99603
```

if `b` is identified with the `O4` mode.

The public galaxy repository's only locked numerical `q` is `0.77`. It is not
proved to be the same variable as the sibling phase exponent, so the following
is explicitly a comparison gate rather than an identification. If they are
identified, the parent prediction is about `2.40` times larger. Forcing the
locked number would require

```text
k(R) proportional R^-zeta,

zeta in [0.414316,0.416285],
```

instead of the spectral-shell value `zeta=1`. No current parent equation owns
that anomalous radial scale map. It cannot be inserted merely to recover
`0.77`.

The result is consequently:

```text
logistic form                         = derived;
MTS numeric phase exponent            = predicted conditionally by Hessian;
identity with locked galaxy q=0.77    = false/open;
direct q=0.77 match                   = rejected under k=xi/R.
```

## 5. One universal gap and source-dependent radii

The universal motion coordinate gives

```text
J_gap=m_gap^2 G_N,
ell_gap=1/m_gap=sqrt(G_N/J_gap).
```

The transition radii are

```text
R_n=xi ell_gap C_n^(-1/theta),
R_b=xi ell_gap C_b^(1/lambda).
```

This separates two logically different ingredients:

- `J_gap` fixes one universal motion length and may not be retuned by galaxy;
- `C_n[T_b]` and `C_b[T_b]` are source/state amplitudes and can generate
  galaxy-dependent transition radii without becoming new couplings.

This factorization is a useful bridge to the empirical `L_eff[h,f_gas,...]`.
It does not derive `L_eff`: that requires calculating `C_n,C_b` from the
parent Green function and baryonic metric/source state.

## 6. Exact source-amplitude obstruction

The selected reflection-even parent satisfies

```text
delta S_matter/delta psi=0,
Gamma_eff^(1,n)|psi=0=0,
Q_psi=0.
```

With stable quadratic operator and vacuum boundary conditions, the classical
equation has the exact solution

```text
psi=0.
```

There is consequently no classical linear baryonic source for `C_n` or
`C_b`. The completed local branch also gives

```text
T_O4,mn|psi=0=0.
```

The `O4` eigenvalue supplies a possible scaling exponent, not a populated
mode. Its weak-curvature kinetic correction and stress are silent on the
selected vacuum. Thus

```text
parent eigenvalue != source amplitude != stress tensor.
```

This is the missing step that the earlier kinematic logistic observation did
not close.

## 7. Why the v19 candidates are not silently adopted

The galaxy artifacts propose useful targets:

```text
(1-ell_Theta^2 nabla_r^2)Theta=A_phase[X_b]P_b,

Delta S_Xi
 =[beta_add A_source-beta_sink A_sink]
   S_canonical G_midouter,
```

with a source-derived normalization candidate. But the current parent
Hessian contains no `Theta`, no derived `A_phase`, no `A_source/A_sink`
projection and no derivation of the displayed beta coefficients. Inserting
them would reproduce an empirical candidate by declaration, not connect MTS
to the galaxy law.

Similarly, substituting `n(R)` or `b(R)` directly into `V_model^2` does not
define

```text
T_activation,mn=-2/sqrt(-g) delta Gamma_activation/delta g^mn.
```

Without that variation there is no Bianchi-compatible conservation law and
no same-action lensing prediction. The direct one-point-Hessian-to-galaxy map
is therefore rejected at the source/stress gate even though its logistic
algebra passes.

## 8. Reflection-even composite survivor

The source obstruction applies to the one-point field `<psi>`. It does not
force the reflection-even two-point function to vanish:

```text
bar_psi=0,
G(x,y)=<psi(x)psi(y)>.
```

Use the Euclidean-convention 2PI action

```text
Gamma_2PI[g,G]
 =S_g[g]+S_m[g]
  +1/2 Tr ln G^-1
  +1/2 Tr(D^-1[g]G-1)
  +Gamma_2[g,G].
```

Stationarity gives the Dyson equation

```text
delta Gamma_2PI/delta G=0,

G^-1=D^-1[g]+2 delta Gamma_2/delta G.
```

The state-dependent physical object is the vacuum-subtracted correlator

```text
Delta G_state=G_state-G_vac.
```

Positive parent-mode projectors can define occupation ratios from
`Delta G_state`; the projective theorem then supplies the logistic radial
coordinates. Source dependence may enter through `D^-1[g(T_b)]`, the 2PI
self-energy and universal state/boundary conditions while preserving
`bar_psi=0`.

Most importantly, the metric source is variational:

```text
T_occ,mn
 =-2/sqrt(-g)
   delta[Gamma_2PI-S_g]/delta g^mn
   at stationary G.
```

For a diffeomorphism-covariant truncation,

```text
nabla^m(T_matter,mn+T_occ,mn)=0
```

on the metric and Dyson equations. The local correspondence limit is

```text
Delta G_state -> 0
 -> T_occ -> 0
 -> checkpoint 4947 GR/Newton/Maxwell branch.
```

This route does not introduce a direct scalar charge, so it can preserve the
4943 fifth-force zero while allowing a nonzero gravitational occupation
stress. It remains a contract, not a calculated galaxy solution.

The 2PI construction is source-anchored to J. Berges,
*Introduction to Nonequilibrium Quantum Field Theory*,
`https://arxiv.org/abs/hep-ph/0409233`. The disk application, projectors and
MTS matching are new derivation targets rather than claims from that source.

## 9. Decision

```text
projective Hessian -> logistic form                  = derived;
natural radial shell dlnk/dlnR                       = -1;
parent growing exponent                              = 1.84969--1.85848;
conditional O4 boundary exponent                     = 3.99603;
canonical exponential support itself logistic        = false;
locked q=0.77 identified with phase q                 = false;
direct natural-shell match to 0.77                    = rejected;
one universal J_gap transition factorization         = derived;
source amplitudes C_n,C_b from one-point field        = absent;
O4 boundary stress on psi=0                           = zero;
v19 Theta/Xi fields parent-derived                    = false;
activation stress from direct logistic insertion      = false;
direct one-point Hessian galaxy map                   = rejected;
reflection-even 2PI occupation contract               = defined;
2PI disk state/source/stress solution                 = open;
galaxy repository modified                            = false;
full MTS galaxy unification                           = false.
```

This is not a return to the old freeze. The parent now explains why the
logistic coordinates are natural and supplies numerical candidate exponents.
The remaining obstacle has been narrowed to a calculable object: a populated,
source-dependent, reflection-even two-point state and its conserved stress.

## 10. Artifacts

- `post-checkpoint-work/scripts/Y5_R2FR_4948_motion_Hessian_to_galaxy_phase_flow.py`
- `post-checkpoint-work/source-intake/functional_rg/4948/motion_Hessian_galaxy_phase_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4948/projective_logistic_derivation.csv`
- `post-checkpoint-work/source-intake/functional_rg/4948/parent_exponent_to_galaxy_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4948/source_amplitude_and_stress_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4948/composite_2PI_survivor_contract.csv`
- `post-checkpoint-work/source-intake/functional_rg/4948/galaxy_readonly_snapshot.csv`

## Next target

`4949-Y5-R2FR-covariant-2PI-motion-occupation-Dyson-source-and-conserved-galaxy-stress-or-composite-route-rejection.md`

Construct the reflection-even 2PI truncation from the completed parent,
derive its renormalized axisymmetric Dyson equation and metric stress, and
test whether any stable state generates nonzero `C_n[T_b],C_b[T_b]` with one
`J_gap`. Reject the composite route if vacuum subtraction, positivity,
conservation, local-GR recovery or source scaling fails. Do not fit SPARC
until the stress tensor exists.

No GitHub action is authorized.
