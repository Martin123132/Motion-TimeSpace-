# Implicit parent jets and the full shift defect

10 September 2026. Private continuation of the archived canonical annular
free-root tubes. Both GR-plus-canonical-scalar control and metric-Gram
candidate are subjected to the same construction. A finite-model obstruction
below is not a rejection of continuum GR or of the MTS research programme.
Final attempt01: **550/550 checks, 18 initial-root and 18 whole-tube cases**.
All 18 exact initial free roots have a certified nonzero full shift residual.

## 1. The derivatives are now owned by the root flow

Predecessor:
`DERIVATION-20260910-compatible-parent-root-and-local-residence.md`.
It encloses unique free-constraint roots Y(w,t), w=(x,pi,mu_inner), and a
positive residence time for their reduced flow. Its original numerical
states and archived map coefficients remain unchanged.

Write the original free constraints as F_f(y_f;w,t)=0, with J_ff their
free Jacobian. The scalar coordinates include the released Hermite slopes.
At each point of the already validated root tube, the reduced rules are

    x_dot = v(y),
    pi_dot = f(x,y),
    u_mu = P(y)^(-1) b(x,y),
    mu_inner,dot = u_mu,inner,
    b = j_Gram-j_matter.

Endpoint scalar velocities have the original affine local histories; their
accelerations are prescribed, their next derivatives zero. Endpoint nodal
momentum rates are exactly zero. No scalar slope force is discarded.

The new helper evaluates the same constraints and force with outward
normalized Taylor coefficients. It uses the original assembly maps, not the
older polynomial reconstruction with a different floating evaluation order.
Every reconstructed basis, Gram and link array is compared exactly with the
predecessor archive before it is used.

For the first jet, assign the known fixed rates

    y_fixed,1=(u_mu,inner,a_left,a_right).

Set free y_1 to zero temporarily, and evaluate the first Taylor coefficient
of F using x_1=v, pi_1=f and C_1 equal to the supplied clock rate. Call that
coefficient k_1. Linearity in the highest derivative gives the exact identity

    J_ff y_free,1 = -k_1.

A componentwise verified interval solve encloses y_free,1. This is the
implicit derivative of Y, not a new freely selected initial jet.

Next differentiate the shift equation itself:

    P u_mu = b,
    P u_mu,1 = b_1-P_1 u_mu.

The metric-link contribution to b_1 includes the varying link kernel AND
the varying Gram current. The second fixed packed derivative is therefore

    y_fixed,2=(u_mu,inner,1,0,0).

Obtain f_1 from the same force Taylor expansion with the completed first
jet. Use x_2=v(y_1), pi_2=f_1 and C_2=0. With only the fixed second packed
derivatives supplied, let k_2=2[t^2]F. Then

    J_ff y_free,2 = -k_2.

The factor of two matters: Taylor coefficients are normalized, whereas the
saved first/second jets are actual derivatives. Both inverse steps use the
actual enclosed Hessian; no guessed tangent, finite-difference acceleration
or independent second-jet box is used as a proof input.

Root uniqueness, smooth finite coefficients and the predecessor residence
theorem imply these are enclosures of the actual reduced solution's jets
throughout its short interval. A zero-containing interval for F_t or F_tt
is only a consistency check. The differentiated identities plus verified
inverse inequalities, not zero containment alone, establish the enclosure.

## 2. Full shift residual and its derivative

Define the coefficient mass-velocity mismatch and the full shift covector

    delta_mu = mu_dot-u_mu,
    R_shift = P delta_mu = P mu_dot-b.

Only delta_mu at the inner coefficient is zero by construction. It does NOT
follow that the inner ROW of R_shift is zero: P couples neighboring mass
coefficients. No other velocity mismatch or equation row is set to zero.

The completed second jet gives

    delta_mu,1 = mu_ddot-u_mu,1,
    R_shift,1 = P_1 delta_mu+P delta_mu,1
              = P_1 mu_dot+P mu_ddot-b_1.

Both equivalent forms are enclosed, and their intersection is retained.
The exact inner velocity and acceleration identities are used to avoid
independent-interval subtraction there. Every other component retains its
computed uncertainty and may be nonzero.

