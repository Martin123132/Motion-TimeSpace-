# 5205 - Normalized CTP regular-mode ensemble, Hamiltonian constraint and zero-`Lambda` second-moment selection theorem

Date: 2026-07-24

Marker: `MTS_5205_NORMALIZED_CTP_REGULAR_MODE_CONSTRAINT_STATE_SELECTION`

Status: private analytic and source-executed checkpoint. It fills the
homogeneous part of the checkpoint-5203 `Gamma_rho_i` slot with a positive
trace-one CTP state class, proves its quadratic stress conservation, and
derives exactly what the cosmological Hamiltonian constraint does and does
not select. This is the first constructive state result after the
checkpoint-5196 amplitude theorem. It is not a claim that the full
microscopic density matrix, primordial perturbation covariance or the
absolute value `Lambda_cal=0` has been derived.

## Executive result

The state slot can be populated lawfully:

```text
rho_i
 =int dA P(A)
   D(A v_reg) rho_0 D(A v_reg)^dagger,

int dA P(A)=1,
P(A)=P(-A).
```

Here `rho_0` is a centered parity-even positive density operator in one
finite regulated homogeneous cell, `D` is its Weyl displacement, and
`v_reg` is the phase-space direction fixed by radiation-era regularity.
Therefore:

```text
rho_i>=0;
Tr rho_i=1;
<chi>=<chi_N>=0;
<A^2>=sigma_A^2>=0.
```

For a Gaussian amplitude measure, the state is Gaussian with covariance

```text
V_i=V_0+sigma_A^2 v_reg v_reg^T.
```

Starting from a pure centered covariance

```text
V_0=diag(Q_0,1/(4Q_0)),
```

the exact determinant is

```text
det V_i
 =1/4
  +sigma_A^2[
     Q_0 v_p^2+v_q^2/(4Q_0)
   ]
 >=1/4.
```

Thus positivity and the one-mode uncertainty inequality are automatic. The
generator verifies the exact density-kernel trace and Hermiticity identities
and repeats the determinant check on 256 deterministic positive trials.

Every source-free regular homogeneous history is

```text
chi_A(N)=A u_reg(N).
```

At minimal canonical quadratic order, after subtraction of the centered
vacuum piece,

```text
<chi^2>=sigma_A^2 u_reg^2;
<chi_N^2>=sigma_A^2 u_reg,N^2.
```

Consequently the full homogeneous background stress depends on `P(A)` only
through `sigma_A^2`. Its higher moments are real state data, but they do not
enter this quadratic background.

The flat FLRW constraint is

```text
Omega_Lambda+K_0 sigma_A^2
 =1-Omega_m-Omega_r,

K_0=u_N0^2+mu^2 u_0^2.
```

This one equation has rank one over the two coordinates
`{Omega_Lambda,sigma_A^2}`:

```text
free Lambda:
  one state/action degeneracy remains;

declared Lambda=0 branch:
  sigma_A^2=(1-Omega_m-Omega_r)/K_0
  is unique and positive.
```

For the locked checkpoint-5195 zero-`Lambda` target, the result is

```text
K_0=0.5181888856456915;
sigma_A^2=1.3282310980366105.
```

This matches the independently rebuilt checkpoint-5196 regular amplitude

```text
A_reg(-12)^2=1.3282310980366112
```

to a residual `-6.66e-16`. The regular phase is already derived, so the
zero-`Lambda` quadratic background has no independent homogeneous-amplitude
fit coordinate.

The qualification is essential:

```text
second moment fixed inside declared Lambda=0 branch = yes;
Lambda_cal=0 derived from the parent                  = no;
unique microscopic density matrix                    = no;
primordial inhomogeneous covariance                   = no.
```

The next executable target is therefore

```text
RUN_CONSTRAINT_REDUCED_ZERO_LAMBDA_SCALAR_TENSOR_REFIT_
WITH_GDOT_BOUNDED_ZETA.
```

It will test the required `F_R` completion without adding an independent
homogeneous amplitude.

## 1. Relation to the prior state no-gos

This construction does not reverse or evade the earlier negative results:

