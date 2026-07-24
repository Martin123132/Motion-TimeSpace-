# 5199 - Exact composite Legendre no-go and projective scale-covariance logistic reduction

Marker: `MTS_5199_COMPOSITE_LEGENDRE_PROJECTIVE_LOGISTIC_GATE`.

Date: `2026-07-24`.

## Decision

Checkpoint 5198 posed a sharp alternative: either the occupied-state
composite action generates the canonical logistic-kink vertex invariant

```text
I_logistic=(U'''^2)/(U'' U'''')=3,
```

or the exact phase flow must be demoted to a reduced-state closure.

The direct calculation has now been done rather than left as another target.
The sourced minimal canonical-kink route fails:

```text
bare |psi|^(4/3) one-point field                 I = 0.4;
exact ultralocal Y=psi^2 Legendre composite      I = 0.7794368858172214;
fractional quantum ground-state composite        I = 0.8298513092338069;
largest converged finite-temperature value       I = 0.871915721557117;
canonical logistic-kink target                   I = 3.
```

Positive mass, the first twelve converged eigenstates, and controlled
Gaussian 2PI closures do not bridge the gap. The source-locked parent
`P(X)` interactions are more than one hundred orders too small to produce
an order-one repair.

That result rejects the **flat-`n`-metric canonical Bogomolny realization**.
It does not reject the logistic phase law. The intended variable is a
normalized occupation, and normalized positive weights have a different
exact reduction:

```text
n = W1/(W0+W1),
z = W1/W0,
d ln W_a/du = Delta_a,
q = Delta_1-Delta_0

therefore

dn/du = q n(1-n).
```

The checkpoint-5148/5151 projective law is precisely

```text
n_q(R/L)=(R/L)^q/[1+(R/L)^q].
```

It is logistic in `u=ln(R/L)`. The phase law therefore does not require
arbitrary cubic and quartic Landau coefficients. It requires the parent
two-point problem to derive two positive scaling weights, their eigenvalue
difference `q`, their projected information metric and their normalization.

The result is a genuine reduction in what remains to be derived:

```text
old target:
  independently obtain m2:g3:g4 = 1:-6:12;

new exact target:
  obtain q=Delta_1-Delta_0 and the occupied/reference projective state
  from the parent composite stability problem.
```

The current numerical `q=0.7698811733853892` remains a conditional internal
scale closure from checkpoint 5198, not yet a parent-signed composite
eigenvalue. The outer `s=4`, `B=8` anti-wall also remains open.

No galaxy, local-GR or full-MTS claim is made.

## 1. Exact ultralocal composite Legendre transform

Take the reflection-even parent zero-mode measure

```text
Z(K)=integral dpsi
 exp[-a |psi|^p-K psi^2/2],

p=4/3,
a=3/4,
Y=psi^2.
```

At `K=0`,

```text
mu_n=<Y^n>
    =a^(-2n/p)
     Gamma[(2n+1)/p]/Gamma(1/p).
```

The exact moments are

```text
mu_1 = 1.4234932304235073,
mu_2 = 8.5555555555555556,
mu_3 = 104.86400130786504,
mu_4 = 2077.098765432099.
```

Writing the second through fourth cumulants of `Y` as `kappa_2`,
`kappa_3`, and `kappa_4` gives

```text
kappa_2 = 6.529222578494003,
kappa_3 = 74.09661761119041,
kappa_4 = 1443.8140892401253.
```

Use

```text
F(K)=-ln Z(K),
G(K)=<Y>=2 F'(K),
U(G)=F(K)-K G/2.
```

Then

```text
U'=-K/2,
G'=-kappa_2/2,
G''=kappa_3/4,
G'''=-kappa_4/8,
```

and the exact composite vertices are

```text
U''   =1/kappa_2
      =0.15315759081238962,

U'''  =-kappa_3/kappa_2^3
      =-0.26620362324469566,

U'''' =(3 kappa_3^2-kappa_2 kappa_4)/kappa_2^5
      =0.5936198898095163.
```

The signs agree with the stable logistic contract,

```text
U''>0,
U'''<0,
U''''>0,
```

but the invariant magnitude does not:

```text
I_ultralocal
 =kappa_3^2/(3 kappa_3^2-kappa_2 kappa_4)
 =0.7794368858172214,

I_logistic/I_ultralocal
 =3.848932550862654.
```

This mismatch cannot be removed by an overall action normalization or a
canonical linear rescaling of `G`.

There is a second obstruction. For any `K<0`,

```text
-a |psi|^(4/3)-K psi^2/2
```

grows without bound at large `|psi|`, so `Z(K)` diverges. The point `K=0`
lies on the edge of the Legendre source domain and has only a one-sided
neighbourhood. A positive quadratic mass moves the physical point into the
interior, but it does not fix the invariant.

