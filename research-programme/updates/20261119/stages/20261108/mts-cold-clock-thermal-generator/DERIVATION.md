# Retained free evolution, thermal derivatives and clock coupling

This continues the saved cold relative-phase branch. It uses the same action-derived scalar sector, native matter equations, finite G192 hierarchy, thermal history and initial preparation as the preceding checkpoints. N=ln(a), H is the conformal Hubble rate in Mpc^-1, k is the comoving wave number and tau is the physical conformal clock in Mpc. The thermal table time is a different interpolation coordinate; the two clocks must not be identified by assumption.

The local source is written before the periodic coordinate maps as

    u_N = G_free u + F (Psi,Phi_N),  (Psi,Phi_N)=L_phys u.

`free_math_v2.py:build` gives every retained free row and metric injection in physical coordinates. Groups are drift, streaming, collision, baryon pressure, clock closure and heavy relative pair. Splitting these terms avoids interpreting rapid skew streaming or dissipative collisions as positive growth.

## 1. Dust, baryon and canonical scalar rows

With eta=H_N/H, the weighted CDM gauge variable obeys

    u_alpha,N = -3u_alpha/2 + sqrt(rho_c) k Psi/H.

The weighted CDM and baryon density rows have diagonal eta-1/2, off-diagonal -1 to their velocity variable, and force 3sqrt(rho_c,b)H Phi_N/k. The baryon velocity diagonal is -3/2. Its pressure entries are

    G_vb,b = cs^2 k^2/H^2
    G_vb,alpha = 3cs^2 sqrt(rho_b/rho_c).

The latter is retained because the native pressure source is cs^2 times the synchronous baryon density. Omitting it while keeping that source would change the implementation. The previous full metric identity retains the matching shared baryon approximation.

For slow-scalar physical coordinates (Omega_s delta_phi_s,delta_v_s), Omega_s^2=k^2+(a m_s)^2,

    G_s = [[(a m_s)^2/Omega_s^2, Omega_s/H],[-Omega_s/H,-2]]
    F_Psi,s = [Omega_s v_s/H, -(a m_s)U/H]
    F_PhiN,s = [0,3v_s], U=a m_s phi_s.

The heavy relative pair uses the already derived canonical equations, not a pressureless substitution. Let c=cos(2theta), s=sin(2theta), alpha=k^2/(a m_h H), b=rho/(2H^2), eta=eta0+b c, h=sqrt(rho)H/k and gamma=eta0-1/2+(3/2+b)c. In the physical heavy coordinates h(delta,W),

    G_h = [[alpha s/2+gamma, -1+c-6s/alpha],
           [alpha^2(1+c)/4, -1-eta-3c-alpha s/2+gamma]]
    F_Psi,h = h[0,k^2/H^2]
    F_PhiN,h = h[3(1-c),3alpha s/2].

The gamma term is the derivative of the changing physical weight. It is not optional.

## 2. Radiation streaming and the source-owned UFA branch

The retained angular weights make adjacent radiation streaming entries opposite transposes. Interior intensity weights are2ell+1; the native final-row closure requires weight ell_max rather than2ell_max+1. Polarization weights are

    w_ell=(2ell+1)(ell+1)(ell+2)/(ell(ell-1)),

with the separately retained terminal weight that balances its source truncation coefficient. Their native lower/upper coefficients satisfy the exact weighted skew relation. The generic logarithmic weight drift is -1; it is separate from streaming.

The half-k family keeps the full massless hierarchy. The balanced/double families ALREADY use the retained ultra-relativistic-fluid approximation (UFA), so the same branch must be derived, not switched off. Its native equation is

    pi_r'=-3pi_r/tau-delta_r,sync'.

Transforming its density and dipole to the existing physical frame gives, with w2=sqrt(rho_r/2),

    u_2,N = [-1-3/(H tau)]u_2 + sqrt(2/3) k u_1/H
            -4w2 H(eta-1)u_alpha/[sqrt(rho_c)k]
            -4w2(Psi+Phi_N).

Thus UFA changes both the free gauge entry and the metric injection. The weight2 for its quadrupole preserves the corresponding skew dipole/quadrupole streaming. This is an imported retained approximation, not a newly derived MTS closure. The initial collector stopped on this source option; the exact rejected attempt is preserved. The v2 implementation derives and checks it without changing the model.

For massive-neutrino nodes use v=(1+a^2m^2/q^2)^-1/2 and w=sqrt(v^2+4H^2/k^2). The special first streaming pair is

    G_01=-w k/(sqrt(3)H), G_10=v^2 k/(sqrt(3)H w),

with symmetric part -2H/(sqrt(3)k w). The monopole drift is -(1+v^2)/2+w_N/w, where

    w_N/w=[-v^2(1-v^2)+4(H/k)^2 eta]/w^2.