Calculations are performed on two different sets per saved state:

- The predecessor's initial root enclosure, with x, pi, inner mass, clock
  and endpoint velocities fixed to the original saved parameters.
- The entire predecessor parameterized root tube, including the varying
  clock and endpoint velocity histories.

Thus one can distinguish a nonzero defect at an exact nearby initial root
from a wide whole-neighborhood upper bound that merely contains zero.

If an initial component has sign-certified magnitude at least ell>0 and
its derivative magnitude is bounded by L over the root tube, then

    T_nonzero = min(T_residence, ell/(2L))

(with T_residence used when L=0) gives a nonzero residual on that interval.
The implementation rounds the time downward and checks T_nonzero L<ell
outward. This is a continuity estimate along the EXISTING reduced solution,
not a new trajectory integration.

For the same initial parameters and prescribed local histories, a different
choice of packed tangent cannot fix this residual while retaining all the
same reduced rules. J_ff is nonsingular and fixes the free tangent uniquely.
This is an obstruction to simultaneously imposing the additional shift
equations on this particular finite zero-shift reduction. It does not exclude
a different discretization, a different admissible parent evolution outside
this reduction, or a controlled continuum limit.

## 3. A constructive consistency route, not a counterterm by fiat

The earlier source identity in
`DERIVATION-20260909-metric-flux-cancellation-and-exact-constraint-jets.md`
already distinguishes weak constraint residuals, strong radial residuals and
the metric-link shift solve. Those distinctions also produce a useful
propagation identity for the present obstruction.

For a consistently differentiated positive-annulus reconstruction, define

    F=1-2mu/R, c=N sqrt(F), E=c/F,
    v=chi_t/c, w=chi_R, S=v^2+w^2,
    s=kappa R^2 F c v w,
    r_H=mu_R-(kappa/2) R^2 F S,
    r_E=(log E)_R-kappa R S,
    r_v=v_t-R^(-2)(R^2 c w)_R,
    r_w=w_t-(c v)_R.

These r terms are definitions, not equations silently set to zero. In the
Gram branch they include actual candidate contributions, in addition to
projection and quadrature discrepancies. Differentiating r_H and using
F_t=-2mu_t/R gives

    (r_H)_t = mu_tR+kappa R mu_t S-(kappa/2)R^2 F S_t,
    S_t=2c(vw)_R+4(c_R+c/R)vw+2(v r_v+w r_w).

With D=mu_t-s, rearrangement yields the off-shell identity

    D_R+kappa R S D
      = (r_H)_t+s r_E+kappa R^2 F(v r_v+w r_w).

Let I_mu be the continuous mass reconstruction, and define the separate
projection/current discrepancy

    e = I_mu u_mu-s,
    d = I_mu delta_mu = D-e.

Then the ACTUAL shift mismatch, not the bulk-only flux mismatch, satisfies

    d_R+A d = H,
    A=kappa R S >= 0,
    H=(r_H)_t+s r_E+kappa R^2 F(v r_v+w r_w)-e_R-A e.

The integrating-factor formula is

    d(R)=exp(-integral_a^R A) d(a)
         + integral_a^R exp(-integral_z^R A) H(z) dz.

Consequently, for continuous piecewise-smooth d,

    abs(d(R)) <= abs(d(a))+integral_a^R abs(H(z)) dz.

If the chosen inner interpolation trace is the fixed inner mass coefficient,
d(a)=0. Otherwise the trace term must be retained. Discontinuous
reconstructions additionally require their interface jump terms; they cannot
be discarded when moving this argument to another numerical formulation.

This supplies a concrete next derivation: reconstruct and bound H channel
by channel, including Gram/projected-current cancellation, and establish a
mesh-consistency rate if one exists. Small free weak covectors alone do not
bound (r_H)_t pointwise. Also the algebra for consistently differentiated
fields is not automatically an interval theorem for separately rounded
assembly value/gradient matrices. Their construction/IBP defects still have
to be linked to it explicitly. No rate, small integral or continuum closure
is assumed here, and no fitted cancellation force has been added.
The identity alone is not a repair or an independent smallness estimate:
backfilling H from d_R+A d would simply restate the measured mismatch. The
next calculation must obtain the source channels from the weak variational
equations and their projection/quadrature/boundary discrepancies, keeping
the candidate's Gram terms until their actual cancellation is established.

