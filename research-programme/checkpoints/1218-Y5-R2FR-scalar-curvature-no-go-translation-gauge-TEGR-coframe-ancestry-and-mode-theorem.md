# 5202 - Scalar-curvature no-go, translation-gauge TEGR coframe ancestry and mode theorem

Marker: `MTS_5202_TRANSLATION_GAUGE_TEGR_COFRAME_ANCESTRY_THEOREM`.

Checked: `2026-07-24`.

## Decision

This checkpoint makes a constructive move rather than recording another
missing input.

The old single motion scalar cannot generate the non-scalar coframe needed
for local GR. More generally:

1. fewer than four scalar gradients cannot make a nondegenerate
   four-dimensional metric;
2. four independent exact gradients with a fixed internal Minkowski metric
   only pull flat spacetime into new coordinates;
3. adding one scalar conformal factor still forces the Weyl tensor to vanish
   and therefore cannot reproduce a generic GR vacuum such as
   Schwarzschild;
4. allowing an arbitrary internal metric `G_AB(X)` restores ten metric
   components but merely rewrites a metric theory rather than deriving
   geometry from scalars.

The scalar-only route is therefore rejected as the ancestry of curved local
GR.

The minimum constructive repair within the relational Cartan route is

```text
four relational fields X^A
+ one internal-vector-valued translation connection mathcalB^A_mu
+ one flat inertial Lorentz connection omega^A_Bmu.
```

They form the coframe

```text
e^A = D_omega X^A + mathcalB^A.
```

The parity-even two-derivative torsion action is then forced onto the TEGR
ray if its pure-tetrad, Weitzenbock-gauge quadratic form is required to retain
all six frame null directions. With the sign convention used here,

```text
S_grav
 = -(M_R^2/2) integral d^4x e T_TEGR
   - M_R^2 integral d^4x e Lambda_cal,

T_TEGR
 = (1/4) T^rho_mn T_rho^mn
   +(1/2) T^rho_mn T^(nm)_rho
   -T_m T^m.
```

The exact identity

```text
R_LC[e] = -T_TEGR[e,omega_inertial]
          +2 e^-1 partial_mu(e T^mu)
```

makes this action equal to the Einstein-Hilbert action in the bulk when the
boundary variational problem is matched. Consequently, this construction
does not merely resemble GR in a weak-field limit: its minimal local
gravitational equations are exactly Einstein's equations.

This is a real local-GR bridge, but it is conditional on adopting
`mathcalB^A_mu` as a new fundamental MTS parent field. The old scalar corpus
has not derived that connection. The result is therefore a constructed and
sharply constrained parent candidate, not a claim that the original scalar
alone secretly contained GR.

## 1. Scalar-only curvature obstruction

Consider a metric made from `N` scalar gradients,

```text
g_mu_nu = G_ab(X) partial_mu X^a partial_nu X^b.
```

At every point,

```text
rank(g) <= rank(partial_mu X^a) <= N.
```

Therefore `N<4` is necessarily degenerate in four dimensions. In
particular, the old motion scalar has rank at most one and cannot supply a
spatial triad.

For four independent scalars with a fixed internal metric,

```text
g_mu_nu = eta_AB partial_mu X^A partial_nu X^B,
det(partial_mu X^A) != 0,
```

the inverse-function theorem makes `X^A` valid local coordinates. In those
coordinates,

```text
ds^2 = eta_AB dX^A dX^B,
```

so the Riemann tensor vanishes identically. The executable witness

```text
e^A_mu = diag(1, 1+2 alpha x, 1, 1)
```

is nontrivial as a coordinate Jacobian but returns

```text
det(e) = 1+2 alpha x,
T^rho_mu_nu = 0,
T_TEGR = 0,
R_LC = 0.
```

Multiplying this scalar-gradient metric by a single conformal factor does
not repair the general problem. A conformally flat metric has

```text
C_mu_nu_rho_sigma = 0,
```

whereas Schwarzschild has

```text
C_mu_nu_rho_sigma C^mu_nu_rho_sigma
 = 48 (G_N M)^2/r^6.
```

An arbitrary `G_AB(X)` can encode curvature, but it carries the ten
components that had to be explained. It is a field redefinition of metric
content, not scalar-only emergence.

