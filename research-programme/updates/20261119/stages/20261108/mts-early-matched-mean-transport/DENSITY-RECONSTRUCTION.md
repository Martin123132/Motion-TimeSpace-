# Derived next correction: reconstruct density before reconstructing observables

The frozen short-interval test is unchanged. Its baseline succeeds while the heavy-field approximation needs a physical correction. This note derives a candidate from the ALREADY RETAINED background invariant, rather than changing an amplitude or fitting a phase. Numerical transport with this reconstruction remains the next experiment.

## Existing invariant
Write u=H/omega_h, f=rho_h/(3H²), eta0=(rho_external,N+U_s²-2V_s²-rho_h)/(6H²). The saved phase construction defines

    g1 = (3/2)u sin(2theta),
    A = (3/2)(1-eta0), B = (9/8)(2-f),
    g2 = -(A/2)u² cos(2theta) -(B/4)u² cos(4theta),
    I = ln[a*rho_h/(a0*rho_h0)] - g1 - g2.

The saved mean density is rho_bar=rho_h0 exp[-(N-N0)+I0]. Therefore the physical density obeys

    x = ln(rho_bar) + g1(exp(x),theta) + g2(exp(x),theta) + Delta_I,
    x=ln(rho_h), Delta_I=I-I0.

Setting Delta_I=0 defines a candidate reconstruction, NOT an exact conservation axiom. Keep the previously derived bound on Delta_I as a separate remainder. This distinction is essential.

## Exact logarithmic sensitivity
Hold the slow scalar coordinates, N, external sources and theta fixed. Then

    partial_x u = f*u/2,
    partial_x f = f*(1-f),
    partial_x eta0 = -f*(1/2+eta0).

The eta0 derivatives cancel within the second corrector, giving the particularly simple exact identity

    partial_x(g1+g2)
      = (3/4) f*u sin(2theta)
        -(9/8) f*u² cos(2theta)
        -(9/32) f*u² cos(4theta).

Consequently

    |partial_x g| <= f[(3/4)u+(45/32)u²].

This is a derived inversion condition, not a phenomenological coupling.

## Existence on a conservative box
For positive retained thermal/scalar components, -2<=eta0<=1 and 0<=f<=1. Thus

    |g| <= (3/2)u+(45/16)u².

The retained mean equations have u_bar,N=(eta0-1)u_bar, so u_bar is nonincreasing. Its original value is below0.001. Consider the mathematical inversion box |x-ln(rho_bar)|<=0.02; this is NOT a fitted prior or a widened physics tolerance. Positivity of the remaining density gives u<=0.001*exp(0.01) on this box.

The bounds above are then strictly below0.02 for |g| and below1 for |partial_x g|. The map preserves the box and is a contraction at every phase. It has one positive reconstructed density on this box. Actual sharper error radii should still use the inherited background tube, not the deliberately broad existence box.

If an invariant offset obeys |Delta_I|<=d, the same box admits it when sup|g|+d<=0.02. For two such fixed points at the same slow coordinates and phase,

    |Delta ln(rho)| <= |Delta_I|/(1-q),

where q bounds |partial_x g| on the common box. Slow-state and external-source differences require their own terms; this theorem does not discard them.

## The phase equation need not acquire an enormous growth bound
Partial_theta g at fixed rho is

    3u cos(2theta) + A u² sin(2theta) + B u² sin(4theta).

Hence |x_theta|<=(3u+6.75u²)/(1-q). For the reconstructed physical phase law F(theta)=omega_h/H(rho_rec(theta))-1.5sin(2theta),

    |F_theta| <= 3 + [1.5+3.375u]/(1-q).

The rapid frequency cancels against u in this Lipschitz bound. It is near4.5 per e-fold on the conservative box, not of order mu. A bounded invariant error adds phase forcing <=mu*f*d/[2(1-q)], plus separately retained slow-state errors. This offers a controlled route to the phase history rather than borrowing the reference phase.

## Constructive continuation
Use the implicit positive density and its own phase equation with the original initial data. Recalculate the initial and final physical maps consistently. For the source mean, freeze the slow invariant rather than instantaneous rho: evaluate A at rho_rec(theta) with its matching clock weights. That retains the density/phase correlation omitted by the first frozen-rho mean.

First repeat the SAME saved short-interval test without fitting. Keep the original failed approximation and baseline results. The construction above gives existence, sensitivities and a remainder condition; it does not by itself establish that the reconstructed transport meets the2e-5 observable gate.