The following independent symbolic control was executed from this document
and returned `off_shell_shift_propagation_identity: exact_zero`, without
imposing either the scalar or metric equations. It checks the algebra only;
it does not evaluate or bound the reconstructed source H.

```python
import sympy as symbolic
radius, kappa, field_f, characteristic, speed, gradient = symbolic.symbols('R kappa F c v w', nonzero=True)
field_radial, characteristic_radial, speed_radial, gradient_radial = symbolic.symbols('F_R c_R v_R w_R')
mass_time, mass_time_radial, speed_time, gradient_time = symbolic.symbols('mu_t mu_tR v_t w_t')
norm_squared = speed**2 + gradient**2
bulk_flux = kappa * radius**2 * field_f * characteristic * speed * gradient
bulk_flux_radial = kappa * ((2 * radius * field_f * characteristic + radius**2 * field_radial * characteristic + radius**2 * field_f * characteristic_radial) * speed * gradient + radius**2 * field_f * characteristic * (speed_radial * gradient + speed * gradient_radial))
hamiltonian_time = mass_time_radial + kappa * radius * mass_time * norm_squared - kappa * radius**2 * field_f * (speed * speed_time + gradient * gradient_time)
lapse_residual = characteristic_radial / characteristic - field_radial / field_f - kappa * radius * norm_squared
wave_residual = speed_time - characteristic * gradient_radial - (2 * characteristic / radius + characteristic_radial) * gradient
kinematic_residual = gradient_time - characteristic_radial * speed - characteristic * speed_radial
left = mass_time_radial - bulk_flux_radial + kappa * radius * norm_squared * (mass_time - bulk_flux)
right = hamiltonian_time + bulk_flux * lapse_residual + kappa * radius**2 * field_f * (speed * wave_residual + gradient * kinematic_residual)
assert symbolic.cancel(left - right) == 0
print('off_shell_shift_propagation_identity: exact_zero')
```

The polynomial identity extends to zero v and w as well; only R,F,c are
denominators and require the positive-chart domain.

## 4. Results and immediate interpretation

The first and second implicit jets are enclosed at all 18 compatible initial
roots AND throughout all 18 existing residence tubes. The full shift residual
is now sign-certified nonzero at every initial root, not merely observed at
a floating Newton approximation. In 14 cases the entire independent root
tube excludes zero in at least one component. In all 18 cases the derivative
bound proves nonzero persistence throughout the entire corresponding short
residence interval; no shortening was necessary. This distinction matters
for the four whole-tube boxes that contain zero.

At the saved time .01, rigorous bounds on the maximum absolute shift
covector component are enclosed by these outward-coarsened summaries:

| Cells | Branch | Initial-root lower | Initial-root upper | Whole-tube upper | Whole-tube time-derivative upper |
| --- | --- | ---: | ---: | ---: | ---: |
| 16 | GR control | 7.18330e-7 | 7.18331e-7 | 8.57608e-7 | 2.09392e-4 |
| 16 | metric-Gram | 1.915995e-6 | 1.915997e-6 | 2.10397e-6 | 3.15163e-4 |
| 32 | GR control | 3.01806e-8 | 3.01809e-8 | 2.84519e-7 | 6.44357e-4 |
| 32 | metric-Gram | 6.33084e-8 | 6.33088e-8 | 4.22908e-7 | 7.97353e-4 |
| 64 | GR control | 8.8794e-10 | 8.8811e-10 | 5.00341e-8 | 2.50839e-4 |
| 64 | metric-Gram | 1.236938e-8 | 1.236944e-8 | 8.29431e-8 | 3.04636e-4 |

These are finite coefficient/covector quantities in the existing code's
normalization, not measurements in SI units. The residual is integrated
against basis functions, so its raw coefficient norm also changes with
resolution. The decrease over these meshes is not a convergence theorem or
a physical comparison score. GR is the same scalar-matter numerical control,
not a claim that exact vacuum Einstein solutions fail their field equations.