## 2. Relational translation-gauge construction

Introduce four relational labels,

```text
X^A = (X^0, X^1, X^2, X^3),
```

where `X^0` is a clock label and `X^i` are three spatial rod labels. Introduce
the translation connection

```text
mathcalB^A = mathcalB^A_mu dx^mu.
```

The coframe is

```text
e^A = D_omega X^A + mathcalB^A.
```

Under a local internal translation,

```text
X'^A = X^A + epsilon^A,
mathcalB'^A = mathcalB^A - D_omega epsilon^A,
```

and hence

```text
e'^A = e^A
```

exactly. The executable uses rational matrices and obtains an exact zero
residual matrix, not a floating-point approximation. Its sample coframe has

```text
det(e) = -3,
```

so the worked construction is nondegenerate.

Under a local Lorentz transformation,

```text
e'^A = Lambda^A_B e^B,
Lambda^T eta Lambda = eta,
```

and therefore

```text
g_mu_nu = eta_AB e^A_mu e^B_nu
```

is invariant. An exact rational boost gives a zero metric residual.

In the teleparallel gauge sector,

```text
R^A_B[omega_inertial] = 0.
```

The torsion is

```text
T^A = D_omega e^A
    = R^A_B[omega] X^B + D_omega mathcalB^A
    = D_omega mathcalB^A.
```

Thus the nonholonomy that represents gravity is carried by the field
strength of `mathcalB^A`, not by an exact scalar gradient.

This is the precise MTS interpretation proposed by this checkpoint:

```text
time   -> X^0 and the timelike coframe leg e^0;
space  -> X^i and the spatial coframe legs e^i;
motion -> the nonholonomic translation connection mathcalB^A;
gravity -> T^A=D_omega e^A, equivalent to Levi-Civita curvature.
```

`mathcalB^A` is not the galaxy outer-wall exponent `B=8`, and it is not the
old motion scalar `psi` with a new symbol.

## 3. TEGR coefficient-selection theorem

Start with the parity-even quadratic torsion family

```text
L_quad = c1 I1 + c2 I2 + c3 I3,

I1 = T^rho_mu_nu T_rho^mu_nu,
I2 = T^rho_mu_nu T^(nu mu)_rho,
I3 = T_mu T^mu.
```

The executable builds the full `16 x 16` quadratic Hessian around a
Minkowski coframe. Requiring the six antisymmetric frame directions to be
null in Weitzenbock gauge gives a coefficient-constraint matrix with

```text
rank = 2,
nullity = 1.
```

The unique ray is

```text
(c1,c2,c3) proportional to (-1/4,-1/2,+1),
```

or

```text
L_quad = -T_TEGR.
```

This is an exact necessity-and-sufficiency result within the stated
three-invariant family:

* exact constraints from several rational momenta establish the
  rank-two necessity result;
* substituting the selected ray with arbitrary symbolic
  `k_mu=(k0,k1,k2,k3)` annihilates all six frame generators and all four
  linearized diffeomorphism generators;
* the generic witness `L=I1` has a nonzero frame response.

The wording matters. A covariant inertial spin connection can make generic
new-general-relativity actions manifestly Lorentz covariant. The theorem
here is stronger and narrower: only the TEGR ray keeps the six
pure-tetrad frame directions null after Weitzenbock gauge fixing and is
Einstein-Hilbert equivalent. It is not a claim that every other covariant
torsion action is mathematically inconsistent.

## 4. Exact Einstein-equivalence witnesses

The general connection-difference identity is

```text
R_LC = -T_TEGR + B_T,
B_T = 2 e^-1 partial_mu(e T^mu).
```

Three independent exact symbolic witnesses were executed.

### 4.1 Flat FLRW

For

```text
e^A_mu = diag(1,a(t),a(t),a(t)),
```

the executable obtains

```text
T_TEGR = 6 adot^2/a^2,

R_LC = 6(a addot+adot^2)/a^2,

B_T = 6(a addot+2 adot^2)/a^2,

R_LC + T_TEGR - B_T = 0.
```

### 4.2 Spatially varying conformal coframe

For

