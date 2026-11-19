# Shared neutrino moments through the background and scalar carrier

## What is inherited

The retained action, G, scalar masses, heavy matching density and initial
slow-field data are unchanged. This is a separate numerical reference
for the late interval z=10, Delta ln a=.001, not a new cosmological fit.
The heavy component still uses the retained late dust background in this
interval; its finite-frequency carrier is a retained W2 approximation,
not a newly exact heavy-background solution.

Upstream files are relative to post-checkpoint-work:

- condensate-origin-20261003/radiation-and-slow-field-transfer-20261007/radiation_common.py
  supplies the retained standard-species parameter factory.
- condensate-origin-20261003/native-heavy-matching-20261007/native/camb/model.py
  maps nominal mnu to omnuh2.
- The same native/fortran/results.f90 sets grhormass and inverts the density
  using native/fortran/massive_neutrinos.f90.
- mts-background-derivatives-20261110 supplies saved cold/heavy backgrounds.
- mts-metric-reduced-action-20261110/action_model.py and series.py supply the
  retained scalar carrier and Taylor-series conventions.

Exact paths/hashes are recorded in the local provenance and closeout.

## Mass is not independently reselected

The original input is nominal mnu=0.06 eV. The Python factory first
converts it to omnuh2=0.000644866570625114 with the native temperature/
effective-species convention. Fortran then obtains its actual dimensionless
mass from the target density. Both cold and heavy give

    m_nu/T_nu0 = 356.5935334924326,
    A = grhormass = 1.902191136579917e-12 Mpc^-2,
    massive degeneracy = 1.0146666666666666.

The nominal input and actual inferred ratio are different kinds of input,
not interchangeable exact numbers. A is grhor times the degeneracy and
is not a free galaxy coupling. Captured five-node source coefficients
recover A to relative error <=6.67e-16. Standard matter/radiation amplitudes
match the saved background at floating-point precision.

This reference holds the actual inferred mass and A fixed. It does NOT
rerun the mass inversion using the new moment formula to restore an exactly
fixed target density. Its present dimensionless density differs from the
target by -2.75278e-10, versus native -2.75956e-10. That small difference
is recorded, not removed by adjusting mass, abundance or H0.

The first normalization check used an incorrect midpoint coordinate.
Captured fractions are linear in conformal time, not in ln a. The saved
clock places their midpoint at Delta ln a=0.00050006229126. Correcting
only this reader resolves the mismatch at the unchanged gate; see
CLOCK-COORDINATE-REPAIR.md and normalization-clock-result.json.

## Derivatives from the same distribution

Write N=ln a, mu=a m_nu/T_nu0. The preceding positive-shell construction
gives dimensionless R_h(mu), P_h(mu) and

    S_h = (4/3)sum B_i sqrt(q_i^2+mu^2)/q_i.

Scaled stresses are R_nu=A R_h/a^2, P_nu=A P_h/a^2 and S_nu=R_nu+P_nu.
Consequently

    dR_nu/dN = 2R_nu-3S_nu = -R_nu-3P_nu.

This is an integral identity from the distribution, not an imposed new
closure. Compute the Taylor series of S_nu directly from the fixed positive
nodes and weights. If R_j,S_j are coefficients about a chosen N, then

    (j+1)R_(j+1) = 2R_j-3S_j,    P_j=S_j-R_j.

R_0 is always the evaluated shell integral at that N, not a freely chosen
integration constant. This recursion obtains higher derivatives without
introducing a second spline or numerically differencing noisy pressure.
Independent 60-decimal differentiation of the closed radial integrals
checks density and pressure through fourth N derivative.

## Paired background initial-value problem

Let u=phi_s' be the slow field's conformal velocity, mu_s=a m_s and H
the conformal expansion rate. Use scaled densities

    R = D/a + Rrad0/a^2 + R_nu + (u^2+mu_s^2 phi_s^2)/2,
    P = Rrad0/(3a^2) + P_nu + (u^2-mu_s^2 phi_s^2)/2.

D includes exactly the saved standard matter and, in heavy, the retained
late heavy matching density. The same field equations give

    dphi_s/dN = u/H,
    du/dN = -2u-mu_s^2 phi_s/H,
    dH/dN = -(R+3P)/(6H),
    dtau/dN = 1/H.

Initial phi_s,u are the saved values. Initial H is sqrt(R/3) with the NEW
reference density, not the old H silently reused with new sources.
This enforces the initial Friedmann constraint, not a fit to observations.
Each constituent obeys R_N=-R-3P, including the slow scalar on its equation,
so d(3H^2-R)/dN=0. The independently propagated constraint is checked.

The input H0=70 sets inherited units/amplitudes; this short local reference
does not claim a freshly calibrated present-day expansion history.
Cold and heavy are distinct matter partitions but their retained late
backgrounds nearly coincide; passing both is not two independent data tests.

## Carrier uses that propagated pressure and clock

Convert N jets with d/dtau=H d/dN. The same background supplies

    H'=-(R+3P)/6,    P=-2H'-H^2

on the Friedmann constraint. The latter is independently checked through
three N derivatives; it is not used as an unrelated pressure fit.

For the retained heavy mass mu_h=a m_h and k=5 Mpc^-1, the imported W2
carrier convention is

    W0=mu_h+3P/(8mu_h),
    r=sqrt(1+k^2/mu_h^2),
    DeltaW=k^2/[mu_h(r+1)] *
       [1-P/mu_h^2*(3r^2+r+1)/(8r^3)
          -H^2/mu_h^2*(r+1)(2r^2+5)/(8r^5)],
    Wk=W0+DeltaW, slopes=-W'/2W.

Evaluate the small beat and pressure piece separately rather than subtracting
large frequencies. The new contribution is their consistent background
input/derivatives, not a new derivation of the W2 approximation itself.
Independent 60-decimal algebra checks those six coefficients and slopes
at the saved initial/mid/final N positions.

## Scope of the result

The background bridge now evolves the slow field and clock using the same
conservative neutrino distribution and supplies coherent carrier jets.
The saved production perturbations have NOT been advanced with new
64-node initial data. That requires an explicit native/reference interface
and appropriately prepared state, not interpolation of five values passed
off as a uniquely derived distribution. The next bounded control is stated
in NEXT.md; this is not an excuse to keep polishing this background.
