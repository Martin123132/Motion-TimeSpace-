# Full cold metric source and physical endpoint maps

This extends the retained relative-phase perturbation equations; it does not replace the MTS parent action or initialize a new late mode. The native equations, saved histories, grids and tolerances are unchanged. `../mts-cold-metric-tube-20261108/DERIVATION.md` gives the preceding full momentum identity and normalized denominator jets.

## 1. All matter columns, not an isolated heavy oscillator

Write N=ln(a), H for the conformal Hubble rate, and k for the retained comoving wave number, all dimensional rates in Mpc^-1. The saved slow coordinates are U=a m_s phi_s, V=v_s. The heavy rescaled density is rho. At fixed N,

    H^2=[R_ext+(U^2+V^2)/2+rho]/3.

Let D,Q,S,P_b denote full density, current, shear and baryon-pressure rows acting on the current physical/relative state. Set c=cos(2theta), s=sin(2theta), alpha=k^2/(a m_h H), Omega_s=sqrt(k^2+(a m_s)^2). The executable column ledger is `full_metric_math.py:rows`. Its nonzero entries include:

    D_c=sqrt(rho_c) k/H, D_b=sqrt(rho_b) k/H
    Q_vb=sqrt(rho_b)
    (D_gamma0,P_gamma0,Q_gamma1,S_gamma2)
      =(2sqrt(rho_gamma),2sqrt(rho_gamma)/3,
        2sqrt(rho_gamma)/sqrt(3),2sqrt(rho_gamma)/sqrt(5))
    D_node0=2sqrt(rho_node)/sqrt(v_node^2+4H^2/k^2)
    P_node0=v_node^2 D_node0/3
    Q_node1=2sqrt(rho_node)/sqrt(3)
    S_node2=2sqrt(rho_node) v_node/sqrt(5)
    D_s=(a m_s U/Omega_s,V)
    P_s=(-a m_s U/Omega_s,V), Q_s=(k V/Omega_s,0)
    D_h=rho(1,0), P_h=rho(-c,2s/alpha)
    Q_h=rho H/k(-alpha s/2,1-c).

The massless-neutrino rows follow the photon form; its retained UFA normalization uses sqrt(2) rather than sqrt(5) if that source option is active. No hierarchy modes are removed in the actual native comparison. Higher multipoles have zero *instantaneous metric readout* columns, not zero dynamics.

Define Wq as the retained metric enthalpy quadrature and Delta=Wq-W_true. Neither scalar contributes to this quadrature defect. Retain the tiny cold/radiation normalization difference between stored native origins and the saved thermal coefficients as well as the massive-neutrino quadrature difference. The gauge column e_alpha carries

    D_alpha=3H Delta/(sqrt(rho_c) k)
    Q_alpha=(rho_c-Delta)/sqrt(rho_c)
    P_b,alpha=3rho_b cs^2 H/(sqrt(rho_c) k),
    P_b,b=cs^2 sqrt(rho_b) k/H.

Here P excludes the baryon pressure only when forming D_free; P+P_b is the full pressure used by the native momentum equation. Thus

    D_free=-D-3P-kQ/H
      +e_alpha[3H(eta Delta+Delta_N)/(sqrt(rho_c) k)
                -k Delta/(sqrt(rho_c) H)]
    eta=1-W_true/(2H^2), d=2k^2+3Wq.

The previous exact cancellation gives the full GR readout

    Psi=-D/(2k^2)-3H Q/(2k^3)-S/k^2
    Phi_N=-Psi+(1-3Delta/d)(Q+Delta e_alpha/sqrt(rho_c))/(2kH)
            -3P_b/d.

The retained spatial-Poisson comparison is

    Psi_P=-D/(2k^2), Phi_P,N=-(D_free+3Delta Psi_P)/d.

The shared -3P_b/d term records the existing native baryon continuity approximation, rather than silently correcting it for one model. Independent verification also reconstructs the unsimplified density/current equation with the full pressure, shear and defect derivative before taking the GR combination.

## 2. Physical metric and coordinate maps

The heavy relative pair is weighted by h=sqrt(rho)H/k; all other columns already use the retained physical energy coordinates. Let D_weight be the diagonal matrix with heavy entries h and all others one. The physical readout is L_phys=L D_weight^-1. Every column now has units Mpc, so its Frobenius bound has a consistent meaning.

Use the retained micromotion T=I+P_micro, affine metric map V_map, and heavy selector J. The self-consistent coordinate closure is M=I-V_map L_h. The physical forward and inverse maps differ from identity only in two heavy rows:

    (S_phys-I)_h = M^-1[P_micro J+h V_map L_phys]
    (R_phys-I)_h = (T^-1-I)J-T^-1 h V_map L_phys.