```text
e^A_mu = Omega(x) delta^A_mu,
```

it obtains

```text
T_TEGR = -6 Omega_x^2/Omega^4,

R_LC = -6 Omega_xx/Omega^3,

B_T = 6(-Omega Omega_xx-Omega_x^2)/Omega^4,

R_LC + T_TEGR - B_T = 0.
```

### 4.3 Boundary-sensitive anholonomic shear

For

```text
e^0=dt,
e^1=dx+kappa_s x dy,
e^2=dy,
e^3=dz,
```

the result is

```text
T_TEGR = 0,
R_LC = -2 kappa_s^2,
B_T = -2 kappa_s^2,
R_LC + T_TEGR - B_T = 0.
```

This third witness is important because curvature is nonzero while the
torsion scalar happens to cancel. The boundary term alone closes the
identity, so the EH/TEGR boundary contract cannot be silently discarded.

With matched boundary data,

```text
delta S_TEGR/delta e^A_mu
 = delta S_EH/delta e^A_mu
```

in the bulk.

## 5. Modes and ghost gate

At a generic rational four-momentum, the selected quadratic tetrad Hessian
has

```text
rank = 6,
nullity = 10.
```

The ten exact null directions span

```text
six pure-tetrad frame directions
+ four linearized diffeomorphism directions.
```

The four diffeomorphism directions must not be confused with the internal
Stueckelberg translation:

* `delta e^A_mu=partial_mu xi^A` is the linearized diffeomorphism action
  after the background coframe identifies internal and spacetime indices;
* `delta X^A=epsilon^A`,
  `delta mathcalB^A=-D epsilon^A` leaves `e^A` unchanged.

The Hessian rank is not itself counted as six propagating degrees of
freedom. The nonlinear two-mode result follows from the exact
Einstein-Hilbert action identity and its Hamiltonian constraints.

For transverse-traceless perturbations, the selected quadratic form is

```text
L_TT
 = (1/2)(h_plus^2+h_cross^2)(omega^2-k^2).
```

Therefore the time kinetic residue is positive for

```text
M_R^2 > 0.
```

The minimal translation-gauge TEGR parent has the same two tensor modes as
GR. This ghost statement does not automatically extend to:

```text
generic quadratic torsion coefficients;
f(T) nonlinearities;
separate kinetic terms for X^A;
mass/reference-metric potentials;
an independent curved Lorentz connection.
```

Those extensions are rejected from the minimum parent or sent to separate
mode analyses.

## 6. Source and matter-coupling theorem

Because

```text
e^A_mu = D_mu X^A + mathcalB^A_mu
```

enters linearly in `mathcalB`, the chain rule gives

```text
delta S/delta mathcalB^A_mu
 = delta S/delta e^A_mu.
```

If the action has no explicit `X^A` dependence beyond the coframe,
integration by parts gives

```text
delta S/delta X^A
 = -D_mu(delta S/delta e^A_mu).
```

The `X^A` equation is therefore the translation/diffeomorphism Ward
consequence of the coframe equation, not an extra scalar equation.

For all visible matter coupled to the same coframe,

```text
delta S_matter/delta mathcalB^A_mu
 = delta S_matter/delta e^A_mu
 = -e T_A^mu.
```

The rank-ten Hilbert source established at checkpoint 5201 is retained.
With visible spinors using `omega_LC[e]` (equivalently the inertial
teleparallel connection plus contortion), the bulk equation is

```text
M_R^2(G_mu_nu+Lambda_cal g_mu_nu)
 = T_total_mu_nu.
```

It follows that the already executed 5201 local branch is inherited:

```text
nabla^2 Phi = 4 pi G_N rho,
G_N = 1/(8 pi M_R^2),

(gamma,beta,xi,alpha1,alpha2,alpha3,
 zeta1,zeta2,zeta3,zeta4)
= (1,1,0,0,0,0,0,0,0,0).
```

The Maxwell sector also uses the same `g[e]`, so its Hilbert stress,
Poynting vector and gravitational source are unchanged:

```text
T_00^EM = (E^2+B^2)/2,
T_0i^EM = (E cross B)_i.
```

No separate Newtonian, orbital, lensing, electromagnetic-energy or
gravitational-wave coupling is introduced.

