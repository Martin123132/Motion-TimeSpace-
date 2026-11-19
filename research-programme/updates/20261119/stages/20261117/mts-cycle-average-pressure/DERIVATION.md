# Exact finite-window wave-pressure coefficient and its remainder

Use the retained scalar definitions mu2=a^2 m^2>0, D=Vg+mu2 Phi f,
P=Vg-mu2 Phi f, C=Phi f, J=Vf+Phi g. The already checked field identity is

2P=J'+2HJ+k^2 C+k Phi V z-Gf-Fg.

Since D-P=2mu2 C, define
u=k^2/(4mu2), c_v=u/(1+u)=k^2/(4mu2+k^2), s=1/(1+u).
Then EXACTLY, without a dust or averaging assumption,

P=c_v D+(s/2)[J'+2HJ+k Phi V z-Gf-Fg].

This coefficient is fixed by the existing mass and gradient operator. It is
not an independently fitted force or equation of state. The remainder must
be controlled before P≈c_v D can be used as an effective closure.

With beta=a/rho0, r=a'/a, mu2'=2r mu2 and fixed comoving k,
s'=2r s c_v. Integrating with the same density-exchange weight H beta gives

integral H beta P dt
 = integral H beta c_v D dt + [H beta s J]/2
 + (1/2) integral beta {
      [s(2H^2-H'-Hr)-H s']J
      +H s[k Phi V z-Gf-Fg]} dt.

The coherent branch has r=H,F=G=0, but neither s' nor the endpoint term
vanishes in general. Completing background cycles does not ensure the
perturbation phase and amplitudes return. All these terms are tested, rather
than discarded to force a pressureless result.

## Independent unforced constant-coefficient analytic control

For H=0,z=0,F=G=0 and constant mu>0, let
Phi=A cos(alpha), f=B cos(beta_phase), alpha'=mu,
beta_phase'=omega=sqrt(mu^2+k^2). Direct products yield

D=(AB mu/2)[(omega+mu)cos(beta_phase-alpha)
                         +(mu-omega)cos(beta_phase+alpha)],
P=(AB mu/2)[(omega-mu)cos(beta_phase-alpha)
                         -(omega+mu)cos(beta_phase+alpha)].

A carrier-phase projection removing only the sum-frequency term therefore gives
c_free=(omega-mu)/(omega+mu)=k^2/(omega+mu)^2.
The exact remaining fast term is
P-c_free D=-2AB mu^2 omega/(omega+mu) cos(beta_phase+alpha).

For a finite time average of length T, its magnitude is bounded by
4|AB| mu^2 omega/[(omega+mu)^2 T].
This is a control under the stated unforced, constant-coefficient assumptions,
not a theorem about the actual expanding, metric-forced history.

Writing u=k^2/(4mu^2), the small-gradient series are
c_v=u-u^2+O(u^3), c_free=u-2u^2+O(u^3).
Both have the leading wave-gradient coefficient u. Their higher-order
difference is precisely why the finite-boundary/remainder calculation matters.

The actual mean-pressure test must retain expansion, phase drift, metric
forcing and representation contacts. A finite-window perturbative P/D ratio
is not automatically a gauge-independent fluid sound speed or background w.
