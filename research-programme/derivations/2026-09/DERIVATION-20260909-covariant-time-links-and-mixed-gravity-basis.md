# Covariant time links, their action current, and the first mixed gravity basis

Private continuation, 2026-09-09. This constructs and tests a new action
completion, rather than searching again for the already derived clock current.
Previous source/output hashes, including the old failed runs, were verified.
All paths in this note are relative to post-checkpoint-work.

## 1. Outcome and scope

The earlier relative-clock germ is extended to a finite, background-dependent
time-connection transport. Its action density obeys the FULL time-coordinate
transformation with R fixed, including the -A epsilon_t term. The connection
current is obtained by varying that action, with nonzero time-boundary work.
The transformed metric is tested before resetting beta to zero.

A fixed face-mass/nodal-lapse basis and its gravitational weak covectors are
also constructed. This is not yet the complete ungauged mixed Einstein/matter
action or a propagating-constraint estimate. No R10, local-GR, horizon, first-u,
physical source calibration, causal evolution or full-spacetime gauge pass.

Important cost: finite background transport is NOT the old zero-relative-clock
germ evaluated unchanged. It substantially changes this finite-grid operator.
Its old Hessian/stability/evolution results must not be inherited. Section 6
quantifies the change instead of concealing it behind successful identities.

## 2. Exact transport, not just a spatial primitive

Keep the prior metric connection and principal time density

    A = g_tR/g_tt = sigma - 1/(EF),
    a = r^2 sqrt(-g_2)[P g^{RR} + 2P_X (grad^R chi)^2].

This exterior chart requires EF != 0; the numerical controls have F > 0.
No horizon-crossing inference is made from these expressions.

For each existing Gram factor l choose a fixed geometric anchor r_l=(S r)_l.
Transport its time s to node i by solving the scalar ODE in radial position:

    partial_R phi_l(s,R) = -A(phi_l(s,R),R),
    phi_l(s,r_l)=s,
    J_l = partial_s phi_l,
    partial_R J_l = -A_t(phi_l,R) J_l,   J_l(s,r_l)=1.

Thus J_l=exp(-integral A_t dR)>0 wherever the smooth transport exists.
It is the required time-density Jacobian, not an adjustable coefficient.
Pull back BOTH the scalar and the density to the factor anchor:

    x_li = chi(phi_li,r_i),       b_li = J_li a(phi_li,r_i),
    z_l = sum_i T_li x_li,        B_l = sum_i S_li b_li,
    V_l = B_l z_l^2/(2h),        S_correction = -integral ds sum_l V_l.

T and S are the already fixed positive Gram factors. No flux or fitted damping
is appended. Since B_l>0, V_l>=0 on this branch. Positivity of this action
potential is NOT positivity of the constrained Hamiltonian of a delayed system.
Time links only use the finite radial support of their factor.

### Finite coordinate transformation

For an orientation-preserving map H(t,R), active pullback gives

    chi'(t,R)=chi(H(t,R),R),
    a'(t,R)=H_t a(H(t,R),R),
    A'(t,R)=[A(H(t,R),R)+H_R]/H_t.

The first-order law is exactly

    delta A=epsilon A_t+epsilon_R-A epsilon_t.

