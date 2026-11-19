# Species budgets and the retained neutrino source defect

Use the retained flat scalar conventions, conformal time in Mpc (c=1),
H and k in Mpc^-1, alpha in Mpc, and stresses multiplied by 8 pi G a^2.
Density, pressure, current and anisotropic stress then have Mpc^-2 units;
their conservation budgets have Mpc^-3 units. No new gravitational coupling
or species parameter is introduced.

## Separate an intrinsic species defect from a common metric defect

Let Ds_i, Qs_i be synchronous sources, Si the background enthalpy and Pi_i
the anisotropic stress. The retained Newtonian sources obey

    Di=Ds_i-3H Si alpha, Qi=Qs_i+k Si alpha,
    Phi=eta-H alpha, Psi=Phi-Pi_total/k^2.

Define the pressure-eliminated Newtonian species budget

    Ji = Di'+H Di+k Qi-3Si Phi'
         +3H Qi'/k+6H^2 Qi/k-3H Si Psi+2H Pi_i,

and its synchronous counterpart

    Ki = Ds_i'+H Ds_i+k Qs_i+kz Si
         +3H Qs_i'/k+6H^2 Qs_i/k+2H Pi_i.

Direct substitution, without imposing the Einstein equations, gives

    Ji=Ki+3H Si Ealpha-3Si Eeta,
    Ealpha=alpha'+H alpha-Psi,
    Eeta=eta'-k(k alpha-z)/3.

Thus assigning all of Ji to the species itself would mix a common clock/
metric defect into the attribution. The numerical implementation keeps
these pieces separate, and includes 3 EH Q_total/k in the total budget,
where EH=H'-H^2+S_total/2. All seven species sum back to the original rows.

For the native baryon approximation,

    Ds_b'=-H Ds_b-k Qs_b-kz Rb,
    Qs_b'=-2H Qs_b+k Ps_b+Xb,
    Kb=3H Ps_b+3H Xb/k.

Photon momentum exchange is -Xb. Pure CDM has Kc=0 algebraically. Finite
differences of their source rows can have appreciable relative error when
the resulting budget is tiny; these errors are recorded, not converted
into exact numerical zeros or evidence of a new force.

## Full momentum hierarchy: a concrete quadrature compatibility condition

The retained native regime has one massive-neutrino eigenstate, five
momentum nodes and no late-fluid or relativistic-tail approximation.
These flags and the mapped monopole/dipole/quadrupole coordinates are
checked from the captured native signature, not assumed from a model name.

At a node of fixed momentum q, write v=(1+(am/q)^2)^(-1/2), with native
quadrature kernel B. Its stress weights are

    d=B/(a^2 v), j=B/a^2, p=Bv/a^2,
    d'=-H(1+v^2)d, j'=-2Hj, j^2=dp.

The original native equations, checked row-by-row, are

    F0'=-k(4z/3+vF1), F1'=kv(F0-2F2)/3.

With D_nu=sum dF0, Q_nu=sum jF1, P_nu,pert=sum pF0/3 and
Pi_nu=sum pF2, substitution gives exactly

    ED_nu,sync=kz(S_nu-S_quadrature),
    EQ_nu,sync=0,
    K_nu=kz(S_nu-S_quadrature),
    S_quadrature=(4/3)sum d.

This is the tested prediction, frozen in NEUTRINO-PREDICTION.md before its
specific evaluation. S_nu comes from the existing thermal background;
S_quadrature comes from the existing perturbation source coefficients.
Neither is chosen using the residual or any galaxy data.

For a continuous Fermi-Dirac distribution f(q), let C=7 pi^4/120 and
epsilon=sqrt(q^2+m^2). Integration by parts, with vanishing endpoint terms,
gives the needed identity

    (1/(3C)) integral q^3 epsilon (-f') dq
      = (1/C) integral [q^2 epsilon+q^4/(3epsilon)] f dq.

Separate finite quadratures need not preserve it. The two continuous
integral expressions agree in the independent reference test; the finite
native representations do not agree exactly with each other.

## Identify both sides, not just the perturbation rule

The original five-node source table's unsuffixed Fortran literals are
REAL32 before promotion into real(dl). Reproducing this detail is required
to reproduce the captured node velocities and weights. It is not a newly
fitted mass; all five velocities yield the same am once literal semantics
are respected. See CONTINUUM-LITERAL-REPAIR.md for the retained failed reader.

The hypothesis that the five-node rule alone accounts for the discrepancy
failed. The native background itself uses a 100-step q=0..30 integral and
a 1400-point interpolation table. Reproducing its own integration and
spline recurrence explains the larger contribution to the mismatch.

For the enthalpy integrand F(q)=[q^2 epsilon+q^4/(3epsilon)]f(q), the
Euler-Maclaurin lower-endpoint terms predict continuum minus native:

    [m h^4/480
     +(m^2-10) h^6/(12096m)
     +(m/115200-1/(13824m)-7/(23040m^3)) h^8]/C,
    h=30/nq.

These coefficients are obtained from the Taylor series, not fitted to
numerical errors. Finite upper-tail and interpolation errors are additional
remainders. The expression predicts the observed 100-step enthalpy error
to about 1.29e-6 relative accuracy over the tested points. The independent
100/200/400/800-step sequence converges as expected. This is reference
evidence, not a rigorous all-time error enclosure or a production edit.

## Route to a metric-consistency bound

Let Ec=2k^2 Phi+D_N+3H Q_N/k. Since
z=[Ds_total/(2k)+k eta]/H, the clock identity including a nonzero Ec is

    Ephi+H Ealpha=Eeta-Ec/(6H)-EH alpha.

Combining this with the retained generalized constraint identity gives

    2k^2 Ephi = Ec'+(H+S_total/(2H))Ec
                -sum Ki-3EH Qs_total/k.

The triangle inequality bounds |Ephi| by the absolute terms on the right
divided by 2k^2. The neutrino-specific contribution is therefore
`-z(S_nu-S_quadrature)/(2k)`, with every other species/background/constraint
term retained separately. This is not a prescription to subtract an error
from the metric. It identifies and bounds a numerical source contribution
to the same GR consistency equation. A uniform time or local-GR statement
requires verified bounds over the relevant domain, not just these probes.