All higher weighted moments have drift -(3-v^2)/2 and skew streaming. The existing G192 extension sets the last upper coupling to zero; it does NOT use the native low-order massive closure -3/tau. Both the interval source and full-vector test retain all190 tail levels and five momentum nodes. No higher moment is declared zero in the evolution.

## 3. Thomson collisions cannot create physical-norm growth

Let chi=opacity/H>=0 and r=4rho_gamma/(3rho_b)>0. The baryon/photon-dipole collision block is

    C_v=chi[[-r,sqrt(r)],[sqrt(r),-1]]
       =-chi [sqrt(r),-1]^T [sqrt(r),-1].

For photon and polarization quadrupoles,

    C_2=chi[[-9/10,sqrt(6)/10],[sqrt(6)/10,-2/5]].

Its eigenvalues are -chi and -3chi/10. All remaining collision-affected moments have -chi on their diagonal. Therefore C is symmetric negative semidefinite in the retained physical norm. This is an exact property of the source coupling, not a favorable numerical sample. It does not make the entire coupled matter/gravity generator dissipative, and it does not certify a conserved GR Hamiltonian.

## 4. Physical clock closure, with its saved uncertainty retained

The full photon, polarization and massless-neutrino terminal damping terms are -c_ell/(H tau), with c_ell=ell_max+1 or ell_max+3. UFA uses c_ell=3. The extended massive G192 tail has the different retained boundary described above.

At fixed slow state,

    partial_tau G_clock = C_diag/(H tau^2)
    (1/(H tau))_N = -eta/(H tau)-1/(H^2 tau^2).

The saved clock obeys tau_N=1/H>0. Its comparison radius obeys the positive equation in `../mts-cold-background-extension-20261107/extend.py:make_rhs`. Hence cold endpoint clocks, enlarged by the final accumulated radius, enclose the window. The retained heavy radius is0.017485713632227135 Mpc; no clock is reset or reconstructed from an unrelated thermal table. Endpoint reliability remains conditional on the previously qualified ODE arithmetic.

The periodic physical maps and metric readout depend on scale, slow scalars and phase, not on this physical clock. Consequently the clock-only change of the closed generator is exactly

    delta A_closed = R_phys (delta G_clock) S_phys

at those fixed variables: F,L_phys and the map derivative have no independent tau entry. This identifies how the current clock bound enters the previous coordinate-map theorem; its final combined bound must still be assembled with the other background/source channels.

## 5. Derive thermal jets from the actual interpolation law

The saved table is uniform in log(table_time). In a cell let t be its local coordinate, h_t its log-time spacing, P(t)=a/table_time and Q(t) either cs^2 or opacity. Both are source-owned cubic Hermite polynomials. Then

    N(t)=ln(table_time_0)+(cell+t)h_t+ln P(t)
    D=h_t P+P_t
    Q_N=P Q_t/D
    Q_NN=P[(P_t Q_t+P Q_tt)D-P Q_t(h_t P_t+P_tt)]/D^3.

No physical-H factor is inserted into this change of variable. Using Q_table_time/H instead would confuse the retained thermal background with the actual physical clock. Bernstein convex hulls enclose P,Q and their derivatives on every relevant cell; positive D makes the scale inverse regular. The second derivative is one-sided at a cell join, not assumed globally continuous.

These coefficients immediately give

    (opacity/H)_N=(opacity_N-eta opacity)/H
    (cs^2 k^2/H^2)_N=(cs^2_N-2eta cs^2)k^2/H^2.

They provide exact source jets for replacing numerical thermal differences in the next coupled coefficient calculation. The thermal history itself is the retained imported source, not a newly predicted MTS recombination history.

## 6. Full retained source sensitivity

Four-variable outward interval differentiation uses (U,V,rho,tau) and the inherited scalar/clock radii. Every N in the cold window and all c,s in[-1,1] are covered. The enclosing state box is convex and denominators stay positive. For each nonzero coefficient,

    |delta G_ij| <= sum_a sup_box |partial_a G_ij| e_a,

and similarly for F. Sparse entry bounds imply both the Frobenius bound and sqrt(norm_one*norm_infinity), whose minimum bounds the operator norm. The finite retained k and source coefficients are fixed inputs; native floating-point/source representation and thermal continuum errors remain separate from this background-replacement theorem.

The resulting source bound is deliberately not exponentiated as a growth rate. Large streaming can be skew; collision terms damp; heavy micromotion must be averaged using the preceding derivation. Next combine the metric, map and free-source envelopes, and carry exact thermal/denominator jets through the closed-map derivative before transporting the original early preparation. This is the remaining calculation, not a reason to introduce a new late initial mode.