The link ODE implies the conjugacy

    H(phi'_li(s),r_i)=phi_li(H(s,r_l)),
    H_t(phi'_li,r_i) J'_li=J_li(H(s,r_l)) H_t(s,r_l).

Consequently V'_l(s)=H_t(s,r_l) V_l(H(s,r_l)). Its time integral transforms
only through its endpoints. At first order delta V_l=partial_s(epsilon_l V_l).
This proves the specified continuum-time, fixed-R symmetry of this correction.
It does not prove invariance of an entire fixed spatial finite-element ansatz
under arbitrary spacetime coordinate changes.

Changing the geometric anchor composes these same links and multiplies V_l
by the anchor-to-anchor Jacobian. The integrated action is unchanged when the
same physical endpoint events are used. Holding different endpoint times fixed
while moving the anchor is not the same variational problem.

### Independent finite metric test

The validator constructs g'=H^*g directly, then recovers E', F', mu' and beta'
in the original (v,r) parameterization. It substitutes q'=H_t q,
w'=w+H_R q and the nonzero beta' into the FULL nonlinear principal coefficient.
This agrees with a'=H_t a(H), rather than assuming that density law in every
test. Artificially setting beta'=0 fails the negative control in both signs
of the finite transformation and both parent fixtures.

## 3. Deriving the connection current and the boundary term

Let y_li=delta phi_li for a connection variation delta A with fixed anchor time.

    partial_R y = -A_t y-delta A(phi,R),
    y_li = -J_li I_li,
    I_li = integral_{r_l}^{r_i} delta A(phi_l(s,R),R)/J_l(s,R) dR.

For each factor define its ordinary action covectors

    c_li=partial V_l/partial x_li = B_l z_l T_li/h,
    e_li=partial V_l/partial b_li = S_li z_l^2/(2h).

Because delta b_li=partial_s[a(phi_li,r_i)y_li], integration by parts gives

    delta integral V_l ds
      = integral sum_i g_li I_li ds + [sum_i e_li a(phi_li,r_i)y_li]_{s0}^{s1},
    g_li=b_li partial_s e_li-(partial_s x_li)c_li,
    sum_i g_li=0.

This is the full connection-only variational block; direct changes of the
matter fields and coefficient a add their own covectors. They are not discarded.
The ODE for y and its time derivative supplies a concrete implementation.

At zero background connection, J=1 and phi=s. Summing factor contributions
gives EXACTLY the earlier nodal clock covector

    sum_l g_li = -q_i(R_a chi)_i+a_i rho_t,i = -div J_graph,i.

The full transported instantaneous density and the earlier energy-weighted
clock germ differ at first order by an explicit total time derivative. The
18 original snapshots verify this identity including a_t, not just frozen a.
Equality modulo that boundary at first order does NOT establish equality of
their complete Hessians at nonzero background connection.

The integrated-action control varies A directly, integrates the actual changed
action, and compares centered finite differences to the derived bulk PLUS
endpoint term. Both time quadratures (16 and 24 points) and both variation
steps (.001 and .0005) are retained.

| Actual reference | Bulk derivative | Time-boundary term | Complete derivative |
|---|---:|---:|---:|
| canonical | 3.54703194664e-8 | 7.84245955739e-11 | 3.55487440620e-8 |
| nonlinear P(X) | 3.63177137061e-8 | 9.73612971497e-11 | 3.64150750033e-8 |

Maximum observed finite-difference discrepancy is 1.63e-17. Dropping the
time-boundary term is detectably wrong. These values use normalized fixtures;
they are neither SI predictions nor interval-certified error bounds.

## 4. Constructed mixed face/nodal gravity basis

Let H_i be the existing positive SBP quadrature weights. Face coordinates are
f_0=r_min, f_{i+1}=f_i+H_i. Let P interpolate face mass to nodes using the fixed
piecewise-linear face basis, Q interpolate nodal values to faces, and B be the
cell incidence matrix with entries (-1,+1). Both bases preserve constants and
affine functions and have nonnegative weights. Their variational adjoints are
their transposes under the explicitly included quadrature, not fitted averages.

The beta=0 gravitational action block is

    L_g0 = E^T [B mu - sigma H P mu_t]/kappa,    E_i=exp(delta_i).

Its derived covectors, with convention L_mu-partial_t Pi_mu, are

    L_delta = E * [B mu-sigma H P mu_t]/kappa,
    Pi_mu = -sigma P^T(H E)/kappa,
    Euler_mu = [B^T E+sigma P^T(H E delta_t)]/kappa.

For constant E and delta_t=0, the mass covector is still nonzero at the two
physical endpoints: (-E_left,+E_right)/kappa. Those are real boundary terms,
not rows to silently delete. A closed variational problem must supply physical
endpoint conditions or the appropriate boundary action. Six background/grid
controls verify these derivatives, momentum, adjoints and endpoint terms.

The beta variation is NOT supplied by this beta=0 block. The previously derived
off-gauge Einstein germ must be incorporated before claiming a mass-time law or
constraint closure. Shared matter coefficient variation and the actual A(mu,
delta) connection variation must also come from this same assembled action.

## 5. Finite-basis covariance: a bounded defect, not a new impossible demand

Ordinary linear interpolation is not closed under products. On one element,

    I(fg)-(If)(Ig)=theta(1-theta)(f_R-f_L)(g_R-g_L),
    abs(defect)<=element_length^2 Lip(f) Lip(g)/4.

This is an exact formula and bound, not a statement that interpolation vaguely
"might break covariance." The sin(r), cos(1.2r) control on N32/64/128 has maxima
0.00456383, 0.00114788, 0.000287054; reduction factors 3.97589 and 3.99881.

We should NOT demand exact lattice diffeomorphism symmetry as a prerequisite
for GR or MTS continuum viability. A consistent, stable discretization may
have truncation-level symmetry defects. What remains necessary here is a
controlled coupled constraint estimate, boundary/source compatibility, and
matched GR/MTS refinement tests. This product bound alone does not supply
that coupled estimate. Nor may it be called a failure of the continuum theory.

## 6. The changed operator is quantitatively important

At t=.18, N128 the old equal-coordinate-time Gram densities are about 5e-14;
the fully transported densities are 4.84315e-5 and 5.56835e-5. Ratios are
9.50e8 and 1.15e9. These are NOT interchangeable discretizations at this mesh.

The large ratio has an identifiable geometric cause. For the leading scalar
phase cos(v/epsilon), fixed-t radial differentiation sees v_R=sigma=.05;
horizontal differentiation D_R=partial_R-A partial_t sees

    D_R v=sigma-A=1/(EF).

Third differences, followed by squaring, strongly magnify that difference in
resolved wave direction. This is not evidence of a new physical interaction.

To put its size in context, a bounded profile-only N128/256/512 calculation
compares it with the leading horizontal principal quadratic form

    Q_horizontal = sum_i H_i a_i[(partial_R-A partial_t)chi_i]^2/2.

This is NOT the full nonlinear/constrained Hamiltonian. No evolution is run.

| Fixture | N128 correction / Q_horizontal | N256 | N512 |
|---|---:|---:|---:|
| canonical | 0.445804% | 0.0287402% | 0.00180847% |
| nonlinear | 0.478157% | 0.0309082% | 0.00194628% |

The correction decreases by factors 15.47-15.89 per halving h, observed orders
3.951-3.990. This agrees with the CONDITIONAL O(h^4) action estimate: each T
factor is a third difference along a smooth horizontal curve, hence O(h^3);
bounded coefficients, the 1/h prefactor and O(1/h) factors give O(h^4).
Uniform bounds on those horizontal third derivatives are still hypotheses for
an evolved solution, and need not be uniform in a separate high-frequency limit.

This check explains why the billion-fold old/new ratio is not by itself a
physical blow-up. It also prevents treating covariance as a free improvement:
new coupling Hessians, causality and constraints have to be tested afresh.

## 7. Evidence and reproducibility

All four owners are terminal, with no new failure suppressed:

- source-intake/navier-stokes/20260909/annular-covariant-transport-and-mixed-basis-derived/status.json: 110/110.
- source-intake/navier-stokes/20260909/annular-transport-anchor-and-resolution-controls/status.json: 13/13.
- source-intake/navier-stokes/20260909/annular-covariant-transport-scale-control/status.json: 11/11.
- source-intake/navier-stokes/20260909/annular-finite-metric-pullback-control/status.json: 14/14.

Finite-coordinate action covariance errors are 2.50e-14 and 1.67e-14 relative
maximum norm across all 253 factors on the actual N128 backgrounds. Reanchoring
errors are 2.86e-14 and 6.88e-14. Transported evaluations stay within owned
advanced-time domains: canonical [.01913,.49044], nonlinear [.01745,.49347].
No out-of-domain parent extrapolation or fabricated source data is used.

Implementation:

- scripts/annular_covariant_time_transport_20260909.py
- scripts/annular_mixed_grid_basis_20260909.py
- scripts/derive_annular_covariant_transport_and_mixed_basis_20260909.py
- scripts/derive_annular_transport_anchor_and_resolution_controls_20260909.py
- scripts/derive_annular_covariant_transport_scale_20260909.py
- scripts/verify_annular_finite_metric_pullback_20260909.py

Parent context: DERIVATION-20260909-clock-coframe-current-and-linearized-coupling.md
and DERIVATION-20260909-joint-Gram-action-and-conservative-mass-transport.md.
Final evidence: source-intake/navier-stokes/20260909/annular-covariant-time-links-final-integrity.json.

## 8. Actual next calculation

Derive the OFF-GAUGE mixed gravitational/matter quadratic action around these
same backgrounds, using the constructed face/nodal basis and the actual finite
time-link current. Include beta before restriction, all coefficient work,
metric connection second derivatives and physical endpoint covectors. Then
test whether the resulting constrained time operator has a causal, controllable
initial-boundary formulation and a convergent constraint residual.

Transport can sample both earlier and later coordinate times along a spacelike
horizontal path. The finite-history action is therefore not automatically a
standard explicit initial-value solver in the old tilted time coordinate.
Use a derived coframe-adapted slicing or a controlled local quadratic reduction;
do not silently run the full history functional as a causal field equation.

There is no reason to repeat the old current hunt or rerun the failed mass-only
repair. No reason to erase it either: FAILED157/164 remains the diagnostic that
motivated this action-based route. No public/GitHub update, subagent, shared
process shutdown or frozen-workbench edit is part of this continuation.
