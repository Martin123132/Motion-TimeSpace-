# Second metric source and clock acceleration: a derived higher-spatial estimate

Date: 2026-09-09. Private canonical annular continuation.

## 1. Result, without promoting its assumptions

The preceding energy estimate needed T2=||theta_t||_Q, where Q is the
ACTUAL positive quadrature. It previously inserted a measured second jet.
This step derives a bound on T2 from the actual second constraint equations,
including the differentiated metric-link Gram current and physical inner
mass-flux trace. No unknown second metric derivative is an input to the bound.

There is an explicit higher spatial regularity input:

    H^2 = ||g_hat||_K^2 + ||M^-1 K z||_M^2,
    z=(chi_t-l_t)_free,
    g_hat=M^-1(K(chi-l)_free-F_b).

Here M,K,F_b and the affine lift l are the unchanged objects from the previous
step. H uses configuration, first rates, scalar spatial operators and boundary
data, not N_tt, mu_tt, theta_t or a new fitted parameter. It is an additional
regularity norm, NOT the Hubble parameter or a new field.

The resulting estimate has the form

    ||theta_t||_Q <= C0(E, boundary, residuals) + C1(E, boundary, residuals) H

within the existing canonical configuration box. The constants contain NO
inverse mesh power. This is a conditional analytic estimate: it is uniform
over mesh spacing when its stated inputs are uniformly bounded. H has NOT
been propagated in time. It is not legitimate to rename that missing evolution
argument a completed stability proof. The constants remain extremely loose.

591/591 implementation/algebra checks pass on 18 unchanged saved states and
six off-shell second-jet controls. These are not independent physics tests,
outward-rounded interval certificates, or evidence of black-hole regularity.

## 2. Source ownership and reproduction

Previous energy and projection theorem:
`DERIVATION-20260909-H1-clock-energy-transport-and-boundary-feedback.md`.
First-source, physical shift and spatial bounds:
`DERIVATION-20260909-first-metric-source-and-pointwise-lapse-bound.md`,
`DERIVATION-20260909-clock-spatial-gradient-and-derived-coefficient-input.md`.
Metric inverse and actual equations:
`scripts/annular_metric_schur_bound_20260909.py`,
`scripts/annular_released_hermite_action_20260909.py`,
`scripts/annular_metric_link_quadratic_20260909.py`.
Independent old jet owner:
`scripts/annular_metric_flux_jets_20260909.py`.

New immutable helper and runner:
`scripts/annular_second_metric_source_20260909.py`,
`scripts/derive_annular_second_metric_source_20260909.py` (derive/seal).
Result:
`source-intake/navier-stokes/20260909/annular-second-metric-source-derived/status.json`.
Final integrity:
`source-intake/navier-stokes/20260909/annular-second-metric-source-final-integrity.json`.

The runner uses one single-core BelowNormal process and python -B. It does
not evolve a new trajectory or prescribe favorable boundary values. It checks
inherited hashes and preserves the old physical mismatch, its time derivative
and full shift residual. Second-jet differentiation is checked against an
independent term-by-term source expansion rather than only calling the same
jet implementation twice.

## 3. Retained domain and notation

Canonical only: b2=b3=m_chi=Lambda=0, kappa=1/10,
R in [47/8,49/8], ell=1/4, n>=17 scalar nodes.
The original positive box is retained:

    .65<=F<=.68, .8<=N<=.84,
    |q|<=Q0=.02, |w|<=W0=.03, |mu_R|<=U0=.002,
    q=chi_t, w=chi_R, A=RF, theta=N_t/N-mu_t/A.

Set A0=(47/8)*.65, N0=.8, N1=.84, m_+=60025/1024,
p_+=16807/640 and the previous positive m_-,p_-.
All scalar slope coordinates stay free; only the original endpoint values
are prescribed. The natural outer clock equation remains part of the action.
The actual scalar endpoint histories are quadratic and outer clock history
linear: scalar endpoint jerk and c_b'' vanish in the saved problem. A nonzero
c_b'' is explicitly retained in the general source and manufactured controls.
Changing to a nonzero scalar endpoint jerk would require its lift terms;
the current theorem must not be used unchanged for that case.

The previous derivation supplies, from E and the physical boundary data,

    R1 >= ||mu_t,R||_2, ||N_t||_(h l2),
    U >= ||mu_t||_infinity, V >= ||N_t||_infinity,
    Q1 >= ||q_R||_2, A2 >= ||chi_tt||_2,
    Lp >= ||p_R||_infinity, Htheta >= ||theta_R||_2.