## 2. Positive-mass ultralocal family

After rescaling, every positive quadratic deformation is represented by

```text
P_lambda(z) proportional
 exp[-z^2/2-lambda |z|^(4/3)],

0<=lambda<infinity.
```

The two exact endpoints are

```text
lambda=0         Gaussian Y=psi^2: I=2/3;
lambda=infinity  pure fractional:  I=0.7794368858172214.
```

The executed `74`-point quadrature over
`lambda=0` and `10^-6<=lambda<=10^6` is monotone between those endpoints.
No point approaches `I=3`. This scan is recorded as a numerical family
check; the endpoint values are exact.

## 3. Nonperturbative fractional quantum zero mode

The local-measure result is not enough because the parent has a kinetic
operator. The dimensionless pure fractional Hamiltonian is

```text
H(K)
 =-1/2 d^2/dpsi^2
  +(3/4)|psi|^(4/3)
  +K psi^2/2.
```

For a pure power potential, coordinate and energy rescalings remove the
dimensional kinetic and potential coefficients. The remaining composite
shape invariant therefore depends on the power `4/3`, not on an arbitrary
unit choice.

The calculation diagonalizes `H(0)` on a Dirichlet grid and evaluates the
first four Rayleigh--Schrodinger energy coefficients for the source operator

```text
V_K=psi^2/2.
```

If

```text
E(K)=E0+E1 K+E2 K^2+E3 K^3+E4 K^4+...,
```

then

```text
G0   =2 E1,
G'   =4 E2,
G''  =12 E3,
G''' =48 E4,

U''   =-1/(2G'),
U'''  =G''/(2G'^3),
U'''' =G'''/(2G'^4)-3G''^2/(2G'^5).
```

At box half-width `14`, `8000` grid points and `180` spectral states,

```text
E0   =0.6407814222367,
G0   =0.4910884701820,
G'   =-0.2896155511610,
G''  =0.582103155829,
G''' =-2.10007106685.
```

The direct fine-grid vertices are

```text
U''   =1.72642663005,
U'''  =-11.9813105273,
U'''' =100.198268561,
I     =0.829851350512.
```

A quadratic extrapolation in `dx^2` over `2000`, `3000`, `4000`, `6000`,
and `8000` grid points gives

```text
I_quantum,continuum=0.8298513092338069.
```

The checks are:

```text
last-two-grid residual                   < 5e-8;
fine-to-continuum residual               < 1e-7;
80-to-180 spectral-state span            < 1e-8;
matched-spacing box span for L>=8        < 1e-7.
```

Thus the quantum dynamics moves the invariant in the right direction but
only from `0.7794` to `0.8299`, not to `3`.

## 4. Mass and occupied-state rescue tests

### 4.1 Positive quadratic mass

The stable deformation is

```text
H_m
 =-1/2 d^2/dpsi^2
  +m^2 psi^2/2
  +(3/4)|psi|^(4/3),

m^2>=0.
```

The executed scan covers

```text
m^2=0 and 10^-4<=m^2<=10^3.
```

The invariant decreases from the fractional value toward the exact harmonic
limit

```text
I_harmonic=3/4.
```

Selected values are

```text
m^2=0      I=0.82985135;
m^2=0.1    I approximately 0.8180;
m^2=1      I approximately 0.7819;
m^2=10     I approximately 0.7566;
m^2->inf   I=0.75.
```

A negative quadratic mass is not an admissible rescue: because `2>4/3`,
it makes the potential unbounded below at large field.

### 4.2 Low eigenstates

The same fourth-order response was evaluated for the first twelve
nondegenerate eigenstates. Every converged state has

```text
U''>0,
U'''<0,
U''''>0.
```

Their invariant interval is

```text
0.7992200728 <= I <= 0.8298513505.
```

The maximum is the ground state, not an excited-state branch.

### 4.3 Thermal state

For the thermal free energy

```text
F_beta(K)=-(1/beta) ln Tr exp[-beta H(K)],
```

the eigenvalue perturbation series was exponentiated and summed before
taking the logarithm. This avoids unstable fourth numerical derivatives of
sampled free energies.

The converged spectral scan covers

```text
1.5<=beta<=100,
```

with exact endpoint checks:

```text
beta->0:       I=0.7794368858172214;
beta->infinity I=0.829851350512...
```

The executed thermal curve reaches

```text
beta_peak=5.079502521963518,
I_peak=0.871915721557117.
```

Independent `(L,N,N_state)` calculations

```text
(12,5000,140),
(14,8000,180),
(16,9000,180)
```

agree on the peak invariant within `2.5e-8`. This is the largest value found
in the controlled minimal state families, still a factor `3.44` below the
logistic target. It is an executed thermal scan, not a theorem over every
possible nonequilibrium density matrix.