The previous free-root/residence result remains valid. What cannot be added
to it is the claim that this reduced finite evolution satisfies the entire
retained shift system. Merely tightening Newton tolerance cannot remove the
certified discrepancy at its exact free roots. A shared discretization or
reduction issue is the next investigation; its precise cause is not proved
by finding the effect in both branches.

The independently propagated whole-tube jet radii are appreciable: at the
final N64 states the largest first-jet radius is approximately .0013455 GR
and .0014865 Gram, and the second-jet radius .45841 GR and .46599 Gram.
These are enclosure overestimates, not measured instability amplitudes, and
they do not automatically fit the old independently chosen narrow jet boxes.
There is still no boundary total-variation or whole-[0,.01] trajectory claim.

The best next step is the sourced residual identity in section 3: derive its
weak-to-strong/projection, quadrature, boundary and Gram-current contributions
on these same data before trying to remove a term or alter the physics. If
the independently derived remainder admits a controlled refinement bound,
that is a route to continuum consistency; if a nonvanishing term survives,
the reduction/action has to be corrected and revalidated. Neither outcome
is assumed. This is more useful now than pretending higher jets alone can
repair an already nonzero lower-order equation.

## 5. Validation and limits

Source owners:
`scripts/annular_implicit_parent_jets_20260910.py` and
`scripts/derive_annular_implicit_parent_jets_20260910.py`.
Both import the previously sealed outward primitives and root action.
The entire source/data hash chain is retained.

Controls include the normalized Taylor second coefficient of (2+3t+5t^2)^2,
positive/negative nonzero interval classifiers, and a zero-containing
classifier that is deliberately NOT treated as a zero proof. A stationary
zero-scalar/zero-momentum/fixed-boundary control checks that the derivative
algebra encloses zero; its arbitrary frozen metric is not asserted to solve
the initial constraints and is not passed off as a certified vacuum root.

At each initial root midpoint the independent original constraint-tangent
implementation is compared with the new first jet and shift covector.
Centered differences of that independent tangent at steps 2e-5 and 1e-5
check the second derivative. They are numerical controls, not proof inputs.
Acceptance tolerances are 1e-8 for normalized tangent difference, 1e-12 for
shift-covector difference, and 1e-5 for normalized centered second-derivative
difference. Actual errors are recorded rather than replaced by tolerances.
Across the full run the maximum normalized tangent difference is 2.193e-13,
the maximum absolute shift difference 4.526e-19, and the largest centered
second-derivative control error 1.789e-8. The one-state development probe
passed 36 checks. The final 550 checks add a stationary algebraic control and
stricter independent comparison tolerances. The separate exact symbolic
identity check above is not included in that 550 count.

Initial and whole-tube interval arrays include the packed first/second jets,
force and its derivative, J, P, P_1, b, b_1, both mass mismatches, both shift
covectors and differentiated constraint residuals. Archives are read back
and every array must match exactly. Endpoint histories and constant nodal
momenta have explicit checks; all four inverse enclosures per scope require
their verified comparison inequalities. Descriptive midpoint/radius summaries
are rounded diagnostics; the saved outward endpoints own all inequalities.

Scope remains the finite canonical real-map action with rational kappa=1/10,
under the inherited correctly rounded binary64/basic-square-root and gradual
underflow assumptions. It is not a proof-kernel verification, continuum
quadrature certificate, nonlinear P(X) theorem, horizon theorem, empirical
local-GR pass or proof of a unified theory. Third jets and a same-map boundary
source/time-variation estimate are not established by this continuation.

Root-source owner:
`source-intake/navier-stokes/20260910/annular-parent-root-residence-final-integrity.json`.
Final candidate:
`source-intake/navier-stokes/20260910/annular-implicit-parent-jets-attempt01/status.json`.
Final seal:
`source-intake/navier-stokes/20260910/annular-implicit-parent-jets-final-integrity.json`.

No original state or predecessor evidence is changed. No numerical evolution,
GitHub operation, galaxy modification or frozen-workbench modification is
performed. One single-core BelowNormal Python worker runs at a time. The
workbench check is an mtime scan since 2026-09-10T13:58:30Z, not a pre-turn
full-content-hash baseline.
