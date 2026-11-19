# Direct source curvature with coupled metric and representation defects

## Scope and source authority

This is a derivative of the retained, unswitched native scalar/background representation, not a new action or a fitted pressure law. The existing 902 signed preparation nodes, their weights, k=5/Mpc, masses and normalization are unchanged. The native conformal time is in Mpc (c=1); first/second derivatives carry one/two inverse conformal-time units relative to their sources. Cold uses its retained normalization and its own native clock. Existing source files are enumerated and hashed in frozen-inputs.json and native-bootstrap-result.json.

The read-only addition to native/fortran/camb_python.f90 calls mts_curvature_hook.inc on original preparation outputs only. It does not replace the native evolution, field tables, photon/scattering bank or metric. Native equations.f90, MTSTwoField.f90, massive_neutrinos.f90 and forutils/Interpolation.f90 remain unchanged copies. Unsupported fluid-approximated massive-neutrino, omitted-multipole, curved, switched or quintic-clock regimes are explicitly rejected by the new readout. Its neutrino-background derivative is restricted to the small-am branch actually encountered here.

## Primitive differentiation

Write b,v for background field/velocity; u,w for perturbation field/velocity; r=(log a)', H for the native Friedmann rate, m2=(a*m_h)^2 and beta=a/R0. Do not set r=H or b'=v for the retained interpolation.

    b' = r*b_N;       v' = r*v_N
    b'' = r'*b_N + r^2*b_NN
    v'' = r'*v_N + r^2*v_NN
    u' = w
    w' = -2H*w - (m2+k^2)*u - k*z*v
    u'' = w'
    w'' = -2H'*w - 2H*w' - 2r*m2*u
          - (m2+k^2)*u' - k*(z'*v + z*v')
    m2' = 2r*m2;     m2'' = (2r'+4r^2)*m2
    beta' = r*beta;  beta'' = (r'+r^2)*beta

The sources are Y=beta*(v*w+m2*b*u, k*v*u, v*w-m2*b*u). For each bare component B:

    Y'' = beta*[B'' + 2r*B' + (r'+r^2)*B].

The field second derivatives are the analytic natural-cubic spline derivatives, not another finite difference of saved source rates. Native thermo interpolation has a(tau)=tau*S(x), x=log(tau/tau_min)/dlntau+1. Thus

    r = 1/tau + S_x/(dlntau*a)
    r' = [S_x/dlntau + S_xx/dlntau^2]/(tau*a) - r^2.

These retain the actual interpolation derivatives. Python's independent natural-cubic values and first/second derivatives agree with the native field jets at the algebra gate.

## Metric and rest derivative, without frozen forcing

For the retained flat convention, D is the unnormalized total perturbed density source, R the total background density source, and eta_k the native metric variable:

    H^2 = R/3
    H' = R'/(6H)
    z = [D/(2k) + eta_k]/H
    z' = [D'/(2k) + eta_k']/H - z*H'/H.

eta_k' is taken from the actual coupled native RHS. D' differentiates all matter, radiation, massive-neutrino and scalar contributions. A matter term R_i*delta_i gives R_i*(delta_i'-r*delta_i); radiation gives R_i*(delta_i'-2r*delta_i). Scalar terms use the first line of the primitive product rule and the coupled w', not a prescribed external source.

For each massive-neutrino eigenstate with coefficient A=a^-2*constant, let I_rho(y,a), I_p(y,a) be the existing momentum integrals. The state dependence is linear and, at fixed state,

    partial_N I_rho = I_rho - 3 I_p
    (A I_rho)' = A*[I_rho(y',a) - r*(I_rho+3 I_p)].

The same native quadrature is applied to y and the full native y'; no massless pressure replacement is made. R' likewise differentiates the actual background field splines and the native neutrino rho_P expansion. Its small-am derivative is differentiated from the rho_P coefficients themselves. The separate native drho routine differs slightly (maximum effect on R' about 6.185e-12 in native units here), so that independent approximation is NOT substituted. Neither old routine is edited; this is not a claim of a general repair or a significant cosmological bias.

## Explicit folded-generator cross-check

Let j=beta*(b*u,b*w,v*u,v*w), E_b=b'-v and E_v=v'+2Hv+m2*b. The retained A_free plus E_b/E_v rank-one background-defect terms gives the bare generator. With G=(0,beta*b*v,0,beta*v^2) and o_D=(m2,0,0,1), fold scalar self-gravity into

    A = A_bare - G o_D/(2H beta)
    zeta = z - Y_D/(2kH beta)
    f = -k*zeta*G.

Differentiate ALL factors, including E_b', E_v', 1/(H beta), G and o_D. The required rest rate is obtained, not assumed:

    zeta' = z' - [Y_D' - Y_D*(H'/H+r)]/(2kH beta).

Then

    j'' = (A' + A^2)j + A*f + f'
    Y'' = O''j + 2O'j' + O*j''.

check_operator_derivative.py implements that folded expression separately from the primitive product expansion. Density, current and pressure match for both first and second derivatives at every prepared node under the unchanged algebra gate. The weighted second derivatives agree to at most 2.57e-14 in absolute native units. Current-rest time dependence and self-gravity are present throughout.

## What is causing the finite-interval sensitivity?

Define E_b'=b''-v' and E_v'=v''+2H'v+2Hv'+2r*m2*b+m2*b'. The exact source curvature can be partitioned as

    Y'' = R_smooth + C_b E_b' + C_v E_v'
    C_b = beta*(m2*u, 0, -m2*u)
    C_v = beta*(w, k*u, w).

Here R_smooth means the algebraic remainder, NOT a proof that every remaining term is slowly varying. Weighted pressure curvature is 0.0003277139150291484; its explicit background-defect derivative contribution is 0.00021262614660543305 (about 65%), leaving 0.00011508776843015094. These contributions are evaluated at the same original nodes with a fixed partition; nothing is removed from the tested prediction. They identify a substantial numerical-representation sensitivity, not proof that it accounts for the entire finite-interval discrepancy.

## Derived next calculation: integrate, rather than freeze, the defect derivative

For any prepared node, offset s and one of the coefficient/defect pairs C,E, integration by parts gives

    integral_0^s (s-t) C(t) E'(t) dt
      = -s*C(0)*E(0) + integral_0^s C(t)*E(t) dt
        - integral_0^s (s-t)*C'(t)*E(t) dt.

This is an exact identity for the piecewise-smooth retained representation, also valid after the fixed signed weighted sum. It removes the need to represent a rapidly varying defect derivative by its initial value. It does NOT set E=0 or change the background bank. C_b' and C_v' follow from the primitive equations above. Any approximation used for their time variation must be frozen and tested, not fitted to the existing pressure discrepancy. The finite-time remainder from R_smooth still requires a check; this identity alone does not guarantee a pass.

The next stage should evaluate this integrated form using the existing backgrounds and equation-owned coefficients. A new long evolution, blind stencil increase, tolerance change or deletion of the defect is not warranted by this result.