## 5. Exact Gaussian 2PI bounds

Two controlled Gaussian reductions can be bounded analytically.

For the quantum variational form

```text
U_Q(G)=A/G+M G+B G^(2/3),
t=M/B>=0,
```

stationarity gives

```text
I_Q(t)
 =(81t+50)^2/
  [4(9t+5)(243t+155)],

dI_Q/dt
 =-45(81t+50)(81t+55)/
   [2(9t+5)^2(243t+155)^2] < 0.
```

Therefore

```text
3/4 <= I_Q <= 25/31
               =0.8064516129032258.
```

For the classical Gaussian entropy form

```text
U_C(G)=-A ln G+M G+B G^(2/3),
```

one obtains

```text
I_C(t)
 =2(27t+14)^2/
  [(9t+4)(243t+134)],

dI_C/dt
 =-36(27t+14)(135t+86)/
  [(9t+4)^2(243t+134)^2] < 0,
```

and hence

```text
2/3 <= I_C <= 49/67
               =0.7313432835820896.
```

Neither controlled Gaussian closure can generate `I=3`.

## 6. Known parent interactions cannot repair the ratio

Checkpoint 5185 already derived the sourced parent interaction packet. The
dynamic endpoint has

```text
c2=-7.283939259579509e-111 eV^-4,
c3= 1.3237331105996603e-223 eV^-8.
```

Its strongest conservative bounds are

```text
interaction kinetic norm ceiling       =3.492540005516476e-116;
Hartree stress fraction ceiling         =6.985080011032952e-116;
coherent accumulated phase ceiling      =5.306102337726383e-101;
maximum log10 collision exposure        =-281.88197921163953.
```

An unknown `O2` coefficient would require at least

```text
4.689488579429405e28
```

times its natural reference to become an order-one rescue. That is not a
controlled consequence of the current parent action.

The first nonlocal `X2` basketball also has the already derived Euclidean
coefficient

```text
-4 c2^2 integral [I2^2+2 I4].
```

It cannot be silently added twice on top of the evolved Vlasov response.
The sourced interaction sector therefore cannot move `I approximately 0.8`
to `I=3`.

## 7. What the failed invariant does and does not reject

The invariant

```text
I=(U'''^2)/(U'' U'''')
```

is unchanged by

```text
U -> C U,
G-G0 -> a(G-G0).
```

The calculations therefore reject the direct identification

```text
canonical composite G
  equivalent to
flat-metric kink coordinate n
```

within the sourced minimal parent truncation and tested state families.

They do not prove that every possible nonlocal 2PI action or nonequilibrium
state fails. Such a rescue would need a new parent-owned operator with an
order-one effect, not another normalization or an unsourced coefficient.

More importantly, they do not reject the radial occupation itself. A
canonical kink field and a normalized statistical occupation are different
geometries.

## 8. Projective scale-covariance theorem

Let `W0` and `W1` be positive weights of a reference and occupied composite
sector. Define

```text
n=W1/(W0+W1),
z=W1/W0.
```

Suppose a radial scale-covariant regime gives

```text
d ln W0/du=Delta0,
d ln W1/du=Delta1,
u=ln(R/L).
```

Then

```text
d ln z/du=Delta1-Delta0=q,
```

and direct differentiation gives

```text
dn/du
 =(1/(1+z)^2) dz/du
 =q z/(1+z)^2
 =q n(1-n).
```

Its unique solution with `n(u0)=1/2` is

```text
n(u)=1/[1+exp(-q(u-u0))]
    =(R/L)^q/[1+(R/L)^q].
```

This is exactly the projective occupation used in checkpoints 5148 and
5151. The numerical identity check over twenty logarithmic scale decades
has maximum residual `1.3e-16`.

The equivalent stable local entropy is

```text
F_bin(n;u)
 =n ln n+(1-n)ln(1-n)-q(u-u0)n.
```

Its stationary equation is

```text
ln[n/(1-n)]=q(u-u0),
```

which gives the same profile.

### Natural projective metric

The entropy Hessian is

```text
g_nn=d^2 F_bin/dn^2
    =1/[n(1-n)].
```

This is the Bernoulli/Fisher information metric. Its canonical coordinate is

```text
theta=2 asin(sqrt(n)),
n=sin^2(theta/2),
g_nn dn^2=dtheta^2.
```

The logistic flow becomes

```text
dtheta/du=(q/2) sin(theta).
```

A canonical first-order completion therefore has

```text
V_theta(theta)=q^2 sin^2(theta)/8,
```

not the flat-`n` quartic

```text
V_n(n)=q^2 n^2(1-n)^2/2.
```

This explains why demanding the `1:-6:12` quartic vertex ratio from the raw
covariance was too restrictive. It was a valid sufficient gate for one
metric choice, not a necessary condition for a projective occupation.

