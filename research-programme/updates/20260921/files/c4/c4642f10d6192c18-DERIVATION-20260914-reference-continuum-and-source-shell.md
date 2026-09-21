# Reference continuum equations and the surviving source shell

Date: 2026-09-14. Private continuation; no GitHub action, no subagents.
Scope: the existing stationary-source nearest-neighbour reference on the annulus
5 <= R <= 6, not the unrestricted parent theory.

## 1. Result and its precise status

There is now an explicit continuum identification, not just a name attached to
the reference branch. Its bulk equations, under the convergence hypotheses
stated below, are the spherical Einstein equations coupled to canonical massless
scalar matter. The shrinking stationary reservoir is NOT empty vacuum: it has
a finite surface mass, a specific lapse matching, and a calculable required
supporting surface stress.

New work in this note:

1. Derive the bulk scalar, mass, lapse, and energy-flux equations from the
   nearest-neighbour expressions.
2. Calculate the Einstein tensor independently and match its components.
3. Derive an O(h) bound for scalar energy in the source collar from the actual
   cumulative endpoint force; this rules out a scalar boundary atom on the
   previously controlled interval.
4. Integrate the actual source constraint to obtain the thin-shell mass jump
   and the physical midpoint-clock normalization.
5. Identify the surface stress required for GR matching, without pretending
   that a parent material/action law for that stress has already been supplied.
6. Establish initial-data constraint consistency analytically, and test it
   against independent radial integration and physical h-refinement.

**Not proved here:** evolving reference-to-continuum convergence, absence of a
bulk quadratic defect for every admissible sequence, an unrestricted GR limit,
a complete parent source action, horizons, black-hole regularity, a Newtonian
limit of the entire theory, or a value of the measured Newton constant.

The previous result compares the two *discrete* branches. Combining it with
this identification still requires convergence of the evolving reference.
It is not legitimate to omit that intervening step.

## 2. Fixed conventions and inherited inputs

Read:

- `DERIVATION-20260914-reference-wave-boundary-decoupling.md`
- `DERIVATION-20260914-live-constrained-mass-relative-energy.md`
- `DERIVATION-20260914-boundary-compatible-h-evolution.md`
- `scripts/annular_compatible_h_evolution_20260914.py`
- `scripts/annular_horizontal_clock_evolution_20260913.py`

Use c = 1, radius R, time t in the existing PILOT units, and

    F = 1 - 2m/R,  U = sqrt(F),  L = NU,
    ds^2 = -N^2 dt^2 + dR^2/F + R^2 dOmega^2.

The scalar momentum p used here is angular-reduced and NOT the surface
pressure P introduced later. The coupling is kappa = 0.1 in this pilot.
For a canonically normalized four-dimensional scalar, the comparison with GR
is kappa = 4 pi G. This is a normalization/calibration identification, not a
derivation of G. Physical SI scales have not been assigned by this test.

Nodes have spacing h, collar width epsilon = h/2, and offsets z in [-1/2,1/2].
The layer weight is W(z) = 6(z+1/2)(1/2-z), with integral W dz = 1.
Node weights omega are h internally and h/2 at the endpoints.
The right source has chi = 0, prescribed velocity and acceleration zero,
and reservoir S = 0.003, independent of z and time.
The mass seed is 0.8 at the full inner support edge, which tends to R = 5.

The physical clock is N/U = 1 at b = 6, the *middle* of the source collar.
The full support ends at B_h = 6+h/4. These are different cuts.

The inherited estimates are conditional on classical solutions in the regular
chart and uniform on fixed T < 0.0008345769328864052 in pilot units.
Saved numerical trajectories reach 0.06; testing identities there does not
extend the proved uniform time interval.

## 3. Bulk limit: do not confuse weak density convergence with pointwise convergence

