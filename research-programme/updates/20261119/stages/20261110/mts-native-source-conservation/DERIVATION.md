# Source-owned Friedmann and shear defects

Use conformal H, comoving wave k, native R=8*pi*G*a^2*rho and likewise P,
D,Q,deltaP,Pi. All formulae below are for the retained spatially flat branch.
The code uses eta'=Q/(2k), z=(D/(2k)+k*eta)/H and
alpha=z/k+3Q/(2k^3). Phi=eta-H*alpha; Psi=Phi-Pi/k^2.

Define genuine equation residuals, not new stress tensors:

    E_R = R' + H*(R+3P),
    E_H = H' + (R+3P)/6 = E_R/(6H),       if R=3H^2,
    E_D = D' + H*(D+3deltaP) + k*Q + k*z*(R+P),
    E_Q = Q' + 2H*Q - k*deltaP + 2k*Pi/3.

Differentiating the constraints, using R=3H^2, gives exactly

    E_alpha = alpha'+H*alpha-Psi
            = E_D/(2k^2 H)+3E_Q/(2k^3)-z*E_H/(kH).       (1)

Pressure terms cancel in this derivation. Thus a background defect alone is
not enough: the corresponding perturbed source defects must also be counted.
CDM delta_c'=-k*z implies dstar_c'= -k^2 alpha, where dstar_c=delta_c-3eta.

For each retained canonical real scalar b with v and mu^2=a^2*m^2 define

    E_b=v'+2H*v+mu^2*b,     E_f=b'-v.

Its actual synchronous perturbation equations are u'=w and
w'=-2H*w-(k^2+mu^2)u-k*z*v. Direct differentiation then yields

    E_R,scalar = v*E_b+mu^2*b*E_f,
    E_D,scalar = w*E_b+mu^2*u*E_f,
    E_Q,scalar = k*u*E_b.                                (2)

These derive from the original action and actual tabulated fields; no
coefficient is selected against a residual. In N=ln(a), E_R/H equals
v*(v_N+2v)+mu^2*b*b_N, so source attribution can be integrated without
numerically differentiating a noisy total H history.

## Baseline pressure approximation must be counted

The inspected native equations evolve baryon density as delta_b'=-k(z+v_b)
with R_b proportional to a^-1, while retaining deltaP_b=R_b*delta_p_b in
the Euler equation. Their background P_b=0. Consequently the native baryon
energy equation has E_D,b=3H*deltaP_b. This is an existing nonrelativistic
approximation, not new MTS physics. Photon/baryon momentum drag cancels by
the explicit qgdot definition in equations.f90; its algebra must be checked.
The predicted baryon contribution to (1) is3deltaP_b/(2k^2).

CDM, photons and massless background radiation have E_R=0 analytically.
Massive-neutrino R,P are read from the retained native history and their
remaining conservation contribution is reported separately. Missing
massive-neutrino pressure perturbations are not invented or set to zero:
any unclosed perturbative remainder remains explicitly unassigned.

## Diagnosis versus physical repair

Integrate the predicted E_H and E_alpha and compare with saved history
residuals before changing sources. Use the original scalar response equations
to assess amplification into the slow-field/current. This use of defects
diagnoses a numerical/approximation interface; do not insert them as extra
physical forces or treat an exact diagnostic identity as a new observation.
