# Quantitative constraint control, not an exact-carrier assumption

Use the real canonical variables and total-stress conventions in DERIVATION.
Define defects from the actual equations being evolved:

    e0=v'+2Hv+mu^2 phi,
    eu=u'-p-C v,
    ep=p'+2Hp+(k^2+mu^2)u-mu^2 Dm phi.

Differentiating the action-derived sources, without setting these defects
to zero, gives the exact residuals

    ED_h=D_h'+H(D_h+3P_h)+k Q_h-3S_h Phi'
        =e0(p+6v Phi)+mu^2 phi eu+v ep,
    EQ_h=Q_h'+2H Q_h-k(P_h+S_h Psi)
        =k(e0 u+v eu).

For a linear ensemble average, average these products with the SAME carried
normalization used in the stress. For the W2 carrier e0=R0 B0/a. Dropping
the fast component or restricting to a non-invariant response plane can
also produce eu,ep; do not assign their measured or bounded values zero.

Include the other species' residuals to form ED_total, EQ_total and let

    EH=H'-(H^2-S_total/2),
    Jerr=ED_total+3H EQ_total/k+3 EH Q_total/k.

Provided the metric momentum equation and anisotropic-slip relation are
enforced, the actual constraint obeys

    E_constraint'+H E_constraint=Jerr,
    E_constraint(t)=a(t_i)/a(t) E_constraint(t_i)
                      +1/a(t) integral[t_i,t] a(s) Jerr(s) ds.

Thus a bound on the retained equations gives a bound on gravitational
constraint violation. For a>0, replace the integrand by
|ED_total|+3|H EQ_total|/k+3|EH Q_total|/k for an absolute enclosure.
This is an exact error identity; a numerical uniform bound still requires
actual trajectory enclosures, not just a maximum over saved sample points.

It also identifies the cold comparison fairly: dust has no carrier defect,
but errors in its continuity/Euler equations, the other species, the
background or the integrator still enter the same total-stress budget.

## Controlled Newtonian comparison

For k>0 and S_total>=0, compare the exact compensated constraint with
Phi_N=-Dstar_total/(2k^2). The exact difference is

    Phi-Phi_N = 3S_total Dstar_total/[2k^2(2k^2+3S_total)]
                 -3H Q_total/[k(2k^2+3S_total)].

Its absolute value is bounded by the sum of the absolute terms. This
comparison needs both small enthalpy/k^2 AND controlled momentum correction
relative to the chosen density scale; k much larger than H alone is not a
proof for every state or a density zero. Lapse obeys the additional bound
|Psi-Phi_N|<=|Phi-Phi_N|+|Pi|/k^2. Include these terms instead of deleting
relativistic or anisotropic contributions by name.

Dstar here is the compensated canonical density, not silently the same as
the physical density perturbation. The exact alternative physical-source
identity is k^2 Phi=-(D_total+3H Q_total/k)/2. Recovering a Poisson problem
with physical density requires bounding that current term and the slip.
The physical G is inherited from the retained Einstein action throughout.
