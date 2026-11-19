# Metric coupling uncertainty from the saved cold background

## 1. Exact scalar pressure cancellation in GR
Use the retained canonical heavy-scalar stress rows at fixed slow state:

    D=rho delta
    P=rho[-c delta+2s W/alpha]
    Q=(rho H/k)[-alpha s delta/2+(1-c)W]
    c=cos(2theta), s=sin(2theta), alpha=k^2/(a m H).

The already-derived source equations give

    D_free=-D-3P-kQ/H
    Q_free=-2Q+kP/H.

Therefore D_free+3H Q_free/k=-D-(k/H+6H/k)Q. The large pressure terms cancel exactly. This is the canonical continuity/current identity, not an assumption that pressure is small.

Let d_phys=2k^2+3Wq and Delta=Wq-W_true. With eta=H_N/H=1-W_true/(2H^2), the GR metric equations reduce, on the heavy columns, to

    Psi_h= -rho/(2k^2) [ e_delta+3(H^2/k^2) q ]
    Phi_N,h = -Psi_h+rho/(2k^2)(1-3Delta/d_phys) q
    q=[-alpha s/2,1-c], e_delta=[1,0].

Unlike the unsimplified pressure/current expression, this row has no1/alpha pressure amplification. The quadrature defect Delta remains explicit. Setting it to zero would be an extra approximation and is not done here.

The separately retained spatial-Poisson row is

    Psi_P,h=-rho e_delta/(2k^2)
    Phi_P,N,h=rho/d_phys [e_delta+3(-c,2s/alpha)+q+3Delta e_delta/(2k^2)].

Its oscillatory pressure term does not cancel in the same way. This distinction explains why the two branches need different sensitivity/remainder bounds. It is not an observational preference or a statement that all spatial-Poisson applications fail.

## 2. The full retained momentum row, both baseline and MTS
Let Q be the full current row in the current physical/relative coordinates, e_alpha the retained CDM gauge/velocity slot and rho_c its background density. Let P_b be the baryon pressure perturbation row as implemented by the native equations. All other canonical scalar, photon and massive/massless-neutrino pressure terms cancel in the same continuity/current combination. The external quadrature-defect derivative cancels as well.

The exact identity for the RETAINED native source approximation is

    Phi_N+Psi = (1-3Delta/d_phys)[Q+Delta e_alpha/sqrt(rho_c)]/(2kH)
                -3P_b/d_phys.

This is verified symbolically and against every full native source row, not just the heavy block. The gauge correction must not be dropped independently of the enthalpy defect.

The residual -3P_b/d_phys is shared by baseline and MTS: the inherited source includes the baryon pressure perturbation in its velocity equation while the matter-density continuity approximation omits the matching -3P_b contribution. This audit exposes and measures that existing approximation rather than misattributing it to MTS. Removing the term by declaration would alter the retained source, so this stage does not do so.

For the heavy columns P_b and e_alpha vanish, giving the simpler identity in section1. The full identity supplies a direct route to the remaining external-column bound without reintroducing cancellation-heavy pressure derivatives.

## 3. Exact normalized denominator jets
At fixed slow state define

    d0=2k^2+3[Wq_ext+v_s^2+rho]
    epsilon=3rho/d0
    d=d_phys/d0=1-epsilon c.

Wq_ext contains cold fluids, radiation and the retained five-node massive-neutrino quadrature, but neither scalar. For physical f0 and fc,

    rho_0=-rho, rho_c=3rho
    v_s,0=-2v_s-(a m_s)^2 phi_s/H
    d0,0=3[Wq_ext,N+2v_s v_s,0-rho]
    epsilon_0=epsilon[-1-d0,0/d0]
    epsilon_c=3epsilon(1-epsilon).

Thus d_0=-epsilon_0 c, d_c=-epsilon_c c and d_theta=2epsilon s. The constant Fourier coefficient is exactly1; both its slow derivatives are exactly0. No subtraction of nearly equal constant coefficients is needed.

The external quadrature derivative follows from its retained particle laws:

    rho_c,b,N=-rho_c,b
    rho_gamma,nu0,N=-2rho_gamma,nu0
    rho_node,N=-(1+v_node^2)rho_node.

No new thermal history or fit is introduced. The baseline has rho=0, epsilon=0 and no heavy-phase denominator. Its physical total denominator is still checked against the native source.

## 4. Propagating the saved uncertainty tube
Use energy coordinates U=a m_s phi_s, V=v_s and rho, with the prior uniform bounds on the saved cold interval:

    ||delta(U,V)||_2 <= r_s
    |delta rho| <= e_rho.

The old analytic growth/positivity bounds give a box containing both the mean path and its uncertainty tube, not just sampled points. For fixed N and phase, the external thermal background is unchanged by these scalar errors.
Use H=sqrt[(R_ext+(U^2+V^2)/2+rho)/3], the positive retained thermal quadrature and exact five-node dilution/speed laws. The conformal-clock uncertainty does not enter these instantaneous metric columns; it must still enter the future free-streaming/closure bound.

Forward interval automatic differentiation at50 decimal digits encloses every partial derivative with respect to U,V,rho, for every N in the cold window and every phase. Taking c,s independently in[-1,1] enlarges the domain safely. Squaring an interval uses its square operation, not an uncorrelated product; divisions require a positive interval distance from zero.

For any matrix-valued source F,

    |delta F_ij| <= sup|F_ij,U| r_s + sup|F_ij,V| r_s + sup|F_ij,rho| e_rho.

The resulting entrywise matrix and its Frobenius norm bound the full background replacement of the selected coefficients. This is a mean-value theorem on the containing convex box, not a finite-difference estimate or sampled maximum.

Apply it to L_h, the physical readout L_h/h with h=sqrt(rho)H/k, and B=V_map L_h. For M=I-B and an interval upper bound b<1 applying to both backgrounds,

    ||delta M^-1|| <= ||delta B||/(1-b)^2.

The same interval calculation supplies H,alpha,mu,h,d_phys and epsilon sensitivity bounds. All elementary bound arithmetic is outward rounded; conversion to stored float bounds rounds upward.

## 5. Source and scope of the enclosure
These enclosures concern the parent's retained finite thermal quadrature and saved scalar uncertainty tube. They do not independently prove the parent's thermal continuum integration or global ODE rounding error. Native source representation differences are separately tested by the unchanged gates, not silently relabelled as interval theorems.

L_h is a set of columns of the FULL coupled system; the other perturbations are not set to zero in an evolution. Their external columns, the free generator, source derivatives and physical endpoint maps must still be included to obtain a complete transport budget. The new full-row momentum identity makes those next calculations simpler and exposes the shared baryon approximation explicitly.

Units: L_h is dimensionless for dimensionless(delta,W); L_h/h has units Mpc when h is in Mpc^-1. Closure/inverse differences are dimensionless. None of these coefficient norms is a fractional observable discrepancy.

Independent70-digit evaluations use the original unsimplified scalar pressure/current equations and original forcing-matrix construction. Bounds are frozen before288 tube fixtures; these checks test implementation, while the analytic interval derivative calculation supplies the uniform enclosure.