The relation

```text
G_N = 1/(8 pi M_R^2)
```

is derived, but the absolute value of `G_N` is still one measured
calibration scale. This checkpoint does not derive Newton's constant from a
dimensionless MTS parameter.

## 7. What is derived and what is assumed

### Derived here

* the scalar-count rank obstruction;
* the flatness of four exact gradients with fixed `eta_AB`;
* the conformal-Weyl obstruction;
* exact translation-gauge invariance of `e=DX+mathcalB`;
* exact local-Lorentz invariance of `g[e]`;
* the one-dimensional TEGR coefficient ray within the parity-even
  two-derivative torsion family;
* arbitrary-momentum frame and diffeomorphism nulls;
* positive TT residue for `M_R^2>0`;
* exact EH/TEGR bulk equivalence with a required boundary match;
* equivalence of translation-connection and coframe source variation;
* redundancy of the relational-coordinate equation.

### Parent premises still required

* four relational fields `X^A`;
* a new non-scalar translation connection `mathcalB^A_mu`;
* a flat inertial Lorentz connection in the minimal TEGR branch;
* one universal matter coframe;
* the 5201 local state `psi=0`, `nabla psi=0` and open-domain boundary
  silence;
* `M_R^2>0`;
* measured calibration of the absolute `G_N` scale;
* matched EH/TEGR boundary data.

### Not derived

* `mathcalB^A_mu` from the old single motion scalar;
* a unique microscopic origin for the translation connection;
* dynamic selection of the exact local vacuum state;
* the absolute numerical value of `G_N`;
* the galaxy phase flow or its parameters from this local construction;
* a complete cosmological, particle and quantum unification.

## 8. Claim discipline

Allowed internal statement:

```text
A minimum relational translation-gauge MTS parent can be constructed whose
pure two-derivative gravitational branch is uniquely selected onto TEGR
within the tested torsion family and is exactly equivalent to local GR.
```

Forbidden statement:

```text
The original scalar MTS corpus has derived GR or uniquely predicted the
translation connection.
```

The checkpoint remains

```text
valid_for_full_MTS_claim = false.
```

It nevertheless moves the programme forward: local GR no longer has to be
inserted as an unexplained metric block. It can be written as the exact
dynamics of a relational motion/translation connection, with the extra
field ownership and remaining derivation debt stated openly.

## 9. Evidence products

Generator:

```text
scripts/Y5_R2FR_5202_translation_gauge_TEGR_coframe_ancestry_gate.py
```

Evidence directory:

```text
source-intake/functional_rg/5202/
```

Expected products:

```text
scalar_gradient_curvature_no_go.csv
relational_translation_gauge_construction.csv
TEGR_pure_tetrad_frame_coefficient_selection.csv
linearized_tetrad_Hessian_mode_gate.csv
TEGR_identity_symbolic_witnesses.csv
source_variation_equivalence.csv
MTS_time_space_motion_dictionary.csv
extension_and_ghost_guard.csv
route_decision.csv
source_provenance.csv
translation_gauge_TEGR_coframe_ancestry_results.json
```

Validation ledger:

```text
source-intake/mts_residuals/P8_Y5_BRR545_5202_VALIDATION.csv
```

The generator locks checkpoints 4070-4074, 5188-5189 and 5201; the
`formalization-workbench` tree; the previous 5201 output tree; the public
worktree; and the read-only galaxy repository.

## 10. Next route

The selected next route is

```text
ASSEMBLE_ONE_CANONICAL_TRANSLATION_GAUGE_MTS_PARENT_ACTION.
```

That checkpoint should place, in one action and one variation ledger:

```text
the relational packet X^A;
the translation connection mathcalB^A;
the flat inertial Lorentz connection;
the TEGR local gravity block;
the visible Maxwell/matter block;
the old reflection-even motion scalar;
the controlled C3/CFF/O4 corridor;
the CTP state/boundary sector.
```

It must then identify every cross-coupling allowed by the symmetries,
separate derived coefficients from calibrated coefficients, and verify that
the exact local GR branch, Maxwell source, galaxy collective branch and
cosmological branch are limits of the same action rather than a list of
unrelated effective models.
