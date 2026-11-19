# Source-complete leading RSA, with stress and metric feedback

Keep the previous native approximation's domain; do not assert an exact
radiation solution. Its missing synchronous scalar stress is (DS,PS),
including both retained slow scalar and heavy scalar. The trace equation
and constraint give the already-derived increments

    delta_qg=delta_qr=-2 DS/(3kH),
    delta_delta_r=(4DS+6PS)/k^2,
    delta_delta_g=delta_delta_r-2 opacity DS/(k^2 H).

Use the same increments for the native gravitational sources and species
RHS. Their additional baryon force is (Rgamma/Rb)opacity delta_qg.
No extra source parameter or fit to the measured residual enters.

## Correct pressure gauge transformation

The retained convention is D_N=D_sync+rho_physical' (8piG a^2)alpha,
or D_sync=D_N+3HS alpha. Pressure transforms with the SAME sign:

    P_sync=P_N-beta alpha,
    beta=Pbar'-2H Pbar,  alpha=(eta-Phi)/H.

Thus for the canonical heavy carrier

    D_h,sync=Rh dstar+3Sh eta,
    P_h,sync=Rh pstar-(beta/H)eta+(3Sh+beta/H)Phi.

The plus sign in (3Sh+beta/H) follows from this convention; substituting
the density transformation into a generic pressure formula with the
opposite clock sign would be wrong. For the slow field the synchronous
action already supplies DS=v delta_v+mu_s^2 phi delta_phi and
PS=v delta_v-mu_s^2 phi delta_phi. The native averaged-heavy comparison
uses its retained pressure, not a newly imposed zero pressure.

Compute beta from the carried W2 ensemble, with pressure evaluated stably:

    Pbar=J[(L0-H)^2+(W0-mu)(W0+mu)]/(a^2 W0),
    J=Rh_initial/initial_weight, W0-mu=3P_total/(8mu).

Differentiate this expression using the retained homogeneous Taylor jets.
Do not form W0^2-mu^2 by subtracting large rounded squares or declare
Pbar zero because the native background is nearly dust.

## Solve the scalar/pressure feedback instead of freezing it

Write DS=dY, PS=pY+t Phi, Rrad=Rgamma+Rmassless, and

    Ad=4Rrad/k^2-2Rgamma opacity/(k^2H),
    Ap=6Rrad/k^2, Aq=-2Rrad/(3kH).

Then added synchronous radiation sources are

    Delta D=Ad DS+Ap(pY+t Phi), Delta Q=Aq DS.

For the canonical heavy state, let B=2k^2+3Sh and let the old potential
be -N/B in the preceding mixed-gauge notation. The corrected potential is

    Phi_new=-[N+Ad DS+Ap pY+3H Aq DS/k]/[B+Ap t].

Here t=3Sh+beta/H; slow scalar stress has no explicit Phi in its native
synchronous coordinates. New alpha fixes the native heavy-current image
Q_h,sync=Rh qN-Sh k alpha. For native heavy/cold controls all their scalar
coordinates remain synchronous, so B=2k^2 and t=0. No screening mass or
new gravitational coupling has been introduced.

## An isolated native source port

The copied native library accepts four radiation increments immediately
before its radiation density/current addition. Consequently the native
z, sigma, eta', cold/baryonic evolution, massive-neutrino hierarchy and
baryon Thomson drag all respond consistently. Unit probes determine its
linear RHS/readout columns, checked against the explicit gravity/drag
formulae. A zero increment/disabled port retains the original capture.

The canonical heavy-current image and scalar metric forcing use Phi_new;
the native heavy derivatives are still discarded in favor of the actual
four-coordinate scalar. This is not an observer-only correction. Native
Weyl_prime remains a momentum-law expression, not an independent metric
conservation test; differentiate the actual corrected source row instead.

Radiation feedback and higher time/opacity orders omitted by leading RSA
remain approximation errors. The cold comparison and independent defect
test determine whether the leading correction suffices in this window.