```text
checkpoint 5156:
  the bulk Hessian does not select an arbitrary Gaussian covariance;

checkpoint 5179:
  a positive quartic-only boundary weight cannot generate the required
  occupied stress, and the weak induced hierarchy is insufficient;

checkpoint 5186:
  free FLRW vacuum production does not generate the required abundance;

checkpoint 5196:
  regularity fixes the phase but leaves one finite amplitude;

checkpoint 5204:
  the curvature pitchfork cannot prepare the fitted amplitude.
```

The new step asks a narrower and previously unfinished question:

```text
once the regular solution space is one dimensional,
what does the gravitational Hamiltonian constraint fix
about a normalized reflection-even state on that space?
```

The answer is exact. It fixes one second moment if `Lambda_cal` is fixed. It
does not manufacture a unique microscopic state or derive `Lambda_cal`.

## 2. Positive CTP state class

Let `q,p` be the regulated homogeneous canonical pair on the initial Cauchy
surface `Sigma_i`. Let `rho_0` be centered, parity even, positive and
trace one. The Weyl operator `D(A v_reg)` displaces its mean along the
regular phase-space direction

```text
v_reg=(u_i,p_i).
```

For every normalized nonnegative amplitude measure `P(A)`,

```text
rho_i
 =int dA P(A)D(A v_reg)rho_0D(A v_reg)^dagger
```

is positive because it is a convex mixture of positive operators. Its trace
is

```text
Tr rho_i
 =int dA P(A)Tr rho_0
 =1.
```

When `P(A)=P(-A)`, parity maps the `A` term to the `-A` term and all odd
amplitude moments vanish.

The corresponding CTP boundary action is not an extra bulk force:

```text
Gamma_rho_i[q_+,q_-]
 =-i ln <q_+|rho_i|q_->.
```

It is supported only on `Sigma_i`.

## 3. Exact Gaussian kernel

Write the zero-mean one-mode covariance as

```text
V=[[Q,C],[C,P]],
D=det V=QP-C^2.
```

The exact position-space density kernel is

```text
rho(q_+,q_-)
 =(2 pi Q)^(-1/2)
  exp[
   -(q_++q_-)^2/(8Q)
   -D(q_+-q_-)^2/(2Q)
   +i C(q_+^2-q_-^2)/(2Q)
  ].
```

The executable obtains

```text
int dq rho(q,q)=1;
rho(q_-,q_+)-rho(q_+,q_-)^*=0.
```

For a Gaussian distribution of regular displacements,

```text
V_i=V_0+sigma_A^2 v_reg v_reg^T.
```

Using the pure centered diagonal representative gives

```text
det V_i-1/4
 =sigma_A^2[
   Q_0 v_p^2+v_q^2/(4Q_0)
  ].
```

Every factor on the right is nonnegative. This is a proof, while the 256
numeric trials guard the implementation.

The construction is more general than the checkpoint-5152 two-branch
mixture. Choosing

```text
P(A)=[delta(A-A_*)+delta(A+A_*)]/2
```

recovers that state. Choosing a centered Gaussian gives the maximum-entropy
shape at fixed variance, but no maximum-entropy principle is promoted as an
MTS axiom here. At quadratic background order both choices are equivalent
when their second moments agree.

## 4. Regular-mode second-moment theorem

Checkpoint 5196 proves that the early regular solution has

```text
chi=A[
  1-mu^2 e^(4N)/(20 Omega_r)+O(e^(8N))
],

chi_N
 =-A mu^2 e^(4N)/(5 Omega_r)+O(e^(8N)).
```

The singular mode is removed, leaving the one-dimensional regular family

```text
chi_A=A u_reg.
```

For any normalized even measure,

```text
<chi>=0;
<chi^2>=sigma_A^2 u_reg^2;
<chi_N^2>=sigma_A^2 u_reg,N^2;
<chi chi_N>=sigma_A^2 u_reg u_reg,N.
```

At minimal canonical quadratic order,

```text
rho_chi
 =3 M_R^2 H0^2 sigma_A^2
  [E^2 u_N^2+mu^2 u^2],

p_chi
 =3 M_R^2 H0^2 sigma_A^2
  [E^2 u_N^2-mu^2 u^2].
```

Therefore

```text
w_chi
 =[E^2 u_N^2-mu^2 u^2]
  /[E^2 u_N^2+mu^2 u^2]
```