The parent calculation still has to show that its projected 2PI metric is
the Fisher/projective metric or derive the actual replacement. This
checkpoint does not insert that metric into the parent action by decree.

## 9. Inner exponent and outer wall

Checkpoint 5198 found the conditional internal scale equality

```text
q_scale=0.7698811733853892,
```

only `1.5432e-4` fractionally below the locked `0.77`. Because that equality
uses the shared phase shape, it is not independent evidence and is not yet
the parent composite eigenvalue.

The correct ownership contract is now

```text
q_collective
 =Delta_occupied-Delta_reference
 =0.7698811733853892
```

to the stated numerical tolerance. It must be calculated from the parent
composite stability/Bethe--Salpeter block. It must not be relabelled as the
existing elementary or UV relevant exponent near `1.85`.

The outer anti-wall has the identical projective form

```text
b(R)=1/[1+(R/(B L))^s],
db/du=-s b(1-b).
```

Its functional form is exact once the two boundary-sector weights scale
with difference `-s`. The present

```text
s=4,
B=8
```

remain state/boundary inputs. A finite-domain normalization and a
parent-derived exterior weight are still required.

## 10. Route decision

```text
bare fractional canonical kink:
  rejected;

minimal ultralocal composite canonical kink:
  rejected;

fractional quantum canonical kink:
  rejected in the sourced minimal truncation;

known P(X) interaction rescue:
  rejected as quantitatively uncontrolled;

projective scale-covariant occupation:
  retained conditionally and derives the logistic form exactly;

current q:
  conditional internal scale closure, parent eigenvalue open;

outer anti-wall:
  exact projective form, parent weights and parameters open;

local GR/Newton/Maxwell branch:
  unchanged.
```

The next calculation should not repeat cubic/quartic scans. It should project
the existing parent CTP/2PI covariance into occupied and reference sectors
and calculate:

```text
1. positivity and normalization of W0 and W1;
2. the scaling difference Delta1-Delta0;
3. the induced metric on n=W1/(W0+W1);
4. whether q=0.7698811733853892 is returned;
5. the exterior/boundary sector giving s and B.
```

If that projection cannot be derived, the logistic phase remains an explicit
reduced-state closure. If it can, the inner phase flow is parent-owned
without inserting arbitrary Landau vertices.

## 11. Claim boundary

Derived or rejected here:

```text
exact ultralocal composite vertices                       derived;
source-domain boundary of pure fractional measure         proved;
positive-mass ultralocal rescue                           rejected numerically;
nonperturbative fractional quantum zero-mode vertices     derived numerically;
grid, box and spectral convergence                        passed;
positive quantum mass rescue                              rejected numerically;
first twelve eigenstate rescues                           rejected numerically;
converged thermal rescue scan                             rejected numerically;
quantum/classical Gaussian 2PI rescue                     rejected analytically;
known sourced P(X) interaction rescue                     rejected quantitatively;
flat-n Bogomolny vertex gate                              rejected in minimal route;
projective scale-covariance logistic theorem              exact;
binary entropy and Fisher metric                          exact;
canonical projective angle potential                      exact conditionally;
```

Still open:

```text
parent selection of occupied/reference projectors;
parent composite scaling eigenvalue q;
parent match to the projective/Fisher metric;
source-selected phase normalization;
outer boundary weights, s and B;
full axisymmetric nonlinear state;
projected lensing likelihood;
galaxy, local-GR or full-MTS claim.
```

The occupied projective route remains locally silent when its occupied
weight vanishes. It introduces no second vacuum pole and does not alter the
checkpoint-5197 separation between the universal local GR branch and the
environmental collective phase.

## 12. Reproduction and files

Executable:

```text
scripts/Y5_R2FR_5199_composite_Legendre_projective_logistic_gate.py
```

Generated evidence:

```text
source-intake/functional_rg/5199/
  exact_ultralocal_composite_vertices.csv
  ultralocal_positive_mass_scan.csv
  fractional_quantum_zero_mode_convergence.csv
  fractional_quantum_positive_mass_scan.csv
  fractional_quantum_eigenstate_scan.csv
  fractional_quantum_thermal_scan.csv
  Gaussian_2PI_analytic_bounds.csv
  projective_scale_covariance_derivation.csv
  known_parent_interaction_gate.csv
  logistic_invariant_comparison.csv
  route_decision.csv
  source_provenance.csv
  composite_Legendre_projective_logistic_results.json
```

Validation:

```text
source-intake/mts_residuals/P8_Y5_BRR545_5199_VALIDATION.csv
```

The protected `formalization-workbench`, checkpoint-5198 output tree, public
worktree and read-only galaxy repository are locked during execution. No
GitHub action is part of this checkpoint.