Write S=V/N0, D=U/A0, Theta=S+D, and let s>=sqrt(2E_raw).
The prior raw/adapted-energy feedback inequality supplies s from E_hat when
its explicitly checked feedback is below one. These rates are bounds from
the first equations, not inserted measurements of interior metric rates.

## 4. What H controls, and why it is not automatically controlled by E

Let B_A and D_infinity be the previously derived H1 mass-transport and
elliptic derivative-sup constants. The actual scalar equation is

    a = l_tt - g_hat - M^-1 M_t z + M^-1 r,
    a=chi_tt,

on free coordinates, with the prescribed acceleration lift restored.
Consequently

    A1 := ||(l_tt)_R||_2 + (H+B_A s+R_graph)/sqrt(p_-)
        >= ||a_R||_2,
    Ainf := A2/sqrt(ell)+sqrt(ell) A1 >= ||a||_infinity,
    Qinf := |(l_t)_R|+D_infinity H >= ||q_R||_infinity.

R_graph is the retained scalar residual in K-graph norm. The last estimate
applies elliptic H2 control to z=K^-1 M(M^-1 K z). It does not apply an
unjustified pointwise inverse inequality to q_R. Boundary-adapting g_hat is
important: separately projecting nonzero endpoint data into a zero-value
space would create an artificial boundary layer in the acceleration estimate.

An exact function-space example shows why H cannot simply be called another
name for E. Take chi=0 and a two-cell, zero-slope Hermite bump q with nodal
height c sqrt(h). Its smoothstep shape has integrals 13/35 and 6/5 for
shape squared and derivative squared respectively. Hence

    ||q||_2^2=(26/35)c^2 h^2,
    ||q_R||_2^2=(12/5)c^2,
    ||M^-1 K q||_M >=
        (12/5)p_- c / [sqrt(m_+)sqrt(26/35) h].

The last inequality follows directly from q^T K q <= ||q||_M||M^-1 Kq||_M.
The lower graph energy stays bounded while the higher graph norm grows.
This is a statement about the actual free approximation space, NOT a
constructed constraint-satisfying physical trajectory or a no-go theorem
for bounding T2 by another lower-regularity argument. A better cancellation
could still avoid H; this step does not prove H is necessary.

## 5. Exact second source: unknown accelerations kept on the left

Let J be the original free constraint Hessian, with metric block J_gg,
scalar block M and coupling C. Its SAME Schur complement is

    S_metric=J_gg-C M^-1 C^T,  ||S_metric^-1||_(X*->X)<=175/118.

X is the existing mass-H1/lapse-nodal-L2 space; mass perturbations vanish at
the inner endpoint after lifting. No new inverse is fitted from eigenvalues.
Differentiate twice, putting mu_tt,N_tt and q_tt on the left. The known
second forcing k is evaluated with those packed second rates set to zero,
but chi_tt=a remains in the configuration derivative. In particular a and
q_tt are different derivative orders and are not interchanged.

For an independently checkable expansion, put s_N=N_t/N, d=mu_t/A.
The known second mass-row density consists of

    g_mu = [2 N_t mu_tR + 6d(N_t mu_R+N mu_tR)
                              +15d^2 N mu_R]/(kappa R F^(3/2)),
    k_mu = R/(2N F^(3/2)) [2a^2+4(-s_N+3d)qa
                              +(2s_N^2-6s_N d+15d^2)q^2],
    w_mu = RN/(2sqrt(F)) [2(q_R^2+w a_R)+4(s_N+d)w q_R
                              +(2s_N d+3d^2)w^2].

Its coefficient paired with the mass test derivative is

    j_mu = [2 N_t d+3N d^2]/(kappa sqrt(F)).

The known lapse-row densities are

    g_N = [2d mu_tR+3d^2 mu_R]/(kappa sqrt(F)),
    k_N = -R^2/(2N^2 sqrt(F)) [2a^2+4(-2s_N+d)qa
                              +(6s_N^2-4s_N d+3d^2)q^2],
    w_N = -R^2 sqrt(F)/2 [2(q_R^2+w a_R)-4d w q_R-d^2 w^2].

Thus k_mu(xi)=Q[(g_mu+k_mu+w_mu)xi+j_mu xi_R] plus Gram and
-c_b''xi(b)/kappa, while k_N(n)=Q[(g_N+k_N+w_N)n] plus Gram.
The repeated k_mu notation denotes its kinetic density or entire functional
according to the displayed argument; the script uses unambiguous separate keys.

The known scalar-velocity source is exactly

    k_v = [M_known,tt q +2M_t a+K_t chi+Kq]_free,
    m_known,tt = m(2s_N^2-2s_N d+3d^2).