Derivation: solve the same implicit relation y_h=T z_h+V_map L y with all external columns retained. Then multiply the input and output heavy coordinates by the same h. This is not a fitted boundary correction. The independent check solves that original relation directly, rather than differentiating the implemented reduced formula.

Baseline has no heavy pair: these two coordinate corrections vanish exactly. It still has its own full matter metric source, tested at the same three saved epochs and wavelengths.

## 3. Thermal coefficients from the retained source

The read-only getters in `build-thermal-readout/camb_python.f90` export the already constructed native table. They change no numerical evolution object. The isolated DLL reuses the parent scalar and equations objects; its numerical readback is checked against the sealed parent operators.

The source table has uniform log-conformal-time spacing. Its scale entry is a/tau, not a. Within a cell with coordinate t in [0,1], a tabulated value and its slopes define

    p(t)=p0+t[m0+t(3(p1-p0)-2m0-m1+t(m0+m1+2(p0-p1)))]
    B=(p0,p0+m0/3,p1-m1/3,p1).

These are exactly equal power-basis and Bernstein polynomials. The Bernstein convex hull encloses the entire cell, with outward interval arithmetic; no sampled maximum is used to establish the enclosure. Multiply the scale polynomial by tau. Positivity of tau[p+p_t/Delta_ln_tau] certifies scale monotonicity in every selected cold cell. The existing native adapter inverts this fixed thermal table by physical a; the saved conformal clock is only an inversion seed for this readout.

All source cells are considered, and all whose interval scale range overlaps the cold interval are retained. The resulting cs^2 and opacity ranges come from the actual source polynomial. Only cs^2 enters the metric envelope in this stage. Opacity is recorded for later free-generator work, not treated as an already completed transport calculation.

## 4. Whole-window background replacement bound

Keep the inherited scalar tube and finite positive thermal quadrature. At every N in the saved cold window, both the mean and allowed background lie inside the analytic box. For any physical metric or map entry F,

    |delta F_ij| <= sup_box |partial_U F_ij| e_s
                  +sup_box |partial_V F_ij| e_s
                  +sup_box |partial_rho F_ij| e_rho.

Forward automatic differentiation with 50-digit outward interval arithmetic encloses these derivatives on the entire box and c,s independently in [-1,1]. The entrywise bounds imply a Frobenius/operator bound. The convex box and positive denominators justify the mean-value step. The phase variables are not fitted, and sampled phase checks do not stand in for the enclosure.

The massive exterior enthalpy derivative is retained analytically:

    rho_node,N=-(1+v_node^2)rho_node
    W_massive,N=-sum rho_physical[1+2v^2-v^4/3]
    delta_c=[(rho_c,0+rho_b,0)a0-(C_c+C_b)]/a
    delta_r=[(rho_gamma,0+rho_nu0,0)a0^2-(C_gamma+C_nu0)]/a^2
    Delta=delta_c+(4/3)delta_r+(4/3)sum rho_node-W_massive
    Delta_N=-delta_c-(8/3)delta_r
            -(4/3)sum rho_node(1+v_node^2)-W_massive,N.

Here a0 and rho_species,0 are retained native normalization inputs; C_species are the saved thermal density coefficients. The finite positive Fermi source and native five-node perturbation source remain distinct. Their complete difference is carried through Delta, not set to zero. `full_envelope_v2.py` is authoritative. The original enclosure and failed validator are preserved: the high-precision comparison exposed a roughly1.2851e-24 normalization defect at the first heavy state, even though its metric effect was far below the original gate. Restoring this algebraic input resolves the identity without changing any gate or source trajectory.

## 5. Meaning and next connection

These are whole-window *instantaneous metric and coordinate-map sensitivity* bounds conditional on the retained source and inherited scalar tube. They do not include the thermal continuum quadrature error, global floating-point ODE error, free-generator/source-jet error, or conformal-clock hierarchy closure error. A zero baseline replacement radius means no heavy-phase averaging replacement in that control; it is not zero numerical or cosmological uncertainty. Tiny baseline JSON values near1e-322 are outward-rounding floors on that exact zero.

The next constructive step is to carry the same source-owned thermal bounds and clock tube through the free generator and slow source derivatives, then use the useful physical logarithmic norm to transport the original early preparation. Keep both endpoint maps and physical readouts; do not reset a late initial mode or exponentiate a large phase-Fourier coefficient norm.
