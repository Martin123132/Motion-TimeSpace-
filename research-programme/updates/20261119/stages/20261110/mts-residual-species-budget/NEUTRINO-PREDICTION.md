# Frozen analytic prediction before the neutrino-specific evaluation

This prediction follows from the retained `Nu_Integrate_L012` and `derivs`
equations, not from fitting the measured residual. Restrict to a flat geometry,
all momentum nodes evolved, no relativistic-tail or late-fluid substitution.
Verify those discrete flags before use.

At each native momentum node write v=(1+(am/q)^2)^(-1/2), with the fixed
integration coefficient B. The synchronous source coefficients are

    d = B/(a^2 v),  j = B/a^2,  p = B v/a^2,
    D_nu = sum d F0, Q_nu = sum j F1, Pi_nu = sum p F2,
    P_nu,pert = sum p F0/3.

The symbols d,j,p here denote source weights, not background density,
current or pressure. Differentiate them at fixed F_l using a'=aH:

    d' = -H(1+v^2)d, j'=-2Hj, jv=p, dv=j.

The native monopole/dipole equations in this regime are

    F0'=-k(4z/3+v F1), F1'=kv(F0-2F2)/3.

Substitution, with no radiation fitting, gives

    ED_nu,sync = D_nu' + H(D_nu+3P_nu,pert) + kQ_nu + kz S_nu
                = kz [S_nu - (4/3)sum d],
    EQ_nu,sync = Q_nu' + 2HQ_nu - kP_nu,pert + 2kPi_nu/3 = 0,
    K_nu = ED_nu,sync + 3H EQ_nu,sync/k
         = kz [S_nu - S_quadrature], S_quadrature=(4/3)sum d.

The background uses a separate thermal integral/interpolation. In the
continuum, integration by parts links its enthalpy to the perturbation kernel;
the two finite numerical representations need not satisfy that identity
exactly. This is a predicted quadrature/representation compatibility defect,
not evidence for a new MTS force or a neutrino non-conservation law.

Test this formula on BOTH corrected and original trajectories in cold,
native heavy, D0 and D01. Recover existing weights from source rows, not
parameter fitting; check their support, j^2=dp, the actual native F0/F1 RHS,
and the retained regime flags. Compute the analytic source derivative as an
independent diagnostic without changing any saved evolution or source row.
Compare the finite-stencil remainder separately. Omitting S_nu-S_quadrature
must fail to predict a resolved nonzero K_nu. A successful diagnosis does not
authorize changing either quadrature weights or the background silently.