This includes the derivative of the actual scalar force; it does not treat
the canonical momentum's second derivative as zero. Its dual norm obeys

    V2 = sqrt(m_+)Q0 sqrt(ell)(2S^2+2SD+3D^2)
           +2sqrt(m_+)Theta A2+B_L s+H
           +(33/sqrt(m_-))[(Lp Theta+p_+Htheta/sqrt(ell))||(l)_R||_2
                                                +Lp||(l_t)_R||_2].

The Gram part annihilates the affine lifts, including with time-varying
coefficients. The H1 transport theorem, not theta_R infinity, bounds K_t.

## 6. Differentiated Gram density and source norms

With the owned nonnegative sampling and factor matrices,

    rho=S_sample^T(Tchi)^2/(2h),
    rho_t=S_sample^T[(Tchi)(Tq)]/h,
    rho_tt=S_sample^T[(Tq)^2+(Tchi)(Ta)]/h.

The existing factor estimates and Cauchy-Schwarz give

    ||rho||_(h^-1 l2) <=2W0^2 sqrt(ell_n), ell_n=17ell/16,
    ||rho_t||_(h^-1 l2) <=sqrt(8)W0 Q1,
    ||rho_tt||_(h^-1 l2) <=sqrt(8)(Qinf Q1+W0 A1).

For the first term use rho_q,j<=2h Qinf^2 and sum rho_q<=Q1^2;
for the cross term use the same factor Cauchy estimate with a in place of q.
The actual known second Gram atoms are

    b_mu = (p/A)[rho_tt+2(s_N+d)rho_t+(2s_N d+3d^2)rho],
    b_N = -(p/N)[rho_tt-2d rho_t-d^2 rho],

evaluated at the owned nodes, not replaced by continuum surrogates.

Take absolute values in section 5 and use, for example,
||a^2||_2<=Ainf A2, ||q_R^2||_2<=Qinf Q1,
||w a_R||_2<=W0 A1 and ||N_t mu_tR||_2<=V R1.
All coefficients are bounded using the canonical box. Denote the resulting
L2 density bounds by G_mu,K_mu,W_mu,J_mu,G_N,K_N,W_N,
and the atom dual bounds by B_mu,B_N. The helper records every one separately.
There is no fit or cancellation assumption in those positive expressions.

    K2_mu = ell(G_mu+K_mu+W_mu)+J_mu
                   +sqrt(17/16)ell B_mu+sqrt(ell)|c_b''|/kappa,
    K2_N  = G_N+K_N+W_N+B_N.

These are actual X*-component bounds. Cubic products are integrated exactly
in the unweighted Q norms; coefficient positivity supplies the weighted
inequalities. No continuum norm of an arbitrary sampled function is substituted.

## 7. The inner-flux derivative is derived, not chosen

The actual full shift solve is P u+matter-Gram=0. Differentiate it using
the ACTUAL packed first rates, not by replacing mu_t everywhere with u:

    P u_t = Gram_t-matter_t-P_t u + residual_t.

The old positive row-gap factor is g=55625/3094. Its star-volume proof gives
the same inverse for this source. Let

    Wplus=1/[kappa N0 F0(4/5)], Iplus=1/(N0^2 F0),
    Jdot=(Rmax^2/(N0 sqrt(F0)))(Ainf W0+Q0 Qinf+Theta Q0 W0),
    Gdot=I_Gram 68 p_+ Iplus(Ainf W0+Q0 Qinf+3Theta Q0 W0),
    Pdot=Wplus(S+3D) Ushift,
    U2=(3/g)(Jdot+Gdot+Pdot)+(6/g)epsilon_shift,t.

Then ||u_t||_infinity<=U2, including its inner component. Ushift is the
already-derived full shift bound; epsilon_shift,t is the retained residual
per star volume. No second metric input occurs in these expressions.

To see the factor 3Theta in Gdot, write the owned link current as a
trilinear function of (chi,q,p). Its derivative is the sum of currents
(q,q,p), (chi,a,p), (chi,q,p_t). The old exact factor-overlap majorant68
applies to each. The inverse-clock link derivative contributes another
2Theta. Hence all signed link integrations and Gram currents are retained.
The canonical local shift-coefficient derivative is identically zero, but
the metric-link current and its derivative are NOT set to zero.

## 8. Eliminating metric accelerations and obtaining T2

Lift mu_tt(a)=u_t(a) as a constant mass field l2; all scalar endpoint jerks
are zero for the actual histories. The exact reduced equation is

    S_metric (x_tt-l2)_g =
       -k_g+C M^-1 k_v-J_g l2+C M^-1 J_v l2.

