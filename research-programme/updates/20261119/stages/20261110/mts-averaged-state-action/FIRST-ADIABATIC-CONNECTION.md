# First adiabatic connection from the real-field sideband

This supplements DERIVATION.md section4 rather than changing its frozen results.
It derives the missing unforced FLRW contribution at first order in H/mu.
Metric-perturbation forcing and a complete higher-order/negative-frequency
reduction remain separate. No retained native history is overwritten.

## 1. Start from the actual oscillator, not the required trace

On homogeneous FLRW the real scalar's conformal canonical variable q=a phi obeys

    q_k'' + [k^2+mu^2-a''/a] q_k=0,  mu=am.

To first adiabatic order let omega=sqrt(k^2+mu^2), w=omega/mu, and use
q0~mu^(-1/2) cos integral(mu d tau), qk~omega^(-1/2) times its carrier.
Dropping a''/a and WKB frequency-curvature errors here is an O(H^2,H')
approximation, explicitly quantified below, not an exact FLRW assertion.

Relative to the real homogeneous carrier write

    delta phi=F[R cos theta+I sin theta], theta'=mu,
    F'/F=L0=-3H/2,
    R'=gamma R+(omega-mu) I,
    I'=gamma I-(omega-mu) R,
    gamma=H(1-1/w^2)/2,
    L=L0+gamma=-H-H/(2w^2).

Then the physical derivative is

    delta phi'=F[(L R+omega I)cos theta+(L I-omega R)sin theta].

Carrier projection of the actual field stress gives, to first order in H/mu,

    delta=(w+1)R+B I,
    Pi=(w-1)R+B I,
    S=I-L0 R/mu,
    B=(L0 omega-mu L)/mu^2
     =(H/mu)(-3w/2+1+1/(2w^2)).

The exact projected background denominator also has L0^2; omitting it at this
step is explicitly second adiabatic order. There is no assumed thermal state,
free damping parameter or empirical pressure coefficient.

## 2. Eliminate the carrier amplitudes

To this order, solving the source/current map gives

    Pi = r delta - (3H r+g) S/mu + O(adiabatic order2),
    r=(w-1)/(w+1),
    g=H(w-1)/w^2.

The additional -g S/mu follows from the field-derivative and current terms.
It was not chosen from the trace condition. Independently,

    g = -W'/W,   W=2w/(w+1)=1+r.

The same term required by the parent's symplectic normalization is therefore
supplied by the first adiabatic real-field projection. This answers the
specific mismatch found in the previous section, within its stated order.

Expanding the derivative of delta and S directly from R,I gives

    delta'=k^2 S/mu-3H Pi,
    S'=-mu Pi

through first adiabatic order. The continuity equation is an independent
check of the pressure and current map, not an extra postulate.

## 3. A specified completion, and what its exact checks mean

If this first-order pressure is retained inside the exact averaged conservation
equations, it defines a useful minimal completion:

    delta'= -3H r delta + [k^2+9H^2 r+3H g] S/mu,
    S'= -mu r delta + (3H r+g)S.

It includes particular O(H^2) products, but does not derive every term of that
order. Its action is

    I_ad = integral W [ S delta' - K_ad ] d tau,
    K_ad = mu*r/2*(delta-3H S/mu)^2
           + k^2*S^2/(2mu) + 3H*g*S^2/(2mu).

Varying the time-dependent W supplies +gS in the second equation.
The extra quadratic term supplies +3H g S/mu in the first. The canonical
momentum is P=W S. In the canonical pair (delta,P), the flow has unit
symplectic determinant; in (delta,S), det transport=W_initial/W_final.
This is a number/energy coordinate connection, not evidence for particle
creation or a new force coupling.

This exact action identity belongs to the stated minimal completion.
The source derivation establishes its first adiabatic terms; do not relabel
its second-order products as a full parent action.

## 4. Independent higher-order consistency probe

Instead of testing only that completion, retain the full projected WKB-template
stress denominator at fixed H:

    D0=2mu^2+L0^2,
    delta=2[(L0 L+mu omega+mu^2)R+(L0 omega-mu L)I]/D0,
    Pi=2[(L0 L+mu omega-mu^2)R+(L0 omega-mu L)I]/D0,
    S=2mu*(mu I-L0 R)/D0.

Propagate R,I with their separately derived WKB equations. Compare the physical
delta,S against the minimal first-order completion, using the same initial
physical variables and a=.01 to a=.01 exp(.001). The metric perturbations are
set to zero for this test-field probe; it is not an observed-galaxy calculation
or the original metric-forced probe.

This full template is not exact KG either. For constant conformal H its
equation residual is explicitly

    residual_k/ q_k = H^2[5/(4w^4)-1/w^2-1],
    residual_0/q0 = -3H^2/4.

Divide by omega^2 or mu^2 to report a dimensionless residual, not a theorem
bounding accumulated solution error. For variable H an additional term
-H'(1+1/(2w^2)) enters the sideband residual; a general error bound must
include it and control the integration interval.

Both the original retained and derived-completion evolutions remain saved.
Cold remains the identical r=g=0 comparison. No pressure, phase or source
normalization is tuned to improve a rotation curve.