For a common layer z, the reference equations are

    chi_t,i = L_i p_i/R_i^2,
    omega_i p_t,i = Fedge_i - Fedge_(i-1),
    Fedge_i = c_i (chi_(i+1)-chi_i)/h,
    c_i = (R_i^2 L_i + R_(i+1)^2 L_(i+1))/2.

The collar scalar energy density is the W/epsilon-weighted sum of the
nearest-neighbour potential and omega_i p_i^2/(2R_i^2).
Its mass is concentrated into collars separated by vacuum gaps.

Already for smooth initial data, the raw density is generally zero in the gaps
and approximately three times the averaged density at collar centres.
It does not have the desired pointwise limit. The correct passage is a weak
density/Riemann-sum passage, together with control of the quadratic energies.

Retain the layer label provisionally. Assuming energy-consistent convergence,
regular limiting fields and well-defined required traces, the limit is

    ebar = (1/2) integral W(z) [R^2 chi_R(z)^2 + p(z)^2/R^2] dz,
    Jbar = L integral W(z) p(z) chi_R(z) dz,

    chi_t(z) = L p(z)/R^2,
    p_t(z)   = partial_R [R^2 L chi_R(z)],

    m_R       = kappa F ebar,
    (log N)_R = m/(R^2 F) + kappa ebar/R.

The metric is common to the layers. A collection of unsynchronized layers is
a weighted collection of canonical scalar fields, not automatically one scalar.

### 3.1 Conditional synchronization is a uniqueness statement, not an assumption

The actual smooth preparation tends to the same chi and p at every z.
The limiting boundary data are also common: zero left scalar flux and fixed
right chi = 0. For two regular limiting layers, their difference solves the
same linear wave equation on their common limiting metric.

Define

    Edelta = (1/2) integral_5^6 L [
                 delta p^2/R^2 + R^2 delta chi_R^2 ] dR.

Integration by parts gives

    Edelta_t = (1/2) integral_5^6 L_t [
                 delta p^2/R^2 + R^2 delta chi_R^2 ] dR.

The endpoint product is zero: left flux is zero and right delta chi_t is zero.
If L > 0 and |L_t/L| is locally bounded, Gronwall and zero initial difference
give Edelta = 0. The right Dirichlet value removes the constant scalar ambiguity.

Thus an adequately converged regular limit is synchronized and is one
Einstein–scalar system. This argument does NOT by itself prove compactness
of the original joint (t,R,z) family or eliminate an unproved bulk defect measure.

### 3.2 The mass-time equation follows; it need not be borrowed

From the two scalar equations,

    ebar_t = partial_R Jbar + (L_R/L) Jbar.

Combining the radial constraints gives

    L_R/L = 2m/(R^2 F)                       (away from the reservoir).

Differentiate m_R with respect to time. For

    d = m_t - kappa F Jbar,

the exact residual equation is

    d_R + (2 kappa ebar/R) d = 0.

The fixed inner mass and zero inner flux imply d(5) = 0, hence

    m_t = kappa F Jbar.

This supplies the energy-flow sign and normalization from this system's own
equations. The sign is important: an outward travelling positive-energy wave
has negative enclosed mass rate with these momentum conventions.

### 3.3 Independent Einstein-tensor and action check

For the metric above, direct Christoffel/Ricci calculation gives

    G^t_t = -2m_R/R^2,
    G^R_R = -2m/R^3 + 2F N_R/(RN),
    G^R_t = 2m_t/R^2.

For canonical scalar stress, summed with weight W if necessary,

    rho = F ebar/R^2,    p_radial = rho,
    T^R_t = F integral W chi_R chi_t dz.

The derived equations therefore give G^mu_nu = 2 kappa T^mu_nu for these
components. Covariant scalar conservation and the contracted Bianchi identity
then force the remaining angular component: if only the equal angular residuals
remain, their radial divergence is -2 E^theta_theta/R.

Independently, the angular-divided scalar action is

    S_scalar/(4 pi) =
      integral dt dR [ R^2 chi_t^2/(2NU) - R^2 NU chi_R^2/2 ].