The runner reconstructs this equation against the independently owned second
jets. Let c_mu,c_N and L_mu,L_N be the coupling and constant mass-lift bounds
already derived in the first-source note. They depend on configuration, not
on which time derivative is lifted. Explicitly c_mu=sqrt(m_+)Q0 ell/A0,
c_N=sqrt(m_+)Q0/N0; the same gravitational, projection and Gram lift terms
are retained. Then

    F2_mu=K2_mu+c_mu V2+L_mu U2,
    F2_N=K2_N+c_N V2+L_N U2,
    R2=(175/118)(hypot(F2_mu,F2_N)+epsilon_second).

The existing inverse yields ||mu_tt,R||_2 and ||N_tt||_(h l2) <=R2.
Only the norm needed for the target is taken; a pointwise N_tt bound is
unnecessary. Restoring the constant inner lift gives

    ||mu_tt||_Q<=sqrt(ell)U2+ell R2,
    ||N_tt||_Q<=R2,
    T2 <= R2/N0+[sqrt(ell)U2+ell R2]/A0
                              +sqrt(ell)(S^2+2D^2).

The last line follows from the EXACT formula
theta_t=N_tt/N-(N_t/N)^2-mu_tt/A-2(mu_t/A)^2.
All second metric derivatives are outputs, not assumptions or measured inputs.

Each component before the final hypot is nonnegative affine in H when the
lower inputs are fixed. Triangle inequality therefore gives a valid affine
T2 majorant. Its slope is formed from the norm of the component slopes,
NOT from f(1)-f(0) of a convex norm, which would generally underbound it.

## 9. Checks and numerical size

591 checks include full independent second-source reconstruction, every
bulk/Gram source norm, the actual differentiated shift equation, constant
inner-lift restoration, the Schur response, the scalar acceleration identity,
and preservation of the old physical discrepancy arrays. Six off-shell
controls change the first-rate signs/amplitudes and use nonzero c_b''=.005.
Their second sources match independent jet differentiation. These controls
are not evolved solutions or evidence for a physical parameter choice.

At the old final N64 states:

| Quantity | GR control | Metric Gram |
|---|---:|---:|
| H, evaluated | 5.963207 | 6.131495 |
| Actual ||theta_t||_Q | 0.00160720 | 0.00154264 |
| Derived T2 bound conditional on H and lower inputs | 4854.620 | 38789.498 |
| Actual inner u_t | 0.00990387 | 0.00975552 |
| Derived entire u_t sup bound | 17.9060 | 3364.319 |
| Actual second metric response norm | 0.100192 | 0.101119 |

These upper bounds are VERY conservative, not predictions of large physical
accelerations. Both branches receive the same methodology. The larger Gram
majorant reflects discarded cancellations, not an observed physical instability.

Substituting the new T2 bound in the prior boundary-energy formula is direct:
add sqrt(2E_hat) times the saved T2 coefficient in F1 times
(new T2 bound minus previously evaluated T2). On the final N64 states this
gives energy-rate upper bounds about 5054.964 (GR) and 39124.735 (Gram),
versus actual rates about .03071. This removes the measured T2 substitution,
but it still conditions on H. It does not certify the saved time interval.

The H values sampled on these grids look finite; this is not a proof of
uniform-in-time or continuum control. All calculations use ordinary floating
arithmetic with residual tests, not outward-rounded numerical certificates.

## 10. Next target: evolve the remaining spatial norm, not another input audit

The second constraint forcing, inner flux derivative and conditional T2 bound
are now explicit. Do not repeat a missing-second-source inventory or promote
the sampled H values to a theorem.

Next attempt a spatially commuted energy estimate for H (or an equivalent
boundary-compatible spatial energy), using the actual projection, Gram and
constraint equations. Establish the regularity and endpoint compatibility it
requires. Avoid simply differentiating the same energy repeatedly in time:
that can manufacture an endless demand for theta_tt, theta_ttt and so on.
If a lower-regularity cancellation avoids H, derive and verify that alternative
rather than assuming the present sufficient estimate proves H necessary.

Then combine the lower-energy inequality with the new estimate, tighten the
constants and prove persistence of the configuration box. Full shift/DAE
compatibility, nonlinear P(X), parent calibration and horizon/global regularity
remain separate open tasks. This F>=.65 annulus is not a black-hole interior.

No GitHub action. Protected-workbench check uses mtimes since
2026-09-09T21:55:00Z, not a complete pre-turn hash baseline.