is independent of the amplitude distribution. The mass and regular transfer
fix the background shape; the state second moment fixes only its
normalization.

This exact stress formula is scoped to the minimal canonical
`zeta_c=0` target used by checkpoints 5193--5196. The finite nonminimal
coordinate required by checkpoint 5203 changes the scalar-tensor background
equations and is the reason a constrained refit is selected next.

## 5. Stress conservation

Define the unit-mode energy kernel

```text
R_u=E^2 u_N^2+mu^2u^2.
```

With

```text
E_N=hE,

u_NN=-(3+h)u_N-mu^2u/E^2,
```

direct differentiation gives

```text
dR_u/dN=-6E^2u_N^2.
```

Since

```text
rho_chi+p_chi
 =6M_R^2H0^2 sigma_A^2 E^2u_N^2,
```

the generated residual is exactly

```text
rho_chi,N+3(rho_chi+p_chi)=0.
```

This requires the amplitude weights to be transported by the state equation:

```text
partial_N P(A)=0
```

for the source-free ensemble. No logistic or other time-dependent weight is
inserted externally. Equivalently, every branch is conserved and averaging
commutes with the covariant divergence.

## 6. Hamiltonian-constraint rank theorem

Normalize the unit regular mode at `N_i=-12`. At the present epoch,

```text
Omega_chi,0
 =sigma_A^2 K_0,

K_0=u_N0^2+mu^2u_0^2.
```

Flatness gives

```text
Omega_Lambda+K_0 sigma_A^2
 =1-Omega_m-Omega_r.
```

As a linear map over

```text
(Omega_Lambda,sigma_A^2),
```

its matrix is

```text
[1,K_0].
```

For positive `K_0` this matrix has

```text
rank=1;
nullity=1.
```

Therefore flatness alone cannot choose between vacuum energy and state
energy. This is the precise free-`Lambda` obstruction.

On the declared `Lambda_cal=0` branch, however,

```text
sigma_A^2
 =(1-Omega_m-Omega_r)/K_0
```

is unique. This is a Hamiltonian-constraint selection inside that branch,
not a derivation of why the renormalized cosmological coordinate vanishes.

## 7. Locked target reconstruction

The calculation loads the raw checkpoint-5195 target rows and the
independently rebuilt checkpoint-5196 regular transfer.

| branch | `A_reg(-12)` | `K_0` | flatness remainder | constraint `sigma_A^2` | locked `A_reg^2` | residual |
|---|---:|---:|---:|---:|---:|---:|
| free `Lambda` | 0.4267395644 | 1.1080370029 | 0.2017809131 | 0.1821066558 | 0.1821066558 | 0 |
| `Lambda=0` | 1.1524890880 | 0.5181888856 | 0.6882745926 | 1.3282310980 | 1.3282310980 | -6.66e-16 |

The raw 5195 flatness residuals and the independent
`{chi_0,x_0}` reconstruction residuals also vanish to the validation
tolerance.

Radiation regularity fixes the initial phase ratios:

```text
free Lambda:
 chi_N/chi=-4.80777e-18 at N=-12;

Lambda=0:
 chi_N/chi=-1.84794e-18 at N=-12.
```

Thus the zero-`Lambda` branch has:

```text
mass mu:
  one universal fitted action coordinate;

regular phase:
  derived;

homogeneous second moment:
  fixed by the Hamiltonian constraint;

independent homogeneous amplitude parameter:
  none.
```

The free-`Lambda` branch retains one joint split between
`Omega_Lambda` and `sigma_A^2`.

## 8. Local-source and PPN gate

For every later compact domain `D` disjoint from the initial surface,

```text
supp(delta Phi) subset D,
D intersect Sigma_i = empty
```

implies

```text
delta Gamma_rho_i/delta Phi(x)=0.
```

The boundary state therefore adds no direct local source vertex.

Reflection evenness also gives

```text
<chi>=0.
```

But the following do not vanish:

```text
<chi^2>;
<T_chi>;
alpha_0^2;
Gdot/G.
```

The `+A/-A` branches have the same quadratic scalar-tensor response, so an
even mixture cannot cancel checkpoint-5204 local pressure. The model-specific
ceilings remain