Its canonical p is R^2 chi_t/(NU), producing the same two first-order equations.
This checks the matter normalization. It does not derive an unrestricted
Einstein–Hilbert parent action from the original motion sector.

For orientation, the standard polar-areal Einstein–scalar variables are
alpha = N, a = 1/U, Phi = chi_R, Pi = p/R^2. Compare equations (1), (4)–(9),
and (12) of [Ferrer-Sánchez et al., arXiv:2511.15247v1](https://arxiv.org/html/2511.15247v1).
The Einstein tensor and mass-time law here were calculated independently;
the displayed mass-time formula in that source's equation (10) is not adopted.

In vacuum bulk, m is constant and N = C(t) sqrt(F); time reparametrization
gives the Schwarzschild form wherever F > 0. This is an annular vacuum
identification, not a horizon or global black-hole theorem.

## 4. Actual endpoint control: scalar energy does not create a boundary atom

Let EV = E0(Y_reference,t). Use the inherited lower coefficient bound

    c_i >= cmin = r_min^2 w_min,
    r_min = 4.9, r_max = 6.1, w_min = 0.459221543661712.

The actual free-node force equation telescopes:

    Fedge_i = sum_(j<=i) omega_j p_t,j.

Cauchy–Schwarz, sum omega_j <= 1, and the kinetic part of EV give

    integral W sup_i |Fedge_i|^2 dz <= 2 r_max^2 EV.

This includes the half-weight left endpoint; it is not an imposed plateau.
Since the source scalar is zero,

    chi_(n-2) = -h Fedge_(n-2)/c_(n-2).

The source-node scalar potential integrated over its collar is consequently

    E_source,scalar
      = integral W R_source^2 chi_(n-2)^2/(4h) dz
      <= [r_max^4/(2 cmin^2)] h EV.

The same argument bounds the gradient contribution of any fixed number of
boundary collars by O(h) EV. The gradient part of EV and q_source = 0 also give

    integral W sup_i |q_i|^2 dz <= 2 EV/r_min^2.

Since p_i = R_i^2 q_i/L_i and L_i >= w_min, their kinetic energies are O(h) EV.
Thus no scalar energy atom is left at either endpoint on the inherited
uniformly controlled time interval.

The left edge obeys the sharper trace estimate

    integral W |Fedge_0|^2 dz <= 2 r_max^2 omega_0 EV = O(h) EV.

A regular limiting trace is therefore Neumann at the left endpoint.
This is a reflecting annular boundary, NOT proof of a smooth continuation
through R = 0 or of matching to an arbitrary interior spacetime.

These statements concern the reference. The earlier branch-decoupling estimate
is what connects the MTS sequence to it; we have not silently substituted
independent smoothness of MTS.

## 5. Shrinking reservoir: integrate first, then match

The exact finite-width equation is

    U_R = m/(R^2 U) - kappa U e/R - kappa sigma/R,
    integral_source sigma dR = S.

The first term has O(h) integral in the regular chart. Section 4 bounds the
source scalar integral by O(h) EV. Thus, on the controlled interval,

    U_plus - U_minus = -kappa S/b
    N_plus = N_minus = N_shell.

Here both limiting traces refer to the same areal radius b = 6.
At finite h the two endpoints have different radii: their vacuum U variation
is O(h) and can even mask the negative source contribution. One must not read
a finite-width endpoint difference as an already asymptotic shell jump.

Write mu_shell = kappa S. Then

    U_plus = U_minus - mu_shell/b,
    m_plus - m_minus = mu_shell U_minus - mu_shell^2/(2b).

The quadratic term is gravitational binding, obtained directly from
m = b(1-U^2)/2. No source coefficient was fitted to obtain it.

### 5.1 The midpoint clock leaves a finite factor

W is symmetric and the reservoir E is constant across layers. Half the source
mass lies on each side of the physical clock cut. The same integrated equation
up to the midpoint gives

    U_mid = U_minus - mu_shell/(2b) = (U_minus+U_plus)/2.
    N_shell = U_mid.
    g_plus = N_shell/U_plus.

Although the limiting lapse is continuous, U has a jump. The selected midpoint
prescription is retained as part of the regulator's physical clock convention.
It cannot be replaced by N_shell = U_minus or U_plus without changing time
normalization. For a different reservoir profile, replace S/2 by its left
cumulative mass; symmetry is used explicitly here.

An appended vacuum exterior has

    N_ext(R) = N_shell sqrt(1-2m_plus/R)/U_plus(b).

We have derived the matching data for such an exterior, not evolved a new
exterior or proved a maximal spacetime extension.

### 5.2 GR requires a supporting surface stress, not pressureless static dust

Let Sigma be proper surface energy density and P the tangential surface
pressure, with normals oriented towards increasing R. GR junction conditions
give

    Sigma = -[U]/(4 pi G b) = S/b^2,
    P = ([U N_R/N] + [U]/b)/(8 pi G)
      = ([U N_R/N] + [U]/b)/(2 kappa).

S is angular-reduced: physical proper shell mass is 4 pi S and its geometric
mass is G(4 pi S) = kappa S. Omitting this convention creates a factor-of-4pi
error.

For vacuum immediately on both sides,

    P = (Sigma/4) [1/(U_minus U_plus) - 1].

These are the static matching relations also given in equations (20)–(21) of
[Acuña-Cárdenas, Sarbach and Tessieri, arXiv:2407.02718v1](https://arxiv.org/html/2407.02718v1).
Their wave-scattering calculations and equations of state are not imported
as MTS results. We independently checked the junction algebra.

If the interior scalar has a nonzero energy trace e_minus and the exterior is
vacuum, retain the extra term:

    P = P_vacuum_formula - U_minus e_minus/(2b).

Consequently the vacuum expression is not automatically valid for a wave
striking the source. Dirichlet chi = 0 makes its time derivative zero, but
does NOT make its spatial derivative or radial pressure zero.

There is also a direct finite-collar consistency check at the compact initial
preparation, where scalar energy is exactly absent near the source.
The radial equations then imply rho_source = U sigma/R^2 and p_radial = 0.
Static stress conservation requires tangential pressure, with proper integral

    P_h = integral_source sigma m/(2R^3 F) dR.

Its thin limit equals the expression above. Equivalently, conservation of
m_plus under a virtual shell displacement and the surface-work law

    d mu_shell/db = -2 kappa b P

give the same P. Both identities were checked symbolically.

**Ownership limit:** these equations derive the surface stress that GR would
require for this prescribed stationary source. They do not yet show that the
parent apparatus action supplies this stress, a material equation of state,
or stability under radial displacement. Keep it explicitly as a supported
boundary unless and until that action variation is supplied. Requiring the
correct stress is stronger than ignoring it, but not the same as deriving
its physical origin.

## 6. Initial constraint consistency and reproducible tests

For the actual common smooth bump b0(R),

    chi0 = 0.02 b0,    p0 = 0.004 R^2 b0,
    e0(R) = (R^2/2)[(0.02 b0')^2+(0.004 b0)^2].

Its support lies strictly inside [5.2,5.8]. Smooth Taylor/Riemann-sum estimates
give a uniform O(h) bound for the cumulative density discrepancy

    sup_R | integral_5^R (e_h-e0) dR | <= C h,

including partial collars. Full moments can converge faster; pointwise density
need not converge at all. Endpoint support padding contributes nothing for
this preparation.

In the source-free bulk, the mass error satisfies

    delta m_R + (2 kappa e_h/R) delta m = kappa F_cont (e_h-e0).

Apply its integrating factor and integrate the right side by parts against
the cumulative discrepancy. The coefficient's supremum and total variation
are bounded uniformly by the L1 energy and regular-chart bounds. This yields
uniform bulk delta m = O(h). The lapse constraint, similarly integrated, gives
delta log N = O(h), with the matching normalization fixed in section 5.
Thus the initial radial constraint problem has a consistent continuum target.
This proof does not replace the harder evolving compactness argument.

### 6.1 Main refinement: same initial preparation, not refitted fields

Independent smooth radial IVP versus actual collar constraints, degree 12:

| nodes | max bulk mass error | max bulk log-lapse error | max weak energy moment error |
|---:|---:|---:|---:|
| 33 | 2.658824e-4 | 9.191111e-5 | 1.507191e-3 |
| 65 | 1.176702e-4 | 3.374227e-5 | 3.608659e-4 |
| 129 | 4.936934e-5 | 1.451191e-5 | 9.079293e-5 |
| 257 | 2.533533e-5 | 6.935048e-6 | 2.280830e-5 |

Bulk probes stop at 5.95; the source midpoint and one-sided support endpoints
are tested separately. This is an INITIAL constraint test, not a replay of
a continuum evolution.

At 257 nodes, in pilot units:

- source mass jump = 2.566439203762e-4;
- matched thin-shell mass-jump error = 1.57e-13;
- actual outer clock = 1.0000292221127338;
- thin-clock error = 2.11e-9;
- required surface pressure = 7.633510051263e-6;
- zero-pressure and zero-source alternatives give resolved discrepancies;
- treating the midpoint mass as exterior misses 1.283215200713e-4.

The extremely small matched mass-jump error isolates the shell map using the
actual interior mass. It is NOT a 1e-13 accuracy claim for the whole continuum
solution: the bulk error in the same run is 2.53e-5.
Finite endpoint U jump errors remain O(h), as predicted.

### 6.2 Verification scope

- Main runner: 41 checks pass.
- Exact symbolic calculation: 15 checks pass, including Einstein components,
  covariant wave, mass-flux compatibility, Bianchi angular residual, source
  root equation, Israel stress, and shell virtual work.
- Independent verifier: 30 checks pass.
- Degree 12 -> 16 and smooth IVP tolerance/step refinement pass.
- Fresh adaptive integration through the actual collars agrees with the
  collocation solution: mass error <= 4.67e-15, log-lapse error <= 1.06e-15.
- Source scalar-energy and left-flux inequalities are checked on all three
  saved reference grids at t = 0, 0.03, 0.06. Those diagnostic checks do not
  extend the analytic uniform time guarantee.

The adaptive verifier reuses the declared discrete density/preparation but
uses a different radial solver. The symbolic check derives tensors directly.
Neither is an external formal proof assistant or independent research group.

Evidence and executed code:

- `scripts/annular_reference_continuum_shell_20260914.py`
- `scripts/derive_annular_reference_continuum_shell_20260914.py`
- `scripts/check_annular_reference_continuum_shell_20260914.py`
- `scripts/verify_annular_reference_continuum_shell_20260914.py`
- `source-intake/navier-stokes/20260914/annular-reference-continuum-shell-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-reference-continuum-shell-algebra-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-reference-continuum-shell-independent-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-reference-wave-decoupling-final-integrity.json`

Source provenance is recorded in
`source-intake/navier-stokes/20260914/reference-continuum-shell-provenance.json`.
Final integrity and the immutable resume snapshot are produced by
`scripts/seal_annular_reference_continuum_shell_20260914.py`.

## 7. Next mathematical target

Prove evolving reference convergence to this now-explicit initial-boundary
problem: obtain strong enough scalar/momentum convergence to pass the
quadratic stress without a hidden bulk defect, account for the layer label,
and retain the derived shell and midpoint clock.

Then the existing discrete-branch decoupling estimate can transfer that
identified spherical GR limit to the MTS sequence on the common controlled
interval. Source-action ownership and longer-time control remain separate
requirements; neither should be disguised as solved by this identification.

This is a specific advance toward a derived restricted GR limit. It is not
a new empirical success or completion of the unified theory.

