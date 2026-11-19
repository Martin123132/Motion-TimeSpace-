# Exact scalar pressure identity for the retained coupled equations

This is a consequence of the retained field/metric equations, not an added
dust law or fitted equation of state. Numerical evaluation is a subsequent
test; a symbolic identity alone does not show that its boundary terms are small.

All derivatives below are conformal-time derivatives. For either retained
canonical quadratic scalar, write its homogeneous field and velocity as Phi,V,
and its perturbation and velocity as f,g. Define mu2=a^2 m^2 and

Phi' = V+F,  V' = -2 H V-mu2 Phi+G,
f' = g,     g' = -2 H g-(k^2+mu2)f-k V z.

F and G are explicit representation defects. They vanish on the exactly
coherent background equations; they must be retained for the original
interpolated background. H is the Friedmann expansion rate used by the
equations. Let r=a'/a for the represented scale factor; do not assume r=H
on the original interpolated branch.

The native a^2-weighted density, current and pressure perturbations are

D=Vg+mu2 Phi f,  Q=k V f,  P=Vg-mu2 Phi f.

With C=Phi f and J=Vf+Phi g, direct differentiation gives

C'=J+Ff,
J'=-2 H J+2 P-k^2 C-k Phi V z+Gf+Fg.

Therefore the pressure is exactly

2P=J'+2HJ+k^2 C+k Phi V z-Gf-Fg.

This separates pressure into a derivative/boundary contribution, expansion,
spatial-gradient response, metric forcing, and the original representation
contacts. It makes clear why averaging oscillations does not by itself justify
putting pressure to zero.

## Direct connection to the already integrated density-exchange work

Use the same frozen normalization beta=a/rho0 as the saved scalar source,
so S_P=beta P and beta'=r beta. On an interval [t0,t1],

integral H S_P dt
 = [H beta J]/2
 + (1/2) integral beta [
       (2H^2-H'-Hr)J
       +H k^2 C
       +H k Phi V z
       -H(Gf+Fg)] dt.

Square brackets here mean terminal minus initial value. The left side is
already available for the owned heavy scalar as minus one third of the
saved integrated pressure-work increment. This connects a field-level
derivation to the existing exchange accounting without fitting a fluid closure.

On the coherent background, F=G=0 and r=H, leaving the coefficient
(H^2-H')J and the same gradient, metric and boundary terms. H' must come
from the retained equations or checked metric packet, not a fitted slope.

The next empirical calculation inside the model is to evaluate these pieces
over the saved multi-cycle interval, with the existing32/64 controls. A
small total pressure could reflect cancellation, not small individual terms.
An effective dust/GR matter limit would require a quantitative bound on the
retained non-dust terms; it is not supplied merely by this identity.

The cold owned-fluid baseline has identically zero pressure; label that a
structural control. Where the saved packets support it, the same scalar
identity can also be checked for the slow field in both cosmological cases.
No galactic population or boundary condition is inferred from this result.