```text
zeta_c<=5.65824e-4  (free Lambda target);
zeta_c<=1.62711e-4  (Lambda=0 target).
```

The result is therefore:

```text
direct boundary source in a later local domain = zero;
odd one-point scalar charge                    = zero;
exact absence of cosmological state stress     = false;
PPN/Gdot cancellation by parity                = false;
bounded leading local-GR branch                = retained.
```

## 9. Parameter and claim count

The constraint-reduced zero-`Lambda` background contains:

```text
G_N:
  one universal gravitational calibration;

J_gap=G_N m_pole^2:
  one universal motion-gap coordinate;

Lambda_cal:
  fixed to zero as a tested branch hypothesis, not predicted;

theta_regular:
  derived;

sigma_A^2:
  fixed by the Hamiltonian constraint;

higher moments of P(A):
  irrelevant to the quadratic background but open for interactions;

primordial inhomogeneous covariance:
  open.
```

This is more predictive than the free-`Lambda` state count without pretending
that all initial-state physics is solved.

## 10. Decision

```text
positive normalized homogeneous CTP state class = constructed;
exact Gaussian boundary kernel                   = derived;
radiation regular phase                          = derived;
quadratic background second-moment universality  = derived;
stress conservation                              = derived;
later direct local boundary source               = zero;

zero-Lambda homogeneous second moment:
  constraint-selected conditionally;

free-Lambda homogeneous amplitude:
  one degeneracy remains;

absolute origin of Lambda_cal=0:
  not derived;

unique microscopic density matrix:
  not derived;

primordial perturbation covariance:
  not derived.
```

This is not a demotion of the whole scalar branch. It supplies a concrete
lawful `Gamma_rho_i` macrostate and removes the independent homogeneous
amplitude from the tested zero-`Lambda` background.

## 11. Executed evidence

Generator:

`scripts/Y5_R2FR_5205_normalized_CTP_regular_mode_state_gate.py`

Evidence directory:

`source-intake/functional_rg/5205/`

Files:

```text
normalized_CTP_Gaussian_state.csv
regular_mode_second_moment_theorem.csv
quadratic_state_stress_conservation.csv
Hamiltonian_constraint_state_normalization.csv
local_boundary_silence_and_residuals.csv
state_parameter_count.csv
route_decision.csv
source_provenance.csv
normalized_CTP_regular_mode_state_results.json
```

Validation:

`source-intake/mts_residuals/P8_Y5_BRR545_5205_VALIDATION.csv`

Every row remains `valid_for_full_MTS_claim=false`.

## 12. Next calculation

The selected next route is

```text
RUN_CONSTRAINT_REDUCED_ZERO_LAMBDA_SCALAR_TENSOR_REFIT_
WITH_GDOT_BOUNDED_ZETA.
```

That calculation must:

1. use the same checkpoint-5203 Jordan-frame `F_R,V,Z` action;
2. impose `Lambda_cal=0` as an explicit tested branch hypothesis;
3. derive `sigma_A^2` from flatness at every likelihood evaluation rather
   than fitting a scalar fraction;
4. derive the regular phase by shooting rather than fitting it;
5. keep `zeta_c` inside the checkpoint-5204 LLR corridor or score the LLR
   likelihood directly;
6. solve the full scalar-tensor Friedmann equations rather than reusing the
   minimal scalar background;
7. compare against fitted `Lambda`CDM, `wCDM`, CPL and the locked minimal
   parent scalar using the same Pantheon+, DESI DR2, compressed-CMB and growth
   rows;
8. retain nonclaim status unless the new branch converges, remains interior
   and survives AIC/BIC plus local bounds.

If it fails, the zero-`Lambda` scalar-tensor route is rejected cleanly. If it
survives, the programme gains a same-action cosmology with no independent
homogeneous amplitude parameter.

## Sources

- Checkpoints 5152 and 5156: reflection-even state and Gaussian covariance
  structure.
- Checkpoint 5179: non-Gaussian boundary hierarchy and perturbative no-go.
- Checkpoints 5195 and 5196: fitted targets, regular transfer and amplitude
  theorem.
- Checkpoint 5200: positive CTP projector and state ownership.
- Checkpoint 5203: canonical CTP parent action.
- Checkpoint 5204: curvature-trigger rejection and local `zeta_c` ceilings.
